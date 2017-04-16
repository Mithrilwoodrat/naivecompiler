project(naivescript  C CXX ASM )
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

Add_Definitions( -Wall -Werror -fPIC -std=c++11 -pthread  -g
-D__STDC_CONSTANT_MACROS -D__STDC_LIMIT_MACROS)

#find_package(LLVM 3.8 CONFIG)

Set( NSWorkingPath ${CMAKE_CURRENT_SOURCE_DIR} )

Set( NSIncludeDir ${NSWorkingPath} 
    ${NSWorkingPath}/serialize
    ${NSWorkingPath}/ast
    ${NSWorkingPath}/codegen 
    /usr/include 
    /usr/local/include
)

Set( NSSrcFiles
    ${NSWorkingPath}/Compiler.cc
    ${NSWorkingPath}/Util.cc

    ${NSWorkingPath}/serialize/SerializeFile.cc
    ${NSWorkingPath}/serialize/SymbolTable.cc

    ${NSWorkingPath}/ast/ASTNode.cc
    ${NSWorkingPath}/ast/NodeFactory.cc
    ${NSWorkingPath}/ast/FunctionNode.cc
    ${NSWorkingPath}/ast/FunctionList.cc
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

add_library(NaiveScript  SHARED ${NSSrcFiles})
Target_Include_Directories( NaiveScript PUBLIC ${NSIncludeDir} )

target_link_libraries(NaiveScript PUBLIC -lrt -ldl -lcurses -lpthread -lz -lm -lLLVMLTO -lLLVMObjCARCOpts -lLLVMSymbolize
 -lLLVMDebugInfoPDB -lLLVMDebugInfoDWARF -lLLVMXCoreDisassembler
 -lLLVMXCoreCodeGen -lLLVMXCoreDesc -lLLVMXCoreInfo -lLLVMXCoreAsmPrinter
 -lLLVMSystemZDisassembler -lLLVMSystemZCodeGen -lLLVMSystemZAsmParser
 -lLLVMSystemZDesc -lLLVMSystemZInfo -lLLVMSystemZAsmPrinter
 -lLLVMSparcDisassembler -lLLVMSparcCodeGen -lLLVMSparcAsmParser
 -lLLVMSparcDesc -lLLVMSparcInfo -lLLVMSparcAsmPrinter
 -lLLVMPowerPCDisassembler -lLLVMPowerPCCodeGen -lLLVMPowerPCAsmParser
 -lLLVMPowerPCDesc -lLLVMPowerPCInfo -lLLVMPowerPCAsmPrinter
 -lLLVMNVPTXCodeGen -lLLVMNVPTXDesc -lLLVMNVPTXInfo -lLLVMNVPTXAsmPrinter
 -lLLVMMSP430CodeGen -lLLVMMSP430Desc -lLLVMMSP430Info
 -lLLVMMSP430AsmPrinter -lLLVMMipsDisassembler -lLLVMMipsCodeGen
 -lLLVMMipsAsmParser -lLLVMMipsDesc -lLLVMMipsInfo -lLLVMMipsAsmPrinter
 -lLLVMHexagonDisassembler -lLLVMHexagonCodeGen -lLLVMHexagonAsmParser
 -lLLVMHexagonDesc -lLLVMHexagonInfo -lLLVMCppBackendCodeGen
 -lLLVMCppBackendInfo -lLLVMBPFCodeGen -lLLVMBPFDesc -lLLVMBPFInfo
 -lLLVMBPFAsmPrinter -lLLVMARMDisassembler -lLLVMARMCodeGen
 -lLLVMARMAsmParser -lLLVMARMDesc -lLLVMARMInfo -lLLVMARMAsmPrinter
 -lLLVMAMDGPUCodeGen -lLLVMAMDGPUAsmParser -lLLVMAMDGPUDesc
 -lLLVMAMDGPUUtils -lLLVMAMDGPUInfo -lLLVMAMDGPUAsmPrinter
 -lLLVMAArch64Disassembler -lLLVMAArch64CodeGen -lLLVMAArch64AsmParser
 -lLLVMAArch64Desc -lLLVMAArch64Info -lLLVMAArch64AsmPrinter
 -lLLVMAArch64Utils -lLLVMMIRParser -lLLVMLibDriver -lLLVMOption
 -lLLVMTableGen -lLLVMLineEditor -lLLVMX86Disassembler -lLLVMX86AsmParser
 -lLLVMX86CodeGen -lLLVMSelectionDAG -lLLVMAsmPrinter -lLLVMX86Desc
 -lLLVMMCDisassembler -lLLVMX86Info -lLLVMX86AsmPrinter -lLLVMX86Utils
 -lLLVMMCJIT -lLLVMPasses -lLLVMipo -lLLVMVectorize -lLLVMLinker
 -lLLVMIRReader -lLLVMAsmParser -lLLVMDebugInfoCodeView -lLLVMInterpreter
 -lLLVMCodeGen -lLLVMScalarOpts -lLLVMInstCombine -lLLVMInstrumentation
 -lLLVMProfileData -lLLVMBitWriter -lLLVMOrcJIT -lLLVMTransformUtils
 -lLLVMExecutionEngine -lLLVMTarget -lLLVMAnalysis -lLLVMRuntimeDyld
 -lLLVMObject -lLLVMMCParser -lLLVMBitReader -lLLVMMC -lLLVMCore
 -lLLVMSupport)