# -*- coding: utf-8 -*-
import sys
import ctypes
if __name__ == "__main__":
    debug_mode = "--debug" in sys.argv
    print(f"Command line arguments: {sys.argv}")  # 调试输出
    print(f"Debug mode: {debug_mode}")  # 调试输出
    
    if debug_mode:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)
    else:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
import ipaddress
import shutil
import subprocess
import logging
import os
import webbrowser
import re
import requests
import chardet
import time
import json
import configparser
from datetime import datetime
from socket import socket
from turtle import color, pos
from packaging import version
import ping3
from PyQt5.QtGui import (
    QFont, QIcon, QTextCharFormat, QColor, QTextCursor, QKeySequence, QSyntaxHighlighter,
    QPixmap, QPalette, QBrush
)
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QFontDialog,
    QTabWidget, QInputDialog, QMenu, QMessageBox, QPushButton, QShortcut,
    QLabel, QTextBrowser, QVBoxLayout, QCheckBox, QWidget, QPlainTextEdit,
    QColorDialog, QDialog, QToolBar, QLineEdit, QDialogButtonBox, QGridLayout,
    QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import QSettings, Qt, QEvent, QFile, QRegExp, QTimer
from PyQt5.QtWidgets import QMessageBox, QListWidget, QListWidgetItem, QVBoxLayout, QDialog, QPushButton, QLabel


# 定义颜色
RESET = '\033[0m'
WHITE = '\033[97m'
YELLOW = '\033[93m'
RED = '\033[91m'
GREEN = '\033[32m'
class ColoredFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno == logging.INFO:
            color = GREEN
        elif record.levelno == logging.WARNING:
            color = YELLOW
        elif record.levelno == logging.ERROR:
            color = RED
        else:
            color = RESET

        message = super().format(record)
        return f'{color}{message}{RESET}'

if os.path.exists('./tsuki/assets/log/'):
    tips_log_dir = './tsuki/assets/log/'
    os.makedirs(tips_log_dir, exist_ok=True)
    def create_and_write_file(directory, filename, content):
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, filename)
        # 写入
        with open(file_path, 'w') as file:
            file.write(content)
    directory = './tsuki/assets/log/'
    filename = 'Log_ZZBuAoYe_Readme.txt'
    content = ('Dear User,\n\nThank you for using this software.\n\nYou are currently looking at the Log folder.\n\nPlease note the following:\n1. Logs are usually stored in the temp folder.\n2. The log files have a .log extension.\n3. Log file names follow this format: TsukiNotes_Log_{timestamp}.log, where {timestamp} is in the format datetime.now().strftime('').\n4. This text file is not pre-existing but is created automatically!\n5. Thanks for using our software.')

    create_and_write_file(directory, filename, content)

# 配置日志记录
def setup_logging():
    # 确保日志目录存在
    log_dir = './tsuki/assets/log/temp/'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    os.makedirs(log_dir, exist_ok=True)

    # 创建处理器
    stream_handler = logging.StreamHandler()  # 输出到控制台
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    file_handler = logging.FileHandler(os.path.join(log_dir, f'TsukiNotes_Log_{timestamp}.log'))  # 输出到文件
    # 设置格式化器
    formatter = ColoredFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)


setup_logging()

logger = logging.getLogger(__name__)
# debug mod
debug_version = '1.0.1FullVersion'
logger.info("[LOG]Welcome Use TsukiNotes")
logger.info("[LOG]You are using version 1.4.9")
logger.info("[INFO]Running DEBUG MOD NOW!")
logger.info("Please wait for the program to start")
logger.info("====================================================================================================================")
logger.info("╔═══╗╔═══╗╔══╗ ╔╗╔╗╔══╗╔══╗╔╗╔╗╔═══╗")
logger.info("╚═╗ ║╚═╗ ║║╔╗║ ║║║║║╔╗║║╔╗║║║║║║╔══╝")
logger.info(" ╔╝╔╝ ╔╝╔╝║╚╝╚╗║║║║║╚╝║║║║║║╚╝║║╚══╗")
logger.info("╔╝╔╝ ╔╝╔╝ ║╔═╗║║║║║║╔╗║║║║║╚═╗║║╔══╝")
logger.info("║ ╚═╗║ ╚═╗║╚═╝║║╚╝║║║║║║╚╝║ ╔╝║║╚══╗")
logger.info("╚═══╝╚═══╝╚═══╝╚══╝╚╝╚╝╚══╝ ╚═╝╚═══╝")
logger.info("====================================================================================================================")
logger.info("\n╔════╗╔══╗╔╗╔╗╔╗╔══╗╔══╗╔╗─╔╗╔══╗╔════╗╔═══╗╔══╗\n"
            "╚═╗╔═╝║╔═╝║║║║║║║╔═╝╚╗╔╝║╚═╝║║╔╗║╚═╗╔═╝║╔══╝║╔═╝\n"
            "  ║║  ║╚═╗║║║║║╚╝║   ║║ ║╔╗ ║║║║║  ║║  ║╚══╗║╚═╗\n"
            "  ║║  ╚═╗║║║║║║╔╗║   ║║ ║║╚╗║║║║║  ║║  ║╔══╝╚═╗║\n"
            "  ║║  ╔═╝║║╚╝║║║║╚═╗╔╝╚╗║║ ║║║╚╝║  ║║  ║╚══╗╔═╝║\n"
            "  ╚╝  ╚══╝╚══╝╚╝╚══╝╚══╝╚╝ ╚╝╚══╝  ╚╝  ╚═══╝╚══╝\n")
logger.info("====================================================================================================================")
logger.info("Running Succeed")
logger.info(f"DebugVersion: {debug_version}")
logger.info('调试模式状态开启')
logger.info("====================================================================================================================\n\n")

import os
import datetime
import re


def delete_old_logs(directory, time_threshold_days=3):
    if not os.path.exists(directory):
        logger.error(f"目录不存在: {directory}")
        return

    now = datetime.datetime.now()
    logs_by_date = {}

    for filename in os.listdir(directory):
        if filename.endswith('.log'):
            match = re.match(r'TsukiNotes_Log_(\d{4}-\d{2}-\d{2})_(\d{2}-\d{2}-\d{2})\.log', filename)
            if match:
                date_str = match.group(1)
                time_str = match.group(2)
                timestamp_str = f"{date_str}_{time_str}"
                try:
                    log_time = datetime.datetime.strptime(timestamp_str, '%Y-%m-%d_%H-%M-%S')
                    time_difference = (now - log_time).days  # 计算时间差

                    if time_difference > time_threshold_days:  # 比较时间差
                        file_path = os.path.join(directory, filename)
                        os.remove(file_path)
                        logger.info(f"删除文件: {file_path}")
                    else:
                        if date_str not in logs_by_date:
                            logs_by_date[date_str] = []
                        logs_by_date[date_str].append((log_time, filename))
                except ValueError as e:
                    logger.error(f"时间戳解析错误: {timestamp_str} - 错误: {e}")

    for date_str, log_files in logs_by_date.items():
        if len(log_files) > 1:
            log_files.sort() 
            latest_log = log_files[-1]
            for log_time, filename in log_files[:-1]:  # 保留最新的一个
                file_path = os.path.join(directory, filename)
                os.remove(file_path)
                logger.info(f"删除文件: {file_path}，保留最新文件: {latest_log[1]}")

log_directory = 'tsuki/assets/log/temp/'
delete_old_logs(log_directory)
# ==============================================================End Welcome===================================================================================================================
class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, light=True, parent=None):
        super().__init__(parent)
        self.l = light
        # self.highlight_keywords = True
        keyword_format = QTextCharFormat()
        if light:
            keyword_format.setForeground(QColor("#b8860b"))
            keyword_format.setFontWeight(QFont.Bold)
        keywords = [
            "and", "as", "assert", "break", "class", "continue", "def",
            "del", "elif", "else", "except", "finally", "for",
            "from", "global", "if", "import", "in", "is", "lambda",
            "not", "or", "pass", "raise", "return", "try",
            "while", "with", "yield", "#", "//", "None", "pass",
            "/n", "/", "parent", "format", "set", "int", "self",
            "set", "__init__", "main", "(", ")", "layout", "QDialog"
            "'''", "False", "True", "range","print","input"
        ]
        self.keyword_patterns = [(QRegExp(r"\b" + keyword + r"\b"), keyword_format)
                                 for keyword in keywords]

        quotation_format = QTextCharFormat()
        if light: quotation_format.setForeground(QColor("#608B4E"))
        self.quotation_pattern = (QRegExp("\".*\""), quotation_format)

        function_format = QTextCharFormat()
        function_format.setFontItalic(True)
        if light: function_format.setForeground(QColor("#569CD6"))
        self.function_pattern = (QRegExp(r"\b[A-Za-z0-9_]+(?=\()"), function_format)

        self.comment_format = QTextCharFormat()
        if light: self.comment_format.setForeground(QColor("#ff0000"))
        self.comment_pattern = (QRegExp(r"#.*"), self.comment_format)

    def highlightBlock(self, text):
        for pattern, format in self.keyword_patterns:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        start_index = 0
        if self.previousBlockState() != 1:
            start_index = self.comment_pattern[0].indexIn(text)

        while start_index >= 0:
            end_index = self.comment_pattern[0].matchedLength()
            self.setFormat(start_index, end_index, self.comment_pattern[1])
            start_index = self.comment_pattern[0].indexIn(text, start_index + end_index)

        self.setCurrentBlockState(1)

class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super(SettingsWindow, self).__init__(parent)
        self.setWindowTitle('Tsuki全局设置[Settings]')  # 更改窗口标题为设置界面
        self.setGeometry(100, 100, 600, 200)  # 设置窗口初始大小
        logger.info('Open Setting')
        layout = QVBoxLayout(self)

        # 添加右上角的“设置”标签
        label = QLabel("|设置", self)
        label.setStyleSheet("""
            QLabel {
                font-size: 20px; 
                font-weight: bold;
                margin-top: 0px;
                margin-right: 10px;
                alignment: AlignLeft;
                font-family: "Microsoft YaHei UI" /* 我最爱的微软雅黑 */
            }
        """)
        layout.addWidget(label, alignment=Qt.AlignLeft | Qt.AlignTop)

        grid_layout = QGridLayout()

        grid_layout.addWidget(self.createButton("设置背景颜色", self.parent().set_background), 0, 0)
        grid_layout.addWidget(self.createButton("重置文本框背景图片", self.parent().reset_background_color), 0, 1)
        grid_layout.addWidget(self.createButton("设置字体大小", self.parent().set_font_size), 1, 0)
        grid_layout.addWidget(self.createButton("初始化字体大小", self.parent().initialize_font_size), 1, 1)
        grid_layout.addWidget(self.createButton("重新设置图标", self.parent().re_icon_setting), 2, 0)
        grid_layout.addWidget(self.createButton("自定义图标", self.parent().diy_icon_setting), 2, 1)
        grid_layout.addWidget(self.createButton("检查图标路径", self.parent().iconpath_check_a1), 3, 0)
        grid_layout.addWidget(self.createButton("统计/关于显示设置", self.parent().total_setting), 3, 1)
        grid_layout.addWidget(self.createButton("设置背景图", self.parent().setBackgroundImage), 4, 0)
        grid_layout.addWidget(self.createButton("重置背景图",self.parent().reset_background), 4,1)
        grid_layout.addWidget(self.createButton("用户背景图[app/default/user_file][测试]", self.parent().select_and_set_background), 5, 0)
    
        layout.addLayout(grid_layout)

        # 应用样式
        self.applyStyle()

    def createButton(self, text, slot):
        button = QPushButton(text)
        button.clicked.connect(slot)
        button.setStyleSheet("""
            QPushButton {
                background-color: #666666;  /* gray按钮背景 */
                color: white;
                border: 1px solid #005a9e;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                font-family: "Microsoft YaHei" 
            }
            QPushButton:hover {
                background-color: #4a4a4a;  /* 按钮悬停的 */
            }
            QPushButton:pressed {
                background-color: #3c3c3c;  /* 按钮按下时候的 */
            }
        """)
        return button

    def applyStyle(self):
        # 设置窗口样式
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;  /* 浅灰色背景 */
            }
            QLabel {
                color: #333333;  /* 深灰色文字 */
                font-size: 14px;
            }
        """)

# 搜索的class
class SearchResultDialog(QDialog):
    def __init__(self, results, parent=None):
        super(SearchResultDialog, self).__init__(parent)
        self.setWindowTitle('搜索成功！')
        print("[Log/INFO]Search Succeed")
        self.results_label = QLabel()
        self.results = results
        self.current_index = 0

        self.next_button = QPushButton('下一个')
        self.next_button.clicked.connect(self.showNextResult)

        self.previous_button = QPushButton('上一个')
        self.previous_button.clicked.connect(self.showPreviousResult)

        self.ok_button = QPushButton('确定')
        self.ok_button.clicked.connect(self.accept)

        self.cancel_button = QPushButton('退出')
        self.cancel_button.clicked.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(self.results_label)
        layout.addWidget(self.next_button)
        layout.addWidget(self.previous_button)
        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)
        self.setLayout(layout)

        self.showResult()

    def showResult(self):
        if self.results:
            result = self.results[self.current_index]
            self.results_label.setText(result)
        else:
            self.results_label.setText("Tips:未找到有关的结果")
            logger.info(f"Can't Find Result[{result}]")
            print(f"[Log/INFO]Can't Find Result[{result}]")

    def showNextResult(self):
        if self.results:
            if self.current_index < len(self.results) - 1:
                self.current_index += 1
            else:
                self.current_index = 0
            self.showResult()

    def showPreviousResult(self):
        if self.results:
            if self.current_index > 0:
                self.current_index -= 1
            else:
                self.current_index = len(self.results) - 1
            self.showResult()
# ======================================================以下是TsukiReader的CLass=====================================================
# ==================================================================================================================================

class TsukiReader(QMainWindow):

    def __init__(self):
        self.before = ''
        self.current_version = '1.4.9'  # 全局版本号
        self.real_version = '1.4.9'
        self.update_Date = '2024/08/05'
        self.version_td = 'FullVersion'
        self.version_gj = 'b-v149FV240805'
        print(f"====================================================================================================================\n"
              f"[Log/INFO]TsukiReader is running ,relatedInformation:"
              f"[Back]Version:{self.current_version}\n"
              f"[Back]UpdateDate:{self.update_Date}\n"
              f"[Back]Version Update The Channel:{self.version_td}\n"
              f"[Back]versionTHE INTERNAL BUILD NUMBER:{self.version_gj}")

        super().__init__()
        self.text_modified = False
        self.include_whitespace = False
        self.highlight_keywords = False
        self.context_menu = None
        self.custom_lines = 0
        self.initUI()

    def initUI(self):
        self.tabWidget = QTabWidget()
        self.setCentralWidget(self.tabWidget)
        self.context_menu = QMenu(self)
        self.createActions()
        self.createMenus()
        self.createShortcuts()
        self.defaultFont = QFont("Microsoft YaHei")
        self.setGeometry(100, 100, 990, 600)
        self.setWindowTitle('TsukiNotes')

        self.text_edit = QPlainTextEdit()
        self.show()
        self.highlighter = PythonHighlighter(self.highlight_keywords, self.text_edit.document())
        self.status_label = QLabel()
        self.statusBar().addPermanentWidget(self.status_label)
        # 初始cfg load=======================================
        print("Loading Cfg=======================================")
        logger.info(f"Loading Config")
        QTimer.singleShot(100, self.read_font_size_from_cfg)
        print(f"[Log/INFO]载入{self.read_font_size_from_cfg}成功")
        QTimer.singleShot(110,self.read_font_family_from_cfg)
        print(f"[Log/INFO]载入{self.read_font_family_from_cfg}成功")
        QTimer.singleShot(120, self.load_background_settings)
        print(f"[Log/INFO]载入{self.load_background_settings}成功")
        logger.info(f"Config Loading Succeed")
        print("End.程序初始化完成=================================")
        # ====================================================
        v = sys.argv
        nv = []
        for i in v:
            if (i != "--debug","-debug"): nv.append(i)
        if len(nv)>1:
            if os.path.isfile(nv[1]):
                self.openFile(nv[1])
                font = QFont("Microsoft YaHei UI")# 默认字体
                logger.info(f"[Log/INFO]载入{nv[1]}成功")
                self.text_edit.setFont(font)
            else:
                QMessageBox.critical(self, 'Open File', f'失败了❌❗: 文件{nv[1]}不存在！')
                self.statusBar().showMessage(f'TsukiOF❌: 文件[{nv[1]}]打开失败！Error:[文件不存在]')
                print("[Log/ERROR]ERROR Init UI Open File:", "文件不存在")
                logger.error(f"[Log/ERROR]ERROR Init UI Open File: 文件{nv[1]}不存在！")
                self.newFile()
        else:
            self.newFile()

        icon_path = "./tsuki/assets/GUI/ico/logo.ico"
        icon2_path = "./tsuki/assets/GUI/ico/old_logo.ico"
        icon = QIcon(icon_path)
        icon2 = QIcon(icon2_path)  # 原始logo
        self.setWindowIcon(icon)
        self.updateStatusLabel()

        currentWidget = self.tabWidget.currentWidget()
        currentWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        currentWidget.customContextMenuRequested.connect(self.showContextMenu)
        self.context_menu = QMenu(self)
        self.loadBackgroundSettings()

    def showContextMenu(self, pos):
        self.context_menu = QMenu(self)
        self.context_menu.setStyleSheet("background-color: rgba(255, 255, 255, 150); border: 2px solid black;")

        # 添加动作到右键菜单
        self.addContextAction("Search", 'Ctrl+F', self.performSearch)
        self.addContextAction("Save", 'Ctrl+S', self.performSave)
        self.addContextAction("Clear", 'Ctrl+Shift+C', self.performClear)
        self.addContextAction("Undo", 'Ctrl+Z', self.performUndo)
        self.addContextAction("Redo", 'Ctrl+Y', self.performRedo)
        self.addContextAction("Cut", 'Ctrl+X', self.performCut)
        self.addContextAction("Open", 'Ctrl+O', lambda: self.openFile(""))
        self.addContextAction("New Tab", 'Ctrl+T', self.newFile)
        self.addContextAction("Close Tab", 'Ctrl+W', self.closeFile)
        self.addContextAction("Update", 'Update->手动', self.update2)
        self.addContextAction("AutoUpdate", 'Update->Auto', self.Show_Auto_Update2)
        self.addContextAction("MathTools", '点后计算[请提前选中计算式]', self.mathTools)

        # 连接右键菜单到右键点击事件
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)
        self.context_menu.exec_(self.mapToGlobal(pos))
    def addContextAction(self, text, shortcut, slot, icon=None):
        if icon:
            action = QAction(icon, text, self)
        else:
            action = QAction(text, self)
        action.setShortcut(shortcut)
        action.triggered.connect(slot)
        self.context_menu.addAction(action)
    def performClear(self):
        currentWidget = self.tabWidget.currentWidget()
        currentWidget.clear()
        self.statusBar().showMessage('Tsuki✔: 您执行了一次清空操作,按下Ctrl+Z撤销更改')
        logger.info(f"[Log/INFO]执行清空操作")

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)
        self.context_menu.exec_(self.mapToGlobal(pos))

    def addContextAction(self, name, shortcut, slot):
        action = QAction(f"{name} ({shortcut})", self)
        action.setShortcut(shortcut)
        action.triggered.connect(slot)
        self.context_menu.addAction(action)


    def set_font_size(self):
        try:
            font_size, ok = QInputDialog.getInt(self, '设置字体大小', '请输入字体大小:', 12, 1, 100, 1)
            logger.info(f"[Log/INFO]打开字体大小操作设置页面")
            if ok:
                current_widget = self.tabWidget.currentWidget()
                current_font = current_widget.font()
                current_font.setPointSize(font_size)
                current_widget.setFont(current_font)

                QMessageBox.information(self, '提示', f'字体大小设置成功为 {font_size}，喵~')
                self.statusBar().showMessage(f'TsukiFS✔: 字体大小设置成功为 {font_size}')
                logger.info(f"[Log/INFO]执行设置字体大小操作")
                self.save_font_size_to_cfg(font_size)
                logger.info(f"[Log/INFO]成功保存字体大小配置文件")

        except Exception as e:
            QMessageBox.critical(self, '错误', f'发生错误：{str(e)}')
            print(f"{e}")
            self.statusBar().showMessage(f'TsukiFS❌: 字体大小设置失败！详见MessageBox！')
            logger.error(f"[Log/ERROR]ERROR Set Font Size: {str(e)}")

    def save_font_size_to_cfg(self, font_size):
        config = configparser.ConfigParser()
        config['Settings'] = {'font_size': str(font_size)}
        
        # 确保目录存在
        cfg_dir = 'tsuki/assets/app/cfg/font'
        if not os.path.exists(cfg_dir):
            os.makedirs(cfg_dir)
            print("[INFO]SAVE")
            logger.info(f"[Log/INFO]创建字体大小配置文件")

        # 保存配置文件
        cfg_path = os.path.join(cfg_dir, 'tn_font.ini')
        with open(cfg_path, 'w') as configfile:
            config.write(configfile)
            print(f"[INFO]SAVE {cfg_path}")
            logger.info(f"[Log/INFO]成功保存字体大小配置文件")

    def read_font_size_from_cfg(self):
        cfg_file = "tsuki/assets/app/cfg/font/tn_font.ini"

        if os.path.exists(cfg_file):
            config = configparser.ConfigParser()
            config.read(cfg_file)

            font_size = config.getint('Settings', 'font_size', fallback=12)
            current_widget = self.tabWidget.currentWidget()
            if current_widget:
                current_font = current_widget.font()
                current_font.setPointSize(font_size)
                current_widget.setFont(current_font)


    def createActions(self):
        self.newAct = QAction(QIcon('./tsuki/assets/GUI/resources/create_tab.png'),'创建新的标签页（Ctrl+T）', self)
        self.newAct.triggered.connect(self.newFile)

        self.openAct = QAction(QIcon('./tsuki/assets/GUI/resources/import_file.png'),'打开文件（Ctrl+O）', self)
        self.openAct.triggered.connect(lambda: (self.openFile("")))

        self.saveAct = QAction(QIcon('./tsuki/assets/GUI/resources/save_file.png'), '保存修改（Ctrl+S）', self)
        self.saveAct.triggered.connect(self.saveFile)

        self.closeAct = QAction(QIcon('./tsuki/assets/GUI/resources/off_file.png'),'关闭文件（Ctrl+W）', self)
        self.closeAct.triggered.connect(self.closeFile)

        self.fontAct = QAction(QIcon('./tsuki/assets/GUI/resources/font_reset_change.png'),'修改字体', self)
        self.fontAct.triggered.connect(self.changeFont)

        self.setfontsizeAct = QAction(QIcon('./tsuki/assets/GUI/resources/font_size_reset_tab.png'),'字体大小',self)
        self.setfontsizeAct.triggered.connect(self.set_font_size)
                                

        self.checkUpdateAct = QAction(QIcon('./tsuki/assets/GUI/resources/update_cloud.png'),'检查更新', self)
        self.checkUpdateAct.triggered.connect(self.checkForUpdates)

        self.aboutAct = QAction(QIcon('./tsuki/assets/GUI/resources/about.png'),'关于Tsuki版本信息', self)
        self.aboutAct.triggered.connect(self.aboutMessage)

        self.aboutDetailsAct = QAction(QIcon('./tsuki/assets/GUI/resources/about.png'),'关于Tsuki详细信息', self)
        self.aboutDetailsAct.triggered.connect(self.aboutDetails)

        self.updateAct = QAction(QIcon('./tsuki/assets/GUI/resources/update_msg.png'),'更新日志', self)
        self.updateAct.triggered.connect(self.updateMessage)

        self.updatetxtAct = QAction(QIcon('./tsuki/assets/GUI/resources/update_msg.png'),'关于Tsuki更新内容',self)
        self.updatetxtAct.triggered.connect(self.updateMessage)

        self.exitAct = QAction(QIcon('./tsuki/assets/GUI/resources/exit_software.png'),'退出程序', self)
        self.exitAct.triggered.connect(self.close)

        self.resetFontAct = QAction(QIcon('./tsuki/assets/GUI/resources/font_reset_change.png'),'重置字体', self)
        self.resetFontAct.triggered.connect(self.resetFont)

        self.update2Act = QAction(QIcon('./tsuki/assets/GUI/resources/update_cloud.png'),'手动检测更新', self)
        self.update2Act.triggered.connect(self.update2)

        self.renameTabAct = QAction(QIcon('./tsuki/assets/GUI/resources/font_size_reset_tab.png'),'重命名标签', self)
        self.renameTabAct.triggered.connect(self.renameTab)

        self.cutTabAct = QAction(QIcon('./tsuki/assets/GUI/resources/settings_list_shortcut.png'),'快捷键', self)
        self.cutTabAct.triggered.connect(self.cutTab)

        self.pingServerManuallyAct = QAction(QIcon('./tsuki/assets/GUI/resources/server_ping.png'),'手动Ping服务器', self)
        self.pingServerManuallyAct.triggered.connect(self.pingServerManually)

        self.url_msgAct = QAction(QIcon('./tsuki/assets/GUI/resources/server_tb.png'),'测试服务器返回', self)
        self.url_msgAct.triggered.connect(self.url_msg)

        self.versionnowAct = QAction(QIcon('./tsuki/assets/GUI/resources/custom_server.png'),'当前版本号')
        self.versionnowAct.triggered.connect(self.versionnow)

        self.online_updateMessageAct = QAction(QIcon('./tsuki/assets/GUI/resources/update_cloud.png'),'在线更新日志')
        self.online_updateMessageAct.triggered.connect(self.online_updateMessage)

        self.settingsAction = QAction(QIcon('./tsuki/assets/GUI/resources/open_list.png'),'设置', self)
        settingicon = "tsuki/assets/ico/setting.ico"
        self.settingsAction.setIcon(QIcon(settingicon))
        self.settingsAction.triggered.connect(self.openSettingsWindow)
        self.settingsAction.setIcon(QIcon(settingicon))
    def createMenus(self):
        menubar = self.menuBar()

        fileMenu = menubar.addMenu('文件')
        fileMenu.addAction(self.newAct)
        fileMenu.addAction(self.openAct)
        fileMenu.addAction(self.saveAct)
        fileMenu.addAction(self.closeAct)
        fileMenu.addAction(self.exitAct)

        editMenu = menubar.addMenu('编辑')
        editMenu.addAction(self.fontAct)
        editMenu.addAction(self.resetFontAct)
        editMenu.addAction(self.renameTabAct)
        editMenu.addAction(self.setfontsizeAct)

        UpdateMenu = menubar.addMenu('更新')
        UpdateMenu.addAction(self.checkUpdateAct)
        UpdateMenu.addAction(self.update2Act)
        UpdateMenu.addAction(self.versionnowAct)
        UpdateMenu.addAction(self.online_updateMessageAct)
        UpdateMenu.addAction(self.updateAct)

        toolbarMenu = menubar.addMenu('关于')
        toolbarMenu.addAction(self.aboutAct)
        toolbarMenu.addAction(self.aboutDetailsAct)
        toolbarMenu.addAction(self.updatetxtAct)

        cutTabMenu = menubar.addMenu('快捷键')
        cutTabMenu.addAction(self.cutTabAct)

        pingServerManuallyMenu = menubar.addMenu('服务器')
        pingServerManuallyMenu.addAction(self.pingServerManuallyAct)
        pingServerManuallyMenu.addAction(self.url_msgAct)

        settings1Menu = menubar.addMenu(QIcon('./tsuki/assets/GUI/resources/settings.png'),'设置')
        settings1Menu.addAction(self.settingsAction)

    def openSettingsWindow(self):
        # 设置main调用
        settings_window = SettingsWindow(self)
        settings_window.exec_()

    # 快捷键绑定
    def createShortcuts(self):
        self.shortcut_search = QShortcut('Ctrl+F', self)
        self.shortcut_save = QShortcut('Ctrl+S', self)
        self.shortcut_clear = QShortcut('Ctrl+Shift+C', self)
        self.shortcut_undo = QShortcut('Ctrl+Z', self)
        self.shortcut_redo = QShortcut('Ctrl+Y', self)
        self.shortcut_cut = QShortcut('Ctrl+X', self)
        self.shortcut_open = QShortcut('Ctrl+O', self)
        self.shortcut_new = QShortcut('Ctrl+T', self)
        self.shortcut_close = QShortcut('Ctrl+W', self)

        self.shortcut_search.activated.connect(self.performSearch)
        self.shortcut_save.activated.connect(self.performSave)
        self.shortcut_clear.activated.connect(self.performClear)
        self.shortcut_undo.activated.connect(self.performUndo)
        self.shortcut_redo.activated.connect(self.performRedo)
        self.shortcut_cut.activated.connect(self.performCut)
        self.shortcut_open.activated.connect(lambda: (self.openFile("")))
        self.shortcut_new.activated.connect(self.newFile)
        self.shortcut_close.activated.connect(self.closeFile)

    def connectTextChangedSignal(self, index):
        currentWidget = self.tabWidget.currentWidget()
        currentWidget.textChanged.connect(self.updateStatusLabel)


    # 新增一个方法用于更新标签的内容
    def updateStatusLabel(self):
        currentWidget = self.tabWidget.currentWidget()
        if currentWidget is not None:
            cursor = currentWidget.textCursor()
            line_number = cursor.blockNumber() + 1
            column_number = cursor.columnNumber() + 1
            char_count = len(currentWidget.toPlainText())
            # 获取当前文件的编码
            encoding = getattr(self, 'current_encoding', 'Unknown-Encoding')

            status_text = f'[总] [ 行数: {line_number} | 列数: {column_number} | 字符数: {char_count} | 编码: {encoding} ]'
            self.status_label.setText(status_text)

    def textChanged(self):
        self.text_modified = True
        self.updateStatusLabel()

    def setDefaultFont(self, textEdit, font):
        if textEdit and isinstance(font, QFont):
            textEdit.setFont(font)

    def changeFont(self):
        try:
            currentWidget = self.tabWidget.currentWidget()
            font, ok = QFontDialog.getFont()

            if ok:
                currentWidget.setFont(font)
                font_name = font.family()
                # 使用QLabel和HTML标签添加图标
                message = QLabel()
                message.setText(
                    f' TsukiFont <img src="./tsuki/assets/GUI/resources/done.png" width="16" height="16">: {font_name} 字体已经成功应用！')
                logging.info(f"[Log/INFO]Change Font: {font_name}")
                self.statusBar().addWidget(message)
                self.save_font_family_to_cfg(font_name)
            else:
                message = QLabel()
                message.setText(
                    f' TsukiFont <img src="./tsuki/assets/GUI/resources/error.png" width="16" height="16">: 字体没能更改！')
                logger.warning("没能更改")
                self.statusBar().addWidget(message)
        except Exception as e:
            message = QLabel()
            message.setText(
                f' TsukiFont <img src="./tsuki/assets/GUI/resources/error.png" width="16" height="16">: 发生错误！！内容: {e}')
            self.statusBar().addWidget(message)
            print("[Log/Error]Change Font Error:", e)
            logger.error("[Log/Error]Change Font Error:", e)

    def save_font_family_to_cfg(self, font_family):
        config = configparser.ConfigParser()
        config['Settings'] = {'font_family': font_family}

        cfg_dir = 'tsuki/assets/app/cfg/font'
        if not os.path.exists(cfg_dir):
            os.makedirs(cfg_dir)
            print("[INFO]SAVE")
            logger.info("[Log/INFO]SAVE")

        cfg_path = os.path.join(cfg_dir, 'tn_font_family.ini')
        with open(cfg_path, 'w') as configfile:
            config.write(configfile)
            print(f"[INFO]SAVE {cfg_path}")
            logger.info(f"[Log/INFO]SAVE {cfg_path}")

    def read_font_family_from_cfg(self):
        cfg_file = "tsuki/assets/app/cfg/font/tn_font_family.ini"

        if os.path.exists(cfg_file):
            config = configparser.ConfigParser()
            config.read(cfg_file)

            font_family = config.get('Settings', 'font_family', fallback='')
            if font_family:
                current_widget = self.tabWidget.currentWidget()
                if current_widget:
                    current_font = current_widget.font()
                    current_font.setFamily(font_family)
                    current_widget.setFont(current_font)

    def MouseDown(self, event=None):
        if event:
            self.x = event.x()
            self.y = event.y()
            self.mouse_press = True
            self.poll()

    def mathTools(self):
        self.statusBar().showMessage('TsukiMathTools🔰: MathTools Loading Successful !')
        logger.info("[Log/INFO]The calculation tool has been successfully loaded and initialization is complete")
        text_edit = self.tabWidget.currentWidget()
        cursor = text_edit.textCursor()
        selected_text = cursor.selectedText().strip()
        math_expr = ''.join(c for c in selected_text if c.isdigit() or c in '+-*/()%')
        try:
            result = eval(math_expr.replace("%", "/100"))
            self.statusBar().showMessage(f'计算结果✔: {result}')
            logger.info(f"[Log/Math]Succeed: MathTools Running , Back: Succeed,{result}")
            if not isinstance(result, (int, float)):
                self.statusBar().showMessage('TsukiMathTools🚫: 不是数学表达式！')
                logger.error("[Log/Error]miscalculated")
        except Exception as e:
            self.statusBar().showMessage(f'计算错误❌: {e}')
            logger.error("[Log/Error]miscalculated")

    def resetFont(self):
        currentWidget = self.tabWidget.currentWidget()
        font = QFont()
        font.setFamily("Microsoft YaHei UI")  # 设置字体家族为微软雅黑
        logger.info("[Log/INFO]Changed the font to Microsoft Yahei UI")
        font_name = font.family()
        currentWidget.setFont(font)
        self.statusBar().showMessage(f'TsukiFontReset: 字体已经成功重置为[{font_name}]！')
        logger.info("[Log/INFO]ReSet Font")

    def openFile(self, fileName):
        if fileName == "":
            options = QFileDialog.Options()
            filters = "Text Files (*.txt *.md *.ini *.xml *.json *.log *.py *.cpp *.java *.tnote);;All Files (*)"
            fileName, _ = QFileDialog.getOpenFileName(self, 'Open File', '', filters, options=options)

        if fileName:
            try:
                encoding = self.detectFileEncoding(fileName)
                self.current_encoding = encoding  # 存储文件编码

                if not self.openFileInTab(fileName, encoding):
                    self.createNewTab(fileName, encoding)

                self.updateWindowTitle(fileName)
                self.statusBar().showMessage(f'TsukiOpen✔: 文件 [{fileName}] 已成功在TsukiNotes内打开！')
                logger.info(f"[Log/INFO]Open File Succeed: {fileName} Encoding: {encoding}\n")

            except Exception as e:
                self.handleError('Open File', fileName, e)

    def detectFileEncoding(self, fileName):
        with open(fileName, 'rb') as file:
            raw_data = file.read(10000)
            result = chardet.detect(raw_data)
            return result['encoding'] or 'utf-8'

    def openFileInTab(self, fileName, encoding):
        for index in range(self.tabWidget.count()):
            if self.tabWidget.tabText(index) == os.path.basename(fileName):
                text_edit = self.tabWidget.widget(index)
                self._load_file_content(fileName, text_edit, encoding)
                self.tabWidget.setCurrentWidget(text_edit)
                return True
        return False

    def createNewTab(self, fileName, encoding):
        tab_name = os.path.basename(fileName)
        text_edit = QPlainTextEdit()
        self.setFont(text_edit)  # 设置默认字体为微软雅黑
        self.tabWidget.addTab(text_edit, tab_name)
        self._load_file_content(fileName, text_edit, encoding)
        self.tabWidget.setCurrentWidget(text_edit)
        text_edit.textChanged.connect(self.updateStatusLabel)

        if fileName.endswith(('.py', '.cpp', '.java')):
            self.highlighter = PythonHighlighter(self.highlight_keywords, text_edit.document())

    def setFont(self, text_edit):
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        text_edit.setFont(font)

    def updateWindowTitle(self, fileName):
        file_name, file_extension = os.path.splitext(fileName)
        window_title = f"TsukiNotes - ['{file_name}.{file_extension[1:]}']"
        self.setWindowTitle(window_title)

    def handleError(self, action, fileName, error):
        QMessageBox.critical(self, action, f'失败了❌❗: {str(error)}')
        self.statusBar().showMessage(f'Tsuki{action[:2]}❌: 文件[{fileName}]操作失败！Error:[{error}]')
        logger.error(f"[Log/ERROR]{action} Error: {error}")

    def _load_file_content(self, fileName, text_edit, encoding):
        try:
            with open(fileName, 'r', encoding=encoding, errors='ignore') as file:
                content = file.read()
                text_edit.setPlainText(content)
        except Exception as e:
            self.handleError('Load File Content', fileName, e)

    def newFile(self):
        textEdit = QPlainTextEdit()
        textEdit.setFont(self.defaultFont)
        self.tabWidget.addTab(textEdit, QIcon('./tsuki/assets/GUI/resources/text_file.png'),"未命名文档")
        logger.info("[Log/INFO]New File")
        textEdit.setLineWrapMode(QPlainTextEdit.NoWrap)
        textEdit.textChanged.connect(self.updateStatusLabel)


    def saveFile(self):
        current_tab_index = self.tabWidget.currentIndex()
        current_tab_widget = self.tabWidget.widget(current_tab_index)
        tab_text = self.tabWidget.tabText(current_tab_index)

        if os.path.isfile(tab_text):
            file_name = tab_text
        else:
            file_name, _ = QFileDialog.getSaveFileName(self, 'TsukiNotes保存文件', '',
                                                       'All Files (*);;Text Files (*.txt);;Markdown Files (*.md);;INI Files (*.ini);;XML Files (*.xml);;JSON Files (*.json);;Log Files (*.log);;Python Files (*.py);;C Files (*.c)')

            if not file_name:
                return

            if not os.path.splitext(file_name)[1]:
                current_file_extension = os.path.splitext(tab_text)[1]
                file_name += current_file_extension

            if file_name != tab_text:
                response = QMessageBox.question(self, '重命名', f'你确定想要将文件名称->> {file_name}?✔',
                                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                logger.info(f"[Log/INFO]Rename File: {tab_text} -> {file_name}")

                if response == QMessageBox.Yes:
                    self.tabWidget.setTabText(current_tab_index, os.path.basename(file_name))
                    logger.info(f"[Log/INFO]Rename File: {tab_text} -> {file_name}")

        text_content = current_tab_widget.toPlainText()
        encoding, ok = QInputDialog.getItem(self, "选择编码", "编码类型🔰:",
                                            ["UTF-8", "ASCII", "ISO-8859-1"], 0, False)
        logger.info(f"[Log/INFO]Save File: {file_name} Encoding: {encoding}")

        if not ok:
            return

        try:
            with open(file_name, 'w', encoding=encoding.lower(), errors='ignore') as file:
                file.write(text_content)
                self.statusBar().showMessage(f'TsukiSave: 文件 [{file_name}] 保存成功！')
                logger.info(f"[Log/INFO]Save File: {file_name} Encoding: {encoding}")
                self.tabWidget.setTabText(current_tab_index, os.path.basename(file_name))
                self.tabWidget.setTabToolTip(current_tab_index, file_name)
                self.tabWidget.setCurrentIndex(current_tab_index)
        except Exception as e:
            QMessageBox.critical(self, 'Save File', f'An error occurred: {str(e)}')
            self.statusBar().showMessage(f'TsukiSave: 保存失败！原因:{str(e)}')
            logger.error(f"[Log/ERROR]Save File Error: {e}")

    def closeFile(self):
        m = self.tabWidget.currentIndex()
        if m == -1: return
        currentWidget = self.tabWidget.currentWidget()
        content = currentWidget.toPlainText() 
        n = self.autoSave(content)
        if (n == 0): self.closeTab(m)

    def closeTab(self, index):
        try:
            # 统计tab的总数
            tab_count = self.tabWidget.count()
            tab_now = self.tabWidget.count() -1 # 总tab关掉一个=-1
            if tab_count > 1:
                # tab>1=ok
                self.tabWidget.removeTab(index)
                self.statusBar().showMessage(f'TsukiTab✔: 成功关闭标签页,还有 {tab_now} 个Tab保留')
                logger.info(f"[Log/INFO]Close Tab: {index}")
            else:
                self.statusBar().showMessage(f'TsukiTab🚫: 无法关闭这个标签页,因为他是最后一个,如需关闭软件,请按退出软件! -注意保存您的文件')
                logger.error(f"[Log/ERROR]Close Tab Error")
        except Exception as e:
            QMessageBox.critical(self, '错误', f'发生错误：{str(e)}')
            logger.error(f"[Log/ERROR]Close Tab Error: {e}")
            self.statusBar().showMessage(f'TsukiTab❌: 关闭标签页失败！详见MessageBox！')


    def checkForUpdates(self):
        version_url = 'https://inkwhispers.us.kg/update/zwrite/version.txt'
        version = self.current_version
        try:
            response = requests.get(version_url, timeout=60)
            if response.status_code == 200:
                latest_version = response.text.strip()
                self.statusBar().showMessage(
                    f'TsukiUpdate: 检测到云端版本号为:[ {latest_version} ] | 本地版本号:[ {version} ] 开始对比...')
                logger.info(f"[Log/INFO]Check For Updates: {latest_version}")

                if latest_version == self.current_version:
                    QMessageBox.information(self, 'TsukiNotes 检测更新 | 成功 | 🔰',
                                            f'当前已经是最新版本✔: {latest_version} ！')
                    self.statusBar().showMessage(f'TsukiUpdate: 检测成功✔！您已经是最新的版本：{latest_version}')
                    logger.info(f"[Log/INFO]Check For Updates: {latest_version}")

                elif latest_version < self.current_version:
                    QMessageBox.warning(self, 'TsukiNotes',
                                        f'🚫您太超前了！云端没你更新快！！🚫')
                    self.statusBar().showMessage(f'TsukiUpdate❓: [ 当前版本号{version} > 云端{latest_version} ] 您可能不是Fv通道')
                    logger.warning(f"[Log/WARNING]Check For Updates: {latest_version}")

                elif latest_version > self.current_version:
                    reply = QMessageBox.question(self, 'TsukiNotes 检测更新 | 成功 | Successful',
                                                 f'🔰✔叮！\nTsukiNotes有全新版本啦！\n最新版本号: {latest_version}\n您的版本号: {version} \n 文件: [Tsuki Notes {latest_version}]',
                                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    self.statusBar().showMessage(f'TsukiUpdate✔: 检测成功！您有新版本：{latest_version}')
                    logger.info(f"[Log/INFO]Check For Updates: {latest_version}")

                    if reply == QMessageBox.Yes:
                        webbrowser.open(
                            'https://zstlya-my.sharepoint.com/:f:/g/personal/zz_zstlya_onmicrosoft_com/EiGVt3ZyYFZPgQu5qxsTNIQB2y0UjGvjBKMRmOfZJ-L3yg?e=iZD2iL')
                        logger.info(f"[Log/INFO]open web")
                else:
                    QMessageBox.warning(self, '检测更新',
                                        f'[未能成功检测最新版本]\n可能是你的客户端过新导致的\n我们建议您尝试手动更新！\n当前版本: {version}|云端: {latest_version}\n')
                    logger.warning(f"[Log/ERROR]Warn,Client Version So New")
            else:
                QMessageBox.warning(self, '检测更新失败',
                                    f'[无法获取版本信息]\n这可能是因为服务器掉线导致的\n当然您需要自行检测您的网络是否正常\n我们将为你启动备选方案\n请您尝试手动更新吧\n是否打开？\n ')

        except Exception as e:
            QMessageBox.critical(self, '检测更新|错误',
                                 f'出错啦！ \nOccurred:\n{str(e)}\n 请关闭您的VPN或加白inkwhispers.us.kg\n 或者尝试手动更新吧')
            logger.error(f"[Log/ERROR]Check For Updates Error: {e}")
            self.statusBar().showMessage(f'TsukiUpdate❌: 检测失败！')

    def url_msg(self):
        version_url = 'https://inkwhispers.us.kg/tn/update.txt'
        versiongj = self.version_gj
        versiontime = self.update_Date
        version = self.current_version
        versiontd = self.version_td

        try:
            response = requests.get(version_url, timeout=60)
            if response.status_code == 200:
                latest_version = response.text.strip()
                self.statusBar().showMessage(f'TsukiUpdate✔: 检测成功！云端版本号为:[ {latest_version} ] 服务器状态：正常')
                logger.info(f"[Log/INFO]Check For Updates: {latest_version}")
                QMessageBox.information(self, 'TSUKI_BACK—Information',
                                        f' 返回成功\n 云端Version: {latest_version} ！\n 服务器：正常')
                self.statusBar().showMessage(f'TsukiBack✔：云端返回数值：{latest_version}')


        except:
            url_text = (f"<h1> TsukiNotes </h1>"
                        f"<p><strong>目标: {version_url} </strong></p>"
                        f"<p><strong>结果：检测失败！！ </strong></p>"
                        f"<p><strong>本地: Version = {version} </strong></p>"
                        f"<p><strong>类型: {versiontd} </strong></p>"
                        f"<p><strong>日期: {versiontime}</strong></p>"
                        f"<p><strong>内部: {versiongj}</strong></p>"
                        f"<p><strong>联系: zzbuaoye@gmail.com </strong></p>")

            QMessageBox.about(self, "TsukiBack", url_text)
            self.statusBar().showMessage(f'TsukiUpdate❌🚫: 检测失败！请尝试关闭VPN测试[有可能是服务器寄了]')
            logger.error(f"[Log/ERROR]Check For Updates Error")

    def Show_Auto_Update2(self):
        current_version = self.current_version
        self.statusBar().showMessage(f'TsukiUpdate :请[更新->> 自动检测更新]|您的版本：{current_version}|')

    def update2(self):
        msgBox = QMessageBox()
        version = self.current_version
        msgBox.setWindowTitle(f"检测更新 | 您的版本Ver{version} | TsukiNotes&Inkwhispers")
        msgBox.setText(
            f"Hey,您现在使用的是：\n[备用]更新方案\n[推荐🔰]自动检测\nVPN用户请将[www.inkwhispers.us.kg/inkwhispers.us.kg]加入您的白名单\nVersion:{version}\nTsukiNotes&Inkwhispers 2024")
        self.statusBar().showMessage(f'TsukiUpdate[2]: 您已选择了手动更新 ')
        self.update2Act = QAction('Update', self)
        self.update2Act.triggered.connect(self.update2)
        yesButton = QPushButton("下载源1-OD")
        source2Button = QPushButton("下载源2-123")
        websiteButton = QPushButton("官网-Inkwhispers")
        newversionButton = QPushButton("官网版本对照🔰")
        cancelButton = QPushButton("取消")

        msgBox.addButton(yesButton, QMessageBox.YesRole)
        msgBox.addButton(source2Button, QMessageBox.YesRole)
        msgBox.addButton(websiteButton, QMessageBox.YesRole)
        msgBox.addButton(cancelButton, QMessageBox.NoRole)
        msgBox.addButton(newversionButton, QMessageBox.YesRole)

        clickedButton = msgBox.exec_()

        if msgBox.clickedButton() == yesButton:
            webbrowser.open(
                'https://zstlya-my.sharepoint.com/:f:/g/personal/zz_zstlya_onmicrosoft_com/EiGVt3ZyYFZPgQu5qxsTNIQB2y0UjGvjBKMRmOfZJ-L3yg?e=iZD2iL')
            self.statusBar().showMessage(f'TsukiUpdate[2]✔: 您已选择OneDrive下载源！已经为您跳转至浏览器')
            logger.info(f"[Log/INFO]Open Web {webbrowser.open}")
        elif msgBox.clickedButton() == source2Button:
            webbrowser.open('https://www.123pan.com/s/ZhtbVv-gagV3.html')
            self.statusBar().showMessage(f'TsukiUpdate[2]✔: 您已选择123Pan下载源！已经为您跳转至浏览器')
        elif msgBox.clickedButton() == websiteButton:
            webbrowser.open('https://inkwhispers.us.kg/')
            self.statusBar().showMessage(f'TsukiUpdate[2]✔: 您已选择浏览Inkwhispers！已经为您跳转至浏览器')
            logger.info(f"[Log/INFO]Open Web {webbrowser.open}")
        elif msgBox.clickedButton() == newversionButton:
            webbrowser.open('https://inkwhispers.us.kg/tn/update.txt')
            logger.info(f"[Log/INFO]Open Web {webbrowser.open}")
        elif msgBox.clickedButton() == cancelButton:
            self.statusBar().showMessage(f'TsukiUpdate[2]🚫: 您已取消操作')
            logger.info(f"[Log/INFO]UserChannel")
            pass

    def versionnow(self):
        version = self.current_version
        QMessageBox.information(self, '当前版本', f'当前版本：[ {version} ]')
        self.statusBar().showMessage(f'✔叮叮！检测成功！您当前版本为：{version}')
        logger.info(f"[Log/INFO]Open VersionNow.def look New Version\n")

    def aboutMessage(self):
        current_version = self.current_version
        versiongj = self.version_gj
        about_text = "<h1> TsukiNotes </h1><p><strong>BY ZZBuAoYe 2024</p></strong><strong><p>Inkwhispers | " \
                     f"{current_version} FullVersion</strong></p>"
        QMessageBox.about(self, f"About TsukiNotes | #{versiongj}", about_text)
        self.statusBar().showMessage(f'TsukiBack✔: 您打开了AboutMessage')
        logger.info(f"[Log/INFO]Open AboutMessage.def look New Version\n")

    def aboutDetails(self):
        versiongj = self.version_gj
        about_text = f"[软件信息]\n | 软件出品:MoonZZ \n | 时间：{self.update_Date}\n | {self.version_td} \nInkwhispers&ZZBuAoYe 2024©Copyright\nInkwhispers.us.kg"
        QMessageBox.about(self, f"AboutSoftWare | #{self.version_gj}", about_text)
        self.statusBar().showMessage(f'TsukiINFO: [{versiongj}] | [{self.version_td}] | [{self.update_Date}] ')
        logger.info(f"[Log/INFO]Open AboutDetails.def\n")

    def updateMessage(self):
        version = self.current_version  # 版本
        versiontime = self.version_gj  # gj是内部版本号
        version_td = self.version_td  # 通道
        update_time = self.update_Date  # 更新时间

        update_text = (
            "<html>"
            "<h2 style='text-align: left;'>| TsukiNotes Update Information🛠</h2>"
            f"<p style='text-align: center;'>Version:{version} {version_td}[{update_time}]</p>"
            "</html>"
            f"======================================================================================<br>"
            f" [质量]1.优化背景图<br>"
            f" [优化]2.优化OpenFile<br>"
            f" [修复]3.OpenFile打开文件后字体全部失效<br>"
            f" [测试]4.Config修复,新增用户快捷切换背景图[测试][不保存cfg]<br>"
            f" [优化]5.优化项目结构，使Assets更加规整<br>"
            f" [优化]6.优化多个函数<br>"
            f" [修复]7.修复已知bug<br>"
            f" [修复]8.解决多处调用不协调<br>"
            f" [删减]9.删除老的代码，废弃部分工程<br>"
            f" [新增]10.修正背景图save函数无法保存cfg的问题<br>"
            f" [新增]11.修改default背景图<br>"
            f" [优化]12.设置页面全局Microsoft YaHei提升观感<br>"
            f" [优化]13.日志删除算法<br>"
            f"======================================================================================<br>"
            f"<p style='text-align: center;'> || FullVersion ||</p>"
            f"<p style='text-align: center;'>[内部版本号:{versiontime}]</p>"
        )
        dialog = QDialog(self)
        dialog.setWindowTitle(f"TsukiNotes[{version}]更新日志 -Ver{version}{version_td}")
        dialog.resize(600, 300)

        layout = QVBoxLayout(dialog)
        label = QLabel()
        label.setTextFormat(Qt.RichText)
        label.setText(update_text)
        layout.addWidget(label)
        label_font = QFont('Microsoft YaHei UI')  # 设置微软雅黑
        label.setFont(label_font)
        label.setAlignment(Qt.AlignLeft)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(dialog.accept)
        layout.addWidget(button_box)

        dialog.exec_()
        self.statusBar().showMessage('TsukiBack✔: 您打开了本地更新日志')
        logger.info(f"[Log/INFO]Open Update Informathion Succeed")

    def online_updateMessage(self):
        try:
            current_version = self.current_version
            online_update = 'https://inkwhispers.us.kg/tn/update.txt'
            now_version_url = 'https://www.inkwhispers.us.kg/tn/version.txt'

            response = requests.get(online_update, timeout=60)
            response.raise_for_status()  # 检查响应是否成功
            update_text = response.text
            logger.info(f"[Log/INFO]Get update.txt Succeed " + f"{online_update}\n")
            now_version_response = requests.get(now_version_url, timeout=60)
            now_version_response.raise_for_status()
            now_version = now_version_response.text.strip()

            if version.parse(current_version) < version.parse(now_version):
                update_text += "\n== == == == == == Tips == == == == == ==\n 您的版本可能太低了，并不适用该更新内容 \n "
                QMessageBox.about(self, f"TsukiNotes更新日志 -Ver {current_version} FullVersion", update_text)
                logger.info(f"[Log/INFO]Parse version RESULT:" + f"{current_version} < {now_version}\n")
            elif version.parse(current_version) == version.parse(now_version):
                update_text += f"\n== == == == == == 当前版本 == == == == == ==\n 您的版本可以适用该更新日志 \n"
                QMessageBox.about(self, f"TsukiNotes更新日志 -Ver {current_version} FullVersion", update_text)
                self.statusBar().showMessage(f'TsukiBack✔: 您打开了更新日志，获取目标在线日志ing...')
                logger.info(f"[Log/INFO]Open UpdateMsg Succeed,RESULT:" + f"{current_version} = {now_version}")
            else:
                QMessageBox.warning(self, "TsukiNotes更新日志",
                                        f" 更新日志获取失败！\n 请求网址： {online_update}\n 请您尝试查看离线日志\n 10秒内请勿再次尝试")
                self.statusBar().showMessage(f"TsukiBack❌: 更新日志获取失败！[目标：{online_update}]")
                logger.info(f"[Log/INFO]Error!")

        except requests.Timeout:
            QMessageBox.warning(self, "TsukiNotes更新日志", " 请求超时，请检查您的网络连接并重试。")
            self.statusBar().showMessage(f"TsukiBack❌: 请求超时，更新日志获取失败！")
            logger.info(f"[Log/INFO]Error!")
        except requests.RequestException as e:
            QMessageBox.warning(self, "TsukiNotes更新日志", f" 更新日志获取失败！[{e}]\n 请尝试查看离线本地日志")
            self.statusBar().showMessage(f"TsukiBack❌: 更新日志获取失败！[{e}]")
            logger.info(f"[Log/INFO]Error!")
        except Exception as e:
            QMessageBox.warning(self, "TsukiNotes更新日志", f" 发生异常!\n 请查看具体错误信息并进行修复\n错误内容请通过cmd Debug")
            self.statusBar().showMessage(f"TsukiBack❌: 更新日志获取失败！[{e}]")
            logger.info(f"[Log/INFO]Error!",e)

    def renameTab(self, index):
        tab_name, ok = QInputDialog.getText(self, '重命名', '新的名称:')
        if ok and tab_name:
            self.tabWidget.setTabText(index, tab_name)
            self.statusBar().showMessage(f'TsukiNotesTab✔： 成功重命名标签页 -> [{tab_name}]')

    def mousePressEvent(self, event):
        if event.button() == 4:
            index = self.tabWidget.tabBar().tabAt(event.pos())
            if index >= 0:
                self.closeTab(index)

    def contextMenuEvent(self, event):
        index = self.tabWidget.tabBar().tabAt(event.pos())
        if index >= 0:
            menu = QMenu(self)
            rename_action = QAction(QIcon('./tsuki/assets/GUI/resources/font_size_reset_tab.png'),'重命名标签', self)
            rename_action.triggered.connect(lambda: self.renameTab(index))
            menu.addAction(rename_action)
            menu.exec_(event.globalPos())
                

    def closeEvent(self, event):
        # 自动检测文本修改，触发自动保存机制
        currentWidget = self.tabWidget.currentWidget()
        content = currentWidget.toPlainText()  # 获取当前标签页的文本内容
        n = self.autoSave(content)
        if (n == -1): event.ignore()

    def autoSave(self, content):
        if str(self.before) == str(content):
            self.text_modified = False
        else:
            self.text_modified = True
        if self.text_modified:
            reply = QMessageBox.question(self, '退出提示🔰', '文本可能被修改❓，是否保存一小下❓',
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                n = self.performSave()
                if n == 0:
                    return 1
                else:
                    return -1
            elif reply == QMessageBox.Cancel:
                return -1
        return 0

    def cutTab(self):
        version = self.current_version
        cuttab = f"Ctrl + Z Undo \n Ctrl + Y Redo \n Ctrl + S Save \n Ctrl + F Search \n Ctrl + Shift + C Clear \n Ctrl + X Cut \n Ctrl + O Open \n Ctrl + T New Tab \n Ctrl + W Close Tab \n Inkwhispers Version:{version}FullVersion  "
        QMessageBox.information(self, "TsukiNotes Shortcut Key🔰", cuttab)

    def textChanged(self):
        self.text_modified = True

    def performSearch(self):
        self.tabWidget.setFocusPolicy(Qt.StrongFocus)
        self.tabWidget.keyPressEvent = self.keyPressEvent
        self.searching = True  # 标记为搜索中
        self.current_search_index = -1  # 当前搜索位置索引
        self.found_positions = []  # 所有搜索到的位置
        self.search_text, ok = QInputDialog.getText(self, '搜索文本', '输入要搜索的文本:')
        if ok and self.search_text:
            currentWidget = self.tabWidget.currentWidget()
            cursor = QTextCursor(currentWidget.document())
            while not cursor.isNull() and not cursor.atEnd():
                cursor = currentWidget.document().find(self.search_text, cursor)
                if not cursor.isNull():
                    self.found_positions.append(cursor.position())

            if self.found_positions:
                search_result_dialog = SearchResultDialog(
                    [f"找到关键词 '{self.search_text}' 的位置：{pos}" for pos in self.found_positions], self)
                logger.info(f"[Log/INFO]Search Result:{self.found_positions}")
                message = f'TsukiSearch✔: 查找关键词[{self.search_text}]成功！|| 所有结果：[{"、".join([str(pos) for pos in self.found_positions])}]'
                self.statusBar().showMessage(message)
                result = search_result_dialog.exec_()

                if result == QDialog.Accepted:
                    # 用户点击确定，将光标移到文本边上
                    cursor = QTextCursor(currentWidget.document())
                    cursor.setPosition(self.found_positions[search_result_dialog.current_index])
                    currentWidget.setTextCursor(cursor)
                    currentWidget.ensureCursorVisible()
                    pass
                else:
                    pass
            else:
                QMessageBox.information(self, '搜索结果', f'抱歉，文本内无关键字 "{self.search_text}"')
                self.statusBar().showMessage(f'TsukiSearch❌: 无关键词"{self.search_text}"')
                logger.info(f"[Log/INFO]Note Have Result{self.search_text}")
 # setting函数===================================================================
    def set_background(self):
        try:
            file_dialog = QFileDialog(self)
            file_path, _ = file_dialog.getOpenFileName(self, '选择背景图片', '', 'Images (*.png *.xpm *.jpg *.bmp *.gif)')
        
            transparency, ok = QInputDialog.getInt(self, '输入', '请输入背景透明度 (0-100):', 100, 0, 100)
            if not ok:
                transparency = 100
            
            if file_path:
                style_sheet_image = f'background-image: url("{file_path}");'
            else:
                style_sheet_image = ''
                
            style_sheet_opacity = f'opacity: {transparency / 100};'
            style_sheet = f'{style_sheet_image} {style_sheet_opacity}'
            
            current_widget = self.tabWidget.currentWidget()
            current_widget.setStyleSheet(style_sheet)
            self.save_background_settings(file_path, transparency)

            if file_path:
                QMessageBox.information(self, '提示', f'背景图片已经修改为 {file_path}，喵~')
            self.statusBar().showMessage(f'TsukiBC✔: 背景设置成功！')
            logger.info(f"[Log/INFO] Background settings applied.")

        except Exception as e:
            QMessageBox.critical(self, '错误', f'发生错误：{str(e)}')
            self.statusBar().showMessage(f'TsukiBC❌: 背景设置失败！详见MessageBox！')
            logger.error(f'[Log/ERROR] Background settings error: {str(e)}')

    def save_background_settings(self, image_path, transparency):
        settings = QSettings('TsukiReader', 'Background')
        settings.setValue('backgroundImage', image_path)
        settings.setValue('backgroundTransparency', transparency)

    def load_background_settings(self):
        try:
            settings = QSettings('TsukiReader', 'Background')
            image_path = settings.value('backgroundImage')
            transparency = settings.value('backgroundTransparency', type=int)

            if image_path and os.path.exists(image_path):
                style_sheet_image = f'background-image: url("{image_path}");'
            else:
                style_sheet_image = ''
            
            if transparency is not None:
                style_sheet_opacity = f'opacity: {transparency / 100};'
            else:
                style_sheet_opacity = 'opacity: 1;'
            
            style_sheet = f'{style_sheet_image} {style_sheet_opacity}'
            
            current_widget = self.tabWidget.currentWidget()
            current_widget.setStyleSheet(style_sheet)
            
            if image_path:
                self.statusBar().showMessage(f'TsukiBC✔: 成功加载背景图片 {image_path}！')
                logger.info(f"[Log/INFO] Background Image Loaded: {image_path}")
            else:
                self.statusBar().showMessage(f'TsukiBC❓: 未找到保存的背景图片设置或图片不存在。')
                logger.warning(f"[Log/WARNING] Background Image Not Found or Not Set.")

        except Exception as e:
            self.statusBar().showMessage(f'TsukiBC❌: 未找到保存的背景设置或加载失败。')
            logger.error(f'[Log/ERROR] Background Settings Load Error: {str(e)}')


    def reset_background_color(self):
        config = configparser.ConfigParser()
        default_image_path = './tsuki/assets/app/default/default_light.png'
        config_path = 'tsuki/assets/app/cfg/background/background_color.ini'

        try:
            config.read(config_path)
            image_path = config['Background'].get('image_path', default_image_path)

            if image_path and os.path.exists(image_path):
                style_sheet_image = f'background-image: url("{image_path}");'
                message = f'成功加载背景图片 {image_path}！'
            else:
                image_path = default_image_path
                style_sheet_image = f'background-image: url("{image_path}");'
                message = f'背景图片不存在，加载默认背景图片 {image_path}！'

            current_widget = self.tabWidget.currentWidget()
            current_widget.setStyleSheet(style_sheet_image)
            self.statusBar().showMessage(f'TsukiBC✔: {message}')
            logger.info(f"[Log/INFO] {message}")

            config['Background'] = {'image_path': image_path}
            with open(config_path, 'w') as configfile:
                config.write(configfile)

        except Exception as e:
            self.statusBar().showMessage(f'TsukiBC❌: 未找到保存的背景色设置或加载失败。')
            logger.error(f"[Log/ERROR] Background Color Load Error: {str(e)}")

    def save_background_color(self, bg_color, text_color):
        try:
            config = configparser.ConfigParser()
            config['Background'] = {
                'color': bg_color,
                'text_color': text_color,
                'image_path': './tsuki/assets/app/default/default_light.png'

            }
        
            os.makedirs('tsuki/assets/app/cfg', exist_ok=True)
            with open('tsuki/assets/app/cfg/background/background_color.ini', 'w') as configfile:
                config.write(configfile)
                logger.info(f"[Log/INFO]Background Color Saved:{bg_color}")
        except Exception as e:
            QMessageBox.critical(self, '错误', f'保存背景色设置时发生错误：{str(e)}')
            self.statusBar().showMessage(f'TsukiBC_Save❌: 背景色设置保存失败！')
            logger.error(f"[Log/ERROR]Background Color Save Error:{str(e)}")

    def clearTempFolder(self):
        temp_folder = 'tsuki/assets/app/temp'
        try:
            if os.path.exists(temp_folder):
                shutil.rmtree(temp_folder)
            os.makedirs(temp_folder)
            self.statusBar().showMessage('TsukiBG✔: 临时文件夹已清空！')
            logger.info(f"[Log/INFO]Temp Folder Cleared:{temp_folder}")
        except Exception as e:
            QMessageBox.critical(self, '清空临时文件夹', f'失败了❌❗: {str(e)}')
            self.statusBar().showMessage(f'TsukiBG❌: 清空临时文件夹失败！原因:{str(e)}')
            logger.error(f"[Log/ERROR]Temp Folder Clear Error:{str(e)}")
            
    def setBackgroundImageFromFile(self, file_name):
        try:
            pixmap = QPixmap(file_name)
            palette = QPalette()
            palette.setBrush(QPalette.Background, QBrush(pixmap))
            self.setPalette(palette)
            self.statusBar().showMessage(f'TsukiBG✔: 背景图片已成功设置！')
            logger.info(f"[Log/INFO]Background Image Set:{file_name}")
        except Exception as e:
            QMessageBox.critical(self, '设置背景图片', f'失败了❌❗: {str(e)}')
            self.statusBar().showMessage(f'TsukiBG❌: 背景图片设置失败！原因:{str(e)}')
            logger.error(f"[Log/ERROR]Background Image Set Error:{str(e)}")

    def setBackgroundImage(self):
        file_name, _ = QFileDialog.getOpenFileName(self, '选择背景图片[内测]', '',
                                                   'Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)')

        if not file_name:
            return
        self.setBackgroundImageFromFile(file_name)
        self.saveBackgroundSettings(file_name)

    def loadBackgroundSettings(self):
        self.config_path = "./tsuki/assets/app/cfg/background/TN_BackGround.ini"
        self.default_background_path = "./tsuki/assets/app/default/default_light.png"
        if not os.path.exists(self.config_path):
            self.saveBackgroundSettings(self.default_background_path)

        config = configparser.ConfigParser()
        config.read(self.config_path)
        logger.info(f"[Log/INFO]Background Settings Loaded:{self.config_path}")

        if 'Background' in config:
            background_path = config['Background'].get('ImagePath', self.default_background_path)
            transparency = config['Background'].getint('Transparency', 100)
            logger.info(f"[Log/INFO]Background Settings Loaded:{background_path}")

            if background_path and os.path.exists(background_path):
                pixmap = QPixmap(background_path)
                palette = QPalette()
                palette.setBrush(QPalette.Background, QBrush(pixmap))
                self.setPalette(palette)
                self.statusBar().showMessage(f'背景图片 [{background_path}] 已加载')
                logger.info(f"[Log/INFO]Background Settings Loaded:{background_path}")
            else:
                # 如果背景图不存在，使用默认背景图
                pixmap = QPixmap(self.default_background_path)
                palette = QPalette()
                palette.setBrush(QPalette.Background, QBrush(pixmap))
                self.setPalette(palette)
                self.statusBar().showMessage(f'背景图片 [{self.default_background_path}] 已加载')
                logger.info(f"[Log/INFO]Background Settings Loaded:{self.default_background_path}")


    def saveBackgroundSettings(self, image_path, transparency=100,image_path2='./Tsuki/assets/app/default/default_light.png'):
        config_path = "tsuki/assets/app/cfg/background/TN_BackGround.ini"
        config = configparser.ConfigParser()
        config['Background'] = {
            'ImagePath': image_path,
            'Transparency': transparency,
            'image_path': image_path2
        }

        os.makedirs(os.path.dirname(config_path), exist_ok=True)

        with open(config_path, 'w') as configfile:
            config.write(configfile)
                    
    def initialize_font_size(self):
        try:
            # 设置默认的字体大小
            default_font_size = 12
            current_widget = self.tabWidget.currentWidget()
            current_font = current_widget.font()
            current_font.setPointSize(default_font_size)
            current_widget.setFont(current_font)

            QMessageBox.information(self, '提示', f'字体大小已经重置为默认值 {default_font_size}，喵~')
            self.statusBar().showMessage(f'TsukiFS✔: 字体大小已重置为默认值 {default_font_size}')
        except Exception as e:
            QMessageBox.critical(self, '错误', f'发生错误：{str(e)}')
            self.statusBar().showMessage(f'TsukiFS✔: 字体大小初始化失败！详见MessageBox！')
            logger.error(f"[Log/ERROR]Font Size Initialization Failed:{str(e)}")

    def re_icon_setting(self):
        def download_and_set_icon(url, target_path):
            try:
                response = requests.get(url)
                response.raise_for_status()
                target_directory = os.path.dirname(target_path)
                if not os.path.exists(target_directory):
                    os.makedirs(target_directory)
                with open(target_path, 'wb') as f:
                    f.write(response.content)
                return True
            except Exception as e:
                QMessageBox.warning(self, '错误下载', f"开香槟，下载失败咯，错误代码:\n {str(e)}")
                logger.error(f"[Log/ERROR]Icon Download Failed:{str(e)}")
                return False
        status_bar = self.statusBar()
        icon_path = "tsuki/assets/ico/logo.ico"
        download_url = "https://download.inkwhispers.us.kg/tn/download/logo.ico"
        alt_download_url = "https://www.mooncn.link/update/tsuki/logo.ico"
        manual_download_url = "https://www.123pan.com/s/ZhtbVv-plgV3.html"
        if ctypes.windll.shell32.IsUserAnAdmin():
            # 如果用户是管理员
            if download_and_set_icon(download_url, icon_path) or download_and_set_icon(alt_download_url, icon_path):
                status_bar.showMessage('ICON Setting Succeeded')
                QMessageBox.information(self, 'LOADING', 'New Icon Set......')
                logger.info("[Log/INFO]Icon Setting Succeeded")
                icon = QIcon(icon_path)
                self.setWindowIcon(icon)
                self.updateStatusLabel()
            else:
                response = QMessageBox.warning(self, 'Download Failed', '自动下载失败，是否手动下载并替换？', QMessageBox.Yes | QMessageBox.No)
                if response == QMessageBox.Yes:
                    manual_download_path, _ = QFileDialog.getSaveFileName(self, '手动下载并替换', '', 'Icon Files (*.ico)')
                    if manual_download_path:
                        if download_and_set_icon(manual_download_url, manual_download_path):
                            QMessageBox.information(self, 'Manual Download Success', '手动下载并替换成功')
                            logger.info("[Log/INFO]Manual Download Success")
                            icon = QIcon(manual_download_path)
                            self.setWindowIcon(icon)
                            self.updateStatusLabel()
                        else:
                            QMessageBox.warning(self, 'Manual Download Failed', '手动下载并替换失败')
                            logger.error("[Log/ERROR]Manual Download Failed")
        else:
            QMessageBox.warning(self, 'Permission Denied', '需要管理员权限来移动文件，请以管理员身份运行程序！')
            logger.error("[Log/ERROR]Permission Denied:Need Admin Permission")
            return
    def diy_icon_setting(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        icon_diy_path, _ = QFileDialog.getOpenFileName(self, '自定义ICON[测试]', '', 'Icon Files (*.ico);;All Files (*)', options=options)

        if not icon_diy_path:
            status_bar = self.statusBar()
            QMessageBox.warning(self, 'File Not Found文件未找到', '未选择文件或选择无效文件路径！')
            status_bar.showMessage(f'TsukiIS🚫: 您未选择任何文件或选择了无效的文件路径！')
            logger.error("[Log/ERROR]File Not Found:File Not Found")
            return

        # 确保用户是管理员
        if not ctypes.windll.shell32.IsUserAnAdmin():
            QMessageBox.warning(self, 'Permission Denied', '需要管理员权限来移动文件，请以管理员身份运行程序！\n Error:{e}')
            logger.error("[Log/ERROR]Permission Denied:Need Admin Permission")
            return

        target_directory = os.path.join('tsuki', 'assets', 'icon')

        # 如果目录不存在那就建一个
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)
        target_path = os.path.join(target_directory, 'logo.ico')
        try:
            shutil.move(icon_diy_path, target_path)
            status_bar = self.statusBar()
            status_bar.showMessage(f'TsukiIS: 自定义图标设置成功[{target_path}]')
            logger.info("[Log/INFO]Custom Icon Set Successfully")
            message_box = QMessageBox()
            message_box.setWindowTitle('自定义ICON[测试]:')
            message_box.setText('Icon set successfully\n新的图标设置成功！')
            logger.info("setting succeed")
            font = QFont("Microsoft YaHei", 12)
            message_box.setFont(font)
            message_box.setIcon(QMessageBox.Information)
            message_box.exec_()
            icon = QIcon(target_path)
            self.setWindowIcon(icon)
            self.updateStatusLabel()
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'An error occurred: {str(e)}')
            logger.error(f"[Log/ERROR]Custom Icon Set Failed:{str(e)}")

    def iconpath_check_a1(self):
        icon_path = "tsuki/assets/ico/logo.ico"
        icon2_path = "tsuki/assets/old_logo.ico"

        if not os.path.exists(icon_path):
            QMessageBox.warning(self, '提示',
                                f'错误提示: {icon_path} 并没被成功引用，但是这并不会影响实际使用！只是会导致icon处变成默认的样子\n{icon2_path}正在寻找！')
            self.statusBar().showMessage(f'TsukiAssets❓: 您的assets中缺少了来自: {icon_path} 的logo.ico 但是这并不会影响实际使用')
            logger.warning(f"[Log/WARNING]Missing Icon:{icon_path}")
        if not os.path.exists(icon2_path):
            QMessageBox.warning(self, '提示',
                                '您的assets中缺少了old_logo.ico\n注意：这完全不会影响只是提醒您您可能缺少了东西，您可以自行核对！')
            self.statusBar().showMessage(f'TsukiAssets: 您的assets中缺少了 {icon2_path} 但是这并不会影响实际使用')
            logger.warning(f"[Log/WARNING]Missing Icon:{icon2_path}")

        else:
           checkmsg = (f'恭喜， {icon_path}和{icon2_path}都正常')
           QMessageBox.about(self, 'Tips:', checkmsg)
           self.statusBar().showMessage(f'TsukiAssets✔: 您的assets看上去并没被删减！')
           logger.info("[Log/INFO]Icon Check Succeeded")

    def total_setting(self):
        try:
            dialog = QDialog(self)
            dialog.setWindowTitle("统计设置")
            layout = QVBoxLayout(dialog)

            checkbox_include_whitespace = QCheckBox("包括空白字符")
            checkbox_include_whitespace.setChecked(self.include_whitespace)
            layout.addWidget(checkbox_include_whitespace)

            label_custom_lines = QLabel("自定义显示行数[0为自动][不可用]：")
            layout.addWidget(label_custom_lines)
            self.line_edit_custom_lines = QLineEdit()

            self.line_edit_custom_lines.setText(str(self.custom_lines))
            layout.addWidget(self.line_edit_custom_lines)

            checkbox_highlight_keywords = QCheckBox("启用关键字高亮")
            checkbox_highlight_keywords.setChecked(self.highlight_keywords) 
            checkbox_highlight_keywords.stateChanged.connect(self.toggle_highlight_keywords)
            layout.addWidget(checkbox_highlight_keywords)

            button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            button_box.accepted.connect(dialog.accept)
            button_box.rejected.connect(dialog.reject)
            layout.addWidget(button_box)

            result = dialog.exec_()

            include_whitespace = checkbox_include_whitespace.isChecked()
            custom_lines = int(self.line_edit_custom_lines.text())
            highlight_keywords = checkbox_highlight_keywords.isChecked()

            self.saveSettings(include_whitespace, custom_lines, highlight_keywords)
            self.applySettings(include_whitespace, custom_lines)
            if highlight_keywords:
                self.addKeywordHighlight()

        except Exception as e:
            QMessageBox.critical(self, '错误', f'发生异常：{str(e)}')
            self.statusBar().showMessage(f'TsukiTotalSetting❌: 发生异常：{str(e)}')
            logger.error(f"[Log/ERROR]Total Setting Failed:{str(e)}")

    def toggle_highlight_keywords(self, state):
        if state == Qt.Checked:
            self.highlight_keywords = True
        else:
            self.highlight_keywords = False
        self.addKeywordHighlight()

    def saveSettings(self, include_whitespace, custom_lines, highlight_keywords):
        try:
            ini_dir = os.path.join('tsuki', 'assets', 'app', 'cfg', 'app_settings')
            ini_path = os.path.join(ini_dir, 'total_settings.ini')
            os.makedirs(ini_dir, exist_ok=True)
            config = configparser.ConfigParser()
            config['Settings'] = {}
            config['Settings']['include_whitespace'] = str(include_whitespace)
            config['Settings']['custom_lines'] = str(custom_lines)
            config['Settings']['highlight_keywords'] = str(highlight_keywords)
            with open(ini_path, 'w') as configfile:
                config.write(configfile)
        except Exception as e:
            QMessageBox.critical(self, '错误', f'保存设置时发生异常：{str(e)}')
            self.statusBar().showMessage(f'TsukiSave❌: 保存设置时发生异常：{str(e)}')
            logger.error(f"[Log/ERROR]Save Settings Failed:{str(e)}")

    def applySettings(self, include_whitespace, custom_lines):
        try:
            current_widget = self.tabWidget.currentWidget()
            current_font = current_widget.font()

            default_font_size = 11
            current_font.setPointSize(default_font_size)

            if custom_lines == 0:
                current_widget.setLineWrapMode(QPlainTextEdit.WidgetWidth)
            else:
                current_widget.setLineWrapMode(QPlainTextEdit.FixedPixelWidth)
                current_widget.setFixedHeight(current_widget.fontMetrics().lineSpacing() * custom_lines)

            # 应用修改后的字体
            current_widget.setFont(current_font)
        except Exception as e:
            QMessageBox.critical(self, '错误', f'应用设置时发生异常：{str(e)}')
            self.statusBar().showMessage(f'TsukiApplySetting❌: 应用设置时发生异常：{str(e)}')
            logger.error(f"[Log/ERROR]Apply Settings Failed:{str(e)}")

    def addKeywordHighlight(self):
        try:
            current_widget = self.tabWidget.currentWidget()
            self.highlighter = PythonHighlighter(self.highlight_keywords, current_widget.document())
        except Exception as e:
            QMessageBox.critical(self, '错误', f'添加关键字高亮时发生异常：{str(e)}')
            self.statusBar().showMessage(f'添加关键字高亮时发生异常：{str(e)}')
            logger.error(f"[Log/ERROR]Add Keyword Highlight Failed:{str(e)}")

    def reset_background(self):
        file_path = './tsuki/assets/app/cfg/background/TN_BackGround.ini'
        config = configparser.ConfigParser()
        filename = "TN_BackGround.ini"
        defaultimage = "./tsuki/assets/app/default/default_light.png"
        if os.path.exists(file_path):
            config.read(file_path)
            if 'Background' not in config.sections():
                config.add_section('Background')
            config.set('Background', 'imagepath', './tsuki/assets/app/default/default_light.png')
            with open(file_path, 'w') as configfile:
                config.write(configfile)
            msg_box = QMessageBox()
            msg_box.setWindowTitle("重置完成[Path]")
            msg_box.setText(f"背景已重置!{file_path}\n{filename}内imagepath已被重置为默认图片{defaultimage}\n操作成功!\n")
            logger.info("Reset Background Succeed!")
            msg_box.setIconPixmap(QIcon('./tsuki/assets/GUI/resources/done.png').pixmap(64, 64))  # 设置自定义图标
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()
            self.setBackgroundImageFromFile('./tsuki/assets/app/default/default_light.png')

        else:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("提示")
            msg_box.setText("你还没设置背景图")
            msg_box.setIconPixmap(QIcon('./tsuki/assets/GUI/resources/tips.png').pixmap(64, 64))  # 设置自定义图标
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()

    def select_and_set_background(self):
        from datetime import datetime
        user_folder = './tsuki/assets/app/default/User_File/'
        image_files = [f for f in os.listdir(user_folder) if f.endswith('.png') or f.endswith('.jpg')]
        if not image_files:
            self.show_message_box("提示", "没有找到任何图片文件。", 'tips.png')
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("选择背景图片")
        layout = QVBoxLayout(dialog)

        list_widget = QListWidget()
        for idx, image_file in enumerate(image_files):
            item = QListWidgetItem(f"{image_file} (ID: {idx})")
        # 转换时间戳为可读的日期字符串
            mod_time = datetime.fromtimestamp(os.path.getmtime(os.path.join(user_folder, image_file)))
            item.setToolTip(mod_time.strftime('%Y-%m-%d %H:%M:%S'))
            list_widget.addItem(item)
        layout.addWidget(list_widget)

        select_button = QPushButton("选择并设置背景")
        select_button.clicked.connect(lambda: self.set_selected_background(list_widget, user_folder))
        layout.addWidget(select_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def set_selected_background(self, list_widget, user_folder):
        selected_items = list_widget.selectedItems()
        if not selected_items:
            self.show_message_box("提示", "请先选择一个图片。", 'tips.png')
            return

        selected_image = selected_items[0].text().split(' (ID: ')[0]
        image_path = os.path.join(user_folder, selected_image)
        self.update_background_config(image_path)
        self.show_message_box("设置成功", f"背景图片已设置为 {image_path}", 'done.png')

    def update_background_config(self, image_path):
        config_path = './tsuki/assets/app/cfg/BackGround/background_color.ini'
        config = configparser.ConfigParser()
        config.read(config_path)
        if 'Background' not in config.sections():
            config.add_section('Background')
        config.set('Background', 'image_path', image_path)
        with open(config_path, 'w') as configfile:
            config.write(configfile)
        self.setBackgroundImageFromFile(image_path)

    def show_message_box(self, title, text, icon):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setIconPixmap(QIcon(f'./tsuki/assets/GUI/resources/{icon}').pixmap(64, 64))
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
    
    # setting函数End==============================================================

    def performSave(self):
        # 标记文本已保存
        self.text_modified = False
        options = QFileDialog.Options()
        filters = "All Files (*);;Text Files (*.txt);;Markdown Files (*.md);;INI Files (*.ini);;XML Files (*.xml);" \
                  "JSON Files (*.json);;Log Files (*.log);;Python Files (*.py);;C Files (*.c)"
        fileName, _ = QFileDialog.getSaveFileName(self, 'Save tsuki File', '', filters, options=options)
        if fileName:
            currentWidget = self.tabWidget.currentWidget()
            text = currentWidget.toPlainText()
            with open(fileName, 'w', encoding='utf-8') as file:
                file.write(text)
                QMessageBox.information(self, '保存成功', f'文件 "{fileName}" 保存成功')
                self.statusBar().showMessage(f'TsukiSave❌: 文件 "{fileName}" 保存成功')
                logger.info(f"[Log/INFO]Save File Success:{fileName}")
            return 0
        return -1

    def pastePlainText(self):
        clipboard = QApplication.clipboard()
        mime_data = clipboard.mimeData()

        if mime_data.hasText():
            plain_text = mime_data.text()
            self.text_edit.insertPlainText(plain_text)

    def performClear(self):
        currentWidget = self.tabWidget.currentWidget()
        self.statusBar().showMessage('"Tsuki✔: 您执行了一次清空操作"')
        logger.info(f"[Log/INFO]Clear File Success:{currentWidget.fileName()}")
        currentWidget.clear()

    def performUndo(self):
        currentWidget = self.tabWidget.currentWidget()
        currentWidget.undo()
        self.statusBar().showMessage('"Tsuki✔: 您执行了一次撤销操作"')
        logger.info(f"[Log/INFO]Undo File Success:{currentWidget.fileName()}")

    def performRedo(self):
        currentWidget = self.tabWidget.currentWidget()
        currentWidget.redo()

    def performCut(self):
        currentWidget = self.tabWidget.currentWidget()
        currentWidget.cut()

    def extractPingDelay(self, ping_output):
        lines = ping_output.split('\n')
        for line in lines:
            if '时间=' in line and 'ms' in line:
                # 找到 "时间=" 和 "ms" 所在的位置
                start_index = line.find('时间=') + len('时间=')
                end_index = line.find('ms', start_index)

                # 提取时间字段
                time_str = line[start_index:end_index].strip()

                try:
                    return float(time_str)
                except ValueError:
                    return None
        return None

    def pingServerManually(self):
        try:
            ping_host1 = 'www.mooncn.link'
            ping_host2 = 'inkwhispers.us.kg'

            delays = self.runPingCommand(ping_host1, ping_host2)

            self.handlePingResult(delays, ping_host1, ping_host2)
        except Exception as e:
            self.handlePingError(str(e))
    def runPing(self, ping_host):
        try:
            ipaddress.ip_address(ping_host)
            # 主机为IPv6
            command = ['ping', '-6', '-n', '1', ping_host]
        except ValueError:
            # 主机为IPv4
            command = ['ping', '-n', '1', ping_host]

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                creationflags=subprocess.CREATE_NO_WINDOW)

        if result.returncode == 0:
            delay = self.extractPingDelay(result.stdout)
            return delay
        else:
            return None


    def runPingCommand(self, ping_host1, ping_host2):
        result1 = self.runPing(ping_host1)
        result2 = self.runPing(ping_host2)

        return result1, result2

    def handlePingResult(self, delays, ping_host1, ping_host2):
        top_delay, link_delay = delays  # 获取每个主机的延迟

        currentWidget = self.tabWidget.currentWidget()

        if top_delay is not None:
            top_info = f'TsukiPingBack - {ping_host1}: {top_delay} ms'
            color_style_top = self.getColorStyle(top_delay)
            currentWidget.setStyleSheet(f"font-color: {color_style_top}")
            self.statusBar().showMessage(top_info)
        else:
            self.handlePingError(f"Unable to ping {ping_host1}.")

        if link_delay is not None:
            link_info = f'TsukiPingBack - {ping_host1}: {top_delay}ms| {ping_host2}: {link_delay} ms'
            color_style_link = self.getColorStyle(link_delay)
            # currentWidget.setheet(f"font-color: {color_style_link}") # 封印
            self.statusBar().showMessage(link_info)
        else:
            self.handlePingError(f"Unable to ping {ping_host2}.")
            logger.error(f"[Log/ERROR]PingServerManually")

    def handlePingError(self, error_message):
        ping_host1 = 'www.mooncn.link'
        ping_host2 = 'inkwhispers.us.kg'

        server_names = [f'Tsuki Back：{ping_host1}', f'Tsuki Back：{ping_host2}']
        for server_name in server_names:
            self.statusBar().showMessage(f'TsukiCheck❓: {server_name} 服务器很可能不在线！Tips：如有请关闭VPN')

        QMessageBox.warning(self, 'PingServerManually | 失败原因报告',
                            f'我很抱歉您的检测失败了 \n 在此之前您需要知道的内容：\n | 检测时禁止使用VPN \n | 检测时可能会未响应，不必担心这是暂时的 \n 您的报错：{error_message} | Powered By MoonCN&TsukiNotes')
        logger.error(f"[Log/ERROR]PingServerManually | 失败原因报告:{error_message}")
    def getColorStyle(self, delay):
        if delay > 150:
            return 'red'
        elif delay > 100:
            return 'yellow'
        else:
            return 'green'


if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    main_window = TsukiReader()
    main_window.show()
    
    sys.exit(app.exec_())
