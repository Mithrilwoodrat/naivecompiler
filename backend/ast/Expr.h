#ifndef EXPR_H
#define EXPR_H

#include "Statement.h"
#include "SerializeStructure.h"
#include "NodeFactory.h"
#include "Util.h"

namespace naivecompiler{

class Visitor;

class Expr: public Statement
{
public:
	Expr(serialize::NodeType type) : Statement(type) {}
};

};

#endif
