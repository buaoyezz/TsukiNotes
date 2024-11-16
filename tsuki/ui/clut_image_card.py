from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QLabel, 
                           QGraphicsDropShadowEffect, QWidget, QSizePolicy)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtSignal,QSize
from PyQt5.QtGui import QColor, QPixmap, QCursor

class ClickableImageLabel(QLabel):
    """可点击的图片标签"""
    clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.PointingHandCursor)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

class ClutImageCard(QFrame):
    """
    图片卡片组件
    image_mode:
        0: 图片在上方，标题和内容在下方
        1: 图片在左侧，标题和内容在右侧
        2: 图片作为背景，内容覆盖在上面
        3: 图片在右侧，标题和内容在左侧
    """
    def __init__(self, title="", msg="", image_url="", image_mode=0, image_clickConnect=None, image_size=None, image_align="center", parent=None):
        super().__init__(parent)
        self.setObjectName("clutImageCard")
        self.image_url = image_url
        self.image_mode = image_mode
        self.image_clickConnect = image_clickConnect
        self.image_size = image_size
        self.image_align = image_align
        
        # 设置最大宽度
        self.setMaximumWidth(800)  # 限制最大宽度
        # 设置大小策略
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        self.setup_ui(title, msg)
        self.setup_animations()
        
    def setup_ui(self, title, msg):
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建容器
        self.container = QWidget()
        self.container.setObjectName("container")
        
        # 根据模式选择布局
        if self.image_mode == 0:  # 图片在上
            self._setup_vertical_layout(title, msg)
        elif self.image_mode == 1:  # 图片在左
            self._setup_horizontal_layout(title, msg, left_image=True)
        elif self.image_mode == 2:  # 图片作为背景
            self._setup_overlay_layout(title, msg)
        else:  # 图片在右
            self._setup_horizontal_layout(title, msg, left_image=False)
            
        main_layout.addWidget(self.container)
        
        # 添加阴影效果
        self._add_shadow_effect()
        
        # 设置基础样式
        self.setStyleSheet("""
            QFrame#clutImageCard {
                background-color: rgba(30, 30, 30, 0.6);
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            QFrame#clutImageCard:hover {
                background-color: rgba(35, 35, 35, 0.7);
                border: 1px solid rgba(255, 255, 255, 0.15);
            }
            
            QLabel#titleLabel {
                color: #ffffff;
                font-size: 16px;
                font-weight: 600;
                font-family: 'Microsoft YaHei';
                background: transparent;
            }
            
            QLabel#msgLabel {
                color: rgba(255, 255, 255, 0.9);
                font-size: 14px;
                line-height: 1.5;
                font-family: 'Microsoft YaHei';
                background: transparent;
            }
        """)
        
    def _setup_vertical_layout(self, title, msg):
        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        
        # 图片容器
        if self.image_url:
            image_container = QWidget()
            image_container.setObjectName("imageContainer")
            image_layout = QHBoxLayout(image_container)
            image_layout.setContentsMargins(20, 20, 20, 0)
            image_layout.setAlignment(Qt.AlignCenter)  # 居中对齐
            
            image_label = self._create_image_label()
            image_layout.addWidget(image_label)
            
            layout.addWidget(image_container)
        
        # 内容区域
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(12)
        
        title_label = self._create_title_label(title)
        msg_label = self._create_msg_label(msg)
        
        content_layout.addWidget(title_label)
        content_layout.addWidget(msg_label)
        content_layout.addStretch()
        
        layout.addWidget(content)
        
    def _setup_horizontal_layout(self, title, msg, left_image=True):
        layout = QHBoxLayout(self.container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 图片区域
        image_label = None
        if self.image_url:
            image_label = self._create_image_label()
            # 根据 image_align 设置对齐方式
            if self.image_mode in (1, 3):  # 图片在左侧或右侧时
                if self.image_align == "center":
                    image_label.setAlignment(Qt.AlignCenter)
                elif self.image_align == "left":
                    image_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                elif self.image_align == "right":
                    image_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        # 内容区域
        content = QWidget()
        content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(12)
        
        title_label = self._create_title_label(title)
        msg_label = self._create_msg_label(msg)
        
        content_layout.addWidget(title_label)
        content_layout.addWidget(msg_label)
        content_layout.addStretch()
        
        # 根据方向添加组件
        if left_image and image_label:
            layout.addWidget(image_label)
            layout.addWidget(content)
        else:
            layout.addWidget(content)
            if image_label:
                layout.addWidget(image_label)
                
    def _setup_overlay_layout(self, title, msg):
        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 背景图片
        if self.image_url:
            image_label = self._create_image_label()
            image_label.setObjectName("backgroundImage")
            layout.addWidget(image_label)
            
            # 内容覆盖层
            content = QWidget(image_label)
            content.setObjectName("overlay")
            content.setStyleSheet("""
                QWidget#overlay {
                    background: linear-gradient(transparent, rgba(0, 0, 0, 0.7));
                }
            """)
            
            content_layout = QVBoxLayout(content)
            content_layout.setContentsMargins(20, 20, 20, 20)
            content_layout.setSpacing(12)
            
            title_label = self._create_title_label(title)
            msg_label = self._create_msg_label(msg)
            
            content_layout.addStretch()
            content_layout.addWidget(title_label)
            content_layout.addWidget(msg_label)
            
            content.setLayout(content_layout)
            content.resize(image_label.size())
            
    def _create_image_label(self):
        image_label = ClickableImageLabel()
        image_label.setObjectName("imageLabel")
        
        # 设置大小策略
        image_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        if self.image_url:
            pixmap = QPixmap(self.image_url)
            
            if pixmap.isNull():
                print(f"警告: 无法加载图片 {self.image_url}")
                # 设置固定尺寸而不是最小尺寸
                if self.image_mode == 0:
                    image_label.setFixedSize(400, 200)
                elif self.image_mode in (1, 3):
                    image_label.setFixedSize(200, 160)
                else:
                    image_label.setFixedSize(400, 240)
                
                image_label.setStyleSheet("""
                    QLabel#imageLabel {
                        background-color: rgba(255, 255, 255, 0.05);
                        border-radius: 8px;
                    }
                """)
                image_label.setText("图片加载失败")
                image_label.setAlignment(Qt.AlignCenter)
                return image_label
            
            # 获取窗口大小
            window_size = self.window().size()
            
            # 根据模式和窗口大小计算目标尺寸
            if self.image_size:  # 如果用户指定了尺寸
                target_size = self.image_size
            else:
                if self.image_mode == 0:  # 图片在上方
                    target_size = QSize(int(window_size.width() * 0.5), int(window_size.height() * 0.3))
                elif self.image_mode in (1, 3):  # 图片在左侧或右侧
                    target_size = QSize(int(window_size.width() * 0.25), int(window_size.height() * 0.2))
                else:  # 图片作为背景
                    target_size = QSize(int(window_size.width() * 0.5), int(window_size.height() * 0.4))
            
            image_label.setFixedSize(target_size)
            
            # 缩放图片
            scaled_pixmap = pixmap.scaled(
                target_size,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            
            image_label.setPixmap(scaled_pixmap)
            
            image_label.setStyleSheet("""
                QLabel#imageLabel {
                    background-color: transparent;
                    border-radius: 8px;
                }
                QLabel#imageLabel:hover {
                    background-color: rgba(255, 255, 255, 0.05);
                }
            """)
            
        if self.image_clickConnect:
            image_label.clicked.connect(self.image_clickConnect)
        
        return image_label
        
    def _create_title_label(self, title):
        title_label = QLabel(title)
        title_label.setObjectName("titleLabel")
        return title_label
        
    def _create_msg_label(self, msg):
        msg_label = QLabel(msg)
        msg_label.setObjectName("msgLabel")
        msg_label.setWordWrap(True)
        return msg_label
        
    def _add_shadow_effect(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 40))
        self.setGraphicsEffect(shadow)
        
    def setup_animations(self):
        self.hover_anim = QPropertyAnimation(self, b"styleSheet")
        self.hover_anim.setDuration(200)
        self.hover_anim.setEasingCurve(QEasingCurve.OutCubic) 