"""Tutor, Dashboard - View Various Aspects on Course Dashboard"""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
# from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from staxing.helper import Student
from selenium.common.exceptions import TimeoutException

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
        162190
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestViewTheListDashboard(unittest.TestCase):
    """T1.45 - View the list dashboard."""

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
        else:
            self.student = Student(
                use_env_vars=True
            )
        self.student.login()


    def tearDown(self):
        """Test destructor."""
        if not LOCAL_RUN:
            self.ps.update_job(
                job_id=str(self.student.driver.session_id),
                **self.ps.test_updates
            )
        try:
            self.student.delete()
        except:
            pass

    # Case C162190 - 001 - Student | View Various Aspects of Tutor
    @pytest.mark.skipif(str(162190) not in TESTS, reason='Excluded')
    def test_student_view_the_assignemnt_list_162190(self):
        """
        #STEPS
        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the student user account [ ] in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, select a Tutor course
        ***The user is presented with their list of assignments.*** 
        ***Assignments for the current week are displayed.*** 
        ***Upcoming assignments are displayed under the table titled 'Coming Up'***
        ***You can see the recent topics under the "Performance Forecast" on the dashboard***(

        Click "Get Help" from the user menu in the upper right corner of the screen
        ***The user is presented with the Tutor Help Center***

        Click the 'View All Topics'
        ***The user is presented with their performance forecast.*** 

        Open the drop down menu by clicking on the menu link with the user's name
        Click on 'Performance Forecast'
        ***The user is presented with their performance forecast.*** 

        Click the button that says "Return to Dashboard"
        Click the button that says 'All Past Work'
        ***The student's past work is displayed.***
        ***Late assignments have a red clock displayed next to their 'Progress' status.***

        Click the 'Browse The Book' button
        # EXPECTED RESULT 
        ***The user is taken to the book in a new tab.*** 

        
        """
        self.ps.test_updates['name'] = 't1.45.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.45', 't1.45.001', '162190']
        self.ps.test_updates['passed'] = False

        # View Dashboard
        self.student.select_course(appearance='college_physics')
        self.student.page.wait_for_page_load()

        # View the Assignments for the current week
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'This Week')
            )
        )

        # View the Upcoming Assignments
        try:
            self.student.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//div[contains(@class,"-upcoming")]')
                )
            )
        except TimeoutException:
            self.student.driver.find_element(
                By.XPATH, '//div[contains(text(),"No upcoming events")]')


        # View Recent Performance Forecast Topics
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//h3[contains(@class, "recent")]')
            )
        )
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class, "guide-group")]')
            )
        )

        # View Performance Forecast Using Dashboard Button
        performance = self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//button[contains(@class,"view-performance-forecast")]')
            )
        )
        self.student.driver.execute_script(
            'return arguments[0].scrollIntoView();', performance)
        self.student.driver.execute_script('window.scrollBy(0, -80);')
        performance.click()
        assert('guide' in self.student.current_url()), \
            'Not viewing the performance forecast'


        # View Performance Forecast Using the Menu

        self.student.open_user_menu()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.CLASS_NAME, 'viewPerformanceGuide')
            )
        ).click()
        assert('guide' in self.student.current_url()), \
            'Not viewing the performance forecast'


        self.student.open_user_menu()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.CLASS_NAME, 'dashboard')
            )
        ).click()

        # # View the Student's Past Work
        # self.student.wait.until(
        #     expect.visibility_of_element_located(
        #         (By.LINK_TEXT, 'All Past Work')
        #     )
        # ).click()
        # assert(past_work.get_attribute('aria-selected') == 'true'),\
        #     'not viewing past work'

        # # Late Assignments have a red clock displayed next to their "Progress" tab

        # late = self.student.wait.until(
        #     expect.visibility_of_element_located(
        #         (By.XPATH, '//i[contains(@class,"info late")]')
        #     )
        # )
        # self.student.driver.execute_script(
        #     'return arguments[0].scrollIntoView();', late)
        # self.student.driver.execute_script('window.scrollBy(0, -80);')
        # late.click()

        # Click Browse The Book button

        book = self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[contains(@class,"view-reference-guide")]' +
                 '//div[contains(text(),"Browse the Book")]')
            )
        )
        self.student.driver.execute_script(
            'return arguments[0].scrollIntoView();', book)
        self.student.driver.execute_script('window.scrollBy(0, -80);')
        book.click()

        window_with_book = self.student.driver.window_handles[1]
        self.student.driver.switch_to_window(window_with_book)
        assert('book' in self.student.current_url()), \
            'Not viewing the textbook PDF'


        self.ps.test_updates['passed'] = True