#ifndef SYMBOLNODE_H
#define SYMBOLNODE_H

#include "NaiveScript.h"
#include "ASTNode.h"
#include "Util.h"

namespace naivescript{

class SymbolNode : public ASTNode
{
public:
    SymbolNode() : symboltype(0) {}
    virtual bool Parse( struct serialize::Symbol * symbol, size_t size );

    virtual void show(void) 
    {
        std::cout <<  "ID: " << id;
    }

    virtual const std::vector<ASTNode *>& GetChildren( void ) 
    {
        return children;
    }

    virtual llvm::Value* accept(Visitor* v);

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