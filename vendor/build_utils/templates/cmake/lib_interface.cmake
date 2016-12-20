# Create a interface library which is only build if used in another project
# This helps because some files depend on configuration through a header file
ADD_LIBRARY({name} INTERFACE)

# Make sure the compiler can find include files for our {name} library
# when other libraries or executables link to {name}
TARGET_INCLUDE_DIRECTORIES({name} INTERFACE ${{CMAKE_CURRENT_SOURCE_DIR}}/src)

# The source files can be found through:
# GET_TARGET_PROPERTIES({name}_SRC_DIR {name} SOURCE_DIR)
SET_TARGET_PROPERTIES({name} PROPERTIES SOURCE_DIR ${{CMAKE_CURRENT_SOURCE_DIR}}/src)
