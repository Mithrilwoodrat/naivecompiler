#include "CodeGen.h"
#include "ASTNode.h"
#include "FunctionList.h"
#include "Function.h"
#include "Declaration.h"
#include "DeclarationList.h"
#include "CodeBlock.h"
#include "StmtList.h"
#include "AssignmentNode.h"
#include "ValueNode.h"
#include "BinaryOpNode.h"
#include "SymbolNode.h"

namespace naivescript{

llvm::Value *LogErrorV(const char *Str) {
  std::cerr << Str << std::endl;
  return nullptr;
}

void CodeGenVisitor::dump( FunctionList *node) {
    for (Function * f : node->GetChildren() ) {
        llvm::Function * func = f->accept(this);
        if (func) {
            func->dump();
        }
    }
}

std::vector<llvm::Function*> CodeGenVisitor::visit(FunctionList *node)
{
    std::vector<llvm::Function*> funcs;
    for (Function * f : node->GetChildren() ) {
        llvm::Function * func = f->accept(this);
        if (func) {
            funcs.push_back(func);
        }
    }
    return funcs;
}

llvm::Function* CodeGenVisitor::visit(Function *func)
{
    auto decls = func->GetParams()->GetChildren();
    std::vector<std::string> params_names;

    for (ASTNode* decl : decls) {
        params_names.push_back(static_cast<Declaration*>(decl)->GetId());
    }

    std::vector<llvm::Type *> Args(decls.size(),
        llvm::Type::getInt32Ty(TheContext));

    llvm::FunctionType *FT =
      llvm::FunctionType::get(llvm::Type::getInt32Ty(TheContext), Args, false);

    llvm::Function *F =
      llvm::Function::Create(FT, llvm::Function::ExternalLinkage, func->GetFuncName(),
        &TheModule);

    uint32_t Idx = 0;
    for (auto &Arg : F->args()) {
        Arg.setName(params_names[Idx++]);
    }

    llvm::BasicBlock *BB = llvm::BasicBlock::Create(TheContext, "entry", F);
    Builder.SetInsertPoint(BB);
    llvm::Value *retval = func->GetBody()->accept(this);
    Builder.CreateRet(retval);
    return F;
}

llvm::Value* CodeGenVisitor::visit(Declaration *node)
{
    return nullptr;
}
llvm::Value* CodeGenVisitor::visit(DeclarationList *node)
{
    return nullptr;
}

llvm::Value* CodeGenVisitor::visit(CodeBlock *node) 
{
    return node->GetStmts()->accept(this);
}

llvm::Value* CodeGenVisitor::visit(StmtList * stmtlist) {
    llvm::Value* retval = nullptr;
    if ( ! stmtlist->GetChildren().size() ) {
        return LogErrorV("Empty StmtList");
    }
    for (ASTNode * node : stmtlist->GetChildren() ) {
        retval = node->accept(this);
    }
    return retval;
}

llvm::Value* CodeGenVisitor::visit(AssignmentNode *node) {
    std::cout << "Register Symbol: " << node->GetID() <<  std::endl;
    llvm::Value * tmpval = node->GetExpr()->accept(this);
    NamedValues[node->GetID()] = tmpval;
    return tmpval;
}

llvm::Value* CodeGenVisitor::visit(BinaryOpNode *node) {
  llvm::Value *L = node->GetLHS()->accept(this);
  llvm::Value *R = node->GetRHS()->accept(this);
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

llvm::Value* CodeGenVisitor::visit(SymbolNode *node) {
    std::string symbol = node->GetSymbol();
    std::cout << "Use Of Symbol: " << symbol <<  std::endl;
    if (!NamedValues.count(symbol)) {
        return LogErrorV("Using Uninitialize Variable");
    }
    return NamedValues.at(node->GetSymbol());
}

llvm::Value* CodeGenVisitor::visit(ValueNode *node) {
    //llvm::Value* tmp = ConstantFP::get(TheContext, APFloat(static_cast<float>(node->GetVal())));
    llvm::Value* tmp = llvm::ConstantInt::get(TheContext, llvm::APInt(32, node->GetVal(), false));
    //tmp->dump();
    return tmp;
}

}