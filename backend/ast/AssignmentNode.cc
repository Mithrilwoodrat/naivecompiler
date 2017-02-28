#include "AssignmentNode.h"
#include "Compiler.h"
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
        case serialize::Value:
            expr = NodeFactory::CreateValue(assignment->expr, assignment->exprSize);
            break;
        case serialize::Symbol:
            expr = NodeFactory::CreateSymbol(assignment->expr, assignment->exprSize);
            break;
        case serialize::BinaryOp:
            expr = NodeFactory::CreateBinaryOp(assignment->expr, assignment->exprSize);
            //std::cout << "BinaryOp" << std::endl;
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
