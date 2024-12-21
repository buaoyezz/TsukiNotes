import webbrowser
from PyQt5.QtWidgets import (
    QWidget, QDialog, QVBoxLayout, QHBoxLayout, QListWidget,
    QStackedWidget, QPushButton, QLabel, QGridLayout,
    QScrollArea
)
from PyQt5.QtCore import Qt, QTimer
from tsuki.ui.utils.clut_card import ClutCard
from tsuki.ui.utils.clut_image_card import ClutImageCard
from tsuki.ui.utils.notification_manager import NotificationManager


class AboutPage(QWidget):
    def __init__(self, current_version=None, version_td=None, version_gj=None, update_Date=None):
        super().__init__()
        self.current_version = current_version or "未知"
        self.version_td = version_td or "未知"
        self.version_gj = version_gj or "未知" 
        self.update_Date = update_Date or "未知"
        self.setup_ui()
        self.notifications_shown = False

    def showEvent(self, event):
        super().showEvent(event)
        if not self.notifications_shown:
            QTimer.singleShot(100, self._show_about_notifications)
            self.notifications_shown = True

    def _show_about_notifications(self):
        notification = NotificationManager()
        
        notification.show_message(
            title="关于TsukiNotes",
            msg="在 GitHub 上查看 TsukiNotes 的项目主页",
            duration=3000
        )
        notification.show_message(
            title="开源许可证", 
            msg="本项目遵循 GPLv3.0 许可证供非商业使用",
            duration=3000
        )
        notification.show_message(
            title="版权声明",
            msg="TsukiNotes 版权所有 © 2024 by ZZBuAoYe",
            duration=3000
        )

    def setup_ui(self):
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # 设置窗口默认大小
        self.resize(940, 544)

        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # 设置滚动条样式
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

        # 创建内容容器
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        
        # 添加原有内容到content_layout
        title = QLabel("| 关于")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: black;
            }
        """)
        content_layout.addWidget(title)

        # Logo 部分使用 ClutImageCard
        logo_card = ClutImageCard(
            title="TsukiNotes",
            msg=" |基于 PyQt5 的记事本软件 \n |一部分基于ClutUI的UI框架 \n |Powered By ZZBuAoYe",
            image_url="./tsuki/assets/GUI/resources/GUI/logo.png",
            image_mode=1,
            image_align="center"
        )
        content_layout.addWidget(logo_card)

        # 版本信息卡片
        version_card = ClutCard(
            title="版本信息",
            msg=f"""Version: {self.current_version}
版本通道: {self.version_td}
内部版本号: {self.version_gj}
更新日期: {self.update_Date}"""
        )

        content_layout.addWidget(version_card)

        # 功能介绍卡片
        features_card = ClutCard(
            title="功能特性",
            msg="""TsukiNotes 是一款功能强大的记事本软件，现已支持:
            
• 支持文本高亮显示
• 可打开16进制文件  
• 支持Python、C++、Java和Markdown语法高亮
• 基于Qt内核，提供优秀的图形界面
• 丰富的QSS样式，带来美观的视觉体验
• 强大的搜索功能
• 超越Windows记事本的使用体验
• 支持多标签页,更高的效率
• 新的设计，新的思路，新的体验

探索更多精彩功能！无限可能！"""
        )
        content_layout.addWidget(features_card)

        # 版权信息卡片
        copyright_card = ClutCard(
            title="版权声明",
            msg="© TsukiNotes 2022-2024 ZZBuAoYe. All rights reserved.\n | GPL-3.0 License \n | Powered By ZZBuAoYe | PyQt-ClutUI"
        )
        content_layout.addWidget(copyright_card)

        # 设置滚动区域的内容
        scroll_area.setWidget(content_widget)
        
        # 添加滚动区域到主布局
        main_layout.addWidget(scroll_area)

    def open_url(self, url, event):
        if event.button() == Qt.LeftButton:
            webbrowser.open(url)
            self.notification_manager.show_message(
                title="正在跳转",
                msg="正在打开外部链接..."
            )