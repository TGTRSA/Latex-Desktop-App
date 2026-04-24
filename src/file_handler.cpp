#include "file_handler.h"
#include <cstdio>
#include <cstdlib>
#include <cstring>

void InputFile::get_file_contents(char *filename) {
    std::string tmp_string;
    std::string file_contents;
    std::ifstream file(filename);
    char ch;
    printf("This is the contents of the text file:\n%s", file_contents.c_str());
    if(file.is_open()){
        while (file.get(ch)) {
            this->content+=ch;
        }
    }else {
        std::cerr << "Failed to open file" << std::endl;
    }
}

void File::create() {
    printf("Attempting to create: %s in %s\n", filename, path);
    std::ofstream file(this->path);
    if(!file.is_open()){
        std::cerr << "Failed to open file\n";
        return;
    }
    file << content;
    file.close();
    if(file.fail()){
        std::cerr << "Write failed\n";
        return;
    }else {
        printf("Write succeded\n");
    }
};

    // removes the file
int File::rm(){
    try{std::filesystem::remove(this->path);
        printf("File deleted\n");
        return 0;
    }catch (const std::filesystem::filesystem_error& e) {
        printf("Error: %s\n", e.what());
        return -1;
    }
}

void File::to_pdf(){
    std::vector<std::string> cmd_base = {
        "latex -output-directory=","pdflatex "
    };
    int n_commands = cmd_base.size();
    for(int i=0;i<n_commands;i++){
        std::stringstream cmd;

        if(i==0){
            system("cd latex_files");
            cmd << cmd_base[i] << this->dir << " " << this->path;
        }if(i!=0){
            cmd << cmd_base[i] << this->path;
        }
        std::string cmd_string = cmd.str();
        std::cout << "Running: " << cmd_string.c_str() << "\n";
        // std::cout << "Attempting:" <<  printable;
        system(cmd_string.c_str());
    }
    // system(cmd_string.c_str());

}

int main(int argc, char** argv) {
    printf("Args: %d\n", argc);
    // size_t n_args = ;
    if(argc>3){
        printf("Too many values\n");
        return 0;
    }else {
        File f;
        const char* directory = "tex_files/";
        const char* extention = ".tex";
        const char* fileName = argv[1];
        size_t len = strlen(extention)+ strlen(fileName);
        char* path = (char *)malloc(len);
        
        strcat(path,directory);
        strcat(path, fileName);      
        strcat(path,extention);
        
        char* content   = argv[2];
        printf("[CPP] path: %s\n\t[CPP] Content: %s\n", path, content);
        f.content = content;
        f.filename = fileName;
        f.path = path;
        f.dir = directory;
        f.create();

    }

    return 0;
}
