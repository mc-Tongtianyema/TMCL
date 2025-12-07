#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简化版测试脚本，用于验证TMCL项目的基本功能
"""

import sys
import os
import traceback

# 设置基础路径
base_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(base_dir, 'src')

# 添加路径到sys.path
sys.path.insert(0, base_dir)
sys.path.insert(0, src_dir)

print(f"基础目录: {base_dir}")
print(f"源代码目录: {src_dir}")

# 测试基本的模块导入和核心组件初始化
def test_basic_imports():
    """测试基本的模块导入"""
    try:
        # 导入基础模块
        from src.core.constants import APP_NAME
        print(f"\n✅ 导入成功: {APP_NAME}")
        
        # 测试配置管理器
        from src.core.config_manager import ConfigManager
        config_manager = ConfigManager()
        print(f"✅ 配置管理器初始化成功，配置路径: {config_manager.config_path}")
        
        # 测试日志系统
        from src.utils.logger import setup_logger
        logger = setup_logger("TestLogger")
        logger.info("测试日志消息")
        print("✅ 日志系统初始化成功")
        
        # 测试版本管理器（简化测试）
        from src.api.bmcl_api import BMCLAPI
        bmcl_api = BMCLAPI()
        print("✅ BMCL API客户端初始化成功")
        
        from src.core.version_manager import VersionManager
        version_manager = VersionManager(config_manager, bmcl_api)
        print("✅ 版本管理器初始化成功")
        
        # 测试游戏启动器
        from src.core.game_launcher import GameLauncher
        game_launcher = GameLauncher(config_manager)
        game_launcher.set_version_manager(version_manager)
        print("✅ 游戏启动器初始化成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 导入测试失败: {type(e).__name__}: {e}")
        traceback.print_exc()
        return False

# 测试PyQt5基本功能
def test_pyqt5_basic():
    """测试PyQt5基本功能"""
    try:
        from PyQt5.QtWidgets import QApplication, QMessageBox
        print("\n✅ PyQt5模块导入成功")
        
        # 创建一个简单的应用程序实例
        app = QApplication(sys.argv)
        app.setApplicationName("TMCL测试")
        
        # 设置中文字体
        from PyQt5.QtGui import QFont
        font = QFont()
        font.setFamily("SimHei")
        app.setFont(font)
        print("✅ PyQt5中文设置成功")
        
        # 显示一个简单的消息框
        msg = QMessageBox()
        msg.setWindowTitle("TMCL测试")
        msg.setText("PyQt5基础功能测试成功！")
        msg.setInformativeText("TMCL项目的基本组件初始化正常")
        msg.setStandardButtons(QMessageBox.Ok)
        
        print("💡 即将显示测试消息框，请点击确定继续...")
        result = msg.exec_()
        
        return True
        
    except Exception as e:
        print(f"❌ PyQt5测试失败: {type(e).__name__}: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("="*50)
    print("TMCL项目基础功能测试")
    print("="*50)
    
    # 首先测试基本导入
    basic_test_result = test_basic_imports()
    
    # 然后测试PyQt5功能
    if basic_test_result:
        pyqt_test_result = test_pyqt5_basic()
    
    print("\n" + "="*50)
    if basic_test_result and (not basic_test_result or pyqt_test_result):
        print("🎉 测试完成！TMCL项目的基础功能运行正常。")
        print("\n提示：")
        print("1. 项目的核心组件能够正常初始化")
        print("2. 日志系统可以正常工作")
        print("3. PyQt5界面功能基本可用")
        print("\n要运行完整的TMCL启动器，您可能需要进一步修复UI组件的属性问题。")
    else:
        print("⚠️  测试完成，但存在一些问题需要解决。")
    print("="*50)
