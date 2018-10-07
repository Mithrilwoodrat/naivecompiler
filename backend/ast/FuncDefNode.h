#ifndef FUNCDEFNODE_H
#define FUNCDEFNODE_H


#include "ASTNode.h"
#include "Util.h"


namespace naivecompiler{

class FuncDefNode : public ASTNode
{
public:
    bool Parse( struct serialize::FuncDef * func, size_t size );

    const std::vector<ASTNode *> GetChildren( void )
    {
        return children;
    }

    std::string GetFuncName(void)
    {
        return func_name;
    }

    ASTNode * GetParams(void) 
    {
        return params_list;
    }

    uint32_t GetReturnType(void) const
    {
    	return return_type;
    }

    ASTNode* GetBody(void)
    {
        return body;
    }

    void show( int offset = 0 )
    {
    	std::string index = std::string(offset, '\t');
    	DLOG(LOG_DEBUG) << index;
        DLOG(LOG_DEBUG) <<  "Function\t";
        DLOG(LOG_DEBUG) << func_name << std::endl;
        for (ASTNode * node : children) {
            node->show(offset+1);
        }
    }

    llvm::Value* accept(Visitor* v);

    ~FuncDefNode() {
        for (ASTNode * node : children) {
            free(node);
        }
    }

private:
    std::string func_name;
    uint32_t return_type;
    ASTNode *params_list;
    ASTNode *body;
    std::vector<ASTNode*> children;
};

}
#endif
