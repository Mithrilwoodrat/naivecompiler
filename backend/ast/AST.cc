#include "AST.h"
#include "Compiler.h"
#include "NodeFactory.h"

namespace naivescript
{
bool AST::Parse( struct serialize::AST * ast, size_t size )
{
    std::cout << "Parsing AST ";
    count =  ast->count;
    std::cout << "Count: " << count << std::endl;
    uint8_t * data = ast->data;
    size_t node_size;
    for (size_t i=0; i<count; i++) {
        node_size = util::getVarStructSize(data);
        uint32_t type = util::getStructType(data);
        switch (type) {
            default:
                std::cout << "Error Unknown stmt type" << std::endl;
                return false;
            case serialize::TypeFunction:
                children.push_back(NodeFactory::CreateFunction(data, node_size));
                break;
        }
        data += node_size;
    }
    return true;
}

std::map<std::string, llvm::Value*>AST::accept(Visitor* v)
{
    return v->visit(this);
}

}