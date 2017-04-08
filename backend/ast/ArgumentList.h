#ifndef ARGUMENTLIST_H
#define ARGUMENTLIST_H

#include "NaiveScript.h"
#include "ASTNode.h"
#include "Util.h"


namespace naivescript{

class ArgumentList : public ASTNode
{
public:
    virtual bool Parse( struct serialize::ArgumentList * args, size_t size );

    virtual const std::vector<ASTNode *> GetChildren( void ) override
    {
        return children;
    }

    virtual void show( void ) override
    {
        std::cout <<  "ArgumentList\t";
        std::cout <<  "Node Count: " << count << std::endl;
        for (ASTNode * node : children) {
            node->show();
        }
    }

    virtual llvm::Value* accept(Visitor* v) override;

    ~ArgumentList() {
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