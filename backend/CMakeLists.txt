project(naivescript  C CXX ASM )
cmake_minimum_required(VERSION 2.8)
SET(CMAKE_C_COMPILER clang)
SET(CMAKE_CXX_COMPILER clang++)


Option(ENABLE_DEBUG "Enable debug , true/false" true)

if(ENABLE_DEBUG) 
    Add_Definitions( -O0 -g -DNSDEBUG )
    Message(STATUS  "Enable debug") 
else() 
Add_Definitions( -O3 ) 
endif()


Add_Definitions( -Wall -Werror -fPIC -std=c++11 -pthread  -g
-D__STDC_CONSTANT_MACROS -D__STDC_LIMIT_MACROS)

#find_package(LLVM 3.8 CONFIG)

Set( NSWorkingPath ${CMAKE_CURRENT_SOURCE_DIR} )

Set( NSIncludeDir ${NSWorkingPath} 
    ${NSWorkingPath}/serialize
    ${NSWorkingPath}/ast
    ${NSWorkingPath}/codegen 
    ${NSWorkingPath}/log
    /usr/include 
    /usr/local/include
	#/usr/lib/llvm-3.8/include
)

if(APPLE)
    # for MacOS X or iOS, watchOS, tvOS (since 3.10.3)
    # list(APPEND ${NSIncludeDir}
    # Add_Definitions( -L/usr/local/opt/llvm@6/lib )
    # Add_Definitions( -I/usr/local/opt/llvm@6/include )
    include_directories(/usr/local/opt/llvm@6/include)
    link_directories(/usr/local/opt/llvm@6/lib)
endif()

Set( NSSrcFiles
    ${NSWorkingPath}/Compiler.cc
    ${NSWorkingPath}/Util.cc
    ${NSWorkingPath}/log/Logging.cc

    ${NSWorkingPath}/serialize/SerializeFile.cc
    ${NSWorkingPath}/serialize/SymbolTable.cc

    ${NSWorkingPath}/ast/ASTNode.cc
    ${NSWorkingPath}/ast/AST.cc
    ${NSWorkingPath}/ast/NodeFactory.cc
    ${NSWorkingPath}/ast/FuncDefNode.cc
    ${NSWorkingPath}/ast/FuncDeclNode.cc
    ${NSWorkingPath}/ast/FuncCallNode.cc
    ${NSWorkingPath}/ast/ArgumentList.cc
    ${NSWorkingPath}/ast/Declaration.cc
    ${NSWorkingPath}/ast/DeclarationList.cc
    ${NSWorkingPath}/ast/Statement.cc
    ${NSWorkingPath}/ast/StmtList.cc
    ${NSWorkingPath}/ast/AssignmentNode.cc
    ${NSWorkingPath}/ast/ReturnNode.cc
    ${NSWorkingPath}/ast/ValueNode.cc
    ${NSWorkingPath}/ast/SymbolNode.cc
    ${NSWorkingPath}/ast/BinaryOpNode.cc
    ${NSWorkingPath}/ast/NodeVisitor.cc

    ${NSWorkingPath}/codegen/CodeGen.cc
)

link_directories(/usr/local/lib/)
if(APPLE)
    add_library(NaiveScript MODULE ${NSSrcFiles})
else()
    add_library(NaiveScript  SHARED ${NSSrcFiles})
    set(CURSES_NEED_NCURSES TRUE) # Make CMake find NCURSES instead of curses in ubuntu
endif()

Target_Include_Directories( NaiveScript PUBLIC ${NSIncludeDir} )

if(APPLE)
  target_link_libraries(NaiveScript PUBLIC -ldl -lcurses -lpthread -lz -lm -lLLVM)
else()
  target_link_libraries(NaiveScript PUBLIC -lrt -ldl -lpthread -lz -lm -lLLVM-6.0)
endif()
