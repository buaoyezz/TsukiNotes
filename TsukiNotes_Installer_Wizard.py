#==================================
# TsukiNotes Install Wizard Ver 2.0.0 Stable
# New Design, New Experience!
# 2025/01/23 CHINA TIME
# GNU General Public License v3.0
# FIX More Bug | Add More Feature | AND NEW DESIGN
#==================================

from itertools import zip_longest
import sys
import os
import shutil
import winreg
import ctypes
import requests
import zipfile
import argparse
import logging
import time
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import win32com.client
import concurrent.futures
import threading
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import psutil
import signal
import stat

# 检查管理员权限
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        try:
            if sys.argv[-1] != 'asadmin':
                script = os.path.abspath(sys.argv[0])
                params = ' '.join([script] + sys.argv[1:] + ['asadmin'])
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
                sys.exit()
        except Exception as e:
            print(f"请求管理员权限失败: {e}")
            sys.exit(1)

def check_version():
    try:
        api_url = 'https://api.github.com/repos/buaoyezz/TsukiNotes/releases'
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'TsukiNotes-Installer'  # 添加User-Agent避免API限制
        }
        
        # 添加超时重试机制
        for attempt in range(3):
            try:
                response = requests.get(api_url, headers=headers, timeout=10)
                response.raise_for_status()
                break
            except requests.RequestException:
                if attempt == 2:
                    raise
                time.sleep(1)
        
        releases = response.json()
        versions = []
        
        for release in releases:
            assets = release.get('assets', [])
            for asset in assets:
                name = asset.get('name', '')
                if name.endswith('.zip') and 'TsukiNotesVer' in name:
                    version_info = {
                        'file_name': name,
                        'download_url': asset.get('browser_download_url'),
                        'size': asset.get('size'),  # 获取文件大小
                        'version': '',
                        'attributes': [],
                        'is_hotfix': 'HotFix' in name
                    }
                    
                    parts = name.replace('.zip', '').split('_')
                    version = parts[0].replace('TsukiNotesVer', '')
                    version_info['version'] = version
                    
                    if len(parts) > 1:
                        version_info['attributes'] = parts[1:]
                    
                    versions.append(version_info)
        
        # 优先选择HotFix版本，如果没有则选择最新普通版本
        hotfix_versions = [v for v in versions if v['is_hotfix']]
        if hotfix_versions:
            return sorted(hotfix_versions, key=lambda x: x['version'], reverse=True)[0]
        else:
            return sorted(versions, key=lambda x: x['version'], reverse=True)[0]
            
    except Exception:
        return None

def get_current_version(install_path):
    version_file = os.path.join(install_path, "VERSION")
    try:
        if not os.path.exists(version_file):
            logging.warning(f"VERSION 文件不存在: {version_file}")
            return "未安装"
            
        with open(version_file, 'r', encoding='utf-8') as f:
            content = f.readlines()
            for line in content:
                if line.startswith("Version:"):
                    version = line.split(":")[1].strip()
                    return version
            
            logging.warning(f"VERSION 文件中未找到版本信息")
            return "未知版本"
                
    except FileNotFoundError:
        logging.error(f"版本文件未找到: {version_file}")
        return "未安装"
    except Exception as e:
        logging.error(f"读取版本文件时出错: {e}")
        return "读取错误"

def compare_versions(current_version, latest_version):
    if not current_version or not latest_version:
        return True
    current_parts = [int(x) for x in current_version.split('.')]
    latest_parts = [int(x) for x in latest_version.split('.')]
    
    for c, l in zip_longest(current_parts, latest_parts, fillvalue=0):
        if l > c:
            return True
        elif l < c:
            return False
    return False

class ModernButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(40)
        self.setCursor(Qt.PointingHandCursor)
        
        # 添加按钮点击动画效果
        self._animation = QPropertyAnimation(self, b"geometry")
        self._animation.setDuration(100)
        self.setFocusPolicy(Qt.NoFocus) # 取消焦点
        
        # 添加阴影效果
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(3)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, 25))
        self.setGraphicsEffect(shadow)
        
        self.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #60CDFF;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                text-align: center;
            }
            QPushButton:hover {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
                    stop:0 #f0f0f0, stop:1 #ffffff);
                color: #99E5FF;
            }
            QPushButton:pressed {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
                    stop:0 #e0e0e0, stop:1 #f5f5f5);
                color: #4BA0FF;
            }
        """)

    def mousePressEvent(self, event):
        # 按下动画
        geo = self.geometry()
        self._animation.setStartValue(geo)
        self._animation.setEndValue(QRect(geo.x()+2, geo.y()+2, geo.width()-4, geo.height()-4))
        self._animation.start()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        # 释放动画
        geo = self.geometry()
        self._animation.setStartValue(geo)
        self._animation.setEndValue(QRect(geo.x()-2, geo.y()-2, geo.width()+4, geo.height()+4))
        self._animation.start()
        super().mouseReleaseEvent(event)

class ModernProgressBar(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: rgba(240, 240, 240, 0.8);
                border-radius: 10px;
                text-align: center;
                height: 20px;
                margin: 0px 5px;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
                    stop:0 #60CDFF, stop:0.5 #99E5FF, stop:1 #60CDFF);
                border-radius: 10px;
            }
        """)
        # 移除模糊效果
        # blur_effect = QGraphicsBlurEffect()
        # blur_effect.setBlurRadius(10) 
        # self.setGraphicsEffect(blur_effect)

class MirrorSelectPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("下载设置")
        self.setSubTitle("请选择下载方式")
        
        layout = QVBoxLayout()
        
        # 创建选择框容器
        select_container = QFrame()
        select_container.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 15px;
                padding: 20px;
                border: 1px solid rgba(96, 205, 255, 0.3);
            }
        """)
        
        select_layout = QVBoxLayout()
        
        # 添加单选按钮组
        self.mirror_group = QButtonGroup()
        
        self.direct_radio = QRadioButton("直接下载")
        self.direct_radio.setChecked(True)
        self.mirror_radio = QRadioButton("使用加速镜像")
        
        self.mirror_group.addButton(self.direct_radio)
        self.mirror_group.addButton(self.mirror_radio)
        
        # 添加说明标签
        info_label = QLabel(
            "加速镜像说明:\n"
            "• 是采用了第三方的镜像源,非作者本人搭建\n"
            "• 此镜像支持多线程,但是不代表本软件支持多线程\n"
            "• 此镜像建议连不上Github的用户使用,若您可以正常访问Github,并且速度正常,请使用直接下载\n"
            "• ✨镜像源: github.hanxuan.filegear-sg.me"
        )
        info_label.setStyleSheet("""
            QLabel {
                color: #666666;
                padding: 10px;
                background-color: rgba(96, 205, 255, 0.1);
                border-radius: 8px;
            }
        """)
        info_label.setWordWrap(True)
        
        select_layout.addWidget(self.direct_radio)
        select_layout.addWidget(self.mirror_radio)
        select_layout.addSpacing(20)
        select_layout.addWidget(info_label)
        
        select_container.setLayout(select_layout)
        layout.addWidget(select_container)
        
        # 添加提示
        tip_label = QLabel("提示: 如果直接下载速度较慢，建议使用加速镜像 | 本软件采用镜像源: github.hanxuan.filegear-sg.me")
        tip_label.setStyleSheet("color: #888888; font-style: italic;")
        layout.addWidget(tip_label)
        
        self.setLayout(layout)
        
    def nextId(self):
        return self.wizard().pageIds()[self.wizard().pageIds().index(self.wizard().currentId()) + 1]

class ModernMessageBox(QDialog):
    def __init__(self, icon, title, text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # 主布局
        layout = QVBoxLayout(self)
        
        # 内容容器
        container = QFrame(self)
        container.setObjectName("container")
        container_layout = QVBoxLayout(container)
        
        # 标题栏
        title_bar = QFrame()
        title_bar_layout = QHBoxLayout(title_bar)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        
        close_btn = QPushButton("×")
        close_btn.setFixedSize(30, 30)
        close_btn.clicked.connect(self.reject)
        close_btn.setStyleSheet("""
            QPushButton {
                border: none;
                color: #666;
                font-size: 20px;
            }
            QPushButton:hover {
                background: #ffebee;
                color: #f44336;
                border-radius: 15px;
            }
        """)
        
        title_bar_layout.addWidget(title_label)
        title_bar_layout.addWidget(close_btn)
        
        # 内容区域
        content = QFrame()
        content_layout = QHBoxLayout(content)
        
        # 图标
        icon_label = QLabel()
        icon_pixmap = self.get_icon_pixmap(icon)
        icon_label.setPixmap(icon_pixmap)
        icon_label.setFixedSize(48, 48)
        
        # 文本
        text_label = QLabel(text)
        text_label.setWordWrap(True)
        text_label.setStyleSheet("color: #333; font-size: 14px;")
        
        content_layout.addWidget(icon_label)
        content_layout.addWidget(text_label, 1)
        
        # 按钮区域
        button_box = QDialogButtonBox()
        ok_btn = button_box.addButton(QDialogButtonBox.Ok)
        ok_btn.setText("确定")
        ok_btn.setStyleSheet("""
            QPushButton {
                min-width: 80px;
                min-height: 32px;
                background: #60CDFF;
                border: none;
                border-radius: 6px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #99E5FF;
            }
            QPushButton:pressed {
                background: #4BA0FF;
            }
        """)
        button_box.accepted.connect(self.accept)
        
        # 组装布局
        container_layout.addWidget(title_bar)
        container_layout.addWidget(content)
        container_layout.addWidget(button_box)
        
        layout.addWidget(container)
        
        # 设置样式
        self.setStyleSheet("""
            QDialog {
                background: transparent;
            }
            #container {
                background: white;
                border-radius: 12px;
                border: 1px solid rgba(0, 0, 0, 0.1);
            }
        """)
        
        # 添加阴影效果
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 50))
        shadow.setOffset(0, 4)
        container.setGraphicsEffect(shadow)
        
        # 添加动画效果
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(200)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()
        
        # 弹出动画
        self.pop_animation = QPropertyAnimation(container, b"geometry")
        self.pop_animation.setDuration(300)
        self.pop_animation.setEasingCurve(QEasingCurve.OutBack)
        
        start_rect = container.geometry()
        start_rect.moveCenter(self.geometry().center())
        start_rect.setHeight(start_rect.height() * 0.8)
        
        end_rect = container.geometry()
        
        self.pop_animation.setStartValue(start_rect)
        self.pop_animation.setEndValue(end_rect)
        self.pop_animation.start()

    def get_icon_pixmap(self, icon_type):
        if icon_type == QMessageBox.Information:
            color = QColor("#2196F3")
            icon_path = "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"
        elif icon_type == QMessageBox.Warning:
            color = QColor("#FFC107") 
            icon_path = "M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"
        elif icon_type == QMessageBox.Critical:
            color = QColor("#F44336")
            icon_path = "M12 2C6.47 2 2 6.47 2 12s4.47 10 10 10 10-4.47 10-10S17.53 2 12 2zm5 13.59L15.59 17 12 13.41 8.41 17 7 15.59 10.59 12 7 8.41 8.41 7 12 10.59 15.59 7 17 8.41 13.41 12 17 15.59z"
        else:
            color = QColor("#4CAF50")
            icon_path = "M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"
            
        # 创建SVG图标
        path = QPainterPath()
        path.addText(QPointF(0, 40), QFont("Material Icons", 40), icon_path)
        
        pixmap = QPixmap(48, 48)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(color)
        painter.drawPath(path)
        painter.end()
        
        return pixmap

    def showEvent(self, event):
        super().showEvent(event)
        # 居中显示
        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

def show_message_box(parent, icon, title, text):
    dialog = ModernMessageBox(icon, title, text, parent)
    return dialog.exec_()

class InstallerWizard(QWizard):
    def __init__(self, silent_mode=False):
        super().__init__()
        self.silent_mode = silent_mode
        self.setWindowTitle("TsukiNotes Install Wizard | Version 2.0.0 Stable | ✨New Design✨")# 软件标题
        self.setWindowIcon(QIcon("icon.ico"))# 软件图标
        self.resize(1017, 536)
        
        # 初始化按钮动画字典
        self.button_animations = {}
        for button_id in [QWizard.BackButton, QWizard.NextButton, QWizard.FinishButton, QWizard.CancelButton]:
            animation = QPropertyAnimation(self)
            animation.setDuration(100)
            animation.setPropertyName(b"geometry")
            self.button_animations[button_id] = animation
        
        # 设置窗口居中显示
        self.center_window()
        
        # 初始化安装路径
        default_path = os.path.join(os.path.expanduser("~"), "Desktop", "TsukiNotes")
        self.install_path = default_path
        
        # 自动获取最新版本
        self.selected_version = check_version()
        
        # 添加页面
        self.mirror_page = MirrorSelectPage()
        self.addPage(WelcomePage())
        self.addPage(DeclarationPage())  # 添加声明页
        self.addPage(InstallLocationPage())
        self.addPage(self.mirror_page)
        self.addPage(InstallProgressPage())
        
        # 设置窗口样式
        self.setWizardStyle(QWizard.ModernStyle)
        self.setOption(QWizard.HaveHelpButton, False)
        self.setOption(QWizard.HaveCustomButton1, False)
        
        # 自定义按钮文本
        self.setButtonText(QWizard.FinishButton, "完成安装")
        self.setButtonText(QWizard.CancelButton, "取消")
        self.setButtonText(QWizard.NextButton, "下一步")
        self.setButtonText(QWizard.BackButton, "上一步")
        
        # 设置全局样式
        self.setStyleSheet("""
            QWizard {
                background-color: #f0f4f8;
            }
            QWizardPage {
                background-color: #ffffff;
                border-radius: 15px;
                margin: 15px;
                padding: 25px;
                border: 1px solid rgba(255, 255, 255, 0.8);
            }
            QLabel {
                color: #333333;
                font-size: 14px;
                font-family: "Microsoft YaHei UI", "Segoe UI";
            }
            QLineEdit, QComboBox {
                border: 2px solid #e0e0e0;
                padding: 8px;
                border-radius: 8px;
                background-color: #ffffff;
                min-height: 30px;
                font-family: "Microsoft YaHei UI", "Segoe UI";
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #60CDFF;
            }
            /* 滚动条样式 */
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 10px;
                margin: 0px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                min-height: 30px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a0a0a0;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            /* 水平滚动条 */
            QScrollBar:horizontal {
                border: none;
                background: #f0f0f0;
                height: 10px;
                margin: 0px;
                border-radius: 5px;
            }
            QScrollBar::handle:horizontal {
                background: #c0c0c0;
                min-width: 30px;
                border-radius: 5px;
            }
            QScrollBar::handle:horizontal:hover {
                background: #a0a0a0;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;
            }
            /* 其他样式保持不变 */
            QPushButton {
                min-height: 35px;
                border-radius: 6px;
                padding: 0 25px;  /* 增加按钮内边距 */
                background-color: #60CDFF;
                color: white;
                border: none;
                font-weight: bold;  /* 加粗按钮文字 */
                font-family: "Microsoft YaHei UI", "Segoe UI";
            }
            QPushButton:hover {
                background-color: #99E5FF;
            }
            QPushButton:pressed {
                background-color: #4BA0FF;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
            QWizard QWidget {
                font-family: "Microsoft YaHei UI", "Segoe UI";
            }
        """)

    def center_window(self):
        """将窗口居中显示"""
        screen = QApplication.desktop().screenGeometry()
        window = self.geometry()
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        self.move(x, y)

    def auto_install(self):
        if self.silent_mode:
            self.next()

    def closeEvent(self, event):
        if hasattr(self, 'current_thread'):
            self.current_thread.quit()
            self.current_thread.wait()
        event.accept()

    def nextId(self):
        # no animation
        return super().nextId()

class WelcomePage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("TsukiNotes Install Wizard | Version 2.0.0 Stable | ✨")
        
        # qhboxlayout
        layout = QHBoxLayout()
        layout.setSpacing(20)
        
        # left container
        left_container = QFrame()
        left_container.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.7);
                border-radius: 20px;
                padding: 20px;
            }
        """)
        left_layout = QVBoxLayout()
        left_layout.setSpacing(30)  # added spacing
        
        # TsukiNotes
        main_title = QLabel("TsukiNotes")
        main_title.setStyleSheet("""
            QLabel {
                font-size: 48px;
                font-weight: bold;
                color: #333333;
                font-family: "Microsoft YaHei UI", "Segoe UI";
                margin-bottom: 20px;  /* 增加下边距 */
            }
        """)
        main_title.setAlignment(Qt.AlignCenter)
        
        # 副标题 Install Wizard
        sub_title = QLabel("Install Wizard")
        sub_title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                color: #666666;
                font-family: "Segoe UI", "Microsoft YaHei UI";
            }
        """)
        sub_title.setAlignment(Qt.AlignCenter)
        
        # 一言显示
        self.hitokoto_label = QLabel("正在获取一言...")
        self.hitokoto_label.setStyleSheet("""
            QLabel {
                color: #888888;
                font-size: 13px;
                font-style: italic;
                padding: 10px;
                background-color: rgba(255, 255, 255, 0.5);
                border-radius: 8px;
                margin-top: 20px;  /* 增加上边距 */
            }
        """)
        self.hitokoto_label.setWordWrap(True)  # 允许文字换行
        self.hitokoto_label.setAlignment(Qt.AlignCenter)
        
        left_layout.addStretch(1)
        left_layout.addWidget(main_title)
        left_layout.addWidget(sub_title)
        left_layout.addWidget(self.hitokoto_label)
        left_layout.addStretch(1)
        left_container.setLayout(left_layout)
        
        # 右侧信息面板
        info_panel = QFrame()
        info_panel.setStyleSheet("""
            QFrame {
                background-color: rgba(96, 205, 255, 0.1);
                border-radius: 15px;
                padding: 20px;
            }
            QLabel {
                color: #444444;
                font-size: 15px;
                line-height: 1.8;  /* 增加行高 */
            }
        """)
        
        info_layout = QVBoxLayout()
        info_layout.setSpacing(20)  # 增加垂直间距
        
        version_label = QLabel("✨TsukiNotes Install Wizard Ver 2.0.0 Stable✨")
        version_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #333;
            margin-bottom: 15px;  /* 增加下边距 */
        """)
        version_label.setAlignment(Qt.AlignCenter)
        
        desc_label = QLabel(
            "欢迎使用 TsukiNotes Install Wizard 2.0.0！\n\n"
            "• 本向导将帮助您安装最新版本的 TsukiNotes\n"
            "• 安装过程中请不要关闭本程序\n"
            "• 点击 [下一步] 开始安装\n"
            "• 点击 [取消] 退出安装"
        )
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignLeft)
        
        info_layout.addWidget(version_label)
        info_layout.addWidget(desc_label)
        info_panel.setLayout(info_layout)
        
        # 添加到主布局
        layout.addWidget(left_container, 1)
        layout.addWidget(info_panel, 1)
        
        self.setLayout(layout)
        
        # 获取一言
        self.get_hitokoto()
        
    def get_hitokoto(self):
        try:
            thread = threading.Thread(target=self._fetch_hitokoto)
            thread.daemon = True
            thread.start()
        except Exception as e:
            self.hitokoto_label.setText("「一言获取失败...」")
            
    def _fetch_hitokoto(self):
        try:
            response = requests.get("https://v1.hitokoto.cn/", timeout=5)
            if response.status_code == 200:
                data = response.json()
                hitokoto = data.get("hitokoto", "")
                from_who = data.get("from_who", "")
                from_where = data.get("from", "")
                
                # 构建显示文本
                text = f"「{hitokoto}」"
                if from_who:
                    text += f"\n—— {from_who}"
                elif from_where:
                    text += f"\n—— {from_where}"
                    
                # 使用信号更新UI
                self.hitokoto_label.setText(text)
            else:
                self.hitokoto_label.setText("「一言获取失败...」")
        except Exception as e:
            self.hitokoto_label.setText("「一言获取失败...」")

class DeclarationPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("| 安装声明")
        
        # 使用水平布局
        layout = QHBoxLayout()
        layout.setSpacing(20)
        
        # 左侧标题区域
        left_container = QFrame()
        left_container.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.7);
                border-radius: 20px;
                padding: 20px;
            }
        """)
        left_layout = QVBoxLayout()
        
        # 主标题
        main_title = QLabel("Declaration")
        main_title.setStyleSheet("""
            QLabel {
                font-size: 42px;  /* 调小字号 */
                font-weight: bold;
                color: #333333;
                font-family: "Microsoft YaHei UI", "Segoe UI";
            }
        """)
        main_title.setAlignment(Qt.AlignCenter)
        
        # 副标题
        sub_title = QLabel("Installation Terms")
        sub_title.setStyleSheet("""
            QLabel {
                font-size: 20px;  /* 调小字号 */
                color: #666666;
                font-family: "Segoe UI", "Microsoft YaHei UI";
                margin-top: -5px;  /* 减小间距 */
            }
        """)
        sub_title.setAlignment(Qt.AlignCenter)
        
        left_layout.addStretch(1)  # 上方添加弹性空间
        left_layout.addWidget(main_title)
        left_layout.addWidget(sub_title)
        left_layout.addStretch(1)  # 下方添加弹性空间
        left_container.setLayout(left_layout)
        
        # 右侧内容区域
        right_container = QFrame()
        right_container.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 15px;
                padding: 25px;  /* 增加内边距 */
                border: 1px solid rgba(96, 205, 255, 0.3);
            }
        """)
        right_layout = QVBoxLayout()
        
        # 声明文本框
        declaration_text = QTextEdit()
        declaration_text.setReadOnly(True)
        declaration_text.setStyleSheet("""
            QTextEdit {
                background-color: rgba(248, 249, 250, 0.9);
                border: none;
                border-radius: 12px;
                padding: 20px;  /* 增加内边距 */
                font-size: 14px;  /* 调整字号 */
                line-height: 1.8;  /* 增加行高 */
                color: #333333;
            }
        """)
        
        content = """【安装声明】

在安装和使用本软件之前，请仔细阅读以下声明：

1. 软件说明
   • 本程序为TsukiNotes的更新安装程序
   • 用于更新或安装TsukiNotes的最新版本
   • 安装过程会替换原有程序文件
   • 本软件采用镜像源: github.hanxuan.filegear-sg.me
   • 全新2.0.0安装向导，新设计，新体验！

2. 安装提示
   • 安装前确保选择目录未被占用否则本软件会一脚把那个软件踹飞
   • 安装前请核对安装路径是否正确
   • 安装过程中请勿返回上一步，或者直接退出程序，这会使软件无法正常关闭

3. 文件关联
   • 安装程序会自动关联.txt、.md等文件格式
   • 将在桌面创建新的快捷方式
   • 一些注册表设置如关联需要重启系统生效
   
4. 注意事项
   • 请确保有足够的磁盘空间
   • 需要管理员权限完成安装
   • 如遇问题请查看日志文件
   
5. 问题说明
   • 有问题建议等欢迎Github提交PR和Issue
   • 如遇链接超时TimeOut，请使用加速镜像，或稍后再试
   • 软件会自动选择下载链接
   • 详细问题请查看日志文件：Tsukinotes_Update.log"""
        
        declaration_text.setText(content)
        
        # 底部容器
        bottom_container = QFrame()
        bottom_container.setStyleSheet("""
            QFrame {
                background-color: rgba(248, 249, 250, 0.9);
                border-radius: 10px;
                padding: 15px;
            }
        """)
        bottom_layout = QHBoxLayout()
        
        # 复选框
        self.agree_checkbox = QCheckBox("我已阅读并同意上述声明")
        self.agree_checkbox.setStyleSheet("""
            QCheckBox {
                color: #333333;
                font-size: 13px;
                padding: 5px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 2px solid #60CDFF;
            }
            QCheckBox::indicator:checked {
                background-color: #60CDFF;
                image: url(check.png);  /* 可以添加自定义勾选图标 */
            }
        """)
        self.agree_checkbox.stateChanged.connect(self.completeChanged)
        
        # 提示文本
        tip_label = QLabel("提示：请仔细阅读上述声明，确认后勾选同意继续安装")
        tip_label.setStyleSheet("""
            QLabel {
                color: #666666;
                font-size: 12px;
                font-style: italic;
            }
        """)
        
        bottom_layout.addWidget(self.agree_checkbox)
        bottom_layout.addStretch()
        bottom_layout.addWidget(tip_label)
        bottom_container.setLayout(bottom_layout)
        
        # 组装右侧布局
        right_layout.addWidget(declaration_text, 1)  # 添加拉伸因子
        right_layout.addSpacing(15)  # 增加间距
        right_layout.addWidget(bottom_container)
        right_container.setLayout(right_layout)
        
        # 设置左右比例为3:7
        layout.addWidget(left_container, 3)
        layout.addWidget(right_container, 7)
        
        self.setLayout(layout)

class InstallLocationPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("选择安装位置")
        
        # 使用水平布局
        layout = QHBoxLayout()
        layout.setSpacing(20)
        
        # 左侧标题区域
        left_container = QFrame()
        left_container.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.7);
                border-radius: 20px;
                padding: 20px;
            }
        """)
        left_layout = QVBoxLayout()
        
        # 主标题
        main_title = QLabel("Location")
        main_title.setStyleSheet("""
            QLabel {
                font-size: 48px;
                font-weight: bold;
                color: #333333;
                font-family: "Microsoft YaHei UI", "Segoe UI";
            }
        """)
        main_title.setAlignment(Qt.AlignCenter)
        
        # 副标题
        sub_title = QLabel("Choose Path")
        sub_title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                color: #666666;
                font-family: "Segoe UI", "Microsoft YaHei UI";
                margin-top: -10px;
            }
        """)
        sub_title.setAlignment(Qt.AlignCenter)
        
        left_layout.addWidget(main_title)
        left_layout.addWidget(sub_title)
        left_container.setLayout(left_layout)
        
        # 右侧内容区域
        right_container = QFrame()
        right_container.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 15px;
                padding: 20px;
                border: 1px solid rgba(96, 205, 255, 0.3);
            }
        """)
        right_layout = QVBoxLayout()
        
        # 路径选择区域
        path_container = QFrame()
        path_container.setStyleSheet("""
            QFrame {
                background-color: rgba(248, 249, 250, 0.9);
                border-radius: 12px;
                padding: 15px;
            }
        """)
        path_layout = QHBoxLayout()
        
        self.path_edit = QLineEdit()
        self.path_edit.setReadOnly(True)
        self.path_edit.setText(os.path.join(os.path.expanduser("~"), "Desktop", "TsukiNotes"))
        self.path_edit.setMinimumWidth(400)
        
        self.browse_btn = ModernButton("浏览...", self)
        self.browse_btn.setFixedWidth(100)
        self.browse_btn.clicked.connect(self.browse_path)
        
        path_layout.addWidget(self.path_edit)
        path_layout.addWidget(self.browse_btn)
        path_container.setLayout(path_layout)
        
        # 空间信息显示
        self.space_info = QLabel()
        self.space_info.setStyleSheet("""
            QLabel {
                color: #666666;
                padding: 15px;
                background-color: rgba(96, 205, 255, 0.1);
                border-radius: 8px;
                font-size: 13px;
            }
        """)
        
        # 提示信息
        tip_label = QLabel("提示：建议安装在非系统盘，以获得更好的性能")
        tip_label.setStyleSheet("""
            QLabel {
                color: #888888;
                font-style: italic;
                font-size: 12px;
            }
        """)
        
        right_layout.addWidget(path_container)
        right_layout.addWidget(self.space_info)
        right_layout.addWidget(tip_label)
        right_layout.addStretch()
        right_container.setLayout(right_layout)
        
        # 添加到主布局
        layout.addWidget(left_container, 1)
        layout.addWidget(right_container, 2)
        
        self.setLayout(layout)
        self.update_space_info()
    
    def browse_path(self):
        base_path = QFileDialog.getExistingDirectory(self, "选择安装位置")
        if base_path:
            # 自动添加TsukiNotes子文件夹
            full_path = os.path.join(base_path, "TsukiNotes")
            self.path_edit.setText(full_path)
            self.update_space_info()
            self.wizard().install_path = full_path
    
    def update_space_info(self):
        try:
            path = os.path.dirname(self.path_edit.text())  # 获取父目录
            if os.path.exists(path):
                total, used, free = shutil.disk_usage(path)
                self.space_info.setText(f"可用空间: {free // (1024*1024*1024)} GB")
            else:
                self.space_info.setText("无法获取磁盘信息")
        except Exception:
            self.space_info.setText("无法获取磁盘信息")

class InstallProgressPage(QWizardPage):
    updateProgress = pyqtSignal(int, str)
    installationComplete = pyqtSignal(bool, str)
    logMessage = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setTitle("| Install Progress")
        self.setSubTitle("请等待安装完成...")
        
        layout = QVBoxLayout()
        
        # 进度条
        self.progress = ModernProgressBar()
        layout.addWidget(self.progress)
        
        # 状态面板
        self.status_panel = QFrame()
        self.status_panel.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 15px;
                padding: 20px;
                border: 1px solid rgba(96, 205, 255, 0.3);
            }
            QLabel {
                color: #444444;
                font-size: 13px;
                padding: 5px;
                background-color: rgba(96, 205, 255, 0.05);
                border-radius: 8px;
                font-family: "Microsoft YaHei UI", "Segoe UI";
            }
        """)
        status_layout = QGridLayout()
        
        # 修改标签文本为中文
        self.speed_label = QLabel("速度: N/A MB/s")
        self.thread_label = QLabel("线程: -")
        self.time_label = QLabel("剩余时间: --")
        self.size_label = QLabel("大小: -/- MB")
        self.file_label = QLabel("当前文件: --")
        self.status_label = QLabel("状态: 准备中...")
        
        status_layout.addWidget(self.speed_label, 0, 0)
        status_layout.addWidget(self.thread_label, 0, 1)
        status_layout.addWidget(self.time_label, 1, 0)
        status_layout.addWidget(self.size_label, 1, 1)
        status_layout.addWidget(self.file_label, 2, 0, 1, 2)
        status_layout.addWidget(self.status_label, 3, 0, 1, 2)
        
        self.status_panel.setLayout(status_layout)
        layout.addWidget(self.status_panel)
        
        # 日志显示
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: rgba(248, 249, 250, 0.9);
                border: 1px solid rgba(96, 205, 255, 0.3);
                border-radius: 15px;
                padding: 15px;
                font-family: "Microsoft YaHei UI", "Segoe UI";
                font-size: 12px;
                line-height: 1.4;
                color: #333333;
            }
        """)
        layout.addWidget(self.log_text)
        
        self.setLayout(layout)
        
        # 连接信号
        self.updateProgress.connect(self.update_progress)
        self.installationComplete.connect(self.handle_installation_complete)
        self.logMessage.connect(self.append_log)
        
        # 初始化安装完成标志
        self.installation_completed = False
        
    def initializePage(self):
        # 确保安装目录存在
        os.makedirs(self.wizard().install_path, exist_ok=True)
        
        # 禁用所有导航按钮
        if self.wizard():
            self.wizard().button(QWizard.FinishButton).setEnabled(False)
            self.wizard().button(QWizard.BackButton).setEnabled(False)

            self.wizard().button(QWizard.CancelButton).setEnabled(False)  # 也禁用取消按钮
            
        QTimer.singleShot(0, self.start_installation)
        
    def start_installation(self):
        self.current_thread = QThread()
        self.worker = InstallationWorker(
            self.wizard().install_path,
            self.wizard().silent_mode,
            self.wizard().selected_version,
            self.wizard().mirror_page.mirror_radio.isChecked()
        )
        
        self.worker.moveToThread(self.current_thread)
        self.current_thread.started.connect(self.worker.run)
        
        # 连接信号
        self.worker.progress.connect(self.updateProgress.emit)
        self.worker.finished.connect(self.handle_worker_finished)
        self.worker.log.connect(self.logMessage.emit)
        self.worker.stats_updated.connect(self.update_stats)
        
        self.current_thread.start()
        
    def update_progress(self, value, status):
        self.progress.setValue(value)
        self.status_label.setText(f"状态: {status}")
        
    def append_log(self, message):
        self.log_text.append(message)
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )
        
    def handle_worker_finished(self, success, message):
        self.installationComplete.emit(success, message)
        if hasattr(self, 'current_thread'):
            self.worker.stop()
            self.current_thread.quit()
            self.current_thread.wait()
            
    def handle_installation_complete(self, success, message):
        self.installation_completed = success
        if success:
            if not self.wizard().silent_mode:
                QMessageBox.information(self, "安装完成", message)
                if self.wizard():
                    self.wizard().button(QWizard.FinishButton).setEnabled(True)
                    # 安装完成后保持后退按钮禁用
                    self.wizard().button(QWizard.BackButton).setEnabled(False)
        else:
            if not self.wizard().silent_mode:
                QMessageBox.critical(self, "安装失败", message)
            else:
                print(f"安装失败: {message}")

    def update_stats(self, stats):
        """更新所有状态标签"""
        self.speed_label.setText(stats['speed'])
        self.thread_label.setText(stats['threads'])
        self.time_label.setText(stats['time'])
        self.size_label.setText(stats['size'])
        self.file_label.setText(stats['file'])
        self.status_label.setText(stats['status'])

    def isComplete(self):
        return self.installation_completed

class InstallationWorker(QObject):
    # 定义信号
    progress = pyqtSignal(int, str)  # 进度信号
    finished = pyqtSignal(bool, str)  # 完成信号
    log = pyqtSignal(str)  # 日志信号
    stats_updated = pyqtSignal(dict)  # 状态更新信号

    def __init__(self, install_path, silent_mode, selected_version, use_mirror=False):
        super().__init__()
        self.install_path = install_path
        self.silent_mode = silent_mode
        self.selected_version = selected_version
        self.use_mirror = use_mirror
        self._is_running = False

    def stop(self):
        self._is_running = False
        
    def run(self):
        self._is_running = True
        try:
            # 配置日志
            log_file = os.path.join(self.install_path, "tsukinotes_update.log")
            logging.basicConfig(
                filename=log_file,
                level=logging.INFO,
                format='[%(asctime)s | %(levelname)s] %(message)s',
                datefmt='%Y/%m/%d %H:%M:%S',
                encoding='utf-8'
            )
            
            self.log.emit("开始安装...")
            self.progress.emit(0, "正在准备...")
            
            # 检查版本
            current_version = get_current_version(self.install_path)
            self.log.emit(f"当前版本: {current_version or '未安装'}")
            
            if not self.selected_version:
                raise Exception("未选择安装版本")
                
            # 下载
            self.progress.emit(20, "正在下载...")
            self.download_package()
            
            # 安装
            self.progress.emit(60, "正在安装...")
            self.extract_and_overwrite_files(self.install_path)
            
            # 创建快捷方式
            self.progress.emit(80, "正在创建快捷方式...")
            self.update_shortcuts(self.install_path)
            
            self.progress.emit(100, "安装完成!")
            self.finished.emit(True, "安装成功完成!")
            
        except Exception as e:
            self.log.emit(f"安装失败: {str(e)}")
            self.finished.emit(False, str(e))
        finally:
            self._is_running = False

    def download_package(self):
        try:
            download_url = self.selected_version['download_url']
            file_size = self.selected_version.get('size', 0)
            
            self.log.emit(f"准备下载，文件大小: {file_size/(1024*1024):.1f} MB")
            
            if self.use_mirror:
                # 使用 github.hanxuan.filegear-sg.me 镜像
                download_url = f"https://github.hanxuan.filegear-sg.me/{download_url}"
            
            # 创建临时文件
            self.temp_file = os.path.join(self.install_path, 
                f"TsukiNotes_UpdateTempPackage_{self.selected_version['version']}.zip")
            
            # 确保临时文件不存在
            if os.path.exists(self.temp_file):
                os.remove(self.temp_file)
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive'
            }
            
            timeout = 60
            
            try:
                # start download
                response = requests.get(download_url, headers=headers, stream=True, timeout=timeout)
                response.raise_for_status()
                
                # 重置下载大小计数器
                downloaded_size = 0
                start_time = time.time()
                
                with open(self.temp_file, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=32768):
                        if chunk:
                            chunk_size = len(chunk)
                            f.write(chunk)
                            downloaded_size += chunk_size
                            
                            elapsed_time = time.time() - start_time
                            if elapsed_time > 0:
                                speed = downloaded_size / (1024 * 1024 * elapsed_time)  # MB/s
                                progress = int((downloaded_size / file_size) * 100) if file_size else 0
                                
                                # 更新状态
                                stats = {
                                    'speed': f"下载速度: {speed:.2f} MB/s",
                                    'threads': f"使用线程: 1",
                                    'time': f"已经下载: {downloaded_size/(1024*1024):.1f} MB",
                                    'size': f"文件大小: {downloaded_size/(1024*1024):.1f} MB",
                                    'file': f"TsukiNotes: {os.path.basename(self.temp_file)}",
                                    'status': f"下载中{progress}%......"
                                }
                                self.stats_updated.emit(stats)
                                self.progress.emit(20 + int(progress * 0.4), f"下载中... {progress}%")
                
                self.log.emit(f"下载完成 - 总大小: {downloaded_size/(1024*1024):.1f} MB")
                return
                    
            except requests.exceptions.RequestException as e:
                raise Exception(f"下载失败: {str(e)}")
                    
        except Exception as e:
            self.log.emit(f"下载失败: {str(e)}")
            if os.path.exists(self.temp_file):
                try:
                    os.remove(self.temp_file)
                except:
                    pass
            raise

    def extract_and_overwrite_files(self, install_path):
        try:
            # 改进文件占用检查
            def check_file_usage(path):
                if os.path.exists(path):
                    try:
                        # 尝试打开目录下的所有文件
                        for root, dirs, files in os.walk(path):
                            for file in files:
                                file_path = os.path.join(root, file)
                                try:
                                    with open(file_path, 'a+b') as f:
                                        pass
                                except:
                                    return True
                        return False
                    except:
                        return True
                return False
                
            # 检查目标文件夹是否被占用
            if check_file_usage(install_path):
                # 尝试强制结束占用进程
                self.log.emit("检测到文件占用，尝试清理...")
                if not self.close_file_occupancy(install_path):
                    raise Exception("无法清理文件占用，请手动关闭相关程序后重试")
                
                # 等待文件系统更新
                time.sleep(2)
                
                # 再次检查
                if check_file_usage(install_path):
                    raise Exception("安装目录仍被占用，请手动关闭相关程序后重试")

            # 原有的解压逻辑
            with zipfile.ZipFile(self.temp_file, 'r') as zip_ref:
                total_files = len(zip_ref.namelist())
                total_size = sum(zip_info.file_size for zip_info in zip_ref.filelist)
                extracted_size = 0
                
                for index, file in enumerate(zip_ref.namelist()):
                    if not self._is_running:
                        raise Exception("安装被取消")
                    
                    start_time = time.time()
                    zip_ref.extract(file, install_path)
                    extracted_size += zip_ref.getinfo(file).file_size
                    
                    # 更新状态
                    stats = {
                        'speed': f"速度: {zip_ref.getinfo(file).file_size/(1024*1024):.2f} MB/s",
                        'threads': f"线程: {threading.active_count()}",
                        'time': f"剩余时间: {self.format_time((total_files-index) * 0.1)}",
                        'size': f"大小: {extracted_size/(1024*1024):.1f}/{total_size/(1024*1024):.1f} MB",
                        'file': f"当前文件: {file}",
                        'status': "正在解压..."
                    }
                    self.stats_updated.emit(stats)
                    
                    progress = int((extracted_size / total_size) * 20) + 60
                    self.progress.emit(progress, f"解压中... {index+1}/{total_files}")
            
            # 解压完成后删除临时文件
            try:
                if os.path.exists(self.temp_file):
                    os.remove(self.temp_file)
                    self.log.emit("临时安装包已清理")
            except Exception as e:
                self.log.emit(f"清理临时文件失败: {str(e)}")
            
            self.log.emit(f"文件解压完成 - 共 {total_files} 个文件")
            
        except Exception as e:
            self.log.emit(f"解压失败: {str(e)}")
            # 出错时也尝试清理临时文件
            try:
                if os.path.exists(self.temp_file):
                    os.remove(self.temp_file)
            except:
                pass
            raise

    def update_shortcuts(self, install_path):
        try:
            self.log.emit("正在更新快捷方式...")
            
            # 获取路径
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            shell = win32com.client.Dispatch("WScript.Shell")
            
            # 创建主程序快捷方式
            target_path = os.path.join(install_path, "TsukiNotes.exe")
            shortcut_path = os.path.join(desktop, "TsukiNotes.lnk")
            
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = target_path
            shortcut.WorkingDirectory = install_path
            shortcut.IconLocation = target_path + ",0"  # 使用程序图标
            shortcut.save()
            
            # 注册文件关联
            file_types = ['.txt', '.md', '.markdown']  # 可以添加更多格式
            
            for ext in file_types:
                try:
                    # 注册文件类型
                    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\\Classes\\{ext}") as key:
                        winreg.SetValue(key, "", winreg.REG_SZ, "TsukiNotes.Document")
                    
                    # 创建程序ID
                    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, "Software\\Classes\\TsukiNotes.Document") as key:
                        winreg.SetValue(key, "", winreg.REG_SZ, f"TsukiNotes {ext} Document")
                        
                        # 添加图标
                        with winreg.CreateKey(key, "DefaultIcon") as icon_key:
                            winreg.SetValue(icon_key, "", winreg.REG_SZ, f"{target_path},0")
                        
                        # 添加打开命令
                        with winreg.CreateKey(key, "shell\\open\\command") as cmd_key:
                            winreg.SetValue(cmd_key, "", winreg.REG_SZ, f'"{target_path}" "%1"')
                    
                    self.log.emit(f"已关联{ext}文件格式")
                    
                except Exception as e:
                    self.log.emit(f"关联{ext}格式失败: {str(e)}")
            
            # 刷新系统图标缓存
            try:
                os.system("ie4uinit.exe -show")
            except:
                pass
            
            self.log.emit("快捷方式和文件关联更新完成")
            
        except Exception as e:
            self.log.emit(f"创建快捷方式失败: {str(e)}")
            raise

    @staticmethod
    def format_time(seconds):
        """格式化时间显示"""
        if seconds < 60:
            return f"{seconds:.0f}秒"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f}分钟"
        else:
            hours = seconds / 3600
            return f"{hours:.1f}小时"

    def close_file_occupancy(self, path):
        """改进的文件占用清理函数"""
        self.log.emit("开始清理文件占用...")
        
        try:
            # 获取占用进程列表
            for proc in psutil.process_iter(['pid', 'name', 'open_files']):
                try:
                    # 检查进程打开的文件
                    for file in proc.open_files():
                        if path.lower() in file.path.lower():
                            # 发现占用进程，尝试结束
                            self.log.emit(f"发现占用进程: {proc.name()} (PID: {proc.pid})")
                            proc.kill()
                            self.log.emit(f"已终止进程: {proc.name()}")
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue

            # 等待进程完全结束
            time.sleep(2)
            
            # 使用系统命令强制结束可能的残留进程
            known_processes = ['TsukiNotes.exe', 'python.exe', 'pythonw.exe']
            for proc_name in known_processes:
                os.system(f'taskkill /F /IM {proc_name} /T 2>nul')
            
            # 清理文件系统缓存
            os.system('ipconfig /flushdns')
            
            return True
            
        except Exception as e:
            self.log.emit(f"清理过程出错: {str(e)}")
            return False

    def extract_package(self):
        """解压安装包"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    self.log.emit(f"正在进行第 {attempt + 1} 次解压尝试...")
                    
                # 强制清理目录
                self.log.emit("准备解压，先清理目录...")
                if not self.close_file_occupancy(self.install_path):
                    if attempt == max_retries - 1:
                        raise Exception("无法清理安装目录")
                    continue

                time.sleep(2)  # 等待文件系统更新

                # 检查目录是否可写
                self.log.emit("检查目录权限...")
                test_file = os.path.join(self.install_path, "write_test")
                try:
                    with open(test_file, 'w') as f:
                        f.write('test')
                    os.remove(test_file)
                    self.log.emit("目录权限检查通过")
                except Exception as e:
                    self.log.emit(f"目录权限检查失败: {str(e)}")
                    if attempt == max_retries - 1:
                        raise Exception("无法获取目录写入权限")
                    continue

                # 解压文件
                self.log.emit("开始解压文件...")
                with zipfile.ZipFile(self.temp_file, 'r') as zip_ref:
                    total_files = len(zip_ref.namelist())
                    for index, file in enumerate(zip_ref.namelist(), 1):
                        try:
                            self.log.emit(f"正在解压: {file}")
                            zip_ref.extract(file, self.install_path)
                            progress = int((index / total_files) * 100)
                            self.progress.emit(60 + int(progress * 0.3), f"正在解压... {progress}%")
                        except Exception as e:
                            self.log.emit(f"解压文件 {file} 失败: {str(e)}")
                            if attempt == max_retries - 1:
                                raise
                            break
                    else:
                        self.log.emit("解压完成")
                        return

                if attempt < max_retries - 1:
                    self.log.emit("解压失败，准备重试...")
                    time.sleep(3)
                
            except Exception as e:
                if attempt == max_retries - 1:
                    raise Exception(f"解压失败: {str(e)}")
            
        raise Exception("解压失败: 已达到最大重试次数")

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        
        # 设置应用程序默认字体
        app.setFont(QFont("Microsoft YaHei UI, Segoe UI", 9))
        
        # 请求管理员权限
        run_as_admin()
        wizard = InstallerWizard(silent_mode=False)
        wizard.show()
        
        sys.exit(app.exec_())
        
    except Exception as e:
        error_msg = f"程序启动失败: {str(e)}"
        logging.error(error_msg)
        try:
            QMessageBox.critical(None, "错误", error_msg)
        except:
            print(error_msg)
        sys.exit(1)