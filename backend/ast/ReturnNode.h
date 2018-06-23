#ifndef RETURNNODE_H
#define RETURNNODE_H

#include "Statement.h"
#include "Util.h"

namespace naivescript{

class Visitor;

class ReturnNode : public Statement 
{
public:
    ReturnNode() : Statement(serialize::TypeReturnStmt), expr(nullptr) {}
    virtual bool Parse( struct serialize::ReturnStmt * return_stmt, size_t size ) ;

    virtual void show( int offset = 0 ) {
    	std::string index = std::string(offset, '\t');
    	std::cout << index;
        std::cout <<  "Return: ";
        if (expr)
        	expr->show(offset + 1);
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
    	if (expr){
    		free(expr);
    	}
    }
private:
    ASTNode* expr;
    std::vector<ASTNode *> children;
};

}
#endif
