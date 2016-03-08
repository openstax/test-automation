"""Jenkins-CI test file."""

import os
import pytest

TESTS = os.environ['CASELIST']


# Case C7796 - S3 Case 1
@pytest.mark.skipif(str(7796) not in TESTS, reason='Excluded')
def test_case_1():
    """Parameter False test."""
    assert '1' != '4'


# Case C7797 - S3 Case 2
@pytest.mark.skipif(str(7797) not in TESTS, reason='Excluded')
def test_case_2():
    """Parameter False test."""
    assert 2.0 == 4.0
