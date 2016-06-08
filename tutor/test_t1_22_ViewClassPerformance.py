"""Tutor v1, Epic 22 - View Class Performance."""

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
    str([12845, 12846, 12847, 12848, 
        12849, 12850, 12851, 12852])  # NOQA
)


@PastaDecorator.on_platforms(BROWSERS)
class TestEpicName(unittest.TestCase):
    """T1.22 - View Class Performance."""

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

    # Case T12845 - 001 - Teacher | View the period Performance Forecast
    @pytest.mark.skipif(str(12845) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_view_the_period_performance_forecast(self):
        """View the period Performance Froecast

        Steps:
        On the calendar dashboard, click on the "Performance Forecast" button on the upper right corner of the calendar OR 
        click on the user drop down menu then click on the "Performance Forecast" button
        Click on the desired period

        Expected Result:
        The period Performance Forecast is presented to the user
        """
        self.ps.test_updates['name'] = 't1.22.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.22',
            't1.22.001',
            '12845'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case T12846 - 002 - Teacher | Info icon shows an explanation of the data
    @pytest.mark.skipif(str(12846) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_info_icon_shows_an_explanation_of_the_data(self):
        """Info icon shows an explanation of the data

        Steps:
        On the calendar dashboard, click on the "Performance Forecast" button on the upper right corner of the calendar OR 
        click on the user drop down menu then click on the "Performance Forecast" button
        Hover the cursor over the info icon that is next to the "Performance Forecast" header

        Expected Result:
        Info icon shows an explanation of the data
        """
        self.ps.test_updates['name'] = 't1.22.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.22',
            't1.22.002',
            '12846'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case T12847 - 003 - Teacher | View the performance color key
    @pytest.mark.skipif(str(12847) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_view_the_performance_color_key(self):
        """View the performance color key

        Steps:
        On the calendar dashboard, click on the "Performance Forecast" button on the upper right corner of the calendar OR click on the user drop down menu 
        click on the "Performance Forecast" button

        Expected Result:
        The performance color key is presented to the user (next to the 'Return to Dashboard' button)
        """
        self.ps.test_updates['name'] = 't1.22.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.22',
            't1.22.003',
            '12847'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case T12848 - 004 - Teacher | Return to Dashboard button returns to the calendar
    @pytest.mark.skipif(str(12848) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_return_to_dashboard_button_returns_to_the_calendar(self):
        """Return to Dashboard button returns to the calendar

        Steps:
        On the calendar dashboard, click on the "Performance Forecast" button on the upper right corner of the calendar OR Click on the user drop down menu 
        Click on the "Performance Forecast" button

        Expected Result:
        The calendar dashboard is presented to the user
        """
        self.ps.test_updates['name'] = 't1.22.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.22',
            't1.22.004',
            '12848'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case T12849 - 005 - Teacher | Periods tabs are shown
    @pytest.mark.skipif(str(12849) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_period_tabs_are_shown(self):
        """Period tabs are shown

        Steps:
        On the calendar dashboard, click on the "Performance Forecast" button on the upper right corner of the calendar OR click on the user drop down menu 
        click on the "Performance Forecast" button

        Expected Result:
        The period tabs are shown to the user (below the "Performance Forecast" header)
        """
        self.ps.test_updates['name'] = 't1.22.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.22',
            't1.22.005',
            '12849'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case T12850 - 006 - Teacher | A period with zero answers does not show section breakdowns
    @pytest.mark.skipif(str(12850) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_a_period_with_zero_answers_does_not_show_section_breakdowns(self):
        """A period with zero answers does not show section breakdowns

        Steps:
        On the calendar dashboard, click on the "Performance Forecast" button on the upper right corner of the calendar OR click on the user drop down menu
        click on the "Performance Forecast" button
        Click on the period with zero answers        

        Expected Result:
        The user should see no section breakdowns as well as the words "There have been no questions worked for this period."
        """
        self.ps.test_updates['name'] = 't1.22.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.22',
            't1.22.006',
            '12850'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case T12851 - 007 - Teacher | Weaker areas shows up to four problematic sections
    @pytest.mark.skipif(str(12851) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_weaker_areas_shows_up_to_four_problematic_sections(self):
        """Weaker areas shows up to four problematic sections

        Steps:
        On the calendar dashboard, click on the "Performance Forecast" button on the upper right corner of the calendar OR click on the user drop down menu
        click on the "Performance Forecast" button
        Click on the desired period

        Expected Result:
        Weaker Areas show up to four problematic sections
        """
        self.ps.test_updates['name'] = 't1.22.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.22',
            't1.22.007',
            '12851'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case T12852 - 008 - Teacher | Chapters are listed on the left with their sections to the right
    @pytest.mark.skipif(str(12852) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_chapters_are_listed_on_the_left_with_their_sections_to_the_right(self):
        """Chapters are listed on the left with their sections to the right

        Steps:
        On the calendar dashboard, click on the "Performance Forecast" button on the upper right corner of the calendar OR click on the user drop down menu
        click on the "Performance Forecast" button
        Click on the desired period
        Scroll to the "Individual Chapters" section

        Expected Result:
        Chapters are listed on the left with their sections to the right
        """
        self.ps.test_updates['name'] = 't1.22.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.22',
            't1.22.008',
            '12852'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True
