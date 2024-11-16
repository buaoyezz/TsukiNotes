from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QGraphicsDropShadowEffect, QFrame)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor, QFont

class ClutCard(QFrame):
    def __init__(self, title="", msg="", parent=None):
        super().__init__(parent)
        self.setObjectName("clutCard")
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(16)
        
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
            }
        """)
        
        # 标题
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 16px;
                font-weight: 600;
                font-family: 'Microsoft YaHei';
                background: transparent;
            }
        """)
        
        # 标题背景框
        title_frame = QFrame()
        title_frame.setObjectName("titleFrame")
        title_frame_layout = QHBoxLayout(title_frame)
        title_frame_layout.setContentsMargins(12, 8, 12, 8)
        title_frame_layout.addWidget(separator)
        title_frame_layout.addWidget(self.title_label)
        title_frame_layout.addStretch()
        
        # 内容区域
        self.content_widget = QWidget()
        self.content_widget.setObjectName("contentWidget")
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(16, 16, 16, 16)
        self.content_layout.setSpacing(16)
        
        if msg:
            msg_label = QLabel(msg)
            msg_label.setWordWrap(True)
            msg_label.setStyleSheet("""
                QLabel {
                    color: rgba(255, 255, 255, 0.9);
                    font-size: 14px;
                    line-height: 1.5;
                    font-family: 'Microsoft YaHei';
                    background: transparent;
                }
            """)
            self.content_layout.addWidget(msg_label)
        
        # 添加到主布局
        self.main_layout.addWidget(title_frame)
        self.main_layout.addWidget(self.content_widget)
        
        # 设置样式
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
            
            QWidget#contentWidget {
                background: transparent;
            }
            
            QFrame#clutCard:hover {
                background-color: rgba(35, 35, 35, 0.7);
                border: 1px solid rgba(255, 255, 255, 0.15);
            }
        """)

    def setContentLayout(self, layout):
        # 清除现有内容
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # 添加新的布局
        self.content_layout.addLayout(layout)