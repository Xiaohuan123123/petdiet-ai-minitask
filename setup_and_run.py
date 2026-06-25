"""
🐾 PetDiet AI - 一键部署脚本
自动检查环境、安装依赖、配置API、启动服务
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

# 颜色输出
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    """打印启动横幅"""
    print(f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   🐾 宠食记 PetDiet AI - 宠物饮食健康助手               ║
║                                                          ║
║   一站式宠物饮食咨询，AI为你定制专属食谱                 ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
{Colors.END}""")

def check_python():
    """检查Python版本"""
    print(f"{Colors.BLUE}📋 检查Python环境...{Colors.END}")

    if sys.version_info < (3, 8):
        print(f"{Colors.RED}❌ Python版本过低，需要3.8或更高版本{Colors.END}")
        print(f"{Colors.YELLOW}💡 当前版本: {sys.version}{Colors.END}")
        sys.exit(1)

    print(f"{Colors.GREEN}✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}{Colors.END}")
    return True

def install_dependencies():
    """安装依赖"""
    print(f"\n{Colors.BLUE}📦 安装依赖包...{Colors.END}")

    requirements_file = Path(__file__).parent / 'requirements.txt'
    if not requirements_file.exists():
        print(f"{Colors.YELLOW}⚠️  未找到 requirements.txt，跳过依赖安装{Colors.END}")
        return True

    try:
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file), '-q'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print(f"{Colors.GREEN}✅ 依赖安装完成{Colors.END}")
        return True
    except subprocess.CalledProcessError:
        print(f"{Colors.RED}❌ 依赖安装失败，请手动运行: pip install -r requirements.txt{Colors.END}")
        return False

def setup_env_file():
    """配置环境变量文件"""
    print(f"\n{Colors.BLUE}⚙️  配置环境变量...{Colors.END}")

    env_file = Path(__file__).parent / '.env'
    env_example = Path(__file__).parent / '.env.example'

    if env_file.exists():
        print(f"{Colors.GREEN}✅ .env 文件已存在{Colors.END}")
        # 检查是否配置了API Key
        with open(env_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'your-api-key-here' in content or 'DEEPSEEK_API_KEY=' in content:
                print(f"{Colors.YELLOW}⚠️  请确保 .env 文件中已填入有效的 API Key{Colors.END}")
        return True

    if env_example.exists():
        shutil.copy(env_example, env_file)
        print(f"{Colors.GREEN}✅ 已从 .env.example 创建 .env 文件{Colors.END}")
        print(f"{Colors.YELLOW}⚠️  请编辑 .env 文件填入你的 DeepSeek API Key{Colors.END}")
        return True
    else:
        # 创建默认 .env 文件
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write("# DeepSeek API 配置\n")
            f.write("# 从 https://platform.deepseek.com 获取 API Key\n")
            f.write("DEEPSEEK_API_KEY=your-api-key-here\n")
        print(f"{Colors.GREEN}✅ 已创建 .env 文件{Colors.END}")
        print(f"{Colors.YELLOW}⚠️  请编辑 .env 文件填入你的 DeepSeek API Key{Colors.END}")
        return True

def get_api_key():
    """交互式获取API Key"""
    print(f"\n{Colors.BLUE}🔑 配置 API Key{Colors.END}")

    env_file = Path(__file__).parent / '.env'

    # 检查是否已有有效Key
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('DEEPSEEK_API_KEY='):
                    key = line.split('=', 1)[1].strip()
                    if key and key != 'your-api-key-here' and key.startswith('sk-'):
                        print(f"{Colors.GREEN}✅ 已检测到 API Key: {key[:10]}...{key[-4:]}{Colors.END}")
                        use_existing = input(f"{Colors.CYAN}是否使用现有Key？(Y/n): {Colors.END}").strip().lower()
                        if use_existing != 'n':
                            return key

    print(f"{Colors.CYAN}请访问 https://platform.deepseek.com 获取 API Key{Colors.END}")
    api_key = input(f"{Colors.CYAN}请输入你的 DeepSeek API Key (sk-开头): {Colors.END}").strip()

    if not api_key:
        print(f"{Colors.RED}❌ API Key 不能为空{Colors.END}")
        return None

    if not api_key.startswith('sk-'):
        print(f"{Colors.YELLOW}⚠️  API Key 格式可能不正确，通常以 sk- 开头{Colors.END}")

    # 写入 .env 文件
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(f"# DeepSeek API 配置\n")
        f.write(f"DEEPSEEK_API_KEY={api_key}\n")

    print(f"{Colors.GREEN}✅ API Key 已保存{Colors.END}")
    return api_key

def start_server():
    """启动服务器"""
    print(f"\n{Colors.BLUE}🚀 启动服务...{Colors.END}")

    server_file = Path(__file__).parent / 'server.py'
    if not server_file.exists():
        print(f"{Colors.RED}❌ 未找到 server.py{Colors.END}")
        sys.exit(1)

    print(f"{Colors.GREEN}✅ 服务启动成功！{Colors.END}")
    print(f"""
{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   🌐 访问地址: http://localhost:5000                    ║
║                                                          ║
║   💡 按 Ctrl+C 停止服务                                 ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
{Colors.END}""")

    # 启动服务器
    os.chdir(Path(__file__).parent)
    os.execv(sys.executable, [sys.executable, 'server.py'])

def main():
    """主函数"""
    print_banner()

    # 检查Python
    check_python()

    # 安装依赖
    install_dependencies()

    # 配置环境变量
    setup_env_file()

    # 获取API Key
    api_key = get_api_key()
    if not api_key:
        print(f"{Colors.RED}❌ 未配置 API Key，无法启动服务{Colors.END}")
        sys.exit(1)

    # 启动服务
    start_server()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}👋 再见！{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}❌ 发生错误: {e}{Colors.END}")
        sys.exit(1)
