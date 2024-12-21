from PyQt5.QtWidgets import QPushButton, QLineEdit, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve
from PyQt5.QtGui import QPainter, QColor, QPen, QLinearGradient

class ClutLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QLineEdit {
                border: 1px solid rgba(255, 255, 255, 0.1);
                background-color: rgba(255, 255, 255, 0.06);
                border-radius: 4px;
                padding: 8px 12px;
                color: #ffffff;
                font-size: 14px;
                font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
            }
            
            QLineEdit:hover {
                background-color: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.15);
            }
            
            QLineEdit:focus {
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid #60CDFF;
            }
            
            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 0.5);
            }
        """)
        
        self.setMinimumHeight(32)

class ClutButton(QPushButton):
    def __init__(self, text="", parent=None, primary=True):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self._primary = primary
        self._pressed = False
        
        # 背景色动画
        self._color_animation = QPropertyAnimation(self, b"styleSheet", self)
        self._color_animation.setDuration(150)
        
        self._setup_default_style()
        
    def _setup_default_style(self):
        """设置默认样式 - Windows Fluent Design"""
        self.setFixedHeight(32)
        self.setMinimumWidth(120 if self._primary else 100)
        
        if self._primary:
            self._normal_style = """
                QPushButton {
                    background-color: #60CDFF;
                    border: 1px solid #60CDFF;
                    border-radius: 4px;
                    color: #000000;
                    padding: 0 16px;
                    font-size: 14px;
                    font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
                }
            """
            self._hover_style = """
                QPushButton {
                    background-color: #8CD8FF;
                    border: 1px solid #8CD8FF;
                    border-radius: 4px;
                    color: #000000;
                    padding: 0 16px;
                    font-size: 14px;
                    font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
                }
            """
            self._pressed_style = """
                QPushButton {
                    background-color: #38BBFF;
                    border: 1px solid #38BBFF;
                    border-radius: 4px;
                    color: #000000;
                    padding: 0 16px;
                    font-size: 14px;
                    font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
                }
            """
            self._disabled_style = """
                QPushButton {
                    background-color: rgba(96, 205, 255, 0.3);
                    border: 1px solid rgba(96, 205, 255, 0.3);
                    border-radius: 4px;
                    color: rgba(0, 0, 0, 0.36);
                    padding: 0 16px;
                    font-size: 14px;
                    font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
                }
            """
        else:
            self._normal_style = """
                QPushButton {
                    background-color: rgba(255, 255, 255, 0.06);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    border-radius: 4px;
                    color: #ffffff;
                    padding: 0 16px;
                    font-size: 14px;
                    font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
                }
            """
            self._hover_style = """
                QPushButton {
                    background-color: rgba(255, 255, 255, 0.08);
                    border: 1px solid rgba(255, 255, 255, 0.15);
                    border-radius: 4px;
                    color: #ffffff;
                    padding: 0 16px;
                    font-size: 14px;
                    font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
                }
            """
            self._pressed_style = """
                QPushButton {
                    background-color: rgba(255, 255, 255, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.15);
                    border-radius: 4px;
                    color: #ffffff;
                    padding: 0 16px;
                    font-size: 14px;
                    font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
                }
            """
            self._disabled_style = """
                QPushButton {
                    background-color: rgba(255, 255, 255, 0.04);
                    border: 1px solid rgba(255, 255, 255, 0.08);
                    border-radius: 4px;
                    color: rgba(255, 255, 255, 0.36);
                    padding: 0 16px;
                    font-size: 14px;
                    font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
                }
            """
        
        self.setStyleSheet(self._normal_style)

    def enterEvent(self, event):
        if self.isEnabled():
            self.setStyleSheet(self._hover_style)
        super().enterEvent(event)

    def leaveEvent(self, event):
        if self.isEnabled():
            self.setStyleSheet(self._normal_style)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.isEnabled():
            self._pressed = True
            self.setStyleSheet(self._pressed_style)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self._pressed:
            self._pressed = False
            if self.rect().contains(event.pos()):
                self.setStyleSheet(self._hover_style)
            else:
                self.setStyleSheet(self._normal_style)
        super().mouseReleaseEvent(event)

    def setEnabled(self, enabled):
        super().setEnabled(enabled)
        self.setStyleSheet(self._normal_style if enabled else self._disabled_style)