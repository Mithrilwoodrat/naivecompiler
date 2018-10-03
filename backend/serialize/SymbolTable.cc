#include "SymbolTable.h"

namespace naivecompiler{
namespace serialize {

bool SymbolTable::Parse( uint8_t * data, size_t size ) {
    size_t start = 0;
    symbols.push_back(std::string(reinterpret_cast<char *>(data+ start)));
    for (size_t i=0; i < size - 1; i++) {
        if (data[i] == '\0') {
            if (i + 1 < size -1) {
                start = i+1;
                symbols.push_back(std::string(reinterpret_cast<char *>(data+ start)));
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

}
}