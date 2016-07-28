"""Tutor v1, Epic 13 - ViewTheCalendarDashboard."""

import inspect
import json
import os
import pytest
import unittest
import datetime

from pastasauce import PastaSauce, PastaDecorator
from random import randint  # NOQA
from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as expect
# from staxing.assignment import Assignment
from staxing.helper import Teacher

basic_test_env = json.dumps([
    {
        'platform': 'Windows 10',
        'browserName': 'chrome',
        'version': 'latest',
        'screenResolution': "1024x768",
    }
])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([
        56150, 56151, 56152, 56153, 56154,
        56155, 56156, 56157, 56158, 56159,
        56160, 56161, 56162, 56163
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestTutorAndJenkins(unittest.TestCase):
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
    @pytest.mark.skipif(str(56150) not in TESTS, reason='Excluded')
    def test_teacher_view_the_calendar_dashboard_56150(self):
        """View the calendar dashboard.

        Steps:
        If the user has more than one course, click on a Tutor course name

        Expected Result:
        The teacher is presented their calendar dashboard.
        """
        self.ps.test_updates['name'] = 't1.13.001' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.001', '7978']
        self.ps.test_updates['passed'] = False

        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.ps.test_updates['passed'] = True

    # Case C7979 - 002 - Teacher | View student scores using the dashboard
    # button
    @pytest.mark.skipif(str(56151) not in TESTS, reason='Excluded')
    def test_teacher_view_student_score_using_the_dashboard_button_56151(self):
        """View student scores using the dashboard button.

        Steps:
        If the user has more than one course, click on a Tutor course name
        Click on the 'Student Scores' button

        Expected Result:
        The teacher is presented with the student scores
        """
        self.ps.test_updates['name'] = 't1.13.002' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.002', '7979']
        self.ps.test_updates['passed'] = False

        self.teacher.select_course(appearance='physics')
        self.teacher.driver.find_element(By.LINK_TEXT, 'Student Score').click()
        assert('scores' in self.teacher.current_url()), \
            'Not viewing student scores'

        self.ps.test_updates['passed'] = True

    # Case C7980 - 003 - Teacher | View student scores using the user menu link
    @pytest.mark.skipif(str(56152) not in TESTS, reason='Excluded')
    def test_teacher_view_student_scores_using_the_user_menu_link_56152(self):
        """View student scores using the user menu link.

        Steps:
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
        self.teacher.open_user_menu()
        self.teacher.driver.find_element(By.CLASS_NAME, 'viewScores').click()
        assert('scores' in self.teacher.current_url()), \
            'Not viewing the student scores'

        self.ps.test_updates['passed'] = True

    # Case C7981 - 004 - Teacher | View performace forecast using the dashboard
    # button
    @pytest.mark.skipif(str(56153) not in TESTS, reason='Excluded')
    def test_teacher_view_performace_forecast_using_the_dash_btn_56153(self):
        """View performance forecast using the dashboard button.

        Steps:
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
        self.teacher.driver.find_element(
            By.LINK_TEXT,
            'Performance Forecast'
        ).click()
        assert('guide' in self.teacher.current_url()), \
            'Not viewing the performance forecast'

        self.ps.test_updates['passed'] = True

    # Case C7982 - 005 - Teacher | View performace forecast using the user menu
    # link
    @pytest.mark.skipif(str(56154) not in TESTS, reason='Excluded')
    def test_teacher_view_performace_forecast_using_user_menu_link_56154(self):
        """View performance forecast using the user menu link.

        Steps:
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
        self.teacher.open_user_menu()
        self.teacher.driver.find_element(
            By.CLASS_NAME,
            'viewTeacherPerformanceForecast'
        ).click()
        assert('guide' in self.teacher.current_url()), \
            'Not viewing the performance forecast'

        self.ps.test_updates['passed'] = True

    # Case C7983 - 006 - Teacher | View a reading assignment summary
    @pytest.mark.skipif(str(56155) not in TESTS, reason='Excluded')
    def test_teacher_view_a_reading_assignment_summary_56155(self):
        """View a reading assignment summary.

        Steps:
        If the user has more than one course, click on a Tutor course name
        Create a reading assignment
        Click on the reading assignment on the calendar

        Expected Result:
        The teacher is presented with the reading assignment summary
        """
        self.ps.test_updates['name'] = 't1.13.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.006', '7983']
        self.ps.test_updates['passed'] = False

        self.teacher.select_course(appearance='physics')
        # create an assignemnt
        assignment_name = 'reading-%s' % randint(100, 999)
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(
            assignment='reading',
            args={
                'title': assignment_name,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'reading_list': ['ch1'],
                'status': 'publish',
            }
        )
        # click on assignemnt
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[contains(text(), "%s")]' % assignment_name
        ).click()
        # check that it opened
        self.teacher.driver.find_element(
            By.XPATH,
            '//h2[contains(text(), "%s")]' % assignment_name
        )

        self.ps.test_updates['passed'] = True

    # #NOT DONE
    # Case C7984 - 007 - Teacher | View a homework assignment summary
    @pytest.mark.skipif(str(56156) not in TESTS, reason='Excluded')
    def test_teacher_view_a_homework_assignment_summary_56156(self):
        """View a homework assignment summary.

        Steps:
        create a homework assignemtn
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
        # create an assignment
        assignment_name = "homework-%s" % randint(100, 999)
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=2)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=4)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(
            assignment='homework',
            args={
                'title': assignment_name,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'problems': {'4.1': (4, 8), },
                'status': 'publish',
            }
        )
        # click on assignemnt
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[contains(text(), "%s")]' % assignment_name
        ).click()  # should it be label not div
        # check that it opened
        self.teacher.driver.find_element(
            By.XPATH, '//h2[contains(text(), "%s")]' % assignment_name)
        self.ps.test_updates['passed'] = True

    # NOT DONE
    # Case C7985 - 008 - Teacher | View an external assignment summary
    @pytest.mark.skipif(str(56157) not in TESTS, reason='Excluded')
    def test_teacher_view_an_external_assignment_summary_56157(self):
        """View an external assignment summary.

        Steps:
        If the user has more than one course, click on a Tutor course name
        Click on an external assignment on the calendar

        Expected Result:
        The teacher is presented with the external assignment summary
        """
        self.ps.test_updates['name'] = 't1.13.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.008', '7985']
        self.ps.test_updates['passed'] = False

        # create an assignemnt
        assignment_name = 'external-%s' % randint(100, 999)
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(
            assignment='external',
            args={
                'title': assignment_name,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'url': 'google.com',
                'status': 'publish'
            }
        )
        # click on assignemnt
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[contains(text(), "%s")]' % assignment_name
        ).click()  # should it be label not div
        # check that it opened
        self.teacher.driver.find_element(
            By.XPATH,
            '//h2[contains(text(), "%s")]' % assignment_name
        )

        self.ps.test_updates['passed'] = True

    # NOT DONE
    # Case C7986 - 009 - Teacher | View an event summary
    @pytest.mark.skipif(str(56158) not in TESTS, reason='Excluded')
    def test_teacher_view_an_event_summary_56158(self):
        """View an event summary.

        Steps:
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
        # create an assignment
        assignment_name = "homework-%s" % randint(100, 999)
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=2)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=4)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(
            assignment='homework',
            args={
                'title': assignment_name,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'status': 'publish'
            }
        )
        # click on assignemnt
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[contains(text(), "%s")]' % assignment_name
        ).click()  # should it be label not div
        # check that it opened
        self.teacher.driver.find_element(
            By.XPATH, '//h2[contains(text(), "%s")]' % assignment_name)
        self.ps.test_updates['passed'] = True

    # Case C7987 - 010 - Teacher | Open the refrenece book using the dashboard
    # button
    @pytest.mark.skipif(str(56159) not in TESTS, reason='Excluded')
    def test_teacher_open_the_reference_book_using_dashboard_btn_56159(self):
        """Open the refrenece book using the dashboard button.

        Steps:
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
        self.teacher.driver.find_element(
            By.LINK_TEXT,
            'Browse The Book'
        ).click()
        window_with_book = self.teacher.driver.window_handles[1]
        self.teacher.driver.switch_to_window(window_with_book)
        assert('book' in self.teacher.current_url()), \
            'Not viewing the textbook PDF'

        self.ps.test_updates['passed'] = True

    # Case C7988 - 011 - Teacher | Open the refrenece book using the user menu
    # link
    @pytest.mark.skipif(str(56160) not in TESTS, reason='Excluded')
    def test_teacher_open_the_reference_book_using_user_menu_link_56160(self):
        """Open the refrenece book using the user menu link.

        Steps:
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
        self.teacher.open_user_menu()
        self.teacher.driver.find_element(
            By.CLASS_NAME,
            'view-reference-guide'
        ).click()
        window_with_book = self.teacher.driver.window_handles[1]
        self.teacher.driver.switch_to_window(window_with_book)
        assert('book' in self.teacher.current_url()), \
            'Not viewing the textbook PDF'

        self.ps.test_updates['passed'] = True

    # Case C7989 - 012 - Teacher | Click on the course name to return to the
    # dashboard
    @pytest.mark.skipif(str(56161) not in TESTS, reason='Excluded')
    def test_teacher_click_course_name_to_return_to_the_dashboard_56161(self):
        """Click on the course name to return to the dashboard.

        Steps:
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
        self.teacher.driver.find_element(
            By.CLASS_NAME,
            'viewTeacherPerformanceForecast'
        ).click()
        self.teacher.driver.find_element(
            By.CLASS_NAME,
            'course-name'
        ).click()
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.ps.test_updates['passed'] = True

    # Case C7990 - 013 - Teacher | Cick on the OpenStax logo to return to the
    # course picker
    @pytest.mark.skipif(str(56162) not in TESTS, reason='Excluded')
    def test_teacher_click_openstax_logo_to_return_to_course_pkr_56162(self):
        """Cick on the OpenStax logo to return to the course picker.

        Steps:
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
        self.teacher.driver.find_element(
            By.CLASS_NAME,
            'ui-brand-logo'
        ).click()
        assert('dashboard' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.ps.test_updates['passed'] = True

    # SHOULD WORK BUT DON'T KNOW HOW TO LOGIN WITH DIFFERENT TEACHER
    # Case C7991 - 014 - Teacher | CLick in the OpenStax logo to return to the
    # dashboard
    @pytest.mark.skipif(str(56163) not in TESTS, reason='Excluded')
    def test_teacher_clicks_openstax_logo_to_return_to_dashboard_56163(self):
        """CLick in the OpenStax logo to return to the dashboard.

        Steps:
        Click on the 'Performance Forecast' button
        Click on the OpenStax logo in the header

        Expected Result:
        The teacher is presented with their calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.13.014' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.014', '7991']
        self.ps.test_updates['passed'] = False

        self.teacher.driver.find_element(
            By.CLASS_NAME,
            'viewTeacherPerformanceForecast'
        ).click()
        self.teacher.driver.find_element(
            By.CLASS_NAME,
            'ui-brand-logo'
        ).click()
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.ps.test_updates['passed'] = True