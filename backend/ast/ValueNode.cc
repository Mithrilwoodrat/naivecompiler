#include "ValueNode.h"

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
}
}