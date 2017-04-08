#ifndef STATEMENT_H
#define STATEMENT_H

#include "ASTNode.h"
#include "SerializeStructure.h"
#include "NodeFactory.h"
#include "Util.h"

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

class LabelNode : public Statement 
{
public:
    LabelNode() : Statement(serialize::TypeLabel), id(0) {}
    virtual bool Parse( struct serialize::Label * label, size_t size ) ;

    virtual void show( void ) {
        std::cout <<  "Label: " << "id=" << id << std::endl;
    }

    virtual const std::vector<ASTNode *> GetChildren( void ) 
    {
        return children;
    }
    
    virtual llvm::Value* accept(Visitor* v);

    inline uint32_t GetID( void )  {
        return id;
    }

private:
    uint32_t id;
    std::vector<ASTNode *> children;
};

class ABSJMPNode : public Statement 
{
public:
    ABSJMPNode() : Statement(serialize::TypeABSJMP), id(0) {}
    virtual bool Parse( struct serialize::ABSJMP * jmp, size_t size ) ;

    virtual void show( void ) {
        std::cout <<  "ABSJMP: " << "id=" << id << std::endl;
    }

    virtual const std::vector<ASTNode *> GetChildren( void ) 
    {
        return children;
    }
    
    virtual llvm::Value* accept(Visitor* v);

    inline uint32_t GetID( void )  {
        return id;
    }

private:
    uint32_t id;
    std::vector<ASTNode *> children;
};

class CMPJMPNode : public Statement 
{
public:
    CMPJMPNode() : Statement(serialize::TypeCMPJMP), id1(0), id2(0), expr(nullptr) {}
    virtual bool Parse( struct serialize::CMPJMP * jmp, size_t size ) ;

    virtual void show( void ) 
    {
        std::cout <<  "CMP: " << "id1=" << id1 << "id2=" << id2 << std::endl;
        expr->show();
    }

    virtual const std::vector<ASTNode *> GetChildren( void ) 
    {
        return children;
    }
    
    virtual llvm::Value* accept(Visitor* v);

    inline uint32_t GetID1( void )  
    {
        return id1;
    }

    inline uint32_t GetID2( void )  
    {
        return id2;
    }

    inline ASTNode* GetExpr( void )  
    {
        return expr;
    }

    ~CMPJMPNode()
    {
        if (expr) {
            free(expr);
        }
    }

private:
    uint32_t id1;
    uint32_t id2;
    ASTNode* expr;
    std::vector<ASTNode *> children;
};

}
#endif
