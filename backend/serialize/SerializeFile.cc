#include "SerializeFile.h"
#include <iostream>
#include <fstream>
#include <stdio.h>


namespace naivescript{
namespace serialize {

bool SymbolTable::Parse( char * data, size_t size ) {
    size_t start = 0;
    symbols.push_back(std::string(const_cast<char *>(data) + start));
    for (size_t i=0; i < size - 1; i++) {
        //printf("%x ", data[i]);
        if (data[i] == '\0') {
            if (i + 1 < size -1) {
                start = i+1;
                symbols.push_back(std::string(const_cast<char *>(data) + start));
            } else {
                break;
            }
        }
    }
    for (auto &s : symbols) {
        std::cout << s << std::endl;
    }
    return true;
}

bool SerializeFile::Load( void ) 
{
    // load binary file into std:string
    FileFormat *file_header;
    std::ifstream fdata(path);
    if (!fdata) {
        std::cout << "Load File Failed" << std::endl;
        return false;
    }
    std::string data_str;
    
    fdata.seekg(0, std::ios::end);   
    data_str.reserve(fdata.tellg());
    fdata.seekg(0, std::ios::beg);

    data_str.assign((std::istreambuf_iterator<char>(fdata)),
               std::istreambuf_iterator<char>());
    const char * data = data_str.c_str();

    size_t length = data_str.size();

    file_header = reinterpret_cast<FileFormat*>( const_cast<char *>(data) ); 
    body_size = file_header->bodySize;
    string_table_size = file_header->stringtableSize;
     std::cout << "StringTableEntry: " << 
        file_header->stringTableEntry << std::endl;
    std::cout << "Bodyentry: " << 
        file_header->bodyEntry << std::endl;
    std::cout << "bodySize: " << 
        file_header->bodySize << std::endl;
    std::cout << "StringTableSize: " << 
        file_header->stringtableSize << std::endl;

    symbol_table.Parse(const_cast<char *>(data) + file_header->stringTableEntry, string_table_size);

    return true;

}

}
}