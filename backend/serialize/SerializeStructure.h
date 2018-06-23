#ifndef SERIALIZESTRUCTURE_H
#define SERIALIZESTRUCTURE_H

#include <stdint.h>

namespace naivescript
{

namespace serialize
{

enum NodeType
{
    TypeAST = 0,
    TypeFuncDef = 1,
	TypeFuncDecl = 2,
    TypeArrayDecl = 3,
    TypeDeclarationList = 4,
    TypeStatementList = 5,
    TypeArgumentList = 6,
    TypeDeclaration = 7,
    TypeWhileStmt =  8,
    TypeIfStmt =  9,
    TypeFuncCall =  10,
    TypeAssignmentExpr = 11,
    TypeReturnStmt = 12,
    TypeBreakStmt = 13,
    TypeContinueStmt = 14,
    TypeBinaryOp =  15,
    TypeSymbol = 16,
    TypeValue = 17,
    TypeLabel = 18,
    TypeABSJMP = 19,
    TypeCMPJMP = 20,
    TypeUnaryOp = 21
};

enum ValueType
{
	VOID = 0,
    CONSTINT = 1,
    CONSTFLOAT = 2,
    CONSTCHAR = 3,
	CONSTSTRING = 4
};

//'+': 0,
//'-': 1,
//'*': 2,
//'/': 3,
//'>': 4,
//'<': 5,
//'>=': 6,
//'<=': 7,
//'&&':, 8,
//'||', 9,
//'==' 10
enum BinaryOpType
{
	ADDOP = 0,
	MINUSOP = 1,
	TIMESOP = 2,
	DIVIDEOP = 3,
	GTOP = 4,
	LTOP = 5,
	GTEOP = 6,
	LTEOP = 7,
	ANDOP = 8,
	OROP = 9,
	EQUALOP = 10
};

const uint32_t FileMD5Size = 16 ;

struct StringTable {
    uint8_t data[0];
}__attribute__((packed)) ;

struct FileFormat
{
    uint32_t magic ;
    uint32_t stringTableEntry ;
    uint32_t bodyEntry ;
    uint32_t bodySize ;
    uint32_t stringtableSize;
    uint8_t bodyMD5[ FileMD5Size ] ;
    StringTable stringtable;
    uint8_t body[ 0 ] ;
} __attribute__((packed)) ;


struct AST
{
    uint32_t type;
    uint32_t size;
    uint32_t count;
    uint32_t datasize;
    uint8_t data[0];
}__attribute__((packed)) ;

struct ArgumentList
{
    uint32_t type;
    uint32_t size;
    uint32_t count;
    uint32_t datasize;
    uint8_t data[0];
}__attribute__((packed)) ;

struct StmtList
{
    uint32_t type;
    uint32_t size;
    uint32_t count;
    uint32_t datasize;
    uint8_t data[0];
}__attribute__((packed)) ;

struct DeclarationList
{
    uint32_t type;
    uint32_t size;
    uint32_t count;
    uint32_t datasize;
    uint8_t data[0];
}__attribute__((packed)) ;

struct Expr {
    uint8_t data[0];
}__attribute__((packed)) ;

struct Declaration
{
    uint32_t type;
    uint32_t size;
    uint32_t symboltype;
    uint32_t id;
}__attribute__((packed)) ;

struct FuncDef
{
    uint32_t type;
    uint32_t size;
    uint32_t id;
    uint32_t return_type;
    uint32_t storage_type;
    uint32_t params_size;
    uint32_t body_size;
    Expr param_list;
    Expr body;
}__attribute__((packed)) ;

struct FuncDecl
{
    uint32_t type;
    uint32_t size;
    uint32_t id;
    uint32_t return_type;
    uint32_t storage_type;
    uint32_t params_size;
    Expr param_list;
}__attribute__((packed)) ;

struct FuncCall
{
    uint32_t type;
    uint32_t size;
    uint32_t id;
    uint32_t argsSize;
    Expr args;
}__attribute__((packed)) ;

struct UnaryOp
{
    uint32_t type;
    uint32_t size;
    uint32_t op;
    uint32_t exprSize;
    Expr expr;
}__attribute__((packed)) ;

struct Assignment
{
    uint32_t type;
    uint32_t size;  //变长的结构都带有大小
    uint32_t castexprSize;
    uint32_t exprSize;
    Expr castexpr;
    Expr expr;
}__attribute__((packed)) ;

struct ReturnStmt
{
    uint32_t type;
    uint32_t size;
    uint32_t exprSize;
    uint8_t expr[0];
}__attribute__((packed)) ;

struct WhileStmt
{
    uint32_t type;
    uint32_t size;
    uint32_t condSize;
    uint32_t bodySize;
    Expr cond;
    Expr body;
}__attribute__((packed)) ;

struct IfStmt
{
    uint32_t type;
    uint32_t size;
    uint32_t condSize;
    uint32_t thenSize;
    uint32_t elseSize;
    Expr cond;
    Expr then;
    Expr _else;
}__attribute__((packed)) ;

struct BreakStmt
{
    uint32_t type;
    uint32_t size;
}__attribute__((packed)) ;


struct ContinueStmt
{
    uint32_t type;
    uint32_t size;
}__attribute__((packed)) ;


struct BinaryOp
{
    uint32_t type;
    uint32_t size;
    uint32_t lhsSize;
    uint32_t rhsSize;
    uint32_t op;
    Expr lhs;
    Expr rhs;
}__attribute__((packed)) ;

struct Symbol {
    uint32_t type;
    uint32_t id;
    uint32_t symboltype;
}__attribute__((packed)) ;

struct Value {
    uint32_t type;
    uint32_t valuetype;
    uint32_t val;
}__attribute__((packed)) ;

struct Label
{
    uint32_t type;
    uint32_t size;
    uint32_t id;
}__attribute__((packed)) ;

struct ABSJMP
{
    uint32_t type;
    uint32_t size;
    uint32_t id;
}__attribute__((packed)) ;

struct CMPJMP
{
    uint32_t type;
    uint32_t size;
    uint32_t exprSize;
    uint32_t id1;
    uint32_t id2;
    uint8_t expr[0];
}__attribute__((packed)) ;


}
}


#endif
