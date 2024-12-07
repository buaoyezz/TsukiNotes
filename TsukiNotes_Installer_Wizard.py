#====================================================================
# Name: TsukiNotes Installer Wizard ✨ | 💠Version 1.5.0.16000 | Online Installer
# Powered by ZZBuAoYe
# Github: https://github.com/buaoyezz
# TsukiNotes Build Date: 2024/12/07
# Install Version: 0.0.2.15200
# Enjoy!
#====================================================================
import sys
import os
import shutil
import winreg
import ctypes
import requests
import zipfile
import time
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import win32com.client
import tempfile

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        # 用管理员权限重启Shell
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

run_as_admin()
        
class InstallerWizard(QWizard):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TsukiNotes Wizard ✨ | 💠Version 1.5.0.16000 | Online Installer")
        self.resize(800, 600)
        
        self.install_path = r"C:\Program Files\TsukiNotes"
        self.create_shortcut = False
        self.add_to_path = False
        self.associate_files = False
        self.add_context_menu = False
        
        self.setStyleSheet("""
            * {
                font-family: "Microsoft YaHei", sans-serif;
            }
            QWizard {
                background-color: #f0f0f0;
            }
            QWizardPage {
                background-color: white;
                border-radius: 10px;
                margin: 10px;
            }
            QPushButton {
                background-color: #60CDFF;  
                color: black;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #99E5FF; 
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                font-size: 13px;
            }
            QCheckBox {
                spacing: 10px;
                font-size: 13px;
            }
            QProgressBar {
                border: none;
                border-radius: 3px;
                background-color: #f0f0f0;
                height: 8px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4a90e2;
                border-radius: 3px;
            }
            QLabel {
                font-size: 13px;
            }
            QGroupBox {
                font-weight: bold;
                padding: 15px;
                margin-top: 10px;
            }
        """)
        
        # 添加页面
        self.addPage(WelcomePage())
        self.addPage(LicensePage())
        self.addPage(InstallPathPage())
        self.addPage(InstallProgressPage())
        self.addPage(FinalOptionsPage())
        self.addPage(CompletePage())
        
        self.setWizardStyle(QWizard.ModernStyle)
        
        # load logo
        logo_url = "https://img.picui.cn/free/2024/10/26/671ca15ba4d46.png"  # 替换为实际的图床URL
        try:
            response = requests.get(logo_url)
            if response.status_code == 200:
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)
                self.setPixmap(QWizard.LogoPixmap, pixmap.scaled(100, 100, Qt.KeepAspectRatio))  # 缩小到100x100
        except:
            pass  # if failed use default
        
        # 添加错误处理标志
        self.error_occurred = False
        
        # 禁用默认按钮
        self.setOption(QWizard.NoBackButtonOnStartPage, True)
        self.setOption(QWizard.NoBackButtonOnLastPage, True)
        
        # 添加按钮点击处理
        self.button(QWizard.BackButton).clicked.connect(self.handle_back_button)
        
    def handle_back_button(self):
        # 如果当前页面是安装页面，阻止返回
        current_page = self.currentPage()
        if isinstance(current_page, InstallProgressPage):
            self.button(QWizard.BackButton).setEnabled(False)
            return False

class WelcomePage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("欢迎使用 TsukiNotes 安装向导")
        
        main_layout = QHBoxLayout()
        left_panel = QWidget()
        left_panel.setFixedWidth(200)
        left_layout = QVBoxLayout(left_panel)
        
        # logo
        logo_label = QLabel()
        logo_url = "https://img.picui.cn/free/2024/10/26/671ca15ba4d46.png"  # url
        try:
            response = requests.get(logo_url)
            if response.status_code == 200:
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)
                logo_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio))
        except:
            pass 
        left_layout.addWidget(logo_label, alignment=Qt.AlignCenter)
        left_layout.addStretch()
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        
        welcome_text = QLabel(
            "<h2>| TsukiNotes Install Wizard</h2>"
            "<p>TsukiNotes 是一个强大的笔记应用程序，"
            "能够帮助您更好地管理和组织您的笔记</p>"
            "<p>感谢使用TsukiNotes,开始您的笔记之旅吧!</p>"
            "<p>此安装器在线安装包|将安装最新版的TsukiNotes</p>"
            "<p>点击<b> Commit </b>开始安装把！</p>"
        )
        welcome_text.setWordWrap(True)
        welcome_text.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #333;
                line-height: 1.6;
            }
        """)
        
        content_layout.addWidget(welcome_text)
        content_layout.addStretch()
        
        # 组合布局
        main_layout.addWidget(left_panel)
        main_layout.addWidget(content_widget, 1)
        self.setLayout(main_layout)
        
        # 添加这行来隐藏Back按钮
        self.setCommitPage(True)

class LicensePage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("许可协议")
        self.setSubTitle("请仔细阅读以下许可协议")
        
        layout = QVBoxLayout()
        
        # 许可协议文本框
        license_text = QTextEdit()
        license_text.setReadOnly(True)
        license_text.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 10px;
            }
        """)
        
        license_content = """
        TsukiNotes 软件关于文档
        
        1. 使用条款
        本软件为免费软件，您可以自由使用、复制和分发本软件
        本软件是开源软件,遵守GPLv3协议
        如果喜欢请给我个star
        
        2. 免责声明
        本软件按"现状"提供，不提供任何明示或暗示的保证
        本软件不存在任何形式的广告/推广/宣传/VIP等模式
        本软件不收集任何用户数据
        本软件可能修改部分文件关联，为了更好的使用体验，不存在任何恶意行为
        
        3. 限制
        请勿将本软件商业性倒卖
        请勿将本软件用于任何违法违规用途
        
        4. 终止
        如果您违反本协议的何条款，本软件不提供任何技支持
        
        5. 适用法律
        本协议受中华人民共和国法律管辖
        """
        license_text.setText(license_content)
        layout.addWidget(license_text)
        
        # 同意复选框
        self.agree_checkbox = QCheckBox("我已阅读并同意上述协议条款")
        self.agree_checkbox.stateChanged.connect(self.completeChanged)
        layout.addWidget(self.agree_checkbox)
        
        self.setLayout(layout)
        
    def isComplete(self):
        return self.agree_checkbox.isChecked()

class InstallPathPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("选择安装位置")
        self.setSubTitle("请选择 TsukiNotes 的安装目录")
        
        layout = QVBoxLayout()
        
        # 路径选择
        path_group = QGroupBox("安装目录")
        path_layout = QHBoxLayout()
        
        self.path_edit = QLineEdit(os.path.join(r"C:\Program Files", "TsukiNotes"))
        self.path_edit.setMinimumWidth(300)
        self.path_edit.textChanged.connect(self.update_space_info)
        
        browse_btn = QPushButton("浏览...")
        browse_btn.clicked.connect(self.browse_path)
        
        path_layout.addWidget(self.path_edit)
        path_layout.addWidget(browse_btn)
        path_group.setLayout(path_layout)
        
        # 空间信息
        self.space_info = QLabel()
        self.update_space_info()
        
        layout.addWidget(path_group)
        layout.addWidget(self.space_info)
        layout.addStretch()
        
        
        # Register the install_path field
        self.skip_button = QPushButton("跳过")
        self.skip_button.clicked.connect(self.skip_installation)
        self.skip_button.setVisible(False)  # 初始隐藏
        layout.addWidget(self.skip_button)
        
        self.setLayout(layout)
        
        # Register the install_path field
        self.registerField("install_path*", self.path_edit)
        
        # 添加验证
        self.path_edit.textChanged.connect(self.completeChanged)
        
    def get_free_space(self, path):
        try:
            # 获取路径所在的驱动器根目录
            drive = os.path.splitdrive(path)[0]
            if drive:
                total, used, free = shutil.disk_usage(drive)
                return free / (2**30)  # 转换为GB
        except:
            return None
            
    def update_space_info(self):
        path = self.path_edit.text()
        free_space = self.get_free_space(path)
        if free_space is not None:
            self.space_info.setText(f"可用空间: {free_space:.2f} GB")
        else:
            self.space_info.setText("无法获取空间信息")
            
    def browse_path(self):
        path = QFileDialog.getExistingDirectory(
            self,
            "选择安装目录",
            self.path_edit.text(),
            QFileDialog.ShowDirsOnly
        )
        if path:
            self.path_edit.setText(os.path.join(path, "TsukiNotes"))
    def initializePage(self):
        path = self.path_edit.text()
        if os.path.exists(os.path.join(path, "TsukiNotes.exe")):
            self.skip_button.setVisible(True)
            QMessageBox.information(self, "已安装", 
                "检测到TsukiNotes已经安装在该目录。\n"
                "您可以选择重新安装或跳过安装。")
        else:
            self.skip_button.setVisible(False)
            
    def skip_installation(self):
        """跳过安装，直接进入完成页面"""
        wizard = self.wizard()
        wizard.next()  # 跳过安装进度页面
        wizard.next()  # 跳过选项页面   

    def isComplete(self):
        # 确保路径不为空且有效
        path = self.path_edit.text()
        return bool(path and os.path.splitdrive(path)[0])


from PyQt5.QtCore import (QThread, pyqtSignal, pyqtSlot, QMetaObject,
                         Qt, Q_ARG)

class InstallProgressPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("正在安装")
        self.setSubTitle("请等待安装完成...")
        
        # 强制禁用返回
        self.setCommitPage(True)
        
        layout = QVBoxLayout()
        
        # 进度条和状态显示
        progress_group = QGroupBox("安装进度")
        progress_layout = QVBoxLayout()
        
        # 主进度条
        self.progress = QProgressBar()
        self.progress.setFixedHeight(8)
        self.progress.setRange(0, 100)
        self.progress.setTextVisible(False)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 3px;
                background-color: #f0f0f0;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4a90e2;
                border-radius: 3px;
            }
        """)
        progress_layout.addWidget(self.progress)
        
        # 状态显示
        self.status_label = QLabel("准备安装...")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #666;
                font-size: 14px;
                margin: 5px 0;
            }
        """)
        progress_layout.addWidget(self.status_label)
        
        # 详细信息文本框
        self.detail_text = QTextEdit()
        self.detail_text.setReadOnly(True)
        self.detail_text.setFixedHeight(200)  # 增加高度以显示更多日志
        self.detail_text.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px;
                font-family: Consolas, monospace;
                font-size: 12px;
            }
        """)
        progress_layout.addWidget(self.detail_text)
        
        progress_group.setLayout(progress_layout)
        layout.addWidget(progress_group)
        
        # 添加提示
        tip_label = QLabel(
            "<p style='color: #666; font-size: 11px;'>"
            "安装完成后，您可以点击*返回*按钮查看完整的安装日志。</p>"
        )
        tip_label.setWordWrap(True)
        layout.addWidget(tip_label)
        
        layout.addStretch()
        self.setLayout(layout)
        
        # 初始化其他属性
        self.download_thread = None
        self.is_installation_complete = False
        self.installation_in_progress = False
        self.is_cancelling = False
        self.is_cleaning = False
        
    def validatePage(self):
        if self.installation_in_progress:
            return False
        return self.is_installation_complete

    def initializePage(self):
        # 立即禁用所有按钮
        QTimer.singleShot(0, self.disable_buttons)
        # 延迟开始安装，给UI时间刷新
        QTimer.singleShot(100, self.start_installation)
        
        # 重写取消按钮的行为
        wizard = self.wizard()
        wizard.button(QWizard.CancelButton).setEnabled(True)
        wizard.button(QWizard.CancelButton).clicked.disconnect() # 断开所有之前的连接
        wizard.button(QWizard.CancelButton).clicked.connect(self.handle_cancel)
    
    def disable_buttons(self):
        wizard = self.wizard()
        wizard.button(QWizard.BackButton).setEnabled(False)
        wizard.button(QWizard.NextButton).setEnabled(False)
    
    def start_installation(self):
        self.installation_in_progress = True
        self.is_installation_complete = False
        self.perform_installation()
    
    def handle_error(self, error_message):
        """处理安装过程中的错误"""
        self.installation_in_progress = False
        
        # 先显示错误消息
        QMessageBox.critical(self, "安装错误", f"安装过程中发生错误:\n{error_message}")
        
        # 启用返回和取消按钮
        wizard = self.wizard()
        wizard.button(QWizard.NextButton).setEnabled(False)
        wizard.button(QWizard.BackButton).setEnabled(True)
        wizard.button(QWizard.CancelButton).setEnabled(True)
        
        # 更新状态
        self.status_label.setText("安装失败")
        self.detail_text.append("\n安装失败: " + error_message)
        self.progress.setValue(0)

    def perform_installation(self):
        install_path = self.wizard().field("install_path")
        
        try:
            # 创建下载线程
            self.download_thread = DownloadThread(
                self.wizard().field("install_path"),
                self.update_status,
                self.update_detail,
                self.installation_complete
            )
            # 设置对安装页面的引用
            self.download_thread.install_page = self
            # 设置wizard引用
            self.download_thread.wizard = self.wizard()
            # 添加错误处理连接
            self.download_thread.error_occurred.connect(self.handle_error)
            self.download_thread.start()
            
        except Exception as e:
            self.handle_error(str(e))

    def update_status(self, message, progress):
        self.status_label.setText(message)
        self.progress.setValue(progress)

    def update_detail(self, message):
        # upd ui
        self.detail_text.append(message)
        scrollbar = self.detail_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def installation_complete(self):
        self.is_installation_complete = True
        self.installation_in_progress = False
        # enable button
        self.wizard().button(QWizard.NextButton).setEnabled(True)
        self.wizard().button(QWizard.BackButton).setEnabled(True)
        self.wizard().button(QWizard.CancelButton).setEnabled(True)
        self.update_detail("安装完成!")
        QTimer.singleShot(500, self.wizard().next)

    def update_dots(self):
        self.dot_count = (self.dot_count + 1) % 4
        dots = "." * self.dot_count
        self.animation_label.setText(f"感谢使用{dots}")
        
    def cleanupPage(self):
        # 防止在安装过程中返回
        if self.installation_in_progress:
            return
        if hasattr(self, 'movie'):
            self.movie.stop()
        if hasattr(self, 'dot_timer'):
            self.dot_timer.stop()
        super().cleanupPage()

    def handle_cancel(self):
        """处理取消安装操作"""
        if self.installation_in_progress and not self.is_cleaning:
            reply = QMessageBox.question(
                self,
                "确认取消",
                "确定要取消安装吗？\n这将删除所有已安装的文件。",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.is_cancelling = True
                self.is_cleaning = True
                
                # 禁用所有按钮
                wizard = self.wizard()
                wizard.button(QWizard.CancelButton).setEnabled(False)
                wizard.button(QWizard.BackButton).setEnabled(False)
                wizard.button(QWizard.NextButton).setEnabled(False)
                
                # 更新UI显示
                self.progress.setValue(0)
                self.status_label.setText("正在清理安装文件...")
                self.detail_text.append("\n开始清理安装文件...")
                
                # 停止下载线程
                if self.download_thread and self.download_thread.isRunning():
                    self.download_thread.terminate()
                    self.download_thread.wait()
                
                # 清理安装文件
                self.cleanup_installation()
                
                # 清理完成后启用回按钮
                wizard.button(QWizard.BackButton).setEnabled(True)
                wizard.button(QWizard.CancelButton).setEnabled(True)
                
                # 重置状态
                self.installation_in_progress = False
                self.is_cleaning = False
                
                # 返回上一页
                wizard.back()
            else:
                # 如果用户选择不取消，则阻止关闭向导
                return True
                
        # 默认允许关闭
        return False
    
    def cleanup_installation(self):
        """清理已安装的文件"""
        install_path = self.wizard().field("install_path")
        try:
            if os.path.exists(install_path):
                self.detail_text.append(f"正在删除目录: {install_path}")
                shutil.rmtree(install_path, ignore_errors=True)
                self.detail_text.append("✓ 安装目录已清理")
            
            # 清理临时文件
            temp_files = [
                os.path.join(tempfile.gettempdir(), "TsukiNotes.zip"),
                os.path.join(tempfile.gettempdir(), "loading_tn_install.gif"),
                os.path.join(tempfile.gettempdir(), "loading_installer.gif")
            ]
            
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    self.detail_text.append(f"✓ 已删除临时文件: {temp_file}")
            
            self.detail_text.append("清理完成")
            
        except Exception as e:
            self.detail_text.append(f"清理过程中出错: {str(e)}")

class DownloadThread(QThread):
    status_updated = pyqtSignal(str, int)
    detail_updated = pyqtSignal(str)
    installation_completed = pyqtSignal()
    error_occurred = pyqtSignal(str)
    progress_updated = pyqtSignal(int, str)

    def __init__(self, install_path, status_callback, detail_callback, complete_callback):
        super().__init__()
        self.install_path = install_path
        self.status_updated.connect(status_callback, Qt.QueuedConnection)
        self.detail_updated.connect(detail_callback, Qt.QueuedConnection)
        self.installation_completed.connect(complete_callback, Qt.QueuedConnection)
        self.install_page = None
        self.wizard = None
        self._is_cancelled = False
        self._current_operation = ""

    def update_detail(self, message):
        """更新详细信息"""
        self.detail_updated.emit(message)

    def update_status(self, message, progress):
        """更新状态"""
        self.status_updated.emit(message, progress)

    def update_progress(self, progress, message):
        """更新进度"""
        self.progress_updated.emit(progress, message)
        self.update_status(message, progress)
        self.update_detail(message)

    def cancel(self):
        """取消安装"""
        self._is_cancelled = True

    def cleanup_on_error(self):
        """安装失败时清理"""
        try:
            if os.path.exists(self.install_path):
                shutil.rmtree(self.install_path, ignore_errors=True)
            self.update_detail("✓ 已清理安装文件")
        except:
            pass

    def check_existing_installation(self):
        """检查是否存在旧版本安装"""
        try:
            # 检查是否存在版本文件夹
            old_version_folder = None
            for item in os.listdir(self.install_path):
                if item.startswith("TsukiNotesVer") and item.endswith("Windows"):
                    old_version_folder = item
                    break

            if old_version_folder:
                self.update_detail(f"检测到旧版本: {old_version_folder}")
                old_version_path = os.path.join(self.install_path, old_version_folder)
                
                # 检查是否有正在运行的实
                exe_name = "TsukiNotes.exe"
                if self.is_process_running(exe_name):
                    raise Exception("检测到TsukiNotes正在运行，请关闭后再继续")

                # 删除旧版本
                self.update_detail("正在删除旧版本...")
                shutil.rmtree(old_version_path)
                self.update_detail("✓ 已删除旧版本")

                # 删除旧的快捷方式
                self.cleanup_old_shortcuts()
                return True
            return False

        except Exception as e:
            raise Exception(f"检查旧版本时出错: {str(e)}")

    def is_process_running(self, process_name):
        """检查进程是否在运行"""
        import psutil
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'].lower() == process_name.lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    def cleanup_old_shortcuts(self):
        """清理旧的快捷方式"""
        try:
            # 清理桌面快捷方式
            desktop_shortcut = os.path.join(os.path.expanduser("~"), "Desktop", "TsukiNotes.lnk")
            if os.path.exists(desktop_shortcut):
                os.remove(desktop_shortcut)
                self.update_detail("✓ 已删除桌面快捷方式")

            # 清理开始菜单快捷方式
            start_menu_shortcut = os.path.join(os.environ["APPDATA"], 
                                             "Microsoft", "Windows", "Start Menu", "Programs",
                                             "TsukiNotes.lnk")
            if os.path.exists(start_menu_shortcut):
                os.remove(start_menu_shortcut)
                self.update_detail("✓ 已删除开始菜单快捷方式")

            # 清理安装目录的快捷方式
            install_shortcut = os.path.join(self.install_path, "TsukiNotes.lnk")
            if os.path.exists(install_shortcut):
                os.remove(install_shortcut)
                self.update_detail("✓ 已删除安装目录快捷方式")

        except Exception as e:
            self.update_detail(f"清理快捷方式时出现警告: {str(e)}")

    def run(self):
        try:
            if self._is_cancelled:
                return

            # 检查并清理旧版本
            self._current_operation = "检查旧版本"
            self.update_progress(5, "检查已安装的版本...")
            has_old_version = self.check_existing_installation()
            if has_old_version:
                self.update_detail("✓ 旧版本清理完成")

            # 创建安装目录
            self._current_operation = "创建目录"
            self.update_progress(10, "创建安装目录...")
            if not os.path.exists(self.install_path):
                os.makedirs(self.install_path)
            self.update_detail("✓ 目录创建成功")

            # 检查版本
            self._current_operation = "检查版本"
            self.update_progress(20, "检查最新版本...")
            latest_version = self.get_latest_version()
            self.update_detail(f"✓ 最新版本: {latest_version}")

            # 下载文件
            self._current_operation = "下载文件"
            self.update_progress(30, "准备下载...")
            self.download_package(latest_version)

            # 解压文件
            self._current_operation = "解压文件"
            self.update_progress(50, "解压文件...")
            self.extract_files()

            # 创建快捷方式
            if self.wizard and self.wizard.field("create_shortcut"):
                self._current_operation = "创建快捷方式"
                self.update_progress(70, "创建快捷方式...")
                self.create_shortcuts()

            # 添加到PATH
            if self.wizard and self.wizard.field("add_to_path"):
                self._current_operation = "添加PATH"
                self.update_progress(80, "添加到系统PATH...")
                self.add_to_path()

            # 文件关联
            if self.wizard and (self.wizard.field("associate_txt") or 
                              self.wizard.field("associate_log") or 
                              self.wizard.field("associate_tsuki")):
                self._current_operation = "文件关联"
                self.update_progress(90, "创建文件关联...")
                self.create_file_associations()

            # 添加右键菜单
            if self.wizard and self.wizard.field("add_context_menu"):
                self._current_operation = "添加右键菜单"
                self.update_progress(95, "添加右键菜单...")
                self.add_context_menu()

            self.update_progress(100, "安装完成!")
            self.installation_completed.emit()

        except Exception as e:
            if not self._is_cancelled:
                error_msg = f"安装失败: 在{self._current_operation}时发生错误: {str(e)}"
                self.error_occurred.emit(error_msg)
                self.cleanup_on_error()

    def get_latest_version(self):
        """获取新版本号"""
        try:
            version_url = "http://zzbuaoye.us.kg/TsukiNotes/version.txt"
            response = requests.get(version_url, timeout=10)
            response.raise_for_status()

            for line in response.text.splitlines():
                if line.startswith("version:"):
                    return line.split(":")[1].strip()
            raise ValueError("无法解析版本信息")
        except Exception as e:
            raise Exception(f"获取版本信息失败: {str(e)}")

    def download_package(self, version):
        """下载安装包"""
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        download_url = (
            f"https://github.com/buaoyezz/TsukiNotes/releases/download/"
            f"TsukiNotesV{version}/"
            f"TsukiNotesVer{version}.Release_x64_Windows.zip"
        )
        temp_zip = os.path.join(tempfile.gettempdir(), "TsukiNotes.zip")

        try:
            response = requests.get(download_url, stream=True, headers=headers, timeout=30)
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))

            if total_size < 1000000:  # 文件太小
                raise ValueError("下载文件大小异常")

            self.update_detail(f"下载大小: {total_size/(1024*1024):.1f} MB")
            
            block_size = 8192
            downloaded = 0
            
            with open(temp_zip, 'wb') as f:
                start_time = time.time()
                for chunk in response.iter_content(block_size):
                    if self._is_cancelled:
                        return
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        progress = int(30 + (downloaded / total_size) * 20)
                        elapsed_time = time.time() - start_time
                        speed = downloaded / (1024 * 1024 * elapsed_time) if elapsed_time > 0 else 0
                        
                        status_msg = f"下载中... {downloaded/(1024*1024):.1f}MB/{total_size/(1024*1024):.1f}MB"
                        detail_msg = f"{status_msg} ({speed:.1f}MB/s)"
                        
                        self.update_progress(progress, status_msg)
                        self.update_detail(detail_msg)

            if os.path.getsize(temp_zip) != total_size:
                raise ValueError("下载文件不完整")

            self.update_detail("✓ 下载完成")

        except Exception as e:
            if os.path.exists(temp_zip):
                os.remove(temp_zip)
            raise Exception(f"下载失败: {str(e)}")

    def extract_files(self):
        """解压文件"""
        temp_zip = os.path.join(tempfile.gettempdir(), "TsukiNotes.zip")
        try:
            with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
                total_files = len(zip_ref.namelist())
                extracted_files = 0
                
                # 首先解压主程序文件
                for file in zip_ref.namelist():
                    if self._is_cancelled:
                        return
                        
                    # 解压文件
                    zip_ref.extract(file, self.install_path)
                    extracted_files += 1
                    
                    # 更新进度
                    progress = int(50 + (extracted_files / total_files) * 20)
                    status_msg = f"解压中... {extracted_files}/{total_files} 个文件"
                    self.update_progress(progress, status_msg)
                    self.update_detail(f"正在解压: {file}")
                    
                    # 如果是ui目录下的文件，确保目录存在
                    if 'tsuki/ui/' in file:
                        ui_dir = os.path.join(self.install_path, 'tsuki', 'ui')
                        if not os.path.exists(ui_dir):
                            os.makedirs(ui_dir, exist_ok=True)
                        self.update_detail(f"✓ 已创建UI目录: {ui_dir}")
                
                # 检查并创建__pycache__目录
                pycache_dir = os.path.join(self.install_path, 'tsuki', 'ui', '__pycache__')
                if not os.path.exists(pycache_dir):
                    os.makedirs(pycache_dir, exist_ok=True)
                    self.update_detail(f"✓ 已创建缓存目录: {pycache_dir}")

            self.update_detail("✓ 解压完成")
            os.remove(temp_zip)

        except Exception as e:
            raise Exception(f"解压失败: {str(e)}")

    def create_shortcuts(self):
        """创建快捷方式"""
        try:
            shell = win32com.client.Dispatch("WScript.Shell")
            
            # 获取实际的exe路径
            version_folder = next(f for f in os.listdir(self.install_path) 
                                if f.startswith("TsukiNotesVer") and f.endswith("Windows"))
            exe_path = os.path.join(self.install_path, version_folder, "TsukiNotes.exe")
            working_dir = os.path.join(self.install_path, version_folder)
            
            if not os.path.exists(exe_path):
                raise FileNotFoundError(f"找不到程序文件: {exe_path}")
            
            # 在安装目录创建主快捷方式
            main_shortcut_path = os.path.join(self.install_path, "TsukiNotes.lnk")
            main_shortcut = shell.CreateShortCut(main_shortcut_path)
            main_shortcut.Targetpath = exe_path
            main_shortcut.WorkingDirectory = working_dir
            main_shortcut.IconLocation = exe_path
            main_shortcut.save()
            self.update_detail("✓ 已在安装目录创建快捷方��")
            
            # 复制到桌面
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            desktop_shortcut = os.path.join(desktop, "TsukiNotes.lnk")
            shutil.copy2(main_shortcut_path, desktop_shortcut)
            self.update_detail("✓ 已复制快捷方式到桌面")
            
            # 复制到开始菜单
            start_menu = os.path.join(os.environ["APPDATA"], 
                                    "Microsoft", "Windows", "Start Menu", "Programs")
            start_menu_shortcut = os.path.join(start_menu, "TsukiNotes.lnk")
            shutil.copy2(main_shortcut_path, start_menu_shortcut)
            self.update_detail("✓ 已复制快捷方式到开始菜单")

        except Exception as e:
            raise Exception(f"创建快捷方式失败: {str(e)}")

    def add_to_path(self):
        """添加到系统PATH"""
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                               r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
                               0, winreg.KEY_ALL_ACCESS)

            path_value, _ = winreg.QueryValueEx(key, "Path")
            if self.install_path not in path_value:
                new_path = path_value + ";" + self.install_path
                winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
                self.update_detail("✓ 已添加到系统PATH")

            winreg.CloseKey(key)

        except Exception as e:
            raise Exception(f"添加到系统PATH失败: {str(e)}")

    def create_file_associations(self):
        """创建文件关联"""
        try:
            extensions = []
            if self.wizard.field("associate_txt"):
                extensions.append((".txt", "文本文件"))
            if self.wizard.field("associate_log"):
                extensions.append((".log", "日志文件"))
            if self.wizard.field("associate_tsuki"):
                extensions.append((".tsuki", "TsukiNotes笔记"))

            for ext, desc in extensions:
                # 创建文件类型注册表项
                with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, ext) as key:
                    winreg.SetValue(key, "", winreg.REG_SZ, f"TsukiNotes{ext}")

                with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, f"TsukiNotes{ext}") as key:
                    winreg.SetValue(key, "", winreg.REG_SZ, desc)
                    # 设置图标
                    with winreg.CreateKey(key, "DefaultIcon") as icon_key:
                        winreg.SetValue(icon_key, "", winreg.REG_SZ, 
                                      f'"{os.path.join(self.install_path, "TsukiNotes.exe")}"')
                    # 设置打开命令
                    with winreg.CreateKey(key, "shell\\open\\command") as cmd_key:
                        winreg.SetValue(cmd_key, "", winreg.REG_SZ,
                                      f'"{os.path.join(self.install_path, "TsukiNotes.exe")}" "%1"')

                self.update_detail(f"✓ 已关联 {ext} 文件")

            # 刷新系统图标缓存
            os.system("ie4uinit.exe -show")

        except Exception as e:
            raise Exception(f"创建文件关联失败: {str(e)}")

    def add_context_menu(self):
        """添加右键菜单"""
        try:
            with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, "*\\shell\\TsukiNotes") as key:
                winreg.SetValue(key, "", winreg.REG_SZ, "用TsukiNotes打开")
                winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, 
                                os.path.join(self.install_path, "TsukiNotes.exe"))
                with winreg.CreateKey(key, "command") as cmd_key:
                    winreg.SetValue(cmd_key, "", winreg.REG_SZ,
                                  f'"{os.path.join(self.install_path, "TsukiNotes.exe")}" "%1"')
            self.update_detail("✓ 已添加右键菜单")

        except Exception as e:
            raise Exception(f"添加右键菜单失败: {str(e)}")

class FinalOptionsPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("附加选项")
        self.setSubTitle("请选择需要的附加功能，您可以点击*返回*按钮查看安装日志")
        
        layout = QVBoxLayout()
        
        # 基本选项组
        options_group = QGroupBox("基本选项")
        options_layout = QVBoxLayout()
        
        self.shortcut_cb = QCheckBox("创建桌面快捷方式")
        self.path_cb = QCheckBox("添加到系统PATH")
        self.context_menu_cb = QCheckBox("添加到右键菜单")

        self.shortcut_cb.setChecked(True)
        
        self.path_cb.setToolTip("将程序添加到系统环境变量，需要管理员权限")
        self.context_menu_cb.setToolTip("在右键菜单添加*用TsukiNotes打开*选项")
        
        options_layout.addWidget(self.shortcut_cb)
        options_layout.addWidget(self.path_cb)
        options_layout.addWidget(self.context_menu_cb)
        
        options_group.setLayout(options_layout)
        
        # 文件关联组
        association_group = QGroupBox("文件关联")
        association_layout = QVBoxLayout()
        
        self.txt_cb = QCheckBox(".txt 文本文件")
        self.log_cb = QCheckBox(".log 日志文件")
        self.tsuki_cb = QCheckBox(".tsuki 笔记文件")
        
        self.tsuki_cb.setChecked(True)
        
        association_layout.addWidget(self.txt_cb)
        association_layout.addWidget(self.log_cb)
        association_layout.addWidget(self.tsuki_cb)
        
        association_group.setLayout(association_layout)
        
        # 提示信息
        tip_label = QLabel(
            "<p style='color: #666; font-size: 11px;'>"
            "提示：您可以点击*返回*按钮查看安装日志，"
            "查看完成后再次点击*下一步*继续安装。</p>"
        )
        tip_label.setWordWrap(True)
        
        layout.addWidget(options_group)
        layout.addWidget(association_group)
        layout.addWidget(tip_label)
        layout.addStretch()
        
        self.setLayout(layout)
        
        # 注册字段
        self.registerField("create_shortcut", self.shortcut_cb)
        self.registerField("add_to_path", self.path_cb)
        self.registerField("add_context_menu", self.context_menu_cb)
        self.registerField("associate_txt", self.txt_cb)
        self.registerField("associate_log", self.log_cb)
        self.registerField("associate_tsuki", self.tsuki_cb)
        
        # 保存选项状态
        self._saved_states = {}
        
    def initializePage(self):
        """初始化页面时恢复保存的选项状态"""
        if self._saved_states:
            self.shortcut_cb.setChecked(self._saved_states.get("create_shortcut", True))
            self.path_cb.setChecked(self._saved_states.get("add_to_path", False))
            self.context_menu_cb.setChecked(self._saved_states.get("add_context_menu", False))
            self.txt_cb.setChecked(self._saved_states.get("associate_txt", False))
            self.log_cb.setChecked(self._saved_states.get("associate_log", False))
            self.tsuki_cb.setChecked(self._saved_states.get("associate_tsuki", True))
            
    def cleanupPage(self):
        """离开页面时保存选项状态"""
        self._saved_states = {
            "create_shortcut": self.shortcut_cb.isChecked(),
            "add_to_path": self.path_cb.isChecked(),
            "add_context_menu": self.context_menu_cb.isChecked(),
            "associate_txt": self.txt_cb.isChecked(),
            "associate_log": self.log_cb.isChecked(),
            "associate_tsuki": self.tsuki_cb.isChecked()
        }
        super().cleanupPage()

class CompletePage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("安装完成")
        self.setSubTitle("TsukiNotes 已成功安装到您的计算机")
        
        layout = QVBoxLayout()
        
        # 完成图标
        complete_label = QLabel()
        complete_url = "https://img.picui.cn/free/2024/10/26/671ccb6079547.png"
        try:
            response = requests.get(complete_url)
            if response.status_code == 200:
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)
                complete_label.setPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio))
        except:
            complete_label.setText("✓")
            complete_label.setStyleSheet("font-size: 48px; color: #4CAF50;")
            
        layout.addWidget(complete_label, alignment=Qt.AlignCenter)
        
        # 完成文本
        complete_text = QLabel(
            "<h3>安装已完成！</h3>"
            "<p>您可以在开始菜单或桌面找到 TsukiNotes 的快捷方式。</p>"
            "<p>感谢使用 TsukiNotes！如果喜欢这个项目，请别忘了给我一个 Star！</p>"
            "<p><a href='https://github.com/buaoyezz/TsukiNotes'>访问 GitHub 项目页面</a></p>"
        )
        complete_text.setOpenExternalLinks(True)
        complete_text.setWordWrap(True)
        complete_text.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #333;
                line-height: 1.6;
            }
            QLabel a {
                color: #0366d6;
                text-decoration: none;
            }
            QLabel a:hover {
                text-decoration: underline;
            }
        """)
        layout.addWidget(complete_text)
        
        # 启动选项
        self.launch_cb = QCheckBox("立即启动 TsukiNotes")
        self.launch_cb.setChecked(True)
        layout.addWidget(self.launch_cb)
        
        layout.addStretch()
        self.setLayout(layout)
        
    def validatePage(self):
        if self.launch_cb.isChecked():
            install_path = self.wizard().field("install_path")
            try:
                # 查找实际的exe路径
                version_folder = next(f for f in os.listdir(install_path) 
                                   if f.startswith("TsukiNotesVer") and f.endswith("Windows"))
                program = os.path.join(install_path, version_folder, "TsukiNotes.exe")
                
                if not os.path.exists(program):
                    raise FileNotFoundError("找不到程序文件")
                    
                # 使用subprocess启动程序
                import subprocess
                subprocess.Popen([program], 
                               creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
                               cwd=os.path.dirname(program))  # 设置工作目录
                
                return True
                
            except Exception as e:
                QMessageBox.warning(self, "启动失败", 
                    f"无法启动 TsukiNotes: {str(e)}\n"
                    "请手动启动程序。")
        return True

def main():
    # 在创建 QApplication 之前设置高DPI属性
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # 创建应用程序实例
    app = QApplication(sys.argv)
    
    # 设置样式表
    app.setStyle('Fusion')
    
    # 创建启动等待对话框
    splash_dialog = QDialog()
    splash_dialog.setWindowTitle("TsukiNotes Installer | Launching...")
    splash_dialog.setFixedSize(300, 150)
    splash_dialog.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
    
    layout = QVBoxLayout()
    
    # Logo
    logo_label = QLabel()
    logo_url = "https://img.picui.cn/free/2024/10/26/671ca15ba4d46.png"
    try:
        response = requests.get(logo_url)
        if response.status_code == 200:
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            logo_label.setPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio))
    except:
        pass
    layout.addWidget(logo_label, alignment=Qt.AlignCenter)
    
    # 加载动画
    loading_label = QLabel()
    movie = QMovie()
    try:
        loading_url = "https://ooo.0x0.ooo/2024/10/26/ODXJuB.gif"
        response = requests.get(loading_url)
        if response.status_code == 200:
            temp_gif = os.path.join(tempfile.gettempdir(), "loading_installer.gif")
            with open(temp_gif, 'wb') as f:
                f.write(response.content)
            movie.setFileName(temp_gif)
    except:
        pass
    loading_label.setMovie(movie)
    movie.start()
    layout.addWidget(loading_label, alignment=Qt.AlignCenter)
    
    loading_text = QLabel("Please wait...\nLaunching TsukiNotes Wizard")
    loading_text.setFont(QFont("Microsoft YaHei"))
    loading_text.setAlignment(Qt.AlignCenter)
    loading_text.setStyleSheet("font-size: 12px; color: #666;")
    layout.addWidget(loading_text)
    
    splash_dialog.setLayout(layout)
    splash_dialog.show()
    

    wizard = InstallerWizard()
    
    def show_main_window():
        wizard.show()
        splash_dialog.close()  
    
    QTimer.singleShot(1500, show_main_window)
    QApplication.processEvents()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()