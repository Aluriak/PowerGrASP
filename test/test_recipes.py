"""Test of recipe'd graph compression.

Note that the test_* functions are generated
from the template_test_function function.

"""

from powergrasp.constants import USE_STAR_MOTIF
from powergrasp.routines import compress_by_cc
from .definitions import unified_bubble, gen_test_functions


def test_recipe():
    found = unified_bubble(compress_by_cc('data/recipe-test.lp', recipe_file='data/recipe-test.txt'))
    expected = unified_bubble(BUBBLELINES.splitlines(keepends=False))
    # with open('out/out.bbl', 'w') as fd:
        # fd.write('\n'.join(found))
    assert found == expected


if USE_STAR_MOTIF:
    BUBBLELINES = """
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
else:
    # in such case, the stars are handled as bicliques, and in this case,
    #  node c being smaller than its neighbor, it is placed in set 1 instead of 2.
    BUBBLELINES = """
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
