import sys
from pathlib import Path
import subprocess

EXTENSION   = ".tex"
FOLDERNAME  = "../tex_files/"

class File:
    def __init__(self,name, content):
        self.file_name = name+EXTENSION
        self.directory = Path(f"{FOLDERNAME}")
        self.path = Path(f"{FOLDERNAME}{self.file_name}")

        self.content = content

    def validate_dir(self):
        if not self.path.is_dir():
            print(self.path.resolve())
            self.directory.mkdir()
            return True
        else:
            return True

    def create(self):
        if(self.validate_dir):
            with open(self.path, 'w') as f:                
                f.write(self.content)
        else:
            self.directory.mkdir()

    def rm(self):
        self.path.unlink()

if __name__ == "__main__":
    argc = len(sys.argv)
    if (argc> 3 or argc <3):
        print(f"Value error: args {argc}")
        exit(1)
    else:
        new_file = File(sys.argv[1], sys.argv[2])
        print(f"File: {new_file.path}")
        new_file.create()

        cmd = ["ls", f"{FOLDERNAME}"]
        cat_cmd = ["cat", f"{new_file.path}"]
        subprocess.run(cmd)
        subprocess.run(cat_cmd)
        delete = input("\nDo you want to delete the file: ")
        if(delete):
            new_file.rm()
