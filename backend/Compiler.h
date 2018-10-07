#ifndef COMPILER_H
#define COMPILER_H

#include <string>
#include <iostream>
#include "SerializeFile.h"
#include "AST.h"
#include "NodeVisitor.h"
#include "CodeGen.h"
#include "Logging.h"

namespace naivecompiler
{

class Compiler 
{
public:
    Compiler() : symbol_table(nullptr) {}
    
    static Compiler * GetCompiler() {
        if (!instance) {
            instance = new Compiler();
        }
        return instance;
    }

    void LoadData(char *path) {
        std::string spath(path);
        file.Load(spath);
        symbol_table = file.GetSymbolTable();
    };

    static const std::string& ResolveSymbol(uint32_t id) {
        return GetCompiler()->symbol_table->ResolveSymbol(id);
    }

    void Compile( char * filename );
    
    static Compiler* instance;
private:
    const serialize::SymbolTable* symbol_table;
    AST ast;
    serialize::SerializeFile file;
    CodeGenVisitor genVisitor;
};

}

#endif
