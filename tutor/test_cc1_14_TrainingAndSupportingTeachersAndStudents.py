"""
Concept Coach v1, Epic 14.

Training and Supporting Teachers and Students.
"""

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
    str([7704, 7705, 7706, 7707, 7708,
         7709, 7710, 7711, 7712, 7713,
         7714])  # NOQA
)


@PastaDecorator.on_platforms(BROWSERS)
class TestTrainingAndSupportingTeachersAndStudents(unittest.TestCase):
    """CC1.14 - Training and Supporting Teachers and Students."""

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

    # Case C7704 - 001 - System | Concept Coach Zendesk is web-accessible
    @pytest.mark.skipif(str(7704) not in TESTS, reason='Excluded')  # NOQA
    def test_system_concept_coach_zendesk_is_web_accessible_7704(self):
        """Concept Coach Zendesk is web-accesible.

        Steps:

        Log in to tutor as teacher
        If more then one course, click on a concept coach course
        In user menu in top right of header, click 'Get Help'


        Expected Result:

        In a new window or tab, zendesk help is opened

        """
        self.ps.test_updates['name'] = 'cc1.14.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.14',
            'cc1.14.001',
            '7704'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # Case C7705 - 002 - Teacher | Can access user support
    @pytest.mark.skipif(str(7705) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_can_access_user_support_7705(self):
        """Can access user support.

        Steps:

        click on the user menu
        Click on the Get Help option


        Expected Result:

        in a new tab or window zendesk is opened

        """
        self.ps.test_updates['name'] = 'cc1.14.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.14',
            'cc1.14.002',
            '7705'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # Case C7706 - 003 - Student | Can access user support
    @pytest.mark.skipif(str(7706) not in TESTS, reason='Excluded')  # NOQA
    def test_student_can_access_user_support_7706(self):
        """Can access user support.

        Steps:

        click on the user menu
        Click on the Get Help option


        Expected Result:

        in a new tab or window zendesk is opened

        """
        self.ps.test_updates['name'] = 'cc1.14.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.14',
            'cc1.14.003',
            '7706'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # Case C7707 - 004 - Non-user | Submit support questions
    @pytest.mark.skipif(str(7707) not in TESTS, reason='Excluded')  # NOQA
    def test_nonuser_submit_support_questions_7707(self):
        """Submit support questions.

        Steps:

        go to http://cc.openstax.org
        click on the help button in the bottom right
        enter keywords to question into text box
        press return key
        click on 'Leave us a message'
        enter name, email and message into corresponding text boxes
        click 'Send'


        Expected Result:

        'Message sent' displayed in help box

        """
        self.ps.test_updates['name'] = 'cc1.14.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.14',
            'cc1.14.004',
            '7707'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # Case C7708 - 005 - Teacher | Submit support questions
    @pytest.mark.skipif(str(7708) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_submit_support_questions_7708(self):
        """Submit support questions.

        Steps:

        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If user has more than one course, click on a Concept Coach course

        Click the user menu in the right corner of the header
        Click "Get Help"
        Click "Submit a request"
        Fill out all the necessary text fields
        Click "Submit"


        Expected Result:

        The user submits support questions

        """
        self.ps.test_updates['name'] = 'cc1.14.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.14',
            'cc1.14.005',
            '7708'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # Case C7709 - 006 - Student | Submit support questions
    @pytest.mark.skipif(str(7709) not in TESTS, reason='Excluded')  # NOQA
    def test_student_submit_support_questions_7709(self):
        """Submit support questions.

        Steps:

        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the student user account in the username and password text boxes
        Click on the 'Sign in' button

        Click the user menu in the right corner of the header
        Click "Get Help"
        Click "Submit a request"
        Fill out all the necessary text fields
        Click "Submit"


        Expected Result:

        The user submits support questions

        """
        self.ps.test_updates['name'] = 'cc1.14.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.14',
            'cc1.14.006',
            '7709'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # Case C7710 - 007 - Teacher | View instructions on how to use CC
    @pytest.mark.skipif(str(7710) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_view_instructions_on_how_to_use_cc_7710(self):
        """View instructions on how to use Concept Coach.

        Steps:

        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If user has more than one course, click on a Concept Coach course

        Click the user menu in the right corner of the header
        Click "Get Help"
        Click "Getting Started Guide"
        Click on the pdf link

        OR

        Click "Getting Started" from the user menu



        Expected Result:

        The user is presented with a guide to use CC


        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # Case C7711 - 008 - Student | View instructions on how to use CC
    @pytest.mark.skipif(str(7711) not in TESTS, reason='Excluded')  # NOQA
    def test_student_view_instructions_on_how_to_use_cc_7711(self):
        """View instructions on how to use Concept Coach.

        Steps:

        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the student user account in the username and password text boxes
        Click on the 'Sign in' button

        Click the user menu in the right corner of the header
        Click "Get Help"
        Scroll down to the questions under "Students"


        Expected Result:

        The user is presented with instructions on how to use CC

        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # Case C7712 - 009 - Teacher | View instructions on how to use CC
    @pytest.mark.skipif(str(7712) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_view_instructions_on_how_to_use_cc_7712(self):
        """View instructions on how to use Concept Coach.

        Steps:

        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If user has more than one course, click on a Concept Coach course

        Click the user menu in the right corner of the header
        Click "Get Help"


        Expected Result:

        taken to zendesk in a new window or tab. assorted help is given

        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # Case C7713 - 010 - Student | Get help during account registration
    @pytest.mark.skipif(str(7713) not in TESTS, reason='Excluded')  # NOQA
    def test_student_get_help_during_account_registration_7713(self):
        """View instructions on how to use Concept Coach.

        Steps:


        Expected Result:



        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # Case C7714 - 011 - Teacher | View instructions for Legacy users
    # transitioning to Concept Coach
    @pytest.mark.skipif(str(7714) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_view_instructions_for_legacy_users_transition_7714(self):
        """View instructions for Legacy users transitioning to Concept Coach.

        Steps:


        Expected Result:


        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)
