#ifndef STMTLIST_H
#define STMTLIST_H

#include "ASTNode.h"
#include "Util.h"


namespace naivecompiler{

class StmtList : public ASTNode
{
public:
    virtual bool Parse( struct serialize::StmtList * stmt_list, size_t size );

    virtual const std::vector<ASTNode *> GetChildren( void ) override
    {
        return children;
    }

    virtual void show( int offset = 0 ) override
    {
    	std::string index = std::string(offset, '\t');
    	std::cout << index;
        std::cout <<  "StmtList\t";
        std::cout <<  "Node Count: " << count << std::endl;
        for (ASTNode * node : children) {
            node->show(offset + 1);
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
