#ifndef ASTNODE_H
#define ASTNODE_H

#include "vector"
#include "string"
#include "iostream"
#include "SerializeStructure.h"

namespace llvm{
class Value;
class Function;
}

namespace naivecompiler{

class Visitor;
	 
class ASTNode 
{
public:
    //virtual bool Parse( uint8_t * data, size_t size ) = 0;
    virtual llvm::Value* accept(Visitor* v) = 0;
    virtual void show( int offset = 0 ) = 0;
    virtual const std::vector<ASTNode *> GetChildren( void ) = 0;
    virtual ~ASTNode(){}
};

}
#endif
