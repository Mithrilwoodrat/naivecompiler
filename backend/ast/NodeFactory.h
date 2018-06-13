#ifndef NODEFACTORY_H
#define NODEFACTORY_H

#include "ASTNode.h"
#include "stdint.h"

namespace naivescript{

class FunctionNode;

class NodeFactory
{
public:
    static ASTNode* CreateFuncDef(uint8_t *data, uint32_t size);
    static ASTNode* CreateFuncDecl(uint8_t *data, uint32_t size);
    static ASTNode* CreateDeclaration(uint8_t *data, uint32_t size);
    static ASTNode* CreateDeclarationList(uint8_t *data, uint32_t size);
    static ASTNode* CreateStmtList(uint8_t *data, uint32_t size);
    static ASTNode* CreateAssignment(uint8_t *data, uint32_t size);
    static ASTNode* CreateReturnNode(uint8_t *data, uint32_t size);
    static ASTNode* CreateFuncCallNode(uint8_t *data, uint32_t size);
    static ASTNode* CreateArgumentList(uint8_t *data, uint32_t size);
    static ASTNode* CreateValue(uint8_t *data, uint32_t size);
    static ASTNode* CreateBinaryOp(uint8_t *data, uint32_t size);
    static ASTNode* CreateSymbol(uint8_t *data, uint32_t size);
    static ASTNode* CreateLabelNode(uint8_t *data, uint32_t size);
    static ASTNode* CreateABSJMPNode(uint8_t *data, uint32_t size);
    static ASTNode* CreateCMPJMPNode(uint8_t *data, uint32_t size);
};

}

#endif
