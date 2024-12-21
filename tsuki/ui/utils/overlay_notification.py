from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, 
                            QDesktopWidget, QPushButton, QApplication, QSizePolicy)
from PyQt5.QtCore import (Qt, QTimer, QPoint, QPropertyAnimation, 
                         QEasingCurve, QSequentialAnimationGroup, pyqtSignal)
from PyQt5.QtGui import QColor, QFont, QFontDatabase

class OverlayNotification(QWidget):
    closed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(None)
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool |
            Qt.NoDropShadowWindowHint |
            Qt.X11BypassWindowManagerHint |
            Qt.SubWindow
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        
        self._setup_ui()
        
        # 初始化动画
        self.slide_animation = QPropertyAnimation(self, b"pos")
        self.slide_animation.setDuration(500)
        
        # 设置定时器
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)  # 确保定时器只触发一次
        self.timer.timeout.connect(self.start_exit_animation)
        self.duration = 3000

        self.is_closing = False
        self.is_exiting = False  # 新增：标记是否正在执行退出动画

        # 创建动画序列组
        self.exit_animation_group = QSequentialAnimationGroup(self)
        self.exit_animation_group.finished.connect(self._on_exit_finished)
        
        # 创建弹跳动画
        self.bounce_animation = QPropertyAnimation(self, b"pos")

        # 设置固定高度
        self.setFixedHeight(100)  # 根据实际需要调整
        self.setMinimumWidth(300)
        self.setMaximumWidth(400)  # 添加最大宽度限制
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)  # 新增：设置大小策略
        
        # 添加默认的链接跳转消息
        self.default_linkout_title = "正在跳转外部链接"
        self.default_linkout_message = "即将在浏览器中打开链接"

    def show_message(self, title="", message="", icon=None, duration=None):
        """显示消息"""
        if self.is_closing or self.is_exiting:
            return
            
        self.title_label.setText(title)
        self.message_label.setText(message)
        
        if icon is not None and not icon.isNull():
            # 缩放图标到合适大小
            scaled_icon = icon.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.icon_label.setPixmap(scaled_icon)
            self.icon_label.show()
        else:
            self.icon_label.hide()
            
        self.adjustSize()
        
        screen = QApplication.primaryScreen().geometry()
        target_x = screen.width() - self.width() - 20
        target_y = self.y() if self.y() > 0 else 40
        
        # 强制设置正确的大小
        self.setFixedHeight(100)
        
        self.move(screen.width() + 50, target_y)
        self.show()
        self.raise_()
        
        # 重置定时器
        self.timer.stop()
        if duration is not None:
            self.timer.start(duration)
        elif self.duration > 0:
            self.timer.start(self.duration)            
    def linkout(self, title=None, message=None, duration=2000):
        """显示链接跳转通知"""
        self.show_message(
            title=title or self.default_linkout_title,
            message=message or self.default_linkout_message,
            duration=duration
        )

    def _setup_ui(self):
        """设置UI"""
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 容器布局
        self.container = QWidget(self)
        self.container.setObjectName("notificationContainer")
        self.container_layout = QHBoxLayout(self.container)
        self.container_layout.setContentsMargins(15, 10, 15, 10)
        self.container_layout.setSpacing(10)
        
        # 左侧布局：图标和文本
        self.left_widget = QWidget()
        self.left_layout = QVBoxLayout(self.left_widget)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout.setSpacing(5)
        
        # 标题标签
        self.title_label = QLabel()
        self.title_label.setFixedHeight(30)
        self.title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        
        # 消息标签
        self.message_label = QLabel()
        self.message_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 180);
                font-size: 12px;
            }
        """)
        self.message_label.setWordWrap(True)
        self.message_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        # 图标标签
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(24, 24)
        
        # 添加标题和消息到左侧布局
        self.left_layout.addWidget(self.title_label)
        self.left_layout.addWidget(self.message_label)
        
        # 关闭按钮
        self.close_btn = QPushButton("×")
        self.close_btn.setObjectName("closeButton")
        self.close_btn.setCursor(Qt.PointingHandCursor)
        self.close_btn.clicked.connect(self.start_exit_animation)
        
        # 添加到容器布局
        self.container_layout.addWidget(self.icon_label)
        self.container_layout.addWidget(self.left_widget)
        self.container_layout.addWidget(self.close_btn)
        
        # 添加容器到主布局
        main_layout.addWidget(self.container)
        
        # 设置消息标签的最大宽度
        self.message_label.setMaximumWidth(350)
        
        # 确保所有控件的大小策略一致
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # 设置样式
        self.setStyleSheet("""
            #notificationContainer {
                background-color: rgba(40, 40, 40, 240);
                border-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 30);
            }
            #closeButton {
                background: transparent;
                border: none;
                color: white;
                font-size: 18px;
                font-weight: bold;
                width: 24px;
                height: 24px;
                border-radius: 12px;
                padding: 0px;
            }
            #closeButton:hover {
                background: rgba(255, 255, 255, 30);
            }
            #closeButton:pressed {
                background: rgba(255, 255, 255, 50);
            }
        """)
        
        # 调整容器布局的边距
        self.container_layout.setContentsMargins(15, 10, 15, 10)
        
        # 确保调整大小以适应内容
        self.adjustSize()

    def start_exit_animation(self):
        """开始退出动画"""
        if self.is_closing or self.is_exiting:
            return
            
        self.is_exiting = True
        self.timer.stop()
        
        screen = QDesktopWidget().screenGeometry()
        current_pos = self.pos()
        current_x = current_pos.x()
        current_y = current_pos.y()
        
        # 清理现有动画
        self.exit_animation_group.clear()
        
        # 弹跳动画
        self.bounce_animation.setDuration(100)
        self.bounce_animation.setStartValue(current_pos)
        self.bounce_animation.setEndValue(QPoint(current_x + 35, current_y))
        self.bounce_animation.setEasingCurve(QEasingCurve.OutQuad)
        
        # 滑出动画
        self.slide_animation.setDuration(200)
        self.slide_animation.setStartValue(QPoint(current_x + 35, current_y))
        self.slide_animation.setEndValue(QPoint(screen.width() + 50, current_y))
        self.slide_animation.setEasingCurve(QEasingCurve.InCubic)
        
        self.exit_animation_group.addAnimation(self.bounce_animation)
        self.exit_animation_group.addAnimation(self.slide_animation)
        self.exit_animation_group.start()

    def _on_exit_finished(self):
        """动画结束后的清理工作"""
        self.is_closing = True
        self.is_exiting = False
        self.hide()
        self.timer.stop()
        self.closed.emit()
        
    def hide(self):
        """确保在隐藏时停止所有动画和定时器"""
        self.timer.stop()
        if self.exit_animation_group.state() == self.exit_animation_group.Running:
            self.exit_animation_group.stop()
        super().hide()

    def closeEvent(self, event):
        """处理窗口关闭事件"""
        if not self.is_closing and not self.is_exiting:
            event.ignore()
            self.start_exit_animation()
        else:
            event.accept()
