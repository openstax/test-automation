"""Tutor v1, Epic 48 - Work an external assignment."""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
# from random import randint
from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as expect
# from staxing.assignment import Assignment

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Student

# for template command line testing only
# - replace list_of_cases on line 31 with all test case IDs in this file
# - replace CaseID on line 52 with the actual cass ID
# - delete lines 17 - 22
list_of_cases = 0
CaseID = 0

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
        8281, 8282, 8283, 8284, 8285,
        8286
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestEpicName(unittest.TestCase):
    """T1.48 - Work an external assignment."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.student = Student(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        self.student.login()

    def tearDown(self):
        """Test destructor."""
        self.ps.update_job(
            job_id=str(self.student.driver.session_id),
            **self.ps.test_updates
        )
        try:
            self.student.delete()
        except:
            pass

    # Case C8281 - 001 - Student | Click on an external assignment
    @pytest.mark.skipif(str(8281) not in TESTS, reason='Excluded')
    def test_student_click_on_a_external_assignment_8281(self):
        """Click on an external assignment.

        Steps:
        Click on an external assignment under the tab "This Week"
        on the dashboard

        Expected Result:
        The user is presented with the assignment link and instructions
        """
        self.ps.test_updates['name'] = 't1.48.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.48',
            't1.48.001',
            '8281'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.select_course(appearance='physics')
        assert('list' in self.student.current_url()), \
            'Not viewing the calendar dashboard'

        assignments = self.student.driver.find_elements_by_tag_name("time")
        for assignment in assignments:
            if (assignment.text == 'Jun 05, 2:34am'):
                assignment.click()
                break

        assert('tasks' in self.student.current_url()), \
            'Not viewing assignment page'

        assert('steps' in self.student.current_url()), \
            'Not viewing assignment page'

        self.ps.test_updates['passed'] = True

    # Case C8282 - 002 - Student | Read the directions below the assignment
    # link or hover over the info icon in the footer
    @pytest.mark.skipif(str(8282) not in TESTS, reason='Excluded')
    def test_student_read_directions_below_or_hover_over_info_icon_8282(self):
        """Read directions below assignment link or hover over the info icon.

        Steps:
        Click on an external assignment under the tab "This Week"
        on the dashboard
        Hover the cursor over the info icon in the footer

        Expected Result:
        The user is presented with the directions for the assignment
        """
        self.ps.test_updates['name'] = 't1.48.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.48',
            't1.48.002',
            '8282'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.select_course(appearance='physics')
        assert('list' in self.student.current_url()), \
            'Not viewing the calendar dashboard'

        assignments = self.student.driver.find_elements_by_tag_name("time")
        for assignment in assignments:
            if (assignment.text == 'Jun 05, 2:34am'):
                assignment.click()
                break

        assert('tasks' in self.student.current_url()), \
            'Not viewing assignment page'

        assert('steps' in self.student.current_url()), \
            'Not viewing assignment page'

        instructions = self.student.driver.find_elements_by_tag_name("p")
        flag = False
        for instruction in instructions:
            if (instruction.text == 'instructions go here'):
                flag = True
                break

        assert(flag), \
            'Did not read instructions'

        self.ps.test_updates['passed'] = True

    # Case C8283 - 003 - Student | Click the assignment link
    @pytest.mark.skipif(str(8283) not in TESTS, reason='Excluded')
    def test_student_click_the_assignment_link_8283(self):
        """Click the assignment link.

        Steps:
        Click on an external assignment under the tab "This Week"
        on the dashboard
        Click on the link to the external assignment

        Expected Result:
        The user is presented with the external assignment
        """
        self.ps.test_updates['name'] = 't1.48.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.48',
            't1.48.003',
            '8283'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.select_course(appearance='physics')
        assert('list' in self.student.current_url()), \
            'Not viewing the calendar dashboard'

        assignments = self.student.driver.find_elements_by_tag_name("time")
        for assignment in assignments:
            if (assignment.text == 'Jun 05, 2:34am'):
                assignment.click()
                break

        assert('tasks' in self.student.current_url()), \
            'Not viewing assignment page'

        assert('steps' in self.student.current_url()), \
            'Not viewing assignment page'

        link = self.student.driver.find_element_by_link_text(
            'due in a long time')
        original = self.student.current_url()
        self.student.driver.get(link.get_attribute("href"))

        assert('google' in self.student.current_url()), \
            'Not viewing assignment link'

        self.student.sleep(5)
        self.student.driver.get(original)

        assert('tasks' in self.student.current_url()), \
            'Not viewing assignment page'

        assert('steps' in self.student.current_url()), \
            'Not viewing assignment page'

        self.ps.test_updates['passed'] = True

    # Case C8284 - 004 - Student | Close the assignment tab or window
    @pytest.mark.skipif(str(8284) not in TESTS, reason='Excluded')
    def test_student_close_the_assignment_8284(self):
        """Close the assignment tab or window.

        Steps:
        Click on an external assignment under the tab "This Week"
        on the dashboard
        Click on the link to the external assignment
        Close the assignment tab

        Expected Result:
        The assignment tab is closed and the user is presented with the
        external assignment link and instructions on Tutor
        """
        self.ps.test_updates['name'] = 't1.48.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.48',
            't1.48.004',
            '8284'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.select_course(appearance='physics')
        assert('list' in self.student.current_url()), \
            'Not viewing the calendar dashboard'

        assignments = self.student.driver.find_elements_by_tag_name("time")
        for assignment in assignments:
            if (assignment.text == 'Jun 05, 2:34am'):
                assignment.click()
                break

        assert('tasks' in self.student.current_url()), \
            'Not viewing assignment page'

        assert('steps' in self.student.current_url()), \
            'Not viewing assignment page'

        link = self.student.driver.find_element_by_link_text(
            'due in a long time')
        original = self.student.current_url()
        self.student.driver.get(link.get_attribute("href"))

        assert('google' in self.student.current_url()), \
            'Not viewing assignment link'

        self.student.sleep(5)
        self.student.driver.get(original)

        assert('tasks' in self.student.current_url()), \
            'Not viewing assignment page'

        assert('steps' in self.student.current_url()), \
            'Not viewing assignment page'

        self.ps.test_updates['passed'] = True

    # Case C8285 - 005 - Student | Click the Back To Dashboard button to
    # finish the assignment
    @pytest.mark.skipif(str(8285) not in TESTS, reason='Excluded')
    def test_student_click_back_to_dashboard_button_8285(self):
        """Click the Back To Dashboard button to finish the assignment.

        Steps:
        Click on an external assignment under the tab "This Week"
        on the dashboard
        Click on the link to the external assignment
        Close the assignment tab
        Click "Back To Dashboard"

        Expected Result:
        The user is presented with the dashboard
        """
        self.ps.test_updates['name'] = 't1.48.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.48',
            't1.48.005',
            '8285'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.select_course(appearance='physics')
        assert('list' in self.student.current_url()), \
            'Not viewing the calendar dashboard'

        assignments = self.student.driver.find_elements_by_tag_name("time")
        for assignment in assignments:
            if (assignment.text == 'Jun 05, 2:34am'):
                assignment.click()
                break

        assert('tasks' in self.student.current_url()), \
            'Not viewing assignment page'

        assert('steps' in self.student.current_url()), \
            'Not viewing assignment page'

        link = self.student.driver.find_element_by_link_text(
            'due in a long time')
        original = self.student.current_url()
        self.student.driver.get(link.get_attribute("href"))

        assert('google' in self.student.current_url()), \
            'Not viewing assignment link'

        self.student.sleep(5)
        self.student.driver.get(original)

        assert('tasks' in self.student.current_url()), \
            'Not viewing assignment page'

        assert('steps' in self.student.current_url()), \
            'Not viewing assignment page'

        self.student.find(By.LINK_TEXT, 'Back To Dashboard').click()

        assert('list' in self.student.current_url()), \
            'Not viewing the calendar dashboard'

        self.student.sleep(5)

        self.ps.test_updates['passed'] = True

    # Case C8286 - 006 - Student | Verify the assignment status as Clicked
    @pytest.mark.skipif(str(8286) not in TESTS, reason='Excluded')
    def test_student_verify_assignment_status_as_clicked_8286(self):
        """Verify the assignment status as Clicked.

        Steps:
        Click on an external assignment under the tab "This Week"
        on the dashboard
        Click on the link to the external assignment
        Close the assignment tab
        Click "Back To Dashboard"

        Expected Result:
        The external assignment is marked as "Clicked" in the Progress column
        on the dashboard
        """
        self.ps.test_updates['name'] = 't1.48.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.48',
            't1.48.006',
            '8286'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.select_course(appearance='physics')
        assert('list' in self.student.current_url()), \
            'Not viewing the calendar dashboard'

        assignments = self.student.driver.find_elements_by_tag_name("time")
        for assignment in assignments:
            if (assignment.text == 'Jun 05, 2:34am'):
                assignment.click()
                break

        assert('tasks' in self.student.current_url()), \
            'Not viewing assignment page'

        assert('steps' in self.student.current_url()), \
            'Not viewing assignment page'

        link = self.student.driver.find_element_by_link_text(
            'due in a long time')
        original = self.student.current_url()
        self.student.driver.get(link.get_attribute("href"))

        assert('google' in self.student.current_url()), \
            'Not viewing assignment link'

        self.student.sleep(5)
        self.student.driver.get(original)

        assert('tasks' in self.student.current_url()), \
            'Not viewing assignment page'

        assert('steps' in self.student.current_url()), \
            'Not viewing assignment page'

        self.student.find(By.LINK_TEXT, 'Back To Dashboard').click()

        assert('list' in self.student.current_url()), \
            'Not viewing the calendar dashboard'

        externals = self.student.driver.find_elements_by_xpath(
            "//div[@class = 'task row external workable']")

        for assignment in externals:
            if assignment.text.find("Clicked") >= 0 \
                    and assignment.text.find("Jun 05, 2:34am") >= 0:
                self.ps.test_updates['passed'] = True
                break
