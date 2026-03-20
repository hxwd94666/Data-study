import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import warnings

warnings.filterwarnings('ignore')
#待优化
#tf提取字段数量增加
#商品特征归类

class DataProcessor:
    """
    核心数据预处理与特征工程管道
    负责CSV数据清洗、缺失值插补、以及文本特征的TF-IDF向量化
    """

    def __init__(self, interaction_path, meta_path):
        self.interaction_path = interaction_path
        self.meta_path = meta_path

    def process_data(self):
        print("[1/4] 正在加载交互数据与商品元数据 (CSV格式)...")
        df_interact = pd.read_csv(self.interaction_path)
        df_meta = pd.read_csv(self.meta_path)

        # --- 1. 交互数据清洗 ---
        print("[2/4] 执行交互数据去重与隐式反馈构建...")
        df_interact = df_interact[['user_id', 'parent_asin', 'rating', 'timestamp']].copy()
        df_interact.rename(columns={'parent_asin': 'item_id'}, inplace=True)

        df_interact.dropna(subset=['user_id', 'item_id'], inplace=True)
        df_interact.sort_values(by=['user_id', 'item_id', 'timestamp'], inplace=True)
        df_interact.drop_duplicates(subset=['user_id', 'item_id'], keep='last', inplace=True)
        df_interact['label'] = 1

        df_interact['user_id_encoded'] = df_interact['user_id'].astype('category').cat.codes
        df_interact['item_id_encoded'] = df_interact['item_id'].astype('category').cat.codes

        item_id_mapping = dict(zip(df_interact['item_id'], df_interact['item_id_encoded']))

        # --- 2. 元数据清洗与缺失值插补 ---
        print("🛠️ [3/4] 修复元数据缺失值 (Price, Category, Title) 并同步ID编码...")
        df_meta.rename(columns={'parent_asin': 'item_id'}, inplace=True)
        df_meta.drop_duplicates(subset=['item_id'], keep='last', inplace=True)

        df_meta['item_id_encoded'] = df_meta['item_id'].map(item_id_mapping)
        df_meta.dropna(subset=['item_id_encoded'], inplace=True)
        df_meta['item_id_encoded'] = df_meta['item_id_encoded'].astype(int)

        if 'price' in df_meta.columns:
            median_price = df_meta['price'].median()
            df_meta['price'] = df_meta['price'].fillna(median_price)

        df_meta['main_category'] = df_meta['main_category'].fillna('Unknown Category')
        df_meta['title'] = df_meta['title'].fillna('No Title')

        # --- 3. 文本特征提取与容错处理 ---
        print("[4/4] 提取商品标题的 TF-IDF 文本特征向量...")
        try:
            tfidf = TfidfVectorizer(max_features=50, stop_words='english')
            tfidf_matrix = tfidf.fit_transform(df_meta['title']).toarray()

            #动态维度补齐 (Padding)
            # 因为只有100行数据，提取的词可能不到50个，为满足神经网络输入要求，不足部分补 0
            if tfidf_matrix.shape[1] < 50:
                padded_matrix = np.zeros((tfidf_matrix.shape[0], 50))
                padded_matrix[:, :tfidf_matrix.shape[1]] = tfidf_matrix
                tfidf_matrix = padded_matrix

            df_meta['title_vector'] = list(tfidf_matrix)
        except ValueError:
            #应对极小数据集时的“空词表”崩溃
            print("⚠️ 警告：当前数据子集有效文本过少，启用全零占位特征...")
            df_meta['title_vector'] = [np.zeros(50) for _ in range(len(df_meta))]

        print("✅ 数据管道处理完毕！可以输出给模型和可视化模块使用了。")
        return df_interact, df_meta


if __name__ == "__main__":
    processor = DataProcessor('../data/Appliances.csv', '../data/meta_Appliances.csv')
    interactions, meta = processor.process_data()
    print("\n--- 修复后的商品元数据预览 (包含 title_vector) ---")
    print(meta[['item_id', 'item_id_encoded', 'title_vector']].head(2))