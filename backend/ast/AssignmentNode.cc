#include "AssignmentNode.h"
#include "Compiler.h"

namespace naivescript
{
namespace ast {
bool AssignmentNode::Parse( struct serialize::Assignment * assignment, size_t size ) 
{
    std::cout << "Parsing Assignment: ";
    id = Compiler::GetCompiler()->ResolveSymbol(assignment->id);
    std::cout << "ID: " << id << std::endl;
    uint32_t type = util::getStructType(assignment->expr);
    switch(type) {
        case serialize::Value:
            expr = ExprFactory::CreateValue(assignment->expr, assignment->exprSize);
            break;
        default:
            return false;
    }
    return true;
}
}
}
