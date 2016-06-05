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
    ['7796', '7797']
)


# Case C7796 - S3 Case 1
@pytest.mark.skipif(str(7796) not in TESTS, reason='Excluded')
def test_case_1_7796():
    """Parameter False test."""
    assert '1' != '4'


# Case C7797 - S3 Case 2
@pytest.mark.skipif(str(7797) not in TESTS, reason='Excluded')
def test_case_2_7797():
    """Parameter False test."""
    assert 2.0 == 4.0
