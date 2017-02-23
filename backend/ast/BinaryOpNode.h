#ifndef BINARYOPNODE_H
#define BINARYOPNODE_H


#include "NaiveScript.h"
#include "ASTNode.h"
#include "Util.h"


namespace naivescript{
namespace ast {

class BinaryOpNode : public ASTNode
{
public:
    virtual bool Parse( struct serialize::BinaryOp * binaryop, size_t size );

    virtual void show( void) {
        std::cout <<  "BinaryOp\t";
    }

    virtual const std::vector<ASTNode *>& GetChildren( void ) 
    {
        children.push_back(lhs);
        children.push_back(rhs);
        return children;
    }
    
private:
    ASTNode * lhs;
    std::string op;
    ASTNode * rhs;
    std::vector<ASTNode *> children;
};

}
}
#endif