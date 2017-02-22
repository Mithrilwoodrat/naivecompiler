#ifndef COMPILER_H
#define COMPILER_H

#include <string>
#include "SerializeFile.h"
#include "AST.h"

namespace naivescript
{

class Compiler 
{
public:
    Compiler() {}
    static Compiler * GetCompiler() {
        if (!instance) {
            instance = new Compiler();
        }
        return instance;
    }

    static void LoadData(const std::string& path) {
        GetCompiler()->file.Load(path);
        GetCompiler()->symbol_table = GetCompiler()->file.GetSymbolTable();
    };

    static const std::string& ResolveSymbol(uint32_t id) {
        return GetCompiler()->symbol_table->ResolveSymbol(id);
    }
    static Compiler* instance;
private:
    const serialize::SymbolTable* symbol_table;
    serialize::SerializeFile file;
};

}

#endif