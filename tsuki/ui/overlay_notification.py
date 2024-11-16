from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, 
                            QDesktopWidget, QPushButton, QApplication)
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
            Qt.X11BypassWindowManagerHint
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
        self.setFixedHeight(96)  # 根据实际需要调整
        self.setMinimumWidth(300)
        self.setMaximumWidth(400)  # 添加最大宽度限制

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
        self.setFixedHeight(96)
        
        self.move(screen.width() + 50, target_y)
        self.show()
        self.raise_()
        
        # 重置定时器
        self.timer.stop()
        if duration is not None:
            self.timer.start(duration)
        elif self.duration > 0:
            self.timer.start(self.duration)

    def _setup_ui(self):
        """设置UI"""
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(3)  # 减小标题和消息之间的间距
        
        # 标题标签
        self.title_label = QLabel()
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
        
        # 图标标签
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(24, 24)  # 设置固定大小
        
        # 容器布局
        self.container = QWidget(self)
        self.container.setObjectName("notificationContainer")
        self.container_layout = QHBoxLayout(self.container)
        self.container_layout.setContentsMargins(15, 10, 15, 10)
        self.container_layout.setSpacing(10)
        
        # 左侧布局：图标和文本
        self.left_widget = QWidget()
        self.left_layout = QVBoxLayout(self.left_widget)  # 改为垂直布局
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout.setSpacing(3)  # 设置标题和消息之间的间距
        
        self.left_layout.addWidget(self.title_label)
        self.left_layout.addWidget(self.message_label)
        
        # 关闭按钮
        self.close_btn = QPushButton("×")
        self.close_btn.setObjectName("closeButton")
        self.close_btn.setCursor(Qt.PointingHandCursor)
        self.close_btn.clicked.connect(self.start_exit_animation)
        
        # 添加到主布局
        self.container_layout.addWidget(self.icon_label)
        self.container_layout.addWidget(self.left_widget)
        self.container_layout.addWidget(self.close_btn)
        
        self.layout.addWidget(self.container)
        
        # 调整容器布局的边距
        self.container_layout.setContentsMargins(15, 10, 15, 10)
        
        # 设置消息标签的最大宽度
        self.message_label.setMaximumWidth(350)
        
        # 移除最小宽度设置，因为已经在构造函数中设置了
        # self.setMinimumWidth(300)
        # self.message_label.setMinimumWidth(200)
        
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