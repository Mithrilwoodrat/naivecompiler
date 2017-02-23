#ifndef SYMBOLNODE_H
#define SYMBOLNODE_H

#include "NaiveScript.h"
#include "ASTNode.h"
#include "Util.h"

namespace naivescript{
namespace ast {

class SymbolNode : public ASTNode
{
public:
    SymbolNode() : symboltype(0) {}
    virtual bool Parse( struct serialize::Symbol * symbol, size_t size );

    virtual void show(void) {
        std::cout <<  "ID: " << id << std::endl;
    }

    virtual const std::vector<ASTNode *>& GetChildren( void ) 
    {
        return children;
    }
private:
    std::string id;
    uint32_t symboltype;
    std::vector<ASTNode *> children;
};
}
}
#endif