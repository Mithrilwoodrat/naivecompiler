#ifndef WHILENODE_H
#define WHILENODE_H

#include "NaiveScript.h"
#include "Statement.h"
#include "Util.h"


#include "CodeBlock.h"


namespace naivescript{

class Visitor;

class WhileNode : public Statement 
{
public:
    WhileNode() : Statement(serialize::TypeWhileStmt), cond(nullptr), body(nullptr) {}
    virtual bool Parse( struct serialize::WhileStmt * stmt, size_t size ) ;

    virtual void show( void ) 
    {
        std::cout <<  "While: ";
        cond->show();
        std::cout << std::endl;
        body->show();
        std::cout << std::endl;
    }

    virtual const std::vector<ASTNode *> GetChildren( void ) 
    {
        children.push_back(cond);
        children.push_back(body);
        return children;
    }
    
    virtual llvm::Value* accept(Visitor* v);

    inline ASTNode* GetCond( void ) const 
    {
        return cond;
    }

    inline ASTNode* GetBody( void ) const 
    {
        return body;
    }

    ~WhileNode()
    { 
        if (cond)
            free(cond);
        if (body)
            free(body);
    }
private:
    ASTNode* cond;
    ASTNode* body;
    std::vector<ASTNode *> children;
};

}
#endif