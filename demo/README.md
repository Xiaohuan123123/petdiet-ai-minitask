# 🐾 宠食记 PetDiet AI

基于 DeepSeek 大模型的宠物饮食健康助手，AI为你定制专属宠物食谱。

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![DeepSeek](https://img.shields.io/badge/DeepSeek-AI-orange)

## ✨ 功能特点

- 🤖 **AI智能对话** - 基于DeepSeek大模型，专业宠物饮食咨询
- 📋 **结构化输出** - 食谱表格、制作步骤、喂食建议清晰展示
- 🎯 **个性化定制** - 根据宠物品种、年龄、体重、健康状况定制方案
- 📱 **移动端适配** - 完美支持手机浏览器访问
- 🍊 **暖色调设计** - 温馨的橙黄色UI，用户体验友好

---

## 🚀 快速启动

### 前置条件

- Python 3.8 或更高版本
- DeepSeek API Key（[点击获取](https://platform.deepseek.com)）

---

### 方式一：一键启动（推荐）

#### Windows 用户
```bash
# 1. 进入 demo 目录
cd demo

# 2. 双击运行 start.bat
# 或者在命令行执行：
start.bat
```

#### Mac / Linux 用户
```bash
# 1. 进入 demo 目录
cd demo

# 2. 添加执行权限并运行
chmod +x start.sh
./start.sh
```

#### 或者直接运行 Python 脚本
```bash
cd demo
python setup_and_run.py
```

**一键脚本会自动帮你：**
1. ✅ 检查 Python 环境
2. ✅ 安装所有依赖包
3. ✅ 引导你输入 API Key
4. ✅ 启动后端服务

---

### 方式二：手动部署

#### Step 1：克隆项目
```bash
git clone https://github.com/your-username/pet-diet-ai.git
cd pet-diet-ai/demo
```

#### Step 2：安装依赖
```bash
pip install -r requirements.txt
```

#### Step 3：配置 API Key
```bash
# 复制配置文件模板
cp .env.example .env

# 编辑 .env 文件，填入你的 DeepSeek API Key
```

`.env` 文件内容：
```
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

> 💡 API Key 获取方式：访问 https://platform.deepseek.com 注册账号后，在 API Keys 页面创建。

#### Step 4：启动服务
```bash
python server.py
```

#### Step 5：访问应用
打开浏览器访问：**http://localhost:5000**

---

## 📁 项目结构

```
pet-diet-ai/
├── demo/
│   ├── index.html          # 前端页面（UI界面）
│   ├── chat.js             # 前端聊天逻辑
│   ├── server.py           # Python 后端服务
│   ├── requirements.txt    # Python 依赖列表
│   ├── .env.example        # 环境变量配置模板
│   ├── .env                # 环境变量配置（需自行创建）
│   ├── setup_and_run.py    # ⭐ 一键部署脚本
│   ├── start.bat           # Windows 启动脚本
│   ├── start.sh            # Mac/Linux 启动脚本
│   └── README.md           # 项目说明文档
├── docs/                   # 产品设计文档
│   ├── prd-v1-part1.md     # PRD 产品需求文档
│   ├── feature-roadmap-v2.md
│   └── ...
└── ...
```

---

## 🔧 配置说明

### DeepSeek API Key 获取步骤

1. 访问 [DeepSeek Platform](https://platform.deepseek.com)
2. 注册并登录账号
3. 进入 **API Keys** 页面
4. 点击 **Create new secret key** 创建新密钥
5. 复制生成的 `sk-xxx...` 密钥
6. 填入项目根目录的 `.env` 文件

### 环境变量

| 变量名 | 说明 | 必填 |
|--------|------|------|
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 | ✅ 是 |

---

## 📱 使用说明

1. 启动服务后，在浏览器打开 `http://localhost:5000`
2. 点击底部导航栏的 **「吃饭」** 进入 AI 对话页面
3. 在输入框输入宠物饮食相关问题
4. AI 会返回结构化的饮食方案和食谱

### 💬 示例问题

```
我想给3岁的金毛做一个南瓜鸡肉粥食谱
柯基软便了应该吃什么？
猫咪能吃蓝莓吗？
如何判断狗粮的好坏？
```

---

## 🛠️ 技术栈

| 模块 | 技术 |
|------|------|
| 前端 | HTML5 + Tailwind CSS + Chart.js |
| 后端 | Python + Flask |
| AI | DeepSeek API（兼容 OpenAI 格式）|

---

## ⚠️ 注意事项

1. **API 费用** - DeepSeek API 按调用量计费，请注意使用量
2. **网络要求** - 需要能访问 `api.deepseek.com`
3. **不替代医疗** - AI 建议仅供参考，宠物健康问题请咨询兽医

---

## 📄 License

MIT License

---

**🐾 宠食记 PetDiet AI** — 让每一餐都充满爱
