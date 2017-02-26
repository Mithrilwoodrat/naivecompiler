#ifndef NODEVISITOR_H
#define NODEVISITOR_H

#include "NaiveScript.h"
#include "ASTNode.h"
#include "Util.h"

#include "StmtList.h"
#include "AssignmentNode.h"
#include "ValueNode.h"
#include "BinaryOpNode.h"
#include "SymbolNode.h"

namespace naivescript{
namespace ast {

class Visitor
{
  public:
    virtual void visit(ASTNode *node) {  }
    virtual void visit(StmtList *node) = 0;
    virtual void visit(AssignmentNode *node) = 0;
    virtual void visit(BinaryOpNode *node) = 0;
    virtual void visit(SymbolNode *node) = 0;
    virtual void visit(ValueNode *node) = 0;
};

class ASTShowVisitor : public Visitor
{
    virtual void visit(StmtList *node);
    virtual void visit(AssignmentNode *node);
    virtual void visit(BinaryOpNode *node);
    virtual void visit(SymbolNode *node);
    virtual void visit(ValueNode *node);
};

}
}

#endif