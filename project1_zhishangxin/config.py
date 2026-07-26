"""项目一配置：跨境智上 — AI智能上新平台"""

PLATFORMS = {
    "Amazon US": {"marketplace": "amazon.com", "lang": "en", "title_max": 200, "bullets_max": 500, "search_terms_max": 250},
    "Amazon JP": {"marketplace": "amazon.co.jp", "lang": "ja", "title_max": 200, "bullets_max": 500, "search_terms_max": 250},
    "Amazon DE": {"marketplace": "amazon.de", "lang": "de", "title_max": 200, "bullets_max": 500, "search_terms_max": 250},
    "Amazon FR": {"marketplace": "amazon.fr", "lang": "fr", "title_max": 200, "bullets_max": 500, "search_terms_max": 250},
    "Amazon ES": {"marketplace": "amazon.es", "lang": "es", "title_max": 200, "bullets_max": 500, "search_terms_max": 250},
    "Temu US": {"marketplace": "temu.com", "lang": "en", "title_max": 120, "bullets_max": 300, "search_terms_max": 200},
}

IMAGE_TYPES = [
    {"id": "white_bg", "name": "白底主图", "desc": "纯白背景产品主图，符合Amazon/Temu首图规范"},
    {"id": "lifestyle", "name": "场景图", "desc": "产品在生活/使用场景中的展示图"},
    {"id": "model", "name": "模特图", "desc": "模特佩戴/使用产品的展示图"},
    {"id": "comparison", "name": "对比图", "desc": "产品尺寸/功能对比展示图"},
    {"id": "detail", "name": "细节图", "desc": "产品材质/工艺/功能细节特写"},
]

IMAGE_SIZES = {
    "Amazon 主图": "2000x2000",
    "Amazon 辅图": "1000x1000",
    "Temu 主图": "800x800",
    "Temu 辅图": "600x600",
    "独立站通用": "1024x1024",
}

TARGET_MARKETS = [
    {"id": "us", "name": "美国市场", "flag": "🇺🇸"},
    {"id": "eu", "name": "欧盟市场", "flag": "🇪🇺"},
    {"id": "jp", "name": "日本市场", "flag": "🇯🇵"},
    {"id": "me", "name": "中东市场", "flag": "🇸🇦"},
    {"id": "sea", "name": "东南亚市场", "flag": "🇸🇬"},
]

COMPLIANCE_CHECKS = [
    {"id": "image_quality", "name": "图片质量", "description": "分辨率、清晰度、噪点检测"},
    {"id": "background", "name": "背景要求", "description": "白底纯度、产品占比检测"},
    {"id": "text_logo", "name": "文字/Logo合规", "description": "未授权商标、促销文字、水印检测"},
    {"id": "cultural", "name": "文化敏感", "description": "宗教符号、禁忌手势、文化冒犯"},
    {"id": "platform_rules", "name": "平台规则", "description": "特定平台图片规范检测"},
]
