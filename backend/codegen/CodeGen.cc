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
#include "WhileNode.h"
#include "IfNode.h"
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
        
    llvm::BasicBlock *Entry = llvm::BasicBlock::Create(TheContext, "entry", TheFunction);
    Builder.SetInsertPoint(Entry);

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
    func->GetBody()->accept(this);
    //llvm::Value *retval = func->GetBody()->accept(this);
    // llvm::BasicBlock *End = llvm::BasicBlock::Create(TheContext, "End", TheFunction);
    // Builder.SetInsertPoint(End);
    //Builder.CreateRet(retval);
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
    node->GetStmts()->accept(this);
    return nullptr;
}

llvm::Value* CodeGenVisitor::visit(StmtList * stmtlist) {
    llvm::Value* retval = llvm::Constant::getNullValue(llvm::Type::getInt32Ty(TheContext));
    if ( ! stmtlist->GetChildren().size() ) {
        return LogErrorV("Empty StmtList");
    }
    for (ASTNode * node : stmtlist->GetChildren() ) {
        Statement* stmt = static_cast<Statement *>(node);
        serialize::NodeType type = stmt->GetNodeType();
        jumpTable tb;
        switch(type) {
            case serialize::TypeReturnStmt:
                return stmt->accept(this);
                break;
            case serialize::TypeBreakStmt:
                tb = BlockStack.top();
                Builder.CreateBr(tb.end);
                return retval;
                break;
            case serialize::TypeContinueStmt:
                tb = BlockStack.top();
                Builder.CreateBr(tb.start);
                return retval;
                break;
            default:
                stmt->accept(this);
                break;
        }
    }
    return retval;
}

// llvm::Value* CodeGenVisitor::visit(WhileNode *node) 
// {
//     auto ParentBlock = Builder.GetInsertBlock()->getParent();
//     llvm::BasicBlock *LoopBB = llvm::BasicBlock::Create(TheContext, "loop", ParentBlock);
//     llvm::Value* EndCond = node->GetCond()->accept(this);
//     EndCond = Builder.CreateICmpNE(EndCond,
//         llvm::ConstantInt::get(TheContext, llvm::APInt(32, 0, false)));
//     llvm::BasicBlock *AfterBB = llvm::BasicBlock::Create(TheContext, "afterloop", ParentBlock);
//     jumpTable tb;
//     tb.start = LoopBB;
//     tb.end = AfterBB;
//     BlockStack.push(tb);
//     Builder.CreateCondBr(EndCond, LoopBB, AfterBB);
//     Builder.SetInsertPoint(LoopBB);
//     node->GetBody()->accept(this);
//     EndCond = node->GetCond()->accept(this);
//     EndCond = Builder.CreateICmpNE(EndCond,
//         llvm::ConstantInt::get(TheContext, llvm::APInt(32, 0, false)));
//     Builder.CreateCondBr(EndCond, LoopBB, AfterBB);
//     Builder.SetInsertPoint(AfterBB);
//     BlockStack.pop();
//     return nullptr;
// }

// llvm::Value* CodeGenVisitor::visit(IfNode *node) 
// {
//     auto ParentBlock = Builder.GetInsertBlock()->getParent();
//     llvm::Value* Cond = node->GetCond()->accept(this);
//     //auto zero = llvm::ConstantInt::get(TheContext, llvm::APInt(32, 0, false));
//     //printf("%d, %d\n", Cond->getType()->isIntegerTy(), zero->getType()->isIntegerTy());
//     Cond = Builder.CreateIntCast(Cond, llvm::Type::getInt32Ty(TheContext), false);
//     Cond = Builder.CreateICmpNE(Cond,
//         llvm::ConstantInt::get(TheContext, llvm::APInt(32, 0, false)));
//     llvm::BasicBlock *ThenBB = llvm::BasicBlock::Create(TheContext, "then", ParentBlock);
//     llvm::BasicBlock *ElseBB = llvm::BasicBlock::Create(TheContext, "else");
//     llvm::BasicBlock *IfBB = llvm::BasicBlock::Create(TheContext, "if");
//     llvm::Value *ThenV, *ElseV=llvm::Constant::getNullValue(llvm::Type::getInt32Ty(TheContext));
//     Builder.CreateCondBr(Cond, ThenBB, ElseBB);
//     Builder.SetInsertPoint(ThenBB);
//     ThenV = node->GetThen()->accept(this);
//     bool hasJmp = false;
//     for (ASTNode * n : node->GetThen()->GetChildren()) {
//         Statement* stmt = static_cast<Statement *>(n);
//         serialize::NodeType type = stmt->GetNodeType();
//         if (type == serialize::TypeReturnStmt || 
//             type == serialize::TypeBreakStmt ||
//             type == serialize::TypeContinueStmt) {
//                 hasJmp = true;
//             }

//     }
//     if (!hasJmp) {
//         Builder.CreateBr(IfBB);
//     }
//     ThenBB = Builder.GetInsertBlock();
//     ParentBlock->getBasicBlockList().push_back(ElseBB);
//     Builder.SetInsertPoint(ElseBB);
//     if (node->GetElse()) {
//         ElseV = node->GetElse()->accept(this);
//     }
//     Builder.CreateBr(IfBB);
//     ElseBB = Builder.GetInsertBlock();
//     ParentBlock->getBasicBlockList().push_back(IfBB);
//     Builder.SetInsertPoint(IfBB);
//     // llvm::PHINode *PN = Builder.CreatePHI(llvm::Type::getInt32Ty(TheContext), 2, "iftmp");
//     // if (ThenV)
//     //     PN->addIncoming(ThenV, ThenBB);
//     // if (ElseV)
//     //     PN->addIncoming(ElseV, ElseBB);
//     return nullptr;
// }

llvm::Value* CodeGenVisitor::visit(AssignmentNode *node) 
{
    std::cout << "Assignment Var: " << node->GetID() <<  std::endl;
    llvm::Value * tmpval = node->GetExpr()->accept(this);
    auto Variable = NamedValues.at(node->GetID());
    Builder.CreateStore(tmpval, Variable);
    return tmpval;
}

llvm::Value* CodeGenVisitor::visit(ReturnNode *node) 
{
    llvm::Value * retval = node->GetExpr()->accept(this);
    Builder.CreateRet(retval);
    return retval;
}

llvm::Value* CodeGenVisitor::visit(BinaryOpNode *node) 
{
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
  case '>':
    L = Builder.CreateICmpUGT(L, R, "cmptmp");
    L->dump();
    return L;
  case '<':
    L = Builder.CreateICmpULT(L, R, "cmptmp");
    L->dump();
    return L;
  default:
    return LogErrorV("invalid binary operator");
  }
}

llvm::Value* CodeGenVisitor::visit(SymbolNode *node) 
{
    std::string symbol = node->GetSymbol();
    std::cout << "Use Of Var: " << symbol <<  std::endl;
    if (!NamedValues.count(symbol)) {
        return LogErrorV("Using Uninitialize Variable");
    }
    auto Val = NamedValues.at(symbol);
    return Builder.CreateLoad(Val, symbol);
}

llvm::Value* CodeGenVisitor::visit(ValueNode *node)
{
    //llvm::Value* tmp = ConstantFP::get(TheContext, APFloat(static_cast<float>(node->GetVal())));
    llvm::Value* tmp = llvm::ConstantInt::get(TheContext, llvm::APInt(32, node->GetVal(), false));
    //tmp->dump();
    return tmp;
}

}