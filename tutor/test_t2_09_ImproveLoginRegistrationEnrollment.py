"""Tutor v2, Epic 9 - Improve Login, Registration, Enrollment."""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
# from random import randint
# from selenium.webdriver.common.by import By
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
LOCAL_RUN = os.getenv('LOCALRUN', 'false').lower() == 'true'
TESTS = os.getenv(
    'CASELIST',
    str([
        14761, 14762, 14763, 14764, 14767,
        14768, 14772, 14773, 14774, 14776,
        14777, 14778, 14779, 14780, 14781,
        14782, 14783, 14784, 14785, 14786,
        14787, 14788, 14789, 14790, 14791,
        14792, 14793, 14794, 14795, 14796,
        85292
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestImproveLoginREgistrationEnrollment(unittest.TestCase):
    """T2.09 - Improve Login, Registration, Enrollment."""

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
        if not LOCAL_RUN:
            self.ps.update_job(
                job_id=str(self.teacher.driver.session_id),
                **self.ps.test_updates
            )
        try:
            self.teacher.delete()
        except:
            pass

    '''
    # C14758 - 001 - User | Create an account that maps to the OS Product I use
    @pytest.mark.skipif(str(14758) not in TESTS, reason='Excluded')
    def test_teacher_view_a_scores_export_for_my_students_work_14758(self):
        """Create an account that maps to the OS Product I use.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.09.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.09',
            't2.09.001',
            '14758'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
    '''

    '''
    # C14760 - 002 - User | Create an openstax.org account and get directed to
    # Concept Coach or Tutor
    @pytest.mark.skipif(str(14760) not in TESTS, reason='Excluded')
    def test_user_create_an_openstax_account_and_get_directed_to_14760(self):
        """Create an openstax.org account and get directed to CC or Tutor.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.09.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.09',
            't2.09.002',
            '14760'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
    '''

    # C14761 - 003 - Teacher | Create a custom URL for student registration
    @pytest.mark.skipif(str(14761) not in TESTS, reason='Excluded')
    def test_teacher_create_a_custom_url_for_student_registration_14761(self):
        """Create a custom URL for student registration.

        Steps:
        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a Tutor course name
        Click "Course Settings and Roster" from the user menu

        Expected Result:
        The user is presented with a custom URL for student registration
        beneath the period tabs
        """
        self.ps.test_updates['name'] = 't2.09.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.09',
            't2.09.003',
            '14761'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # C14762 - 004 - Student | Register for Tutor with a custom URL
    @pytest.mark.skipif(str(14762) not in TESTS, reason='Excluded')
    def test_student_register_for_tutor_with_a_custom_url_14762(self):
        """Register for Tutor with a custom URL.

        Steps:
        Enter the custom URL into the search bar
        Sign in or sign up
        Enter a school-issued ID or skip the step for now

        Expected Result:
        The user is presented with the student dashboard with the message
        "Enrollment successful! It may take a few minutes to build your
        assignments."
        (if student is already enrolled in course message notifies student of
        this)
        """
        self.ps.test_updates['name'] = 't2.09.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.09',
            't2.09.004',
            '14762'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # C14763 - 005 - System | Students have a verified email
    @pytest.mark.skipif(str(14763) not in TESTS, reason='Excluded')
    def test_system_students_have_a_verified_email_14763(self):
        """Student has a verified email.

        Steps:
        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the student account in the username and password text boxes
        Click on the 'Sign in' button
        Click "My Account" from the user menu

        Expected Result:
        There is no "Click to verify" link next to the email
        """
        self.ps.test_updates['name'] = 't2.09.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.09',
            't2.09.005',
            '14763'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # C14764 - 006 - User | Verify email using the new PIN approach
    @pytest.mark.skipif(str(14764) not in TESTS, reason='Excluded')
    def test_user_verify_email_using_the_new_pin_approach_14764(self):
        """Verify email using the new PIN approach.

        Steps:
        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a Tutor course name
        Click "Verify now" on the orange header that pops up
        Enter a 6 digit verification code into the text box from the email
        Click "Go"

        Expected Result:
        A message confirming email verification pops up
        """
        self.ps.test_updates['name'] = 't2.09.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.09',
            't2.09.006',
            '14764'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # C14767 - 007 - Teacher | Register for teaching a Tutor course as new
    # faculty
    @pytest.mark.skipif(str(14767) not in TESTS, reason='Excluded')
    def test_teacher_register_for_teaching_a_tutor_course_as_new_14767(self):
        """Register for teaching a Tutor course as new faculty.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.09.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.09',
            't2.09.007',
            '14767'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # C14768 - 008 - Teacher | Register for teaching a Tutor course as
    # returning faculty
    @pytest.mark.skipif(str(14768) not in TESTS, reason='Excluded')
    def test_teacher_register_for_teaching_a_tutor_course_as_retur_14768(self):
        """Register for teaching a Tutor course as returning faculty.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.09.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.09',
            't2.09.008',
            '14768'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # C14772 - 009 - Student | Agree to join or drop from each research
    # protocol that is running in my course
    @pytest.mark.skipif(str(14772) not in TESTS, reason='Excluded')
    def test_student_agree_to_join_or_drop_from_each_research_14772(self):
        """Agree to join or drop from each research protocol.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.09.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.09',
            't2.09.009',
            '14772'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # C14773 - 010 - Researcher | Gather electronic parental consent for minors
    @pytest.mark.skipif(str(14773) not in TESTS, reason='Excluded')
    def test_researcher_gather_electronic_parental_consent_from_mi_14773(self):
        """Gather electronic parental consent from minors.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.09.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.09',
            't2.09.010',
            '14773'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # C14774 - 011 - Admin | Gather electronic parental consent from minors
    @pytest.mark.skipif(str(14774) not in TESTS, reason='Excluded')
    def test_admin_gather_electronic_parental_consent_from_minors_14774(self):
        """Gather electronic parental consent from minors.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.09.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.09',
            't2.09.011',
            '14774'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # C14776 - 012 - Researcher | Enable/Disable 'ask me later' for consent
    @pytest.mark.skipif(str(14776) not in TESTS, reason='Excluded')
    def test_researcher_enable_or_disable_ask_me_later_for_consent_14776(self):
        """Enable/Disable 'ask me later' for consent.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.09.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.09',
            't2.09.012',
            '14776'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # C14777 - 013 - Admin | Enable/Disable 'ask me later' for consent
    @pytest.mark.skipif(str(14777) not in TESTS, reason='Excluded')
    def test_admin_enable_or_disable_ask_me_later_for_consent_14777(self):
        """Enable/Disable 'ask me later' for consent.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.09.013' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.09',
            't2.09.013',
            '14777'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # C14778 - 014 - Researcher | Reprompt 'ask me later' to students on a
    # schedule
    @pytest.mark.skipif(str(14778) not in TESTS, reason='Excluded')
    def test_researcher_reprompt_ask_me_later_to_students_on_a_sch_14778(self):
        """Reprompt 'ask me later' to students on a schedule.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.09.014' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.09',
            't2.09.014',
            '14778'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # C14779 - 015 - Admit | Reprompt 'ask me later' to students on a
    # schedule
    @pytest.mark.skipif(str(14779) not in TESTS, reason='Excluded')
    def test_admin_reprompt_ask_me_later_to_students_on_a_schedule_14779(self):
        """Reprompt 'ask me later' to students on a schedule.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.09.015' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.09',
            't2.09.015',
            '14779'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # C14780 - 016 - Student | Reprompt 'ask me later' by pressing a button
    @pytest.mark.skipif(str(14780) not in TESTS, reason='Excluded')
    def test_student_reprompt_ask_me_later_by_pressing_a_button_14780(self):
        """Reprompt 'ask me later' by pressing a button.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.09.016' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.09',
            't2.09.016',
            '14780'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # C14781 - 017 - Researcher | View number of students who have opted-in,
    # opted-out, ask-me-later
    @pytest.mark.skipif(str(14781) not in TESTS, reason='Excluded')
    def test_researcher_view_number_of_students_who_have_opted_in_14781(self):
        """View number of students who have opted-in, opted-out.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.09.017' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.09',
            't2.09.017',
            '14781'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # C14782 - 018 - Admin | View number of students who have opted-in,
    # opted-out, ask-me-latered
    @pytest.mark.skipif(str(14782) not in TESTS, reason='Excluded')
    def test_admin_view_number_of_students_who_have_optedin_14782(self):
        """View number of students who have opted-in, opted-out.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.09.018' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.09',
            't2.09.018',
            '14782'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # C14783 - 019 -  Researcher | Apply one protocol to multiple courses
    @pytest.mark.skipif(str(14783) not in TESTS, reason='Excluded')
    def test_researcher_apply_one_protocol_to_multiple_courses_14783(self):
        """Apply one protocol to multiple courses.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.09.019' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.09',
            't2.09.019',
            '14783'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # C14784 - 020 -  Admin | Apply one protocol to multiple courses
    @pytest.mark.skipif(str(14784) not in TESTS, reason='Excluded')
    def test_admin_apply_one_protocol_to_multiple_courses_14784(self):
        """Apply one protocol to multiple courses.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.09.020' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.09',
            't2.09.020',
            '14784'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # C14785 - 021 - Researcher | Set time bounds on when students can be asked
    # for consent
    @pytest.mark.skipif(str(14785) not in TESTS, reason='Excluded')
    def test_researcher_set_time_bounds_on_when_students_can_be_as_14785(self):
        """Set time bounds on when students can be asked for consent.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.09.021' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.09',
            't2.09.021',
            '14785'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # C14786 - 022 - Admin | Set time bounds on when students can be asked
    # for consent
    @pytest.mark.skipif(str(14786) not in TESTS, reason='Excluded')
    def test_admin_set_time_bounds_on_when_students_can_be_asked_14786(self):
        """Set time bounds on when students can be asked for consent.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.09.022' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.09',
            't2.09.022',
            '14786'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # C14787 - 023 - Researcher | Set if a protocol requires an e-signature
    @pytest.mark.skipif(str(14787) not in TESTS, reason='Excluded')
    def test_researcher_set_if_a_protocol_requires_an_esignature_14787(self):
        """Set if a protocol requires an e-signature.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.09.023' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.09',
            't2.09.023',
            '14787'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # C14788 - 024 -  Admin | Set if a protocol requires an e-signature
    @pytest.mark.skipif(str(14788) not in TESTS, reason='Excluded')
    def test_admin_set_if_a_protocol_requires_an_esignature_14788(self):
        """Set if a protocol requires an e-signature.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.09.024' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.09',
            't2.09.024',
            '14788'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # C14789 - 025 - User | Reset password with an unverified email address
    @pytest.mark.skipif(str(14789) not in TESTS, reason='Excluded')
    def test_user_reset_password_with_an_unverified_email_address_14789(self):
        """Reset password with an unverified email address.

        Steps:
        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter any user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a Tutor course name
        Click "My Account" from the user menu
        Click on the pencil next to the password
        Enter a new password
        Click the checkmark

        Expected Result:
        The user is presented with the message that confirms password change
        """
        self.ps.test_updates['name'] = 't2.09.025' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.09',
            't2.09.025',
            '14789'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # C14790 - 026 - User | Disable login for X minutes after Y unsuccessful
    # login attempts
    @pytest.mark.skipif(str(14790) not in TESTS, reason='Excluded')
    def test_user_disable_login_for_x_minutes_after_y_unsuccessful_14790(self):
        """Disable login for X minutes after Y unsuccessful login attempts.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.09.026' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.09',
            't2.09.026',
            '14790'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # C14791 - 027 - Security | Rate limit login URLs based on IP address
    @pytest.mark.skipif(str(14791) not in TESTS, reason='Excluded')
    def test_security_rate_limit_login_urls_based_on_ip_address_14791(self):
        """Rate limit login URLs based on IP address.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.09.027' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.09',
            't2.09.027',
            '14791'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # C14792 - 028 - Security | Require recent login when adding/changing
    # authentications
    @pytest.mark.skipif(str(14792) not in TESTS, reason='Excluded')
    def test_security_require_recent_login_when_adding_or_changing_14792(self):
        """Require recent login when adding/changing authentications.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.09.028' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.09',
            't2.09.028',
            '14792'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # C14793 - 029 - Security | Deactivate accounts with no courses
    @pytest.mark.skipif(str(14793) not in TESTS, reason='Excluded')
    def test_security_deactivate_accounts_with_no_courses_14793(self):
        """Deactivate accounts with no courses.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.09.029' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.09',
            't2.09.029',
            '14793'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # C14794 - 030 - Security | Log out Accounts admins after X mins of
    # inactivity
    @pytest.mark.skipif(str(14794) not in TESTS, reason='Excluded')
    def test_security_log_out_accounts_admins_after_x_mins_of_inac_14794(self):
        """Log out Accounts admins after X mins of inactivity.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.09.030' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.09',
            't2.09.030',
            '14794'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # C14795 - 031 - Admin | Register faculty for Tutor using the CC method
    @pytest.mark.skipif(str(14795) not in TESTS, reason='Excluded')
    def test_admin_register_faculty_for_tutor_using_the_cc_method_14795(self):
        """Register faculty for Tutor using the Concept Coach method.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.09.031' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.09',
            't2.09.031',
            '14795'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # C14796 - 032 - Teacher | Correct a student ID
    @pytest.mark.skipif(str(14796) not in TESTS, reason='Excluded')
    def test_teacher_correct_a_student_id_14796(self):
        """Correct a student ID.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.09.032' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.09',
            't2.09.032',
            '14796'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # C85292 - 033 - Student | Change user ID
    @pytest.mark.skipif(str(85292) not in TESTS, reason='Excluded')
    def test_student_change_user_id_85292(self):
        """Change user ID.

        Steps:
        Login as a student.
        Click on the student name
        From the dropdown menu click on my account
        In the new tab that opened, modify the username.
        Logout
        Login with the new username

        Expected Result:
        Able to modify the username and login successfully with it
        """
        self.ps.test_updates['name'] = 't2.09.033' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.09',
            't2.09.033',
            '85292'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
