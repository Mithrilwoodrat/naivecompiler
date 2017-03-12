#ifndef SERIALIZESTRUCTURE_H
#define SERIALIZESTRUCTURE_H

#include <stdint.h>

namespace naivescript
{

namespace serialize
{

enum NodeType
{
    FuncList = 0,
    Function = 1,
    CodeBlock = 2,
    DeclarationList = 3,
    StatementList = 4,
    ArgumentList = 5,
    Declaration = 6,
    ForStmt =  7,
    FuncCall =  8,
    AssignmentExpr = 9,
    BinaryOp =  10,
    Symbol = 11,
    Value = 12,
};

enum ValueType
{
    CONSTINT = 0,
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
    struct StringTable stringtable;
    uint8_t body[ 0 ] ;
} __attribute__((packed)) ;


struct FunctionList
{
    uint32_t type;
    uint32_t count;
    uint32_t size;
    uint8_t data[0];
}__attribute__((packed)) ;

struct ArgumentList
{
    uint32_t type;
    uint32_t count;
    uint32_t size;
    uint8_t data[0];
}__attribute__((packed)) ;

struct StmtList
{
    uint32_t type;
    uint32_t count;
    uint32_t size;
    uint8_t data[0];
}__attribute__((packed)) ;

struct DeclarationList
{
    uint32_t type;
    uint32_t count;
    uint32_t size;
    uint8_t data[0];
}__attribute__((packed)) ;

struct Expr {
    uint8_t data[0];
}__attribute__((packed)) ;

struct CodeBlock
{
    uint32_t type;
    uint32_t decls_size;
    uint32_t stmts_size;
    Expr decls;
    Expr stmts;
}__attribute__((packed)) ;

struct Declaration
{
    uint32_t type;
    uint32_t symboltype;
    uint32_t id;
}__attribute__((packed)) ;

struct Function
{
    uint32_t type;
    uint32_t size;
    uint32_t id;
    uint32_t return_type;
    uint32_t params_size;
    uint32_t body_size;
    Expr param_list;
    Expr body;
}__attribute__((packed)) ;

struct FuncCall
{
    uint32_t type;
    uint32_t size;
    uint32_t id;
    uint32_t args_size;
    Expr args;
}__attribute__((packed)) ;



struct Assignment
{
    uint32_t type;
    uint32_t size;  //变长的结构都带有大小
    uint32_t id;
    uint32_t exprSize;
    uint8_t expr[0];
}__attribute__((packed)) ;


struct BinaryOp
{
    uint32_t type;
    uint32_t size;
    uint32_t lhsSize;
    uint32_t rhsSize;
    uint8_t op;
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


}
}


#endif
