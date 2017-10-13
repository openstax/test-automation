"""Tutor, Performance Forecast, Student
User With Only One Course and No Work Done"""

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
        162193
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestViewTheListDashboard(unittest.TestCase):
    """Student Performance Forecast"""

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

    # Case C162193 - 005 - Student | Using a student with one Tutor course with
    # no work done
    @pytest.mark.skipif(str(162193) not in TESTS, reason='Excluded')
    def test_student_bypass_the_course_picker_162193(self):
        """
        #STEPS
        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the student user account [  |  ] in the username and password
        text boxes
        Click on the 'Sign in' button
        ***The user bypasses the course picker and is presented with the
        dashboard***

        If the user has more than one course, click on a Tutor course name
        Click on the user menu in the upper right corner
        Click on "Performance Forecast"
        ***The user is presented with blank performance forecast with no
        section breakdowns and the words
        "You haven't worked enough problems for Tutor to predict your weakest
        topics."***

        Click the OpenStax logo
        # EXPECTED RESULT
        ***The user is returned to their dashboard.***

        """
        self.ps.test_updates['name'] = 't1.38.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.38',
            't1.38.002',
            '162193'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.user = Student(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        self.user.login(username="qas_01")
        assert('list' in self.user.current_url()), \
            'Not in a course'

        # The user is presented with blank performance forecast with no section
        # breakdowns and the words
        # "You haven't worked enough problems for Tutor to predict your weakest
        # topics."
        self.student.logout()
        self.student.driver.get("https://tutor-qa.openstax.org/")
        self.student.login(username=os.getenv('STUDENT_NO_WORK'),
                           url="https://tutor-qa.openstax.org/")
        self.student.select_course(appearance='college_physics')
        self.student.find(By.CSS_SELECTOR, '.student-dashboard')
        self.student.open_user_menu()
        self.student.find(By.PARTIAL_LINK_TEXT, 'Performance Forecast').click()
        assert('guide' in self.student.current_url()), \
            'Not viewing performance forecast'
        self.student.find(By.CLASS_NAME, "no-data-message")
        self.student.sleep(5)

        # Click on the OpenStax logo to return to the dashboard

        self.student.logout()
        student2 = Student(
            username=os.getenv('STUDENT_USER_ONE_COURSE'),
            password=os.getenv('STUDENT_PASSWORD'),
            existing_driver=self.student.driver,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        student2.login()
        student2.page.wait_for_page_load()
        student2.open_user_menu()
        student2.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//a[contains(text(),"Performance Forecast") ' +
                 'and @role="menuitem"]')
            )
        ).click()
        self.student.driver.find_element(
            By.XPATH,
            '//i[contains(@class,"ui-brand-logo")]'
        ).click()
        assert('list' in self.student.current_url()), \
            'Not viewing the list dashboard 011'

        self.ps.test_updates['passed'] = True
