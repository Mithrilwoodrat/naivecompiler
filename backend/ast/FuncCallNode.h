#ifndef FUNCCALLNODE_H
#define FUNCCALLNODE_H

#include "NaiveScript.h"
#include "Statement.h"
#include "Util.h"


namespace naivescript{

class Visitor;

class FuncCallNode : public Statement 
{
public:
    FuncCallNode() : Statement(serialize::TypeFuncCall) {}
    virtual bool Parse( struct serialize::FuncCall * func_call, size_t size ) ;

    virtual void show( void ) {
        std::cout <<  "FuncCall: " << func_name;
        args->show();
        std::cout << std::endl;
    }

    virtual const std::vector<ASTNode *> GetChildren( void ) 
    {
        children.push_back(args);
        return children;
    }
    
    virtual llvm::Value* accept(Visitor* v);

    inline ASTNode* GetArgs( void )  {
        return args;
    }

    ~FuncCallNode()
    { 
        free(args);
    }
private:
    ASTNode* args;
    std::string func_name;
    std::vector<ASTNode *> children;
};

}
#endif