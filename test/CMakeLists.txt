# We need thread support

IF (TEST_FRAMEWORK_GTEST)
    MESSAGE("Using GTest for testing")
    FIND_PACKAGE(GTest REQUIRED)
    SET(TEST_FRAMEWORK_INCLUDE_DIRS ${GTEST_INCLUDE_DIRS})
    SET(TEST_FRAMEWORK_LIBRARIES    ${GTEST_LIBRARIES})
ELSE()
    MESSAGE("Using Unity for testing")
    IF (TEST_FRAMEWORK_UNITY)
        FIND_PACKAGE(Unity REQUIRED)
        FIND_PACKAGE(fff REQUIRED)
        SET(TEST_FRAMEWORK_INCLUDE_DIRS ${UNITY_INCLUDE_DIRS} ${FFF_INCLUDE_DIRS})
        SET(TEST_FRAMEWORK_LIBRARIES    ${UNITY_LIBRARIES})

        ADD_CUSTOM_TARGET(alwaysRebuild ALL DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/__some_imagenary_file.x)
        ADD_CUSTOM_COMMAND(OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/__some_imagenary_file.x COMMAND echo "Always Rebuilding")

        ADD_CUSTOM_COMMAND(TARGET alwaysRebuild PRE_BUILD COMMAND python3 ${CMAKE_CURRENT_SOURCE_DIR}/update_runners.py)

    ELSE()
        MESSAGE("Not implemented unkown test framework")
    ENDIF()
ENDIF()

IF (FULLTEST)
    ADD_DEFINITIONS(-DFULL_TESTS)
ENDIF (FULLTEST)

# Project test directories | Do not edit/remove this comment!!!
