from PyQt5.QtCore import QObject, pyqtSlot, QVariant, pyqtSignal
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
# @file 
TEX_FILES_DIR = "tex_files/"

latex = r"This is a latex straight from python ! \int{ x + c } dx !"

class Backend(QObject):
    sendtex = pyqtSignal(str)

    # @brief This function takes whatever content is served from the compiler.html input field via the saveContent
    # @param content: string
    @pyqtSlot(str, str)
    def saveContent(self, fileName: str, content: str):
        print(f"[PYTHON] Content to save: {content[0:20]}")
        cmd = ["./file_handler", fileName,content]
        subprocess.run(cmd)
        

    # @brief runs the latex parse so we can start the compile stage 
    # @params takes in some content from the input 
    @pyqtSlot(str)
    def compile_btn(self, content):
        cmd = ["latex_parser/./main", content]
        subprocess.run(cmd)

    # @brief runs a simply log
    @pyqtSlot(str)
    def logToPython(self, message):
        """Receive logs from JavaScript"""
        print(f"[JS]: {message}")

    # @brief retrieves the list of files from a particular directory and sends it to the js file
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

    @pyqtSlot(str)
    def readFile(self, filename):
        path = rf"{TEX_FILES_DIR}{filename}"
        try:
            with open(path, "r") as f:
                content = f.read()
                # print(f"File content: {content}")
                self.sendtex.emit(content)
            print("[PYTHON] EOF")
        except Exception as e:
            print(f"[PYTHON:readFile] Error: {e}")

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
