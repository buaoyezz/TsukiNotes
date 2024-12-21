from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextBrowser
from PyQt5.QtGui import QFont, QTextCursor, QIcon
import logging
from tsuki.ui.utils.message_box import ClutMessageBox
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