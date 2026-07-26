"""详情页预览组装标签页"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import streamlit as st
from modules.preview_assembler import assemble_preview, PREVIEW_TEMPLATES


def render_preview_tab(config: dict):
    st.header("🖼️ 详情页预览组装")
    st.caption("将AI生成的商品图+Listing自动组合为完整的详情页预览")

    # 检查是否有生成的图片和Listing
    has_images = "generated_images" in st.session_state and st.session_state["generated_images"]
    has_listings = "generated_listings" in st.session_state and st.session_state["generated_listings"]

    if not has_images and not has_listings:
        st.info("👈 请先在【商品图生成】和【Listing写作】标签页生成内容，然后在此处预览组装效果")
        _show_empty_demo()
        return

    # 选择模板
    col1, col2 = st.columns(2)
    with col1:
        template = st.selectbox(
            "选择预览模板",
            list(PREVIEW_TEMPLATES.keys()),
            format_func=lambda x: {"Amazon": "🟠 Amazon 标准模板", "Temu": "🟡 Temu 模板", "独立站": "⚫ 独立站品牌模板"}.get(x, x),
        )
    with col2:
        marketplace = st.selectbox(
            "目标市场",
            ["US", "UK", "DE", "JP", "FR", "ES", "SA", "SG"],
            index=0,
        )

    # 选择图片
    if has_images:
        st.subheader("📸 选择商品图")
        images = st.session_state["generated_images"]
        cols = st.columns(len(images))
        selected_images = []
        for i, img in enumerate(images):
            with cols[i]:
                st.image(img["url"], use_container_width=True)
                if st.checkbox(f"使用", value=(i == 0), key=f"use_img_{i}"):
                    selected_images.append(img)
    else:
        selected_images = []

    # 选择Listing
    if has_listings:
        st.subheader("📝 选择Listing")
        listings = st.session_state["generated_listings"]
        listing_keys = list(listings.keys())
        listing_names = [f"{listings[k]['lang_flag']} {listings[k]['lang_name']} · {listings[k]['platform']}" for k in listing_keys]
        selected_listing_key = st.selectbox("选择已生成的Listing", listing_keys, format_func=lambda x: f"{listings[x]['lang_flag']} {listings[x]['lang_name']} · {listings[x]['platform']}")
        selected_listing = listings[selected_listing_key]
    else:
        selected_listing = None

    # 组装预览
    if st.button("🎨 组装预览", type="primary", use_container_width=True):
        if not selected_images:
            st.warning("请至少选择一张商品图")
            return
        if not selected_listing:
            st.warning("请选择一个Listing")
            return

        html = assemble_preview(
            images=selected_images,
            listing=selected_listing,
            template=template,
            marketplace=marketplace,
            category=config.get("category", ""),
        )

        st.session_state["preview_html"] = html
        st.success("✅ 详情页预览已生成")

    # 显示预览
    if "preview_html" in st.session_state and st.session_state["preview_html"]:
        st.divider()
        st.subheader("🔍 预览效果")

        # 切换模式
        view_mode = st.radio("查看模式", ["渲染预览", "HTML源码"], horizontal=True)

        if view_mode == "渲染预览":
            st.components.v1.html(st.session_state["preview_html"], height=800, scrolling=True)
        else:
            st.code(st.session_state["preview_html"], language="html")

        # 下载
        st.download_button(
            "📥 下载HTML文件",
            data=st.session_state["preview_html"],
            file_name="product_detail_page.html",
            mime="text/html",
        )


def _show_empty_demo():
    """展示一个静态Demo预览"""
    st.divider()
    st.subheader("🎭 快速体验Demo")

    demo_html = """<div style="max-width:800px;margin:0 auto;font-family:Arial,sans-serif;color:#0F1111;border:1px solid #ddd;border-radius:8px;padding:24px">
    <div style="display:flex;gap:16px">
        <div style="width:400px;height:400px;background:linear-gradient(135deg,#f5f5f5,#e0e0e0);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:48px">🎧</div>
        <div style="flex:1">
            <h1 style="font-size:20px;line-height:1.3">Wireless Bluetooth 5.3 Earbuds with 40H Battery Life, IPX7 Waterproof Sport Earphones</h1>
            <div style="color:#C7511F;font-size:18px;margin:8px 0">★★★★☆ <span style="color:#007185;font-size:14px">2,847 ratings</span></div>
            <div style="font-size:24px;color:#B12704;margin:8px 0">$44.99 <span style="color:#999;text-decoration:line-through;font-size:16px">$59.99</span></div>
            <div style="border-top:1px solid #eee;padding-top:12px;margin-top:12px">
                <p style="margin:4px 0;font-size:14px">• 40-Hour Total Playtime & LED Display</p>
                <p style="margin:4px 0;font-size:14px">• Bluetooth 5.3 & One-Step Pairing</p>
                <p style="margin:4px 0;font-size:14px">• IPX7 Waterproof & Sweatproof</p>
                <p style="margin:4px 0;font-size:14px">• ENC Noise Cancelling Calls</p>
                <p style="margin:4px 0;font-size:14px">• Ergonomic Design & Comfort Fit</p>
            </div>
        </div>
    </div>
    <p style="text-align:center;color:#999;margin-top:16px;font-size:12px">Amazon Listing Preview — AI Generated Demo</p>
</div>"""

    st.components.v1.html(demo_html, height=550, scrolling=True)
    st.caption("👆 这是一个静态Demo展示，请先在各标签页生成真实的图片和Listing内容以获得完整预览")
