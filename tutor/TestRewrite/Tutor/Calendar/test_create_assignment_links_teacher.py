"""
System: tutor
Title: create assignment links
User(s): teacher
Testrail ID: C148104


Jacob Diaz
7/28/17


Corresponding Case(s):
    t2.05.04 --> 05


Progress:
All written

Work to be done/Questions:
Test, update and add test cases where necessary

Merge-able with any scripts? If so, which? :


"""

# import inspect
import json
import os
import pytest
import unittest
import datetime

from pastasauce import PastaSauce, PastaDecorator
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
# from staxing.assignment import Assignment
# from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
# from selenium.common.exceptions import TimeoutException

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Teacher, Student

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

    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestAnalyzeCollegeWorkflow(unittest.TestCase):
    """T2.05 - Analyze College Workflow."""

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
            self.student = Student(
                use_env_vars=True,
                pasta_user=self.ps,
                capabilities=self.desired_capabilities,
                existing_driver=self.teacher.driver
            )
        else:
            self.teacher = Teacher(
                use_env_vars=True
            )
            self.student = Student(
                use_env_vars=True,
                existing_driver=self.teacher.driver
            )

    def tearDown(self):
        """Test destructor."""
        if not LOCAL_RUN:
            self.ps.update_job(
                job_id=str(self.teacher.driver.session_id),
                **self.ps.test_updates
            )
        self.student = None
        try:
            self.teacher.delete()
        except:
            pass

    @pytest.mark.skipif(str(1) not in TESTS, reason='Excluded')
    def test_create_assignment_links_teacher(self):
        """
        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Login to student account
        Click 'Next'
        Enter the teacher password [ password ] in the password text box
        Click on the 'Login' button
        If the user has more than one course, click on a Tutor course name
        Click on a published reading assignment on the calendar dashboard
        Click "Get Assignment Link"
        ***User is presented with links to assigned readings (t2.05.04)***

        Click on 'X' to get out of pop-up menu
        Click on a published homework assignment on the calendar dashboard
        ***Click "Get Assignment Link"
        User is presented with links to assigned homework (t2.05.05)***

        Expected Results:


        Corresponds to...
        t2.05.04 --> 05
        :return:
        """
        # t2.05.04 --> ser is presented with links to assigned readings
        # (t2.05.04)
        self.teacher.login()

        self.teacher.select_course(appearance='biology')
        assignment_name = 'reading004_%d' % (randint(100, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=4)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='reading',
                                    args={
                                         'title': assignment_name,
                                         'description': 'description',
                                         'periods': {'all': (begin, end)},
                                         'reading_list': ['1.1'],
                                         'status': 'publish'
                                     })
        try:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH,
                "//div/label[contains(text(), '" + assignment_name + "')]"
            ).click()
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, "//a[contains(@class, 'header-control next')]"
            ).click()
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH,
                "//div/label[contains(text(), '" + assignment_name + "')]"
            ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[@class="get-link"]')
            )
        ).click()
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.XPATH,
                 '//div[@class="popover-content"]' +
                 '//input[contains(@value,"https://tutor")]')
            )
        )

        # t2.05.05 --> Clicking "Get Assignment Link presents
        # user with links to assigned homework (t2.05.05)***

        # FIND A WAY TO GET BACK TO MY CURRENT COURSES PAGE (maybe use teacher
        # goto... method)

        self.teacher.select_course(appearance='biology')
        assignment_name = 'hw005_%d' % (randint(100, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=4)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='homework',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'problems': {'1.1': (2, 3), },
                                        'status': 'publish',
                                        'feedback': 'immediate'
                                     })
        try:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.sleep(1)
            self.teacher.find(
                By.XPATH,
                "//div/label[contains(text(), '" + assignment_name + "')]"
            ).click()
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, "//a[contains(@class, 'header-control next')]"
            ).click()
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH,
                "//div/label[contains(text(), '" + assignment_name + "')]"
            ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[@class="get-link"]')
            )
        ).click()
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.XPATH,
                 '//div[@class="popover-content"]' +
                 '//input[contains(@value,"https://tutor")]')
            )
        )
