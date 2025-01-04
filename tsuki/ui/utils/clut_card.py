from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QGraphicsDropShadowEffect, QFrame, QScrollArea)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor, QFont
import logging
import markdown

logger = logging.getLogger(__name__)

class UpdateLogLabel(QLabel):
    """专门用于更新日志的 Markdown 标签"""
    def __init__(self, md_text="", parent=None):
        super().__init__(parent)
        self.setTextFormat(Qt.RichText)
        html = markdown.markdown(md_text, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.nl2br',
            'markdown.extensions.sane_lists',
            'markdown.extensions.tables'
        ])
        styled_html = f"""
        <div style="
            font-family: 'Microsoft YaHei';
            line-height: 1.6;
            color: #000000;
        ">
            {html}
        </div>
        """
        self.setText(styled_html)
        self.setWordWrap(True)
        self.setOpenExternalLinks(True)
        self.setTextInteractionFlags(
            Qt.TextBrowserInteraction | 
            Qt.TextSelectableByMouse
        )

class MarkdownLabel(QLabel):
    """原始的 MarkdownLabel，保持简单的格式"""
    def __init__(self, md_text="", parent=None):
        super().__init__(parent)
        self.setTextFormat(Qt.RichText)
        html = markdown.markdown(md_text)
        self.setText(html)
        self.setWordWrap(True)
        self.setOpenExternalLinks(True)

class ClutCard(QFrame):
    def __init__(self, title="", msg="", parent=None):
        super().__init__(parent)
        self.setWindowTitle("TsukiNotes Update Log")
        self.setObjectName("clutCard")
        self.setup_ui(title, msg)
        self.setup_animations()
        
    def setup_ui(self, title, msg):
        # 主布局
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
        content_container.setContentsMargins(16, 0, 0, 0)
        
        # 消息文本
        msg_label = MarkdownLabel(msg, self)  # 使用 MarkdownLabel
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
        
        content_container.addWidget(msg_label)
        
        # 添加到主布局
        self.main_layout.addWidget(title_frame)
        self.main_layout.addLayout(content_container)
        
    def setup_animations(self):
        # 添加阴影效果
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
        
        # 设置样式
        self.setStyleSheet("""
            QFrame#clutCard {
                background-color: #1a1a1a;
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        
    def show_update_log(self, update_logs):
        try:
            # 清除现有内容
            while self.main_layout.count():
                item = self.main_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

            # 创建滚动区域
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setFrameShape(QFrame.NoFrame)
            scroll_area.setStyleSheet("""
                QScrollArea {
                    background: transparent;
                    border: none;
                }
                QScrollBar:vertical {
                    background: rgba(255, 255, 255, 0.1);
                    width: 8px;
                    border-radius: 4px;
                }
                QScrollBar::handle:vertical {
                    background: rgba(255, 255, 255, 0.2);
                    border-radius: 4px;
                }
                QScrollBar::handle:vertical:hover {
                    background: rgba(255, 255, 255, 0.3);
                }
            """)

            # 创建内容容器
            content_widget = QWidget()
            content_layout = QVBoxLayout(content_widget)
            content_layout.setSpacing(16)
            content_layout.setContentsMargins(20, 20, 20, 20)

            # 版本标题框
            version_frame = QFrame()
            version_frame.setObjectName("versionFrame")
            version_layout = QHBoxLayout(version_frame)
            version_layout.setContentsMargins(12, 8, 12, 8)

            version_label = QLabel("| TsukiNotes Update Log")
            version_label.setStyleSheet("""
                QLabel {
                    color: #000000;
                    font-size: 18px;
                    font-weight: bold;
                    background-color:transparent;
                    font-family: 'Microsoft YaHei';
                    padding: 8px 16px;
                    border-radius: 4px;
                }
            """)
            version_layout.addWidget(version_label)

            # 更新内容框
            content_frame = QFrame()
            content_frame.setObjectName("contentFrame")
            content_layout_inner = QVBoxLayout(content_frame)
            content_layout_inner.setContentsMargins(16, 12, 16, 12)

            # 使用新的 UpdateLogLabel 显示更新日志
            content_text = UpdateLogLabel(update_logs[0]['content'], content_frame)
            content_text.setStyleSheet("""
                QLabel {
                    color: #000000;
                    font-size: 14px;
                    line-height: 1.6;
                    font-family: 'Microsoft YaHei';
                    background: rgba(255, 255, 255, 0.95);
                    padding: 20px;
                    border-radius: 8px;
                }
                QLabel a {
                    color: #0366d6;
                    text-decoration: none;
                }
                QLabel a:hover {
                    text-decoration: underline;
                }
                QLabel h1 {
                    font-size: 24px;
                    font-weight: 600;
                    margin: 20px 0 10px 0;
                    border-bottom: 1px solid #eaecef;
                    padding-bottom: 10px;
                }
                QLabel h2 {
                    font-size: 20px;
                    font-weight: 600;
                    margin: 16px 0 8px 0;
                }
                QLabel h3 {
                    font-size: 16px;
                    font-weight: 600;
                    margin: 14px 0 7px 0;
                }
                QLabel p {
                    margin: 8px 0;
                }
                QLabel ul, QLabel ol {
                    margin: 8px 0;
                    padding-left: 20px;
                }
                QLabel li {
                    margin: 4px 0;
                }
                QLabel code {
                    font-family: 'Consolas', monospace;
                    background: rgba(27, 31, 35, 0.05);
                    padding: 2px 4px;
                    border-radius: 3px;
                }
                QLabel pre {
                    background: rgba(27, 31, 35, 0.05);
                    padding: 16px;
                    border-radius: 6px;
                    overflow-x: auto;
                    margin: 10px 0;
                }
                QLabel hr {
                    border: none;
                    border-top: 1px solid #eaecef;
                    margin: 16px 0;
                }
            """)
            content_layout_inner.addWidget(content_text)

            # 添加到主布局
            content_layout.addWidget(version_frame)
            content_layout.addWidget(content_frame)
            content_layout.addStretch()

            scroll_area.setWidget(content_widget)
            self.main_layout.addWidget(scroll_area)

            # 设置框架样式
            version_frame.setStyleSheet("""
                QFrame#versionFrame {
                    background-color: rgba(139, 92, 246, 0.2);
                    border-radius: 8px;
                    border: 1px solid rgba(139, 92, 246, 0.3);
                }
            """)
            content_frame.setStyleSheet("""
                QFrame#contentFrame {
                    background-color: rgba(255, 255, 255, 0.1);
                    border-radius: 8px;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                }
            """)

        except Exception as e:
            logger.error(f"更新日志显示失败: {str(e)}")
            error_label = QLabel(f"更新日志加载失败: {str(e)}")
            error_label.setStyleSheet("""
                QLabel {
                    color: #ff4444;
                    font-size: 14px;
                    padding: 16px;
                    background: rgba(255, 255, 255, 0.9);
                    border-radius: 4px;
                }
            """)
            self.main_layout.addWidget(error_label)