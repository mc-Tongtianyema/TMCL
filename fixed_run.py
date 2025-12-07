#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
修复版运行脚本，解决LoggerManager导入问题
"""

import sys
import os
import traceback

# 先确保所有必要的路径都在Python路径中
base_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(base_dir, 'src')

# 添加路径到sys.path
sys.path.insert(0, base_dir)
sys.path.insert(0, src_dir)

print(f"基础目录: {base_dir}")
print(f"源代码目录: {src_dir}")
print(f"Python路径: {sys.path}")

# 提前导入关键模块，确保依赖关系正确
print("预加载关键模块...")
try:
    # 先导入logger模块
    from src.utils.logger import LoggerManager, setup_logger
    print("LoggerManager导入成功")
    
    # 初始化日志系统
    logger_manager = LoggerManager()  # 全局日志配置
    logger = setup_logger("FixRunner")
    logger.info("修复版运行脚本启动")
    
    # 然后导入其他核心模块
    from src.core.constants import APP_NAME
    from src.core.config_manager import ConfigManager
    from src.core.version_manager import VersionManager
    from src.core.game_launcher import GameLauncher
    from src.api.bmcl_api import BMCLAPI
    print("核心模块导入成功")
    
    # 导入PyQt5组件
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QFont
    print("PyQt5模块导入成功")
    
    # 导入UI组件
    from src.ui.main_window import MainWindow, SplashScreen, PreloadThread
    print("UI组件导入成功")
    
except Exception as e:
    print(f"模块预加载失败: {type(e).__name__}: {e}")
    traceback.print_exc()

def run_application():
    """运行应用程序"""
    try:
        # 确保所有必要的模块在函数内部可用
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import Qt, QTimer
        from PyQt5.QtGui import QFont
        from src.core.constants import APP_NAME
        from src.core.config_manager import ConfigManager
        from src.core.version_manager import VersionManager
        from src.core.game_launcher import GameLauncher
        from src.api.bmcl_api import BMCLAPI
        from src.ui.main_window import MainWindow, SplashScreen, PreloadThread
        from src.utils.logger import setup_logger
        
        # 创建应用程序实例
        app = QApplication(sys.argv)
        
        # 设置应用程序属性
        app.setApplicationName(APP_NAME)
        app.setOrganizationName("TMCL")
        
        # 设置中文字体支持
        font = QFont()
        font.setFamily("SimHei")  # 确保支持中文
        app.setFont(font)
        
        # 创建启动画面
        splash = SplashScreen()
        splash.show_message("初始化启动器...", 0)
        splash.show()
        app.processEvents()
        
        # 再次确保日志系统初始化
        logger = setup_logger("Main")
        logger.info("TMCL启动器启动")
        
        # 创建核心组件实例 - 确保正确的初始化顺序
        config_manager = ConfigManager()
        bmcl_api = BMCLAPI()  # 使用正确的BMCLAPI类（有信号系统）
        version_manager = VersionManager(config_manager, bmcl_api)  # 传入必要的两个参数
        
        # 创建预加载线程
        preload_thread = PreloadThread(config_manager, version_manager, bmcl_api)
        
        def on_progress_updated(progress, message):
            """处理进度更新"""
            splash.show_message(message, progress)
            app.processEvents()
        
        def on_loading_completed():
            """处理加载完成"""
            nonlocal preload_thread, splash
            
            try:
                # 加载完成后，先更新最后的启动画面消息
                splash.show_message("启动完成！", 100)
                
                # 确保所有绘制操作完成
                from PyQt5.QtCore import QTimer
                
                def create_main_window():
                    try:
                        # 创建主窗口
                        game_launcher = GameLauncher(config_manager)
                        game_launcher.set_version_manager(version_manager)  # 设置版本管理器引用
                        main_window = MainWindow(
                            config_manager,
                            bmcl_api,
                            version_manager,
                            game_launcher
                        )
                        
                        # 确保splash完全清理后再显示主窗口
                        splash.hide()
                        
                        # 显示主窗口
                        main_window.show()
                        
                        # 记录启动成功
                        logger.info("启动器主窗口已显示")
                        
                    except Exception as e:
                        logger.error(f"启动器初始化失败: {e}")
                        traceback.print_exc()
                    finally:
                        # 延迟清理线程，确保UI操作完成
                        QTimer.singleShot(0, lambda: preload_thread.deleteLater())
                
                # 使用定时器确保绘制完成后再创建主窗口
                QTimer.singleShot(200, create_main_window)
                
            except Exception as e:
                logger.error(f"启动器初始化失败: {e}")
                traceback.print_exc()
        
        # 连接信号槽
        preload_thread.progress_updated.connect(on_progress_updated)
        preload_thread.loading_completed.connect(on_loading_completed)
        
        # 开始预加载
        preload_thread.start()
        
        # 运行应用程序
        return app.exec_()
        
    except Exception as e:
        # 异常处理
        print(f"应用程序运行异常: {type(e).__name__}: {e}")
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    print("\n开始运行应用程序...")
    sys.exit(run_application())
