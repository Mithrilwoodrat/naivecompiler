#include "StmtList.h"
#include "Compiler.h"

namespace naivescript{
bool StmtList::Parse( struct serialize::StmtList * stmt_list, size_t size )
{
    std::cout << "Parsing StmtList ";
    //std::cout << "TypeId: " << stmt_list->type << std::endl;
    count =  stmt_list->count;
    std::cout << "Count: " << count << std::endl;
    uint8_t * data = stmt_list->data;
    size_t total_size = 0;
    size_t node_size;
    for (size_t i=0; i<count; i++) {
        if (total_size > size)
             break;
        uint32_t type = util::getStructType(data);
        //std::cout <<  "TypeId: " << type << std::endl;
        switch (type) {
            case serialize::TypeFuncCall:
                node_size = util::getVarStructSize(data);
                break;
            case serialize::TypeAssignmentExpr:
                node_size = util::getVarStructSize(data);
                children.push_back(NodeFactory::CreateAssignment(data, node_size));
                break;
            case serialize::TypeReturnStmt:
                node_size = util::getVarStructSize(data);
                children.push_back(NodeFactory::CreateReturnNode(data, node_size));
                break;
            default:
                return false;
        }
        total_size += node_size;
        data += node_size;
    }
    return true;
}

llvm::Value* StmtList::accept(Visitor* v)
{
    return v->visit(this);
}

}