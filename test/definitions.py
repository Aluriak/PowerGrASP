"""Various definitions needed by testing routines.

"""

import os
from powergrasp import constants


def unified_bubble(bubble_lines):
    """Return the set of comparable lines found in given bubble lines"""
    filtered = ['#']
    if not constants.BUBBLE_WITH_NODES:
        filtered.append('NODE')
    if not constants.BUBBLE_WITH_SETS:
        filtered.append('SET')
    filtered = tuple(filtered)

    # filter out comments and blank lines
    return set(line.strip() for line in bubble_lines
               if not line.startswith(filtered) and len(line.strip()) > 0)


def gen_test_functions(cases:dict, template_test_function:callable):
    for fname, bubble in cases.items():
        func = template_test_function('data/' + fname, bubble)
        yield 'test_' + os.path.basename(fname).replace('-', '_'), func
