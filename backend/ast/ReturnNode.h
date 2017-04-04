#ifndef RETURNNODE_H
#define RETURNNODE_H

#include "NaiveScript.h"
#include "Statement.h"
#include "Util.h"

#include "ValueNode.h"
#include "BinaryOpNode.h"


namespace naivescript{

class Visitor;

class ReturnNode : public Statement 
{
public:
    ReturnNode() : Statement(serialize::TypeReturnStmt) {}
    virtual bool Parse( struct serialize::ReturnStmt * return_stmt, size_t size ) ;

    virtual void show( void ) {
        std::cout <<  "Return: ";
        expr->show();
        std::cout << std::endl;
    }

    virtual const std::vector<ASTNode *> GetChildren( void ) 
    {
        children.push_back(expr);
        return children;
    }
    
    virtual llvm::Value* accept(Visitor* v);

    inline ASTNode* GetExpr( void )  {
        return expr;
    }

    ~ReturnNode()
    { 
        free(expr);
    }
private:
    ASTNode* expr;
    std::vector<ASTNode *> children;
};

}
#endif