#ifndef ASSIGNMENT_H
#define ASSIGNMENT_H

#include "NaiveScript.h"
#include "ASTNode.h"
#include "Util.h"

#include "ValueNode.h"


namespace naivescript{
namespace ast {

class ExprFactory
{
public:
    static ASTNode * CreateValue(uint8_t *data, size_t size) {
        ValueNode *node = new ValueNode();
        node->Parse(reinterpret_cast<struct serialize::Value*>(data), size);
        return node;
    }
};

class AssignmentNode : public ASTNode 
{
public:
    virtual bool Parse( struct serialize::Assignment * assignment, size_t size ) ;

    virtual void show( void) {
        std::cout <<  "Assignment\t";
        //expr->show();
    }

    virtual const std::vector<ASTNode *>& GetChildren( void ) 
    {
        children.push_back(expr);
        return children;
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
}
#endif
