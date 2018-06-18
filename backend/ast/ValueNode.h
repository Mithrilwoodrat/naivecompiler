#ifndef VALUENODE_H
#define VALUENODE_H

#include "Expr.h"
#include "Util.h"

namespace naivescript{

class ValueNode : public Expr {

public:
    ValueNode() : Expr(serialize::NodeType::TypeValue), val(0) , valstring(""), valuetype(0) {}

    virtual bool Parse( struct serialize::Value * value, size_t size );

    virtual void show(int offset = 0) {
    	std::string index = std::string(offset, '\t');
    	std::cout << index;
    	std::cout << "ConstValue Type: " << ShowType(valuetype) << "\tVal: " << val << std::endl;
    }

    virtual const std::vector<ASTNode *> GetChildren( void ) 
    {
        return children;
    }

    virtual llvm::Value* accept(Visitor* v);

    inline const uint32_t GetVal( void ) const {
        return val;
    }

    inline const uint32_t GetValType( void ) const {
        return valuetype;
    }

    inline std::string ShowType( const uint32_t type) {
    	switch(type) {
    		case serialize::ValueType::CONSTINT:
    			return "Unsigned Int";
    		case serialize::ValueType::CONSTSTRING:
    			return "StringLiteral";
    		default:
    			return std::to_string(type);
    	}
    }
private:
    uint32_t val;
    std::string valstring;
    uint32_t valuetype;
    std::vector<ASTNode *> children;
};

}
#endif
