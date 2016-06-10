"""Concept Coach v1, Epic 1 - Recruiting Teachers."""

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
from staxing.helper import Admin, Teacher  # NOQA

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': '50.0',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([7751, 7752, 7753, 7754, 7755,
         7756, 7757, 7758, 7759, 7760,
         7761, 7762, 7763, 7764, 7765,
         7766, 7767, 7770, 7771, 7772, 
         7773, 7774, 7775])  # NOQA
)


@PastaDecorator.on_platforms(BROWSERS)
class TestEpicName(unittest.TestCase):
    """CC1.01 - Recruiting Teachers."""

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

    # Case C7751 - 001 - Admin | Recruitment and promo website is available 
    @pytest.mark.skipif(str(7751) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
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

        self.ps.test_updates['passed'] = True


    # Case C7752 - 002 - Teacher | Information about Concept Coach and the pilot are available on the demo site
    @pytest.mark.skipif(str(7752) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Information about Concept Coach and the pilot are available on the demo site.

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

        self.ps.test_updates['passed'] = True


    # Case C7753 - 003 - Teacher | Can interact with a Concept Coach wire frame for each subject
    @pytest.mark.skipif(str(7753) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Can interact with a Concept Coach wire frame for each subject.

        Steps: 

        Go to the recruitment website ( http://cc.openstax.org/)
        Click on the 'demo' link in the header OR scroll down until 'Interactive Demos' is displayed
        Click on a Concept Coach book title

        Expected Result:

        A new tab or window opens rendering the demo content for the selected book

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

        self.ps.test_updates['passed'] = True


    # Case C7754 - 004 - Teacher | View a Concept Coach demo video
    @pytest.mark.skipif(str(7754) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """View a Concept Coach demo video.

        Steps: 

        Open recruitment website ( http://cc.openstax.org/ )
        Click on the 'demo' link in the header OR scroll down until 'Interactive Demos' is displayed
        Click on a Concept Coach book title
        Scroll down until an embedded video pane is displayed
        Click on the right-pointing arrow to play the video


        Expected Result:

        The video loads and plays

        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)


    # Case C7755 - 005 - Teacher | Sample exercise questions are seen in the wire frames
    @pytest.mark.skipif(str(7755) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Sample exercise questions are seen in the wire frames.

        Steps: 

        Open recruitment website ( http://cc.openstax.org/ )
        Click on the 'demo' link in the header OR scroll down until 'Interactive Demos' is displayed
        Click on a Concept Coach book title
        Scroll down until the 'CONCEPT COACH' pane is displayed

        Expected Result:

        Demo exercises are rendered and can be answered along with showing feedback

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

        self.ps.test_updates['passed'] = True


    # Case C7756 - 006 - Teacher | Access Concept Coach help and support before the teacher's course is created
    @pytest.mark.skipif(str(7756) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Access Concept Coach help and support before the teacher's course is created.

        Steps: 

        Send a test e-mail to 'ccsupport@openstax.org'
        Open the recruitment website ( http://cc.openstax.org/ )
        Click on the 'faq' link in the header

        Expected Result:

        E-mail sends successfully
        Frequently Asked Questions are displayed on the recruitment website

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

        self.ps.test_updates['passed'] = True


    # Case C7757 - 007 - Teacher | Teacher registers to use a Concept Coach course
    @pytest.mark.skipif(str(7757) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
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

        self.ps.test_updates['passed'] = True


    # Case C7758 - 008 - Teacher | Teacher uses a web form to sign up for Concept Coach
    @pytest.mark.skipif(str(7758) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Teacher uses a web form to sign up for Concept Coach.

        Steps: 

        Teacher fills out the form 


        Expected Result:

        Preconditions pass. Teacher is able to submit the application successfully.

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

        self.ps.test_updates['passed'] = True


    # Case C7759 - 009 - Teacher | Receive error messages if required fields on the sign up form are blank
    @pytest.mark.skipif(str(7759) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Receive error messages if required fields on the sign up form are blank.

        Steps: 

        Go to the recruitment website ( http://cc.openstax.org/ )
        Click on the 'sign up now' button
        Submit the form without changing any of the text fields


        Expected Result:

        Receive 'Please fill out this field.' error messages in red for each blank required field

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

        self.ps.test_updates['passed'] = True


    # Case C7760 - 010 - Teacher | Submit a form to supply required course information
    @pytest.mark.skipif(str(7760) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Submit a form to supply required course information.

        Steps: 

        Go to the recruitment website ( http://cc.openstax.org )
        Click on the 'sign up now' button
        Fill out the intent to participate form ( http://cc.openstax.org/sign-up )
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

        self.ps.test_updates['passed'] = True


    # Case C7761 - 011 - Teacher | Submit co-instructors, classes, names and other data
    @pytest.mark.skipif(str(7761) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Submit co-instructors, classes, names and other data.

        Steps: 

        Go to the recruitment and promo website ( http://cc.openstax.org/ )
        Click on the 'sign up now' button
        Click on the 'Co-Teaching class with a colleague?' circle button
        Enter the co-instructor's (or co-instructors') information


        Expected Result:

        Input box exists for instructor information, class details and other data

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

        self.ps.test_updates['passed'] = True


    # Case C7762 - 012 - Teacher | Select the textbook to use in the course
    @pytest.mark.skipif(str(7762) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Select the textbook to use in the course.

        Steps: 

        Go to the recruitment website ( http://cc.openstax.org )
        Click on the 'sign up now' button
        Select the course textbook from the 'Book' pull down menu


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

        self.ps.test_updates['passed'] = True


    # Case C7763 - 013 - Teacher | Indicate if the teacher was or was not recruited by OpenStax
    @pytest.mark.skipif(str(7763) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Indicate if the teacher was or was not recruited by OpenStax.

        Steps: 

        Go to the recruitment and promo website ( http://cc.openstax.org/ )
        Click on the 'sign up now' button ( http://cc.openstax.org/sign-up )
        Input recruitment information into the 'Anything else we need to know?' text box


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

        self.ps.test_updates['passed'] = True


    # Case C7764 - 014 - Teacher | Presented a thank you page after registering to use Concept Coach
    @pytest.mark.skipif(str(7764) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Presented a thank you page after registering to use Concept Coach.

        Steps: 

        Go to the recruitment website ( http://cc.openstax.org )
        Click on the 'sign up now' button
        Fill out the intent to participate form ( http://cc.openstax.org/sign-up )
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

        self.ps.test_updates['passed'] = True


    # Case C7765 - 015 - Teacher | Sign up for an OpenStax Accounts username
    @pytest.mark.skipif(str(7765) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Sign up for an OpenStax Accounts username.

        Steps: 

        Go to the recruitment website ( http://cc.openstax.org )
        Click on the 'sign up now' button
        Fill out the intent to participate form ( http://cc.openstax.org/sign-up )
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

        self.ps.test_updates['passed'] = True


    # Case C7766 - 016 - Teacher | Sign up to receive additional Concept Coach information by e-mail
    @pytest.mark.skipif(str(7766) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Sign up to receive additional Concept Coach information by e-mail.

        Steps: 

        Go to the recruitment website ( http://cc.openstax.org/ )
        Click on the 'faq' header link


        Expected Result:

        'Contact Us' pane is visible with the info@ email and the general phone number

        """
        self.ps.test_updates['name'] = 'cc1.01.016' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.01',
            'cc1.01.016',
            '7766'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C7767 - 017 - Teacher | Sign up to receive additional Concept Coach information by webform
    @pytest.mark.skipif(str(7767) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Sign up to receive additional Concept Coach information by webform.

        Steps: 

        Go to the recruitment website ( http://cc.openstax.org/ )
        Click on the 'sign up now' button
        Fill out the web form required fields
        Click on the submit button


        Expected Result:

        'Display a Thank You message

        """
        self.ps.test_updates['name'] = 'cc1.01.017' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.01',
            'cc1.01.017',
            '7767'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C7770 - 020 - Teacher | Add co-instructors to a course
    @pytest.mark.skipif(str(7770) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Add co-instructors to a course.

        Steps: 

        Log into Tutor as an admin (admin : password)
        From the user menu, select 'Admin'
        From the 'Course Organization' menu, select 'Courses'
        In the Courses table, find the correct course and click the 'Edit' button on the right side of that row
        Click on the 'Teachers' tab
        In the search box, enter the teacher's name or username
        Select the teacher in the list below the search bar or hit the down arrow followed by the enter/return key


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

        self.ps.test_updates['passed'] = True


    # Case C7771 - 021 - Teacher | Log in with an Existing OpenStax Accounts username
    @pytest.mark.skipif(str(7771) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Log in with an Existing OpenStax Accounts username.

        Steps: 

        Go to the recruitment website ( http://cc.openstax.org/ )
        Click on faculty login
        You are redirected to the accounts page.
        Enter a username and password
        click on Login.


        Expected Result:

        Login should be successful. It should take you to the teacher course picker/dashboard page.

        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)


    # Case C7772 - 022 - Teacher | Access the Concept Coach course
    @pytest.mark.skipif(str(7772) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Access the Concept Coach course.

        Steps: 

        Once you login you will be taken to a course picker page. 
        Click on the course you want to check the dashboard


        Expected Result:

        At Concept Coach teacher dashboard

        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)


    # Case C7773 - 023 - Teacher | Distribute access codes for the teacher's course
    @pytest.mark.skipif(str(7773) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Distribute access codes for the teacher's course.

        Steps: 

        CC approves a faculty.
        Login as admin [admin | password]
        Click on user menu
        Click on Admin
        Click on Salesforce tab
        Click on import [Do not check the box. For testing we work ONLY with Denver University]
        This will automatically create a course for the teacher created.
        Email is sent to the email id used when signing up with the unique course URL.


        Expected Result:

        Instructors are emailed the unique course url to the address provided when they signed up.

        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)


    # Case C7774 - 024 - Teacher | Access Concept Coach help and support during the course
    @pytest.mark.skipif(str(7774) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Access Concept Coach help and support during the course.

        Steps: 

        Login as teacher
        Click on the course name
        On dashboard click on the name of the teacher
        It drops down and displays several options.
        Click on Get Help
        It should open a new tab which shows the openstaxcc.zendesk


        Expected Result:

        It should open a new tab which shows the openstaxcc.zendesk

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

        self.ps.test_updates['passed'] = True


    # Case C7775 - 025 - Teacher | Access Concept Coach help and support after the end of the course
    @pytest.mark.skipif(str(7775) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Access Concept Coach help and support after the end of the course.

        Steps: 

        Login as teacher
        Click on the course name
        On dashboard click on the name of the teacher
        It drops down and displays several options.
        Click on Get Help
        It should open a new tab which shows the openstaxcc.zendesk


        Expected Result:

        It should open a new tab which shows the openstaxcc.zendesk

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

        self.ps.test_updates['passed'] = True