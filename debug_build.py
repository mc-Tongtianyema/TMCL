#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
调试版本构建脚本 - 使用--onedir模式便于调试
"""

import os
import sys
import shutil
import subprocess

# 获取项目根目录
ROOT_DIR = os.path.abspath('.')
SRC_DIR = os.path.join(ROOT_DIR, 'src')
BUILD_DIR = os.path.join(ROOT_DIR, 'build_debug')
DIST_DIR = os.path.join(ROOT_DIR, 'dist_debug')

# 清理之前的构建
if os.path.exists(BUILD_DIR):
    shutil.rmtree(BUILD_DIR)
    print(f"清理构建目录: {BUILD_DIR}")
if os.path.exists(DIST_DIR):
    shutil.rmtree(DIST_DIR)
    print(f"清理发布目录: {DIST_DIR}")

# 创建调试入口文件
def create_debug_entry():
    """创建调试入口文件"""
    debug_main = os.path.join(ROOT_DIR, 'debug_main.py')
    with open(debug_main, 'w', encoding='utf-8') as f:
        f.write('''#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import traceback

# 打印当前路径信息进行调试
print(f"当前工作目录: {os.getcwd()}")
print(f"入口文件路径: {os.path.abspath(__file__)}")
print(f"Python路径: {sys.path}")

# 添加项目根目录和src目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

# 打印更新后的路径
print(f"更新后的Python路径: {sys.path}")

# 尝试导入关键模块
try:
    print("尝试导入src模块...")
    import src
    print("src模块导入成功")
    
    print("尝试导入src.utils.api_client...")
    from src.utils.api_client import BMCLAPIClient
    print("src.utils.api_client导入成功")
    
except Exception as e:
    print(f"导入失败: {str(e)}")
    traceback.print_exc()

# 设置环境变量，确保中文显示正常
os.environ['QT_FONT_DPI'] = '96'

# 导入并启动应用
try:
    from src.main import main
    print("main函数导入成功，启动应用...")
    sys.exit(main())
except Exception as e:
    print(f"启动应用失败: {str(e)}")
    traceback.print_exc()
    sys.exit(1)
''')
    return debug_main

# 运行PyInstaller构建
def build_with_pyinstaller(entry_point):
    """使用PyInstaller构建可执行文件（目录模式）"""
    # 构建命令 - 使用--onedir模式
    cmd = [
        'pyinstaller',
        '--name=TMCL_debug',
        '--onedir',
        '--console',  # 使用控制台模式以便看到输出
        f'--workpath={BUILD_DIR}',
        f'--distpath={DIST_DIR}',
        '--paths=' + os.path.abspath('src'),
        '--paths=' + os.path.abspath('.'),
        '--hidden-import=src',
        '--hidden-import=src.utils',
        '--hidden-import=src.utils.api_client',
        '--hidden-import=src.utils.logger',
        '--hidden-import=src.utils.utils',
        '--hidden-import=src.core',
        '--hidden-import=src.core.config_manager',
        '--hidden-import=src.core.version_manager',
        '--hidden-import=src.core.game_launcher',
        '--hidden-import=src.core.constants',
        '--hidden-import=src.ui',
        '--hidden-import=src.ui.main_window',
        '--hidden-import=requests',
        '--hidden-import=yaml',
        '--log-level=DEBUG',
        entry_point
    ]
    
    # 执行构建命令
    print(f"执行构建命令: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(f"构建完成，返回代码: {result.returncode}")
    print(f"构建输出:\n{result.stdout}")
    if result.stderr:
        print(f"构建错误:\n{result.stderr}")
    
    return result.returncode == 0

if __name__ == "__main__":
    print("开始调试模式构建TMCL...")
    print(f"项目根目录: {ROOT_DIR}")
    print(f"源代码目录: {SRC_DIR}")
    
    # 创建调试入口文件
    debug_entry = create_debug_entry()
    print(f"创建了调试入口文件: {debug_entry}")
    
    # 使用PyInstaller构建
    success = build_with_pyinstaller(debug_entry)
    
    if success:
        print("构建成功！调试版本位于:")
        print(f"  构建目录: {BUILD_DIR}")
        print(f"  发布目录: {DIST_DIR}")
        print("\n运行命令:")
        print(f"  {os.path.join(DIST_DIR, 'TMCL_debug', 'TMCL_debug.exe')}")
    else:
        print("构建失败，请查看上面的错误信息")
    
    # 清理临时文件
    if os.path.exists(debug_entry):
        os.remove(debug_entry)
        print(f"清理临时文件: {debug_entry}")
