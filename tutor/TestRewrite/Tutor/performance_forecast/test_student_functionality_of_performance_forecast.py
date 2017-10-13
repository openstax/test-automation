"""Tutor, Performance Forecast, Student
Functionality of Performance Forecast"""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
# from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from staxing.helper import Student
# from selenium.common.exceptions import TimeoutException

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
        162191
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestViewTheListDashboard(unittest.TestCase):
    """T1.45 - View the list dashboard."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        if not LOCAL_RUN:
            self.student = Student(
                use_env_vars=True,
                pasta_user=self.ps,
                capabilities=self.desired_capabilities
            )
        else:
            self.student = Student(
                use_env_vars=True
            )
        self.student.login()

    def tearDown(self):
        """Test destructor."""
        if not LOCAL_RUN:
            self.ps.update_job(
                job_id=str(self.student.driver.session_id),
                **self.ps.test_updates
            )
        try:
            self.student.delete()
        except:
            pass

    # Case C162191 - 001 - Student | View the Performance Forecast and its
    # functions
    @pytest.mark.skipif(str(162191) not in TESTS, reason='Excluded')
    def test_student_view_personal_performance_forecast_162191(self):
        """
        #STEPS
        Go to OpenStax Tutor QA
        Click on the 'Login' button
        Enter the student user account [  |  ] in the username and password
        text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a Tutor course name

        Click on the user menu in the upper right corner
        Click on "Performance Forecast"
        ***The user is presented with personal Performance Forecast***
        ***The performance color key is presented to the user (next to the
        'Return to Dashboard' button)***
        ***The user is presented with up to four problematic sections under My
        Weaker Areas***

        Hover the cursor over the info icon that is next to the "Performance
        Forecast" header
        ***Info icon shows an explanation of the data.***

        Scroll to Individual Chapters section
        ***The user is presented with chapters listed on the left and their
        sections on the right.***
        ***The user is presented with the "Practice More To Get Forecast"
        button under a section without
        enough data instead of a color bar.***


        Click on a chapter bar
        # EXPECTED RESULT
        ***The user is presented with up to five practice assessments for that
        chapter***

        """
        self.ps.test_updates['name'] = 't1.50.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.50',
            't1.50.001',
            '162191'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.select_course(appearance='college_physics')
        self.student.page.wait_for_page_load()

        # View Personal Performance Forecast
        self.student.open_user_menu()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.CLASS_NAME, 'viewPerformanceGuide')
            )
        ).click()
        assert('guide' in self.student.current_url()), \
            'Not viewing the performance forecast'

        # View Performance Color Key
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.CLASS_NAME, 'guide-key')
            )
        )

        self.student.sleep(5)

        # User is presented with 4 problematic sections
        weak = self.student.driver.find_elements_by_xpath(
            "//div[@class='chapter-panel weaker']/div[@class='sections']" +
            "/div[@class='section']")

        self.student.sleep(5)

        assert(len(weak) <= 4), \
            'More than four weaker sections'

        # Info icon shows an explanation of data
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.CLASS_NAME, 'info-link')
            )
        ).click()

        self.student.sleep(5)

        # User is presented with chapters listed on the left and their sections
        # on the right
        # Get all the chapter panels
        panels = self.student.driver.find_elements_by_class_name(
            'chapter-panel')

        # Should be one chapter button for each panel, at least one section
        # button per panel
        for panel in panels:
            chapter = panel.find_elements_by_class_name('chapter')
            sections = panel.find_elements_by_class_name('sections')
            assert(len(sections) > 0), \
                'no sections found'
            assert(chapter[0].location.get('x') <=
                   sections[0].location.get('x')), \
                'section to the left of chapter'
        self.student.sleep(5)

        # User is presented with the "Practice More To Get Forecast" button
        # under a section without
        # enough data instead of a color bar

        self.student.open_user_menu()
        self.student.find(By.PARTIAL_LINK_TEXT, 'Performance Forecast').click()
        assert('guide' in self.student.current_url()), \
            'Not viewing performance forecast'
        self.student.find(By.CLASS_NAME, 'no-data')

        # User is presented with up to five practice assesments for that
        # chapter

        self.student.wait.until(
            expect.presence_of_element_located((
                By.XPATH,
                "//div[@class='chapter']/button"
            ))
        ).click()

        assert('practice' in self.student.current_url()), \
            'Not presented with practice problems'

        self.student.sleep(5)
        breadcrumbs = self.student.find_all(
            By.XPATH,
            '//span[contains(@class,"breadcrumb-exercise")]')
        assert(len(breadcrumbs) <= 5), \
            "more than 5 questions"

        self.ps.test_updates['passed'] = True
