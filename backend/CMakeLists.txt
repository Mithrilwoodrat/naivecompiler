project(naivescript)
cmake_minimum_required(VERSION 2.8)
SET(CMAKE_C_COMPILER clang)
SET(CMAKE_CXX_COMPILER clang++)


Option(ENABLE_DEBUG "Enable debug , true/false" true)

if(ENABLE_DEBUG) 
    Add_Definitions( -O0 -g -DNSDEBUG )
    Message(STATUS  "Enable debug") 
else() 
Add_Definitions( -O4 ) 
endif()

Add_Definitions( -Wall -Werror -fPIC -std=c++11 
-D__STDC_CONSTANT_MACROS -D__STDC_LIMIT_MACROS)

#find_package(LLVM 3.8 CONFIG)

Set( NSWorkingPath ${CMAKE_CURRENT_SOURCE_DIR} )

Set( NSIncludeDir ${NSWorkingPath} 
    ${NSWorkingPath}/serialize
    ${NSWorkingPath}/ast
    ${NSWorkingPath}/codegen 
    /usr/include )

Set( NSSrcFiles
    ${NSWorkingPath}/Compiler.cc
    ${NSWorkingPath}/Util.cc

    ${NSWorkingPath}/serialize/SerializeFile.cc
    ${NSWorkingPath}/serialize/SymbolTable.cc

    ${NSWorkingPath}/ast/ASTNode.cc
    ${NSWorkingPath}/ast/NodeFactory.cc
    ${NSWorkingPath}/ast/StmtList.cc
    ${NSWorkingPath}/ast/AssignmentNode.cc
    ${NSWorkingPath}/ast/ValueNode.cc
    ${NSWorkingPath}/ast/SymbolNode.cc
    ${NSWorkingPath}/ast/BinaryOpNode.cc
    ${NSWorkingPath}/ast/NodeVisitor.cc

    ${NSWorkingPath}/codegen/CodeGen.cc
)



add_executable(testNS  ${NSSrcFiles} test.cc)
Target_Include_Directories( testNS PUBLIC ${NSIncludeDir} )
target_link_libraries(testNS PUBLIC LLVM-3.9)
