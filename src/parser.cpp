#include "parse.h"

int main(int argc, char* argv[]) {

    if(argc>2){
        printf("Too many values given: %d", argc);
        exit(1);
    }else {
        std::string content = argv[1];
        Document::full_ doc = lex_content(content);
        Parser p;
        p.doc_content = doc;
        p.compile_latex();
        p.print_();
    }

}