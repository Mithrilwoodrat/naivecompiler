#include "ValueNode.h"
#include "Compiler.h"

namespace naivescript{

bool ValueNode::Parse( struct serialize::Value * value, size_t size ) 
{
    std::cout << "Parsing ValueNode: ";
    this->val = value->val;
    this->valuetype = value->valuetype;
    std::cout << "Type: " << valuetype << "Val: " << val << std::endl;
    return true;
}

llvm::Value* ValueNode::accept(Visitor* v)
{
    return v->visit(this);
}

}