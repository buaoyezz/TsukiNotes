#==================================
# Install Lite For TsukiNotes
# Lite Version ≠ Wizard
# B1.1.0
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


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        try:
            # 安全方式->管理员权限
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
        if releases:
            latest_release = releases[0]  # 获取最新发布
            tag_name = latest_release.get('tag_name', '')
            if tag_name.startswith('TsukiNotesV'):
                version = tag_name[10:]  # 移除 'TsukiNotesV' 前缀
                # 如果版本号以'V'开头,移除它
                if version.startswith('V'):
                    version = version[1:]
                return version
        return None
    except Exception:
        return None

def get_current_version(install_path):
    version_file = os.path.join(install_path, "VERSION")
    try:
        with open(version_file, 'r', encoding='utf-8') as f:
            version = f.read().strip()
            if version and all(part.isdigit() for part in version.split('.')):
                return version
    except FileNotFoundError:
        logging.error(f"版本文件未找到: {version_file}")
    except Exception as e:
        logging.error(f"读取版本文件时出错: {e}")
    return None

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

class InstallerWizard(QWizard):
    def __init__(self, silent_mode=False):
        super().__init__()
        self.silent_mode = silent_mode
        self.setWindowTitle("TsukiNotes Update Installer")
        self.setWindowIcon(QIcon('tsuki/assets/GUI/resources/GUI/logo.png'))
        self.resize(600, 400)
        
        # 设置按钮文本
        self.setButtonText(QWizard.FinishButton, "结束安装")
        self.setButtonText(QWizard.CancelButton, "取消安装")
        self.setButtonText(QWizard.NextButton, "下一步")
        self.setButtonText(QWizard.BackButton, "上一步")

        
        
        self.install_path = os.getcwd()
        
        # 更新样式表
        self.setStyleSheet("""
            QWizard, QWizardPage {
                background-color: #f0f0f0;
                font-family: "Microsoft YaHei";
            }
            
            QPushButton {
                background-color: #ffffff;
                color: #333333;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: 500;
            }
            
            QPushButton:hover {
                background-color: #f5f5f5;
            }
            
            QPushButton:pressed {
                background-color: #e0e0e0;
            }
            
            QProgressBar {
                border: none;
                background-color: #ffffff;
                border-radius: 10px;
                height: 20px;
                text-align: center;
            }
            
            QProgressBar::chunk {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
                    stop:0 #60CDFF, stop:1 #99E5FF);
                border-radius: 10px;
            }
            
            QLineEdit, QTextEdit {
                padding: 8px;
                background-color: #ffffff;
                border: none;
                border-radius: 8px;
            }
        """)
        
        # 为所有按钮添加阴影效果
        for button in self.findChildren(QPushButton):
            shadow = QGraphicsDropShadowEffect(self)
            shadow.setBlurRadius(15)
            shadow.setXOffset(3)
            shadow.setYOffset(3)
            shadow.setColor(QColor(0, 0, 0, 30))
            button.setGraphicsEffect(shadow)
        
        # 添加窗口渐变动画效果
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(300)
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.start()
        
        self.addPage(InstallProgressPage())
        
        self.setWizardStyle(QWizard.ModernStyle)
        
        QTimer.singleShot(0, self.auto_install)
    
    def auto_install(self):
        self.next()

    def cancel_installation(self):
        temp_path = os.path.join(os.environ["TEMP"], "TsukiNotes.zip")
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass
        QApplication.quit()

    def closeEvent(self, event):
        for page_id in self.pageIds():
            page = self.page(page_id)
            if hasattr(page, 'closeEvent'):
                page.closeEvent(event)
        super().closeEvent(event)

class InstallProgressPage(QWizardPage):
    updateProgress = pyqtSignal(int, str)
    installationComplete = pyqtSignal(bool, str)
    logMessage = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setTitle("TsukiNotes 正在安装")
        self.thread = None
        self.worker = None
        
        layout = QVBoxLayout()
        
        self.progress = QProgressBar()
        self.status_label = QLabel("| 正在准备安装...")
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        
        layout.addWidget(self.progress)
        layout.addWidget(self.status_label)
        layout.addWidget(self.log_text)
        
        self.setLayout(layout)

        self.updateProgress.connect(self.update_progress)
        self.installationComplete.connect(self.handle_installation_complete)
        self.logMessage.connect(self.append_log)
        
        # 为进度条添加阴影效果
        progress_shadow = QGraphicsDropShadowEffect(self)
        progress_shadow.setBlurRadius(10)
        progress_shadow.setXOffset(0)
        progress_shadow.setYOffset(2)
        progress_shadow.setColor(QColor(0, 0, 0, 30))
        self.progress.setGraphicsEffect(progress_shadow)
        
        # 添加进度条动画
        self.progress_animation = QPropertyAnimation(self.progress, b"value")
        self.progress_animation.setDuration(300)
        self.progress_animation.setEasingCurve(QEasingCurve.OutCubic)
    
    def closeEvent(self, event):
        if self.thread and self.thread.isRunning():
            self.worker.stop()
            self.worker.progress.disconnect()
            self.worker.finished.disconnect()
            self.worker.log.disconnect()
            self.thread.quit()
            self.thread.wait()
            self.thread.deleteLater()
            self.worker.deleteLater()
        super().closeEvent(event)

    def __del__(self):
        if self.thread:
            if self.thread.isRunning():
                self.thread.quit()
                self.thread.wait()
            self.thread.deleteLater()
        if self.worker:
            self.worker.deleteLater()

    def initializePage(self):
        QTimer.singleShot(0, self.start_installation_thread)

    def start_installation_thread(self):
        if self.thread and self.thread.isRunning():
            self.worker.stop()
            self.worker.progress.disconnect()
            self.worker.finished.disconnect()
            self.worker.log.disconnect()
            self.thread.quit()
            self.thread.wait()
            self.thread.deleteLater()
            self.worker.deleteLater()
            
        self.thread = QThread()
        self.worker = InstallationWorker(self.wizard().install_path, self.wizard().silent_mode)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.updateProgress.emit)
        self.worker.finished.connect(self.handle_worker_finished)
        self.worker.log.connect(self.logMessage.emit)
        self.thread.start()

    def update_progress(self, value, status):
        # 使用动画更新进度条
        self.progress_animation.setStartValue(self.progress.value())
        self.progress_animation.setEndValue(value)
        self.progress_animation.start()
        
        # 状态文本更新动画
        self.status_label.setText(f"| {status}")
        fade = QGraphicsOpacityEffect(self.status_label)
        self.status_label.setGraphicsEffect(fade)
        
        fade_anim = QPropertyAnimation(fade, b"opacity")
        fade_anim.setDuration(200)
        fade_anim.setStartValue(0)
        fade_anim.setEndValue(1)
        fade_anim.start()

    def handle_worker_finished(self, success, message):
        self.installationComplete.emit(success, message)
        if self.thread:
            self.worker.stop()
            self.worker.progress.disconnect()
            self.worker.finished.disconnect()
            self.worker.log.disconnect()
            self.thread.quit()
            self.thread.wait()
            self.thread.deleteLater()
            self.worker.deleteLater()
            self.thread = None
            self.worker = None

    def handle_installation_complete(self, success, message):
        if success:
            if not self.wizard().silent_mode:
                QMessageBox.information(self, "Finished!", message)
        else:
            if not self.wizard().silent_mode:
                QMessageBox.critical(self, "Error", message)
            else:
                print(message)

    def append_log(self, message):
        self.log_text.append(message)
        self.log_text.verticalScrollBar().setValue(self.log_text.verticalScrollBar().maximum())

class InstallationWorker(QObject):
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(bool, str)
    log = pyqtSignal(str)

    def __init__(self, install_path, silent_mode):
        super().__init__()
        self.install_path = install_path
        self.silent_mode = silent_mode
        self._is_running = False

    def stop(self):
        self._is_running = False

    def run(self):
        self._is_running = True
        log_file = os.path.join(self.install_path, "tsuki_update.log")
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='[%(asctime)s | %(levelname)s]%(message)s',
            datefmt='%Y/%m/%d %H:%M:%S',
            encoding='utf-8'
        )
        
        try:
            if not self._is_running:
                self.finished.emit(False, "Installation cancelled")
                return
            self.log.emit("开始更新检查...")
            logging.debug("Welcome To TsukiNotes Update Installer")
            logging.debug("===============================================")
            logging.debug("The Install Tool Version: 1.1.0")
            logging.debug("SoftWare Initializing...")
            logging.debug("SoftWare By ZZBuAoYe")
            logging.debug("Enjoy TsukiNotes!")
            logging.debug("================================================")
            logging.info("Starting update check")
            self.progress.emit(10, "检查最新版本...")
            
            current_version = get_current_version(self.install_path)
            self.log.emit(f"当前版本: {current_version or '未安装'}")
            logging.info(f"Current version: {current_version or '未安装'}")
            
            latest_version = check_version()
            if not latest_version:
                raise Exception("无法获取最新版本信息")
            self.log.emit(f"最新版本: {latest_version}")
            logging.info(f"Latest version: {latest_version}")
            
            if not compare_versions(current_version, latest_version):
                self.log.emit("已是最新版本，无需更新")
                logging.info("Your Are The Latest Version! No Need To Update")
                self.progress.emit(100, "已是最新版本!")
                self.finished.emit(True, "当前已是最新版本，无需更新!")
                return
                
            self.log.emit("发现新版本，开始更新")
            logging.info("Find New Version, Start Update....")
            self.progress.emit(30, "下载更新包...")
            self.download_package(latest_version)
            self.log.emit("下载完成")
            logging.info("Download Completed √")
            
            self.progress.emit(60, "解压并覆盖文件...")
            self.extract_and_overwrite_files(self.install_path)
            self.log.emit("文件覆盖完成")
            logging.info("Files Overwrite Completed √")
            
            desktop_shortcut = os.path.join(os.path.expanduser("~"), "Desktop", "TsukiNotes.lnk")
            if os.path.exists(desktop_shortcut):
                self.progress.emit(80, "更新快捷方式...")
                try:
                    self.update_shortcuts(self.install_path)
                    self.log.emit("快捷方式更新完成")
                    logging.info("Lnk Shortcut Update Completed √")
                except Exception as shortcut_error:
                    self.log.emit(f"快捷方式更新失败（非致命错误）: {str(shortcut_error)}")
                    logging.warning(f"Lnk Shortcut Update Failed(Non-Critical Error): {str(shortcut_error)}")
            
            self.progress.emit(100, "安装完成!")
            self.log.emit("安装完成")
            logging.info("Installation Completed √")
            logging.info("ALL Done")
            
            self.finished.emit(True, "TsukiNotes 已成功更新!")
            
        except Exception as e:
            if self._is_running:
                self.log.emit(f"Update Failed: {str(e)}")
                logging.error(f"Update Failed: {str(e)}")
                self.finished.emit(False, f"Update Failed: {str(e)}")

    def download_package(self, version):
        try:
            # 清除上次的日志文件
            log_file = os.path.join(self.install_path, "tsuki_update.log")
            if os.path.exists(log_file):
                try:
                    os.remove(log_file)
                except:
                    pass
                
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/octet-stream'
            }
            
            download_urls = [
                (f"https://github.com/buaoyezz/TsukiNotes/releases/download/"
                 f"TsukiNotesV{version}/"
                 f"TsukiNotesVer{version}.Release_x64_Windows.zip"),
                (f"https://kkgithub.com/buaoyezz/TsukiNotes/releases/download/"
                 f"TsukiNotesV{version}/"
                 f"TsukiNotesVer{version}.Release_x64_Windows.zip")
            ]

            temp_path = os.path.join(os.environ["TEMP"], "TsukiNotes.zip")
            
            for url in download_urls:
                try:
                    self.log.emit(f"尝试从 {url} 下载...")
                    self.progress.emit(30, f"正在下载...")
                    
                    # 使用 GET 请求而不是 HEAD 请求来获取文件大小
                    response = requests.get(url, headers=headers, stream=True, timeout=10)
                    response.raise_for_status()
                    total_size = int(response.headers.get('content-length', 0))
                    
                    if total_size == 0:
                        # 如果无法获取文件大小，尝试直接下载
                        content = response.content
                        if len(content) > 0:
                            with open(temp_path, 'wb') as f:
                                f.write(content)
                            self.log.emit(f"下载完成，文件保存至: {temp_path}")
                            return
                        else:
                            raise Exception("无法获取文件内容")
                    
                    # 多线程下载部分
                    chunk_size = max(total_size // 16, 1024 * 1024)  # 确保每个分块至少1MB
                    chunks = []
                    for i in range(0, total_size, chunk_size):
                        end = min(i + chunk_size - 1, total_size - 1)
                        chunks.append((i, end))
                    
                    downloaded = [0]
                    start_time = time.time()
                    
                    def download_chunk(start, end):
                        chunk_headers = headers.copy()
                        chunk_headers['Range'] = f'bytes={start}-{end}'
                        retry_count = 3
                        
                        while retry_count > 0:
                            try:
                                response = requests.get(url, headers=chunk_headers, timeout=30)
                                response.raise_for_status()
                                return start, response.content
                            except Exception as e:
                                retry_count -= 1
                                if retry_count == 0:
                                    raise e
                                time.sleep(1)
                    
                    # 创建临时文件
                    with open(temp_path, 'wb') as f:
                        f.truncate(total_size)
                    
                    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
                        future_to_chunk = {executor.submit(download_chunk, start, end): (i, start, end) 
                                         for i, (start, end) in enumerate(chunks)}
                        
                        for future in concurrent.futures.as_completed(future_to_chunk):
                            try:
                                start, data = future.result()
                                with open(temp_path, 'rb+') as f:
                                    f.seek(start)
                                    f.write(data)
                                
                                downloaded[0] += len(data)
                                percent = (downloaded[0] / total_size) * 100
                                speed = downloaded[0] / (1024 * 1024 * max(time.time() - start_time, 0.1))
                                
                                status = (f"下载中... {percent:.1f}% | {speed:.1f} MB/s | "
                                        f"{downloaded[0]/(1024*1024):.1f}MB/{total_size/(1024*1024):.1f}MB")
                                
                                self.progress.emit(30 + int(percent * 0.3), status)
                                
                            except Exception as e:
                                raise Exception(f"下载失败: {str(e)}")
                    
                    # 验证文件大小
                    if os.path.getsize(temp_path) != total_size:
                        raise Exception("文件下载不完整")
                    
                    self.log.emit(f"下载完成，文件保存至: {temp_path}")
                    return
                    
                except Exception as e:
                    self.log.emit(f"从 {url} 下载失败: {str(e)}")
                    continue
                    
            raise Exception("所有下载源均失败")
                
        except Exception as e:
            raise Exception(f"下载失败: {str(e)}")

    def extract_and_overwrite_files(self, install_path):
        try:
            temp_path = os.path.join(os.environ["TEMP"], "TsukiNotes.zip")
            self.log.emit(f"正在验证下载文件...")
            
            # 验证文件是否存在且大小不为0
            if not os.path.exists(temp_path):
                raise Exception("下载文件不存在")
            
            if os.path.getsize(temp_path) == 0:
                raise Exception("下载文件大小为0")
                
            # 验证ZIP文件格式
            try:
                with open(temp_path, 'rb') as f:
                    magic_number = f.read(4)
                    if magic_number != b'PK\x03\x04':
                        raise Exception("文件格式错误，不是效的ZIP文件")
            except Exception as e:
                raise Exception(f"文件验证失败: {str(e)}")
                
            # 尝试打开并验证ZIP文件
            try:
                with zipfile.ZipFile(temp_path, 'r') as test_zip:
                    # 测试ZIP文件完整性
                    test_result = test_zip.testzip()
                    if test_result is not None:
                        raise Exception(f"ZIP文件损坏，首个错误文件: {test_result}")
            except zipfile.BadZipFile:
                raise Exception("无效的ZIP文件格式")
                
            self.log.emit("文件验证通过，开始解压...")
            
            # 解压文件
            with zipfile.ZipFile(temp_path, 'r') as zip_ref:
                total_files = len(zip_ref.namelist())
                extracted_files = 0
                
                for file in zip_ref.namelist():
                    try:
                        zip_ref.extract(file, install_path)
                        extracted_files += 1
                        progress = (extracted_files / total_files) * 100
                        self.progress.emit(60 + int(progress * 0.2), f"正在解压: {progress:.1f}% | {file}")
                        self.log.emit(f"已解压: {file}")
                    except Exception as e:
                        raise Exception(f"解压文件 {file} 失败: {str(e)}")
                        
            # 清理临时文件
            try:
                os.remove(temp_path)
                self.log.emit("临时文件已清理")
            except Exception as e:
                self.log.emit(f"清理临时文件失败（非致命错误）: {str(e)}")
                
            self.log.emit("文件解压完成")
            
        except Exception as e:
            # 确保出错时也清理临时文件
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            except:
                pass
            raise Exception(f"解压和覆盖文件失败: {str(e)}")

    def update_shortcuts(self, install_path):
        try:
            exe_path = None
            for root, dirs, files in os.walk(install_path):
                for dir in dirs:
                    if dir.startswith("TsukiNotesVer") and dir.endswith("Windows"):
                        potential_exe = os.path.join(root, dir, "TsukiNotes.exe")
                        if os.path.exists(potential_exe):
                            exe_path = potential_exe
                            break
                if exe_path:
                    break
            
            if not exe_path:
                raise Exception("Cannot find TsukiNotes.exe")
            
            self.log.emit(f"Found TsukiNotes.exe: {exe_path}")
            
            shell = win32com.client.Dispatch("WScript.Shell")
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            shortcut_path = os.path.join(desktop, "TsukiNotes.lnk")
            
            if os.path.exists(shortcut_path):
                try:
                    os.remove(shortcut_path)
                    self.log.emit("Deleted Old Shortcut")
                except Exception as e:
                    self.log.emit(f"Failed To Delete Old Shortcut: {str(e)}")
            
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = exe_path
            shortcut.WorkingDirectory = os.path.dirname(exe_path)
            shortcut.IconLocation = exe_path
            shortcut.save()
            
        except Exception as e:
            raise Exception(f"Update Shortcuts Failed: {str(e)}")

    def emit_finished(self, message, success=True):
        self.finished.emit(success, message)

if __name__ == "__main__":
    # Create config
    try:
        logging.basicConfig(
            filename="tsuki_installer.log",
            level=logging.DEBUG,
            format='[%(asctime)s | %(levelname)s]%(message)s',
            datefmt='%Y/%m/%d %H:%M:%S',
            encoding='utf-8'
        )
    except Exception as e:
        print(f"日志初始化失败: {e}")

    try:
        app = QApplication(sys.argv)
        
        app.setFont(QFont("Microsoft YaHei", 10))

        run_as_admin()
        
        wizard = InstallerWizard(silent_mode=False)  # 默认非静默模式
        app.aboutToQuit.connect(wizard.close)
        
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