#!/usr/bin/env python

import re
import os


UNITY_RUNNER = """\
#include "unity.h"

{externs}

int main(int argc, char* argv[])
{{
    UNITY_BEGIN();
{runners}
    return UNITY_END();
}}

""".format

UNITY_RUNNER_EXTERN = "extern void {name}(void);".format
UNITY_RUNNER_RUN_TEST = "    RUN_TEST({name});".format

def find_test_functions(src_file):
    pattern = re.compile(r"^\s*void\s+(test_.+)\s*\([void]*\)")
    functions = []
    with open(src_file, 'r') as f:
        for line in f:
            match = pattern.match(line)
            if match:
                functions.append(match.group(1))
    return functions


def append_test_functions(main_file, test_functions):
    ext_func_pattern = re.compile(r"^\s*extern\s*void\s*(test_.*)\s*\([void]*\);")
    run_test_pattern = re.compile(r"^\s*/*\s*RUN_TEST\((test_.*)\);")
    found_ext_tests = []
    found_run_tests = []
    with open(main_file, 'r') as f:
        for line in f:
            match = ext_func_pattern.match(line)
            if match:
                found_ext_tests.append(match.group(1))
            match = run_test_pattern.match(line)
            if match:
                found_run_tests.append(match.group(1))

    should_update_exts = False
    for func in test_functions:
        if func not in found_ext_tests:
            should_update_exts = True
            break
    else:
        # Not encountered a break statement in the for loop
        for func in found_ext_tests:
            if func not in test_functions:
                should_update_exts = True
                break

    should_update_runs = False
    for func in test_functions:
        if func not in found_run_tests:
            should_update_runs = True
            break
    else:
        # Not encountered a break statement in the for loop
        for func in found_run_tests:
            if func not in test_functions:
                should_update_runs = True
                break

    if should_update_runs or should_update_exts:
        externs = [UNITY_RUNNER_EXTERN(name=name) for name in test_functions]
        runners = [UNITY_RUNNER_RUN_TEST(name=name) for name in test_functions]

        main_src = UNITY_RUNNER(externs='\n'.join(externs),
                                runners='\n'.join(runners))

        with open(main_file, 'w') as f:
            f.write(main_src)


def update_all_runners():
    for dirname, dirs, files in os.walk(os.path.dirname(os.path.realpath(__file__))):
        source_dir = dirname.split(os.path.sep)[-1]
        test_files = []
        if source_dir == 'src':
            for file in files:
                if file.startswith('test_'):
                    test_files.append(file)

        test_functions = []
        if test_files:
            for file in test_files:
                test_functions.extend(find_test_functions(os.path.join(dirname, file)))

        if test_functions:
            if not 'main.c' in files:
                with open(os.path.join(dirname, 'main.c'), 'w') as f:
                    f.write('\n')
            append_test_functions(os.path.join(dirname, 'main.c'), test_functions)


if __name__ == '__main__':
    update_all_runners()
