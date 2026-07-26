"""项目一边栏组件"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import streamlit as st

AVAILABLE_MODELS = [
    "qwen/qwen3.7-max",
    "qwen/qwen3.6-plus",
    "qwen/qwen3.5-flash",
    "qwen/deepseek-r1",
    "qwen/deepseek-v4-pro",
    "qwen/kimi-k2.6",
    "qwen/glm-5.1",
]


def render_sidebar() -> dict:
    """渲染侧边栏，返回用户配置"""
    st.sidebar.image("https://img.icons8.com/color/96/amazon.png", width=64)
    st.sidebar.title("跨境智上")
    st.sidebar.caption("AI-Powered Listing Automation")

    st.sidebar.divider()

    # API Key
    api_key = st.sidebar.text_input(
        "🔑 Model Router API Key",
        type="password",
        placeholder="留空使用Mock模式演示",
        help="初赛通过后发放的API Key，留空使用模拟数据展示",
    )

    if api_key:
        st.sidebar.success("✅ 真实API模式")
    else:
        st.sidebar.info("🔶 Mock演示模式 — 展示完整功能流程")

    st.sidebar.divider()

    # 模型选择
    model = st.sidebar.selectbox(
        "🧠 AI 模型",
        AVAILABLE_MODELS,
        index=0,
        help="选择用于文本生成和Listing写作的AI模型",
    )

    st.sidebar.divider()

    # 全局配置
    platform = st.sidebar.selectbox(
        "📦 目标平台",
        ["Amazon", "Temu", "独立站"],
        help="选择目标电商平台，影响图片尺寸和Listing格式",
    )

    language = st.sidebar.selectbox(
        "🌐 目标语言",
        ["en (English)", "ja (日本語)", "de (Deutsch)", "fr (Français)", "es (Español)"],
        help="选择Listing的目标语言",
    )

    st.sidebar.divider()

    # 产品类别
    category = st.sidebar.selectbox(
        "📂 产品类别",
        ["蓝牙耳机", "智能手表", "充电器/充电宝", "手机壳", "瑜伽用品", "厨房用具", "宠物用品", "灯具", "运动水杯", "其他"],
    )

    st.sidebar.divider()

    st.sidebar.caption("AI+跨境黑客松 · 初赛作品")
    st.sidebar.caption("© 2026 跨境智上 Team")

    return {
        "api_key": api_key if api_key else None,
        "model": model,
        "platform": platform,
        "language": language.split(" ")[0],
        "category": category,
    }
