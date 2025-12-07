#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
最小化测试脚本，只包含基本Python功能
"""

import os
import sys
import time

# 创建日志文件记录运行信息
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_log.txt')
with open(log_file, 'w') as f:
    f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 最小化测试脚本开始运行\n")
    f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Python版本: {sys.version}\n")
    f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 当前工作目录: {os.getcwd()}\n")
    f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 脚本路径: {os.path.abspath(__file__)}\n")
    f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Python路径: {sys.path}\n")
    f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 测试完成\n")

# 打印一些信息到控制台
print("最小化测试脚本运行成功！")
print(f"日志已保存到: {log_file}")
print("按任意键退出...")
input()
