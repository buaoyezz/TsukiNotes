from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QTextEdit, QWidget, QToolBar, 
                           QComboBox, QLabel, QLineEdit, QPushButton, QCheckBox,
                           QHBoxLayout, QFileDialog,QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QTimer, QRegExp, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import (QTextCharFormat, QColor, QFont, QIcon, QPalette)
import logging
from queue import Queue
from datetime import datetime

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
        self.setWindowIcon(QIcon("./tsuki/assets/resources/GUI/terminal.png"))
        
        self.auto_scroll = True # 自动滚动[default enable]
        
        # 主布局
        main_layout = QVBoxLayout()
        
        # 工具栏
        toolbar = QToolBar()
        toolbar.setStyleSheet("""
            QToolBar {
                spacing: 5px;
                background: #ECECEC;
                border-radius: 15px;
                padding: 10px;
            }
        """)
        
        # 添加日志级别过滤
        self.level_combo = QComboBox()
        self.level_combo.addItems(['ALL', 'DEBUG', 'INFO', 'WARNING', 'ERROR'])
        self.level_combo.currentTextChanged.connect(self.filter_logs)
        toolbar.addWidget(QLabel("📊"))  # 使用图表符号
        toolbar.addWidget(self.level_combo)
        
        # 添加搜索框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(self.tr("🔍 搜索日志..."))  # 使用放大镜符号
        self.search_input.textChanged.connect(self.search_logs)
        toolbar.addWidget(self.search_input)
        
        # 添加功能按钮
        export_btn = QPushButton("📥 导出")  # 添加文字说明
        export_btn.setToolTip(self.tr("导出日志"))
        export_btn.clicked.connect(self.export_logs)
        toolbar.addWidget(export_btn)
        
        clear_btn = QPushButton("🗑️ 清除")  # 添加文字说明
        clear_btn.setToolTip(self.tr("清除日志"))
        clear_btn.clicked.connect(self.clear_logs)
        toolbar.addWidget(clear_btn)
        
        # 自动滚动开关也添加文字
        self.scroll_check = QCheckBox("📜 自动滚动")  # 添加文字说明
        self.scroll_check.setToolTip(self.tr("自动滚动"))
        self.scroll_check.setChecked(True)
        self.scroll_check.stateChanged.connect(self.toggle_auto_scroll)
        toolbar.addWidget(self.scroll_check)
        
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
        font_layout.addWidget(QLabel("🔤"))  # 使用字母符号
        font_layout.addWidget(self.font_combo)
        main_layout.addLayout(font_layout)
        
        # 统计信息
        self.stats_label = QLabel(self.tr("📊 Lines: 0\nINFO: 0 | WARNING: 0 | ERROR: 0 | DEBUG: 0"))
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
        self.setStyleSheet("""
            QWidget {
                background-color: #E0E5EC;
                color: #333333;
            }
            QTextEdit, QLineEdit, QComboBox, QPushButton, QCheckBox {
                background-color: #E0E5EC;
                color: #333333;
                padding: 10px;
                border-radius: 15px;
                border: none;
            }
            QPushButton {
                min-width: 80px;
                min-height: 40px;
                font-size: 14px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #EDF0F5;
            }
            QPushButton:pressed {
                background-color: #D1D9E6;
                padding: 12px;
            }
            QLineEdit:focus, QTextEdit:focus {
                background-color: #EDF0F5;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
            }
        """)
        
        # 为所有控件添加双重阴影效果
        widgets = [self.log_text_edit, self.search_input, self.level_combo] + \
                 [w for w in self.findChildren(QPushButton)] + \
                 [self.scroll_check]
                 
        for widget in widgets:
            self.add_neumorphic_effect(widget)

    def add_neumorphic_effect(self, widget):
        """添加双重阴影效果"""
        # 亮色主题保持原有效果
        outer_shadow = QGraphicsDropShadowEffect()
        outer_shadow.setBlurRadius(15)
        outer_shadow.setXOffset(5)
        outer_shadow.setYOffset(5)
        outer_shadow.setColor(QColor(163, 177, 198, 160))
        
        # 创建动画
        self.shadow_animation = QPropertyAnimation(outer_shadow, b"blurRadius")
        self.shadow_animation.setDuration(200)
        self.shadow_animation.setStartValue(15)
        self.shadow_animation.setEndValue(20)
        self.shadow_animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        # 连接鼠标事件
        widget.enterEvent = lambda e: self.shadow_animation.start()
        widget.leaveEvent = lambda e: self.shadow_animation.start()
        
        widget.setGraphicsEffect(outer_shadow)

    def filter_logs(self):
        level = self.level_combo.currentText()
        self.log_text_edit.clear()
        filtered_logs = (log for log in self.original_logs if f' - {level} - ' in log) if level != 'ALL' else self.original_logs
        for log in filtered_logs:
            self.log_handler.format_and_append_log(log)
    
    def search_logs(self):
        search_text = self.search_input.text()
        self.filter_logs()
        
        if search_text:
            cursor = self.log_text_edit.textCursor()
            format = QTextCharFormat()
            format.setBackground(QColor("#FFE4B5"))  # 柔和的高亮色
            
            regex = QRegExp(search_text, Qt.CaseInsensitive)
            pos = 0
            while True:
                cursor = self.log_text_edit.document().find(regex, pos)
                if cursor.isNull():
                    break
                cursor.mergeCharFormat(format)
                pos = cursor.position()
    
    def export_logs(self):
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
        self.log_text_edit.clear()
        self.original_logs.clear()
        self.log_counters = {'INFO': 0, 'WARNING': 0, 'ERROR': 0, 'DEBUG': 0}
        self.update_statistics()
        self.search_input.clear()
        logger.info("Logs cleared")
    
    def toggle_auto_scroll(self, state):
        self.auto_scroll = state == Qt.Checked

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
        total_lines = self.log_text_edit.document().blockCount()
        stats_text = f"📊 Lines: {total_lines}\n"
        stats_text += f"ℹ️ INFO: {self.log_counters['INFO']} | "
        stats_text += f"⚠️ WARNING: {self.log_counters['WARNING']} | "
        stats_text += f"❌ ERROR: {self.log_counters['ERROR']} | "
        stats_text += f"🔧 DEBUG: {self.log_counters['DEBUG']}"
        
        self.stats_label.setText(self.tr(stats_text))