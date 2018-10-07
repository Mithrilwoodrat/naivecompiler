#include "SymbolNode.h"
#include "Compiler.h"

namespace naivecompiler
{

bool SymbolNode::Parse( struct serialize::Symbol * symbol, size_t size ) {
    DLOG(LOG_DEBUG) << "Parsing Symbol: ";
    id = Compiler::GetCompiler()->ResolveSymbol(symbol->id);
    symboltype = symbol->symboltype;
    DLOG(LOG_DEBUG) << "ID: " << id << std::endl;
    return true;
}

llvm::Value* SymbolNode::accept(Visitor* v)
{
    return v->visit(this);
}

}