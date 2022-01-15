cmake_minimum_required(VERSION 3.18)
project(my_proj LANGUAGES C Fortran)

# Turn off obsolete code
option(OLDALLOC "Old alloction for pgf95" OFF)

# Set compiler arguments
if(CMAKE_Fortran_COMPILER_ID MATCHES "GNU")
  set(CMAKE_Fortran_FLAGS "-fallow-argument-mismatch" ${CMAKE_Fortran_FLAGS})
endif()
set(CMAKE_Fortran_PREPROCESS ON)

# Find BLAS and LAPACK
include(CMakeFindDependencyMacro)
find_dependency(BLAS)
find_dependency(LAPACK)
find_package(BLAS) 
find_package(LAPACK)

# Build shared library
set(srcs)
add_subdirectory(src)
add_library(dlfind SHARED ${srcs})
target_link_libraries(dlfind ${BLAS_LIBRARIES} ${LAPACK_LIBRARIES})

# Install
if(SKBUILD)
  install(TARGETS dlfind LIBRARY DESTINATION libdlfind)
endif()
