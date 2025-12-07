#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TMCL启动器 - 主入口文件
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 确保可以正确导入模块
try:
    # 尝试导入模块以验证路径设置
    pass
except ImportError:
    # 如果导入失败，添加当前目录到路径
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# 设置环境变量，确保中文显示正常
os.environ['QT_FONT_DPI'] = '96'

# 导入核心组件
from src.core.config_manager import ConfigManager
from src.core.version_manager import VersionManager
from src.core.game_launcher import GameLauncher
from src.utils.api_client import BMCLAPIClient
from src.utils.logger import LoggerManager

# 导入UI组件
from src.ui.main_window import MainWindow, SplashScreen, PreloadThread

# 导入常量
from src.core.constants import APP_NAME

def main():
    """
    应用程序主入口
    """
    try:
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
        
        # 初始化日志系统
        logger_manager = LoggerManager()
        logger = logger_manager.get_logger("Main")
        logger.info("TMCL启动器启动")
        
        # 创建核心组件实例
        config_manager = ConfigManager()
        version_manager = VersionManager(config_manager)
        bmcl_api = BMCLAPIClient()
        
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
                        game_launcher = GameLauncher(config_manager, version_manager)
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
                        import traceback
                        logger.error(traceback.format_exc())
                    finally:
                        # 延迟清理线程，确保UI操作完成
                        QTimer.singleShot(0, lambda: preload_thread.deleteLater())
                
                # 使用定时器确保绘制完成后再创建主窗口
                QTimer.singleShot(200, create_main_window)
                
            except Exception as e:
                logger.error(f"启动器初始化失败: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        # 连接信号槽
        preload_thread.progress_updated.connect(on_progress_updated)
        preload_thread.loading_completed.connect(on_loading_completed)
        
        # 开始预加载
        preload_thread.start()
        
        # 运行应用程序
        return app.exec_()
    except Exception as e:
        # 如果有未捕获的异常，确保记录日志
        try:
            from src.utils.logger import LoggerManager
            logger_manager = LoggerManager()
            logger = logger_manager.get_logger("Main")
            logger.error(f"程序未捕获异常: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
        except:
            pass
        print(f"严重错误: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
