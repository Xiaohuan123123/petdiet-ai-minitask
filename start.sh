#!/bin/bash
# PetDiet AI 启动脚本 (Mac/Linux)

echo ""
echo "🐾 ===================================="
echo "   宠食记 PetDiet AI"
echo "===================================="
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python3，请先安装 Python 3.8+"
    exit 1
fi

# 运行一键部署脚本
python3 setup_and_run.py
