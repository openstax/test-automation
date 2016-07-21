"""Concept Coach v1, Epic 7.

Student Registration, Enrollment, Login, and Authentification.
"""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
from random import randint  # NOQA
from selenium.webdriver.common.by import By  # NOQA
from selenium.webdriver.support import expected_conditions as expect  # NOQA
from staxing.assignment import Assignment  # NOQA

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Student, Teacher  # NOQA

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': '50.0',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([7631, 7632, 7633, 7634,
         7635, 7636, 7637, 7638,
         7639, 7640, 7641, 7642,
         7643, 7644, 7645, 7646,
         7647, 7648, 7650])  # NOQA
)


@PastaDecorator.on_platforms(BROWSERS)
class TestStudentRegistrationEnrollmentLoginAuthentificatio(unittest.TestCase):
    """CC1.07 - Student Registration, Enrollment, Login and Authentication."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.Teacher = Teacher(
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

    # Case C7631 - 001 - Student | Register for a class using a provided
    # registration code - non-social login
    @pytest.mark.skipif(str(7631) not in TESTS, reason='Excluded')  # NOQA
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

        self.ps.test_updates['passed'] = True

    # Case C7632 - 002 - Student | Register for a class using a provided
    # registration code - Facebook login
    @pytest.mark.skipif(str(7632) not in TESTS, reason='Excluded')  # NOQA
    def test_student_register_for_a_class_using_a_provided_registra_7632(self):
        """Register for a class using a provided registration code - Facebook login.

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

        self.ps.test_updates['passed'] = True

    # Case C7633 - 003 - Student | Register for a class using a provided
    # registration code - Twitter login
    @pytest.mark.skipif(str(7633) not in TESTS, reason='Excluded')  # NOQA
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

        self.ps.test_updates['passed'] = True

    # Case C7634 - 004 - Student | Register for a class using a provided
    # registration code - Google login
    @pytest.mark.skipif(str(7634) not in TESTS, reason='Excluded')  # NOQA
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

        self.ps.test_updates['passed'] = True

    # Case C7635 - 005 - Student | After registering the user is shown a
    # confirmation message
    @pytest.mark.skipif(str(7635) not in TESTS, reason='Excluded')  # NOQA
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

        self.ps.test_updates['passed'] = True

    # Case C7636 - 006 - Student | After a failed registration the user
    # is shown an error message
    @pytest.mark.skipif(str(7636) not in TESTS, reason='Excluded')  # NOQA
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

        self.ps.test_updates['passed'] = True

    # Case C7637 - 007 - Student | Able to change to another course
    @pytest.mark.skipif(str(7637) not in TESTS, reason='Excluded')  # NOQA
    def test_student_able_to_change_to_another_course_7637(self):
        """Able to change to another course.

        Steps:

        Sign in as teacher100
        Click on a different Concept Coach course
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

        The student is in a new course.
        The student is presented with a confirmation message and CC questions


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

        self.ps.test_updates['passed'] = True

    # Case C7638 - 008 - Student | Able to change period in the same course
    @pytest.mark.skipif(str(7638) not in TESTS, reason='Excluded')  # NOQA
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

        self.ps.test_updates['passed'] = True

    # Case C7639 - 009- Student | Able to enroll in more than one CC course
    @pytest.mark.skipif(str(7639) not in TESTS, reason='Excluded')  # NOQA
    def test_student_able_to_enroll_in_more_than_one_cc_course_7639(self):
        """Able to enroll in more than one Concept Coach course.

        Steps:

        Access a Concept Coach book that the student is not enrolled in
        Access Chapter 1 Section 1 of the book
        Click on 'Launch Concept Coach'
        Enter the course code in the text box labeled 'enrollment code'
        Click 'Enroll'
        Click 'Confirm'


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

        self.ps.test_updates['passed'] = True

    # Case C7640 - 010- Student | If not logged in, the sign up and sign in
    # widget options are displayed
    @pytest.mark.skipif(str(7640) not in TESTS, reason='Excluded')  # NOQA
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

        self.ps.test_updates['passed'] = True

    # Case C7641 - 011- Student | Able to view their name in header sections
    @pytest.mark.skipif(str(7641) not in TESTS, reason='Excluded')  # NOQA
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

        self.ps.test_updates['passed'] = True

    # Case C7642 - 012- Student | Presented the current privacy policy
    # when registering for an account
    @pytest.mark.skipif(str(7642) not in TESTS, reason='Excluded')  # NOQA
    def test_student_presented_the_current_privacy_policy_when_regi_7642(self):
        """Presented the current privacy policy when registering for an account.

        Steps:

        Go to tutor-qa
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

        self.ps.test_updates['passed'] = True

    # Case C7643 - 013- Student | Presented the current terms of service
    # when registering for an account
    @pytest.mark.skipif(str(7643) not in TESTS, reason='Excluded')  # NOQA
    def test_student_presented_the_current_terms_of_service_when_re_7643(self):
        """Presented the current terms of service when registering for an account.

        Steps:

        Go to tutor-qa
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

        self.ps.test_updates['passed'] = True

    # Case C7644 - 014 - Student | Presented the new privacy policy
    # when the privacy policy is changed
    @pytest.mark.skipif(str(7644) not in TESTS, reason='Excluded')  # NOQA
    def test_student_presented_the_changed_privacy_policy_7644(self):
        """Presented the new privacy policy when the privacy policy is changed.

        Steps:

        Go to https://tutor-qa.openstax.org/
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

        self.ps.test_updates['passed'] = True

    # Case C7645 - 015 - Student | Presented the new terms of service when
    # the terms of service is changed
    @pytest.mark.skipif(str(7645) not in TESTS, reason='Excluded')  # NOQA
    def test_student_presented_the_changed_terms_of_service_7645(self):
        """Presented the new terms of service when the terms of service is changed.

        Steps:

        Go to https://tutor-qa.openstax.org/
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

        self.ps.test_updates['passed'] = True

    # Case C7646 - 016 - Student | Re-presented the current privacy policy
    # if not accepted previously
    @pytest.mark.skipif(str(7646) not in TESTS, reason='Excluded')  # NOQA
    def test_student_represented_the_current_privacy_policy_if_not_7646(self):
        """Re-presented the current privacy policy if not accepted previously.

        Steps:

        Go to https://tutor-qa.openstax.org/
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

        self.ps.test_updates['passed'] = True

    # Case C7647 - 017 - Student | Re-presented the current terms of service
    # if not accepted previously
    @pytest.mark.skipif(str(7647) not in TESTS, reason='Excluded')  # NOQA
    def test_student_represented_the_current_terms_of_service_7647(self):
        """Re-presented the current terms of service if not accepted previously.

        Steps:

        Go to https://tutor-qa.openstax.org/
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

        self.ps.test_updates['passed'] = True

    # Case C7648 - 018 - Student | Able to edit their OpenStax Accounts profile
    @pytest.mark.skipif(str(7648) not in TESTS, reason='Excluded')  # NOQA
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

        self.ps.test_updates['passed'] = True

    # Case C7650 - 019 - Student |  Registration and login are assistive
    # technology-friendly
    @pytest.mark.skipif(str(7650) not in TESTS, reason='Excluded')  # NOQA
    def test_student_registration_and_login_are_assistive_technolog_7650(self):
        """Registration and login are assistive technology-friendly.

        Steps:

        Signing in:

        Go to https://tutor-staging.openstax.org/
        Click on the 'Login' button
        Hit the Tab key
        Enter student01 as the username
        Hit the Tab key
        Enter password as the password
        Hit the Enter/Return key

        Registering:

        Go to https://tutor-staging.openstax.org/
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

        self.ps.test_updates['passed'] = True