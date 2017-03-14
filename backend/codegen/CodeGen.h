#ifndef CODEGEN_H
#define CODEGEN_H

#include "NaiveScript.h"
#include "NodeVisitor.h"
#include "llvm/ADT/APInt.h"
#include "llvm/ADT/APFloat.h"
#include "llvm/ADT/STLExtras.h"
#include "llvm/IR/BasicBlock.h"
#include "llvm/IR/Constants.h"
#include "llvm/IR/DerivedTypes.h"
#include "llvm/IR/Function.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/LLVMContext.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/Type.h"
#include "llvm/IR/Verifier.h"
#include <llvm/ExecutionEngine/ExecutionEngine.h>
#include <llvm/ExecutionEngine/GenericValue.h>
#include <llvm/ExecutionEngine/MCJIT.h>
#include <llvm/Support/TargetSelect.h>
#include <cctype>
#include <cstdio>
#include <cstdlib>
#include <map>
#include <memory>
#include <string>
#include <vector>

namespace naivescript{
static  llvm::LLVMContext TheContext;
static  llvm::IRBuilder<> Builder(TheContext);
static  std::unique_ptr<llvm::Module> owner = llvm::make_unique<llvm::Module>("naivescript", TheContext);
static  llvm::Module *TheModule = owner.get();
//static    llvm::Module TheModule("naivescript", TheContext);

class FunctionList;
class FunctionNode;
class Declaration;
class DeclarationList;
class CodeBlock;
class StmtList;
class AssignmentNode;
class BinaryOpNode;
class SymbolNode;
class ValueNode;

class CodeGenVisitor : public Visitor
{
public:
    void dump( FunctionList *node);
    void run( FunctionList *node );
    virtual std::map<std::string, llvm::Function*> visit(FunctionList *node);
    virtual llvm::Function* visit(FunctionNode *node);
    virtual llvm::Value* visit(Declaration *node);
    virtual llvm::Value* visit(DeclarationList *node);
    virtual llvm::Value* visit(CodeBlock *node);
    virtual llvm::Value* visit(StmtList *node);
    virtual llvm::Value* visit(AssignmentNode *node);
    virtual llvm::Value* visit(BinaryOpNode *node);
    virtual llvm::Value* visit(SymbolNode *node);
    virtual llvm::Value* visit(ValueNode *node);
private:
    std::map<std::string, llvm::Value *> NamedValues;
};
}
#endif