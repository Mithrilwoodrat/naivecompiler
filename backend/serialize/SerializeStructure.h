#ifndef SERIALIZESTRUCTURE_H
#define SERIALIZESTRUCTURE_H

#include <stdint.h>

namespace naivescript
{

namespace serialize
{

enum NodeType
{
    StmtList = 3,
    Declaration = 4, 
    ForStmt = 5,
    ReadStmt = 6,  
    WriteStmt = 7, 
    Assignment = 8, 
    BinaryOp = 9, 
    Symbol = 10, 
    Value = 11, 
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
    StringTable stringtable;
    uint8_t body[ 0 ] ;
} __attribute__((packed)) ;


struct StmtList
{
    uint32_t type;
    uint32_t count;
    uint32_t size;
    uint8_t data[0];
}__attribute__((packed)) ;


struct ReadStmt
{
    uint32_t type;
    uint32_t id;
}__attribute__((packed)) ;  

struct WriteStmt
{
    uint32_t type;
    uint32_t id;
}__attribute__((packed)) ; 

struct Expr {
    uint8_t data[0];
}__attribute__((packed)) ;

struct Assignment
{
    uint32_t type;
    uint32_t id;
    uint32_t size;  //变长的结构都带有大小
    uint32_t exprSize;
    uint8_t expr[0];
}__attribute__((packed)) ;


struct BinaryOp
{
    uint32_t type;
    uint8_t op;
    uint32_t size;
    uint32_t expr1Size;
    uint32_t expr2Size;
    Expr expr1;
    Expr expr2;
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
