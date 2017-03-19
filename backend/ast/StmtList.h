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
    virtual bool Parse( struct serialize::StmtList * stmt_list, size_t size );

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