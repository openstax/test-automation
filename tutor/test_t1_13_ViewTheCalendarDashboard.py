"""Tutor v1, Epic 13 - ViewTheCalendarDashboard."""

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
from staxing.helper import Teacher

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
    str([7978])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestViewTheCalendarDashboard(unittest.TestCase):
    """T1.13 - View the calendar."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.teacher = Teacher(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        self.teacher.login()

    def tearDown(self):
        """Test destructor."""
        self.ps.update_job(job_id=str(self.teacher.driver.session_id),
                           **self.ps.test_updates)
        try:
            self.teacher.delete()
        except:
            pass

    # Case C7978 - 001 - Teacher | View the calendar dashboard
    @pytest.mark.skipif(str(7978) not in TESTS, reason='Excluded')
    def test_teacher_view_the_calendar_dashboard(self):
        """View the calendar dashboard.

        Steps:
        Go to https://tutor-XXXX.openstax.org/
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a Tutor course name

        Expected Result:
        The teacher is presented their calendar dashboard.
        """
        self.ps.test_updates['name'] = 't1.13.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.001', '7978']
        self.ps.test_updates['passed'] = False

        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.ps.test_updates['passed'] = True


    # Case C7979 - 002 - Teacher | View student scores using the dashboard button
    @pytest.mark.skipif(str(7979) not in TESTS, reason='Excluded')
    def test_teacher_view_student_scores_using_the_dashboard_button(self):
        """ View student scores using the dashboard button

        Steps:
        Go to https://tutor-XXXX.openstax.org/
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a Tutor course name
        Click on the 'Student Scores' button

        Expected Result:
        The teacher is presented with the student scores
        """
        self.ps.test_updates['name'] = 't1.13.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.002', '7979']
        self.ps.test_updates['passed'] = False
        
        self.teacher.select_course(appearance='physics')
        #click the student scores button
        assert('scores' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'
        
        self.ps.test_updates['passed'] = True

   # Case C7980 - 003 - Teacher | View student scores using the user menu link
    @pytest.mark.skipif(str(7980) not in TESTS, reason='Excluded')
    def test_teacher_view_student_scores_using_the_user_menu_link(self):
        """ View student scores using the user menu link

        Steps:
        Go to https://tutor-XXXX.openstax.org/
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a Tutor course name
        Click on the user menu
        Click on the 'Student Scores' link

        Expected Result:
        The teacher is presented with the student scores
        """
        self.ps.test_updates['name'] = 't1.13.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.003', '7980']
        self.ps.test_updates['passed'] = False
        
        self.teacher.select_course(appearance='physics')
        #click the user menu
        #click the student scores link
        assert('scores' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'
        
        self.ps.test_updates['passed'] = True

 # Case C7981 - 004 - Teacher | View performace forecast using the dashboard button
    @pytest.mark.skipif(str(7981) not in TESTS, reason='Excluded')
    def test_teacher_view_performace_forecast_using_the_dashboard_button(self):
        """ View performance forecast using the dashboard button

        Steps:
        Go to https://tutor-XXXX.openstax.org/
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a Tutor course name
        Click on the 'Performace Forecast' button

        Expected Result:
        The teacher is presented with the performance forecast
        """
        self.ps.test_updates['name'] = 't1.13.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.004', '7981']
        self.ps.test_updates['passed'] = False
        
        self.teacher.select_course(appearance='physics')
        #click the performace forecast button
        assert('guide' in self.teacher.current_url()), \
            'Not viewing the performance forecast'
        
        self.ps.test_updates['passed'] = True

    # Case C7982 - 005 - Teacher | View performace forecast using the user menu link
    @pytest.mark.skipif(str(7982) not in TESTS, reason='Excluded')
    def test_teacher_view_performace_forecast_using_the_user_menu_link(self):
        """ View performance forecast using the user menu link

        Steps:
        Go to https://tutor-XXXX.openstax.org/
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a Tutor course name
        Click on the user menu
        Click on the 'Performance Forecast' link

        Expected Result:
        The teacher is presented with the performance forecast
        """
        self.ps.test_updates['name'] = 't1.13.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.005', '7982']
        self.ps.test_updates['passed'] = False
        
        self.teacher.select_course(appearance='physics')
        #click the user menu
        #click on the performance forecast link
        assert('guide' in self.teacher.current_url()), \
            'Not viewing the performance forecast'
        
        self.ps.test_updates['passed'] = True

    # Case C7983 - 006 - Teacher | View a reading assignment summary
    @pytest.mark.skipif(str(7983) not in TESTS, reason='Excluded')
    def test_teacher_view_a_reading_assignment_summary(self):
        """ View a reading assignment summary

        Steps:
        Go to https://tutor-XXXX.openstax.org/
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a Tutor course name
        Click on a reading assignment on the calendar

        Expected Result:
        The teacher is presented with the reading assignment summary
        """
        self.ps.test_updates['name'] = 't1.13.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.006', '7983']
        self.ps.test_updates['passed'] = False
        
        self.teacher.select_course(appearance='physics')
        #click on a reading assignment
        #assert(  , \
        #    'Not viewing reading assignemnt summary'
        
        self.ps.test_updates['passed'] = True

   # Case C7984 - 007 - Teacher | View a homework assignment summary
    @pytest.mark.skipif(str(7984) not in TESTS, reason='Excluded')
    def test_teacher_view_a_homework_assignment_summary(self):
        """ View a homework assignment summary

        Steps:
        Go to https://tutor-XXXX.openstax.org/
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a Tutor course name
        Click on a homework assignment on the calendar

        Expected Result:
        The teacher is presented with the homework assignment summary
        """
        self.ps.test_updates['name'] = 't1.13.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.007', '7984']
        self.ps.test_updates['passed'] = False
        
        self.teacher.select_course(appearance='physics')
        #click on a homework assignment
        #assert(  , \
        #    'Not viewing homework assignemnt summary'
        
        self.ps.test_updates['passed'] = True

    # Case C7985 - 008 - Teacher | View an external assignment summary
    @pytest.mark.skipif(str(7985) not in TESTS, reason='Excluded')
    def test_teacher_view_an_external_assignment_summary(self):
        """ View an external assignment summary

        Steps:
        Go to https://tutor-XXXX.openstax.org/
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a Tutor course name
        Click on an external assignment on the calendar

        Expected Result:
        The teacher is presented with the external assignment summary
        """
        self.ps.test_updates['name'] = 't1.13.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.008', '7985']
        self.ps.test_updates['passed'] = False
        
        self.teacher.select_course(appearance='physics')
        #click on a external assignment
        #assert(  , \
        #    'Not viewing external assignemnt summary'
        
        self.ps.test_updates['passed'] = True

    # Case C7986 - 009 - Teacher | View an event summary
    @pytest.mark.skipif(str(7986) not in TESTS, reason='Excluded')
    def test_teacher_view_an_event_summary(self):
        """ View an event summary

        Steps:
        Go to https://tutor-XXXX.openstax.org/
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a Tutor course name
        Click on an event on the calendar

        Expected Result:
        The teacher is presented with the event summary
        """
        self.ps.test_updates['name'] = 't1.13.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.009', '7986']
        self.ps.test_updates['passed'] = False
        
        self.teacher.select_course(appearance='physics')
        #click on an event
        #assert(  , \
        #    'Not viewing event summary'
        
        self.ps.test_updates['passed'] = True

    # Case C7987 - 010 - Teacher | Open the refrenece book using the dashboard button
    @pytest.mark.skipif(str(7987) not in TESTS, reason='Excluded')
    def test_teacher_open_the_reference_book_using_the_dashboard_button(self):
        """ Open the refrenece book using the dashboard button

        Steps:
        Go to https://tutor-XXXX.openstax.org/
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a Tutor course name
        Click on the 'Browse The Book'button

        Expected Result:
        A new window or tab is opened with the PDF view of the textbook
        """
        self.ps.test_updates['name'] = 't1.13.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.010', '7987']
        self.ps.test_updates['passed'] = False
        
        self.teacher.select_course(appearance='physics')
        #click on browse the book
        #assert(  , \
        #    'Not viewing the textbook PDF'
        
        self.ps.test_updates['passed'] = True

 # Case C7988 - 011 - Teacher | Open the refrenece book using the user menu link
    @pytest.mark.skipif(str(7988) not in TESTS, reason='Excluded')
    def test_teacher_open_the_reference_book_using_the_user_menu_link(self):
        """ Open the refrenece book using the user menu link

        Steps:
        Go to https://tutor-XXXX.openstax.org/
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a Tutor course name
        Click on the user menu
        Click on the 'Browse the Book' link

        Expected Result:
        A new window or tab is opened with the PDF view of the textbook
        """
        self.ps.test_updates['name'] = 't1.13.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.011', '7988']
        self.ps.test_updates['passed'] = False
        
        self.teacher.select_course(appearance='physics')
        #click on the user menu
        #click on browse the book
        #assert(  , \
        #    'Not viewing the textbook PDF'
        
        self.ps.test_updates['passed'] = True

    # Case C7989 - 012 - Teacher | Click on the course name to return to the dashboard
    @pytest.mark.skipif(str(7989) not in TESTS, reason='Excluded')
    def test_teacher_click_on_the_course_name_to_return_to_the_dashboard(self):
        """ Click on the course name to return to the dashboard

        Steps:
        Go to https://tutor-XXXX.openstax.org/
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a Tutor course name
        Click on the 'Performance Forecast' button
        Click on the course name in the header

        Expected Result:
        The teacher is presented with their calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.13.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.012', '7989']
        self.ps.test_updates['passed'] = False
        
        self.teacher.select_course(appearance='physics')
        #click on performance forecast
        #click on the course name
        #assert(  , \
        #    'Not viewing the textbook PDF'
        
        self.ps.test_updates['passed'] = True


    #ASK ABOUT THIS BECAUSE THE NAME IS SO LONG
    # Case C7990 - 013 - Teacher | For a user with multiple courses, cick on the OpenStax logo ...
    @pytest.mark.skipif(str(7990) not in TESTS, reason='Excluded')
    def test_teacher_click_on_the_course_name_to_return_to_the_dashboard(self):
        """ 

        Steps:
        Go to https://tutor-XXXX.openstax.org/
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a Tutor course name
        Click in the OpenStax logo in the header

        Expected Result:
        The teacher is presented with the course picker
        """
        self.ps.test_updates['name'] = 't1.13.013' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.013', '7990']
        self.ps.test_updates['passed'] = False
        
        self.teacher.select_course(appearance='physics')
        #click on the openstax logo
        #assert(  , \
        #    'Not viewing the course picker'
        
        self.ps.test_updates['passed'] = True

    #ASK ABOUT THIS BECAUSE THE NAME IS SO LONG
    # Case C7991 - 014 - Teacher | For a user with one course, CLick in the OpenStax logo ...
    @pytest.mark.skipif(str(7991) not in TESTS, reason='Excluded')
    def test_teacher_click_on_the_course_name_to_return_to_the_dashboard(self):
        """ 

        Steps:
        Go to https://tutor-XXXX.openstax.org/
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a Tutor course name
        Click on the 'Performance Forecast' button
        Click on the OpenStax logo in the header

        Expected Result:
        The teacher is presented with their calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.13.014' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.014', '7991']
        self.ps.test_updates['passed'] = False
        
        self.teacher.select_course(appearance='physics')
        #click on performance forecast
        #click on the OpenStax logo
        #assert(  , \
        #    'Not viewing the calendar dashboard'
        
        self.ps.test_updates['passed'] = True
