"""Tutor, Performance Forecast, Student
More Performance Forecast Functionality"""

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
        162192
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

    # Case C162192 - 004 - Student | View more Performance Forecast functions
    @pytest.mark.skipif(str(162192) not in TESTS, reason='Excluded')
    def test_student_return_to_dashboard_button_162192(self):
        """
        #STEPS
        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the student user account [ | ] in the username and password text
        boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a Tutor course name

        Click on the user menu in the upper right corner
        Click on "Performance Forecast"
        Click on "Return To Dashboard"
        ***The user is presented with the list dashboard.***

        Click on the user menu in the upper right corner
        Click on "Performance Forecast"
        Scroll to the Individual Chapters section
        Click on a section bar.
        # EXPECTED RESULT
        ***The user is presented with up to five practice assessments for that
        section.***


        """
        self.ps.test_updates['name'] = 't1.50.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.50',
            't1.50.004',
            '162192'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.select_course(appearance='college_physics')
        self.student.page.wait_for_page_load()

        # The User is presented with the list dashboard
        self.student.open_user_menu()
        self.student.find(By.PARTIAL_LINK_TEXT, 'Performance Forecast').click()
        assert('guide' in self.student.current_url()), \
            'Not viewing performance forecast'
        self.student.sleep(5)
        self.student.open_user_menu()
        self.student.wait.until(
            expect.presence_of_element_located(
                (By.LINK_TEXT, 'Dashboard')
            )
        ).click()

        self.student.sleep(5)

        self.student.find(By.CSS_SELECTOR, '.student-dashboard')

        # The User is presented with up to five practice assessments for that
        # section

        self.student.open_user_menu()
        self.student.find(By.PARTIAL_LINK_TEXT, 'Performance Forecast').click()
        assert('guide' in self.student.current_url()), \
            'Not viewing performance forecast'
        self.student.find(
            By.XPATH,
            "//div[@class='chapter-panel']/div[@class='sections']" +
            "/div[@class='section']/button"
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
