#include "file_handler.h"
#include <cstdio>

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

void File::create(const char* filename,std::string directory, std::string filetype) {
    this->path = directory + "/" + filename + filetype;
    this->dir = directory;
    std::cout << "Attempting to create: " << path << std::endl;
    std::ofstream file(this->path);
    file << content;
    file.close();
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

int main(int argv, char** argc) {
    printf("Args: %d\n", argv);
    // size_t n_args = ;
    if(argv>3){
        printf("Too many values\n");
        return 0;
    }else {
        char* directory = argc[1];
        char* content   = argc[2];
        printf("[CPP] Directory: %s\n\t[CPP] Content: %s\n", directory, content);
    }

    return 0;
}
