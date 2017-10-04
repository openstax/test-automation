"""
System: exercises
Title: start reading assignment
User(s): student
Testrail ID: C148103


Jacob Diaz
7/28/17


Corresponding Case(s):
    t1.28.21


Progress:
Not written code yet

Work to be done/Questions:
Write code, test

Merge-able with any scripts? If so, which? :
Perhaps work a reading?

"""

# import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
# from random import randint
# from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
# from staxing.assignment import Assignment

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Student, Teacher

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
        1
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestWorkAReading(unittest.TestCase):
    """T1.28 - Work a reading."""

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
                pasta_user=self.ps,
                existing_driver=self.student.driver,
                capabilities=self.desired_capabilities
            )
        else:
            self.student = Student(
                use_env_vars=True,
            )
            self.teacher = Teacher(
                use_env_vars=True
            )
        self.teacher.login()

        # Create a reading for the student to work
        self.teacher.select_course(appearance='physics')
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(
            By.PARTIAL_LINK_TEXT, 'Add Reading').click()
        assert('readings/new' in self.teacher.current_url()), \
            'Not on the add a reading page'

        self.teacher.find(
            By.XPATH, "//input[@id = 'reading-title']").send_keys('Epic 28')
        self.teacher.find(
            By.XPATH, "//textarea[@class='form-control empty']").send_keys(
            "instructions go here")
        self.teacher.find(
            By.XPATH, "//input[@id = 'hide-periods-radio']").click()

        # Choose the first date calendar[0], second is calendar[1]
        # and set the open date to today
        self.teacher.driver.find_elements_by_xpath(
            "//div[@class = 'datepicker__input-container']")[0].click()
        self.teacher.driver.find_element_by_xpath(
            "//div[@class = 'datepicker__day datepicker__day--today']").click()

        # Choose the second date calendar[1], first is calendar[0]
        self.teacher.driver.find_elements_by_xpath(
            "//div[@class = 'datepicker__input-container']")[1].click()
        while(self.teacher.find(
            By.XPATH,
            "//span[@class = 'datepicker__current-month']"
        ).text != 'December 2016'):
            self.teacher.find(
                By.XPATH,
                "//a[@class = 'datepicker__navigation datepicker__" +
                "navigation--next']").click()

        # Choose the due date of December 31, 2016
        weekends = self.teacher.driver.find_elements_by_xpath(
            "//div[@class = 'datepicker__day datepicker__day--weekend']")
        for day in weekends:
            if day.text == '31':
                due = day
                due.click()
                break

        # Choose reading sections, pick physics chapter 6 since it has a video
        self.teacher.find(
            By.XPATH, "//button[@id='reading-select']").click()
        self.teacher.driver.find_elements_by_xpath(
            "//span[@class='chapter-checkbox']")[5].click()
        self.teacher.find(
            By.XPATH,
            "//button[@class='-show-problems btn btn-primary']").click()
        self.teacher.sleep(10)

        # Publish the assignment
        self.teacher.find(
            By.XPATH,
            "//button[@class='async-button -publish btn btn-primary']").click()
        self.teacher.sleep(60)

        self.student.login()

    def tearDown(self):
        """Test destructor."""
        if not LOCAL_RUN:
            self.ps.update_job(
                job_id=str(self.student.driver.session_id),
                **self.ps.test_updates
            )
        try:
            # Delete the assignment
            assert('calendar' in self.teacher.current_url()), \
                'Not viewing the calendar dashboard'

            spans = self.teacher.driver.find_elements_by_tag_name('span')
            for element in spans:
                if element.text.endswith('2016'):
                    month = element

            # Change the calendar date if necessary
            while (month.text != 'December 2016'):
                self.teacher.find(
                    By.XPATH,
                    "//a[@class = 'calendar-header-control next']").click()

            # Select the newly created assignment and delete it
            assignments = self.teacher.driver.find_elements_by_tag_name(
                'label')
            for assignment in assignments:
                if assignment.text == 'Epic 28':
                    assignment.click()
                    self.teacher.find(
                        By.XPATH,
                        "//a[@class='btn btn-default -edit-assignment']"
                    ).click()
                    self.teacher.find(
                        By.XPATH,
                        "//button[@class='async-button delete-link " +
                        "pull-right btn btn-default']").click()
                    self.teacher.find(
                        By.XPATH, "//button[@class='btn btn-primary']").click()
                    self.teacher.sleep(5)
                    break
        except:
            pass
        try:
            self.teacher.driver.refresh()
            self.teacher.sleep(5)

            self.teacher = None
            self.student.delete()
        except:
            pass

    @pytest.mark.skipif(str(1) not in TESTS, reason='Excluded')
    def test_start_reading_assignment_student(self):
        """
        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the student user account [ student04 | password ] in the username
        and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a Tutor course name
        Click on a reading assignment under the tab "This Week" on the
        dashboard
        Click the "Continue" button
        On a card with a free response assessment, enter a free response into
        the free response assessment text box
        Click the "Answer" button
        Select a multiple choice answer
        Click the "Submit" button in the left corner of the footer

        Click on the course name in the upper left corner of the page
        OR
        Click the user menu
        Click the "Dashboard" button
        ***The user returns to dashboard and the reading is marked "In
        Progress" in the dashboard progress column (t1.28.21)***

        Corresponds to...
        t1.28.21
        :return:
        """

    # POSSIBLY GROUP WITH ANOTHER TEST --> THIS IS VERY SMALL
