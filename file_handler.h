
#ifndef FILE_HANDER_H
#define FILE_HANDER_H

#include <filesystem>
#include <fstream>
#include <iostream>
#include <cstdlib>
#include <sstream>
#include <vector>

// struct for handling the latex file
struct InputFile {
    std::string content;        // the physical content it will contain
    void get_file_contents(char *filename);
};

// Base struct for handling files
struct File {
    std::string content;    // actual content
    std::string path;       // full path
    std::string dir;        // solely used for directory

    // well ... im sure u can tell
    void create(const char* filename,std::string directory, std::string filetype);

    // removes the file
    int rm();

    void to_pdf();

};

#endif
