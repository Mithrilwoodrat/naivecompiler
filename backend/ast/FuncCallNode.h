#ifndef FUNCCALLNODE_H
#define FUNCCALLNODE_H

#include "Expr.h"
#include "Util.h"


namespace naivescript{

class Visitor;

class FuncCallNode : public Expr
{
public:
    FuncCallNode() : Expr(serialize::TypeFuncCall) {}
    virtual bool Parse( struct serialize::FuncCall * func_call, size_t size ) ;

    virtual void show( int offset = 0 ) {
    	std::string index = std::string(offset, '\t');
    	std::cout << index;
        std::cout <<  "FuncCall: " << func_name << std::endl;
        std::cout << "\t";
        args->show(offset + 1);
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

    inline std::string GetFuncName()
    {
        return func_name;
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
