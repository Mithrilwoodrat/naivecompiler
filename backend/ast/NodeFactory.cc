#include "NodeFactory.h"
#include "SerializeStructure.h"
#include "AssignmentNode.h"
#include "ValueNode.h"
#include "BinaryOpNode.h"
#include "SymbolNode.h"
#include "Function.h"
#include "Declaration.h"
#include "DeclarationList.h"
#include "CodeBlock.h"
#include "StmtList.h"
#include "Compiler.h"


namespace naivescript{

ASTNode * NodeFactory::CreateStmtList(uint8_t *data, uint32_t size) {
    StmtList *node = new StmtList();
    node->Parse(reinterpret_cast<struct serialize::StmtList*>(data), size);
    return node;
}

ASTNode * NodeFactory::CreateAssignment(uint8_t *data, uint32_t size) {
    AssignmentNode *node = new AssignmentNode();
    node->Parse(reinterpret_cast<struct serialize::Assignment*>(data), size);
    return node;
}

ASTNode * NodeFactory::CreateValue(uint8_t *data, uint32_t size) {
    ValueNode *node = new ValueNode();
    node->Parse(reinterpret_cast<struct serialize::Value*>(data), size);
    return node;
}

ASTNode * NodeFactory::CreateBinaryOp(uint8_t *data, uint32_t size) {
    BinaryOpNode *node = new BinaryOpNode();
    node->Parse(reinterpret_cast<struct serialize::BinaryOp*>(data), size);
    return node;
}

ASTNode* NodeFactory::CreateSymbol(uint8_t *data, uint32_t size) {
    SymbolNode *node = new SymbolNode();
    node->Parse(reinterpret_cast<struct serialize::Symbol*>(data), size);
    return node;
}

ASTNode* NodeFactory::CreateFunction(uint8_t *data, uint32_t size)
{
    auto *node = new Function();
    node->Parse(reinterpret_cast<struct serialize::Function*>(data), size);
    return node;
}

ASTNode* NodeFactory::CreateCodeBlock(uint8_t *data, uint32_t size)
{
    auto *node = new CodeBlock();
    node->Parse(reinterpret_cast<struct serialize::CodeBlock*>(data), size);
    return node;
}

ASTNode* NodeFactory::CreateDeclaration(uint8_t *data, uint32_t size)
{
    auto *node = new Declaration();
    node->Parse(reinterpret_cast<struct serialize::Declaration*>(data), size);
    return node;
}

ASTNode* NodeFactory::CreateDeclarationList(uint8_t *data, uint32_t size)
{
    auto *node = new DeclarationList();
    node->Parse(reinterpret_cast<struct serialize::DeclarationList*>(data), size);
    return node;
}

}