#ifndef ASSIGNMENT_H
#define ASSIGNMENT_H

#include "Statement.h"
#include "Util.h"


namespace naivescript{

class Visitor;

class AssignmentNode : public Statement 
{
public:
    AssignmentNode() : Statement(serialize::TypeAssignmentExpr) {}
    virtual bool Parse( struct serialize::Assignment * assignment, size_t size ) ;

    virtual void show( int offset = 0 ) {
    	std::string index = std::string(offset, '\t');
    	std::cout << index;
        std::cout <<  "Assignment: ID: " << id << " = ";
        expr->show(offset+1);
        std::cout << std::endl;
    }

    virtual const std::vector<ASTNode *> GetChildren( void ) 
    {
        children.push_back(expr);
        return children;
    }
    
    virtual llvm::Value* accept(Visitor* v);

    inline const std::string& GetID( void ) const {
        return id;
    }

    inline ASTNode* GetExpr( void )  {
        return expr;
    }

    ~AssignmentNode()
    { 
        free(expr);
    }
private:
    std::string id;
    std::vector<ASTNode *> children;
    ASTNode* expr;
};

}
#endif
