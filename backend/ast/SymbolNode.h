#ifndef SYMBOLNODE_H
#define SYMBOLNODE_H

#include "Expr.h"
#include "Util.h"

namespace naivescript{

class SymbolNode : public Expr
{
public:
    SymbolNode() : Expr(serialize::NodeType::TypeSymbol), symboltype(0) {}
    virtual bool Parse( struct serialize::Symbol * symbol, size_t size );

    virtual void show(int offset = 0)
    {
    	std::string index = std::string(offset, '\t');
    	std::cout << index;
        std::cout <<  "ID: " << id;
    }

    virtual const std::vector<ASTNode *> GetChildren( void ) 
    {
        return children;
    }

    virtual llvm::Value* accept(Visitor* v);

    inline const std::string& GetSymbol( void ) const {
        return id;
    }

    inline const uint32_t GetSymbolType( void ) const {
        return symboltype;
    }

private:
    std::string id;
    uint32_t symboltype;
    std::vector<ASTNode *> children;
};
}
#endif
