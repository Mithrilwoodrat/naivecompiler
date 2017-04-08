#include "AssignmentNode.h"
#include "Compiler.h"
#include "ValueNode.h"
#include "BinaryOpNode.h"
#include "NodeFactory.h"

namespace naivescript
{

bool AssignmentNode::Parse( struct serialize::Assignment * assignment, size_t size ) 
{
    std::cout << "Parsing Assignment: ";
    id = Compiler::GetCompiler()->ResolveSymbol(assignment->id);
    std::cout << "ID: " << id << std::endl;
    uint32_t type = util::getStructType(assignment->expr);
    switch(type) {
        case serialize::TypeValue:
            expr = NodeFactory::CreateValue(assignment->expr, assignment->exprSize);
            break;
        case serialize::TypeSymbol:
            expr = NodeFactory::CreateSymbol(assignment->expr, assignment->exprSize);
            break;
        case serialize::TypeBinaryOp:
            expr = NodeFactory::CreateBinaryOp(assignment->expr, assignment->exprSize);
            break;
        case serialize::TypeFuncCall:
            expr = NodeFactory::CreateFuncCallNode(assignment->expr, assignment->exprSize);
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
