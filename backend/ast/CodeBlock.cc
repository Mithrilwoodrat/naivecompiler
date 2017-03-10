#include "CodeBlock.h"
#include "Compiler.h"

namespace naivescript
{

llvm::Value* CodeBlock::accept(Visitor* v)
{
    return v->visit(this);
}

}