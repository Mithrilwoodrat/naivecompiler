#include "NodeVisitor.h"

#include "StmtList.h"
#include "AssignmentNode.h"
#include "ValueNode.h"
#include "BinaryOpNode.h"
#include "SymbolNode.h"

namespace naivecompiler{

llvm::Value* ASTShowVisitor::visit(StmtList * node) {
    node->show();
    return nullptr;
}

llvm::Value* ASTShowVisitor::visit(AssignmentNode *node) {
    node->show();
    return nullptr;
}

llvm::Value* ASTShowVisitor::visit(BinaryOpNode *node) {
    node->show();
    return nullptr;
}

llvm::Value* ASTShowVisitor::visit(SymbolNode *node) {
    node->show();
    return nullptr;
}

llvm::Value* ASTShowVisitor::visit(ValueNode *node) {
    node->show();
    return nullptr;
}

}