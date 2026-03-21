import streamlit as st
import torch
import pandas as pd
import numpy as np
import ast

# 引入我们自己写的核心模块
from utils.data_processor import DataProcessor
from models.ncf_advanced import AdvancedNCFModel

# ================= 1. 页面基础配置 =================
st.set_page_config(page_title="智能电商推荐系统", page_icon="🛍️", layout="wide")
st.title("🛍️ 增强型双塔推荐系统 (Text-Enhanced NCF)")
st.markdown("基于 PyTorch 与 Amazon 真实数据集的个性化购物展示平台")
st.markdown("---")


# ================= 2. 缓存加载引擎 =================
@st.cache_resource
def init_system():
    # 确保这里的路径和你实际运行的 CSV 名字一致
    processor = DataProcessor('data/Appliances_sampled.csv', 'data/meta_Appliances.csv')
    df_interact, df_meta = processor.process_data()

    num_users = df_interact['user_id_encoded'].nunique()
    num_items = df_interact['item_id_encoded'].nunique()

    device = torch.device("cpu")
    model = AdvancedNCFModel(num_users=num_users, num_items=num_items, text_dim=50)
    # 加载权重
    model.load_state_dict(torch.load('advanced_ncf.pth', map_location=device))
    model.eval()

    item2vec = dict(zip(df_meta['item_id_encoded'], df_meta['title_vector']))

    return df_interact, df_meta, model, num_users, num_items, item2vec


with st.spinner("🚀 正在加载底层推荐引擎与模型权重..."):
    df_interact, df_meta, model, num_users, num_items, item2vec = init_system()

# ================= 3. 侧边栏：用户交互区 =================
st.sidebar.header("👤 模拟用户登录")

valid_users = ["🌟 全新注册用户 (冷启动演示)"] + sorted(df_interact['user_id_encoded'].unique().tolist())
selected_user = st.sidebar.selectbox("请选择当前登录用户", valid_users)

top_k = st.sidebar.slider("生成推荐数量 (Top-K)", min_value=3, max_value=8, value=4)
generate_btn = st.sidebar.button("✨ 生成个性化推荐", use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.caption("💡 核心算法：融合文本语义的双塔 NCF 模型 + 热门兜底策略")

# ================= 4. 推荐核心推断逻辑与渲染 =================
if generate_btn:
    st.subheader(f"🎯 您的专属【猜你喜欢】")

    # ---------------- 场景 A: 新用户冷启动兜底策略 ----------------
    if selected_user == "🌟 全新注册用户 (冷启动演示)":
        st.warning("⚠️ 检测到当前为全新注册用户，无历史交互数据。")
        st.info("🛡️ 系统已自动降级为【全局热门榜单兜底策略】(Popularity Fallback)。")

        popular_item_ids = df_interact['item_id_encoded'].value_counts().index.tolist()

        # 获取商品详情并根据标题去重
        recommendations = df_meta.set_index('item_id_encoded').loc[popular_item_ids].reset_index()
        recommendations = recommendations.drop_duplicates(subset=['title']).head(top_k)

        simulated_scores = [0.99 - (i * 0.02) for i in range(len(recommendations))]

        # 渲染新用户推荐卡片
        cols = st.columns(len(recommendations))
        for idx, (col, row) in enumerate(zip(cols, recommendations.itertuples())):
            with col:
                img_url = "https://via.placeholder.com/300x300.png?text=Hot+Item"
                try:
                    images_list = ast.literal_eval(row.images)
                    if isinstance(images_list, list) and len(images_list) > 0:
                        img_url = images_list[0].get('large', img_url)
                except:
                    pass
                st.image(img_url, use_container_width=True)
                st.markdown(f"**{row.title[:40]}...**")
                st.markdown(f"🏷️ 类目: `{row.main_category}`")
                st.markdown(
                    f"🔥 热度指数: <span style='color:#e74c3c; font-weight:bold;'>{simulated_scores[idx] * 100:.1f}</span>",
                    unsafe_allow_html=True)
                st.success("💡 推荐理由：该商品为全站销量与好评双料冠军。")

    # ---------------- 场景 B: 老用户个性化神经网络推荐 ----------------
    else:
        interacted_items = set(df_interact[df_interact['user_id_encoded'] == selected_user]['item_id_encoded'])
        candidates = [i for i in df_meta['item_id_encoded'].unique() if i not in interacted_items]

        if not candidates:
            st.warning("该用户已经买遍了所有商品！")
        else:
            u_tensor = torch.full((len(candidates),), selected_user, dtype=torch.long)
            i_tensor = torch.tensor(candidates, dtype=torch.long)
            t_tensor = torch.tensor(np.array([item2vec.get(item, np.zeros(50)) for item in candidates]),
                                    dtype=torch.float32)

            with torch.no_grad():
                predictions = model(u_tensor, i_tensor, t_tensor).view(-1)

            # 提取 3 倍候选商品以应对去重消耗
            _, top_indices = torch.topk(predictions, k=min(top_k * 3, len(predictions)))
            recommended_item_ids = [candidates[idx] for idx in top_indices.numpy()]

            # 按预测顺序对齐数据并执行标题去重
            recommendations = df_meta.set_index('item_id_encoded').loc[recommended_item_ids].reset_index()
            recommendations = recommendations.drop_duplicates(subset=['title']).head(top_k)

            # 提取去重后商品对应的真实预测分数
            valid_scores = [predictions[top_indices[i]].item() for i in recommendations.index]

            # 渲染老用户推荐卡片
            cols = st.columns(len(recommendations))
            for idx, (col, row) in enumerate(zip(cols, recommendations.itertuples())):
                with col:
                    img_url = "https://via.placeholder.com/300x300.png?text=No+Image"
                    try:
                        images_list = ast.literal_eval(row.images)
                        if isinstance(images_list, list) and len(images_list) > 0:
                            img_url = images_list[0].get('large', img_url)
                    except:
                        pass
                    st.image(img_url, use_container_width=True)
                    st.markdown(f"**{row.title[:40]}...**")
                    st.markdown(f"🏷️ 类目: `{row.main_category}`")
                    st.markdown(
                        f"💰 预测匹配度: <span style='color:#e74c3c; font-size:18px; font-weight:bold;'>{(valid_scores[idx] * 100):.1f}%</span>",
                        unsafe_allow_html=True)
                    st.info(f"💡 推荐理由：结合您的行为画像，该商品语义特征与您的潜在偏好高度吻合。")

# 注意：代码到此结束，下面绝对不要再有任何脱离缩进的 cols = st.columns(...) 代码了！