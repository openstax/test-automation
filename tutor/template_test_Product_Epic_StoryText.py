"""Product, Epic ## - Epic Text."""

import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
from random import randint  # NOQA
from selenium.webdriver.common.by import By  # NOQA
from selenium.webdriver.support import expected_conditions as expect  # NOQA
from staxing.assignment import Assignment  # NOQA

# user types: Admin, ContentQA, Teacher, Student
from staxing.helper import Teacher  # NOQA

# for template command line testing only
# - replace list_of_cases on line 31 with all test case IDs in this file
# - replace CaseID on line 52 with the actual cass ID
# - delete lines 17 - 22
list_of_cases = 0
CaseID = 0

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': '48.0',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([list_of_cases])  # NOQA
)


@PastaDecorator.on_platforms(BROWSERS)
class TestEpicName(unittest.TestCase):
    """T1.13 - View the calendar."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()

    def tearDown(self):
        """Test destructor."""
        try:
            pass
        except:
            pass

    # Case CaseID - Story# - UserType
    @pytest.mark.skipif(str(CaseID) not in TESTS, reason='Excluded')  # NOQA
    def test_story_text(self):
        """Story Text.

        Steps:


        Expected Result:

        """
        pass
