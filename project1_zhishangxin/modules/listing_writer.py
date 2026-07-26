"""多语言Listing写作模块 — 调用Qwen系列模型生成平台适配的Listing"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from shared.model_router import ModelRouter

LANGUAGE_CONFIG = {
    "en": {"name": "English", "flag": "🇺🇸", "model": "qwen/qwen3.7-max"},
    "ja": {"name": "日本語", "flag": "🇯🇵", "model": "qwen/qwen3.7-max"},
    "de": {"name": "Deutsch", "flag": "🇩🇪", "model": "qwen/qwen3.7-max"},
    "fr": {"name": "Français", "flag": "🇫🇷", "model": "qwen/qwen3.7-max"},
    "es": {"name": "Español", "flag": "🇪🇸", "model": "qwen/qwen3.7-max"},
}

PLATFORM_RULES = {
    "Amazon": {
        "title_max": 200,
        "bullets_max": 500,
        "search_terms_max": 250,
        "bullets_count": 5,
        "title_rule": "Title must be under 200 characters. Capitalize first letter of each word. Include brand + key feature + model + material + size/color.",
        "bullets_rule": "5 bullet points, each under 500 characters. Start each with a keyword in 【brackets】. Focus on benefits, not just features.",
        "search_terms_rule": "Under 250 bytes total. Use space-separated keywords. Do NOT repeat words already in title. Include: synonyms, common misspellings, alternative names, related categories.",
    },
    "Temu": {
        "title_max": 120,
        "bullets_max": 300,
        "search_terms_max": 200,
        "bullets_count": 3,
        "title_rule": "Title must be under 120 characters. Be concise and direct. Include main keyword + key selling point + target user.",
        "bullets_rule": "3 bullet points, each under 300 characters. Use emoji + short benefit statement. Casual, friendly tone.",
        "search_terms_rule": "Under 200 bytes. Focus on high-volume search keywords. Include use-case keywords and gift-occasion keywords.",
    },
}


def generate_listing(
    router: ModelRouter,
    product_name: str,
    product_category: str,
    features: str,
    materials: str = "",
    target_audience: str = "",
    unique_selling_points: str = "",
    platform: str = "Amazon",
    language: str = "en",
) -> dict:
    """
    为指定产品生成平台+语言适配的完整Listing。
    返回: {"title": "...", "bullets": [...], "search_terms": "...", "char_counts": {...}}
    """
    lang_cfg = LANGUAGE_CONFIG.get(language, LANGUAGE_CONFIG["en"])
    rules = PLATFORM_RULES.get(platform, PLATFORM_RULES["Amazon"])

    system_prompt = f"""You are a professional {platform} listing optimization expert specializing in the {lang_cfg['name']} marketplace. You create high-converting product listings that rank well organically and convert browsers into buyers.

Your writing style:
- Native-level fluency in {lang_cfg['name']}
- Persuasive benefits-focused copy (not just feature lists)
- SEO-optimized keyword integration that reads naturally
- Understanding of {platform}'s A9/A10 search algorithm
- Knowledge of what makes shoppers click "Add to Cart"

IMPORTANT RULES:
{rules['title_rule']}
{rules['bullets_rule']}
{rules['search_terms_rule']}

Respond ONLY in JSON format, no other text."""

    user_prompt = f"""Generate a complete {platform} {lang_cfg['name']} listing for:

PRODUCT: {product_name}
CATEGORY: {product_category}
KEY FEATURES: {features}
MATERIALS: {materials if materials else 'N/A'}
TARGET AUDIENCE: {target_audience if target_audience else 'General consumers'}
UNIQUE SELLING POINTS: {unique_selling_points if unique_selling_points else 'N/A'}

Return JSON:
{{
  "title": "...",
  "bullets": ["...", "...", {"..." if rules['bullets_count'] == 5 else ""}],
  "search_terms": "..."
}}"""

    response = router.chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        model=lang_cfg["model"],
        temperature=0.8,
    )

    content = router.extract_content(response)

    # 尝试解析JSON
    import json
    import re

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        # 尝试提取JSON块
        match = re.search(r"\{[\s\S]*\}", content)
        if match:
            data = json.loads(match.group())
        else:
            data = {"title": content[:rules["title_max"]], "bullets": ["Content generation failed"], "search_terms": ""}

    # 计算字符数
    char_counts = {
        "title": len(data.get("title", "")),
        "title_max": rules["title_max"],
        "bullets": [len(b) for b in data.get("bullets", [])],
        "bullets_max": rules["bullets_max"],
        "search_terms": len(data.get("search_terms", "")),
        "search_terms_max": rules["search_terms_max"],
    }

    return {
        "title": data.get("title", ""),
        "bullets": data.get("bullets", []),
        "search_terms": data.get("search_terms", ""),
        "char_counts": char_counts,
        "platform": platform,
        "language": language,
        "lang_name": lang_cfg["name"],
        "lang_flag": lang_cfg["flag"],
    }


def generate_multi_listing(
    router: ModelRouter,
    product_info: dict,
    platforms: list[str],
    languages: list[str],
) -> list[dict]:
    """
    批量生成多平台×多语言的Listing。
    返回: list of listing dicts
    """
    results = []
    for platform in platforms:
        for lang in languages:
            listing = generate_listing(
                router=router,
                product_name=product_info.get("name", ""),
                product_category=product_info.get("category", ""),
                features=product_info.get("features", ""),
                materials=product_info.get("materials", ""),
                target_audience=product_info.get("audience", ""),
                unique_selling_points=product_info.get("usp", ""),
                platform=platform,
                language=lang,
            )
            results.append(listing)
    return results
