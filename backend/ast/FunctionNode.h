#ifndef FUNCTIONNODE_H
#define FUNCTIONNODE_H


#include "ASTNode.h"
#include "DeclarationList.h"
#include "CodeBlock.h"
#include "Util.h"


namespace naivescript{

class FunctionNode
{
public:
    bool Parse( struct serialize::Function * func, size_t size );

    const std::vector<ASTNode *> GetChildren( void )
    {
        return children;
    }

    std::string GetFuncName(void)
    {
        return func_name;
    }

    DeclarationList * GetParams(void) 
    {
        return static_cast<DeclarationList*>(params_list);
    }

    CodeBlock* GetBody(void)
    {
        return static_cast<CodeBlock*>(body);
    }

    void show( void )
    {
        std::cout <<  "Function\t";
        std::cout << func_name << std::endl;
        for (ASTNode * node : children) {
            node->show();
        }
    }

    llvm::Function* accept(Visitor* v);

    ~FunctionNode() {
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