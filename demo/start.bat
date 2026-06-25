@echo off
chcp 65001 >nul
title 宠食记 PetDiet AI

echo.
echo ╔══════════════════════════════════════════╗
echo ║                                          ║
echo ║    🐾 宠食记 PetDiet AI                   ║
echo ║    宠物饮食健康助手                        ║
echo ║                                          ║
echo ╚══════════════════════════════════════════╝
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [1/3] 正在安装依赖...
pip install flask flask-cors requests python-dotenv -q
if errorlevel 1 (
    echo [警告] 依赖安装可能不完整，继续启动...
)

echo [2/3] 检查配置...
if not exist .env (
    echo [提示] 未找到 .env 文件，正在创建...
    echo DEEPSEEK_API_KEY=sk-your-api-key-here > .env
    echo 请编辑 .env 文件填入你的 DeepSeek API Key
)

echo [3/3] 启动服务...
echo.
echo ╔══════════════════════════════════════════╗
echo ║  展示首页: http://localhost:5000        ║
echo ║  Demo应用: http://localhost:5000/app    ║
echo ║                                          ║
echo ║  按 Ctrl+C 停止服务                      ║
echo ╚══════════════════════════════════════════╝
echo.

REM 用 Python 启动服务器并打开浏览器
start "" http://localhost:5000
python server.py

pause
