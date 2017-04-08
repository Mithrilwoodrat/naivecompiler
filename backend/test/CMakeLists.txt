Set( testSrc ${NSWorkingPath}/test/test.cc )

Add_Executable( testNS ${testSrc} )

Target_Include_Directories( testNS PUBLIC ${NSIncludeDir} )

Set_Target_Properties( testNS PROPERTIES 
    OUTPUT_NAME testNaiveScript )

Set(libDir ${CMAKE_CURRENT_BINARY_DIR})
link_directories( libDir )

Set_Target_Properties( testNS PROPERTIES 
    RUNTIME_OUTPUT_DIRECTORY ${NSOutputDir})

Target_Link_Libraries( testNS PUBLIC -lnaivescript )

Add_Dependencies( testNS NaiveScript )