#include "unity.h"
#include "fff.h"
DEFINE_FFF_GLOBALS;

#include "{name}.h"

void test_StommeFunc_should_Multiply(void)
{{
    int a = 5;
    TEST_ASSERT_EQUAL(25, {name}_func(a));
}}
