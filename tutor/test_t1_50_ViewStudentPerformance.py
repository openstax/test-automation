"""Tutor v1, Epic 50 - View student performance."""

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
    str([8287, 8288, 8289, 8290, 8291, 
        8292, 8293, 8294, 8295, 8296])  # NOQA
)


@PastaDecorator.on_platforms(BROWSERS)
class TestEpicName(unittest.TestCase):
    """T1.50 - View Student Performance."""

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

    # Case C8287 - 001 - Student | View the personal Performance Forecast
    @pytest.mark.skipif(str(8287) not in TESTS, reason='Excluded')  # NOQA
    def test_student_view_personal_performance_forecast(self):
        """View the personal Performance Forecast

        Steps:
        Click on the user menu in the upper right corner 
        Click on "Performance Forecast"

        Expected Result:
        The user is presented with personal Performance Forecast
        """
        self.ps.test_updates['name'] = 't1.50.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.50',
            't1.50.001',
            '8287'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8288 - 002 - Student | Info icon shows an explanation of the data
    @pytest.mark.skipif(str(8288) not in TESTS, reason='Excluded')  # NOQA
    def test_student_info_icon_shows_explanation_of_the_data(self):
        """Info icon shows an explanation of the data

        Steps:
        Click on the user menu in the upper right corner of the page
        Click on "Performance Forecast"
        Hover the cursor over the info icon that is next to the "Performance Forecast" header

        Expected Result:
        Info icon shows an explanation of the data
        """
        self.ps.test_updates['name'] = 't1.50.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.50',
            't1.50.002',
            '8288'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8289 - 003 - Student | View the performance color key
    @pytest.mark.skipif(str(8289) not in TESTS, reason='Excluded')  # NOQA
    def test_student_view_the_performance_color_key(self):
        """View the performance color key

        Steps:
        Click on the user menu in the upper right corner of the page
        Click on "Performance Forecast"

        Expected Result:
        The performance color key is presented to the user (next to the 'Return to Dashboard' button)
        """
        self.ps.test_updates['name'] = 't1.50.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.50',
            't1.50.003',
            '8289'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8290 - 004 - Student | Return To Dashboard button returns to the list dashboard
    @pytest.mark.skipif(str(8290) not in TESTS, reason='Excluded')  # NOQA
    def test_student_return_to_dashboard_button(self):
        """Return To Dashboard button returns to the list dashboard

        Steps:
        Click on the user menu in the upper right corner 
        Click on "Performance Forecast"
        Click on "Return To Dashboard"

        Expected Result:
        The user is presented with the list dashboard
        """
        self.ps.test_updates['name'] = 't1.50.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.50',
            't1.50.004',
            '8290'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8291 - 005 - Student | A student with zero answers does not show section breakdowns
    @pytest.mark.skipif(str(8291) not in TESTS, reason='Excluded')  # NOQA
    def test_student_no_answers_does_not_show_breakdown(self):
        """A student with zero answers does not show section breakdowns

        Steps:
        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the student user account [ student532 | password ] in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a Tutor course name
        Click on the user menu in the upper right corner 
        Click on "Performance Forecast"

        Expected Result:
        The user is presented with blank performance forecast with no section breakdowns and the words "You have not worked any questions yet"
        """
        self.ps.test_updates['name'] = 't1.50.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.50',
            't1.50.005',
            '8291'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8292 - 006 - Student | My Weaker Areas shows up to four problematic sections
    @pytest.mark.skipif(str(8292) not in TESTS, reason='Excluded')  # NOQA
    def test_student_weaker_areas_shows_up_to_four_sections(self):
        """My Weaker Areas shows up to four problematic sections

        Steps:
        Click on the user menu in the upper right corner 
        Click on "Performance Forecast"

        Expected Result:
        The user is presented with up to four problematic sections under My Weaker Areas
        """
        self.ps.test_updates['name'] = 't1.50.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.50',
            't1.50.006',
            '8292'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8293 - 007 - Student | Chapters are listed on the left with their sections to the right
    @pytest.mark.skipif(str(8293) not in TESTS, reason='Excluded')  # NOQA
    def test_student_chapters_listed_on_left_with_sections_on_right(self):
        """Chapters are listed on the left with their sections to the right

        Steps:
        Click on the user menu in the upper right corner 
        Click on "Performance Forecast"
        Scroll to Individual Chapters section

        Expected Result:
        The user is presented with chapters listed on the left and their sections on the right
        """
        self.ps.test_updates['name'] = 't1.50.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.50',
            't1.50.007',
            '8293'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8294 - 008 - Student | Clicking on a chapter bar brings up to five practice assessments for that chapter
    @pytest.mark.skipif(str(8294) not in TESTS, reason='Excluded')  # NOQA
    def test_student_clicking_chapter_brings_up_to_five_assessments(self):
        """Clicking on a chapter bar brings up to five practice assessments for that chapter

        Steps:
        Click on the user menu in the upper right corner 
        Click on "Performance Forecast"
        Scroll to the Individual Chapters section
        Click on a chapter bar

        Expected Result:
        The user is presented with up to five practice assessments for that chapter
        """
        self.ps.test_updates['name'] = 't1.50.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.50',
            't1.50.008',
            '8294'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8295 - 009 - Student | Clicking on a section bar brings up to five practice assessments for that section
    @pytest.mark.skipif(str(8295) not in TESTS, reason='Excluded')  # NOQA
    def test_student_clicking_section_brings_up_to_five_assessments(self):
        """Clicking on a section bar brings up to five practice assessments for that section

        Steps:
        Click on the user menu in the upper right corner 
        Click on "Performance Forecast"
        Scroll to the Individual Chapters section
        Click on a section bar

        Expected Result:
        The user is presented with up to five practice assessments for that section
        """
        self.ps.test_updates['name'] = 't1.50.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.50',
            't1.50.009',
            '8295'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8296 - 010 - Student | Bars without enough data show Practice More To Get Forecast instead of a color bar
    @pytest.mark.skipif(str(8296) not in TESTS, reason='Excluded')  # NOQA
    def test_student_(self):
        """Bars without enough data show Practice More To Get Forecast instead of a color bar

        Steps:
        Click on the user menu in the upper right corner 
        Click on "Performance Forecast"
        Scroll to the Individual Chapters section

        Expected Result:
        The user is presented with the "Practice More To Get Forecast" button under a section without enough data instead of a color bar
        """
        self.ps.test_updates['name'] = 't1.50.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.50',
            't1.50.010',
            '8296'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True
