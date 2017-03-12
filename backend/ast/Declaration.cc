#include "Declaration.h"
#include "Compiler.h"

namespace naivescript
{

bool Declaration::Parse( struct serialize::Declaration * decl, size_t size ) {
    std::cout << "Parsing Declaration: ";
    id = Compiler::GetCompiler()->ResolveSymbol(decl->id);
    symboltype = decl->symboltype;
    std::cout << "ID: " << decl->id << ":" << id << std::endl;
    return true;
}

llvm::Value* Declaration::accept(Visitor* v)
{
    return v->visit(this);
}

}