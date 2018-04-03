"""Test of graph compression.

Note that the test_* functions are generated
from the template_test_function function.

"""
import os
import pytest

from powergrasp.routines import compress_by_cc
from powergrasp import constants
from .test_cases import cases


def template_test_function(file:str, bubblelines:str):
    def test_function():
        found = unified_bubble(compress_by_cc(file))
        expected = unified_bubble(bubblelines.splitlines(keepends=False))
        assert found == expected
    return test_function


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


for fname, bubble in cases.items():
    func = template_test_function('data/' + fname, bubble)
    globals()['test_' + os.path.basename(fname).replace('-', '_')] = func
