import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

# 导入项目中自己编写的工业级模块
from utils.data_processor import DataProcessor
from utils.data_loader import AdvancedInteractionSampler, get_advanced_loader
from models.ncf_advanced import AdvancedNCFModel
from utils.metrics import Evaluator


def main():
    # ================= 1. 工程全局配置 =================
    # 使用你本地的真实 CSV 路径
    interaction_path = 'data/Appliances_sampled.csv'
    meta_path = 'data/meta_Appliances.csv'

    epochs = 10
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

    # ================= 4. 初始化文本增强型双塔模型 =================
    print("\n🧠 初始化 Advanced-NCF 增强型神经网络...")
    model = AdvancedNCFModel(num_users=num_users, num_items=num_items, text_dim=50)
    model.to(device)

    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=1e-5)

    # ================= 5. 模型训练循环 =================
    print("\n🔥 开始模型训练与参数寻优...")
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

    # 保存模型，方便后续前端读取
    torch.save(model.state_dict(), 'advanced_ncf.pth')
    print("💾 模型训练完毕，权重已持久化保存至 advanced_ncf.pth")

    # ================= 6. 工业级极速离线评估 (100样本打分制) =================
    print(f"\n🎯 启动极速离线评估 (1正样本 + 99负样本打分制, Top-{k})...")
    model.eval()
    evaluator = Evaluator(sampler.train_df, k=k)

    test_user_groups = sampler.test_df.groupby('user_id_encoded')['item_id_encoded'].apply(list).reset_index()
    user_metrics_dict = {}

    import random  # 确保顶部导入了 random

    for _, row in test_user_groups.iterrows():
        user = row['user_id_encoded']
        true_items = row['item_id_encoded']

        # 只取测试集里最新的一次交互作为“目标正样本”
        target_item = true_items[-1]

        # 找出用户在训练集里买过的东西
        interacted = {item for (u, item) in sampler.train_user_item_set if u == user}
        interacted.add(target_item)  # 把目标样本也加进去，防止负采样抽到

        # 随机抽取 99 个负样本
        negative_items = set()
        while len(negative_items) < 99:
            j = random.randint(0, num_items - 1)
            if j not in interacted:
                negative_items.add(j)

        # 候选集 = 1个真实样本 + 99个负样本
        candidates = [target_item] + list(negative_items)

        # 推断
        u_tensor = torch.full((len(candidates),), user, dtype=torch.long).to(device)
        i_tensor = torch.tensor(candidates, dtype=torch.long).to(device)
        t_tensor = torch.tensor(np.array([sampler.item2vec.get(item, np.zeros(50)) for item in candidates]),
                                dtype=torch.float32).to(device)

        with torch.no_grad():
            predictions = model(u_tensor, i_tensor, t_tensor).view(-1)

        # 提取 Top-K
        _, top_indices = torch.topk(predictions, k=min(k, len(predictions)))
        recommended_items = [candidates[idx] for idx in top_indices.cpu().numpy()]

        # 计算指标 (真实集就这1个 target_item)
        user_metrics_dict[user] = evaluator.calculate_metrics([target_item], recommended_items)

    overall, active, cold = evaluator.evaluate_groups(user_metrics_dict)

    print("\n" + "=" * 50)
    print(" 📊 实验结果分析评估报告 (极速版)")
    print("=" * 50)
    print(
        f"【整体表现】 Precision@{k}: {overall[0]:.4f} | Recall@{k}: {overall[1]:.4f} | F1: {overall[2]:.4f} | NDCG: {overall[3]:.4f}")
    print("=" * 50)


if __name__ == "__main__":
    main()