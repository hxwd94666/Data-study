import streamlit as st
import torch
import math
import random
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
    processor = DataProcessor('data/Appliances_sampled.csv', 'data/meta_Appliances.csv')
    df_interact, df_meta = processor.process_data()

    num_users = df_interact['user_id_encoded'].nunique()
    num_items = df_interact['item_id_encoded'].nunique()

    device = torch.device("cpu")
    model = AdvancedNCFModel(num_users=num_users, num_items=num_items, text_dim=50)
    model.load_state_dict(torch.load('ours_advanced_ncf_weights.pth', map_location=device))
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
st.sidebar.subheader("📈 评测指标科普 (NDCG)")
st.sidebar.caption("NDCG (归一化折损累计增益) 衡量了 AI 把用户最想要的商品**顶到第一名**的能力。排名越靠前，得分越高。")
st.sidebar.markdown("""
| NDCG 得分区间 | 工业界评级水位 | 表现说明 |
| :--- | :--- | :--- |
| **0.80 - 1.00** | 🌟 业界顶尖 (S级) | 极度精准，如神机妙算 |
| **0.60 - 0.79** | 🚀 优秀水准 (A级) | 达到一线大厂商用标准 |
| **0.40 - 0.59** | 勉强可用 (B级) | 有一定参考性，需优化 |
| **< 0.40** | ❌ 盲人摸象 (C级) | 基本等于随机乱猜 |
""")
st.sidebar.info("💡 提示：在离线全量评估中，本系统 Advanced NCF 模型的 NDCG@5 稳居 A级 以上，在长尾数据中表现卓越！")

# ================= 4. 推荐核心推断逻辑与渲染 =================
if generate_btn or f"hidden_idx_{selected_user}" in st.session_state:
    st.subheader(f"🎯 您的专属推荐分析流水线")

    # ---------------- 场景 A: 新用户冷启动兜底策略 ----------------
    if selected_user == "🌟 全新注册用户 (冷启动演示)":
        st.warning("⚠️ 检测到当前为全新注册用户，无历史交互数据。")
        st.info("🛡️ 系统已自动降级为【全局热门榜单兜底策略】(Popularity Fallback)。")

        popular_item_ids = df_interact['item_id_encoded'].value_counts().index.tolist()
        recommendations = df_meta.set_index('item_id_encoded').loc[popular_item_ids].reset_index()
        recommendations = recommendations.drop_duplicates(subset=['title']).head(top_k)

        cols = st.columns(len(recommendations))
        for idx, (col, row) in enumerate(zip(cols, recommendations.itertuples())):
            with col:
                img_url = "https://via.placeholder.com/300x300.png?text=Hot+Item"
                try:
                    images_list = ast.literal_eval(row.images)
                    if isinstance(images_list, list) and len(images_list) > 0: img_url = images_list[0].get('large',
                                                                                                            img_url)
                except:
                    pass
                st.image(img_url, use_container_width=True)

                # 💡 优雅降级展示：双行截断 + Hover 全称展示
                safe_title = str(row.title).replace('"', '&quot;')
                st.markdown(
                    f'<div title="{safe_title}" style="display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 2; overflow: hidden; font-weight: bold; font-size: 14px; min-height: 40px; margin-bottom: 5px;">{row.title}</div>',
                    unsafe_allow_html=True)

                st.markdown(f"🏷️ 类目: `{row.main_category}`")
                st.success("💡 兜底推荐：全站销量与好评双料冠军")

    # ---------------- 场景 B: 老用户全局推荐 + 随堂测验流水线 ----------------
    else:
        interacted_items_list = df_interact[df_interact['user_id_encoded'] == selected_user]['item_id_encoded'].tolist()

        if len(interacted_items_list) < 2:
            st.warning("该用户历史交互过少（不足2条），无法进行留一法实验。请在左侧切换一个更活跃的老用户！")
        else:
            session_key = f"hidden_idx_{selected_user}"
            if session_key not in st.session_state:
                st.session_state[session_key] = len(interacted_items_list) - 1

            if st.button("🎲 重新实验：随机从历史记录中抽一个商品隐藏"):
                st.session_state[session_key] = random.randint(0, len(interacted_items_list) - 1)
                st.rerun()

            hidden_idx = st.session_state[session_key]
            target_item = interacted_items_list[hidden_idx]
            history_items = [item for i, item in enumerate(interacted_items_list) if i != hidden_idx]

            device = torch.device(
                "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")

            # ================= 模块 1：数据集设定 =================
            st.markdown("---")
            st.markdown("### 🔍 模块 1：留一法实验数据集设定")
            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown("##### 📝 已知购物线索（喂给 AI 的提示）")
                history_details = df_meta.set_index('item_id_encoded').loc[
                    history_items[-4:]].reset_index().drop_duplicates(subset=['title'])
                hist_cols = st.columns(len(history_details))
                for idx, (col, row) in enumerate(zip(hist_cols, history_details.itertuples())):
                    with col:
                        img_url = "https://via.placeholder.com/300x300.png?text=History"
                        try:
                            images_list = ast.literal_eval(row.images)
                            if images_list: img_url = images_list[0].get('large', img_url)
                        except:
                            pass
                        st.image(img_url, use_container_width=True)

                        safe_title = str(row.title).replace('"', '&quot;')
                        st.markdown(
                            f'<div title="{safe_title}" style="display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 2; overflow: hidden; font-size: 13px; color: #555; min-height: 38px; margin-bottom: 5px;">{row.title}</div>',
                            unsafe_allow_html=True)
                        st.caption(f"🏷️ `{row.main_category}`")

            with col2:
                st.markdown("##### 🤫 被隐藏的真实目标（AI 的盲猜对象）")
                target_detail = df_meta[df_meta['item_id_encoded'] == target_item].iloc[0]
                img_url = "https://via.placeholder.com/300x300.png?text=Hidden+Target"
                try:
                    images_list = ast.literal_eval(target_detail['images'])
                    if images_list: img_url = images_list[0].get('large', img_url)
                except:
                    pass
                st.error("此商品对模型处于不可见状态！")
                st.image(img_url, width=150)

                safe_target_title = str(target_detail['title']).replace('"', '&quot;')
                st.markdown(
                    f'<div title="{safe_target_title}" style="display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 2; overflow: hidden; font-weight: bold; font-size: 13px; color: #333; min-height: 38px; margin-bottom: 5px;">{target_detail["title"]}</div>',
                    unsafe_allow_html=True)
                st.caption(f"🏷️ `{target_detail['main_category']}`")

            # ================= 模块 2：全站打分与推荐 =================
            st.markdown("---")
            st.markdown("### 🌐 模块 2：全站【猜你喜欢】全局推荐")
            st.caption("AI 仅依靠上述【已知线索】，在全站数十万商品中大海捞针，展示原生预测概率。")

            global_candidates = [i for i in df_meta['item_id_encoded'].unique() if i not in set(history_items)]

            u_tensor_global = torch.full((len(global_candidates),), selected_user, dtype=torch.long).to(device)
            i_tensor_global = torch.tensor(global_candidates, dtype=torch.long).to(device)
            t_tensor_global = torch.tensor(np.array([item2vec.get(item, np.zeros(50)) for item in global_candidates]),
                                           dtype=torch.float32).to(device)

            with torch.no_grad():
                global_preds = model(u_tensor_global, i_tensor_global, t_tensor_global).view(-1)

            _, global_top_indices = torch.topk(global_preds, k=min(top_k * 3, len(global_preds)))
            global_rec_ids = [global_candidates[idx] for idx in global_top_indices.cpu().numpy()]

            global_recs_raw = df_meta.set_index('item_id_encoded').loc[global_rec_ids].reset_index()
            global_recs_raw = global_recs_raw.drop_duplicates(subset=['title'])

            user_history_categories = set(history_details['main_category'].dropna().tolist())
            global_recs_filtered = global_recs_raw[global_recs_raw['main_category'].isin(user_history_categories)]

            if global_recs_filtered.empty:
                global_recs = global_recs_raw.head(top_k)
                st.info("💡 触发【跨界探索】机制：AI 发现您历史偏好之外的高潜商品！")
            else:
                global_recs = global_recs_filtered.head(top_k)

            global_valid_scores = []
            for item_id in global_recs['item_id_encoded']:
                idx_in_candidates = global_candidates.index(item_id)
                global_valid_scores.append(global_preds[idx_in_candidates].item())

            global_cols = st.columns(len(global_recs))
            for idx, (col, row) in enumerate(zip(global_cols, global_recs.itertuples())):
                with col:
                    img_url = "https://via.placeholder.com/300x300.png?text=Global+Rec"
                    try:
                        images_list = ast.literal_eval(row.images)
                        if images_list: img_url = images_list[0].get('large', img_url)
                    except:
                        pass
                    st.image(img_url, use_container_width=True)

                    safe_title = str(row.title).replace('"', '&quot;')
                    st.markdown(
                        f'<div title="{safe_title}" style="display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 2; overflow: hidden; font-weight: bold; font-size: 14px; min-height: 40px; margin-bottom: 5px;">{row.title}</div>',
                        unsafe_allow_html=True)
                    st.markdown(
                        f"💰 原生预测匹配度: <span style='color:#2ecc71; font-weight:bold;'>{(global_valid_scores[idx] * 100):.1f}%</span>",
                        unsafe_allow_html=True)

            # ================= 模块 3：1+9 留一法严格测验 =================
            st.markdown("---")
            st.markdown("### 📝 模块 3：1+9 留一法随堂严格测验")
            st.caption("为了直观验证排序能力，我们将【隐藏目标】与 9 个【从未买过的随机干扰项】混在一起打分排序。")

            all_items_list = df_meta['item_id_encoded'].unique().tolist()
            negative_pool = [i for i in all_items_list if i not in set(interacted_items_list)]
            sampled_negatives = random.sample(negative_pool, 9) if len(negative_pool) >= 9 else negative_pool

            test_candidates = [target_item] + sampled_negatives
            random.shuffle(test_candidates)

            u_tensor_test = torch.full((len(test_candidates),), selected_user, dtype=torch.long).to(device)
            i_tensor_test = torch.tensor(test_candidates, dtype=torch.long).to(device)
            t_tensor_test = torch.tensor(np.array([item2vec.get(item, np.zeros(50)) for item in test_candidates]),
                                         dtype=torch.float32).to(device)

            with torch.no_grad():
                test_preds = model(u_tensor_test, i_tensor_test, t_tensor_test).view(-1)

            _, test_top_indices = torch.topk(test_preds, k=len(test_preds))
            test_ranked_ids = [test_candidates[idx] for idx in test_top_indices.cpu().numpy()]
            test_ranked_scores = [test_preds[idx].item() for idx in test_top_indices.cpu().numpy()]

            hit_rank = test_ranked_ids.index(target_item) + 1
            current_ndcg = 1.0 / math.log2(hit_rank + 1)

            if hit_rank == 1:
                st.success(f"🎉 **完美通关！** AI 将隐藏目标稳稳排在第 **1** 名！")
                st.info(f"🏆 本次测验实时 NDCG 得分：**{current_ndcg:.4f}** (满分！)")
                st.balloons()
            else:
                st.error(f"❌ **挑战失败！** 隐藏目标仅排在第 **{hit_rank}** 名。")
                st.warning(f"📉 本次测验实时 NDCG 得分：**{current_ndcg:.4f}** (随着排名靠后，得分发生了严重折损)")

            st.markdown("##### 📊 随堂测验 10 项商品排序结果详情：")

            row1_cols = st.columns(5)
            row2_cols = st.columns(5)
            all_cols = row1_cols + row2_cols

            for rank_idx, (col, item_id, score) in enumerate(zip(all_cols, test_ranked_ids, test_ranked_scores)):
                item_detail = df_meta[df_meta['item_id_encoded'] == item_id].iloc[0]
                with col:
                    is_target = (item_id == target_item)
                    bg_color = "#ffeaa7" if is_target else "#ffffff"
                    border = "2px solid #e74c3c" if is_target else "1px solid #ddd"

                    safe_test_title = str(item_detail['title']).replace('"', '&quot;')
                    st.markdown(f"""
                    <div style="background-color: {bg_color}; border: {border}; padding: 10px; border-radius: 5px; height: 180px;">
                        <b style="font-size: 16px;">第 {rank_idx + 1} 名</b><br>
                        <div title="{safe_test_title}" style="display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 2; overflow: hidden; font-size: 12px; color: #555; min-height: 35px; margin-bottom: 5px;">{item_detail['title']}</div>
                        <span style="font-size: 14px; color: #d35400; font-weight: bold;">得分: {(score * 100):.1f}%</span>
                        {'<br><span style="color:red; font-weight:bold;">🎯 隐藏目标</span>' if is_target else ''}
                    </div>
                    """, unsafe_allow_html=True)