from PyQt5.QtCore import QObject, pyqtSlot, QVariant
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
import sys
import os
import subprocess
import json
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings

main_page = "views/html_pages/homepage.html"
TEX_FILES_DIR = "tex_files/"

latex = r"This is a latex straight from python ! \int{ x + c } dx !"

class Backend(QObject):
    @pyqtSlot()
    def compile_btn(self):
        cmd = ["latex_parser/./main", "some_latex.txt"]
        subprocess.run(cmd)

    @pyqtSlot(str)
    def logToPython(self, message):
        """Receive logs from JavaScript"""
        print(f"[JS]: {message}")

    @pyqtSlot(result=str)
    def getFileList(self):
        """Return list of tex files - no path needed from JS"""
        print("[Python] getFileList called")
        try:
            files = os.listdir(TEX_FILES_DIR)
            print(f"[Python] Files found: {files}")
            return json.dumps({'files': files, 'error': None})
        except Exception as e:
            print(f"[Python] Error: {str(e)}")
            return json.dumps({'files': [], 'error': str(e)})
    @pyqtSlot(str)
    def logToPython(self, message):
        """Receive logs from JavaScript"""
        print(f"[JS]: {message}")

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pastel Aquatic Greeting")
        self.setGeometry(100, 100, 600, 700)

        # Disable error logging for WebGL
        os.environ["QT_LOGGING_RULES"] = "qt.webenginecontext.debug=false"
        os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = (
            "--disable-gpu "
            "--disable-gpu-compositing "
            "--disable-software-rasterizer "
            "--disable-webgl "
            "--ignore-gpu-blocklist "
            "--disable-logging "
            "--log-level=3"
        )

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create web view
        self.view = QWebEngineView()

        # Load backend
        self.backend = Backend()
        self.channel = QWebChannel()
        self.channel.registerObject("backend", self.backend)
        self.view.page().setWebChannel(self.channel)

        # Configure settings to reduce errors
        settings = self.view.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.ScrollAnimatorEnabled, False)

        layout.addWidget(self.view)

        # Load your HTML file
        html_path = os.path.abspath(main_page)
        if os.path.exists(html_path):
            self.view.load(QUrl.fromLocalFile(html_path))
        else:
            print(f"Error: {html_path} not found")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
