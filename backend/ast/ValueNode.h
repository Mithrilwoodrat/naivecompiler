#ifndef VALUENODE_H
#define VALUENODE_H

#include "Expr.h"
#include "Util.h"

namespace naivecompiler{

class IntegerNode;

class ValueNode : public Expr {

public:
	ValueNode() : Expr(serialize::NodeType::TypeValue), valuetype(0) {}
    ValueNode(int valuetype) : Expr(serialize::NodeType::TypeValue), valuetype(valuetype) {}
    virtual bool Parse( struct serialize::Value * value, size_t size );

    virtual void show(int offset = 0) {
    	std::string index = std::string(offset, '\t');
		DLOG(LOG_DEBUG) << index;
		switch (valuetype) {
			case serialize::ValueType::CONSTINT:
				DLOG(LOG_DEBUG) << "ConstValue Type: " << ShowType(valuetype) << "\tVal: " << std::endl;
				return;
			case serialize::ValueType::CONSTSTRING:
				DLOG(LOG_DEBUG) << "ConstValue Type: " << ShowType(valuetype) << "\tVal: " << std::endl;
				return;
			}
    }

    virtual const std::vector<ASTNode *> GetChildren( void ) 
    {
        return children;
    }

    virtual llvm::Value* accept(Visitor* v);

    virtual const uint32_t GetVal( void ) const {return 0;};
    virtual const std::string GetValString( void ) const {return "";};

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
    uint32_t valuetype;
private:
    std::vector<ASTNode *> children;
};

class IntegerNode : public ValueNode {
public:
	IntegerNode() : ValueNode(serialize::ValueType::CONSTINT),  val(0) {}

	IntegerNode(std::string val) : ValueNode(serialize::ValueType::CONSTINT), val(0) {}

    virtual bool Parse( struct serialize::Value * value, size_t size );

    virtual void show(int offset = 0) {
    	std::string index = std::string(offset, '\t');
    	DLOG(LOG_DEBUG) << index;
    	DLOG(LOG_DEBUG) << "ConstValue Type: " << ShowType(valuetype) << "\tVal: " << val << std::endl;
    }

    virtual llvm::Value* accept(Visitor* v);

    virtual inline const uint32_t GetVal( void ) const {
        return val;
    }

private:
    uint32_t val;
    std::vector<ASTNode *> children;
};


class StringLiteralNode : public ValueNode {
public:
	StringLiteralNode() : ValueNode(serialize::ValueType::CONSTSTRING),  valstring("") {}

	StringLiteralNode(std::string val) : ValueNode(serialize::ValueType::CONSTSTRING), valstring(val) {}

    virtual bool Parse( struct serialize::Value * value, size_t size );

    virtual void show(int offset = 0) {
    	std::string index = std::string(offset, '\t');
    	DLOG(LOG_DEBUG) << index;
    	DLOG(LOG_DEBUG) << "StringLiteralNode Type: " << ShowType(valuetype) << "\tVal: " << valstring << std::endl;
    }

    virtual llvm::Value* accept(Visitor* v);

    inline const std::string GetValString( void ) const {
        return valstring;
    }

private:
    std::string valstring;
    std::vector<ASTNode *> children;
};

}
#endif
