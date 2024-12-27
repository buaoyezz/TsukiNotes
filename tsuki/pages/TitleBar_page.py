from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QFrame, QMenu,QGraphicsOpacityEffect
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QRect, QSize, QSequentialAnimationGroup
from PyQt5.QtGui import QIcon, QPixmap
import os

class TitleBar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.initUI()
        self._setup_animations()
        
    def _setup_animations(self):
        # 菜单展开动画
        self.menu_animation = QPropertyAnimation(self, b"geometry")
        self.menu_animation.setDuration(300)
        self.menu_animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        # 按钮悬停动画
        self.hover_animations = {}
        
    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 标题栏部分
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(10, 5, 10, 5)
        title_layout.setSpacing(8)
        
        # 控制按钮容器
        control_layout = QHBoxLayout()
        control_layout.setSpacing(4)
        
        # Logo和标题放在最左边
        logo = QLabel()
        pixmap = QPixmap('./tsuki/assets/resources/GUI/logo.png')
        logo.setPixmap(pixmap.scaled(24, 24, Qt.KeepAspectRatio))
        control_layout.addWidget(logo)
        
        title = QLabel('TsukiNotes')
        title.setStyleSheet('''
            QLabel {
                font-family: Microsoft YaHei;
                font-size: 14px;
                font-weight: bold;
                color: #333333;
                border-radius: 20px;
            }
        ''')
        control_layout.addWidget(title)
        
        # 文件路径标签
        self.path_label = QLabel('未命名文件.txt')
        self.path_label.setStyleSheet('''
            QLabel {
                font-family: Microsoft YaHei;
                font-size: 12px;
                color: #666666;
                padding: 0 10px;
            }
        ''')
        control_layout.addWidget(self.path_label)
        
        # 菜单按钮
        menu_data = [
            ('文件', './tsuki/assets/resources/create_tab.png', [
                ('新建', './tsuki/assets/resources/create_tab.png', self.parent.newFile),
                ('打开', './tsuki/assets/resources/import_file.png', self.parent.openFile),
                ('保存', './tsuki/assets/resources/save_file.png', self.parent.saveFile),
                ('另存为', './tsuki/assets/resources/save_file.png', self.parent.saveAs),
                ('关闭', './tsuki/assets/resources/off_file.png', self.parent.closeFile),
                ('退出', './tsuki/assets/resources/exit_software.png', self.parent.close)
            ]),
            ('编辑', './tsuki/assets/resources/font_reset_change.png', [
                ('字体', './tsuki/assets/resources/font_reset_change.png', self.parent.changeFont),
                ('重置字体', './tsuki/assets/resources/font_reset_change.png', self.parent.resetFont),
                ('字体大小', './tsuki/assets/resources/font_size_reset_tab.png', self.parent.set_font_size)
            ]),
            ('更新', './tsuki/assets/resources/update_cloud.png', [
                ('检查更新', './tsuki/assets/resources/update_cloud.png', self.parent.checkForUpdates),
                ('手动更新', './tsuki/assets/resources/update_cloud.png', self.parent.update2),
                ('当前版本', './tsuki/assets/resources/custom_server.png', self.parent.versionnow),
                ('更新日志', './tsuki/assets/resources/update_cloud.png', self.parent.online_updateMessage)
            ]),
            ('关于', './tsuki/assets/resources/about.png', [
                ('关于', './tsuki/assets/resources/about.png', self.parent.aboutMessage),
                ('详细信息', './tsuki/assets/resources/about.png', self.parent.aboutDetails)
            ])
        ]
        
        # 添加菜单按钮
        for menu_text, icon_path, menu_items in menu_data:
            def create_menu_callback(items=menu_items):
                return lambda: self.showMenu(items)
            menu_btn = self._create_button(menu_text, icon_path, create_menu_callback())
            control_layout.addWidget(menu_btn)
            
        control_layout.addStretch()
        
        # 添加设置和运行按钮
        for btn_text, icon_path, slot in [
            ('设置', './tsuki/assets/resources/settings.png', self.parent.openSettingsWindow),
            ('运行', './tsuki/assets/resources/start.png', self.parent.runcode)
        ]:
            action_btn = self._create_button(btn_text, icon_path, slot)
            control_layout.addWidget(action_btn)
            
        # 添加分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setStyleSheet('''
            QFrame {
                color: #e0e0e0;
                border: none;
                background: #e0e0e0;
                width: 1px;
                margin: 4px 2px;
                height: 16px;
            }
        ''')
        control_layout.addWidget(separator)
        
        # 窗口控制按钮
        window_controls = QHBoxLayout()
        window_controls.setSpacing(0)
        
        for icon_name, tip, slot in [
            ('mini.png', '最小化', self.parent.showMinimized),
            ('max3.png', '最大化', self.toggleMaximize),
            ('close.png', '关闭', self.parent.close)
        ]:
            btn = QPushButton()
            btn.setFixedSize(46, 32)  # 增大按钮尺寸
            btn.setIcon(QIcon(f'./tsuki/assets/resources/{icon_name}'))
            btn.setToolTip(tip)
            btn.clicked.connect(slot)
            btn.setStyleSheet('''
                QPushButton {
                    border: none;
                    background: transparent;
                }
                QPushButton:hover {
                    background: rgba(0, 0, 0, 0.05);
                }
                QPushButton:pressed {
                    background: rgba(0, 0, 0, 0.1);
                }
                QPushButton[toolTip="关闭"]:hover {
                    background: #ff4081;
                }
            ''')
            window_controls.addWidget(btn)
        
        # 组装布局
        title_layout.addLayout(control_layout)
        title_layout.addLayout(window_controls)
        
        main_layout.addLayout(title_layout)
        
        self.setStyleSheet('''
            TitleBar {
                background: rgba(245, 245, 245, 0.95);  /* 半透明背景 */
                border: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
        ''')
        
    def _create_button(self, text, icon_path, slot):
        btn = QPushButton()
        
        # 分别设置图标和文本
        if icon_path:
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(16, 16))  # 设置图标大小
        
        if text:
            btn.setText(text)
        
        # 为每个按钮创建独立的动画对象
        scale_anim = QPropertyAnimation(btn, b"geometry")
        scale_anim.setDuration(300)
        scale_anim.setEasingCurve(QEasingCurve.InOutQuad)
        
        # 将动画对象保存到按钮的属性中
        btn.scale_anim = scale_anim
        
        normal_style = '''
            QPushButton {
                border: none;
                background: transparent;
                padding: 8px 12px;
                font-family: Microsoft YaHei;
                font-size: 13px;
                color: #333333;
                text-align: left;  /* 文本左对齐 */
            }
        '''
        
        hover_style = '''
            QPushButton {
                border: none;
                background: rgba(0, 0, 0, 0.05);
                padding: 8px 12px;
                font-family: Microsoft YaHei;
                font-size: 13px;
                color: #333333;
                border-radius: 4px;
                text-align: left;  /* 文本左对齐 */
            }
        '''
        
        btn.setStyleSheet(normal_style)
        
        def enterEvent(e):
            orig_geo = btn.geometry()
            scaled_geo = QRect(
                int(orig_geo.x() - orig_geo.width() * 0.005),
                int(orig_geo.y() - orig_geo.height() * 0.005),
                int(orig_geo.width() * 1.01),
                int(orig_geo.height() * 1.01)
            )
            btn.scale_anim.setStartValue(orig_geo)
            btn.scale_anim.setEndValue(scaled_geo)
            btn.scale_anim.start()
            btn.setStyleSheet(hover_style)
            
        def leaveEvent(e):
            orig_geo = btn.geometry()
            normal_geo = QRect(
                int(orig_geo.x() + orig_geo.width() * 0.005),
                int(orig_geo.y() + orig_geo.height() * 0.005),
                int(orig_geo.width() / 1.01),
                int(orig_geo.height() / 1.01)
            )
            btn.scale_anim.setStartValue(orig_geo)
            btn.scale_anim.setEndValue(normal_geo)
            btn.scale_anim.start()
            btn.setStyleSheet(normal_style)
        
        btn.enterEvent = enterEvent
        btn.leaveEvent = leaveEvent
        btn.clicked.connect(slot)
        
        return btn

    def _start_hover_animation(self, widget, target_style):
        if widget not in self.hover_animations:
            self.hover_animations[widget] = QPropertyAnimation(widget, b"styleSheet")
            self.hover_animations[widget].setDuration(200)
        
        anim = self.hover_animations[widget]
        anim.setStartValue(widget.styleSheet())
        anim.setEndValue(target_style)
        anim.start()

    def showMenu(self, menu_items):
        menu = QMenu(self)
        menu.setStyleSheet('''
            QMenu {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 4px;
            }
            QMenu::item {
                padding: 6px 32px 6px 32px;
                font-family: Microsoft YaHei;
                font-size: 12px;
                color: #333333;
            }
            QMenu::item:selected {
                background-color: rgba(0, 0, 0, 0.05);
                border-radius: 2px;
            }
        ''')
        
        for text, icon_path, slot in menu_items:
            action = menu.addAction(QIcon(icon_path), text)
            action.triggered.connect(slot)
            
        button = self.sender()
        if button:
            menu.exec_(self.mapToGlobal(button.pos() + QPoint(0, button.height())))
            
        # 添加菜单展开动画
        menu.aboutToShow.connect(lambda: self._animate_menu(menu))
        
    def _animate_menu(self, menu):
        start_geo = menu.geometry()
        end_geo = QRect(start_geo.x(), start_geo.y(), 
                       start_geo.width(), start_geo.height())
        
        # 设置起始位置(折叠状态)
        menu.setGeometry(QRect(start_geo.x(), start_geo.y(), 
                             start_geo.width(), 0))
        
        # 创建果冻弹动画组
        anim_group = QSequentialAnimationGroup()
        
        # 主展开动画
        expand_anim = QPropertyAnimation(menu, b"geometry")
        expand_anim.setDuration(200)
        expand_anim.setStartValue(menu.geometry())
        expand_anim.setEndValue(end_geo)
        expand_anim.setEasingCurve(QEasingCurve.OutBack)  # 使用 OutBack 曲线实现果冻效果
        
        # 添加弹性效果
        bounce_anim = QPropertyAnimation(menu, b"geometry")
        bounce_anim.setDuration(100)
        bounce_anim.setStartValue(end_geo)
        bounce_anim.setEndValue(QRect(end_geo.x(), end_geo.y(), 
                                     int(end_geo.width() * 0.98), end_geo.height()))
        bounce_anim.setEasingCurve(QEasingCurve.InOutQuad)
        
        # 恢复动画
        restore_anim = QPropertyAnimation(menu, b"geometry")
        restore_anim.setDuration(50)
        restore_anim.setStartValue(QRect(end_geo.x(), end_geo.y(), 
                                       int(end_geo.width() * 0.98), end_geo.height()))
        restore_anim.setEndValue(end_geo)
        restore_anim.setEasingCurve(QEasingCurve.OutQuad)
        
        # 将动画添加到动画组
        anim_group.addAnimation(expand_anim)
        anim_group.addAnimation(bounce_anim)
        anim_group.addAnimation(restore_anim)
        
        # 启动动画组
        anim_group.start()
        
    def toggleMaximize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()
            
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.parent.frameGeometry().topLeft()
            event.accept()
            
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.parent.move(event.globalPos() - self.dragPosition) 
    
    def updatePath(self, path):
        """优化显示文件路径,提供更好的视觉体验"""
        if not path:
            self.path_label.setText('未命名文件.txt')
            return
                
        # ���取文件名
        file_name = os.path.basename(path)
        
        # 获取绝对路径用于工具提示
        abs_path = os.path.abspath(path)
        
        # 设置工具提示显示完整路径
        self.path_label.setToolTip(abs_path)
        
        # 只显示文件名
        self.path_label.setText(file_name)
        
        # 设置右键菜单
        self.path_label.setContextMenuPolicy(Qt.CustomContextMenu)
        self.path_label.customContextMenuRequested.connect(lambda pos: self.showPathMenu(pos, abs_path))
        
        # 更新样式
        self.path_label.setStyleSheet('''
            QLabel {
                font-family: Microsoft YaHei;
                font-size: 12px;
                color: #666666;
                padding: 2px 12px;
                margin-left: 6px;
                background: transparent;
                border-radius: 4px;
            }
            QLabel:hover {
                color: #333333;
                background: rgba(0,0,0,0.05);
            }
        ''')
        
    def showPathMenu(self, pos, path):
        """显示路径标签的右键菜单"""
        menu = QMenu(self)
        menu.setStyleSheet('''
            QMenu {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 4px;
            }
            QMenu::item {
                padding: 6px 32px 6px 32px;
                font-family: Microsoft YaHei;
                font-size: 12px;
                color: #333333;
            }
            QMenu::item:selected {
                background-color: rgba(0, 0, 0, 0.05);
                border-radius: 2px;
            }
        ''')
        
        # 添加打开文件路径选项
        open_path_action = menu.addAction("打开文件路径")
        open_path_action.triggered.connect(lambda: os.startfile(os.path.dirname(path)))
        
        # 添加关闭文件选项
        close_file_action = menu.addAction("关闭文件")
        close_file_action.triggered.connect(self.parent.closeFile)
        
        menu.exec_(self.path_label.mapToGlobal(pos))