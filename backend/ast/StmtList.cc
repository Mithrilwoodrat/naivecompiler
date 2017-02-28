#include "StmtList.h"
#include "Compiler.h"

namespace naivescript{


llvm::Value* StmtList::accept(Visitor* v)
{
    return v->visit(this);
}

}