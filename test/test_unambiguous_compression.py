"""Test of graph compression.

Note that the test_* functions are generated
from the template_test_function function.

"""

from powergrasp.routines import compress_by_cc
from .test_cases import cases
from .definitions import unified_bubble, gen_test_functions


def template_test_function(file:str, bubblelines:str):
    def test_function():
        found = unified_bubble(compress_by_cc(file))
        expected = unified_bubble(bubblelines.splitlines(keepends=False))
        assert found == expected
    return test_function


for name, func in gen_test_functions(cases, template_test_function):
    globals()[name] = func
