#include "WhileNode.h"
#include "Compiler.h"
#include "NodeFactory.h"

namespace naivescript
{

bool WhileNode::Parse(  struct serialize::WhileStmt * stmt, size_t size ) 
{
    std::cout << "Parsing WhileStmt: ";
    uint8_t *p_cond = (uint8_t *)(stmt->cond.data);
    uint8_t *p_body = p_cond + stmt->condSize;
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
    body = NodeFactory::CreateStmtList(p_body, stmt->bodySize);
    return true;
}

llvm::Value* WhileNode::accept(Visitor* v)
{
    return v->visit(this);
}

}