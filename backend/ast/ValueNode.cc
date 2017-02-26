#include "ValueNode.h"
#include "Compiler.h"

namespace naivescript{
namespace ast {

bool ValueNode::Parse( struct serialize::Value * value, size_t size ) 
{
    std::cout << "Parsing ValueNode: ";
    val = value->val;
    valuetype = value->valuetype;
    std::cout << "Val: " << val << std::endl;
    return true;
}

void ValueNode::accept(Visitor* v)
{
    v->visit(this);
}

}
}