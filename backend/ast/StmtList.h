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
        stmt_count =  stmt_list->count;
        std::cout << "Count: " << stmt_count << std::endl;
        uint8_t * data = stmt_list->data;
        size_t node_size;
        for (size_t i=0; i<stmt_count; i++) {
            uint32_t type = util::getStructType(data);
            //std::cout <<  "TypeId: " << type << std::endl;
            switch (type) {
                case serialize::WriteStmt:
                    data += getStructSize(serialize::WriteStmt);
                    break;
                case serialize::Assignment:
                    //std::cout << "Assigment " << "size: " << util::getVarStructSize(data) << std::endl;
                    node_size = util::getVarStructSize(data);
                    stmts.push_back(NodeFactory::CreateAssignment(data, node_size));
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
        return stmts;
    }

    virtual void show( void ) override
    {
        std::cout <<  "StmtList\t";
        std::cout <<  "Node Count: " << stmt_count << std::endl;
        for (ASTNode * node : stmts) {
            node->show();
        }
    }

    virtual llvm::Value* accept(Visitor* v) override;

    ~StmtList() {
        for (ASTNode * node : stmts) {
            free(node);
        }
    }

private:
    size_t stmt_count;
    std::vector<ASTNode*> stmts;
};

}
#endif