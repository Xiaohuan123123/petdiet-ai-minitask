"""
宠食记 PetDiet AI · 一键启动脚本
"""
import os, sys, subprocess, time

def print_box(title):
    print()
    print("=" * 42)
    print(f"  {title}")
    print("=" * 42)

def print_ok(msg):
    print(f"  [OK] {msg}")

def print_err(msg):
    print(f"  [ERROR] {msg}")

# ========== 欢迎界面 ==========
os.system('cls' if os.name == 'nt' else 'clear')
print()
print("=" * 42)
print("  🐾  宠 食 记  PetDiet AI")
print("  宠物饮食健康 + 购买决策助手")
print("=" * 42)
print()
print("  欢迎启动「宠食记」！按 Enter 即可一键部署！")
input()

# ========== 1. 检查 Python ==========
os.system('cls' if os.name == 'nt' else 'clear')
print_box("[1/3] 检查运行环境")

py_ver = sys.version.split()[0]
print(f"  Python {py_ver}")
print_ok("Python 环境正常")

# ========== 2. 安装依赖 ==========
print_box("[2/3] 安装依赖包")

try:
    subprocess.check_call(
        [sys.executable, '-m', 'pip', 'install', 'flask', 'flask-cors', 'requests', 'python-dotenv', '-q'],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    print_ok("依赖包安装完成")
except Exception:
    print()
    print("  [WARN] 自动安装失败，请手动运行：")
    print("  pip install flask flask-cors requests python-dotenv")
    print()
    input("  按 Enter 退出...")
    sys.exit(1)

# ========== 3. 检查配置 ==========
print_box("[3/3] 检查配置文件")

env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
if not os.path.exists(env_file):
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write("DEEPSEEK_API_KEY=sk-your-api-key-here\n")
    print("  [提示] 已创建 .env 模板文件")
    print("  请编辑 .env 填入你的 DeepSeek API Key")
    print("  获取地址: https://platform.deepseek.com")
else:
    print_ok(".env 配置文件就绪")

# ========== 部署完成 ==========
print()
print("=" * 42)
print("          ✅  部署完成！")
print("=" * 42)
print()
print("  📍 展示首页: http://localhost:5000")
print("  📍 Demo应用: http://localhost:5000/app")
print()
print("  浏览器即将自动打开...")
print("  按 Ctrl+C 停止服务")
print("=" * 42)
print()

# 自动打开浏览器
time.sleep(1)
import webbrowser
webbrowser.open("http://localhost:5000")

# 启动服务
demo_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(demo_dir)
try:
    subprocess.run([sys.executable, 'server.py'])
except KeyboardInterrupt:
    print("\n  服务已停止，再见！")
except Exception as e:
    print()
    print("-" * 42)
    print("  [提示] 服务启动异常")
    print("-" * 42)
    print(f"  错误信息: {e}")
    print()
    print("  请尝试手动部署：")
    print("  1. pip install flask flask-cors requests python-dotenv")
    print("  2. 检查 .env 中 API Key 是否正确")
    print("  3. python server.py")
    print("-" * 42)
    print()
    input("  按 Enter 退出...")
