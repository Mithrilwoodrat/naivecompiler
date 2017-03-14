#include "FunctionList.h"
#include "Compiler.h"

namespace naivescript
{

std::map<std::string, llvm::Function*>FunctionList::accept(Visitor* v)
{
    return v->visit(this);
}

}