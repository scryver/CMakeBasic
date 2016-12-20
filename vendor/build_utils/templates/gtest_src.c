#include <gtest/gtest.h>

#include "{name}.h"

TEST({Name}, StommeFunc)
{{
    int a = 5;
    EXPECT_EQ({name}_func(a), 25);
}}
