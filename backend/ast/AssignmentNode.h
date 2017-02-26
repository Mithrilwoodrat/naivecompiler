#ifndef ASSIGNMENT_H
#define ASSIGNMENT_H

#include "NaiveScript.h"
#include "ASTNode.h"
#include "Util.h"

#include "ValueNode.h"
#include "BinaryOpNode.h"


namespace naivescript{
namespace ast {

class Visitor;

class AssignmentNode : public ASTNode 
{
public:
    virtual bool Parse( struct serialize::Assignment * assignment, size_t size ) ;

    virtual void show( void ) {
        std::cout <<  "Assignment: ID: " << id << " = ";
        expr->show();
        std::cout << std::endl;
    }

    virtual const std::vector<ASTNode *>& GetChildren( void ) 
    {
        children.push_back(expr);
        return children;
    }
    
    virtual void accept(Visitor* v);

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
}
#endif
