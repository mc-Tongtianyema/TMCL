import os
import sys
import subprocess
import shutil
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent

# 输出目录
OUTPUT_DIR = PROJECT_ROOT / 'dist'
BUILD_DIR = PROJECT_ROOT / 'build'

# 清理旧的构建文件
def clean_old_builds():
    print("清理旧的构建文件...")
    
    # 清理输出目录
    if OUTPUT_DIR.exists():
        try:
            shutil.rmtree(OUTPUT_DIR)
            print(f"已删除旧的输出目录: {OUTPUT_DIR}")
        except Exception as e:
            print(f"删除输出目录时出错: {e}")
    
    # 清理构建目录
    if BUILD_DIR.exists():
        try:
            shutil.rmtree(BUILD_DIR)
            print(f"已删除旧的构建目录: {BUILD_DIR}")
        except Exception as e:
            print(f"删除构建目录时出错: {e}")
    
    # 清理spec文件
    for spec_file in PROJECT_ROOT.glob('*.spec'):
        try:
            spec_file.unlink()
            print(f"已删除旧的spec文件: {spec_file}")
        except Exception as e:
            print(f"删除spec文件时出错: {e}")

# 检查PyInstaller是否安装
def check_pyinstaller():
    print("检查PyInstaller是否安装...")
    try:
        # 尝试导入PyInstaller
        import PyInstaller
        print(f"PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("PyInstaller未安装，尝试安装...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
            print("PyInstaller安装成功")
        except Exception as e:
            print(f"PyInstaller安装失败: {e}")
            sys.exit(1)

# 安装所有依赖
def install_dependencies():
    print("安装项目依赖...")
    requirements_file = PROJECT_ROOT / 'requirements.txt'
    if requirements_file.exists():
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)])
            print("依赖安装成功")
        except Exception as e:
            print(f"依赖安装失败: {e}")
            sys.exit(1)
    else:
        print("requirements.txt文件不存在")

# 构建可执行文件
def build_executable():
    print("开始构建可执行文件...")
    
    # 确保依赖已安装
    install_dependencies()
    check_pyinstaller()
    
    # 主入口文件
    main_file = PROJECT_ROOT / 'src' / 'main.py'
    
    # 简化的构建命令，使用--onedir而不是--onefile以便更容易调试
    cmd = [
        sys.executable,
        '-m', 'PyInstaller',
        '--name=TMCL',
        '--onedir',  # 使用目录模式
        '--console',  # 使用控制台模式以便查看错误
        '--clean',
        '--distpath=' + str(OUTPUT_DIR),
        '--workpath=' + str(BUILD_DIR),
        str(main_file)
    ]
    
    print(f"执行命令: {' '.join(cmd)}")
    
    try:
        # 执行构建命令
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # 输出构建日志
        if result.stdout:
            print("构建输出:")
            print(result.stdout)
        
        if result.stderr:
            print("构建错误:")
            print(result.stderr)
        
        # 检查构建是否成功
        if result.returncode != 0:
            print(f"构建失败，返回代码: {result.returncode}")
            return False
        else:
            print("构建成功")
            return True
    except Exception as e:
        print(f"构建过程中出现异常: {e}")
        return False

# 主函数
def main():
    print("===== TMCL启动器打包脚本 =====")
    
    # 清理旧的构建
    clean_old_builds()
    
    # 构建可执行文件
    if not build_executable():
        print("构建可执行文件失败!")
        return 1
    
    print("\n===== 打包完成 =====")
    print(f"可执行文件位于: {OUTPUT_DIR / 'TMCL'}")
    print("请运行 TMCL\TMCL.exe 启动程序")
    print("注意: 由于使用了--console模式，运行时会显示控制台窗口用于调试")
    return 0

if __name__ == "__main__":
    sys.exit(main())
