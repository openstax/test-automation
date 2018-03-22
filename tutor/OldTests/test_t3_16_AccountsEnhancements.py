"""Tutor v3, Epic 16 - AccountsEnhancements."""

import inspect
import json
import os
import pytest
import unittest
# import datetime

from pastasauce import PastaSauce, PastaDecorator
# from random import randint
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as expect
# from staxing.assignment import Assignment
from staxing.helper import Teacher
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.action_chains import ActionChains


basic_test_env = json.dumps([
    {
        'platform': 'Windows 10',
        'browserName': 'chrome',
        'version': 'latest',
        'screenResolution': "1024x768",
    }
])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
LOCAL_RUN = os.getenv('LOCALRUN', 'false').lower() == 'true'
TESTS = os.getenv(
    'CASELIST',
    str([
        # not implemented
        # 105592, 105593, 105594, 105595, 105596,
        # 105597, 105598, 105599, 105600, 105602,
        # 107581, 107586, 107587, 107588, 107589,
        # 107590, 107591, 107592, 107593, 107594
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestAccountEnhancements(unittest.TestCase):
    """T3.16 - Accounts Enhancements."""

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

    # Case C105592 - 001 - Student | Cannot use the same email for more than
    # one account
    @pytest.mark.skipif(str(105592) not in TESTS, reason='Excluded')
    def test_student_cannot_use_the_same_email_for_more_than_one_105592(self):
        """Cannot use the same email for more than one account.

        Steps:
        Create a student account with email and password
        Log out of new account.
        Try to Create another account with the same email

        Expected Result:
        "Email already in use. Are you trying to log in?" message displayed.
        Account cannot be created with the same email.
        """
        self.ps.test_updates['name'] = 't3.16.001' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.16', 't3.16.001', '105592']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C105593 - 002 - Teacher | Cannot use the same email for more than
    # one account
    @pytest.mark.skipif(str(105593) not in TESTS, reason='Excluded')
    def test_teacher_cannot_use_the_same_email_for_more_than_one_105593(self):
        """Cannot use the same email for more than one account.

        Steps:
        Create a teacher account with email and password
        Log out of new account.
        Try to Create another account with the same email

        Expected Result:
        "Email already in use. Are you trying to log in?" message displayed.
        Account cannot be created with the same email.
        """
        self.ps.test_updates['name'] = 't3.16.002' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.16', 't3.16.002', '105593']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C105594 - 003 - Student | Email must be verified
    @pytest.mark.skipif(str(105594) not in TESTS, reason='Excluded')
    def test_student_email_must_be_verified_105594(self):
        """Email must be verified.

        Steps:
        Go to https://accounts-qa.openstax.org/login
        Click the 'Sign up here' link
        Select 'Student' from the 'I am a' drop down menu
        Enter an email into the email text box
        Click 'Next'
        [an email with a pin is sent, log onto email and get pin]
        Enter Pin into text box
        Click 'Confirm'

        Expected Result:
        Email is verified by retrieving the pin.
        Cannot move on in account creation without pin
        """
        self.ps.test_updates['name'] = 't3.16.003' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.16', 't3.16.003', '105594']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C105595 - 004 - Teacher | Email must be verified
    @pytest.mark.skipif(str(105595) not in TESTS, reason='Excluded')
    def test_teacher_email_must_be_verified_105595(self):
        """Email must be verified.

        Steps:
        Go to https://accounts-qa.openstax.org/login
        Click the 'Sign up here' link
        Select 'Instructor' from the 'I am a' drop down menu
        Enter an email into the email text box
        Click 'Next'
        [an email with a pin is sent, log onto email and get pin]
        Enter Pin into text box
        Click 'Confirm'

        Expected Result:
        Email is verified by retrieving the pin.
        Cannot move on in account creation without pin
        """
        self.ps.test_updates['name'] = 't3.16.004' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.16', 't3.16.004', '105595']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C105596 - 005 - Student | Following login the student is shown
    # MyOpenstax
    @pytest.mark.skipif(str(105596) not in TESTS, reason='Excluded')
    def test_student_following_login_student_is_ahown_my_openstax_105596(self):
        """Following login the student is shown MyOpenStax.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 't3.16.005' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.16', 't3.16.005', '105596']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C105597 - 006 - Teacher | Following login the teacher is shown
    # MyOpenstax
    @pytest.mark.skipif(str(105597) not in TESTS, reason='Excluded')
    def test_teacher_following_login_teacher_is_ahown_my_openstax_105597(self):
        """Following login the teacher is shown MyOpenStax.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 't3.16.006' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.16', 't3.16.006', '105597']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C105598 - 007 - Teacher | Accounts stores faculty verification
    @pytest.mark.skipif(str(105598) not in TESTS, reason='Excluded')
    def test_teacher_accounts_stores_faculty_verification_105598(self):
        """Accounts stores faculty verification.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 't3.16.007' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.16', 't3.16.007', '105598']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C105599 - 008 - Student | User must have at least one email
    @pytest.mark.skipif(str(105599) not in TESTS, reason='Excluded')
    def test_student_user_must_have_at_least_one_email_105599(self):
        """User must have at least one email.

        Steps:
        Go to https://accounts-qa.openstax.org/
        Login to an account with one email
        Click on the email

        Expected Result:
        No delete option is available.
        """
        self.ps.test_updates['name'] = 't3.16.008' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.16', 't3.16.008', '105599']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C105600 - 009 - Teacher | User must have at least one email
    @pytest.mark.skipif(str(105600) not in TESTS, reason='Excluded')
    def test_teacher_user_must_have_at_least_one_email_105600(self):
        """User must have at least one email.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 't3.16.009' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.16', 't3.16.009', '105600']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    '''
    # Case C105601 - 010 - Student | Student is alerted during registration if
    # their school ID is already in use
    @pytest.mark.skipif(str(105601) not in TESTS, reason='Excluded')
    def test_student_is_alerted_during_registration_is_their_scho_105601(self):
        """Student is alerted during registration if their school ID is already
        in use.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 't3.16.010' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.16', 't3.16.010', '105601']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
    '''

    # Case C105602 - 011 - Teacher | Account information is sent to Salseforce
    @pytest.mark.skipif(str(105602) not in TESTS, reason='Excluded')
    def test_teacher_account_information_is_sent_to_salesforce_105602(self):
        """Account information is sent to Salseforce.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 't3.16.011' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.16', 't3.16.011', '105602']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C107581 - 012 - Teacher | Reason for requiring additional contact
    # information shown
    @pytest.mark.skipif(str(107581) not in TESTS, reason='Excluded')
    def test_teacher_reason_for_requiring_additional_contact_info_107581(self):
        """Reason for requiring additional contact information shown.

        Steps:
        Go to Accounts
        Start signup for an instructor account
        Proceed until the signup pin is confirmed

        Expected Result:
        Instructor verification is presented
        Current: "We need information to help verify you’re an instructor and
            give you access to materials like test banks and OpenStax Tutor
            course setup."
        """
        self.ps.test_updates['name'] = 't3.16.012' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.16', 't3.16.012', '107581']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C107586 - 013 - Student | Register for an account without a username
    @pytest.mark.skipif(str(107586) not in TESTS, reason='Excluded')
    def test_student_register_for_an_Account_without_a_username_107586(self):
        """Register for an account without a username.

        Steps:
        Go to https://accounts-qa.openstax.org/login
        Click the 'Sign up here' link
        Select 'Student' from the 'I am a' drop down menu
        Enter an email into the email text box
        Click 'Next'
        [an email with a pin is sent, log onto email and get pin]
        Enter Pin into text box
        Click 'Confirm'
        Enter password into password text box
        Re-Enter password in confirm password text box
        Click Submit
        Enter first name into the 'First Name' text box
        Enter last name into the 'Last Name' text box
        Enter school into 'School' text box
        Click checkbox 'I Agree' for the Terms of Use and the Privacy Policy
        Click 'Create Account'
        Click the checkbox and click 'I Agree' for the Terms of Use
        Click the checkbox and click 'I Agree' for the Privacy Policy

        Expected Result:
        Account is created without username. Login only with email
        """
        self.ps.test_updates['name'] = 't3.16.013' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.16', 't3.16.013', '107586']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C107587 - 014 - Admin | Login using a username
    @pytest.mark.skipif(str(107587) not in TESTS, reason='Excluded')
    def test_admin_login_using_a_username_107587(self):
        """Login using a username.

        Steps:
        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the admin username in the username text box
        Click 'Next'
        Enter the admin password in the password text box
        Click on the 'Login' button

        Expected Result:
        User logged in.
        """
        self.ps.test_updates['name'] = 't3.16.014' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.16', 't3.16.014', '107587']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C107588 - 015 - Teacher | Login using a username
    @pytest.mark.skipif(str(107588) not in TESTS, reason='Excluded')
    def test_teacher_login_using_a_username_107588(self):
        """Login using a username.

        Steps:
        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the teacher username in the username text box
        Click 'Next'
        Enter the teacher password in the password text box
        Click on the 'Login' button

        Expected Result:
        User logged in.

        Expected Result:
        """
        self.ps.test_updates['name'] = 't3.16.015' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.16', 't3.16.015', '107588']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C107589 - 016 - Student | Login using a username
    @pytest.mark.skipif(str(107589) not in TESTS, reason='Excluded')
    def test_student_login_using_a_username_107589(self):
        """Login using a username.

        Steps:
        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the student username in the username text box
        Click 'Next'
        Enter the student password in the password text box
        Click on the 'Login' button

        Expected Result:
        User logged in.
        """
        self.ps.test_updates['name'] = 't3.16.016' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.16', 't3.16.016', '107589']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C107590 - 017 - Content Analyst | Login using a username
    @pytest.mark.skipif(str(107590) not in TESTS, reason='Excluded')
    def test_content_analyst_login_using_a_username_107590(self):
        """Login using a username.

        Steps:
        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the content username in the username text box
        Click 'Next'
        Enter the content password in the password text box
        Click on the 'Login' button

        Expected Result:
        User logged in.
        """
        self.ps.test_updates['name'] = 't3.16.017' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.16', 't3.16.017', '107590']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C107591 - 018 - Admin | Login using an email address
    @pytest.mark.skipif(str(107591) not in TESTS, reason='Excluded')
    def test_admin_login_using_an_email_address_107591(self):
        """Login using an email address.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 't3.16.018' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.16', 't3.16.018', '107591']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C107592 - 019 - Teacher | Login using an email address
    @pytest.mark.skipif(str(107592) not in TESTS, reason='Excluded')
    def test_teacher_login_using_an_email_address_107592(self):
        """Login using an email address.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 't3.16.019' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.16', 't3.16.019', '107592']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C107593 - 020 - Student | Login using an email address
    @pytest.mark.skipif(str(107593) not in TESTS, reason='Excluded')
    def test_student_login_using_an_email_address_107593(self):
        """Login using an email address.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 't3.16.020' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.16', 't3.16.020', '107593']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C107594 - 021 - Content Analyst | Login using an email address
    @pytest.mark.skipif(str(107594) not in TESTS, reason='Excluded')
    def test_content_analyst_login_using_an_email_address_107594(self):
        """Login using an email address.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 't3.16.021' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.16', 't3.16.021', '107594']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
