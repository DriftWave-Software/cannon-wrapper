cmake_minimum_required(VERSION 3.14)
project(edsdk_bindings)

set(CMAKE_CXX_STANDARD 14)

# Find pybind11
find_package(pybind11 REQUIRED)

# Set EDSDK paths (can be overridden from setup.py)
if(NOT DEFINED EDSDK_PATH)
    if(CMAKE_SIZEOF_VOID_P EQUAL 8)
        # 64-bit default
        set(EDSDK_PATH "${CMAKE_CURRENT_SOURCE_DIR}/lib/EDSDK_64")
    else()
        # 32-bit default
        set(EDSDK_PATH "${CMAKE_CURRENT_SOURCE_DIR}/lib/EDSDK")
    endif()
endif()

message(STATUS "Using EDSDK path: ${EDSDK_PATH}")

# Include directories
include_directories(
    ${EDSDK_PATH}/include
    ${CMAKE_CURRENT_SOURCE_DIR}/edsdk/include
)

# Source files
file(GLOB EDSDK_SOURCES
    ${CMAKE_CURRENT_SOURCE_DIR}/edsdk/src/*.cpp
)

add_library(edsdk_bindings MODULE bindings.cpp ${EDSDK_SOURCES})

# Link directories
if(WIN32)
    link_directories(${EDSDK_PATH}/lib)
endif()

# Link pybind11
target_link_libraries(edsdk_bindings PRIVATE pybind11::module)

# Link EDSDK library
if(WIN32)
    target_link_libraries(edsdk_bindings PRIVATE ${EDSDK_PATH}/lib/EDSDK.lib)
elseif(APPLE)
    # For macOS frameworks
    find_library(EDSDK_LIB EDSDK PATHS ${EDSDK_PATH})
    target_link_libraries(edsdk_bindings PRIVATE ${EDSDK_LIB})
else()
    # For Linux
    find_library(EDSDK_LIB edsdk PATHS ${EDSDK_PATH})
    target_link_libraries(edsdk_bindings PRIVATE ${EDSDK_LIB})
endif()

# On Windows, set the output name to .pyd for Python
if (WIN32)
    set_target_properties(edsdk_bindings PROPERTIES SUFFIX ".pyd")
endif() 