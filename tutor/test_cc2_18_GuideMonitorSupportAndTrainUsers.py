"""Concept Coach v2, Epic 18 - Guide, Monitor, Support, and Train Users."""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
from random import randint  # NOQA
from selenium.webdriver.common.by import By  # NOQA
from selenium.webdriver.support import expected_conditions as expect  # NOQA
from staxing.assignment import Assignment  # NOQA

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Teacher, Student  # NOQA

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': '50.0',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([14823, 14824, 14825])  # NOQA
)


@PastaDecorator.on_platforms(BROWSERS)
class TestGuideMonitorSupportAndTrainUsers(unittest.TestCase):
    """CC2.18 - Guide, Monitor, Support, and Train Users."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.Teacher = Teacher(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )

    def tearDown(self):
        """Test destructor."""
        self.ps.update_job(job_id=str(self.teacher.driver.session_id),
                           **self.ps.test_updates)
        try:
            self.teacher.delete()
        except:
            pass

    # 14823 - 001 - Teacher | Guided tutorial of Concept Coach
    @pytest.mark.skipif(str(14823) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_guided_tutorial_of_concept_coach_14823(self):
        """Guided tutorial of Concept Coach.

        Steps:



        Expected Result:


        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # 14824 - 002 - Student | Guided tutorial of Concept Coach
    @pytest.mark.skipif(str(14824) not in TESTS, reason='Excluded')  # NOQA
    def test_student_guided_tutorial_of_concept_coach_14824(self):
        """Guided tutorial of Concept Coach.

        Steps:



        Expected Result:


        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # 14825 - 003 - Teacher | CC assignments have links that can be added to
    # teacher's LMS
    @pytest.mark.skipif(str(14825) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_cc_assignments_have_links_that_can_be_added_14825(self):
        """CC assignments have links that can be added to teacher's LMS.

        Steps:

        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a CC course name

        Click "Assignment Links"


        Expected Result:

        The user is presented with links to CC assignments


        """
        self.ps.test_updates['name'] = 'cc2.18.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc2',
            'cc2.18',
            'cc2.18.003',
            '14825'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True
