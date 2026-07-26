"""
跨境智上 — AI智能上新平台
AI+跨境黑客松巅峰赛 · 项目一
AI实现从商品图生成到详情页上架的自动化
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from shared.model_router import ModelRouter

# 页面配置
st.set_page_config(
    page_title="跨境智上 — AI智能上新",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 导入组件
from components.sidebar import render_sidebar
from components.image_tab import render_image_tab
from components.listing_tab import render_listing_tab
from components.compliance_tab import render_compliance_tab
from components.preview_tab import render_preview_tab


def init_session():
    """初始化session state"""
    if "router" not in st.session_state:
        st.session_state.router = ModelRouter(api_key=None)
    if "generated_images" not in st.session_state:
        st.session_state.generated_images = []
    if "generated_listings" not in st.session_state:
        st.session_state.generated_listings = {}
    if "preview_html" not in st.session_state:
        st.session_state.preview_html = None


def main():
    init_session()

    # 渲染侧边栏
    config = render_sidebar()

    # 根据API Key重新初始化router
    if config["api_key"]:
        if st.session_state.router.mock_mode or st.session_state.router.api_key != config["api_key"]:
            st.session_state.router = ModelRouter(api_key=config["api_key"])
    else:
        if not st.session_state.router.mock_mode:
            st.session_state.router = ModelRouter(api_key=None)

    router = st.session_state.router

    # 主体区域
    st.title("🚀 跨境智上 — AI智能上新平台")
    st.caption("从选品到上架，AI将新品上架流程从数天压缩至分钟级 | AI+跨境黑客松巅峰赛")

    # Mock模式提示
    if router.mock_mode:
        st.info(
            "🔶 **Mock演示模式** — 所有AI功能使用模拟数据展示完整流程。"
            "在侧边栏输入Model Router API Key即可切换为真实AI生成模式。"
        )

    # 四标签页
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎨 商品图生成",
        "📝 Listing写作",
        "🔍 合规检测",
        "🖼️ 详情页预览",
    ])

    with tab1:
        render_image_tab(router, config)

    with tab2:
        render_listing_tab(router, config)

    with tab3:
        render_compliance_tab(router, config)

    with tab4:
        render_preview_tab(config)


if __name__ == "__main__":
    main()
