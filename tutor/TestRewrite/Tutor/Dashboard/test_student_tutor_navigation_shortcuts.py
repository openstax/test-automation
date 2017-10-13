"""Tutor, Student - Navigation Shortcuts."""

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
        162194
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestViewTheListDashboard(unittest.TestCase):
    """Student - Navigation Shortcuts."""

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

    # Case C162194 - 005 - Student | Navigation Shortcuts
    @pytest.mark.skipif(str(162194) not in TESTS, reason='Excluded')
    def test_student_select_a_course_162194(self):
        """
        #STEPS
        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the student username [  ] in the username text box
        Click 'Next'
        Enter the student password [  ] in the password text box
        Click on the 'Login' button
        ***The user logs into Tutor and is presented with a list of courses if
        they
        have multiple courses, or their dashboard for a course if they are only
        enrolled in one course***

        Click on a Tutor course name
        ***The user selects a course and is presented with the dashboard.***

        Open the drop down menu by clicking the menu link containing the user's
        name
        Click the 'Performance Forecast' button
        Click on the name of the course
        ***The user is returned to their dashboard.***

        Click on the OpenStax logo
        ***The user is returned to the course picker.***

        Click on the user menu on the right of the header
        Click 'Log Out'
        # EXPECTED RESULT
        ***User is logged out of tutor***

        """
        self.ps.test_updates['name'] = 't1.38.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.38',
            't1.38.001',
            '162194'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        # Select a Course
        self.student.select_course(appearance='intro_sociology')
        self.student.page.wait_for_page_load()

        # Click on course name to return to the dashboard

        self.student.open_user_menu()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.CLASS_NAME, 'viewPerformanceGuide')
            )
        ).click()

        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.CLASS_NAME, 'course-name')
            )
        ).click()

        # Click on logo to return to course picker

        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.CLASS_NAME, 'ui-brand-logo')
            )
        ).click()

        self.ps.test_updates['passed'] = True
