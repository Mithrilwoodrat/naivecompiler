#include "ASTNode.h"
#include "Compiler.h"
#include "NodeVisitor.h"


namespace naivescript{
namespace ast {

void ASTNode::visit(Visitor* v) {
        v->visit(this);
}    

}
}