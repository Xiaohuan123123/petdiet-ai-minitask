@echo off
chcp 65001 >nul
echo.
echo 🐾 ====================================
echo    宠食记 PetDiet AI
echo ====================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到 Python，请先安装 Python 3.8+
    echo 📥 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 运行一键部署脚本
python setup_and_run.py
pause
