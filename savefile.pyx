# savefile.pyx
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QInputDialog
import os

def saveFile(self):
    current_tab_index = self.tabWidget.currentIndex()
    current_tab_widget = self.tabWidget.widget(current_tab_index)
    tab_text = self.tabWidget.tabText(current_tab_index)

    # Determine the file name
    if os.path.isfile(tab_text):
        file_name = tab_text
    else:
        file_name, _ = QFileDialog.getSaveFileName(
            self, 'TsukiNotes保存文件', '',
            'All Files (*);;Text Files (*.txt);;Markdown Files (*.md);;INI Files (*.ini);;XML Files (*.xml);;JSON Files (*.json);;Log Files (*.log);;Python Files (*.py);;C Files (*.c)'
        )

        if not file_name:
            return

        if not os.path.splitext(file_name)[1]:
            file_name += os.path.splitext(tab_text)[1]

        if file_name != tab_text:
            response = QMessageBox.question(
                self, '重命名',
                f'你确定想要将文件名称 ->> {file_name}? ✔',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )

            if response == QMessageBox.Yes:
                self.tabWidget.setTabText(current_tab_index, os.path.basename(file_name))

    # Save the file
    text_content = current_tab_widget.toPlainText()
    encoding, ok = QInputDialog.getItem(
        self, "选择编码", "编码类型🔰:",
        ["UTF-8", "ASCII", "ISO-8859-1"], 0, False
    )

    if not ok:
        return

    try:
        with open(file_name, 'w', encoding=encoding.lower(), errors='ignore') as file:
            file.write(text_content)
            self.statusBar().showMessage(f'TsukiSave: 文件 [{file_name}] 保存成功！')
            self.tabWidget.setTabText(current_tab_index, os.path.basename(file_name))
            self.tabWidget.setTabToolTip(current_tab_index, file_name)
            self.tabWidget.setCurrentIndex(current_tab_index)
    except Exception as e:
        QMessageBox.critical(self, 'Save File', f'An error occurred: {str(e)}')
        self.statusBar().showMessage(f'TsukiSave: 保存失败！原因:{str(e)}')
