#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简单测试启动脚本，用于诊断和解决编译问题
"""

import sys
import os
import time

# 打印基本信息用于诊断
print(f"[{time.strftime('%H:%M:%S')}] 测试启动脚本开始运行")
print(f"[{time.strftime('%H:%M:%S')}] Python版本: {sys.version}")
print(f"[{time.strftime('%H:%M:%S')}] 当前工作目录: {os.getcwd()}")
print(f"[{time.strftime('%H:%M:%S')}] 脚本路径: {os.path.abspath(__file__)}")
print(f"[{time.strftime('%H:%M:%S')}] Python路径: {sys.path}")

# 尝试导入基本模块
try:
    print(f"[{time.strftime('%H:%M:%S')}] 尝试导入基本模块...")
    import os, sys, time, json, logging
    print(f"[{time.strftime('%H:%M:%S')}] 基本模块导入成功")
except Exception as e:
    print(f"[{time.strftime('%H:%M:%S')}] 基本模块导入失败: {e}")

# 尝试导入PyQt5
try:
    print(f"[{time.strftime('%H:%M:%S')}] 尝试导入PyQt5...")
    from PyQt5 import QtWidgets, QtGui, QtCore
    print(f"[{time.strftime('%H:%M:%S')}] PyQt5模块导入成功")
    # 简单的PyQt5测试
    app = QtWidgets.QApplication([])
    print(f"[{time.strftime('%H:%M:%S')}] QApplication初始化成功")
except Exception as e:
    print(f"[{time.strftime('%H:%M:%S')}] PyQt5模块导入失败: {e}")

# 尝试导入其他依赖
try:
    print(f"[{time.strftime('%H:%M:%S')}] 尝试导入requests和yaml...")
    import requests, yaml
    print(f"[{time.strftime('%H:%M:%S')}] requests和yaml模块导入成功")
except Exception as e:
    print(f"[{time.strftime('%H:%M:%S')}] requests或yaml模块导入失败: {e}")

# 测试完成
print(f"[{time.strftime('%H:%M:%S')}] 测试完成")
print("按任意键退出...")
input()
