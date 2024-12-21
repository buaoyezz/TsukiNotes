from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, 
                            QPushButton, QLabel, QScrollArea)
from PyQt5.QtCore import (QSize, Qt, QTimer, QPropertyAnimation, 
                         QEasingCurve, QPoint, QRect)
from PyQt5.QtGui import QIcon
from assets.utils.style_loader import load_stylesheet

def setup_main_layout():
    # Main Layout
    main_layout = QVBoxLayout()
    main_layout.setContentsMargins(0, 0, 0, 0)
    main_layout.setSpacing(0)
    return main_layout

def setup_content_layout():
    # Content Layout
    content_layout = QHBoxLayout()
    content_layout.setContentsMargins(0, 0, 0, 0)
    content_layout.setSpacing(0)
    
    # 创建滚动区域
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    
    # 设置滚动区域样式
    scroll_area.setStyleSheet("""
        QScrollArea {
            border: none;
            background-color: transparent;
        }
        QScrollBar:vertical {
            border: none;
            background: #f0f0f0;
            width: 8px;
            margin: 0px 0px 0px 0px;
        }
        QScrollBar::handle:vertical {
            background: #c0c0c0;
            min-height: 20px;
            border-radius: 4px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
    """)
    
    return content_layout, scroll_area

def setup_sidebar(page_manager):
    # 创建侧边栏容器
    sidebar_widget = QWidget()
    sidebar_widget.setFixedWidth(50)
    sidebar = QVBoxLayout(sidebar_widget)
    sidebar.setSpacing(5)
    sidebar.setContentsMargins(5, 10, 5, 10)
    sidebar_widget.setStyleSheet(load_stylesheet('sidebar.qss'))

    # 创建动画对象
    animation = QPropertyAnimation(sidebar_widget, b"minimumWidth")
    animation.setDuration(150)  # 动画持续延迟
    animation.setEasingCurve(QEasingCurve.InOutQuad)  # 缓动曲线

    expand_timer = QTimer()
    expand_timer.setSingleShot(True)  # 单次触发
    collapse_timer = QTimer()
    collapse_timer.setSingleShot(True)

    # 创建按钮
    buttons = []
    normal_buttons = page_manager.get_buttons()[:-1]  # 除了最后一个设置按钮
    for text, page_name, icon_path in normal_buttons:
        btn = QPushButton()
        btn.setIcon(QIcon(icon_path))
        btn.setIconSize(QSize(24, 24))
        btn.setText(text)
        btn.setToolTip(text)
        btn.setFixedHeight(40)
        btn.setStyleSheet("QPushButton { text-align: left; padding-left: 20px; *font-family: 'Microsoft YaHei'; }")
        btn.clicked.connect(lambda checked, p=page_name: 
            page_manager.slide_to_page(p))
        sidebar.addWidget(btn)
        buttons.append(btn)
    
    sidebar.addStretch()  # 添加弹性空间
    
    # 创建设置按钮（最后一个按钮）
    settings_button = page_manager.get_buttons()[-1]  # 获取设置按钮信息
    btn = QPushButton()
    btn.setIcon(QIcon(settings_button[2]))
    btn.setIconSize(QSize(24, 24))
    btn.setText(settings_button[0])
    btn.setToolTip(settings_button[0])
    btn.setFixedHeight(40)
    btn.setStyleSheet("QPushButton { text-align: left; padding-left: 20px; *font-family: 'Microsoft YaHei'; }")
    btn.clicked.connect(lambda checked, p=settings_button[1]: 
        page_manager.slide_to_page(p))
    sidebar.addWidget(btn)
    buttons.append(btn)
    
    # 展开动画
    def start_expand():
        if not animation.state() == QPropertyAnimation.Running:
            animation.setStartValue(sidebar_widget.width())
            animation.setEndValue(200)
            animation.start()
            for btn in buttons:
                btn.setStyleSheet(load_stylesheet('sidebar_expanded.qss'))

    # 收缩动画
    def start_collapse():
        if not animation.state() == QPropertyAnimation.Running:
            animation.setStartValue(sidebar_widget.width())
            animation.setEndValue(50)
            animation.start()
            for btn in buttons:
                btn.setStyleSheet(load_stylesheet('sidebar.qss'))

    # 鼠标进入事件
    def enterEvent(event):
        collapse_timer.stop()  # 停止收缩计时器
        expand_timer.stop()    # 停止之前的展开计时器（如果有的话）
        expand_timer.start(150)  # 150ms后开始展开
        
    # 鼠标离开事件
    def leaveEvent(event):
        expand_timer.stop()    # 停止展开计时器
        collapse_timer.stop()  # 停止之前的收缩计时器（如果有的话）
        collapse_timer.start(200)  # 200ms后开始收缩

    # 连接定时器信号到动画槽
    expand_timer.timeout.connect(start_expand)
    collapse_timer.timeout.connect(start_collapse)

    # 设置事件处理器
    sidebar_widget.enterEvent = enterEvent
    sidebar_widget.leaveEvent = leaveEvent

    return sidebar_widget