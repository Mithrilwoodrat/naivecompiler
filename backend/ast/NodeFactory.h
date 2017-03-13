#ifndef NODEFACTORY_H
#define NODEFACTORY_H

#include "ASTNode.h"
#include "stdint.h"

namespace naivescript{

class Function;

class NodeFactory
{
public:
    static Function* CreateFunction(uint8_t *data, uint32_t size);
    static ASTNode* CreateCodeBlock(uint8_t *data, uint32_t size);
    static ASTNode* CreateDeclaration(uint8_t *data, uint32_t size);
    static ASTNode* CreateDeclarationList(uint8_t *data, uint32_t size);
    static ASTNode* CreateStmtList(uint8_t *data, uint32_t size);
    static ASTNode* CreateAssignment(uint8_t *data, uint32_t size);
    static ASTNode* CreateValue(uint8_t *data, uint32_t size);
    static ASTNode* CreateBinaryOp(uint8_t *data, uint32_t size);
    static ASTNode* CreateSymbol(uint8_t *data, uint32_t size);
};

}

#endif