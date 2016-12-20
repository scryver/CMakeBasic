FILE(GLOB SRCS src/*.{extension})

ADD_EXECUTABLE(test{Name} ${{SRCS}})

TARGET_LINK_LIBRARIES(test{Name}
    {name}
    ${{TEST_FRAMEWORK_LIBRARIES}}
)

INCLUDE_DIRECTORIES(${{TEST_FRAMEWORK_INCLUDE_DIRS}})

# ADD_CUSTOM_COMMAND(TARGET test{Name} POST_BUILD COMMAND "./test{Name}")
ADD_TEST({Name} test{Name})
