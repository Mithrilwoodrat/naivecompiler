#include "Statement.h"
#include "NodeFactory.h"
#include "Compiler.h"

namespace naivecompiler
{

bool LabelNode::Parse( struct serialize::Label * label, size_t size )
{
    std::cout << "Parsing Label" << std::endl;
    id = label->id;
    return true;
}

bool ABSJMPNode::Parse( struct serialize::ABSJMP * jmp, size_t size ) 
{
    std::cout << "Parsing ABSJMP" << std::endl;
    id = jmp->id;
    return true;
}

bool CMPJMPNode::Parse( struct serialize::CMPJMP * jmp, size_t size )
{
    std::cout << "Parsing CMPJMPNode: ";
    id1 = jmp->id1;
    id2 = jmp->id2;
    std::cout << id1 << "\t" << id2 << std::endl;
    uint32_t type = util::getStructType(jmp->expr);
    switch(type) {
        case serialize::TypeValue:
            expr = NodeFactory::CreateValue(jmp->expr, jmp->exprSize);
            break;
        case serialize::TypeSymbol:
            expr = NodeFactory::CreateSymbol(jmp->expr, jmp->exprSize);
            break;
        case serialize::TypeBinaryOp:
            expr = NodeFactory::CreateBinaryOp(jmp->expr, jmp->exprSize);
            break;
        default:
            return false;
    }
    return true;
}

llvm::Value* LabelNode::accept(Visitor* v)
{
    return v->visit(this);
}

llvm::Value* ABSJMPNode::accept(Visitor* v)
{
    return v->visit(this);
}

llvm::Value* CMPJMPNode::accept(Visitor* v)
{
    return v->visit(this);
}

}