#ifndef DECLARACTION_H
#define DECLARACTION_H

#include "Statement.h"
#include "Util.h"

namespace naivescript{

class Declaration : public Statement
{
public:
    Declaration() : Statement(serialize::TypeDeclaration) {}
    virtual bool Parse( struct serialize::Declaration * decl, size_t size );

    virtual void show(int offset = 0) override
    {
    	std::string index = std::string(offset, '\t');
    	std::cout << index;
        std::cout <<  "Declaration: ID: " << id << "\t" << "type: " << symboltype << std::endl;
    }

    virtual const std::vector<ASTNode *> GetChildren( void ) override
    {
        return children;
    }

    std::string GetID(void)
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
