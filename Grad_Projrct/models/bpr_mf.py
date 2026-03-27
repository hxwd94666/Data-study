import torch
import torch.nn as nn


class MatrixFactorization(nn.Module):
    """
    经典矩阵分解模型 (Matrix Factorization)
    作为论文的 Baseline 1：仅利用 User 和 Item 的 ID 隐向量进行协同过滤。
    用来在论文第五章证明：缺乏文本多模态特征的传统模型，在面对冷启动时表现较差。
    """

    def __init__(self, num_users, num_items, embed_dim=32):
        super(MatrixFactorization, self).__init__()

        # 1. 构建隐向量空间 (Latent Factor Space)
        # 相当于给每个用户和商品发一张 32 维的“性格卡片”
        self.user_embedding = nn.Embedding(num_embeddings=num_users, embedding_dim=embed_dim)
        self.item_embedding = nn.Embedding(num_embeddings=num_items, embedding_dim=embed_dim)

        # 初始化权重，让模型一开始的“性格”是随机的，避免梯度消失
        nn.init.normal_(self.user_embedding.weight, std=0.01)
        nn.init.normal_(self.item_embedding.weight, std=0.01)

        # 输出激活函数
        self.sigmoid = nn.Sigmoid()

    def forward(self, u, i, text_features=None):
        """
        前向传播计算偏好得分
        💡 核心工程技巧：这里故意保留了 text_features 参数，并设为默认值 None。
        作用：为了完美兼容你的 train_eval.py！这样主干代码传文本特征进来时程序不会报错，
        但传统 MF 根本没有能力利用文本，它只能默默无视掉这个特征。
        """
        # 提取用户和商品对应的隐向量
        user_vec = self.user_embedding(u)
        item_vec = self.item_embedding(i)

        # 矩阵分解的核心数学操作：计算点积 (Dot Product)
        # 将用户向量和商品向量逐元素相乘后求和，得分越高说明“性格越匹配”
        dot_product = torch.sum(user_vec * item_vec, dim=-1)

        # 压缩到 0~1 的概率区间，输出预测值
        return self.sigmoid(dot_product)