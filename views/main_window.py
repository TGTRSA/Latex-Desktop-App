from PyQt6.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout, QLabel

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.setWindowTitle("Main window")
        layout = QVBoxLayout()
        self.setLayout(layout)
        button = QPushButton("Click me")
        label = QLabel("This is the main window!")
        layout.addWidget(label)
        layout.addWidget(button)