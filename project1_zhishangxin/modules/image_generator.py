"""商品图生成模块 — 调用 wan2.7-image-pro 生成多类型商品图"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from shared.model_router import ModelRouter


IMAGE_PROMPTS = {
    "white_bg": {
        "template": "Professional product photography of {product_name}, pure white background (#FFFFFF), studio lighting, no shadows on background, Amazon product main image standard, {size}px, commercial photography quality, product fills 85%+ of frame, sharp focus, no props, no text",
        "model": "qwen/wan2.7-image-pro",
    },
    "lifestyle": {
        "template": "{product_name} in a {setting}, natural warm lighting, lifestyle photography, authentic real-world usage scene, shallow depth of field, {size}px, editorial style, aspirational aesthetic, Target and West Elm catalog style",
        "model": "qwen/wan2.7-image-pro",
    },
    "model": {
        "template": "{product_name} being used by a {model_desc}, professional model photography, clean modern studio, well-lit, {size}px, e-commerce fashion style, natural pose, smiling, genuine usage moment",
        "model": "qwen/wan2.7-image-pro",
    },
    "comparison": {
        "template": "Before and after comparison of {product_name}, split screen layout, left side showing problem or competitor, right side showing {product_name} solution, clean infographic style, {size}px, clear labels, professional design",
        "model": "qwen/wan2.7-image-pro",
    },
    "detail": {
        "template": "Extreme close-up macro shot of {product_name} details, showing material texture and build quality, macro lens effect, {size}px, shallow depth of field, premium product photography, highlight craftsmanship",
        "model": "qwen/wan2.7-image-pro",
    },
}

SETTINGS = {
    "home_office": "modern minimalist home office with natural sunlight, plants, and wooden desk",
    "kitchen": "bright modern kitchen with marble countertops and morning sunlight",
    "outdoor": "sunny park with green grass and trees, golden hour lighting",
    "gym": "modern fitness studio with equipment, clean and bright",
    "bedroom": "cozy bedroom with morning sunlight, white bedding, Scandinavian style",
    "coffee_shop": "trendy coffee shop interior, warm ambient lighting, wooden tables",
    "travel": "airport lounge or hotel room, sophisticated travel aesthetic",
    "living_room": "bright contemporary living room, neutral tones, natural light",
}

MODEL_DESC = {
    "male_young": "young athletic male model in his 20s, casual sportswear, genuine smile",
    "female_young": "young female model in her 20s, athletic casual wear, natural expression",
    "professional": "professional model in business casual attire, confident demeanor",
    "family": "family of three in a warm home setting, genuine interaction",
}


def generate_product_images(
    router: ModelRouter,
    product_name: str,
    product_category: str,
    image_types: list[str],
    style_prompt: str = "",
    size: str = "1024x1024",
    setting: str = "home_office",
    model_desc: str = "male_young",
) -> list[dict]:
    """
    为产品生成多张商品图。
    返回: [{"type": "...", "url": "...", "prompt": "..."}, ...]
    """
    results = []
    setting_text = SETTINGS.get(setting, SETTINGS["home_office"])
    model_text = MODEL_DESC.get(model_desc, MODEL_DESC["male_young"])

    for img_type in image_types:
        if img_type not in IMAGE_PROMPTS:
            continue

        cfg = IMAGE_PROMPTS[img_type]
        prompt = cfg["template"].format(
            product_name=product_name,
            setting=setting_text,
            model_desc=model_text,
            size=size.split("x")[0],
        )
        if style_prompt:
            prompt = f"{prompt}, {style_prompt}"

        response = router.generate_image(
            prompt=prompt,
            model=cfg["model"],
            n=1,
            size=size,
        )

        urls = router.extract_image_urls(response)
        results.append({
            "type": img_type,
            "url": urls[0] if urls else None,
            "prompt": prompt,
            "size": size,
        })

    return results


def generate_image_prompt(product_name: str, image_type: str, **kwargs) -> str:
    """预览生成将使用的prompt"""
    if image_type not in IMAGE_PROMPTS:
        return ""
    cfg = IMAGE_PROMPTS[image_type]
    return cfg["template"].format(
        product_name=product_name,
        setting=SETTINGS.get(kwargs.get("setting", "home_office"), SETTINGS["home_office"]),
        model_desc=MODEL_DESC.get(kwargs.get("model_desc", "male_young"), MODEL_DESC["male_young"]),
        size=kwargs.get("size", "1024"),
    )
