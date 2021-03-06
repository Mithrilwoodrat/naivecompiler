#ifndef ARGUMENTLIST_H
#define ARGUMENTLIST_H

#include "../NaiveCompiler.h"
#include "ASTNode.h"
#include "Util.h"


namespace naivecompiler{

class ArgumentList : public ASTNode
{
public:
    virtual bool Parse( struct serialize::ArgumentList * args, size_t size );

    virtual const std::vector<ASTNode *> GetChildren( void ) override
    {
        return children;
    }

    virtual void show( int offset = 0 ) override
    {
    	std::string index = std::string(offset, '\t');
    	DLOG(LOG_DEBUG) << index;
        DLOG(LOG_DEBUG) <<  "ArgumentList  ";
        DLOG(LOG_DEBUG) <<  "Node Count: " << count << std::endl;
        DLOG(LOG_DEBUG) << "\t";
        for (ASTNode * node : children) {
            node->show(offset + 1);
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
