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
    Number = 11, 
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

struct Assignment
{
    uint32_t type;
    uint32_t id;
    uint32_t size;  //变长的结构都带有大小
    uint32_t expSize;
    uint8_t exp;
}__attribute__((packed)) ;

struct Expr {
    uint8_t data[0];
}__attribute__((packed)) ;

struct BinaryOp
{
    uint32_t type;
    uint8_t op;
    uint32_t size;
    uint32_t exp1Size;
    uint32_t exp2Size;
    Expr exp1;
    Expr exp2;
}__attribute__((packed)) ;

struct Symbol {
    uint32_t type;
    uint32_t id;
    uint32_t _type;
}__attribute__((packed)) ;

struct Number {
    uint32_t type;
    uint32_t _type;
    uint32_t val;
}__attribute__((packed)) ;



}
}


#endif
