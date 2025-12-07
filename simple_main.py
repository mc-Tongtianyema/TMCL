#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简化的入口点文件，用于PyInstaller打包
"""

import sys
import os
import traceback
import json  # 预先导入标准库模块

# 预先导入PyQt5，确保依赖被正确打包
try:
    import PyQt5
    print("PyQt5 imported successfully!")
    # 导入常用的PyQt5组件
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import Qt
    print("PyQt5 components imported successfully!")
except ImportError as e:
    print(f"Failed to import PyQt5: {str(e)}")

# 获取当前脚本的目录
base_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(base_dir, 'src')

# 将src目录添加到Python路径
sys.path.insert(0, base_dir)
sys.path.insert(0, src_dir)
print(f"Base directory: {base_dir}")
print(f"Src directory: {src_dir}")
print(f"Python path: {sys.path}")

try:
    # 使用正常的导入方式导入main模块
    from src.main import main
    print("Imported main function successfully!")
    
    # 运行主函数
    sys.exit(main())
    
except Exception as e:
    print(f"Error: {str(e)}")
    traceback.print_exc()
    sys.exit(1)
