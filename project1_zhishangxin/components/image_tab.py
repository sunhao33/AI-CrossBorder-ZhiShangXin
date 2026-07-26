"""商品图生成标签页"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import streamlit as st
from shared.model_router import ModelRouter
from modules.image_generator import generate_product_images, IMAGE_PROMPTS


def render_image_tab(router: ModelRouter, config: dict):
    st.header("🎨 AI商品图生成")
    st.caption("使用 wan2.7-image-pro 模型，自动生成符合各平台规范的商品图片")

    col1, col2 = st.columns([2, 1])

    with col1:
        product_name = st.text_input(
            "产品名称",
            value="Wireless Bluetooth 5.3 Earbuds",
            placeholder="输入产品名称，如：Yoga Mat, USB-C Charger...",
        )

    with col2:
        st.caption("&nbsp;")
        st.caption("*支持中英文输入*")

    col_a, col_b = st.columns(2)

    with col_a:
        image_types = st.multiselect(
            "选择图片类型",
            options=["white_bg", "lifestyle", "model", "comparison", "detail"],
            default=["white_bg", "lifestyle"],
            format_func=lambda x: {
                "white_bg": "白底主图",
                "lifestyle": "场景图",
                "model": "模特图",
                "comparison": "对比图",
                "detail": "细节图",
            }.get(x, x),
            help="选择需要生成的商品图类型（可多选）",
        )

    with col_b:
        size = st.selectbox(
            "图片尺寸",
            ["1024x1024", "800x800", "2000x2000", "600x600"],
            index=0,
            help="选择输出图片尺寸",
        )

    with st.expander("高级设置"):
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            setting = st.selectbox(
                "场景风格",
                ["home_office", "kitchen", "outdoor", "gym", "bedroom", "coffee_shop", "travel", "living_room"],
                format_func=lambda x: {
                    "home_office": "居家办公", "kitchen": "现代厨房", "outdoor": "户外自然",
                    "gym": "健身房", "bedroom": "温馨卧室", "coffee_shop": "咖啡厅",
                    "travel": "旅行场景", "living_room": "客厅",
                }.get(x, x),
            )
        with col_s2:
            model_desc = st.selectbox(
                "模特风格",
                ["male_young", "female_young", "professional", "family"],
                format_func=lambda x: {
                    "male_young": "年轻男性", "female_young": "年轻女性",
                    "professional": "职场风格", "family": "家庭场景",
                }.get(x, x),
            )

        style_prompt = st.text_input("额外风格描述（选填）", placeholder="如：minimalist, warm tones, Scandinavian style")

    # 生成按钮
    if st.button("🚀 生成商品图", type="primary", use_container_width=True):
        if not product_name:
            st.warning("请输入产品名称")
            return
        if not image_types:
            st.warning("请至少选择一种图片类型")
            return

        with st.spinner(f"AI正在生成 {len(image_types)} 张商品图..."):
            results = generate_product_images(
                router=router,
                product_name=product_name,
                product_category=config.get("category", ""),
                image_types=image_types,
                style_prompt=style_prompt if style_prompt else "",
                size=size,
                setting=setting,
                model_desc=model_desc,
            )

        # 存入session_state供预览页使用
        st.session_state["generated_images"] = results

        # 展示结果
        st.success(f"✅ 成功生成 {len(results)} 张商品图")
        _display_image_gallery(results)

    # 展示缓存的结果
    if "generated_images" in st.session_state and st.session_state["generated_images"]:
        st.divider()
        st.caption("📸 上次生成结果")
        _display_image_gallery(st.session_state["generated_images"])


def _display_image_gallery(images: list[dict]):
    """展示图片画廊"""
    cols = st.columns(min(len(images), 3))
    for i, img in enumerate(images):
        col_idx = i % len(cols)
        with cols[col_idx]:
            type_names = {
                "white_bg": "白底主图",
                "lifestyle": "场景图",
                "model": "模特图",
                "comparison": "对比图",
                "detail": "细节图",
            }
            st.image(img["url"], caption=type_names.get(img["type"], img["type"]), use_container_width=True)
            with st.expander("查看Prompt"):
                st.code(img["prompt"], language="text")
