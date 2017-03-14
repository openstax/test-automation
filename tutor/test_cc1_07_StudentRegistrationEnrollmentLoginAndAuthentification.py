"""Concept Coach v1, Epic 7.

Student Registration, Enrollment, Login, and Authentification.
"""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
# from staxing.assignment import Assignment
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Student, Teacher, Admin

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
        7631, 7632, 7634, 7635, 7636,
        7637, 7639, 7640, 7641, 7642,
        7643, 7644, 7645, 7648, 7650,
        87364, 87365
    ])
    # issues:
    # 7650 - assistive tech, not registering tab key to move from elements
    # 87364, 87365 - no steps testrail.
)


@PastaDecorator.on_platforms(BROWSERS)
class TestStudentRegistrationEnrollmentLoginAuthentificatio(unittest.TestCase):
    """CC1.07 - Student Registration, Enrollment, Login and Authentication."""

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
            self.teacher = Teacher(
                use_env_vars=True,
                existing_driver=self.student.driver,
                pasta_user=self.ps,
                capabilities=self.desired_capabilities
            )
            self.admin = Admin(
                use_env_vars=True,
                existing_driver=self.student.driver,
                pasta_user=self.ps,
                capabilities=self.desired_capabilities
            )
        else:
            self.student = Student(
                use_env_vars=True,
            )
            self.teacher = Teacher(
                use_env_vars=True,
                existing_driver=self.student.driver,
            )
            self.admin = Admin(
                use_env_vars=True,
                existing_driver=self.student.driver,
            )

    def tearDown(self):
        """Test destructor."""
        if not LOCAL_RUN:
            self.ps.update_job(
                job_id=str(self.student.driver.session_id),
                **self.ps.test_updates
            )
        self.teacher = None
        self.admin = None
        try:
            self.student.delete()
        except:
            pass

    def get_enrollemnt_code(self, number=0):
        """
        Steps:
        Sign in as teacher
        Click on a Concept Coach course
        Click on "Course Settings and Roster" from the user menu
        Click "Your Student Enrollment Code"

        Return value: code, enrollemnt_url
            code - enrollment code
            enrollemnt_url - url of book for course
        """
        self.teacher.login()
        if number != 0:
            cc_courses = self.teacher.find_all(
                By.XPATH, '//a[contains(@href,"/cc-dashboard")]'
            )
            cc_courses[number].click()
        else:
            self.teacher.find(
                By.XPATH, '//a[contains(@href,"/cc-dashboard")]'
            ).click()
        self.teacher.open_user_menu()
        self.teacher.find(
            By.LINK_TEXT, 'Course Settings and Roster'
        ).click()
        self.teacher.find(
            By.XPATH, '//span[contains(text(),"Your student enrollment code")]'
        ).click()
        self.teacher.sleep(1)
        code = self.teacher.find(
            By.XPATH, '//p[@class="code"]'
        ).text
        enrollement_url = self.teacher.find(
            By.XPATH, '//textarea'
        ).text
        enrollement_url = enrollement_url.split('\n')[5]
        self.teacher.find(
            By.XPATH, '//button[@class="close"]'
        ).click()
        self.teacher.sleep(0.5)
        self.teacher.logout()
        return code, enrollement_url

    def create_user(self, start_num, end_num):
        """
        creates a new user and return the username
        """
        self.student.get("http://accounts-qa.openstax.org")
        num = str(randint(start_num, end_num))
        self.student.find(By.LINK_TEXT, 'Sign up').click()
        self.student.find(
            By.ID, 'identity-login-button').click()
        self.student.find(
            By.ID, 'signup_first_name').send_keys('first_name_001')
        self.student.find(
            By.ID, 'signup_last_name').send_keys('last_name_001')
        self.student.find(
            By.ID, 'signup_email_address').send_keys('email_001@test.com')
        self.student.find(
            By.ID, 'signup_username').send_keys('automated_07_'+num)
        self.student.find(
            By.ID, 'signup_password'
        ).send_keys(os.getenv('STUDENT_PASSWORD'))
        self.student.find(
            By.ID, 'signup_password_confirmation'
        ).send_keys(os.getenv('STUDENT_PASSWORD'))
        self.student.find(By.ID, 'signup_i_agree').click()
        self.student.find(
            By.ID, 'create_account_submit').click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'Sign out')
            )
        ).click()
        return 'automated_07_'+num

    # Case C7631 - 001 - Student | Register for a class using a provided
    # registration code - non-social login
    @pytest.mark.skipif(str(7631) not in TESTS, reason='Excluded')
    def test_student_register_for_a_class_using_a_provided_registra_7631(self):
        """Register for a class using a provided registration code - non-social login.

        Steps:
        Sign in as teacher100
        Click on a Concept Coach course
        Click on "Course Settings and Roster" from the user menu
        Click "Your Student Enrollment Code"
        Copy and paste the URL into an incognito window
        Click "Jump to Concept Coach"
        Click "Launch Concept Coach"
        Click Sign In
        Sign in as student71
        Enter the numerical enrollment code you get from the teacher
        Click "Enroll"
        Enter school issued ID, OR skip this step for now

        Expected Result:
        The student registers for a class using a provided registration code
        Is presented with Concept Coach after creating a free account
        """
        self.ps.test_updates['name'] = 'cc1.07.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.07',
            'cc1.07.001',
            '7631'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        # create a new user that will enroll in course
        rand_username = self.create_user(0, 999)
        # login as teacher to get access code
        code, enrollement_url = self.get_enrollemnt_code()
        # login as student to register for course
        self.student.get(enrollement_url)
        self.student.wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Jump to Concept Coach')
            )
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[text()="Launch Concept Coach"]')
            )
        ).click()
        self.student.page.wait_for_page_load()
        self.student.find(
            By.XPATH, '//div[text()="Sign in"]'
        ).click()
        self.student.sleep(0.5)
        login_window = self.student.driver.window_handles[1]
        cc_window = self.student.driver.window_handles[0]
        self.student.driver.switch_to_window(login_window)
        self.student.find(
            By.ID, 'auth_key').send_keys(rand_username)
        self.student.find(
            By.ID, 'password').send_keys(self.student.password)
        self.student.find(
            By.XPATH, '//button[text()="Sign in"]').click()
        try:
            self.student.find(By.ID, "i_agree").click()
            self.student.find(By.ID, "agreement_submit").click()
            self.student.find(By.ID, "i_agree").click()
            self.student.find(By.ID, "agreement_submit").click()
        except NoSuchElementException:
            pass
        self.student.driver.switch_to_window(cc_window)
        self.student.sleep(1)
        self.student.find(
            By.XPATH, '//input[@placeholder="enrollment code"]'
        ).send_keys(code)
        self.student.find(
            By.XPATH, '//button/span[text()="Enroll"]'
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[@class="skip"]')
            )
        ).click()
        # check that enrollemnt code worked, and student is at cc questions
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="task-breadcrumbs"]')
            )
        )
        self.ps.test_updates['passed'] = True

    # Case C7632 - 002 - Student | Register for a class using a provided
    # registration code - Facebook login
    @pytest.mark.skipif(str(7632) not in TESTS, reason='Excluded')
    def test_student_register_for_a_class_using_a_provided_registra_7632(self):
        """Register for a class using FB and a provided registration code.

        Steps:
        Sign in as teacher100
        Click on 'Course Settings and Roster' from the user menu
        Click 'Your Student Enrollment Code'
        Copy and paste the URL into an incognito window
        Click 'Jump to Concept Coach'
        Click 'Launch Concept Coach'
        Click 'Sign up'
        Click 'Sign up with Facebook'
        Log into Facebook
        Click 'Create Account'
        Enter enrollment code you get from teacher

        Expected Result:
        The student is presented with a confirmation message and
        Concept Coach questions after creating a free account
        """
        self.ps.test_updates['name'] = 'cc1.07.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.07',
            'cc1.07.002',
            '7632'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        # login as teacher to get access code
        code, enrollement_url = self.get_enrollemnt_code()
        # login as student to register for course
        self.student.get(enrollement_url)
        self.student.wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Jump to Concept Coach')
            )
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[text()="Launch Concept Coach"]')
            )
        ).click()
        self.student.page.wait_for_page_load()
        self.student.find(
            By.XPATH, '//div[text()="Sign in"]'
        ).click()
        self.student.sleep(0.5)
        login_window = self.student.driver.window_handles[1]
        cc_window = self.student.driver.window_handles[0]
        self.student.driver.switch_to_window(login_window)
        self.student.find(
            By.ID, 'facebook-login-button'
        ).click()

        self.student.find(
            By.ID, 'email'
        ).send_keys(os.getenv('FACEBOOK_USER'))
        self.student.find(
            By.ID, 'pass'
        ).send_keys(os.getenv('FACEBOOK_PASSWORD') + Keys.RETURN)
        self.student.driver.switch_to_window(cc_window)
        self.student.sleep(1)
        self.student.find(
            By.XPATH, '//input[@placeholder="enrollment code"]'
        ).send_keys(code)
        self.student.find(
            By.XPATH, '//button/span[text()="Enroll"]'
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[@class="skip"]')
            )
        ).click()
        # check that enrollemnt code worked, and student is at cc questions
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="task-breadcrumbs"]')
            )
        ).click()
        self.ps.test_updates['passed'] = True

    '''
    # Case C7633 - 003 - Student | Register for a class using a provided
    # registration code - Twitter login
    @pytest.mark.skipif(str(7633) not in TESTS, reason='Excluded')
    def test_student_register_for_a_class_using_a_provided_registra_7633(self):
        """Register for a class using a provided registration code - Twitter login.

        Steps:
        Sign in as teacher100
        Click on 'Course Settings and Roster' from the user menu
        Click 'Your Student Enrollment Code'
        Copy and paste the URL into an incognito window
        Click 'Jump to Concept Coach'
        Click 'Launch Concept Coach'
        Click 'Sign up'
        Click 'Sign up with Twitter'
        Log into Twitter
        Click 'Create Account'
        Enter enrollment code you get from teacher
        Enter school-issued ID or skip the step for now

        Expected Result:
        The student is presented with a confirmation message and CC questions
        """
        self.ps.test_updates['name'] = 'cc1.07.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.07',
            'cc1.07.003',
            '7633'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        # login as teacher to get access code
        code, enrollement_url = self.get_enrollemnt_code()
        # login as student to register for course
        self.student.get(enrollement_url)
        self.student.wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Jump to Concept Coach')
            )
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[text()="Launch Concept Coach"]')
            )
        ).click()
        self.student.page.wait_for_page_load()
        self.student.find(
            By.XPATH, '//div[text()="Sign in"]'
        ).click()
        self.student.sleep(0.5)
        login_window = self.student.driver.window_handles[1]
        cc_window = self.student.driver.window_handles[0]
        self.student.driver.switch_to_window(login_window)
        self.student.find(
            By.ID, 'twitter-login-button'
        ).click()
        self.student.find(
            By.ID, 'username_or_email'
        ).send_keys(os.getenv('TWITTER_USER'))
        self.student.find(
            By.ID, 'password'
        ).send_keys(os.getenv('TWITTER_PASSWORD') + Keys.RETURN)
        self.student.driver.switch_to_window(cc_window)
        self.student.sleep(1)
        self.student.find(
            By.XPATH, '//input[@placeholder="enrollment code"]'
        ).send_keys(code)
        self.student.find(
            By.XPATH, '//button/span[text()="Enroll"]'
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[@class="skip"]')
            )
        ).click()
        # check that enrollemnt code worked, and student is at cc questions
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="task-breadcrumbs"]')
            )
        )
        self.ps.test_updates['passed'] = True
    '''

    # Case C7634 - 004 - Student | Register for a class using a provided
    # registration code - Google login
    @pytest.mark.skipif(str(7634) not in TESTS, reason='Excluded')
    def test_student_register_for_a_class_using_a_provided_registra_7634(self):
        """Register for a class using a provided registration code - Google login.

        Steps:
        Sign in as teacher100
        Click on 'Course Settings and Roster' from the user menu
        Click 'Your Student Enrollment Code'
        Copy and paste the URL into an incognito window
        Click 'Jump to Concept Coach'
        Click 'Launch Concept Coach'
        Click 'Sign up'
        Click 'Sign up with Google'
        Log into Google
        Click 'Create Account'
        Enter enrollment code you get from teacher
        Enter school-issued ID or skip the step for now

        Expected Result:
        The student is presented with a confirmation message and CC questions
        """
        self.ps.test_updates['name'] = 'cc1.07.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.07',
            'cc1.07.004',
            '7634'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        # login as teacher to get access code
        code, enrollement_url = self.get_enrollemnt_code()
        # login as student to register for course
        self.student.get(enrollement_url)
        self.student.wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Jump to Concept Coach')
            )
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[text()="Launch Concept Coach"]')
            )
        ).click()
        self.student.page.wait_for_page_load()
        self.student.find(
            By.XPATH, '//div[text()="Sign in"]'
        ).click()
        self.student.sleep(0.5)
        login_window = self.student.driver.window_handles[1]
        cc_window = self.student.driver.window_handles[0]
        self.student.driver.switch_to_window(login_window)
        self.student.find(
            By.ID, 'google-login-button'
        ).click()
        self.student.find(
            By.ID, 'Email'
        ).send_keys(os.getenv('GOOGLE_USER') + Keys.RETURN)
        self.student.find(
            By.ID, 'Passwd'
        ).send_keys(os.getenv('GOOGLE_PASSWORD') + Keys.RETURN)
        self.student.driver.switch_to_window(cc_window)
        self.student.sleep(1)
        self.student.find(
            By.XPATH, '//input[@placeholder="enrollment code"]'
        ).send_keys(code)
        self.student.find(
            By.XPATH, '//button/span[text()="Enroll"]'
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[@class="skip"]')
            )
        ).click()
        # check that enrollemnt code worked, and student is at cc questions
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="task-breadcrumbs"]')
            )
        ).click()
        self.ps.test_updates['passed'] = True

    # Case C7635 - 005 - Student | After registering the user is shown a
    # confirmation message
    @pytest.mark.skipif(str(7635) not in TESTS, reason='Excluded')
    def test_student_after_registering_user_is_shown_a_confirmation_7635(self):
        """After registering the user is shown a confirmation message.

        Steps:
        Sign in as teacher100
        Click on a Concept Coach course
        Click on "Course Settings and Roster" from the user menu
        Click "Your Student Enrollment Code"
        Copy and paste the URL into an incognito window
        Click "Jump to Concept Coach"
        Click "Launch Concept Coach"
        Click Sign In
        Sign in as student71
        Enter the numerical enrollment code you get from the teacher
        Click "Enroll"
        Enter school issued ID, OR skip this step for now

        Expected Result:
        The user is presented with a confirmation message
        """
        self.ps.test_updates['name'] = 'cc1.07.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.07',
            'cc1.07.005',
            '7635'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        # create a new user that will enroll in course
        rand_username = self.create_user(1000, 1999)
        # login as teacher to get access code
        code, enrollement_url = self.get_enrollemnt_code()
        # login as student to register for course
        self.student.get(enrollement_url)
        self.student.wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Jump to Concept Coach')
            )
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[text()="Launch Concept Coach"]')
            )
        ).click()
        self.student.page.wait_for_page_load()
        self.student.find(
            By.XPATH, '//div[text()="Sign in"]'
        ).click()
        self.student.sleep(0.5)
        login_window = self.student.driver.window_handles[1]
        cc_window = self.student.driver.window_handles[0]
        self.student.driver.switch_to_window(login_window)
        self.student.find(
            By.ID, 'auth_key').send_keys(rand_username)
        self.student.find(
            By.ID, 'password').send_keys(self.student.password)
        self.student.find(
            By.XPATH, '//button[text()="Sign in"]').click()
        self.student.driver.switch_to_window(cc_window)
        self.student.sleep(1)
        self.student.find(
            By.XPATH, '//input[@placeholder="enrollment code"]'
        ).send_keys(code)
        self.student.find(
            By.XPATH, '//button/span[text()="Enroll"]'
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[@class="skip"]')
            )
        ).click()
        # check that enrollemnt code worked, and student is at cc questions
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//*[contains(text(),"You have successfully joined")]')
            )
        )

        self.ps.test_updates['passed'] = True

    # Case C7636 - 006 - Student | After a failed registration the user
    # is shown an error message
    @pytest.mark.skipif(str(7636) not in TESTS, reason='Excluded')
    def test_student_after_a_failed_registration_user_is_shown_an_7636(self):
        """After a failed registration the user is shown an error message.

        Steps:
        Sign in as teacher100
        Click on a Concept Coach course
        Click on "Course Settings and Roster" from the user menu
        Click "Your Student Enrollment Code"
        Copy and paste the URL into an incognito window
        Click "Jump to Concept Coach"
        Click "Launch Concept Coach"
        Click Sign In
        Sign in as student71
        Enter an incorrect enrollment code
        Click "Enroll"

        Expected Result:
        A failed registration results in an error message.
        """
        self.ps.test_updates['name'] = 'cc1.07.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.07',
            'cc1.07.006',
            '7636'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        # create a new user that will enroll in course
        rand_username = self.create_user(2000, 2999)
        # login as teacher to get access code
        code, enrollement_url = self.get_enrollemnt_code()
        # login as student to register for course
        self.student.get(enrollement_url)
        self.student.wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Jump to Concept Coach')
            )
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[text()="Launch Concept Coach"]')
            )
        ).click()
        self.student.page.wait_for_page_load()
        self.student.find(
            By.XPATH, '//div[text()="Sign in"]'
        ).click()
        self.student.sleep(0.5)
        login_window = self.student.driver.window_handles[1]
        cc_window = self.student.driver.window_handles[0]
        self.student.driver.switch_to_window(login_window)
        self.student.find(
            By.ID, 'auth_key').send_keys(rand_username)
        self.student.find(
            By.ID, 'password').send_keys(self.student.password)
        self.student.find(
            By.XPATH, '//button[text()="Sign in"]').click()
        self.student.driver.switch_to_window(cc_window)
        self.student.sleep(1)
        self.student.find(
            By.XPATH, '//input[@placeholder="enrollment code"]'
        ).send_keys('not a real enrollment code')
        self.student.find(
            By.XPATH, '//button/span[text()="Enroll"]'
        ).click()
        # find an error message
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//li[contains(text(),' +
                 '"The provided enrollment code is not valid.")]')
            )
        )
        self.ps.test_updates['passed'] = True

    # Case C7637 - 007 - Student | Able to change to another course
    @pytest.mark.skipif(str(7637) not in TESTS, reason='Excluded')
    def test_student_able_to_change_to_another_course_7637(self):
        """Able to change to another course.

        Steps:
        Go to a cc book
        go to a non-intorductory section
        launch Concept Coach
        login as student01
        go to a differnet cc book
        go to a non-intorductory section
        launch Concept Coach

        Expected Result:
        The student is in a new course and the student is still logged in
        """
        self.ps.test_updates['name'] = 'cc1.07.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.07',
            'cc1.07.007',
            '7637'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        # is it okay to use the url like this
        self.student.get(
            "https://qa.cnx.org/contents/JydfSfIS@2.2:HR_VN3f7@3/" +
            "Introduction-to-Science-and-th")
        # get to non-into section
        self.student.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button//span[text()="Contents"]')
            )
        ).click()
        self.student.sleep(0.5)
        self.student.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//span[@class="chapter-number" and text()="1.1"]')
            )
        ).click()
        # open concept coach
        self.student.wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Jump to Concept Coach')
            )
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[text()="Launch Concept Coach"]')
            )
        ).click()
        # login
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[text()="Sign in"]')
            )
        ).click()
        self.student.sleep(0.5)
        login_window = self.student.driver.window_handles[1]
        cc_window = self.student.driver.window_handles[0]
        self.student.driver.switch_to_window(login_window)
        self.student.find(
            By.ID, 'auth_key').send_keys('student01')
        self.student.find(
            By.ID, 'password').send_keys(self.student.password)
        self.student.find(
            By.XPATH, '//button[text()="Sign in"]').click()
        self.student.driver.switch_to_window(cc_window)
        self.student.sleep(0.5)
        # check for name
        self.student.find(
            By.XPATH, '//span[contains(text(),"Atticus")]'
        )
        # go to another course
        self.student.get(
            'https://qa.cnx.org/contents/lHoUF1_V@2.2:6RH0nLs4@8/' +
            'What-Economics-Is-and-Why-Its-')
        self.student.page.wait_for_page_load()
        # open concept coach
        self.student.wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Jump to Concept Coach')
            )
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[text()="Launch Concept Coach"]')
            )
        ).click()
        # check that still logged in
        self.student.find(
            By.XPATH, '//span[contains(text(),"Atticus")]'
        )
        self.ps.test_updates['passed'] = True

    '''
    # Case C7638 - 008 - Student | Able to change period in the same course
    @pytest.mark.skipif(str(7638) not in TESTS, reason='Excluded')
    def test_student_able_to_change_period_in_the_same_course_7638(self):
        """Able to change period in the same course.

        Steps:
        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the student user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a CC course name
        Select a section in the table of contents
        Scroll to the bottom of the section
        Click on 'Launch Concept Coach'
        Click on the user menu
        Click on 'Change Course'
        Enter the course code in the text box labeled 'enrollment code'
        Click the 'Enroll' button
        Click the 'Confirm' button

        Expected Result:
        The student is in a new period.
        """
        self.ps.test_updates['name'] = 'cc1.07.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.07',
            'cc1.07.008',
            '7638'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
    '''

    # Case C7639 - 009- Student | Able to enroll in more than one CC course
    @pytest.mark.skipif(str(7639) not in TESTS, reason='Excluded')
    def test_student_able_to_enroll_in_more_than_one_cc_course_7639(self):
        """Able to enroll in more than one Concept Coach course.

        Steps:
        create a new student
        get enrollment codes, and urls for two differnet cc courses
            -login as teacher
            - click on a cc course
            - in the user menu click Course settings and Roster
            - click Your student enrollment code
            (repeat for a second cc course)
        logout of teacher
        go to first url
        Click Jump to Concept Coach
        Click Launch Concept Coach
        login as student created earlier
        enter enrollemnt code
        repeat with second url and code(except don't have to login again)

        Expected Result:
        The student joins a new course.
        """
        self.ps.test_updates['name'] = 'cc1.07.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.07',
            'cc1.07.009',
            '7639'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        # create new student
        rand_username = self.create_user(8000, 8999)
        # get enrollemnet code for two diff cc courses
        code1, enrollement_url1 = self.get_enrollemnt_code()
        code2, enrollement_url2 = self.get_enrollemnt_code(1)
        # enroll in first course
        self.student.get(enrollement_url1)
        self.student.wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Jump to Concept Coach')
            )
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[text()="Launch Concept Coach"]')
            )
        ).click()
        self.student.page.wait_for_page_load()
        self.student.find(
            By.XPATH, '//div[text()="Sign in"]'
        ).click()
        self.student.sleep(0.5)
        login_window = self.student.driver.window_handles[1]
        cc_window = self.student.driver.window_handles[0]
        self.student.driver.switch_to_window(login_window)
        self.student.find(
            By.ID, 'auth_key').send_keys(rand_username)
        self.student.find(
            By.ID, 'password').send_keys(self.student.password)
        self.student.find(
            By.XPATH, '//button[text()="Sign in"]').click()
        try:
            self.student.find(By.ID, "i_agree").click()
            self.student.find(By.ID, "agreement_submit").click()
            self.student.find(By.ID, "i_agree").click()
            self.student.find(By.ID, "agreement_submit").click()
        except NoSuchElementException:
            pass
        self.student.driver.switch_to_window(cc_window)
        self.student.sleep(1)
        self.student.find(
            By.XPATH, '//input[@placeholder="enrollment code"]'
        ).send_keys(code1)
        self.student.find(
            By.XPATH, '//button/span[text()="Enroll"]'
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[@class="skip"]')
            )
        ).click()
        # check that enrollemnt code worked, and student is at cc questions
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="task-breadcrumbs"]')
            )
        )
        # enroll in second course
        self.student.get(enrollement_url2)
        self.student.wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Jump to Concept Coach')
            )
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[text()="Launch Concept Coach"]')
            )
        ).click()
        self.student.page.wait_for_page_load()   # check if have to login again
        # self.student.find(
        #     By.XPATH, '//div[text()="Sign in"]'
        # ).click()
        # self.student.sleep(0.5)
        # login_window = self.student.driver.window_handles[1]
        # cc_window = self.student.driver.window_handles[0]
        # self.student.driver.switch_to_window(login_window)
        # self.student.find(
        #     By.ID, 'auth_key').send_keys(rand_username)
        # self.student.find(
        #     By.ID, 'password').send_keys(self.student.password)
        # self.student.find(
        #     By.XPATH, '//button[text()="Sign in"]').click()
        # self.student.driver.switch_to_window(cc_window)
        self.student.sleep(1)
        self.student.find(
            By.XPATH, '//input[@placeholder="enrollment code"]'
        ).send_keys(code2)
        self.student.find(
            By.XPATH, '//button/span[text()="Enroll"]'
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[@class="skip"]')
            )
        ).click()
        # check that enrollemnt code worked, and student is at cc questions
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="task-breadcrumbs"]')
            )
        )

        self.ps.test_updates['passed'] = True

    # Case C7640 - 010- Student | If not logged in, the sign up and sign in
    # widget options are displayed
    @pytest.mark.skipif(str(7640) not in TESTS, reason='Excluded')
    def test_student_if_not_logged_in_sign_up_and_sign_in_widgets_7640(self):
        """If not logged in, the sign up and sign in widget options are displayed.

        Steps:
        Access a Concept Coach book while not logged in
        Click a chapter
        Click a non-introductory section
        Click 'Launch Concept Coach'

        Expected Result:
        The sign up and sign in widgets appear.
        """
        self.ps.test_updates['name'] = 'cc1.07.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.07',
            'cc1.07.010',
            '7640'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        # is it okay to use the url like this
        self.student.get(
            "https://qa.cnx.org/contents/JydfSfIS@2.2:HR_VN3f7@3/" +
            "Introduction-to-Science-and-th")
        # get to non-into section
        self.student.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button//span[text()="Contents"]')
            )
        ).click()
        self.student.sleep(0.5)
        self.student.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//span[@class="chapter-number" and text()="1.1"]')
            )
        ).click()
        # open concept coach
        self.student.wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Jump to Concept Coach')
            )
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[text()="Launch Concept Coach"]')
            )
        ).click()
        # view sign in and sign up buttons
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(text(),"Sign up")]')
            )
        )
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[text()="Sign in"]')
            )
        )
        self.ps.test_updates['passed'] = True

    # Case C7641 - 011- Student | Able to view their name in header sections
    @pytest.mark.skipif(str(7641) not in TESTS, reason='Excluded')
    def test_student_able_to_view_their_name_in_header_sections_7641(self):
        """Able to view their name in the header sections.

        Steps:
        Select a chapter in the table of contents
        Select a section in the table of contents
        Scroll to the bottom of the section
        Click on 'Launch Concept Coach'

        Expected Result:
        The student's name is visible in the header.
        """
        self.ps.test_updates['name'] = 'cc1.07.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.07',
            'cc1.07.011',
            '7641'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        # is it okay to use the url like this
        self.student.get(
            "https://qa.cnx.org/contents/JydfSfIS@2.2:HR_VN3f7@3/" +
            "Introduction-to-Science-and-th")
        # get to non-into section
        self.student.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button//span[text()="Contents"]')
            )
        ).click()
        self.student.sleep(0.5)
        self.student.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//span[@class="chapter-number" and text()="1.1"]')
            )
        ).click()
        # open concept coach
        self.student.wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Jump to Concept Coach')
            )
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[text()="Launch Concept Coach"]')
            )
        ).click()
        # login
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[text()="Sign in"]')
            )
        ).click()
        self.student.sleep(0.5)
        login_window = self.student.driver.window_handles[1]
        cc_window = self.student.driver.window_handles[0]
        self.student.driver.switch_to_window(login_window)
        self.student.find(
            By.ID, 'auth_key').send_keys('student01')
        self.student.find(
            By.ID, 'password').send_keys(self.student.password)
        self.student.find(
            By.XPATH, '//button[text()="Sign in"]').click()
        self.student.driver.switch_to_window(cc_window)
        self.student.sleep(0.5)
        # view name in header
        self.student.find(
            By.XPATH, '//span[contains(text(),"Atticus")]'
        )
        self.ps.test_updates['passed'] = True

    # Case C7642 - 012- Student | Presented the current privacy policy
    # when registering for an account
    @pytest.mark.skipif(str(7642) not in TESTS, reason='Excluded')
    def test_student_presented_the_current_privacy_policy_when_regi_7642(self):
        """Presented the current privacy policy when registering for an account.

        Steps:
        Go to Tutor
        Click Login
        Click "Sign up"
        Click "Sign up with a password"
        Fill out the required fields
        Click "Create Account"
        Click on the checkbox
        Click "I agree"

        Expected Result:
        Current privacy policy is displayed
        """
        self.ps.test_updates['name'] = 'cc1.07.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.07',
            'cc1.07.012',
            '7642'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.get("http://accounts-qa.openstax.org")
        num = str(randint(4000, 4999))
        self.student.find(By.LINK_TEXT, 'Sign up').click()
        self.student.find(
            By.ID, 'identity-login-button').click()
        self.student.find(
            By.ID, 'signup_first_name').send_keys('first_name_001')
        self.student.find(
            By.ID, 'signup_last_name').send_keys('last_name_001')
        self.student.find(
            By.ID, 'signup_email_address').send_keys('email_001@test.com')
        self.student.find(
            By.ID, 'signup_username').send_keys('automated_07_'+num)
        self.student.find(
            By.ID, 'signup_password'
        ).send_keys(os.getenv('STUDENT_PASSWORD'))
        self.student.find(
            By.ID, 'signup_password_confirmation'
        ).send_keys(os.getenv('STUDENT_PASSWORD'))
        self.student.find(
            By.LINK_TEXT, 'Privacy Policy'
        ).click()
        self.student.find(
            By.XPATH, '//div[@id="terms_dialog"]//h3[text()="Privacy Policy"]')
        self.student.find(
            By.XPATH, '//div[@id="terms_dialog"]//button[@class="close"]'
        ).click()
        self.student.find(By.ID, 'signup_i_agree').click()
        self.ps.test_updates['passed'] = True

    # Case C7643 - 013- Student | Presented the current terms of service
    # when registering for an account
    @pytest.mark.skipif(str(7643) not in TESTS, reason='Excluded')
    def test_student_presented_the_current_terms_of_service_when_re_7643(self):
        """Presented the current terms of service when registering for an account.

        Steps:
        Go to Tutor
        Click Login
        Click "Sign up"
        Click "Sign up with a password"
        Fill out the required fields
        Click "Create Account"

        Expected Result:
        Current terms of service are displayed.
        """
        self.ps.test_updates['name'] = 'cc1.07.013' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.07',
            'cc1.07.013',
            '7643'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.get("http://accounts-qa.openstax.org")
        num = str(randint(5000, 5999))
        self.student.find(By.LINK_TEXT, 'Sign up').click()
        self.student.find(
            By.ID, 'identity-login-button').click()
        self.student.find(
            By.ID, 'signup_first_name').send_keys('first_name_001')
        self.student.find(
            By.ID, 'signup_last_name').send_keys('last_name_001')
        self.student.find(
            By.ID, 'signup_email_address').send_keys('email_001@test.com')
        self.student.find(
            By.ID, 'signup_username').send_keys('automated_07_'+num)
        self.student.find(
            By.ID, 'signup_password'
        ).send_keys(os.getenv('STUDENT_PASSWORD'))
        self.student.find(
            By.ID, 'signup_password_confirmation'
        ).send_keys(os.getenv('STUDENT_PASSWORD'))
        self.student.find(By.LINK_TEXT, 'Terms of Use').click()
        self.student.find(
            By.XPATH, '//div[@id="terms_dialog"]//h3[text()="Terms of Use"]')
        self.student.find(
            By.XPATH, '//div[@id="terms_dialog"]//button[@class="close"]'
        ).click()
        self.student.find(By.ID, 'signup_i_agree').click()

        self.ps.test_updates['passed'] = True

    # Case C7644 - 014 - Student | Presented the new privacy policy
    # when the privacy policy is changed
    @pytest.mark.skipif(str(7644) not in TESTS, reason='Excluded')
    def test_student_presented_the_changed_privacy_policy_7644(self):
        """Presented the new privacy policy when the privacy policy is changed.

        Steps:
        Go to Tutor
        Sign in as admin
        Click "Legal"
        Click "Terms"
        Click "New Version" for a privacy policy
        Click "Create"
        Click "Publish"

        Open an incognito window
        Click on the 'Login' button
        Enter the student user account in the username and password text boxes
        Click on the 'Sign in' button

        Expected Result:
        The user is presented with the new privacy policy when the
        privacy policy is changed.
        """
        self.ps.test_updates['name'] = 'cc1.07.014' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.07',
            'cc1.07.014',
            '7644'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.login()
        self.admin.open_user_menu()
        self.admin.find(By.LINK_TEXT, 'Admin').click()
        self.admin.page.wait_for_page_load()
        self.admin.find(By.LINK_TEXT, 'Legal').click()
        self.admin.find(By.LINK_TEXT, 'Terms').click()
        self.admin.page.wait_for_page_load()
        contracts = self.admin.find_all(
            By.XPATH,
            '//div[@class="fine_print contract_index"]/ul'
        )
        for contract in contracts:
            contract_name = contract.find_element(By.XPATH, './li').text
            if contract_name == 'privacy_policy':
                contract.find_element(
                    By.XPATH, './/a[text()="New Version"]'
                ).click()
                break
        self.admin.page.wait_for_page_load()
        self.admin.find(
            By.XPATH, '//input[@name="commit"]'
        ).click()
        self.admin.page.wait_for_page_load()
        self.admin.find(By.LINK_TEXT, 'Publish').click()
        try:
            self.admin.wait. \
                until(
                    expect.alert_is_present(),
                    'Timed out waiting for alert.'
                )
            alert = self.admin.driver.switch_to_alert()
            alert.accept()
            print('alert accepted')
        except TimeoutException:
            print('no alert')
        # logout funtion not working for admin from this page.
        self.admin.find(By.LINK_TEXT, 'Log Out').click()
        self.admin.sleep(1)
        # have to log student in manually, login function accepts policy
        self.student.page.wait_for_page_load()
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
                (By.LINK_TEXT, 'Login')
            )
        ).click()
        self.student.page.wait_for_page_load()
        self.student.find(
            By.ID, 'auth_key').send_keys(self.student.username)
        self.student.find(
            By.ID, 'password').send_keys(self.student.password)
        # click on the sign in button
        self.student.find(
            By.XPATH, '//button[text()="Sign in"]'
        ).click()
        self.student.page.wait_for_page_load()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//h2[text()="Privacy Policy"]')
            )
        )
        self.student.find(By.ID, 'i_agree').click()
        self.student.find(By.ID, 'agreement_submit').click()
        self.ps.test_updates['passed'] = True

    # Case C7645 - 015 - Student | Presented the new terms of service when
    # the terms of service is changed
    @pytest.mark.skipif(str(7645) not in TESTS, reason='Excluded')
    def test_student_presented_the_changed_terms_of_service_7645(self):
        """Presented the new terms of service when the terms of service is changed.

        Steps:
        Go to Tutor
        Sign in as admin
        Click "Legal"
        Click "Terms"
        Click "New Version" for Terms of Use
        Click "Create"
        Click "Publish"
        Open an incognito window
        Click on the 'Login' button
        Enter the student user account in the username and password text boxes
        Click on the 'Sign in' button

        Expected Result:
        The user is presented with the new terms of service when
        the terms of service is changed
        """
        self.ps.test_updates['name'] = 'cc1.07.015' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.07',
            'cc1.07.015',
            '7645'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.login()
        self.admin.open_user_menu()
        self.admin.find(By.LINK_TEXT, 'Admin').click()
        self.admin.page.wait_for_page_load()
        self.admin.find(By.LINK_TEXT, 'Legal').click()
        self.admin.find(By.LINK_TEXT, 'Terms').click()
        self.admin.page.wait_for_page_load()
        contracts = self.admin.find_all(
            By.XPATH,
            '//div[@class="fine_print contract_index"]/ul'
        )
        for contract in contracts:
            contract_name = contract.find_element(By.XPATH, './li').text
            if contract_name == 'general_terms_of_use':
                contract.find_element(
                    By.XPATH, './/a[text()="New Version"]'
                ).click()
                break
        self.admin.page.wait_for_page_load()
        self.admin.find(
            By.XPATH, '//input[@name="commit"]'
        ).click()
        self.admin.page.wait_for_page_load()
        self.admin.find(By.LINK_TEXT, 'Publish').click()
        try:
            self.admin.wait. \
                until(
                    expect.alert_is_present(),
                    'Timed out waiting for alert.'
                )
            alert = self.admin.driver.switch_to_alert()
            alert.accept()
            print('alert accepted')
        except TimeoutException:
            print('no alert')
        # logout funtion not working for admin from this page.
        self.admin.find(By.LINK_TEXT, 'Log Out').click()
        self.admin.sleep(1)
        # have to log student in manually, login function accepts policy
        self.student.page.wait_for_page_load()
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
                (By.LINK_TEXT, 'Login')
            )
        ).click()
        self.student.page.wait_for_page_load()
        self.student.find(
            By.ID, 'auth_key').send_keys(self.student.username)
        self.student.find(
            By.ID, 'password').send_keys(self.student.password)
        # click on the sign in button
        self.student.find(
            By.XPATH, '//button[text()="Sign in"]'
        ).click()
        self.student.page.wait_for_page_load()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//h2[text()="Terms of Use"]')
            )
        )
        self.student.find(By.ID, 'i_agree').click()
        self.student.find(By.ID, 'agreement_submit').click()

        self.ps.test_updates['passed'] = True

    '''
    # Case C7646 - 016 - Student | Re-presented the current privacy policy
    # if not accepted previously
    @pytest.mark.skipif(str(7646) not in TESTS, reason='Excluded')
    def test_student_represented_the_current_privacy_policy_if_not_7646(self):
        """Re-presented the current privacy policy if not accepted previously.

        Steps:
        Go to Tutor
        Click on the 'Login' button
        Click "Sign up"
        Click "Sign up with password"
        Fill out the required fields
        Click "Create Account"
        Click on the checkbox for the terms of use
        Click "I agree"
        Click "Log Out"
        Log back in wth the same username/password

        Expected Result:
        The user is re-presented with the current privacy policy
        """
        self.ps.test_updates['name'] = 'cc1.07.016' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.07',
            'cc1.07.016',
            '7646'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.get("http://accounts-qa.openstax.org")
        num = str(randint(6000, 6999))
        self.student.find(By.LINK_TEXT, 'Sign up').click()
        self.student.find(
            By.ID, 'identity-login-button').click()
        self.student.find(
            By.ID, 'signup_first_name').send_keys('first_name_001')
        self.student.find(
            By.ID, 'signup_last_name').send_keys('last_name_001')
        self.student.find(
            By.ID, 'signup_email_address').send_keys('email_001@test.com')
        self.student.find(
            By.ID, 'signup_username').send_keys('automated_07_'+num)
        self.student.find(
            By.ID, 'signup_password'
        ).send_keys(os.getenv('STUDENT_PASSWORD'))
        self.student.find(
            By.ID, 'signup_password_confirmation'
        ).send_keys(os.getenv('STUDENT_PASSWORD'))
        self.student.find(
            By.LINK_TEXT, 'Privacy Policy'
        ).click()
        self.student.find(
            By.XPATH, '//div[@id="terms_dialog"]//h3[text()="Privacy Policy"]')
        self.student.find(
            By.XPATH, '//div[@id="terms_dialog"]//button[@class="close"]'
        ).click()
        self.student.find(By.ID, 'signup_i_agree').click()

        self.ps.test_updates['passed'] = True
    '''

    '''
    # Case C7647 - 017 - Student | Re-presented the current terms of service
    # if not accepted previously
    @pytest.mark.skipif(str(7647) not in TESTS, reason='Excluded')
    def test_student_represented_the_current_terms_of_service_7647(self):
        """Re-presented current terms of service if not accepted previously.

        Steps:
        Go to Tutor
        Click on the 'Login' button
        Click "Sign up"
        Click "Sign up with password"
        Fill out the required fields
        Click "Create Account"
        Click "Log Out"
        Log back in wth the same username/password

        Expected Result:
        The user is re-presented with the current terms of service
        """
        self.ps.test_updates['name'] = 'cc1.07.017' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.07',
            'cc1.07.017',
            '7647'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.get("http://accounts-qa.openstax.org")
        num = str(randint(7000, 7999))
        self.student.find(By.LINK_TEXT, 'Sign up').click()
        self.student.find(
            By.ID, 'identity-login-button').click()
        self.student.find(
            By.ID, 'signup_first_name').send_keys('first_name_001')
        self.student.find(
            By.ID, 'signup_last_name').send_keys('last_name_001')
        self.student.find(
            By.ID, 'signup_email_address').send_keys('email_001@test.com')
        self.student.find(
            By.ID, 'signup_username').send_keys('automated_07_'+num)
        self.student.find(
            By.ID, 'signup_password'
        ).send_keys(os.getenv('STUDENT_PASSWORD'))
        self.student.find(
            By.ID, 'signup_password_confirmation'
        ).send_keys(os.getenv('STUDENT_PASSWORD'))
        self.student.find(By.LINK_TEXT, 'Terms of Use').click()
        self.student.find(
            By.XPATH, '//div[@id="terms_dialog"]//h3[text()="Terms of Use"]')
        self.student.find(
            By.XPATH, '//div[@id="terms_dialog"]//button[@class="close"]'
        ).click()
        self.student.find(By.ID, 'signup_i_agree').click()

        self.ps.test_updates['passed'] = True
    '''

    # Case C7648 - 018 - Student | Able to edit their OpenStax Accounts profile
    @pytest.mark.skipif(str(7648) not in TESTS, reason='Excluded')
    def test_student_able_to_edit_their_openstax_accounts_profile_7648(self):
        """Able to edit their OpenStax Accounts profile.

        Steps:
        Click the user menu in the right corner of the header
        Click "My Account"

        Expected Result:
        The user is presented with "Your Account" page that allows them to edit
        their OpenStax Accounts profile
        """
        self.ps.test_updates['name'] = 'cc1.07.018' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.07',
            'cc1.07.018',
            '7648'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        # is it okay to use the url like this
        self.student.get(
            "https://qa.cnx.org/contents/JydfSfIS@2.2:HR_VN3f7@3/" +
            "Introduction-to-Science-and-th")
        # get to non-into section
        self.student.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button//span[text()="Contents"]')
            )
        ).click()
        self.student.sleep(0.5)
        self.student.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//span[@class="chapter-number" and text()="1.1"]')
            )
        ).click()
        # open concept coach
        self.student.wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Jump to Concept Coach')
            )
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[text()="Launch Concept Coach"]')
            )
        ).click()
        # login
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[text()="Sign in"]')
            )
        ).click()
        self.student.sleep(0.5)
        login_window = self.student.driver.window_handles[1]
        cc_window = self.student.driver.window_handles[0]
        self.student.driver.switch_to_window(login_window)
        self.student.find(
            By.ID, 'auth_key').send_keys('student01')
        self.student.find(
            By.ID, 'password').send_keys(self.student.password)
        self.student.find(
            By.XPATH, '//button[text()="Sign in"]').click()
        self.student.driver.switch_to_window(cc_window)
        self.student.sleep(0.5)
        # go to profile
        self.student.find(
            By.XPATH, '//span[contains(text(),"Atticus")]'
        ).click()
        self.student.find(
            By.LINK_TEXT, 'Account Profile'
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[contains(@class,"concept-coach-view-profile")]')
            )
        )
        self.ps.test_updates['passed'] = True

    # Case C7650 - 019 - Student |  Registration and login are assistive
    # technology-friendly
    @pytest.mark.skipif(str(7650) not in TESTS, reason='Excluded')
    def test_student_registration_and_login_are_assistive_technolog_7650(self):
        """Registration and login are assistive technology-friendly.

        Steps:
        Signing in:
        Go to Tutor
        Click on the 'Login' button
        Hit the Tab key
        Enter student01 as the username
        Hit the Tab key
        Enter password as the password
        Hit the Enter/Return key

        Registering:
        Go to Tutor
        Click on the 'Login' button
        Click the 'Sign up' button
        Click the 'Sign up with a password' button
        Hit the Tab key
        Enter a first name for the student
        Hit the Tab key
        Enter a last name for the student
        Hit the Tab key
        Enter an email address for the student
        Hit the Tab key
        Enter a username for the student
        Hit the Tab key
        Enter a password for the student
        Hit the Tab key
        Verify the password for the student
        Check the Terms of Service and Privacy Policy Box
        Hit the Tab key until a text box is elected
        Hit the Enter/Return key

        Expected Result:
        The user is successfully logged in or registered.
        """
        self.ps.test_updates['name'] = 'cc1.07.019' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.07',
            'cc1.07.019',
            '7650'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)
        # raise NotImplementedError(inspect.currentframe().f_code.co_name)
        # signing in
        self.student.get('https://tutor-qa.openstax.org')
        self.student.page.wait_for_page_load()
        self.student.sleep(10)

        action = ActionChains(self.student.driver)
        action.send_keys(Keys.TAB + Keys.TAB + Keys.RETURN)
        action.perform()
        self.student.sleep(5)

        # tab_action = ActionChains(self.student.driver)
        # tab_action.send_keys(Keys.TAB)
        # tab_action.perform()
        # tab_action.perform()
        # return_action = ActionChains(self.student.driver)
        # return_action.send_keys(Keys.ENTER)
        # return_action.perform()
        # self.student.sleep(5)
        # enter account information
        # for _ in range(5):
        #     tab_action.perform()
        # name_action = ActionChains(self.student.driver)
        # name_action.send_keys(os.getenv('STUDENT_USER') + Keys.TAB)
        # name_action.perform()
        # password_action = ActionChains(self.student.driver)
        # password_action.send_keys(
        #   os.getenv('STUDENT_PASSWORD') + Keys.RETURN)
        # password_action.perform()
        assert('accounts' in self.student.current_url()), 'not logged in'

        # registering

        self.ps.test_updates['passed'] = True

    # Case C87364 - 020 - Student |  The same social login may be used by more
    # than one account
    @pytest.mark.skipif(str(87364) not in TESTS, reason='Excluded')
    def test_student_the_same_socail_login_may_be_used_by_more_tha_87364(self):
        """The same social login may be used by more than one account.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 'cc1.07.020' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.07',
            'cc1.07.020',
            '87364'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C87365 - 021 - Student |  The same socail login may not be added to
    # the same account twice
    @pytest.mark.skipif(str(87365) not in TESTS, reason='Excluded')
    def test_student_the_same_social_login_may_not_be_added_to_the_87365(self):
        """The same socail login may not be added to the same account twice.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 'cc1.07.021' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.07',
            'cc1.07.021',
            '87365'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
