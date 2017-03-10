#include "FunctionList.h"
#include "Compiler.h"

namespace naivescript
{

llvm::Value* FunctionList::accept(Visitor* v)
{
    return v->visit(this);
}

}