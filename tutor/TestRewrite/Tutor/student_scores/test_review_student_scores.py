"""
System: tutor
Title: reviewing scores
User(s): teacher
Testrail ID: C148073



Jacob Diaz
7/28/17


Corresponding Case(s):
t2.10 06,07
t1.23 1,3,5 --> 11

Progress:
Written

Work to be done/Questions:
test, update and add where needed

-the way it is there might not be any assignments to look at under student
scores
-how are we going to ensure that there are?
-do we just have to test on teachers whose students have worked assignments?
-or do we automate the work ourselves to ensure that there is data to work
with?

Merge-able with any scripts? If so, which? :


"""

import json
import os
import pytest
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
from selenium.webdriver.support.ui import WebDriverWait
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
        1
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
        self.wait = WebDriverWait(self.student.driver, Assignment.WAIT_TIME)

        self.teacher.login()

        # go to student scores
        self.teacher.select_course(appearance='biology')
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

    @pytest.mark.skipif(str(1) not in TESTS, reason='Excluded')
    def test_review_student_scores(self):
        '''
        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the teacher user account [ teacher01 | password ] in the username
        and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a Tutor course name

        Click "Student Scores" from the calendar dashboard
        ***The user is presented with scores at due date (t2.10.06)***

        Click on the orange flag in the upper right corner of a progress cell
        for the desired student
        ***The user is presented with the current score (t2.10.07)***

        Period tabs are displayed
        ***Period tabs are displayed (t1.23.02)***

        Click on the tab for the desired period
        ***Scores for selected period are displayed in table (t1.23.01)***

        Click on the name of an arbitrary student
        ***Performance Forecast for selected student is displayed (t1.23.05)***

        Click on the name of the student to open a drop down menu
        In the drop down menu click the name of selected student
        ***Performance Forecast for second selected student is displayed
        (t1.23.06)***

        Click on the info icon next to the student's name
        ***Information about Performance Forecast is displayed. (t1.23.07)***

        Click on the "Return to Scores" button
        ***User at Student scores page on the first tab (t1.23.08)***

        Click on "Student Name" on the table [this will make the names in
        reverse alphabetical order by last name]
        Click on "Student Name" on the table again [this will make the names in
        alphabetical order by last name]
        ***The students are sorted alphabetically by last name. (t1.23.09)***

        Click "Progress" button
        ***Students are sorted by completion of selected assignment.
        (t1.23.10)***

        Click on the tab for selected section
        ***Due date for selected assignment is displayed in the cell below the
        assignment name (t1.23.011)***

        Corresponds to...
        t2.10 06,07
        t1.23 1,3,5 --> 11
        '''

        # t1.23.01 --> Scores for selected period are displayed in table
        assert ('scores' in self.teacher.current_url()), \
            'Not viewing Student Scores'

        # (t1.23.02) --> Period tabs are displayed
        current_period = 0
        period_tabs = self.teacher.wait.until(
            expect.visibility_of_elements_located(
                (By.XPATH, '//span[contains(@class, "tab-item-period-name")]')
            )
        )
        period_tabs[current_period+1].click()

        # DO SOMETHING HERE TO WAIT FOR THIS TO BE CLICKABLE
        period_tabs[current_period].click()

        # (t2.10.06) -->  The user is presented with scores at due date
        #  Test steps and verification assertions
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="course-scores-container"]')
            )
        )

        # t2.10.07 --> The user is presented with the current score
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
                late_caret = self.teacher.find(
                    By.XPATH, '//div[@class="late-caret accepted"]'
                )
                late_caret.click()
                pie_progress = late_caret.findElement(
                    By.XPATH,
                    "/..//svg[contains(@class,'pie-progress')]"
                )
                print(pie_progress)

                # self.teacher.find(
                #     By.XPATH,
                #     '//div[contains(@class,"late-status")]' +
                #     '//span[text()="due date"]'
                # )
                # break
            except (NoSuchElementException,
                    ElementNotVisibleException,
                    WebDriverException):
                bar += scroll_width
                if scroll_total_size <= bar:
                    print("No Late assignments for this class :(")
                    raise Exception
                # drag scroll bar instead of scrolling
                actions = ActionChains(self.teacher.driver)
                actions.move_to_element(scroll_bar)
                actions.click_and_hold()
                actions.move_by_offset(scroll_width, 0)
                actions.release()
                actions.perform()

        # t1.23.05 --> Performance Forecast for selected student is displayed
        # Test steps and verification assertions
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                    '//a[contains(@class,"name-cell")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.presence_of_element_located((
                By.XPATH,
                '//span[contains(text(), "Performance Forecast for")]'
            ))
        )

        # (t1.23.06) --> Performance Forecast for second selected student is
        # displayed
        self.teacher.find(By.ID, 'student-selection').click()
        student_select = self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//a[contains(@role, "menuitem")]' +
                 '//span[contains(@class,"-name")]')
            )
        )

        student_name = student_select.text
        student_select.click()

        self.teacher.wait.until(expect.presence_of_element_located((
            By.XPATH, '//span[contains(text(), "' + student_name + '")]'))
        )

        # (t1.23.07 --> Information about Performance Forecast is displayed.
        self.teacher.find(
            By.XPATH, '//button[contains(@class,"info-link")]').click()
        self.teacher.driver.find_element(
            By.XPATH, '//div[contains(@class,"tooltip-inner")]')

        # (t1.23.08 --> User at Student scores page on the first tab
        self.teacher.find(
            By.LINK_TEXT, 'Return to Scores').click()

        assert('scores' in self.teacher.current_url()), \
            'Not viewing Student Scores'

        # NOTE: ## signifies the selectors that possibly need editing

        # (t1.23.09 --> The students are sorted alphabetically by last name.

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(text(),"Name and Student ID")]')
            )
        ).click()

        # WATCH OUT-- THERE'S MULTIPLE HEADER-CELLS
        self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"header-row")]' +
            '//div[contains(@class,"is-descending")]')

        # self.teacher.find(
        #     By.XPATH, '//div[contains(text(),"Name and Student ID")]')
        # .click() ##
        #
        #
        # self.teacher.find(
        #     By.XPATH,
        #     '//div[contains(@class,"header-cell")]' +
        #     '//div[contains(@class,"is-ascending")]')

        # t1.23.10 --> Students are sorted by completion of selected
        # assignment.

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[contains(@class,"scores-cell")]' +
                 '//div[contains(text(),"Progress")]')
            )
        ).click()

        self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"scores-cell")]' +
            '//div[contains(@class,"is-descending")]')

        # self.teacher.driver.find_element(
        #     By.XPATH,
        #     '//div[contains(@class,"scores-cell")]' + ##
        #     '//div[contains(text(),"Progress")]' ##
        # ).click()
        # self.teacher.driver.find_element(
        #     By.XPATH,
        #     '//div[contains(@class,"scores-cell")]' + ##
        #     '//div[contains(@class,"is-ascending")]') ##

        # t1.23.11 --> Due date for selected assignment is displayed in
        # the cell below the assignment name

        assignment_cell = self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@data-assignment-type,"reading")]')
            )
        )
        assignment_cell.find_element(
            By.XPATH,
            '//following-sibling::div[contains(@class,"due")]'
        )
