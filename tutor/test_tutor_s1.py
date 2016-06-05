"""Jenkins-CI test file."""

import json
import os
import pytest


basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': '48.0',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    ['7788', '7789', '7790']
)


# Case C7788 - S1 Case 1
@pytest.mark.skipif(str(7788) not in TESTS, reason='Excluded')
def test_case_1_7788():
    """Parameter False test."""
    assert 1 != 4


# Case C7789 - S1 Case 2
@pytest.mark.skipif(str(7789) not in TESTS, reason='Excluded')
def test_case_2_7789():
    """Parameter False test."""
    assert 2 != 4


# Case C7790 - S1 Case 3
@pytest.mark.skipif(str(7790) not in TESTS, reason='Excluded')
def test_case_3_7790():
    """Parameter False test."""
    assert 4 == 4
