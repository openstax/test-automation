"""Tutor v2, Epic 12 - Create New Question and Assignment Types."""

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
    str([14739, 14741, 14742, 14743, 14744])  # NOQA
)


@PastaDecorator.on_platforms(BROWSERS)
class TestCreateNewQuestionAndAssignmentTypes(unittest.TestCase):
    """T2.11 - Create New Question and Assignment Types."""

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

    # 14739 - 001 - Teacher | Vocabulary question is a question type
    @pytest.mark.skipif(str(14739) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_vocabulary_question_is_a_question_type_14739(self):
        """Vocabulary question is a question type.

        Steps:

        Go to https://exercises-qa.openstax.org/
        Click on the 'Login' button
        Enter the teacher account in the username and password text boxes
        Click on the 'Sign in' button

        Click "Write a new exercise"
        Click "New Vocabulary Term"


        Expected Result:

        The user is presented with a page where a new vocabulary question can
        be created


        """
        self.ps.test_updates['name'] = 't2.12.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.12',
            't2.12.001',
            '14739'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14741 - 002 - Teacher | True/False is a question type
    @pytest.mark.skipif(str(14741) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_truefalse_is_a_question_type_14741(self):
        """True/False is a question type.

        Steps:

        Click "Write a new exercise"
        Click on the "True/False" radio button


        Expected Result:

        The user is presented with a page where a True/False question can be
        created


        """
        self.ps.test_updates['name'] = 't2.12.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.12',
            't2.12.002',
            '14741'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14742 - 003 - System | Display embedded videos with attribution and link
    # back to author
    @pytest.mark.skipif(str(14742) not in TESTS, reason='Excluded')  # NOQA
    def test_system_display_embedded_videos_with_attribution_14742(self):
        """Display embedded videos with attribution and a link back to author.

        Steps:

        Go to tutor-qa
        Click Login
        Sign in as student01

        Click "HS AP Physics LG"
        Click on a homework assignment
        Click through it until you get to a video
        Click on the info icon on the video


        Expected Result:

        Attribution and links are displayed

        """
        self.ps.test_updates['name'] = 't2.12.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.12',
            't2.12.003',
            '14742'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14743 - 004 - Teacher | Each part of a multi-part question counts as a
    # seperate problem when scored
    @pytest.mark.skipif(str(14743) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_each_part_of_a_multipart_question_counts_as_14743(self):
        """Each part of a multi-part question counts as a seperate problem when scored.

        Steps:

        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Log in as teacher03
        Click "College Introduction to Sociology"

        Go to "Student Scores"
        Pick a homework that has multipart question
        Click "Review"


        Expected Result:

        There is a breadcrumb for each part of a multipart question

        """
        self.ps.test_updates['name'] = 't2.12.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.12',
            't2.12.004',
            '14743'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14744 - 005 - Student | Each part of a multi-part question counts as a
    # seperate problem when scored
    @pytest.mark.skipif(str(14744) not in TESTS, reason='Excluded')  # NOQA
    def test_student_each_part_of_a_multipart_question_counts_as_14744(self):
        """Each part of a multi-part question counts as a seperate problem when scored.

        Steps:

        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Log in as abarnes
        Click "College Introduction to Sociology"

        Click on a homework assignment
        Go through the questions


        Expected Result:

        There is a breadcrumb for each part in the multipart question and the
        progress/score is out of the total number of questions, rather than
        counting the multipart question as one question

        """
        self.ps.test_updates['name'] = 't2.12.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.12',
            't2.12.005',
            '14744'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True
