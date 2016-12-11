# We need thread support
FIND_PACKAGE(Threads REQUIRED)

INCLUDE(ExternalProject)

SET(GTEST_FORCE_SHARED_CRT ON)
SET(GTEST_DISABLE_PTHREADS OFF)

IF(MINGW)
    SET(GTEST_DISABLE_PTHREADS ON)
ENDIF()

ExternalProject_Add(googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    CMAKE_ARGS -DCMAKE_ARCHIVE_OUTPUT_DIRECTORY_DEBUG:PATH=DebugLibs
    -DCMAKE_ARCHIVE_OUTPUT_DIRECTORY_RELEASE:PATH=ReleaseLibs
    -DCMAKE_CXX_FLAGS=${MSVC_COMPILER_DEFS}
    -Dgtest_force_shared_crt=${GTEST_FORCE_SHARED_CRT}
    -Dgtest_disable_pthreads=${GTEST_DISABLE_PTHREADS}
    -DBUILD_GTEST=ON
    PREFIX "${CMAKE_CURRENT_BINARY_DIR}"
    # Disable install step
    INSTALL_COMMAND ""
)

# Specify include dir
ExternalProject_Get_Property(googletest source_dir)
SET(GTEST_INCLUDE_DIRS ${source_dir}/googletest/include)

# Specify MainTest's link libraries
ExternalProject_Get_Property(googletest binary_dir)
SET(GTEST_LIBS_DIR ${binary_dir}/googlemock/gtest)

if(NOT WIN32 OR MINGW)
    FIND_LIBRARY( GTEST_gtest_LIBRARY
        NAMES
            gtest
        HINTS
            "${GTEST_LIBS_DIR}"
        PATHS
            "${GTEST_LIBS_DIR}"
        DOC
            "The gtest library"
    )
    FIND_LIBRARY( GTEST_gtest_main_LIBRARY
        NAMES
            gtest_main
        HINTS
            "${GTEST_LIBS_DIR}"
        PATHS
            "${GTEST_LIBS_DIR}"
        DOC
            "The gtest_main library"
    )
    SET(GTEST_LIBRARIES "${GTEST_gtest_LIBRARY}"
                        "${GTEST_gtest_main_LIBRARY}"
                        "${CMAKE_THREAD_LIBS_INIT}")
else()
    MESSAGE("Not implemented")
    # SET(GTEST_LIBRARIES
    #     debug ${GTEST_LIBS_DIR}/DebugLibs/${CMAKE_FIND_LIBRARY_PREFIXES}gtest${CMAKE_FIND_LIBRARY_SUFFIXES}
    #     debug ${GTEST_LIBS_DIR}/DebugLibs/${CMAKE_FIND_LIBRARY_PREFIXES}gtest_main${CMAKE_FIND_LIBRARY_SUFFIXES}
    #     optimized ${GTEST_LIBS_DIR}/ReleaseLibs/${CMAKE_FIND_LIBRARY_PREFIXES}gtest${CMAKE_FIND_LIBRARY_SUFFIXES}
    #     optimized ${GTEST_LIBS_DIR}/ReleaseLibs/${CMAKE_FIND_LIBRARY_PREFIXES}gtest_main${CMAKE_FIND_LIBRARY_SUFFIXES}
    # )
endif()

SET(GTEST_FOUND "YES")
