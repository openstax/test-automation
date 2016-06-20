"""Tutor v1, Epic 42 - ViewTheListDashboard."""

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
from selenium.webdriver.support.ui import WebDriverWait

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Student  # NOQA


basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': '50.0',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([8268, 8269, 8270, 8271, 8272,
         8273, 8274, 8275, 8276, 8277,
         8278, 8279, 8280])  # NOQA
)


@PastaDecorator.on_platforms(BROWSERS)
class TestViewTheListDashboard(unittest.TestCase):
    """T1.45 - View the list dashboard."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.student = Student(
            use_env_vars=True#,
            #pasta_user=self.ps,
            #capabilities=self.desired_capabilities
        )
        self.student.login()

    def tearDown(self):
        """Test destructor."""
        self.ps.update_job(job_id=str(self.student.driver.session_id),
                           **self.ps.test_updates)
        try:
            self.student.delete()
        except:
            pass

    # Case C8268 - 001 - Student| View the assignment list
    @pytest.mark.skipif(str(8268) not in TESTS, reason='Excluded')  # NOQA
    def test_student_view_the_assignemnt_list(self):
        """View the assignment list

        Steps:
        If the user has more than one course, select a Tutor course

        Expected Result:
        The User is presented with their assignment list
        """
        self.ps.test_updates['name'] = 't1.45.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.45', 't1.45.001', '8268']
        self.ps.test_updates['passed'] = False

        self.student.select_course(appearance='physics')
        assert('list' in self.student.current_url()), \
            'Not viewing the list dashboard'

        self.ps.test_updates['passed'] = True

    # Case C8269 - 002 - Student| View the performance forecast using the dashboard button
    @pytest.mark.skipif(str(8269) not in TESTS, reason='Excluded')  # NOQA
    def test_student_view_the_performance_forecast_using_the_dashboard_button(self):
        """View the performance forecast using the dashboard button

        Steps:
        If the user has more than one course, select a Tutor course
        Click the View All Topics button

        Expected Result:
        The User is presented with their performance forecast
        """
        self.ps.test_updates['name'] = 't1.45.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.45', 't1.45.002', '8269']
        self.ps.test_updates['passed'] = False

        self.student.select_course(appearance='physics')
        wait = WebDriverWait(self.student.driver, Assignment.WAIT_TIME)
        performance = wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"view-performance-forecast")]')
            )
        )         
        self.student.driver.execute_script('return arguments[0].scrollIntoView();', performance)
        self.student.driver.execute_script('window.scrollBy(0, -80);')
        performance.click()
        assert('guide' in self.student.current_url()), \
            'Not viewing the performance forecast'
        self.ps.test_updates['passed'] = True

    # Case C8270 - 003 - Student| View the performance forecast using the menu link
    @pytest.mark.skipif(str(8270) not in TESTS, reason='Excluded')  # NOQA
    def test_student_view_the_performance_forecast_using_the_menu_link(self):
        """View the performance forecast using the menu link

        Steps:
        If the user has more than one course, select a Tutor course
        Click on the user menu
        Click on the Performance Forecast option

        Expected Result:
        The User is presented with their performance forecast
        """
        self.ps.test_updates['name'] = 't1.45.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.45', 't1.45.003', '8270']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.select_course(appearance='physics')
        self.student.open_user_menu()
        wait = WebDriverWait(self.student.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.CLASS_NAME, 'viewPerformanceForecast')
            )
        ).click()
        assert('guide' in self.student.current_url()), \
            'Not viewing the performance forecast'
        self.ps.test_updates['passed'] = True

    # Case C8271 - 004 - Student| View the assignments for the current week
    @pytest.mark.skipif(str(8271) not in TESTS, reason='Excluded')  # NOQA
    def test_student_view_the_assignemnts_for_the_current_week(self):
        """View the assignments for the current week

        Steps:
        If the user has more than one course, select a Tutor course

        Expected Result:
        The Assignemnts for the current week are displayed
        """
        self.ps.test_updates['name'] = 't1.45.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.45', 't1.45.004', '8271']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.select_course(appearance='physics')
        wait = WebDriverWait(self.student.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'This Week')
            )
        )
        self.ps.test_updates['passed'] = True

    # Case C8272 - 005 - Student| View the upcoming assignments
    @pytest.mark.skipif(str(8272) not in TESTS, reason='Excluded')  # NOQA
    def test_student_view_the_upcoming_assignemnts(self):
        """View the upcoming assignments

        Steps:
        If the user has more than one course, select a Tutor course

        Expected Result:
        The Upcoming Assignemnts are displayed
        """
        self.ps.test_updates['name'] = 't1.45.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.45', 't1.45.005', '8272']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.select_course(appearance='physics')
        wait = WebDriverWait(self.student.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"-upcoming")]')
            )
        )
        self.ps.test_updates['passed'] = True

    # Case C8273 - 006 - Student| View past work
    @pytest.mark.skipif(str(8273) not in TESTS, reason='Excluded')  # NOQA
    def test_student_view_past_work(self):
        """View past work

        Steps:
        If the user has more than one course, select a Tutor course
        Click on the All Past Work tab

        Expected Result:
        The Past work is displayed
        """
        self.ps.test_updates['name'] = 't1.45.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.45', 't1.45.006', '8273']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.select_course(appearance='physics')
        wait = WebDriverWait(self.student.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'All Past Work')
            )
        ).click()
        ####some sort of assertion that student is actually looking at past work
        self.ps.test_updates['passed'] = True

    # Case C8274 - 007 - Student| Check which assignments were late
    @pytest.mark.skipif(str(8274) not in TESTS, reason='Excluded')  # NOQA
    def test_student_check_which_assignments_were_late(self):
        """Check which assignments were late

        Steps:
        If the user has more than one course, select a Tutor course
        Click on the All Past Work tab

        Expected Result:
        Late Assignemnts have a red clock icon next to their progress status
        """
        self.ps.test_updates['name'] = 't1.45.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.45', 't1.45.007', '8274']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.select_course(appearance='physics')
        wait = WebDriverWait(self.student.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'All Past Work')
            )
        ).click()
        late = wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//i[contains(@class,"info late")]')
            )
        )
        self.student.driver.execute_script('return arguments[0].scrollIntoView();', late)
        self.student.driver.execute_script('window.scrollBy(0, -80);')
        late.click()

        self.ps.test_updates['passed'] = True

    # Case C8275 - 008 - Student| View recent performance forecast topics
    @pytest.mark.skipif(str(8275) not in TESTS, reason='Excluded')  # NOQA
    def test_student_view_recent_performance_topics(self):
        """View recent performance forecast topics

        Steps:
        If the user has more than one course, select a Tutor course

        Expected Result:
        Recent topics are displayed on the dashboard under performance forecast
        """
        self.ps.test_updates['name'] = 't1.45.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.45', 't1.45.008', '8275']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.select_course(appearance='physics')
        wait = WebDriverWait(self.student.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//h2[contains(@class, "recent")]')
            )
        )
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class, "guide-group")]')
            )
        )
        self.ps.test_updates['passed'] = True

    # Case C8276 - 009 - Student| Open the refrence book using the dashboard button
    @pytest.mark.skipif(str(8276) not in TESTS, reason='Excluded')  # NOQA
    def test_student_open_the_refrence_book_using_the_dashboard_button(self):
        """Open the refrence book using the dashboard button

        Steps:
        If the user has more than one course, select a Tutor course
        Click the Browse The Book button

        Expected Result:
        The refrence book is opened in a new tab or window
        """
        self.ps.test_updates['name'] = 't1.45.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.45', 't1.45.009', '8276']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.select_course(appearance='physics')
        wait = WebDriverWait(self.student.driver, Assignment.WAIT_TIME)
        book = wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[contains(@class,"view-reference-guide")]'\
                 '//div[contains(text(),"Browse the Book")]')
            )
        )
        self.student.driver.execute_script('return arguments[0].scrollIntoView();', book)
        self.student.driver.execute_script('window.scrollBy(0, -80);')
        book.click()
        window_with_book = self.student.driver.window_handles[1]
        self.student.driver.switch_to_window(window_with_book)
        assert( 'book' in self.student.current_url()) , \
            'Not viewing the textbook PDF'

        self.ps.test_updates['passed'] = True

    # Case C8277 - 010 - Student| Open the refrence book using the menu link
    @pytest.mark.skipif(str(8277) not in TESTS, reason='Excluded')  # NOQA
    def test_student_open_the_refrence_book_using_the_menu_link(self):
        """Open the refrence book using the menu link

        Steps:
        If the user has more than one course, select a Tutor course
        Click on the user menu
        Click the Browse The Book option

        Expected Result:
        The refrence book is opened in a new tab or window
        """
        self.ps.test_updates['name'] = 't1.45.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.45', 't1.45.010', '8277']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.select_course(appearance='physics')
        self.student.open_user_menu()
        wait = WebDriverWait(self.student.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.CLASS_NAME, 'view-reference-guide')
            )
        ).click()
        window_with_book = self.student.driver.window_handles[1]
        self.student.driver.switch_to_window(window_with_book)
        assert( 'book' in self.student.current_url()) , \
            'Not viewing the textbook PDF'

        self.ps.test_updates['passed'] = True

    # Case C8278 - 011 - Student| Click on the course name to return to the dasboard
    @pytest.mark.skipif(str(8278) not in TESTS, reason='Excluded')  # NOQA
    def test_student_click_on_the_course_name_to_return_to_the_dashboard(self):
        """Click on the course name to return to the dashboard

        Steps:
        If the user has more than one course, select a Tutor course
        Click on the View All Topics button
        Click on the course name

        Expected Result:
        The user is returned to their dashboard
        """
        self.ps.test_updates['name'] = 't1.45.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.45', 't1.45.011', '8278']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.select_course(appearance='physics')
        wait = WebDriverWait(self.student.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"view-performance-forecast")]')
            )
        ).click()
        self.student.driver.find_element(
            By.XPATH,'//a[contains(@aria-describedby,"course-name-tooltip")]').click()
        assert( 'list' in self.student.current_url()) , \
            'Not viewing the list dashboard 011'

        self.ps.test_updates['passed'] = True

    # Case C8279 - 012 - Student| Click on the OpneStax logo to return to the course picker
    @pytest.mark.skipif(str(8279) not in TESTS, reason='Excluded')  # NOQA
    def test_student_click_on_the_openstax_logo_to_return_to_the_course_picker(self):
        """Click on the OpenStax logo to return to the course picker

        Steps:
        If the user has more than one course, select a Tutor course
        Click on the OpenStax logo

        Expected Result:
        The user is returned to the course picker
        """
        self.ps.test_updates['name'] = 't1.45.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.45', 't1.45.012', '8279']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.select_course(appearance='physics')
        self.student.driver.find_element(
            By.XPATH,'//i[contains(@class,"ui-brand-logo")]').click()
        assert( 'dashboard' in self.student.current_url()) , \
            'Not viewing the course picker 012'

        self.ps.test_updates['passed'] = True

    ####this should work but needs a sutdent with one course to test on
    # # Case C8280 - 013 - Student| Click on the course OpenStax logo to return to the dasboard
    # @pytest.mark.skipif(str(8280) not in TESTS, reason='Excluded')  # NOQA
    # def test_student_click_on_the_OpenStax_logo_to_return_to_the_dashboard(self):
    #     """Click on the OpenStax logo to return to the dashboard

    #     Steps:
    #     If the user has more than one course, select a Tutor course
    #     Click on the View All Topics button
    #     Click on the OpenStax logo

    #     Expected Result:
    #     The user is returned to their dashboard
    #     """
    #     self.ps.test_updates['name'] = 't1.45.013' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = ['t1', 't1.45', 't1.45.013', '8280']
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions
    #     wait = WebDriverWait(self.student.driver, Assignment.WAIT_TIME)
    #     wait.until(
    #         expect.visibility_of_element_located(
    #             (By.XPATH, '//button[contains(@class,"view-performance-forecast")]')
    #         )
    #     ).click()
    #     self.student.driver.find_element(
    #         By.XPATH,'//i[contains(@class,"ui-brand-logo")]').click()
    #     assert( 'list' in self.student.current_url()) , \
    #         'Not viewing the list dashboard 011'
    #     self.ps.test_updates['passed'] = True

