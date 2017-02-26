#include "NodeVisitor.h"

namespace naivescript{
namespace ast {

void ASTShowVisitor::visit(StmtList * node) {
    node->show();
}

void ASTShowVisitor::visit(AssignmentNode *node) {
    node->show();
}

void ASTShowVisitor::visit(BinaryOpNode *node) {
    node->show();
}

void ASTShowVisitor::visit(SymbolNode *node) {
    node->show();
}

void ASTShowVisitor::visit(ValueNode *node) {
    node->show();
}

}
}