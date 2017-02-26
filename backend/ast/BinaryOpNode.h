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
    BinaryOpNode() : lhs(NULL), rhs(NULL) {}
    virtual bool Parse( struct serialize::BinaryOp * binaryop, size_t size );

    virtual void show( void ) 
    {
        std::cout << "BinaryOp: ";
        lhs->show();
        std::cout << "\t OP: " << op << "\t";
        rhs->show();
    }

    virtual const std::vector<ASTNode *>& GetChildren( void ) 
    {
        children.push_back(lhs);
        children.push_back(rhs);
        return children;
    }

    virtual void accept(Visitor* v);

    ~BinaryOpNode() 
    {
        if (lhs) {
            free(lhs);
        }
        if (rhs) {
            free(rhs);
        }
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