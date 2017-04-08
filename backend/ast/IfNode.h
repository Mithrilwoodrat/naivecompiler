#ifndef IFNODE_H
#define IFNODE_H

#include "Statement.h"
#include "Util.h"


namespace naivescript{

class Visitor;

class IfNode : public Statement 
{
public:
    IfNode() : Statement(serialize::TypeIfStmt), cond(nullptr), then(nullptr), _else(nullptr) {}
    virtual bool Parse( struct serialize::IfStmt * stmt, size_t size ) ;

    virtual void show( void ) 
    {
        std::cout <<  "If: ";
        cond->show();
        std::cout << std::endl;
        then->show();
        std::cout << std::endl;
        if (_else) {
            _else->show();
            std::cout << std::endl;
        }
    }

    virtual const std::vector<ASTNode *> GetChildren( void ) 
    {
        children.push_back(cond);
        children.push_back(then);
        if (_else)
            children.push_back(_else);
        return children;
    }
    
    virtual llvm::Value* accept(Visitor* v);

    inline ASTNode* GetCond( void ) const 
    {
        return cond;
    }

    inline ASTNode* GetThen( void ) const 
    {
        return then;
    }

    inline ASTNode* GetElse( void ) const 
    {
        return _else;
    }

    ~IfNode()
    { 
        if (cond)
            free(cond);
        if (then)
            free(then);
        if (_else)
            free(_else);
    }
private:
    ASTNode* cond;
    ASTNode* then;
    ASTNode* _else;
    std::vector<ASTNode *> children;
};

}
#endif