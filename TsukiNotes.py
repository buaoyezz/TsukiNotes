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
import threading
import zipfile
from datetime import datetime
from socket import socket
from turtle import color, pos
from packaging import version
import ping3
from PyQt5.QtCore import QSettings, QThread, Qt, QEvent, QFile, QRegExp, QTimer, pyqtSignal, QPoint, QObject, QMetaType, QMetaObject, QLocale, QUrl
from PyQt5.QtGui import QTextCursor
from PyQt5.QtGui import (
    QFont, QIcon, QTextCharFormat, QColor, QTextCursor, QKeySequence, QSyntaxHighlighter,
    QPixmap, QPalette, QBrush, QPainter, QDesktopServices
)
import re
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QFontDialog,
    QTabWidget, QInputDialog, QMenu, QMessageBox, QPushButton, QShortcut,
    QLabel, QTextBrowser, QVBoxLayout, QCheckBox, QWidget, QPlainTextEdit,
    QColorDialog, QDialog, QToolBar, QLineEdit, QDialogButtonBox, QGridLayout,
    QSpacerItem, QSizePolicy, QComboBox, QProgressDialog
)
from PyQt5.QtCore import QSettings, QThread, Qt, QEvent, QFile, QRegExp, QTimer, pyqtSignal,QPoint,QObject,QMetaType, QMetaObject
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
        self.setWindowTitle(self.tr(f"TsukiNotes -Debug Ver{debug_version}"))
        self.setGeometry(100, 100, 800, 600)
        self.setFont(QFont("Microsoft YaHei", 9))
        self.setWindowIcon(QIcon("./tsuki/assets/GUI/ico/logo.ico"))
        
        self.log_counters = {'INFO': 0, 'WARNING': 0, 'ERROR': 0, 'DEBUG': 0}

        layout = QVBoxLayout()
        
        self.log_text_edit = QTextEdit()
        self.log_text_edit.setReadOnly(True)
        layout.addWidget(self.log_text_edit)
        
        self.font_combo = QComboBox()
        self.font_combo.addItems([self.tr("Normal Font Size"),"10","11","12","13", "14","15", "16", "17","18", "19","20","21", "22","365"])
        self.font_combo.currentTextChanged.connect(self.change_font_size)
        layout.addWidget(self.font_combo)
        
        self.stats_label = QLabel(self.tr("Lines: 0\nINFO: 0 | WARNING: 0 | ERROR: 0 | DEBUG: 0"))
        layout.addWidget(self.stats_label)
        
        self.setLayout(layout)
        
        self.log_handler = QTextEditHandler(self.log_text_edit, self.log_counters)
        self.log_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(self.log_handler)
    
    def closeEvent(self, event):
        logging.getLogger().removeHandler(self.log_handler)
        super().closeEvent(event)

    def change_font_size(self, size_str):
        if size_str == self.tr("Normal Font Size"):
            size = 9 
        else:
            size = int(size_str)
        font = QFont()
        font.setPointSize(size)
        self.log_text_edit.setFont(font)
        logging.info(self.tr("Font Size Changed to %s"), size)
    def update_statistics(self):
        total_lines = self.log_text_edit.document().blockCount()
        info_count = self.log_counters.get('INFO', 0)
        warning_count = self.log_counters.get('WARNING', 0)
        error_count = self.log_counters.get('ERROR', 0)
        debug_count = self.log_counters.get('DEBUG', 0)
        self.stats_label.setText(self.tr(f"Lines: {total_lines}\nINFO: {info_count} | WARNING: {warning_count} | ERROR: {error_count} | DEBUG: {debug_count}"))

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
        
        bold_action = QAction(self.tr("Bold"), self)
        bold_action.triggered.connect(self.set_bold)
        menu.addAction(bold_action)
        
        italic_action = QAction(self.tr("Italic"), self)
        italic_action.triggered.connect(self.set_italic)
        menu.addAction(italic_action)
        
        underline_action = QAction(self.tr("Underline"), self)
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
            QMessageBox.warning(self, self.tr('Error'), self.tr(f'Failed to save file: {e}'))
# ==============================================================End Welcome===================================================================================================================

class FileLoaderThread(QThread):
    dataLoaded = pyqtSignal(list)
    updateGui = pyqtSignal(str)  # 新增信号

    def __init__(self, fileName):
        super().__init__()
        self.fileName = fileName

    def run(self):
        chunks = cython_utils.read_file_in_chunks(self.fileName)
        self.dataLoaded.emit(chunks)
        self.updateGui.emit(self.tr("File loaded"))  # 发送信号而不是直接更新 GUI


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
        self.highlightMultilineComments(text)

class PythonHighlighter(SyntaxHighlighter):
    def __init__(self, light=True, parent=None):
        super().__init__(parent)
        self.light = light
        
        # 定义更柔和的颜色
        self.colors = {
            'keyword': "#6A5ACD",
            'builtin': "#4169E1",
            'string': "#32CD32",  # 改为好看见的绿色
            'function': "#8B4513",
            'comment': "#708090",
            'decorator': "#A0522D",
            'number': "#800080",
            'special': "#B22222",
            'qt': "#4682B4",
            'color_code': "#8B008B",
            'class': "#2F4F4F",
            'param': "#696969",
            'operator': "#8B0000",
            'bracket': "#2F4F4F"
        }

        # 创建格式
        self.formats = {key: self.create_format(color) for key, color in self.colors.items()}
        
        # 定义关键词和模式
        self.patterns = {
            'keyword': r"\b(and|as|assert|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|not|or|pass|raise|return|try|while|with|yield|None|True|False|async|await|nonlocal)\b",
            'builtin': r"\b(abs|all|any|ascii|bin|bool|bytearray|bytes|callable|chr|classmethod|compile|complex|delattr|dict|dir|divmod|enumerate|eval|exec|filter|float|format|frozenset|getattr|globals|hasattr|hash|help|hex|id|input|int|isinstance|issubclass|iter|len|list|locals|map|max|memoryview|min|next|object|oct|open|ord|pow|print|property|range|repr|reversed|round|set|setattr|slice|sorted|staticmethod|str|sum|super|tuple|type|vars|zip)\b",
            'string': r'("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\')',
            'function': r"\b([A-Za-z_][A-Za-z0-9_]*(?=\s*\())",
            'comment': r"(#[^\n]*)",
            'decorator': r"(@\w+)",
            'number': r"\b([+-]?[0-9]*\.?[0-9]+(?:[eE][+-]?[0-9]+)?)\b",
            'special': r"(\\[nrtfvb]|/\S+)",
            'qt': r"\b(QMessage|Dialog|QWidget|QMainWindow|QApplication)\b",
            'color_code': r"(#[0-9A-Fa-f]{3,6})",
            'class': r"\b(class\s+(\w+))",
            'param': r"\b(?<=def\s+\w+\()[\w,\s=]+(?=\):)",
            'operator': r"(\+|-|\*|/|%|=|<|>|&|\||\^|~|@)",
            'bracket': r"(\(|\)|\[|\]|\{|\})"
        }

        # 编译正则表达式
        self.regex = {key: QRegExp(pattern) for key, pattern in self.patterns.items()}

    def create_format(self, color):
        format = QTextCharFormat()
        format.setForeground(QColor(color))
        format.setFontWeight(QFont.Bold)
        return format

    def highlightBlock(self, text):
        for key, regex in self.regex.items():
            index = regex.indexIn(text)
            while index >= 0:
                length = regex.matchedLength()
                self.setFormat(index, length, self.formats[key])
                index = regex.indexIn(text, index + length)

        # 特殊处理多行注释
        self.highlightMultilineComments(text)

    def highlightMultilineComments(self, text):
        start = QRegExp(r'"""')
        end = QRegExp(r'"""')
        self.highlightMultiline(text, start, end, self.formats['comment'])

        start = QRegExp(r"'''")
        end = QRegExp(r"'''")
        self.highlightMultiline(text, start, end, self.formats['comment'])

    def highlightMultiline(self, text, start, end, format):
        if self.previousBlockState() == 1:
            startIndex = 0
            add = 0
        else:
            startIndex = start.indexIn(text)
            add = start.matchedLength()

        while startIndex >= 0:
            endIndex = end.indexIn(text, startIndex + add)
            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLength = len(text) - startIndex
            else:
                commentLength = endIndex - startIndex + end.matchedLength()

            self.setFormat(startIndex, commentLength, format)
            startIndex = start.indexIn(text, startIndex + commentLength)

    def rehighlight(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        QSyntaxHighlighter.rehighlight(self)
        QApplication.restoreOverrideCursor()

    def setDocument(self, document):
        super().setDocument(document)
        self.rehighlight()

class CppHighlighter(SyntaxHighlighter):
    def __init__(self, light=True, parent=None):
        super().__init__(parent)
        self.l = light
        
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#FFD700" if light else "#FFA500"))  # 更鲜艳的颜色
        keyword_format.setFontWeight(QFont.Bold)
        keywords = [
            # C关键词
            "auto", "break", "case", "char", "const", "continue", "default", "do",
            "double", "else", "enum", "extern", "float", "for", "goto", "if",
            "int", "long", "register", "return", "short", "signed", "sizeof", "static",
            "struct", "switch", "typedef", "union", "unsigned", "void", "volatile", "while",
            
            # C++额外关键词
            "asm", "bool", "catch", "class", "const_cast", "delete", "dynamic_cast",
            "explicit", "export", "false", "friend", "inline", "mutable", "namespace",
            "new", "operator", "private", "protected", "public", "reinterpret_cast",
            "static_cast", "template", "this", "throw", "true", "try", "typeid",
            "typename", "using", "virtual", "wchar_t",
            
            "alignas", "alignof", "char16_t", "char32_t", "constexpr", "decltype",
            "noexcept", "nullptr", "static_assert", "thread_local",
            
            "abstract", "as", "base", "byte", "checked", "decimal", "delegate", "event",
            "finally", "fixed", "foreach", "in", "interface", "internal", "is", "lock",
            "object", "out", "override", "params", "readonly", "ref", "sbyte", "sealed",
            "stackalloc", "string", "uint", "ulong", "unchecked", "unsafe", "ushort", "var"
        ]
        self.keyword_patterns = [(QRegExp(r"\b" + keyword + r"\b"), keyword_format)
                                 for keyword in keywords]

        quotation_format = QTextCharFormat()
        quotation_format.setForeground(QColor("#32CD32" if light else "#228B22")) 
        self.quotation_pattern = (QRegExp(r"\".*?\"|'.'"), quotation_format) 

        function_format = QTextCharFormat()
        function_format.setFontItalic(True)
        function_format.setForeground(QColor("#00BFFF" if light else "#1E90FF"))  
        self.function_pattern = (QRegExp(r"\b[A-Za-z_][A-Za-z0-9_]*(?=\s*\()"), function_format)

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#FF4500" if light else "#B22222"))  
        self.comment_pattern = (QRegExp(r"//[^\n]*|/\*[\s\S]*?\*/"), comment_format)  

        preprocessor_format = QTextCharFormat()
        preprocessor_format.setForeground(QColor("#8B008B" if light else "#9370DB")) 
        self.preprocessor_pattern = (QRegExp(r"^\s*#\s*\w+"), preprocessor_format)

    def highlightBlock(self, text):
        for pattern, format in self.keyword_patterns:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.highlightPattern(text, self.quotation_pattern)
        self.highlightPattern(text, self.function_pattern)
        self.highlightPattern(text, self.comment_pattern)
        self.highlightPattern(text, self.preprocessor_pattern)

    def highlightPattern(self, text, pattern):
        expression, format = pattern
        index = expression.indexIn(text)
        while index >= 0:
            length = expression.matchedLength()
            self.setFormat(index, length, format)
            index = expression.indexIn(text, index + length)

class JavaHighlighter(SyntaxHighlighter):
    def __init__(self, light=True, parent=None):
        super().__init__(parent)
        self.light = light
        
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#FFD700" if light else "#FFA500"))
        keyword_format.setFontWeight(QFont.Bold)
        keywords = [
            "abstract", "assert", "boolean", "break", "byte", "case",
            "catch", "char", "class", "const", "continue", "default",
            "do", "double", "else", "enum", "extends", "final",
            "finally", "float", "for", "if", "implements",
            "import", "instanceof", "int", "interface", "long",
            "native", "new", "package", "private", "protected",
            "public", "return", "short", "static", "strictfp",
            "super", "switch", "synchronized", "this", "throw", "throws",
            "transient", "try", "void", "volatile", "while",
            "true", "false", "null", "var", "yield", "record", "sealed", "permits"
        ]
        self.keyword_patterns = [(QRegExp(r"\b" + keyword + r"\b"), keyword_format)
                                 for keyword in keywords]

        quotation_format = QTextCharFormat()
        quotation_format.setForeground(QColor("#32CD32" if light else "#228B22"))
        self.quotation_pattern = (QRegExp(r'"(?:\\.|[^"\\])*"'), quotation_format)

        function_format = QTextCharFormat()
        function_format.setFontItalic(True)
        function_format.setForeground(QColor("#00BFFF" if light else "#1E90FF"))
        self.function_pattern = (QRegExp(r"\b[A-Za-z_][A-Za-z0-9_]*(?=\s*\()"), function_format)

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#FF4500" if light else "#B22222"))
        self.single_line_comment_pattern = (QRegExp(r"//[^\n]*"), comment_format)
        self.multi_line_comment_pattern = (QRegExp(r"/\*.*?\*/", QRegExp.DotAll), comment_format)

        annotation_format = QTextCharFormat()
        annotation_format.setForeground(QColor("#8B008B" if light else "#9370DB"))
        self.annotation_pattern = (QRegExp(r"@\w+"), annotation_format)

    def highlightBlock(self, text):
        for pattern, format in self.keyword_patterns:
            self.highlightPattern(text, pattern, format)

        self.highlightPattern(text, *self.quotation_pattern)
        self.highlightPattern(text, *self.function_pattern)
        self.highlightPattern(text, *self.single_line_comment_pattern)
        self.highlightPattern(text, *self.multi_line_comment_pattern)
        self.highlightPattern(text, *self.annotation_pattern)

    def highlightPattern(self, text, pattern, format):
        expression = QRegExp(pattern)
        index = expression.indexIn(text)
        while index >= 0:
            length = expression.matchedLength()
            self.setFormat(index, length, format)
            index = expression.indexIn(text, index + length)


class MarkdownHighlighter(QSyntaxHighlighter):
    def __init__(self, light=True, parent=None):
        super().__init__(parent)
        self.light = light
        # 格式
        self.basic_formatting()
        # 标题
        self.header_format = QTextCharFormat()
        self.header_format.setFontWeight(QFont.Bold)
        self.header_format.setForeground(QColor("#0000FF" if light else "#4169E1"))
        
        self.emphasis_format = QTextCharFormat()
        self.emphasis_format.setFontItalic(True)
        self.emphasis_format.setForeground(QColor("#008000" if light else "#32CD32"))
        
        self.strong_format = QTextCharFormat()
        self.strong_format.setFontWeight(QFont.Bold)
        self.strong_format.setForeground(QColor("#800000" if light else "#CD5C5C"))

        self.link_format = QTextCharFormat()
        self.link_format.setForeground(QColor("#1E90FF" if light else "#87CEFA"))
        self.link_format.setFontUnderline(True)

        self.code_block_format = QTextCharFormat()
        self.code_block_format.setForeground(QColor("#808080" if light else "#A9A9A9"))
        self.code_block_format.setBackground(QColor("#F0F0F0" if light else "#2F4F4F"))

        self.list_format = QTextCharFormat()
        self.list_format.setForeground(QColor("#FF8C00" if light else "#FFA500"))

    def basic_formatting(self):
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#FFD700" if self.light else "#FFA500"))
        keyword_format.setFontWeight(QFont.Bold)
        keywords = [
            "#", "##", "###", "####", "#####", "######", "*", "_", ">", "-",
            "1.", "2.", "3.", "4.", "5.", "6.", "```", "[", "]", "(", ")",
            "!", "!!", "!!!", "!!!!", "!!!!!", "!!!!!!", "~~"
        ]
        self.keyword_patterns = [(QRegExp(re.escape(keyword)), keyword_format)
                                 for keyword in keywords]

        self.quotation_format = QTextCharFormat()
        self.quotation_format.setForeground(QColor("#32CD32" if self.light else "#228B22"))
        self.quotation_pattern = QRegExp(r"`.*`")

        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor("#FF4500" if self.light else "#B22222"))
        self.comment_pattern = QRegExp(r"<!--.*-->")

    def highlightBlock(self, text):
        for pattern, format in self.keyword_patterns:
            self.highlight_pattern(text, pattern, format)
        self.highlight_pattern(text, self.quotation_pattern, self.quotation_format)
        self.highlight_pattern(text, self.comment_pattern, self.comment_format)
        self.highlight_headers(text)
        self.highlight_emphasis_and_strong(text)
        self.highlight_links(text)
        self.highlight_code_blocks(text)
        self.highlight_lists(text)

    def highlight_pattern(self, text, pattern, format):
        expression = QRegExp(pattern)
        index = expression.indexIn(text)
        while index >= 0:
            length = expression.matchedLength()
            self.setFormat(index, length, format)
            index = expression.indexIn(text, index + length)

    def highlight_headers(self, text):
        expression = QRegExp(r"^#{1,6}\s.*$")
        self.highlight_pattern(text, expression, self.header_format)

    def highlight_emphasis_and_strong(self, text):
        self.highlight_pattern(text, r"\*[^\*]+\*", self.emphasis_format)
        self.highlight_pattern(text, r"_[^_]+_", self.emphasis_format)
        self.highlight_pattern(text, r"\*\*[^\*]+\*\*", self.strong_format)
        self.highlight_pattern(text, r"__[^_]+__", self.strong_format)

    def highlight_links(self, text):
        expression = QRegExp(r"\[([^\]]+)\]\(([^\)]+)\)")
        self.highlight_pattern(text, expression, self.link_format)

    def highlight_code_blocks(self, text):
        expression = QRegExp(r"```[\s\S]*?```")
        self.highlight_pattern(text, expression, self.code_block_format)

    def highlight_lists(self, text):
        expression = QRegExp(r"^\s*[\*\+\-]\s")
        self.highlight_pattern(text, expression, self.list_format)
        expression = QRegExp(r"^\s*\d+\.\s")
        self.highlight_pattern(text, expression, self.list_format)

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
        sidebar.addItem("语言设置") 
        sidebar.addItem("调试设置")
        sidebar.addItem("关于设置")
        sidebar.currentRowChanged.connect(self.display)

        self.stack = QStackedWidget(self)
        self.stack.addWidget(self.interfacePage())
        self.stack.addWidget(self.fontPage())
        self.stack.addWidget(self.languagePage())  # 添加语言设置页面
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

    def languagePage(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        title_label = QLabel("| 语言设置", self)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px; 
                font-family: "Microsoft YaHei";
                font-weight: bold;
                color: #333333;
                padding: 10px;
                border-bottom: 2px solid #e0e0e0;
            }
        """)
        layout.addWidget(title_label, alignment=Qt.AlignLeft | Qt.AlignTop)

        language_layout = QHBoxLayout()
        language_layout.setContentsMargins(20, 20, 20, 20)
        language_layout.setSpacing(15)

        # 创建语言选择下拉框
        self.language_combobox = QComboBox()
        self.language_combobox.setStyleSheet("""
            QComboBox {
                border: 1px solid #c0c0c0;
                border-radius: 3px;
                padding: 5px;
                min-width: 150px;
                font-family: "Microsoft YaHei";
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #c0c0c0;
                border-left-style: solid;
                font-family: "Microsoft YaHei";
            }
        """)
        available_languages = self.parent().list_available_languages()
        self.language_combobox.addItems(available_languages)
        language_layout.addWidget(QLabel("选择语言：", font=QFont("Microsoft YaHei")), 1)
        language_layout.addWidget(self.language_combobox, 2)

        # 创建确定按钮
        confirm_button = self.createButton("确定", self.confirmLanguageChange)
        language_layout.addWidget(confirm_button, 1)

        # 创建打开语言文件夹按钮
        open_folder_button = self.createButton("打开语言文件夹", self.openLanguageFolder)
        language_layout.addWidget(open_folder_button, 1)

        layout.addLayout(language_layout)

        return page

    def openLanguageFolder(self):
        language_folder = './tsuki/assets/languages/'
        QDesktopServices.openUrl(QUrl.fromLocalFile(language_folder))

    def confirmLanguageChange(self):
        selected_language = self.language_combobox.currentText()
        self.parent().change_language(selected_language)
        QMessageBox.information(self, "语言设置", f"语言已更改为：{selected_language}")

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
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 创建水平布局来放置logo和文字
        h_layout = QHBoxLayout()

        # 添加logo
        logo_label = QLabel()
        logo_pixmap = QPixmap("./tsuki/assets/GUI/resources/GUI/logo.png")
        logo_label.setPixmap(logo_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        h_layout.addWidget(logo_label, alignment=Qt.AlignLeft | Qt.AlignTop)

        # 创建垂直布局来放置标题和关于文字
        v_layout = QVBoxLayout()

        # 添加标题
        title_label = QLabel("关于 TsukiNotes", self)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px; 
                font-family: "Microsoft YaHei";
                font-weight: bold;
                color: #333333;
            }
        """)
        v_layout.addWidget(title_label, alignment=Qt.AlignLeft | Qt.AlignTop)

        version_label = QLabel(f"Version: {self.parent().current_version} {self.parent().version_td}", self)
        version_label.setStyleSheet("""
            QLabel {
                font-size: 14px; 
                font-family: "Microsoft YaHei";
                color: #666666;
            }
        """)
        v_layout.addWidget(version_label, alignment=Qt.AlignLeft | Qt.AlignTop)

        about_label = QLabel("""
            TsukiNotes 是一款功能强大的记事本软件，现已支持:
                             
            • 支持文本高亮显示
            • 可打开16进制文件
            • 支持Python、C++、Java和Markdown语法高亮
            • 基于Qt内核，提供优秀的图形界面
            • 丰富的QSS样式，带来美观的视觉体验
            • 强大的搜索功能
            • 超越Windows记事本的使用体验
            • 支持多标签页,更高的效率
            • 新的设计，新的思路，新的体验

            探索更多精彩功能！无限可能！
        """)
        about_label.setStyleSheet("""
            QLabel {
                font-size: 14px; 
                font-family: "Microsoft YaHei";
                color: #333333;
                line-height: 1.5;
            }
        """)
        about_label.setWordWrap(True)
        v_layout.addWidget(about_label, alignment=Qt.AlignLeft | Qt.AlignTop)
        h_layout.addLayout(v_layout)
        layout.addLayout(h_layout)

        copyright_label = QLabel("© TsukiNotes 2022-2024 ZZBuAoYe. All rights reserved.", self)
        copyright_label2 = QLabel("GPL-3.0 License", self)
        style = "QLabel {font-size: 12px; font-family: 'Microsoft YaHei'; color: #999999;}"
        copyright_label.setStyleSheet(style)
        copyright_label2.setStyleSheet(style)
        layout.addWidget(copyright_label, alignment=Qt.AlignCenter)
        layout.addWidget(copyright_label2, alignment=Qt.AlignCenter)
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

    def changeLanguage(self, language_code):
        self.parent().change_language(language_code)
        QMessageBox.information(self, "语言更改", f"语言已更改为: {language_code}")


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
        QMetaType.type("QTextCursor")
        self.before = ''
        self.current_version = '1.5.7' 
        self.real_version = '1.5.7'
        self.update_Date = '2024/10/19'
        self.version_td = 'Release'
        self.version_gj = 'b-v157B-241019R'
        self.config_file = './tsuki/assets/app/config/launch/launch_config.ini'  
        self.load_langs()

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
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)
        
        self.setTabCloseButtonStyle()
        self.tabWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tabWidget.customContextMenuRequested.connect(self.showTabContextMenu)

        self.add_tab_button = QPushButton()
        self.add_tab_button.setIcon(QIcon('./tsuki/assets/GUI/resources/tips.png'))
        self.add_tab_button.setFixedSize(24, 24)
        self.add_tab_button.clicked.connect(self.newFile)
        self.tabWidget.setCornerWidget(self.add_tab_button, Qt.TopRightCorner)
        self.loadAllStyles()
        
    def load_langs(self):
        language_folder = './tsuki/assets/languages/'
        default_language = 'zh-cn'  # 默认语言
        system_language = QLocale.system().name()[:2]

        # 尝试加载系统语言文件,如果不存在则使用默认语言
        language_file = os.path.join(language_folder, f'{system_language}.json')
        if not os.path.exists(language_file):
            language_file = os.path.join(language_folder, f'{default_language}.json')

        self.load_language_file(language_file)

    def load_language_file(self, language_file):
        try:
            with open(language_file, 'r', encoding='utf-8') as f:
                self.translations = json.load(f)
        except Exception as e:
            logger.error(f"加载语言文件失败: {e}")
            self.translations = {}

    def tr(self, text):
        return self.translations.get(text, text)

    def list_available_languages(self):
        language_folder = './tsuki/assets/languages/'
        default_language_folder = './tsuki/assets/languages/'
        languages = []
        
        if os.path.exists(language_folder):
            for file in os.listdir(language_folder):
                if file.endswith('.json'):
                    languages.append(file.replace('.json', ''))
        else:
            for file in os.listdir(default_language_folder):
                if file.endswith('.json'):
                    languages.append(file.replace('.json', ''))
        
        return languages

    def change_language(self, language_code):
        language_folder = './tsuki/assets/languages/'
        language_file = os.path.join(language_folder, f'{language_code}.json')
        if os.path.exists(language_file):
            self.load_language_file(language_file)
            logger.info(f"语言已更改为: {language_code}")
        else:
            logger.error(f"语言文件不存在: {language_file}")
    
    
    def loadAllStyles(self):
        tab_bar_style = """
        QTabBar::tab {
            background-color: #f0f0f0;
            color: #333333;
            border: 1px solid #c0c0c0;
            padding: 5px 10px;
            margin-right: 2px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }
        QTabBar::tab:selected, QTabBar::tab:hover {
            background-color: #ffffff;
        }
        QTabBar::tab:selected {
            border-bottom-color: #ffffff;
        }
        QTabBar::close-button {
            image: url(./tsuki/assets/GUI/resources/error.png);
            subcontrol-position: right;
        }
        QTabBar::close-button:hover {
            image: url(./tsuki/assets/GUI/resources/off_file.png);
        }
        QPushButton#addTabButton {
            border: none;
            background-color: transparent;
        }
        QPushButton#addTabButton:hover {
            background-color: #e0e0e0;
        }
        """

        scrollbar_style = ""
        qss_file_path = './tsuki/assets/theme/Main_Scrollbar_Style.qss'
        try:
            with open(qss_file_path, 'r', encoding='utf-8') as file:
                scrollbar_style = file.read()
        except Exception as e:
            logging.error(f"加载滚动条样式失败: {e}")
            QMessageBox.warning(self, "样式加载错误", f"加载滚动条样式失败: {e}")

        combined_style = tab_bar_style + scrollbar_style
        self.setStyleSheet(combined_style)


    def showTabContextMenu(self, pos):
        index = self.tabWidget.tabBar().tabAt(pos)
        menu = QMenu(self)

        if index != -1:
            rename_action = menu.addAction("重命名标签")
            rename_action.triggered.connect(lambda: self.renameTab(index))

            close_action = menu.addAction("关闭标签")
            close_action.triggered.connect(lambda: self.closeTab(index))
        else:
            new_tab_action = menu.addAction("新建标签")
            new_tab_action.triggered.connect(self.newFile)

        menu.exec_(self.tabWidget.mapToGlobal(pos))


    def setTabCloseButtonStyle(self):
        style = """
        QTabBar::close-button {
            image: url(./tsuki/assets/GUI/resources/error.png);
        }
        QTabBar::close-button:hover {
            image: url(./tsuki/assets/GUI/resources/off_file.png);
        }
        """
        self.setStyleSheet(style)

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
        self.setWindowIcon(QIcon('./tsuki/assets/GUI/resources/GUI/logo.png'))
        logging.debug("initUI initialization is complete")
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)
        

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
        self.newAct = QAction(QIcon('./tsuki/assets/GUI/resources/create_tab.png'), self.tr('创建新的标签页（Ctrl+T）'), self)
        self.newAct.triggered.connect(self.newFile)

        self.openAct = QAction(QIcon('./tsuki/assets/GUI/resources/import_file.png'), self.tr('打开文件（Ctrl+O）'), self)
        self.openAct.triggered.connect(self.openFile)

        self.saveAct = QAction(QIcon('./tsuki/assets/GUI/resources/save_file.png'), self.tr('保存修改（Ctrl+S）'), self)
        self.saveAct.triggered.connect(self.saveFile)

        self.closeAct = QAction(QIcon('./tsuki/assets/GUI/resources/off_file.png'), self.tr('关闭文件（Ctrl+W）'), self)
        self.closeAct.triggered.connect(self.closeFile)

        self.fontAct = QAction(QIcon('./tsuki/assets/GUI/resources/font_reset_change.png'), self.tr('修改字体'), self)
        self.fontAct.triggered.connect(self.changeFont)

        self.setfontsizeAct = QAction(QIcon('./tsuki/assets/GUI/resources/font_size_reset_tab.png'), self.tr('字体大小'), self)
        self.setfontsizeAct.triggered.connect(self.set_font_size)
                                

        self.checkUpdateAct = QAction(QIcon('./tsuki/assets/GUI/resources/update_cloud.png'), self.tr('检查更新'), self)
        self.checkUpdateAct.triggered.connect(self.checkForUpdates)

        self.aboutAct = QAction(QIcon('./tsuki/assets/GUI/resources/about.png'), self.tr('关于Tsuki版本信息'), self)
        self.aboutAct.triggered.connect(self.aboutMessage)

        self.aboutDetailsAct = QAction(QIcon('./tsuki/assets/GUI/resources/about.png'), self.tr('关于Tsuki详细信息'), self)
        self.aboutDetailsAct.triggered.connect(self.aboutDetails)

        self.exitAct = QAction(QIcon('./tsuki/assets/GUI/resources/exit_software.png'), self.tr('退出程序'), self)
        self.exitAct.triggered.connect(self.close)

        self.resetFontAct = QAction(QIcon('./tsuki/assets/GUI/resources/font_reset_change.png'), self.tr('重置字体'), self)
        self.resetFontAct.triggered.connect(self.resetFont)

        self.update2Act = QAction(QIcon('./tsuki/assets/GUI/resources/update_cloud.png'), self.tr('手动检测更新'), self)
        self.update2Act.triggered.connect(self.update2)

        self.renameTabAct = QAction(QIcon('./tsuki/assets/GUI/resources/font_size_reset_tab.png'), self.tr('重命名标签'), self)
        self.renameTabAct.triggered.connect(self.renameTab)

        self.pingServerManuallyAct = QAction(QIcon('./tsuki/assets/GUI/resources/server_ping.png'), self.tr('手动Ping服务器'), self)
        self.pingServerManuallyAct.triggered.connect(self.pingServerManually)

        self.url_msgAct = QAction(QIcon('./tsuki/assets/GUI/resources/server_tb.png'), self.tr('测试服务器返回'), self)
        self.url_msgAct.triggered.connect(self.url_msg)

        self.versionnowAct = QAction(QIcon('./tsuki/assets/GUI/resources/custom_server.png'), self.tr('当前版本号'))
        self.versionnowAct.triggered.connect(self.versionnow)

        self.online_updateMessageAct = QAction(QIcon('./tsuki/assets/GUI/resources/update_cloud.png'), self.tr('在线更新日志'))
        self.online_updateMessageAct.triggered.connect(self.online_updateMessage)

        self.settingsAction = QAction(QIcon('./tsuki/assets/GUI/resources/open_list.png'), self.tr('设置'), self)
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
        fileMenu = menubar.addMenu(self.tr('文件'))
        fileMenu.addAction(self.newAct)
        fileMenu.addAction(self.openAct)
        fileMenu.addAction(self.saveAct)
        fileMenu.addAction(self.closeAct)
        fileMenu.addAction(self.exitAct)
        
        editMenu = menubar.addMenu(self.tr('编辑'))
        editMenu.addAction(self.fontAct)
        editMenu.addAction(self.resetFontAct)
        editMenu.addAction(self.renameTabAct)
        editMenu.addAction(self.setfontsizeAct)

        updateMenu = menubar.addMenu(self.tr('更新'))
        updateMenu.addAction(self.checkUpdateAct)
        updateMenu.addAction(self.update2Act)
        updateMenu.addAction(self.versionnowAct)
        updateMenu.addAction(self.online_updateMessageAct)

        aboutMenu = menubar.addMenu(self.tr('关于'))
        aboutMenu.addAction(self.aboutAct)
        aboutMenu.addAction(self.aboutDetailsAct)

        serverMenu = menubar.addMenu(self.tr('服务器'))
        serverMenu.addAction(self.pingServerManuallyAct)
        serverMenu.addAction(self.url_msgAct)

        settingsMenu = menubar.addMenu(QIcon('./tsuki/assets/GUI/resources/settings.png'), self.tr('设置'))
        settingsMenu.addAction(self.settingsAction)


        runCodeMenu = menubar.addMenu(self.tr('运行'))
        runCodeMenu.setIcon(QIcon('./tsuki/assets/GUI/resources/start.png'))
        
        self.runcodeAction = QAction(self.tr('Run Code'), self)
        self.runcodeAction.setIcon(QIcon('./tsuki/assets/GUI/resources/start.png'))
        self.runcodeAction.setShortcut('F5')
        self.runcodeAction.triggered.connect(self.runcode)
        runCodeMenu.addAction(self.runcodeAction)
        
        self.runcode_debugAction = QAction(self.tr('Debug Run Code'), self)
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
                encoding = getattr(self, 'current_encoding', self.tr('Unknown-Encoding'))
                document = currentWidget.document()
                block = document.begin()
                line_count = 0
                max_column_count = 0

                while block.isValid():
                    line_text = block.text()
                    line_count += 1
                    max_column_count = max(max_column_count, len(line_text))
                    block = block.next()

                status_text = (self.tr('[当前文本] [ 行数: {0} | 列数: {1} | 字符数: {2} | '
                            '编码: {3} | 光标位置: 行{4} 列{5} ]').format(line_count, max_column_count, char_count, encoding, cursor_line, cursor_column))
                self.status_label.setText(status_text)
                self.status_label.setFont(QFont(self.tr("微软雅黑")))
            except Exception as e:
                logging.error(self.tr("An error occurred while updating the status label: {0}").format(e))
        else:
            logging.warning(self.tr("Current widget is not valid."))



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
                    self.tr(f' TsukiFont <img src="./tsuki/assets/GUI/resources/done.png" width="16" height="16">: {font_name} 字体已经成功应用！'))
                logging.info(self.tr(f"[Log/INFO]Change Font: {font_name}"))
                self.statusBar().addWidget(message)
                self.save_font_family_to_cfg(font_name)
            else:
                message = QLabel()
                message.setText(
                    self.tr(f' TsukiFont <img src="./tsuki/assets/GUI/resources/error.png" width="16" height="16">: 字体没能更改！'))
                logger.warning(self.tr("没能更改"))
                self.statusBar().addWidget(message)
        except Exception as e:
            message = QLabel()
            message.setText(
                self.tr(f' TsukiFont <img src="./tsuki/assets/GUI/resources/error.png" width="16" height="16">: 发生错误！！内容: {e}'))
            self.statusBar().addWidget(message)
            logger.error(self.tr("[Log/Error]Change Font Error:"), e)

    def save_font_family_to_cfg(self, font_family):
        config = configparser.ConfigParser()
        config['Settings'] = {'font_family': font_family}

        cfg_dir = 'tsuki/assets/app/cfg/font'
        if not os.path.exists(cfg_dir):
            os.makedirs(cfg_dir)
            logging.info(self.tr("[INFO]SAVE"))
            logger.info(self.tr("[Log/INFO]SAVE"))

        cfg_path = os.path.join(cfg_dir, 'tn_font_family.ini')
        with open(cfg_path, 'w') as configfile:
            config.write(configfile)
            logging.info(self.tr(f"[INFO]SAVE {cfg_path}"))
            logger.info(self.tr(f"[Log/INFO]SAVE {cfg_path}"))

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
        self.statusBar().showMessage(self.tr('TsukiMathTools🔰: MathTools Loading Successful !'))
        logger.info(self.tr("[Log/INFO]The calculation tool has been successfully loaded and initialization is complete"))
        
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

            self.statusBar().showMessage(self.tr(f'计算结果✔: {result}'))
            logger.info(self.tr(f"[Log/Math]Succeed: MathTools Running, Result: {result}"))

        except SympifyError as e:
            self.statusBar().showMessage(self.tr('TsukiMathTools🚫: 不是数学表达式！'))
            logger.error(self.tr("[Log/Error]Misinterpreted as a non-mathematical expression."))
        except Exception as e:
            self.statusBar().showMessage(self.tr(f'计算错误❌: {e}'))
            logger.error(self.tr(f"[Log/Error]Miscalculated: {e}"))

    def resetFont(self):
        currentWidget = self.tabWidget.currentWidget()
        font = QFont()
        font.setFamily("Microsoft YaHei UI")   
        logger.info(self.tr("[Log/INFO]Changed the font to Microsoft Yahei UI"))
        font_name = font.family()
        currentWidget.setFont(font)
        self.statusBar().showMessage(self.tr(f'TsukiFontReset: 字体已经成功重置为[{font_name}]！'))
        logger.info(self.tr("[Log/INFO]ReSet Font"))


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
                font_name = self.tr("Microsoft YaHei UI")
                
        except configparser.NoSectionError:
            logging.error(self.tr("配置文件中没有 'Settings' 部分"))
            font_name = self.tr("Microsoft YaHei UI")
        except configparser.NoOptionError:
            logging.error(self.tr("配置文件中没有 'font_family' 选项"))
            font_name = self.tr("Microsoft YaHei UI")
        except UnicodeDecodeError as e:
            logging.error(self.tr(f"读取文件时发生编码错误: {e}"))
            font_name = self.tr("Microsoft YaHei UI")
        except Exception as e:
            logging.error(self.tr(f"读取字体配置时发生错误: {e}"))
            font_name = self.tr("Microsoft YaHei UI") 

        return font_name

    def openFile(self, fileName):
        if not fileName:
            options = QFileDialog.Options()
            filters = self.tr("Text Files (*.txt *.md *.ini *.xml *.json *.log *.py *.cpp *.java *.tnote);;16进制文件 (*.exe);;所有文件 (*)")
            fileName, _ = QFileDialog.getOpenFileName(self, self.tr('Open File'), '', filters, options=options)
            if fileName:  # 确保文件名不为空
                try:
                    encoding = self.detectFileEncoding(fileName)  # 检测文件编码
                    self.createNewTab(fileName, encoding)
                except TypeError as e:
                    logging.error(self.tr(f"创建新标签页时出错: {e}"))

        if fileName:
            try:
                file_extension = os.path.splitext(fileName)[1].lower()
                icon_map = self.getIconMap()
                
                if fileName.endswith(('.exe', '.pyd')):
                    self.openHexFileInTab(fileName)
                else:
                    encoding = self.detectFileEncoding(fileName)
                    self.current_encoding = encoding  
                    if not self.openFileInTab(fileName, encoding):
                        self.createNewTab(fileName, encoding)
                        if file_extension in icon_map:
                            icon_path = icon_map[file_extension]
                            self.tabWidget.setTabIcon(self.tabWidget.currentIndex(), QIcon(icon_path))
                        else:
                            self.tabWidget.setTabText(self.tabWidget.currentIndex(), os.path.basename(fileName))

                self.updateWindowTitle(fileName)
                self.statusBar().showMessage(self.tr(f'TsukiOpen✔: 文件 [{fileName}] 已成功在TsukiNotes内打开！'))
                logger.info(self.tr(f"[Log/INFO]Open File Succeed: {fileName}"))

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
                        font = QFont(self.tr("Microsoft YaHei"), 10)
                        config['Settings'] = {'font_family': self.tr('Microsoft YaHei')}
                        with open(font_config_path, 'w', encoding='utf-8') as configfile:
                            config.write(configfile)
                else:
                    font = QFont(self.tr("Microsoft YaHei"), 10)
                    config = configparser.ConfigParser()
                    config['Settings'] = {'font_family': self.tr('Microsoft YaHei')}
                    os.makedirs(os.path.dirname(font_config_path), exist_ok=True)
                    with open(font_config_path, 'w', encoding='utf-8') as configfile:
                        config.write(configfile)
                
                currentWidget.setFont(font)
                logger.info(self.tr(f"[Log/INFO]Font set to: {font.family()}"))

                self.apply_background_settings(currentWidget)

                if file_extension in icon_map:
                    icon_path = icon_map[file_extension]
                    self.tabWidget.addTab(currentWidget, QIcon(icon_path), os.path.basename(fileName))
                else:
                    self.tabWidget.addTab(currentWidget, os.path.basename(fileName))
                self.tabWidget.setCurrentWidget(currentWidget)
                self.updateTabIcon(self.tabWidget.count() - 1)
                currentWidget.setContextMenuPolicy(Qt.CustomContextMenu)
                currentWidget.customContextMenuRequested.connect(self.showContextMenu)

            except UnicodeDecodeError as e:
                self.handleError(self.tr('Open File'), fileName, self.tr(f"编码错误: {e}，尝试使用其他编码打开文件。"))
            except Exception as e:
                self.handleError(self.tr('Open File'), fileName, e)

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
        dialog.setWindowTitle(self.tr("为新标签命名"))
        
        # 加载QSS文件
        qss_file_path = './tsuki/assets/theme/New_Tab_Dialog.qss'
        try:
            with open(qss_file_path, 'r', encoding='utf-8') as file:
                qss = file.read()
                dialog.setStyleSheet(qss)
        except Exception as e:
            logging.error(self.tr(f"加载新标签对话框样式失败: {e}"))
        
        layout = QVBoxLayout(dialog)
        
        name_input = QLineEdit(tab_name)
        layout.addWidget(name_input)
        
        button_layout = QHBoxLayout()
        ok_button = QPushButton(self.tr("确定"))
        skip_button = QPushButton(self.tr("跳过"))
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
        msgBox.setWindowTitle(self.tr("您确定要加入测试版通道吗？"))
        msgBox.setText(
            self.tr("测试版\n若加入测试版，您将优先享受最新的功能，但是他可能存在bug！\n你确定要加入测试版吗？"))

        yesButton = QPushButton(self.tr("确定加入测试版通道"))
        source2Button = QPushButton(self.tr("了解测试版"))
        cancelButton = QPushButton(self.tr("取消"))

        msgBox.addButton(yesButton, QMessageBox.YesRole)
        msgBox.addButton(source2Button, QMessageBox.YesRole)
        msgBox.addButton(cancelButton, QMessageBox.NoRole)

        clickedButton = msgBox.exec()

        if msgBox.clickedButton() == yesButton:
            self.update_config(True)  
            QMessageBox.information(self, self.tr("提示"), self.tr("您已加入测试版通道!感谢加入!\n请注意,测试版可能会存在bug,并且随时可能会被删除"))
            logging.debug(f"[Log/INFO]User joined the test channel!")
        elif msgBox.clickedButton() == source2Button:
            QMessageBox.information(self, self.tr("提示"), self.tr("测试版通道是实验性的\n一切bug都可能发生\n并且一旦加入，当前版本还不支持退出"))
            logging.info(f"[Log/INFO]User looked about -> Beta version")
        elif msgBox.clickedButton() == cancelButton:
            self.update_config(False)
            QMessageBox.information(self, self.tr("提示"), self.tr("您已取消加入测试版通道!\n若需要随时可以加入"))
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
        font.setFamily(self.tr("Microsoft YaHei UI"))
        text_edit.setFont(font)

    def updateWindowTitle(self, fileName):
        file_name, file_extension = os.path.splitext(fileName)
        window_title = self.tr(f"TsukiNotes - ['{file_name}.{file_extension[1:]}']")
        self.setWindowTitle(window_title)

    def handleError(self, action, fileName, error):
        QMessageBox.critical(self, action, self.tr(f'失败了❌❗: {str(error)}'))
        self.statusBar().showMessage(self.tr(f'Tsuki{action[:2]}❌: 文件[{fileName}]操作失败！Error:[{error}]'))
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
                font_name = self.tr("Microsoft YaHei")
                logging.info(f"[Log/INFO] Font not found in config, using default font: {font_name}")
            
            font = QFont(font_name)
            logging.info(f"[Log/INFO] Font name: {font_name}, path: {font_path}")
        except Exception as e:
            logging.debug(f"[Log/ERROR] Error reading font config: {e} \n Using default font: Microsoft YaHei ")
            font = QFont(self.tr("Microsoft YaHei"))
            logging.info(f"[Log/INFO] Using default font due to error: Microsoft YaHei")

        try:
            with open(fileName, 'r', encoding=encoding, errors='ignore') as file:
                content = file.read()
                text_edit.setPlainText(content)
                text_edit.setFont(font)
        except Exception as e:
            self.handleError(self.tr('Load File Content'), fileName, e)
            logging.error(f"[Log/ERROR] Error loading file content from {fileName}: {e}")



    def runcode(self):
        current_index = self.tabWidget.currentIndex()
        current_widget = self.tabWidget.widget(current_index)
        tab_name = self.tabWidget.tabText(current_index)
        font = QFont(self.tr("Microsoft YaHei"))

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
                QMessageBox.warning(self, self.tr('Save Error'), self.tr(f'无法保存文件：{str(e)}'))
                return

            if hasattr(current_widget, 'setFont'):
                current_widget.setFont(font)
            
            self.runcodeAction.setIcon(QIcon('./tsuki/assets/GUI/resources/stop.png'))
            markdown_text = current_widget.toPlainText()
            html_text = markdown2.markdown(markdown_text)
            
            preview_window = QDialog(self)
            preview_window.setWindowTitle(self.tr(f'Preview - {tab_name}'))
        
            preview_text_edit = CustomTextEdit(file_path=file_path, parent=preview_window)
            preview_text_edit.setHtml(html_text)
            preview_text_edit.setAcceptRichText(True) 
            
            toggle_mode_button = QPushButton(self.tr('Toggle Dark/Light Mode'), preview_window)
            toggle_mode_button.clicked.connect(lambda: self.toggle_mode(preview_text_edit))
            
            save_button = QPushButton(self.tr('Save Changes'), preview_window)
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
            QMessageBox.warning(self, self.tr('Warning'), self.tr('请运行[.md][.markdown]后缀的文件\n暂不支持预览其他格式文件\n'))

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
            logging.debug(self.tr("runcode function has been executed with debugging mode."))
        
        except Exception as e:
            logging.error(self.tr(f"An error occurred: {e}"))
            logging.error(self.tr("".join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__))))
            
            self.close_debug_window()
    
        finally:
            self.close_debug_window()
            self.statusBar().showMessage(self.tr("TsukiRunCode✔: 运行结束,调试窗口自动关闭"), 5000)  
    
    def newFile(self, filePath='./tsuki/assets/resources/'):
        textEdit = QPlainTextEdit()
        
        # 设置字体
        font = QFont(self.tr("Microsoft YaHei"), 10)
        textEdit.setFont(font)
        logging.info(self.tr(f"[Log/INFO] Font set to: Microsoft YaHei, point size: 10"))
        
        logging.info(self.tr(f"Received filePath: {filePath}"))

        if self.tabWidget.count() == 0:
            tab_name = self.tr("原始文本")
            file_encoding = "UTF-8"
        else:
            tab_name, file_encoding = self.getNewFileInfo(filePath)
        
        new_tab_index = self.tabWidget.count()
        self.tabWidget.addTab(textEdit, tab_name)
        self.updateTabIcon(new_tab_index)
        
        tab_font = QFont(self.tr("Microsoft YaHei"), 9)
        self.tabWidget.tabBar().setFont(tab_font)

        textEdit.setLineWrapMode(QPlainTextEdit.NoWrap)
        textEdit.setTabStopDistance(4 * self.fontMetrics().averageCharWidth())
        logging.info(self.tr(f"[Log/INFO] New File: {tab_name}, Encoding: {file_encoding}"))
        self.apply_background_settings(textEdit)
        
        self.tabWidget.setCurrentIndex(new_tab_index)
        textEdit.textChanged.connect(lambda: self.updateTabIconOnTextChange(new_tab_index))
        # 设置右键菜单
        textEdit.setContextMenuPolicy(Qt.CustomContextMenu)
        textEdit.customContextMenuRequested.connect(self.showContextMenu)

        # 更新状态栏
        self.statusBar().showMessage(self.tr(f'TsukiTab✔: 新建标签页 "{tab_name}" 成功'))


    def apply_background_settings(self, widget):
        config = configparser.ConfigParser()
        config_path = 'tsuki/assets/app/cfg/background/background_color.ini'
        
        try:
            config.read(config_path, encoding='utf-8')
            image_path = config.get('Background', 'image_path', fallback='./tsuki/assets/app/default/default_light.png')
            
            if image_path and os.path.exists(image_path):
                style_sheet = f'background-image: url("{image_path}");'
                widget.setStyleSheet(style_sheet)
                logging.info(self.tr(f"[Log/INFO] Background image applied: {image_path}"))
            else:
                logging.warning(self.tr(f"[Log/WARNING] Background image not found: {image_path}"))
        
        except Exception as e:
            logging.error(self.tr(f"[Log/ERROR] Failed to apply background settings: {str(e)}"))
        
            
    def getNewFileInfo(self, filePath):
        dialog = QDialog(self)
        dialog.setWindowTitle(self.tr("新建标签页"))
        dialog.setFont(QFont(self.tr("Microsoft YaHei")))
        dialog.resize(300, 200)

        # 加载QSS文件
        qss_file_path = './tsuki/assets/theme/New_File_Dialog.qss'
        try:
            with open(qss_file_path, 'r', encoding='utf-8') as file:
                qss = file.read()
                dialog.setStyleSheet(qss)
        except Exception as e:
            self.statusBar().showMessage(self.tr(f'应用QSS样式失败: {e}'))
        
        layout = QVBoxLayout(dialog)
        
        name_label = QLabel(self.tr("文件名:"))
        name_input = QLineEdit("")
        name_input.setFont(QFont(self.tr("Microsoft YaHei"), 10))
        layout.addWidget(name_label)
        layout.addWidget(name_input)
        
        type_label = QLabel(self.tr("文件类型:"))
        type_combo = QComboBox()
        type_combo.setFont(QFont(self.tr("Microsoft YaHei"), 10))
        icon_map = self.getIconMap()
        type_combo.addItem(self.tr('[自定][读取你输入的文件名里面的后缀]'))
        type_combo.addItems(list(icon_map.keys()))
        layout.addWidget(type_label)
        layout.addWidget(type_combo)
        
        encoding_label = QLabel(self.tr("编码:"))
        encoding_combo = QComboBox()
        encoding_combo.setFont(QFont(self.tr("Microsoft YaHei"), 10))
        encoding_combo.addItems(["UTF-8", "GBK", "ASCII", "ISO-8859-1"])
        layout.addWidget(encoding_label)
        layout.addWidget(encoding_combo)
        
        button_layout = QHBoxLayout()
        ok_button = QPushButton(self.tr("确定"))
        ok_button.setFont(QFont(self.tr("Microsoft YaHei"), 10))
        skip_button = QPushButton(self.tr("跳过"))
        skip_button.setFont(QFont(self.tr("Microsoft YaHei"), 10))
        button_layout.addWidget(ok_button)
        button_layout.addWidget(skip_button)
        layout.addLayout(button_layout)
        
        ok_button.clicked.connect(dialog.accept)
        skip_button.clicked.connect(dialog.reject)
        
        if dialog.exec_() == QDialog.Accepted:
            file_name = name_input.text().strip()
            file_type = type_combo.currentText()
            
            if file_type == self.tr('[自定][读取你输入的文件名里面的后缀]'):
                # 如果选择了自定义，则从文件名中提取后缀
                _, extension = os.path.splitext(file_name)
                if not extension:
                    extension = '.txt'  # 如果没有后缀，默认为.txt
            else:
                extension = file_type
            
            if not file_name:
                tab_name = self.tr(f"无名文本{extension}")
            else:
                if not file_name.endswith(extension):
                    tab_name = f"{file_name}{extension}"
                else:
                    tab_name = file_name
            
            file_encoding = encoding_combo.currentText()
        else:
            tab_name = self.tr("未命名文档.txt")
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
            '.md': './tsuki/assets/GUI/resources/language/markdown.png',
            '.markdown': './tsuki/assets/GUI/resources/language/markdown.png',
            '.html': './tsuki/assets/GUI/resources/language/html.png',
            '.css': './tsuki/assets/GUI/resources/language/css.png',
            '.js': './tsuki/assets/GUI/resources/language/javascript.png',
            '.php': './tsuki/assets/GUI/resources/language/php.png',
            '.json': './tsuki/assets/GUI/resources/language/json.png',
            '.otf': './tsuki/assets/GUI/resources/language/otf.png',
            '.ini': './tsuki/assets/GUI/resources/language/ini.png', # Nope
            '.txt': './tsuki/assets/GUI/resources/language/text.png', 
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
        
        # logging.info(self.tr(f"为文件 {file_name} 选择图标: {icon_path}"))
        
        if not os.path.isfile(icon_path):
            logging.warning(self.tr(f"图标文件不存在: {icon_path}，使用默认图标"))
            icon_path = './tsuki/assets/GUI/resources/language/unknown.png'
            if not os.path.isfile(icon_path):
                logging.error(self.tr(f"默认图标文件也不存在: {icon_path}"))
                return None
        return icon_path

    def updateTabIconOnTextChange(self, index):
        textEdit = self.tabWidget.widget(index)
        if isinstance(textEdit, QPlainTextEdit):
            content = textEdit.toPlainText()
            first_line = content.split('\n', 1)[0] if content else ''
            if '.' in first_line:
                file_extension = first_line.rsplit('.', 1)[-1].lower()
                new_tab_name = self.tr(f"未命名.{file_extension}")
            else:
                new_tab_name = self.tabWidget.tabText(index)
            
            self.tabWidget.setTabText(index, new_tab_name)
            self.updateTabIcon(index)

    def updateTabIcon(self, index):
        tab_text = self.tabWidget.tabText(index)
        icon_path = self.getIconPath(tab_text)
        icon = QIcon(icon_path)
        close_icon = QIcon('./tsuki/assets/GUI/resources/close.png')
        merged_icon = QIcon()
        merged_icon.addPixmap(icon.pixmap(16, 16))
        merged_icon.addPixmap(close_icon.pixmap(16, 16), QIcon.Normal, QIcon.On)
        self.tabWidget.setTabIcon(index, merged_icon)
        

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
            if tab_count > 1:
                widget = self.tabWidget.widget(index)
                if widget is not None:
                    widget.deleteLater()
                self.tabWidget.removeTab(index)
                tab_now = self.tabWidget.count()
                self.statusBar().showMessage(self.tr(f'TsukiTab✔: 成功关闭标签页,还有 {tab_now} 个Tab保留'))
                logger.info(self.tr(f"[Log/INFO]Close Tab: {index}"))
            else:
                self.statusBar().showMessage(self.tr(f'TsukiTab🚫: 无法关闭这个标签页,因为他是最后一个,如需关闭软件,请按退出软件! -注意保存您的文件'))
                logger.error(self.tr(f"[Log/ERROR]Close Tab Error"))
        except Exception as e:
            QMessageBox.critical(self, self.tr('错误'), self.tr(f'发生错误：{str(e)}'))
            logger.error(self.tr(f"[Log/ERROR]Close Tab Error: {e}"))
            self.statusBar().showMessage(self.tr(f'TsukiTab❌: 关闭标签页失败！详见MessageBox！'))


    def checkForUpdates(self):
        config_file_path = './tsuki/assets/app/config/update/update.cfg'
        version_url = 'https://zzbuaoye.us.kg/TsukiNotes/version.txt'
        if os.path.exists(config_file_path):
            config = configparser.ConfigParser()
            config.read(config_file_path)
            beta_version_status = config.get('BetaVersion', 'BetaVersion', fallback='off')
            if beta_version_status.lower() == 'activity':
                version_url = 'https://zzbuaoye.us.kg/TsukiNotes/Beta/version.txt'
        
        try:
            response = requests.get(version_url, timeout=60)
            if response.status_code == 200:
                content = response.text.strip().split('\n')
                latest_version = None
                update_link = None
                
                for line in content:
                    if line.lower().startswith('version:'):
                        latest_version = line.split(':', 1)[1].strip()
                    elif line.lower().startswith('update_link:'):
                        update_link = line.split(':', 1)[1].strip()
                    
                    if latest_version and update_link:
                        break
                
                if latest_version and update_link:
                    if latest_version > self.current_version:
                        msgBox = QMessageBox()
                        msgBox.setWindowTitle(self.tr('TsukiNotes 检测更新 | 成功 | Successful'))
                        msgBox.setText(self.tr(f'🔰✔叮！\nTsukiNotes有新的更新包可用。\n当前版本：{self.current_version}\n最新版本：{latest_version}\n是否下载并安装？'))
                        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                        msgBox.setDefaultButton(QMessageBox.No)
                        
                        msgBox.setStyleSheet("""
                        QMessageBox {
                            background-color: #f0f8ff;
                            border: 2px solid #87cefa;
                            border-radius: 10px;
                     
                        }
                        QPushButton {
                            background-color: #1e90ff;
                            color: white;
                            border: none;
                            padding: 5px 15px;
                            margin: 5px;
                            border-radius: 5px;
                            font-size: 13px;
                            font-family: 'Microsoft YaHei', sans-serif;   
                            font-weight: bold;
                        }
                        QPushButton:hover {
                            background-color: #4169e1;
                        }
                        QPushButton:pressed {
                            background-color: #0000cd;
                        }
                        """)
                        
                        reply = msgBox.exec_()
                        self.statusBar().showMessage(self.tr(f'TsukiUpdate✔: 检测成功！发现新的更新包 {latest_version} | URL: {update_link}'))

                        if reply == QMessageBox.Yes:
                            self.download_and_install_update(update_link, latest_version)
                    else:
                        infoBox = QMessageBox()
                        infoBox.setWindowTitle(self.tr('TsukiNotes 检测更新 | 成功 | 🔰'))
                        infoBox.setText(self.tr(f'您的版本已是最新。\n当前版本：{self.current_version}'))
                        infoBox.setStyleSheet("""
                        QMessageBox {
                            background-color: #f0f8ff;
                            border: 2px solid #87cefa;
                            border-radius: 10px;
                        }
                        QMessageBox QLabel {
                            font-size: 14px;
                            font-weight: bold;
                            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 #FFC0CB, stop:0.25 #FFFFFF,
                                stop:0.5 #E6F3FF, stop:0.75 #40E0D0,
                                stop:1 #FFFFFF);
                            -webkit-background-clip: text;
                            -webkit-text-fill-color: transparent;
                            font-family: 'Microsoft YaHei', sans-serif;   
                        }
                        QPushButton {
                            background-color: #1e90ff;
                            color: white;
                            border: none;
                            padding: 5px 15px;
                            margin: 5px;
                            border-radius: 5px;
                            font-size: 13px;
                            font-family: 'Microsoft YaHei', sans-serif;   
                            font-weight: bold;
                        }
                        QPushButton:hover {
                            background-color: #4169e1;
                        }
                        QPushButton:pressed {
                            background-color: #0000cd;
                        }
                        """)
                        infoBox.exec_()
                        self.statusBar().showMessage(self.tr(f'TsukiUpdate: 检测成功✔！当前已是最新版本'))
                else:
                    raise ValueError(self.tr("无法从服务器获取版本信息"))
            else:
                raise ConnectionError(self.tr("无法连接到服务器"))

        except Exception as e:
            errorBox = QMessageBox()
            errorBox.setWindowTitle(self.tr('检测更新|错误'))
            errorBox.setText(self.tr(f'出错啦！ \nOccurred:\n{str(e)}\n 您可以尝试使用加速器加速GitHub\n 或者尝试手动更新吧'))
            errorBox.setIcon(QMessageBox.Critical)
            
            errorBox.setStyleSheet("""
            QMessageBox {
                background-color: #ffebee;
                border: 2px solid #f44336;
                border-radius: 10px;
            }
            QMessageBox QLabel {
                color: #b71c1c;
                font-size: 14px;
            }
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 5px 15px;
                margin: 5px;
                border-radius: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
            """)
            
            errorBox.exec_()
            logger.error(self.tr(f"[Log/ERROR]Check For Updates Error: {e}"))
            self.statusBar().showMessage(self.tr(f'TsukiUpdate❌: 检测失败！'))

    def download_and_install_update(self, update_link, latest_version):
        download_dialog = QProgressDialog(self.tr("下载更新中..."), self.tr("取消"), 0, 100, self)
        download_dialog.setWindowTitle(self.tr("下载更新"))
        download_dialog.setWindowModality(Qt.WindowModal)
        
        # 直接设置下载对话框的QSS样式
        download_dialog.setStyleSheet("""
        QProgressDialog {
            background-color: #e8f5e9;
            border: 2px solid #4caf50;
            border-radius: 10px;
        }
        QProgressDialog QLabel {
            color: #1b5e20;
            font-size: 14px;
        }
        QProgressBar {
            border: 2px solid #4caf50;
            border-radius: 5px;
            text-align: center;
        }
        QProgressBar::chunk {
            background-color: #4caf50;
            width: 10px;
            margin: 0.5px;
        }
        QPushButton {
            background-color: #4caf50;
            color: white;
            border: none;
            padding: 5px 15px;
            margin: 5px;
            border-radius: 5px;
            font-size: 12px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        """)
        
        download_dialog.show()

        try:
            response = requests.get(update_link, stream=True)
            total_length = response.headers.get('content-length')

            if total_length is None:  # no content length header
                download_dialog.close()
                QMessageBox.critical(self, self.tr('下载更新失败'), self.tr('无法获取文件大小'))
            else:
                dl = 0
                total_length = int(total_length)
                update_filename = f'TsukiNotes_UpdatePack_{latest_version}.zip'
                with open(update_filename, 'wb') as f:
                    for data in response.iter_content(chunk_size=4096):
                        dl += len(data)
                        f.write(data)
                        done = int(100 * dl / total_length)
                        download_dialog.setValue(done)
                        QApplication.processEvents()  # 更新UI
                        if download_dialog.wasCanceled():
                            QMessageBox.warning(self, self.tr('下载更新'), self.tr('下载已取消'))
                            return

                download_dialog.close()
                
                try:
                    with zipfile.ZipFile(update_filename, 'r') as zip_ref:
                        zip_ref.extractall('.')
                    os.remove(update_filename)
                    QMessageBox.information(self, self.tr('更新完成'), self.tr(f'更新已下载并解压，将重启应用。版本号: {latest_version}'))
                    subprocess.run(["python", "TsukiNotes.py"])  # 重启应用
                    sys.exit()
                except zipfile.BadZipFile:
                    QMessageBox.critical(self, self.tr('更新失败'), self.tr('下载的文件不是有效的zip文件'))
                    logger.error(self.tr("[Log/ERROR]Download Update Error: File is not a zip file"))
                except Exception as e:
                    QMessageBox.critical(self, self.tr('更新失败'), self.tr(f'解压或安装更新失败：{str(e)}'))
                    logger.error(self.tr(f"[Log/ERROR]Install Update Error: {e}"))
        except Exception as e:
            download_dialog.close()
            QMessageBox.critical(self, self.tr('下载更新失败'), self.tr(f'下载更新失败：{str(e)}'))
            logger.error(self.tr(f"[Log/ERROR]Download Update Error: {e}"))
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
                self.statusBar().showMessage(self.tr(f'TsukiUpdate✔: 检测成功！云端版本号为:[ {latest_version} ] 服务器状态：正常'))
                logger.info(self.tr(f"[Log/INFO]Check For Updates: {latest_version}"))
                QMessageBox.information(self, self.tr('TSUKI_BACK—Information'),
                                        self.tr(f' 返回成功\n 云端Version: {latest_version} ！\n 服务器：正常'))
                self.statusBar().showMessage(self.tr(f'TsukiBack✔：云端返回数值：{latest_version}'))


        except:
            url_text = self.tr(f"<h1> TsukiNotes </h1>"
                        f"<p><strong>目标: {version_url} </strong></p>"
                        f"<p><strong>结果：检测失败！！ </strong></p>"
                        f"<p><strong>本地: Version = {version} </strong></p>"
                        f"<p><strong>类型: {versiontd} </strong></p>"
                        f"<p><strong>日期: {versiontime}</strong></p>"
                        f"<p><strong>内部: {versiongj}</strong></p>"
                        f"<p><strong>联系: zzbuaoye@gmail.com </strong></p>")

            QMessageBox.about(self, self.tr("TsukiBack"), url_text)
            self.statusBar().showMessage(self.tr(f'TsukiUpdate❌🚫: 检测失败！请尝试关闭VPN测试[有可能是服务器寄了]'))
            logger.error(self.tr(f"[Log/ERROR]Check For Updates Error"))

    def Show_Auto_Update2(self):
        current_version = self.current_version
        self.statusBar().showMessage(self.tr(f'TsukiUpdate :请[更新->> 自动检测更新]|您的版本：{current_version}|'))

    def update2(self):
        msgBox = QMessageBox()
        version = self.current_version
        msgBox.setWindowTitle(self.tr(f"检测更新 | 您的版本Ver{version} | TsukiNotes"))
        msgBox.setText(
            self.tr(f"Hey,您现在使用的是：\n[备用]更新方案\n[推荐🔰]自动检测\n若无法成功检测，建议打开魔法再次尝试\nVersion:{version}\nTsukiNotes 2024"))
        msgBox.setIcon(QMessageBox.Information)  # 使用QMessageBox的内置图标类型
        self.statusBar().showMessage(self.tr(f'TsukiUpdate[2]: 您已选择了手动更新 '))
        
        # 加载QSS文件
        qss_file_path = './tsuki/assets/theme/Update_Dialog_OnHand.qss'
        try:
            with open(qss_file_path, 'r', encoding='utf-8') as file:
                qss = file.read()
                msgBox.setStyleSheet(qss)
        except Exception as e:
            logger.error(self.tr(f"加载更新对话框样式失败: {e}"))

        yesButton = QPushButton(self.tr("下载源1-OD"))
        source2Button = QPushButton(self.tr("下载源2-123"))
        websiteButton = QPushButton(self.tr("Github"))
        newversionButton = QPushButton(self.tr("官网版本对照🔰"))
        cancelButton = QPushButton(self.tr("取消"))

        msgBox.addButton(yesButton, QMessageBox.YesRole)
        msgBox.addButton(source2Button, QMessageBox.YesRole)
        msgBox.addButton(websiteButton, QMessageBox.YesRole)
        msgBox.addButton(cancelButton, QMessageBox.NoRole)
        msgBox.addButton(newversionButton, QMessageBox.YesRole)

        clickedButton = msgBox.exec_()

        if msgBox.clickedButton() == yesButton:
            webbrowser.open(
                'https://zstlya-my.sharepoint.com/:f:/g/personal/zz_zstlya_onmicrosoft_com/EiGVt3ZyYFZPgQu5qxsTNIQB2y0UjGvjBKMRmOfZJ-L3yg?e=iZD2iL')
            self.statusBar().showMessage(self.tr(f'TsukiUpdate[2]✔: 您已选择OneDrive下载源！已经为您跳转至浏览器'))
            logger.info(self.tr(f"[Log/INFO]Open Web {webbrowser.open}"))
        elif msgBox.clickedButton() == source2Button:
            webbrowser.open('https://www.123pan.com/s/ZhtbVv-gagV3.html')
            self.statusBar().showMessage(self.tr(f'TsukiUpdate[2]✔: 您已选择123Pan下载源！已经为您跳转至浏览器'))
        elif msgBox.clickedButton() == websiteButton:
            webbrowser.open('https://github.com/buaoyezz/TsukiNotes')
            self.statusBar().showMessage(self.tr(f'TsukiUpdate[2]✔: 您已选择浏览zzbuaoye0已经为您跳转至浏览器'))
            logger.info(self.tr(f"[Log/INFO]Open Web {webbrowser.open}"))
        elif msgBox.clickedButton() == newversionButton:
            webbrowser.open(f'https://zzbuaoye.us.kg/TsukiNotes/{version}/update.txt')
            logger.info(self.tr(f"[Log/INFO]Open Web {webbrowser.open}"))
        elif msgBox.clickedButton() == cancelButton:
            self.statusBar().showMessage(self.tr(f'TsukiUpdate[2]🚫: 您已取消操作'))
            logger.info(self.tr(f"[Log/INFO]UserChannel"))

    def versionnow(self):
        version = self.current_version
        QMessageBox.information(self, self.tr('当前版本'), self.tr(f'当前版本：[ {version} ]'))
        self.statusBar().showMessage(self.tr(f'✔叮叮！检测成功！您当前版本为：{version}'))
        logger.info(self.tr(f"[Log/INFO]Open VersionNow.def look New Version\n"))

    def aboutMessage(self):
        current_version = self.current_version
        versiongj = self.version_gj
        version_td = self.version_td
        about_text = self.tr("<h1> TsukiNotes </h1><p><strong>BY ZZBuAoYe 2024</p></strong><strong><p>ZZBuAoYe | " \
                     f"{current_version} {version_td}</strong></p>")
        QMessageBox.about(self, self.tr(f"About TsukiNotes | #{versiongj}"), about_text)
        self.statusBar().showMessage(self.tr(f'TsukiBack✔: 您打开了AboutMessage'))
        logger.info(self.tr(f"[Log/INFO]Open AboutMessage.def look New Version"))

    def aboutDetails(self):
        versiongj = self.version_gj
        about_text = self.tr(f"[软件信息]\n | 软件出品:MoonZZ \n | 时间：{self.update_Date}\n | {self.version_td} \nZZBuAoYe 2024©Copyright\n")
        QMessageBox.about(self, self.tr(f"AboutSoftWare | #{self.version_gj}"), about_text)
        self.statusBar().showMessage(self.tr(f'TsukiINFO: [{versiongj}] | [{self.version_td}] | [{self.update_Date}] '))
        logger.info(self.tr(f"[Log/INFO]Open AboutDetails.def"))


    def getOnlineUpdateText(self):
        try:
            ver = self.current_version
            update_log_url = f'https://zzbuaoye.us.kg/TsukiNotes/{ver}/update.txt'
            response = requests.get(update_log_url)
            
            if response.status_code == 200:
                return response.text
            else:
                return self.tr("<p style='text-align: center;'>无法获取在线更新日志，请检查网络连接或稍后再试。</p>")
        except Exception as e:
            logger.error(self.tr(f"[Log/ERROR]Failed to fetch online update log: {e}"))
            return self.tr("<p style='text-align: center;'>发生错误：无法获取在线更新日志。</p>")


    def online_updateMessage(self):
        version = self.current_version 
        versiontime = self.version_gj  
        version_td = self.version_td
        update_time = self.update_Date
        
        try:
            online_update_text = self.getOnlineUpdateText()
        except Exception as e:
            logger.error(self.tr(f"[Log/ERROR]获取在线更新日志失败: {e}"))
            online_update_text = self.tr("无法获取在线更新日志，请检查网络连接或稍后再试。")

        update_text = (
            "<html>"
            "<h2 style='color: #4a4a4a; font-family: \"Microsoft YaHei\", sans-serif; text-align: left; margin-bottom: 20px;'>" + self.tr("| TsukiNotes 在线更新信息🌐") + "</h2>"
            f"<p style='color: #666; font-size: 16px; text-align: center; margin-bottom: 15px;'>" + self.tr("版本: {0} {1} [{2}]").format(version, version_td, update_time) + "</p>"
            "</html>"
            f"<hr style='border: 0; height: 1px; background: #d4d4d4; margin: 20px 0;'>"
            f"<div style='background-color: #f9f9f9; padding: 15px; border-radius: 5px; margin-bottom: 20px;'>{online_update_text}</div>"
            f"<hr style='border: 0; height: 1px; background: #d4d4d4; margin: 20px 0;'>"
            f"<p style='color: #888; font-size: 14px; text-align: center;'>" + self.tr("[+代表细节优化 | *代表重要改动]") + "</p>"
            f"<p style='color: #4a4a4a; font-size: 18px; font-weight: bold; text-align: center; margin-top: 10px;'> || {version_td} ||</p>"
            f"<p style='color: #888; font-size: 14px; text-align: center;'>" + self.tr("[内部版本号: {0}]").format(versiontime) + "</p>"
        )

        dialog = QDialog(self)
        dialog.setWindowTitle(self.tr("TsukiNotes[{0}]在线更新日志 -Ver{1}{2}").format(version, version, version_td))
        dialog.resize(600, 400)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 10px;
            }
            QLabel {
                color: #333333;
                font-family: "Microsoft YaHei", sans-serif;
            }
            QPushButton {
                background-color: #4a86e8;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #3a76d8;
            }
            QPushButton:pressed {
                background-color: #2a66c8;
            }
        """)

        layout = QVBoxLayout(dialog)
        label = QLabel()
        label.setTextFormat(Qt.RichText)
        label.setText(update_text)
        layout.addWidget(label)
        label_font = QFont('Microsoft YaHei UI', 10)
        label.setFont(label_font)
        label.setAlignment(Qt.AlignLeft)
        label.setWordWrap(True)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(dialog.accept)
        layout.addWidget(button_box)
        
        dialog.exec_()

        self.statusBar().showMessage(self.tr('TsukiBack✔: 您查看了更新日志'))
        logger.info(self.tr("[Log/INFO]打开更新信息成功"))



    def renameTab(self, index):
        current_name = self.tabWidget.tabText(index)
        
        dialog = QDialog(self)
        dialog.setWindowTitle(self.tr("重命名标签"))
        layout = QVBoxLayout(dialog)
        
        name_input = QLineEdit(current_name)
        layout.addWidget(name_input)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        # 加载QSS文件
        qss_file_path = './tsuki/assets/theme/Tab_Rename.qss'
        try:
            with open(qss_file_path, 'r', encoding='utf-8') as file:
                qss = file.read()
                dialog.setStyleSheet(qss)
        except Exception as e:
            self.statusBar().showMessage(self.tr('应用QSS样式失败: {0}').format(e))
            logger.error(self.tr("加载重命名对话框样式失败: {0}").format(e))

        if dialog.exec_() == QDialog.Accepted:
            new_name = name_input.text().strip()
            if new_name and new_name != current_name:
                self.tabWidget.setTabText(index, new_name)
                self.updateTabIcon(index)  # 更新图标
                self.statusBar().showMessage(self.tr('TsukiTab✔: 标签已重命名为 "{0}"').format(new_name))
                logger.info(self.tr("[Log/INFO] Tab renamed: {0} -> {1}").format(current_name, new_name))
            elif not new_name:
                QMessageBox.warning(self, self.tr("重命名失败"), self.tr("标签名不能为空"))
                logger.warning(self.tr("[Log/WARNING] Attempted to rename tab with empty name"))
            else:
                self.statusBar().showMessage(self.tr('TsukiTab: 标签名未更改'))
                logger.info(self.tr("[Log/INFO] Tab name unchanged: {0}").format(current_name))

    def closeTab(self, index):
        self.tabWidget.removeTab(index)

    

    def mousePressEvent(self, event):
        if event.button() == 4:
            index = self.tabWidget.tabBar().tabAt(event.pos())
            if index >= 0:
                self.closeTab(index)

    def contextMenuEvent(self, event):
        index = self.tabWidget.tabBar().tabAt(event.pos())
        if index >= 0:
            menu = QMenu(self)
            rename_action = QAction(QIcon('./tsuki/assets/GUI/resources/font_size_reset_tab.png'), self.tr('重命名标签'), self)
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
            msgBox = QMessageBox(self)
            msgBox.setText(self.tr('文本可能被修改，是否保存？'))
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            msgBox.setDefaultButton(QMessageBox.Cancel)
            
            msgBox.setStyleSheet("""
            QMessageBox {
                background-color: #f8f9fa;
                border: 2px solid #dee2e6;
                border-radius: 8px;
            }
            QLabel {
                color: #495057;
                font-size: 15px;
                font-family: 'Microsoft YaHei', sans-serif;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 10px 20px;
                margin: 6px;
                border-radius: 4px;
                font-size: 14px;
                font-family: 'Microsoft YaHei', sans-serif;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0069d9;
            }
            QPushButton:pressed {
                background-color: #0056b3;
            }
            QPushButton#Yes {
                background-color: #28a745;
                font-family: 'Microsoft YaHei', sans-serif;
            }
            QPushButton#Yes:hover {
                background-color: #218838;
            }
            QPushButton#Yes:pressed {
                background-color: #1e7e34;
            }
            QPushButton#No {
                background-color: #dc3545;
                font-family: 'Microsoft YaHei', sans-serif;
            }
            QPushButton#No:hover {
                background-color: #c82333;
            }
            QPushButton#No:pressed {
                background-color: #bd2130;
            }
            QPushButton#Cancel {
                background-color: #6c757d;
                font-family: 'Microsoft YaHei', sans-serif;
            }
            QPushButton#Cancel:hover {
                background-color: #5a6268;
                font-family: 'Microsoft YaHei', sans-serif;
            }
            QPushButton#Cancel:pressed {
                background-color: #545b62;
                font-family: 'Microsoft YaHei', sans-serif;
            }
            """)
            
            msgBox.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
            
            yes_button = msgBox.button(QMessageBox.Yes)
            no_button = msgBox.button(QMessageBox.No)
            cancel_button = msgBox.button(QMessageBox.Cancel)
            if yes_button:
                yes_button.setObjectName("Yes")
                yes_button.setText(self.tr("保存"))
                yes_button.setStyleSheet("""
                QPushButton#Yes {
                    background-color: #28a745;
                    font-family: 'Microsoft YaHei', sans-serif;
                }
                QPushButton#Yes:hover {
                    background-color: #218838;
                    font-family: 'Microsoft YaHei', sans-serif;
                }""")
            if no_button:
                no_button.setObjectName("No")
                no_button.setText(self.tr("不保存退出"))
                no_button.setStyleSheet("""
                QPushButton#No {
                    background-color: #dc3545;
                    font-family: 'Microsoft YaHei', sans-serif;
                }
                QPushButton#No:hover {
                    background-color: #c82333;
                    font-family: 'Microsoft YaHei', sans-serif;
                }""")
                
            if cancel_button:
                cancel_button.setObjectName("Cancel")
                cancel_button.setText(self.tr("取消"))
                cancel_button.setStyleSheet("""
                QPushButton#Cancel {
                    background-color: #6c757d;
                    font-family: 'Microsoft YaHei', sans-serif;
                }
                QPushButton#Cancel:hover {
                    background-color: #5a6268;
                    font-family: 'Microsoft YaHei', sans-serif;
                }
                                            """)
                                            
            
            reply = msgBox.exec_()
            
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
        search_dialog.setWindowTitle(self.tr('搜索'))
        search_dialog.resize(300, 100)
        search_dialog.setFont(QFont(self.tr("Microsoft YaHei")))

        # 加载QSS文件
        qss_file_path = './tsuki/assets/theme/Search_Perform_Dialog.qss'
        try:
            with open(qss_file_path, 'r', encoding='utf-8') as file:
                qss = file.read()
                search_dialog.setStyleSheet(qss)
        except Exception as e:
            logger.error(self.tr(f"加载搜索对话框样式失败: {e}"))

        layout = QVBoxLayout(search_dialog)
        
        search_input = QLineEdit()
        search_input.setPlaceholderText(self.tr('请输入搜索内容'))
        layout.addWidget(search_input)

        button_layout = QHBoxLayout()
        search_button = QPushButton(self.tr('搜索'))
        cancel_button = QPushButton(self.tr('取消'))
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
                        QMessageBox.information(self, self.tr('搜索结果'), self.tr('未找到匹配项'))
                else:
                    QMessageBox.warning(self, self.tr('错误'), self.tr('当前标签页不支持搜索'))

 # setting函数===================================================================
    def set_background(self):
        try:
            file_dialog = QFileDialog(self)
            file_path, _ = file_dialog.getOpenFileName(self, self.tr('选择背景图片'), '', self.tr('Images (*.png *.xpm *.jpg *.bmp *.gif)'))
        
            transparency, ok = QInputDialog.getInt(self, self.tr('输入'), self.tr('请输入背景透明度 (0-100):'), 100, 0, 100)
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
                QMessageBox.information(self, self.tr('提示'), self.tr(f'背景图片已经修改为 {file_path}，喵~'))
            self.statusBar().showMessage(self.tr(f'TsukiBC✔: 背景设置成功！'))
            logger.info(self.tr(f"[Log/INFO] Background settings applied."))

        except Exception as e:
            QMessageBox.critical(self, self.tr('错误'), self.tr(f'发生错误：{str(e)}'))
            self.statusBar().showMessage(self.tr(f'TsukiBC❌: 背景设置失败！详见MessageBox！'))
            logger.error(self.tr(f'[Log/ERROR] Background settings error: {str(e)}'))

    def save_background_settings(self, image_path, transparency):
        settings = QSettings('TsukiReader', 'Background')
        settings.setValue('backgroundImage', image_path)
        settings.setValue('backgroundTransparency', transparency)

    def load_background_settings(self, widget=None):
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
                message = self.tr(f'成功加载背景图片 {image_path}！')
            else:
                image_path = default_image_path
                style_sheet_image = f'background-image: url("{image_path}");'
                message = self.tr(f'背景图片不存在，加载默认背景图片 {image_path}！')
            
            # 更新当前 widget 的样式表
            if widget:
                widget.setStyleSheet(style_sheet_image)
            elif self.tabWidget.currentWidget():
                self.tabWidget.currentWidget().setStyleSheet(style_sheet_image)
            
            # 显示状态信息
            self.statusBar().showMessage(self.tr(f'TsukiBC✔: {message}'))
            logger.info(self.tr(f"[Log/INFO] {message}"))
            
            config['Background'] = {'image_path': image_path}
            with open(config_path, 'w', encoding='utf-8') as configfile:
                config.write(configfile)
        
        except Exception as e:
            self.statusBar().showMessage(self.tr(f'TsukiBC❌: 未找到保存的背景设置或加载失败。'))
            logger.error(self.tr(f"[Log/ERROR] Background Color Load Error: {str(e)}"))



    def reset_background_color(self):
        config = configparser.ConfigParser()
        default_image_path = './tsuki/assets/app/default/default_light.png'
        config_path = 'tsuki/assets/app/cfg/background/background_color.ini'

        try:
            config.read(config_path)
            image_path = config['Background'].get('image_path', default_image_path)

            if image_path and os.path.exists(image_path):
                style_sheet_image = f'background-image: url("{image_path}");'
                message = self.tr(f'成功加载背景图片 {image_path}！')
            else:
                image_path = default_image_path
                style_sheet_image = f'background-image: url("{image_path}");'
                message = self.tr(f'背景图片不存在，加载默认背景图片 {image_path}！')

            current_widget = self.tabWidget.currentWidget()
            current_widget.setStyleSheet(style_sheet_image)
            self.statusBar().showMessage(self.tr(f'TsukiBC✔: {message}'))
            logger.info(self.tr(f"[Log/INFO] {message}"))

            config['Background'] = {'image_path': image_path}
            with open(config_path, 'w') as configfile:
                config.write(configfile)

        except Exception as e:
            self.statusBar().showMessage(self.tr(f'TsukiBC❌: 未找到保存的背景色设置或加载失败。'))
            logger.error(self.tr(f"[Log/ERROR] Background Color Load Error: {str(e)}"))

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
                logger.info(self.tr(f"[Log/INFO]Background Color Saved:{bg_color}"))
        except Exception as e:
            QMessageBox.critical(self, self.tr('错误'), self.tr(f'保存背景色设置时发生错误：{str(e)}'))
            self.statusBar().showMessage(self.tr(f'TsukiBC_Save❌: 背景色设置保存失败！'))
            logger.error(self.tr(f"[Log/ERROR]Background Color Save Error:{str(e)}"))

    def clearTempFolder(self):
        temp_folder = 'tsuki/assets/app/temp'
        try:
            if os.path.exists(temp_folder):
                shutil.rmtree(temp_folder)
            os.makedirs(temp_folder)
            self.statusBar().showMessage(self.tr('TsukiBG✔: 临时文件夹已清空！'))
            logger.info(self.tr(f"[Log/INFO]Temp Folder Cleared:{temp_folder}"))
        except Exception as e:
            QMessageBox.critical(self, self.tr('清空临时文件夹'), self.tr(f'失败了❌❗: {str(e)}'))
            self.statusBar().showMessage(self.tr(f'TsukiBG❌: 清空临时文件夹失败！原因:{str(e)}'))
            logger.error(self.tr(f"[Log/ERROR]Temp Folder Clear Error:{str(e)}"))
            
    def setBackgroundImageFromFile(self, file_name):
        try:
            pixmap = QPixmap(file_name)
            palette = QPalette()
            palette.setBrush(QPalette.Background, QBrush(pixmap))
            self.setPalette(palette)
            self.statusBar().showMessage(self.tr(f'TsukiBG✔: 背景图片已成功设置！'))
            logger.info(self.tr(f"[Log/INFO]Background Image Set:{file_name}"))
        except Exception as e:
            QMessageBox.critical(self, self.tr('设置背景图片'), self.tr(f'失败了❌❗: {str(e)}'))
            self.statusBar().showMessage(self.tr(f'TsukiBG❌: 背景图片设置失败！原因:{str(e)}'))
            logger.error(self.tr(f"[Log/ERROR]Background Image Set Error:{str(e)}"))

    def setBackgroundImage(self):
        file_name, _ = QFileDialog.getOpenFileName(self, self.tr('选择背景图片[内测]'), '',
                                                   self.tr('Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)'))

        if not file_name:
            return
        self.setBackgroundImageFromFile(file_name)
        self.saveBackgroundSettings(file_name)

    def loadBackgroundSettings(self):
        self.config_path = self.tr("./tsuki/assets/app/cfg/background/TN_BackGround.ini")
        self.default_background_path = self.tr("./tsuki/assets/app/default/default_light.png")

        if not os.path.exists(self.config_path):
            self.saveBackgroundSettings(self.default_background_path)

        config = configparser.ConfigParser()
        config.read(self.config_path)
        logger.info(self.tr(f"[Log/INFO]Background Settings Loaded:{self.config_path}"))

        if 'Background' in config:
            background_path = config['Background'].get('ImagePath', self.default_background_path)
            transparency = config['Background'].getint('Transparency', 100)
            logger.info(self.tr(f"[Log/INFO]Background Settings Loaded:{background_path}"))

            if background_path and os.path.exists(background_path):
                pixmap = QPixmap(background_path)
                palette = QPalette()
                palette.setBrush(QPalette.Background, QBrush(pixmap))
                self.setPalette(palette)
                self.statusBar().showMessage(self.tr(f'背景图片 [{background_path}] 已加载'))
                logger.info(self.tr(f"[Log/INFO]Background Settings Loaded:{background_path}"))
            else:
                # 如果背景图不存在，使用默认背景图
                pixmap = QPixmap(self.default_background_path)
                palette = QPalette()
                palette.setBrush(QPalette.Background, QBrush(pixmap))
                self.setPalette(palette)
                self.statusBar().showMessage(self.tr(f'背景图片 [{self.default_background_path}] 已加载'))
                logger.info(self.tr(f"[Log/INFO]Background Settings Loaded:{self.default_background_path}"))

    def saveBackgroundSettings(self, image_path, transparency=100):
        config_path = self.tr("tsuki/assets/app/cfg/background/TN_BackGround.ini")
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

            QMessageBox.information(self, self.tr('提示'), self.tr(f'字体大小已经重置为默认值 {default_font_size}，喵~'))
            self.statusBar().showMessage(self.tr(f'TsukiFS✔: 字体大小已重置为默认值 {default_font_size}'))
        except Exception as e:
            QMessageBox.critical(self, self.tr('错误'), self.tr(f'发生错误：{str(e)}'))
            self.statusBar().showMessage(self.tr(f'TsukiFS✔: 字体大小初始化失败！详见MessageBox！'))
            logger.error(self.tr(f"[Log/ERROR]Font Size Initialization Failed:{str(e)}"))

    def total_setting(self):
        try:
            dialog = QDialog(self)
            dialog.setWindowTitle(self.tr("统计设置"))
            layout = QVBoxLayout(dialog)

            checkbox_include_whitespace = QCheckBox(self.tr("包括空白字符"))
            checkbox_include_whitespace.setChecked(self.include_whitespace)
            layout.addWidget(checkbox_include_whitespace)

            label_custom_lines = QLabel(self.tr("自定义显示行数[0为自动][不可用]："))
            layout.addWidget(label_custom_lines)
            self.line_edit_custom_lines = QLineEdit()

            self.line_edit_custom_lines.setText(str(self.custom_lines))
            layout.addWidget(self.line_edit_custom_lines)

            checkbox_highlight_keywords = QCheckBox(self.tr("启用关键字高亮"))
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
            QMessageBox.critical(self, self.tr('错误'), self.tr(f'发生异常：{str(e)}'))
            self.statusBar().showMessage(self.tr(f'TsukiTotalSetting❌: 发生异常：{str(e)}'))
            logger.error(self.tr(f"[Log/ERROR]Total Setting Failed:{str(e)}"))

    def toggle_highlight_keywords(self, state):
        if state == Qt.Checked:
            self.highlight_keywords = True
            QMessageBox.information(self, self.tr("高亮模式"), self.tr("Highlight Mode Enabled\nSupport Language: MD Py Java Cpp"))
        else:
            self.highlight_keywords = False
            QMessageBox.information(self, self.tr("高亮模式"), self.tr("Highlight Mode Disabled\n"))
        self.addKeywordHighlight()

    def saveSettings(self, include_whitespace, custom_lines, highlight_keywords):
        try:
            ini_dir = self.tr('tsuki/assets/app/cfg/app_settings')
            ini_path = os.path.join(ini_dir, self.tr('total_settings.ini'))
            os.makedirs(ini_dir, exist_ok=True)
            config = configparser.ConfigParser()
            config['Settings'] = {}
            config['Settings']['include_whitespace'] = str(include_whitespace)
            config['Settings']['custom_lines'] = str(custom_lines)
            config['Settings']['highlight_keywords'] = str(highlight_keywords)
            with open(ini_path, 'w') as configfile:
                config.write(configfile)
        except Exception as e:
            QMessageBox.critical(self, self.tr('错误'), self.tr(f'保存设置时发生异常：{str(e)}'))
            self.statusBar().showMessage(self.tr(f'TsukiSave❌: 保存设置时发生异常：{str(e)}'))
            logger.error(self.tr(f"[Log/ERROR]Save Settings Failed:{str(e)}"))

    def applySettings(self, include_whitespace, custom_lines):
        try:
            current_widget = self.tabWidget.currentWidget()
            if current_widget is None:
                raise ValueError(self.tr("当前没有选中的小部件"))
            logger.info(self.tr(f"当前小部件类型: {type(current_widget)}"))
            
            if not isinstance(current_widget, (QPlainTextEdit, QTextEdit)):
                raise TypeError(self.tr("当前小部件不是 QPlainTextEdit 或 QTextEdit 类型"))
            
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
            QMessageBox.critical(self, self.tr('错误'), self.tr(f'应用设置时发生异常：{str(e)}'))
            self.statusBar().showMessage(self.tr(f'TsukiApplySetting❌: 应用设置时发生异常：{str(e)}'))
            logger.error(self.tr(f"[Log/ERROR]Apply Settings Failed:{str(e)}"))


    def addKeywordHighlight(self):
        try:
            current_widget = self.tabWidget.currentWidget()
            self.highlighter = PythonHighlighter(self.highlight_keywords, current_widget.document())
        except Exception as e:
            QMessageBox.critical(self, self.tr('错误'), self.tr(f'添加关键字高亮时发生异常：{str(e)}'))
            self.statusBar().showMessage(self.tr(f'添加关键字高亮时发生异常：{str(e)}'))
            logger.error(self.tr(f"[Log/ERROR]Add Keyword Highlight Failed:{str(e)}"))

    def reset_background(self):
        file_path = self.tr('./tsuki/assets/app/cfg/background/TN_BackGround.ini')
        config = configparser.ConfigParser()
        filename = self.tr("TN_BackGround.ini")
        defaultimage = self.tr("./tsuki/assets/app/default/default_light.png")
        if os.path.exists(file_path):
            config.read(file_path)
            if 'Background' not in config.sections():
                config.add_section('Background')
            config.set('Background', 'imagepath', self.tr('./tsuki/assets/app/default/default_light.png'))
            with open(file_path, 'w') as configfile:
                config.write(configfile)
            msg_box = QMessageBox()
            msg_box.setWindowTitle(self.tr("重置完成[Path]"))
            msg_box.setText(self.tr(f"背景已重置!{file_path}\n{filename}内imagepath已被重置为默认图片{defaultimage}\n操作成功!\n"))
            logger.info(self.tr("Reset Background Succeed!"))
            msg_box.setIconPixmap(QIcon(self.tr('./tsuki/assets/GUI/resources/done.png')).pixmap(64, 64))  # 设置自定义图标
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()
            self.setBackgroundImageFromFile(self.tr('./tsuki/assets/app/default/default_light.png'))

        else:
            msg_box = QMessageBox()
            msg_box.setWindowTitle(self.tr("提示"))
            msg_box.setText(self.tr("你还没设置背景图"))
            msg_box.setIconPixmap(QIcon(self.tr('./tsuki/assets/GUI/resources/tips.png')).pixmap(64, 64))  # 设置自定义图标
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()

    def select_and_set_background(self):
        from datetime import datetime
        user_folder = self.tr('./tsuki/assets/app/default/User_File/')
        image_files = [f for f in os.listdir(user_folder) if f.endswith('.png') or f.endswith('.jpg')]
        if not image_files:
            self.show_message_box(self.tr("提示"), self.tr("没有找到任何图片文件。"), 'tips.png')
            return

        dialog = QDialog(self)
        dialog.setWindowTitle(self.tr("选择背景图片"))
        layout = QVBoxLayout(dialog)

        list_widget = QListWidget()
        for idx, image_file in enumerate(image_files):
            item = QListWidgetItem(self.tr(f"{image_file} (ID: {idx})"))
            mod_time = datetime.fromtimestamp(os.path.getmtime(os.path.join(user_folder, image_file)))
            item.setToolTip(mod_time.strftime('%Y-%m-%d %H:%M:%S'))
            list_widget.addItem(item)
        layout.addWidget(list_widget)

        select_button = QPushButton(self.tr("选择并设置背景"))
        select_button.clicked.connect(lambda: self.set_selected_background(list_widget, user_folder))
        layout.addWidget(select_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def set_selected_background(self, list_widget, user_folder):
        selected_items = list_widget.selectedItems()
        if not selected_items:
            self.show_message_box(self.tr("提示"), self.tr("请先选择一个图片。"), 'tips.png')
            return

        selected_image = selected_items[0].text().split(' (ID: ')[0]
        image_path = os.path.join(user_folder, selected_image)
        self.update_background_config(image_path)
        self.show_message_box(self.tr("设置成功"), self.tr(f"背景图片已设置为 {image_path}"), 'done.png')

    def update_background_config(self, image_path):
        config_path = self.tr('./tsuki/assets/app/cfg/BackGround/background_color.ini')
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
        msg_box.setIconPixmap(QIcon(self.tr(f'./tsuki/assets/GUI/resources/{icon}')).pixmap(64, 64))
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
    
    # setting函数End==============================================================

    def performSave(self):
        self.text_modified = False
        options = QFileDialog.Options()
        current_tab_name = self.tabWidget.tabText(self.tabWidget.currentIndex())
        filters = self.tr(f"所有文件 (*);;文本文件 (*.txt);;Markdown 文件 (*.md);;INI 文件 (*.ini);;XML 文件 (*.xml);" \
                  f"JSON 文件 (*.json);;日志文件 (*.log);;Python 文件 (*.py);;C 文件 (*.c)")
        fileName, selectedFilter = QFileDialog.getSaveFileName(self, self.tr(f'保存文件 - {current_tab_name}'), '', filters, options=options)
        if fileName:
            currentWidget = self.tabWidget.currentWidget()
            text = currentWidget.toPlainText()
            encoding = 'utf-8'  # 默认编码
            encoding_options = {
                self.tr('文本文件 (*.txt)'): 'utf-8',
                self.tr('Markdown 文件 (*.md)'): 'utf-8',
                self.tr('INI 文件 (*.ini)'): 'utf-8',
                self.tr('XML 文件 (*.xml)'): 'utf-8',
                self.tr('JSON 文件 (*.json)'): 'utf-8',
                self.tr('日志文件 (*.log)'): 'utf-8',
                self.tr('Python 文件 (*.py)'): 'utf-8',
                self.tr('C 文件 (*.c)'): 'utf-8'
            }
            for key, value in encoding_options.items():
                if key in selectedFilter:
                    encoding = value
                    break

            with open(fileName, 'w', encoding=encoding) as file:
                file.write(text)
                QMessageBox.information(self, self.tr('保存成功'), self.tr(f'文件 "{fileName}" 已成功保存'))
                self.statusBar().showMessage(self.tr(f'TsukiSave✔: 文件 "{fileName}" 已成功保存'))
                logger.info(self.tr(f"[Log/INFO]Save File Success: {fileName}"))
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
        self.statusBar().showMessage(self.tr('"Tsuki✔: 您执行了一次清空操作"'))
        logger.info(self.tr(f"[Log/INFO]Clear File Success"))
        currentWidget.clear()

    def performUndo(self):
        currentWidget = self.tabWidget.currentWidget()
        currentWidget.undo()
        self.statusBar().showMessage(self.tr('"Tsuki✔: 您执行了一次撤销操作"'))
        logger.info(self.tr(f"[Log/INFO]Undo File Success"))

    def performRedo(self):
        currentWidget = self.tabWidget.currentWidget()
        currentWidget.redo()

    def performCut(self):
        currentWidget = self.tabWidget.currentWidget()
        currentWidget.cut()

    def extractPingDelay(self, ping_output):
        lines = ping_output.split('\n')
        for line in lines:
            if self.tr('时间=') in line and self.tr('ms') in line:
                start_index = line.find(self.tr('时间=')) + len(self.tr('时间='))
                end_index = line.find(self.tr('ms'), start_index)

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
            info = self.tr(f'TsukiPingBack - {ping_host1}: {delay} ms')
            color_style = self.getColorStyle(delay)
            currentWidget.setStyleSheet(f"color: {color_style}")
            self.statusBar().showMessage(info)
        else:
            self.handlePingError(self.tr(f"无法 ping 到 {ping_host1}。"))

    def handlePingError(self, error_message):
        ping_host1 = 'zzbuaoye.us.kg'

        server_names = [self.tr(f'Tsuki Back：{ping_host1}')]
        for server_name in server_names:
            self.statusBar().showMessage(self.tr(f'TsukiCheck❓: {server_name} 服务器很可能不在线！Tips：如有请关闭VPN'))

        QMessageBox.warning(self, self.tr('PingServerManually | 失败原因报告'),
                            self.tr(f'我很抱歉您的检测失败了 \n 在此之前您需要知道的内容：\n | 检测时禁止使用VPN \n | 检测时可能会未响应，不必担心这是暂时的 \n 您的报错：{error_message} | Powered By MoonCN&TsukiNotes'))
        logger.error(self.tr(f"[Log/ERROR]PingServerManually | 失败原因报告:{error_message}"))
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
