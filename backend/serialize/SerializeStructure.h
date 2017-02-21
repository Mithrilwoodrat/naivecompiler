#ifndef STRUCTURE_HPP
#define STRUCTURE_HPP

#include <cstdint>

namespace naivescript
{

namespace serialize
{

enum NodeType
{
    StatementList = 2,
    Declaration,
    ForStmt,
    WriteStmt,
    AssignmentExpr,
    BinaryOp,
    ID,
    Number,
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


}
}


#endif
