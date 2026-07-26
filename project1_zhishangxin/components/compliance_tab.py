"""商品图合规检测标签页"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import streamlit as st
from shared.model_router import ModelRouter
from modules.compliance_checker import check_image_compliance, get_market_rules_summary


def render_compliance_tab(router: ModelRouter, config: dict):
    st.header("🔍 AI商品图跨境合规检测")
    st.caption("使用视觉模型检测商品图是否违反目标市场的广告法/平台规则")

    col1, col2 = st.columns([1, 1])

    with col1:
        target_market = st.selectbox(
            "目标市场",
            ["us", "eu", "jp", "me", "sea"],
            format_func=lambda x: {
                "us": "🇺🇸 美国", "eu": "🇪🇺 欧盟",
                "jp": "🇯🇵 日本", "me": "🇸🇦 中东", "sea": "🇸🇬 东南亚",
            }.get(x, x),
        )
        platform = st.selectbox("目标平台", ["Amazon", "Temu"])

        # 显示市场规则摘要
        rules = get_market_rules_summary(target_market, platform)
        if rules:
            with st.expander(f"📜 {platform} {target_market.upper()} 市场规则"):
                for r in rules:
                    st.markdown(f"- {r}")

    with col2:
        uploaded_file = st.file_uploader(
            "上传商品图",
            type=["png", "jpg", "jpeg", "webp"],
            help="上传需要合规检测的商品图片",
        )

        product_category = st.text_input("产品类别（选填）", value=config.get("category", ""))

        # 预览
        if uploaded_file:
            st.image(uploaded_file, caption="上传的图片", use_container_width=True)

    # 检测按钮
    if st.button("🔎 开始合规检测", type="primary", use_container_width=True):
        if not uploaded_file:
            st.warning("请先上传商品图片")
            return

        # 读取图片为base64或data URL
        import base64
        from io import BytesIO
        from PIL import Image

        image = Image.open(uploaded_file)
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_data = base64.b64encode(buffered.getvalue()).decode()
        image_url = f"data:image/png;base64,{img_data}"

        with st.spinner(f"AI正在检测商品图合规性（{target_market.upper()}市场）..."):
            result = check_image_compliance(
                router=router,
                image_url=image_url,
                target_market=target_market,
                platform=platform,
                product_category=product_category,
            )

        # 展示结果
        _display_compliance_result(result)

    # Demo快速演示
    if not uploaded_file:
        st.divider()
        st.info("💡 **没有商品图？** 可以使用Demo模式快速体验合规检测功能：")
        if st.button("🎭 加载Demo检测结果"):
            st.session_state["demo_compliance"] = True

    if st.session_state.get("demo_compliance"):
        _display_demo_results()


def _display_compliance_result(result: dict):
    """展示合规检测结果"""
    status = result.get("overall_status", "UNKNOWN")

    if status == "PASS":
        st.success(f"### ✅ 合规通过 — 综合评分: {result.get('overall_score', 0)}/100")
    elif status == "FAIL":
        st.error(f"### ❌ 不合规 — 综合评分: {result.get('overall_score', 0)}/100")
    else:
        st.warning(f"### ⚠️ 有警告 — 综合评分: {result.get('overall_score', 0)}/100")

    st.caption(f"目标市场: {result.get('market_name', '')} · 平台: {result.get('platform', '')}")

    # 逐项检查
    for check in result.get("checks", []):
        emoji = {"PASS": "✅", "FAIL": "❌", "WARNING": "⚠️"}.get(check["status"], "❓")
        with st.expander(f"{emoji} {check['category']} — {check['status']}"):
            st.write(check.get("detail", ""))
            if "fix" in check:
                st.info(f"🔧 修复建议: {check['fix']}")
            st.progress(check.get("score", 50) / 100)

    # 总体建议
    if result.get("recommendations"):
        st.subheader("📌 改进建议")
        for rec in result["recommendations"]:
            st.markdown(f"- {rec}")


def _display_demo_results():
    """展示Demo合规检测结果"""
    st.divider()
    st.subheader("🎭 Demo检测结果示例")

    col_a, col_b = st.columns(2)
    with col_a:
        st.success("### ✅ 合规通过 (92分)")
        checks_pass = [
            ("图片质量", "PASS", "分辨率2000x2000px符合Amazon ≥1000px要求"),
            ("主图背景", "PASS", "纯白背景 #FFFFFF确认，产品占比87%"),
            ("文字/Logo", "PASS", "未检测到未经授权的商标或水印"),
            ("文化敏感", "PASS", "无宗教符号或文化禁忌内容"),
            ("平台规则", "PASS", "符合Amazon主图规范"),
        ]
        for cat, status, detail in checks_pass:
            st.markdown(f"✅ **{cat}**: {detail}")

    with col_b:
        st.error("### ❌ 不合规 (45分)")
        checks_fail = [
            ("图片质量", "FAIL", "分辨率800x800px不满足Amazon ≥1000px要求"),
            ("主图背景", "FAIL", "背景非纯白(RGB 238,242,245)，产品占比仅55%"),
            ("文字/Logo", "FAIL", "图片含'SALE 50% OFF'促销文字（Amazon禁止）"),
            ("文化敏感", "WARN", "检测到特定手势，在中东市场可能有冒犯性"),
            ("平台规则", "FAIL", "图片包含竞品Logo，存在商标侵权风险"),
        ]
        for cat, status, detail in checks_fail:
            st.markdown(f"❌ **{cat}**: {detail}")
