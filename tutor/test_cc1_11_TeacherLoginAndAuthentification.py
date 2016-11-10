"""Concept Coach v1, Epic 11 - Teacher Login and Authentification."""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
# from random import randint
from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as expect
# from staxing.assignment import Assignment

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Teacher

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': 'latest',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([
        7688, 7689, 7690
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestTeacherLoginAndAuthentification(unittest.TestCase):
    """CC1.11 - Teacher Login and Authentification."""

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

    # Case C7688 - 001 - Teacher | Log into Concept Coach
    @pytest.mark.skipif(str(7688) not in TESTS, reason='Excluded')
    def test_teacher_log_into_concept_coach_7688(self):
        """Log into Concept Coach.

        Steps:
        Go to Tutor
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a CC course name

        Expected Result:
        User is taken to the class dashboard.
        """
        self.ps.test_updates['name'] = 'cc1.11.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.11',
            'cc1.11.001',
            '7688'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='macro_economics')
        self.teacher.sleep(5)

        assert('cc-dashboard' in self.teacher.current_url()), \
            'Not viewing the cc dashboard'

        self.ps.test_updates['passed'] = True

    # Case C7689 - 002 - Teacher | Logging out returns to the login page
    @pytest.mark.skipif(str(7689) not in TESTS, reason='Excluded')
    def test_teacher_loggin_out_returns_to_the_login_page_7689(self):
        """Logging out returns to the login page.

        Steps:
        Click the user menu containing the user's name
        Click the 'Log Out' button

        Expected Result:
        User is taken to cc.openstax.org
        """
        self.ps.test_updates['name'] = 'cc1.11.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.11',
            'cc1.11.002',
            '7689'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='macro_economics')
        self.teacher.sleep(5)

        assert('dashboard' in self.teacher.current_url()), \
            'Not viewing the cc dashboard'

        self.teacher.open_user_menu()
        self.teacher.sleep(1)
        self.teacher.find(By.XPATH, "//a/form[@class='-logout-form']").click()

        assert('cc.openstax.org' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.ps.test_updates['passed'] = True

    # Case C7690 - 003 - Teacher | Can log into Tutor and be redirected to CC
    @pytest.mark.skipif(str(7690) not in TESTS, reason='Excluded')
    def test_teacher_can_log_into_tutor_and_be_redirected_to_cc_7690(self):
        """Can log into Tutor and be redirected to Concept Coach.

        Steps:
        Go to Tutor
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a CC course name

        Expected Result:
        User is taken to the class dashboard
        """
        self.ps.test_updates['name'] = 'cc1.11.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.11',
            'cc1.11.003',
            '7690'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='macro_economics')
        self.teacher.sleep(5)

        assert('cc-dashboard' in self.teacher.current_url()), \
            'Not viewing the cc dashboard'

        self.ps.test_updates['passed'] = True
