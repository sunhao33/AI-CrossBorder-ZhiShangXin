"""商品图合规检测模块 — 调用视觉模型检查图片合规性"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from shared.model_router import ModelRouter

MARKET_RULES = {
    "us": {
        "name": "美国市场",
        "platforms": {
            "Amazon": ["FTC truth-in-advertising compliance", "No unsubstantiated claims", "No competitor brand references"],
            "Temu": ["No Amazon-branded packaging in images", "No 'Prime' or 'FBA' badges", "Clean product-only images"],
        },
    },
    "eu": {
        "name": "欧盟市场",
        "platforms": {
            "Amazon": ["CE marking visible on product if applicable", "No misleading environmental claims (Green Claims Directive)", "GDPR-compliant — no personal data visible"],
            "Temu": ["EU Responsible Person info in listing (not image)", "Language neutrality preferred", "No country-specific flags unless actually made there"],
        },
    },
    "jp": {
        "name": "日本市场",
        "platforms": {
            "Amazon": ["PSE mark for electrical products", "No culturally insensitive imagery (tattoos, certain hand gestures)", "Japanese text must be grammatically correct (no machine translation errors)"],
            "Temu": ["Clean minimal design preferred by Japanese consumers", "Product dimensions in metric (cm, not inches)", "White/pastel backgrounds preferred"],
        },
    },
    "me": {
        "name": "中东市场",
        "platforms": {
            "Amazon": ["Saudi SASO certification marks", "No images of women in revealing clothing", "No alcohol, pork, or religious imagery", "Arabic text right-to-left orientation correct"],
            "Temu": ["UAE/GCC compliance marks", "Conservative imagery", "Family-friendly content only"],
        },
    },
    "sea": {
        "name": "东南亚市场",
        "platforms": {
            "Amazon": ["Halal certification if applicable (Indonesia/Malaysia)", "No politically sensitive imagery (maps showing disputed territories)", "Tropical climate product positioning"],
            "Temu": ["Local language options preferred", "Mobile-first image composition", "Bright/vibrant color palette preference"],
        },
    },
}


def check_image_compliance(
    router: ModelRouter,
    image_url: str,
    target_market: str = "us",
    platform: str = "Amazon",
    product_category: str = "",
) -> dict:
    """
    对商品图进行跨境合规检测。
    返回: {"overall_status": "PASS/FAIL", "overall_score": 0-100, "checks": [...], "recommendations": [...]}
    """
    market = MARKET_RULES.get(target_market, MARKET_RULES["us"])
    platform_rules = market.get("platforms", {}).get(platform, [])

    system_prompt = f"""You are a cross-border e-commerce image compliance auditor. You inspect product images for violations of {market['name']} regulations and {platform} platform rules.

Rules to check for {platform} in {market['name']}:
{chr(10).join(f'- {r}' for r in platform_rules)}

Additionally, always check these universal standards:
- Image resolution: minimum 1000px on longest side for Amazon, 800px for Temu
- Main image background: pure white (#FFFFFF) with 85%+ product coverage for Amazon
- No promotional text, watermarks, or logos on main images
- No misleading representations or exaggerated claims
- Product clearly visible and in focus
- Culturally appropriate content for the target market

Respond ONLY in JSON format:
{{
  "overall_status": "PASS" or "FAIL",
  "overall_score": 0-100,
  "checks": [
    {{"category": "...", "status": "PASS"/"FAIL"/"WARNING", "score": 0-100, "detail": "..."}}
  ],
  "recommendations": ["..."]
}}"""

    user_prompt = f"Inspect this product image for {market['name']} ({platform}) compliance."
    if product_category:
        user_prompt += f" Product category: {product_category}."

    response = router.vision_chat(
        image_urls=[image_url],
        prompt=user_prompt,
        model="qwen/qwen3-vl-plus",
    )

    content = router.extract_content(response)

    import json
    import re

    try:
        data = json.loads(content)
    except (json.JSONDecodeError, TypeError):
        match = re.search(r"\{[\s\S]*\}", content) if content else None
        if match:
            data = json.loads(match.group())
        else:
            data = {
                "overall_status": "WARNING",
                "overall_score": 0,
                "checks": [],
                "recommendations": ["Unable to analyze image. Please try again with a clear product photo."],
            }

    data["market_name"] = market["name"]
    data["platform"] = platform
    return data


def get_market_rules_summary(target_market: str, platform: str) -> list[str]:
    """获取目标市场的合规规则摘要"""
    market = MARKET_RULES.get(target_market, MARKET_RULES["us"])
    return market.get("platforms", {}).get(platform, [])
