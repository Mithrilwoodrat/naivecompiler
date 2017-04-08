#ifndef CODEGEN_H
#define CODEGEN_H

#include "NodeVisitor.h"
#include <cctype>
#include <cstdio>
#include <cstdlib>
#include <map>
#include <memory>
#include <iostream>
#include <string>
#include <vector>
#include <stack>

namespace llvm {
    class AllocaInst;
    class BasicBlock;
}

namespace naivescript{
//static    llvm::Module TheModule("naivescript", TheContext);

class CodeGenVisitor : public Visitor
{
public:
    void dump( FunctionList *node);
    void run( FunctionList *node );
    void GenObj(const std::string & Filename);
    virtual std::map<std::string, llvm::Function*> visit(FunctionList *node);
    virtual llvm::Function* visit(FunctionNode *node);
    virtual llvm::Value* visit(Declaration *node);
    virtual llvm::Value* visit(DeclarationList *node);
    virtual llvm::Value* visit(CodeBlock *node);
    virtual llvm::Value* visit(StmtList *node);
    virtual llvm::Value* visit(AssignmentNode *node);
    virtual llvm::Value* visit(ReturnNode *node);
    virtual llvm::Value* visit(FuncCallNode *node);
    virtual llvm::Value* visit(ArgumentList *node) {return nullptr;}
    virtual llvm::Value* visit(BinaryOpNode *node);
    virtual llvm::Value* visit(SymbolNode *node);
    virtual llvm::Value* visit(ValueNode *node);
    virtual llvm::Value* visit(LabelNode *node);
    virtual llvm::Value* visit(ABSJMPNode *node);
    virtual llvm::Value* visit(CMPJMPNode *node);
private:
    std::map<std::string, llvm::AllocaInst*> NamedValues;
    std::map<uint32_t, llvm::BasicBlock*> BlockMap;
};
}
#endif