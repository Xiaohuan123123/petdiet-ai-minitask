@echo off
chcp 65001 >nul
title PetDiet AI

cls
echo.
echo ==========================================
echo   PetDiet AI - Pet Food & Health Assistant
echo ==========================================
echo.
echo   Press Enter to start deployment...
echo.
pause >nul

cls
echo.
echo ==========================================
echo  [1/3] Checking Python...
echo ==========================================

python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ----------------------------------------
    echo  [ERROR] Python not found
    echo ----------------------------------------
    echo  Please install Python 3.8+
    echo  https://www.python.org/downloads/
    echo  Make sure to check Add Python to PATH
    echo ----------------------------------------
    echo.
    pause
    exit /b 1
)

python --version
echo  [OK] Python ready
echo.

echo ==========================================
echo  [2/3] Installing dependencies...
echo ==========================================

pip install flask flask-cors requests python-dotenv -q 2>nul
if errorlevel 1 (
    echo.
    echo ----------------------------------------
    echo  [WARN] Auto install failed
    echo ----------------------------------------
    echo  Run this command manually, then retry:
    echo  pip install flask flask-cors requests python-dotenv
    echo ----------------------------------------
    echo.
    pause
    exit /b 1
)
echo  [OK] Dependencies ready
echo.

echo ==========================================
echo  [3/3] Checking config...
echo ==========================================

if not exist .env (
    echo  Creating .env template...
    echo DEEPSEEK_API_KEY=sk-your-api-key-here > .env
    echo  [OK] .env created
    echo  Edit .env to add your DeepSeek API Key
    echo  Get key at: https://platform.deepseek.com
) else (
    echo  [OK] .env config ready
)

echo.
echo ==========================================
echo            DEPLOYMENT COMPLETE
echo ==========================================
echo.
echo   Landing page: http://localhost:5000
echo   Demo app:     http://localhost:5000/app
echo.
echo   Browser will open automatically...
echo   Press Ctrl+C to stop the server
echo ==========================================
echo.

start "" http://localhost:5000
python server.py

if errorlevel 1 (
    echo.
    echo ----------------------------------------
    echo  [INFO] Server stopped unexpectedly
    echo ----------------------------------------
    echo  Try manual deployment:
    echo  1. pip install flask flask-cors requests python-dotenv
    echo  2. check .env API Key
    echo  3. python server.py
    echo ----------------------------------------
    echo.
    pause
)
