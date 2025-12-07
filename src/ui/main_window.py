#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QStatusBar, QApplication
from PyQt5.QtCore import Qt, QSize, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QIcon, QPalette, QColor, QFont, QPainter
from PyQt5.Qt import QRect

from src.ui.styles.theme import theme
from src.ui.styles.stylesheet import StyleSheetGenerator
from src.ui.components.custom_label import CustomLabel

class PreloadThread(QThread):
    """
    预加载线程，用于在后台加载应用程序资源
    """
    progress_updated = pyqtSignal(int, str)
    loading_completed = pyqtSignal()
    
    def __init__(self, config_manager, version_manager, bmcl_api):
        """
        初始化预加载线程
        
        Args:
            config_manager: 配置管理器实例
            version_manager: 版本管理器实例
            bmcl_api: BMCL API实例
        """
        super().__init__()
        self.config_manager = config_manager
        self.version_manager = version_manager
        self.bmcl_api = bmcl_api
        
    def run(self):
        """
        运行预加载任务
        """
        try:
            # 配置已经在外部初始化，不需要再次加载
            self.progress_updated.emit(20, "初始化配置...")
            
            # 扫描本地版本
            self.progress_updated.emit(50, "扫描本地版本...")
            self.version_manager.scan_local_versions()
            
            # 获取远程版本信息 (可选，不阻塞UI)
            self.progress_updated.emit(80, "获取远程版本信息...")
            try:
                self.bmcl_api.get_versions()
            except Exception:
                # 网络请求失败不影响启动
                pass
            
            # 完成加载
            self.progress_updated.emit(100, "加载完成！")
            
        except Exception as e:
            from src.utils.logger import setup_logger
            logger = setup_logger("PreloadThread")
            logger.error(f"预加载失败: {e}")
        finally:
            # 确保发射完成信号
            self.loading_completed.emit()


class SplashScreen(QWidget):
    """
    启动加载界面 - 使用更安全的QWidget实现，避免QSplashScreen的线程安全问题
    """
    def __init__(self):
        """
        初始化启动加载界面
        """
        super().__init__()
        
        # 设置窗口属性
        self.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedSize(400, 250)
        
        # 存储当前消息和进度
        self._message = ""
        self._progress = 0
        
    def show_message(self, message, progress=0):
        """
        显示加载消息和进度
        
        Args:
            message: 加载消息
            progress: 进度值 (0-100)
        """
        # 更新内部状态
        self._message = message
        self._progress = progress
        
        # 触发重绘
        self.update()
        
    def paintEvent(self, event):
        """
        重写绘制事件，确保线程安全
        """
        # 创建QPainter，使用局部变量确保自动清理
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        try:
            # 绘制背景
            painter.fillRect(self.rect(), Qt.white)
            
            # 设置字体
            font = QFont()
            font.setPointSize(16)
            font.setBold(True)
            painter.setFont(font)
            
            # 绘制标题
            painter.setPen(QColor(52, 152, 219))  # 蓝色
            painter.drawText(QRect(0, 80, 400, 30), Qt.AlignCenter, "TMCL 启动器")
            
            # 绘制消息
            font.setPointSize(12)
            font.setBold(False)
            painter.setFont(font)
            painter.setPen(QColor(50, 50, 50))
            painter.drawText(QRect(0, 130, 400, 30), Qt.AlignCenter, self._message)
            
            # 绘制进度条背景
            painter.setPen(QColor(200, 200, 200))
            painter.setBrush(QColor(200, 200, 200))
            painter.drawRect(50, 180, 300, 10)
            
            # 绘制进度条
            painter.setPen(QColor(52, 152, 219))
            painter.setBrush(QColor(52, 152, 219))
            painter.drawRect(50, 180, int(300 * self._progress / 100), 10)
            
        finally:
            # 确保painter被正确清理
            painter.end()


class MainWindow(QMainWindow):
    """
    主窗口类，应用程序的主界面
    """
    
    def __init__(self, config_manager, bmcl_api, version_manager, game_launcher, parent=None):
        """
        初始化主窗口
        
        Args:
            config_manager: 配置管理器实例
            bmcl_api: BMCLAPI实例
            version_manager: 版本管理器实例
            game_launcher: 游戏启动器实例
            parent: 父窗口
        """
        super().__init__(parent)
        
        # 存储核心组件实例
        self.config_manager = config_manager
        self.bmcl_api = bmcl_api
        self.version_manager = version_manager
        self.game_launcher = game_launcher
        
        # 初始化UI
        self._init_ui()
        
        # 初始化窗口淡入动画
        self._init_animations()
        
        # 设置初始透明度
        self.setWindowOpacity(0.0)
    
    def _init_ui(self):
        """
        初始化UI组件
        """
        # 设置窗口基本属性
        self.setWindowTitle("TMCL - Minecraft启动器")
        self.setMinimumSize(QSize(900, 600))
        self.setGeometry(100, 100, 900, 600)  # 设置默认位置和大小
        
        # 设置窗口图标 (可以稍后添加)
        # self.setWindowIcon(QIcon("path/to/icon.ico"))
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建顶部栏
        self._create_header()
        main_layout.addWidget(self.header_widget)
        
        # 创建选项卡控件
        self.tab_widget = QTabWidget()
        self._setup_tab_widget()
        main_layout.addWidget(self.tab_widget, 1)  # 1表示伸缩因子，让选项卡占据大部分空间
        
        # 创建状态栏
        self._create_status_bar()
        
        # 初始化选项卡页面
        self._init_tabs()
        
        # 应用全局样式
        self._apply_global_style()
    
    def _create_header(self):
        """
        创建顶部栏
        """
        self.header_widget = QWidget()
        self.header_widget.setMinimumHeight(60)
        self.header_widget.setMaximumHeight(60)
        
        # 创建顶部栏布局
        header_layout = QHBoxLayout(self.header_widget)
        header_layout.setContentsMargins(20, 10, 20, 10)
        header_layout.setSpacing(16)
        
        # 创建启动器标题
        self.title_label = CustomLabel(
            "TMCL", 
            label_type=CustomLabel.HEADING_2,
            alignment=Qt.AlignLeft | Qt.AlignVCenter
        )
        header_layout.addWidget(self.title_label)
        
        # 添加分隔线
        separator = QWidget()
        separator.setMinimumWidth(1)
        separator.setMaximumWidth(1)
        separator.setStyleSheet(f"background-color: {theme.border};")
        header_layout.addWidget(separator)
        
        # 添加描述文本
        self.description_label = CustomLabel(
            "我的世界启动器", 
            label_type=CustomLabel.BODY,
            alignment=Qt.AlignLeft | Qt.AlignVCenter
        )
        header_layout.addWidget(self.description_label)
        
        # 添加伸缩项，将右侧内容推到最右边
        header_layout.addStretch(1)
        
        # 添加启动器版本信息
        from src.core.constants import VERSION as APP_VERSION
        self.version_label = CustomLabel(
            f"v{APP_VERSION}", 
            label_type=CustomLabel.CAPTION,
            alignment=Qt.AlignCenter
        )
        header_layout.addWidget(self.version_label)
        
        # 设置顶部栏样式
        self.header_widget.setStyleSheet(f"""
        background-color: {theme.surface};
        border-bottom: 1px solid {theme.border};
        """)
    
    def _setup_tab_widget(self):
        """
        设置选项卡控件
        """
        # 设置选项卡属性
        self.tab_widget.setTabPosition(QTabWidget.North)
        self.tab_widget.setMovable(False)
        self.tab_widget.setDocumentMode(True)
        self.tab_widget.setUsesScrollButtons(True)
        
        # 设置选项卡样式
        self.tab_widget.setStyleSheet(f"""
        QTabWidget::pane {{
            border: none;
            background-color: {theme.background};
        }}
        
        QTabBar::tab {{
            background-color: transparent;
            color: {theme.text_secondary};
            padding: 10px 20px;
            border-bottom: 2px solid transparent;
            font-size: {theme.font_size_normal}px;
            font-family: {theme.font_family};
            min-width: 100px;
        }}
        
        QTabBar::tab:selected {{
            color: {theme.primary};
            border-bottom: 2px solid {theme.primary};
        }}
        
        QTabBar::tab:hover {{
            color: {theme.text_primary};
            background-color: {theme.surface_dark};
        }}
        """)
    
    def _init_tabs(self):
        """
        初始化选项卡页面
        """
        # 导入页面类
        from src.ui.pages.launch_page import LaunchPage
        from src.ui.pages.version_page import VersionPage
        from src.ui.pages.settings_page import SettingsPage
        from src.ui.pages.about_page import AboutPage
        # 以下页面暂未实现，注释掉
        # from src.ui.pages.mod_page import ModPage
        # from src.ui.pages.account_page import AccountPage
        
        # 创建各个页面实例
        self.launch_page = LaunchPage(
            self.config_manager,
            self.game_launcher
        )
        
        self.version_page = VersionPage(
            self.config_manager,
            self.bmcl_api,
            self.version_manager,
            self.game_launcher,
            self
        )
        
        self.settings_page = SettingsPage(
            self.config_manager,
            self
        )
        
        self.about_page = AboutPage(
            self
        )
        
        # 添加页面到选项卡
        self.tab_widget.addTab(self.launch_page, "游戏启动")
        self.tab_widget.addTab(self.version_page, "游戏版本")
        # 以下页面暂未实现，暂时不添加
        # self.tab_widget.addTab(self.mod_page, "模组管理")
        # self.tab_widget.addTab(self.account_page, "账户")
        self.tab_widget.addTab(self.settings_page, "设置")
        self.tab_widget.addTab(self.about_page, "关于")
        
        # 连接选项卡切换信号
        self.tab_widget.currentChanged.connect(self._on_tab_changed)
    
    def _create_status_bar(self):
        """
        创建状态栏
        """
        # 创建状态栏
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        
        # 设置状态栏高度
        status_bar.setMinimumHeight(30)
        status_bar.setMaximumHeight(30)
        
        # 添加状态栏信息
        self.status_label = CustomLabel(
            "欢迎使用TMCL启动器！",
            label_type=CustomLabel.CAPTION
        )
        status_bar.addWidget(self.status_label)
        
        # 设置状态栏样式
        status_bar.setStyleSheet(f"""
        QStatusBar {{
            background-color: {theme.surface};
            color: {theme.text_secondary};
            border-top: 1px solid {theme.border};
        }}
        """)
    
    def _init_animations(self):
        """
        初始化动画效果
        """
        # 创建窗口淡入动画
        self.fade_animation = QPropertyAnimation(self, b'windowOpacity')
        self.fade_animation.setDuration(500)  # 动画持续时间
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.setEasingCurve(QEasingCurve.InOutQuad)  # 缓动曲线
        
    def showEvent(self, event):
        """
        窗口显示事件，用于触发淡入动画
        
        Args:
            event: 事件对象
        """
        super().showEvent(event)
        # 启动淡入动画
        self.fade_animation.start()
    
    def _apply_global_style(self):
        """
        应用全局样式
        """
        # 生成并应用全局样式表
        style_sheet = StyleSheetGenerator.generate()
        self.setStyleSheet(style_sheet)
        
        # 添加按钮和控件的动画样式
        animation_styles = """
        /* 按钮悬停动画 */
        QPushButton {
            border: 1px solid #4B5563;
            border-radius: 4px;
            padding: 6px 12px;
            background-color: #1F2937;
            color: #F9FAFB;
            transition: background-color 0.2s, border-color 0.2s, padding 0.2s;
        }
        
        QPushButton:hover {
            background-color: #374151;
            border-color: #3B82F6;
        }
        
        QPushButton:pressed {
            padding: 7px 11px;
            background-color: #3B82F6;
            color: #FFFFFF;
        }
        
        /* 进度条动画 */
        QProgressBar {
            border: 1px solid #4B5563;
            border-radius: 4px;
            text-align: center;
            background-color: #1F2937;
        }
        
        QProgressBar::chunk {
            background-color: #3B82F6;
            border-radius: 4px;
            transition: width 0.3s ease-in-out;
        }
        
        /* 滚动条样式 */
        QScrollBar:vertical {
            width: 8px;
            background: #1F2937;
            margin: 0px;
            border-radius: 4px;
        }
        
        QScrollBar::handle:vertical {
            background: #4B5563;
            min-height: 20px;
            border-radius: 4px;
            transition: background-color 0.2s;
        }
        
        QScrollBar::handle:vertical:hover {
            background: #3B82F6;
        }
        
        /* 标签页切换动画 */
        QTabWidget::pane {
            border: 1px solid #4B5563;
            border-radius: 4px;
        }
        
        QTabBar::tab {
            background-color: #1F2937;
            border: 1px solid #4B5563;
            border-bottom: none;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            padding: 8px 16px;
            margin-right: 2px;
            min-width: 80px;
            transition: background-color 0.2s, color 0.2s;
        }
        
        QTabBar::tab:hover {
            background-color: #374151;
        }
        
        QTabBar::tab:selected {
            background-color: #3B82F6;
            color: #FFFFFF;
            border-color: #3B82F6;
        }
        
        /* 标签页内容淡入效果 */
        QStackedWidget {
            background-color: #1F2937;
            border-radius: 0 4px 4px 4px;
        }
        
        /* 列表项悬停效果 */
        QListWidget::item {
            border-radius: 4px;
            padding: 8px;
            transition: background-color 0.2s;
        }
        
        QListWidget::item:hover {
            background-color: #374151;
        }
        
        QListWidget::item:selected {
            background-color: #3B82F6;
            color: #FFFFFF;
        }
        """
        
        # 合并样式表
        self.setStyleSheet(style_sheet + animation_styles)
        
        # 添加窗口大小变化时的平滑过渡效果
        self.setMinimumSize(QSize(800, 600))
    
    def _on_tab_changed(self, index):
        """
        选项卡切换处理
        
        Args:
            index: 当前选项卡索引
        """
        # 根据当前选项卡更新状态栏信息
        tab_names = ["游戏启动", "游戏版本", "设置", "关于"]
        if 0 <= index < len(tab_names):
            self.status_label.setText(f"当前页面: {tab_names[index]}")
            
            # 当切换到启动页面时，刷新版本列表
            if index == 0 and hasattr(self, 'launch_page'):
                self.launch_page.refresh_version_list()
        
        # 获取当前选中的标签页
        current_widget = self.tab_widget.widget(index)
        if current_widget and hasattr(current_widget, 'refresh_content'):
            # 如果当前页面支持刷新，调用刷新方法
            current_widget.refresh_content()
    
    def update_status_message(self, message):
        """
        更新状态栏消息
        
        Args:
            message: 要显示的消息
        """
        self.status_label.setText(message)
    
    def show_notification(self, title, message, notification_type="info"):
        """
        显示通知
        
        Args:
            title: 通知标题
            message: 通知消息
            notification_type: 通知类型 (info, success, warning, error)
        """
        # TODO: 实现通知系统
        # 临时使用状态栏显示消息
        self.update_status_message(f"{title}: {message}")
        
        # 可以使用QMessageBox来显示通知
        from PyQt5.QtWidgets import QMessageBox
        
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        
        # 根据通知类型设置图标
        icon_map = {
            "info": QMessageBox.Information,
            "success": QMessageBox.Information,  # Qt没有直接的成功图标，可以使用Information代替
            "warning": QMessageBox.Warning,
            "error": QMessageBox.Critical
        }
        
        msg_box.setIcon(icon_map.get(notification_type, QMessageBox.Information))
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
