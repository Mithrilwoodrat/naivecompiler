#include "NodeFactory.h"
#include "SerializeStructure.h"
#include "AssignmentNode.h"
#include "ValueNode.h"
#include "BinaryOpNode.h"
#include "SymbolNode.h"

#include "Compiler.h"


namespace naivescript{

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

}