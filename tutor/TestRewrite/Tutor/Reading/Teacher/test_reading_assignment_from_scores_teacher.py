"""
System:
Title: view reading assignments from scores
User(s): teacher
Testrail ID: C148070


Jacob Diaz
7/28/17


Corresponding Case(s):
t1.23. 12,16, 19, 20, 22, 24


Progress:
Not all written yet. Need to add t1.23.16
Run and add/update code

Work to be done/Questions:
Need to add t1.23.16
Run and add/update code
Add imports

Merge-able with any scripts? If so, which? :


"""
import json
import os
# import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
# from random import randint
from selenium.common.exceptions import NoSuchElementException, \
    ElementNotVisibleException, WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
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

    def TestReadingAssignments(self):
        '''
        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the teacher user account [ teacher01 | password ] in the username
        and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a Tutor course name

        Click on the "Review" button under the selected reading assignment.
        ***Displays students progress on chosen assignment for selected period,
        actual questions, and question results. (t1.23.12)***
        ***Complete, In Progress, and Not Started counts for selected period
        are displayed (t1.23.19)***
        ***Current Topics Performance and Spaced Practice Performance
         section numbers match the section breadcrumbs (t1.23.20)***

        Click on a breadcrumb of selected section of reading.
        ***Screen is moved down to selected section of reading. (t1.23.16)***

        Click on "View Student Text Responses" button for selected question
        ***List of student text responses for selected question is displayed.
        (t1.23.22)***

        Click on user menu for drop down
        Click on "Student Scores"
        Hover over cell for chosen student and reading assignment
        Click review in the popup
        ***Teacher view of student work shown. Teacher can go through different
        sections with side arrows or breadcrumbs. Only sections student has
        gone through are shown. (t1.23.24)***

        Expected Results:

        ***Corresponds to***
        t1.23. 12,16, 19, 20, 22, 24
        '''
        # t1.23.12 --> Displays students progress on chosen assignment for
        # selected period, actual questions, and question results.
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[contains(@class, "tab-item-period-name")]')
            )
        ).click()

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
                    '//span[contains(@class,"review-link wide")]' +
                    '//a[contains(text(),"Review")]'
                ).click()
                assert ('metrics' in self.teacher.current_url()), \
                    'Not viewing reading assignment summary'
                break
            except (NoSuchElementException,
                    ElementNotVisibleException,
                    WebDriverException):
                bar += scroll_width
                if scroll_total_size <= bar:
                    print("No readings for this class :(")
                    raise Exception
                # drag scroll bar instead of scrolling
                actions = ActionChains(self.teacher.driver)
                actions.move_to_element(scroll_bar)
                actions.click_and_hold()
                actions.move_by_offset(scroll_width, 0)
                actions.release()
                actions.perform()

        # t1.23.19 --> Complete, In Progress, and Not Started counts for
        # selected period are displayed
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//ul[contains(@role,"tablist")]' +
                 '//span[contains(@class,"tab-item-period-name")]')
            )
        )

        self.teacher.driver.find_element(
            By.XPATH, '//div[contains(@class,"stat complete")]' +
                      '//label[contains(text(),"Complete")]')
        self.teacher.driver.find_element(
            By.XPATH, '//div[contains(@class,"stat in-progress")]' +
                      '//label[contains(text(),"In Progress")]')
        self.teacher.driver.find_element(
            By.XPATH, '//div[contains(@class,"stat not-started")]' +
                      '//label[contains(text(),"Not Started")]')

        # T1.23.16 --> Screen is moved down to selected section of reading
        # MAYBE ADD T1.23.16 HERE??
        # I'M NOT SURE IF WOULD WORK --> ON LINE 766
        # SELECTING ON SECTIONS[-1] MIGHT MEAN IT WON'T WORK

        # t1.23.20 --> Current Topics Performance and
        # Spaced Practice Performance section numbers match the section
        # breadcrumbs

        sections = self.teacher.driver.find_elements(
            By.XPATH,
            '//label[contains(text(),"Current Topics")]/..' +
            '//div[contains(@class,"reading-progress")]' +
            '//span[contains(@class,"text-success")]')
        section_breadcrumbs = self.teacher.driver.find_elements(
            By.XPATH, '//span[contains(@class,"breadcrumbs")]')
        section_nums = []
        for x in section_breadcrumbs:
            section_nums.append(x.get_attribute("data-chapter"))
        for x in sections:
            assert (x.text in section_nums), \
                ("section and breadcrumb don't match: " + x.text)

        # ALMOST SURE THAT 23 IS A SUBCASE OF 19 -- VERIFY

        # only check against current topics because spaced Practice
        # will not be displayed in breadcrubms if no students have worked
        # problems from a section yet

        # t1.23.16 -->Screen is moved down to selected section of reading.

        sections = self.teacher.driver.find_elements(
            By.XPATH, '//span[contains(@class,"breadcrumbs")]')
        section = sections[-1]
        section.click()
        chapter = section.get_attribute("data-chapter")
        assert (self.teacher.driver.find_element(
            By.XPATH,
            '//span[contains(text(),"' + chapter + '")]').is_displayed()), \
            'chapter not displayed'

        # t1.23.22 -->List of student text responses for selected question is
        # displayed

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//a[contains(text(),"View student text responses")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="free-response"]')
            )
        ).click()

        # t1.23.24 -->
        # LOOKING BACK AT THIS CODE, I'M NOT SURE WHAT THIS ELEMNET IS SUPPOSED
        # TO BE
        '''element.click()
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(element)
        for _ in range(90):
            actions.move_by_offset(-1, 0)
        for _ in range(15):
            actions.move_by_offset(0, 1)
        actions.click()
        actions.perform()'''

        assert ('step' in self.teacher.current_url()), 'not at student work'
