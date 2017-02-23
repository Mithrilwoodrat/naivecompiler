#ifndef ASTNODE_H
#define ASTNODE_H

#include "vector"
#include "SerializeStructure.h"

namespace naivescript{
namespace ast {


class Visitor
{
  public:
    virtual void visit(void *) = 0;
};

class ASTNode 
{
public:
    //virtual bool Parse( uint8_t * data, size_t size ) = 0;
    virtual void visit(Visitor* v) {
        v->visit(this);
    }
    virtual void show( void ) = 0;
    virtual const std::vector<ASTNode *>& GetChildren( void ) = 0;
};

}
}
#endif