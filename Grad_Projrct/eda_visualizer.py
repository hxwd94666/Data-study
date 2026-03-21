import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from utils.data_processor import DataProcessor

# 设置中文字体，确保图表显示正常
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


class EDAGenerator:
    """
    探索性数据分析 (EDA) 图表生成器
    批量输出论文所需的高清统计图表
    """

    def __init__(self, df_interact, df_meta):
        self.df_interact = df_interact
        self.df_meta = df_meta
        self.plot_dir = 'thesis_plots'
        if not os.path.exists(self.plot_dir):
            os.makedirs(self.plot_dir)

    def plot_price_distribution(self):
        print("📊 生成价格分布直方图...")
        plt.figure(figsize=(10, 6))
        sns.histplot(self.df_meta['price'], bins=20, kde=True, color='#2ecc71')
        plt.title('商品价格分布特征与核密度估计', fontsize=15)
        plt.xlabel('价格 (USD)', fontsize=12)
        plt.ylabel('商品频数', fontsize=12)
        plt.savefig(os.path.join(self.plot_dir, 'price_distribution.png'), dpi=300, bbox_inches='tight')
        plt.close()

    def plot_category_pie(self):
        print("📊 生成主类目占比饼图...")
        category_counts = self.df_meta['main_category'].value_counts().head(5)
        plt.figure(figsize=(8, 8))
        plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=140,
                colors=sns.color_palette('pastel'))
        plt.title('Top 5 商品主类目结构占比', fontsize=15)
        plt.savefig(os.path.join(self.plot_dir, 'category_pie.png'), dpi=300)
        plt.close()

    def plot_title_wordcloud(self):
        print("☁️ 生成商品标题文本词云...")
        text = " ".join(title for title in self.df_meta['title'])
        wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis',
                              max_words=100).generate(text)

        plt.figure(figsize=(12, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.title('商品标题高频词汇特征挖掘', fontsize=15)
        plt.savefig(os.path.join(self.plot_dir, 'title_wordcloud.png'), dpi=300, bbox_inches='tight')
        plt.close()


if __name__ == "__main__":
    # 1. 调取数据管道
    processor = DataProcessor('data/Appliances_sampled.csv', 'data/meta_Appliances.csv')
    interactions, meta = processor.process_data()

    # 2. 生成图表
    print("\n🚀 启动可视化绘图引擎...")
    generator = EDAGenerator(interactions, meta)
    generator.plot_price_distribution()
    generator.plot_category_pie()
    generator.plot_title_wordcloud()
    print(f"\n🎉 大功告成！请前往项目中的 'thesis_plots' 文件夹查看你的毕业论文高清配图。")