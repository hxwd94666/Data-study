import torch
import torch.nn as nn

#需要增加多个推荐模型
class AdvancedNCFModel(nn.Module):
    """
    融合文本语义特征的增强版神经协同过滤模型
    (Text-Enhanced Neural Collaborative Filtering)
    解决冷启动问题：即使商品没有被交互过，模型依然可以通过提取它的 title_vector 预测用户偏好。
    """

    def __init__(self, num_users, num_items, text_dim=50, mf_dim=16, layers=[64, 32, 16], dropout=0.2):
        super(AdvancedNCFModel, self).__init__()

        # 1. 广义矩阵分解塔 (GMF Layer) - 捕捉协同过滤的线性关系
        self.emb_user_mf = nn.Embedding(num_users, mf_dim)
        self.emb_item_mf = nn.Embedding(num_items, mf_dim)

        # 2. 多层感知机塔 (MLP Layer) - 捕捉非线性高阶关系
        mlp_dim = layers[0] // 2
        self.emb_user_mlp = nn.Embedding(num_users, mlp_dim)
        self.emb_item_mlp = nn.Embedding(num_items, mlp_dim)

        # 💡 创新点：文本特征降维层 (将 50 维的 TF-IDF 向量压缩映射，提取语义信息)
        self.text_dense_layer = nn.Sequential(
            nn.Linear(text_dim, 16),
            nn.ReLU(),
            nn.Dropout(dropout)
        )

        # 💡 创新点：MLP 现在的输入不仅是 user 和 item 的 Embedding，还要拼接上 text 的特征！
        # 输入维度 = 用户MLP维度 + 商品MLP维度 + 文本压缩后维度(16)
        mlp_input_dim = mlp_dim * 2 + 16

        # 构建深层网络
        mlp_modules = []
        mlp_modules.append(nn.Linear(mlp_input_dim, layers[1]))
        mlp_modules.append(nn.ReLU())
        mlp_modules.append(nn.Dropout(dropout))

        mlp_modules.append(nn.Linear(layers[1], layers[2]))
        mlp_modules.append(nn.ReLU())
        mlp_modules.append(nn.Dropout(dropout))

        self.mlp_network = nn.Sequential(*mlp_modules)

        # 3. 预测输出层
        self.prediction_layer = nn.Linear(mf_dim + layers[-1], 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, u, i, text_features):
        # --- 左塔：GMF ---
        mf_vec = torch.mul(self.emb_user_mf(u), self.emb_item_mf(i))

        # --- 右塔：MLP (融合文本特征) ---
        user_mlp = self.emb_user_mlp(u)
        item_mlp = self.emb_item_mlp(i)

        # 压缩文本向量
        text_vec = self.text_dense_layer(text_features)

        # 三重拼接：[用户画像, 商品画像, 商品文本语义]
        mlp_vec = torch.cat([user_mlp, item_mlp, text_vec], dim=-1)
        mlp_vec = self.mlp_network(mlp_vec)

        # --- 最终融合预测 ---
        predict_vec = torch.cat([mf_vec, mlp_vec], dim=-1)
        return self.sigmoid(self.prediction_layer(predict_vec)).squeeze()