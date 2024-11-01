#====================================================================
# Powered by ZZBuAoYe
# Github: https://github.com/buaoyezz
# TsukiNotes Build Date: 2024/11/01
# Install Version: 0.0.1.19000
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
        self.setWindowTitle("TsukiNotes 安装向导 | 安装器版本0.0.1.19000 | VERSION 1.5.9")
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
            "<p>此安装器属于Ver1.5.9专属在线安装包"
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
        如果您违反本协议的任何条款，本软件不会提供任何技术支持
        
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


from PyQt5.QtCore import (QThread, pyqtSignal, pyqtSlot, QMetaObject,
                         Qt, Q_ARG)

class InstallProgressPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("正在安装")
        self.setSubTitle("请等待安装完成...")
        
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
        self.detail_text.setFixedHeight(150)
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
        
        # add move
        self.animation_label = QLabel()
        self.movie = QMovie()
        self.movie.setFileName("loading_tn_install.gif")
        try:
            loading_url = "https://ooo.0x0.ooo/2024/10/26/ODXJuB.gif"
            response = requests.get(loading_url)
            if response.status_code == 200:
                temp_gif = os.path.join(tempfile.gettempdir(), "loading_tn_install.gif")
                with open(temp_gif, 'wb') as f:
                    f.write(response.content)
                self.movie.setFileName(temp_gif)
        except:
            self.dot_count = 0
            self.dot_timer = QTimer()
            self.dot_timer.timeout.connect(self.update_dots)
            self.dot_timer.start(500)
            
        self.animation_label.setMovie(self.movie)
        self.movie.start()
        self.animation_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.animation_label)
        
        layout.addStretch()
        self.setLayout(layout)
        
        # c thread
        self.download_thread = None
        self.is_installation_complete = False
        
        # mark
        self.installation_in_progress = False

    def isComplete(self):
        return self.is_installation_complete

    def initializePage(self):
        self.installation_in_progress = True
        self.is_installation_complete = False
        
        # disable button .all
        wizard = self.wizard()
        wizard.button(QWizard.NextButton).setEnabled(False)
        wizard.button(QWizard.BackButton).setEnabled(False)
        wizard.button(QWizard.CancelButton).setEnabled(False)
        
        # start 
        QTimer.singleShot(0, self.perform_installation)

    def perform_installation(self):
        install_path = self.wizard().field("install_path")
        backup_dir = Path('./backup')
        
        try:
            # c thread
            self.download_thread = DownloadThread(
                self.wizard().field("install_path"),
                self.update_status,
                self.update_detail,
                self.installation_complete
            )
            # 设置wizard引用
            self.download_thread.wizard = self.wizard()
            # 添加错误处理连接
            self.download_thread.error_occurred.connect(self.handle_error)
            self.download_thread.start()
            
        except Exception as e:
            self.handle_error(str(e))

    def handle_error(self, error_message):
        """处理安装过程中的错误"""
        self.installation_in_progress = False
        QMessageBox.critical(self, "安装错误", f"安装过程中发生错误:\n{error_message}")
        self.wizard().back()

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
        # anti back
        if self.installation_in_progress:
            return
        if hasattr(self, 'movie'):
            self.movie.stop()
        if hasattr(self, 'dot_timer'):
            self.dot_timer.stop()
        super().cleanupPage()

class DownloadThread(QThread):
    status_updated = pyqtSignal(str, int)
    detail_updated = pyqtSignal(str)
    installation_completed = pyqtSignal()
    error_occurred = pyqtSignal(str)  # add error signal

    def __init__(self, install_path, status_callback, detail_callback, complete_callback):
        super().__init__()
        self.install_path = install_path
        
        # back
        self.status_updated.connect(status_callback, Qt.QueuedConnection)
        self.detail_updated.connect(detail_callback, Qt.QueuedConnection)
        self.installation_completed.connect(complete_callback, Qt.QueuedConnection)
        
        self.wizard = None
    def run(self):
        try:
            # create path
            self.update_status("Creating directory...", 10)
            self.update_detail("Creating installation directory...")
            os.makedirs(self.install_path, exist_ok=True)
            self.update_detail("Directory created successfully ✓")
            
            # download
            self.update_status("Downloading...", 30)
            self.update_detail("\nInitiating download...")
            
            latest_version = "1.5.9"
            download_url = (
                f"https://github.com/buaoyezz/TsukiNotes/releases/download/"
                f"TsukiNotesV{latest_version}/"
                f"TsukiNotesVer{latest_version}.Release_x64_Windows.zip"
            )
            
            # Thread
            temp_zip = os.path.join(tempfile.gettempdir(), "TsukiNotes.zip")
            self.download_with_progress(download_url, temp_zip)
            
            # unpack
            self.update_status("UnPacking...", 50)
            self.update_detail("\nExtracting files...")
            
            with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
                total_files = len(zip_ref.namelist())
                for index, file in enumerate(zip_ref.namelist()):
                    zip_ref.extract(file, self.install_path)
                    progress = int(50 + (index / total_files) * 20)
                    self.update_status(f"Unpacking... {index + 1}/{total_files} Files", progress)
                    self.update_detail(f"Unpacking... {file} [{index + 1}/{total_files}]")
            
            self.update_detail("Extraction completed ✓")
            
            # remove the temp
            os.remove(temp_zip)
            
            # create shortcuts
            if self.wizard and self.wizard.field("create_shortcut"):
                self.update_status("创建快捷方式...", 70)
                self.update_detail("\nCreating shortcuts...")
                self.create_shortcuts()
                self.update_detail("Shortcuts created successfully ✓")
            
            # add path
            if self.wizard and self.wizard.field("add_to_path"):
                self.update_status("添加到系统PATH...", 80)
                self.update_detail("\nAdding to system PATH...")
                self.add_to_path()
                self.update_detail("Added to PATH successfully ✓")
            
            # cfa
            if self.wizard and (self.wizard.field("associate_txt") or 
                              self.wizard.field("associate_log") or 
                              self.wizard.field("associate_tsuki")):
                self.update_status("创建文件关联...", 90)
                self.update_detail("\nCreating file associations...")
                self.create_file_associations()
                self.update_detail("File associations created successfully ✓")
            # youjian caidan
            if self.wizard and self.wizard.field("add_context_menu"):
                self.update_status("添加右键菜单...", 95)
                self.update_detail("\nAdding context menu...")
                self.add_context_menu()
                self.update_detail("Context menu added successfully ✓")
            
            self.update_status("安装完成!", 100)
            self.update_detail("\nInstallation completed successfully! ✓")
            self.update_detail("Thank you for using TsukiNotes!\n")
            self.installation_complete()
            
        except Exception as e:
            self.update_detail(f"\nError: {str(e)}")
            self.error_occurred.emit(str(e))  # send error signal
            return

    def update_status(self, message, progress):
        self.status_updated.emit(message, progress)

    def update_detail(self, message):
        self.detail_updated.emit(message)

    def installation_complete(self):
        self.installation_completed.emit()

    def download_with_progress(self, url, dest_path):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                response = requests.get(url, stream=True, headers=headers, timeout=30)
                response.raise_for_status()
                total_size = int(response.headers.get('content-length', 0))
                
                if total_size < 1000000:  # file too small
                    raise ValueError("下载文件大小异常")
                
                self.update_detail(f"Total size: {total_size/(1024*1024):.1f} MB")
                
                block_size = 8192
                downloaded = 0
                
                with open(dest_path, 'wb') as f:
                    start_time = time.time()
                    for chunk in response.iter_content(block_size):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            progress = int(30 + (downloaded / total_size) * 20)
                            elapsed_time = time.time() - start_time
                            speed = downloaded / (1024 * 1024 * elapsed_time) if elapsed_time > 0 else 0
                            
                            self.update_status(
                                f"下载中... {downloaded/(1024*1024):.1f}MB/{total_size/(1024*1024):.1f}MB",
                                progress
                            )
                            self.update_detail(
                                f"Downloading... {downloaded/(1024*1024):.1f}MB/{total_size/(1024*1024):.1f}MB "
                                f"({speed:.1f}MB/s)"
                            )
                
                # 验证下载完整性
                if os.path.getsize(dest_path) != total_size:
                    raise ValueError("下载文件不完整")
                    
                self.update_detail("Download completed ✓")
                break
                
            except Exception as e:
                retry_count += 1
                if retry_count == max_retries:
                    self.error_occurred.emit(f"下载失败: {str(e)}")  # 发送错误信号
                    return
                self.update_detail(f"\nRetrying download... ({retry_count}/{max_retries})")
                time.sleep(2)

    def create_shortcuts(self):
        try:
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            
            # 创建桌面快捷方式
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(os.path.join(desktop, "TsukiNotes.lnk"))
            shortcut.Targetpath = os.path.join(self.install_path, "TsukiNotes.exe")
            shortcut.WorkingDirectory = self.install_path
            shortcut.IconLocation = os.path.join(self.install_path, "TsukiNotes.exe")
            shortcut.save()
            self.update_detail("Desktop shortcut created")
            
            start_menu = os.path.join(os.environ["APPDATA"], 
                                    "Microsoft", "Windows", "Start Menu", "Programs")
            start_menu_shortcut = shell.CreateShortCut(
                os.path.join(start_menu, "TsukiNotes.lnk"))
            start_menu_shortcut.Targetpath = os.path.join(self.install_path, "TsukiNotes.exe")
            start_menu_shortcut.WorkingDirectory = self.install_path
            start_menu_shortcut.IconLocation = os.path.join(self.install_path, "TsukiNotes.exe")
            start_menu_shortcut.save()
            self.update_detail("Start menu shortcut created")
            
        except Exception as e:
            raise Exception(f"创建快捷方式失败: {str(e)}")

    def add_to_path(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                               r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
                               0, winreg.KEY_ALL_ACCESS)
            
            path_value, _ = winreg.QueryValueEx(key, "Path")
            if self.install_path not in path_value:
                new_path = path_value + ";" + self.install_path
                winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
                self.update_detail("Added to system PATH")
            
            winreg.CloseKey(key)
            
        except Exception as e:
            raise Exception(f"添加到系统PATH失败: {str(e)}")

    def create_file_associations(self):
        try:
            extensions = []
            if self.wizard.field("associate_txt"):
                extensions.append(".txt")
            if self.wizard.field("associate_log"):
                extensions.append(".log")
            if self.wizard.field("associate_tsuki"):
                extensions.append(".tsuki")
            
            for ext in extensions:
                with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, ext) as key:
                    winreg.SetValue(key, "", winreg.REG_SZ, "TsukiNotes.Document")
                self.update_detail(f"Associated {ext} files")
            
            if extensions:
                with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, "TsukiNotes.Document") as key:
                    winreg.SetValue(key, "", winreg.REG_SZ, "TsukiNotes文档")
                    with winreg.CreateKey(key, "DefaultIcon") as icon_key:
                        winreg.SetValue(icon_key, "", winreg.REG_SZ, 
                                      f"{os.path.join(self.install_path, 'TsukiNotes.exe')},0")
                    with winreg.CreateKey(key, "shell\\open\\command") as cmd_key:
                        winreg.SetValue(cmd_key, "", winreg.REG_SZ, 
                                      f'"{os.path.join(self.install_path, "TsukiNotes.exe")}" "%1"')
                
        except Exception as e:
            raise Exception(f"创建文件关联失败: {str(e)}")

    def add_context_menu(self):
        try:
            with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, "*\\shell\\TsukiNotes") as key:
                winreg.SetValue(key, "", winreg.REG_SZ, "用TsukiNotes打开")
                winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, 
                                os.path.join(self.install_path, "TsukiNotes.exe"))
                with winreg.CreateKey(key, "command") as cmd_key:
                    winreg.SetValue(cmd_key, "", winreg.REG_SZ,
                                  f'"{os.path.join(self.install_path, "TsukiNotes.exe")}" "%1"')
            self.update_detail("Added context menu integration")
                    
        except Exception as e:
            raise Exception(f"添加右键菜单失败: {str(e)}")

class FinalOptionsPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("附加选项")
        self.setSubTitle("请选择需要的附加功能")
        
        layout = QVBoxLayout()
        
        # 基本选项组
        options_group = QGroupBox("基本选项")
        options_layout = QVBoxLayout()
        
        self.shortcut_cb = QCheckBox("创建桌面快捷方式")
        self.path_cb = QCheckBox("添加到系统PATH")
        self.context_menu_cb = QCheckBox("添加到右键菜单")

        self.shortcut_cb.setChecked(True)
        
        self.path_cb.setToolTip("将程序添加到系统环境变量，需要管理员权限")
        self.context_menu_cb.setToolTip("在右键菜单添加""<用TsukiNotes打开>""选项")
        
        options_layout.addWidget(self.shortcut_cb)
        options_layout.addWidget(self.path_cb)
        options_layout.addWidget(self.context_menu_cb)
        
        options_group.setLayout(options_layout)
        
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
        
        layout.addWidget(options_group)
        layout.addWidget(association_group)
        layout.addStretch()
        
        self.setLayout(layout)
        
        # 注册字段
        self.registerField("create_shortcut", self.shortcut_cb)
        self.registerField("add_to_path", self.path_cb)
        self.registerField("add_context_menu", self.context_menu_cb)
        self.registerField("associate_txt", self.txt_cb)
        self.registerField("associate_log", self.log_cb)
        self.registerField("associate_tsuki", self.tsuki_cb)

class CompletePage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("安装完成")
        self.setSubTitle("TsukiNotes 已成功安装到您的计算机")
        
        layout = QVBoxLayout()
        
        # done icon
        complete_label = QLabel()
        complete_url = "https://img.picui.cn/free/2024/10/26/671ccb6079547.png"  # 替换为实际的图床URL
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
        
        # done text
        complete_text = QLabel(
            "安装已完成！\n\n"
            "您可以在开始菜单或桌面找到 TsukiNotes 的快捷方式\n"
            "感谢使用 TsukiNotes！\n"
            "喜欢项目不要忘记给我Star！！！"
        )
        complete_text.setWordWrap(True)
        complete_text.setStyleSheet("font-size: 12px; color: #666;")
        layout.addWidget(complete_text)
        
        # 启动!
        self.launch_cb = QCheckBox("立即启动 TsukiNotes")
        self.launch_cb.setChecked(True)
        layout.addWidget(self.launch_cb)
        
        layout.addStretch()
        self.setLayout(layout)
        
    def validatePage(self):
        if self.launch_cb.isChecked():
            install_path = self.wizard().field("install_path")
            try:
                os.startfile(os.path.join(install_path, "TsukiNotes.exe"))
            except:
                QMessageBox.warning(self, "启动失败", "无法启动 TsukiNotes")
        return True

def main():
    app = QApplication(sys.argv)
    wizard = InstallerWizard()
    wizard.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
