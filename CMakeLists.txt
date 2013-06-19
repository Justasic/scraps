# Cmake require version we're using, too old? too bad.
cmake_minimum_required(VERSION 2.8 FATAL_ERROR)

# do not like building from source in the same directory as the source tree
# force the user to build somewhere else like build/
if(${CMAKE_CURRENT_SOURCE_DIR} STREQUAL ${CMAKE_CURRENT_BINARY_DIR} AND NOT WIN32)
        message(FATAL_ERROR "You can not use CMake to build RTCW from the root of it's source tree! Remove the CMakeCache.txt file from this directory, then create a separate directory (either below this directory or elsewhere), and then re-run CMake from there.")
endif(${CMAKE_CURRENT_SOURCE_DIR} STREQUAL ${CMAKE_CURRENT_BINARY_DIR} AND NOT WIN32)

project(OpenGLTest CXX)
enable_language(C)

set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake)

# Project version
SET(${PROJECT_NAME}_MAJOR_VERSION 0)
SET(${PROJECT_NAME}_MINOR_VERSION 0)
SET(${PROJECT_NAME}_PATCH_LEVEL 0)
message(STATUS ${WolfSP_SOURCE_DIR})

# Get the git revision location for the branch we're on
if(EXISTS "${${PROJECT_NAME}_SOURCE_DIR}/.git/HEAD")
	file(READ ${${PROJECT_NAME}_SOURCE_DIR}/.git/HEAD GIT_HEAD_LOC)
	string(LENGTH ${GIT_HEAD_LOC} HEAD_LEN)
	math(EXPR LEN "${HEAD_LEN} - 5")
	string(SUBSTRING ${GIT_HEAD_LOC} 5 ${LEN} GIT_HEAD)
endif(EXISTS "${${PROJECT_NAME}_SOURCE_DIR}/.git/HEAD")
	
# Get the git revision we're on for the version string
if(EXISTS "${${PROJECT_NAME}_SOURCE_DIR}/.git/${GIT_HEAD}")
	file(READ ${${PROJECT_NAME}_SOURCE_DIR}/.git/${GIT_HEAD} VERSION_STR)
	# Get the length of the string
	string(LENGTH ${VERSION_STR} VERSION_LEN)
	# Subtract 7 from the string's length
	math(EXPR VERSION_NUM_LEN "${VERSION_LEN} - ${VERSION_LEN} + 7")
	# Extract the value from the string
	string(SUBSTRING ${VERSION_STR} 0 ${VERSION_NUM_LEN} VERSION_GIT)
endif(EXISTS "${${PROJECT_NAME}_SOURCE_DIR}/.git/${GIT_HEAD}")

# Set our version strings
SET(VERSION_SIMPLE "${${PROJECT_NAME}_MAJOR_VERSION}.${${PROJECT_NAME}_MINOR_VERSION}.${${PROJECT_NAME}_PATCH_LEVEL}")
SET(VERSION_FULL "${${PROJECT_NAME}_MAJOR_VERSION}.${${PROJECT_NAME}_MINOR_VERSION}.${${PROJECT_NAME}_PATCH_LEVEL}-${VERSION_GIT}")

# include cmake stuff for checking various system specific defines
include(CheckTypeSize)
include(CheckFunctionExists)
include(CheckIncludeFile)
include(CheckLibraryExists)
include(CheckCXXCompilerFlag)
include(CheckCCompilerFlag)
include(TestBigEndian)

find_package(OpenGL REQUIRED)
find_package(GLFW REQUIRED)
find_package(FTGL REQUIRED)
include_directories(${OPENGL_INCLUDES} ${GLFW_INCLUDE_DIR} ${FTGL_INCLUDE_DIRS})

if(CMAKE_C_COMPILER_ID STREQUAL "Clang")
	add_definitions(-D__extern_always_inline=inline)
endif(CMAKE_C_COMPILER_ID STREQUAL "Clang")

# Check type sizes since we need them
check_type_size(int8_t INT8_T)
check_type_size(uint8_t UINT8_T)
check_type_size(int16_t INT16_T)
check_type_size(uint16_t UINT16_T)
check_type_size(int32_t INT32_T)
check_type_size(uint32_t UINT32_T)
check_type_size(int64_t INT64_T)
check_type_size(uint64_t UINT64_T)

file(GLOB OPENGL_SRC RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} "*.cpp")
list(SORT OPENGL_SRC)

set_source_files_properties(${OPENGL_SRC} PROPERTIES LANGUAGE CXX COMPILE_FLAGS "${CXXFLAGS} -g -std=c++11")

add_executable(${PROJECT_NAME} ${OPENGL_SRC})
add_dependencies(${PROJECT_NAME} ${OPENGL_LIBRARY} ${GLFW_LIBRARY} ${FTGL_LIBRARIES})
target_link_libraries(${PROJECT_NAME} ${OPENGL_LIBRARY} ${GLFW_LIBRARY} ${FTGL_LIBRARIES})

set_target_properties(${PROJECT_NAME} PROPERTIES LINKER_LANGUAGE CXX PREFIX "" SUFFIX "")
