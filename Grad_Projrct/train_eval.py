import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random  # 移到顶部统一导入

# 导入项目中自己编写的工业级模块
from utils.data_processor import DataProcessor
from utils.data_loader import AdvancedInteractionSampler, get_advanced_loader
from models.ncf_advanced import AdvancedNCFModel
from models.bpr_mf import MatrixFactorization
from models.deepfm import DeepFM
from utils.metrics import Evaluator


def main():
    # ================= 1. 工程全局配置 =================
    interaction_path = 'data/Appliances_sampled.csv'
    meta_path = 'data/meta_Appliances.csv'

    epochs = 50
    batch_size = 4096
    lr = 0.001
    k = 5  # 计算 Top-5 推荐

    device = torch.device(
        "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")
    print(f"⚡ 启动计算引擎，当前设备: {device}")

    # ================= 2. 数据处理与文本特征提取 =================
    processor = DataProcessor(interaction_path, meta_path)
    df_interact, df_meta = processor.process_data()

    num_users = df_interact['user_id_encoded'].nunique()
    num_items = df_interact['item_id_encoded'].nunique()

    # ================= 3. 高级数据加载与负采样 =================
    sampler = AdvancedInteractionSampler(df_interact, df_meta, num_items, num_negatives=4)
    u_in, i_in, t_in, labels = sampler.generate_training_data()
    train_loader = get_advanced_loader(u_in, i_in, t_in, labels, batch_size=batch_size)

    # 准备阅卷老师（在循环外初始化一次即可）
    evaluator = Evaluator(sampler.train_df, k=k)
    test_user_groups = sampler.test_df.groupby('user_id_encoded')['item_id_encoded'].apply(list).reset_index()

    # ================= 4. 构建自动化模型流水线 =================
    # 将要打擂台的模型装进字典，排队执行
    model_pipeline = {
        "Baseline_MF": MatrixFactorization(num_users=num_users, num_items=num_items, embed_dim=32),
        "Baseline_DeepFM": DeepFM(num_users=num_users, num_items=num_items, text_dim=50, embed_dim=32),
        "Ours_Advanced_NCF": AdvancedNCFModel(num_users=num_users, num_items=num_items, text_dim=50)
    }

    # 建立终极计分板
    scoreboard = {}

    # ================= 5. 开启排队串行训练与评估 =================
    for model_name, model in model_pipeline.items():
        print("\n" + "━" * 60)
        print(f"🚀 开始流水线任务: 【{model_name}】")
        print("━" * 60)

        # 挂载当前模型到显卡/CPU
        model = model.to(device)
        criterion = nn.BCELoss()
        optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=1e-5)

        # ---------------- A. 训练阶段 ----------------
        print(f"🔥 [{model_name}] 开始模型训练与参数寻优...")
        for epoch in range(epochs):
            model.train()
            total_loss = 0.0
            for u, i, t, y in train_loader:
                u, i, t, y = u.to(device), i.to(device), t.to(device), y.to(device)
                optimizer.zero_grad()
                preds = model(u, i, t)
                loss = criterion(preds, y)
                loss.backward()
                optimizer.step()
                total_loss += loss.item()
            print(f"▶ Epoch [{epoch + 1}/{epochs}] | BCE Loss: {total_loss / len(train_loader):.4f}")

        # 动态保存权重，避免相互覆盖
        save_path = f"{model_name.lower()}_weights.pth"
        torch.save(model.state_dict(), save_path)
        print(f"💾 权重已持久化保存至 {save_path}")

        # ---------------- B. 评估阶段 ----------------
        print(f"\n🎯 [{model_name}] 启动极速离线评估 (1+99打分制)...")
        model.eval()

        # ⚠️ 极度关键：每个模型必须用干净的字典记录自己的成绩
        user_metrics_dict = {}

        for _, row in test_user_groups.iterrows():
            user = row['user_id_encoded']
            true_items = row['item_id_encoded']
            target_item = true_items[-1]

            interacted = {item for (u, item) in sampler.train_user_item_set if u == user}
            interacted.add(target_item)

            negative_items = set()
            while len(negative_items) < 99:
                j = random.randint(0, num_items - 1)
                if j not in interacted:
                    negative_items.add(j)

            candidates = [target_item] + list(negative_items)

            u_tensor = torch.full((len(candidates),), user, dtype=torch.long).to(device)
            i_tensor = torch.tensor(candidates, dtype=torch.long).to(device)
            t_tensor = torch.tensor(np.array([sampler.item2vec.get(item, np.zeros(50)) for item in candidates]),
                                    dtype=torch.float32).to(device)

            with torch.no_grad():
                # 兼容不同模型的输出并展平
                predictions = model(u_tensor, i_tensor, t_tensor).view(-1)

            _, top_indices = torch.topk(predictions, k=min(k, len(predictions)))
            recommended_items = [candidates[idx] for idx in top_indices.cpu().numpy()]

            user_metrics_dict[user] = evaluator.calculate_metrics([target_item], recommended_items)

        # 结算当前模型的成绩
        overall, active, cold = evaluator.evaluate_groups(user_metrics_dict)
        scoreboard[model_name] = overall
        print(f"✅ [{model_name}] 评估完成！NDCG@{k}: {overall[3]:.4f}")

    # ================= 6. 输出全模型打擂台成绩单 =================
    print("\n\n" + "★" * 60)
    print(" 🏆 毕业设计核心实验：全模型对比成绩汇总报告")
    print("★" * 60)
    print(f"{'模型名称':<22} | {'Precision':<10} | {'Recall':<10} | {'F1-Score':<10} | {'NDCG':<10}")
    print("-" * 60)
    for name, metrics in scoreboard.items():
        print(f"{name:<25} | {metrics[0]:.4f}      | {metrics[1]:.4f}    | {metrics[2]:.4f}    | {metrics[3]:.4f}")
    print("★" * 60)


if __name__ == "__main__":
    main()