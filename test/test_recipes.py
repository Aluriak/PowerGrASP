"""Test of recipe'd graph compression.

Note that the test_* functions are generated
from the template_test_function function.

"""

from powergrasp.constants import RECIPE_FILE
from powergrasp.routines import compress_by_cc
from .definitions import unified_bubble, gen_test_functions

if RECIPE_FILE:
    def test_recipe():
        found = unified_bubble(compress_by_cc('data/recipe-test.lp'))
        expected = unified_bubble(BUBBLELINES.splitlines(keepends=False))
        assert found == expected

BUBBLELINES = """

"""
