#include "StmtList.h"
#include "Compiler.h"

namespace naivescript{
namespace ast {


void StmtList::accept(Visitor* v)
{
    v->visit(this);
}

}
}