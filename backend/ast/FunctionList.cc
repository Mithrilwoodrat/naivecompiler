#include "FunctionList.h"
#include "Compiler.h"

namespace naivescript
{

std::vector<llvm::Function*>FunctionList::accept(Visitor* v)
{
    return v->visit(this);
}

}