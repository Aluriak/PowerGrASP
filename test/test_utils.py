
from powergrasp.utils import quoted

def test_quoted():
    """Hard to test in docstring because of all the backslashs"""
    assert quoted('"a') == r'"\"a"'
    assert quoted('a"b') == r'"a\"b"'
    assert len(quoted('a"b')) == 6
    assert quoted(r'"\"a"') == r'"\"\"a\""'
    assert quoted(r'"\"a\""') == r'"\"\"a\"\""'
    assert len(quoted('"a')) == 5
    assert '{}'.format(quoted('"a')) == r'"\"a"'
    assert len('{}'.format(quoted('"a'))) == 5
    assert quoted(r'"\"a"') == r'"\"\"a\""'
