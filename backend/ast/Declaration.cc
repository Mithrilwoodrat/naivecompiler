#include "Declaration.h"
#include "Compiler.h"

namespace naivecompiler
{

bool Declaration::Parse( struct serialize::Declaration * decl, size_t size ) {
    DLOG(LOG_DEBUG) << "Parsing Declaration: ";
    id = Compiler::GetCompiler()->ResolveSymbol(decl->id);
    symboltype = decl->symboltype;
    DLOG(LOG_DEBUG) << "ID: " << decl->id << ":" << id << std::endl;
    return true;
}

llvm::Value* Declaration::accept(Visitor* v)
{
    return v->visit(this);
}

}