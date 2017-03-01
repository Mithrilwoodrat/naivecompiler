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
#include <cctype>
#include <cstdio>
#include <cstdlib>
#include <map>
#include <memory>
#include <string>
#include <vector>

using namespace llvm;

namespace naivescript{
static    LLVMContext TheContext;
static    IRBuilder<> Builder(TheContext);
static    std::unique_ptr<Module> TheModule;
class StmtList;
class AssignmentNode;
class BinaryOpNode;
class SymbolNode;
class ValueNode;

class CodeGenVisitor : public Visitor
{
public:
    void dump( StmtList *node);
    virtual Value* visit(StmtList *node);
    virtual Value* visit(AssignmentNode *node);
    virtual Value* visit(BinaryOpNode *node);
    virtual Value* visit(SymbolNode *node);
    virtual Value* visit(ValueNode *node);
private:
    std::map<std::string, Value *> NamedValues;
};
}
#endif