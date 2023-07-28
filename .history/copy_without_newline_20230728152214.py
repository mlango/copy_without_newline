import sys, re
import pyperclip
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTextEdit, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 创建控件
        self.input_label = QLabel("请输入文本：")
        self.input_edit = QTextEdit()
        self.input_edit.setFixedHeight(150)  # 设置输入框高度
        self.output_label = QLabel("处理后的文本：")
        self.output_edit = QTextEdit()
        self.output_edit.setFixedHeight(150)  # 设置输出框高度
        self.output_edit.setReadOnly(True)  # 输出框设置为只读
        self.copy_button = QPushButton("复制")

        # 创建布局
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_label)
        input_layout.addWidget(self.input_edit)

        output_layout = QHBoxLayout()
        output_layout.addWidget(self.output_label)
        output_layout.addWidget(self.output_edit)

        button_layout = QHBoxLayout()
        button_layout.addStretch()  # 添加一个弹簧，使复制按钮靠右对齐
        button_layout.addWidget(self.copy_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addLayout(output_layout)
        main_layout.addLayout(button_layout)

        # 设置窗口布局
        self.setLayout(main_layout)

        # 设置窗口标题
        self.setWindowTitle("换行换为空格")

        # 设置窗口大小
        self.setFixedSize(700, 500)

        # 连接信号和槽
        self.input_edit.textChanged.connect(self.process_text)  # 当输入框的文本发生变化时，处理文本
        self.copy_button.clicked.connect(self.copy_output)  # 点击复制按钮时，复制输出框中的文本

        # 监视剪贴板变化
        clipboard = QApplication.clipboard()
        clipboard.dataChanged.connect(self.on_clipboard_data_changed)

    def process_text(self):
        text = self.input_edit.toPlainText()  # 获取输入框中的文本
        text = text.replace('\n', ' ')  # 将换行符替换为空格
        self.output_edit.setText(text)  # 将处理后的文本显示在输出框中
        self.copy_output()  # 复制输出框中的文本

    def copy_output(self):
        text = self.output_edit.toPlainText()  # 获取输出框中的文本
        pyperclip.copy(text)  # 将输出框中的文本复制到剪贴板中
        
    def on_clipboard_data_changed(self):
        QTimer.singleShot(2000, self.read_clipboard)  # 延迟 2 秒后再执行剪贴板读取操作

    def read_clipboard(self):
        clipboard = QApplication.clipboard()  # 获取剪贴板对象
        clipboard_text = clipboard.text()  # 从剪贴板中读取文本

        # 将读取到的文本显示在输入框中
        if clipboard_text:
            self.input_edit.setText(clipboard_text)
        else:
            QMessageBox.warning(self, "错误", "剪贴板中没有文本")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())