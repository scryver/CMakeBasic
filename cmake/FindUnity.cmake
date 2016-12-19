SET(UNITY_INCLUDE_DIRS ${CMAKE_SOURCE_DIR}/vendor/Unity/src)

IF(NOT EXISTS ${UNITY_INCLUDE_DIRS})
    # Could not find unity source directory
    MESSAGE("Going to pull Unity sources")

    EXECUTE_PROCESS(COMMAND git submodule update --init -- vendor/Unity
                    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR})
ENDIF()

ADD_LIBRARY(Unity      STATIC ${UNITY_INCLUDE_DIRS}/unity.c)

IF(NOT WIN32 OR MINGW)
    # TARGET_INCLUDE_DIRECTORIES(Unity PUBLIC ${UNITY_INCLUDE_DIRS})
    SET(UNITY_LIBRARIES Unity)
ELSE()
    MESSAGE("Not implemented")
ENDIF()

SET(UNITY_FOUND "YES")
