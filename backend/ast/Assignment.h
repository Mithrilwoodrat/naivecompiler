#ifndef ASSIGNMENT_H
#define ASSIGNMENT_H

#include "ASTNode.h"
#include "iostream"
#include "Util.h"
#include <stdio.h>


namespace naivescript{
namespace ast {

class Assignment : public ASTNode 
{
public:
    virtual bool Parse( struct serialize::Assignment * assignment, size_t size ) 
    {
        return true;
    }

    virtual void show( void) {
        std::cout <<  "Assignment\t";
        //node->show();
    }

    virtual const std::vector<ASTNode *>& GetChildren( void ) 
    {
        children.push_back(expr);
        return children;
    }

private:
    //std::string id;
    std::vector<ASTNode *> children;
    ASTNode* expr;
};

}
}
#endif