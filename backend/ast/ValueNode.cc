#include "ValueNode.h"
#include "Compiler.h"

namespace naivescript{

bool ValueNode::Parse( struct serialize::Value * value, size_t size ) 
{
    std::cout << "Parsing ValueNode: ";
    val = value->val;
    valuetype = value->valuetype;
    std::cout << "Val: " << val << std::endl;
    return true;
}

llvm::Value* ValueNode::accept(Visitor* v)
{
    return v->visit(this);
}

}