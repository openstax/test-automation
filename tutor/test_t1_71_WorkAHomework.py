"""Tutor v1, Epic 71 - Work a homework."""

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
from staxing.helper import Student  # NOQA

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': '50.0',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([8362, 8363, 8364, 8365, 8366,
         8367, 8368, 8369, 8370, 8371,
         8372, 8373, 8374, 8375, 8376, 
         8377, 8378, 8379, 8380, 8381,
         8382, 8383, 8384, 8385, 8386])  # NOQA
)


@PastaDecorator.on_platforms(BROWSERS)
class TestEpicName(unittest.TestCase):
    """T1.71 - Work a Homework."""

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

    # Case C8362 - 001 - Student | Start an open homework assignment 
    @pytest.mark.skipif(str(8362) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Start an open homework assignment.

        Steps:

        Click on a homework assignment on the list dashboard


        Expected Result:

        The user is presented with the first question of the homework assignment

        """
        self.ps.test_updates['name'] = 't1.71.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.71',
            't1.71.001',
            '8362'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8363 - 002 - Student | Hover over the information icon in the footer to view the assignment description
    @pytest.mark.skipif(str(8363) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Hover over the information icon in the footer to view the assignment description.

        Steps:

        Click on a homework assignment on the list dashboard
        Hover the cursor over the information icon in right corner of the footer


        Expected Result:

        The user is presented with the assignment description/instructions

        """
        self.ps.test_updates['name'] = 't1.71.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.71',
            't1.71.002',
            '8363'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8364 - 003 - Student | Navigate between questions using the breadcrumbs
    @pytest.mark.skipif(str(8364) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Navigate between questions using the breadcrumbs.

        Steps:

        Click on a homework assignment on the list dashboard
        Click on the next breadcrumb


        Expected Result:

        The user is presented with the next question

        """
        self.ps.test_updates['name'] = 't1.71.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.71',
            't1.71.003',
            '8364'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8365 - 004 - Student | Inputting a free response into a free response textblock activates the Answer button
    @pytest.mark.skipif(str(8365) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Inputting a free response into a free response textblocl activates the Answer button.

        Steps:

        Click on a homework assignment on the list dashboard
        If the assessment has a free response text box, enter a free response into the free response text box


        Expected Result:

        The Answer button is activated

        """
        self.ps.test_updates['name'] = 't1.71.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.71',
            't1.71.004',
            '8365'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8366 - 005 - Student |  Submit a free response answer
    @pytest.mark.skipif(str(8366) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """ Submit a free response answer.

        Steps:

        Click on a homework assignment on the list dashboard
        If the assessment has a free response text box, enter a free response into the free response text box
        Click "Answer"


        Expected Result:

        A free response answer is submitted

        """
        self.ps.test_updates['name'] = 't1.71.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.71',
            't1.71.005',
            '8366'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8367 - 006 - Student | Selecting a multiple choice answer activates the Submit button
    @pytest.mark.skipif(str(8367) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Selecting a multiple choice answer activates the Submit button.

        Steps:

        Click on a homework assignment on the list dashboard
        If the assessment has a free response text box, enter a free response into the free response text box
        Click "Answer"
        Select a multiple choice answer


        Expected Result:

        The Submit button is activated

        """
        self.ps.test_updates['name'] = 't1.71.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.71',
            't1.71.006',
            '8367'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8368 - 007 - Student | Submit a multiple choice answer
    @pytest.mark.skipif(str(8368) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Submit a multiple choice answer.

        Steps:

        Click on a homework assignment on the list dashboard
        If the assessment has a free response text box, enter a free response into the free response text box
        Click "Answer"
        Select a multiple choice answer
        Click "Submit"


        Expected Result:

        A multiple choice answer is submitted

        """
        self.ps.test_updates['name'] = 't1.71.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.71',
            't1.71.007',
            '8368'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8369 - 008 - Student | Verify the free response saved after entering it into the assessment 
    @pytest.mark.skipif(str(8369) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Verify the free response saved after entering it into the assessment.

        Steps:

        Click on a homework assignment on the list dashboard
        If the assessment has a free response text box, enter a free response into the free response text box
        Click on the next breadcrumb to get to the next assessment
        Click back to the original assessment


        Expected Result:

        The free response on the original assessment is saved

        """
        self.ps.test_updates['name'] = 't1.71.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.71',
            't1.71.008',
            '8369'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8370 - 009 - Student | Verify the mutliple choice answer saved
    @pytest.mark.skipif(str(8370) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Verify the multiple choice answer saved.

        Steps:

        Click on a homework assignment on the list dashboard
        Select a multiple choice answer
        Click on the next breadcrumb to get to the next assessment
        Click back to the original assessment


        Expected Result:

        The multiple choice answer on the original assessment is saved

        """
        self.ps.test_updates['name'] = 't1.71.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.71',
            't1.71.009',
            '8370'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8371 - 010 - Student | Verify the assignment progress changed
    @pytest.mark.skipif(str(8371) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Verify the multiple choice answer saved.

        Steps:

        Click on a homework assignment on the list dashboard
        If the assessment has a free response text box, enter a free response into the free response text box
        Click "Answer"
        If the assessment has multiple choices, select a multiple choice answer
        Click "Submit"

        Click on the course name in the left corner of the header 
        OR
        Click on the user menu
        Click "Dashboard"

        Expected Result:

        The user returns to dashboard and the assignment progress shows the number of questions answered

        """
        self.ps.test_updates['name'] = 't1.71.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.71',
            't1.71.010',
            '8371'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8372 - 011 - Student | Answer all of the assessments in an assignment and view the completion report
    @pytest.mark.skipif(str(8372) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Answer all of the assessments in an assignment and view the completion report.

        Steps:

        Click on a homework assignment on the list dashboard
        If the assessment has a free response text box, enter a free response into the free response text box
        Click "Answer"
        If the assessment has multiple choices, select a multiple choice answer
        Click "Submit"
        Continue answering all assessments

        Expected Result:

        The user is presented with the completion report at the end of the assignment

        """
        self.ps.test_updates['name'] = 't1.71.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.71',
            't1.71.011',
            '8372'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8373 - 012 - Student | Before the due date, change a mutliple choice answer
    @pytest.mark.skipif(str(8373) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Before the due date, change a mutliple choice answer.

        Steps:

        Click on a homework assignment on the list dashboard (that does not have instant feedback)
        If the assessment has a free response text box, enter a free response into the free response text box
        Click "Answer"
        If the assessment has multiple choices, select a multiple choice answer
        Click "Submit"

        Click on the course name in the left corner of the header 
        OR
        Click on the user menu
        Click "Dashboard"
        Change a multiple choice answer on an assessment
        Click "Submit"

        Expected Result:

        A multiple choice answer is changed on an assessment

        """
        self.ps.test_updates['name'] = 't1.71.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.71',
            't1.71.012',
            '8373'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8374 - 013 - Student | View the completion report and return to the dashboard
    @pytest.mark.skipif(str(8374) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """View the completion report and return to the dashboard.

        Steps:

        Click on a homework assignment on the list dashboard
        If the assessment has a free response text box, enter a free response into the free response text box
        Click "Answer"
        If the assessment has multiple choices, select a multiple choice answer
        Click "Submit"
        Continue answering all assessments
        Click "Back To Dashboard"

        Expected Result:

        The user is returned to the dashboard

        """
        self.ps.test_updates['name'] = 't1.71.013' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.71',
            't1.71.013',
            '8374'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8375 - 014 - Student | A completed homework should show "You are done" in the completion report
    @pytest.mark.skipif(str(8375) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """A completed homework should show "You are done" in the completion report.

        Steps:

        Click on a homework assignment on the list dashboard
        If the assessment has a free response text box, enter a free response into the free response text box
        Click "Answer"
        If the assessment has multiple choices, select a multiple choice answer
        Click "Submit"
        Continue answering all assessments


        Expected Result:

        The user is presented with the completion report that shows "You are done"

        """
        self.ps.test_updates['name'] = 't1.71.014' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.71',
            't1.71.014',
            '8375'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8376 - 015 - Student | A completed homework should show X/X answered in the dashboard progress column
    @pytest.mark.skipif(str(8376) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """A completed homework should show X/X answered in the dashboard progress column.

        Steps:

        Click on a homework assignment on the list dashboard
        If the assessment has a free response text box, enter a free response into the free response text box
        Click "Answer"
        If the assessment has multiple choices, select a multiple choice answer
        Click "Submit"
        Continue answering all assessments
        Click "Back To Dashboard"


        Expected Result:

        The user is returned to the dashboard.
        The completed homework shows X/X answered in the dashboard progress column.

        """
        self.ps.test_updates['name'] = 't1.71.015' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.71',
            't1.71.015',
            '8376'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8377 - 016 - Student | A homework may have a Review assessment
    @pytest.mark.skipif(str(8377) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """ A homework may have a Review assessment.

        Steps:

        Click on a homework assignment on the list dashboard
        If the assessment has a free response text box, enter a free response into the free response text box
        Click "Answer"
        If the assessment has multiple choices, select a multiple choice answer
        Click "Submit"
        Continue answering all assessments


        Expected Result:

        A homework may have a Review assessment toward the end

        """
        self.ps.test_updates['name'] = 't1.71.016' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.71',
            't1.71.016',
            '8377'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8378 - 017 - Student | A homework may have a Personalized assessment
    @pytest.mark.skipif(str(8378) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """A homework may have a Personalized assessment.

        Steps:

        Click on a homework assignment on the list dashboard
        If the assessment has a free response text box, enter a free response into the free response text box
        Click "Answer"
        If the assessment has multiple choices, select a multiple choice answer
        Click "Submit"
        Continue answering all assessments


        Expected Result:

        A homework may have a Personalized assessment toward the end

        """
        self.ps.test_updates['name'] = 't1.71.017' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.71',
            't1.71.017',
            '8378'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8379 - 018 - Student | Start a late homework assignment
    @pytest.mark.skipif(str(8379) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """A homework may have a Personalized assessment.

        Steps:

        Click on the "All Past Work" tab on the dashboard
        Click on a homework assignment


        Expected Result:

        The user starts a late homework assignment

        """
        self.ps.test_updates['name'] = 't1.71.018' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.71',
            't1.71.018',
            '8379'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8380 - 019 - Student | Submit a multiple choice answer
    @pytest.mark.skipif(str(8380) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Submit a multiple choice answer.

        Steps:

        Click on the "All Past Work" tab on the dashboard
        Click on a homework assignment
        Enter a free response into the free response text box
        Click "Answer"
        Select a multiple choice answer 
        Click "Submit"


        Expected Result:

        A multiple choice answer is submitted

        """
        self.ps.test_updates['name'] = 't1.71.019' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.71',
            't1.71.019',
            '8380'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8381 - 020 - Student | Answer feedback is presented
    @pytest.mark.skipif(str(8381) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Answer feedback is presented.

        Steps:

        Click on the "All Past Work" tab on the dashboard
        Click on a homework assignment
        Enter a free response into the free response text box
        Click "Answer"
        Select a multiple choice answer 
        Click "Submit"


        Expected Result:

        The multiple choice answer is submitted and answer feedback is presented

        """
        self.ps.test_updates['name'] = 't1.71.020' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.71',
            't1.71.020',
            '8381'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8382 - 021 - Student | Correctness for a completed assessment is displayed in the breadcrumbs
    @pytest.mark.skipif(str(8382) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Correctness for a completed assessment is displayed in the breadcrumbs.

        Steps:

        Click on the "All Past Work" tab on the dashboard
        Click on a homework assignment
        Enter a free response into the free response text box
        Click "Answer"
        Select a multiple choice answer 
        Click "Submit"


        Expected Result:

        Correctness for a completed assessment is displayed in the breadcrumbs

        """
        self.ps.test_updates['name'] = 't1.71.021' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.71',
            't1.71.021',
            '8382'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8383 - 022 - Student | Start an open homework assignment with immediate feedback
    @pytest.mark.skipif(str(8383) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Start an open homework assignment with immediate feedback.

        Steps:

        Click on a homework assignment on the list dashboard


        Expected Result:

        The user starts an open homework assignment

        """
        self.ps.test_updates['name'] = 't1.71.022' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.71',
            't1.71.022',
            '8383'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8384 - 023 - Student | Submit a multiple choice answer
    @pytest.mark.skipif(str(8384) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Submit a multiple choice answer.

        Steps:

        Click on a homework assignment on the list dashboard
        Enter a free response into the free response text box
        Click "Answer"
        Select a multiple choice answer 
        Click "Submit"


        Expected Result:

        A multiple choice answer is submitted

        """
        self.ps.test_updates['name'] = 't1.71.023' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.71',
            't1.71.023',
            '8384'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8385 - 024 - Student | Answer feedback is presented
    @pytest.mark.skipif(str(8385) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Answer feedback is presented.

        Steps:

        Click on a homework assignment on the list dashboard
        Enter a free response into the free response text box
        Click "Answer"
        Select a multiple choice answer 
        Click "Submit"


        Expected Result:

        Answer feedback is presented

        """
        self.ps.test_updates['name'] = 't1.71.024' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.71',
            't1.71.024',
            '8385'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8386 - 025 - Student | Correctness for a completed assessment is displayed in the breadcrumbs
    @pytest.mark.skipif(str(8386) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Correctness for a completed assessment is displayed in the breadcrumbs.

        Steps:

        Click on a homework assignment on the list dashboard
        Enter a free response into the free response text box
        Click "Answer"
        Select a multiple choice answer 
        Click "Submit"


        Expected Result:

        Correctness for a completed assessment is displayed in the breadcrumbs

        """
        self.ps.test_updates['name'] = 't1.71.025' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.71',
            't1.71.025',
            '8386'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


