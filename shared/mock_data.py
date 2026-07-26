"""
Mock Data Provider — 为无API Key时的Demo提供真实感数据
所有返回数据模拟真实API响应格式，关键词智能路由匹配上下文
"""

import random
import hashlib
import base64


class MockDataProvider:

    # ═══════════════════════════════════════════════════════
    # 文本对话响应 — 关键词路由
    # ═══════════════════════════════════════════════════════

    def get_chat_response(self, prompt: str, system: str = "") -> str:
        p = prompt.lower()
        s = system.lower()

        # Listing / 商品文案
        if any(k in p for k in ["listing", "title", "bullet", "search term", "product description", "五点", "标题", "搜索词"]):
            return self._listing_response(prompt)

        # 合规检测
        if any(k in p for k in ["compliance", "合规", "violation", "forbidden", "policy", "policy", "检测", "审查"]):
            return self._compliance_response(prompt)

        # 评论分析
        if any(k in p for k in ["review", "评论", "pain point", "sentiment", "customer feedback", "痛点"]):
            return self._review_analysis_response(prompt)

        # 竞品追踪
        if any(k in p for k in ["competitor", "竞品", "price history", "listing change", "monitor"]):
            return self._competitor_response(prompt)

        # 选品
        if any(k in p for k in ["选品", "product selection", "opportunity", "blue ocean", "market gap", "niche"]):
            return self._product_selection_response(prompt)

        # 定价
        if any(k in p for k in ["pricing", "定价", "price strategy", "促销", "discount"]):
            return self._pricing_response(prompt)

        # 趋势报告
        if any(k in p for k in ["trend", "趋势", "market report", "行业报告", "forecast"]):
            return self._trend_report_response(prompt)

        # 通用跨境专家
        return self._generic_expert_response(prompt)

    # ═══════════════════════════════════════════════════════
    # Listing 生成响应
    # ═══════════════════════════════════════════════════════

    def _listing_response(self, prompt: str) -> str:
        # 尝试识别产品类型
        product = "Your Product"
        if "earbuds" in prompt or "耳机" in prompt or "bluetooth" in prompt:
            return self._listing_bluetooth_earbuds()
        if "yoga" in prompt or "瑜伽" in prompt:
            return self._listing_yoga_mat()
        if "charger" in prompt or "充电" in prompt:
            return self._listing_charger()
        if "lamp" in prompt or "灯" in prompt:
            return self._listing_desk_lamp()
        if "water bottle" in prompt or "水杯" in prompt or "水瓶" in prompt:
            return self._listing_water_bottle()
        if "phone case" in prompt or "手机壳" in prompt:
            return self._listing_phone_case()
        if "cat" in prompt or "dog" in prompt or "宠物" in prompt:
            return self._listing_pet_toy()
        # 默认通用产品
        return self._listing_generic(prompt)

    def _listing_bluetooth_earbuds(self) -> str:
        return """【Title (Amazon US)】
Wireless Bluetooth 5.3 Earbuds with 40H Battery Life, IPX7 Waterproof Sport Earphones with ENC Noise Cancelling Mic, Deep Bass Stereo Sound for Workout Running Gym — Black

【5 Bullet Points】
• 【40-Hour Total Playtime & LED Display】Single charge delivers 8 hours of listening, with the compact charging case extending total playtime to 40 hours. The smart LED display shows remaining battery percentage at a glance, so you never run out of power unexpectedly.
• 【Bluetooth 5.3 & One-Step Pairing】Equipped with the latest Bluetooth 5.3 chip, these earbuds offer faster transmission, more stable connectivity, and lower power consumption. Open the charging case lid and they auto-connect to your last paired device in seconds.
• 【IPX7 Waterproof & Sweatproof】With IPX7 nano-coating technology, these earbuds are fully protected against rain, sweat, and splashes. Perfect for intense workouts, outdoor running, hiking, and daily commutes — no need to worry about water damage.
• 【ENC Noise Cancelling Calls】Built-in Environmental Noise Cancellation microphones filter out background noise during calls, ensuring crystal-clear voice transmission even in windy or crowded environments. Your voice comes through loud and clear.
• 【Ergonomic Design & Comfort Fit】Weighing only 4.2g per earbud, the semi-in-ear design with 3 sizes of silicone ear tips (S/M/L) provides a secure, comfortable fit for all ear shapes. Wear them all day without discomfort.

【Search Terms】
bluetooth earbuds wireless earphones, sport headphones waterproof, noise cancelling earbuds, wireless ear buds with microphone, running earbuds bluetooth 5.3, gym headphones long battery life, workout earphones ipx7, bluetooth earphones for iphone android"""

    def _listing_yoga_mat(self) -> str:
        return """【Title (Amazon US)】
Extra Thick 1/2" Premium Yoga Mat, Non-Slip Exercise Mat with Carrying Strap, Eco-Friendly TPE Material, Double-Sided Texture for Pilates Stretching Meditation — 72"x24" (Teal/Purple)

【5 Bullet Points】
• 【Extra Thick 1/2" for Joint Protection】At 12mm thickness with high-density TPE foam, this mat provides superior cushioning for knees, elbows, and spine during yoga, pilates, and floor exercises. Unlike standard 3-6mm mats, you will feel the difference on hard floors.
• 【Double-Sided Non-Slip Surface】Both sides feature our patented wave-texture pattern that grips the floor and your body. No sliding, no bunching, even during hot yoga or sweaty HIIT sessions. Laboratory tested for slip resistance exceeding ASTM standards.
• 【Eco-Friendly TPE Material】Made from 100% recyclable Thermoplastic Elastomer — free from PVC, latex, phthalates, and toxic glues. Zero chemical smell straight out of the box. Safe for you, safe for the planet.
• 【Lightweight & Portable with Strap】Weighs only 2.5 lbs and rolls up compactly to 24"x6" diameter. Includes a free carrying strap with adjustable buckle for easy transport to the studio, park, or gym. Fits in most yoga mat bags.
• 【72"x24" Extra-Long & Wide】Generous dimensions provide full-body coverage for all poses. Taller practitioners no longer need to choose between their head or feet touching the floor. Ideal for all yoga styles: Hatha, Vinyasa, Ashtanga, Bikram, restorative.

【Search Terms】
yoga mat extra thick, non slip exercise mat, tpe yoga mat eco friendly, pilates mat with carrying strap, large workout mat 72 inch, fitness mat for home gym, meditation floor mat thick, travel yoga mat lightweight"""

    def _listing_charger(self) -> str:
        return """【Title (Amazon US)】
65W USB C Fast Charger Block, GaN III Compact Wall Charger with 3-Port (2x USB-C + 1x USB-A), PD 3.0 PPS Quick Charge for iPhone 16 Pro Max Samsung Galaxy MacBook iPad — White

【5 Bullet Points】
• 【65W Ultra-Fast Charging】GaN III technology delivers up to 65W of power through a single USB-C port, charging a MacBook Air from 0% to 50% in just 30 minutes. Charges your iPhone 16 Pro Max to 60% in only 25 minutes — 3x faster than original 5W chargers.
• 【3-in-1 Multi-Port Design】Two USB-C ports and one USB-A port allow you to charge three devices simultaneously. Intelligent power distribution automatically adjusts output based on connected devices: 45W+20W, 30W+20W+15W, or 65W single-port max.
• 【GaN III Ultra-Compact】At 40% smaller than traditional 65W chargers, this pocket-sized GaN charger (2.1"x1.3"x1.3") easily fits in your bag or pocket. Weighs only 3.2 oz — the perfect travel companion without sacrificing power.
• 【Universal Compatibility】Supports PD 3.0, PPS, QC 4+, AFC, FCP, SCP fast charging protocols. Works with iPhone 16/15/14 series, Samsung Galaxy S25/S24, Google Pixel, MacBook Air/Pro, iPad Pro, Dell XPS, Surface, Steam Deck, Nintendo Switch, and more.
• 【Advanced Safety Protection】Built-in smart chip provides over-voltage, over-current, over-temperature, short-circuit, and foreign object detection protection. Certified by UL, FCC, CE, and RoHS. Fire-resistant casing for peace of mind.

【Search Terms】
65w usb c charger, gan iii charger block, fast charger for iphone 16, usb c laptop charger, 3 port wall charger, pd 3.0 quick charger, travel charger compact, macbook charger usb c, samsung fast charger"""

    def _listing_desk_lamp(self) -> str:
        return """【Title (Amazon US)】
LED Desk Lamp with Clamp, 24W Super Bright Architect Task Light, 5 Color Modes 10 Brightness Levels, Auto-Dimming Eye-Caring Reading Lamp with 1H Timer for Home Office Study — Black

【5 Bullet Points】
• 【Customizable 5 Color × 10 Brightness】5 color temperatures (3000K-6500K) and 10 brightness levels give you 50 lighting combinations. Warm light for relaxing, natural light for reading, cool white for focused work — find your perfect setting with one-touch memory recall.
• 【Space-Saving Clamp Design】The sturdy metal C-clamp mounts securely to desks up to 2.3" thick, requiring zero desk space. The gooseneck arm extends 31.5" with full 360° flexibility, positioning light exactly where you need it.
• 【Eye-Caring Technology】Flicker-free LED beads with soft diffuser panel eliminate harsh glare, shadows, and blue light hazards. The built-in ambient light sensor auto-adjusts brightness to match your environment, reducing eye strain during long work sessions.
• 【1-Hour Auto-Off Timer】Perfect for bedtime reading or reminding yourself to take breaks. The timer gently dims before shutting off, giving you time to wrap up. Includes a 30/60 minute preset option.
• 【Energy Efficient 24W LEDs】Equivalent to 150W incandescent brightness while consuming 80% less energy. Rated for 50,000+ hours of lifespan — that is over 25 years of normal use. Replaceable LED module extends the product life even further.

【Search Terms】
led desk lamp with clamp, architect task light, eye caring reading lamp, adjustable gooseneck lamp, home office desk lighting, bright led work lamp, dimmable study lamp, space saving clamp light"""

    def _listing_water_bottle(self) -> str:
        return """【Title (Amazon US)】
32oz Insulated Water Bottle with Straw Lid, Stainless Steel Vacuum Thermos, 24H Cold 12H Hot, BPA-Free Leak-Proof Sports Flask for Gym Hiking Travel — Gradient Blue

【5 Bullet Points】
• 【Double-Wall Vacuum Insulation】18/8 food-grade stainless steel with copper-coated inner wall keeps drinks ice-cold for 24 hours and piping hot for 12 hours. Laboratory tested and proven — fill with ice water at 7am, still icy at 7am next day. No exterior condensation, no sweaty hands.
• 【Two Leak-Proof Lids Included】Comes with both a flip-top straw lid (perfect for sipping at the gym, driving, or at your desk) and a wide-mouth screw-top lid (ideal for chugging, adding ice cubes, or pouring). Both lids feature silicone O-ring seals tested waterproof at all angles.
• 【BPA-Free & Taste-Free】Made from 100% BPA-free materials — the bottle, both lids, and the straw are all toxin-free. Electropolished interior surface leaves zero metallic aftertaste, so your water tastes like water, not metal. Safe for acidic drinks like lemon water and smoothies.
• 【Powder-Coated Durability】The premium gradient powder coat finish is scratch-resistant, rust-proof, and provides a secure non-slip grip. Survives drops, dings, and the chaos of your gym bag. Fits most standard car cup holders (2.9" base diameter).
• 【Wide Mouth for Easy Cleaning】The 2.2-inch wide opening accommodates ice cubes, fruit infusions, and bottle brushes with ease. Every component (bottle, lids, straw, seals) is dishwasher safe — top rack recommended for lids to preserve the silicone.

【Search Terms】
insulated water bottle 32oz, stainless steel thermos, vacuum flask with straw, leak proof sports water bottle, bpa free reusable bottle, cold water bottle 24 hours, gym water flask, travel thermal mug"""

    def _listing_phone_case(self) -> str:
        return """【Title (Amazon US)】
Military-Grade Drop Protection Phone Case for iPhone 16 Pro Max, 15ft Shockproof Slim Clear Cover with 2x Tempered Glass Screen Protector, Anti-Yellowing Magnetic Ring — Crystal Clear

【5 Bullet Points】
• 【20ft Military-Grade Drop Protection】Tested to survive 20-foot drops onto concrete — exceeding MIL-STD-810G military standards. Airbag corner cushions + raised bezels (2.5mm camera lip, 1.8mm screen lip) absorb impact and protect your $1200+ investment.
• 【Anti-Yellowing Forever Clear Technology】Our proprietary Blue-Tech resin formula with UV stabilizers resists yellowing 4x longer than standard TPU cases. The crystal-clear back stays transparent for years — backed by our lifetime anti-yellow guarantee. Show off your iPhone's original color.
• 【Built-in Super Strong Magnetic Ring】38 N52-grade magnets (vs 18 in standard cases) deliver 2x the magnetic attachment strength. Fully compatible with MagSafe chargers, car mounts, wallets, and battery packs. Perfect alignment every time with the visual guide ring.
• 【Ultra-Slim Yet Protective】At only 1.1mm thin and 29g, this case adds almost zero bulk to your iPhone 16 Pro Max. The precision cutouts allow flawless button feedback, and the tactile buttons feel just like the originals. Easy to press, satisfying click.
• 【Bonus: 2x Tempered Glass Screen Protectors】Each case includes two 9H hardness tempered glass screen protectors with an alignment frame for bubble-free installation in under 60 seconds. Oleophobic coating resists fingerprints and smudges all day.

【Search Terms】
iphone 16 pro max case, military grade drop protection, clear phone case anti yellowing, magsafe compatible case, slim shockproof iphone cover, magnetic iphone case with screen protector, crystal clear protective case, heavy duty phone case clear"""

    def _listing_pet_toy(self) -> str:
        return """【Title (Amazon US)】
Interactive Cat Toys, 7-in-1 Retractable Feather Wand with 2 Replaceable Teasers + 5 Crinkle Balls, Catnip Toy Set for Indoor Cats Kittens Exercise & Bonding

【5 Bullet Points】
• 【7-in-1 Value Pack】Includes 1 retractable wand (extends 15"-38"), 2 interchangeable feather teaser attachments, and 5 crinkle balls — everything you need for hours of interactive play. Swap teasers in seconds with the quick-release clip.
• 【Retractable & Portable】The stainless steel telescopic pole extends from 15" to 38" with a twist-lock mechanism. Retract it for storage or travel to the vet, a friend's house, or outdoor adventures. The included storage bag keeps everything organized.
• 【Stimulates Natural Hunting Instincts】The erratic flutter of the feather teaser mimics real prey movement, triggering your cat's chase-pounce-capture sequence. 15 minutes of interactive play reduces anxiety, prevents destructive behavior, and strengthens your bond.
• 【100% Natural Catnip Infused】Both feather teasers and crinkle balls are infused with premium North American-grown catnip, vacuum-sealed for maximum potency. The crinkle texture of the balls adds an extra sensory dimension that cats find irresistible.
• 【Safe & Durable Materials】All feathers are heat-sanitized and color-fixed. The wand is made from BPA-free ABS plastic with a non-slip handle. The teaser string is bite-resistant braided nylon — tested to withstand 1000+ play sessions without fraying.

【Search Terms】
interactive cat toys, feather wand cat toy, retractable cat teaser, catnip toys for indoor cats, kitten exercise toy set, crinkle balls cats, cat play wand, cat enrichment toys"""

    def _listing_generic(self, prompt: str) -> str:
        # 尝试从 prompt 提取产品名称
        return """【Title (Amazon US)】
Premium [Product Name] — High Quality, Fast Shipping, 30-Day Money-Back Guarantee

【5 Bullet Points】
• 【Premium Quality Material】Crafted from high-grade materials that are built to last. Every unit undergoes rigorous quality control inspection before shipping to ensure you receive a flawless product.
• 【Easy to Use & Versatile】Designed with simplicity in mind — no complicated setup required. Suitable for home, office, travel, and everyday use. The thoughtful design adapts to your lifestyle.
• 【Perfect Gift Choice】Beautifully packaged and ready to give. An ideal present for family, friends, and loved ones on birthdays, holidays, anniversaries, or any special occasion.
• 【Compact & Portable Design】Lightweight and space-saving, easily fits in your bag or luggage. Take it anywhere — from your daily commute to weekend getaways and international travel.
• 【100% Satisfaction Guarantee】We stand behind every product we sell. If you are not completely satisfied, contact us for a full refund or replacement within 30 days — no questions asked.

【Search Terms】
[product] premium quality, best [product] 2025, [product] for home office travel, affordable [product] gift, high rated [product]"""

    # ═══════════════════════════════════════════════════════
    # 合规检测响应
    # ═══════════════════════════════════════════════════════

    def _compliance_response(self, prompt: str) -> str:
        has_violation = random.random() > 0.4
        if not has_violation:
            return """{
  "overall_status": "PASS",
  "overall_score": 92,
  "checks": [
    {"category": "Image Quality", "status": "PASS", "score": 95, "detail": "Image resolution meets platform requirements. No pixelation, blur, or compression artifacts detected."},
    {"category": "Main Image Requirements", "status": "PASS", "score": 100, "detail": "Pure white background (RGB 255,255,255) confirmed. Product occupies 85%+ of frame. No props, text, or watermarks."},
    {"category": "Text & Logo Compliance", "status": "PASS", "score": 88, "detail": "No unauthorized logos, watermarks, or promotional text detected on the main image."},
    {"category": "Cultural Sensitivity", "status": "PASS", "score": 90, "detail": "No religious symbols, culturally sensitive imagery, or potentially offensive content detected for target market."},
    {"category": "Platform-Specific Rules", "status": "PASS", "score": 85, "detail": "Image complies with Amazon main image requirements. Product shown clearly without misleading representations."}
  ],
  "recommendations": [
    "Consider adding lifestyle images (scene/setting shots) as secondary images to improve conversion rate.",
    "Ensure all secondary images also meet platform-specific dimension requirements (minimum 1000px on longest side)."
  ]
}"""
        violations = random.choice([
            """{
  "overall_status": "FAIL",
  "overall_score": 45,
  "checks": [
    {"category": "Image Quality", "status": "FAIL", "score": 40, "detail": "Image resolution 800x800px is below Amazon's minimum 1000px requirement. Image appears pixelated on high-resolution displays.", "fix": "Resize image to at least 1000x1000px. For best results, use 2000x2000px or higher."},
    {"category": "Main Image Requirements", "status": "FAIL", "score": 20, "detail": "Background is not pure white (detected RGB 238, 242, 245 — light gray/blue tint). Product occupies only ~55% of frame instead of required 85%.", "fix": "Remove background and replace with pure white #FFFFFF. Crop or zoom so product fills 85%+ of the image frame."},
    {"category": "Text & Logo Compliance", "status": "PASS", "score": 90, "detail": "No prohibited text or branding detected on main image."},
    {"category": "Cultural Sensitivity", "status": "PASS", "score": 85, "detail": "No cultural or religious sensitivities identified for the target market."},
    {"category": "Platform-Specific Rules", "status": "FAIL", "score": 30, "detail": "Image contains a 'SALE 50% OFF' overlay text banner, which is prohibited on Amazon main images per category style guides.", "fix": "Remove all overlay text, badges, and promotional graphics. Use clean product-only imagery for main images."}
  ],
  "recommendations": [
    "URGENT: Replace main image with a 2000x2000px pure white background product shot.",
    "Remove the 'SALE 50% OFF' overlay — this violates Amazon's main image policy and may result in listing suppression.",
    "Invest in professional product photography to ensure consistent quality across all listing images."
  ]
}""",
            """{
  "overall_status": "FAIL",
  "overall_score": 38,
  "checks": [
    {"category": "Image Quality", "status": "PASS", "score": 88, "detail": "Resolution adequate at 1500x1500px. Acceptable sharpness and lighting."},
    {"category": "Main Image Requirements", "status": "PASS", "score": 90, "detail": "White background meets standard. Product fills approximately 82% of frame."},
    {"category": "Text & Logo Compliance", "status": "FAIL", "score": 15, "detail": "Competitor brand logo 'SoundMax' visible on product packaging in the image, which violates platform policies on displaying unlicensed trademarks.", "fix": "Remove or digitally edit out the competitor brand logo. Ensure only your registered brand appears on products and packaging."},
    {"category": "Cultural Sensitivity", "status": "FAIL", "score": 25, "detail": "Image contains a hand gesture (index finger and thumb forming a circle) that is considered offensive in certain Middle Eastern and South American markets.", "fix": "Replace the image with neutral hand poses or use only the product on a plain background. Research target market cultural norms before photoshoots."},
    {"category": "Platform-Specific Rules", "status": "PASS", "score": 80, "detail": "No additional platform-specific violations detected."}
  ],
  "recommendations": [
    "Remove or blur the 'SoundMax' logo from product packaging — this is a trademark violation that could result in a listing takedown.",
    "Reshoot with culturally neutral hand poses. When selling to Middle Eastern markets, avoid hand gestures entirely in product imagery.",
    "Create a compliance checklist for future product photoshoots to catch these issues before production."
  ]
}"""
        ])
        return violations

    # ═══════════════════════════════════════════════════════
    # 评论分析响应
    # ═══════════════════════════════════════════════════════

    def _review_analysis_response(self, prompt: str) -> str:
        return """## Review Analysis Report

### Sentiment Distribution
| Sentiment | Percentage | Review Count |
|-----------|-----------|-------------|
| Positive (4-5 stars) | 62% | 1,240 |
| Neutral (3 stars) | 18% | 360 |
| Negative (1-2 stars) | 20% | 400 |

### Top 5 Pain Points (ranked by frequency × severity)
1. **Battery Life Degrades After 3-4 Months** (28% of negative reviews, severity: HIGH)
   - "Battery barely lasts 2 hours after 4 months of use" — Verified Purchase
   - "Used to get 8 hours, now lucky to get 90 minutes" — Verified Purchase
   - Root cause analysis: Likely low-quality lithium battery cells without proper charge cycle management IC

2. **Bluetooth Disconnects Randomly During Calls** (22% of negative reviews, severity: HIGH)
   - "Drops connection every 10-15 minutes during Zoom calls" — Verified Purchase
   - "Right earbud disconnects while left keeps playing" — Verified Purchase
   - Root cause analysis: Antenna placement or Bluetooth firmware instability

3. **Poor Fit — Falls Out During Exercise** (18% of negative reviews, severity: MEDIUM)
   - "Even with the smallest tips, they fall out when I start running"
   - "Only stays in if I hold perfectly still — useless for gym"
   - Root cause analysis: Earbud body shape too large for smaller ear canals, limited ear tip size range

4. **Charging Case Lid Feels Flimsy** (15% of negative reviews, severity: LOW)
   - "The hinge is already loose after 2 weeks"
   - "Feels like it will snap off any day now"
   - Root cause analysis: Plastic hinge without metal reinforcement

5. **ANC/Noise Cancelling Barely Works** (12% of negative reviews, severity: MEDIUM)
   - "Can still hear my AC and keyboard typing clearly with ANC on"
   - "No difference between ANC on and off — marketing gimmick"
   - Root cause analysis: Passive isolation only, ANC feature may be defective or misleadingly advertised

### Top Feature Requests
- **Longer battery lifespan** (145 mentions) — use higher quality cells
- **Better ear fit/ergonomics** (98 mentions) — more tip sizes, wing tips
- **Stronger Bluetooth connection** (87 mentions) — antenna redesign
- **USB-C instead of Micro-USB** (72 mentions)
- **Wireless charging case** (54 mentions)

### Actionable Insights
1. **PRIORITY**: Switch to A-grade lithium polymer batteries with Texas Instruments BQ series charge management IC — increases BOM by ~$0.35/unit but eliminates #1 complaint
2. **PRIORITY**: Add Bluetooth antenna diversity (left+right earbud antennas) and update firmware to handle single-earbud fallback gracefully
3. **Quick Win**: Include 5 pairs of ear tips (XS/S/M/L/XL) + 2 pairs of memory foam tips — cost ~$0.15/unit, dramatically improves fit satisfaction
4. **Quick Win**: Metal hinge pin on charging case — $0.08/unit BOM increase
5. **Marketing Fix**: If ANC performance cannot be improved, rename feature from 'Active Noise Cancelling' to 'Environmental Noise Reduction' to set accurate expectations

### Review Velocity Trend
Week 1: 45 reviews (4.1 avg) → Week 4: 112 reviews (3.7 avg) → Trend: Rating declining as more long-term reviews come in; battery complaints accelerate after month 3"""

    # ═══════════════════════════════════════════════════════
    # 竞品追踪响应
    # ═══════════════════════════════════════════════════════

    def _competitor_response(self, prompt: str) -> str:
        return """## Competitor Intelligence Dashboard

### Monitored Competitors (Last 30 Days)
| Competitor | Current Price | Price Change | Rating | Reviews | Review Velocity |
|-----------|-------------|-------------|--------|---------|-----------------|
| SoundPro X1 | $49.99 | -$5.00 (-9%) | 4.3 ★ | 8,421 | +320/mo |
| AudioMax T3 | $59.99 | $0 (stable) | 4.5 ★ | 12,089 | +450/mo |
| BassBeats Pro | $39.99 | +$3.00 (+8%) | 4.1 ★ | 5,234 | +180/mo |
| EarFit Elite | $54.99 | -$10.00 (-15%) | 4.6 ★ | 3,891 | +210/mo |

### Price Trend Analysis
- **SoundPro X1**: Aggressive $5 price drop on July 15, likely clearing inventory before V2 launch. Their social media hints at "something new coming August."
- **EarFit Elite**: Flash sale at $44.99 (20% off) for Prime Day — returned to $54.99 after. Effective strategy to boost BSR temporarily.
- **BassBeats Pro**: Price increase signals strong demand or supply constraints. Their BSR improved from #847 to #523 despite the price hike.

### Listing Change Detection
| Competitor | Date | Change Type | Detail |
|-----------|------|------------|--------|
| SoundPro X1 | Jul 18 | Title Update | Added "2025 New Version" and "Bluetooth 5.4" to title |
| SoundPro X1 | Jul 20 | Image Update | Replaced 3 lifestyle images with higher quality photos |
| AudioMax T3 | Jul 15 | A+ Content | Added comparison chart module showing advantage over "generic earbuds" |
| EarFit Elite | Jul 22 | Bullet Points | Rewrote bullets 1 & 2, now emphasizing "comfort" and "14-day trial" |
| BassBeats Pro | Jul 10 | Price | Raised price from $36.99 → $39.99 (+8.1%) |

### Strategic Analysis
- **SoundPro** is preparing for a V2 launch — expect a new listing within 4-6 weeks that may cannibalize their own V1 sales. Opportunity: capture their V1 customers who feel abandoned.
- **AudioMax** is the category leader and appears to be focusing on A+ Content to improve conversion. Their strategy is brand-building, not price competition.
- **EarFit Elite** discovered that "comfort" is their unique selling point (per review analysis) and is pivoting their messaging accordingly. Smart move.

### Recommended Actions
1. Monitor SoundPro's V2 launch closely — set up alerts for new ASINs in this subcategory
2. Consider a comfort-focused differentiation strategy (like EarFit Elite) — this appears underserved
3. Prime Day price point of $39.99-$44.99 generated highest sales velocity for the category"""

    # ═══════════════════════════════════════════════════════
    # 选品推荐响应
    # ═══════════════════════════════════════════════════════

    def _product_selection_response(self, prompt: str) -> str:
        return """## Product Opportunity Discovery Report

### Top 5 Niche Opportunities (Scored 0-100)
| Rank | Niche | Opp. Score | Search Vol Trend | Competition | Avg. Price | Entry Difficulty |
|------|-------|-----------|-----------------|------------|-----------|-----------------|
| 1 | Open-Ear Air Conduction Earbuds | 87/100 | +62% YoY | Medium | $59.99 | Moderate |
| 2 | Kids' Volume-Limited Headphones (BLE) | 82/100 | +38% YoY | Low | $29.99 | Easy |
| 3 | Magnetic Charging 3-in-1 Stands (Qi2) | 78/100 | +55% YoY | Medium-High | $39.99 | Moderate |
| 4 | USB-C Retro Mechanical Numpads | 74/100 | +85% YoY | Low | $34.99 | Easy |
| 5 | Eco-Friendly Biodegradable Phone Cases | 71/100 | +28% YoY | Low-Medium | $24.99 | Easy |

### Deep Dive: #1 Open-Ear Air Conduction Earbuds
**Why this opportunity exists:**
- Safety-conscious runners and cyclists are actively seeking alternatives to in-ear buds
- Existing products (Shokz, Oladance) are priced $79-$179 — massive gap at $40-$60
- Patent landscape: key bone conduction patents expiring 2025-2026
- Search volume for "open ear earbuds" grew from 12,000/mo → 32,000/mo in 6 months

**Market Gap Analysis:**
| Feature | Premium Tier ($100+) | Your Opportunity ($50) |
|---------|---------------------|----------------------|
| Audio Quality | Hi-Res, LDAC | AAC/SBC acceptable |
| Battery Life | 8-10 hours | 6-8 hours competitive |
| Water Resistance | IP67 | IPX5 sufficient |
| Multipoint BT | Standard | Must-have feature |
| App Support | Full EQ | Basic EQ presets |

**Entry Strategy:**
1. Target "good enough" audio with superior comfort and battery at half the premium price
2. Launch with 3 color variants targeting the fitness/sport aesthetic
3. Amazon PPC: target "open ear headphones running" (low competition, 32% conversion rate)
4. Influencer seeding: 20 running/fitness micro-influencers (5K-50K followers) for authentic reviews
5. Estimated TAM: $280M growing at 35% CAGR

### Blue Ocean Indicators
- **Kids' Volume-Limited Headphones**: Only 3 established competitors, avg rating 4.0★ (easily beatable with 4.3+ product), parent pain points clear in reviews
- **USB-C Retro Numpads**: Exploding mechanical keyboard community, zero major brands in numpad-only space, keyboard YouTubers hungry for content

### Risk Factors to Monitor
- Tariff changes on electronics from China (Section 301 review pending)
- Bluetooth SIG certification timeline (8-12 weeks for new products)
- Apple potentially entering open-ear category (patent filings suggest interest)"""

    # ═══════════════════════════════════════════════════════
    # 定价策略响应
    # ═══════════════════════════════════════════════════════

    def _pricing_response(self, prompt: str) -> str:
        return """## Pricing Strategy Report

### Recommended Price Point: $44.99

### Price Elasticity Analysis
| Price Point | Est. Daily Units | Daily Revenue | Monthly Profit (30% margin) |
|------------|-----------------|--------------|---------------------------|
| $34.99 | 85 | $2,974 | $8,030 |
| $39.99 | 72 | $2,879 | $7,774 |
| $44.99 ★ | 60 | $2,699 | $7,287 |
| $49.99 | 48 | $2,399 | $6,478 |
| $54.99 | 32 | $1,760 | $4,751 |
| $59.99 | 20 | $1,200 | $3,239 |

★ Recommended: Optimal balance of unit volume and per-unit margin

### Strategy Timeline
**Launch Phase (Days 1-14)**
- Launch price: $39.99 (introductory discount, 11% off target price)
- Strategy: Aggressive PPC at $200/day budget, target ACOS 40-50%
- Goal: 30+ verified reviews, BSR under #5,000 in subcategory

**Growth Phase (Days 15-45)**
- Raise to $44.99 target price
- PPC budget: $150/day, target ACOS 25-30%
- Enable coupons: 5% off for subscribers (drives conversion without price dilution)
- Goal: BSR under #2,000, organic rank page 1 for 5+ keywords

**Maturity Phase (Days 46-90+)**
- Maintain $44.99 base price
- PPC budget: $100/day, target ACOS 15-20%
- Introduce bundle: product + accessory → $54.99 (increases AOV)
- Goal: BSR under #1,000, profitability target achieved

### Promotional Calendar
| Month | Event | Strategy | Discount |
|-------|-------|----------|----------|
| October | Prime Fall Deal | Lightning Deal | 20% off ($35.99) |
| November | Black Friday | 7-day Deal of the Day | 25% off ($33.74) |
| December | Holiday Shopping | Coupon + Gift Wrap option | 10% off coupon |
| January | New Year Fitness | Bundle with gym accessory | 15% off bundle |

### Break-Even Analysis
- **COGS**: $18.50/unit (at 5,000 unit order quantity)
- **FBA fees**: $5.32/unit (standard size, 4-8oz)
- **Referral fee**: $6.75/unit (15% of $44.99)
- **PPC per unit**: $4.50/unit (at 10% ACOS target)
- **Total unit cost**: $35.07
- **Unit profit**: $9.92 (22% margin)
- **Monthly break-even**: ~1,100 units at target price

### Competitive Price Positioning
```
                    BassBeats Pro    Your Product    SoundPro X1    AudioMax T3
                        $39.99          $44.99          $49.99         $59.99
Rating:                  4.1★            4.4★ (target)   4.3★           4.5★
Features:               Basic            Premium         Premium        Premium
Positioning:           Budget          Value-Leader    Performance     Premium
```
Your product occupies the "value-leader" sweet spot — premium features at a mid-range price point, directly above the budget option but significantly below the premium tier."""

    # ═══════════════════════════════════════════════════════
    # 趋势报告响应
    # ═══════════════════════════════════════════════════════

    def _trend_report_response(self, prompt: str) -> str:
        return """## Cross-Border E-Commerce Market Trend Report
### Category: Consumer Electronics — Personal Audio
### Period: Q3 2026 Outlook

---

### Executive Summary
The global personal audio market is projected to reach $58.4B in 2026, growing at a 12.4% CAGR. Three disruptive shifts are reshaping the competitive landscape: the transition from in-ear to open-ear form factors, mandatory USB-C compliance (EU Regulation 2024/2825 effective Dec 2026), and AI-powered audio features (real-time translation, adaptive EQ) becoming table stakes.

### Market Size & Growth
| Segment | 2025 Size | 2026 Projected | Growth |
|---------|----------|---------------|--------|
| TWS Earbuds | $32.1B | $35.6B | +10.9% |
| Open-Ear / Air Conduction | $2.8B | $4.2B | +50.0% |
| Over-Ear Headphones | $12.5B | $13.1B | +4.8% |
| Kids Audio | $1.9B | $2.3B | +21.1% |
| Gaming Headsets | $3.8B | $4.1B | +7.9% |

### Key Trends Reshaping the Market
1. **Open-Ear Revolution (STRONG SIGNAL)** — 50% YoY growth driven by safety-conscious consumers and improvements in air conduction technology. Shokz no longer has the category to themselves. Multiple white-label ODM solutions now available at $15-25 COGS.

2. **USB-C Mandate Creates Opportunity (CERTAIN)** — EU Common Charger Regulation takes full effect December 28, 2026. All new audio products sold in EU/EEA must use USB-C. Lightning-ecosystem accessory market ($4.2B) will need complete refresh.

3. **AI Audio Features Going Mainstream (EMERGING)** — Real-time translation earbuds (Timekettle, Google Pixel Buds), AI adaptive EQ (AirPods Pro), and AI hearing assistance features (FDA OTC hearing aid category) are converging. The $50 price point with AI features is the new battleground.

4. **Sustainability Differentiation (GROWING)** — 64% of Gen Z consumers consider sustainability in electronics purchases (McKinsey 2025). Products using recycled ocean plastic, biodegradable packaging, and modular/repairable design command 12-18% price premium.

5. **Social Commerce Driving Discovery (ACCELERATING)** — TikTok Shop now accounts for 22% of consumer electronics discovery among 18-34 demographic. Products that "demo well" in 60-second videos have a structural advantage.

### Consumer Behavior Shifts
- **"Right to Repair" sentiment**: Products with replaceable batteries and repairable designs see 23% higher customer satisfaction scores
- **"Try before you buy"**: 40% of consumers now expect free returns/exchanges, making return rate management a critical business function
- **"One device, all ecosystems"**: Multi-platform compatibility (iOS + Android + Windows + macOS) is now a baseline expectation

### Regulatory Watch
| Regulation | Effective Date | Impact | Preparation |
|-----------|---------------|--------|------------|
| EU USB-C Mandate | Dec 28, 2026 | Must use USB-C for all audio products | Source USB-C components now |
| EU Digital Product Passport | Jan 2027 | Supply chain transparency required | Begin supplier documentation |
| EU Battery Regulation | Feb 2027 | Replaceable batteries in portable electronics | Design for removable battery |
| US INFORM Consumers Act | Active | Identity verification for high-volume sellers | Already compliant |

### Recommended Actions (Priority Order)
1. **LAUNCH open-ear earbuds within 90 days** — fastest-growing segment, still underserved at $40-60 price point, ODM solutions readily available
2. **TRANSITION all products to USB-C** — get ahead of EU mandate, market as "future-proof" now, avoid stranded Lightning inventory in Q4
3. **DEVELOP eco-friendly product line** — start with biodegradable packaging (easy win), then recycled materials for product body (differentiation)
4. **INVEST in TikTok-first marketing** — short-form video content showing product demos, user-generated reviews, and "unboxing experience"
5. **PREPARE for EU Digital Product Passport** — start documenting supply chain now, it takes 6+ months for a typical consumer electronics supply chain audit

### Data Sources & Methodology
- Amazon BSR data (Keepa, Jungle Scout): 50,000+ ASINs tracked across 5 marketplaces
- Google Trends: 120 keyword groups monitored weekly
- Social listening: Brand24 + manual TikTok/Reddit analysis
- Industry reports: Grand View Research, Counterpoint, Canalys Q1 2026
- Customs/trade data: Panjiva import records, USITC HTS code analysis"""

    # ═══════════════════════════════════════════════════════
    # 通用专家响应
    # ═══════════════════════════════════════════════════════

    def _generic_expert_response(self, prompt: str) -> str:
        responses = [
            "Based on my analysis of the cross-border e-commerce landscape, I recommend focusing on three key areas: (1) AI-powered content localization that goes beyond translation to cultural adaptation, (2) automated compliance checking for multi-market regulations, and (3) data-driven pricing optimization using competitive intelligence. Would you like me to dive deeper into any of these areas?",

            "That is an excellent question for a cross-border seller. From my analysis of top-performing Amazon listings across US, EU, and JP marketplaces, the most successful sellers are leveraging AI in three ways: automated listing optimization, dynamic pricing, and review sentiment analysis to drive product improvements. The key differentiator is speed — AI reduces the listing-to-optimization cycle from weeks to hours.",

            "Looking at the data from 50,000+ cross-border listings, I can share that products with AI-optimized listings (title, bullets, A+ content) see an average 34% higher conversion rate compared to manually created listings. The biggest impact comes from culturally-adapted imagery and locally-resonant copy — not just translation, but true localization for each target market.",
        ]
        return random.choice(responses)

    # ═══════════════════════════════════════════════════════
    # 图片生成 → 返回占位图URL
    # ═══════════════════════════════════════════════════════

    def get_image_urls(self, prompt: str, n: int = 1, size: str = "1024x1024") -> list[str]:
        urls = []
        for i in range(n):
            urls.append(self._generate_placeholder_image(prompt, i, size))
        return urls

    def _generate_placeholder_image(self, prompt: str, index: int, size: str) -> str:
        # 生成带产品信息的SVG占位图
        product_name = self._extract_product_from_prompt(prompt)
        image_type = self._extract_image_type(prompt)

        colors = {
            "white background": ("#FFFFFF", "#333333"),
            "lifestyle": ("#F5F0E8", "#2C3E50"),
            "model": ("#EDE7F6", "#1A237E"),
            "scene": ("#E8F5E9", "#1B5E20"),
            "default": ("#F8F9FA", "#495057"),
        }
        bg, text_color = colors.get(image_type, colors["default"])

        # 分辨率适配
        w, h = 800, 800
        if "1024" in size:
            w, h = 1024, 1024
        elif "512" in size:
            w, h = 512, 512

        type_labels = {
            "white background": "WHITE BACKGROUND",
            "lifestyle": "LIFESTYLE SHOT",
            "model": "MODEL SHOT",
            "scene": "SCENE SHOT",
            "default": "PRODUCT IMAGE",
        }
        type_label = type_labels.get(image_type, type_labels["default"])

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{bg};stop-opacity:1"/>
      <stop offset="100%" style="stop-color:#E0E0E0;stop-opacity:1"/>
    </linearGradient>
  </defs>
  <rect width="{w}" height="{h}" fill="url(#bg)"/>
  <rect x="{w*0.1}" y="{h*0.35}" width="{w*0.8}" height="{h*0.3}" rx="16" fill="white" stroke="#CCC" stroke-width="2" opacity="0.9"/>
  <text x="{w/2}" y="{h*0.48}" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-size="{w*0.04}" fill="{text_color}" font-weight="bold">{product_name[:40]}</text>
  <text x="{w/2}" y="{h*0.56}" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-size="{w*0.03}" fill="#888">{type_label}</text>
  <text x="{w/2}" y="{h*0.64}" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-size="{w*0.025}" fill="#AAA">{size}px — Mock Preview</text>
  <text x="{w/2}" y="{h*0.88}" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-size="{w*0.02}" fill="#BBB">Connect API Key to generate real images</text>
</svg>"""
        b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
        return f"data:image/svg+xml;base64,{b64}"

    def _extract_product_from_prompt(self, prompt: str) -> str:
        p = prompt.lower()
        if "earbuds" in p or "耳机" in p:
            return "Bluetooth Earbuds"
        if "yoga" in p or "瑜伽" in p:
            return "Yoga Mat"
        if "charger" in p or "充电" in p:
            return "USB-C Charger"
        if "lamp" in p or "灯" in p:
            return "Desk Lamp"
        if "bottle" in p or "水杯" in p:
            return "Water Bottle"
        if "phone case" in p or "手机壳" in p:
            return "Phone Case"
        if "toy" in p or "宠物" in p:
            return "Pet Toy"
        return "Product"

    def _extract_image_type(self, prompt: str) -> str:
        p = prompt.lower()
        if "white" in p or "白底" in p or "pure" in p:
            return "white background"
        if "lifestyle" in p or "场景" in p or "living" in p or "office" in p:
            return "lifestyle"
        if "model" in p or "模特" in p or "person" in p or "wear" in p:
            return "model"
        if "scene" in p or "环境" in p:
            return "scene"
        return "default"

    # ═══════════════════════════════════════════════════════
    # 视觉理解响应 (合规检测用)
    # ═══════════════════════════════════════════════════════

    def get_vision_response(self, image_urls: list[str], prompt: str) -> str:
        # 模拟视觉模型对图片的分析
        if "compliance" in prompt.lower() or "合规" in prompt:
            return self._compliance_response(prompt)
        return """Image Analysis Results:
- Main subject detected: Consumer electronics product
- Background: White (#FEFEFE) — 98.7% white coverage, acceptable
- Text overlay: None detected
- Product coverage: ~82% of frame
- Image quality: Sharp, no motion blur or compression artifacts
- Color profile: sRGB, suitable for web display
- Recommendation: Minor adjustment — increase product coverage to 85%+ for Amazon compliance"""
