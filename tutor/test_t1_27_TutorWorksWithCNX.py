"""Tutor v1, Epic 27 - Tutor works with CNX."""

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
# - replace CaseID on line 52 with the actual cass ID
# - delete lines 17 - 22
list_of_cases = None
CaseID = 'skip'

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': 'latest',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([
        8182, 8183
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestTutorWorksWithCNX(unittest.TestCase):
    """T1.27 - Tutor works with CNX."""

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

    # Case C8182 - 001 - System | CNX needs to handle LaTeX in Exercises
    @pytest.mark.skipif(str(8182) not in TESTS, reason='Excluded')
    def test_system_cnx_needs_to_handle_latex_in_exercises_8182(self):
        """CNX needs to handle LaTeX in Exercises.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't1.27.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.27',
            't1.27.001',
            '8182'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C8183 - 002 - System | CNX pulls exercises from Tutor
    @pytest.mark.skipif(str(8183) not in TESTS, reason='Excluded')
    def test_system_cnx_pulls_exercises_from_tutor_8183(self):
        """Story Text.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't1.27.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.27',
            't1.27.002',
            '8183'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
