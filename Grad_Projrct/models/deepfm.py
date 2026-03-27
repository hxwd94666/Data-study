import torch
import torch.nn as nn


class DeepFM(nn.Module):
    """
    工业界标杆模型：DeepFM (Deep Factorization Machine)
    作为论文的 Baseline 2：不仅融合了文本特征，还能显式地进行特征交叉。
    用来在论文第五章证明：复杂的特征交叉（FM）+ 深度非线性学习（Deep）的威力。
    """

    def __init__(self, num_users, num_items, text_dim=50, embed_dim=32, mlp_dims=[64, 32]):
        super(DeepFM, self).__init__()

        # ================= 1. 共享 Embedding 层 =================
        # 用户和商品的 ID 映射为稠密向量
        self.user_embedding = nn.Embedding(num_users, embed_dim)
        self.item_embedding = nn.Embedding(num_items, embed_dim)
        # 将 50 维的文本 TF-IDF 向量降维到与 ID 相同的维度，作为“第3个特征域(Field)”
        self.text_embedding = nn.Linear(text_dim, embed_dim)

        # ================= 2. FM 线性部分 (一阶特征 1st-order) =================
        self.user_linear = nn.Embedding(num_users, 1)
        self.item_linear = nn.Embedding(num_items, 1)
        self.text_linear = nn.Linear(text_dim, 1)
        self.fm_bias = nn.Parameter(torch.zeros(1))

        # ================= 3. Deep 深度部分 (高阶特征 High-order) =================
        # 输入维度是 3 个 Field 的向量拼接 (User + Item + Text)
        deep_input_dim = embed_dim * 3
        layers = []
        for dim in mlp_dims:
            layers.append(nn.Linear(deep_input_dim, dim))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(0.2))  # 防止过拟合
            deep_input_dim = dim
        layers.append(nn.Linear(deep_input_dim, 1))
        self.mlp = nn.Sequential(*layers)

        # 最终输出转概率
        self.sigmoid = nn.Sigmoid()

    def forward(self, u, i, text_features):
        # --- 获取共享特征表示 ---
        u_emb = self.user_embedding(u)  # [batch, embed_dim]
        i_emb = self.item_embedding(i)  # [batch, embed_dim]
        t_emb = self.text_embedding(text_features)  # [batch, embed_dim]

        # --- A. FM 的一阶线性组合 ---
        # 相当于给 User、Item、Text 各自一个基础权重分数
        u_lin = self.user_linear(u).squeeze(-1)
        i_lin = self.item_linear(i).squeeze(-1)
        t_lin = self.text_linear(text_features).squeeze(-1)
        fm_1st = u_lin + i_lin + t_lin + self.fm_bias

        # --- B. FM 的二阶特征交叉 (核心数学技巧：Sum-square minus Square-sum) ---
        # 这里模拟了 User与Item、User与Text、Item与Text 两两特征之间的化学反应
        stacked_emb = torch.stack([u_emb, i_emb, t_emb], dim=1)  # 维度: [batch, 3, embed_dim]
        sum_of_square = torch.sum(stacked_emb ** 2, dim=1)
        square_of_sum = torch.sum(stacked_emb, dim=1) ** 2
        fm_2nd = 0.5 * torch.sum(square_of_sum - sum_of_square, dim=-1)  # [batch]

        # --- C. Deep 层的非线性高阶交叉 ---
        deep_input = torch.cat([u_emb, i_emb, t_emb], dim=-1)  # 维度: [batch, embed_dim * 3]
        deep_out = self.mlp(deep_input).squeeze(-1)

        # --- D. 融合输出 ---
        # 将 FM 一阶、FM 二阶 和 Deep 高阶结果相加
        out = fm_1st + fm_2nd + deep_out
        return self.sigmoid(out)