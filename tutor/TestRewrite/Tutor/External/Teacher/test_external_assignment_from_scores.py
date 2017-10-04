"""
System: Tutor
Title: go to external assignment from student scores
User(s): Teacher
Testrail ID: C148072



Jacob Diaz
7/28/17


Corresponding Case(s):
        t1.23 15, 26


Progress:
Written


Work to be done/Questions:
Need to test and udpate

Merge-able with any scripts? If so, which? :


"""

# import inspect
import json
import os
# import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
# from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import WebDriverException

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Teacher
from staxing.assignment import Assignment

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
        162172, 162173, 162174, 162175, 162176,
        162177, 162178, 162179, 162180, 162181,
        162182, 162183, 162184, 162185, 162186,
        162187, 162188
        # 162188

    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestViewClassScores(unittest.TestCase):

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
        self.teacher.login()
        # go to student scores
        self.teacher.select_course(appearance='college_physics')
        self.teacher.driver.find_element(
            By.LINK_TEXT, 'Student Scores').click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[contains(text(), "Student Scores")]')
            )
        ).click()

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

    def TestExternalFromStudentScores(self):
        '''
        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a Tutor course name

        Click on the "Student Scores" button
        ***For external assignments the percentage of students who have clicked
        on the assignment is displayed.***
        (T1.23.15)


        Click on the tab for the chosen period
        Click on cell for chosen student and external assignment assignment
        ***Teacher view of student work shown. (Shows link to external
        assignment as a student would see it) (t1.23.26)***

        Corresponds to
        t1.23 15, 26
        '''
        # t1.23.15 --> For external assignments the percentage of students
        # who have clicked on the assignment is displayed

        scroll_bar = self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"ScrollbarLayout_faceHorizontal")]')
        scroll_width = scroll_bar.size['width']
        scroll_total_size = self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"ScrollbarLayout_mainHorizontal")]'
        ).size['width']

        bar = scroll_width
        while (bar < scroll_total_size):
            try:
                self.teacher.driver.find_element(
                    By.XPATH,
                    '//span[@class="click-rate"]')
                break
            except (NoSuchElementException,
                    ElementNotVisibleException,
                    WebDriverException):
                bar += scroll_width
                if scroll_total_size <= bar:
                    print("No readings for this class")
                    raise Exception
                # drag scroll bar instead of scrolling
                actions = ActionChains(self.teacher.driver)
                actions.move_to_element(scroll_bar)
                actions.click_and_hold()
                actions.move_by_offset(scroll_width, 0)
                actions.release()
                actions.perform()

        # t1.23.26 -->  Teacher view of student work shown.
        # (Shows link to external assignment as a student would see it)

        external_assignment = self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"external-cell")]' +
            '//span[contains(text(),"---")]')
        Assignment.scroll_to(self.teacher.driver, external_assignment)
        external_assignment.click()

        self.student.find(
            By.XPATH,
            '//div[contains(@class,"external-step")]'
        )
