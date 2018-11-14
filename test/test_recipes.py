"""Test of recipe'd graph compression.

Note that the test_* functions are generated
from the template_test_function function.

"""

import pytest
from powergrasp.constants import USE_STAR_MOTIF
from powergrasp.routines import compress_by_cc
from powergrasp.recipe import RecipeError
from .definitions import unified_bubble, gen_test_functions


def test_simple_recipe():
    found = unified_bubble(compress_by_cc('data/recipe-test.lp', recipe_file='data/recipe-test.txt'))
    expected = unified_bubble(BUBBLELINES_SIMPLE.splitlines(keepends=False))
    # with open('out/out.bbl', 'w') as fd:
        # fd.write('\n'.join(found))
    assert found == expected

def test_recipe_options():
    found = unified_bubble(compress_by_cc('data/recipe-option-test.lp', recipe_file='data/recipe-option-test.txt'))
    expected = unified_bubble(BUBBLELINES_OPTIONS.splitlines(keepends=False))
    # with open('out/out.bbl', 'w') as fd:
        # fd.write('\n'.join(found))
    assert found == expected

def test_recipe_error_because_of_unknow_nodes():
    with pytest.raises(RecipeError):
        unified_bubble(compress_by_cc('data/recipe-option-test.lp', recipe_file="""
biclique	c	g h i
biclique,open	a b	d e
biclique	unexisting nodes	are not compressible
"""))

def test_recipe_error_because_of_impossible_compression():
    with pytest.raises(RecipeError):
        unified_bubble(compress_by_cc('data/recipe-option-test.lp', recipe_file="""
biclique	c	g h i
biclique	a b	d e c
"""))

def test_recipe_error_because_of_overlapping_entries():
    with pytest.raises(RecipeError):
        unified_bubble(compress_by_cc('data/recipe-option-test.lp', recipe_file="""
biclique	c	g h i
biclique	a b	d e
biclique	a b c	d e f
"""))


if USE_STAR_MOTIF:
    BUBBLELINES_SIMPLE = """
    NODE\ta
    NODE\tb
    NODE\tc
    NODE\td
    NODE\te
    NODE\tf
    NODE\tg
    NODE\th
    NODE\ti
    NODE\tj
    SET\tPWRN-a-1-1\t1.0
    SET\tPWRN-a-2-1\t1.0
    SET\tPWRN-a-2-2\t1.0
    SET\tPWRN-a-5-1\t1.0
    IN\ta\tPWRN-a-2-1
    IN\tb\tPWRN-a-2-1
    IN\td\tPWRN-a-2-2
    IN\te\tPWRN-a-2-2
    IN\tf\tPWRN-a-5-1
    IN\tg\tPWRN-a-1-1
    IN\th\tPWRN-a-1-1
    IN\ti\tPWRN-a-1-1
    IN\tj\tPWRN-a-5-1
    EDGE\tPWRN-a-1-1\tc\t1.0
    EDGE\tPWRN-a-2-1\tPWRN-a-2-2\t1.0
    EDGE\tPWRN-a-2-1\tf\t1.0
    EDGE\tPWRN-a-2-2\tc\t1.0
    EDGE\tPWRN-a-5-1\tc\t1.0
    """
    BUBBLELINES_OPTIONS = """
    NODE\ta
    NODE\tb
    NODE\tc
    NODE\td
    NODE\te
    NODE\tf
    NODE\tg
    NODE\th
    NODE\ti
    NODE\tj
    NODE\tk
    NODE\tl
    NODE\tm
    SET\tPWRN-a-1-1\t1.0
    SET\tPWRN-a-2-1\t1.0
    SET\tPWRN-a-2-2\t1.0
    SET\tPWRN-a-4-1\t1.0
    IN\ta\tPWRN-a-2-1
    IN\tb\tPWRN-a-2-1
    IN\tc\tPWRN-a-2-1
    IN\td\tPWRN-a-2-2
    IN\te\tPWRN-a-2-2
    IN\tf\tPWRN-a-2-2
    IN\tg\tPWRN-a-1-1
    IN\th\tPWRN-a-1-1
    IN\ti\tPWRN-a-1-1
    IN\tj\tPWRN-a-4-1
    IN\tk\tPWRN-a-4-1
    EDGE\tPWRN-a-1-1\tc\t1.0
    EDGE\tPWRN-a-2-1\tPWRN-a-2-2\t1.0
    EDGE\tPWRN-a-4-1\tc\t1.0
    EDGE\tc\tl\t1.0
    EDGE\tc\tm\t1.0
    """
else:
    # in such case, the stars are handled as bicliques, and in this case,
    #  node c being smaller than its neighbor, it is placed in set 1 instead of 2.
    BUBBLELINES_SIMPLE = """
    NODE\ta
    NODE\tb
    NODE\tc
    NODE\td
    NODE\te
    NODE\tf
    NODE\tg
    NODE\th
    NODE\ti
    NODE\tj
    SET\tPWRN-a-2-1\t1.0
    SET\tPWRN-a-2-2\t1.0
    # Sets modifications:
    SET\tPWRN-a-1-2\t1.0
    SET\tPWRN-a-5-2\t1.0
    IN\ta\tPWRN-a-2-1
    IN\tb\tPWRN-a-2-1
    IN\td\tPWRN-a-2-2
    IN\te\tPWRN-a-2-2
    # Inclusions modifications:
    IN\tf\tPWRN-a-5-2
    IN\tg\tPWRN-a-1-2
    IN\th\tPWRN-a-1-2
    IN\ti\tPWRN-a-1-2
    IN\tj\tPWRN-a-5-2
    EDGE\tPWRN-a-2-1\tPWRN-a-2-2\t1.0
    EDGE\tPWRN-a-2-1\tf\t1.0
    EDGE\tPWRN-a-2-2\tc\t1.0
    # Edges modifications:
    EDGE\tPWRN-a-1-2\tc\t1.0
    EDGE\tPWRN-a-5-2\tc\t1.0
    """
    BUBBLELINES_OPTIONS = """
    NODE\ta
    NODE\tb
    NODE\tc
    NODE\td
    NODE\te
    NODE\tf
    NODE\tg
    NODE\th
    NODE\ti
    NODE\tj
    NODE\tk
    NODE\tl
    NODE\tm
    SET\tPWRN-a-2-1\t1.0
    SET\tPWRN-a-2-2\t1.0
    # Sets modifications:
    SET\tPWRN-a-1-2\t1.0
    SET\tPWRN-a-4-2\t1.0
    IN\ta\tPWRN-a-2-1
    IN\tb\tPWRN-a-2-1
    IN\tc\tPWRN-a-2-1
    IN\td\tPWRN-a-2-2
    IN\te\tPWRN-a-2-2
    IN\tf\tPWRN-a-2-2
    # Inclusions modifications:
    IN\tg\tPWRN-a-1-2
    IN\th\tPWRN-a-1-2
    IN\ti\tPWRN-a-1-2
    IN\tj\tPWRN-a-4-2
    IN\tk\tPWRN-a-4-2
    EDGE\tPWRN-a-2-1\tPWRN-a-2-2\t1.0
    EDGE\tc\tl\t1.0
    EDGE\tc\tm\t1.0
    # Edges modifications:
    EDGE\tPWRN-a-1-2\tc\t1.0
    EDGE\tPWRN-a-4-2\tc\t1.0
    """
