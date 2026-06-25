@echo off
chcp 65001 >nul
title 宠食记 PetDiet AI

echo.
echo ╔══════════════════════════════════════════╗
echo ║                                          ║
echo ║    🐾  宠 食 记  PetDiet AI               ║
echo ║    宠物饮食健康 + 购买决策助手              ║
echo ║                                          ║
echo ╚══════════════════════════════════════════╝
echo.
echo    欢迎启动"宠食记"！按 Enter 即可一键部署！
echo.
pause >nul

echo.
echo ═══════════════════════════════════════════
echo  [1/3] 检查运行环境...
echo ═══════════════════════════════════════════

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ┌─────────────────────────────────────┐
    echo │  ❌ 错误：未找到 Python                 │
    echo ├─────────────────────────────────────┤
    echo │  请先安装 Python 3.8 或更高版本         │
    echo │  下载地址：                            │
    echo │  https://www.python.org/downloads/    │
    echo │                                      │
    echo │  安装时请勾选 "Add Python to PATH"     │
    echo └─────────────────────────────────────┘
    echo.
    pause
    exit /b 1
)

python --version
echo    ✅ Python 环境正常
echo.

echo ═══════════════════════════════════════════
echo  [2/3] 安装依赖包...
echo ═══════════════════════════════════════════

pip install flask flask-cors requests python-dotenv -q 2>nul
if errorlevel 1 (
    echo    ⚠️  自动安装失败，尝试手动安装...
    echo.
    echo    请手动运行以下命令：
    echo    pip install flask flask-cors requests python-dotenv
    echo.
    echo    安装完成后重新运行 start.bat
    echo.
    pause
    exit /b 1
)
echo    ✅ 依赖包安装完成
echo.

echo ═══════════════════════════════════════════
echo  [3/3] 检查配置文件...
echo ═══════════════════════════════════════════

if not exist .env (
    echo    ⚠️  未找到 .env 文件，正在创建...
    echo DEEPSEEK_API_KEY=sk-your-api-key-here > .env
    echo    ✅ 已创建 .env 文件
    echo.
    echo    📝 请编辑 .env 文件，填入你的 DeepSeek API Key
    echo      获取地址：https://platform.deepseek.com
    echo.
) else (
    echo    ✅ .env 配置文件就绪
)

echo.
echo ╔══════════════════════════════════════════╗
echo ║                                          ║
echo ║          ✅  部署完成！                     ║
echo ║                                          ║
echo ║   📍 展示首页                              ║
echo ║   http://localhost:5000                 ║
echo ║                                          ║
echo ║   📍 Demo 应用                            ║
echo ║   http://localhost:5000/app             ║
echo ║                                          ║
echo ║   🛑 按 Ctrl+C 停止服务                    ║
echo ║                                          ║
echo ╚══════════════════════════════════════════╝
echo.

REM 自动打开浏览器
start "" http://localhost:5000

REM 启动服务
python server.py

REM 如果 server.py 异常退出
if errorlevel 1 (
    echo.
    echo ┌─────────────────────────────────────┐
    echo │  ⚠️  服务启动异常                       │
    echo ├─────────────────────────────────────┤
    echo │  请尝试手动部署：                       │
    echo │                                      │
    echo │  1. pip install flask flask-cors     │
    echo │     requests python-dotenv           │
    echo │  2. 检查 .env 中 API Key 是否正确      │
    echo │  3. python server.py                 │
    echo │                                      │
    echo │  如仍有问题，请查看上方错误信息           │
    echo └─────────────────────────────────────┘
    echo.
    pause
)
