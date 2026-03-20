import sys
from PyQt6.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout
from views.main_window import MainWindow

def main():
    print("hello world")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    
if __name__ == "__main__":
    main()