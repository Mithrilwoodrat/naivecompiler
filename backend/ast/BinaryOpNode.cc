#include "BinaryOpNode.h"
#include "Compiler.h"
#include "NodeFactory.h"


namespace naivescript{
namespace ast {

bool BinaryOpNode::Parse( struct serialize::BinaryOp * binaryop, size_t size ) {
        std::cout << "Parsing BinaryOP: ";
        op = binaryop->op;
        std::cout << "OP: " << op << std::endl;
        uint8_t *p_lhs = (uint8_t *)(binaryop->lhs.data);
        uint32_t type = util::getStructType(p_lhs);
        switch(type) {
            case serialize::Value:
                lhs = NodeFactory::CreateValue(p_lhs, binaryop->lhsSize);
                break;
            case serialize::Symbol:
                lhs = NodeFactory::CreateSymbol(p_lhs, binaryop->lhsSize);
                break;
            case serialize::BinaryOp:
                lhs = NodeFactory::CreateBinaryOp(p_lhs, binaryop->lhsSize);
                break;
            default:
                return false;
        }

        uint8_t* p_rhs = p_lhs + binaryop->lhsSize;
        type = util::getStructType(p_rhs);
        switch(type) {
            case serialize::Value:
                rhs = NodeFactory::CreateValue(p_rhs, binaryop->rhsSize);
                break;
            case serialize::Symbol:
                rhs = NodeFactory::CreateSymbol(p_rhs, binaryop->rhsSize);
                break;
            case serialize::BinaryOp:
                rhs = NodeFactory::CreateBinaryOp(p_rhs, binaryop->rhsSize);
                break;
            default:
                std::cout << "Unknown Type" << std::endl;
                return false;
        }

        return true;
}

void BinaryOpNode::accept(Visitor* v)
{
    v->visit(this);
}

}
}