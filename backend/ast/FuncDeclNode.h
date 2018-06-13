#ifndef FUNCDECLNODE_H
#define FUNCDECLNODE_H


#include "ASTNode.h"
#include "Util.h"


namespace naivescript{

class FuncDeclNode : public ASTNode
{
public:
    bool Parse( struct serialize::FuncDecl * func, size_t size );

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

    void show( void )
    {
        std::cout <<  "Function\t";
        std::cout << func_name << std::endl;
        for (ASTNode * node : children) {
            node->show();
        }
    }

    llvm::Value* accept(Visitor* v);

    ~FuncDeclNode() {
        for (ASTNode * node : children) {
            free(node);
        }
    }

private:
    std::string func_name;
    uint32_t return_type;
    ASTNode *params_list;
    std::vector<ASTNode*> children;
};

}
#endif
