#include "StmtList.h"
#include "NodeFactory.h"
#include "AssignmentNode.h"
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
            default:
                std::cout << "Error Unknown stmt type" << std::endl;
                return false;
            case serialize::TypeDeclaration:
                node_size = util::getVarStructSize(data);
                children.push_back(NodeFactory::CreateDeclaration(data, node_size));
                break;
            case serialize::TypeFuncCall:
                node_size = util::getVarStructSize(data);
                children.push_back(NodeFactory::CreateFuncCallNode(data, node_size));
                break;
            case serialize::TypeLabel:
                node_size = util::getVarStructSize(data);
                children.push_back(NodeFactory::CreateLabelNode(data, node_size));
                break;
            case serialize::TypeABSJMP:
                node_size = util::getVarStructSize(data);
                children.push_back(NodeFactory::CreateABSJMPNode(data, node_size));
                break;
            case serialize::TypeCMPJMP:
                node_size = util::getVarStructSize(data);
                children.push_back(NodeFactory::CreateCMPJMPNode(data, node_size));
                break;
            case serialize::TypeAssignmentExpr:
                node_size = util::getVarStructSize(data);
                children.push_back(NodeFactory::CreateAssignment(data, node_size));
                break;
            case serialize::TypeReturnStmt:
                node_size = util::getVarStructSize(data);
                children.push_back(NodeFactory::CreateReturnNode(data, node_size));
                break;
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