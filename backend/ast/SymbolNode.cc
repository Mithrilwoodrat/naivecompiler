#include "SymbolNode.h"
#include "Compiler.h"

namespace naivescript
{
namespace ast {

bool SymbolNode::Parse( struct serialize::Symbol * symbol, size_t size ) {
    std::cout << "Parsing Symbol: ";
    id = Compiler::GetCompiler()->ResolveSymbol(symbol->id);
    symboltype = symbol->symboltype;
    std::cout << "ID: " << id << std::endl;
    return true;
}

void SymbolNode::accept(Visitor* v)
{
    v->visit(this);
}


}
}