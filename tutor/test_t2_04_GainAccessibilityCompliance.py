"""Tutor v2, Epic 4 - Gain Accessibility Compliance."""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
# from random import randint
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as expect
# from staxing.assignment import Assignment

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Teacher

# for template command line testing only
# - replace list_of_cases on line 31 with all test case IDs in this file
# - replace CaseID on line 52 with the actual case ID
# - delete lines 17 - 22
list_of_cases = None
CaseID = 'skip'

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': '50.0',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([list_of_cases])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestGainAccessibilityCompliance(unittest.TestCase):
    """T2.04 - Gain Accessibility Compliance."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.teacher = Teacher(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )

    def tearDown(self):
        """Test destructor."""
        self.ps.update_job(
            job_id=str(self.teacher.driver.session_id),
            **self.ps.test_updates
        )
        try:
            self.teacher.delete()
        except:
            pass

    # Case CaseID - Story# - UserType | StoryText
    @pytest.mark.skipif(str(CaseID) not in TESTS, reason='Excluded')
    def test_usertype_storytext_CaseID(self):
        """Story Text.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 'product.epic.story' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'product',
            'product.epic',
            'product.epic.story',
            'CaseID'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
