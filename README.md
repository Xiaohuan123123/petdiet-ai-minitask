# 🐾 宠食记 PetDiet AI

基于 DeepSeek 大模型的宠物饮食健康助手，AI 为你定制专属宠物食谱。

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![DeepSeek](https://img.shields.io/badge/DeepSeek-AI-orange)

---

## 🚀 快速启动（只需两步）

### 前置条件

- Python 3.8 或更高版本
- DeepSeek API Key — [免费获取](https://platform.deepseek.com)（注册后在 API Keys 页面创建）

### Step 1：双击 `start.bat`

脚本会自动完成：检查 Python → 安装依赖包 → 创建 `.env` 配置 → 启动服务。

> Mac/Linux 用户运行 `chmod +x start.sh && ./start.sh`

### Step 2：浏览器自动打开

- **展示首页**：http://localhost:5000 — 产品介绍、功能展示、用户评价
- **Demo 应用**：http://localhost:5000/app — AI 聊天、食谱生成、一键购物车

如果是第一次启动，`.env` 文件会自动生成模板。编辑 `.env` 填入你的 API Key 即可：

```
DEEPSEEK_API_KEY=sk-你的密钥
```

> 💡 本项目已内置 API Key，如果你拿到的是带了 `.env` 的完整包，直接双击 start.bat 就能用。

---

## 📁 项目文件

```
demo/
├── landing.html          # 展示首页（启动后首先看到）
├── index.html            # Demo 应用（AI聊天+食谱+购物车）
├── chat.js               # 前端聊天逻辑
├── server.py             # Python 后端服务
├── requirements.txt      # Python 依赖
├── start.bat             # ⭐ Windows 一键启动（双击就行）
├── start.sh              # Mac/Linux 一键启动
├── setup_and_run.py      # 一键部署脚本
├── .env                  # API Key 配置（自动创建）
├── .env.example          # 配置模板
├── hero-bg.png           # 展示首页背景图
├── footer-bg.jpeg        # 展示首页底部背景图
└── README.md             # 你正在看的文件
```

---

## 🛠️ 技术栈

| 模块 | 技术 |
|------|------|
| 前端 | HTML5 + Tailwind CSS + Chart.js + Lucide Icons |
| 后端 | Python + Flask |
| AI | DeepSeek API（兼容 OpenAI 格式）|
| 设计 | Claymorphism 黏土风格 + 暖黄色调 |

---

## ⚠️ 注意事项

- **API 有费用**：DeepSeek 按调用量计费（约 ¥6/百万 tokens），日常使用几乎忽略不计
- **不替代兽医**：AI 提供饮食建议，健康问题请咨询专业兽医
- **建议用手机访问**：Demo 针对移动端触控优化

---

**🐾 宠食记 PetDiet AI** — 让每一餐都充满爱
