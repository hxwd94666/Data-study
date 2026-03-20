import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np
from sklearn.model_selection import train_test_split
#根据总样本数量，负样本数量减少

class AdvancedInteractionSampler:
    """
    高级负采样与数据划分模块
    支持将商品的文本特征 (TF-IDF Vector) 同步对齐并输入模型
    """

    def __init__(self, df_interact, df_meta, num_items, num_negatives=4, test_size=0.2):
        self.df_interact = df_interact
        self.num_items = num_items
        self.num_negatives = num_negatives

        # 构建商品 ID 到 文本向量 的快速映射字典
        # 这样在负采样时，不仅能取到随机的假商品，还能取到假商品对应的文本特征
        self.item2vec = dict(zip(df_meta['item_id_encoded'], df_meta['title_vector']))

        # 划分训练集与测试集
        self.train_df, self.test_df = train_test_split(
            self.df_interact, test_size=test_size, random_state=42
        )
        self.train_user_item_set = set(zip(self.train_df['user_id_encoded'], self.train_df['item_id_encoded']))

    def generate_training_data(self):
        print(f"🔄 正在生成包含【文本特征】的训练样本 (正负比例 1:{self.num_negatives})...")
        user_input, item_input, text_input, labels = [], [], [], []

        for row in self.train_df.itertuples():
            u, i = row.user_id_encoded, row.item_id_encoded

            # 正样本
            user_input.append(u)
            item_input.append(i)
            text_input.append(self.item2vec.get(i, np.zeros(50)))  # 50 是 TF-IDF 的维度
            labels.append(1.0)

            # 负样本
            for _ in range(self.num_negatives):
                j = np.random.randint(self.num_items)
                while (u, j) in self.train_user_item_set:
                    j = np.random.randint(self.num_items)

                user_input.append(u)
                item_input.append(j)
                text_input.append(self.item2vec.get(j, np.zeros(50)))
                labels.append(0.0)

        print(f"✅ 高级训练集构造完毕！总样本数: {len(labels)}")
        return user_input, item_input, text_input, labels


class AdvancedNCFDataset(Dataset):
    def __init__(self, users, items, texts, labels):
        self.users = torch.tensor(users, dtype=torch.long)
        self.items = torch.tensor(items, dtype=torch.long)
        self.texts = torch.tensor(np.array(texts), dtype=torch.float32)  # 文本特征是浮点数
        self.labels = torch.tensor(labels, dtype=torch.float32)

    def __getitem__(self, idx):
        return self.users[idx], self.items[idx], self.texts[idx], self.labels[idx]

    def __len__(self):
        return len(self.users)


def get_advanced_loader(users, items, texts, labels, batch_size=256):
    dataset = AdvancedNCFDataset(users, items, texts, labels)
    return DataLoader(dataset, batch_size=batch_size, shuffle=True)