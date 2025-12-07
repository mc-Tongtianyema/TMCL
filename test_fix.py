#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简单测试脚本，验证修复是否有效
"""

import sys
import os

# 设置Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

print("测试脚本启动...")

try:
    # 导入PyQt5
    from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QProgressBar
    from PyQt5.QtCore import QThread, pyqtSignal, Qt, QTimer
    from PyQt5.QtGui import QPainter, QColor, QFont
    print("PyQt5导入成功！")
    
    # 测试SplashScreen修复
    class SplashScreen(QWidget):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("启动加载")
            self.setFixedSize(600, 400)
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
            
            # 添加进度条
            self.progress_bar = QProgressBar(self)
            self.progress_bar.setGeometry(100, 300, 400, 20)
            self.progress_bar.setValue(0)
            
            # 内部状态变量
            self._message = "正在启动TMCL启动器..."
            self._progress = 0
            self._is_painting = False
            
        def setMessage(self, message):
            self._message = message
            self.update()
        
        def setProgress(self, progress):
            self._progress = progress
            self.progress_bar.setValue(progress)
            self.update()
        
        def paintEvent(self, event):
            painter = QPainter(self)
            try:
                # 绘制背景
                painter.fillRect(self.rect(), QColor(45, 45, 45))
                
                # 绘制标题
                painter.setPen(QColor(255, 255, 255))
                painter.setFont(QFont("微软雅黑", 16, QFont.Bold))
                painter.drawText(200, 150, "TMCL启动器")
                
                # 绘制消息
                painter.setFont(QFont("微软雅黑", 10))
                painter.drawText(200, 200, self._message)
            finally:
                painter.end()
    
    # 模拟加载线程
    class PreloadThread(QThread):
        progress_updated = pyqtSignal(int, str)
        loading_completed = pyqtSignal()
        
        def run(self):
            # 模拟加载过程
            for i in range(0, 101, 10):
                message = f"正在加载资源... {i}%"
                self.progress_updated.emit(i, message)
                self.msleep(200)
            
            # 完成加载
            self.loading_completed.emit()
    
    # 主应用程序
    def main():
        app = QApplication(sys.argv)
        
        # 创建启动画面
        splash = SplashScreen()
        splash.show()
        
        # 创建加载线程
        preload_thread = PreloadThread()
        preload_thread.progress_updated.connect(lambda progress, message: (
            splash.setProgress(progress), splash.setMessage(message)
        ))
        
        # 创建主窗口函数
        def create_main_window():
            print("创建主窗口...")
            main_window = QWidget()
            main_window.setWindowTitle("TMCL启动器")
            main_window.setGeometry(100, 100, 800, 600)
            
            # 添加一些内容
            layout = QVBoxLayout()
            label = QLabel("TMCL启动器 - 修复测试成功！")
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)
            main_window.setLayout(layout)
            
            # 显示主窗口
            splash.hide()
            main_window.show()
            
            # 延迟清理加载线程
            QTimer.singleShot(0, preload_thread.deleteLater)
        
        # 加载完成信号处理
        def on_loading_completed():
            # 使用定时器延迟创建主窗口，确保线程安全
            QTimer.singleShot(200, create_main_window)
        
        preload_thread.loading_completed.connect(on_loading_completed)
        preload_thread.start()
        
        # 运行应用程序
        sys.exit(app.exec_())
    
    # 启动应用程序
    if __name__ == "__main__":
        main()
        
    print("测试脚本运行成功！")
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
