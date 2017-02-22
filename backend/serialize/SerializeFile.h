#ifndef SERIALIZEFILE_H
#define SERIALIZEFILE_H

#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <stdio.h>
#include "SerializeStructure.h"


namespace naivescript{
namespace serialize {

class SymbolTable{
public:
    bool Parse( char * data, size_t size);

    const std::string & ResolveSymbol(uint32_t id) const {
        if (id < symbols.size()) {
            return symbols[id];
        }
        static std::string empty_symbol = "";
        return empty_symbol;
    }

private:
    std::vector<std::string> symbols;
};

class SerializeFile 
{
public:
    SerializeFile():string_table_size(0), body_size(0) {}

    size_t GetBodySize(void) {
        return body_size;
    }

    const char * GetBody(void) const {
        return body;
    }

    const SymbolTable * GetSymbolTable( void ) const {
        return &symbol_table;
    }

    bool Load( const std::string& path );

    ~SerializeFile() {
    }

private:
    size_t string_table_size;
    size_t body_size;
    SymbolTable symbol_table;
    const char * body;
};

}
}

#endif
