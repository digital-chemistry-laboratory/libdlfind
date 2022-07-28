cmake_minimum_required(VERSION 3.18)
project(libdlfind LANGUAGES Fortran)

# Follow GNU conventions for installing directories
include(GNUInstallDirs)

# Turn on preprocessing
set(CMAKE_Fortran_PREPROCESS ON)

# Find BLAS and LAPACK
include(CMakeFindDependencyMacro)
find_dependency(BLAS)
find_dependency(LAPACK)
find_package(BLAS REQUIRED)
find_package(LAPACK REQUIRED)

# Build shared library
set(srcs)
add_subdirectory(src)
add_library(dlfind SHARED ${srcs})
target_link_libraries(dlfind ${BLAS_LIBRARIES} ${LAPACK_LIBRARIES})

# Set compiler arguments
if(CMAKE_Fortran_COMPILER_ID STREQUAL GNU AND CMAKE_Fortran_COMPILER_VERSION
                                              VERSION_LESS 10)
  target_compile_options(dlfind PRIVATE -Wargument-mismatch)
elseif(CMAKE_Fortran_COMPILER_ID STREQUAL GNU AND CMAKE_Fortran_COMPILER_VERSION
                                                  VERSION_GREATER 9)
  target_compile_options(dlfind PRIVATE -fallow-argument-mismatch)
endif()

# Install
if(SKBUILD)
  if(WIN32)
    # Set flags for Windows compatibility
    set_target_properties(dlfind PROPERTIES LIBRARY_PREFIX "lib")
    set_target_properties(dlfind PROPERTIES WINDOWS_EXPORT_ALL_SYMBOLS ON)

    # Link statically against dependencies for Windows
    if(CMAKE_Fortran_COMPILER_ID MATCHES "GNU")
      target_link_options(dlfind PRIVATE "-static")
    endif()
  endif()

  message(STATUS "The project is built using scikit-build")
  install(
    TARGETS dlfind
    LIBRARY DESTINATION libdlfind
    ARCHIVE DESTINATION libdlfind
    RUNTIME DESTINATION libdlfind)
else()
  set_target_properties(dlfind PROPERTIES PUBLIC_HEADER "include/libdlfind.h")
  install(
    TARGETS dlfind
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_LIBDIR}
    PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
endif()
