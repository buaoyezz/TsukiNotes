from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QProgressBar, QPushButton)
from PyQt5.QtCore import Qt, QTimer
from assets.utils.clut_button import ClutButton
from PyQt5.QtWidgets import QWidget

class ClutProgressDialog(QDialog):
    def __init__(self, parent=None, title="进度", can_background=True):
        super().__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(400, 200)
        
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建背景小部件
        self.bg_widget = QWidget()
        self.bg_widget.setObjectName("bg_widget")
        self.bg_widget.setStyleSheet("""
            QWidget#bg_widget {
                background: #2d2d2d;
                border-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        
        # 内容布局
        content_layout = QVBoxLayout(self.bg_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        title_layout = QHBoxLayout()
        title_label = QLabel(f"| {title}")
        title_label.setStyleSheet("""
            color: white;
            font-size: 16px;
            font-weight: bold;
        """)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        # 进度信息
        self.status_label = QLabel("准备中...")
        self.status_label.setStyleSheet("color: white; font-size: 14px;")
        
        # 速度和进度信息
        info_layout = QHBoxLayout()
        self.speed_label = QLabel("速度: 0 KB/s")
        self.speed_label.setStyleSheet("color: rgba(255,255,255,0.7); font-size: 12px;")
        self.progress_label = QLabel("0%")
        self.progress_label.setStyleSheet("color: rgba(255,255,255,0.7); font-size: 12px;")
        info_layout.addWidget(self.speed_label)
        info_layout.addStretch()
        info_layout.addWidget(self.progress_label)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background: rgba(255, 255, 255, 0.1);
                border: none;
                border-radius: 4px;
                height: 8px;
                text-align: center;
            }
            QProgressBar::chunk {
                background: #4A9EFF;
                border-radius: 4px;
            }
        """)
        self.progress_bar.setTextVisible(False)
        
        # 按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # 创建按钮但先不添加
        self.background_button = ClutButton("后台运行", primary=False)
        self.view_button = ClutButton("查看", primary=True)
        self.close_button = ClutButton("关闭", primary=False)
        
        if can_background:
            button_layout.addWidget(self.background_button)
            # 默认隐藏其他按钮
            self.view_button.hide()
            self.close_button.hide()
            button_layout.addWidget(self.view_button)
            button_layout.addWidget(self.close_button)
        
        # 添加所有元素
        content_layout.addLayout(title_layout)
        content_layout.addWidget(self.status_label)
        content_layout.addLayout(info_layout)
        content_layout.addWidget(self.progress_bar)
        content_layout.addStretch()
        content_layout.addLayout(button_layout)
        
        # 添加背景小部件到主布局
        main_layout.addWidget(self.bg_widget)
        
        # 初始化速度计算
        self._last_bytes = 0
        self._speed_timer = QTimer()
        self._speed_timer.timeout.connect(self._update_speed)
        self._speed_timer.start(1000)  # 每秒更新一次
        
    def _update_speed(self):
        """更新下载速度"""
        current_bytes = self.progress_bar.value()
        speed = current_bytes - self._last_bytes
        self._last_bytes = current_bytes
        
        if speed < 1024:
            speed_text = f"{speed} B/s"
        elif speed < 1024 * 1024:
            speed_text = f"{speed/1024:.1f} KB/s"
        else:
            speed_text = f"{speed/1024/1024:.1f} MB/s"
            
        self.speed_label.setText(f"速度: {speed_text}")
        
    def update_progress(self, value, total):
        """更新进度"""
        percentage = int(value / total * 100)
        self.progress_bar.setValue(value)
        self.progress_bar.setMaximum(total)
        self.progress_label.setText(f"{percentage}%")
        
    def set_status(self, text):
        """更新状态文本"""
        self.status_label.setText(text)
        
    def on_clone_complete(self):
        """克隆完成时更新UI"""
        self.status_label.setText("克隆完成")
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background: rgba(255, 255, 255, 0.1);
                border: none;
                border-radius: 4px;
                height: 8px;
                text-align: center;
            }
            QProgressBar::chunk {
                background: #4CAF50;
                border-radius: 4px;
            }
        """)
        # 切换按钮
        self.background_button.hide()
        self.view_button.show()
        self.close_button.show()