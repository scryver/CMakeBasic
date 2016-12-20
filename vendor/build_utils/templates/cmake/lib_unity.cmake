FILE(GLOB ALL_TEST_SRCS src/test_*.{extension})

INCLUDE_DIRECTORIES(${{TEST_FRAMEWORK_INCLUDE_DIRS}})

FOREACH(TEST_SRC ${{ALL_TEST_SRCS}})
    GET_FILENAME_COMPONENT(TEST_NAME ${{TEST_SRC}} NAME)
    STRING(REPLACE "test_" "main_" MAIN_SRC ${{TEST_SRC}})
    STRING(REPLACE "test_" "" TEST_NAME ${{TEST_NAME}})
    STRING(REPLACE ".{extension}" "" TEST_NAME ${{TEST_NAME}})

    IF (EXISTS "${{{NAME}_SRC_DIR}}/${{TEST_NAME}}.{extension}")
        ADD_EXECUTABLE(test_${{TEST_NAME}} ${{TEST_SRC}} ${{MAIN_SRC}}
                    ${{{NAME}_SRC_DIR}}/${{TEST_NAME}}.{extension}
                    )
    ELSE()
        ADD_EXECUTABLE(test_${{TEST_NAME}} ${{TEST_SRC}} ${{MAIN_SRC}})
    ENDIF()

    TARGET_LINK_LIBRARIES(test_${{TEST_NAME}} {name} ${{TEST_FRAMEWORK_LIBRARIES}})

    ADD_TEST(${{TEST_NAME}} test_${{TEST_NAME}})
ENDFOREACH()
