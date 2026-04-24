import doctest
from html_gui import Backend
from src import file_handler
# 
def test_file_creation():
    path = "tex_files/test.tex"
    file_name = "test"
    text      = "latex content"
    s = Backend()
    s.saveContent(fileName=file_name, content=text)
    # f = file_handler.File(file_name, text)
    
    # assert f.file_name == f"{file_name}.tex"
    # assert f.path == path


if __name__ == "__main__":
    test_file_creation()