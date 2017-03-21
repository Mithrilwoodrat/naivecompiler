#include "CodeGen.h"
#include "ASTNode.h"
#include "Statement.h"
#include "FunctionList.h"
#include "FunctionNode.h"
#include "Declaration.h"
#include "DeclarationList.h"
#include "CodeBlock.h"
#include "StmtList.h"
#include "AssignmentNode.h"
#include "ReturnNode.h"
#include "ValueNode.h"
#include "BinaryOpNode.h"
#include "SymbolNode.h"

namespace naivescript{

llvm::Value *LogErrorV(const char *Str) {
  std::cerr << Str << std::endl;
  return nullptr;
}

void CodeGenVisitor::dump( FunctionList *node) {
    for (FunctionNode * f : node->GetChildren() ) {
        llvm::Function * func = f->accept(this);
        if (func) {
            func->dump();
        }
    }
}

void CodeGenVisitor::run(FunctionList *node)
{
    auto funcs = node->accept(this);
    TheModule->dump();
    LLVMInitializeNativeTarget();
    LLVMInitializeNativeAsmPrinter();
    LLVMInitializeNativeAsmParser();
    //std::unique_ptr<llvm::Module> mod = llvm::make_unique<llvm::Module>(TheModule);
    llvm::ExecutionEngine *engine = llvm::EngineBuilder(std::move(owner)).create();
    engine->finalizeObject(); // memory for generated code marked executable:
    for (const auto &f : funcs ) {
        if (f.first == "main") {
            if (f.second)
                engine->runFunction(f.second, std::vector<llvm::GenericValue>());
        }
    }
}

std::map<std::string, llvm::Function*> CodeGenVisitor::visit(FunctionList *node)
{
    std::map<std::string, llvm::Function*> funcs;
    for (FunctionNode * f : node->GetChildren() ) {
        auto * func = f->accept(this);
        if (func) {
            funcs[f->GetFuncName()] = func;
        }
    }
    return funcs;
}

llvm::Function* CodeGenVisitor::visit(FunctionNode *func)
{
    auto decls = func->GetParams()->GetChildren();
    std::vector<std::string> params_names;

    for (ASTNode* decl : decls) {
        params_names.push_back(static_cast<Declaration*>(decl)->GetID());
    }

    std::vector<llvm::Type *> Args(decls.size(),
        llvm::Type::getInt32Ty(TheContext));

    llvm::FunctionType *FT =
      llvm::FunctionType::get(llvm::Type::getInt32Ty(TheContext), Args, false);

    llvm::Function *TheFunction =
      llvm::Function::Create(FT, llvm::Function::ExternalLinkage, func->GetFuncName(),
        TheModule);
        
    llvm::BasicBlock *BB = llvm::BasicBlock::Create(TheContext, "entry", TheFunction);
    Builder.SetInsertPoint(BB);

    uint32_t Idx = 0;
    for (auto &Arg : TheFunction->args()) {
        Arg.setName(params_names[Idx++]);
        llvm::IRBuilder<> TmpB(&TheFunction->getEntryBlock(),
            TheFunction->getEntryBlock().begin());
        llvm::AllocaInst *Alloca =  TmpB.CreateAlloca(llvm::Type::getInt32Ty(TheContext), nullptr, Arg.getName());
        Builder.CreateStore(&Arg, Alloca);
        // Add arguments to variable symbol table.
        NamedValues[Arg.getName()] = Alloca;
    }

    
    llvm::Value *retval = func->GetBody()->accept(this);
    Builder.CreateRet(retval);
    return TheFunction;
}

llvm::Value* CodeGenVisitor::visit(Declaration *node)
{
    llvm::Function *TheFunction = Builder.GetInsertBlock()->getParent();
    llvm::IRBuilder<> TmpB(&TheFunction->getEntryBlock(),
                   TheFunction->getEntryBlock().begin());
    llvm::AllocaInst *Alloca =  TmpB.CreateAlloca(llvm::Type::getInt32Ty(TheContext), nullptr, node->GetID());
    NamedValues[node->GetID()] = Alloca;
    return nullptr;
}

llvm::Value* CodeGenVisitor::visit(DeclarationList *node)
{
    if ( ! node->GetChildren().size() ) {
        return LogErrorV("Empty StmtList");
    }
    for (auto decl : node->GetChildren()) {
        decl->accept(this);
    }
    return nullptr;
}

llvm::Value* CodeGenVisitor::visit(CodeBlock *node) 
{
    node->GetDecls()->accept(this);
    return node->GetStmts()->accept(this);
}

llvm::Value* CodeGenVisitor::visit(StmtList * stmtlist) {
    llvm::Value* retval = nullptr;
    if ( ! stmtlist->GetChildren().size() ) {
        return LogErrorV("Empty StmtList");
    }
    for (ASTNode * node : stmtlist->GetChildren() ) {
        Statement* stmt = static_cast<Statement *>(node);
        if (stmt->GetNodeType() == serialize::TypeReturnStmt) {
            return stmt->accept(this);
        } else {
            stmt->accept(this);
        }
    }
    return retval;
}

llvm::Value* CodeGenVisitor::visit(AssignmentNode *node) {
    std::cout << "Assignment Var: " << node->GetID() <<  std::endl;
    llvm::Value * tmpval = node->GetExpr()->accept(this);
    auto Variable = NamedValues.at(node->GetID());
    Builder.CreateStore(tmpval, Variable);
    return tmpval;
}

llvm::Value* CodeGenVisitor::visit(ReturnNode *node) {
    llvm::Value * tmpval = node->GetExpr()->accept(this);
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
    std::cout << "Use Of Var: " << symbol <<  std::endl;
    if (!NamedValues.count(symbol)) {
        return LogErrorV("Using Uninitialize Variable");
    }
    auto Val = NamedValues.at(symbol);
    return Builder.CreateLoad(Val, symbol);
}

llvm::Value* CodeGenVisitor::visit(ValueNode *node) {
    //llvm::Value* tmp = ConstantFP::get(TheContext, APFloat(static_cast<float>(node->GetVal())));
    llvm::Value* tmp = llvm::ConstantInt::get(TheContext, llvm::APInt(32, node->GetVal(), false));
    //tmp->dump();
    return tmp;
}

}