"""多语言Listing写作标签页"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import streamlit as st
from shared.model_router import ModelRouter
from modules.listing_writer import generate_listing, LANGUAGE_CONFIG, PLATFORM_RULES


def render_listing_tab(router: ModelRouter, config: dict):
    st.header("📝 AI多语言Listing写作")
    st.caption("基于Qwen系列模型，为不同平台和语言生成高转化率的商品Listing")

    # 产品信息表单
    with st.expander("📋 产品信息", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            product_name = st.text_input("产品名称", value="Wireless Bluetooth 5.3 Earbuds")
            product_category = st.text_input("产品类别", value=config.get("category", "消费电子/蓝牙耳机"))
        with col2:
            materials = st.text_input("材质/规格", value="ABS + Silicone, Bluetooth 5.3 chip, 13mm dynamic drivers")
            target_audience = st.text_input("目标用户", value="运动爱好者、通勤族、学生")

        features = st.text_area(
            "核心卖点（每行一个）",
            value="Bluetooth 5.3 stable connection\n40 hours total battery life\nIPX7 waterproof for sports\nENC noise cancelling calls\nErgonomic comfortable fit",
            height=120,
        )
        usp = st.text_input("独特卖点（一句话）", value="Half the price of AirPods with 3x longer battery life")

    # 平台和语言选择
    col_p, col_l = st.columns(2)
    with col_p:
        platform = st.selectbox("目标平台", ["Amazon", "Temu"], index=0)
    with col_l:
        language = st.selectbox(
            "目标语言",
            ["en", "ja", "de", "fr", "es"],
            format_func=lambda x: f"{LANGUAGE_CONFIG[x]['flag']} {LANGUAGE_CONFIG[x]['name']}",
        )

    # 平台规则参考
    rules = PLATFORM_RULES.get(platform, PLATFORM_RULES["Amazon"])
    with st.expander("📏 平台规则参考"):
        st.info(f"""
        **{platform} Listing规则:**
        - 标题最长: {rules['title_max']} 字符
        - 每条Bullet最长: {rules['bullets_max']} 字符
        - 搜索词最长: {rules['search_terms_max']} 字节
        """)

    if st.button("✨ 生成Listing", type="primary", use_container_width=True):
        if not product_name or not features:
            st.warning("请至少填写产品名称和核心卖点")
            return

        with st.spinner(f"AI正在撰写{platform} {LANGUAGE_CONFIG[language]['name']} Listing..."):
            listing = generate_listing(
                router=router,
                product_name=product_name,
                product_category=product_category,
                features=features,
                materials=materials,
                target_audience=target_audience,
                unique_selling_points=usp,
                platform=platform,
                language=language,
            )

        # 存入session_state供预览页使用
        if "generated_listings" not in st.session_state:
            st.session_state["generated_listings"] = {}
        key = f"{platform}_{language}"
        st.session_state["generated_listings"][key] = listing

        _display_listing_result(listing)

    # 显示缓存的listing
    if "generated_listings" in st.session_state and st.session_state["generated_listings"]:
        st.divider()
        st.caption("📋 已生成的Listing")
        for key, listing in st.session_state["generated_listings"].items():
            with st.expander(f"{listing['lang_flag']} {listing['lang_name']} · {listing['platform']}"):
                _display_listing_result(listing)


def _display_listing_result(listing: dict):
    """展示Listing结果"""
    # 标题
    st.subheader("📌 标题")
    cc = listing["char_counts"]
    title_pct = min(100, cc["title"] / cc["title_max"] * 100) if cc["title_max"] else 0
    st.code(listing["title"], language="text")
    st.progress(title_pct / 100, f"字符数: {cc['title']}/{cc['title_max']}")

    # Bullet Points
    st.subheader("🔹 Bullet Points")
    for i, bullet in enumerate(listing["bullets"]):
        bullet_pct = min(100, cc["bullets"][i] / cc["bullets_max"] * 100) if i < len(cc["bullets"]) and cc["bullets_max"] else 0
        with st.container():
            st.markdown(f"**{i+1}.** {bullet}")
            st.caption(f"字符数: {cc['bullets'][i] if i < len(cc['bullets']) else '?'}/{cc['bullets_max']}")
            st.progress(bullet_pct / 100)
            st.divider()

    # 搜索词
    st.subheader("🔍 Search Terms")
    st.code(listing["search_terms"], language="text")
    st.caption(f"字符数: {cc['search_terms']}/{cc['search_terms_max']}")

    # 操作按钮
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        full_text = f"{listing['title']}\n\n" + "\n".join(listing["bullets"]) + f"\n\n{listing['search_terms']}"
        st.download_button("📥 下载全文", data=full_text, file_name=f"listing_{listing['language']}.txt")
    with col_b:
        st.button("📋 复制全部", key=f"copy_{listing['language']}_{listing['platform']}", help="已复制到剪贴板")
    with col_c:
        if st.button("🔄 重新生成", key=f"regen_{listing['language']}_{listing['platform']}"):
            st.rerun()
