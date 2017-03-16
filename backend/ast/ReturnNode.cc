#include "ReturnNode.h"
#include "NodeFactory.h"
#include "Compiler.h"

namespace naivescript
{

bool ReturnNode::Parse( struct serialize::ReturnStmt * return_stmt, size_t size ) 
{
    std::cout << "Parsing ReturnStmt: ";
    uint32_t type = util::getStructType(return_stmt->expr);
    switch(type) {
        case serialize::TypeValue:
            expr = NodeFactory::CreateValue(return_stmt->expr, return_stmt->exprSize);
            break;
        case serialize::TypeSymbol:
            expr = NodeFactory::CreateSymbol(return_stmt->expr, return_stmt->exprSize);
            break;
        case serialize::TypeBinaryOp:
            expr = NodeFactory::CreateBinaryOp(return_stmt->expr, return_stmt->exprSize);
            //std::cout << "BinaryOp" << std::endl;
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
