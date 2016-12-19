SET(FFF_INCLUDE_DIRS ${CMAKE_SOURCE_DIR}/vendor/fff)

# Test one directory deeper to be sure the directory is not empty
IF(NOT EXISTS ${FFF_INCLUDE_DIRS}/test)
    # Could not find fff source directory
    MESSAGE("Going to pull FFF sources")

    EXECUTE_PROCESS(COMMAND git submodule update --init -- vendor/fff
                    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR})
ENDIF()

SET(FFF_FOUND "YES")
