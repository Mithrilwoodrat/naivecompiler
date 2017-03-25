#include "IfNode.h"
#include "Compiler.h"
#include "NodeFactory.h"

namespace naivescript
{

bool IfNode::Parse(  struct serialize::IfStmt * stmt, size_t size ) 
{
    std::cout << "Parsing IfStmt: ";
    uint8_t *p_cond = (uint8_t *)(stmt->cond.data);
    uint8_t *p_then = p_cond + stmt->condSize;
    uint32_t type = util::getStructType(p_cond);
    switch(type) {
        case serialize::TypeValue:
            cond = NodeFactory::CreateValue(p_cond, stmt->condSize);
            break;
        case serialize::TypeSymbol:
            cond = NodeFactory::CreateSymbol(p_cond, stmt->condSize);
            break;
        case serialize::TypeBinaryOp:
            cond = NodeFactory::CreateBinaryOp(p_cond, stmt->condSize);
            break;
        default:
            return false;
    }
    then = NodeFactory::CreateStmtList(p_then, stmt->thenSize);
    if (stmt->elseSize) {
        uint8_t *p_else = p_then + stmt->thenSize;
        _else = NodeFactory::CreateStmtList(p_else, stmt->elseSize);
    }
    return true;
}

llvm::Value* IfNode::accept(Visitor* v)
{
    return v->visit(this);
}

}