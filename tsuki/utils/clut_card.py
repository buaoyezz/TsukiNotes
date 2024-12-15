from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QGraphicsDropShadowEffect, QFrame)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor, QFont

class ClutCard(QFrame):
    def __init__(self, title="", msg="", parent=None):
        super().__init__(parent)
        self.setObjectName("clutCard")
        self.setup_ui(title, msg)
        self.setup_animations()
        
    def setup_ui(self, title, msg):
        # 主布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # 标题容器
        title_container = QHBoxLayout()
        title_container.setSpacing(8)
        
        # 分隔符
        separator = QLabel("|")
        separator.setFixedWidth(4)
        separator.setStyleSheet("""
            QLabel {
                color: #8B5CF6;
                font-size: 18px;
                font-weight: bold;
                background: transparent;
                padding: 0px;
            }
        """)
        
        # 标题
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 16px;
                font-weight: 600;
                font-family: 'Microsoft YaHei';
                background: transparent;
                padding: 0px;
            }
        """)
        
        # 标题背景框
        title_frame = QFrame()
        title_frame.setObjectName("titleFrame")
        title_frame_layout = QHBoxLayout(title_frame)
        title_frame_layout.setContentsMargins(12, 8, 12, 8)
        title_frame_layout.addWidget(separator)
        title_frame_layout.addWidget(title_label)
        title_frame_layout.addStretch()
        
        # 内容容器（用于对齐）
        content_container = QHBoxLayout()
        content_container.setContentsMargins(16, 0, 0, 0)  # 左边距16px，与标题文字对齐
        
        # 消息文本
        msg_label = QLabel(msg)
        msg_label.setWordWrap(True)
        msg_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                font-size: 14px;
                line-height: 1.5;
                font-family: 'Microsoft YaHei';
                background: transparent;
                padding: 0px;
            }
        """)
        
        # 将消息文本添加到内容容器
        content_container = QHBoxLayout()
        content_container.setContentsMargins(16, 0, 16, 0)
        content_container.addWidget(msg_label)
        
        # 添加到主布局
        layout.addWidget(title_frame)
        layout.addLayout(content_container)
        layout.addStretch()
        
        # 卡片样式
        self.setStyleSheet("""
            QFrame#clutCard {
                background-color: rgba(30, 30, 30, 0.6);
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            QFrame#titleFrame {
                background-color: rgba(139, 92, 246, 0.15);
                border-radius: 8px;
                border: none;
            }
            
            QFrame#clutCard:hover {
                background-color: rgba(35, 35, 35, 0.7);
                border: 1px solid rgba(255, 255, 255, 0.15);
            }
        """)
        
        # 添加拟态效果
        outer_shadow = QGraphicsDropShadowEffect()
        outer_shadow.setBlurRadius(20)
        outer_shadow.setOffset(8, 8)
        outer_shadow.setColor(QColor(0, 0, 0, 40))
        
        inner_shadow = QGraphicsDropShadowEffect()
        inner_shadow.setBlurRadius(20)
        inner_shadow.setOffset(-8, -8)
        inner_shadow.setColor(QColor(255, 255, 255, 10))
        
        # 应用阴影效果
        title_frame.setGraphicsEffect(inner_shadow)
        self.setGraphicsEffect(outer_shadow)
        
    def setup_animations(self):
        # 悬停动画
        self.hover_anim = QPropertyAnimation(self, b"styleSheet")
        self.hover_anim.setDuration(200)
        self.hover_anim.setEasingCurve(QEasingCurve.OutCubic)
        
    def enterEvent(self, event):
        self.setCursor(Qt.PointingHandCursor)
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        super().leaveEvent(event) 