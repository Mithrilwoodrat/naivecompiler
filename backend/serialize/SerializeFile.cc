#include "SerializeFile.h"

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
    std::cout << "Symbols : "; 
    for (auto &s : symbols) {
        std::cout << s << " ";
    }
    std::cout << std::endl;
    return true;
}

bool SerializeFile::Load( const std::string& path ) 
{
    // load binary file into std:string
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

    //size_t length = data_str.size();
    FileFormat *file;
    file = reinterpret_cast<FileFormat*>( const_cast<char *>(data) ); 
    body_size = file->bodySize;
    string_table_size = file->stringtableSize;
     std::cout << "StringTableEntry: " << 
        file->stringTableEntry << std::endl;
    std::cout << "Bodyentry: " << 
        file->bodyEntry << std::endl;
    std::cout << "bodySize: " << 
        file->bodySize << std::endl;
    std::cout << "StringTableSize: " << 
        file->stringtableSize << std::endl;

    symbol_table.Parse(const_cast<char *>(data) + file->stringTableEntry, string_table_size);
    this->body = reinterpret_cast<char *>(const_cast<char *>(data) + file->bodyEntry);
    return true;

}

}
}