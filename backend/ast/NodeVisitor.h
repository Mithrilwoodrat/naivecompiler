#ifndef NODEVISITOR_H
#define NODEVISITOR_H

#include <stdio.h>
#include <string>
#include <vector>
#include <map>
#include <iostream>
#include <fstream>

namespace llvm{
class Value;
class Function;
}

namespace naivescript{

class FunctionList;
class FunctionNode;
class Declaration;
class DeclarationList;
class StmtList;
class AssignmentNode;
class ReturnNode;
class ArgumentList;
class FuncCallNode;
class BinaryOpNode;
class SymbolNode;
class ValueNode;
class LabelNode;
class ABSJMPNode;
class CMPJMPNode;


class Visitor
{
  public:
    virtual std::map<std::string, llvm::Function*> visit(FunctionList *node) = 0;
    virtual llvm::Function* visit(FunctionNode *node) = 0;
    virtual llvm::Value* visit(Declaration *node) = 0;
    virtual llvm::Value* visit(DeclarationList *node) = 0;
    virtual llvm::Value* visit(StmtList *node) = 0;
    virtual llvm::Value* visit(AssignmentNode *node) = 0;
    virtual llvm::Value* visit(ReturnNode *node) = 0;
    virtual llvm::Value* visit(FuncCallNode *node) = 0;
    virtual llvm::Value* visit(ArgumentList *node) = 0;
    virtual llvm::Value* visit(BinaryOpNode *node) = 0;
    virtual llvm::Value* visit(SymbolNode *node) = 0;
    virtual llvm::Value* visit(ValueNode *node) = 0;
    virtual llvm::Value* visit(LabelNode *node) = 0;
    virtual llvm::Value* visit(ABSJMPNode *node) = 0;
    virtual llvm::Value* visit(CMPJMPNode *node) = 0;
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