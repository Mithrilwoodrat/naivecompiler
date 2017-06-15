#include "AssignmentNode.h"
#include "Compiler.h"
#include "ValueNode.h"
#include "SymbolNode.h"
#include "BinaryOpNode.h"
#include "NodeFactory.h"

namespace naivescript
{

bool AssignmentNode::Parse( struct serialize::Assignment * assignment, size_t size ) 
{
    std::cout << "Parsing Assignment: ";
    uint32_t type = util::getStructType(assignment->castexpr.data);

    switch(type) {
        case serialize::TypeSymbol:
            ASTNode* castexpr = NodeFactory::CreateSymbol(assignment->castexpr.data, assignment->castexprSize);
            SymbolNode * symbol = static_cast<SymbolNode *>(castexpr);
            id = symbol->GetSymbol();
            break;
        default:
            std::cout << "Error Unknown castexpr type" << std::endl;
            return false;
    }

    std::cout << "ID: " << id << std::endl;
    uint8_t * data = assignment->expr.data;
    type = util::getStructType(data);
    switch(type) {
        case serialize::TypeValue:
            expr = NodeFactory::CreateValue(data, assignment->exprSize);
            break;
        case serialize::TypeSymbol:
            expr = NodeFactory::CreateSymbol(data, assignment->exprSize);
            break;
        case serialize::TypeBinaryOp:
            expr = NodeFactory::CreateBinaryOp(data, assignment->exprSize);
            break;
        case serialize::TypeFuncCall:
            expr = NodeFactory::CreateFuncCallNode(data, assignment->exprSize);
            break;
        default:
            return false;
    }
    return true;
}

llvm::Value* AssignmentNode::accept(Visitor* v)
{
    return v->visit(this);
}

}
