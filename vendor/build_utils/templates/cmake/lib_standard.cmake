# Create a library called "{name}" which includes the source file "{name}.{extension}".
ADD_LIBRARY({name} src/{name}.{extension})

# Make sure the compiler can find include files for our {name} library
# when other libraries or executables link to {name}
TARGET_INCLUDE_DIRECTORIES({name} PUBLIC ${{CMAKE_CURRENT_SOURCE_DIR}}/src)
