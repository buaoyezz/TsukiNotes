# -*- coding: utf-8 -*-
import sys
import ctypes
import markdown2
import markdown
import traceback
from markdown2 import markdown as md_to_html
import html2text
from html2text import html2text 
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
import colorlog
from datetime import datetime
from socket import socket
from turtle import color, pos
from packaging import version
import ping3
from PyQt5.QtGui import (
    QFont, QIcon, QTextCharFormat, QColor, QTextCursor, QKeySequence, QSyntaxHighlighter,
    QPixmap, QPalette, QBrush, QPainter
)
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QFontDialog,
    QTabWidget, QInputDialog, QMenu, QMessageBox, QPushButton, QShortcut,
    QLabel, QTextBrowser, QVBoxLayout, QCheckBox, QWidget, QPlainTextEdit,
    QColorDialog, QDialog, QToolBar, QLineEdit, QDialogButtonBox, QGridLayout,
    QSpacerItem, QSizePolicy, QComboBox
)
from PyQt5.QtCore import QSettings, QThread, Qt, QEvent, QFile, QRegExp, QTimer, pyqtSignal,QPoint,QObject
from PyQt5.QtWidgets import QMessageBox, QListWidget, QListWidgetItem, QVBoxLayout, QDialog, QPushButton, QLabel
from sympy import sympify, SympifyError
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application, parse_expr
# target_path = './tsuki/assets/kernel/cython_utils.cp312-win_amd64.pyd'
# sys.path.append(os.path.join('./tsuki/assets/kernel/cython_utils.cp312-win_amd64.pyd'))
import ctypes
current_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(current_dir, './tsuki/assets/kernel/'))
import cython_utils
import savefile
LOG_COLORS = {
    'DEBUG': 'purple',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red,bold'
}

class ColoredFormatter(colorlog.ColoredFormatter):
    def format(self, record):
        color = LOG_COLORS.get(record.levelname, 'white')
        formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s%(reset)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors=LOG_COLORS
        )
        return formatter.format(record)

if os.path.exists('./tsuki/assets/log/'):
    tips_log_dir = './tsuki/assets/log/'
    os.makedirs(tips_log_dir, exist_ok=True)
    def create_and_write_file(directory, filename, content):
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, filename)

        with open(file_path, 'w') as file:
            file.write(content)
    directory = './tsuki/assets/log/'
    filename = 'Log_ZZBuAoYe_Readme.txt'
    content = ('Dear User,\n\nThank you for using this software.\n\nYou are currently looking at the Log folder.\n\nPlease note the following:\n1. Logs are usually stored in the temp folder.\n2. The log files have a .log extension.\n3. Log file names follow this format: TsukiNotes_Log_{timestamp}.log, where {timestamp} is in the format datetime.now().strftime('').\n4. This text file is not pre-existing but is created automatically!\n5. Thanks for using our software.')

    create_and_write_file(directory, filename, content)

def setup_logging():
    log_dir = './tsuki/assets/log/temp/'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    stream_handler = logging.StreamHandler()
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_file_path = os.path.join(log_dir, f'TsukiNotes_Log_{timestamp}.log')
    
    def detect_encoding(file_path):
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            return result['encoding']

    try:
        file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
    except Exception as e:
        logging.error(f"文件处理错误: {e}")
        file_handler = logging.FileHandler(log_file_path) 

    formatter = ColoredFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors=LOG_COLORS
    )
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

setup_logging()
logger = logging.getLogger(__name__)

setup_logging()
logger = logging.getLogger(__name__)

class QTextEditHandler(logging.Handler):
    COLOR_MAP = {
        'DEBUG': '<font color="purple">',
        'INFO': '<font color="green">',
        'WARNING': '<font color="orange">',
        'ERROR': '<font color="red">',
        'CRITICAL': '<font color="darkred">',
    }

    def __init__(self, text_edit, counters):
        super().__init__()
        self.text_edit = text_edit
        self.counters = counters

    def emit(self, record):
        try:
            msg = self.format(record)
            color = self.COLOR_MAP.get(record.levelname, '<font color="black">')
            html_msg = f'{color}{msg}</font>'
            self.text_edit.append(html_msg)
            levelname = record.levelname
            if levelname in self.counters:
                self.counters[levelname] += 1
            else:
                self.counters[levelname] = 1
            self.update_statistics()
        except Exception:
            self.handleError(record)
    
    def update_statistics(self):
        self.text_edit.parent().update_statistics()

class DebugWindow(QWidget):
    def __init__(self):
        super().__init__()
        debug_version = '0.1.1'
        self.setWindowTitle(f"TsukiNotes -Debug Ver{debug_version}")
        self.setGeometry(100, 100, 800, 600)
        self.setFont(QFont("Microsoft YaHei", 9))
        self.setWindowIcon(QIcon("./tsuki/assets/GUI/ico/logo.ico"))
        
        self.log_counters = {'INFO': 0, 'WARNING': 0, 'ERROR': 0, 'DEBUG': 0}

        layout = QVBoxLayout()
        
        self.log_text_edit = QTextEdit()
        self.log_text_edit.setReadOnly(True)
        layout.addWidget(self.log_text_edit)
        
        self.font_combo = QComboBox()
        self.font_combo.addItems(["Normal Font Size","10","11","12","13", "14","15", "16", "17","18", "19","20","21", "22","365"])
        self.font_combo.currentTextChanged.connect(self.change_font_size)
        layout.addWidget(self.font_combo)
        
        self.stats_label = QLabel("Lines: 0\nINFO: 0 | WARNING: 0 | ERROR: 0 | DEBUG: 0")
        layout.addWidget(self.stats_label)
        
        self.setLayout(layout)
        
        self.log_handler = QTextEditHandler(self.log_text_edit, self.log_counters)
        self.log_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(self.log_handler)
    
    def closeEvent(self, event):
        logging.getLogger().removeHandler(self.log_handler)
        super().closeEvent(event)

    def change_font_size(self, size_str):
        if size_str == "Normal Font Size":
            size = 9 
        else:
            size = int(size_str)
        font = QFont()
        font.setPointSize(size)
        self.log_text_edit.setFont(font)
        logging.info("Font Size Changed to %s", size)
    def update_statistics(self):
        total_lines = self.log_text_edit.document().blockCount()
        info_count = self.log_counters.get('INFO', 0)
        warning_count = self.log_counters.get('WARNING', 0)
        error_count = self.log_counters.get('ERROR', 0)
        debug_count = self.log_counters.get('DEBUG', 0)
        self.stats_label.setText(f"Lines: {total_lines}\nINFO: {info_count} | WARNING: {warning_count} | ERROR: {error_count} | DEBUG: {debug_count}")

# debug mod
debug_version = '1.1.0Release'
logger.info("====================================================================================================================")
logger.info("╔═══╗╔═══╗╔══╗ ╔╗╔╗╔══╗╔══╗╔╗╔╗╔═══╗")
logger.info("╚═╗ ║╚═╗ ║║╔╗║ ║║║║║╔╗║║╔╗║║║║║║╔══╝")
logger.info(" ╔╝╔╝ ╔╝╔╝║╚╝╚╗║║║║║╚╝║║║║║║╚╝║║╚══╗")
logger.info("╔╝╔╝ ╔╝╔╝ ║╔═╗║║║║║║╔╗║║║║║╚═╗║║╔══╝")
logger.info("║ ╚═╗║ ╚═╗║╚═╝║║╚╝║║║║║║╚╝║ ╔╝║║╚══╗")
logger.info("╚═══╝╚═══╝╚═══╝╚══╝╚╝╚╝╚══╝ ╚═╝╚═══╝")
logger.info("\n╔════╗╔══╗╔╗╔╗╔╗╔══╗╔══╗╔╗─╔╗╔══╗╔════╗╔═══╗╔══╗\n"
            "╚═╗╔═╝║╔═╝║║║║║║║╔═╝╚╗╔╝║╚═╝║║╔╗║╚═╗╔═╝║╔══╝║╔═╝\n"
            "  ║║  ║╚═╗║║║║║╚╝║   ║║ ║╔╗ ║║║║║  ║║  ║╚══╗║╚═╗\n"
            "  ║║  ╚═╗║║║║║║╔╗║   ║║ ║║╚╗║║║║║  ║║  ║╔══╝╚═╗║\n"
            "  ║║  ╔═╝║║╚╝║║║║╚═╗╔╝╚╗║║ ║║║╚╝║  ║║  ║╚══╗╔═╝║\n"
            "  ╚╝  ╚══╝╚══╝╚╝╚══╝╚══╝╚╝ ╚╝╚══╝  ╚╝  ╚═══╝╚══╝\n")
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

class CustomTextEdit(QTextEdit):
    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.create_context_menu)
        self.setFont(QFont("Microsoft YaHei"))  # Set the font to Microsoft YaHei

        # Load content from file
        with open(file_path, 'r', encoding='utf-8') as f:
            markdown_text = f.read()
            self.setHtml(md_to_html(markdown_text))

    def create_context_menu(self, position):
        menu = QMenu(self)
        
        bold_action = QAction("Bold", self)
        bold_action.triggered.connect(self.set_bold)
        menu.addAction(bold_action)
        
        italic_action = QAction("Italic", self)
        italic_action.triggered.connect(self.set_italic)
        menu.addAction(italic_action)
        
        underline_action = QAction("Underline", self)
        underline_action.triggered.connect(self.set_underline)
        menu.addAction(underline_action)
        
        menu.exec_(self.mapToGlobal(position))

    def set_bold(self):
        cursor = self.textCursor()
        cursor.select(QTextCursor.WordUnderCursor)
        format = cursor.charFormat()
        format.setFontWeight(QFont.Bold if format.fontWeight() != QFont.Bold else QFont.Normal)
        cursor.setCharFormat(format)
        self.setTextCursor(cursor)

    def set_italic(self):
        cursor = self.textCursor()
        cursor.select(QTextCursor.WordUnderCursor)
        format = cursor.charFormat()
        format.setFontItalic(not format.fontItalic())
        cursor.setCharFormat(format)
        self.setTextCursor(cursor)

    def set_underline(self):
        cursor = self.textCursor()
        cursor.select(QTextCursor.WordUnderCursor)
        format = cursor.charFormat()
        format.setFontUnderline(not format.fontUnderline())
        cursor.setCharFormat(format)
        self.setTextCursor(cursor)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            cursor = self.cursorForPosition(event.pos())
            cursor.select(cursor.WordUnderCursor)
            cursor_position = cursor.selectedText()

            if cursor_position.startswith("http"):
                webbrowser.open(cursor_position)
            else:
                super().mouseReleaseEvent(event)
        else:
            super().mouseReleaseEvent(event)

    def save_to_file(self):
        import html2text 
        try:
            html_text = self.toHtml()
            markdown_text = html2text.html2text(html_text) 
            
            with open(self.file_path, 'w', encoding='utf-8') as f:
                f.write(markdown_text)
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to save file: {e}')
# ==============================================================End Welcome===================================================================================================================

class FileLoaderThread(QThread):
    dataLoaded = pyqtSignal(list)

    def __init__(self, fileName):
        super().__init__()
        self.fileName = fileName

    def run(self):
        chunks = cython_utils.read_file_in_chunks(self.fileName)
        self.dataLoaded.emit(chunks)

class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.keyword_patterns = []
        self.comment_pattern = (None, None)
        self.quotation_pattern = (None, None)
        self.function_pattern = (None, None)

    def highlightBlock(self, text):
        for pattern, format in self.keyword_patterns:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        start_index = 0
        if self.previousBlockState() != 1:
            start_index = self.comment_pattern[0].indexIn(text)

        while start_index >= 0:
            end_index = self.comment_pattern[0].matchedLength()
            self.setFormat(start_index, end_index, self.comment_pattern[1])
            start_index = self.comment_pattern[0].indexIn(text, start_index + end_index)

        if self.quotation_pattern[0] is not None:
            expression = QRegExp(self.quotation_pattern[0])
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, self.quotation_pattern[1])
                index = expression.indexIn(text, index + length)

        if self.function_pattern[0] is not None:
            expression = QRegExp(self.function_pattern[0])
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, self.function_pattern[1])
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(1)

class PythonHighlighter(SyntaxHighlighter):
    def __init__(self, light=True, parent=None):
        super().__init__(parent)
        self.l = light
        
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#FFD700" if light else "#FFA500"))  # 更鲜艳的颜色
        keyword_format.setFontWeight(QFont.Bold)
        keywords = [
            "and", "as", "assert", "break", "class", "continue", "def",
            "del", "elif", "else", "except", "finally", "for",
            "from", "global", "if", "import", "in", "is", "lambda",
            "not", "or", "pass", "raise", "return", "try",
            "while", "with", "yield", "None", "True", "False",
            "async", "await", "nonlocal", "self"  # 新增 'self'
        ]
        self.keyword_patterns = [(QRegExp(r"\b" + keyword + r"\b"), keyword_format)
                                 for keyword in keywords]

        quotation_format = QTextCharFormat()
        quotation_format.setForeground(QColor("#32CD32" if light else "#228B22"))  # 更鲜艳的颜色
        self.quotation_pattern = (QRegExp(r"\".*\"|'.*'"), quotation_format)  # 支持单引号字符串

        function_format = QTextCharFormat()
        function_format.setFontItalic(True)
        function_format.setForeground(QColor("#00BFFF" if light else "#1E90FF"))  # 更鲜艳的颜色
        self.function_pattern = (QRegExp(r"\b[A-Za-z0-9_]+(?=\()"), function_format)

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#FF4500" if light else "#B22222"))  # 更鲜艳的颜色
        self.comment_pattern = (QRegExp(r"#.*"), comment_format)

class CppHighlighter(SyntaxHighlighter):
    def __init__(self, light=True, parent=None):
        super().__init__(parent)
        self.l = light
        
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#FFD700" if light else "#FFA500"))  # 更鲜艳的颜色
        keyword_format.setFontWeight(QFont.Bold)
        keywords = [
            "class", "const", "delete", "double", "dynamic_cast", "enum",
            "explicit", "export", "false", "float", "for", "friend",
            "goto", "if", "inline", "int", "long", "namespace", "new",
            "operator", "private", "protected", "public", "return",
            "short", "signed", "sizeof", "static", "struct", "switch",
            "template", "this", "throw", "true", "try", "typedef",
            "typeid", "unsigned", "using", "virtual", "void", "volatile",
            "wchar_t", "constexpr", "noexcept", "override"  # 新增 'override'
        ]
        self.keyword_patterns = [(QRegExp(r"\b" + keyword + r"\b"), keyword_format)
                                 for keyword in keywords]

        quotation_format = QTextCharFormat()
        quotation_format.setForeground(QColor("#32CD32" if light else "#228B22"))  # 更鲜艳的颜色
        self.quotation_pattern = (QRegExp(r"\".*\"|'.*'"), quotation_format)  # 支持单引号字符串

        function_format = QTextCharFormat()
        function_format.setFontItalic(True)
        function_format.setForeground(QColor("#00BFFF" if light else "#1E90FF"))  # 更鲜艳的颜色
        self.function_pattern = (QRegExp(r"\b[A-Za-z0-9_]+(?=\()"), function_format)

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#FF4500" if light else "#B22222"))  # 更鲜艳的颜色
        self.comment_pattern = (QRegExp(r"//.*|/\*.*\*/"), comment_format)  # 支持多行注释

class JavaHighlighter(SyntaxHighlighter):
    def __init__(self, light=True, parent=None):
        super().__init__(parent)
        self.l = light
        
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#FFD700" if light else "#FFA500"))  # 更鲜艳的颜色
        keyword_format.setFontWeight(QFont.Bold)
        keywords = [
            "abstract", "assert", "boolean", "break", "byte", "case",
            "catch", "char", "class", "const", "continue", "default",
            "do", "double", "else", "enum", "extends", "final",
            "finally", "float", "for", "goto", "if", "implements",
            "import", "instanceof", "int", "interface", "long",
            "native", "new", "null", "package", "private", "protected",
            "public", "return", "short", "static", "strictfp",
            "super", "switch", "synchronized", "this", "throw", "throws",
            "transient", "try", "void", "volatile", "while",
            "synchronized", "transient", "volatile", "enum"  # 重复关键词已删除
        ]
        self.keyword_patterns = [(QRegExp(r"\b" + keyword + r"\b"), keyword_format)
                                 for keyword in keywords]

        quotation_format = QTextCharFormat()
        quotation_format.setForeground(QColor("#32CD32" if light else "#228B22"))  # 更鲜艳的颜色
        self.quotation_pattern = (QRegExp(r"\".*\"|'.*'"), quotation_format)  # 支持单引号字符串

        function_format = QTextCharFormat()
        function_format.setFontItalic(True)
        function_format.setForeground(QColor("#00BFFF" if light else "#1E90FF"))  # 更鲜艳的颜色
        self.function_pattern = (QRegExp(r"\b[A-Za-z0-9_]+(?=\()"), function_format)

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#FF4500" if light else "#B22222"))  # 更鲜艳的颜色
        self.comment_pattern = (QRegExp(r"//.*|/\*.*\*/"), comment_format)  # 支持多行注释

class MarkdownHighlighter(SyntaxHighlighter):
    def __init__(self, light=True, parent=None):
        super().__init__(parent)
        self.l = light
        
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#FFD700" if light else "#FFA500"))  # 更鲜艳的颜色
        keyword_format.setFontWeight(QFont.Bold)
        keywords = [
            "#", "##", "###", "####", "#####", "######", "*", "_", ">", "-",
            "1.", "2.", "3.", "4.", "5.", "6.", "```", "[", "]", "(", ")",
            "!", "!!", "!!!", "!!!!", "!!!!!", "!!!!!!", "~~"  # 新增 '~~'
        ]
        self.keyword_patterns = [(QRegExp(re.escape(keyword)), keyword_format)
                                 for keyword in keywords]

        quotation_format = QTextCharFormat()
        quotation_format.setForeground(QColor("#32CD32" if light else "#228B22"))  # 更鲜艳的颜色
        self.quotation_pattern = (QRegExp(r"`.*`"), quotation_format)

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#FF4500" if light else "#B22222"))  # 更鲜艳的颜色
        self.comment_pattern = (QRegExp(r"<!--.*-->"), comment_format)

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QListWidget, QStackedWidget, QPushButton, QLabel, QGridLayout, QWidget
from PyQt5.QtCore import Qt

class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super(SettingsWindow, self).__init__(parent)
        self.setWindowTitle('Tsuki全局设置[Settings]')
        self.setWindowIcon(QIcon('./Tsuki/assets/GUI/resources/settings.png'))

        # 应用样式
        # self.setStyleSheet("background-image: url('./tsuki/assets/app/default/default_light.png');")
        self.setGeometry(100, 100, 800, 400)
        logger.info('Open Setting')

        # 设置布局
        main_layout = QHBoxLayout(self)

        sidebar = QListWidget(self)
        sidebar.setFixedWidth(150)
        sidebar.addItem("界面设置")
        sidebar.addItem("字体设置")
        sidebar.addItem("图标设置")
        sidebar.addItem("调试设置")
        sidebar.addItem("关于设置")
        sidebar.currentRowChanged.connect(self.display)

        self.stack = QStackedWidget(self)
        self.stack.addWidget(self.interfacePage())
        self.stack.addWidget(self.fontPage())
        self.stack.addWidget(self.iconPage())
        self.stack.addWidget(self.debugPage())
        self.stack.addWidget(self.aboutPage())

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stack)

        self.setLayout(main_layout)

        # 应用样式
        self.applyStyle()
    def interfacePage(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        title_label = QLabel("| 界面设置", self)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px; 
                font-weight: bold;
                color: #333333;
            }
        """)
        layout.addWidget(title_label, alignment=Qt.AlignLeft | Qt.AlignTop)

        # 创建按钮布局
        button_layout = QGridLayout()
        button_layout.setSpacing(15)

        button_layout.addWidget(self.createButton("设置背景颜色", self.parent().set_background), 0, 0)
        button_layout.addWidget(self.createButton("重置文本框背景图片", self.parent().reset_background_color), 0, 1)
        button_layout.addWidget(self.createButton("设置背景图", self.parent().setBackgroundImage), 1, 0)
        button_layout.addWidget(self.createButton("重置背景图", self.parent().reset_background), 1, 1)
        button_layout.addWidget(self.createButton("高亮显示设置", self.parent().total_setting), 2, 0)
        button_layout.addWidget(self.createButton("彩色设置背景", self.parent().color_bg), 2, 1)

        layout.addLayout(button_layout)
        return page

    def fontPage(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        title_label = QLabel("| 字体设置", self)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px; 
                font-weight: bold;
                color: #333333;
            }
        """)
        layout.addWidget(title_label, alignment=Qt.AlignLeft | Qt.AlignTop)

        button_layout = QGridLayout()
        button_layout.setSpacing(15)

        button_layout.addWidget(self.createButton("设置字体大小", self.parent().set_font_size), 0, 0)
        button_layout.addWidget(self.createButton("初始化字体大小", self.parent().initialize_font_size), 0, 1)

        layout.addLayout(button_layout)
        return page

    def iconPage(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        title_label = QLabel("| 图标设置", self)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px; 
                font-weight: bold;
                color: #333333;
            }
        """)
        layout.addWidget(title_label, alignment=Qt.AlignLeft | Qt.AlignTop)

        button_layout = QGridLayout()
        button_layout.setSpacing(15)

        button_layout.addWidget(self.createButton("重新设置图标", self.parent().re_icon_setting), 0, 0)
        button_layout.addWidget(self.createButton("自定义图标", self.parent().diy_icon_setting), 0, 1)
        button_layout.addWidget(self.createButton("检查图标路径", self.parent().iconpath_check_a1), 1, 0)

        layout.addLayout(button_layout)
        return page

    def debugPage(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        title_label = QLabel("| 调试设置", self)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px; 
                font-weight: bold;
                color: #333333;
            }
        """)
        layout.addWidget(title_label, alignment=Qt.AlignLeft | Qt.AlignTop)

        button_layout = QGridLayout()
        button_layout.setSpacing(15)

        button_layout.addWidget(self.createButton("调试模式", self.parent().toggle_debug_mode), 0, 0)
        button_layout.addWidget(self.createButton("加入TsukiNotes预览计划", self.parent().beta_version), 0, 1)

        layout.addLayout(button_layout)
        return page
    
    def aboutPage(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        # 减少布局的上下内边距和组件间距
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        title_label = QLabel("| 关于", self)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px; 
                font-family: "Microsoft YaHei";
                font-weight: bold;
                color: #333333;
            }
        """)

        font = QFont("Microsoft YaHei")
        about_label = QLabel("""
            TsukiNotes
            TsukiNotes 是一个具备高亮文本的记事本软件
            支持16进制文件打开，支持Python,C++,Java,MarkDown四种语言高亮，
            强大的Qt内核给你带来不一样的体验，更加完美的图形，超多丰富QSS
            等待你来发现！强大的搜索和不一样的感受，给你超越Windows的体验！
                             
            """)
        about_label.setFont(font)

        layout.addWidget(title_label, alignment=Qt.AlignLeft | Qt.AlignTop)
        layout.addWidget(about_label, alignment=Qt.AlignLeft | Qt.AlignTop)

        layout.addStretch()
        return page

    def createButton(self, text, slot):
        button = QPushButton(text)
        button.clicked.connect(slot)
        
        qss_file_path = './tsuki/assets/theme/Setting_button.qss'
        try:
            with open(qss_file_path, 'r', encoding='utf-8') as file:
                qss = file.read()
                button.setStyleSheet(qss)
        except Exception as e:
            self.statusBar().showMessage(f'应用按钮QSS样式失败: {e}')
        
        return button

    def display(self, index):
        self.stack.setCurrentIndex(index)

    def applyStyle(self):
        qss_file_path = './tsuki/assets/theme/Settings_Window_Style.qss'
        try:
            with open(qss_file_path, 'r', encoding='utf-8') as file:
                qss = file.read()
                self.setStyleSheet(qss)
        except Exception as e:
            self.statusBar().showMessage(f'应用设置窗口QSS样式失败: {e}')


from PyQt5.QtGui import QTextCursor

# 搜索的class
class SearchResultDialog(QDialog):
    def __init__(self, results, parent=None):
        super(SearchResultDialog, self).__init__(parent)
        self.setWindowTitle('搜索结果')
        logging.info("[Log/INFO] 搜索成功")
        self.setWindowIcon(QIcon("./tsuki/assets/GUI/resources/search.png"))
        self.results = results or []
        self.current_index = 0

        self.results_label = QTextBrowser()
        self.results_label.setOpenExternalLinks(True)
        self.results_label.setFont(QFont("Microsoft YaHei"))

        self.preview_label = QLabel()
        self.preview_label.setWordWrap(True)
        self.preview_label.setStyleSheet("background-color: #e0e0e0; padding: 10px; border-radius: 5px;")

        self.next_button = QPushButton('下一个')
        self.previous_button = QPushButton('上一个')
        self.cancel_button = QPushButton('退出')
        self.confirm_button = QPushButton('确定')

        self.next_button.clicked.connect(lambda: self.navigateResults(1))
        self.previous_button.clicked.connect(lambda: self.navigateResults(-1))
        self.cancel_button.clicked.connect(self.reject)
        self.confirm_button.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.results_label)
        layout.addWidget(self.preview_label)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.previous_button)
        button_layout.addWidget(self.next_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.confirm_button)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.loadStyle()
        self.showResult()

    def loadStyle(self):
        qss_file_path = './tsuki/assets/theme/Search_Result_Dialog.qss'
        try:
            with open(qss_file_path, 'r', encoding='utf-8') as file:
                qss = file.read()
                self.setStyleSheet(qss)
        except Exception as e:
            logging.error(f"加载搜索结果对话框样式失败: {e}")
            QMessageBox.warning(self, "样式加载错误", f"加载搜索结果对话框样式失败: {e}")

    def showResult(self):
        if self.results:
            result = self.results[self.current_index]
            highlighted_result = f'<p style="background-color: #4a86e8; color: white; padding: 10px; border-radius: 5px;">{result[2]}</p>'
            self.results_label.setHtml(highlighted_result)
            
            cursor = self.results_label.textCursor()
            cursor.movePosition(QTextCursor.Start)
            self.results_label.setTextCursor(cursor)
            
            self.results_label.setHtml(f"{highlighted_result}<br>结果 {self.current_index + 1} / {len(self.results)}")
            
            self.results_label.moveCursor(QTextCursor.Start)
            self.results_label.ensureCursorVisible()
            
            context = self.parent().getContext(result[0], result[1])
            self.preview_label.setText(f"预览: ...{context}...")
            
            if hasattr(self.parent(), 'jumpToSearchResult'):
                self.parent().jumpToSearchResult(self.current_index)
            else:
                logging.error("错误：主窗口缺少 'jumpToSearchResult' 方法")
        else:
            self.results_label.setText("提示：未找到相关结果")
            self.preview_label.setText("")
            logging.info("未找到搜索结果")

    def navigateResults(self, direction):
        if self.results:
            new_index = (self.current_index + direction) % len(self.results)
            if new_index != self.current_index:
                self.current_index = new_index
                self.showResult()

class ReNameDialog(QDialog):
    def __init__(self, parent=None, title="", label=""):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.layout = QVBoxLayout(self)
        self.label = QLabel(label)
        self.input = QLineEdit(self)
        self.button = QPushButton("确定", self)
        self.button.clicked.connect(self.accept)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

    def getText(self):
        return self.input.text()
    
# ======================================================以下是TsukiReader的CLass=====================================================
# ==================================================================================================================================
class TsukiReader(QMainWindow):

    def __init__(self):
        super().__init__()
        self.before = ''
        self.current_version = '1.5.4' 
        self.real_version = '1.5.4'
        self.update_Date = '2024/10/03'
        self.version_td = 'Release'
        self.version_gj = 'b-v154B-241003'
        self.config_file = './tsuki/assets/app/config/launch/launch_config.ini'  

        logging.debug(f"\n====================================================================================================================\n"
                      f"[Log/INFO]TsukiReader is running ,relatedInformation:"
                      f"[Back]Version:{self.current_version}\n"
                      f"[Back]UpdateDate:{self.update_Date}\n"
                      f"[Back]Version Update The Channel:{self.version_td}\n"
                      f"[Back]versionTHE INTERNAL BUILD NUMBER:{self.version_gj}\n"
                      f"====================================================================================================================")

        self.text_modified = False
        self.include_whitespace = False
        self.highlight_keywords = False
        self.context_menu = None
        self.custom_lines = 0
        self.initUI()
        self.tabWidget.currentChanged.connect(self.onTabChanged)
        self.connectCurrentWidgetSignals()
        self.tabWidget.currentChanged.connect(self.updateStatusLabel)
        self.initialize_settings()

        self.loadScrollbarStyle()

    def loadScrollbarStyle(self):
        qss_file_path = './tsuki/assets/theme/Main_Scrollbar_Style.qss'
        try:
            with open(qss_file_path, 'r', encoding='utf-8') as file:
                qss = file.read()
                self.setStyleSheet(qss)
        except Exception as e:
            logging.error(f"加载滚动条样式失败: {e}")
            QMessageBox.warning(self, "样式加载错误", f"加载滚动条样式失败: {e}")

    def initUI(self):
        self.tabWidget = QTabWidget()
        self.setCentralWidget(self.tabWidget)
        self.context_menu = QMenu(self)
        self.createActions()
        self.createMenus()
        self.debug_window = DebugWindow()
        self.debug_window.hide()
        self.createShortcuts()
        self.defaultFont = QFont("Microsoft YaHei")
        self.setGeometry(100, 100, 990, 600)
        self.setWindowTitle('TsukiNotes')
        self.setWindowIcon(QIcon('./tsuki/assets/GUI/ico/logo.ico'))
        logging.debug("initUI initialization is complete")

        self.text_edit = QPlainTextEdit()

        self.show()
        self.highlighter = PythonHighlighter(self.highlight_keywords, self.text_edit.document())
        self.status_label = QLabel()
        self.statusBar().addPermanentWidget(self.status_label)
        

        v = sys.argv
        nv = [i for i in v if i not in ["--debug", "-debug"]]
        
        if len(nv) > 1:
            if os.path.isfile(nv[1]):
                self.openFile(nv[1])
                config = configparser.ConfigParser()
                font_path = './tsuki/assets/app/cfg/font/tn_font_family.ini'
                try:
                    with open(font_path, 'rb') as f:
                        raw_data = f.read()
                        result = chardet.detect(raw_data)
                        encoding = result['encoding']
                    
                    with open(font_path, 'r', encoding=encoding) as file:
                        config.read_file(file)
                    
                    font_name = config.get('Settings', 'font_family', fallback='').strip()
                    if not font_name:
                        font_name = "Microsoft YaHei UI"
                        
                    font = QFont(font_name)
                    self.text_edit.setFont(font)
                    self.initialize_settings()
                    logger.info(f"[Log/INFO]载入{nv[1]}成功")
                except Exception as e:
                    logging.error(f"读取字体配置时发生错误: {e}")
                    font = QFont("Microsoft YaHei UI")
                    self.text_edit.setFont(font)
                    self.initialize_settings()
                    logger.error(f"[Log/ERROR]读取配置文件失败: {e}")
            else:
                QMessageBox.critical(self, 'Open File', f'失败了❌❗: 文件{nv[1]}不存在！')
                self.statusBar().showMessage(f'TsukiOF❌: 文件[{nv[1]}]打开失败！Error:[文件不存在]')
                logger.error(f"[Log/ERROR]ERROR Init UI Open File: 文件{nv[1]}不存在！")
                self.newFile()
        else:
            self.newFile()

        self.updateStatusLabel()

        currentWidget = self.tabWidget.currentWidget()
        currentWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        currentWidget.customContextMenuRequested.connect(self.showContextMenu)
        self.context_menu = QMenu(self)
        self.loadBackgroundSettings()
        self.checkFirstRun()

    def jumpToSearchResult(self, index):
        current_widget = self.tabWidget.currentWidget()
        if isinstance(current_widget, QPlainTextEdit):
            cursor = current_widget.textCursor()
            cursor.setPosition(self.search_results[index][0])
            cursor.setPosition(self.search_results[index][1], QTextCursor.KeepAnchor)
            current_widget.setTextCursor(cursor)
            current_widget.ensureCursorVisible()

    def getContext(self, start, end):
        current_widget = self.tabWidget.currentWidget()
        if isinstance(current_widget, QPlainTextEdit):
            text = current_widget.toPlainText()
            sentence_start = text.rfind('.', 0, start) + 1
            sentence_end = text.find('.', end)
            if sentence_end == -1:
                sentence_end = len(text)
            return text[start:end].strip()
        return ""
    
    def onTabChanged(self):
        self.connectCurrentWidgetSignals()
        self.updateStatusLabel()

    def connectCurrentWidgetSignals(self):
        currentWidget = self.tabWidget.currentWidget()
        if currentWidget:
            currentWidget.textChanged.connect(self.updateStatusLabel)
            currentWidget.cursorPositionChanged.connect(self.updateStatusLabel)

    def initialize_settings(self):
        QTimer.singleShot(100, lambda: self.log_and_call(self.read_font_size_from_cfg, "FontSettings_1"))
        QTimer.singleShot(110, lambda: self.log_and_call(self.read_font_family_from_cfg, "FontSettings_2"))
        QTimer.singleShot(120, lambda: self.log_and_call(self.load_background_settings, "BackGroundSettings"))

    def log_and_call(self, method, setting_name):
        try:
            method()
            logging.debug(f"[Log/INFO] 载入{setting_name}成功")
        except Exception as e:
            logging.error(f"[Log/ERROR] 载入{setting_name}失败: {str(e)}")

    def handleCommandLineArgs(self):
        v = sys.argv
        nv = []
        for i in v:
            if i not in ("--debug", "-debug"):
                nv.append(i)
        if len(nv) > 1:
            file_path = nv[1]
            
            if os.path.isfile(file_path):
                self.openFile(file_path)
                
                font = QFont("Microsoft YaHei UI")
                self.editor.setFont(font)
                self.text_edit.setFont(font)
                self.loadInitialConfig()
                
                logger.info(f"[Log/INFO] 载入 {file_path} 成功")
            else:
                QMessageBox.critical(self, 'Open File', f'失败了❌❗: 文件 {file_path} 不存在！')
                self.statusBar().showMessage(f'TsukiOF❌: 文件 [{file_path}] 打开失败！Error: [文件不存在]')
                logger.error(f"[Log/ERROR] ERROR Init UI Open File: 文件 {file_path} 不存在！")
                
                self.newFile()
        else:
            self.newFile()

    def toggle_debug_mode(self):
        if self.debug_window.isVisible():
            self.debug_window.hide()
        else:
            self.debug_window.show()

    def close_debug_window(self):
        if self.debug_window:
            self.debug_window.close()
            logging.debug("Debug window closed")

    def color_bg(self):
        QMessageBox.information(self, "提示", "正在努力")
        logging.info("TipsShowing Color_bg")

    def checkFirstRun(self):
        say_zz = ("Welcome! Your Are First Run!\nThanks For Your Use\nThis Text Is Program Auto Make!")
        if not os.path.exists('./tsuki/assets/app/config/launch'):
            os.makedirs('./tsuki/assets/app/config/launch/', exist_ok=True)
            os.path.join('./tsuki/assets/app/config/launch/', 'launch_first.md')

        if not os.path.exists(self.config_file):
            msg_box = QMessageBox()
            msg_box.setWindowTitle('Welcome to TsukiNotes!')
            msg_box.setText('TuskiNotes Welcome\n\n\n感谢使用TsukiNotes!\nTsukiNotes 可以帮助你更好的创建文本\n本产品是一个轻量文本编辑器\n基于GPLv3 -可以在Github查阅该项目\n')
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.setWindowFlags(Qt.FramelessWindowHint)
            msg_box.setFont(QFont("Microsoft YaHei UI", 6))

            # 加载QSS文件
            qss_file_path = './tsuki/assets/theme/Welcome_Message.qss'
            try:
                with open(qss_file_path, 'r', encoding='utf-8') as file:
                    qss = file.read()
                    msg_box.setStyleSheet(qss)
            except Exception as e:
                logging.error(f"加载欢迎消息样式失败: {e}")

            msg_box.exec_()

            with open(self.config_file, 'w') as file:
                file.write(say_zz)
        else:
            pass

        return 

    logging.info("NEXT")


    def showContextMenu(self, pos):
        self.context_menu = QMenu(self)
        self.context_menu.setStyleSheet("background-color: rgba(255, 255, 255, 150); border: 2px solid black;")

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
            logging.error(f"{e}")
            self.statusBar().showMessage(f'TsukiFS❌: 字体大小设置失败！详见MessageBox！')
            logger.error(f"[Log/ERROR]ERROR Set Font Size: {str(e)}")

    def save_font_size_to_cfg(self, font_size):
        config = configparser.ConfigParser()
        config['Settings'] = {'font_size': str(font_size)}
        
        # 确保目录存在
        cfg_dir = 'tsuki/assets/app/cfg/font'
        if not os.path.exists(cfg_dir):
            os.makedirs(cfg_dir)
            logging.info("[INFO]SAVE")
            logger.info(f"[Log/INFO]创建字体大小配置文件")

        # 保存配置文件
        cfg_path = os.path.join(cfg_dir, 'tn_font.ini')
        with open(cfg_path, 'w') as configfile:
            config.write(configfile)
            logging.info(f"[INFO]SAVE {cfg_path}")
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

        # self.updateAct = QAction(QIcon('./tsuki/assets/GUI/resources/update_msg.png'),'更新日志', self)
        # self.updateAct.triggered.connect(self.updateMessage)

        self.exitAct = QAction(QIcon('./tsuki/assets/GUI/resources/exit_software.png'),'退出程序', self)
        self.exitAct.triggered.connect(self.close)

        self.resetFontAct = QAction(QIcon('./tsuki/assets/GUI/resources/font_reset_change.png'),'重置字体', self)
        self.resetFontAct.triggered.connect(self.resetFont)

        self.update2Act = QAction(QIcon('./tsuki/assets/GUI/resources/update_cloud.png'),'手动检测更新', self)
        self.update2Act.triggered.connect(self.update2)

        self.renameTabAct = QAction(QIcon('./tsuki/assets/GUI/resources/font_size_reset_tab.png'),'重命名标签', self)
        self.renameTabAct.triggered.connect(self.renameTab)

        # self.cutTabAct = QAction(QIcon('./tsuki/assets/GUI/resources/settings_list_shortcut.png'),'快捷键', self)
        # self.cutTabAct.triggered.connect(self.cutTab)

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

        self.runcodeAction = QAction(self)
        self.runcodeAction.setIcon(QIcon('./tsuki/assets/GUI/resources/run.png'))
        self.runcodeAction.setShortcut('F5')
        self.runcodeAction.triggered.connect(self.runcode)

        self.runcode_debugAction = QAction(self)
        self.runcode_debugAction.setIcon(QIcon('./tsuki/assets/GUI/resources/debug.png'))
        self.runcode_debugAction.setShortcut('F6')
        self.runcode_debugAction.triggered.connect(self.runcode_debug)


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

        updateMenu = menubar.addMenu('更新')
        updateMenu.addAction(self.checkUpdateAct)
        updateMenu.addAction(self.update2Act)
        updateMenu.addAction(self.versionnowAct)
        updateMenu.addAction(self.online_updateMessageAct)

        aboutMenu = menubar.addMenu('关于')
        aboutMenu.addAction(self.aboutAct)
        aboutMenu.addAction(self.aboutDetailsAct)

        serverMenu = menubar.addMenu('服务器')
        serverMenu.addAction(self.pingServerManuallyAct)
        serverMenu.addAction(self.url_msgAct)

        settingsMenu = menubar.addMenu(QIcon('./tsuki/assets/GUI/resources/settings.png'), '设置')
        settingsMenu.addAction(self.settingsAction)


        runCodeMenu = menubar.addMenu('运行')
        runCodeMenu.setIcon(QIcon('./tsuki/assets/GUI/resources/start.png'))
        
        self.runcodeAction = QAction('Run Code', self)
        self.runcodeAction.setIcon(QIcon('./tsuki/assets/GUI/resources/start.png'))
        self.runcodeAction.setShortcut('F5')
        self.runcodeAction.triggered.connect(self.runcode)
        runCodeMenu.addAction(self.runcodeAction)
        
        self.runcode_debugAction = QAction('Debug Run Code', self)
        self.runcode_debugAction.setIcon(QIcon('./tsuki/assets/GUI/resources/debug.png'))
        self.runcode_debugAction.setShortcut('F6')
        self.runcode_debugAction.triggered.connect(self.runcode_debug)
        runCodeMenu.addAction(self.runcode_debugAction)
    def openSettingsWindow(self):
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
        self.shortcut_run = QShortcut('Ctrl+F5', self)
        self.shortcut_debugrun = QShortcut('Ctrl+F6', self)

        self.shortcut_search.activated.connect(self.performSearch)
        self.shortcut_save.activated.connect(self.performSave)
        self.shortcut_clear.activated.connect(self.performClear)
        self.shortcut_undo.activated.connect(self.performUndo)
        self.shortcut_redo.activated.connect(self.performRedo)
        self.shortcut_cut.activated.connect(self.performCut)
        self.shortcut_open.activated.connect(lambda: (self.openFile("")))
        self.shortcut_new.activated.connect(self.newFile)
        self.shortcut_close.activated.connect(self.closeFile)
        self.shortcut_run.activated.connect(self.runcode)
        self.shortcut_debugrun.activated.connect(self.runcode_debug)


    def updateStatusLabel(self):
        currentWidget = self.tabWidget.currentWidget()
        if currentWidget:
            try:
                cursor = currentWidget.textCursor()
                cursor_line = cursor.blockNumber() + 1
                cursor_column = cursor.columnNumber() + 1
                char_count = len(currentWidget.toPlainText())
                encoding = getattr(self, 'current_encoding', 'Unknown-Encoding')
                document = currentWidget.document()
                block = document.begin()
                line_count = 0
                max_column_count = 0

                while block.isValid():
                    line_text = block.text()
                    line_count += 1
                    max_column_count = max(max_column_count, len(line_text))
                    block = block.next()

                status_text = (f'[当前文本] [ 行数: {line_count} | 列数: {max_column_count} | 字符数: {char_count} | '
                            f'编码: {encoding} | 光标位置: 行{cursor_line} 列{cursor_column} ]')
                self.status_label.setText(status_text)
                self.status_label.setFont(QFont("微软雅黑"))
            except Exception as e:
                logging.error(f"An error occurred while updating the status label: {e}")
        else:
            logging.warning("Current widget is not valid.")



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
            logger.error("[Log/Error]Change Font Error:", e)

    def save_font_family_to_cfg(self, font_family):
        config = configparser.ConfigParser()
        config['Settings'] = {'font_family': font_family}

        cfg_dir = 'tsuki/assets/app/cfg/font'
        if not os.path.exists(cfg_dir):
            os.makedirs(cfg_dir)
            logging.info("[INFO]SAVE")
            logger.info("[Log/INFO]SAVE")

        cfg_path = os.path.join(cfg_dir, 'tn_font_family.ini')
        with open(cfg_path, 'w') as configfile:
            config.write(configfile)
            logging.info(f"[INFO]SAVE {cfg_path}")
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

        # 构建允许的符号集合
        allowed_chars = '0123456789+-*/()%.^ '
        math_expr = ''.join(c for c in selected_text if c in allowed_chars)

        # 使用 sympy 进行解析和计算
        try:
            # 使用 sympy 的转换器处理隐式乘法
            transformations = (standard_transformations + (implicit_multiplication_application,))
            parsed_expr = parse_expr(math_expr, transformations=transformations)
            
            # 计算表达式
            result = parsed_expr.evalf()

            self.statusBar().showMessage(f'计算结果✔: {result}')
            logger.info(f"[Log/Math]Succeed: MathTools Running, Result: {result}")

        except SympifyError as e:
            self.statusBar().showMessage('TsukiMathTools🚫: 不是数学表达式！')
            logger.error("[Log/Error]Misinterpreted as a non-mathematical expression.")
        except Exception as e:
            self.statusBar().showMessage(f'计算错误❌: {e}')
            logger.error(f"[Log/Error]Miscalculated: {e}")

    def resetFont(self):
        currentWidget = self.tabWidget.currentWidget()
        font = QFont()
        font.setFamily("Microsoft YaHei UI")   
        logger.info("[Log/INFO]Changed the font to Microsoft Yahei UI")
        font_name = font.family()
        currentWidget.setFont(font)
        self.statusBar().showMessage(f'TsukiFontReset: 字体已经成功重置为[{font_name}]！')
        logger.info("[Log/INFO]ReSet Font")


    def loadFontSettings(self):
        config = configparser.ConfigParser()
        font_path = './tsuki/assets/app/cfg/font/tn_font_family.ini'

        with open(font_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']

        try:
            with open(font_path, 'r', encoding=encoding) as file:
                config.read_file(file)
            font_name = config.get('Settings', 'font_family', fallback='').strip()
            if not font_name:
                font_name = "Microsoft YaHei UI"
                
        except configparser.NoSectionError:
            logging.error("配置文件中没有 'Settings' 部分")
            font_name = "Microsoft YaHei UI"
        except configparser.NoOptionError:
            logging.error("配置文件中没有 'font_family' 选项")
            font_name = "Microsoft YaHei UI"
        except UnicodeDecodeError as e:
            logging.error(f"读取文件时发生编码错误: {e}")
            font_name = "Microsoft YaHei UI"
        except Exception as e:
            logging.error(f"读取字体配置时发生错误: {e}")
            font_name = "Microsoft YaHei UI" 

        return font_name

    def openFile(self, fileName):
        
        if fileName == "":
            options = QFileDialog.Options()
            filters = "Text Files (*.txt *.md *.ini *.xml *.json *.log *.py *.cpp *.java *.tnote);;16进制文件 (*.exe);;所有文件 (*)"
            fileName, _ = QFileDialog.getOpenFileName(self, 'Open File', '', filters, options=options)

        if fileName:
            try:
                if fileName.endswith(('.exe', '.pyd')):
                    self.openHexFileInTab(fileName)
                else:
                    encoding = self.detectFileEncoding(fileName)
                    self.current_encoding = encoding  
                    if not self.openFileInTab(fileName, encoding):
                        self.createNewTab(fileName, encoding)

                self.updateWindowTitle(fileName)
                self.statusBar().showMessage(f'TsukiOpen✔: 文件 [{fileName}] 已成功在TsukiNotes内打开！')
                logger.info(f"[Log/INFO]Open File Succeed: {fileName}")

                currentWidget = self.tabWidget.currentWidget()
                font_config_path = './tsuki/assets/app/cfg/font/tn_font_family.ini'
                
                if os.path.exists(font_config_path):
                    config = configparser.ConfigParser()
                    try:
                        config.read(font_config_path, encoding='utf-8')
                    except UnicodeDecodeError:
                        config.read(font_config_path, encoding='gbk')
                    font_family = config.get('Settings', 'font_family', fallback='').strip()
                    
                    if font_family:
                        font = QFont(font_family, 10)
                    else:
                        font = QFont("Microsoft YaHei", 10)
                        config['Settings'] = {'font_family': 'Microsoft YaHei'}
                        with open(font_config_path, 'w', encoding='utf-8') as configfile:
                            config.write(configfile)
                else:
                    font = QFont("Microsoft YaHei", 10)
                    config = configparser.ConfigParser()
                    config['Settings'] = {'font_family': 'Microsoft YaHei'}
                    os.makedirs(os.path.dirname(font_config_path), exist_ok=True)
                    with open(font_config_path, 'w', encoding='utf-8') as configfile:
                        config.write(configfile)
                
                currentWidget.setFont(font)
                logger.info(f"[Log/INFO]Font set to: {font.family()}")

                self.apply_background_settings(currentWidget)

            except UnicodeDecodeError as e:
                self.handleError('Open File', fileName, f"编码错误: {e}，尝试使用其他编码打开文件。")
            except Exception as e:
                self.handleError('Open File', fileName, e)

    def detectFileEncoding(self, fileName):
        with open(fileName, 'rb') as file:
            raw_data = file.read(10000)
            result = chardet.detect(raw_data)
            return result['encoding'] or 'utf-8'

    def openFileInTab(self, fileName, encoding):
        file_extension = os.path.splitext(fileName)[1].lower()


        for index in range(self.tabWidget.count()):
            if self.tabWidget.tabText(index) == os.path.basename(fileName):
                text_edit = self.tabWidget.widget(index)
                self._load_file_content(fileName, text_edit, encoding)
                self.tabWidget.setCurrentWidget(text_edit)
                return True

        new_text_edit = QTextEdit()
        self.tabWidget.addTab(new_text_edit, os.path.basename(fileName))
        self._load_file_content(fileName, new_text_edit, encoding)
        self.tabWidget.setCurrentWidget(new_text_edit)
        return True

    def openHexFileInTab(self, fileName):
        iconPath = './tsuki/assets/GUi/resource/dll.png'  # Assuming a new icon for DLL files
        text_edit = QTextEdit()
        self.tabWidget.addTab(text_edit, QIcon(iconPath), os.path.basename(fileName))
        self._load_hex_content(fileName, text_edit)
        self.tabWidget.setCurrentWidget(text_edit)

    def createNewTab(self, fileName, encoding):
        tab_name = os.path.basename(fileName)
        
        dialog = QDialog(self)
        dialog.setWindowTitle("为新标签命名")
        
        # 加载QSS文件
        qss_file_path = './tsuki/assets/theme/New_Tab_Dialog.qss'
        try:
            with open(qss_file_path, 'r', encoding='utf-8') as file:
                qss = file.read()
                dialog.setStyleSheet(qss)
        except Exception as e:
            logging.error(f"加载新标签对话框样式失败: {e}")
        
        layout = QVBoxLayout(dialog)
        
        name_input = QLineEdit(tab_name)
        layout.addWidget(name_input)
        
        button_layout = QHBoxLayout()
        ok_button = QPushButton("确定")
        skip_button = QPushButton("跳过")
        button_layout.addWidget(ok_button)
        button_layout.addWidget(skip_button)
        layout.addLayout(button_layout)
        
        ok_button.clicked.connect(dialog.accept)
        skip_button.clicked.connect(dialog.reject)
        
        if dialog.exec_() == QDialog.Accepted:
            tab_name = name_input.text()
        
        text_edit = QPlainTextEdit()
        self.setFont(text_edit)
        self.load_background_settings(text_edit)
        
        icon = self.getFileIcon(fileName)
        self.tabWidget.addTab(text_edit, icon, tab_name)

        self.loadFileContent(fileName, text_edit, encoding)

        self.tabWidget.setCurrentWidget(text_edit)
        text_edit.textChanged.connect(self.updateStatusLabel)
        
        self.setHighlighter(text_edit, fileName)

    def getFileIcon(self, fileName):
        icon_map = {
            ('.py', '.pyx', '.pyw', '.pyi'): './tsuki/assets/GUI/resource/python.png',
            ('.cpp', '.h', '.hpp', '.c', '.cxx', '.cc', '.hh', '.hxx', '.ino'): './tsuki/assets/GUI/resource/cpp.png',
            ('.java', '.class'): './tsuki/assets/GUI/resource/java.png',
            ('.md', '.markdown'): './tsuki/assets/GUI/resource/markdown.png'
        }
        
        for extensions, icon_path in icon_map.items():
            if fileName.endswith(extensions):
                return QIcon(icon_path)
        
        return QIcon('./tsuki/assets/GUI/resource/default_file.png')

    def loadFileContent(self, fileName, text_edit, encoding):
        if fileName.endswith(('.bin', '.dat')):
            self._load_hex_content(fileName, text_edit)
        else:
            self._load_file_content(fileName, text_edit, encoding)

    def setHighlighter(self, text_edit, fileName):
        highlighter_map = {
            ('.py', '.pyx', '.pyw', '.pyi'): PythonHighlighter,
            ('.cpp', '.h', '.hpp', '.c', '.cxx', '.cc', '.hh', '.hxx', '.ino'): CppHighlighter,
            ('.java', '.class'): JavaHighlighter,
            ('.md', '.markdown'): MarkdownHighlighter
        }
        
        for extensions, highlighter_class in highlighter_map.items():
            if fileName.endswith(extensions):
                self.highlighter = highlighter_class(self.highlight_keywords, text_edit.document())
                return
        
        self.highlighter = None

    def _load_hex_content(self, fileName, text_edit):
        self.loader_thread = FileLoaderThread(fileName)
        self.loader_thread.dataLoaded.connect(lambda chunks: text_edit.setPlainText('\n'.join(chunks)))
        self.loader_thread.start()

    def beta_version(self):
        msgBox = QMessageBox()
        version = self.current_version
        msgBox.setWindowTitle(f"您确定要加入测试版通道吗？")
        msgBox.setText(
            f"测试版\n若加入测试版，您将优先享受最新的功能，但是他可能存在bug！\n你确定要加入测试版吗？")

        yesButton = QPushButton("确定加入测试版通道")
        source2Button = QPushButton("了解测试版")
        cancelButton = QPushButton("取消")

        msgBox.addButton(yesButton, QMessageBox.YesRole)
        msgBox.addButton(source2Button, QMessageBox.YesRole)
        msgBox.addButton(cancelButton, QMessageBox.NoRole)

        clickedButton = msgBox.exec()

        if msgBox.clickedButton() == yesButton:
            self.update_config(True)  
            QMessageBox.information(self, "提示", "您已加入测试版通道!感谢加入!\n请注意,测试版可能会存在bug,并且随时可能会被删除")
            logging.debug(f"[Log/INFO]User joined the test channel!")
        elif msgBox.clickedButton() == source2Button:
            QMessageBox.information(self, "提示", "测试版通道是实验性的\n一切bug都可能发生\n并且一旦加入，当前版本还不支持退出")
            logging.info(f"[Log/INFO]User looked about -> Beta version")
        elif msgBox.clickedButton() == cancelButton:
            self.update_config(False)
            QMessageBox.information(self, "提示", "您已取消加入测试版通道!\n若需要随时可以加入")
            logging.info(f"[Log/INFO]User canceled the operation")

    def update_config(self, is_beta):
        config = configparser.ConfigParser()
        config_file_path = './tsuki/assets/app/cfg/update/update.cfg'
        
        os.makedirs(os.path.dirname(config_file_path), exist_ok=True)

        config['BetaVersion'] = {'BetaVersion': 'Activity' if is_beta else 'off'}
        config['Download'] = {'Download Link': 'https://zzbuaoye.us.kg/TsukiNotes/beta/version.txt' if is_beta else 'https://zzbuaoye.us.kg/TsukiNotes/version.txt'}

        with open(config_file_path, 'w') as configfile:
            config.write(configfile)
        
        logging.info(f"[Log/INFO]Config updated: BetaVersion = {'Activity' if is_beta else 'off'}")

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
        config = configparser.ConfigParser()
        font_path = './tsuki/assets/app/cfg/font/tn_font_family.ini'
        
        try:
            with open(font_path, 'rb') as f:
                raw_data = f.read()
                result = chardet.detect(raw_data)
                detected_encoding = result['encoding']
            
            with open(font_path, 'r', encoding=detected_encoding) as file:
                config.read_file(file)
            
            font_name = config.get('Settings', 'font_family', fallback='').strip()
            if not font_name:
                font_name = "Microsoft YaHei"
                logging.info(f"[Log/INFO] Font not found in config, using default font: {font_name}")
            
            font = QFont(font_name)
            logging.info(f"[Log/INFO] Font name: {font_name}, path: {font_path}")
        except Exception as e:
            logging.error(f"[Log/ERROR] Error reading font config: {e}")
            font = QFont("Microsoft YaHei")
            logging.info(f"[Log/INFO] Using default font due to error: Microsoft YaHei")

        try:
            with open(fileName, 'r', encoding=encoding, errors='ignore') as file:
                content = file.read()
                text_edit.setPlainText(content)
                text_edit.setFont(font)
        except Exception as e:
            self.handleError('Load File Content', fileName, e)
            logging.error(f"[Log/ERROR] Error loading file content from {fileName}: {e}")



    def runcode(self):
        current_index = self.tabWidget.currentIndex()
        current_widget = self.tabWidget.widget(current_index)
        tab_name = self.tabWidget.tabText(current_index)
        font = QFont("Microsoft YaHei")

        if tab_name.endswith('.md') or tab_name.endswith('.markdown'):
            if hasattr(current_widget, 'file_path') and current_widget.file_path:
                file_path = current_widget.file_path
            else:
                file_path = os.path.join(os.getcwd(), tab_name)
            
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(current_widget.toPlainText())
                logging.info(f"File saved: {file_path}")
            except Exception as e:
                QMessageBox.warning(self, 'Save Error', f'无法保存文件：{str(e)}')
                return

            if hasattr(current_widget, 'setFont'):
                current_widget.setFont(font)
            
            self.runcodeAction.setIcon(QIcon('./tsuki/assets/GUI/resources/stop.png'))
            markdown_text = current_widget.toPlainText()
            html_text = markdown2.markdown(markdown_text)
            
            preview_window = QDialog(self)
            preview_window.setWindowTitle(f'Preview - {tab_name}')
        
            preview_text_edit = CustomTextEdit(file_path=file_path, parent=preview_window)
            preview_text_edit.setHtml(html_text)
            preview_text_edit.setAcceptRichText(True) 
            
            toggle_mode_button = QPushButton('Toggle Dark/Light Mode', preview_window)
            toggle_mode_button.clicked.connect(lambda: self.toggle_mode(preview_text_edit))
            
            save_button = QPushButton('Save Changes', preview_window)
            save_button.clicked.connect(preview_text_edit.save_to_file)
            preview_window.resize(800, 600) 
        
            preview_layout = QVBoxLayout(preview_window)
            preview_layout.addWidget(preview_text_edit)
            preview_layout.addWidget(toggle_mode_button)
            preview_layout.addWidget(save_button)
            preview_window.setLayout(preview_layout)
            
            preview_window.exec_()
            
            self.runcodeAction.setIcon(QIcon('./tsuki/assets/GUI/resources/start.png'))
        else:
            QMessageBox.warning(self, 'Warning', '请运行[.md][.markdown]后缀的文件\n暂不支持预览其他格式文件\n')

    def toggle_mode(self, text_edit):
        current_stylesheet = text_edit.styleSheet()
        if "background-color: black" in current_stylesheet:
            text_edit.setStyleSheet("background-color: white; color: black;")
        else:
            text_edit.setStyleSheet("background-color: black; color: white;")

    def runcode_debug(self):
        self.toggle_debug_mode()
        
        try:
            self.runcode()
            logging.debug("runcode function has been executed with debugging mode.")
        
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            logging.error("".join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)))
            
            self.close_debug_window()
    
        finally:
            self.close_debug_window()
            self.statusBar().showMessage("TsukiRunCode✔: 运行结束,调试窗口自动关闭", 5000)  

    def newFile(self, filePath='./tsuki/assets/resources/'):
        textEdit = QPlainTextEdit()
        
        # 设置字体
        font = QFont("Microsoft YaHei", 10)
        textEdit.setFont(font)
        logging.info(f"[Log/INFO] Font set to: Microsoft YaHei, point size: 10")
        
        logging.info(f"Received filePath: {filePath}")
 
        if self.tabWidget.count() == 0:
            tab_name = "原始文本"
            file_encoding = "UTF-8"
        else:
            tab_name, file_encoding = self.getNewFileInfo(filePath)
        
        new_tab_index = self.tabWidget.count()
        self.tabWidget.addTab(textEdit, tab_name)
        self.updateTabIcon(new_tab_index)
        
        textEdit.setLineWrapMode(QPlainTextEdit.NoWrap)
        textEdit.setTabStopDistance(4 * self.fontMetrics().averageCharWidth())
        logging.info(f"[Log/INFO] New File: {tab_name}, Encoding: {file_encoding}")
        self.apply_background_settings(textEdit)
        
        self.tabWidget.setCurrentIndex(new_tab_index)
        textEdit.textChanged.connect(lambda: self.updateTabIconOnTextChange(new_tab_index))
        # 设置右键菜单
        textEdit.setContextMenuPolicy(Qt.CustomContextMenu)
        textEdit.customContextMenuRequested.connect(self.showContextMenu)
        


    def apply_background_settings(self, widget):
        config = configparser.ConfigParser()
        config_path = 'tsuki/assets/app/cfg/background/background_color.ini'
        
        try:
            config.read(config_path, encoding='utf-8')
            image_path = config.get('Background', 'image_path', fallback='./tsuki/assets/app/default/default_light.png')
            
            if image_path and os.path.exists(image_path):
                style_sheet = f'background-image: url("{image_path}");'
                widget.setStyleSheet(style_sheet)
                logging.info(f"[Log/INFO] Background image applied: {image_path}")
            else:
                logging.warning(f"[Log/WARNING] Background image not found: {image_path}")
        
        except Exception as e:
            logging.error(f"[Log/ERROR] Failed to apply background settings: {str(e)}")
        
            
    def getNewFileInfo(self, filePath):
        dialog = QDialog(self)
        dialog.setWindowTitle("新建标签页")
        dialog.setFont(QFont("Microsoft YaHei"))
        dialog.resize(300, 200)

        # 加载QSS文件
        qss_file_path = './tsuki/assets/theme/New_File_Dialog.qss'
        try:
            with open(qss_file_path, 'r', encoding='utf-8') as file:
                qss = file.read()
                dialog.setStyleSheet(qss)
        except Exception as e:
            self.statusBar().showMessage(f'应用QSS样式失败: {e}')
        
        layout = QVBoxLayout(dialog)
        
        name_label = QLabel("文件名:")
        name_input = QLineEdit("")
        name_input.setFont(QFont("Microsoft YaHei", 10))
        layout.addWidget(name_label)
        layout.addWidget(name_input)
        
        type_label = QLabel("文件类型:")
        type_combo = QComboBox()
        type_combo.setFont(QFont("Microsoft YaHei", 10))
        icon_map = self.getIconMap()
        type_combo.addItem('[自定][读取你输入的文件名里面的后缀]')
        type_combo.addItems(list(icon_map.keys()))
        layout.addWidget(type_label)
        layout.addWidget(type_combo)
        
        encoding_label = QLabel("编码:")
        encoding_combo = QComboBox()
        encoding_combo.setFont(QFont("Microsoft YaHei", 10))
        encoding_combo.addItems(["UTF-8", "GBK", "ASCII", "ISO-8859-1"])
        layout.addWidget(encoding_label)
        layout.addWidget(encoding_combo)
        
        button_layout = QHBoxLayout()
        ok_button = QPushButton("确定")
        ok_button.setFont(QFont("Microsoft YaHei", 10))
        skip_button = QPushButton("跳过")
        skip_button.setFont(QFont("Microsoft YaHei", 10))
        button_layout.addWidget(ok_button)
        button_layout.addWidget(skip_button)
        layout.addLayout(button_layout)
        
        ok_button.clicked.connect(dialog.accept)
        skip_button.clicked.connect(dialog.reject)
        
        if dialog.exec_() == QDialog.Accepted:
            file_name = name_input.text().strip()
            file_type = type_combo.currentText()
            
            if file_type == '[自定][读取你输入的文件名里面的后缀]':
                # 如果选择了自定义，则从文件名中提取后缀
                _, extension = os.path.splitext(file_name)
                if not extension:
                    extension = '.txt'  # 如果没有后缀，默认为.txt
            else:
                extension = file_type
            
            if not file_name:
                tab_name = f"无名文本{extension}"
            else:
                if not file_name.endswith(extension):
                    tab_name = f"{file_name}{extension}"
                else:
                    tab_name = file_name
            
            file_encoding = encoding_combo.currentText()
        else:
            tab_name = "未命名文档.txt"
            file_encoding = "UTF-8"
        
        return tab_name, file_encoding

    def getIconMap(self):
        return {
            '.exe': './tsuki/assets/GUI/resources/language/exe.png',
            '.py': './tsuki/assets/GUI/resources/language/python.png',
            '.cpp': './tsuki/assets/GUI/resources/language/cpp.png',
            '.c' : './tsuki/assets/GUI/resources/language/c.png',
            '.java': './tsuki/assets/GUI/resources/language/java.png',
            '.class' : './tsuki/assets/GUI/resources/language/class.png',
            '.txt': './tsuki/assets/GUI/resources/language/text_file.png',
            '.md': './tsuki/assets/GUI/resources/language/markdown.png',
            '.markdown': './tsuki/assets/GUI/resources/language/markdown.png',
            '.html': './tsuki/assets/GUI/resources/language/html.png',
            '.css': './tsuki/assets/GUI/resources/language/css.png',
            '.js': './tsuki/assets/GUI/resources/language/javascript.png',
            '.php': './tsuki/assets/GUI/resources/language/php.png',
            '.json': './tsuki/assets/GUI/resources/language/json.png',
            '.otf': './tsuki/assets/GUI/resources/language/otf.png',
        }

    def getIconPath(self, file_name):
        fileExt = os.path.splitext(file_name)[1].lower()
        
        icon_map = self.getIconMap()
        
        if not fileExt:
            icon_path = './tsuki/assets/GUI/resources/language/text.png'
        elif fileExt in icon_map:
            icon_path = icon_map[fileExt]
        else:
            icon_path = './tsuki/assets/GUI/resources/language/unknown.png'
        
        # logging.info(f"为文件 {file_name} 选择图标: {icon_path}")
        
        if not os.path.isfile(icon_path):
            logging.warning(f"图标文件不存在: {icon_path}，使用默认图标")
            icon_path = './tsuki/assets/GUI/resources/language/unknown.png'
            if not os.path.isfile(icon_path):
                logging.error(f"默认图标文件也不存在: {icon_path}")
                return None
        return icon_path

    def updateTabIconOnTextChange(self, index):
        textEdit = self.tabWidget.widget(index)
        if isinstance(textEdit, QPlainTextEdit):
            content = textEdit.toPlainText()
            first_line = content.split('\n', 1)[0] if content else ''
            if '.' in first_line:
                file_extension = first_line.rsplit('.', 1)[-1].lower()
                new_tab_name = f"未命名.{file_extension}"
            else:
                new_tab_name = self.tabWidget.tabText(index)
            
            self.tabWidget.setTabText(index, new_tab_name)
            self.updateTabIcon(index)

    def updateTabIcon(self, index):
        tab_text = self.tabWidget.tabText(index)
        icon_path = self.getIconPath(tab_text)
        self.tabWidget.setTabIcon(index, QIcon(icon_path))
        # logging.info(f"图标更新成功: {icon_path}")
        

    def saveFile(self):
        savefile.saveFile(self)

    def closeFile(self):
        m = self.tabWidget.currentIndex()
        if m == -1: return
        currentWidget = self.tabWidget.currentWidget()
        content = currentWidget.toPlainText() 
        n = self.autoSave(content)
        if (n == 0): self.closeTab(m)

    def closeTab(self, index):
        try:
            tab_count = self.tabWidget.count()
            tab_now = self.tabWidget.count() -1 
            if tab_count > 1:
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
        config_file_path = './tsuki/assets/app/config/update/update.cfg'
        version_url = 'https://zzbuaoye.us.kg/TsukiNotes/version.txt'
        if os.path.exists(config_file_path):
            config = configparser.ConfigParser()
            config.read(config_file_path)
            beta_version_status = config.get('BetaVersion', 'BetaVersion', fallback='off')
            match beta_version_status:
                case 'Activity':
                    version_url = 'https://zzbuaoye.us.kg/TsukiNotes/Beta/version.txt'
                case _:
                    version_url = 'https://zzbuaoye.us.kg/TsukiNotes/version.txt'
        
        version = self.current_version
        try:
            response = requests.get(version_url, timeout=60)
            if response.status_code == 200:
                latest_version = response.text.strip()
                self.statusBar().showMessage(
                    f'TsukiUpdate: 检测到云端版本号为:[ {latest_version} ] | 本地版本号:[ {version} ] 开始对比...')
                logger.info(f"[Log/INFO]Check For Updates: {latest_version}")
                match latest_version:
                    case _ if latest_version == self.current_version:
                        QMessageBox.information(self, 'TsukiNotes 检测更新 | 成功 | 🔰',
                                                f'当前已经是最新版本✔: {latest_version} ！')
                        self.statusBar().showMessage(f'TsukiUpdate: 检测成功✔！您已经是最新的版本：{latest_version}')
                        logger.info(f"[Log/INFO]Check For Updates: {latest_version}")

                    case _ if latest_version < self.current_version:
                        QMessageBox.warning(self, 'TsukiNotes',
                                            f'🚫您太超前了！云端没你更新快！！🚫')
                        self.statusBar().showMessage(f'TsukiUpdate❓: [ 当前版本号{version} > 云端{latest_version} ] 您可能不是Fv通道')
                        logger.warning(f"[Log/WARNING]Check For Updates: {latest_version}")

                    case _ if latest_version > self.current_version:
                        reply = QMessageBox.question(self, 'TsukiNotes 检测更新 | 成功 | Successful',
                                                    f'🔰✔叮！\nTsukiNotes有全新版本啦！\n最新版本号: {latest_version}\n您的版本号: {version} \n 文件: [Tsuki Notes {latest_version}]',
                                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                        self.statusBar().showMessage(f'TsukiUpdate✔: 检测成功！您有新版本：{latest_version}')
                        logger.info(f"[Log/INFO]Check For Updates: {latest_version}")

                        if reply == QMessageBox.Yes:
                            webbrowser.open('https://zzbuaoye.us.kg/TsukiNotes/download_url')  # 根据实际情况修改下载链接
                            logger.info(f"[Log/INFO]Open Web")
                    case _:
                        QMessageBox.warning(self, '检测更新',
                                            f'[未能成功检测最新版本]\n可能是你的客户端过新导致的\n我们建议您尝试手动更新！\n当前版本: {version}|云端: {latest_version}\n')
                        logger.warning(f"[Log/ERROR]Warn,Client Version So New")
            else:
                QMessageBox.warning(self, '检测更新失败',
                                    f'[无法获取版本信息]\n这可能是因为服务器掉线导致的\n当然您需要自行检测您的网络是否正常\n我们将为你启动备选方案\n请您尝试手动更新吧\n是否打开？\n ')

        except Exception as e:
            QMessageBox.critical(self, '检测更新|错误',
                                f'出错啦！ \nOccurred:\n{str(e)}\n 您可以尝试使用加速器加速GitHub\n 或者尝试手动更新吧')
            logger.error(f"[Log/ERROR]Check For Updates Error: {e}")
            self.statusBar().showMessage(f'TsukiUpdate❌: 检测失败！')

    def url_msg(self):
        versiongj = self.version_gj
        versiontime = self.update_Date
        version = self.current_version
        versiontd = self.version_td
        version_url = f'https://zzbuaoye.us.kg/TsukiNotes/{version}/update.txt'

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
        msgBox.setWindowTitle(f"检测更新 | 您的版本Ver{version} | TsukiNotes")
        msgBox.setText(
            f"Hey,您现在使用的是：\n[备用]更新方案\n[推荐🔰]自动检测\n若无法成功检测，建议打开魔法再次尝试\nVersion:{version}\nTsukiNotes 2024")
        msgBox.setIcon(QMessageBox.Information)  # 使用QMessageBox的内置图标类型
        self.statusBar().showMessage(f'TsukiUpdate[2]: 您已选择了手动更新 ')
        
        # 加载QSS文件
        qss_file_path = './tsuki/assets/theme/Update_Dialog_OnHand.qss'
        try:
            with open(qss_file_path, 'r', encoding='utf-8') as file:
                qss = file.read()
                msgBox.setStyleSheet(qss)
        except Exception as e:
            logger.error(f"加载更新对话框样式失败: {e}")

        yesButton = QPushButton("下载源1-OD")
        source2Button = QPushButton("下载源2-123")
        websiteButton = QPushButton("Github")
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
            webbrowser.open('https://github.com/buaoyezz/TsukiNotes')
            self.statusBar().showMessage(f'TsukiUpdate[2]✔: 您已选择浏览zzbuaoye0已经为您跳转至浏览器')
            logger.info(f"[Log/INFO]Open Web {webbrowser.open}")
        elif msgBox.clickedButton() == newversionButton:
            webbrowser.open(f'https://zzbuaoye.us.kg/TsukiNotes/{version}/update.txt')
            logger.info(f"[Log/INFO]Open Web {webbrowser.open}")
        elif msgBox.clickedButton() == cancelButton:
            self.statusBar().showMessage(f'TsukiUpdate[2]🚫: 您已取消操作')
            logger.info(f"[Log/INFO]UserChannel")

    def versionnow(self):
        version = self.current_version
        QMessageBox.information(self, '当前版本', f'当前版本：[ {version} ]')
        self.statusBar().showMessage(f'✔叮叮！检测成功！您当前版本为：{version}')
        logger.info(f"[Log/INFO]Open VersionNow.def look New Version\n")

    def aboutMessage(self):
        current_version = self.current_version
        versiongj = self.version_gj
        version_td = self.version_td
        about_text = "<h1> TsukiNotes </h1><p><strong>BY ZZBuAoYe 2024</p></strong><strong><p>ZZBuAoYe | " \
                     f"{current_version} {version_td}</strong></p>"
        QMessageBox.about(self, f"About TsukiNotes | #{versiongj}", about_text)
        self.statusBar().showMessage(f'TsukiBack✔: 您打开了AboutMessage')
        logger.info(f"[Log/INFO]Open AboutMessage.def look New Version")

    def aboutDetails(self):
        versiongj = self.version_gj
        about_text = f"[软件信息]\n | 软件出品:MoonZZ \n | 时间：{self.update_Date}\n | {self.version_td} \nZZBuAoYe 2024©Copyright\n"
        QMessageBox.about(self, f"AboutSoftWare | #{self.version_gj}", about_text)
        self.statusBar().showMessage(f'TsukiINFO: [{versiongj}] | [{self.version_td}] | [{self.update_Date}] ')
        logger.info(f"[Log/INFO]Open AboutDetails.def")


    def getOnlineUpdateText(self):
        try:
            ver = self.current_version
            update_log_url = f'https://zzbuaoye.us.kg/TsukiNotes/{ver}/update.txt'
            response = requests.get(update_log_url)
            
            if response.status_code == 200:
                return response.text
            else:
                return "<p style='text-align: center;'>无法获取在线更新日志，请检查网络连接或稍后再试。</p>"
        except Exception as e:
            logger.error(f"[Log/ERROR]Failed to fetch online update log: {e}")
            return "<p style='text-align: center;'>发生错误：无法获取在线更新日志。</p>"


    def online_updateMessage(self):
        version = self.current_version 
        versiontime = self.version_gj  
        version_td = self.version_td
        update_time = self.update_Date
        online_update_text = self.getOnlineUpdateText()

        update_text = (
            "<html>"
            "<h2 style='text-align: left;'>| TsukiNotes Online Update Information🌐</h2>"
            f"<p style='text-align: center;'>Version:{version} {version_td}[{update_time}]</p>"
            "</html>"
            f"======================================================================================<br>"
            f"{online_update_text}<br>"
            f"======================================================================================<br>"
            f"<p style='text-align: center;'>[+代表细节优化|*代表重要改动]</p>"
            f"<p style='text-align: center;'> || {version_td} ||</p>"
            f"<p style='text-align: center;'>[内部版本号:{versiontime}]</p>"
        )

        dialog = QDialog(self)
        dialog.setWindowTitle(f"TsukiNotes[{version}]在线更新日志 -Ver{version}{version_td}")
        dialog.resize(600, 300)

        layout = QVBoxLayout(dialog)
        label = QLabel()
        label.setTextFormat(Qt.RichText)
        label.setText(update_text)
        layout.addWidget(label)
        label_font = QFont('Microsoft YaHei UI')
        label.setFont(label_font)
        label.setAlignment(Qt.AlignLeft)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(dialog.accept)
        layout.addWidget(button_box)
        dialog.exec_()

        self.statusBar().showMessage('TsukiBack✔: 您查看了更新日志')
        logger.info(f"[Log/INFO]Open Update Information Succeed")



    def renameTab(self):
        current_index = self.tabWidget.currentIndex()
        
        dialog = ReNameDialog(self, "重命名", "新的名称:")
        
        qss_file_path = './tsuki/assets/theme/Tab_Rename.qss'
        try:
            with open(qss_file_path, 'r') as file:
                qss = file.read()
                dialog.setStyleSheet(qss)
        except Exception as e:
            self.statusBar().showMessage(f'应用QSS样式失败: {e}')

        if dialog.exec_() == QDialog.Accepted:
            tab_name = dialog.getText()
            if tab_name:
                self.tabWidget.setTabText(current_index, tab_name)
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
        for index in range(self.tabWidget.count()):
            currentWidget = self.tabWidget.widget(index)
            content = currentWidget.toPlainText()  # 获取当前标签页的文本内容
            n = self.autoSave(content)
            if n == -1:
                event.ignore()
                return
        event.accept()

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


    def textChanged(self):
        self.text_modified = True

    def performSearch(self):
        search_dialog = QDialog(self)
        search_dialog.setWindowTitle('搜索')
        search_dialog.resize(300, 100)
        search_dialog.setFont(QFont("Microsoft YaHei"))

        # 加载QSS文件
        qss_file_path = './tsuki/assets/theme/Search_Perform_Dialog.qss'
        try:
            with open(qss_file_path, 'r', encoding='utf-8') as file:
                qss = file.read()
                search_dialog.setStyleSheet(qss)
        except Exception as e:
            logger.error(f"加载搜索对话框样式失败: {e}")

        layout = QVBoxLayout(search_dialog)
        
        search_input = QLineEdit()
        search_input.setPlaceholderText('请输入搜索内容')
        layout.addWidget(search_input)

        button_layout = QHBoxLayout()
        search_button = QPushButton('搜索')
        cancel_button = QPushButton('取消')
        button_layout.addWidget(search_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        search_button.clicked.connect(search_dialog.accept)
        cancel_button.clicked.connect(search_dialog.reject)

        if search_dialog.exec_() == QDialog.Accepted:
            search_text = search_input.text()
            if search_text:
                current_widget = self.tabWidget.currentWidget()
                if isinstance(current_widget, QPlainTextEdit):
                    text = current_widget.toPlainText()
                    self.search_results = []
                    for match in re.finditer(re.escape(search_text), text):
                        start = match.start()
                        end = match.end()
                        self.search_results.append((int(start), int(end), match.group()))
                    
                    if self.search_results:
                        dialog = SearchResultDialog(self.search_results, self)
                        dialog.exec_()
                    else:
                        QMessageBox.information(self, '搜索结果', '未找到匹配项')
                else:
                    QMessageBox.warning(self, '错误', '当前标签页不支持搜索')

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
        config = configparser.ConfigParser()
        default_image_path = './tsuki/assets/app/default/default_light.png'
        config_path = 'tsuki/assets/app/cfg/background/background_color.ini'
        
        try:
            # 读取配置文件
            config.read(config_path, encoding='utf-8')
            
            # 获取背景图片路径
            image_path = config.get('Background', 'image_path', fallback=default_image_path)
            
            # 检查图片路径是否存在
            if image_path and os.path.exists(image_path):
                style_sheet_image = f'background-image: url("{image_path}");'
                message = f'成功加载背景图片 {image_path}！'
            else:
                image_path = default_image_path
                style_sheet_image = f'background-image: url("{image_path}");'
                message = f'背景图片不存在，加载默认背景图片 {image_path}！'
            
            # 更新当前 widget 的样式表
            current_widget = self.tabWidget.currentWidget()
            if current_widget:
                current_widget.setStyleSheet(style_sheet_image)
            
            # 显示状态信息
            self.statusBar().showMessage(f'TsukiBC✔: {message}')
            logger.info(f"[Log/INFO] {message}")
            
            # 更新配置文件中的图片路径
            config['Background'] = {'image_path': image_path}
            with open(config_path, 'w', encoding='utf-8') as configfile:
                config.write(configfile)
        
        except Exception as e:
            self.statusBar().showMessage(f'TsukiBC❌: 未找到保存的背景设置或加载失败。')
            logger.error(f"[Log/ERROR] Background Color Load Error: {str(e)}")



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

    def saveBackgroundSettings(self, image_path, transparency=100):
        config_path = "tsuki/assets/app/cfg/background/TN_BackGround.ini"
        config = configparser.ConfigParser()
        config['Background'] = {
            'ImagePath': image_path,
            'Transparency': transparency
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
        download_url = "https://zzbuaoye.us.kg/TsukiNotes/logo.ico"
        manual_download_url = "https://www.123pan.com/s/ZhtbVv-plgV3.html"
        if ctypes.windll.shell32.IsUserAnAdmin():
            # 如果用户是管理员
            if download_and_set_icon(download_url, icon_path):
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
            QMessageBox.information(self,"高亮模式","Highlight Mode Enabled\nSupport Language: MD Py Java Cpp")
        else:
            self.highlight_keywords = False
            QMessageBox.information(self,"高亮模式","Highlight Mode Disabled\n")
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
            if current_widget is None:
                raise ValueError("当前没有选中的小部件")
            logger.info(f"当前小部件类型: {type(current_widget)}")
            
            if not isinstance(current_widget, (QPlainTextEdit, QTextEdit)):
                raise TypeError("当前小部件不是 QPlainTextEdit 或 QTextEdit 类型")
            
            # 对 QPlainTextEdit 和 QTextEdit 应用不同的设置
            if isinstance(current_widget, QPlainTextEdit):
                current_font = current_widget.font()
                default_font_size = 11
                current_font.setPointSize(default_font_size)

                if custom_lines == 0:
                    current_widget.setLineWrapMode(QPlainTextEdit.WidgetWidth)
                else:
                    current_widget.setLineWrapMode(QPlainTextEdit.FixedPixelWidth)
                    current_widget.setFixedHeight(current_widget.fontMetrics().lineSpacing() * custom_lines)

                current_widget.setFont(current_font)
            
            elif isinstance(current_widget, QTextEdit):
                current_font = current_widget.font()
                default_font_size = 11
                current_font.setPointSize(default_font_size)

                if custom_lines == 0:
                    current_widget.setLineWrapMode(QTextEdit.WidgetWidth)
                else:
                    current_widget.setLineWrapMode(QTextEdit.FixedPixelWidth)
                    current_widget.setFixedHeight(current_widget.fontMetrics().lineSpacing() * custom_lines)
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
        self.text_modified = False
        options = QFileDialog.Options()
        current_tab_name = self.tabWidget.tabText(self.tabWidget.currentIndex())
        filters = f"所有文件 (*);;文本文件 (*.txt);;Markdown 文件 (*.md);;INI 文件 (*.ini);;XML 文件 (*.xml);" \
                  f"JSON 文件 (*.json);;日志文件 (*.log);;Python 文件 (*.py);;C 文件 (*.c)"
        fileName, selectedFilter = QFileDialog.getSaveFileName(self, f'保存文件 - {current_tab_name}', '', filters, options=options)
        if fileName:
            currentWidget = self.tabWidget.currentWidget()
            text = currentWidget.toPlainText()
            encoding = 'utf-8'  # 默认编码
            encoding_options = {
                '文本文件 (*.txt)': 'utf-8',
                'Markdown 文件 (*.md)': 'utf-8',
                'INI 文件 (*.ini)': 'utf-8',
                'XML 文件 (*.xml)': 'utf-8',
                'JSON 文件 (*.json)': 'utf-8',
                '日志文件 (*.log)': 'utf-8',
                'Python 文件 (*.py)': 'utf-8',
                'C 文件 (*.c)': 'utf-8'
            }
            for key, value in encoding_options.items():
                if key in selectedFilter:
                    encoding = value
                    break

            with open(fileName, 'w', encoding=encoding) as file:
                file.write(text)
                QMessageBox.information(self, '保存成功', f'文件 "{fileName}" 已成功保存')
                self.statusBar().showMessage(f'TsukiSave✔: 文件 "{fileName}" 已成功保存')
                logger.info(f"[Log/INFO]Save File Success: {fileName}")
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
        logger.info(f"[Log/INFO]Clear File Success")
        currentWidget.clear()

    def performUndo(self):
        currentWidget = self.tabWidget.currentWidget()
        currentWidget.undo()
        self.statusBar().showMessage('"Tsuki✔: 您执行了一次撤销操作"')
        logger.info(f"[Log/INFO]Undo File Success")

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
                start_index = line.find('时间=') + len('时间=')
                end_index = line.find('ms', start_index)

                time_str = line[start_index:end_index].strip()

                try:
                    return float(time_str)
                except ValueError:
                    return None
        return None

    def pingServerManually(self):
        try:
            ping_host1 = 'zzbuaoye.us.kg'

            delays = self.runPingCommand(ping_host1)

            self.handlePingResult(delays, ping_host1)
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


    def runPingCommand(self, ping_host1):
        result1 = self.runPing(ping_host1)
        return result1

    def handlePingResult(self, delay, ping_host1):
        currentWidget = self.tabWidget.currentWidget()

        if delay is not None:
            info = f'TsukiPingBack - {ping_host1}: {delay} ms'
            color_style = self.getColorStyle(delay)
            currentWidget.setStyleSheet(f"color: {color_style}")
            self.statusBar().showMessage(info)
        else:
            self.handlePingError(f"无法 ping 到 {ping_host1}。")

    def handlePingError(self, error_message):
        ping_host1 = 'zzbuaoye.us.kg'

        server_names = [f'Tsuki Back：{ping_host1}']
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
