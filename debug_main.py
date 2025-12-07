#!/usr/bin/env python
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
