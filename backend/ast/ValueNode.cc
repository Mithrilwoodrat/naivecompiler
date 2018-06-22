#include "ValueNode.h"
#include "Compiler.h"

namespace naivescript{

bool ValueNode::Parse( struct serialize::Value * value, size_t size ) 
{
	return false;
}

llvm::Value* ValueNode::accept(Visitor* v)
{
    return v->visit(this);
}

bool IntegerNode::Parse( struct serialize::Value * value, size_t size ) {
	this->valuetype = value->valuetype;
	if (this->valuetype == serialize::CONSTINT) {
		this->val = value->val;
		std::cout << "Type: " << ShowType(valuetype) << "\tVal: " << val << std::endl;
		return true;
	}
	return false;
}

llvm::Value* IntegerNode::accept(Visitor* v)
{
    return v->visit(this);
}


bool StringLiteralNode::Parse( struct serialize::Value * value, size_t size ) {
	this->valuetype = value->valuetype;
	if (this->valuetype == serialize::CONSTSTRING) {
		this->valstring = Compiler::GetCompiler()->ResolveSymbol(value->val);
		std::cout << "Type: " << ShowType(valuetype) << "\tVal: " << valstring << std::endl;
		return true;
	}
	return false;
}

llvm::Value* StringLiteralNode::accept(Visitor* v)
{
    return v->visit(this);
}

}
