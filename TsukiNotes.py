# -*- coding: utf-8 -*-
# ===============================================
# TsukiNotes
# Copyright (c) 2023-2024 ZZBuAoYe
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# GUI created by ZZBuAoYe using PyQt5
# For version changes and updates:
# - Visit our GitHub repository
# - Check APP -> Update -> OnlineChangeLog
#
# Note: If you see "�" characters, it indicates an encoding issue
# Please check and fix your file encoding (recommended: UTF-8)
#
# Project Homepage: https://github.com/buaoyezz/TsukiNotes
# Report Issues: https://github.com/buaoyezz/TsukiNotes/issues
# ===============================================
import sys
import ctypes
import markdown2
import traceback
from markdown2 import markdown as md_to_html
import html2text
from html2text import html2text 
import ipaddress
import shutil
import builtins
import keyword
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
from PyQt5.QtCore import (
    QSettings, QThread, Qt, QEvent, QFile, QRegExp, QTimer, pyqtSignal, 
    QPoint, QObject, QMetaType, QMetaObject, QLocale, QUrl,QSize,QPropertyAnimation
)
from PyQt5.QtGui import (
    QFont, QIcon, QTextCharFormat, QColor, QTextCursor, QKeySequence, 
    QSyntaxHighlighter, QPixmap, QPalette, QBrush, QPainter, QDesktopServices,
    QImage
)
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QFontDialog,
    QTabWidget, QInputDialog, QMenu, QMessageBox, QPushButton, QShortcut,
    QLabel, QTextBrowser, QVBoxLayout, QCheckBox, QWidget, QPlainTextEdit,
    QColorDialog, QDialog, QToolBar, QLineEdit, QDialogButtonBox, QGridLayout,
    QSpacerItem, QSizePolicy, QComboBox, QProgressDialog, QToolButton, QFrame,
    QGroupBox, QListWidget, QListWidgetItem, QSpinBox,QGraphicsDropShadowEffect, QSplitter,
    QGraphicsOpacityEffect
)
from sympy import sympify, SympifyError
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application, parse_expr
import tempfile
# The UI
from tsuki.ui.utils.message_box import ClutMessageBox
from tsuki.ui.utils.clut_card import ClutCard
from tsuki.ui.utils.clut_image_card import ClutImageCard
from tsuki.ui.utils.overlay_notification import OverlayNotification
from tsuki.pages.About_page import AboutPage
# The Pages
from tsuki.core.crash_report import CrashReport
from tsuki.pages.Search_page import SearchResultDialog
from tsuki.pages.Debug_page import QTextEditHandler,DebugWindow
from tsuki.pages.Delete_old_Temp import DeleteOldTemp
from tsuki.pages.Settings_page import SettingsWindow
# The Core
from tsuki.core.HighLight.SyntaxHighlighter import SyntaxHighlighter,PythonHighlighter,CppHighlighter,JavaHighlighter,MarkdownHighlighter


DeleteOldTemp.delete_old_logs(os.path.join('tsuki', 'assets', 'log', 'temp'))
crash_report = CrashReport.crash_report

LOG_COLORS = {
    'DEBUG': 'purple',
    'debug': 'purple',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red,bold'
}

class ColoredFormatter(colorlog.ColoredFormatter):
    def format(self, record):
        color = LOG_COLORS.get(record.levelname, 'white')
        formatter = colorlog.ColoredFormatter(
            '%(log_color)s[%(asctime)s | %(levelname)s] | %(name)s | - %(message)s%(reset)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors=LOG_COLORS
        )
        return formatter.format(record)

logger = logging.getLogger(__name__)

def setup_logging():
    log_dir = os.path.join(tempfile.gettempdir(), 'tsuki', 'assets', 'log', 'temp')
    
    # 确保日志目录存在
    try:
        os.makedirs(log_dir, exist_ok=True)
        print(f"Created log directory: {log_dir}")  # 使用print替代logger
    except Exception as e:
        print(f"Failed to create log directory: {e}")  # 使用print替代logger
        # 如果创建失败,使用系统临时目录
        log_dir = tempfile.gettempdir()

    # 创建日志处理器
    stream_handler = logging.StreamHandler()
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_file_path = os.path.join(log_dir, f'TsukiNotes_Log_{timestamp}.log')
    
    try:
        file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
    except Exception as e:
        print(f"文件处理错误: {e}")  # 
        # 如果创建文件处理器失败,尝试使用系统默认编码
        file_handler = logging.FileHandler(log_file_path)

    # 设置格式化器
    formatter = ColoredFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors=LOG_COLORS
    )
    
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # 配置根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(stream_handler)
    root_logger.addHandler(file_handler)

setup_logging()

# setup logger
logger = logging.getLogger(__name__)

# debug mod
debug_version = '1.1.3Release'
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
            ClutMessageBox.show_message(self, self.tr('Error'), self.tr(f'Failed to save file: {e}'))
# ==============================================================End Welcome===================================================================================================================

class HexViewerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.loader_thread = None  # 添加线程引用
        
        # 使用QPlainTextEdit作为显示组件
        self.text_view = QPlainTextEdit()
        self.text_view.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.text_view.setFont(QFont("Courier New", 10))
        self.text_view.setReadOnly(True)
        self.text_view.setStyleSheet("""
            * {
                font-family: Microsoft YaHei;
            }
            QPlainTextEdit {
                background-color: #ffffff;
                color: #333333;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPlainTextEdit:focus {
                background-color: #f8f8f8;
            }
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #05B8CC;
                width: 20px;
            }
        """)
        
        # 添加工具栏
        self.toolbar = QToolBar()
        self.toolbar.setStyleSheet("""
            * {
                font-family: Microsoft YaHei;
            }
            QToolBar {
                background-color: transparent;
                border: none;
                spacing: 8px;
                padding: 8px;
            }
        """)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(self.tr("搜索十六进制或ASCII"))
        self.search_input.setStyleSheet("""
            * {
                font-family: Microsoft YaHei;
            }
            QLineEdit {
                background-color: #ffffff;
                color: #333333;
                border: none;
                border-radius: 6px;
                padding: 8px 12px;
                min-width: 200px;
            }
            QLineEdit:focus {
                background-color: #f8f8f8;
            }
        """)
        
        self.search_button = QPushButton(self.tr("搜索"))
        self.search_button.setStyleSheet("""
            * {
                font-family: Microsoft YaHei;
            }
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 6px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
        """)
        
        self.toolbar.addWidget(self.search_input)
        self.toolbar.addWidget(self.search_button)
        
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.text_view)
        
        # 设置整体样式
        self.setStyleSheet("""
            * {
                font-family: Microsoft YaHei;
            }
            QWidget {
                background-color: #f0f0f0;
            }
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
                background-color: #f0f0f0;
            }
            QProgressBar::chunk {
                background-color: #05B8CC;
                border-radius: 3px;
            }
            QProgressDialog {
                background-color: #ffffff;
                border: 1px solid #cccccc;
                border-radius: 8px;
            }
            QProgressDialog QLabel {
                color: #333333;
                font-size: 12px;
                margin: 5px;
            }
        """)
        
        # 连接搜索功能
        self.search_button.clicked.connect(self.search_hex)
        
    def closeEvent(self, event):
        # 关闭时停止线程
        if self.loader_thread and self.loader_thread.isRunning():
            self.loader_thread.stop()
            self.loader_thread.wait()  
        super().closeEvent(event)
        
    # 代理方法
    def append_content(self, content):
        self.text_view.appendPlainText(content)
        
    def toPlainText(self):
        return self.text_view.toPlainText()
        
    def setPlainText(self, text):
        self.text_view.setPlainText(text)
        
    def clear(self):
        self.text_view.clear()
        
    def textCursor(self):
        return self.text_view.textCursor()
        
    def setTextCursor(self, cursor):
        self.text_view.setTextCursor(cursor)
        
    def document(self):
        return self.text_view.document()
        
    def find(self, *args, **kwargs):
        return self.text_view.find(*args, **kwargs)
        
    def search_hex(self):
        search_text = self.search_input.text().strip()
        if not search_text:
            return
            
        cursor = self.text_view.textCursor()
        cursor.movePosition(QTextCursor.Start)
        self.text_view.setTextCursor(cursor)
        
        found = self.text_view.find(search_text) or \
                self.text_view.find(search_text.encode().hex())

class FileLoaderThread(QThread):
    dataLoaded = pyqtSignal(str)
    progressUpdated = pyqtSignal(int)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, file_path, chunk_size=4096):
        super().__init__()
        self.file_path = file_path
        self.chunk_size = chunk_size
        self.is_running = True
        
        self.progress_style = """
            QProgressDialog {
                background-color: #F0F0F0;
                border-radius: 10px;
            }
            QProgressBar {
                border: 2px solid grey;
                border-radius: 10px;
                text-align: center;
                background-color: #F0F0F0;
            }
            QProgressBar::chunk {
                background-color: #808080;
                border-radius: 8px;
            }
        """
        
    def run(self):
        try:
            file_size = os.path.getsize(self.file_path)
            processed_size = 0
            buffer = []
            
            with open(self.file_path, 'rb') as f:
                while self.is_running:
                    chunk = f.read(self.chunk_size)
                    if not chunk:
                        break
                        
                    # 处理每16字节为一行
                    for i in range(0, len(chunk), 16):
                        line_bytes = chunk[i:i+16]
                        # 格式化十六进制显示
                        hex_part = ' '.join(f'{b:02x}' for b in line_bytes)
                        # 格式化ASCII显示
                        ascii_part = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in line_bytes)
                        # 添加偏移量
                        offset = processed_size + i
                        line = f'{offset:08x}  {hex_part:<48}  |{ascii_part}|'
                        buffer.append(line)
                    
                    processed_size += len(chunk)
                    
                    # 每1000行发送一次,避免GUI过度更新
                    if len(buffer) >= 5000:
                        self.dataLoaded.emit('\n'.join(buffer))
                        buffer.clear()
                        
                    # 更新进度
                    progress = int((processed_size / file_size) * 100)
                    self.progressUpdated.emit(progress)
                    
            # 发送剩余内容
            if buffer:
                self.dataLoaded.emit('\n'.join(buffer))
                
            self.finished.emit()
        
        finally:
            self.is_running = False
        
            
    def stop(self):
        self.is_running = False
        self.wait()  # 等待线程结束


def openHexFileInTab(self, fileName):
    try:
        hex_viewer = HexViewerWidget()
        
        # 创建进度对话框
        progress = QProgressDialog(self.tr("正在加载文件..."), self.tr("取消"), 0, 100, self)
        progress.setWindowModality(Qt.WindowModal)
        progress.setMinimumDuration(0)  # 立即显示
        progress.setStyleSheet("""
            QProgressDialog {
                background-color: #ffffff;
                border-radius: 4px;
            }
            QProgressBar {
                border: none;
                background-color: #f0f0f0;
                border-radius: 2px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #0078d4;
                border-radius: 2px;
            }
        """)
        
        # 创建加载线程
        loader = FileLoaderThread(fileName)
        
        # 连接信号
        loader.dataLoaded.connect(hex_viewer.append_content)
        loader.progressUpdated.connect(progress.setValue)
        loader.error.connect(lambda e: self.handleError(self.tr('加载十六进制文件'), fileName, e))
        loader.finished.connect(progress.close)
        
        # 处理取消操作
        progress.canceled.connect(loader.stop)
        
        # 添加到标签页
        index = self.tabWidget.addTab(hex_viewer, os.path.basename(fileName))
        self.tabWidget.setCurrentIndex(index)
        
        # 设置图标
        icon_path = './tsuki/assets/resources/language/exe.png'
        if os.path.exists(icon_path):
            self.tabWidget.setTabIcon(index, QIcon(icon_path))
            
        # 启动加载线程
        loader.start()
        
        # 更新状态栏
        self.statusBar().showMessage(self.tr(f'正在加载文件: {fileName}'))
        
    except Exception as e:
        self.handleError(self.tr('打开十六进制文件'), fileName, e)


from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QListWidget, QStackedWidget, QPushButton, QLabel, QGridLayout, QWidget
from PyQt5.QtCore import Qt
from tsuki.pages.About_page import AboutPage


from PyQt5.QtGui import QTextCursor


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
        app = QApplication.instance()
        font = QFont("Microsoft YaHei")
        font.setPointSize(10)
        self.settings = QSettings('TsukiNotes', 'Editor')
        app.setFont(font)
        QMetaType.type("QTextCursor")
        self.before = ''
        with open('VERSION', 'r') as version_file:
            self.current_version = version_file.read().strip()
        self.update_Date = '2024/12/21'
        self.version_td = 'Release'
        self.version_gj = 'b1-v63d_241221R'
        self.config_file = './tsuki/assets/app/config/launch/launch_config.ini'  
        self.load_langs()

        logging.debug(f"\n====================================================================================================================\n"
                      f"TsukiReader is running ,relatedInformation:"
                      f"[Back]Version:{self.current_version}\n"
                      f"[Back]UpdateDate:{self.update_Date}\n"
                      f"[Back]Version Update The Channel:{self.version_td}\n"
                      f"[Back]versionTHE INTERNAL BUILD NUMBER:{self.version_gj}\n"
                      f"[Back]Powered By ZZBuAoYe\n"
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
        self.add_tab_button.setIcon(QIcon('./tsuki/assets/resources/tips.png'))
        self.add_tab_button.setFixedSize(24, 24)
        self.add_tab_button.clicked.connect(self.newFile)
        self.tabWidget.setCornerWidget(self.add_tab_button, Qt.TopRightCorner)
        self.loadAllStyles()

    def closeEvent(self, event):
        try:
            # 关闭主窗口前先关闭调试窗口
            if hasattr(self, 'debug_window') and self.debug_window:
                self.debug_window.close()

            # 处理主窗口的标签页
            for i in range(self.tabWidget.count()):
                self.tabWidget.setCurrentIndex(i)
                currentWidget = self.tabWidget.currentWidget()
                
                # 检查是否为文本编辑器
                if isinstance(currentWidget, (QTextEdit, QPlainTextEdit)):
                    content = currentWidget.toPlainText()
                    if content.strip():  # 如果有内容
                        n = self.autoSave(content)
                        if n != 0:
                            event.ignore()
                            return
                # 对于图片查看器(QLabel)不需要保存内容
                elif isinstance(currentWidget, QLabel):
                    continue
                    
            event.accept()
        except Exception as e:
            logger.error(f"[Log/ERROR]Close Event Error: {e}")
            event.accept()
        
    def load_langs(self):
        language_folder = './tsuki/assets/languages/'
        system_language = QLocale.system().name()[:2]

        # 尝试加载系统语言文件
        language_file = os.path.join(language_folder, f'{system_language}.json')
        if os.path.exists(language_file):
            self.load_language_file(language_file)
            logger.info(f"已加载系统语言文件: {language_file}")
        else:
            logger.warning("未找到系统语言文件，使用默认文本")
            self.translations = {}  

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
            image: url(./tsuki/assets/resources/error.png);
            subcontrol-position: right;
        }
        QTabBar::close-button:hover {
            image: url(./tsuki/assets/resources/off_file.png);
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
        qss_file_path = './tsuki/ui/theme/Main_Scrollbar_Style.qss'
        try:
            with open(qss_file_path, 'r', encoding='utf-8') as file:
                scrollbar_style = file.read()
        except Exception as e:
            logging.error(f"加载滚动条样式失败: {e}")
            ClutMessageBox.show_message(self, "样式加载错误", f"加载滚动条样式失败: {e}")

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

            open_path_action = menu.addAction("打开文件路径")
            open_path_action.triggered.connect(lambda: self.openFilePath(index))
        else:
            new_tab_action = menu.addAction("新建标签")
            new_tab_action.triggered.connect(self.newFile)

        menu.exec_(self.tabWidget.mapToGlobal(pos))


    def setTabCloseButtonStyle(self):
        style = """
        QTabBar::close-button {
            image: url(./tsuki/assets/resources/error.png);
        }
        QTabBar::close-button:hover {
            image: url(./tsuki/assets/resources/off_file.png);
        }
        """
        self.setStyleSheet(style)

    def loadScrollbarStyle(self):
        qss_file_path = './tsuki/ui/theme/Main_Scrollbar_Style.qss'
        try:
            with open(qss_file_path, 'r', encoding='utf-8') as file:
                qss = file.read()
                self.setStyleSheet(qss)
        except Exception as e:
            logging.error(f"加载滚动条样式失败: {e}")
            ClutMessageBox.show_message(self, "样式加载错误", f"加载滚动条样式失败: {e}")

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
        self.setWindowIcon(QIcon('./tsuki/assets/resources/GUI/logo.png'))
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
                font_path = './tsuki/assets/app/config/font/tn_font_family.ini'
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
                    logger.info(f"载入{nv[1]}成功")
                except Exception as e:
                    logging.error(f"读取字体配置时发生错误: {e}")
                    font = QFont("Microsoft YaHei UI")
                    self.text_edit.setFont(font)
                    self.initialize_settings()
                    logger.error(f"[Log/ERROR]读取配置文件失败: {e}")
            else:
                ClutMessageBox.show_message(self, 'Open File', f'失败了❌❗: 文件{nv[1]}不存在！')
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
            # 检查是否为文本编辑器组件
            if isinstance(currentWidget, (QTextEdit, QPlainTextEdit)):
                try:
                    # 断开之前的连接
                    currentWidget.textChanged.disconnect()
                except:
                    pass
                # 重新连接信号
                currentWidget.textChanged.connect(self.updateStatusLabel)
            # 对于图片查看器，不需要连接textChanged信号
            elif isinstance(currentWidget, QLabel):
                # 可以在这里添加图片查看器特定的信号连接（如果需要）
                pass

    def initialize_settings(self):
        QTimer.singleShot(100, lambda: self.log_and_call(self.read_font_size_from_cfg, "FontSettings_1"))
        QTimer.singleShot(110, lambda: self.log_and_call(self.read_font_family_from_cfg, "FontSettings_2"))
        QTimer.singleShot(120, lambda: self.log_and_call(self.load_background_settings, "BackGroundSettings"))

    def log_and_call(self, method, setting_name):
        try:
            method()
            logging.debug(f" 载入{setting_name}成功")
        except Exception as e:
            logging.error(f"载入{setting_name}失败: {str(e)}")

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
                
                logger.info(f" 载入 {file_path} 成功")
            else:
                ClutMessageBox.show_message(self, 'Open File', f'失败了❌❗: 文件 {file_path} 不存在！')
                self.statusBar().showMessage(f'TsukiOF❌: 文件 [{file_path}] 打开失败！Error:[文件不存在]')
                logger.error(f"ERROR Init UI Open File: 文件 {file_path} 不存在！")
                
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
        ClutMessageBox.show_message(self, "提示", "正在努力")
        logging.info("TipsShowing Color_bg")

    def checkFirstRun(self):
        say_zz = ("Welcome! Your Are First Run!\nThanks For Your Use\nThis Text Is Program Auto Make!")
        if not os.path.exists('./tsuki/assets/app/config/launch'):
            os.makedirs('./tsuki/assets/app/config/launch/', exist_ok=True)
            os.path.join('./tsuki/assets/app/config/launch/', 'launch_first.md')

        if not os.path.exists(self.config_file):
            ClutMessageBox.show_message(
                self,
                'Welcome to TsukiNotes!', 
                'TuskiNotes Welcome\n\n\n感谢使用TsukiNotes!\nTsukiNotes 可以帮助你更好的创建文本\n本产品是一个轻量文本编辑器\n基于GPLv3 -可以在Github查阅该项目\n'
            )

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
        logger.info(f"执行清空操作")

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
            logger.info(f"打开字体大小操作设置页面")
            if ok:
                current_widget = self.tabWidget.currentWidget()
                current_font = current_widget.font()
                current_font.setPointSize(font_size)
                current_widget.setFont(current_font)

                ClutMessageBox.show_message(self, '提示', f'字体大小设置成功为 {font_size}，喵~')
                self.statusBar().showMessage(f'TsukiFS✔: 字体大小设置成功为 {font_size}')
                logger.info(f"执行设置字体大小操作")
                self.save_font_size_to_cfg(font_size)
                logger.info(f"成功保存字体大小配置文件")

        except Exception as e:
            ClutMessageBox.show_message(self, '错误', f'发生错误：{str(e)}')
            logging.error(f"{e}")
            self.statusBar().showMessage(f'TsukiFS❌: 字体大小设置失败！详见MessageBox！')
            logger.error(f"[Log/ERROR]ERROR Set Font Size: {str(e)}")

    def save_font_size_to_cfg(self, font_size):
        config = configparser.ConfigParser()
        config['Settings'] = {'font_size': str(font_size)}
        
        # 确保目录存在
        cfg_dir = 'tsuki/assets/app/config/font'
        if not os.path.exists(cfg_dir):
            os.makedirs(cfg_dir)
            logging.info("[INFO]SAVE")
            logger.info(f"创建字体大小配置文件")

        # 保存配置文件
        cfg_path = os.path.join(cfg_dir, 'tn_font.ini')
        with open(cfg_path, 'w') as configfile:
            config.write(configfile)
            logging.info(f"[INFO]SAVE {cfg_path}")
            logger.info(f"成功保存字体大小配置文件")

    def read_font_size_from_cfg(self):
        cfg_file = "tsuki/assets/app/config/font/tn_font.ini"

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
        self.newAct = QAction(QIcon('./tsuki/assets/resources/create_tab.png'), self.tr('创建新的标签页（Ctrl+T）'), self)
        self.newAct.triggered.connect(self.newFile)

        self.openAct = QAction(QIcon('./tsuki/assets/resources/import_file.png'), self.tr('打开文件（Ctrl+O）'), self)
        self.openAct.triggered.connect(self.openFile)

        self.saveAct = QAction(QIcon('./tsuki/assets/resources/save_file.png'), self.tr('直接保存修改（Ctrl+S）'), self)
        self.saveAct.triggered.connect(self.saveFile)

        self.saveAsAct = QAction(QIcon('./tsuki/assets/resources/save_file.png'), self.tr('另存为（Ctrl+Shift+S）'), self)
        self.saveAsAct.triggered.connect(self.saveAs)  # 改为 saveAs

        self.closeAct = QAction(QIcon('./tsuki/assets/resources/off_file.png'), self.tr('关闭文件（Ctrl+W）'), self)
        self.closeAct.triggered.connect(self.closeFile)

        self.fontAct = QAction(QIcon('./tsuki/assets/resources/font_reset_change.png'), self.tr('修改字体'), self)
        self.fontAct.triggered.connect(self.changeFont)

        self.setfontsizeAct = QAction(QIcon('./tsuki/assets/resources/font_size_reset_tab.png'), self.tr('字体大小'), self)
        self.setfontsizeAct.triggered.connect(self.set_font_size)
                                

        self.checkUpdateAct = QAction(QIcon('./tsuki/assets/resources/update_cloud.png'), self.tr('检查更新'), self)
        self.checkUpdateAct.triggered.connect(self.checkForUpdates)

        self.aboutAct = QAction(QIcon('./tsuki/assets/resources/about.png'), self.tr('关于Tsuki版本信息'), self)
        self.aboutAct.triggered.connect(self.aboutMessage)

        self.aboutDetailsAct = QAction(QIcon('./tsuki/assets/resources/about.png'), self.tr('关于Tsuki详细信息'), self)
        self.aboutDetailsAct.triggered.connect(self.aboutDetails)

        self.exitAct = QAction(QIcon('./tsuki/assets/resources/exit_software.png'), self.tr('退出程序'), self)
        self.exitAct.triggered.connect(self.close)

        self.resetFontAct = QAction(QIcon('./tsuki/assets/resources/font_reset_change.png'), self.tr('重置字体'), self)
        self.resetFontAct.triggered.connect(self.resetFont)

        self.update2Act = QAction(QIcon('./tsuki/assets/resources/update_cloud.png'), self.tr('手动检测更新'), self)
        self.update2Act.triggered.connect(self.update2)

        self.renameTabAct = QAction(QIcon('./tsuki/assets/resources/font_size_reset_tab.png'), self.tr('重命名标签'), self)
        self.renameTabAct.triggered.connect(self.renameTab)

        #self.pingServerManuallyAct = QAction(QIcon('./tsuki/assets/resources/server_ping.png'), self.tr('手动Ping服务器'), self)
        #self.pingServerManuallyAct.triggered.connect(self.pingServerManually)

        self.url_msgAct = QAction(QIcon('./tsuki/assets/resources/server_tb.png'), self.tr('测试服务器返回'), self)
        self.url_msgAct.triggered.connect(self.url_msg)

        self.versionnowAct = QAction(QIcon('./tsuki/assets/resources/custom_server.png'), self.tr('当前版本号'))
        self.versionnowAct.triggered.connect(self.versionnow)

        self.online_updateMessageAct = QAction(QIcon('./tsuki/assets/resources/update_cloud.png'), self.tr('在线更新日志'))
        self.online_updateMessageAct.triggered.connect(self.online_updateMessage)

        self.settingsAction = QAction(QIcon('./tsuki/assets/resources/open_list.png'), self.tr('设置'), self)
        settingicon = "tsuki/assets/ico/setting.ico"
        self.settingsAction.setIcon(QIcon(settingicon))
        self.settingsAction.triggered.connect(self.openSettingsWindow)
        self.settingsAction.setIcon(QIcon(settingicon))

        self.runcodeAction = QAction(self)
        self.runcodeAction.setIcon(QIcon('./tsuki/assets/resources/run.png'))
        self.runcodeAction.setShortcut('F5')
        self.runcodeAction.triggered.connect(self.runcode)

        self.runcode_debugAction = QAction(self)
        self.runcode_debugAction.setIcon(QIcon('./tsuki/assets/resources/debug.png'))
        self.runcode_debugAction.setShortcut('F6')
        self.runcode_debugAction.triggered.connect(self.runcode_debug)


    def createMenus(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu(self.tr('文件'))
        fileMenu.addAction(self.newAct)
        fileMenu.addAction(self.openAct)
        fileMenu.addAction(self.saveAct)
        fileMenu.addAction(self.saveAsAct)
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

        #serverMenu = menubar.addMenu(self.tr('服务器'))
        #serverMenu.addAction(self.pingServerManuallyAct)
        #serverMenu.addAction(self.url_msgAct)

        runButton = QToolButton(self)
        runButton.setIcon(QIcon('./tsuki/assets/resources/start.png'))
        runButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
        runButton.setStyleSheet("QToolButton { border: none; padding: 2px; }")
        runButton.clicked.connect(self.runcode) 

        runMenu = QMenu()
        
        self.runcodeAction = QAction(self.tr('Run Code'), self)
        self.runcodeAction.setIcon(QIcon('./tsuki/assets/resources/start.png'))
        self.runcodeAction.setShortcut('F5')
        self.runcodeAction.triggered.connect(self.runcode)
        runMenu.addAction(self.runcodeAction)
        
        self.runcode_debugAction = QAction(self.tr('Debug Run Code'), self)
        self.runcode_debugAction.setIcon(QIcon('./tsuki/assets/resources/debug.png'))
        self.runcode_debugAction.setShortcut('F6')
        self.runcode_debugAction.triggered.connect(self.runcode_debug)
        runMenu.addAction(self.runcode_debugAction)

        # 下拉箭头
        arrowButton = QToolButton(self)
        arrowButton.setIcon(QIcon('./tsuki/assets/resources/open_list.png'))
        arrowButton.setStyleSheet("QToolButton { border: none; padding: 2px; }")
        arrowButton.clicked.connect(lambda: runMenu.exec_(arrowButton.mapToGlobal(QPoint(0, arrowButton.height()))))

        # buju
        buttonLayout = QHBoxLayout()
        buttonLayout.setSpacing(0) 
        buttonLayout.setContentsMargins(0, 0, 0, 0)
        # 设置
        settingsButton = QToolButton(self)
        settingsButton.setIcon(QIcon('./tsuki/assets/resources/settings.png'))
        settingsButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
        settingsButton.setStyleSheet("QToolButton { border: none; padding: 2px; }")
        settingsButton.clicked.connect(self.openSettingsWindow)

        # 分割线防止奇怪
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("""
            QFrame {
                color: #e0e0e0;
                border: none;
                background: #e0e0e0;
                width: 1px;
                margin: 4px 2px;
                height: 16px;
            }
        """)

        # 添加设置按钮到布局
        buttonLayout.addWidget(settingsButton)
        buttonLayout.addWidget(separator)
        
        # 添加运行按钮和箭头按钮
        buttonLayout.addWidget(runButton)
        buttonLayout.addWidget(arrowButton)

        # 创建容器widget
        containerWidget = QWidget()
        containerWidget.setLayout(buttonLayout)
        
        # 将容器widget添加到菜单栏右侧
        menubar.setCornerWidget(containerWidget, Qt.TopRightCorner)

    def openSettingsWindow(self):
        settings_window = SettingsWindow(self)
        settings_window.exec_()

    # 快捷键绑定
    def createShortcuts(self):
        self.shortcut_search = QShortcut(QKeySequence('Ctrl+F'), self)
        self.shortcut_save = QShortcut(QKeySequence('Ctrl+S'), self)
        self.shortcut_clear = QShortcut(QKeySequence('Ctrl+Shift+C'), self)
        self.shortcut_undo = QShortcut(QKeySequence('Ctrl+Z'), self)
        self.shortcut_redo = QShortcut(QKeySequence('Ctrl+Y'), self)
        self.shortcut_cut = QShortcut(QKeySequence('Ctrl+X'), self)
        self.shortcut_open = QShortcut(QKeySequence('Ctrl+O'), self)
        self.shortcut_new = QShortcut(QKeySequence('Ctrl+T'), self)
        self.shortcut_close = QShortcut(QKeySequence('Ctrl+W'), self)
        self.shortcut_run = QShortcut(QKeySequence('Ctrl+F5'), self)
        self.shortcut_debugrun = QShortcut(QKeySequence('Ctrl+F6'), self)
        self.shortcut_save_as = QShortcut(QKeySequence('Ctrl+Shift+S'), self)

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
        self.shortcut_save_as.activated.connect(self.saveAs)
        

    def updateStatusLabel(self):
        currentWidget = self.tabWidget.currentWidget()
        if currentWidget:
            try:
                # 检查是否为图片查看器(QLabel)
                if isinstance(currentWidget, QLabel):
                    if hasattr(currentWidget, 'pixmap') and currentWidget.pixmap():
                        pixmap = currentWidget.pixmap()
                        size = pixmap.size()
                        file_name = self.tabWidget.tabText(self.tabWidget.currentIndex())
                        status_text = self.tr(f'[图片查看] [ 文件: {file_name} | 尺寸: {size.width()}x{size.height()}px ]')
                        self.status_label.setText(status_text)
                        self.status_label.setFont(QFont(self.tr("微软雅黑")))
                    return

                cursor = currentWidget.textCursor()
                cursor_line = cursor.blockNumber() + 1
                cursor_column = cursor.columnNumber() + 1
                char_count = len(currentWidget.toPlainText())
                
                text = currentWidget.toPlainText()
                encoding = 'UTF-8'  # 默认使用UTF-8编码
                
                if text:
                    # 增加检测样本大小到8KB以提高准确性
                    sample_size = min(len(text), 8192)
                    sample = text[:sample_size].encode()
                    
                    try:
                        # 使用更高的置信度阈值
                        result = chardet.detect(sample)
                        if result and result['encoding'] and result['confidence'] > 0.9:
                            encoding = result['encoding'].upper()
                    except Exception as e:
                        logger.error(self.tr(f"编码检测出错: {str(e)}"))
                
                self.current_encoding = encoding
                
                # 使用QTextDocument的方法优化行数和列数计算
                document = currentWidget.document()
                line_count = document.lineCount()
                max_column_count = max(len(line.strip('\n')) for line in text.splitlines()) if text else 0

                # 更新状态栏文本
                status_text = (self.tr('[当前文本] [ 行数: {0} | 列数: {1} | 字符数: {2} | '
                            '编码: {3} | 光标位置: 行{4} 列{5} ]').format(
                                line_count, max_column_count, char_count, 
                                encoding, cursor_line, cursor_column))
                
                self.status_label.setText(status_text)
                self.status_label.setFont(QFont(self.tr("微软雅黑"), 9))
                
            except Exception as e:
                logger.error(self.tr(f"状态栏更新失败: {str(e)}"))
                self.status_label.setText(self.tr("状态更新失败"))
        else:
            self.status_label.setText(self.tr("无活动标签页"))
            logger.warning(self.tr("当前没有活动的标签页"))


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
                    self.tr(f' TsukiFont <img src="./tsuki/assets/resources/done.png" width="16" height="16">: {font_name} 字体已经成功应用！'))
                logging.info(self.tr(f"Change Font: {font_name}"))
                self.statusBar().addWidget(message)
                self.save_font_family_to_cfg(font_name)
            else:
                message = QLabel()
                message.setText(
                    self.tr(f' TsukiFont <img src="./tsuki/assets/resources/error.png" width="16" height="16">: 字体没能更改！'))
                logger.warning(self.tr("没能更改"))
                self.statusBar().addWidget(message)
        except Exception as e:
            message = QLabel()
            message.setText(
                self.tr(f' TsukiFont <img src="./tsuki/assets/resources/error.png" width="16" height="16">: 发生错误！！内容: {e}'))
            self.statusBar().addWidget(message)
            logger.error(self.tr("[Log/Error]Change Font Error:"), e)

    def save_font_family_to_cfg(self, font_family):
        config = configparser.ConfigParser()
        config['Settings'] = {'font_family': font_family}

        cfg_dir = 'tsuki/assets/app/config/font'
        if not os.path.exists(cfg_dir):
            os.makedirs(cfg_dir)
            logging.info(self.tr("[INFO]SAVE"))
            logger.info(self.tr("SAVE"))

        cfg_path = os.path.join(cfg_dir, 'tn_font_family.ini')
        with open(cfg_path, 'w') as configfile:
            config.write(configfile)
            logging.info(self.tr(f"[INFO]SAVE {cfg_path}"))
            logger.info(self.tr(f"SAVE {cfg_path}"))

    def read_font_family_from_cfg(self):
        cfg_file = "tsuki/assets/app/config/font/tn_font_family.ini"

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
        logger.info(self.tr("The calculation tool has been successfully loaded and initialization is complete"))
        
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
        logger.info(self.tr("Changed the font to Microsoft Yahei UI"))
        font_name = font.family()
        currentWidget.setFont(font)
        self.statusBar().showMessage(self.tr(f'TsukiFontReset: 字体已经成功重置为[{font_name}]！'))
        logger.info(self.tr("ReSet Font"))


    def loadFontSettings(self):
        config = configparser.ConfigParser()
        font_path = './tsuki/assets/app/config/font/tn_font_family.ini'

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
            filters = self.tr("Text Files (*.txt *.md *.ini *.xml *.json *.log *.py *.cpp *.java *.tnote);;"
                            "图片文件 (*.png *.jpg *.jpeg *.gif *.bmp *.svg);;"
                            "16进制文件 (*.exe *.dll *.so *.dylib *.bin *.dat *.pyd);;"
                            "所有文件 (*)")
            fileName, _ = QFileDialog.getOpenFileName(self, self.tr('Open File'), '', filters, options=options)

        if fileName:
            try:
                # 检查是否是二进制文件
                binary_extensions = ('.exe', '.dll', '.so', '.dylib', '.bin', '.dat', '.pyd')
                image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg')
                file_extension = os.path.splitext(fileName)[1].lower()

                # 处理二进制文件
                if file_extension in binary_extensions:
                    self.openHexFileInTab(fileName)
                    self.updateWindowTitle(fileName)
                    self.statusBar().showMessage(self.tr(f'TsukiOpen✔: 二进制文件 [{fileName}] 已以十六进制方式打开！'))
                    logger.info(self.tr(f"Open Binary File Succeed: {fileName}"))
                    return

                # 处理图片文件
                if file_extension in image_extensions:
                    try:
                        image_viewer = QLabel()
                        image_viewer.setAlignment(Qt.AlignCenter)
                        
                        if file_extension == '.svg':
                            renderer = QSvgRenderer(fileName)
                            image = QImage(800, 600, QImage.Format_ARGB32)
                            image.fill(0)
                            painter = QPainter(image)
                            renderer.render(painter)
                            painter.end()
                            pixmap = QPixmap.fromImage(image)
                        else:
                            pixmap = QPixmap(fileName)
                        
                        scaled_pixmap = pixmap.scaled(800, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        image_viewer.setPixmap(scaled_pixmap)
                        
                        # 获取图标
                        icon = QIcon(self.getIconPath(fileName))
                        
                        # 添加标签页并设置图标
                        index = self.tabWidget.addTab(image_viewer, os.path.basename(fileName))
                        self.tabWidget.setTabIcon(index, icon)
                        
                        self.updateWindowTitle(fileName)
                        self.statusBar().showMessage(self.tr(f'TsukiOpen✔: 图片 [{fileName}] 已成功打开！'))
                        logger.info(self.tr(f"Open Image File Succeed: {fileName}"))
                        return
                    except Exception as e:
                        self.handleError(self.tr('打开图片文件'), fileName, e)
                        return

                # 处理文本文件
                try:
                    # 尝试使用chardet检测编码
                    encoding = self.detectFileEncoding(fileName)
                    self.current_encoding = encoding

                    # 检查文件是否已经打开
                    for index in range(self.tabWidget.count()):
                        if self.tabWidget.tabText(index) == os.path.basename(fileName):
                            self.tabWidget.setCurrentIndex(index)
                            text_edit = self.tabWidget.widget(index)
                            self.tryOpenWithEncodings(fileName, text_edit)
                            return

                    # 创建新标签页
                    text_edit = QPlainTextEdit()
                    text_edit.setContextMenuPolicy(Qt.CustomContextMenu)
                    text_edit.customContextMenuRequested.connect(self.showContextMenu)
                    self.setFont(text_edit)
                    self.load_background_settings(text_edit)
                    
                    # 设置图标
                    icon_map = self.getIconMap()
                    if file_extension in icon_map:
                        icon = QIcon(icon_map[file_extension])
                    else:
                        icon = QIcon('./tsuki/assets/resources/default_file.png')
                    
                    self.tabWidget.addTab(text_edit, icon, os.path.basename(fileName))
                    
                    # 尝试使用多种编码打开文件
                    if not self.tryOpenWithEncodings(fileName, text_edit):
                        raise UnicodeDecodeError('utf-8', b'', 0, 1, '无法使用任何已知编码打开文件')
                    
                    self.tabWidget.setCurrentWidget(text_edit)
                    text_edit.textChanged.connect(self.updateStatusLabel)
                    
                    # 设置语法高亮
                    self.setHighlighter(text_edit, fileName)
                    
                    self.updateWindowTitle(fileName)
                    self.statusBar().showMessage(self.tr(f'TsukiOpen✔: 文件 [{fileName}] 已成功打开！'))
                    logger.info(self.tr(f"Open Text File Succeed: {fileName}"))

                except UnicodeDecodeError as e:
                    self.handleError(self.tr('Open File'), fileName, 
                                self.tr(f"编码错误: {e}，已尝试所有可用编码但均失败。"))
                except Exception as e:
                    self.handleError(self.tr('Open File'), fileName, e)

            except Exception as e:
                self.handleError(self.tr('Open File'), fileName, e)
                logger.error(self.tr(f"[Log/ERROR]Failed to open file: {fileName}, Error: {str(e)}"))

    def tryOpenWithEncodings(self, fileName, text_edit):
        encodings_to_try = ['utf-8', 'gbk', 'gb2312', 'big5', 'shift-jis', 'windows-1254', 'iso-8859-1']
        
        # 首先使用chardet检测编码
        try:
            with open(fileName, 'rb') as file:
                raw_data = file.read()
                result = chardet.detect(raw_data)
                detected_encoding = result['encoding']
                if detected_encoding:
                    encodings_to_try.insert(0, detected_encoding)
        except Exception as e:
            logger.error(f"Error detecting encoding: {str(e)}")

        # 尝试所有可能的编码
        for encoding in encodings_to_try:
            try:
                with open(fileName, 'r', encoding=encoding) as file:
                    content = file.read()
                    text_edit.setPlainText(content)
                    self.current_encoding = encoding
                    logger.info(f"Successfully opened file with encoding: {encoding}")
                    return True
            except UnicodeDecodeError:
                logger.error(f"Failed to open file with encoding: {encoding}")
                continue
            except Exception as e:
                logger.error(f"Error opening file: {str(e)}")
                continue
                
        return False

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
        try:
            hex_viewer = HexViewerWidget()
            
            # 创建进度对话框并设置样式
            progress = QProgressDialog(self.tr("正在加载文件..."), self.tr("取消"), 0, 100, self)
            progress.setFont(QFont("Microsoft YaHei UI", 10))
            progress.setWindowTitle(self.tr("TsukiNotes -16进制Kernel"))
            progress.setWindowModality(Qt.WindowModal)
            progress.setMinimumDuration(0)
            progress.setStyleSheet("""
                * {
                    font-family: "Microsoft YaHei UI";
                }
                
                QProgressDialog {
                    background-color: #ffffff;
                    border: 1px solid #e0e0e0;
                    border-radius: 8px;
                    padding: 20px;
                    min-width: 350px;
                    min-height: 120px;
                    font-family: "Microsoft YaHei UI";
                }
                
                QProgressDialog QLabel {
                    color: #333333;
                    font-size: 13px;
                    font-weight: 500;
                    margin: 8px;
                    font-family: "Microsoft YaHei UI";
                }
                
                QProgressDialog QPushButton {
                    background-color: #0078d4;
                    color: white;
                    border: none;
                    padding: 6px 16px;
                    border-radius: 4px;
                    font-weight: 500;
                    min-width: 80px;
                    font-family: "Microsoft YaHei UI";
                }
                
                QProgressDialog QPushButton:hover {
                    background-color: #106ebe;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.12);
                }
                
                QProgressDialog QPushButton:pressed {
                    background-color: #005a9e;
                    box-shadow: inset 0 1px 3px rgba(0,0,0,0.2);
                }
                
                QProgressBar {
                    border: none;
                    background-color: #f0f0f0;
                    border-radius: 6px;
                    text-align: center;
                    min-height: 8px;
                    max-height: 8px;
                    font-family: "Microsoft YaHei UI";
                }
                
                QProgressBar::chunk {
                    background-color: qlineargradient(
                        x1:0, y1:0, x2:1, y2:0,
                        stop:0 #00b7c3,
                        stop:1 #00d4e4
                    );
                    border-radius: 4px;
                }
                
                QProgressBar:horizontal {
                    margin: 4px 20px;
                }
                
                QProgressBar::chunk:horizontal {
                    margin: 0px;
                }
            """)
            
            # 额外设置字体
            progress.findChild(QLabel).setFont(QFont("Microsoft YaHei UI", 10))
            if progress.findChild(QPushButton):
                progress.findChild(QPushButton).setFont(QFont("Microsoft YaHei UI", 10))
                
            
            # 创建并保存线程引用
            loader = FileLoaderThread(fileName)
            hex_viewer.loader_thread = loader
            
            # 连接信号
            loader.dataLoaded.connect(hex_viewer.append_content)
            loader.progressUpdated.connect(progress.setValue)
            loader.error.connect(lambda e: self.handleError(self.tr('加载十六进制文件'), fileName, e))
            loader.finished.connect(progress.close)
            
            # 处理取消操作
            progress.canceled.connect(loader.stop)
            
            # 添加到标签页
            index = self.tabWidget.addTab(hex_viewer, os.path.basename(fileName))
            self.tabWidget.setCurrentIndex(index)
            
            # 设置图标 - 根据文件扩展名设置对应图标
            file_ext = os.path.splitext(fileName)[1].lower()
            icon_path = None
            
            # 图片文件扩展名图标映射
            image_extensions = {
                '.png': './tsuki/assets/resources/language/image.png',
                '.jpg': 'image.png', 
                '.jpeg': 'image.png',
                '.gif': 'gif.png',
                '.bmp': 'bmp.png',
                '.ico': 'ico.png',
                '.svg': 'svg.png',
                '.webp': 'webp.png'
            }
            
            if file_ext in image_extensions:
                icon_path = f'./tsuki/assets/resources/language/{image_extensions[file_ext]}'
            else:
                # 默认使用exe图标
                icon_path = './tsuki/assets/resources/language/exe.png'
                
            if os.path.exists(icon_path):
                self.tabWidget.setTabIcon(index, QIcon(icon_path))
                
            # 启动加载线程
            loader.start()
            
            # 更新状态栏
            self.statusBar().showMessage(self.tr(f'正在加载文件: {fileName}'))
            
        except Exception as e:
            self.handleError(self.tr('打开十六进制文件'), fileName, e)


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

    def loadFileContent(self, fileName, text_edit):
        try:
            # 改进编码检测逻辑
            encoding = self.detect_encoding(fileName)
            
            # 设置字体
            try:
                font = QFont(self.tr("Microsoft YaHei"))
                logging.info(f" Using font: Microsoft YaHei")
            except:
                font = QFont(self.tr("Microsoft YaHei"))
                logging.info(f" Using default font due to error: Microsoft YaHei")

            with open(fileName, 'r', encoding=encoding, errors='ignore') as file:
                content = file.read()
                text_edit.setPlainText(content)
                text_edit.setFont(font)
                
            # 保存文件编码信息到 text_edit
            text_edit.setProperty("file_encoding", encoding)
            
            # 应用背景
            self.load_background_settings(text_edit)
            
        except Exception as e:
            self.handleError(self.tr('Load File Content'), fileName, e)
            logging.error(f"Error loading file content from {fileName}: {e}")

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
        result = ClutMessageBox.show_message(
            self,
            title="您确定要加入测试版通道吗？",
            text="测试版\n若加入测试版，您将优先享受最新的功能，但是他可能存在bug！\n你确定要加入测试版吗？",
            buttons=["确定加入测试版通道", "了解测试版", "取消"]
        )
        
        if result == "确定加入测试版通道":
            self.update_config(True)
            ClutMessageBox.show_message(self, "提示", "您已加入测试版通道!感谢加入!\n请注意,测试版可能会存在bug,并且随时可能会被删除")
            logging.debug("User joined the test channel!")
        elif result == "了解测试版":
            ClutMessageBox.show_message(self, "提示", "测试版通道是实验性的\n一切bug都可能发生\n并且一旦加入，当前版本还不支持退出")
            logging.info("User looked about -> Beta version")
        elif result == "取消":
            self.update_config(False)
            ClutMessageBox.show_message(self, "提示", "您已取消加入测试版通道!\n若需要随时可以加入")
            logging.info("User canceled the operation")
            
    def crash_app(self):
        result = ClutMessageBox.show_message(
            self,
            title="警告Warning",
            text="崩溃按钮\n按下此按钮软件将迅速崩溃\n你确定要继续吗?",
            buttons=["崩！", "算了"]
        )
        if result == "崩！":
            logger.critical("用户触发了崩溃按钮")
            crash_report() # 调用崩溃报告
            raise Exception("用户手动触发崩溃")
        elif result == "算了":
            logger.info("PASS")
            pass
        
    def update_config(self, is_beta):
        config = configparser.ConfigParser()
        config_file_path = './tsuki/assets/app/config/update/update.cfg'
        
        os.makedirs(os.path.dirname(config_file_path), exist_ok=True)

        config['BetaVersion'] = {'BetaVersion': 'Activity' if is_beta else 'off'}
        config['Download'] = {'Download Link': 'https://zzbuaoye.us.kg/TsukiNotes/beta/version.txt' if is_beta else 'https://zzbuaoye.us.kg/TsukiNotes/version.txt'}

        with open(config_file_path, 'w') as configfile:
            config.write(configfile)
        
        logging.info(f"Config updated: BetaVersion = {'Activity' if is_beta else 'off'}")

    def setFont(self, text_edit):
        font = QFont()
        font.setFamily(self.tr("Microsoft YaHei UI"))
        text_edit.setFont(font)

    def updateWindowTitle(self, fileName):
        file_name, file_extension = os.path.splitext(fileName)
        window_title = self.tr(f"TsukiNotes - ['{file_name}.{file_extension[1:]}']")
        self.setWindowTitle(window_title)

    def handleError(self, action, fileName, error):
        ClutMessageBox.show_message(self, action, self.tr(f'失败了❌❗: {str(error)}'))
        self.statusBar().showMessage(self.tr(f'Tsuki{action[:2]}❌: 文件[{fileName}]操作失败！Error:[{error}]'))
        logger.error(f"[Log/ERROR]{action} Error: {error}")
        
    def _load_file_content(self, fileName, text_edit, encoding):
        # 检查是否为图片文件
        if isinstance(text_edit, QLabel):
            try:
                file_extension = os.path.splitext(fileName)[1].lower()
                if file_extension == '.svg':
                    # SVG处理
                    renderer = QSvgRenderer(fileName)
                    image = QImage(800, 600, QImage.Format_ARGB32)
                    image.fill(0)
                    painter = QPainter(image)
                    renderer.render(painter)
                    painter.end()
                    pixmap = QPixmap.fromImage(image)
                else:
                    # 其他图片格式处理
                    pixmap = QPixmap(fileName)
                
                # 自适应缩放
                scaled_pixmap = pixmap.scaled(800, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                text_edit.setPixmap(scaled_pixmap)
                return
            except Exception as e:
                self.handleError(self.tr('Load Image'), fileName, e)
                return

        # 文本文件处理逻辑
        try:
            config = configparser.ConfigParser()
            font_path = './tsuki/assets/app/config/font/tn_font_family.ini'
            
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
                    logging.info(f" Font not found in config, using default font: {font_name}")
                
                font = QFont(font_name)
                logging.info(f" Font name: {font_name}, path: {font_path}")
            except Exception as e:
                logging.debug(f"Error reading font config: {e} \n Using default font: Microsoft YaHei ")
                font = QFont(self.tr("Microsoft YaHei"))
                logging.info(f" Using default font due to error: Microsoft YaHei")

            with open(fileName, 'r', encoding=encoding, errors='ignore') as file:
                content = file.read()
                text_edit.setPlainText(content)
                text_edit.setFont(font)
        except Exception as e:
            self.handleError(self.tr('Load File Content'), fileName, e)
            logging.error(f"Error loading file content from {fileName}: {e}")



    def runcode(self):
        from PyQt5.QtCore import Qt, QTimer, QRegExp, QPropertyAnimation, QEasingCurve
        current_index = self.tabWidget.currentIndex()
        current_widget = self.tabWidget.widget(current_index)
        tab_name = self.tabWidget.tabText(current_index)
        
        if not (tab_name.endswith('.md') or tab_name.endswith('.markdown')):
            ClutMessageBox.show_message(self, self.tr('Warning'), 
                self.tr('请运行[.md][.markdown]后缀的文件\n暂不支持预览其他格式文件\n'))
            return

        # 创建预览窗口
        preview_window = QDialog(self)
        preview_window.setWindowTitle(self.tr(f'Markdown Preview - {tab_name}'))
        preview_window.resize(1200, 800)
        
        # 设置窗口动画
        window_animation = QPropertyAnimation(preview_window, b"windowOpacity")
        window_animation.setDuration(250)
        window_animation.setStartValue(0)
        window_animation.setEndValue(1)
        window_animation.start()
        
        # 设置窗口样式
        preview_window.setStyleSheet("""
            QDialog {
                background-color: #f5f6fa;
                border-radius: 15px;
                border: 1px solid #e2e8f0;
            }
            QSplitter::handle {
                background-color: #e2e8f0;
                margin: 2px;
                border-radius: 2px;
            }
            QScrollBar:vertical {
                border: none;
                background: #f1f5f9;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #cbd5e1;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #94a3b8;
            }
            QMenu {
                background: rgba(255, 255, 255, 0.95);
                border: 1px solid rgba(226, 232, 240, 0.8);
                border-radius: 12px;
                padding: 8px;
            }
            QMenu::item {
                padding: 8px 25px;
                border-radius: 6px;
                margin: 2px 4px;
                color: #1e293b;
            }
            QMenu::item:selected {
                background: rgba(241, 245, 249, 0.8);
                color: #2563eb;
            }
            QMenu::separator {
                height: 1px;
                background: rgba(226, 232, 240, 0.8);
                margin: 6px 4px;
            }
        """)

        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        
        # 创建编辑区
        edit_widget = QWidget()
        edit_layout = QVBoxLayout(edit_widget)
        
        editor = QPlainTextEdit()
        editor.setPlainText(current_widget.toPlainText())
        editor.setFont(QFont("Microsoft YaHei", 11))
        editor.setStyleSheet("""
            QPlainTextEdit {
                background-color: #ffffff;
                border-radius: 12px;
                padding: 20px;
                border: 1px solid #e2e8f0;
                color: #1e293b;
                line-height: 1.6;
            }
        """)

        # 创建右键菜单
        editor.setContextMenuPolicy(Qt.CustomContextMenu)
        editor.customContextMenuRequested.connect(lambda pos: self.show_editor_context_menu(editor, pos))
        
        # 创建预览区
        preview_widget = QWidget()
        preview_layout = QVBoxLayout(preview_widget)
        
        preview = QTextBrowser()
        preview.setOpenExternalLinks(True)
        preview.setStyleSheet("""
            QTextBrowser {
                background-color: #ffffff;
                border-radius: 12px;
                padding: 20px;
                border: 1px solid #e2e8f0;
                color: #1e293b;
            }
        """)
        
        # 添加工具栏
        toolbar = QToolBar()
        toolbar.setStyleSheet("""
            QToolBar {
                background-color: #ffffff;
                border-radius: 8px;
                padding: 5px;
                border: 1px solid #e2e8f0;
            }
            QToolButton {
                border: none;
                border-radius: 4px;
                padding: 5px;
                margin: 2px;
            }
            QToolButton:hover {
                background-color: #f1f5f9;
            }
            QMenu {
                background: rgba(255, 255, 255, 0.95);
                border: 1px solid rgba(226, 232, 240, 0.8);
                border-radius: 12px;
                padding: 8px;
            }
            QMenu::item {
                padding: 8px 25px;
                border-radius: 6px;
                margin: 2px 4px;
                color: #1e293b;
            }
            QMenu::item:selected {
                background: rgba(241, 245, 249, 0.8);
                color: #2563eb;
            }
            QMenu::separator {
                height: 1px;
                background: rgba(226, 232, 240, 0.8);
                margin: 6px 4px;
            }
        """)
        
        # 基础工具
        basic_tools = [
            ("# 标题", "# "), 
            ("**粗体**", "**"),
            ("*斜体*", "*"),
            ("- 列表", "- "),
            ("> 引用", "> "),
            ("```代码块```", "```\n"),
            ("---分隔线", "---\n"),
            ("[链接]()", "[]()")
        ]
        
        # 扩展工具菜单
        extended_tools = [
            ("表格", "|列1|列2|\n|---|---|\n|内容1|内容2|\n"),
            ("任务列表", "- [ ] 待办事项\n"),
            ("脚注", "[^1]\n\n[^1]: 脚注内容\n"),
            ("上标", "^上标^"),
            ("下标", "~下标~"),
            ("高亮", "==高亮=="),
            ("删除线", "~~删除线~~"),
            ("数学公式", "$$\n数学公式\n$$"),
            ("图片", "![图片描述](图片链接)"),
            ("HTML表格", "<table>\n  <tr>\n    <th>表头1</th>\n    <th>表头2</th>\n  </tr>\n</table>")
        ]
        
        # 创建更多工具的下拉菜单
        more_menu = QMenu()
        for text, md in extended_tools:
            action = more_menu.addAction(text)
            action.triggered.connect(lambda x, md=md: self.insert_markdown(editor, md))
        
        # 添加基础工具按钮
        for text, md in basic_tools:
            btn = QToolButton()
            btn.setText(text)
            btn.clicked.connect(lambda x, md=md: self.insert_markdown_with_selection(editor, md))
            toolbar.addWidget(btn)
        
        # 添加更多工具下拉按钮
        more_btn = QToolButton()
        more_btn.setText("更多工具")
        more_btn.setPopupMode(QToolButton.InstantPopup)
        more_btn.setMenu(more_menu)
        toolbar.addWidget(more_btn)
        
        # 设置布局
        edit_layout.addWidget(toolbar)
        edit_layout.addWidget(editor)
        preview_layout.addWidget(preview)
        
        splitter.addWidget(edit_widget)
        splitter.addWidget(preview_widget)
        splitter.setSizes([600, 600])
        
        # 主布局
        main_layout = QVBoxLayout(preview_window)
        main_layout.addWidget(splitter)
        
        # 底部按钮区域
        button_layout = QHBoxLayout()
        save_button = QPushButton(self.tr("💾 保存更改"))
        
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                border-radius: 8px;
                padding: 10px 20px;
                color: #1e293b;
                border: 1px solid #e2e8f0;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f8fafc;
                border-color: #cbd5e1;
            }
            QPushButton:pressed {
                background-color: #f1f5f9;
            }
        """)
        
        button_layout.addWidget(save_button)
        main_layout.addLayout(button_layout)
        
        # 添加阴影效果
        for widget in [editor, preview, toolbar]:
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(20)
            shadow.setColor(QColor(0, 0, 0, 25))
            shadow.setOffset(0, 2)
            widget.setGraphicsEffect(shadow)
        
        # 实时预览功能
        def update_preview():
            markdown_text = editor.toPlainText()
            html_text = markdown2.markdown(markdown_text)
            preview.setHtml(html_text)
        
        editor.textChanged.connect(update_preview)
        
        # 保存按钮点击事件
        def save_content():
            try:
                content = editor.toPlainText()
                current_widget.setPlainText(content)
                # 保存到文件
                self.save_markdown(content, tab_name)
                
                # 添加关闭动画
                close_animation = QPropertyAnimation(preview_window, b"windowOpacity")
                close_animation.setDuration(250)
                close_animation.setStartValue(1)
                close_animation.setEndValue(0)
                close_animation.finished.connect(preview_window.close)
                close_animation.start()
                
            except Exception as e:
                ClutMessageBox.show_message(self, self.tr('保存错误'), 
                    self.tr(f'保存文件时发生错误：{str(e)}'))
        
        save_button.clicked.connect(save_content)
        
        # 初始化预览
        update_preview()
        preview_window.exec_()

    def show_editor_context_menu(self, editor, pos):
        """显示编辑器右键菜单"""
        from PyQt5.QtCore import Qt, QTimer, QRegExp, QPropertyAnimation, QEasingCurve
        from PyQt5.QtWidgets import QGraphicsOpacityEffect
        context_menu = QMenu(editor)
        
        # 设置菜单透明度动画
        opacity_effect = QGraphicsOpacityEffect(context_menu)
        context_menu.setGraphicsEffect(opacity_effect)
        
        animation = QPropertyAnimation(opacity_effect, b"opacity")
        animation.setDuration(150)
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation.start()
        
        # 基本编辑操作
        undo_action = context_menu.addAction("↩ 撤销")
        redo_action = context_menu.addAction("↪ 重做")
        context_menu.addSeparator()
        cut_action = context_menu.addAction("✂ 剪切")
        copy_action = context_menu.addAction("📋 复制")
        paste_action = context_menu.addAction("📌 粘贴")
        delete_action = context_menu.addAction("🗑 删除")
        context_menu.addSeparator()
        select_all_action = context_menu.addAction("📑 全选")
        
        # Markdown 快捷操作子菜单
        markdown_menu = context_menu.addMenu("📝 Markdown")
        markdown_actions = [
            ("# 标题", "# "),
            ("**粗体**", "**"),
            ("*斜体*", "*"),
            ("~~删除线~~", "~~"),
            ("```代码块```", "```\n"),
            ("> 引用", "> "),
            ("- 列表", "- "),
            ("[链接]()", "[]()")
        ]
        
        for text, md in markdown_actions:
            action = markdown_menu.addAction(text)
            action.triggered.connect(lambda x, md=md: self.insert_markdown_with_selection(editor, md))
        
        # 连接基本编辑操作的信号
        undo_action.triggered.connect(editor.undo)
        redo_action.triggered.connect(editor.redo)
        cut_action.triggered.connect(editor.cut)
        copy_action.triggered.connect(editor.copy)
        paste_action.triggered.connect(editor.paste)
        delete_action.triggered.connect(lambda: editor.textCursor().removeSelectedText())
        select_all_action.triggered.connect(editor.selectAll)
        
        # 显示菜单
        context_menu.exec_(editor.mapToGlobal(pos))

    def insert_markdown_with_selection(self, editor, md_text):
        """插入 Markdown 语法，支持选中文本"""
        cursor = editor.textCursor()
        selected_text = cursor.selectedText()
        
        if selected_text:
            # 如果是成对的标记（如**粗体**）
            if md_text.count("*") == 2 or md_text.count("`") == 3:
                start_mark = md_text[:len(md_text)//2]
                end_mark = md_text[len(md_text)//2:]
                cursor.insertText(f"{start_mark}{selected_text}{end_mark}")
            else:
                cursor.insertText(f"{md_text}{selected_text}")
        else:
            cursor.insertText(md_text)
        
        editor.setFocus()

    def insert_markdown(self, editor, md_text):
        """插入 Markdown 语法"""
        cursor = editor.textCursor()
        cursor.insertText(md_text)
        editor.setFocus()

    def save_markdown(self, content, tab_name):
        """保存 Markdown 文件"""
        try:
            with open(tab_name, 'w', encoding='utf-8') as f:
                f.write(content)
            self.statusBar().showMessage(self.tr(f'✔ Markdown 文件已保存: {tab_name}'), 3000)
        except Exception as e:
            ClutMessageBox.show_message(self, self.tr('保存错误'), 
                self.tr(f'无法保存文件：{str(e)}'))

    def toggle_mode(self, text_edit):
        current_stylesheet = text_edit.styleSheet()
        if "background-color: black" in current_stylesheet:
            text_edit.setStyleSheet("background-color: white; color: black;")
        else:
            text_edit.setStyleSheet("background-color: black; color: white;")
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
        # 检查是否是第一个标签页
        if self.tabWidget.count() == 0:
            # 第一个标签页直接创建，使用默认值
            tab_name = self.tr("未命名文档.txt")
            file_encoding = "UTF-8"
            logger.info(self.tr("Creating first default tab"))
        else:
            # 后续标签页弹出对话框
            tab_info = self.getNewFileInfo(filePath)
            if tab_info is None or tab_info == (None, None):
                logger.info(self.tr("New file creation cancelled"))
                return
            tab_name, file_encoding = tab_info

        textEdit = QPlainTextEdit()
        
        # 设置字体
        font = QFont(self.tr("Microsoft YaHei"), 10)
        textEdit.setFont(font)
        logging.info(self.tr(f" Font set to: Microsoft YaHei, point size: 10"))
        
        logging.info(self.tr(f"Received filePath: {filePath}"))
        
        new_tab_index = self.tabWidget.count()
        self.tabWidget.addTab(textEdit, tab_name)
        self.updateTabIcon(new_tab_index)
        
        tab_font = QFont(self.tr("Microsoft YaHei"), 9)
        self.tabWidget.tabBar().setFont(tab_font)

        textEdit.setLineWrapMode(QPlainTextEdit.NoWrap)
        textEdit.setTabStopDistance(4 * self.fontMetrics().averageCharWidth())
        logging.info(self.tr(f" New File: {tab_name}, Encoding: {file_encoding}"))
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
        config_path = self.get_app_path('assets/app/config/background/background_color.ini')
        
        try:
            config.read(config_path, encoding='utf-8')
            image_path = config.get('Background', 'image_path', fallback='./tsuki/assets/app/default/default_light.png')
            
            if image_path and os.path.exists(image_path):
                style_sheet = f'background-image: url("{image_path}");'
                widget.setStyleSheet(style_sheet)
                logging.info(self.tr(f" Background image applied: {image_path}"))
            else:
                logging.warning(self.tr(f"[Log/WARNING] Background image not found: {image_path}"))
        
        except Exception as e:
            logging.error(self.tr(f"Failed to apply background settings: {str(e)}"))
        
            
    def getNewFileInfo(self, filePath):
        dialog = QDialog(self)
        dialog.setWindowTitle(self.tr("新建标签页"))
        dialog.setFont(QFont(self.tr("Microsoft YaHei")))
        dialog.resize(600, 200)

        # 加载Fluent风格QSS
        qss_file_path = './tsuki/ui/theme/New_File_Dialog.qss'
        try:
            with open(qss_file_path, 'r', encoding='utf-8') as file:
                qss = file.read()
                dialog.setStyleSheet(qss)
        except Exception as e:
            self.statusBar().showMessage(self.tr(f'应用QSS样式失败: {e}'))
            logger.error(self.tr(f"[Log/ERROR]Failed to load QSS: {e}"))

        # 添加阴影效果
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 25))
        shadow.setOffset(2, 2)
        dialog.setGraphicsEffect(shadow)

        # 设置透明度
        dialog.setWindowOpacity(0.98)
        
        # 主布局
        main_layout = QHBoxLayout(dialog)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 标准字体
        label_font = QFont(self.tr("Microsoft YaHei"), 10)
        
        # 左侧布局 - 文件名输入
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        name_group = QGroupBox()
        name_group.setStyleSheet("""
            QGroupBox {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 8px;
                padding: 12px;
                border: 1px solid rgba(0, 0, 0, 0.1);
            }
        """)
        
        name_layout = QVBoxLayout(name_group)
        name_layout.setSpacing(8)
        
        name_label = QLabel(self.tr("文件名:"))
        name_label.setFont(label_font)
        
        name_input = QLineEdit()
        name_input.setFont(label_font)
        name_input.setStyleSheet("""
            QLineEdit {
                border: none;
                border-radius: 4px;
                padding: 8px;
                background: rgba(255, 255, 255, 0.9);
                border-bottom: 2px solid transparent;
            }
            QLineEdit:focus {
                background: white;
                border-bottom: 2px solid #0078D4;
            }
        """)
        
        name_layout.addWidget(name_label)
        name_layout.addWidget(name_input)
        left_layout.addWidget(name_group)
        
        # 右侧布局 - 选项和按钮
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # 选项组
        options_group = QGroupBox()
        options_group.setStyleSheet("""
            QGroupBox {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 8px;
                padding: 12px;
                border: 1px solid rgba(0, 0, 0, 0.1);
            }
        """)
        
        options_layout = QGridLayout(options_group)
        options_layout.setSpacing(10)
        
        type_label = QLabel(self.tr("文件类型:"))
        type_label.setFont(label_font)
        
        type_combo = QComboBox()
        type_combo.setFont(label_font)
        icon_map = self.getIconMap()
        type_combo.addItem(self.tr('[自定][读取你输入的文件名里面的后缀]'))
        type_combo.addItems(list(icon_map.keys()))
        
        encoding_label = QLabel(self.tr("编码:"))
        encoding_label.setFont(label_font)
        
        encoding_combo = QComboBox()
        encoding_combo.setFont(label_font)
        encoding_combo.addItems(["UTF-8", "GBK", "ASCII", "ISO-8859-1"])
        
        options_layout.addWidget(type_label, 0, 0)
        options_layout.addWidget(type_combo, 0, 1)
        options_layout.addWidget(encoding_label, 1, 0)
        options_layout.addWidget(encoding_combo, 1, 1)
        
        right_layout.addWidget(options_group)
        
        # 按钮布局
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.setContentsMargins(0, 0, 0, 0)
        
        ok_button = QPushButton(self.tr("确定"))
        ok_button.setFont(label_font)
        ok_button.setStyleSheet("""
            QPushButton {
                background: #0078D4;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 20px;
                min-width: 80px;
            }
            QPushButton:hover {
                background: #1484D7;
            }
            QPushButton:pressed {
                background: #006CBE;
            }
        """)
        
        quit_button = QPushButton(self.tr("退出"))
        quit_button.setFont(label_font)
        quit_button.setStyleSheet("""
            QPushButton {
                background: #E0E0E0;
                border: none;
                border-radius: 4px;
                padding: 8px 20px;
                min-width: 80px;
            }
            QPushButton:hover {
                background: #D0D0D0;
            }
            QPushButton:pressed {
                background: #C0C0C0;
            }
        """)
        
        button_layout.addStretch()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(quit_button)
        
        right_layout.addWidget(button_widget)
        
        # 添加左右布局到主布局
        main_layout.addWidget(left_widget, 1)
        main_layout.addWidget(right_widget, 1)
        
        # 添加淡入淡出动画
        opacity_effect = QGraphicsOpacityEffect(dialog)
        dialog.setGraphicsEffect(opacity_effect)
        
        fade_in = QPropertyAnimation(opacity_effect, b"opacity")
        fade_in.setDuration(200)
        fade_in.setStartValue(0)
        fade_in.setEndValue(1)
        fade_in.start()
        
        def handle_quit():
            fade_out = QPropertyAnimation(opacity_effect, b"opacity")
            fade_out.setDuration(150)
            fade_out.setStartValue(1)
            fade_out.setEndValue(0)
            fade_out.finished.connect(lambda: dialog.done(QDialog.Rejected))
            fade_out.start()
            
        ok_button.clicked.connect(dialog.accept)
        quit_button.clicked.connect(handle_quit)
        
        result = dialog.exec_()
        
        if result == QDialog.Accepted:
            file_name = name_input.text().strip()
            file_type = type_combo.currentText()
            
            if file_type == self.tr('[自定][读取你输入的文件名里面的后缀]'):
                _, extension = os.path.splitext(file_name)
                if not extension:
                    extension = '.txt'
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
            logger.info(self.tr(f"New file created: {tab_name} with encoding {file_encoding}"))
            return tab_name, file_encoding
            
        elif result == QDialog.Rejected:
            if dialog.result() == 0:
                logger.info(self.tr("File creation cancelled by user"))
                return None, None
        
        return None, None

    def getIconMap(self):
        return {
            '.exe': './tsuki/assets/resources/language/exe.png',
            '.py': './tsuki/assets/resources/language/python.png',
            '.cpp': './tsuki/assets/resources/language/cpp.png',
            '.c' : './tsuki/assets/resources/language/c.png',
            '.java': './tsuki/assets/resources/language/java.png',
            '.class' : './tsuki/assets/resources/language/class.png',
            '.md': './tsuki/assets/resources/language/markdown.png',
            '.markdown': './tsuki/assets/resources/language/markdown.png',
            '.html': './tsuki/assets/resources/language/html.png',
            '.css': './tsuki/assets/resources/language/css.png',
            '.js': './tsuki/assets/resources/language/javascript.png',
            '.php': './tsuki/assets/resources/language/php.png',
            '.json': './tsuki/assets/resources/language/json.png',
            '.otf': './tsuki/assets/resources/language/otf.png',
            '.ini': './tsuki/assets/resources/language/ini.png', # Nope
            '.txt': './tsuki/assets/resources/language/text.png', 
        }

    def getIconPath(self, file_name):
        fileExt = os.path.splitext(file_name)[1].lower()
        
        icon_map = self.getIconMap()
        
        if not fileExt:
            icon_path = './tsuki/assets/resources/language/text.png'
        elif fileExt in icon_map:
            icon_path = icon_map[fileExt]
        else:
            icon_path = './tsuki/assets/resources/language/unknown.png'
        
        # logging.info(self.tr(f"为文件 {file_name} 选择图标: {icon_path}"))
        
        if not os.path.isfile(icon_path):
            logging.warning(self.tr(f"图标文件不存在: {icon_path}，使用默认图标"))
            icon_path = './tsuki/assets/resources/language/unknown.png'
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
        close_icon = QIcon('./tsuki/assets/resources/close.png')
        merged_icon = QIcon()
        merged_icon.addPixmap(icon.pixmap(16, 16))
        merged_icon.addPixmap(close_icon.pixmap(16, 16), QIcon.Normal, QIcon.On)
        self.tabWidget.setTabIcon(index, merged_icon)
        

    def saveFile(self):
        current_tab = self.tabWidget.currentWidget()
        if not current_tab:
            return
        
        # 获取当前文件路径
        file_path = current_tab.file_path if hasattr(current_tab, 'file_path') else None
        
        if not file_path:
            # 构建文件类型过滤器
            filters = self.tr(
                "文本文件 (*.txt);;Python文件 (*.py);;Markdown文件 (*.md);;所有文件 (*)"
            )
            
            # 获取上次保存路径
            last_path = self.settings.value('last_save_path', '')
            
            # 打开保存对话框
            file_path, selected_filter = QFileDialog.getSaveFileName(
                self,
                self.tr("保存文件"),
                last_path,
                filters
            )
            
            if not file_path:
                return
                
            # 记住这次的保存路径
            self.settings.setValue('last_save_path', os.path.dirname(file_path))
            current_tab.file_path = file_path
        
        try:
            # 检测文件编码
            text = current_tab.toPlainText()
            try:
                # 尝试使用UTF-8编码
                text.encode('utf-8')
                encoding = 'utf-8'
            except UnicodeEncodeError:
                # 如果UTF-8失败,使用GBK
                encoding = 'gbk'
            
            # 保存文件
            with open(file_path, 'w', encoding=encoding) as file:
                file.write(text)
            
            # 更新UI状态
            self.updateTabIcon(self.tabWidget.currentIndex())
            self.statusBar().showMessage(
                self.tr(f'✔ 文件已保存: {os.path.basename(file_path)} [{encoding}]'), 
                3000
            )
            logger.info(self.tr(f"文件已保存: {file_path} (编码: {encoding})"))
            
            # 清除修改标记
            if hasattr(current_tab, 'document'):
                current_tab.document().setModified(False)
                
        except (IOError, OSError) as e:
            # 处理IO错误
            error_msg = self.tr(f"无法保存文件: {str(e)}")
            ClutMessageBox.show_message(
                self, 
                self.tr('保存错误'), 
                error_msg
            )
            logger.error(self.tr(f"[Log/ERROR]保存失败(IO): {str(e)}"))
            self.statusBar().showMessage(self.tr('❌ 保存失败'), 3000)
            
        except Exception as e:
            # 处理其他错误
            error_msg = self.tr(f"保存时发生未知错误: {str(e)}")
            ClutMessageBox.show_message(
                self,
                self.tr('保存错误'),
                error_msg
            )
            logger.error(self.tr(f"[Log/ERROR]保存失败: {str(e)}"))
            self.statusBar().showMessage(self.tr('❌ 保存失败'), 3000)

    def saveAs(self):
        """另存为功能"""
        current_tab = self.tabWidget.currentWidget()
        if not current_tab:
            return
        
        # 获取当前标签页的名称和文件后缀
        current_tab_name = self.tabWidget.tabText(self.tabWidget.currentIndex())
        file_extension = os.path.splitext(current_tab_name)[1]
        
        dialog = QFileDialog(self)
        dialog.setWindowTitle(self.tr("另存为"))
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setOption(QFileDialog.DontUseNativeDialog)
        
        # 设置默认文件名和后缀
        dialog.selectFile(current_tab_name)
        
        # 根据文件后缀设置默认选中的文件类型过滤器
        filters = [
            ("文本文件", "*.txt"),
            ("Python文件", "*.py"),
            ("Markdown文件", "*.md"),
            ("所有文件", "*")
        ]
        
        filter_string = ";;".join([f"{name} ({ext})" for name, ext in filters])
        dialog.setNameFilter(filter_string)
        
        # 根据当前文件后缀选择对应的过滤器
        if file_extension:
            for name, ext in filters:
                if ext.endswith(file_extension):
                    dialog.selectNameFilter(f"{name} ({ext})")
                    break
        
        # 查找并设置工具按钮的图标和样式
        for button in dialog.findChildren(QToolButton):
            button.setIconSize(QSize(20, 20))
            if button.accessibleName() == "Back":
                button.setIcon(QIcon('./tsuki/assets/resources/nav/back.png'))
            elif button.accessibleName() == "Forward":
                button.setIcon(QIcon('./tsuki/assets/resources/nav/forward.png'))
            elif button.accessibleName() == "Parent Directory":
                button.setIcon(QIcon('./tsuki/assets/resources/nav/up.png'))
            elif button.accessibleName() == "Create New Folder":
                button.setIcon(QIcon('./tsuki/assets/resources/nav/new_folder.png'))
                button.setIconSize(QSize(16, 16))
            elif button.accessibleName() == "List View":
                button.setIcon(QIcon('./tsuki/assets/resources/nav/list_view.png'))
                button.setIconSize(QSize(16, 16))
            elif button.accessibleName() == "Detail View":
                button.setIcon(QIcon('./tsuki/assets/resources/nav/detail_view.png'))
                button.setIconSize(QSize(16, 16))
                
            # 设置按钮样式
            button.setStyleSheet("""
                QToolButton {
                    background-color: transparent;
                    border: 1px solid transparent;
                    border-radius: 4px;
                    padding: 4px;
                    margin: 2px;
                    min-width: 30px;
                    min-height: 30px;
                }
                QToolButton:hover {
                    background-color: #e5f3ff;
                    border: 1px solid #cce4f7;
                }
                QToolButton:pressed {
                    background-color: #cce4f7;
                    border: 1px solid #99d1ff;
                }
            """)
        
        # 设置对话框的整体样式为拟态风格
        dialog.setStyleSheet("""
            QFileDialog {
                background-color: #f0f0f0;
                border-radius: 10px;
                border: 1px solid #ddd;
            }
            QLabel {
                color: #333;
                font-family: 'Microsoft YaHei';
                font-size: 12px;
            }
            QComboBox {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px;
                min-width: 120px;
                background: #f0f0f0;
                font-family: 'Microsoft YaHei';
            }
            QComboBox:hover {
                border-color: #0078d4;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 4px;
                font-family: 'Microsoft YaHei';
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton[text="Cancel"] {
                background-color: #f0f0f0;
                color: #333;
            }
            QPushButton[text="Cancel"]:hover {
                background-color: #e0e0e0;
            }
            QLineEdit {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 6px;
                font-family: 'Microsoft YaHei';
                background: #ffffff;
            }
            QLineEdit:focus {
                border-color: #0078d4;
            }
            QTreeView, QListView {
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: #f0f0f0;
                font-family: 'Microsoft YaHei';
                selection-background-color: #e5f3ff;
                selection-color: #000;
                outline: none;
            }
            QTreeView::item, QListView::item {
                padding: 4px;
                border-radius: 2px;
            }
            QTreeView::item:hover, QListView::item:hover {
                background-color: #f0f9ff;
            }
            QTreeView::item:selected, QListView::item:selected {
                background-color: #e5f3ff;
                color: #000;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                border: none;
                border-right: 1px solid #ddd;
                border-bottom: 1px solid #ddd;
                padding: 4px;
                font-family: 'Microsoft YaHei';
                font-size: 12px;
            }
            QScrollBar:vertical {
                border: none;
                background: #f5f5f5;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #cdcdcd;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a6a6a6;
            }
        """)
        
        # 创建编码选择组件
        encoding_label = QLabel(self.tr("编码:"), dialog)
        encoding_combo = QComboBox(dialog)
        encodings = [
            'UTF-8', 'GBK', 'GB2312', 'GB18030', 'BIG5', 'UTF-16', 'UTF-32',
            'Shift-JIS', 'EUC-JP', 'EUC-KR', 'KOI8-R', 'Windows-1251',
            'Windows-1252', 'ISO-8859-1', 'ISO-8859-2', 'ISO-8859-5',
            'ASCII', 'Latin-1', 'CP949', 'CP950'
        ]
        encoding_combo.addItems(encodings)
        
        # 使用chardet检测当前文本编码
        text = current_tab.toPlainText()
        result = chardet.detect(text.encode())
        detected_encoding = result['encoding']
        
        # 如果检测到编码在列表中,则设置为默认选项
        if detected_encoding and detected_encoding.upper() in encodings:
            encoding_combo.setCurrentText(detected_encoding.upper())
        else:
            encoding_combo.setCurrentText('UTF-8')
        
        # 获取对话框的布局
        layout = dialog.layout()
        
        # 创建水平布局来放置编码选择组件
        encoding_layout = QHBoxLayout()
        encoding_layout.addWidget(encoding_label)
        encoding_layout.addWidget(encoding_combo)
        encoding_layout.addStretch()
        
        # 将编码选择添加到对话框布局的底部
        if isinstance(layout, QGridLayout):
            row = layout.rowCount()
            layout.addLayout(encoding_layout, row, 0, 1, layout.columnCount())
        
        if dialog.exec_() == QDialog.Accepted:
            try:
                file_path = dialog.selectedFiles()[0]
                encoding = encoding_combo.currentText()
                
                # 获取文本内容
                text = current_tab.toPlainText()
                
                # 尝试使用选定的编码保存文件
                try:
                    # 先尝试编码测试
                    text.encode(encoding)
                    
                    # 如果编码测试通过，则保存文件
                    with open(file_path, 'w', encoding=encoding) as file:
                        file.write(text)
                        
                except UnicodeEncodeError:
                    # 如果选定的编码无法编码内容，使用 UTF-8 作为后备编码
                    logger.warning(f"无法使用 {encoding} 编码保存文件，将使用 UTF-8")
                    encoding = 'utf-8'
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(text)
                
                # 更新标签页信息
                current_tab.file_path = file_path
                current_tab.current_encoding = encoding
                
                # 更新UI
                self.updateTabIcon(self.tabWidget.currentIndex())
                self.tabWidget.setTabText(self.tabWidget.currentIndex(), os.path.basename(file_path))
                
                # 保存编码信息
                try:
                    encoding_info_path = file_path + '.encoding'
                    with open(encoding_info_path, 'w', encoding='utf-8') as f:
                        f.write(encoding)
                except Exception as e:
                    logger.warning(f"保存编码信息文件失败: {str(e)}")
                
                # 更新状态
                if hasattr(current_tab, 'document'):
                    current_tab.document().setModified(False)
                    
                self.statusBar().showMessage(
                    self.tr(f'✔ 文件已另存为: {os.path.basename(file_path)} [{encoding}]'), 
                    3000
                )
                logger.info(self.tr(f"文件已另存为: {file_path} (编码: {encoding})"))
                
                if hasattr(current_tab, 'document'):
                    current_tab.document().setModified(False)
                    
            except Exception as e:
                error_msg = f"另存为失败: {str(e)}"
                ClutMessageBox.show_message(self, self.tr('保存错误'), self.tr(error_msg))
                logger.error(f"[Log/ERROR]另存为失败: {str(e)}")
                self.statusBar().showMessage(self.tr('❌ 另存为失败'), 3000)

    def closeFile(self):
        m = self.tabWidget.currentIndex()
        if m == -1: return
        currentWidget = self.tabWidget.currentWidget()
        # 检查是否为图片查看器
        if isinstance(currentWidget, QLabel):
            self.closeTab(m)
            return
            
        # 文本编辑器的处理逻辑
        content = currentWidget.toPlainText() 
        n = self.autoSave(content)
        if (n == 0): self.closeTab(m)
        
    def openFilePath(self, index):
        current_tab = self.tabWidget.widget(index)
        if current_tab:
            # 获取当前标签页的文本
            tab_name = self.tabWidget.tabText(index)
            
            # 尝试获取文件路径
            file_path = getattr(current_tab, 'file_path', None)
            
            # 如果没有file_path属性,尝试使用标签名作为路径
            if not file_path and os.path.exists(tab_name):
                file_path = tab_name
                
            if file_path and os.path.exists(file_path):
                try:
                    # 使用 explorer /select 命令打开文件夹并选中文件
                    file_path = os.path.normpath(file_path)  # 规范化路径
                    subprocess.run(['explorer', '/select,', file_path])
                    logger.info(f"Opened folder and selected file: {file_path}")
                    self.statusBar().showMessage(self.tr(f"TsukiTab✔: 成功打开文件夹并定位文件: {file_path}"))
                except Exception as e:
                    error_msg = f"无法打开文件夹: {str(e)}"
                    self.statusBar().showMessage(self.tr(f"TsukiTab❌: {error_msg}"))
                    logger.error(self.tr(f"Failed to open folder: {str(e)}"))
            else:
                # 如果是新建的未保存
                if tab_name.startswith(self.tr("未命名")):
                    self.statusBar().showMessage(self.tr("TsukiTab❌: 新建文件尚未保存,无法打开所在文件夹"))
                    logger.info("Attempted to open folder of unsaved new file")
                else:
                    self.statusBar().showMessage(self.tr("TsukiTab❌: 文件路径不存在"))
                    logger.warning(f"File path does not exist: {file_path or tab_name}")
        else:
            self.statusBar().showMessage(self.tr("TsukiTab❌: 当前标签页为空"))
            logger.error(self.tr("Current tab is empty"))

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
                logger.info(self.tr(f"Close Tab: {index}"))
            else:
                self.statusBar().showMessage(self.tr(f'TsukiTab🚫: 无法关闭这个标签页,因为他是最后一个,如需关闭软件,请按退出软件! -注意保存您的文件'))
                logger.error(self.tr(f"[Log/ERROR]Close Tab Error"))
                ClutMessageBox.show_message(self, '错误', f'发生错误：无法关闭这个标签页,因为他是最后一个,如需关闭软件,请按退出软件! -注意保存您的文件')
                return
        except Exception as e:
            logger.error(self.tr(f"[Log/ERROR]Close Tab Error: {e}"))
            ClutMessageBox.show_message(self, self.tr('错误'), self.tr(f'发生错误：{str(e)}'))
            self.statusBar().showMessage(self.tr(f'TsukiTab❌: 关闭标签页失败！详见MessageBox！'))
            return
    def checkForUpdates(self):
        update_software = 'TsukiNotes_Update.exe'
        try:
            os.system(f"start {update_software}")
            logger.info(self.tr(f"Check For Update: {update_software}"))
        except Exception as e:
            logger.error(self.tr(f"[Log/ERROR]Check For Update Error: {e}"))
            ClutMessageBox.show_message(self, self.tr('错误'), self.tr(f'发生错误：{str(e)}'))
            self.statusBar().showMessage(self.tr(f'TsukiUpdate❌: 检测更新失败！详见MessageBox！'))

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
                logger.info(self.tr(f"Check For Updates: {latest_version}"))
                ClutMessageBox.show_message(self, self.tr('TSUKI_BACK—Information'),
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
        result = ClutMessageBox.show_message(
            self,
            title=self.tr(f"检测更新 | 您的版本Ver{self.current_version} | TsukiNotes"),
            text=self.tr(f"Hey,您现在使用的是：\n[备用]更新方案\n[推荐🔰]自动检测\n若无法成功检测，建议打开魔法再次尝试\nVersion:{self.current_version}\nTsukiNotes 2024"),
            buttons=["下载源1-OD", "下载源2-123", "Github", "官网版本对照🔰", "取消"]
        )

        if result == "下载源1-OD":
            webbrowser.open(
                'https://zstlya-my.sharepoint.com/:f:/g/personal/zz_zstlya_onmicrosoft_com/EiGVt3ZyYFZPgQu5qxsTNIQB2y0UjGvjBKMRmOfZJ-L3yg?e=iZD2iL')
            self.statusBar().showMessage(self.tr(f'TsukiUpdate[2]✔: 您已选择OneDrive下载源！已经为您跳转至浏览器'))
            logger.info(self.tr(f"Open Web {webbrowser.open}"))
        elif result == "下载源2-123":
            webbrowser.open('https://www.123pan.com/s/ZhtbVv-gagV3.html')
            self.statusBar().showMessage(self.tr(f'TsukiUpdate[2]✔: 您已选择123Pan下载源！已经为您跳转至浏览器'))
        elif result == "Github":
            webbrowser.open('https://github.com/buaoyezz/TsukiNotes')
            self.statusBar().showMessage(self.tr(f'TsukiUpdate[2]✔: 您已选择浏览zzbuaoye0已经为您跳转至浏览器'))
            logger.info(self.tr(f"Open Web {webbrowser.open}"))
        elif result == "官网版本对照🔰":
            webbrowser.open(f'https://zzbuaoye.us.kg/TsukiNotes/{self.current_version}/update.txt')
            logger.info(self.tr(f"Open Web {webbrowser.open}"))
        elif result == "取消":
            self.statusBar().showMessage(self.tr(f'TsukiUpdate[2]🚫: 您已取消操作'))
            logger.info(self.tr(f"UserChannel"))

    def versionnow(self):
        version = self.current_version
        ClutMessageBox.show_message(self, self.tr('当前版本'), self.tr(f'当前版本：[ {version} ]'))
        self.statusBar().showMessage(self.tr(f'✔叮叮！检测成功！您当前版本为：{version}'))
        logger.info(self.tr(f"Open VersionNow.def look New Version\n"))

    def aboutMessage(self):
        current_version = self.current_version
        versiongj = self.version_gj
        version_td = self.version_td
        
        about_text = self.tr("""
            <div style='background: linear-gradient(135deg, #e6f3ff 0%, #ffffff 100%); padding: 30px; border-radius: 10px; box-shadow: 0 8px 16px rgba(0,0,0,0.1);'>
                <h1 style='font-family: "Microsoft YaHei", sans-serif; text-align: center; margin-bottom: 20px; text-shadow: 2px 2px 4px rgba(0,0,0,0.1);'>
                    <span style='background: linear-gradient(45deg, #4b9cdb 0%, #2171b5 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Tsuki</span>
                    <span style='background: linear-gradient(45deg, #2171b5 0%, #08519c 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Notes</span>
                </h1>
                
                <div style='text-align: center; margin: 20px 0;'>
                    <img src='./tsuki/assets/resources/GUI/logo.png' width='64' height='64' style='border-radius: 50%; box-shadow: 0 4px 8px rgba(0,0,0,0.15);'>
                </div>
                
                <p style='font-family: "Microsoft YaHei", sans-serif; font-size: 16px; text-align: center; margin: 15px 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.1);'>
                    <strong>BY ZZBuAoYe 2024</strong>
                </p>
                
                <div style='background: linear-gradient(135deg, #ffffff 0%, #f0f8ff 100%); padding: 15px; border-radius: 8px; margin: 20px 0; box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);'>
                    <p style='font-family: "Microsoft YaHei", sans-serif; font-size: 14px; text-align: center; margin: 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.1);'>
                        <strong>Version: {0} {1}</strong>
                    </p>
                </div>
                
                <p style='font-family: "Microsoft YaHei", sans-serif; font-size: 12px; text-align: center; margin-top: 20px; color: #6e7c7c; text-shadow: 1px 1px 1px rgba(0,0,0,0.05);'>
                    Copyright © 2024 ZZBuAoYe. All rights reserved.
                </p>
            </div>
        """.format(current_version, version_td))

        msg = QMessageBox(self)
        msg.setWindowTitle(self.tr(f"About TsukiNotes | #{versiongj}"))
        msg.setText(about_text)
        msg.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        msg.setStyleSheet("""
            QMessageBox {
                background: linear-gradient(135deg, #e6f3ff 0%, #ffffff 100%);
                border: 2px solid #4b9cdb;
                border-radius: 10px;
            }
            QMessageBox QLabel {
                min-width: 450px;
                min-height: 450px;
                font-family: "Microsoft YaHei";
            }
            QPushButton {
                font-family: "Microsoft YaHei";
                padding: 8px 20px;
                background: linear-gradient(135deg, #4b9cdb 0%, #2171b5 100%);
                color: white;
                border: none;
                border-radius: 5px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background: linear-gradient(135deg, #2171b5 0%, #08519c 100%);
            }
            #closeButton {
                position: absolute;
                top: 10px;
                right: 10px;
                width: 20px;
                height: 20px;
                background: #ff4d4d;
                border: none;
                border-radius: 10px;
                color: white;
                font-weight: bold;
            }
            #closeButton:hover {
                background: #ff0000;
            }
        """)
        

        closeButton = QPushButton("×", msg)
        closeButton.setObjectName("closeButton") 
        closeButton.setFixedSize(20, 20)
        closeButton.setCursor(Qt.PointingHandCursor)
        closeButton.clicked.connect(msg.close)
        
        msg.setStyleSheet("""
            QMessageBox {
                background: linear-gradient(135deg, #e6f3ff 0%, #ffffff 100%);
                border: 2px solid #4b9cdb;
                border-radius: 10px;
            }
            QMessageBox QLabel {
                min-width: 450px;
                min-height: 450px;
                font-family: "Microsoft YaHei";
            }
            QPushButton {
                font-family: "Microsoft YaHei";
                padding: 8px 20px;
                background: linear-gradient(135deg, #4b9cdb 0%, #2171b5 100%);
                color: white;
                border: none;
                border-radius: 5px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background: linear-gradient(135deg, #2171b5 0%, #08519c 100%);
            }
            #closeButton {
                background: transparent;
                border: none;
                color: #666666;
                font-family: Arial, sans-serif;
                font-size: 16px;
                font-weight: bold;
                padding: 0;
                margin: 0;
            }
            #closeButton:hover {
                color: #ff4d4d;
                background: transparent;
            }
            #closeButton:pressed {
                color: #cc0000;
            }
        """)
        
        def adjustButtonPosition():
            margin = 10
            closeButton.move(msg.width() - closeButton.width() - margin, margin)
        
        msg.show()
        adjustButtonPosition()
        
        # 处理窗口大小变化
        def resizeEvent(event):
            adjustButtonPosition()
            QMessageBox.resizeEvent(msg, event)
        
        msg.resizeEvent = resizeEvent
        
        msg.exec_()

    def aboutDetails(self):
        versiongj = self.version_gj
        
        msg = QMessageBox(self)
        msg.setWindowTitle("软件信息")
       # msg.setWindowFlags(msg.windowFlags() & ~Qt.WindowTitleHint)
        msg.setMinimumWidth(900)  # 设置最小宽度
        
        about_html = f"""
        <div style='padding:20px 30px;letter-spacing:0px'>
            <div style='padding:15px;min-width:350px'>
                <p style='color:#444;font-size:15px;line-height:1.8;margin:10px 0'>
                    <span style='color:#666;display:inline-block;width:80px'>软件出品:</span> <span style='margin-left:10px'>MoonZZ</span><br>
                    <span style='color:#666;display:inline-block;width:80px'>发布时间:</span> <span style='margin-left:10px'>{self.update_Date}</span><br>
                    <span style='color:#666;display:inline-block;width:80px'>版本信息:</span> <span style='margin-left:10px'>{self.version_td}</span><br>
                    <span style='color:#666;display:inline-block;width:80px'>内部版本:</span> <span style='margin-left:10px'>{versiongj}</span>
                </p>
                <p style='color:#888;font-size:13px;text-align:center;margin-top:20px;padding-top:15px;border-top:1px solid #eee'>
                    ZZBuAoYe 2024©Copyright
                </p>
            </div>
        </div>
        """
        
        msg.setText(about_html)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #fafafa;
                min-width: 400px;
            }
            QPushButton {
                padding: 6px 20px;
                background-color: #e0e0e0;
                border: none;
                border-radius: 4px;
                font-size: 13px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
        """)
        
        msg.exec_()
        
        self.statusBar().showMessage(self.tr(f'TsukiINFO: [{versiongj}] | [{self.version_td}] | [{self.update_Date}] '))
        logger.info(self.tr(f"Open AboutDetails.def"))


    def getOnlineUpdateText(self):
        try:
            api_url = 'https://api.github.com/repos/buaoyezz/TsukiNotes/releases'
            
            headers = {
                'Accept': 'application/vnd.github.v3+json'
            }
            if hasattr(self, 'github_token'):
                headers['Authorization'] = f'token {self.github_token}'
            
            response = requests.get(api_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                releases = response.json()
                if releases:
                    current_version = f"TsukiNotesV{self.current_version}"
                    matching_release = None
                    
                    for release in releases:
                        tag_name = release.get('tag_name', '')
                        name = release.get('name', '')
                        
                        if current_version in tag_name or current_version in name:
                            matching_release = release
                            break
                    
                    if matching_release:
                        body = matching_release.get('body', '')
                        # 调整宽度,使内容不超出屏幕
                        return f"""
                        <div style='color: #ffffff; font-family: "Microsoft YaHei", sans-serif; 
                             white-space: pre-wrap; line-height: 1.5; padding: 10px;
                             max-width: 800px; margin: 0 auto; word-wrap: break-word;'>
                            {body}
                        </div>
                        """
                    else:
                        logger.error(f"未找到版本 {current_version} 的更新日志")
                        return self.tr("<p style='text-align: center; color: #ffffff;'>未找到当前版本的更新日志</p>")
                else:
                    return self.tr("<p style='text-align: center; color: #ffffff;'>未找到任何发布信息</p>")
                    
            elif response.status_code == 403:
                logger.error(self.tr("API 访问次数超限"))
                return self.tr("<p style='text-align: center; color: #ffffff;'>API 访问次数超限，请稍后再试</p>")
            else:
                error_msg = f"API请求失败 (状态码: {response.status_code})"
                logger.error(self.tr(f"Github API请求失败: {error_msg}"))
                return self.tr("<p style='text-align: center; color: #ffffff;'>无法获取Github更新日志，请检查网络连接或稍后再试。</p>")
                
        except requests.exceptions.Timeout:
            logger.error(self.tr("Github API 请求超时"))
            return self.tr("<p style='text-align: center; color: #ffffff;'>请求超时，请检查网络连接</p>")
            
        except requests.exceptions.RequestException as e:
            logger.error(self.tr(f"网络请求异常: {e}"))
            return self.tr("<p style='text-align: center; color: #ffffff;'>网络连接异常，无法获取更新日志。</p>")
            
        except Exception as e:
            logger.error(self.tr(f"获取更新日志时发生错误: {e}"))
            return self.tr("<p style='text-align: center; color: #ffffff;'>获取更新日志时发生错误。</p>")

    def online_updateMessage(self):
        version = self.current_version 
        versiontime = self.version_gj  
        version_td = self.version_td
        update_time = self.update_Date
        
        try:
            online_update_text = self.getOnlineUpdateText()
        except Exception as e:
            logger.error(self.tr(f"[Log/ERROR]获取Github更新日志失败: {e}"))
            online_update_text = self.tr("无法获取Github更新日志，请检查网络连接或稍后再试。")

        update_text = (
            "<html>"
            "<h2 style='color: #ffffff; font-family: \"Microsoft YaHei\", sans-serif; text-align: left; margin-bottom: 20px;'>" + 
            self.tr("| TsukiNotes Github更新日志🌐") + "</h2>"
            f"<p style='color: #cccccc; font-size: 16px; text-align: center; margin-bottom: 15px;'>" + 
            self.tr("版本: {0} {1} [{2}]").format(version, version_td, update_time) + "</p>"
            "</html>"
            f"<hr style='border: 0; height: 1px; background: #555555; margin: 20px 0;'>"
            f"<div style='padding: 15px; border-radius: 5px; margin-bottom: 20px;'>{online_update_text}</div>"
            f"<hr style='border: 0; height: 1px; background: #555555; margin: 20px 0;'>"
            f"<p style='color: #ffffff; font-size: 18px; font-weight: bold; text-align: center; margin-top: 10px;'> || {version_td} ||</p>"
            f"<p style='color: #aaaaaa; font-size: 14px; text-align: center;'>" + 
            self.tr("[内部版本号: {0}]").format(versiontime) + "</p>"
        )

        ClutMessageBox.show_message(
            parent=self,
            title=self.tr("TsukiNotes[{0}] Github更新日志 -Ver{1}{2}").format(version, version, version_td),
            text=update_text
        )

        self.statusBar().showMessage(self.tr('TsukiBack✔: 您查看了Github更新日志'))
        logger.info(self.tr("成功获取Github更新日志"))



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
        qss_file_path = './tsuki/ui/theme/Tab_Rename.qss'
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
                logger.info(self.tr(" Tab renamed: {0} -> {1}").format(current_name, new_name))
            elif not new_name:
                ClutMessageBox.show_message(self, self.tr("重命名失败"), self.tr("标签名不能为空"))
                logger.warning(self.tr("[Log/WARNING] Attempted to rename tab with empty name"))
            else:
                self.statusBar().showMessage(self.tr('TsukiTab: 标签名未更改'))
                logger.info(self.tr(" Tab name unchanged: {0}").format(current_name))

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
                logger.info(self.tr(f"Close Tab: {index}"))
            else:
                self.statusBar().showMessage(self.tr(f'TsukiTab🚫: 无法关闭这个标签页,因为他是最后一个,如需关闭软件,请按退出软件! -注意保存您的文件'))
                logger.error(self.tr(f"[Log/ERROR]Close Tab Error"))
        except Exception as e:
            ClutMessageBox.show_message(self, self.tr('错误'), self.tr(f'发生错误：{str(e)}'))
            logger.error(self.tr(f"[Log/ERROR]Close Tab Error: {e}"))
            self.statusBar().showMessage(self.tr(f'TsukiTab❌: 关闭标签页失败！详见MessageBox！'))
        

    def mousePressEvent(self, event):
        if event.button() == 4:
            index = self.tabWidget.tabBar().tabAt(event.pos())
            if index >= 0:
                self.closeTab(index)

    def contextMenuEvent(self, event):
        index = self.tabWidget.tabBar().tabAt(event.pos())
        if index >= 0:
            menu = QMenu(self)
            rename_action = QAction(QIcon('./tsuki/assets/resources/font_size_reset_tab.png'), self.tr('重命名标签'), self)
            rename_action.triggered.connect(lambda: self.renameTab(index))
            menu.addAction(rename_action)
            menu.exec_(event.globalPos())
                

    def autoSave(self, content):
        print("开始自动保存检查")  # 调试日志
        if str(self.before) == str(content):
            self.text_modified = False
        else:
            self.text_modified = True
                
        if self.text_modified:
            try:
                print("显示保存对话框")  # 调试日志
                result = ClutMessageBox.show_message(
                    self,
                    title=self.tr("保存提醒"), 
                    text=self.tr("文本可能被修改，是否保存？"),
                    buttons=["保存", "不保存退出", "取消"]
                )
                
                print(f"用户选择: {result}")  # 调试日志
                
                if result == "保存":
                    print("开始执行保存操作")  # 调试日志
                    current_tab = self.tabWidget.currentWidget()
                    if not current_tab:
                        print("没有活动的标签页")  # 调试日志
                        return -1
                        
                    # 调用保存方法
                    save_result = self.performSave()
                    print(f"保存结果: {save_result}")  # 调试日志
                    return save_result
                    
                elif result == "不保存退出":
                    print("用户选择不保存退出")  # 调试日志
                    return 0
                elif result == "取消":
                    print("用户取消操作")  # 调试日志
                    return -1
                else:
                    print(f"未知的返回值: {result}")  # 调试日志
                    return -1
                    
            except Exception as e:
                print(f"自动保存过程发生错误: {e}")  # 调试日志
                logger.error(self.tr(f"[Log/ERROR]自动保存过程发生错误: {e}"))
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
        qss_file_path = './tsuki/ui/theme/Search_Perform_Dialog.qss'
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
                        ClutMessageBox.show_message(self, self.tr('搜索结果'), self.tr('未找到匹配项'))
                else:
                    ClutMessageBox.show_message(self, self.tr('错误'), self.tr('当前标签页不支持搜索'))

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
            logger.info(self.tr(f" Background settings applied."))

        except Exception as e:
            QMessageBox.critical(self, self.tr('错误'), self.tr(f'发生错误：{str(e)}'))
            self.statusBar().showMessage(self.tr(f'TsukiBC❌: 背景设置失败！详见MessageBox！'))
            logger.error(self.tr(f'Background settings error: {str(e)}'))

    def save_background_settings(self, image_path, transparency):
        settings = QSettings('TsukiReader', 'Background')
        settings.setValue('backgroundImage', image_path)
        settings.setValue('backgroundTransparency', transparency)

    def load_background_settings(self, widget=None):
        try:
            if widget is None:
                logger.info("没有指定 widget,跳过背景设置")
                return
                
            config = configparser.ConfigParser()
            config_dir = self.get_app_path('assets/app/config/background')
            config_path = os.path.join(config_dir, 'background_color.ini')
            
            if not os.path.exists(config_dir):
                try:
                    os.makedirs(config_dir, exist_ok=True)
                    logger.info(f"创建配置目录: {config_dir}")
                except Exception as e:
                    logger.error(f"创建配置目录失败: {e}")
                    return
                    
            if not os.path.exists(config_path):
                try:
                    config['Background'] = {
                        'image_path': self.get_app_path('assets/app/default/default_light.png'),
                        'color': '#FFFFFF'
                    }
                    with open(config_path, 'w', encoding='utf-8') as f:
                        config.write(f)
                    logger.info("创建默认背景配置文件")
                except Exception as e:
                    logger.error(f"创建默认配置文件失败: {e}")
                    return
                    
            try:
                config.read(config_path, encoding='utf-8')
                image_path = config.get('Background', 'image_path', 
                                      fallback=self.get_app_path('assets/app/default/default_light.png'))
                
                # 规范化路径并将反斜杠转换为正斜杠
                image_path = os.path.normpath(image_path).replace('\\', '/')
                
                if os.path.exists(image_path):
                    style_sheet = """
                        QPlainTextEdit {
                            background-image: url('%s');
                            background-position: center;
                            background-repeat: no-repeat;
                            background-attachment: fixed;
                        }
                    """ % image_path
                    widget.setStyleSheet(style_sheet)
                    logger.info(f"成功加载背景图片: {image_path}")
                else:
                    logger.warning(f"背景图片不存在: {image_path}")
                    default_image = self.get_app_path('assets/app/default/default_light.png')
                    default_image = os.path.normpath(default_image).replace('\\', '/')
                    if os.path.exists(default_image):
                        style_sheet = """
                            QPlainTextEdit {
                                background-image: url('%s');
                                background-position: center;
                                background-repeat: no-repeat;
                                background-attachment: fixed;
                            }
                        """ % default_image
                        widget.setStyleSheet(style_sheet)
                        logger.info("使用默认背景图片")
                    
            except Exception as e:
                logger.error(f"读取配置文件失败: {e}")
                
        except Exception as e:
            logger.error(f"载入BackGroundSettings失败: {e}")

    def reset_background_color(self):
        config = configparser.ConfigParser()
        
        try:
            # 使用用户目录作为配置文件位置
            user_config_dir = os.path.expanduser('~/.tsuki/config/background')
            os.makedirs(user_config_dir, exist_ok=True)
            config_path = os.path.join(user_config_dir, 'background_color.ini').replace('\\', '/')
            
            # 规范化默认图片路径
            default_image_path = os.path.normpath(self.get_apppath('assets/app/default/default_light.png')).replace('\\', '/')
            
            # 如果配置文件不存在，创建新的配置
            if not os.path.exists(config_path):
                config['Background'] = {
                    'image_path': default_image_path,
                    'color': '#FFFFFF'
                }
                try:
                    with open(config_path, 'w', encoding='utf-8') as configfile:
                        config.write(configfile)
                    logger.info(f"创建新的配置文件: {config_path}")
                except Exception as e:
                    logger.warning(f"无法创建配置文件: {e}，将使用内存中的设置喵~")
            else:
                try:
                    config.read(config_path, encoding='utf-8')
                    logger.info(f"成功读取配置文件: {config_path}")
                except Exception as e:
                    logger.warning(f"读取配置文件失败: {e}，将使用默认设置喵~")
            
            # 获取图片路径
            image_path = default_image_path
            if 'Background' in config:
                config_image_path = config['Background'].get('image_path', default_image_path)
                if os.path.exists(config_image_path):
                    image_path = config_image_path
                else:
                    logger.warning(f"配置的图片路径不存在: {config_image_path}，使用默认图片喵~")
            
            # 修改背景样式表，移除不支持的属性
            style_sheet = f"""
                QPlainTextEdit {{
                    background-image: url('{image_path}');
                    background-position: center;
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                    padding: 10px;
                    border: none;
                }}
            """
            
            # 应用样式
            if current_widget := self.tabWidget.currentWidget():
                current_widget.setStyleSheet(style_sheet)
                message = f'成功加载背景图片！'
                self.statusBar().showMessage(f'TsukiBC✔: {message}')
                logger.info(f"背景设置成功: {image_path}")
                
                # 尝试更新配置文件
                try:
                    if not config.has_section('Background'):
                        config.add_section('Background')
                    config['Background']['image_path'] = image_path
                    with open(config_path, 'w', encoding='utf-8') as configfile:
                        config.write(configfile)
                    logger.info("配置文件更新成功喵~")
                except Exception as e:
                    logger.warning(f"更新配置文件失败: {e}，但背景已成功应用喵~")

        except Exception as e:
            self.statusBar().showMessage('TsukiBC❌: 背景设置失败喵~')
            logger.error(f"Background Color Load Error: {str(e)}")
            # 修改后备方案的样式表
            if current_widget := self.tabWidget.currentWidget():
                fallback_style = f"""
                    QPlainTextEdit {{
                        background-image: url('{default_image_path}');
                        background-position: center;
                        background-repeat: no-repeat;
                        background-attachment: fixed;
                        padding: 10px;
                        border: none;
                    }}
                """
                current_widget.setStyleSheet(fallback_style)
                logger.info("已应用默认背景喵~")

    def save_background_color(self, bg_color, text_color):
        try:
            config = configparser.ConfigParser()
            config['Background'] = {
                'color': bg_color,
                'text_color': text_color,
                'image_path': './tsuki/assets/app/default/default_light.png'

            }
        
            os.makedirs('tsuki/assets/app/config', exist_ok=True)
            with open('tsuki/assets/app/config/background/background_color.ini', 'w') as configfile:
                config.write(configfile)
                logger.info(self.tr(f"Background Color Saved:{bg_color}"))
        except Exception as e:
            ClutMessageBox.show_message(self, self.tr('错误'), self.tr(f'保存背景色设置时发生错误：{str(e)}'))
            self.statusBar().showMessage(self.tr(f'TsukiBC_Save❌: 背景色设置保存失败！'))
            logger.error(self.tr(f"[Log/ERROR]Background Color Save Error:{str(e)}"))

    def clearTempFolder(self):
        temp_folder = 'tsuki/assets/app/temp'
        try:
            if os.path.exists(temp_folder):
                shutil.rmtree(temp_folder)
            os.makedirs(temp_folder)
            self.statusBar().showMessage(self.tr('TsukiBG✔: 临时文件夹已清空！'))
            logger.info(self.tr(f"Temp Folder Cleared:{temp_folder}"))
        except Exception as e:
            ClutMessageBox.show_message(self, self.tr('清空临时文件夹'), self.tr(f'失败了❌❗: {str(e)}'))
            self.statusBar().showMessage(self.tr(f'TsukiBG❌: 清空临时文件夹失败！原因:{str(e)}'))
            logger.error(self.tr(f"[Log/ERROR]Temp Folder Clear Error:{str(e)}"))
            
    def setBackgroundImageFromFile(self, file_name):
        try:
            pixmap = QPixmap(file_name)
            palette = QPalette()
            palette.setBrush(QPalette.Background, QBrush(pixmap))
            self.setPalette(palette)
            self.statusBar().showMessage(self.tr(f'TsukiBG✔: 背景图片已成功设置！'))
            logger.info(self.tr(f"Background Image Set:{file_name}"))
        except Exception as e:
            ClutMessageBox.show_message(self, self.tr('设置背景图片'), self.tr(f'失败了❌❗: {str(e)}'))
            self.statusBar().showMessage(self.tr(f'TsukiBG❌: 背景图片设置失败！原因:{str(e)}'))
            logger.error(self.tr(f"[Log/ERROR]Background Image Set Error:{str(e)}"))

    def setBackgroundImage(self):
        file_name, _ = QFileDialog.getOpenFileName(self, self.tr('选择背景图片[内测]'), '',
                                                   self.tr('Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)'))

        if not file_name:
            return
        self.setBackgroundImageFromFile(file_name)
        self.saveBackgroundSettings(file_name)

    def loadDefaultBackground(self):
        try:
            # 默认背景图片路径
            default_bg = './tsuki/assets/app/default/default_light.png'
            
            if os.path.exists(default_bg):
                # 设置默认背景图片
                self.text_edit.setStyleSheet(f"""
                    QTextEdit {{
                        background-image: url({default_bg});
                        background-position: center;
                        background-repeat: no-repeat;
                        background-attachment: fixed;
                        padding: 10px;
                        border: none;
                    }}
                """)
                logger.info("已加载默认背景图片")
            else:
                # 如果默认背景不存在，使用纯色背景
                self.text_edit.setStyleSheet("""
                    QTextEdit {
                        background-color: #ffffff;
                        padding: 10px;
                        border: none;
                    }
                """)
                logger.warning("[Log/WARNING]默认背景图片不存在，使用纯色背景")
        except Exception as e:
            logger.error(f"[Log/ERROR]加载默认背景失败: {str(e)}")
            # 发生错误时使用纯色背景
            self.text_edit.setStyleSheet("""
                QTextEdit {
                    background-color: #ffffff;
                    padding: 10px;
                    border: none;
                }
            """)

    def loadBackgroundSettings(self):
        try:
            # 定义配置文件和默认背景图片的路径
            self.config_path = "./tsuki/assets/app/config/background/TN_BackGround.ini"
            self.default_background_path = "./tsuki/assets/app/default/default_light.png"

            # 确保配置目录存在
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)

            # 如果配置文件不存在，创建默认配置
            if not os.path.exists(self.config_path):
                self.saveBackgroundSettings(self.default_background_path)
                logger.info(self.tr(f"Created default background settings at: {self.config_path}"))

            # 读取配置文件
            config = configparser.ConfigParser()
            config.read(self.config_path, encoding='utf-8')
            logger.info(self.tr(f"Background Settings Loaded: {self.config_path}"))

            if 'Background' in config:
                background_path = config['Background'].get('ImagePath', self.default_background_path)
                transparency = config['Background'].getint('Transparency', 100)
                
                # 验证背景图片路径
                if background_path and os.path.exists(background_path):
                    try:
                        pixmap = QPixmap(background_path)
                        if pixmap.isNull():
                            raise ValueError(self.tr("无效的图片文件"))
                            
                        palette = QPalette()
                        palette.setBrush(QPalette.Background, QBrush(pixmap))
                        self.setPalette(palette)
                        self.statusBar().showMessage(self.tr(f'TsukiBG✔: 背景图片 [{background_path}] 已加载'))
                        logger.info(self.tr(f"Successfully loaded background image: {background_path}"))
                    except Exception as e:
                        logger.error(self.tr(f"[Log/ERROR]Failed to load background image {background_path}: {str(e)}"))
                        self.loadDefaultBackground()
                else:
                    logger.warning(self.tr(f"[Log/WARNING]Background image not found: {background_path}"))
                    self.loadDefaultBackground()
            else:
                logger.warning(self.tr("[Log/WARNING]No background settings found in config"))
                self.loadDefaultBackground()

        except Exception as e:
            logger.error(self.tr(f"[Log/ERROR]Failed to load background settings: {str(e)}"))
            crash_report()
            self.loadDefaultBackground()

    def saveBackgroundSettings(self, image_path, transparency=100):
        try:
            # 使用与loadBackgroundSettings相同的配置路径
            config_path = os.path.join(os.path.expanduser('~'), '.tsuki/config/background/TN_BackGround.ini')
            
            # 确保配置目录存在
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            
            config = configparser.ConfigParser()
            config['Background'] = {
                'ImagePath': image_path,
                'Transparency': str(transparency)
            }

            with open(config_path, 'w') as configfile:
                config.write(configfile)
                
            logger.info(self.tr(f"Background settings saved to {config_path}"))
        except Exception as e:
            logger.error(self.tr(f"[Log/ERROR]Failed to save background settings: {str(e)}"))
            raise
                    
    def initialize_font_size(self):
        try:
            # 设置默认的字体大小
            default_font_size = 12
            current_widget = self.tabWidget.currentWidget()
            current_font = current_widget.font()
            current_font.setPointSize(default_font_size)
            current_widget.setFont(current_font)

            ClutMessageBox.show_message(self, self.tr('提示'), self.tr(f'字体大小已经重置为默认值 {default_font_size}，喵~'))
            self.statusBar().showMessage(self.tr(f'TsukiFS✔: 字体大小已重置为默认值 {default_font_size}'))
        except Exception as e:
            ClutMessageBox.show_message(self, self.tr('错误'), self.tr(f'发生错误：{str(e)}'))
            self.statusBar().showMessage(self.tr(f'TsukiFS✔: 字体大小初始化失败！详见MessageBox！'))
            logger.error(self.tr(f"[Log/ERROR]Font Size Initialization Failed:{str(e)}"))
            crash_report()

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
            ClutMessageBox.show_message(self, self.tr('错误'), self.tr(f'发生异常：{str(e)}'))
            self.statusBar().showMessage(self.tr(f'TsukiTotalSetting❌: 发生异常：{str(e)}'))
            logger.error(self.tr(f"[Log/ERROR]Total Setting Failed:{str(e)}"))

    def toggle_highlight_keywords(self, state):
        if state == Qt.Checked:
            self.highlight_keywords = True
            ClutMessageBox.show_message(self, self.tr("高亮模式"), self.tr("Highlight Mode Enabled\nSupport Language: MD Py Java Cpp"))
        else:
            self.highlight_keywords = False
            ClutMessageBox.show_message(self, self.tr("高亮模式"), self.tr("Highlight Mode Disabled\n"))
        self.addKeywordHighlight()

    def saveSettings(self, include_whitespace, custom_lines, highlight_keywords):
        try:
            ini_dir = self.tr('tsuki/assets/app/config/app_settings')
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
            ClutMessageBox.show_message(self, self.tr('错误'), self.tr(f'保存设置时发生异常：{str(e)}'))
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
            ClutMessageBox.show_message(self, self.tr('错误'), self.tr(f'应用设置时发生异常：{str(e)}'))
            self.statusBar().showMessage(self.tr(f'TsukiApplySetting❌: 应用设置时发生异常：{str(e)}'))
            logger.error(self.tr(f"[Log/ERROR]Apply Settings Failed:{str(e)}"))

    def addKeywordHighlight(self):
        try:
            current_widget = self.tabWidget.currentWidget()
            self.highlighter = PythonHighlighter(self.highlight_keywords, current_widget.document())
        except Exception as e:
            ClutMessageBox.show_message(self, self.tr('错误'), self.tr(f'添加关键字高亮时发生异常：{str(e)}'))
            self.statusBar().showMessage(self.tr(f'添加关键字高亮时发生异常：{str(e)}'))
            crash_report()
            logger.error(self.tr(f"[Log/ERROR]Add Keyword Highlight Failed:{str(e)}"))

    def reset_background(self):
        file_path = self.tr('./tsuki/assets/app/config/background/TN_BackGround.ini')
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
            msg_box.setIconPixmap(QIcon(self.tr('./tsuki/assets/resources/done.png')).pixmap(64, 64))  # 设置自定义图标
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()
            self.setBackgroundImageFromFile(self.tr('./tsuki/assets/app/default/default_light.png'))

        else:
            msg_box = QMessageBox()
            msg_box.setWindowTitle(self.tr("提示"))
            msg_box.setText(self.tr("你还没设置背景图"))
            msg_box.setIconPixmap(QIcon(self.tr('./tsuki/assets/resources/tips.png')).pixmap(64, 64))  # 设置自定义图标
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()

    def select_and_set_background(self):
        from datetime import datetime
        user_folder = self.tr('./tsuki/assets/app/default/User_File/')
        image_files = [f for f in os.listdir(user_folder) if f.endswith('.png') or f.endswith('.jpg')]
        if not image_files:
            ClutMessageBox.show_message(self, "提示", "没有找到任何图片文件。")
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
            ClutMessageBox.show_message(self, "提示", "请先选择一个图片。")
            return

        selected_image = selected_items[0].text().split(' (ID: ')[0]
        image_path = os.path.join(user_folder, selected_image)
        self.update_background_config(image_path)
        ClutMessageBox.show_message(self, "设置成功", f"背景图片已设置为 {image_path}")

    def update_background_config(self, image_path):
        config_path = self.tr('./tsuki/assets/app/config/BackGround/background_color.ini')
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
        msg_box.setIconPixmap(QIcon(self.tr(f'./tsuki/assets/resources/{icon}')).pixmap(64, 64))
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
    
    # setting函数End==============================================================

    def performSave(self):
        try:
            options = QFileDialog.Options()
            current_tab_name = self.tabWidget.tabText(self.tabWidget.currentIndex())
            filters = self.tr("所有文件 (*);;文本文件 (*.txt);;Markdown 文件 (*.md);;Python 文件 (*.py)")
            
            fileName, selectedFilter = QFileDialog.getSaveFileName(
                self,
                self.tr(f'保存文件 - {current_tab_name}'),
                '',
                filters,
                options=options
            )
            
            if fileName:
                currentWidget = self.tabWidget.currentWidget()
                if currentWidget:
                    text = currentWidget.toPlainText()
                    with open(fileName, 'w', encoding='utf-8') as file:
                        file.write(text)
                    
                    # 更新文件路径
                    currentWidget.file_path = fileName
                    
                    # 更新状态
                    self.text_modified = False
                    self.statusBar().showMessage(self.tr(f'TsukiSave✔: 文件已保存到 {fileName}'))
                    logger.info(self.tr(f" 文件已成功保存到 {fileName}"))
                    return 0
                else:
                    logger.error(self.tr("无法获取当前文本编辑器"))
                    return -1
            else:
                logger.info(self.tr(" 用户取消了保存操作"))
                return -1
                
        except Exception as e:
            logger.error(self.tr(f"保存文件时发生错误: {str(e)}"))
            crash_report()
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
        logger.info(self.tr(f"Clear File Success"))
        currentWidget.clear()

    def performUndo(self):
        currentWidget = self.tabWidget.currentWidget()
        currentWidget.undo()
        self.statusBar().showMessage(self.tr('"Tsuki✔: 您执行了一次撤销操作"'))
        logger.info(self.tr(f"Undo File Success"))

    def performRedo(self):
        currentWidget = self.tabWidget.currentWidget()
        currentWidget.redo()

    def performCut(self):
        currentWidget = self.tabWidget.currentWidget()
        currentWidget.cut()


    def get_app_path(self, relative_path=''):
        """
        获取应用程序路径，自动处理权限和目录创建
        
        Args:
            relative_path (str): 相对路径，例如 'assets/app/config/first'
            
        Returns:
            str: 完整的文件路径
        """
        try:
            # 确定基础目录：优先使用当前目录，失败则使用用户目录
            try:
                base_dir = os.path.abspath('./tsuki')
                # 测试是否有写入权限
                test_file = os.path.join(base_dir, '.write_test')
                if not os.path.exists(base_dir):
                    os.makedirs(base_dir)
                with open(test_file, 'w') as f:
                    f.write('test')
                os.remove(test_file)
            except (PermissionError, OSError):
                # 如果没有权限，使用用户目录
                base_dir = os.path.expanduser('~/TsukiNotes/tsuki')
                if not os.path.exists(base_dir):
                    os.makedirs(base_dir)
                logger.info(self.tr(f"Using user directory: {base_dir}"))

            # 构建完整路径
            full_path = os.path.join(base_dir, relative_path)
            
            # 如果路径不存在则创建
            if relative_path and not os.path.exists(full_path):
                os.makedirs(full_path, exist_ok=True)
                logger.info(self.tr(f"Created directory: {full_path}"))
                
            return full_path
            
        except Exception as e:
            logger.error(self.tr(f"[Log/ERROR]Error accessing path {relative_path}: {str(e)}"))
            # 返回用户目录作为后备方案
            fallback_path = os.path.expanduser(f'~/TsukiNotes/tsuki/{relative_path}')
            os.makedirs(fallback_path, exist_ok=True)
            return fallback_path

    def getLatestVersion(self):
        try:
            # 获取 releases 信息
            response = requests.get("https://api.github.com/repos/buaoyezz/TsukiNotes/releases")
            releases = response.json()
            
            if releases and len(releases) > 0:
                # 获取最新版本信息
                latest_release = releases[0]
                version = latest_release["tag_name"].replace("TsukiNotesV", "")
                return version
                
        except Exception as e:
            logger.error(f"获取最新版本失败: {e}")
            return None

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        main_window = TsukiReader()
        main_window.show()
        logger.info("Main window displayed")
        sys.exit(app.exec_())
    except Exception as e:
        logger.error(f"Application failed to start: {str(e)}")
        crash_report()  # 在这里添加
        raise