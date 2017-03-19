#ifndef SERIALIZEFILE_H
#define SERIALIZEFILE_H

#include "NaiveScript.h"
#include "SerializeStructure.h"
#include "SymbolTable.h"


namespace naivescript{
namespace serialize {

class SerializeFile 
{
public:
    SerializeFile():string_table_size(0), body_size(0) {}

    size_t GetBodySize(void) {
        return body_size;
    }

    const u_int8_t * GetBody(void) const {
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
    const u_int8_t * body;
};

}
}

#endif
