"""Concept Coach v1, Epic 11 - Teacher Login and Authentification."""

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
        7688, 7689
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestTeacherLoginAndAuthentification(unittest.TestCase):
    """CC1.11 - Teacher Login and Authentification."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        if not LOCAL_RUN:
            self.teacher = Teacher(
                use_env_vars=True,
                pasta_user=self.ps,
                capabilities=self.desired_capabilities
            )
        else:
            self.teacher = Teacher(
                use_env_vars=True
            )

    def tearDown(self):
        """Test destructor."""
        if not LOCAL_RUN:
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
        self.ps.test_updates['tags'] = ['cc1', 'cc1.11', 'cc1.11.001', '7688']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.get(self.teacher.url)
        self.teacher.page.wait_for_page_load()
        # check to see if the screen width is normal or condensed
        if self.teacher.driver.get_window_size()['width'] <= \
           self.teacher.CONDENSED_WIDTH:
            # get small-window menu toggle
            is_collapsed = self.teacher.find(
                By.XPATH,
                '//button[contains(@class,"navbar-toggle")]'
            )
            # check if the menu is collapsed and, if yes, open it
            if('collapsed' in is_collapsed.get_attribute('class')):
                is_collapsed.click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'Log in')
            )
        ).click()
        self.teacher.page.wait_for_page_load()
        self.teacher.find(
            By.ID, 'login_username_or_email'
        ).send_keys(self.teacher.username)
        self.teacher.find(By.CSS_SELECTOR, '.primary').click()
        self.teacher.find(
            By.ID, 'login_password'
        ).send_keys(self.teacher.password)
        self.teacher.find(By.CSS_SELECTOR, '.primary').click()
        self.teacher.page.wait_for_page_load()
        # check if a password change is required
        if 'reset your password' in self.teacher.driver.page_source.lower():
            try:
                self.teacher.find(By.ID, 'set_password_password') \
                    .send_keys(self.teacher.password)
                self.teacher.find(
                    By.ID, 'set_password_password_confirmation') \
                    .send_keys(self.teacher.password)
                self.teacher.find(By.CSS_SELECTOR, '.primary').click()
                self.teacher.sleep(1)
                self.teacher.find(By.CSS_SELECTOR, '.primary').click()
            except Exception as e:
                raise e
        self.teacher.page.wait_for_page_load()
        source = self.teacher.driver.page_source.lower()
        print('Reached Terms/Privacy')
        while 'terms of use' in source or 'privacy policy' in source:
            self.teacher.accept_contract()
            self.teacher.page.wait_for_page_load()
            source = self.teacher.driver.page_source.lower()
        assert('dashboard' in self.teacher.current_url()),\
            'Not taken to dashboard: %s' % self.teacher.current_url()

        self.teacher.driver.find_element(
            By.XPATH,
            '//p[contains(text(),"OpenStax Concept Coach")]'
        ).click()
        self.teacher.driver.find_element(
            By.XPATH,
            '//span[text()="Class Dashboard"]'
        )

        self.ps.test_updates['passed'] = True

    # Case C7689 - 002 - Teacher | Logging out returns to the Concept Coach
    # landing page
    @pytest.mark.skipif(str(7689) not in TESTS, reason='Excluded')
    def test_teacher_loggin_out_returns_to_concept_coach_landing_pa_7689(self):
        """Logging out returns to the Concept Coach landing page.

        Steps:
        Click the user menu containing the user's name
        Click the 'Log Out' button

        Expected Result:
        User is taken to cc.openstax.org
        """
        self.ps.test_updates['name'] = 'cc1.11.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc1', 'cc1.11', 'cc1.11.002', '7689']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.driver.find_element(
            By.XPATH,
            '//p[contains(text(),"OpenStax Concept Coach")]'
        ).click()
        self.teacher.open_user_menu()
        self.teacher.sleep(1)
        self.teacher.find(By.XPATH, "//a//input[@value='Log out']").click()

        assert('cc.openstax.org' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.ps.test_updates['passed'] = True

    '''
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
    '''
