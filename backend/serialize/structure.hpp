#ifndef STRUCTURE_HPP
#define STRUCTURE_HPP

#include <cstdint>

namespace naivescript
{

namespace serialize
{

enum NodeType
{
    CodeBlock = 0,
    DeclarationList,
    StatementList,
    Declaration,
    ForStmt,
    WriteStmt,
    AssignmentExpr,
    BinaryOp,
    ID,
    Number,
};

const uint32_t FileMD5Size = 16 ;

struct FileHeader
{
    uint32_t magic ;
    uint32_t entry ;
    uint32_t bodySize ;
    uint8_t bodyMD5[ FileMD5Size ] ;
    uint8_t body[ 0 ] ;
} __attribute__((packed)) ;


}
}


#endif
