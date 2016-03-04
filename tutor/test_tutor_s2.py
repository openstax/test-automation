"""Jenkins-CI test file."""

import os
import pytest

TESTS = os.environ['CASELIST']


# Case C7791 - S2 Case 1
@pytest.mark.skipif(str(7791) not in TESTS, reason='Excluded')
def test_case_1():
    """Parameter False test."""
    assert 1 != 4


# Case C7792 - S2 Case 2
@pytest.mark.skipif(str(7792) not in TESTS, reason='Excluded')
def test_case_2():
    """Parameter False test."""
    assert 2 <= 4


# Case C7793 - S2 Case 3
@pytest.mark.skipif(str(7793) not in TESTS, reason='Excluded')
def test_case_3():
    """Parameter False test."""
    assert 3 < 4


# Case C7794 - S2 Case 4
@pytest.mark.skipif(str(7794) not in TESTS, reason='Excluded')
def test_case_4():
    """Parameter False test."""
    assert 4 == 4


# Case C7795 - S2 Case 5
@pytest.mark.skipif(str(7795) not in TESTS, reason='Excluded')
def test_case_5():
    """Parameter False test."""
    assert 5 > 4
