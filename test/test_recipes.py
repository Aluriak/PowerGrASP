"""Test of recipe'd graph compression.

Note that the test_* functions are generated
from the template_test_function function.

"""

from powergrasp.routines import compress_by_cc
from .definitions import unified_bubble, gen_test_functions

def test_recipe():
    found = unified_bubble(compress_by_cc('data/recipe-test.lp', recipe_file='data/recipe-test.txt'))
    expected = unified_bubble(BUBBLELINES.splitlines(keepends=False))
    assert found == expected

BUBBLELINES = """
NODE\ta
NODE\tb
NODE\tc
NODE\td
NODE\te
NODE\tf
NODE\th
NODE\ti
NODE\tj
SET\tPWRN-a-1-1\t1.0
SET\tPWRN-a-2-1\t1.0
SET\tPWRN-a-2-2\t1.0
EDGE\tPWRN-a-1-1\tc\t1.0
EDGE\tPWRN-a-2-1\tPWRN-a-2-2\t1.0
IN\ta\tPWRN-a-2-1
IN\tb\tPWRN-a-2-1
IN\tc\tPWRN-a-2-1
IN\td\tPWRN-a-2-2
IN\te\tPWRN-a-2-2
IN\tf\tPWRN-a-2-2
IN\th\tPWRN-a-1-1
IN\ti\tPWRN-a-1-1
IN\tj\tPWRN-a-1-1
"""
