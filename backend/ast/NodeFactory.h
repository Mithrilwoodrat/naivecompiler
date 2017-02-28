#ifndef NODEFACTORY_H
#define NODEFACTORY_H

#include "ASTNode.h"
#include "stdint.h"

namespace naivescript{

class NodeFactory
{
public:
    static ASTNode * CreateAssignment(uint8_t *data, uint32_t size);
    static ASTNode * CreateValue(uint8_t *data, uint32_t size);
    static ASTNode * CreateBinaryOp(uint8_t *data, uint32_t size);
    static ASTNode* CreateSymbol(uint8_t *data, uint32_t size);
};

}

#endif