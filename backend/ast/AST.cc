#include "AST.h"
#include "Compiler.h"
#include "NodeFactory.h"

namespace naivecompiler
{
bool AST::Parse( struct serialize::AST * ast, size_t size )
{
    DLOG(LOG_DEBUG) << "Parsing AST ";
    count =  ast->count;
    DLOG(LOG_DEBUG) << "Count: " << count << std::endl;
    uint8_t * data = ast->data;
    size_t node_size;
    for (size_t i=0; i<count; i++) {
        node_size = util::getVarStructSize(data);
        uint32_t type = util::getStructType(data);
        switch (type) {
            default:
                DLOG(LOG_DEBUG) << "Error Unknown stmt type: " << type << std::endl;
                return false;
            case serialize::TypeFuncDef:
                children.push_back(NodeFactory::CreateFuncDef(data, node_size));
                break;
            case serialize::TypeFuncDecl:
            	children.push_back(NodeFactory::CreateFuncDecl(data, node_size));
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
