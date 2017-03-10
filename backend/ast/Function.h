#ifndef FUNCTION_H
#define FUNCTION_H

#include "NaiveScript.h"
#include "ASTNode.h"
#include "DeclarationList.h"
#include "CodeBlock.h"
#include "Util.h"


namespace naivescript{

class Function : public ASTNode
{
public:
    virtual bool Parse( struct serialize::Function * func, size_t size );

    virtual const std::vector<ASTNode *> GetChildren( void ) override
    {
        return children;
    }

    virtual void show( void ) override
    {
        std::cout <<  "Function\t";
        std::cout << func_name << std::endl;
        for (ASTNode * node : children) {
            node->show();
        }
    }

    virtual llvm::Value* accept(Visitor* v) override;

    ~Function() {
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