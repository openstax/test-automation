"""Tutor v1, Epic 38 - Choose Course."""

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
from staxing.helper import Teacher  # NOQA
from staxing.helper import Student  # NOQA
from staxing.helper import User  # NOQA

# for template command line testing only
# - replace list_of_cases on line 31 with all test case IDs in this file
# - replace CaseID on line 52 with the actual cass ID
# - delete lines 17 - 22
list_of_cases = 0
CaseID = 0

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': '50.0',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([8254, 8255, 8256, 8257])  # NOQA
)


@PastaDecorator.on_platforms(BROWSERS)
class TestEpicName(unittest.TestCase):
    """T1.38 - Choose Course."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        # self.Teacher = Teacher(
        #    use_env_vars=True,
        #    pasta_user=self.ps,
        #    capabilities=self.desired_capabilities
        # )
        # = Teacher(use_env_vars=True)
        # self.user.login()
        # self.student = Student(use_env_vars=True)
        # self.student.login()

    def tearDown(self):
        """Test destructor."""
        self.ps.update_job(job_id=str(self.user.driver.session_id),
                           **self.ps.test_updates)

        try:
            self.user.delete()
        except:
            pass

    # Case C8254 - 001 - Student | Select a course
    @pytest.mark.skipif(str(8254) not in TESTS, reason='Excluded')  # NOQA
    def test_student_select_a_course(self):
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
        self.user = User(username='student01', password='password',
                         site='https://tutor-qa.openstax.org/')
        self.user.login()
        self.user.find(By.PARTIAL_LINK_TEXT, 'AP Physics').click()

        assert('courses/1/list/' in self.user.current_url()), \
            'Not in a course'

        self.user.sleep(5)

        self.ps.test_updates['passed'] = True

    # Case C8255 - 002 - Student | Bypass the course picker
    @pytest.mark.skipif(str(8255) not in TESTS, reason='Excluded')  # NOQA
    def test_student_bypass_the_course_picker(self):
        """Bypass the course picker.

        Steps:
        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the student user account [ qas_01 | password ] in the username
        and password text boxes
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

        self.user = User(username='qas_04', password='password',
                         site='https://tutor-qa.openstax.org/')
        self.user.login()
        assert('courses/75/list/' in self.user.current_url()), \
            'Not in a course'

        self.user.sleep(5)
        self.ps.test_updates['passed'] = True

    # Case C8256 - 003 - Teacher | Select a course
    @pytest.mark.skipif(str(8256) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_select_a_course(self):
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
        self.user = User(username='teacher01', password='password',
                         site='https://tutor-qa.openstax.org/')
        self.user.login()
        self.user.find(By.PARTIAL_LINK_TEXT, 'AP Physics').click()
        assert('calendar' in self.user.current_url()), \
            'Not in a course'
        self.user.sleep(5)

        self.ps.test_updates['passed'] = True

    # Case C8257 - 004 - Teacher | Bypass the course picker
    @pytest.mark.skipif(str(8257) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_bypass_the_course_picker(self):
        """Bypass the course picker.

        Steps:
        Go to https://tutor-qa.openstax.org/
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
        self.user = User(username='qateacher', password='password',
                         site='https://tutor-qa.openstax.org/')
        self.user.login()
        assert('calendar' in self.user.current_url()), \
            'Not in a course'

        self.user.sleep(5)

        self.ps.test_updates['passed'] = True
