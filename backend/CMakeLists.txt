project(naivescript)
cmake_minimum_required(VERSION 2.8)
SET(CMAKE_C_COMPILER gcc)
SET(CMAKE_CXX_COMPILER g++)

file(GLOB_RECURSE sources serialize/SerializeFile.cc serialize/SerializeFile.h serialize/SerializeStructure.h)
file(GLOB_RECURSE sources_test test.cc)

add_executable(testNS  ${sources} ${sources_test})
target_compile_options(testNS PUBLIC -O0 -std=c++11 -Wall -lm -lpthread)
#target_link_libraries(test PUBLIC gflags glog)