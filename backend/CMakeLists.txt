project(naivescript)
cmake_minimum_required(VERSION 2.8)
SET(CMAKE_C_COMPILER clang)
SET(CMAKE_CXX_COMPILER clang++)

Option(ENABLE_DEBUG "Enable debug , true/false" true)

if(ENABLE_DEBUG) 
    Add_Definitions( -O0 -g -DDOLPHIN_DEBUG )
    Message(STATUS  "Enable debug") 
else() 
Add_Definitions( -O4 ) 
endif()

Add_Definitions( -Wall -Werror -fPIC -std=c++11)

Set( NSWorkingPath ${CMAKE_CURRENT_SOURCE_DIR} )

Set( NSIncludeDir ${NSWorkingPath} 
    ${NSWorkingPath}/serialize
    ${NSWorkingPath}/ast 
    /usr/include )

Set( NSSrcFiles
    ${NSWorkingPath}/Compiler.h
    ${NSWorkingPath}/Compiler.cc
    ${NSWorkingPath}/Util.h
    ${NSWorkingPath}/Util.cc

    ${NSWorkingPath}/serialize/SerializeFile.cc
    ${NSWorkingPath}/serialize/SerializeFile.h
    ${NSWorkingPath}/serialize/SerializeStructure.h

    ${NSWorkingPath}/ast/AST.h
    ${NSWorkingPath}/ast/ASTNode.h
    ${NSWorkingPath}/ast/StmtList.h
    ${NSWorkingPath}/ast/Assignment.h
)



add_executable(testNS  ${NSSrcFiles} test.cc)
Target_Include_Directories( testNS PUBLIC ${NSIncludeDir} )
#target_link_libraries(test PUBLIC gflags glog)