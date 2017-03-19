#ifndef SYMBOLTABLE_H
#define SYMBOLTABLE_H

#include "NaiveScript.h"

namespace naivescript{
namespace serialize {

class SymbolTable{
public:
    bool Parse( uint8_t * data, size_t size);

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

}
}
#endif