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

}
#endif
