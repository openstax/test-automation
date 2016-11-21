"""Tutor v1, Epic 38 - Choose Course."""

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
from staxing.helper import Student, Teacher

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
LOCAL_RUN = os.getenv('LOCALRUN', 'false').lower() == 'true'
TESTS = os.getenv(
    'CASELIST',
    str([
        8254, 8255, 8256, 8257
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestChooseCourse(unittest.TestCase):
    """T1.38 - Choose Course."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.user = None

    def tearDown(self):
        """Test destructor."""
        if not LOCAL_RUN:
            self.ps.update_job(
                job_id=str(self.user.driver.session_id),
                **self.ps.test_updates
            )
        try:
            self.user.delete()
        except:
            pass

    # Case C8254 - 001 - Student | Select a course
    @pytest.mark.skipif(str(8254) not in TESTS, reason='Excluded')
    def test_student_select_a_course_8254(self):
        """Select a course.

        Steps:
        Click on a Tutor course name

        Expected Result:
        The user selects a course and is presented with the dashboard.
        """
        self.ps.test_updates['name'] = 't1.38.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.38',
            't1.38.001',
            '8254'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.user = Student(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        self.user.login()
        self.user.select_course(appearance='physics')

        assert('list' in self.user.current_url()), \
            'Not in a course'

        self.ps.test_updates['passed'] = True

    # Case C8255 - 002 - Student | Bypass the course picker
    @pytest.mark.skipif(str(8255) not in TESTS, reason='Excluded')
    def test_student_bypass_the_course_picker_8255(self):
        """Bypass the course picker.

        Steps:
        Go to Tutor
        Click on the 'Login' button
        Enter the student user account qas_01
        Click on the 'Sign in' button

        Expected Result:
        The user bypasses the course picker and is presented with the
        dashboard (because qas_01 is only enrolled in one course)
        """
        self.ps.test_updates['name'] = 't1.38.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.38',
            't1.38.002',
            '8255'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.user = Student(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        self.user.login(username="qas_01")
        assert('list' in self.user.current_url()), \
            'Not in a course'

        self.ps.test_updates['passed'] = True

    # Case C8256 - 003 - Teacher | Select a course
    @pytest.mark.skipif(str(8256) not in TESTS, reason='Excluded')
    def test_teacher_select_a_course_8256(self):
        """Select a course.

        Steps:
        Click on a Tutor course name

        Expected Result:
        The user selects a course and is presented with the calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.38.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.38',
            't1.38.003',
            '8256'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.user = Teacher(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        self.user.login()
        self.user.select_course(appearance='physics')
        assert('calendar' in self.user.current_url()), \
            'Not in a course'

        self.ps.test_updates['passed'] = True

    # Case C8257 - 004 - Teacher | Bypass the course picker
    @pytest.mark.skipif(str(8257) not in TESTS, reason='Excluded')
    def test_teacher_bypass_the_course_picker_8257(self):
        """Bypass the course picker.

        Steps:
        Go to Tutor
        Click on the 'Login' button
        Enter the teacher user account [ qateacher | password ] in the
            username and password text boxes
        Click on the 'Sign in' button

        Expected Result:
        The user bypasses the course picker and is presented with the
        calendar dashboard (because qateacher only has one course)
        """
        self.ps.test_updates['name'] = 't1.38.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.38',
            't1.38.004',
            '8257'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.user = Teacher(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        self.user.login(username="qateacher")
        assert('calendar' in self.user.current_url()), \
            'Not in a course'

        self.ps.test_updates['passed'] = True
