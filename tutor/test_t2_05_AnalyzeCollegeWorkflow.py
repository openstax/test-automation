"""Tutor v2, Epic 5 - Analyze College Workflow."""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
# from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
# from staxing.assignment import Assignment
from selenium.webdriver import ActionChains

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
        14645, 14646, 14647, 14648, 14649,
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestAnalyzeCollegeWorkflow(unittest.TestCase):
    """T2.05 - Analyze College Workflow."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
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
        self.student.select_course(appearance='physics')
        assert('list/' in self.student.current_url()), \
            'Not viewing the calendar dashboard'

        self.student.sleep(5)

        page = self.student.driver.page_source
        assert('Coming Up' in page or 'No upcoming events' in page), \
            'No Coming Up/No upcoming events text is visible/present'

        self.ps.test_updates['passed'] = True

    # 14646 - 002 - Teacher | Create a link to the OpenStax Dashboard
    @pytest.mark.skipif(str(14646) not in TESTS, reason='Excluded')
    def test_teacher_create_a_link_to_the_openstax_dashboard_14646(self):
        """Create a link to the OpenStax Dashboard.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.05.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.05',
            't2.05.002',
            '14646'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 14647 - 003 - Teacher | Create a link to the OpenStax Dashboard
    @pytest.mark.skipif(str(14647) not in TESTS, reason='Excluded')
    def test_teacher_create_a_link_to_the_openstax_dashboard_14647(self):
        """Create a link to the OpenStax Dashboard.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.05.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.05',
            't2.05.003',
            '14647'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 14648 - 004 - Teacher | Create links to assigned readings in their LMS
    @pytest.mark.skipif(str(14648) not in TESTS, reason='Excluded')
    def test_teacher_create_links_to_assigned_readings_in_lms_14648(self):
        """Create links to assigned readings in their LMS.

        Steps:
        Go to Tutor
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a CC course name
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

        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Reading').click()
        assert('readings' in self.teacher.current_url()), \
            'Not on the add a homework page'

        self.teacher.find(
            By.XPATH, "//input[@id = 'reading-title']").send_keys('Epic 5-4')
        self.teacher.find(
            By.XPATH, "//input[@id = 'hide-periods-radio']").click()

        # Choose the second date calendar[1], first is calendar[0]
        self.teacher.driver.find_elements_by_xpath(
            "//div[@class = 'datepicker__input-container']")[1].click()
        while(self.teacher.find(
            By.XPATH,
            "//span[@class = 'datepicker__current-month']"
        ).text != 'December 2016'):
            self.teacher.find(
                By.XPATH, "//a[@class = 'datepicker__navigation datepicker__" +
                "navigation--next']").click()

        # Choose the due date of December 31, 2016
        weekends = self.teacher.driver.find_elements_by_xpath(
            "//div[@class = 'datepicker__day datepicker__day--weekend']")
        for day in weekends:
            if day.text == '31':
                due = day
                due.click()
                break

        self.teacher.sleep(3)

        # Choose reading sections
        self.teacher.find(
            By.XPATH, "//button[@id='reading-select']").click()
        self.teacher.find(
            By.XPATH, "//span[@class = 'chapter-checkbox']").click()
        self.teacher.find(
            By.XPATH,
            "//button[@class='-show-problems btn btn-primary']").click()
        self.teacher.sleep(10)

        # Publish the assignment
        self.teacher.driver.execute_script('window.scrollBy(0, -200);')
        self.teacher.find(
            By.XPATH,
            "//button[@class='async-button -publish btn btn-primary']").click()

        # Give the assignment time to publish
        self.teacher.sleep(60)

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

        # Select the newly created assignment, get the LMS link, and delete it
        assignments = self.teacher.driver.find_elements_by_tag_name('label')
        for assignment in assignments:
            if assignment.text == 'Epic 5-4':
                assignment.click()
                self.teacher.find(
                    By.PARTIAL_LINK_TEXT, "Get assignment link").click()
                self.teacher.find(
                    By.XPATH,
                    "//div[@class = 'fade in lms-sharable-link popover top']")
                self.teacher.sleep(5)
                self.teacher.find(
                    By.XPATH,
                    "//a[@class='btn btn-default -edit-assignment']").click()
                self.teacher.sleep(5)
                self.teacher.find(
                    By.XPATH,
                    "//button[@class='async-button delete-link pull-" +
                    "right btn btn-default']").click()
                self.teacher.find(
                    By.XPATH, "//button[@class='btn btn-primary']").click()
                self.teacher.sleep(5)
                break

        self.teacher.driver.refresh()
        deleted = True

        # Verfiy the assignment was deleted
        spans = self.teacher.driver.find_elements_by_tag_name('span')
        for element in spans:
            if element.text.endswith('2016'):
                month = element

        while (month.text != 'December 2016'):
            self.teacher.find(
                By.XPATH,
                "//a[@class = 'calendar-header-control next']").click()

        assignments = self.teacher.driver.find_elements_by_tag_name('label')
        for assignment in assignments:
            if assignment.text == 'Epic 5-4':
                deleted = False
                break

        if deleted:
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

        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks' in self.teacher.current_url()), \
            'Not on the add a homework page'

        self.teacher.find(
            By.XPATH, "//input[@id = 'reading-title']").send_keys('Epic 5-5')
        self.teacher.find(
            By.XPATH, "//input[@id = 'hide-periods-radio']").click()

        # Choose the second date calendar[1], first is calendar[0]
        self.teacher.driver.find_elements_by_xpath(
            "//div[@class = 'datepicker__input-container']")[1].click()
        while(self.teacher.find(
            By.XPATH,
            "//span[@class = 'datepicker__current-month']"
        ).text != 'December 2016'):
            self.teacher.find(
                By.XPATH, "//a[@class = 'datepicker__navigation datepicker__" +
                "navigation--next']").click()

        # Choose the due date of December 31, 2016
        weekends = self.teacher.driver.find_elements_by_xpath(
            "//div[@class = 'datepicker__day datepicker__day--weekend']")
        for day in weekends:
            if day.text == '31':
                due = day
                due.click()
                break

        self.teacher.sleep(3)

        # Open the select problem cards
        self.teacher.find(
            By.XPATH, "//button[@id = 'problems-select']").click()
        self.teacher.find(
            By.XPATH, "//span[@class = 'chapter-checkbox']").click()
        self.teacher.find(
            By.XPATH,
            "//button[@class='-show-problems btn btn-primary']").click()
        self.teacher.sleep(10)

        # Choose a problem for the assignment
        element = self.teacher.find(
            By.XPATH, "//div[@class = 'controls-overlay'][1]")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(element)
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action include']").click()
        self.teacher.find(
            By.XPATH,
            "//button[@class='-review-exercises btn btn-primary']").click()
        self.teacher.sleep(2)

        # Publish the assignment
        self.teacher.driver.execute_script('window.scrollBy(0, -200);')
        self.teacher.find(
            By.XPATH,
            "//button[@class='async-button -publish btn btn-primary']").click()

        # Give the assignment time to publish
        self.teacher.sleep(60)

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

        # Select the newly created assignment, get the LMS link, and delete it
        assignments = self.teacher.driver.find_elements_by_tag_name('label')
        for assignment in assignments:
            if assignment.text == 'Epic 5-5':
                assignment.click()
                self.teacher.find(
                    By.PARTIAL_LINK_TEXT, "Get assignment link").click()
                self.teacher.find(
                    By.XPATH,
                    "//div[@class = 'fade in lms-sharable-link popover top']")
                self.teacher.sleep(5)
                self.teacher.find(
                    By.XPATH,
                    "//a[@class='btn btn-default -edit-assignment']").click()
                self.teacher.sleep(5)
                self.teacher.find(
                    By.XPATH,
                    "//button[@class='async-button delete-link pull-" +
                    "right btn btn-default']").click()
                self.teacher.find(
                    By.XPATH, "//button[@class='btn btn-primary']").click()
                self.teacher.sleep(5)
                break

        self.teacher.driver.refresh()
        deleted = True

        # Verfiy the assignment was deleted
        spans = self.teacher.driver.find_elements_by_tag_name('span')
        for element in spans:
            if element.text.endswith('2016'):
                month = element

        while (month.text != 'December 2016'):
            self.teacher.find(
                By.XPATH,
                "//a[@class = 'calendar-header-control next']").click()

        assignments = self.teacher.driver.find_elements_by_tag_name('label')
        for assignment in assignments:
            if assignment.text == 'Epic 5-5':
                deleted = False
                break

        if deleted:
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
