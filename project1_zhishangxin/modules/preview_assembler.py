"""详情页预览组装模块 — 将生成的图片+Listing组合为完整预览页"""

PREVIEW_TEMPLATES = {
    "Amazon": """
<div style="max-width:800px;margin:0 auto;font-family:'Amazon Ember',Arial,sans-serif;color:#0F1111">
    <!-- 主图区 -->
    <div style="display:flex;gap:16px;margin-bottom:24px">
        <div style="flex:1;background:#f8f8f8;border-radius:8px;display:flex;align-items:center;justify-content:center;min-height:400px;overflow:hidden">
            {main_image}
        </div>
        <div style="display:flex;flex-direction:column;gap:8px;width:80px">
            {thumbnails}
        </div>
    </div>
    <!-- 标题 -->
    <h1 style="font-size:24px;line-height:1.3;margin-bottom:8px;font-weight:500">{title}</h1>
    <!-- 评分 -->
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:16px;color:#C7511F">
        <span style="font-size:18px">★★★★☆</span>
        <span style="color:#007185">4.3 rating from 2,847 reviews</span>
    </div>
    <!-- 价格 -->
    <div style="margin-bottom:16px">
        <span style="font-size:28px;color:#B12704">$44.99</span>
        <span style="color:#565959;margin-left:8px;text-decoration:line-through">$59.99</span>
        <span style="color:#565959;margin-left:8px">Save 25%</span>
    </div>
    <!-- 五点描述 -->
    <div style="border-top:1px solid #e7e7e7;padding-top:16px;margin-bottom:16px">
        <h3 style="font-size:16px;margin-bottom:8px">About this item</h3>
        <ul style="list-style:none;padding:0;margin:0">
            {bullets}
        </ul>
    </div>
    <!-- 商品图区 -->
    {image_gallery}
    <div style="border-top:1px solid #e7e7e7;padding-top:12px;margin-top:20px;color:#565959;font-size:12px">
        Platform: Amazon | Marketplace: {marketplace} | AI-Generated Preview
    </div>
</div>""",

    "Temu": """
<div style="max-width:600px;margin:0 auto;font-family:-apple-system,BlinkMacSystemFont,sans-serif;color:#222">
    <!-- 主图轮播 -->
    <div style="background:#f5f5f5;border-radius:12px;display:flex;align-items:center;justify-content:center;min-height:400px;overflow:hidden;margin-bottom:12px">
        {main_image}
    </div>
    <!-- 小图导航 -->
    <div style="display:flex;gap:8px;margin-bottom:16px;overflow-x:auto">
        {thumbnails}
    </div>
    <!-- 标题 -->
    <h2 style="font-size:18px;line-height:1.4;margin-bottom:8px;font-weight:600">{title}</h2>
    <!-- 价格 -->
    <div style="display:flex;align-items:baseline;gap:8px;margin-bottom:12px">
        <span style="font-size:24px;color:#FB7701;font-weight:700">$39.99</span>
        <span style="color:#999;text-decoration:line-through;font-size:14px">$59.99</span>
        <span style="background:#FB7701;color:white;padding:2px 6px;border-radius:4px;font-size:12px">-33%</span>
    </div>
    <!-- 卖点 -->
    <div style="background:#FFF7EF;border-radius:8px;padding:12px;margin-bottom:12px">
        {bullets}
    </div>
    <!-- 商品图 -->
    {image_gallery}
    <div style="border-top:1px solid #eee;padding-top:12px;margin-top:20px;color:#999;font-size:11px">
        Platform: Temu | AI-Generated Preview
    </div>
</div>""",

    "独立站": """
<div style="max-width:1000px;margin:0 auto;font-family:'Segoe UI',system-ui,sans-serif">
    <!-- 双栏布局 -->
    <div style="display:flex;gap:40px">
        <div style="flex:1">
            <div style="background:#f8f8f8;border-radius:12px;overflow:hidden;margin-bottom:16px">
                {main_image}
            </div>
            <div style="display:flex;gap:8px">
                {thumbnails}
            </div>
        </div>
        <div style="flex:1;padding-top:20px">
            <p style="color:#666;text-transform:uppercase;letter-spacing:2px;font-size:12px;margin-bottom:8px">{category}</p>
            <h1 style="font-size:32px;font-weight:300;margin-bottom:16px;line-height:1.2">{title}</h1>
            <div style="font-size:28px;font-weight:600;margin-bottom:24px">$49.99 <span style="color:#999;font-size:16px;font-weight:400;text-decoration:line-through;margin-left:8px">$69.99</span></div>
            <div style="margin-bottom:24px">
                {bullets}
            </div>
            <button style="background:#000;color:white;border:none;padding:14px 40px;font-size:16px;border-radius:6px;cursor:pointer;width:100%">Add to Cart</button>
            <p style="text-align:center;color:#666;font-size:13px;margin-top:12px">Free shipping on orders over $35 · 30-day returns</p>
        </div>
    </div>
    {image_gallery}
</div>""",
}


def assemble_preview(
    images: list[dict],
    listing: dict,
    template: str = "Amazon",
    marketplace: str = "US",
    category: str = "",
) -> str:
    """
    将图片和Listing组装为完整的详情页预览HTML。
    返回: HTML string
    """
    tpl = PREVIEW_TEMPLATES.get(template, PREVIEW_TEMPLATES["Amazon"])

    # 主图
    main_img = images[0] if images else None
    main_image_html = (
        f'<img src="{main_img["url"]}" style="width:100%;height:100%;object-fit:contain" alt="Product main image">'
        if main_img
        else '<div style="width:100%;height:400px;background:#eee;display:flex;align-items:center;justify-content:center;color:#999">No Image</div>'
    )

    # 缩略图
    thumb_html = ""
    for img in images[:6]:
        thumb_html += f'<div style="width:80px;height:80px;border:1px solid #ddd;border-radius:4px;overflow:hidden;cursor:pointer"><img src="{img["url"]}" style="width:100%;height:100%;object-fit:cover" alt="thumbnail"></div>\n'

    # 标题
    title = listing.get("title", "Product Title") if listing else "Product Title"

    # 五点
    bullets = listing.get("bullets", []) if listing else []
    if template == "Temu":
        bullets_html = "".join(
            f'<div style="display:flex;align-items:flex-start;gap:8px;margin-bottom:8px;font-size:14px"><span>✓</span><span>{b}</span></div>'
            for b in bullets[:3]
        )
    elif template == "独立站":
        bullets_html = "".join(
            f'<div style="display:flex;align-items:flex-start;gap:8px;margin-bottom:8px;font-size:14px;color:#555"><span style="color:#000">✓</span><span>{b}</span></div>'
            for b in bullets[:5]
        )
    else:
        bullets_html = "".join(
            f'<li style="margin-bottom:6px;line-height:1.5;list-style:disc;margin-left:20px">{b}</li>'
            for b in bullets[:5]
        )

    # 图片画廊
    gallery_html = ""
    if len(images) > 1:
        gallery_html = '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:16px;margin-top:24px">'
        for img in images[1:]:
            gallery_html += f'<div style="background:#f8f8f8;border-radius:8px;overflow:hidden;aspect-ratio:1"><img src="{img["url"]}" style="width:100%;height:100%;object-fit:contain" alt="product image"></div>'
        gallery_html += "</div>"

    html = tpl.format(
        main_image=main_image_html,
        thumbnails=thumb_html,
        title=title,
        bullets=bullets_html,
        image_gallery=gallery_html,
        marketplace=marketplace,
        category=category or "General",
    )

    return html
