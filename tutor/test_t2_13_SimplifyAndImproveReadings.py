"""Tutor v2, Epic 13 - Simplify and Improve Readings."""

import inspect
import json
import os
import pytest
import unittest
import datetime

from autochomsky import chomsky
from pastasauce import PastaSauce, PastaDecorator
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
# from staxing.assignment import Assignment

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Teacher, Student

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': '50.0',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([
        14745, 14746
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestSimplifyAndImproveReadings(unittest.TestCase):
    """T2.13 - Simplify and Improve Readings."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.teacher = Teacher(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        # create a reading for the student to work
        self.teacher.login()
        self.assignment_name = 't1.18 reading-%s' % randint(100, 999)
        today = datetime.date.today()
        begin = today.strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=randint(1, 10))) \
            .strftime('%m/%d/%Y')
        self.teacher.add_assignment(
            assignment='reading',
            args={
                'title': self.assignment_name,
                'description': chomsky(),
                'periods': {'all': (begin, end)},
                'reading_list': ['1.1', '1.2'],
                'status': 'publish',
            }
        )
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"calendar-container")]')
            )
        )
        self.teacher.logout()
        # login as a student to work the reading
        self.student = Student(
            existing_driver=self.teacher.driver,
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        self.student.login()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'This Week')
            )
        )
        reading = self.student.driver.find_element(
            By.XPATH,
            '//span[text()="%s"]' % self.assignment_name
        )
        self.teacher.driver.execute_script(
            'return arguments[0].scrollIntoView();',
            reading
        )
        self.teacher.driver.execute_script('window.scrollBy(0, -80);')
        reading.click()

    def tearDown(self):
        """Test destructor."""
        self.ps.update_job(
            job_id=str(self.teacher.driver.session_id),
            **self.ps.test_updates
        )
        self.student = None
        try:
            self.teacher.delete()
        except:
            pass

    # 14745 - 001 - Student | Relative size and progress are displayed while
    # working a reading assignment
    @pytest.mark.skipif(str(14745) not in TESTS, reason='Excluded')
    def test_student_relative_size_and_progress_are_displayed_whil_14745(self):
        """Size and progress are displayed while working a reading.

        Steps:
        Go to Tutor
        Click on the 'Login' button
        Enter the student user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a Tutor course name
        Click on a reading assignment
        Click on the right arrow

        Expected Result:
        The progress bar at the top reflects how far along you are as you work
        through the reading assignment
        """
        self.ps.test_updates['name'] = 't2.13.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t2', 't2.13', 't2.13.001', '14745']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"progress-bar progress-bar-success")]')

        self.ps.test_updates['passed'] = True

    # 14746 - 002 - Student | Access prior milestones in the reading assignment
    # with breadcrumbs
    @pytest.mark.skipif(str(14746) not in TESTS, reason='Excluded')
    def test_student_access_prior_milestones_in_the_reading_assign_14746(self):
        """Access prior milestones in the reading assignment with breadcrumbs.

        Steps:
        If the user has more than one course, click on a Tutor course name
        Click on a reading assignment
        Click on the icon next to the calendar on the header

        Expected Result:
        The user is presented with prior milestones
        """
        self.ps.test_updates['name'] = 't2.13.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t2', 't2.13', 't2.13.002', '14746']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.find(By.CSS_SELECTOR, 'a.paging-control.next').click()
        self.student.sleep(1)
        self.student.find(By.CSS_SELECTOR, 'a.milestones-toggle').click()
        self.student.sleep(1)
        cards = self.student.find_all(
            By.CSS_SELECTOR,
            'div[class="milestone"]'
        )
        preview = ''
        if not isinstance(cards, list):
            preview = cards.find_element(
                By.XPATH,
                '/div[@class="milestone-preview"]'
            ).text
            cards.click()
        else:
            card = randint(0, len(cards) - 1)
            preview = cards[card].find_element(
                By.XPATH,
                '/div[@class="milestone-preview"]'
            ).text
            cards[card].click()
        # Issue: section titles are not in the content
        preview

        self.ps.test_updates['passed'] = True
