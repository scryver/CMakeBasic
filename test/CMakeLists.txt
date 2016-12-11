# We need thread support

IF (TEST_FRAMEWORK_GTEST)
    MESSAGE("Using GTest for testing")
    FIND_PACKAGE(GTest REQUIRED)
    SET(TEST_FRAMEWORK_INCLUDE_DIRS ${GTEST_INCLUDE_DIRS})
    SET(TEST_FRAMEWORK_LIBRARIES    ${GTEST_LIBRARIES})
ELSE()
    MESSAGE("Using Unity for testing")
    IF (TEST_FRAMEWORK_UNITY)
        MESSAGE("Not implemented unity")
    ENDIF()
ENDIF()

IF (FULLTEST)
    ADD_DEFINITIONS(-DFULL_TESTS)
ENDIF (FULLTEST)

# Project test directories | Do not edit/remove this comment!!!
