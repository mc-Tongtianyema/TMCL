#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TMCL - Tongtian Minecraft Launcher
由通天野马(GitHub: mc-Tongtianyema)创建并开发
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import main

if __name__ == "__main__":
    sys.exit(main())
