#include "DeclarationList.h"
#include "Compiler.h"

namespace naivecompiler{

llvm::Value* DeclarationList::accept(Visitor* v)
{
    return v->visit(this);
}

}