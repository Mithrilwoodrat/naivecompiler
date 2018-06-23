#ifndef BINARYOPNODE_H
#define BINARYOPNODE_H

#include "ASTNode.h"
#include "Util.h"


namespace naivescript{

class BinaryOpNode : public ASTNode
{
public:
    BinaryOpNode() : lhs(NULL), op(0), rhs(NULL) {}
    virtual bool Parse( struct serialize::BinaryOp * binaryop, size_t size );

    virtual void show( int offset = 0 )
    {
    	std::string index = std::string(offset, '\t');
    	std::cout << index;
        std::cout << "BinaryOp: ";
        lhs->show(offset + 1);
        std::cout << "\t OP: " << op << "\t";
        rhs->show(offset + 1);
    }

    std::string ShowBinaryOp(uint32_t op) {
    	switch(op) {
    	case serialize::BinaryOpType::ADDOP:
    		return "+";
    	case serialize::BinaryOpType::MINUSOP:
    		return "-";
    	case serialize::BinaryOpType::TIMESOP:
    		return "*";
    	case serialize::BinaryOpType::DIVIDEOP:
    		return "-";
    	case serialize::BinaryOpType::GTOP:
    		return ">";
    	case serialize::BinaryOpType::LTOP:
    		return "<";
    	case serialize::BinaryOpType::GTEOP:
    		return ">=";
    	case serialize::BinaryOpType::LTEOP:
    		return "<=";
    	case serialize::BinaryOpType::ANDOP:
    		return "&&";
    	case serialize::BinaryOpType::OROP:
    		return "||";
    	case serialize::BinaryOpType::EQUALOP:
    		return "==";
    	default:
    		std::cerr << "Unknown BinaryOp" << op << std::endl;
    	}
    	return "";
    }

    virtual const std::vector<ASTNode *> GetChildren( void ) 
    {
        children.push_back(lhs);
        children.push_back(rhs);
        return children;
    }

    virtual llvm::Value* accept(Visitor* v);

    inline const char GetOp( void ) const {
        return op;
    }

    inline ASTNode* GetLHS( void )  {
        return lhs;
    }

    inline ASTNode* GetRHS( void )  {
        return rhs;
    }

    ~BinaryOpNode() 
    {
        if (lhs) {
            free(lhs);
        }
        if (rhs) {
            free(rhs);
        }
    }
    
private:
    ASTNode * lhs;
    uint32_t op;
    ASTNode * rhs;
    std::vector<ASTNode *> children;
};

}
#endif
