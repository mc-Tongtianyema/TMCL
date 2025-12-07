#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
修复导入路径问题的构建脚本
"""

import os
import sys
import shutil

# 获取项目根目录
ROOT_DIR = os.path.abspath('.')
SRC_DIR = os.path.join(ROOT_DIR, 'src')
BUILD_DIR = os.path.join(ROOT_DIR, 'build')
DIST_DIR = os.path.join(ROOT_DIR, 'dist')

# 清理之前的构建
if os.path.exists(BUILD_DIR):
    shutil.rmtree(BUILD_DIR)
if os.path.exists(DIST_DIR):
    shutil.rmtree(DIST_DIR)

# 创建一个修复导入的入口文件
def create_fixed_entry_point():
    """创建一个修复导入的入口文件"""
    fixed_main = os.path.join(ROOT_DIR, 'fixed_main.py')
    with open(fixed_main, 'w', encoding='utf-8') as f:
        f.write('''#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

# 添加项目根目录和src目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

# 设置环境变量，确保中文显示正常
os.environ['QT_FONT_DPI'] = '96'

# 导入必要的模块
import logging

# 尝试直接导入并启动应用
from src.main import main

if __name__ == "__main__":
    sys.exit(main())
''')
    return fixed_main

# 运行PyInstaller构建
def build_with_pyinstaller(entry_point):
    """使用PyInstaller构建可执行文件"""
    # 构建命令
    cmd = [
        'pyinstaller',
        '--name=TMCL',
        '--onefile',
        '--windowed',
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
        entry_point
    ]
    
    # 执行构建命令
    print(f"执行构建命令: {' '.join(cmd)}")
    os.system(' '.join(cmd))

if __name__ == "__main__":
    print("开始修复导入路径并构建TMCL...")
    
    # 创建修复的入口文件
    fixed_entry = create_fixed_entry_point()
    print(f"创建了修复的入口文件: {fixed_entry}")
    
    # 使用PyInstaller构建
    build_with_pyinstaller(fixed_entry)
    
    # 清理临时文件
    if os.path.exists(fixed_entry):
        os.remove(fixed_entry)
    
    print("构建完成！请检查dist目录中的TMCL.exe文件")
