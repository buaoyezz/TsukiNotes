#==================================
# Install Lite For TsukiNotes
# Lite Version ≠ Wizard
# B1.0.0
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
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import win32com.client
import concurrent.futures


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

run_as_admin()

def check_version():
    try:
        version_url = "http://zzbuaoye.us.kg/TsukiNotes/version.txt"
        response = requests.get(version_url, timeout=10)
        response.raise_for_status()
        
        for line in response.text.splitlines():
            if line.startswith("version:"):
                return line.split(":")[1].strip()
        return None
    except:
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
    current_parts = map(int, (current_version or '0').split('.'))
    latest_parts = map(int, (latest_version or '0').split('.'))
    return any(l > c for l, c in zip_longest(latest_parts, current_parts, fillvalue=0))

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
        
        self.setStyleSheet("""
            QWizard, QWizardPage {
                background-color: white;
                font-family: "Microsoft YaHei";
            }
            QPushButton {
                background-color: #60CDFF;
                color: black;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-family: "Microsoft YaHei";
            }
            QPushButton:hover {
                background-color: #99E5FF;
            }
            QLineEdit, QTextEdit {
                padding: 6px;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                font-family: "Microsoft YaHei";
            }
        """)
        
        self.addPage(InstallProgressPage())
        
        self.setWizardStyle(QWizard.ModernStyle)
        
        QTimer.singleShot(0, self.auto_install)
    
    def auto_install(self):
        self.next()

    def cancel_installation(self):
        temp_path = os.path.join(os.environ["TEMP"], "TsukiNotes.zip")
        if os.path.exists(temp_path):
            os.remove(temp_path)
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
    
    def closeEvent(self, event):
        if self.thread and self.thread.isRunning():
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
        self.progress.setValue(value)
        self.status_label.setText(status)

    def handle_worker_finished(self, success, message):
        self.installationComplete.emit(success, message)
        if self.thread:
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
            logging.debug("The Install Tool Version: 1.0.0")
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
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            download_url = (
                f"https://github.com/buaoyezz/TsukiNotes/releases/download/"
                f"TsukiNotesV{version}/"
                f"TsukiNotesVer{version}.Release_x64_Windows.zip"
            )
            self.log.emit(f"Start Download: {download_url}")
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(requests.get, download_url, headers=headers)
                response = future.result()
            response.raise_for_status()
            
            temp_path = os.path.join(os.environ["TEMP"], "TsukiNotes.zip")
            with open(temp_path, "wb") as f:
                f.write(response.content)
            self.log.emit(f"Download Completed,Save To: {temp_path}")
                
        except Exception as e:
            raise Exception(f"Download Failed: {str(e)}")

    def extract_and_overwrite_files(self, install_path):
        try:
            temp_path = os.path.join(os.environ["TEMP"], "TsukiNotes.zip")
            self.log.emit(f"Extracting and Overwriting Files: {temp_path}")
            with zipfile.ZipFile(temp_path, 'r') as zip_ref:
                for file in zip_ref.namelist():
                    zip_ref.extract(file, install_path)
                    self.log.emit(f"Extracted: {file}")
            os.remove(temp_path)
            self.log.emit("Template Files Extracted And Overwritten Successfully")
        except Exception as e:
            raise Exception(f"Extract and Overwrite Files Failed: {str(e)}")

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

        if not is_admin():
            if sys.argv[-1] != 'asadmin':
                script = os.path.abspath(sys.argv[0])
                params = ' '.join([script] + sys.argv[1:] + ['asadmin'])
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
                sys.exit()
            else:
                QMessageBox.critical(None, "错误", "无法获取管理员权限")
                sys.exit(1)
        
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