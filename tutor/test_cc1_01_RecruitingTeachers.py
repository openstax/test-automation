"""Concept Coach v1, Epic 1 - Recruiting Teachers."""

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
    'version': '50.0',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([
        7751, 7752, 7753, 7754, 7755,
        7756, 7757, 7758, 7759, 7760,
        7761, 7762, 7763, 7764, 7765,
        7770, 7771, 7772, 7773, 7774,
        7775
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestRecruitingTeachers(unittest.TestCase):
    """CC1.01 - Recruiting Teachers."""

    def setUp(self):
        """Pretest settings."""
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.teacher = Teacher(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )

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

    # Case C7751 - 001 - Admin | Recruitment and promo website is available
    @pytest.mark.skipif(str(7751) not in TESTS, reason='Excluded')
    def test_admin_recruitment_and_promo_website_is_available_7751(self):
        """Recruitment and promo website is available.

        Steps:
        Go to the recruitment website ( http://cc.openstax.org/ )

        Expected Result:
        Recruitment website loads and renders
        """
        self.ps.test_updates['name'] = 'cc1.01.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.01',
            'cc1.01.001',
            '7751'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7752 - 002 - Teacher | Information about Concept Coach and the
    # pilot are available on the demo site
    @pytest.mark.skipif(str(7752) not in TESTS, reason='Excluded')
    def test_teacher_information_about_cc_is_available_on_demo_site_7752(self):
        """Information about CC and pilot are available on the demo site.

        Steps:
        Go to the recruitment website ( http://cc.openstax.org/ )

        Expected Result:
        Page loads several sections describing Concept Coach
        """
        self.ps.test_updates['name'] = 'cc1.01.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.01',
            'cc1.01.002',
            '7752'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7753 - 003 - Teacher | Can interact with a Concept Coach wire frame
    # for each subject
    @pytest.mark.skipif(str(7753) not in TESTS, reason='Excluded')
    def test_teacher_can_interact_with_a_cc_wire_frame_for_subjects_7753(self):
        """Can interact with a Concept Coach wire frame for each subject.

        Steps:
        Go to the recruitment website ( http://cc.openstax.org/)
        Hover over "demos" in the header
        Click "Interactice Demo"
        CLick on a Concept Coach book title

        Expected Result:
        A new tab or window opens rendering the demo content for the selected
        book
        """
        self.ps.test_updates['name'] = 'cc1.01.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.01',
            'cc1.01.003',
            '7753'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7754 - 004 - Teacher | View a Concept Coach demo video
    @pytest.mark.skipif(str(7754) not in TESTS, reason='Excluded')
    def test_teacher_view_a_concept_coach_demo_video_7754(self):
        """View a Concept Coach demo video.

        Steps:
        Open recruitment website ( http://cc.openstax.org/ )
        Hover over "demos" in the header
        Click "Interactive Demo"
        Click on a Concept Coach book title
        Scroll down until an embedded video pane is displayed
        Click on the right-pointing arrow to play the video

        Expected Result:
        The video loads and plays
        """
        self.ps.test_updates['name'] = 'cc1.01.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.01',
            'cc1.01.004',
            '7754'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7755 - 005 - Teacher | Sample exercise questions are seen in
    # the wire frames
    @pytest.mark.skipif(str(7755) not in TESTS, reason='Excluded')
    def test_teacher_sample_exercise_questions_are_in_wire_frames_7755(self):
        """Sample exercise questions are seen in the wire frames.

        Steps:
        Open recruitment website ( http://cc.openstax.org/ )
        Hover over "demos" in the header
        Click "Interactive Demo"
        Click on a Concept Coach book title
        Scroll down until the 'CONCEPT COACH' pane is displayed

        Expected Result:
        Demo exercises are rendered and can be answered along with showing
        feedback
        """
        self.ps.test_updates['name'] = 'cc1.01.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.01',
            'cc1.01.005',
            '7755'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7756 - 006 - Teacher | Access Concept Coach help and support before
    # the teacher's course is created
    @pytest.mark.skipif(str(7756) not in TESTS, reason='Excluded')
    def test_teacher_access_cc_support_before_course_is_created_7756(self):
        """Access CC help and support before the teacher's course is created.

        Steps:
        Open the recruitment website ( http://cc.openstax.org/ )
        Click "Support" in the header

        Expected Result:
        A new tab opens with the CC Help Center
        """
        self.ps.test_updates['name'] = 'cc1.01.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.01',
            'cc1.01.006',
            '7756'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7757 - 007 - Teacher | Teacher registers to use a CC course
    @pytest.mark.skipif(str(7757) not in TESTS, reason='Excluded')
    def test_teacher_teacher_registers_to_use_a_cc_course_7757(self):
        """Teacher registers to use a Concept Coach course.

        Steps:
        Go to the recruitment website ( http://cc.openstax.org )
        Click on the 'sign up now' button

        Expected Result:
        Web form renders
        """
        self.ps.test_updates['name'] = 'cc1.01.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.01',
            'cc1.01.007',
            '7757'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7758 - 008 - Teacher | Teacher uses a web form to sign up for CC
    @pytest.mark.skipif(str(7758) not in TESTS, reason='Excluded')
    def test_teacher_teacher_uses_a_web_form_to_sign_up_for_cc_7758(self):
        """Teacher uses a web form to sign up for Concept Coach.

        Steps:
        Teacher fills out the form

        Expected Result:
        Preconditions pass.
        User is presented with a confirmation message
        """
        self.ps.test_updates['name'] = 'cc1.01.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.01',
            'cc1.01.008',
            '7758'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7759 - 009 - Teacher | Receive error messages if required fields on
    # the sign up form are blank
    @pytest.mark.skipif(str(7759) not in TESTS, reason='Excluded')
    def test_teacher_receive_error_messages_if_required_fields_are_7759(self):
        """Receive error messages if required fields on the sign up form are blank.

        Steps:
        Go to the recruitment website ( http://cc.openstax.org/ )
        Click on the 'sign up now' button
        Submit the form without changing any of the text fields

        Expected Result:
        Receive 'Please fill out this field' error messages in red for
        each blank required field
        """
        self.ps.test_updates['name'] = 'cc1.01.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.01',
            'cc1.01.009',
            '7759'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7760 - 010 - Teacher | Submit a form to supply required course info
    @pytest.mark.skipif(str(7760) not in TESTS, reason='Excluded')
    def test_teacher_submit_a_form_to_supply_required_course_info_7760(self):
        """Submit a form to supply required course information.

        Steps:
        Go to the recruitment website ( http://cc.openstax.org )
        Click on the 'sign up now' button
        Fill out the intent to participate form
        Submit the form

        Expected Result:
        Web form submits
        Displays a Thank you message panel
        """
        self.ps.test_updates['name'] = 'cc1.01.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.01',
            'cc1.01.010',
            '7760'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7761 - 011 - Teacher | Submit co-instructors, classes, names, etc.
    @pytest.mark.skipif(str(7761) not in TESTS, reason='Excluded')
    def test_teacher_submit_coinstructors_classes_names_etc_7761(self):
        """Submit co-instructors, classes, names and other data.

        Steps:
        Go to the recruitment and promo website ( http://cc.openstax.org/ )
        Click on the 'sign up now' button
        Click on the 'Co-Teaching class with a colleague?' circle button
        Enter the co-instructor's (or co-instructors') information
        Enter text into other fields concerning classe, names, etc.

        Expected Result:
        Input box exists for instructor information, class details and
        other data.
        The user is able to input information.
        """
        self.ps.test_updates['name'] = 'cc1.01.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.01',
            'cc1.01.011',
            '7761'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7762 - 012 - Teacher | Select the textbook to use in the course
    @pytest.mark.skipif(str(7762) not in TESTS, reason='Excluded')
    def test_teacher_select_the_textbook_to_use_in_the_course_7762(self):
        """Select the textbook to use in the course.

        Steps:
        Go to the recruitment website ( http://cc.openstax.org )
        Click on the 'sign up now' button
        Select the course textbook from the 'Book' dropdown options

        Expected Result:
        Able to select any Concept Coach textbook
        """
        self.ps.test_updates['name'] = 'cc1.01.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.01',
            'cc1.01.012',
            '7762'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7763 - 013 - Teacher | Indicate whether the teacher was recruited
    # by OpenStax
    @pytest.mark.skipif(str(7763) not in TESTS, reason='Excluded')
    def test_teacher_indicate_whether_the_teacher_was_recruited_by_7763(self):
        """Indicate if the teacher was or was not recruited by OpenStax.

        Steps:
        Go to the recruitment and promo website ( http://cc.openstax.org/ )
        Click on the 'sign up now' button ( http://cc.openstax.org/sign-up )
        Enter recruitment information into the 'Anything else we need to know?'
        text box

        Expected Result:
        Able to input recruitment information
        """
        self.ps.test_updates['name'] = 'cc1.01.013' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.01',
            'cc1.01.013',
            '7763'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7764 - 014 - Teacher | Presented a thank you page after registering
    # to use Concept Coach
    @pytest.mark.skipif(str(7764) not in TESTS, reason='Excluded')
    def test_teacher_presented_a_thank_you_page_after_registering_7764(self):
        """Presented a thank you page after registering to use Concept Coach.

        Steps:
        Go to the recruitment website ( http://cc.openstax.org )
        Click on the 'sign up now' button
        Fill out the intent to participate form
        Submit the form

        Expected Result:
        Displays a Thank you message panel
        """
        self.ps.test_updates['name'] = 'cc1.01.014' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.01',
            'cc1.01.014',
            '7764'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7765 - 015 - Teacher | Sign up for an OpenStax Accounts username
    @pytest.mark.skipif(str(7765) not in TESTS, reason='Excluded')
    def test_teacher_sign_up_for_an_openstax_accounts_username_7765(self):
        """Sign up for an OpenStax Accounts username.

        Steps:
        Go to the recruitment website ( http://cc.openstax.org )
        Click on the 'sign up now' button
        Fill out the intent to participate form
        Submit the form

        Expected Result:
        Displays a Thank you message panel
        """
        self.ps.test_updates['name'] = 'cc1.01.015' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.01',
            'cc1.01.015',
            '7765'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7770 - 020 - Admin | Add co-instructors to a course
    @pytest.mark.skipif(str(7770) not in TESTS, reason='Excluded')
    def test_admin_add_coinstructors_to_a_course_7770(self):
        """Add co-instructors to a course.

        Steps:
        Log into Tutor as an admin (admin : password)
        From the user menu, select 'Admin'
        From the 'Course Organization' menu, select 'Courses'
        In the Courses table, find the correct course and click the 'Edit'
            button on the right side of that row
        Click on the 'Teachers' tab
        In the search box, enter the teacher's name or username
        Select the teacher in the list below the search bar or hit the down
            arrow followed by the enter/return key

        Expected Result:
        Co-instructor is linked to the affected course
        """
        self.ps.test_updates['name'] = 'cc1.01.020' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.01',
            'cc1.01.020',
            '7770'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7771 - 021 - Teacher | Login with an Existing OpenStax Account
    @pytest.mark.skipif(str(7771) not in TESTS, reason='Excluded')
    def test_teacher_login_with_an_existing_openstax_account_7771(self):
        """Log in with an Existing OpenStax Accounts username.

        Steps:
        Go to the recruitment website ( http://cc.openstax.org/ )
        Click on faculty login
        You are redirected to the accounts page.
        Enter a username and password
        click on Login.

        Expected Result:
        Login should be successful. It should take you to the teacher course
        picker/dashboard page.
        """
        self.ps.test_updates['name'] = 'cc1.01.021' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.01',
            'cc1.01.021',
            '7771'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7772 - 022 - Teacher | Access the Concept Coach course
    @pytest.mark.skipif(str(7772) not in TESTS, reason='Excluded')
    def test_teacher_access_the_cc_course_7772(self):
        """Access the Concept Coach course.

        Steps:
        Once you login you will be taken to a course picker page.
        Click on the course you want to check the dashboard

        Expected Result:
        At Concept Coach teacher dashboard
        """
        self.ps.test_updates['name'] = 'cc1.01.022' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.01',
            'cc1.01.022',
            '7772'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7773 - 023 - Teacher | Distribute access codes for the course
    @pytest.mark.skipif(str(7773) not in TESTS, reason='Excluded')
    def test_teacher_distribute_access_codes_for_the_course_7773(self):
        """Distribute access codes for the teacher's course.

        Steps:
        CC approves a faculty.
        Login as admin [admin | password]
        Click on user menu
        Click on Admin
        Click on Salesforce tab
        Click on import [Do not check the box]
        This will automatically create a course for the teacher created.
        Email is sent to the email id used when signing up with
            the unique course URL.

        Expected Result:
        Instructors are emailed the unique course url to the address provided
        when they signed up.
        """
        self.ps.test_updates['name'] = 'cc1.01.023' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.01',
            'cc1.01.023',
            '7773'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7774 - 024 - Teacher | Access CC help and support during the course
    @pytest.mark.skipif(str(7774) not in TESTS, reason='Excluded')
    def test_teacher_acccess_cc_help_and_support_during_the_course_7774(self):
        """Access Concept Coach help and support during the course.

        Steps:
        Login as teacher
        Click on the course name
        On dashboard click on the name of the teacher
        It drops down and displays several options.
        Click on Get Help

        Expected Result:
        It should open a new tab which shows the openstax.force.com
        """
        self.ps.test_updates['name'] = 'cc1.01.024' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.01',
            'cc1.01.024',
            '7774'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7775 - 025 - Teacher | Access CC help and support after course ends
    @pytest.mark.skipif(str(7775) not in TESTS, reason='Excluded')
    def test_teacher_access_cc_help_and_support_after_course_ends_7775(self):
        """Access Concept Coach help and support after the end of the course.

        Steps:
        Login as teacher
        Click on the course name
        On dashboard click on the name of the teacher
        It drops down and displays several options.
        Click on Get Help

        Expected Result:
        It should open a new tab which shows the openstax.force.com
        """
        self.ps.test_updates['name'] = 'cc1.01.025' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.01',
            'cc1.01.025',
            '7775'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
