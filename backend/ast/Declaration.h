#ifndef DECLARACTION_H
#define DECLARACTION_H

#include "NaiveScript.h"
#include "ASTNode.h"
#include "Util.h"

namespace naivescript{

class Declaration : public ASTNode
{
public:
    Declaration() : symboltype(0) {}
    virtual bool Parse( struct serialize::Declaration * decl, size_t size );

    virtual void show(void) override
    {
        std::cout <<  "Declaration: ID: " << id << "\t" << "type: " << symboltype << std::endl;
    }

    virtual const std::vector<ASTNode *> GetChildren( void ) override
    {
        return children;
    }

    std::string GetId(void)
    {
        return id;
    }

    virtual llvm::Value* accept(Visitor* v) override;

    inline const std::string& GetSymbol( void ) const {
        return id;
    }

private:
    std::string id;
    uint32_t symboltype;
    std::vector<ASTNode *> children;
};
}
#endif