from PyQt5.QtWidgets import QFrame, QHBoxLayout, QPushButton, QLabel, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QRect, QPoint

class Clut_Bar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(40)
        self.setStyleSheet("""
            QFrame {
                background-color: #202020;
                color: white;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }
            QPushButton {
                border: none;
                background-color: transparent;
                color: white;
                padding: 5px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
            }
        """)

        # 初始化动画和状态
        self._is_maximized = False
        self._normal_geometry = None
        self.animation = QPropertyAnimation(self.window(), b"geometry")
        self.animation.setEasingCurve(QEasingCurve.OutCubic)  # 使用更平滑的曲线
        self.animation.setDuration(100)  # 增加动画持续时间以提高流畅性
        
        # 获取屏幕尺寸
        self.screen = QApplication.primaryScreen().availableGeometry()

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 0, 0, 0)
        self.title = QLabel(" ClutCommitCanvas")
        self.title.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(self.title)

        self.min_button = QPushButton()
        self.min_button.setIcon(QIcon("assets/icons/mini.png"))
        
        self.max_button = QPushButton()
        self.max_button.setIcon(QIcon("assets/icons/max3.png"))
        
        self.close_button = QPushButton()
        self.close_button.setIcon(QIcon("assets/icons/close2.png"))
        
        for btn in [self.min_button, self.max_button, self.close_button]:
            btn.setFixedSize(QSize(40, 30))
            layout.addWidget(btn)

        self.setLayout(layout)
        self.start_pos = None
        
        self.min_button.clicked.connect(self.window().showMinimized)
        self.max_button.clicked.connect(self.toggle_maximize_animation)
        self.close_button.clicked.connect(self.window().close)
        
        # 添加新的属性来跟踪拖动状态
        self.dragging = False
        self.drag_start_position = None
        
        # 修改动画持续时间和曲线
        self.animation.setDuration(150)  # 稍微增加动画时间使其更流畅
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)  # 使用更自然的缓动曲线
        
    def toggle_maximize_animation(self):
        """切换最大化状态的动画"""
        if self.animation.state() == QPropertyAnimation.Running:
            return
            
        if not self._is_maximized:
            self._maximize_window()
        else:
            self._restore_window()
            
        self.animation.start()
        
    def _maximize_window(self):
        """最大化窗口"""
        self._normal_geometry = self.window().geometry()
        self.animation.setStartValue(self._normal_geometry)
        self.animation.setEndValue(self.screen)
        self._is_maximized = True
        self.max_button.setIcon(QIcon("assets/icons/restore.png"))  # 更改为还原图标

    def _restore_window(self):
        """还原窗口"""
        self.animation.setStartValue(self.window().geometry())
        self.animation.setEndValue(self._normal_geometry)
        self._is_maximized = False
        self.max_button.setIcon(QIcon("assets/icons/max3.png"))  # 更改为最大化图标
            
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_start_position = event.globalPos()
            self.window_start_position = self.window().pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton and self.dragging):
            return
            
        # 计算移动距离
        delta = event.globalPos() - self.drag_start_position
        
        if self._is_maximized:
            # 如果窗口最大化，先还原窗口
            self._restore_window_at_cursor(event.globalPos())
        else:
            # 限制窗口在屏幕范围内
            new_pos = self.window_start_position + delta
            new_pos.setX(max(0, min(new_pos.x(), 
                self.screen.width() - self.window().width())))
            new_pos.setY(max(0, min(new_pos.y(), 
                self.screen.height() - self.window().height())))
            self.window().move(new_pos)
        
        event.accept()

    def mouseReleaseEvent(self, event):
        self.dragging = False
        self.drag_start_position = None
        self.window_start_position = None
        event.accept()

    def _restore_window_at_cursor(self, global_pos):
        """在鼠标位置还原窗口"""
        if not self._normal_geometry:
            return
            
        # 计算鼠标在窗口中的相对位置比例
        ratio = (global_pos.x() - self.screen.left()) / self.screen.width()
        target_width = self._normal_geometry.width()
        
        # 计算新窗口位置，使鼠标保持在相对位置
        new_x = global_pos.x() - (target_width * ratio)
        new_y = global_pos.y() - 20  # 标题栏高度的一半左右
        
        # 设置新的窗口几何属性
        self._normal_geometry.moveTopLeft(QPoint(int(new_x), int(new_y)))
        self.window().setGeometry(self._normal_geometry)
        self._is_maximized = False
        self.max_button.setIcon(QIcon("assets/icons/max3.png"))
        
        # 更新拖动起始位置
        self.drag_start_position = global_pos
        self.window_start_position = self.window().pos()

    def mouseDoubleClickEvent(self, event):
        """双击标题栏切换最大化状态"""
        if event.button() == Qt.LeftButton:
            self.toggle_maximize_animation()