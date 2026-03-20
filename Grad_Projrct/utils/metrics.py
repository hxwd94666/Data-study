import numpy as np
from math import log2
#缺少ab测试

class Evaluator:
    """
    推荐系统多维度评价指标与多群体分析评估器
    对标任务书要求：使用准确率、召回率、F1-score、NDCG 进行全面评估，并分析不同用户群体的差异。
    """

    def __init__(self, train_df, k=10):
        self.k = k
        # 统计每个用户在训练集中的交互次数，用于划分用户群体
        self.user_interaction_counts = train_df['user_id_encoded'].value_counts().to_dict()

        # 定义阈值：交互次数大于等于 5 次的视为“活跃用户”，否则视为“长尾/冷启动用户”
        self.active_threshold = 5

    def calculate_metrics(self, true_items, recommended_items):
        """
        计算单个用户的各项 Top-K 指标
        """
        hits = len(set(true_items).intersection(set(recommended_items)))

        # 1. 准确率 Precision@K
        precision = hits / self.k

        # 2. 召回率 Recall@K
        recall = hits / len(true_items)

        # 3. F1-score (任务书硬性要求：准确率与召回率的调和平均数)
        f1_score = 0.0
        if precision + recall > 0:
            f1_score = 2 * (precision * recall) / (precision + recall)

        # 4. NDCG@K (归一化折损累计增益)
        dcg = 0.0
        for rank, item in enumerate(recommended_items):
            if item in true_items:
                dcg += 1.0 / log2(rank + 2)

        idcg = sum([1.0 / log2(rank + 2) for rank in range(min(len(true_items), self.k))])
        ndcg = dcg / idcg if idcg > 0 else 0.0

        return precision, recall, f1_score, ndcg

    def evaluate_groups(self, user_metrics_dict):
        """
        对不同用户群体（活跃用户 vs 长尾用户）的表现进行对比分析
        """
        active_users_metrics = []
        cold_users_metrics = []

        for u, metrics in user_metrics_dict.items():
            count = self.user_interaction_counts.get(u, 0)
            if count >= self.active_threshold:
                active_users_metrics.append(metrics)
            else:
                cold_users_metrics.append(metrics)

        # 计算平均值
        def get_avg(metrics_list):
            if not metrics_list:
                return 0.0, 0.0, 0.0, 0.0
            return np.mean(metrics_list, axis=0)

        active_avg = get_avg(active_users_metrics)
        cold_avg = get_avg(cold_users_metrics)
        overall_avg = get_avg(list(user_metrics_dict.values()))

        return overall_avg, active_avg, cold_avg