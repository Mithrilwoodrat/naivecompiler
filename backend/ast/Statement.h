#ifndef STATEMENT_H
#define STATEMENT_H

#include "ASTNode.h"
#include "SerializeStructure.h"

namespace naivescript{

class Visitor;
	 
class Statement: public ASTNode 
{
public:
    Statement(serialize::NodeType type) : nodetype(type) {}
    serialize::NodeType nodetype;
    virtual serialize::NodeType GetNodeType(void)
    {
        return nodetype;
    }

};

class BreakNode : public Statement
{
public:
    BreakNode() : Statement(serialize::TypeBreakStmt) {}
    virtual const std::vector<ASTNode *> GetChildren( void ) 
    {
        return children;
    }
    
    virtual llvm::Value* accept(Visitor* v)
    {
       return nullptr;
    }
    virtual void show( void ) {
        std::cout <<  "Break" << std::endl;
    }
private:
    std::vector<ASTNode *> children;
};

class ContinueNode : public Statement
{
public:
    ContinueNode() : Statement(serialize::TypeContinueStmt) {}
    virtual const std::vector<ASTNode *> GetChildren( void ) 
    {
        return children;
    }
    virtual llvm::Value* accept(Visitor* v)
    {
       return nullptr;
    }
    virtual void show( void ) {
        std::cout << "Continue" << std::endl;
    }
private:
    std::vector<ASTNode *> children;
};

}
#endif
