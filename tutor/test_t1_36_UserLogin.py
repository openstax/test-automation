"""Tutor v1, Epic 36 - User login."""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from staxing.helper import Admin, Student, Teacher, ContentQA

basic_test_env = json.dumps([
    {
        'platform': 'Windows 10',
        'browserName': 'chrome',
        'version': '50.0',
        'screenResolution': "1024x768",
    },
])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([
        8238, 8239, 8240, 8241, 8242,
        8243, 8244, 8245, 8246, 58271,
        58272
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestUserLogin(unittest.TestCase):
    """T1.36 - User login."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.user = None

    def tearDown(self):
        """Test destructor."""
        self.ps.update_job(
            job_id=str(self.user.driver.session_id),
            **self.ps.test_updates
        )
        try:
            self.user.delete()
        except:
            pass

    # Case C8238 - 001 - Admin | Log into Tutor
    @pytest.mark.skipif(str(8238) not in TESTS, reason='Excluded')
    def test_admin_log_into_tutor_8238(self):
        """Log into Tutor.

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

        admin = Admin(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        self.user = admin
        admin.driver.get(admin.url)
        admin.page.wait_for_page_load()
        # check to see if the screen width is normal or condensed
        if admin.driver.get_window_size()['width'] <= admin.CONDENSED_WIDTH:
            # get small-window menu toggle
            is_collapsed = admin.driver.find_element(
                By.XPATH,
                '//button[contains(@class,"navbar-toggle")]'
            )
            # check if the menu is collapsed and, if yes, open it
            if('collapsed' in is_collapsed.get_attribute('class')):
                is_collapsed.click()
        admin.wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'Login')
            )
        ).click()
        admin.page.wait_for_page_load()
        admin.driver.find_element(By.ID, 'auth_key').send_keys(admin.username)
        admin.driver.find_element(By.ID, 'password').send_keys(admin.password)
        # click on the sign in button
        admin.driver.find_element(
            By.XPATH,
            '//button[text()="Sign in"]'
        ).click()
        admin.page.wait_for_page_load()
        assert('dashboard' in admin.current_url()), \
            'Not taken to dashboard: %s' % admin.current_url()

        self.ps.test_updates['passed'] = True

    # Case C8239 - 002 - Admin | Access the Admin Console
    @pytest.mark.skipif(str(8239) not in TESTS, reason='Excluded')
    def test_admin_access_the_admin_console_8239(self):
        """Access the Admin console.

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

        admin = Admin(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        self.user = admin
        admin.login()
        admin.open_user_menu()
        admin.wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Admin')
            )
        ).click()
        admin.page.wait_for_page_load()
        admin.driver.find_element(
            By.XPATH, '//h1[contains(text(),"Admin Console")]')

        self.ps.test_updates['passed'] = True

    # Case C8240 - 003 - Admin | Log out
    @pytest.mark.skipif(str(8240) not in TESTS, reason='Excluded')
    def test_admin_log_out_8240(self):
        """Log out.

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

        admin = Admin(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        self.user = admin
        admin.login()
        admin.open_user_menu()
        admin.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//input[contains(@value,"Log Out")]')
            )
        ).click()
        admin.page.wait_for_page_load()
        admin.driver.find_element(
            By.XPATH, '//div[contains(@class,"tutor-home")]')

        self.ps.test_updates['passed'] = True

    # Case C8241 - 004 - Content Analyst | Log into Tutor
    @pytest.mark.skipif(str(8241) not in TESTS, reason='Excluded')
    def test_content_analyst_log_into_tutor_8241(self):
        """Log into Tutor.

        Steps:
        Click on the 'Login' button
        Enter the content analyst account in the username and password boxes
        Click on the 'Sign in' button

        Expected Result:
        The user is signed in
        """
        self.ps.test_updates['name'] = 't1.36.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.36', 't1.36.004', '8241']
        self.ps.test_updates['passed'] = False

        content = ContentQA(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        self.user = content
        content.driver.get(content.url)
        content.page.wait_for_page_load()
        # check to see if the screen width is normal or condensed
        if content.driver.get_window_size()['width'] <= \
           content.CONDENSED_WIDTH:
            # get small-window menu toggle
            is_collapsed = content.driver.find_element(
                By.XPATH,
                '//button[contains(@class,"navbar-toggle")]'
            )
            # check if the menu is collapsed and, if yes, open it
            if('collapsed' in is_collapsed.get_attribute('class')):
                is_collapsed.click()
        content.wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'Login')
            )
        ).click()
        content.page.wait_for_page_load()
        content.driver.find_element(
            By.ID,
            'auth_key'
        ).send_keys(content.username)
        content.driver.find_element(
            By.ID,
            'password'
        ).send_keys(content.password)
        # click on the sign in button
        content.driver.find_element(
            By.XPATH,
            '//button[text()="Sign in"]'
        ).click()
        content.page.wait_for_page_load()
        assert('dashboard' in content.current_url()), \
            'Not taken to dashboard: %s' % content.current_url()

        self.ps.test_updates['passed'] = True

    # Case C8242 - 005 - Content Analyst | Access the QA Viewer
    @pytest.mark.skipif(str(8242) not in TESTS, reason='Excluded')
    def test_content_analyst_access_the_qa_viewer_8242(self):
        """Access the QA Viewer.

        Steps:
        Click on the 'Login' button
        Enter the content analyst account in the username and password boxes
        Click on the 'Sign in' button
        Click on the user menu
        Click on the QA Content option

        Expected Result:
        The user is presented with the QA viewer
        """
        self.ps.test_updates['name'] = 't1.36.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.36', 't1.36.005', '8242']
        self.ps.test_updates['passed'] = False

        content = ContentQA(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        self.user = content
        content.login()
        content.open_user_menu()
        content.wait.until(
            expect.element_to_be_clickable((
                By.XPATH,
                '//a[contains(text(),"QA Content") and @role="menuitem"]'
            ))
        ).click()
        content.page.wait_for_page_load()
        assert('/qa' in content.current_url()), \
            'Not taken to the QA viewer: %s' % content.current_url()

        self.ps.test_updates['passed'] = True

    # Case C8243 - 006 - Content Analyst | Access the Content Analyst Console
    @pytest.mark.skipif(str(8243) not in TESTS, reason='Excluded')
    def test_content_analyst_access_the_content_analyst_console_8243(self):
        """Access the Content Annalyst Console.

        Steps:
        Click on the 'Login' button
        Enter the content analyst account in the username and password boxes
        Click on the 'Sign in' button
        Click on the user menu
        Click on the Content Analyst option

        Expected Result:
        The user is presented with the Content Analyst Console
        """
        self.ps.test_updates['name'] = 't1.36.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.36', 't1.36.006', '8243']
        self.ps.test_updates['passed'] = False

        content = ContentQA(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        self.user = content
        content.login()
        content.open_user_menu()
        content.wait.until(
            expect.element_to_be_clickable((
                By.XPATH,
                '//a[contains(text(),"Content Analyst") and @role="menuitem"]'
            ))
        ).click()
        content.page.wait_for_page_load()
        content.driver.find_element(
            By.XPATH,
            '//h1[contains(text(),"Content Analyst Console")]'
        )

        self.ps.test_updates['passed'] = True

    # Case C8244 - 007 - Content Analyst | Log out
    @pytest.mark.skipif(str(8244) not in TESTS, reason='Excluded')
    def test_content_analyst_log_out_8244(self):
        """Log out.

        Steps:
        Click on the 'Login' button
        Enter the content analyst account in the username and password boxes
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

        content = ContentQA(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        self.user = content
        content.login()
        content.open_user_menu()
        content.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//input[contains(@value,"Log Out")]')
            )
        ).click()
        content.page.wait_for_page_load()
        content.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"tutor-home")]'
        )

        self.ps.test_updates['passed'] = True

    # Case C8245 - 008 - Student | Log into Tutor
    @pytest.mark.skipif(str(8245) not in TESTS, reason='Excluded')
    def test_student_log_into_tutor_8245(self):
        """Log into Tutor.

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

        student = Student(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        self.user = student
        student.driver.get(student.url)
        student.page.wait_for_page_load()
        # check to see if the screen width is normal or condensed
        if student.driver.get_window_size()['width'] <= \
           student.CONDENSED_WIDTH:
            # get small-window menu toggle
            is_collapsed = student.driver.find_element(
                By.XPATH,
                '//button[contains(@class,"navbar-toggle")]'
            )
            # check if the menu is collapsed and, if yes, open it
            if('collapsed' in is_collapsed.get_attribute('class')):
                is_collapsed.click()
        student.wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'Login')
            )
        ).click()
        student.page.wait_for_page_load()
        student.driver.find_element(
            By.ID,
            'auth_key'
        ).send_keys(student.username)
        student.driver.find_element(
            By.ID,
            'password'
        ).send_keys(student.password)
        # click on the sign in button
        student.driver.find_element(
            By.XPATH,
            '//button[text()="Sign in"]'
        ).click()
        student.page.wait_for_page_load()
        assert('dashboard' in student.current_url()), \
            'Not taken to dashboard: %s' % student.current_url()

        self.ps.test_updates['passed'] = True

    # Case C8246 - 009 - Teacher | Log into Tutor
    @pytest.mark.skipif(str(8246) not in TESTS, reason='Excluded')
    def test_teacher_log_into_tutor_8246(self):
        """Log into Tutor.

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

        teacher = Teacher(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        self.user = teacher
        teacher.driver.get(teacher.url)
        teacher.page.wait_for_page_load()
        # check to see if the screen width is normal or condensed
        if teacher.driver.get_window_size()['width'] <= \
           teacher.CONDENSED_WIDTH:
            # get small-window menu toggle
            is_collapsed = teacher.driver.find_element(
                By.XPATH,
                '//button[contains(@class,"navbar-toggle")]'
            )
            # check if the menu is collapsed and, if yes, open it
            if('collapsed' in is_collapsed.get_attribute('class')):
                is_collapsed.click()
        teacher.wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'Login')
            )
        ).click()
        teacher.page.wait_for_page_load()
        teacher.driver.find_element(
            By.ID,
            'auth_key'
        ).send_keys(teacher.username)
        teacher.driver.find_element(
            By.ID,
            'password'
        ).send_keys(teacher.password)
        # click on the sign in button
        teacher.driver.find_element(
            By.XPATH,
            '//button[text()="Sign in"]'
        ).click()
        teacher.page.wait_for_page_load()
        assert('dashboard' in teacher.current_url()),\
            'Not taken to dashboard: %s' % teacher.current_url()

        self.ps.test_updates['passed'] = True

    # Case C58271 - 010 - Student | Log out
    @pytest.mark.skipif(str(58271) not in TESTS, reason='Excluded')
    def test_content_analyst_log_out_58271(self):
        """Log out.

        Steps:
        Click on the 'Login' button
        Enter the student account in the username and password boxes
        Click on the 'Sign in' button
        Click on the user menu
        Click on the Log out option

        Expected Result:
        The user is logged out
        """
        self.ps.test_updates['name'] = 't1.36.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.36', 't1.36.010', '58271']
        self.ps.test_updates['passed'] = False

        student = Student(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        self.user = student
        student.login()
        student.open_user_menu()
        student.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//input[contains(@value,"Log Out")]')
            )
        ).click()
        student.page.wait_for_page_load()
        student.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"tutor-home")]'
        )

        self.ps.test_updates['passed'] = True

    # Case C58272 - 011 - Teacher | Log out
    @pytest.mark.skipif(str(58272) not in TESTS, reason='Excluded')
    def test_teacher_log_out_58272(self):
        """Log out.

        Steps:
        Click on the 'Login' button
        Enter the teacher account in the username and password boxes
        Click on the 'Sign in' button
        Click on the user menu
        Click on the Log out option

        Expected Result:
        The user is logged out
        """
        self.ps.test_updates['name'] = 't1.36.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.36', 't1.36.011', '58272']
        self.ps.test_updates['passed'] = False

        teacher = Teacher(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        self.user = teacher
        teacher.login()
        teacher.open_user_menu()
        teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//input[contains(@value,"Log Out")]')
            )
        ).click()
        teacher.page.wait_for_page_load()
        teacher.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"tutor-home")]'
        )

        self.ps.test_updates['passed'] = True
