#==================================
# Install Lite For TsukiNotes
# Lite Version ≠ Wizard
# B2.0.0
# 2025/01/01
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
            'Accept': 'application/vnd.github.v3+json'
        }
        
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()
        
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
                        'size': asset.get('size'),
                        'version': '',
                        'attributes': []
                    }
                    
                    parts = name.replace('.zip', '').split('_')
                    version = parts[0].replace('TsukiNotesVer', '')
                    version_info['version'] = version
                    
                    if len(parts) > 1:
                        version_info['attributes'] = parts[1:]
                    
                    versions.append(version_info)
        
        return versions if versions else None
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

class InstallerWizard(QWizard):
    def __init__(self, silent_mode=False):
        super().__init__()
        self.silent_mode = silent_mode
        self.setWindowTitle("TsukiNotes 更新安装向导")
        self.setWindowIcon(QIcon('tsuki/assets/GUI/resources/GUI/logo.png'))
        self.resize(800, 600)
        
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
                margin: 10px;
                padding: 20px;
                border: 1px solid rgba(255, 255, 255, 0.8);
            }
            QLabel {
                color: #333333;
                font-size: 14px;
            }
            QLineEdit, QComboBox {
                border: 2px solid #e0e0e0;
                padding: 8px;
                border-radius: 8px;
                background-color: #ffffff;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #60CDFF;
            }
            QPushButton {
                min-height: 35px;
                border-radius: 6px;
                padding: 0 20px;
                background-color: #60CDFF;
                color: white;
                border: none;
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
        """)
        
        self.install_path = os.getcwd()
        self.selected_version = None
        
        # 添加页面
        self.addPage(WelcomePage())
        self.addPage(VersionSelectPage())
        self.addPage(InstallProgressPage())
        
        # 窗口动画效果
        self.setWindowOpacity(0)
        self.fade_in_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_animation.setDuration(300)
        self.fade_in_animation.setStartValue(0)
        self.fade_in_animation.setEndValue(1)
        self.fade_in_animation.start()
        
        # 添加页面切换动画
        self.page_animation = QPropertyAnimation(self, b"windowOpacity")
        self.page_animation.setDuration(200)
        
        # 自动安装定时器
        QTimer.singleShot(0, self.auto_install)

    def auto_install(self):
        if self.silent_mode:
            self.next()

    def closeEvent(self, event):
        if hasattr(self, 'worker') and self.worker:
            self.worker.stop()
        if hasattr(self, 'thread') and isinstance(self.thread, QThread):
            self.thread.quit()
            self.thread.wait()
        super().closeEvent(event)

    def nextId(self):
        # 页面切换动画
        self.page_animation.setStartValue(1.0)
        self.page_animation.setEndValue(0.8)
        self.page_animation.start()
        QTimer.singleShot(200, lambda: self.fade_in())
        return super().nextId()
        
    def fade_in(self):
        self.page_animation.setStartValue(0.8)
        self.page_animation.setEndValue(1.0)
        self.page_animation.start()

class WelcomePage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Hey Welcome -TsukiNotes 更新安装向导")
        
        layout = QVBoxLayout()
        
        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap('tsuki/assets/GUI/resources/GUI/logo.png')
        if not logo_pixmap.isNull():
            logo_pixmap = logo_pixmap.scaled(128, 128, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(logo_pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(logo_label)
        
        # 欢迎文本
        welcome_text = QLabel(
            "TsukiNotes Update Lite Ver2.0.0\n\n"
            "Click <Next> to start the installation process.\n"
            "Click <Cancel> to exit the installation process."
        )
        welcome_text.setWordWrap(True)
        welcome_text.setAlignment(Qt.AlignCenter)
        welcome_text.setStyleSheet("""
            QLabel {
                color: #333333;
                font-size: 16px;
                margin: 20px;
            }
        """)
        
        layout.addWidget(welcome_text)
        layout.addStretch()
        
        self.setLayout(layout)

class VersionSelectPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("| Select Version")
        self.setSubTitle("请选择要安装的 TsukiNotes 版本\n我建议你安装最新版本")
        self.setFocusPolicy(Qt.NoFocus) # 取消焦点       
        layout = QVBoxLayout()
        # 版本列表
        self.version_list = QListWidget()
        self.version_list.setFocusPolicy(Qt.NoFocus) # 取消焦点
        self.version_list.setStyleSheet("""
            QListWidget {
                border: 2px solid #e0e0e0;
                border-radius: 12px;
                padding: 5px;
                background-color: #ffffff;
            }
            QListWidget::item {
                padding: 12px;
                margin: 5px;
                border-radius: 8px;
                background-color: #f8f9fa;
                border: 1px solid #e0e0e0;
            }
            QListWidget::item:selected {
                background-color: #60CDFF;
                color: white;
                border: none;
            }
            QListWidget::item:hover:!selected {
                background-color: #f0f0f0;
                border: 1px solid #60CDFF;
            }
        """)
        
        layout.addWidget(self.version_list)
        
        # 版本信息面板
        self.info_panel = QTextEdit()
        self.info_panel.setReadOnly(True)
        self.info_panel.setMaximumHeight(100)
        self.info_panel.setStyleSheet("""
            QTextEdit {
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 10px;
                background-color: #F8F9FA;
            }
        """)
        
        layout.addWidget(self.info_panel)
        
        self.setLayout(layout)
        
        # 连接信号
        self.version_list.currentItemChanged.connect(self.update_info_panel)
        
        # 为列表添加阴影效果
        list_shadow = QGraphicsDropShadowEffect()
        list_shadow.setBlurRadius(20)
        list_shadow.setXOffset(0)
        list_shadow.setYOffset(2)
        list_shadow.setColor(QColor(0, 0, 0, 30))
        self.version_list.setGraphicsEffect(list_shadow)
        
    def initializePage(self):
        self.version_list.clear()
        self.info_panel.clear()
        
        versions = check_version()
        if not versions:
            self.version_list.addItem("无法获取版本信息")
            return
            
        for version_info in versions:
            version = version_info['version']
            attributes = ' | '.join(version_info['attributes'])
            size_mb = round(version_info['size'] / (1024 * 1024), 2)
            
            item = QListWidgetItem(f"TsukiNotes {version}")
            item.setData(Qt.UserRole, version_info)
            self.version_list.addItem(item)
            
        if self.version_list.count() > 0:
            self.version_list.setCurrentRow(0)
            
    def update_info_panel(self, current, previous):
        if current:
            try:
                version_info = current.data(Qt.UserRole)
                if not version_info:
                    self.info_panel.setText("无法获取版本信息")
                    return
                    
                info_text = (
                    f"选中版本号: {version_info.get('version', '未知')}\n"
                    f"版本特性: {' | '.join(version_info.get('attributes', []))}\n"
                    f"版本大小: {round(version_info.get('size', 0) / (1024 * 1024), 2)} MB\n"
                    f"已安装版本: {get_current_version(self.wizard().install_path) or '未安装'}"
                )
                self.info_panel.setText(info_text)
            except Exception as e:
                self.info_panel.setText(f"获取版本信息时出错: {str(e)}")
            
    def validatePage(self):
        current_item = self.version_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "警告", "你必须选择一个版本")
            return False
            
        version_info = current_item.data(Qt.UserRole)
        self.wizard().selected_version = version_info
        return True

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
                padding: 10px;
            }
        """)
        status_layout = QGridLayout()
        
        # 添加详细信息标签
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
        
        # 美化日志显示
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: rgba(248, 249, 250, 0.9);
                border: 1px solid rgba(224, 224, 224, 0.8);
                border-radius: 15px;
                padding: 15px;
                font-family: "Cascadia Code", "Consolas", monospace;
                font-size: 12px;
                line-height: 1.4;
            }
        """)
        layout.addWidget(self.log_text)
        
        self.setLayout(layout)
        
        # 连接信号
        self.updateProgress.connect(self.update_progress)
        self.installationComplete.connect(self.handle_installation_complete)
        self.logMessage.connect(self.append_log)
        
    def initializePage(self):
        QTimer.singleShot(0, self.start_installation)
        
    def start_installation(self):
        self.thread = QThread()
        self.worker = InstallationWorker(
            self.wizard().install_path,
            self.wizard().silent_mode,
            self.wizard().selected_version
        )
        
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        
        # 连接所有信号
        self.worker.progress.connect(self.updateProgress.emit)
        self.worker.finished.connect(self.handle_worker_finished)
        self.worker.log.connect(self.logMessage.emit)
        self.worker.stats_updated.connect(self.update_stats)  # 新增状态更新连接
        
        self.thread.start()
        
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
        if self.thread:
            self.worker.stop()
            self.thread.quit()
            self.thread.wait()
            
    def handle_installation_complete(self, success, message):
        if success:
            if not self.wizard().silent_mode:
                QMessageBox.information(self, "安装完成", message)
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

class InstallationWorker(QObject):
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(bool, str)
    log = pyqtSignal(str)
    stats_updated = pyqtSignal(dict)  # 新增统一的状态更新信号

    def __init__(self, install_path, silent_mode, selected_version):
        super().__init__()
        self.install_path = install_path
        self.silent_mode = silent_mode
        self.selected_version = selected_version
        self._is_running = False
        
    def stop(self):
        self._is_running = False
        
    def run(self):
        self._is_running = True
        try:
            # 配置日志
            log_file = os.path.join(self.install_path, "tsuki_update.log")
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

    def download_package(self):
        try:
            download_url = self.selected_version['download_url']
            self.temp_file = os.path.join(self.install_path, "TsukiNotes_UpdateTempPackage_{version}.zip".format(version=self.selected_version['version']))
            
            # 获取文件大小
            total_size = self.selected_version.get('size', 0)
            if total_size == 0:
                response = requests.get(download_url, stream=True)
                total_size = int(response.headers.get('content-length', 0))
                response.close()
            
            self.log.emit(f"文件大小: {total_size/(1024*1024):.1f} MB")
            
            # 清理可能存在的损坏文件
            if os.path.exists(self.temp_file):
                os.remove(self.temp_file)
            
            # 使用单线程下载以确保文件完整性
            response = requests.get(download_url, stream=True)
            response.raise_for_status()
            
            with open(self.temp_file, 'wb') as f:
                downloaded_size = 0
                last_update_time = time.time()
                bytes_since_last_update = 0
                
                for chunk in response.iter_content(chunk_size=1024*1024):
                    if not self._is_running:
                        return
                    
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        bytes_since_last_update += len(chunk)
                        
                        current_time = time.time()
                        time_diff = current_time - last_update_time
                        
                        # 每0.5秒更新一次状态
                        if time_diff >= 0.5:
                            progress = int((downloaded_size / total_size) * 40) + 20 if total_size > 0 else 0
                            speed = bytes_since_last_update / (time_diff * 1024 * 1024) if time_diff > 0 else 0
                            
                            # 计算剩余时间
                            remaining_time = "--"
                            if speed > 0:
                                remaining_seconds = (total_size - downloaded_size) / (speed * 1024 * 1024)
                                remaining_time = self.format_time(remaining_seconds)
                            
                            stats = {
                                'speed': f"速度: {speed:.2f} MB/s",
                                'threads': "线程: 1",
                                'time': f"剩余时间: {remaining_time}",
                                'size': f"大小: {downloaded_size/(1024*1024):.1f}/{total_size/(1024*1024):.1f} MB",
                                'file': f"当前文件: {os.path.basename(self.temp_file)}",
                                'status': "正在下载..."
                            }
                            self.stats_updated.emit(stats)
                            self.progress.emit(progress, f"下载中... {downloaded_size/(1024*1024):.1f}/{total_size/(1024*1024):.1f} MB")
                            
                            # 重置计数器
                            last_update_time = current_time
                            bytes_since_last_update = 0
                
            # 验证下载的文件
            if os.path.getsize(self.temp_file) != total_size:
                raise Exception("下载的文件大小不正确")
            
            # 验证是否为有效的ZIP文件
            try:
                with zipfile.ZipFile(self.temp_file, 'r') as test_zip:
                    test_zip.testzip()
            except zipfile.BadZipFile:
                raise Exception("下载的文件不是有效的ZIP文件")
            
            self.log.emit(f"下载完成 - 总大小: {total_size/(1024*1024):.1f} MB")
            
        except Exception as e:
            if os.path.exists(self.temp_file):
                os.remove(self.temp_file)
            self.log.emit(f"下载失败: {str(e)}")
            raise

    def extract_and_overwrite_files(self, install_path):
        try:
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
            
            self.log.emit(f"文件解压完成 - 共 {total_files} 个文件")
            
        except Exception as e:
            self.log.emit(f"解压失败: {str(e)}")
            raise

    def update_shortcuts(self, install_path):
        try:
            self.log.emit("正在更新快捷方式...")
            
            # 获取桌面路径
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            
            # 创建快捷方式
            target_path = os.path.join(install_path, "TsukiNotes.exe")
            shortcut_path = os.path.join(desktop, "TsukiNotes.lnk")
            
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = target_path
            shortcut.WorkingDirectory = install_path
            shortcut.save()
            
            self.log.emit("快捷方式更新完成")
            
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

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        
        # 设置应用程序样式
        app.setStyle("Fusion")
        app.setFont(QFont("Microsoft YaHei UI", 9))
        
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