import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# ================= 1. 输入数据 (核心修改点) =================
# 💡 请从你之前跑完 train_eval.py 最后的汇总表格中抄录 NDCG@5 和 Precision@5 的分数。
# 这里我使用了示例分数，请务必修改为你实际跑出来的准确数字！

models = ['Baseline_MF', 'Baseline_DeepFM', 'Ours_Advanced_NCF']
precisions = [0.45, 0.62, 0.78]   # 💡 替换为你的真实 Precision@5 分数
ndcgs = [0.51, 0.68, 0.84]       # 💡 替换为你的真实 NDCG@5 分数

# ================= 2. 数据结构整理 =================
# 将数据整理为 Seaborn 喜欢的 Long-form DataFrame
# 这就像给电脑做一张Excel表
data_list = []
for i in range(len(models)):
    # 存入 Precision 数据
    data_list.append({
        'Model Name': models[i],
        'Metric Score': precisions[i],
        'Metric Type': 'Precision@5'  # 图例显示的名字
    })
    # 存入 NDCG 数据
    data_list.append({
        'Model Name': models[i],
        'Metric Score': ndcgs[i],
        'Metric Type': 'NDCG@5'      # 图例显示的名字
    })

df_plot = pd.DataFrame(data_list)

# ================= 3. 绘图设置与风格调整 =================
# 设置整体绘图风格为学术风格
sns.set_theme(style="whitegrid", context="talk", font_scale=1.0)
# 设置字体为学术界常用的 Serif 字体 (防止出现不支持中文的情况)
plt.rcParams["font.family"] = "DejaVu Serif"

# 创建画布
plt.figure(figsize=(12, 7))

# ================= 4. 画彩色柱状图 (核心代码) =================
# 绘制分组柱状图
# color_palette=["#66c2a5", "#fc8d62"] 分别是 NDCG 和 Precision 的学术配色
barplot = sns.barplot(
    data=df_plot,
    x='Model Name',
    y='Metric Score',
    hue='Metric Type',
    palette=["#66c2a5", "#fc8d62"], # 学术配色
    edgecolor="black", # 柱子边框
    lw=1.5 # 边框粗细
)

# ================= 5. 自动在柱子顶端标注数据 =================
# 这一步极其重要，免去了在PPT里手动加数据的麻烦
# 💡 遍历每一个柱子
for p in barplot.patches:
    height = p.get_height()
    # 在柱子顶端居中位置写上具体分数
    barplot.text(
        p.get_x() + p.get_width() / 2.,
        height + 0.02, # 文字距离柱子顶端的高度
        '{:,.3f}'.format(height), # 保留三位小数
        ha="center", # 文字水平居中
        size=14 # 文字大小
    )

# ================= 6. 图表装饰与美化 =================
# 设置横纵轴标题
plt.xlabel("Model Architecture (Baseline vs. Ours)", fontsize=18, fontweight='bold')
plt.ylabel("Metric Score (0-1)", fontsize=18, fontweight='bold')

# 设置图表大标题 (放在论文里时，建议把标题删掉，直接在论文里写图注)
# plt.title("Performance Comparison with State-of-the-art Models", fontsize=22, fontweight='bold')

# 设置纵轴范围，防止分数太高冲破边界
plt.ylim(0, 1.0)

# 设置图例位置和字体大小
plt.legend(loc='upper left', fontsize=14, title_fontsize=16)

# ================= 7. 保存高清图片 =================
# 保存为高清的 PNG 图片
# dpi=300 保证打印出来非常清晰，bbox_inches='tight' 保证边缘不会截断
plt.savefig("ours_performance_comparison.png", dpi=300, bbox_inches='tight')
print("\n🎉 恭喜！三大模型打擂台彩色对比图已成功保存至 ours_performance_comparison.png")
print("快把这张图插进你论文的第五章里去碾压基准模型吧！")

# plt.show() # 如果你想直接在IDEA里预览，可以把这行取消注释