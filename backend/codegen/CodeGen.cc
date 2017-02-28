#include "CodeGen.h"
#include "ASTNode.h"
#include "StmtList.h"
#include "AssignmentNode.h"
#include "ValueNode.h"
#include "BinaryOpNode.h"
#include "SymbolNode.h"

namespace naivescript{

Value *LogErrorV(const char *Str) {
  std::cerr << Str << std::endl;
  return nullptr;
}

void CodeGenVisitor::dump( StmtList *node) {
        Value * val = node->accept(this);
        val->dump();
}

Value* CodeGenVisitor::visit(StmtList * stmtlist) {
    Value* retval;
    for (ASTNode * node : stmtlist->GetChildren()) {
        retval = node->accept(this);
    }
    return retval;
}

Value* CodeGenVisitor::visit(AssignmentNode *node) {
    Value * tmpval = node->GetExpr()->accept(this);
    std::cout << "Register Symbol:" << node->GetID() <<  std::endl;
    NamedValues[node->GetID()] = tmpval;
    return tmpval;
}

Value* CodeGenVisitor::visit(BinaryOpNode *node) {
  Value *L = node->GetLHS()->accept(this);
  Value *R = node->GetRHS()->accept(this);
  if (!L || !R)
    return nullptr;

  switch (node->GetOp()) {
  case '+':
    return Builder.CreateAdd(L, R, "addtmp");
  case '-':
    return Builder.CreateSub(L, R, "subtmp");
  case '*':
    return Builder.CreateMul(L, R, "multmp");
  default:
    return LogErrorV("invalid binary operator");
  }
}

Value* CodeGenVisitor::visit(SymbolNode *node) {
    std::string symbol = node->GetSymbol();
    std::cout << "Use Of Symbol" << symbol <<  std::endl;
    if (!NamedValues.count(symbol)) {
        return LogErrorV("Using Uninitialize Variable");
    }
    return NamedValues.at(node->GetSymbol());
}

Value* CodeGenVisitor::visit(ValueNode *node) {
    Value* tmp = ConstantInt::get(TheContext, APInt(/*nbits*/32, node->GetVal(), /*bool*/true));
    tmp->dump();
    return tmp;
    //return ConstantFP::get(TheContext, APFloat());
}

}