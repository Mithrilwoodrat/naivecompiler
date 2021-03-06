#include "NodeFactory.h"
#include "SerializeStructure.h"
#include "AssignmentNode.h"
#include "ReturnNode.h"
#include "ValueNode.h"
#include "BinaryOpNode.h"
#include "SymbolNode.h"
#include "FuncDefNode.h"
#include "FuncDeclNode.h"
#include "FuncCallNode.h"
#include "ArgumentList.h"
#include "Declaration.h"
#include "DeclarationList.h"
#include "Statement.h"
#include "StmtList.h"


namespace naivecompiler{

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

ASTNode * NodeFactory::CreateLabelNode(uint8_t *data, uint32_t size) {
    LabelNode *node = new LabelNode();
    node->Parse(reinterpret_cast<struct serialize::Label*>(data), size);
    return node;
}

ASTNode * NodeFactory::CreateABSJMPNode(uint8_t *data, uint32_t size) {
    ABSJMPNode *node = new ABSJMPNode();
    node->Parse(reinterpret_cast<struct serialize::ABSJMP*>(data), size);
    return node;
}

ASTNode * NodeFactory::CreateCMPJMPNode(uint8_t *data, uint32_t size) {
    CMPJMPNode *node = new CMPJMPNode();
    node->Parse(reinterpret_cast<struct serialize::CMPJMP*>(data), size);
    return node;
}

ASTNode* NodeFactory::CreateReturnNode(uint8_t *data, uint32_t size)
{
    ReturnNode *node = new ReturnNode();
    node->Parse(reinterpret_cast<struct serialize::ReturnStmt*>(data), size);
    return node;
}

ASTNode * NodeFactory::CreateValue(uint8_t *data, uint32_t size) {
	//ASTNode *node = nullptr;
	struct serialize::Value* value = reinterpret_cast<struct serialize::Value*>(data);
	uint32_t valuetype = value->valuetype;
	bool parse_ret;
	switch (valuetype) {
	case serialize::ValueType::CONSTINT: {
		IntegerNode* node = (IntegerNode*) new IntegerNode();
		parse_ret = node->Parse(value, size);
		if (parse_ret == false) {
			std::cerr << "Parsing Value Failed" << std::endl;
		}
		//node = static_cast<ValueNode *>(node);
		return node;
	}
	case serialize::ValueType::CONSTSTRING: {
		StringLiteralNode* node2 = (StringLiteralNode*) new StringLiteralNode();
		node2->Parse(value, size);
		//node = static_cast<ValueNode *>(node);
		return node2;
	}
	}
    return nullptr;
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

ASTNode * NodeFactory::CreateFuncDecl(uint8_t *data, uint32_t size)
{
    auto *node = new FuncDeclNode();
    node->Parse(reinterpret_cast<struct serialize::FuncDecl*>(data), size);
    return node;
}

ASTNode * NodeFactory::CreateFuncDef(uint8_t *data, uint32_t size)
{
    auto *node = new FuncDefNode();
    node->Parse(reinterpret_cast<struct serialize::FuncDef*>(data), size);
    return node;
}

ASTNode* NodeFactory::CreateFuncCallNode(uint8_t *data, uint32_t size)
{
    auto *node = new FuncCallNode();
    node->Parse(reinterpret_cast<struct serialize::FuncCall*>(data), size);
    return node;
}

ASTNode* NodeFactory::CreateArgumentList(uint8_t *data, uint32_t size)
{
    auto *node = new ArgumentList();
    node->Parse(reinterpret_cast<struct serialize::ArgumentList*>(data), size);
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
