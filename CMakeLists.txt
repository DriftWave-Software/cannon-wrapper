cmake_minimum_required(VERSION 3.14)
project(edsdk_bindings)

set(CMAKE_CXX_STANDARD 14)

# Find Python and pybind11
find_package(Python COMPONENTS Interpreter Development REQUIRED)

# Use Python to find the pybind11 directory if find_package fails
execute_process(
    COMMAND ${Python_EXECUTABLE} -c "import pybind11; print(pybind11.get_cmake_dir())"
    OUTPUT_VARIABLE PYBIND11_CMAKE_DIR
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

if(PYBIND11_CMAKE_DIR)
    list(APPEND CMAKE_PREFIX_PATH ${PYBIND11_CMAKE_DIR})
    message(STATUS "Found pybind11 at: ${PYBIND11_CMAKE_DIR}")
endif()

# Try to find pybind11 package
find_package(pybind11 CONFIG)
if(NOT pybind11_FOUND)
    message(FATAL_ERROR "pybind11 not found. Please install with 'pip install pybind11'")
endif()

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

# Find EDSDK header directory
if(EXISTS "${EDSDK_PATH}/Header")
    set(EDSDK_HEADER_DIR "${EDSDK_PATH}/Header")
    message(STATUS "Found EDSDK header directory: ${EDSDK_HEADER_DIR}")
elseif(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/lib/EDSDK/Header")
    set(EDSDK_HEADER_DIR "${CMAKE_CURRENT_SOURCE_DIR}/lib/EDSDK/Header")
    message(STATUS "Found EDSDK header directory: ${EDSDK_HEADER_DIR}")
else()
    message(FATAL_ERROR "EDSDK header directory not found. Please check your EDSDK installation.")
endif()

# Find EDSDK library directory
if(EXISTS "${EDSDK_PATH}/Library")
    set(EDSDK_LIB_DIR "${EDSDK_PATH}/Library")
    message(STATUS "Found EDSDK library directory: ${EDSDK_LIB_DIR}")
elseif(EXISTS "${EDSDK_PATH}/lib")
    set(EDSDK_LIB_DIR "${EDSDK_PATH}/lib")
    message(STATUS "Found EDSDK library directory: ${EDSDK_LIB_DIR}")
else()
    message(FATAL_ERROR "EDSDK library directory not found. Please check your EDSDK installation.")
endif()

# Add definitions to disable MFC dependencies
add_definitions(-DSIMPLE_SDK_WRAPPER -DNOAFX -DNOMFC)

# Include directories - only include the EDSDK header, not our own headers with MFC dependencies
include_directories(
    ${EDSDK_HEADER_DIR}
)

# Create the pybind11 module - just compile the bindings.cpp file without the MFC-dependent files
pybind11_add_module(edsdk_bindings MODULE bindings.cpp)

# Link directories
if(WIN32)
    target_link_directories(edsdk_bindings PRIVATE ${EDSDK_LIB_DIR})
endif()

# Link EDSDK library
if(WIN32)
    if(EXISTS "${EDSDK_LIB_DIR}/EDSDK.lib")
        target_link_libraries(edsdk_bindings PRIVATE ${EDSDK_LIB_DIR}/EDSDK.lib)
    else()
        message(FATAL_ERROR "EDSDK.lib not found in ${EDSDK_LIB_DIR}")
    endif()
elseif(APPLE)
    # For macOS frameworks
    find_library(EDSDK_LIB EDSDK PATHS ${EDSDK_PATH})
    target_link_libraries(edsdk_bindings PRIVATE ${EDSDK_LIB})
else()
    # For Linux
    find_library(EDSDK_LIB edsdk PATHS ${EDSDK_PATH})
    target_link_libraries(edsdk_bindings PRIVATE ${EDSDK_LIB})
endif()

# On Windows, ensure the DLLs can be found at runtime
if(WIN32)
    if(EXISTS "${EDSDK_PATH}/Dll")
        add_custom_command(TARGET edsdk_bindings POST_BUILD
            COMMAND ${CMAKE_COMMAND} -E copy_directory
                "${EDSDK_PATH}/Dll"
                "$<TARGET_FILE_DIR:edsdk_bindings>")
    elseif(EXISTS "${EDSDK_PATH}/bin")
        add_custom_command(TARGET edsdk_bindings POST_BUILD
            COMMAND ${CMAKE_COMMAND} -E copy_directory
                "${EDSDK_PATH}/bin"
                "$<TARGET_FILE_DIR:edsdk_bindings>")
    else()
        message(WARNING "DLL directory not found. Runtime errors may occur.")
    endif()
endif() 