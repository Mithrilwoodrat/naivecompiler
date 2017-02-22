#ifndef VALUENODE_H
#define VALUENODE_H

#include "NaiveScript.h"
#include "ASTNode.h"
#include "Util.h"

namespace naivescript{
namespace ast {

class ValueNode : public ASTNode {

public:
    ValueNode() : val(0) {}

    virtual bool Parse( struct serialize::Value * value, size_t size );

    virtual void show(void) {
        std::cout <<  "ConstValue: " << val << std::endl;
    }

    virtual const std::vector<ASTNode *>& GetChildren( void ) 
    {
        return children;
    }

private:
    uint32_t val;
    uint32_t valuetype;
    std::vector<ASTNode *> children;
};

}
}
#endif