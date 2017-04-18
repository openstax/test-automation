"""Tutor v2, Epic 5 - Analyze College Workflow."""

import inspect
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
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

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
        14645, 14648, 14649,
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

    # 14645 - 001 - Student | All work is visible for college students
    # not just "This Week"
    @pytest.mark.skipif(str(14645) not in TESTS, reason='Excluded')
    def test_student_all_work_is_visible_for_college_students_14645(self):
        """All work is visible for college students, not just 'This Week'.

        Steps:
        Log into tutor-qa as student
        Click on a college course

        Expected Result:
        Can view assignments due later than this week
        """
        self.ps.test_updates['name'] = 't2.05.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.05',
            't2.05.001',
            '14645'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.login()
        self.student.select_course(title='College Physics with Courseware')

        # find either upcoming events, or a message stating there are none.
        try:
            self.teacher.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH,
                     '//span[contains(text(),"%s")]' % "Coming Up")
                )
            )
        except TimeoutException:
            self.teacher.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH,
                     '//div[contains(text(),"%s")]' % "No upcoming events")
                )
            )
        self.ps.test_updates['passed'] = True

    '''
    # 14646 - 002 - Teacher | Create a link to the OpenStax Dashboard
    @pytest.mark.skipif(str(14646) not in TESTS, reason='Excluded')
    def test_teacher_create_a_link_to_the_openstax_dashboard_14646(self):
        """Create a link to the OpenStax Dashboard.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 't2.05.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t2', 't2.05', 't2.05.002', '14646']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
    '''

    '''
    # 14647 - 003 - Teacher | Create a link to the OpenStax Dashboard
    @pytest.mark.skipif(str(14647) not in TESTS, reason='Excluded')
    def test_teacher_create_a_link_to_the_openstax_dashboard_14647(self):
        """Create a link to the OpenStax Dashboard.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 't2.05.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t2', 't2.05', 't2.05.003', '14647']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
    '''

    # 14648 - 004 - Teacher | Create links to assigned readings in their LMS
    @pytest.mark.skipif(str(14648) not in TESTS, reason='Excluded')
    def test_teacher_create_links_to_assigned_readings_in_lms_14648(self):
        """Create links to assigned readings in their LMS.

        Steps:
        Login as a teacher
        If the user has more than one course, click on a tutor course name
        Click on a published reading assignment on the calendar dashboard
        Click "Get Assignment Link"

        Expected Result:
        The user is presented with links to assigned readings
        """
        self.ps.test_updates['name'] = 't2.05.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.05',
            't2.05.004',
            '14648'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
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
        self.ps.test_updates['passed'] = True

    # 14649 - 005 - Teacher | Create links to assigned homework in their LMS
    @pytest.mark.skipif(str(14649) not in TESTS, reason='Excluded')
    def test_teacher_create_links_to_assigned_homework_in_lms_14649(self):
        """Create links to assigned homework in their LMS.

        Steps:
        Go to Tutor
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a CC course name
        Click on a published homework assignment on the calendar dashboard
        Click "Get Assignment Link"

        Expected Result:
        The user is presented with links to assigned homework
        """
        self.ps.test_updates['name'] = 't2.05.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.05',
            't2.05.005',
            '14649'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()

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
        self.ps.test_updates['passed'] = True

    '''
    # 14650 - 006 - Teacher | View instructions on how to export summary grade
    # for my student's OpenStax practice to my LMS
    @pytest.mark.skipif(str(14650) not in TESTS, reason='Excluded')
    def test_teacher_view_instructions_on_how_to_export_summary_14650(self):
        """View instructions on how to export summary grade into LMS.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.05.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.05',
            't2.05.006',
            '14650'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
    '''
