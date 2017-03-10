#include "DeclarationList.h"
#include "Compiler.h"

namespace naivescript{

llvm::Value* DeclarationList::accept(Visitor* v)
{
    return v->visit(this);
}

}