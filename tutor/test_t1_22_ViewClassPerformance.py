"""Tutor v1, Epic 22 - View Class Performance."""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
# from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
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
    'version': '50.0',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([
        8148, 8149, 8150, 8151, 8152,
        8153, 8154, 8155
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestViewClassPerformance(unittest.TestCase):
    """T1.22 - View Class Performance."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.teacher = Teacher(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        self.teacher.login()

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

    # Case C8148 - 001 - Teacher | View the period Performance Forecast
    @pytest.mark.skipif(str(8148) not in TESTS, reason='Excluded')
    def test_teacher_view_the_period_performance_forecast_8148(self):
        """View the period Performance Forecast.

        Steps:
        On the calendar dashboard, click on the "Performance Forecast" button
        on the upper right corner of the calendar OR
        click on the user drop down menu then click on the
        "Performance Forecast" button
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
            '8148'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Performance Forecast').click()
        assert('guide' in self.teacher.current_url()), \
            'Not viewing performance forecast'

        self.ps.test_updates['passed'] = True

    # Case C8149 - 002 - Teacher | Info icon shows an explanation of the data
    @pytest.mark.skipif(str(8149) not in TESTS, reason='Excluded')
    def test_teacher_info_icon_shows_an_explanation_of_the_data_8149(self):
        """Info icon shows an explanation of the data.

        Steps:
        On the calendar dashboard, click on the "Performance Forecast" button
            on the upper right corner of the calendar
            OR
        Click on the user drop down menu then click on the
        "Performance Forecast" button
        Hover the cursor over the info icon that is next to the
        "Performance Forecast" header

        Expected Result:
        Info icon shows an explanation of the data
        """
        self.ps.test_updates['name'] = 't1.22.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.22',
            't1.22.002',
            '8149'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Performance Forecast').click()
        assert('guide' in self.teacher.current_url()), \
            'Not viewing performance forecast'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.CLASS_NAME, 'info-link')
            )
        ).click()

        self.ps.test_updates['passed'] = True

    # Case C8150 - 003 - Teacher | View the performance color key
    @pytest.mark.skipif(str(8150) not in TESTS, reason='Excluded')
    def test_teacher_view_the_performance_color_key_8150(self):
        """View the performance color key.

        Steps:
        On the calendar dashboard, click on the "Performance Forecast"
        button on the upper right corner of the calendar OR
        click on the user drop down menu
        click on the "Performance Forecast" button

        Expected Result:
        The performance color key is presented to the user
        (next to the 'Return to Dashboard' button)
        """
        self.ps.test_updates['name'] = 't1.22.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.22',
            't1.22.003',
            '8150'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Performance Forecast').click()
        assert('guide' in self.teacher.current_url()), \
            'Not viewing performance forecast'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.CLASS_NAME, 'guide-key')
            )
        )

        self.ps.test_updates['passed'] = True

    # Case C8151 - 004 - Teacher | Return to Dashboard button returns to
    # the calendar
    @pytest.mark.skipif(str(8151) not in TESTS, reason='Excluded')
    def test_teacher_return_to_dashboard_button_returns_to_the_cal_8151(self):
        """Return to Dashboard button returns to the calendar.

        Steps:
        On the calendar dashboard, click on the "Performance Forecast"
        button on the upper right corner of the calendar OR
        Click on the user drop down menu
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
            '8151'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Performance Forecast').click()
        assert('guide' in self.teacher.current_url()), \
            'Not viewing performance forecast'

        self.teacher.open_user_menu()
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.LINK_TEXT, 'Dashboard')
            )
        ).click()

        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.ps.test_updates['passed'] = True

    # Case C8152 - 005 - Teacher | Periods tabs are shown
    @pytest.mark.skipif(str(8152) not in TESTS, reason='Excluded')
    def test_teacher_period_tabs_are_shown_8152(self):
        """Period tabs are shown.

        Steps:
        On the calendar dashboard, click on the "Performance Forecast" button
        on the upper right corner of the calendar OR
        click on the user drop down menu
        click on the "Performance Forecast" button

        Expected Result:
        The period tabs are shown to the user
        (below the "Performance Forecast" header)
        """
        self.ps.test_updates['name'] = 't1.22.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.22',
            't1.22.005',
            '8152'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Performance Forecast').click()
        assert('guide' in self.teacher.current_url()), \
            'Not viewing performance forecast'

        self.teacher.find(By.CLASS_NAME, 'active')

        self.ps.test_updates['passed'] = True

    # Case C8153 - 006 - Teacher | A period with zero answers does not
    # show section breakdowns
    @pytest.mark.skipif(str(8153) not in TESTS, reason='Excluded')
    def test_teacher_a_period_w_zero_answers_does_not_show_breaks_8153(self):
        """A period with zero answers does not show section breakdowns.

        Steps:
        On the calendar dashboard, click on the "Performance Forecast"
            button on the upper right corner of the calendar OR
        Click on the user drop down menu
        Click on the "Performance Forecast" button
        Click on the period with zero answers

        Expected Result:
        The user should see no section breakdowns as well as the words
        "There have been no questions worked for this period."
        """
        self.ps.test_updates['name'] = 't1.22.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.22',
            't1.22.006',
            '8153'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        # Create an empty period to use for the test
        self.teacher.open_user_menu()
        self.teacher.find(
            By.PARTIAL_LINK_TEXT, 'Course Settings and Roster').click()
        self.teacher.sleep(5)

        self.teacher.find(
            By.XPATH, "//li[@class='control add-period']/button").click()
        self.teacher.find(
            By.XPATH,
            "//input[@class='form-control empty']").send_keys("Epic 22")
        self.teacher.find(
            By.XPATH,
            "//button[@class='async-button " +
            "-edit-period-confirm btn btn-default']").click()
        self.teacher.sleep(5)

        # Check the new empty period in Performance Forecast
        self.teacher.open_user_menu()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Performance Forecast').click()
        assert('guide' in self.teacher.current_url()), \
            'Not viewing performance forecast'

        self.teacher.wait.until(
            expect.visibility_of_element_located((
                By.LINK_TEXT, 'Epic 22'))).click()

        self.teacher.wait.until(
            expect.visibility_of_element_located((
                By.CLASS_NAME, 'no-data-message')))
        self.teacher.sleep(5)

        # Archive the new period
        self.teacher.open_user_menu()
        self.teacher.find(
            By.PARTIAL_LINK_TEXT, 'Course Settings and Roster').click()
        self.teacher.sleep(5)

        self.teacher.wait.until(
            expect.visibility_of_element_located((
                By.LINK_TEXT, 'Epic 22'))).click()

        self.teacher.find(
            By.XPATH, "//a[@class='control archive-period']").click()
        self.teacher.find(
            By.XPATH,
            "//button[@class='async-button archive-section btn btn-default']"
        ).click()
        self.teacher.sleep(5)

        self.ps.test_updates['passed'] = True

    # Case C8154 - 007 - Teacher | Weaker areas shows up to
    # four problematic sections
    @pytest.mark.skipif(str(8154) not in TESTS, reason='Excluded')
    def test_teacher_weaker_shows_up_to_four_problematic_sections_8154(self):
        """Weaker areas shows up to four problematic sections.

        Steps:
        On the calendar dashboard, click on the "Performance Forecast"
        button on the upper right corner of the calendar OR
        click on the user drop down menu
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
            '8154'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Performance Forecast').click()
        assert('guide' in self.teacher.current_url()), \
            'Not viewing performance forecast'

        weak = self.teacher.driver.find_elements_by_xpath(
            "//div[@class='chapter-panel weaker']/div[@class='sections']/div")

        assert(len(weak) <= 4), \
            'Not viewing performance forecast'

        self.teacher.sleep(5)

        self.ps.test_updates['passed'] = True

    # Case C8155 - 008 - Teacher | Chapters are listed on the left with
    # their sections to the right
    @pytest.mark.skipif(str(8155) not in TESTS, reason='Excluded')
    def test_teacher_chapters_listed_on_left_w_sections_on_right_8155(self):
        """Chapter are listed on the left with their sections to the right.

        Steps:
        On the calendar dashboard, click on the "Performance Forecast"
            button on the upper right corner of the calendar
            OR
        Click on the user drop down menu
        Click on the "Performance Forecast" button
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
            '8155'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Performance Forecast').click()
        assert('guide' in self.teacher.current_url()), \
            'Not viewing performance forecast'

        self.teacher.page.wait_for_page_load()

        panels = self.teacher.driver.find_elements_by_class_name(
            'chapter-panel')
        for panel in panels:
            panel.find_elements_by_class_name('chapter')
            panel.find_elements_by_class_name('sections')
        self.teacher.sleep(5)

        self.ps.test_updates['passed'] = True
