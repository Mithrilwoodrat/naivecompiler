#ifndef STMTLIST_H
#define STMTLIST_H

#include "ASTNode.h"
#include "Assignment.h"
#include "iostream"
#include "Util.h"
#include <stdio.h>


namespace naivescript{
namespace ast {

class StmtFactory
{
public:
    static ASTNode * CreateAssignment(uint8_t *data, size_t size) {
        Assignment *node = new Assignment();
        node->Parse(reinterpret_cast<struct serialize::Assignment*>(data), size);
        return node;
    }
};

class StmtList : public ASTNode
{
public:
    virtual bool Parse( struct serialize::StmtList * stmt_list, size_t size )
    {
        std::cout << "Parsing StmtList "  << std::endl;
        std::cout << "TypeId: " << stmt_list->type << std::endl;
        stmt_count =  stmt_list->count;
        std::cout << "Count: " << stmt_count << std::endl;
        uint8_t * data = stmt_list->data;
        size_t node_size;
        for (size_t i=0; i<stmt_count; i++) {
            uint32_t type = util::getStructType(data);
            std::cout <<  "TypeId: " << type << std::endl;
            switch (type) {
                case serialize::WriteStmt:
                    data += getStructSize(serialize::WriteStmt);
                    break;
                case serialize::Assignment:
                    std::cout << "Assigment " << "size: " << util::getVarStructSize(data) << std::endl;
                    node_size = util::getVarStructSize(data);
                    stmts.push_back(StmtFactory::CreateAssignment(data, node_size));
                    data += node_size;
                    break;
                case serialize::BinaryOp:
                    break;
                default:
                    return false;
            }
        }
        return true;
    }

    virtual const std::vector<ASTNode *>& GetChildren( void ) 
    {
        return stmts;
    }

    virtual void show( void) {
        std::cout <<  "StmtList\t";
        std::cout <<  "Node Count: " << stmt_count << std::endl;
        for (ASTNode * node : stmts) {
            node->show();
        }
    }

private:
    size_t stmt_count;
    std::vector<ASTNode*> stmts;
};

}
}
#endif