PROJECT(PackageTest)
cmake_minimum_required(VERSION 2.8.12)

message("Cmake binary directory " ${CMAKE_BINARY_DIR})
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()


set(CMAKE_CXX_STANDARD 14)
option(CXX11 "Enable use of C++11 headers if available (requires client code use C++11)." ON)

ADD_EXECUTABLE(example example.cpp)
TARGET_LINK_LIBRARIES(example ${CONAN_LIBS})
