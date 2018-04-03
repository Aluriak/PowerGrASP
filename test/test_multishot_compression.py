"""Test of ambiguous and multishot graph compression.

Note that the test_* functions are generated
from the template_test_function function.

"""
import os
import pytest
import itertools

from powergrasp.routines import compress_by_cc
from powergrasp import constants
from .ambiguous_test_cases import cases


def template_test_function(file:str, all_bubblelines:set):
    def test_function():
        found = unified_bubble(compress_by_cc(file))
        variants_keys = itertools.permutations(all_bubblelines['values'])
        variants = {all_bubblelines['common'] + '\n'
                    + all_bubblelines['variant'].format(**dict(zip('abcde', keys)))
                    for keys in variants_keys}
        expecteds = tuple(unified_bubble(variant.splitlines(keepends=False))
                          for variant in variants)
        # The following lines are here to get a proper understanding of the data
        #  in case of error.
        for expected in expecteds:
            if found == expected:
                return
        print('FOUND:', found)
        for idx, expected in enumerate(expecteds, start=1):
            print('EXPECTED', idx, ':', expected - found)
        assert found in expecteds, "Expected not found"
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
    return frozenset(line.strip() for line in bubble_lines
                     if not line.startswith(filtered) and len(line.strip()) > 0)


for fname, bubbles in cases.items():
    func = template_test_function('data/' + fname, bubbles)
    globals()['test_' + os.path.basename(fname).replace('-', '_')] = func
