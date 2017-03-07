#ifndef NODEVISITOR_H
#define NODEVISITOR_H

#include "NaiveScript.h"

namespace llvm{
class Value;
}

namespace naivescript{

class StmtList;
class AssignmentNode;
class BinaryOpNode;
class SymbolNode;
class ValueNode;


class Visitor
{
  public:
    virtual llvm::Value* visit(StmtList *node) = 0;
    virtual llvm::Value* visit(AssignmentNode *node) = 0;
    virtual llvm::Value* visit(BinaryOpNode *node) = 0;
    virtual llvm::Value* visit(SymbolNode *node) = 0;
    virtual llvm::Value* visit(ValueNode *node) = 0;
};

class ASTShowVisitor : public Visitor
{
    virtual llvm::Value* visit(StmtList *node);
    virtual llvm::Value* visit(AssignmentNode *node);
    virtual llvm::Value* visit(BinaryOpNode *node);
    virtual llvm::Value* visit(SymbolNode *node);
    virtual llvm::Value* visit(ValueNode *node);
};

}

#endif