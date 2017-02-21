#ifndef SERIALIZEFILE_H
#define SERIALIZEFILE_H

#include <string>
#include <vector>
#include "SerializeStructure.h"


namespace naivescript{
namespace serialize {

class SymbolTable{
public:
    bool Parse( char * data, size_t size);
private:
    std::vector<std::string> symbols;
};

class SerializeFile 
{
public:
    SerializeFile(const std::string path) : path(path), 
    string_table_size(0), body_size(0) {}
    bool Load( void );
    ~SerializeFile() {
    }

private:
    std::string path;
    SymbolTable symbol_table;
    size_t string_table_size;
    size_t body_size;
};

}
}

#endif
