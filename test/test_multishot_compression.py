"""Test of ambiguous and multishot graph compression.

Note that the test_* functions are generated
from the template_test_function function.

"""
import os
import itertools

from powergrasp.routines import compress_by_cc
from .ambiguous_test_cases import cases
from .definitions import unified_bubble, gen_test_functions


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


for name, func in gen_test_functions(cases, template_test_function):
    globals()[name] = func
