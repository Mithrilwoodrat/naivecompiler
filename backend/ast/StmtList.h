#ifndef STMTLIST_H
#define STMTLIST_H

#include "NaiveScript.h"
#include "ASTNode.h"
#include "NodeFactory.h"
#include "AssignmentNode.h"
#include "Util.h"


namespace naivescript{

class StmtList : public ASTNode
{
public:
    virtual bool Parse( struct serialize::StmtList * stmt_list, size_t size )
    {
        std::cout << "Parsing StmtList ";
        //std::cout << "TypeId: " << stmt_list->type << std::endl;
        count =  stmt_list->count;
        std::cout << "Count: " << count << std::endl;
        uint8_t * data = stmt_list->data;
        size_t node_size;
        for (size_t i=0; i<count; i++) {
            uint32_t type = util::getStructType(data);
            //std::cout <<  "TypeId: " << type << std::endl;
            switch (type) {
                case serialize::TypeFuncCall:
                    data += util::getVarStructSize(data);
                    break;
                case serialize::TypeAssignmentExpr:
                    //std::cout << "Assigment " << "size: " << util::getVarStructSize(data) << std::endl;
                    node_size = util::getVarStructSize(data);
                    children.push_back(NodeFactory::CreateAssignment(data, node_size));
                    data += node_size;
                    break;
                case serialize::TypeReturnStmt:
                    node_size = util::getVarStructSize(data);
                    children.push_back(NodeFactory::CreateReturnNode(data, node_size));
                    data += node_size;
                    break;
                default:
                    return false;
            }
        }
        return true;
    }

    virtual const std::vector<ASTNode *> GetChildren( void ) override
    {
        return children;
    }

    virtual void show( void ) override
    {
        std::cout <<  "StmtList\t";
        std::cout <<  "Node Count: " << count << std::endl;
        for (ASTNode * node : children) {
            node->show();
        }
    }

    virtual llvm::Value* accept(Visitor* v) override;

    ~StmtList() {
        for (ASTNode * node : children) {
            free(node);
        }
    }

private:
    size_t count;
    std::vector<ASTNode*> children;
};

}
#endif