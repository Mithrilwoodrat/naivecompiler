#include "ReturnNode.h"
#include "NodeFactory.h"
#include "Compiler.h"

namespace naivescript
{

bool ReturnNode::Parse( struct serialize::ReturnStmt * return_stmt, size_t size ) 
{
    std::cout << "Parsing ReturnStmt: ";
    if (return_stmt->exprSize == 0) {
    	std::cout << "Void" << std::endl;
    }
    uint32_t type = util::getStructType(return_stmt->expr);
    switch(type) {
        case serialize::TypeValue:
            util::debug_parse(return_stmt->expr, return_stmt->exprSize);
            expr = NodeFactory::CreateValue(return_stmt->expr, return_stmt->exprSize);
            break;
        case serialize::TypeSymbol:
            expr = NodeFactory::CreateSymbol(return_stmt->expr, return_stmt->exprSize);
            break;
        case serialize::TypeBinaryOp:
            expr = NodeFactory::CreateBinaryOp(return_stmt->expr, return_stmt->exprSize);
            break;
        case serialize::TypeFuncCall:
            expr = NodeFactory::CreateFuncCallNode(return_stmt->expr, return_stmt->exprSize);
            break;
        default:
            return false;
    }
    return true;
}

llvm::Value* ReturnNode::accept(Visitor* v)
{
    return v->visit(this);
}

}
