#ifndef NODEFACTORY_H
#define NODEFACTORY_H

#include "ASTNode.h"
#include "stdint.h"

namespace naivescript{

class FunctionNode;

class NodeFactory
{
public:
    static FunctionNode* CreateFunction(uint8_t *data, uint32_t size);
    static ASTNode* CreateCodeBlock(uint8_t *data, uint32_t size);
    static ASTNode* CreateDeclaration(uint8_t *data, uint32_t size);
    static ASTNode* CreateDeclarationList(uint8_t *data, uint32_t size);
    static ASTNode* CreateStmtList(uint8_t *data, uint32_t size);
    static ASTNode* CreateAssignment(uint8_t *data, uint32_t size);
    static ASTNode* CreateIfNode(uint8_t *data, uint32_t size);
    static ASTNode* CreateWhileNode(uint8_t *data, uint32_t size);
    static ASTNode* CreateReturnNode(uint8_t *data, uint32_t size);
    static ASTNode* CreateValue(uint8_t *data, uint32_t size);
    static ASTNode* CreateBinaryOp(uint8_t *data, uint32_t size);
    static ASTNode* CreateSymbol(uint8_t *data, uint32_t size);
};

}

#endif