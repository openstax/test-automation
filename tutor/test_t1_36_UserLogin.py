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
from selenium.webdriver.common.keys import Keys

basic_test_env = json.dumps([
    {
        'platform': 'Windows 10',
        'browserName': 'chrome',
        'version': 'latest',
        'screenResolution': "1024x768",
    },
])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
LOCAL_RUN = os.getenv('LOCALRUN', 'false').lower() == 'true'
TESTS = os.getenv(
    'CASELIST',
    str([
        8238, 8239, 8240, 8241, 8242,
        8243, 8244, 8245, 58271, 8246,
        58272, 96962, 96964,
    ])
    # Not implemented
    # 96963
    # 96965
    # 96966
    # 96967
)


@PastaDecorator.on_platforms(BROWSERS)
class TestUserLogin(unittest.TestCase):
    """T1.36 - User login."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        if not LOCAL_RUN:
            self.admin = Admin(
                use_env_vars=True,
                pasta_user=self.ps,
                capabilities=self.desired_capabilities
            )
            self.content = ContentQA(
                existing_driver=self.admin.driver,
                use_env_vars=True,
                pasta_user=self.ps,
                capabilities=self.desired_capabilities
            )
            self.student = Student(
                existing_driver=self.admin.driver,
                use_env_vars=True,
                pasta_user=self.ps,
                capabilities=self.desired_capabilities
            )
            self.teacher = Teacher(
                existing_driver=self.admin.driver,
                use_env_vars=True,
                pasta_user=self.ps,
                capabilities=self.desired_capabilities
            )
        else:
            self.admin = Admin(
                use_env_vars=True,
            )
            self.content = ContentQA(
                existing_driver=self.admin.driver,
                use_env_vars=True,
            )
            self.student = Student(
                existing_driver=self.admin.driver,
                use_env_vars=True,
            )
            self.teacher = Teacher(
                existing_driver=self.admin.driver,
                use_env_vars=True,
            )

    def tearDown(self):
        """Test destructor."""
        if not LOCAL_RUN:
            self.ps.update_job(
                job_id=str(self.admin.driver.session_id),
                **self.ps.test_updates
            )
        try:
            self.teacher = None
            self.student = None
            self.content = None
            self.admin.delete()
        except:
            pass

    # Case C8238 - 001 - Admin | Log into Tutor
    @pytest.mark.skipif(str(8238) not in TESTS, reason='Excluded')
    def test_admin_log_into_tutor_8238(self):
        """Log into Tutor.

        Steps:
        Click on the 'Log in' button
        Enter the admin account in the username and password text boxes
        Click on the 'Sign in' button

        Expected Result:
        User is logged in
        """
        self.ps.test_updates['name'] = 't1.36.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.36', 't1.36.001', '8238']
        self.ps.test_updates['passed'] = False

        self.admin.get(self.admin.url)
        self.admin.page.wait_for_page_load()

        # check to see if the screen width is normal or condensed
        if self.admin.driver.get_window_size()['width'] <= \
                self.admin.CONDENSED_WIDTH:
            # get small-window menu toggle
            is_collapsed = self.admin.find(
                By.XPATH,
                '//button[contains(@class,"navbar-toggle")]'
            )
            # check if the menu is collapsed and, if yes, open it
            if('collapsed' in is_collapsed.get_attribute('class')):
                is_collapsed.click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'Log in')
            )
        ).click()
        self.admin.page.wait_for_page_load()

        self.admin.find(By.ID, 'login_username_or_email') \
            .send_keys(self.admin.username)
        self.admin.find(By.XPATH, "//input[@value='Next']").click()
        self.admin.find(By.ID, 'login_password') \
            .send_keys(self.admin.password)

        # click on the sign in button
        self.admin.find(By.XPATH, "//input[@value='Log in']").click()
        self.admin.page.wait_for_page_load()
        assert('dashboard' in self.admin.current_url()), \
            'Not taken to dashboard: %s' % self.admin.current_url()

        self.ps.test_updates['passed'] = True

    # Case C8239 - 002 - Admin | Access the Admin Console
    @pytest.mark.skipif(str(8239) not in TESTS, reason='Excluded')
    def test_admin_access_the_admin_console_8239(self):
        """Access the Admin console.

        Steps:
        Click on the 'Log in' button
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

        self.admin.login()
        self.admin.open_user_menu()
        self.admin.wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Admin')
            )
        ).click()
        self.admin.page.wait_for_page_load()
        self.admin.find(
            By.XPATH,
            '//h1[contains(text(),"Admin Console")]'
        )

        self.ps.test_updates['passed'] = True

    # Case C8240 - 003 - Admin | Log out
    @pytest.mark.skipif(str(8240) not in TESTS, reason='Excluded')
    def test_admin_log_out_8240(self):
        """Log out.

        Steps:
        Click on the 'Log in' button
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

        self.admin.login()
        self.admin.open_user_menu()
        self.admin.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//input[contains(@value,"Log out")]')
            )
        ).click()
        self.admin.page.wait_for_page_load()

        self.admin.find(
            By.XPATH,
            '//div[contains(@class,"tutor-home")]'
        )

        self.ps.test_updates['passed'] = True

    # Case C8241 - 004 - Content Analyst | Log into Tutor
    @pytest.mark.skipif(str(8241) not in TESTS, reason='Excluded')
    def test_content_analyst_log_into_tutor_8241(self):
        """Log into Tutor.

        Steps:
        Click on the 'Log in' button
        Enter the content analyst account in the username and password boxes
        Click on the 'Sign in' button

        Expected Result:
        The user is signed in
        """
        self.ps.test_updates['name'] = 't1.36.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.36', 't1.36.004', '8241']
        self.ps.test_updates['passed'] = False

        self.content.get(self.content.url)
        self.content.page.wait_for_page_load()

        # check to see if the screen width is normal or condensed
        if self.content.driver.get_window_size()['width'] <= \
           self.content.CONDENSED_WIDTH:
            # get small-window menu toggle
            is_collapsed = self.content.find(
                By.XPATH,
                '//button[contains(@class,"navbar-toggle")]'
            )
            # check if the menu is collapsed and, if yes, open it
            if('collapsed' in is_collapsed.get_attribute('class')):
                is_collapsed.click()
        self.content.wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'Log in')
            )
        ).click()
        self.content.page.wait_for_page_load()

        self.content.find(By.ID, 'login_username_or_email') \
            .send_keys(self.content.username)
        self.content.find(By.XPATH, "//input[@value='Next']").click()
        self.content.find(By.ID, 'login_password') \
            .send_keys(self.content.password)

        # click on the sign in button
        self.content.find(By.XPATH, "//input[@value='Log in']").click()
        self.content.page.wait_for_page_load()

        assert('dashboard' in self.content.current_url()), \
            'Not taken to dashboard: %s' % self.content.current_url()

        self.ps.test_updates['passed'] = True

    # Case C8242 - 005 - Content Analyst | Access the QA Viewer
    @pytest.mark.skipif(str(8242) not in TESTS, reason='Excluded')
    def test_content_analyst_access_the_qa_viewer_8242(self):
        """Access the QA Viewer.

        Steps:
        Click on the 'Log in' button
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

        self.content.login()
        self.content.open_user_menu()
        self.content.wait.until(
            expect.element_to_be_clickable((
                By.XPATH,
                '//div[contains(text(),"QA Content")]'
            ))
        ).click()
        self.content.page.wait_for_page_load()

        assert('/qa' in self.content.current_url()), \
            'Not taken to the QA viewer: %s' % self.content.current_url()

        self.ps.test_updates['passed'] = True

    # Case C8243 - 006 - Content Analyst | Access the Content Analyst Console
    @pytest.mark.skipif(str(8243) not in TESTS, reason='Excluded')
    def test_content_analyst_access_the_content_analyst_console_8243(self):
        """Access the Content Annalyst Console.

        Steps:
        Click on the 'Log in' button
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

        self.content.login()
        self.content.open_user_menu()
        self.content.wait.until(
            expect.element_to_be_clickable((
                By.XPATH,
                '//div[contains(text(),"Content Analyst")]'
            ))
        ).click()
        self.content.page.wait_for_page_load()

        self.content.find(

            By.XPATH,
            '//h1[contains(text(),"Content Analyst Console")]'
        )

        self.ps.test_updates['passed'] = True

    # Case C8244 - 007 - Content Analyst | Log out
    @pytest.mark.skipif(str(8244) not in TESTS, reason='Excluded')
    def test_content_analyst_log_out_8244(self):
        """Log out.

        Steps:
        Click on the 'Log in' button
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

        self.content.login()
        self.content.open_user_menu()
        self.content.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//input[contains(@value,"Log out")]')
            )
        ).click()
        self.content.page.wait_for_page_load()

        self.content.find(
            By.XPATH,
            '//div[contains(@class,"tutor-home")]'
        )

        self.ps.test_updates['passed'] = True

    # Case C8245 - 008 - Student | Log into Tutor
    @pytest.mark.skipif(str(8245) not in TESTS, reason='Excluded')
    def test_student_log_into_tutor_8245(self):
        """Log into Tutor.

        Steps:
        Click on the 'Log in' button
        Enter the student account in the username and password text boxes
        Click on the 'Sign in' button

        Expected Result:
        The user is logged in
        """
        self.ps.test_updates['name'] = 't1.36.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.36', 't1.36.008', '8245']
        self.ps.test_updates['passed'] = False

        self.student.get(self.student.url)
        self.student.page.wait_for_page_load()

        # check to see if the screen width is normal or condensed
        if self.student.driver.get_window_size()['width'] <= \
           self.student.CONDENSED_WIDTH:
            # get small-window menu toggle
            is_collapsed = self.student.find(
                By.XPATH,
                '//button[contains(@class,"navbar-toggle")]'
            )
            # check if the menu is collapsed and, if yes, open it
            if('collapsed' in is_collapsed.get_attribute('class')):
                is_collapsed.click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'Log in')
            )
        ).click()
        self.student.page.wait_for_page_load()

        self.student.find(By.ID, 'login_username_or_email') \
            .send_keys(self.student.username)
        self.student.find(By.XPATH, "//input[@value='Next']") \
            .click()
        self.student.find(By.ID, 'login_password') \
            .send_keys(self.student.password)

        # click on the sign in button
        self.student.find(By.XPATH, "//input[@value='Log in']").click()
        self.student.page.wait_for_page_load()

        assert('dashboard' in self.student.current_url()), \
            'Not taken to dashboard: %s' % self.student.current_url()

        self.ps.test_updates['passed'] = True

    # Case C8246 - 009 - Teacher | Log into Tutor
    @pytest.mark.skipif(str(8246) not in TESTS, reason='Excluded')
    def test_teacher_log_into_tutor_8246(self):
        """Log into Tutor.

        Steps:
        Click on the 'Log in' button
        Enter the teacher account in the username and password text boxes
        Click on the 'Sign in' button

        Expected Result:
        The user is logged in
        """
        self.ps.test_updates['name'] = 't1.36.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.36', 't1.36.009', '8246']
        self.ps.test_updates['passed'] = False

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

        self.teacher.find(By.ID, 'login_username_or_email') \
            .send_keys(self.teacher.username)
        self.teacher.find(By.XPATH, "//input[@value='Next']").click()
        self.teacher.find(By.ID, 'login_password') \
            .send_keys(self.teacher.password)

        # click on the sign in button
        self.teacher.find(By.XPATH, "//input[@value='Log in']").click()
        self.teacher.page.wait_for_page_load()

        assert('dashboard' in self.teacher.current_url()),\
            'Not taken to dashboard: %s' % self.teacher.current_url()

        self.ps.test_updates['passed'] = True

    # Case C58271 - 010 - Student | Log out
    @pytest.mark.skipif(str(58271) not in TESTS, reason='Excluded')
    def test_content_analyst_log_out_58271(self):
        """Log out.

        Steps:
        Click on the 'Log in' button
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

        self.student.login()
        self.student.open_user_menu()
        self.student.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//input[contains(@value,"Log out")]')
            )
        ).click()
        self.student.page.wait_for_page_load()

        self.student.find(By.XPATH, '//div[contains(@class,"tutor-home")]')

        self.ps.test_updates['passed'] = True

    # Case C58272 - 011 - Teacher | Log out
    @pytest.mark.skipif(str(58272) not in TESTS, reason='Excluded')
    def test_teacher_log_out_58272(self):
        """Log out.

        Steps:
        Click on the 'Log in' button
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

        self.teacher.login()
        self.teacher.open_user_menu()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//input[contains(@value,"Log out")]')
            )
        ).click()
        self.teacher.page.wait_for_page_load()

        self.teacher.find(By.XPATH, '//div[contains(@class,"tutor-home")]')

        self.ps.test_updates['passed'] = True

    # Case C96962 - 012 - Content Reviewer | Log into Exercises
    @pytest.mark.skipif(str(96962) not in TESTS, reason='Excluded')
    def test_content_reviewer_log_into_exercises_96962(self):
        """Log into Exercises.

        Steps:
        Go to https://exercises-qa.openstax.org/
        Click "SIGN IN"
        Enter the Content username into "Email or username" text box
        Click "Next"
        Enter the Content password into "password" text box
        Click "Login"

        Expected Result:
        User is logged in
        """
        self.ps.test_updates['name'] = 't1.36.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.36', 't1.36.012', '96962']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.content.driver.get("https://exercises-qa.openstax.org/")
        self.content.sleep(3)

        self.content.find(By.LINK_TEXT, "SIGN IN").click()
        self.content.find(By.XPATH, "//input[@id='login_username_or_email']") \
            .send_keys(os.getenv('CONTENT_USER'))
        self.content.find(By.XPATH, "//input[@id='login_username_or_email']") \
            .send_keys(Keys.RETURN)
        self.content.sleep(2)

        self.content.find(By.XPATH, "//input[@id='login_password']") \
            .send_keys(os.getenv('CONTENT_PASSWORD'))
        self.content.find(By.XPATH, "//input[@id='login_password']") \
            .send_keys(Keys.RETURN)
        self.content.sleep(3)

        self.content.find(By.LINK_TEXT, "SIGN OUT")

        self.ps.test_updates['passed'] = True

    # Case C96963 - 013 - Content Reviewer | Access Reviewer Display
    @pytest.mark.skipif(str(96963) not in TESTS, reason='Excluded')
    def test_content_reviewer_access_reviewer_display_96963(self):
        """Access Reviewer Display.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 't1.36.013' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.36', 't1.36.013', '96963']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C96964 - 014 - Content Reviewer | Log out
    @pytest.mark.skipif(str(96964) not in TESTS, reason='Excluded')
    def test_content_reviewer_log_out_96964(self):
        """Log out.

        Steps:
        go to https://exercises-qa.openstax.org/
        Click "SIGN IN"
        Enter into "Email or username" text box
        Click "Next"
        Enter into "password" text box
        Click "Login"
        Click "SIGN OUT"

        Expected Result:
        User is logged out.
        """
        self.ps.test_updates['name'] = 't1.36.014' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.36', 't1.36.014', '96964']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.content.driver.get("https://exercises-qa.openstax.org/")
        self.content.sleep(3)

        self.content.find(By.LINK_TEXT, "SIGN IN").click()
        self.content.find(By.XPATH, "//input[@id='login_username_or_email']") \
            .send_keys(os.getenv('CONTENT_USER'))
        self.content.find(By.XPATH, "//input[@id='login_username_or_email']") \
            .send_keys(Keys.RETURN)
        self.content.sleep(2)

        self.content.find(By.XPATH, "//input[@id='login_password']") \
            .send_keys(os.getenv('CONTENT_PASSWORD'))
        self.content.find(By.XPATH, "//input[@id='login_password']") \
            .send_keys(Keys.RETURN)
        self.content.sleep(3)

        self.content.find(By.LINK_TEXT, "SIGN OUT").click()
        self.content.sleep(2)

        self.content.find(By.LINK_TEXT, "SIGN IN")

        self.ps.test_updates['passed'] = True

    # Case C96965 - 015 - Content Editor | Log into Exercises
    @pytest.mark.skipif(str(96965) not in TESTS, reason='Excluded')
    def test_content_editor_log_into_exercises_96965(self):
        """Log into Exercises.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 't1.36.015' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.36', 't1.36.015', '96965']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C96962 - 016 - Content Editor | Access the Exercise Editor
    @pytest.mark.skipif(str(96966) not in TESTS, reason='Excluded')
    def test_content_editor_access_the_exercise_editor_96966(self):
        """Access the Exercise Editor.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 't1.36.016' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.36', 't1.36.016', '96966']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C96967 - 017 - Content Editor | Log out
    @pytest.mark.skipif(str(96967) not in TESTS, reason='Excluded')
    def test_content_editor_log_out_96967(self):
        """Log out.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 't1.36.017' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.36', 't1.36.017', '96967']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
