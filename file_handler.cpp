#include "file_handler.h"

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

int main(int argv, char** argc) {
    printf("Args: %d\n", argv);
    // size_t n_args = ;
    int i = 1;
    while(argc[i]!=nullptr){
        printf("Arg: %s\n", argc[i]);
        i++;
    } 
    return 0;
}
