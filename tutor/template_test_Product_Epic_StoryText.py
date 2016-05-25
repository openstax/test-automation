"""Tutor v1, Epic 08 - StudentsWorkAssignments."""

import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
# from random import randint
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as expect
# from staxing.assignment import Assignment
# from staxing.helper import Teacher, Student
from staxing.helper import Teacher

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': '48.0',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([7978])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestViewTheCalendarDashboard(unittest.TestCase):
    """T1.13 - View the calendar."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.teacher = Teacher(use_env_vars=True)

    def tearDown(self):
        """Test destructor."""
        try:
            self.teacher.delete()
        except:
            pass

    # Case C7978 - 001 - Teacher | View the calendar dashboard
    @pytest.mark.skipif(str(7978) not in TESTS, reason='Excluded')
    def test_select_an_exercise_answer(self):
        """View the calendar dashboard.

        Steps:
        Go to https://tutor-XXXX.openstax.org/
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a Tutor course name

        Expected Result:
        The teacher is presented their calendar dashboard.
        """
        pass
