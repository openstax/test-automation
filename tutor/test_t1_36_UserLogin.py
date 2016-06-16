"""Tutor v1, Epic 36 - UserLogin."""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
from random import randint  # NOQA
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as expect
# from staxing.assignment import Assignment
# from staxing.helper import Teacher, Student
from staxing.helper import Admin, Student, Teacher, ContentQA

basic_test_env = json.dumps([
    {
        'platform': 'Windows 10',
        'browserName': 'chrome',
        'version': '50.0',
        'screenResolution': "1024x768",
    },
    {
        'platform': 'Windows 7',
        'browserName': 'firefox',
        'version': 'latest',
        'screenResolution': '1024x768',
    },
])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([8238, 8239, 8240, 8241, 8242,
         8243, 8244, 8245, 8246])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestUserLogin(unittest.TestCase):
    """T1.36 - User Login."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.teacher = Teacher(
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

    # Case C8238 - 001 - Admin | Log into Tutuor
    @pytest.mark.skipif(str(8238) not in TESTS, reason='Excluded')
    def test_teacher_view_the_calendar_dashboard(self):
        """View the calendar dashboard.

        Steps:
        If the user has more than one course, click on a Tutor course name
        Click on the 'Login' button
        Enter the admin account in the username and password text boxes
        Click on the 'Sign in' button

        Expected Result:
        User is logged in
        """
        self.ps.test_updates['name'] = 't1.36.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.36', 't1.36.001', '8238']
        self.ps.test_updates['passed'] = False

        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.ps.test_updates['passed'] = True

    # Case C8238 - 001 - Admin | Log into Tutuor
    @pytest.mark.skipif(str(8238) not in TESTS, reason='Excluded')
    def test_admin_view_the_calendar_dashboard(self):
        """View the calendar dashboard.

        Steps:
        Click on the 'Login' button
        Enter the admin account in the username and password text boxes
        Click on the 'Sign in' button

        Expected Result:
        User is logged in
        """
        self.ps.test_updates['name'] = 't1.36.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.36', 't1.36.001', '8238']
        self.ps.test_updates['passed'] = False



        self.ps.test_updates['passed'] = True


    # Case C8239 - 002 - Admin | Access the Admin Console
    @pytest.mark.skipif(str(8239) not in TESTS, reason='Excluded')
    def test_admin_access_the_admin_console(self):
        """Access the Admin Console

        Steps:
        Click on the 'Login' button
        Enter the admin account in the username and password text boxes
        Click on the 'Sign in' button
        Click on the user menu
        Click on the Admin option

        Expected Result:
        User is presented with the admin console
        """
        self.ps.test_updates['name'] = 't1.36.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.36', 't1.36.002', '8239']
        self.ps.test_updates['passed'] = False



        self.ps.test_updates['passed'] = True

    # Case C8240 - 003 - Admin | Access the Admin Console
    @pytest.mark.skipif(str(8240) not in TESTS, reason='Excluded')
    def test_admin_access_the_admin_console(self):
        """Access the Admin Console

        Steps:
        Click on the 'Login' button
        Enter the admin account in the username and password text boxes
        Click on the 'Sign in' button
        Click on the user menu
        Click on the Log out option

        Expected Result:
        The User is signed out
        """
        self.ps.test_updates['name'] = 't1.36.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.36', 't1.36.003', '8240']
        self.ps.test_updates['passed'] = False



        self.ps.test_updates['passed'] = True

    # Case C8241 - 004 - Content Annalyst | Log into Tutor
    @pytest.mark.skipif(str(8241) not in TESTS, reason='Excluded')
    def test_content_annalyst_log_into_tutor(self):
        """Log into Tutor

        Steps:
        Click on the 'Login' button
        Enter the content annalyst account in the username and password text boxes
        Click on the 'Sign in' button

        Expected Result:
        The user is signed out
        """
        self.ps.test_updates['name'] = 't1.36.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.36', 't1.36.004', '8241']
        self.ps.test_updates['passed'] = False



        self.ps.test_updates['passed'] = True

    # Case C8242 - 005 - Content Annalyst | Access the QA Viewer
    @pytest.mark.skipif(str(8242) not in TESTS, reason='Excluded')
    def test_content_annalyst_access_the_qa_viewer(self):
        """Access the QA Viewer

        Steps:
        Click on the 'Login' button
        Enter the content annalyst account in the username and password text boxes
        Click on the 'Sign in' button
        Click on the user menu
        Click on the QA content option

        Expected Result:
        The user is presented with the QA viewer
        """
        self.ps.test_updates['name'] = 't1.36.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.36', 't1.36.005', '8242']
        self.ps.test_updates['passed'] = False



        self.ps.test_updates['passed'] = True

    # Case C8243 - 006 - Content Annalyst | Access the Content Annalyst Console
    @pytest.mark.skipif(str(8243) not in TESTS, reason='Excluded')
    def test_content_annalyst_access_the_content_annalyst_console(self):
        """ Access the Content Annalyst Console

        Steps:
        Click on the 'Login' button
        Enter the content annalyst account in the username and password text boxes
        Click on the 'Sign in' button
        Click on the user menu
        Click on the Content Annalyst option

        Expected Result:
        The user is presented with the Content Annalyst Console
        """
        self.ps.test_updates['name'] = 't1.36.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.36', 't1.36.006', '8243']
        self.ps.test_updates['passed'] = False



        self.ps.test_updates['passed'] = True

    # Case C8244 - 007 - Content Annalyst | Log out
    @pytest.mark.skipif(str(8244) not in TESTS, reason='Excluded')
    def test_content_annalyst_log_out(self):
        """ Log out

        Steps:
        Click on the 'Login' button
        Enter the content annalyst account in the username and password text boxes
        Click on the 'Sign in' button
        Click on the user menu
        Click on the Log out option

        Expected Result:
        The user is logged out
        """
        self.ps.test_updates['name'] = 't1.36.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.36', 't1.36.007', '8244']
        self.ps.test_updates['passed'] = False



        self.ps.test_updates['passed'] = True

    # Case C8245 - 008 - Student | Log into Tutor
    @pytest.mark.skipif(str(8245) not in TESTS, reason='Excluded')
    def test_student_log_into_tutor(self):
        """ Log into Tutor

        Steps:
        Click on the 'Login' button
        Enter the student account in the username and password text boxes
        Click on the 'Sign in' button

        Expected Result:
        The user is logged in
        """
        self.ps.test_updates['name'] = 't1.36.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.36', 't1.36.008', '8245']
        self.ps.test_updates['passed'] = False



        self.ps.test_updates['passed'] = True

    # Case C8246 - 009 - Teacher | Log into Tutor
    @pytest.mark.skipif(str(8246) not in TESTS, reason='Excluded')
    def test_teacher_log_into_tutoe(self):
        """ Log into Tutor

        Steps:
        Click on the 'Login' button
        Enter the teacher account in the username and password text boxes
        Click on the 'Sign in' button

        Expected Result:
        The user is logged in
        """
        self.ps.test_updates['name'] = 't1.36.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.36', 't1.36.009', '8246']
        self.ps.test_updates['passed'] = False



        self.ps.test_updates['passed'] = True
