from PyQt6.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout, QLabel,QTextEdit
import subprocess

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.setWindowTitle("Main window")
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.compile_button = QPushButton("Click me")
        label = QLabel("This is the main window!")
        self.textbox = QTextEdit()
        self.viewBox = QTextEdit()
        self.viewBox.setReadOnly(True)
        self.textbox.setText("Type here")
        layout.addWidget(self.textbox)
        layout.addWidget(self.viewBox)
        layout.addWidget(label)
        layout.addWidget(self.compile_button)
        self.compile_button.clicked.connect(self.compile)


    def compile(self):
        source_code = self.textbox.toPlainText()
        print(type(source_code))
        print(source_code)
        subprocess.run("ls 'latex_parser'")
        # output = subprocess.run(f"/home/tash/pythonProds/latex_desktop/latex_app/latex_parser/main {source_code}", capture_output=True)
        # print(output)
        self.viewBox.setPlainText(source_code)
