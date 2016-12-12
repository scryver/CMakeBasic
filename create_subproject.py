#!/usr/bin/env python

from __future__ import print_function
from builtins import input

import os

"""

1. Choose exec or lib
2. create dir
3. if lib => create test dir
4. create appropiate CMakeLists.txt
5. generate some basic files

"""

BASE_DIR = os.path.abspath(os.path.curdir)
PROJECT_NAME = os.getcwd().split(os.path.sep)[-1].upper()

CMAKE_BASE_COMMENT = '# Project directories | Do not edit/remove this comment!!!'
CMAKE_TEST_COMMENT = '# Project test directories | Do not edit/remove this comment!!!'
CMAKE_SUBDIR = 'ADD_SUBDIRECTORY({name})'.format

CMAKE_LIBRARY = """\
# Create a library called "{name}" which includes the source file "{name}.cpp".
ADD_LIBRARY({name} src/{name}.cpp)

# Make sure the compiler can find include files for our {name} library
# when other libraries or executables link to {name}
TARGET_INCLUDE_DIRECTORIES({name} PUBLIC ${{CMAKE_CURRENT_SOURCE_DIR}}/src)

""".format

CMAKE_LIBRARY_HEADER = """\
#ifndef {PROJECT_NAME}_{NAME}_H
#define {PROJECT_NAME}_{NAME}_H

int {name}_func(int a);

#endif  // {PROJECT_NAME}_{NAME}_H

""".format

CMAKE_LIBRARY_SOURCE = """\
#include "{name}.h"

int {name}_func(int a)
{{
    return a * 5;
}}

""".format

CMAKE_TEST_LIBRARY = """\
FILE(GLOB SRCS src/*.cpp)

ADD_EXECUTABLE(test{CapName} ${{SRCS}})

TARGET_LINK_LIBRARIES(test{CapName}
    {name}
    ${{TEST_FRAMEWORK_LIBRARIES}}
)

INCLUDE_DIRECTORIES(${{TEST_FRAMEWORK_INCLUDE_DIRS}})

# ADD_CUSTOM_COMMAND(TARGET test{CapName} POST_BUILD COMMAND "./test{CapName}")
ADD_TEST({CapName} test{CapName})

""".format

CMAKE_TEST_MAIN = """\
#include <gtest/gtest.h>

int main(int argc, char* argv[])
{{
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}}

""".format

CMAKE_TEST_SOURCE = """\
#include <gtest/gtest.h>

#include "{name}.h"

TEST({CapName}, StommeFunc)
{{
    int a = 5;
    EXPECT_EQ({name}_func(a), 25);
}}

""".format

CMAKE_EXECUTABLE = """\
SET(EXECUTABLE_NAME "{name}")

ADD_EXECUTABLE(${{EXECUTABLE_NAME}}
               src/main.cpp)

# TARGET_LINK_LIBRARIES(${{EXECUTABLE_NAME}} LINK_PUBLIC voorbeeld)
""".format

CMAKE_EXECUTABLE_MAIN = """\
#include <stdio.h>


int main(int argc, char const *argv[])
{{
    printf("Hallo allemaal, groetjes van {name}\\n");
    return 0;
}}

""".format


def ask_and_update_user():
    exec_or_lib = keep_bothering_user(
        "Do you want to add a 'lib' or 'executable'? ",
        lambda x: x is not None and (x.startswith('l') or x.startswith('e')))
    name = keep_bothering_user(
        "How should it be named? ",
        lambda x: x is not None)
    if exec_or_lib.startswith('l'):
        create_library(name)
    else:
        create_executable(name)


def create_library(name):
    print("Creating library: {}".format(name))
    libdir, srcdir = create_basic_source_dirs(name)

    if not libdir or not srcdir:
        print("Library {} already exists".format(name))
        return

    testdir = os.path.join(BASE_DIR, 'test')
    try:
        os.mkdir(testdir)
    except FileExistsError:
        pass

    testlibdir, testsrcdir = create_basic_source_dirs(os.path.join('test', name))

    if not testlibdir or not testsrcdir:
        print("Library test environment {} already exists".format(name))
        os.rmdir(srcdir)
        os.rmdir(libdir)

    insert_into_file_after_line(os.path.join(BASE_DIR, 'CMakeLists.txt'),
                                CMAKE_BASE_COMMENT,
                                CMAKE_SUBDIR(name=name))
    create_file_and_format(libdir, 'CMakeLists.txt',
                           source=CMAKE_LIBRARY, name=name)
    create_file_and_format(srcdir, name + '.h',
                           source=CMAKE_LIBRARY_HEADER,
                           PROJECT_NAME=PROJECT_NAME, NAME=name.upper(),
                           name=name)
    create_file_and_format(srcdir, name + '.cpp',
                           source=CMAKE_LIBRARY_SOURCE,
                           name=name)

    insert_into_file_after_line(os.path.join(testdir, 'CMakeLists.txt'),
                                CMAKE_TEST_COMMENT,
                                CMAKE_SUBDIR(name=name))
    create_file_and_format(testlibdir, 'CMakeLists.txt',
                           source=CMAKE_TEST_LIBRARY,
                           name=name, CapName=name.capitalize())
    create_file_and_format(testsrcdir, 'main.cpp',
                           source=CMAKE_TEST_MAIN)
    create_file_and_format(testsrcdir, 'test_' + name + '.cpp',
                           source=CMAKE_TEST_SOURCE,
                           name=name, CapName=name.capitalize())


def create_executable(name):
    print("Creating executable: {}".format(name))
    exedir, srcdir = create_basic_source_dirs(name)

    if not exedir or not srcdir:
        print("Executable {} already exists".format(name))
        return

    insert_into_file_after_line(os.path.join(BASE_DIR, 'CMakeLists.txt'),
                                CMAKE_BASE_COMMENT,
                                CMAKE_SUBDIR(name=name))
    create_file_and_format(exedir, 'CMakeLists.txt',
                           source=CMAKE_EXECUTABLE, name=name)
    create_file_and_format(srcdir, 'main.cpp',
                           source=CMAKE_EXECUTABLE_MAIN,
                           name=name)


def keep_bothering_user(question, validator):
    answer = None
    while not validator(answer):
        answer = input(question)
    return answer


def insert_into_file_after_line(filename, line_to_find, line_to_insert):
    with open(filename, 'r') as f:
        lines = f.readlines()

    idx = lines.index(line_to_find + '\n')
    lines.insert(idx + 1, line_to_insert + '\n')

    with open(filename, 'w') as f:
        f.writelines(lines)


def create_basic_source_dirs(name, lib_or_exec='lib'):
    basedir = os.path.join(BASE_DIR, name)
    try:
        os.mkdir(basedir)
    except FileExistsError:
        return False, False
    else:
        srcdir = os.path.join(basedir, 'src')
        os.mkdir(srcdir)

    return basedir, srcdir


def create_file_and_format(*pathargs, source=None, **kwargs):
    with open(os.path.join(*pathargs), 'w') as f:
        f.writelines(source(**kwargs))


if __name__ == '__main__':
    ask_and_update_user()
