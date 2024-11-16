from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                           QPushButton, QLabel, QGraphicsDropShadowEffect,
                           QWidget, QApplication, QScrollArea)
from PyQt5.QtCore import Qt, QPropertyAnimation, QPoint, QParallelAnimationGroup, QEasingCurve, pyqtProperty
from PyQt5.QtGui import QColor, QFont, QTransform

class ClutMessageBox(QDialog):
    def __init__(self, parent=None, title="提示", text="", buttons=["确定"]):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.Dialog | 
            Qt.WindowStaysOnTopHint | 
            Qt.FramelessWindowHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setModal(True)
        
        # 初始化结果
        self.dragPos = None
        self.result = None
        
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: rgba(255, 255, 255, 0.1);
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.3);
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar:horizontal {
                background: rgba(255, 255, 255, 0.1);
                height: 8px;
                margin: 0px;
            }
            QScrollBar::handle:horizontal {
                background: rgba(255, 255, 255, 0.3);
                min-width: 20px;
                border-radius: 4px;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
        """)
        
        # 创建容器
        self.container = QWidget()
        self.container.setObjectName("container")
        self.container.setStyleSheet("""
            QWidget#container {
                background: #2d2d2d;
                border-radius: 8px;
            }
        """)
        
        # 容器布局
        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        # 创建标题容器
        title_container = QHBoxLayout()
        title_container.setSpacing(8)
        title_container.setContentsMargins(0, 0, 0, 0)
        
        # 竖线
        separator = QLabel("|")
        separator.setFixedWidth(15)
        separator.setStyleSheet("""
            QLabel {
                color: #0078d4;
                font-size: 18px;
                font-weight: bold;
            }
        """)
        
        # 标题文字
        title_text = QLabel(title)
        title_text.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 16px;
                font-weight: 600;
                font-family: 'Microsoft YaHei';
            }
        """)
        
        title_container.addWidget(separator)
        title_container.addWidget(title_text)
        title_container.addStretch()
        
        # 创建消息容器
        message_container = QHBoxLayout()
        message_container.setContentsMargins(15, 0, 0, 0)
        
        # 修改文本标签以支持HTML
        text_label = QLabel()
        text_label.setWordWrap(True)
        text_label.setOpenExternalLinks(True)  # 支持点击链接
        text_label.setTextFormat(Qt.RichText)  # 设置为富文本格式
        text_label.setText(text)
        text_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                font-size: 14px;
                font-family: 'Microsoft YaHei';
                padding: 10px;
                background: transparent;
            }
        """)
        
        message_container.addWidget(text_label)
        
        # 按钮容器
        button_container = QHBoxLayout()
        button_container.setSpacing(10)
        button_container.addStretch()
        
        # 创建按钮
        self.buttons = []
        def create_click_handler(btn_text):
            def handler():
                self.result = btn_text
                self.close_with_animation()
            return handler
        
        for btn_text in buttons:
            btn = QPushButton(btn_text)
            btn.setFixedSize(100, 32)
            btn.setCursor(Qt.PointingHandCursor)
            
            if btn_text == buttons[-1]:  # 主要按钮
                btn.setStyleSheet("""
                    QPushButton {
                        background: #0078d4;
                        border: none;
                        border-radius: 4px;
                        color: white;
                        font-size: 14px;
                        font-family: 'Microsoft YaHei';
                    }
                    QPushButton:hover {
                        background: #2b88d8;
                    }
                    QPushButton:pressed {
                        background: #006cbe;
                    }
                """)
            else:  # 次要按钮
                btn.setStyleSheet("""
                    QPushButton {
                        background: rgba(255, 255, 255, 0.06);
                        border: 1px solid rgba(255, 255, 255, 0.1);
                        border-radius: 4px;
                        color: white;
                        font-size: 14px;
                        font-family: 'Microsoft YaHei';
                    }
                    QPushButton:hover {
                        background: rgba(255, 255, 255, 0.08);
                        border: 1px solid rgba(255, 255, 255, 0.15);
                    }
                    QPushButton:pressed {
                        background: rgba(255, 255, 255, 0.1);
                    }
                """)
            
            btn.clicked.connect(create_click_handler(btn_text))
            button_container.addWidget(btn)
            self.buttons.append(btn)
        
        # 添加所有元素到布局
        layout.addLayout(title_container)
        layout.addLayout(message_container)
        layout.addStretch()
        layout.addLayout(button_container)
        
        # 设置滚动区域的内容
        scroll_area.setWidget(self.container)
        
        # 添加滚动区域到主布局
        main_layout.addWidget(scroll_area)
        
        # 添加阴影效果
        shadow = QGraphicsDropShadowEffect(self.container)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 4)
        self.container.setGraphicsEffect(shadow)
        
        # 自动调整大小
        self.adjustSize()
        screen = QApplication.primaryScreen().geometry()
        max_height = int(screen.height() * 0.8)  # 最大高度为屏幕高度的80%
        max_width = int(screen.width() * 0.8)   # 最大宽度为屏幕宽度的80%
        
        # 设置最小和最大尺寸
        self.setMinimumSize(400, 200)
        self.setMaximumSize(max_width, max_height)
        
        # 根据内容自动调整大小，但不超过最大尺寸
        content_size = self.container.sizeHint()
        final_width = min(max(250, content_size.width() + 50), max_width)
        final_height = min(max(150, content_size.height() + 50), max_height)
        self.resize(final_width, final_height)

    def setup_animations(self):
        """设置动画"""
        # 创建动画组
        self.show_animation_group = QParallelAnimationGroup(self)
        
        # 位置动画
        self.pos_anim = QPropertyAnimation(self, b"pos")
        self.pos_anim.setDuration(300)
        self.pos_anim.setEasingCurve(QEasingCurve.OutBack)  # 使用弹性曲线
        
        # 透明度动画
        self.opacity_anim = QPropertyAnimation(self, b"windowOpacity")
        self.opacity_anim.setDuration(200)
        self.opacity_anim.setEasingCurve(QEasingCurve.OutCubic)
        
        # 添加到动画组
        self.show_animation_group.addAnimation(self.pos_anim)
        self.show_animation_group.addAnimation(self.opacity_anim)

    def show_with_animation(self):
        """显示动画"""
        # 获取屏幕尺寸和目标位置
        screen = QApplication.primaryScreen().geometry()
        target_x = (screen.width() - self.width()) // 2
        target_y = (screen.height() - self.height()) // 2
        
        # 设置初始位置（从目标位置下方50像素开始）
        start_y = target_y + 50
        self.move(target_x, start_y)
        
        # 设置初始透明度
        self.setWindowOpacity(0.0)
        
        # 配置位置动画
        self.pos_anim.setStartValue(QPoint(target_x, start_y))
        self.pos_anim.setEndValue(QPoint(target_x, target_y))
        
        # 配置透明度动画
        self.opacity_anim.setStartValue(0.0)
        self.opacity_anim.setEndValue(1.0)
        
        # 开始动画组
        self.show_animation_group.start()

    def close_with_animation(self):
        """带动画的关闭"""
        if hasattr(self, 'fade_anim') and self.fade_anim.state() == QPropertyAnimation.Running:
            return
            
        # 创建淡出动画
        self.fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self.fade_anim.setDuration(200)
        self.fade_anim.setStartValue(1.0)
        self.fade_anim.setEndValue(0.0)
        self.fade_anim.setEasingCurve(QEasingCurve.OutCubic)
        
        def finish_close():
            self.accept()
            self.fade_anim = None
            
        self.fade_anim.finished.connect(finish_close)
        self.fade_anim.start()

    @staticmethod
    def show_message(parent=None, title="提示", text="", buttons=None):
        if buttons is None:
            buttons = ["确定"]
        dialog = ClutMessageBox(parent, title, text, buttons)
        if parent:
            # 调整位置到父窗口中心
            center = parent.geometry().center()
            dialog.move(center.x() - dialog.width() // 2,
                       center.y() - dialog.height() // 2)
        
        dialog.setup_animations()
        dialog.show()
        dialog.show_with_animation()
        dialog.exec_()  # 执行对话框
        return dialog.result  # 返回结果字符串

    # 添加缩放属性支持
    def setScale(self, scale):
        """设置缩放值"""
        self.container.setProperty("scale", scale)
        # 计算缩放中心点
        center = self.container.rect().center()
        transform = QTransform()
        transform.translate(center.x(), center.y())
        transform.scale(scale, scale)
        transform.translate(-center.x(), -center.y())
        self.container.setTransform(transform)
    
    def getScale(self):
        """获取缩放值"""
        return self.container.property("scale")
    
    scale = pyqtProperty(float, getScale, setScale)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPos)
            event.accept()
            
    def keyPressEvent(self, event):
        """处理按键事件"""
        if event.key() == Qt.Key_Escape:
            self.close_with_animation()
        else:
            super().keyPressEvent(event)