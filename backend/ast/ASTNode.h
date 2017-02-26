#ifndef ASTNODE_H
#define ASTNODE_H

#include "vector"
#include "SerializeStructure.h"


namespace naivescript{
namespace ast {

class Visitor;

class ASTNode 
{
public:
    //virtual bool Parse( uint8_t * data, size_t size ) = 0;
    virtual void visit(Visitor* v);
    virtual void show( void ) = 0;
    virtual const std::vector<ASTNode *>& GetChildren( void ) = 0;
};

}
}
#endif