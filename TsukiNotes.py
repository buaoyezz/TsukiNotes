# -*- coding: utf-8 -*-
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
    QPoint, QObject, QMetaType, QMetaObject, QLocale, QUrl,QSize
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
    QGroupBox, QListWidget, QListWidgetItem, QSpinBox,QGraphicsDropShadowEffect
)
from sympy import sympify, SympifyError
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application, parse_expr
import tempfile
from tsuki.utils.message_box import ClutMessageBox
from tsuki.utils.clut_card import ClutCard
from tsuki.utils.clut_image_card import ClutImageCard
from tsuki.utils.overlay_notification import OverlayNotification
from tsuki.widgets.tsuki_titlebar import TsukiTitleBar

# current_dir = os.path.dirname(__file__)
# sys.path.append(os.path.join(current_dir, './tsuki/assets/kernel/'))
# import cython_utils
# import savefile

def crash_report():
    try:
        # 获取当前目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        crash_report_path = os.path.join(current_dir, 'CrashReport.exe')
        
        # 检查文件是否存在
        if not os.path.exists(crash_report_path):
            logger.error(f"崩溃报告程序不存在: {crash_report_path}")
            return
            
        # 使用subprocess.Popen静默运行
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        
        process = subprocess.Popen([crash_report_path], startupinfo=startupinfo)
        
        # 等待进程启动
        process.wait(timeout=5)
        
        if process.returncode != 0:
            logger.error(f"崩溃报告程序返回错误代码: {process.returncode}")
            
    except Exception as e:
        logger.error(f"启动崩溃报告程序失败: {str(e)}")

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

class QTextEditHandler(logging.Handler):
    def __init__(self, text_edit, counters, original_logs):
        super().__init__()
        self.text_edit = text_edit
        self.counters = counters
        self.original_logs = original_logs
        
        # 初始化所有日志级别的颜色
        self.level_colors = {
            'DEBUG': '#808080',    # 灰色
            'INFO': '#008000',     # 绿色  
            'WARNING': '#FFA500',  # 橙色
            'ERROR': '#FF0000',    # 红色
            'CRITICAL': '#FF0000'  # 红色
        }
    
    def emit(self, record):
        msg = self.format(record)
        self.original_logs.append(msg)
        self.format_and_append_log(msg)
        
        # 更新计数器
        level = record.levelname  # 直接使用记录的级别名称
        self.counters[level] = self.counters.get(level, 0) + 1
        
        # 通知 DebugWindow 更新统计信息
        if hasattr(self.text_edit.parent(), 'update_statistics'):
            self.text_edit.parent().update_statistics()

    
    def format_and_append_log(self, msg):
        """格式化并添加日志消息到文本编辑器"""
        cursor = self.text_edit.textCursor()
        cursor.movePosition(cursor.End)
        
        # 设置默认格式
        format = QTextCharFormat()
        format.setForeground(QColor("#000000"))  # 默认黑色
        
        # 根据日志级别设置颜色
        for level, color in self.level_colors.items():
            if f' - {level} - ' in msg:
                format.setForeground(QColor(color))
                break
        
        cursor.insertText(msg + '\n', format)
        
        # 如果启用了自动滚动，滚动到底部
        if hasattr(self.text_edit.parent(), 'auto_scroll') and self.text_edit.parent().auto_scroll:
            scrollbar = self.text_edit.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())

class DebugWindow(QWidget):
    def __init__(self):
        super().__init__()
        # 初始化计数器
        self.log_counters = {
            'DEBUG': 0,
            'INFO': 0, 
            'WARNING': 0,
            'ERROR': 0,
            'CRITICAL': 0
        }
        debug_version = '2.0.0'
        self.setWindowTitle(self.tr(f"TsukiNotes -Debug Ver {debug_version}"))
        self.setGeometry(100, 100, 800, 600)
        self.setFont(QFont("Microsoft YaHei", 9))
        self.setWindowIcon(QIcon("./tsuki/assets/GUI/resources/GUI/terminal.png"))
        
        self.auto_scroll = True # 自动滚动[default enable]
        
        # 主布局
        main_layout = QVBoxLayout()
        
        # 工具栏
        toolbar = QToolBar()
        toolbar.setStyleSheet("QToolBar{spacing:5px;}")
        
        # 添加日志级别过滤
        self.level_combo = QComboBox()
        self.level_combo.addItems(['ALL', 'DEBUG', 'INFO', 'WARNING', 'ERROR'])
        self.level_combo.currentTextChanged.connect(self.filter_logs)
        toolbar.addWidget(QLabel(self.tr("日志级别:")))
        toolbar.addWidget(self.level_combo)
        
        # 添加搜索框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(self.tr("搜索日志..."))
        self.search_input.textChanged.connect(self.search_logs)
        toolbar.addWidget(self.search_input)
        
        # 添加功能按钮
        export_btn = QPushButton(self.tr("导出日志"))
        export_btn.clicked.connect(self.export_logs)
        toolbar.addWidget(export_btn)
        
        clear_btn = QPushButton(self.tr("清除日志"))
        clear_btn.clicked.connect(self.clear_logs)
        toolbar.addWidget(clear_btn)
        
        # 自动滚动开关
        self.scroll_check = QCheckBox(self.tr("自动滚动"))
        self.scroll_check.setChecked(True)
        self.scroll_check.stateChanged.connect(self.toggle_auto_scroll)
        toolbar.addWidget(self.scroll_check)
        
        # 主题切换
        theme_btn = QPushButton(self.tr("切换主题"))
        theme_btn.clicked.connect(self.toggle_theme)
        toolbar.addWidget(theme_btn)
        
        main_layout.addWidget(toolbar)
        
        # 日志显示区域
        self.log_text_edit = QTextEdit()
        self.log_text_edit.setReadOnly(True)
        main_layout.addWidget(self.log_text_edit)
        
        # 字体设置
        font_layout = QHBoxLayout()
        self.font_combo = QComboBox()
        self.font_combo.addItems([self.tr("Normal Font Size"),"10","11","12","13","14","15","16","17","18","19","20","21","22","365"])
        self.font_combo.currentTextChanged.connect(self.change_font_size)
        font_layout.addWidget(QLabel(self.tr("字体大小:")))
        font_layout.addWidget(self.font_combo)
        main_layout.addLayout(font_layout)
        
        # 统计信息
        self.stats_label = QLabel(self.tr("Lines: 0\nINFO: 0 | WARNING: 0 | ERROR: 0 | DEBUG: 0"))
        main_layout.addWidget(self.stats_label)
        
        self.setLayout(main_layout)
        
        # 添加原始日志存储
        self.original_logs = []
        
        # 日志处理器
        self.log_handler = QTextEditHandler(self.log_text_edit, self.log_counters, self.original_logs)
        self.log_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(self.log_handler)
        
        # 应用拟态风格
        self.apply_neumorphic_style()

    def apply_neumorphic_style(self):
        #qss + QGraphicsDropShadowEffect
        self.setStyleSheet("""
            QWidget {
                background-color: #ECECEC;
                color: #333333;
            }
            QTextEdit, QLineEdit, QComboBox, QPushButton, QCheckBox {
                border: none;
                background-color: #ECECEC;
                color: #333333;
                padding: 6px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #D1D1D1;
            }
            QPushButton:pressed {
                background-color: #C0C0C0;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 1px solid #A3A3A3;
            }
        """)
        self.add_shadow(self.log_text_edit)
        self.add_shadow(self.search_input)
        self.add_shadow(self.level_combo)
    

    def add_shadow(self, widget):
        """为控件添加阴影效果"""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(5, 5)
        widget.setGraphicsEffect(shadow)

    def filter_logs(self):
        # 优化
        level = self.level_combo.currentText()
        self.log_text_edit.clear()
        # 使用更高效的方式处理大量日志
        filtered_logs = (log for log in self.original_logs if f' - {level} - ' in log) if level != 'ALL' else self.original_logs
        for log in filtered_logs:
            self.log_handler.format_and_append_log(log)
    
    def search_logs(self):
        """搜索日志内容"""
        search_text = self.search_input.text()
        
        # 先恢复原始显示
        self.filter_logs()
        
        if search_text:
            cursor = self.log_text_edit.textCursor()
            format = QTextCharFormat()
            format.setBackground(QColor("yellow"))
            
            # 高亮匹配文本
            regex = QRegExp(search_text, Qt.CaseInsensitive)
            pos = 0
            while True:
                cursor = self.log_text_edit.document().find(regex, pos)
                if cursor.isNull():
                    break
                cursor.mergeCharFormat(format)
                pos = cursor.position()
    
    def export_logs(self):
        """导出日志到文件"""
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            self.tr("导出日志"),
            "",
            self.tr("日志文件 (*.log);;文本文件 (*.txt);;所有文件 (*.*)")
        )
        if file_name:
            try:
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(self.log_text_edit.toPlainText())
                logger.info(f"Logs exported to {file_name}")
            except Exception as e:
                logger.error(f"[Log/ERROR]Failed to export logs: {str(e)}")
    
    def clear_logs(self):
        """清除日志"""
        self.log_text_edit.clear()
        self.original_logs.clear()
        self.log_counters = {'INFO': 0, 'WARNING': 0, 'ERROR': 0, 'DEBUG': 0}
        self.update_statistics()
        self.search_input.clear()  # 清除搜索框
        logger.info("Logs cleared")
    
    def toggle_auto_scroll(self, state):
        # AC
        self.auto_scroll = state == Qt.Checked
    
    def toggle_theme(self):
        # d/l mod
        current_bg = self.log_text_edit.palette().color(QPalette.Base)
        if current_bg.lightness() > 128:
            self.apply_theme('dark')
        else:
            self.apply_theme('light')
        self.ensure_round_corners()

    def ensure_round_corners(self):
        
        widgets_with_round_corners = [self.log_text_edit, self.search_input, self.level_combo, self.scroll_check]
        for widget in widgets_with_round_corners:
            widget.setStyleSheet(widget.styleSheet() + "border-radius: 10px;")

    def apply_theme(self, theme):
        """应用主题并添加阴影效果"""
        if theme == 'dark':
            self.setStyleSheet("""
                QWidget {
                    background-color: #2b2b2b;
                    color: #ffffff;
                }
                QTextEdit, QLineEdit, QComboBox, QPushButton, QCheckBox {
                    background-color: #1e1e1e;
                    color: #ffffff;
                    border: 1px solid #3c3c3c;
                }
                QPushButton {
                    background-color: #3c3c3c;
                    border: none;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #4c4c4c;
                }
                QComboBox {
                    background-color: #3c3c3c;
                    border: 1px solid #505050;
                }
                QLineEdit {
                    background-color: #3c3c3c;
                    border: 1px solid #505050;
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget {
                    background-color: #ffffff;
                    color: #000000;
                }
                QTextEdit, QLineEdit, QComboBox, QPushButton, QCheckBox {
                    background-color: #ffffff;
                    color: #000000;
                    border: 1px solid #cccccc;
                }
                QPushButton {
                    background-color: #f0f0f0;
                    border: none;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
                QComboBox {
                    background-color: #ffffff;
                    border: 1px solid #cccccc;
                }
                QLineEdit {
                    background-color: #ffffff;
                    border: 1px solid #cccccc;
                }
            """)
        self.add_shadow_effects()

    def add_shadow_effects(self):
        """为控件添加阴影效果"""
        widgets_to_shadow = [self.log_text_edit, self.search_input, self.level_combo, self.scroll_check]
        for widget in widgets_to_shadow:
            self.add_shadow(widget)

    # 保留原有方法
    def closeEvent(self, event):
        event.accept()
        logger.info("Debug window closed")

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
        """更新统计信息显示"""
        total_lines = self.log_text_edit.document().blockCount()
        stats_text = f"Lines: {total_lines}\n"
        stats_text += f"INFO: {self.log_counters['INFO']} | "
        stats_text += f"WARNING: {self.log_counters['WARNING']} | "
        stats_text += f"ERROR: {self.log_counters['ERROR']} | "
        stats_text += f"DEBUG: {self.log_counters['DEBUG']}"
        
        self.stats_label.setText(self.tr(stats_text))

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
import os
import datetime
import re


def delete_old_logs(directory, time_threshold_days=3):
    # 确保目录存在
    try:
        os.makedirs(directory, exist_ok=True)
    except Exception as e:
        logger.error(f"创建日志目录失败: {e}")
        return

    if not os.path.exists(directory):
        logger.error(f"目录不存在: {directory}")
        return

    now = datetime.datetime.now()
    logs_by_date = {}

    try:
        for filename in os.listdir(directory):
            if filename.endswith('.log'):
                match = re.match(r'TsukiNotes_Log_(\d{4}-\d{2}-\d{2})_(\d{2}-\d{2}-\d{2})\.log', filename)
                if match:
                    date_str = match.group(1)
                    time_str = match.group(2)
                    timestamp_str = f"{date_str}_{time_str}"
                    try:
                        log_time = datetime.datetime.strptime(timestamp_str, '%Y-%m-%d_%H-%M-%S')
                        time_difference = (now - log_time).days

                        if time_difference > time_threshold_days:
                            file_path = os.path.join(directory, filename)
                            try:
                                os.remove(file_path)
                                logger.info(f"删除过期日志文件: {file_path}")
                            except Exception as e:
                                logger.error(f"删除文件失败 {file_path}: {e}")
                        else:
                            if date_str not in logs_by_date:
                                logs_by_date[date_str] = []
                            logs_by_date[date_str].append((log_time, filename))
                    except ValueError as e:
                        logger.error(f"时间戳解析错误: {timestamp_str} - {e}")
    except Exception as e:
        logger.error(f"处理日志文件时发生错误: {e}")

log_directory = os.path.join('tsuki', 'assets', 'log', 'temp')
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
        icon_path = './tsuki/assets/GUI/resources/language/exe.png'
        if os.path.exists(icon_path):
            self.tabWidget.setTabIcon(index, QIcon(icon_path))
            
        # 启动加载线程
        loader.start()
        
        # 更新状态栏
        self.statusBar().showMessage(self.tr(f'正在加载文件: {fileName}'))
        
    except Exception as e:
        self.handleError(self.tr('打开十六进制文件'), fileName, e)


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

def any(name, alternates):
    """Return a named group pattern matching list of alternates."""
    return "(?P<%s>" % name + "|".join(alternates) + ")"

def make_pat():
    """Generate pattern for Python syntax highlighting.
    
    Adapted from Python IDLE's colorizer.py
    Licensed under the Python Software Foundation License Version 2.
    """
    kw = r"\b" + any("KEYWORD", keyword.kwlist) + r"\b"
    match_softkw = (
        r"^[ \t]*" +  
        r"(?P<MATCH_SOFTKW>match)\b" +
        r"(?![ \t]*(?:" + "|".join([  
            r"[:,;=^&|@~)\]}]",  
            r"\b(?:" + r"|".join(keyword.kwlist) + r")\b",  
        ]) +
        r"))"
    )
    case_default = (
        r"^[ \t]*" +  
        r"(?P<CASE_SOFTKW>case)" +
        r"[ \t]+(?P<CASE_DEFAULT_UNDERSCORE>_\b)"
    )
    case_softkw_and_pattern = (
        r"^[ \t]*" +  
        r"(?P<CASE_SOFTKW2>case)\b" +
        r"(?![ \t]*(?:" + "|".join([  
            r"_\b",  
            r"[:,;=^&|@~)\]}]",  
            r"\b(?:" + r"|".join(keyword.kwlist) + r")\b",  
        ]) +
        r"))"
    )
    builtinlist = [str(name) for name in dir(builtins)
                   if not name.startswith('_') and
                   name not in keyword.kwlist]
    builtin = r"([^.'\"\\#]\b|^)" + any("BUILTIN", builtinlist) + r"\b"
    comment = any("COMMENT", [r"#[^\n]*"])
    stringprefix = r"(?i:r|u|f|fr|rf|b|br|rb)?"
    sqstring = stringprefix + r"'[^'\\\n]*(\\.[^'\\\n]*)*'?"
    dqstring = stringprefix + r'"[^"\\\n]*(\\.[^"\\\n]*)*"?'
    sq3string = stringprefix + r"'''[^'\\]*((\\.|'(?!''))[^'\\]*)*(''')?"
    dq3string = stringprefix + r'"""[^"\\]*((\\.|"(?!""))[^"\\]*)*(""")?'
    string = any("STRING", [sq3string, dq3string, sqstring, dqstring])
    return re.compile("|".join([
        builtin, comment, string, kw,
        match_softkw, case_default,
        case_softkw_and_pattern,
        any("SYNC", [r"\n"]),
    ]), re.DOTALL | re.MULTILINE)

def matched_named_groups(re_match):
    """Get only the non-empty named groups from an re.Match object."""
    return ((k, v) for (k, v) in re_match.groupdict().items() if v)

# 定义tag映射
prog_group_name_to_tag = {
    "MATCH_SOFTKW": "KEYWORD",
    "CASE_SOFTKW": "KEYWORD",
    "CASE_DEFAULT_UNDERSCORE": "KEYWORD",
    "CASE_SOFTKW2": "KEYWORD",
}

class PythonHighlighter(SyntaxHighlighter):
    """Python syntax highlighter based on IDLE's colorizer.
    
    This implementation is adapted from Python IDLE's colorizer.py
    Licensed under the Python Software Foundation License Version 2.
    Original source: https://github.com/python/cpython/blob/main/Lib/idlelib/colorizer.py
    """
    def __init__(self, light=True, parent=None):
        super().__init__(parent)
        self.light = light
        
        # 基于IDLE的配色方案
        self.colors = {
            'COMMENT': "#DD0000",    # 红色注释
            'KEYWORD': "#FF7700",    # 橙色关键字
            'BUILTIN': "#900090",    # 紫色内置函数
            'STRING': "#00AA00",     # 绿色字符串
            'DEFINITION': "#0000FF", # 蓝色定义
            'SYNC': None,            # 同步标记(无颜色)
            'TODO': None,            # 待处理标记(无颜色)
            'ERROR': "#FF0000",      # 错误标记
            'hit': "#HHH"           # 搜索匹配(保持原样)
        }

        # 创建格式
        self.formats = {}
        for tag, color in self.colors.items():
            format = QTextCharFormat()
            if color:
                format.setForeground(QColor(color))
            self.formats[tag] = format

        # 编译正则表达式
        self.prog = make_pat()  # 使用IDLE的pattern生成函数
        self.idprog = re.compile(r"\s+(\w+)")

    def create_format(self, color):
        format = QTextCharFormat()
        format.setForeground(QColor(color))
        format.setFontWeight(QFont.Bold)
        return format

    def highlightBlock(self, text):
        # 清除之前的格式
        self.setFormat(0, len(text), QTextCharFormat())
        
        # 逐个匹配并应用格式
        for match in self.prog.finditer(text):
            for group_name, matched_text in matched_named_groups(match):
                start, end = match.span(group_name)
                # 使用IDLE的tag映射
                tag = prog_group_name_to_tag.get(group_name, group_name)
                if tag in self.formats:
                    self.setFormat(start, end - start, self.formats[tag])
                
                # 处理函数/类定义
                if matched_text in ("def", "class"):
                    if m1 := self.idprog.match(text, end):
                        start, end = m1.span(1)
                        self.setFormat(start, end - start, self.formats['DEFINITION'])

    def highlightMultilineComments(self, text):
        # 处理三引号字符串
        triple_quote_pattern = r'""".*?"""|\'\'\'.*?\'\'\''
        triple_quote_matches = re.finditer(triple_quote_pattern, text, re.DOTALL)
        for match in triple_quote_matches:
            start, end = match.span()
            self.setFormat(start, end - start, self.formats['STRING'])
        
        # 处理多行注释
        comment_start = QRegExp(r'(?<!\"|\'|\w)"""(?!\"|\')')
        comment_end = QRegExp(r'(?<!\"|\'|\w)"""(?!\"|\')')
        self.highlightMultiline(text, comment_start, comment_end, self.formats['COMMENT'])

        comment_start = QRegExp(r"(?<!\"|\'|\w)'''(?!\"|\')")
        comment_end = QRegExp(r"(?<!\"|\'|\w)'''(?!\"|\')")
        self.highlightMultiline(text, comment_start, comment_end, self.formats['COMMENT'])

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
        sidebar.addItem("调试设置")
        sidebar.addItem("关于设置")
        sidebar.currentRowChanged.connect(self.display)

        self.stack = QStackedWidget(self)
        self.stack.addWidget(self.interfacePage())
        self.stack.addWidget(self.fontPage())
        self.stack.addWidget(self.debugPage())
        # 传入版本信息
        self.stack.addWidget(AboutPage(
            current_version=parent.current_version,
            version_td=parent.version_td,
            version_gj=parent.version_gj,
            update_Date=parent.update_Date
        ))

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stack)

        self.setLayout(main_layout)

        # 应用样式
        self.applyStyle()

    def interfacePage(self):
        """创建界面设置页面"""
        page = QWidget()
        layout = QVBoxLayout(page)

        # 标题
        title_label = QLabel("| 界面设置", self)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px; 
                font-weight: bold;
                color: #333333;
            }
        """)
        layout.addWidget(title_label, alignment=Qt.AlignLeft | Qt.AlignTop)

        # 按钮布局
        button_layout = QGridLayout()
        button_layout.setSpacing(15)

        # 添加按钮
        self._add_interface_buttons(button_layout)

        layout.addLayout(button_layout)
        return page

    def _add_interface_buttons(self, layout):
        """添加界面设置按钮"""
        buttons = [
            ("设置背景颜色", self.parent().set_background, 0, 0),
            ("重置文本框背景图片", self.parent().reset_background_color, 0, 1),
            ("设置背景图", self.parent().setBackgroundImage, 1, 0),
            ("重置背景图", self.parent().reset_background, 1, 1),
            ("高亮显示设置", self.parent().total_setting, 2, 0),
            ("彩色设置背景", self.parent().color_bg, 2, 1),
            ("API背景", self.openApiDialog, 3, 0, 1, 2)
        ]
        
        for button in buttons:
            if len(button) == 4:
                name, callback, row, col = button
                layout.addWidget(self.createButton(name, callback), row, col)
            else:
                name, callback, row, col, rowspan, colspan = button
                layout.addWidget(self.createButton(name, callback), row, col, rowspan, colspan)

    def openApiDialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("API背景")
        dialog.setWindowIcon(QIcon('./Tsuki/assets/GUI/resources/settings.png'))
        # 设置更大的窗口尺寸
        dialog.setFixedSize(700, 600)  # 增加高度
        
        self._setup_api_dialog_ui(dialog)
        dialog.exec_()

    def _setup_api_dialog_ui(self, dialog):
        # 主布局
        layout = QVBoxLayout(dialog)
        layout.setSpacing(20)
        # 增加边距给更多空间
        layout.setContentsMargins(30, 30, 30, 30)

        # 添加状态标签
        self.status_label = QLabel()
        self.status_label.setStyleSheet("""
            QLabel {
                color: #666666;
                font-family: Microsoft YaHei;
                padding: 5px;
            }
        """)

        # API设置卡片
        api_card = ClutCard("API设置", "")
        api_content = QVBoxLayout()
        # 增加内容间距
        api_content.setSpacing(20)
        
        # API输入框组
        api_input_group = QVBoxLayout()
        api_input_group.setSpacing(12)  # 增加控件间距
        
        # API输入框
        self.api_input = QLineEdit()
        self.api_input.setPlaceholderText("输入API地址")
        self.api_input.setMinimumHeight(40)  # 增加输入框高度
        
        # JSON路径输入框
        self.json_input = QLineEdit()
        self.json_input.setPlaceholderText("输入JSON路径 (如: data.url)")
        self.json_input.setMinimumHeight(40)
        
        # 预设API下拉框
        self.preset_combo = QComboBox()
        self.preset_combo.addItems(["[预设]自定义", "[预设]樱花Random", "[预设]夏沫Random", "[预设]必应Bing每日UHD", "[预设]Bing Random"])
        self.preset_combo.setMinimumHeight(40)
        
        api_input_group.addWidget(self.api_input)
        api_input_group.addWidget(self.json_input)
        api_input_group.addWidget(self.preset_combo)
        
        api_content.addLayout(api_input_group)
        api_card.setContentLayout(api_content)
        layout.addWidget(api_card)

        # 自动化设置卡片
        auto_card = ClutCard("自动化设置[Auto|不可改变]", "")
        auto_content = QVBoxLayout()
        auto_content.setSpacing(20)
        
        # 自动更新设置
        update_group = QHBoxLayout()
        update_group.setSpacing(12)
        self.auto_update_check = QCheckBox("启用自动更新")
        self.update_interval = QSpinBox()
        self.update_interval.setRange(1, 24*60*60)
        self.update_interval.setValue(3600)
        self.update_interval.setSuffix(" 秒")
        self.update_interval.setMinimumHeight(40)
        self.update_interval.setEnabled(False)
        update_group.addWidget(self.auto_update_check)
        update_group.addWidget(self.update_interval)
        auto_content.addLayout(update_group)
        
        # 自动清理设置
        clean_group = QHBoxLayout()
        clean_group.setSpacing(12)
        self.auto_clean_check = QCheckBox("启用自动清理")
        self.clean_interval = QSpinBox()
        self.clean_interval.setRange(1, 7*24*60*60)
        self.clean_interval.setValue(86400)
        self.clean_interval.setSuffix(" 秒")
        self.clean_interval.setMinimumHeight(40)
        self.clean_interval.setEnabled(False)
        clean_group.addWidget(self.auto_clean_check)
        clean_group.addWidget(self.clean_interval)
        auto_content.addLayout(clean_group)
        
        # 清除缓存按钮
        clear_cache_btn = QPushButton("清除缓存")
        clear_cache_btn.setMinimumHeight(35)
        clear_cache_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(139, 92, 246, 0.15);
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background-color: rgba(139, 92, 246, 0.25);
            }
            QPushButton:pressed {
                background-color: rgba(139, 92, 246, 0.35);
            }
        """)
        clear_cache_btn.clicked.connect(self._clear_api_cache)
        auto_content.addWidget(clear_cache_btn)
        
        auto_card.setContentLayout(auto_content)
        layout.addWidget(auto_card)

        # 底部按钮组
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        download_btn = QPushButton("下载并设置")
        cancel_btn = QPushButton("取消")
        download_btn.setMinimumHeight(35)
        cancel_btn.setMinimumHeight(35)
        download_btn.setStyleSheet(clear_cache_btn.styleSheet())
        cancel_btn.setStyleSheet(clear_cache_btn.styleSheet())
        button_layout.addWidget(download_btn)
        button_layout.addWidget(cancel_btn)
        
        # 添加状态标签和按钮到布局
        layout.addWidget(self.status_label)
        layout.addLayout(button_layout)

        # 连接信号
        download_btn.clicked.connect(lambda: self._download_image(dialog, self.api_input, self.json_input, download_btn, self.status_label))
        cancel_btn.clicked.connect(dialog.reject)
        self.preset_combo.currentTextChanged.connect(self._on_preset_changed)

        # 设置窗口样式
        dialog.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
            }
        """)

    def _clear_api_cache(self):
        """手动清理缓存"""
        try:
            cache_dir = './tsuki/assets/app/api_temp'
            if os.path.exists(cache_dir):
                for file in os.listdir(cache_dir):
                    file_path = os.path.join(cache_dir, file)
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        logger.error(f"删除缓存文件失败 {file_path}: {str(e)}")
                ClutMessageBox.show_message(self, "成功", "缓存已清除")
                logger.info("API图片缓存已手动清除")
            else:
                ClutMessageBox.show_message(self, "提示", "缓存目录不存在")
        except Exception as e:
            ClutMessageBox.show_message(self, "错误", f"清除缓存失败: {str(e)}")
            logger.error(f"清除缓存失败: {str(e)}")

    def _load_and_apply_settings(self):
        """加载并应用设置"""
        try:
            config = configparser.ConfigParser()
            config.read('./tsuki/assets/app/cfg/background_api_get.ini')
            
            if 'API' in config:
                # 加载设置
                self.api_input.setText(config['API'].get('url', ''))
                self.json_input.setText(config['API'].get('json_path', ''))
                self.auto_update_check.setChecked(config['API'].getboolean('auto_update', False))
                self.update_interval.setValue(config['API'].getint('update_interval', 3600))
                self.auto_clean_check.setChecked(config['API'].getboolean('auto_clean', False))
                self.clean_interval.setValue(config['API'].getint('clean_interval', 86400))
                
                # 设置最后使用的图片
                last_image = config['API'].get('last_image', '')
                if last_image and os.path.exists(last_image):
                    self.parent().setBackgroundImageFromFile(last_image)
                
                # 启动定时器
                self._setup_timers()
                
                # 如果启用了自动更新，立即更新一次
                if self.auto_update_check.isChecked():
                    self._auto_update_background()
                    
        except Exception as e:
            logger.error(f"加载API设置失败: {str(e)}")

    def _setup_timers(self):
        """设置定时器"""
        # 自动更新定时器
        if self.auto_update_check.isChecked():
            interval = self.update_interval.value() * 1000  # 转换为毫秒
            self.update_timer.start(interval)
        else:
            self.update_timer.stop()
            
        # 自动清理定时器
        if self.auto_clean_check.isChecked():
            interval = self.clean_interval.value() * 1000  # 转换为毫秒
            self.clean_timer.start(interval)
        else:
            self.clean_timer.stop()

    def _auto_update_background(self):
        """自动更新背景"""
        try:
            api_url = self.api_input.text().strip()
            json_path = self.json_input.text().strip()
            if api_url:
                self._download_image(api_url, json_path)
        except Exception as e:
            logger.error(f"自动更新背景失败: {str(e)}")

    def _auto_clean_cache(self):
        """自动清理缓存"""
        try:
            cache_dir = './tsuki/assets/app/api_temp'
            if os.path.exists(cache_dir):
                current_time = time.time()
                for file in os.listdir(cache_dir):
                    file_path = os.path.join(cache_dir, file)
                    # 保留最后使用的图片
                    if file_path != self._get_last_image_path():
                        try:
                            file_time = os.path.getmtime(file_path)
                            if (current_time - file_time) > self.clean_interval.value():
                                os.remove(file_path)
                        except Exception as e:
                            logger.error(f"删除缓存文件失败 {file_path}: {str(e)}")
                logger.info("API图片缓存已自动清理")
        except Exception as e:
            logger.error(f"自动清理缓存失败: {str(e)}")

    def _get_last_image_path(self):
        """获取最后使用的图片路径"""
        try:
            config = configparser.ConfigParser()
            config.read('./tsuki/assets/app/cfg/background_api_get.ini')
            return config['API'].get('last_image', '')
        except:
            return ''

    def _create_api_input_group(self):
        api_group = QGroupBox("API设置")
        api_layout = QVBoxLayout()
        api_layout.setSpacing(15)
        
        api_input = QLineEdit()
        api_input.setPlaceholderText("输入API URL (必填)")
        api_input.setMinimumHeight(35)
        
        json_input = QLineEdit()
        json_input.setPlaceholderText("输入JSON路径 (选填，如: data.url)")
        json_input.setMinimumHeight(35)
        
        api_layout.addWidget(api_input)
        api_layout.addWidget(json_input)
        api_group.setLayout(api_layout)
        
        return api_group, api_input, json_input

    def _create_preset_group(self):
        preset_group = QGroupBox("预设API")
        preset_layout = QHBoxLayout()
        
        preset_combo = QComboBox()
        preset_combo.setMinimumHeight(35)
        preset_combo.addItems([
            "自定义",
            "樱花Random",
            "夏沫Random", 
            "必应Bing每日UHD",
            "Bing Random"
        ])
        
        # 连接信号槽
        preset_combo.currentIndexChanged.connect(self._on_preset_changed)
        
        preset_layout.addWidget(preset_combo)
        preset_group.setLayout(preset_layout)
        return preset_group, preset_combo

    def _create_dialog_buttons(self):
        """创建对话框按钮"""
        download_btn = QPushButton("下载并设置")
        download_btn.setMinimumHeight(35)
        download_btn.setMinimumWidth(120)
        
        cancel_btn = QPushButton("取消")
        cancel_btn.setMinimumHeight(35)
        cancel_btn.setMinimumWidth(120)
        
        return download_btn, cancel_btn

    def _create_status_label(self):
        """创建状态标签"""
        status_label = QLabel()
        status_label.setStyleSheet("color: #666666; font-family: Microsoft YaHei;")
        return status_label

    def _setup_api_dialog_events(self, dialog, preset_combo, api_input, json_input,
                               download_btn, cancel_btn, status_label):
        """设置API对话框事件"""
        # 预设API选择事件
        preset_combo.currentIndexChanged.connect(
            lambda index: self._on_preset_changed(index, api_input, json_input)
        )
        
        # 下载按钮事件
        download_btn.clicked.connect(
            lambda: self._download_image(dialog, api_input, json_input, download_btn, status_label)
        )
        
        # 取消按钮事件
        cancel_btn.clicked.connect(dialog.reject)

    def _on_preset_changed(self, index):
        """处理预设API选择变更"""
        presets = {
            "[预设]樱花Random": {
                "url": "https://www.dmoe.cc/random.php?return=json",
                "path": "imgurl"
            },
            "[预设]夏沫Random": {
                "url": "https://cdn.seovx.com/d/?mom=302", 
                "path": ""
            },
            "[预设]必应Bing每日UHD": {
                "url": "https://bing.img.run/uhd.php",
                "path": ""
            },
            "[预设]Bing Random": {
                "url": "https://bing.img.run/rand.php",
                "path": ""
            }
        }
        
        selected = self.preset_combo.currentText()
        if selected in presets:
            preset = presets[selected]
            self.api_input.setText(preset["url"])
            self.json_input.setText(preset["path"])

    def _download_image(self, dialog, api_input, json_input, download_btn, status_label):
        """下载并设置背景图片"""
        api_url = api_input.text().strip()
        json_path = json_input.text().strip()
        
        if not api_url:
            status_label.setText("请输入API地址")
            return
            
        status_label.setText("正在下载...")
        download_btn.setEnabled(False)
        
        try:
            # 创建api_temp目录
            temp_dir = './tsuki/assets/app/api_temp'
            os.makedirs(temp_dir, exist_ok=True)
            
            # 获取图片
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            response = requests.get(api_url, timeout=10, verify=False)
            response.raise_for_status()
            
            if json_path:
                data = response.json()
                image_url = data
                for key in json_path.split('.'):
                    image_url = image_url[key]
                if not image_url.startswith('http'):
                    image_url = 'https://www.bing.com' + image_url
            else:
                image_url = api_url if 'image' in response.headers.get('Content-Type', '') else response.url
            
            # 下载图片
            img_response = requests.get(image_url, timeout=10, verify=False)
            img_response.raise_for_status()
            
            # 获取原始格式并保存
            content_type = img_response.headers.get('Content-Type', '')
            ext = content_type.split('/')[-1] if '/' in content_type else 'jpg'
            save_path = os.path.join(temp_dir, f'api_image_{int(time.time())}.{ext}')
            
            with open(save_path, 'wb') as f:
                f.write(img_response.content)
            
            # 尝试设置背景
            try:
                self.parent().setBackgroundImageFromFile(save_path)
                self.parent().text_edit.setStyleSheet(f"background-image: url({save_path});")
            except Exception:
                # 转换格式重试
                from PIL import Image
                img = Image.open(save_path)
                converted_path = os.path.join(temp_dir, f'api_image_{int(time.time())}.png')
                img.save(converted_path, 'PNG')
                self.parent().setBackgroundImageFromFile(converted_path)
                self.parent().text_edit.setStyleSheet(f"background-image: url({converted_path});")
                save_path = converted_path
            
            # 保存配置
            config = configparser.ConfigParser()
            config['API'] = {
                'url': api_url,
                'json_path': json_path,
                'last_image': save_path,
                'auto_update': 'false',
                'update_interval': '3600',
                'auto_clean': 'false', 
                'clean_interval': '86400'
            }
            
            config_dir = './tsuki/assets/app/cfg'
            os.makedirs(config_dir, exist_ok=True)
            with open(os.path.join(config_dir, 'background_api_get.ini'), 'w') as f:
                config.write(f)
            
            dialog.accept()
            ClutMessageBox.show_message(dialog, "成功", 
                                  f"图片已下载并设置为背景\n保存路径: {save_path}")
            logger.info(f"API image downloaded and set as background: {save_path}")
            
        except Exception as e:
            status_label.setText(f"下载失败: {str(e)}")
            logger.error(f"[Log/ERROR]API image download failed: {str(e)}")
        finally:
            download_btn.setEnabled(True)

        # 添加自动更新设置
        auto_update_check = QCheckBox("启用自动更新")
        update_interval = QSpinBox()
        update_interval.setRange(1, 24*60*60)
        update_interval.setValue(3600)
        update_interval.setSuffix(" 秒")
        update_interval.setEnabled(False)
        
        auto_update_check.stateChanged.connect(update_interval.setEnabled)
        
        # 添加自动清理设置  
        auto_clean_check = QCheckBox("启用自动清理")
        clean_interval = QSpinBox()
        clean_interval.setRange(1, 7*24*60*60)
        clean_interval.setValue(86400)
        clean_interval.setSuffix(" 秒")
        clean_interval.setEnabled(False)
        
        auto_clean_check.stateChanged.connect(clean_interval.setEnabled)
        
        # 添加到布局
        settings_layout = QGridLayout()
        settings_layout.addWidget(auto_update_check, 0, 0)
        settings_layout.addWidget(update_interval, 0, 1)
        settings_layout.addWidget(auto_clean_check, 1, 0)
        settings_layout.addWidget(clean_interval, 1, 1)
        
        # 保存设置
        def save_settings():
            config = configparser.ConfigParser()
            config['API'] = {
                'url': api_input.text(),
                'json_path': json_input.text(),
                'auto_update': str(auto_update_check.isChecked()).lower(),
                'update_interval': str(update_interval.value()),
                'auto_clean': str(auto_clean_check.isChecked()).lower(),
                'clean_interval': str(clean_interval.value())
            }
            
            with open('./tsuki/assets/app/cfg/background_api_get.ini', 'w') as f:
                config.write(f)
        
        # 加载设置
        def load_settings():
            try:
                config = configparser.ConfigParser()
                config.read('./tsuki/assets/app/cfg/background_api_get.ini')
                if 'API' in config:
                    api_input.setText(config['API'].get('url', ''))
                    json_input.setText(config['API'].get('json_path', ''))
                    auto_update_check.setChecked(config['API'].getboolean('auto_update', False))
                    update_interval.setValue(config['API'].getint('update_interval', 3600))
                    auto_clean_check.setChecked(config['API'].getboolean('auto_clean', False))
                    clean_interval.setValue(config['API'].getint('clean_interval', 86400))
            except Exception as e:
                logger.error(f"[Log/ERROR]Failed to load API settings: {str(e)}")
        
        # 连接信号
        download_btn.clicked.connect(lambda: (self._download_image(dialog, api_input, json_input, download_btn, status_label), save_settings()))
        dialog.finished.connect(save_settings)
        
        # 初始加载设置
        load_settings()

    def _apply_api_dialog_style(self, dialog):
        dialog.setStyleSheet("""
            * {
                font-family: "Microsoft YaHei";
            }
            QDialog {
                background-color: #ffffff;
            }
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 12px;
                padding: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
                background-color: #ffffff;
            }
            QPushButton {
                font-size: 14px;
                padding: 8px 20px;
                border-radius: 5px;
                background-color: #4a90e2;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
            QLineEdit {
                font-size: 14px;
                padding: 8px;
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #4a90e2;
            }
            QComboBox {
                font-size: 14px;
                padding: 8px;
                padding-right: 20px; /* 为下拉箭头留出空间 */
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                background-color: white;
            }
            QComboBox:hover {
                border-color: #4a90e2;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: url(./tsuki/assets/GUI/resources/open_list.png); /* 添加自定义箭头图标 */
                width: 12px;
                height: 12px;
            }
            QComboBox::down-arrow:on { /* 点击时的样式 */
                top: 1px;
            }
            QLabel {
                font-size: 14px;
            }
        """)
    def fontPage(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        title_label = QLabel("| 字体设置", self)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px; 
                font-weight: bold;
                color: #333333;
                font-family: "Microsoft YaHei";
            }
        """)
        layout.addWidget(title_label, alignment=Qt.AlignLeft | Qt.AlignTop)

        button_layout = QGridLayout()
        button_layout.setSpacing(15)

        button_layout.addWidget(self.createButton("设置字体大小", self.parent().set_font_size), 0, 0)
        button_layout.addWidget(self.createButton("初始化字体大小", self.parent().initialize_font_size), 0, 1)

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
        button_layout.addWidget(self.createButton("快速Crash按钮[测试用警告]",self.parent().crash_app),0, 2)

        layout.addLayout(button_layout)
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
        ClutMessageBox.show_message(self, "语言更改", f"语言已更改为: {language_code}")

class AboutPage(QWidget):
    def __init__(self, current_version=None, version_td=None, version_gj=None, update_Date=None):
        super().__init__()
        self.current_version = current_version or "未知"
        self.version_td = version_td or "未知"
        self.version_gj = version_gj or "未知" 
        self.update_Date = update_Date or "未知"
        self.setup_ui()
        self.notifications_shown = False

    def showEvent(self, event):
        super().showEvent(event)
        if not self.notifications_shown:
            QTimer.singleShot(100, self._show_about_notifications)
            self.notifications_shown = True

    def _show_about_notifications(self):
        # 修改前: from .tsuki.utils.notification_manager import NotificationManager
        from tsuki.utils.notification_manager import NotificationManager
        notification = NotificationManager()
        
        notification.show_message(
            title="关于TsukiNotes",
            msg="在 GitHub 上查看 TsukiNotes 的项目主页",
            duration=3000
        )
        notification.show_message(
            title="开源许可证", 
            msg="本项目遵循 GPLv3.0 许可证供非商业使用",
            duration=3000
        )
        notification.show_message(
            title="版权声明",
            msg="TsukiNotes 版权所有 © 2024 by ZZBuAoYe",
            duration=3000
        )

    def setup_ui(self):
        # 创建主布局
        from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QListWidget, 
                           QStackedWidget, QPushButton, QLabel, QGridLayout, 
                           QWidget, QScrollArea)  # 添加 QScrollArea
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # 设置窗口默认大小
        self.resize(940, 544)

        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # 设置滚动条样式
        scroll_area.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: rgba(255, 255, 255, 0.1);
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.3);
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar:horizontal {
                background: rgba(255, 255, 255, 0.1);
                height: 8px;
                margin: 0px;
            }
            QScrollBar::handle:horizontal {
                background: rgba(255, 255, 255, 0.3);
                min-width: 20px;
                border-radius: 4px;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
        """)

        # 创建内容容器
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        
        # 添加原有内容到content_layout
        title = QLabel("| 关于")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: black;
            }
        """)
        content_layout.addWidget(title)

        # Logo 部分使用 ClutImageCard
        logo_card = ClutImageCard(
            title="TsukiNotes",
            msg=" |基于 PyQt5 的记事本软件 \n |一部分基于ClutUI的UI框架 \n |Powered By ZZBuAoYe",
            image_url="./tsuki/assets/GUI/resources/GUI/logo.png",
            image_mode=1,
            image_align="center"
        )
        content_layout.addWidget(logo_card)

        # 版本信息卡片
        version_card = ClutCard(
            title="版本信息",
            msg=f"""Version: {self.current_version}
版本通道: {self.version_td}
内部版本号: {self.version_gj}
更新日期: {self.update_Date}"""
        )

        content_layout.addWidget(version_card)

        # 功能介绍卡片
        features_card = ClutCard(
            title="功能特性",
            msg="""TsukiNotes 是一款功能强大的记事本软件，现已支持:
            
• 支持文本高亮显示
• 可打开16进制文件  
• 支持Python、C++、Java和Markdown语法高亮
• 基于Qt内核，提供优秀的图形界面
• 丰富的QSS样式，带来美观的视觉体验
• 强大的搜索功能
• 超越Windows记事本的使用体验
• 支持多标签页,更高的效率
• 新的设计，新的思路，新的体验

探索更多精彩功能！无限可能！"""
        )
        content_layout.addWidget(features_card)

        # 版权信息卡片
        copyright_card = ClutCard(
            title="版权声明",
            msg="© TsukiNotes 2022-2024 ZZBuAoYe. All rights reserved.\n | GPL-3.0 License \n | Powered By ZZBuAoYe | PyQt-ClutUI"
        )
        content_layout.addWidget(copyright_card)

        # 设置滚动区域的内容
        scroll_area.setWidget(content_widget)
        
        # 添加滚动区域到主布局
        main_layout.addWidget(scroll_area)

    def open_url(self, url, event):
        if event.button() == Qt.LeftButton:
            webbrowser.open(url)
            self.notification_manager.show_message(
                title="正在跳转",
                msg="正在打开外部链接..."
            )

from PyQt5.QtGui import QTextCursor

# 搜索的class
class SearchResultDialog(QDialog):
    def __init__(self, results, parent=None):
        super(SearchResultDialog, self).__init__(parent)
        self.setWindowTitle('搜索结果')
        logging.info(" 搜索成功")
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
            ClutMessageBox.show_message(self, "样式加载错误", f"加载搜索结果对话框样式失败: {e}")

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
        app = QApplication.instance()
        font = QFont("Microsoft YaHei")
        font.setPointSize(10)
        self.settings = QSettings('TsukiNotes', 'Editor')
        app.setFont(font)
        QMetaType.type("QTextCursor")
        self.before = ''
        with open('VERSION', 'r') as version_file:
            self.current_version = version_file.read().strip()
        self.real_version = '1.6.2'
        self.update_Date = '2024/12/15'
        self.version_td = 'Release'
        self.version_gj = 'b-v162B-241215R'
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
        self.add_tab_button.setIcon(QIcon('./tsuki/assets/GUI/resources/tips.png'))
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
                    # 断开之前的连接（如果有的���）
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
                self.statusBar().showMessage(f'TsukiOF❌: 文件 [{file_path}] 打开失败！Error: [文件不存在]')
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
            self.statusBar().showMessage(f'TsukiFS❌: 字体大小��置失败！详见MessageBox！')
            logger.error(f"[Log/ERROR]ERROR Set Font Size: {str(e)}")

    def save_font_size_to_cfg(self, font_size):
        config = configparser.ConfigParser()
        config['Settings'] = {'font_size': str(font_size)}
        
        # 确保目录存在
        cfg_dir = 'tsuki/assets/app/cfg/font'
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

        self.saveAct = QAction(QIcon('./tsuki/assets/GUI/resources/save_file.png'), self.tr('直接保存修改（Ctrl+S）'), self)
        self.saveAct.triggered.connect(self.saveFile)

        self.saveAsAct = QAction(QIcon('./tsuki/assets/GUI/resources/save_file.png'), self.tr('另存为（Ctrl+Shift+S）'), self)
        self.saveAsAct.triggered.connect(self.saveAs)  # 改为 saveAs

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

        #self.pingServerManuallyAct = QAction(QIcon('./tsuki/assets/GUI/resources/server_ping.png'), self.tr('手动Ping服务器'), self)
        #self.pingServerManuallyAct.triggered.connect(self.pingServerManually)

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
        runButton.setIcon(QIcon('./tsuki/assets/GUI/resources/start.png'))
        runButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
        runButton.setStyleSheet("QToolButton { border: none; padding: 2px; }")
        runButton.clicked.connect(self.runcode) 

        runMenu = QMenu()
        
        self.runcodeAction = QAction(self.tr('Run Code'), self)
        self.runcodeAction.setIcon(QIcon('./tsuki/assets/GUI/resources/start.png'))
        self.runcodeAction.setShortcut('F5')
        self.runcodeAction.triggered.connect(self.runcode)
        runMenu.addAction(self.runcodeAction)
        
        self.runcode_debugAction = QAction(self.tr('Debug Run Code'), self)
        self.runcode_debugAction.setIcon(QIcon('./tsuki/assets/GUI/resources/debug.png'))
        self.runcode_debugAction.setShortcut('F6')
        self.runcode_debugAction.triggered.connect(self.runcode_debug)
        runMenu.addAction(self.runcode_debugAction)

        # 下拉箭头
        arrowButton = QToolButton(self)
        arrowButton.setIcon(QIcon('./tsuki/assets/GUI/resources/open_list.png'))
        arrowButton.setStyleSheet("QToolButton { border: none; padding: 2px; }")
        arrowButton.clicked.connect(lambda: runMenu.exec_(arrowButton.mapToGlobal(QPoint(0, arrowButton.height()))))

        # buju
        buttonLayout = QHBoxLayout()
        buttonLayout.setSpacing(0) 
        buttonLayout.setContentsMargins(0, 0, 0, 0)
        # 设置
        settingsButton = QToolButton(self)
        settingsButton.setIcon(QIcon('./tsuki/assets/GUI/resources/settings.png'))
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

                # 文本编辑器的原有逻辑
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
                            '编码: {3} | 光标位置: 行{4} 列{5} ]').format(
                                line_count, max_column_count, char_count, 
                                encoding, cursor_line, cursor_column))
                self.status_label.setText(status_text)
                self.status_label.setFont(QFont(self.tr("微软雅黑")))
                
            except Exception as e:
                logger.error(self.tr(f"状态栏更新时发生错误: {str(e)}"))
        else:
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
                    self.tr(f' TsukiFont <img src="./tsuki/assets/GUI/resources/done.png" width="16" height="16">: {font_name} 字体已经成功应用！'))
                logging.info(self.tr(f"Change Font: {font_name}"))
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
            logger.info(self.tr("SAVE"))

        cfg_path = os.path.join(cfg_dir, 'tn_font_family.ini')
        with open(cfg_path, 'w') as configfile:
            config.write(configfile)
            logging.info(self.tr(f"[INFO]SAVE {cfg_path}"))
            logger.info(self.tr(f"SAVE {cfg_path}"))

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
                    encoding = self.detectFileEncoding(fileName)
                    self.current_encoding = encoding

                    # 检查文件是否已经打开
                    for index in range(self.tabWidget.count()):
                        if self.tabWidget.tabText(index) == os.path.basename(fileName):
                            self.tabWidget.setCurrentIndex(index)
                            text_edit = self.tabWidget.widget(index)
                            with open(fileName, 'r', encoding=encoding) as file:
                                text_edit.setPlainText(file.read())
                            return

                    # 创建新标签页
                    text_edit = QPlainTextEdit()
                    self.setFont(text_edit)
                    self.load_background_settings(text_edit)
                    
                    # 设置图标
                    icon_map = self.getIconMap()
                    if file_extension in icon_map:
                        icon = QIcon(icon_map[file_extension])
                    else:
                        icon = QIcon('./tsuki/assets/GUI/resources/default_file.png')
                    
                    self.tabWidget.addTab(text_edit, icon, os.path.basename(fileName))
                    
                    # 加载文件内容
                    with open(fileName, 'r', encoding=encoding) as file:
                        text_edit.setPlainText(file.read())
                    
                    self.tabWidget.setCurrentWidget(text_edit)
                    text_edit.textChanged.connect(self.updateStatusLabel)
                    
                    # 设置语法高亮
                    self.setHighlighter(text_edit, fileName)
                    
                    self.updateWindowTitle(fileName)
                    self.statusBar().showMessage(self.tr(f'TsukiOpen✔: 文件 [{fileName}] 已成功打开！'))
                    logger.info(self.tr(f"Open Text File Succeed: {fileName}"))

                except UnicodeDecodeError as e:
                    self.handleError(self.tr('Open File'), fileName, 
                                self.tr(f"编码错误: {e}，尝试用其他编码打开文件。"))
                except Exception as e:
                    self.handleError(self.tr('Open File'), fileName, e)

            except Exception as e:
                self.handleError(self.tr('Open File'), fileName, e)
                logger.error(self.tr(f"[Log/ERROR]Failed to open file: {fileName}, Error: {str(e)}"))

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
                '.png': './tsuki/assets/GUI/resources/language/image.png',
                '.jpg': 'image.png', 
                '.jpeg': 'image.png',
                '.gif': 'gif.png',
                '.bmp': 'bmp.png',
                '.ico': 'ico.png',
                '.svg': 'svg.png',
                '.webp': 'webp.png'
            }
            
            if file_ext in image_extensions:
                icon_path = f'./tsuki/assets/GUI/resources/language/{image_extensions[file_ext]}'
            else:
                # 默认使用exe图标
                icon_path = './tsuki/assets/GUI/resources/language/exe.png'
                
            if os.path.exists(icon_path):
                self.tabWidget.setTabIcon(index, QIcon(icon_path))
                
            # 启动加载线程
            loader.start()
            
            # 更新状态栏
            self.statusBar().showMessage(self.tr(f'正在加载文件: {fileName}'))
            
        except Exception as e:
            self.handleError(self.tr('打开十六进制文件'), fileName, e)

    def createNewTab(self, fileName, encoding):
        tab_name = os.path.basename(fileName)
        file_extension = os.path.splitext(fileName)[1].lower()
        
        # 检查是否为图片文件
        if file_extension in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg']:
            # 创建图片查看器
            image_viewer = QLabel()
            image_viewer.setAlignment(Qt.AlignCenter)
            
            if file_extension == '.svg':
                # SVG处理
                renderer = QSvgRenderer(fileName)
                from PyQt5.QtGui import QImage
                image = QImage(800, 600, QImage.Format_ARGB32)
                image.fill(0) # 透明背景
                painter = QPainter(image)
                renderer.render(painter)
                painter.end()
                pixmap = QPixmap.fromImage(image)
            else:
                # 其他图片格式处理
                pixmap = QPixmap(fileName)
            
            # 自适应缩放
            scaled_pixmap = pixmap.scaled(800, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_viewer.setPixmap(scaled_pixmap)
            
            # 添加到标签页
            icon = self.getFileIcon(fileName)
            self.tabWidget.addTab(image_viewer, icon, tab_name)
            self.tabWidget.setCurrentWidget(image_viewer)
            return
        
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
        config_file_path = './tsuki/assets/app/cfg/update/update.cfg'
        
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
                ClutMessageBox.show_message(self, self.tr('Save Error'), self.tr(f'无法保存文件：{str(e)}'))
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
            ClutMessageBox.show_message(self, self.tr('Warning'), self.tr('请运行[.md][.markdown]后缀的文件\n暂不支持预览其他格式文件\n'))

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
        config_path = self.get_app_path('assets/app/cfg/background/background_color.ini')
        
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
        dialog.resize(300, 200)

        # 加载QSS文件
        qss_file_path = './tsuki/assets/theme/New_File_Dialog.qss'
        try:
            with open(qss_file_path, 'r', encoding='utf-8') as file:
                qss = file.read()
                dialog.setStyleSheet(qss)
        except Exception as e:
            self.statusBar().showMessage(self.tr(f'应用QSS样式失败: {e}'))
            logger.error(self.tr(f"[Log/ERROR]Failed to load QSS: {e}"))
        
        layout = QVBoxLayout(dialog)
        
        # 创建标准字体
        label_font = QFont(self.tr("Microsoft YaHei"), 10)
        
        # 文件名标签和输入框
        name_label = QLabel(self.tr("文件名:"))
        name_label.setFont(label_font)
        name_input = QLineEdit("")
        name_input.setFont(label_font)
        layout.addWidget(name_label)
        layout.addWidget(name_input)
        
        # 文件类型标签和下拉框
        type_label = QLabel(self.tr("文件类型:"))
        type_label.setFont(label_font)
        type_combo = QComboBox()
        type_combo.setFont(label_font)
        icon_map = self.getIconMap()
        type_combo.addItem(self.tr('[自定][读取你输入的文件名里面的后缀]'))
        type_combo.addItems(list(icon_map.keys()))
        layout.addWidget(type_label)
        layout.addWidget(type_combo)
        
        # 编码标签和下��框
        encoding_label = QLabel(self.tr("编码:"))
        encoding_label.setFont(label_font)
        encoding_combo = QComboBox()
        encoding_combo.setFont(label_font)
        encoding_combo.addItems(["UTF-8", "GBK", "ASCII", "ISO-8859-1"])
        layout.addWidget(encoding_label)
        layout.addWidget(encoding_combo)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        button_font = QFont(self.tr("Microsoft YaHei"), 10)
        
        ok_button = QPushButton(self.tr("确定"))
        ok_button.setFont(button_font)
        quit_button = QPushButton(self.tr("退出"))
        quit_button.setFont(button_font)
        
        button_layout.addWidget(ok_button)
        button_layout.addWidget(quit_button)
        layout.addLayout(button_layout)
        
        def handle_quit():
            dialog.done(QDialog.Rejected)  # 使用Rejected而不是close
            
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
            if dialog.result() == 0:  # quit_button
                logger.info(self.tr("File creation cancelled by user"))
                return None, None
        
        return None, None 

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
                button.setIcon(QIcon('./tsuki/assets/GUI/resources/nav/back.png'))
            elif button.accessibleName() == "Forward":
                button.setIcon(QIcon('./tsuki/assets/GUI/resources/nav/forward.png'))
            elif button.accessibleName() == "Parent Directory":
                button.setIcon(QIcon('./tsuki/assets/GUI/resources/nav/up.png'))
            elif button.accessibleName() == "Create New Folder":
                button.setIcon(QIcon('./tsuki/assets/GUI/resources/nav/new_folder.png'))
                button.setIconSize(QSize(16, 16))
            elif button.accessibleName() == "List View":
                button.setIcon(QIcon('./tsuki/assets/GUI/resources/nav/list_view.png'))
                button.setIconSize(QSize(16, 16))
            elif button.accessibleName() == "Detail View":
                button.setIcon(QIcon('./tsuki/assets/GUI/resources/nav/detail_view.png'))
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
        encodings = ['UTF-8', 'GBK', 'GB2312', 'GB18030', 'ASCII', 'ISO-8859-1']
        encoding_combo.addItems(encodings)
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
            file_path = dialog.selectedFiles()[0]
            encoding = encoding_combo.currentText()
            
            try:
                # 保存文件
                text = current_tab.toPlainText()
                with open(file_path, 'w', encoding=encoding) as file:
                    file.write(text)
                
                # 更新UI状态
                current_tab.file_path = file_path
                self.updateTabIcon(self.tabWidget.currentIndex())
                self.tabWidget.setTabText(self.tabWidget.currentIndex(), os.path.basename(file_path))
                
                self.statusBar().showMessage(
                    self.tr(f'✔ 文件已另存为: {os.path.basename(file_path)} [{encoding}]'), 
                    3000
                )
                logger.info(self.tr(f"文件已另存为: {file_path} (编码: {encoding})"))
                
                if hasattr(current_tab, 'document'):
                    current_tab.document().setModified(False)
                    
            except Exception as e:
                error_msg = self.tr(f"另存为失败: {str(e)}")
                ClutMessageBox.show_message(self, self.tr('保存错误'), error_msg)
                logger.error(self.tr(f"[Log/ERROR]另存为失败: {str(e)}"))
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
                    <img src='./tsuki/assets/GUI/resources/GUI/logo.png' width='64' height='64' style='border-radius: 50%; box-shadow: 0 4px 8px rgba(0,0,0,0.15);'>
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
            "<h2 style='color: #ffffff; font-family: \"Microsoft YaHei\", sans-serif; text-align: left; margin-bottom: 20px;'>" + self.tr("| TsukiNotes 在线更新信息🌐") + "</h2>"
            f"<p style='color: #cccccc; font-size: 16px; text-align: center; margin-bottom: 15px;'>" + self.tr("版本: {0} {1} [{2}]").format(version, version_td, update_time) + "</p>"
            "</html>"
            f"<hr style='border: 0; height: 1px; background: #555555; margin: 20px 0;'>"
            f"<div style='padding: 15px; border-radius: 5px; margin-bottom: 20px;'>{online_update_text}</div>"
            f"<hr style='border: 0; height: 1px; background: #555555; margin: 20px 0;'>"
            f"<p style='color: #aaaaaa; font-size: 14px; text-align: center;'>" + self.tr("[+代表细节优化 | *代表重要改动]") + "</p>"
            f"<p style='color: #ffffff; font-size: 18px; font-weight: bold; text-align: center; margin-top: 10px;'> || {version_td} ||</p>"
            f"<p style='color: #aaaaaa; font-size: 14px; text-align: center;'>" + self.tr("[内部版本号: {0}]").format(versiontime) + "</p>"
        )

        ClutMessageBox.show_message(
            parent=self,
            title=self.tr("TsukiNotes[{0}]在线更新日志 -Ver{1}{2}").format(version, version, version_td),
            text=update_text
        )

        self.statusBar().showMessage(self.tr('TsukiBack✔: 您查看了更新日志'))
        logger.info(self.tr("打开更新信息成功"))



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
            rename_action = QAction(QIcon('./tsuki/assets/GUI/resources/font_size_reset_tab.png'), self.tr('重命名标签'), self)
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
            # 配置文件路径
            default_image_path = './tsuki/assets/app/default/default_light.png'
            config_path = 'tsuki/assets/app/cfg/background/background_color.ini'
            
            # 读取配置
            config = configparser.ConfigParser()
            config.read(config_path, encoding='utf-8')
            image_path = config.get('Background', 'image_path', fallback=default_image_path)
            
            # 如果图片不存在，使用默认图片
            if not os.path.exists(image_path):
                image_path = default_image_path
                
            # 获取目标widget
            target_widget = widget if widget else self.tabWidget.currentWidget()
            if not target_widget:
                return
                
            # 设置背景图片
            pixmap = QPixmap(image_path)
            palette = QPalette()
            palette.setColor(QPalette.Base, QColor("white"))
            palette.setColor(QPalette.Text, QColor("black"))
            palette.setBrush(QPalette.Base, QBrush(pixmap))
            target_widget.setPalette(palette)
            
            # 记录设置
            message = self.tr(f'成功加载背景图片：{image_path}')
            self.statusBar().showMessage(self.tr(f'TsukiBC✔: {message}'))
            logger.info(self.tr(f" {message}"))
            
            # 保存配置
            config['Background'] = {'image_path': image_path}
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, 'w', encoding='utf-8') as configfile:
                config.write(configfile)
                
        except Exception as e:
            self.statusBar().showMessage(self.tr(f'TsukiBC❌: 背景加载失败'))
            logger.error(self.tr(f"Background load error: {str(e)}"))

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
            logger.info(self.tr(f" {message}"))

            config['Background'] = {'image_path': image_path}
            with open(config_path, 'w') as configfile:
                config.write(configfile)

        except Exception as e:
            self.statusBar().showMessage(self.tr(f'TsukiBC❌: 未找到保存的背景色设置或加载失败。'))
            logger.error(self.tr(f"Background Color Load Error: {str(e)}"))

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
            self.config_path = "./tsuki/assets/app/cfg/background/TN_BackGround.ini"
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

    #def pingServerManually(self):
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

        ClutMessageBox.show_message(self, self.tr('PingServerManually | 失败原因报告'),
                            self.tr(f'我很抱歉您的检测失败了 \n 在此之前您需要知道的内容：\n | 检测时禁止使用VPN \n | 检测时可能会未响应，不必担心这是暂时的 \n 您的报错：{error_message} | Powered By MoonCN&TsukiNotes'))
        logger.error(self.tr(f"[Log/ERROR]PingServerManually | 失败原因报告:{error_message}"))
    def getColorStyle(self, delay):
        if delay > 150:
            return 'red'
        elif delay > 100:
            return 'yellow'
        else:
            return 'green'
        

    def get_app_path(self, relative_path=''):
        """
        获取应用程序路径，自动处理权限和目录创建
        
        Args:
            relative_path (str): 相对路径，例如 'assets/app/cfg/first'
            
        Returns:
            str: 完整的路��
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