#include "ValueNode.h"
#include "Compiler.h"

namespace naivescript{

bool ValueNode::Parse( struct serialize::Value * value, size_t size ) 
{
    std::cout << "Parsing ValueNode: ";
    this->valuetype = value->valuetype;
    if (this->valuetype == serialize::CONSTSTRING) {
    	this->valstring = Compiler::GetCompiler()->ResolveSymbol(value->val);
    	std::cout << "Type: " << valuetype << "Val: " << valstring << std::endl;
    } else {
    	this->val = value->val;
    	std::cout << "Type: " << valuetype << "Val: " << val << std::endl;
    }
    return true;
}

llvm::Value* ValueNode::accept(Visitor* v)
{
    return v->visit(this);
}

}
