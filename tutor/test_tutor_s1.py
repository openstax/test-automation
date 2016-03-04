"""Jenkins-CI test file."""

import os
import pytest

TESTS = os.environ['CASELIST']


# Case C7788 - S1 Case 1
@pytest.mark.skipif(str(7788) not in TESTS, reason='Excluded')
def test_case_1():
    """Parameter False test."""
    assert 1 != 4


# Case C7789 - S1 Case 2
@pytest.mark.skipif(str(7789) not in TESTS, reason='Excluded')
def test_case_2():
    """Parameter False test."""
    assert 2 != 4


# Case C7790 - S1 Case 3
@pytest.mark.skipif(str(7790) not in TESTS, reason='Excluded')
def test_case_3():
    """Parameter False test."""
    assert 4 == 4
