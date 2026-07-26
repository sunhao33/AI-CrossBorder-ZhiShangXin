# 跨境智上 — AI智能上新平台

> AI+跨境黑客松巅峰赛 · 项目一 | 团队：你说的都

**一句话定义**：为跨境品牌卖家提供一站式AI上新解决方案，自动完成商品图生成→多语言Listing→合规检测→详情页组装，将上架效率提升50倍。

---

## 项目背景

跨境电商卖家每上一个新品，平均需要：
- 📸 拍摄商品图：2-3天（找摄影师、布景、修图）
- ✍️ 撰写Listing：1-2天（不同语言、不同平台格式各异）
- 🔍 合规检查：1天（各市场规则不同，容易遗漏）

**跨境智上** 用AI将整个流程压缩至分钟级。

---

## 核心功能

| 功能 | 说明 | 调用的AI模型 |
|------|------|------------|
| 🎨 商品图生成 | 白底图/场景图/模特图/对比图/细节图 | wan2.7-image-pro |
| 📝 Listing写作 | 5语言×2平台，自动生成标题+五点+搜索词 | Qwen 3.7 Max |
| 🔍 合规检测 | 美/欧/日/中东/东南亚5大市场规范检测 | qwen3-vl-plus |
| 🖼️ 详情页预览 | Amazon/Temu/独立站3套模板自动组装 | — |

---

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动应用
cd project1_zhishangxin
streamlit run app.py

# 3. 打开浏览器访问 http://localhost:8501
```

> **Mock模式**：无需API Key即可体验完整功能。在侧边栏输入Model Router API Key后自动切换为真实AI生成模式。

---

## 项目结构

```
project1_zhishangxin/
├── app.py                      # Streamlit 主入口
├── config.py                   # 平台/图片/合规配置
├── modules/                    # 业务逻辑（纯Python，可复用）
│   ├── image_generator.py      # 图片生成Prompt工程
│   ├── listing_writer.py       # 多语言Listing生成
│   ├── compliance_checker.py   # 跨境合规检测
│   └── preview_assembler.py    # HTML详情页组装
├── components/                 # UI组件（Streamlit渲染层）
│   ├── sidebar.py              # 侧边栏
│   ├── image_tab.py            # 商品图生成页
│   ├── listing_tab.py          # Listing写作页
│   ├── compliance_tab.py       # 合规检测页
│   └── preview_tab.py          # 详情页预览页
└── shared/                     # 共享模块
    ├── model_router.py         # Model Router API 统一客户端
    └── mock_data.py            # Mock数据生成器
```

---

## 技术架构

```
┌─────────────────────────────────┐
│   Streamlit Web UI (4 Tab)      │  ← 用户交互层
├─────────────────────────────────┤
│   Modules (pure Python)         │  ← 业务逻辑层
│   Image / Listing / Compliance  │
├─────────────────────────────────┤
│   ModelRouter (shared)          │  ← AI调用层
│   Mock ⇄ Real (zero-code swap)  │
├─────────────────────────────────┤
│   Model Router API (126 models) │  ← 阿里云百炼
│   wan2.7 / Qwen / DeepSeek ...  │
└─────────────────────────────────┘
```

---

## 技术栈

- **前端**: Streamlit
- **AI**: 阿里云百炼 Model Router API
- **图片生成**: wan2.7-image-pro
- **文本生成**: Qwen 3.7 Max
- **视觉理解**: qwen3-vl-plus
- **语言**: Python 3.11+

---

## 比赛信息

- 赛事：AI+跨境黑客松巅峰赛
- 命题场景：AI 智能上新
- 初赛截止：2026年8月20日
