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


def ask_and_update_user():
    exec_or_lib = keep_bothering_user(
        "Do you want to add a 'lib' or 'executable'? ",
        lambda x: x is not None and (x.startswith('l') or x.startswith('e')))
    name = keep_bothering_user(
        "How should it be named? ",
        lambda x: x is not None)
    source = keep_bothering_user(
        "Do you want C or C++? ",
        lambda x: x is not None and x.startswith('c'))
    src_type = 'cpp' if source.endswith('+') else 'c'
    test_framework = extract_test_framework()
    if exec_or_lib.startswith('l'):
        create_library(name, src_type, test_framework)
    else:
        create_executable(name, src_type, test_framework)


def create_library(name, src_type, test_framework):
    print("Creating library: {}".format(name))
    libdir, srcdir = create_basic_source_dirs(BASE_DIR, name)

    if not libdir or not srcdir:
        print("Library {} already exists".format(name))
        return

    testdir = os.path.join(BASE_DIR, 'test')
    try:
        os.mkdir(testdir)
    except FileExistsError:
        pass

    testlibdir, testsrcdir = create_basic_source_dirs(BASE_DIR, os.path.join('test', name))

    if not testlibdir or not testsrcdir:
        print("Library test environment {} already exists".format(name))
        os.rmdir(srcdir)
        os.rmdir(libdir)

    insert_into_file_after_line(os.path.join(BASE_DIR, 'CMakeLists.txt'),
                                CMAKE_BASE_COMMENT,
                                CMAKE_SUBDIR(name=name))
    create_file(libdir, 'CMakeLists.txt',
                source=load_and_format_template('lib_standard.cmake',
                                                name, extension=src_type))
    create_file(srcdir, name + '.h',
                source=load_and_format_template('lib.h',
                                                name, PROJECT_NAME=PROJECT_NAME))
    create_file(srcdir, name + '.' + src_type,
                source=load_and_format_template('lib.c', name))

    if test_framework == 'gtest':
        test_lib = 'lib_gtest.cmake'
        main_src = 'gtest_main.c'
        test_src = 'gtest_src.c'
    elif test_framework == 'unity':
        test_lib = 'lib_unity.cmake'
        main_src = None
        test_src = 'unity_src.c'
    else:
        raise NotImplementedError("Undefined test framework")

    insert_into_file_after_line(os.path.join(testdir, 'CMakeLists.txt'),
                                CMAKE_TEST_COMMENT,
                                CMAKE_SUBDIR(name=name))

    create_file(testlibdir, 'CMakeLists.txt',
                source=load_and_format_template(test_lib,
                                                name, extension=src_type))
    if main_src:
        create_file(testsrcdir, 'main.' + src_type,
                    source=load_and_format_template(main_src, name))
    create_file(testsrcdir, 'test_' + name + '.' + src_type,
                source=load_and_format_template(test_src, name))


def create_executable(name, src_type, test_framework):
    print("Creating executable: {}".format(name))
    exedir, srcdir = create_basic_source_dirs(BASE_DIR, name)

    if not exedir or not srcdir:
        print("Executable {} already exists".format(name))
        return

    insert_into_file_after_line(os.path.join(BASE_DIR, 'CMakeLists.txt'),
                                CMAKE_BASE_COMMENT,
                                CMAKE_SUBDIR(name=name))

    create_file(exedir, 'CMakeLists.txt',
                source=load_and_format_template('project.cmake',
                                                name, extension=src_type))
    create_file(srcdir, 'main.' + src_type,
                source=load_and_format_template('main.c',
                                                name))


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


def create_basic_source_dirs(base_dir, name, lib_or_exec='lib'):
    basedir = os.path.join(base_dir, name)
    try:
        os.mkdir(basedir)
    except FileExistsError:
        return False, False
    else:
        srcdir = os.path.join(basedir, 'src')
        os.mkdir(srcdir)

    return basedir, srcdir


def create_file(*pathargs, source=None):
    with open(os.path.join(*pathargs), 'w') as f:
        f.writelines(source)


def load_and_format_template(template_name, name, **format_kwargs):
    paths = [BASE_DIR]
    if template_name.endswith('.cmake'):
        paths.append('cmake')
    paths.append(template_name)

    source = ''
    with open(os.path.join(*paths), 'r') as f:
        lines = f.readlines()
        source = ''.join(lines)

    return source.format(name=name,
                         Name=name.capitalize(),
                         NAME=name.upper(),
                         **format_kwargs)


def extract_test_framework():
    test_framework = None
    with open(os.path.join(BASE_DIR, 'CMakeLists.txt')) as f:
        for line in f:
            if 'TEST_FRAMEWORK_GTEST' in line and 'ON' in line:
                test_framework = 'gtest'
                break
            elif 'TEST_FRAMEWORK_UNITY' in line and 'ON' in line:
                test_framework = 'unity'
                break
    return test_framework



if __name__ == '__main__':
    ask_and_update_user()
