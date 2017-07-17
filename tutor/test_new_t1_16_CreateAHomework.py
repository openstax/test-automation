"""Tutor v1, Epic 16 - Create A Homework."""

import datetime
import inspect
import json
import os
import pytest
import unittest
import random

from pastasauce import PastaSauce, PastaDecorator
from random import randint
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.ui import WebDriverWait
from staxing.assignment import Assignment
from staxing.helper import Teacher
from time import sleep

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
    str([ #301, 302, 303, 304, 305,
          310

    ])
)

@PastaDecorator.on_platforms(BROWSERS)
class TestCreateHomework(unittest.TestCase):
    """T1.16 Create a Homework."""

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
                use_env_vars = True
            )
        self.teacher.login()
        self.teacher.select_course(appearance='college_biology')

    def tearDown(self):
        """Test Destructor"""
        if not LOCAL_RUN:
            self.ps.update_job(
                job_id = str(self.teacher.driver.session_id),
                **self.ps.test_updates
            )
        try:
            self.teacher.delete()
        except:
            pass


    # Case C301 - Teacher | Add an open homework from sidebar
    @pytest.mark.skipif(str(301) not in TESTS, reason="Excluded")
    def test_teacher_create_and_publish_a_new_open_homework_from_sidebar(self):
        """
        Click on the Add Assignment menu on the user dashboard
        Click on the 'Add Homework' button
        ***The teacher is taken to the page where they create the assignment.***

        Edit the text box named 'Assignment name'
        ***Text is visible in the 'Assignment name' text box.***

        Edit the text box named 'Description or special instructions'
        ***Text is visible in the 'Description or special instructions' text box.***

        Select the 'All Periods' radio button if it is not selected by default
        Select an today's date as the open date for the assignment using the calendar element
        Type 00:00am as the open time for the assignment
        Select a due date in the future for the assignment using the calendar element

        Select an option on the 'Show feedback' drop down menu
        ***The option chosen is shown on the drop down menu.***

        Click the '+ Select Problems' button
        Select at least one chapter or section to use for the homework
        Click the 'Show Problems' button
        Click at least one problem to be used for My Selections
        Click the 'Next' button
        Click the 'Publish' button

        #Expected result
        ***The teacher is returned to the dashboard where the new assignment is displayed.***
        """
        self.ps.test_updates['name'] = \
            't1.16.001' + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.001', '8028']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'hw_001_%d' % randint(100, 999)
        assignment = Assignment()

        # Open Add Homework page
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(
            By.LINK_TEXT, 'Add Homework'
        ).click()
        assert ('homework/new' in self.teacher.current_url()), \
            'not at add homework page'

        # Find and fill in title
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        ).send_keys(assignment_name)

        # Fill in description
        self.teacher.find(
            By.XPATH, '//textarea[contains(@class, "form-control")]'
        ).send_keys('description')

        # Set due dates
        today = datetime.date.today()
        end = randint(1, 5)
        opens_on = today.strftime('%m/%d/%Y')  # make an open homework
        closes_on = (today + datetime.timedelta(days=end)) \
            .strftime('%m/%d/%Y')
        assignment.assign_periods(
            self.teacher.driver, {'all': (opens_on, closes_on)})

        # Add homework problems to the assignment
        assignment.add_homework_problems(
            self.teacher.driver, {'1.1': 3}
        )
        self.teacher.sleep(1)

        # Publish the homework
        publish_button = self.teacher.find(
            By.XPATH, '//button[contains(@class,"publish")]'
        )
        self.teacher.scroll_to(publish_button)
        publish_button.click()

        # Verify the homework is created
        try:
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(assignment_name)
            )
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH,
                '//a[contains(@class,"header-control next")]'
            ).click()
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(assignment_name)
            )

        self.ps.test_updates['passed'] = True

    # Case C302 - Teacher | Save a draft for individual periods
    @pytest.mark.skipif(str(302) not in TESTS, reason="Excluded")
    def test_teacher_save_a_draft_for_individual_periods(self):
        """
        # Steps
        Go to https://tutor-qa.openstax.org/
        Login with the user account [ teacher01 | staxly16 ]
        If the user has more than one course, select a Tutor course

        Click on the Add Assignment drop down menu on the user dashboard, OR
        click on a calendar date at least one day later than the current date
        Click on the 'Add Homework' button
        ***The teacher is taken to the page where they create the assignment.***

        Give the homework a name in the 'Assignment name' text box
        Select the 'Individual Periods' radio button
        Select the periods that should be required to complete the assignment
        Select open and due dates for each section using the calendar element
        ***Each section that is assigned the homework has an individual open
        and due date.*** (T1.15.004)

        Click the '+ Select Problems' button
        Select at least one chapter or section to use for the homework
        Click the 'Show Problems' button
        Click at least one problem to be used for My Selections
        Click the 'Next' button
        Click 'Save As Draft'

        #Expected result
        ***The teacher is returned to the dashboard where the draft assignment
        is now displayed on the calendar.***
        corresponds to T1.16.001, 004, 005
        """
        self.ps.test_updates['name'] = \
            't1.16.001' + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.001', '8028']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'hw_002_%d' % randint(100, 999)
        assignment = Assignment()

        # Open Add Homework page
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Homework').click()
        assert ('homework/new' in self.teacher.current_url()), \
            'not at add homework page'

        # Find and fill in title
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        ).send_keys(assignment_name)

        # Fill in description
        self.teacher.find(
            By.XPATH, '//textarea[contains(@class, "form-control")]'
        ).send_keys('description')

        # Set due dates
        today = datetime.date.today()
        end = randint(1, 5)
        opens_on = today.strftime('%m/%d/%Y')  # make an open homework
        closes_on = (today + datetime.timedelta(days=end)) \
            .strftime('%m/%d/%Y')

        # Find all individual periods
        self.teacher.find(By.ID, 'show-periods-radio').click()
        period_boxes = self.teacher.driver.find_elements(
            By.XPATH, '//input[contains(@id, "period-toggle-period")]'
        )
        period_assignment = {}
        for period in period_boxes:
            period_assignment[
                self.teacher.driver.find_element(
                    By.XPATH,
                    '//label[contains(@for, "%s")]' % period.get_attribute(
                        'id')).text
            ] = (opens_on, closes_on)

        assignment.assign_periods(self.teacher.driver, period_assignment)

        # Add homework problems to the assignment
        assignment.add_homework_problems(
            self.teacher.driver, {'1.1': 3}
        )
        self.teacher.sleep(1)

        # Publish the homework
        save_button = self.teacher.find(
            By.XPATH, '//button[contains(@class,"save")]'
        )
        self.teacher.scroll_to(save_button)
        save_button.click()

        # Verify the homework is created
        try:
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(assignment_name)
            )
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH,
                '//a[contains(@class,"header-control next")]'
            ).click()
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(assignment_name)
            )

        self.ps.test_updates['passed'] = True

    # Case C303 - Teacher | Add an unopened homework from calendar
    @pytest.mark.skipif(str(303) not in TESTS, reason="Excluded")
    def test_teacher_add_an_unopened_homework_from_calendar(self):
        """
        Click on a date at least one day after the current date on the calendar
        From the menu that appears, click on 'Add Homework'
        ***The teacher is taken to a page where they create the assignment.***

        Click on the info icon
        ***Definitions for the status bar buttons are displayed.*** (T1.15.031)

        Give the homework a name in the 'Assignment name' text box
        Select a due date (individually or collectively) for the assignment
         using the calendar element
        Click the '+ Select Problems' button
        Select at least one chapter or section to use for the homework
        Click the 'Show Problems' button
        Click at least one problem to be used for My Selections
        Click the 'Next' button
        Click the 'Publish' button

        #Expected result
        The teacher is returned to the dashboard where the new assignment is displayed.***
        """
        self.ps.test_updates['name'] = \
            't1.16.001' + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.001', '8028']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        calendar_date = self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//div[contains(@class,"Day--upcoming")]')
            )
        )
        self.teacher.driver.execute_script(
            'return arguments[0].scrollIntoView();', calendar_date)
        self.teacher.sleep(1)
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(calendar_date)
        actions.move_by_offset(0, -35)
        actions.click()
        actions.move_by_offset(30, 45)
        actions.click()
        actions.perform()
        self.teacher.page.wait_for_page_load()
        assert ('homework/new' in self.teacher.current_url()), \
            'not at Add Homework page'

        assignment_name = 'hw_003_%d' % (randint(100, 999))
        assignment = Assignment()
        # Find and fill in title
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        ).send_keys(assignment_name)

        # Fill in description
        self.teacher.find(
            By.XPATH, '//textarea[contains(@class, "form-control")]'
        ).send_keys('description')

        # Set due dates
        today = datetime.date.today()
        start = randint(1, 5)
        end = start + randint(1, 5)
        opens_on = (today + datetime.timedelta(days=start)) \
            .strftime(
            '%m/%d/%Y')  # set a future date for it to be published as unopened
        closes_on = (today + datetime.timedelta(days=end)) \
            .strftime('%m/%d/%Y')
        assignment.assign_periods(
            self.teacher.driver, {'all': (opens_on, closes_on)})

        # Add problems to assignment
        assignment.add_homework_problems(
            self.teacher.driver, {'1.1': 3}
        )
        self.teacher.sleep(1)

        # Publish the homework
        save_button = self.teacher.find(
            By.XPATH, '//button[contains(@class,"save")]'
        )
        self.teacher.scroll_to(save_button)
        save_button.click()

        # Verify the homework is created
        try:
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(assignment_name)
            )
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH,
                '//a[contains(@class,"header-control next")]'
            ).click()
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(assignment_name)
            )

        self.ps.test_updates['passed'] = True

    # Case C30 - Teacher | Publish a draft homework
    @pytest.mark.skipif(str(304) not in TESTS, reason="Excluded")
    def test_publish_a_draft_homework(self):
        """
        Steps:
        If the user has more than one course, select a Tutor course

        From the user dashboard, click on a draft assignment
        Click the 'Publish' button

        Result:
        A draft homework is published
        """
        self.ps.test_updates['name'] = 't1.14.007' \
                                       + inspect.currentframe().f_code.co_name[
                                         4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.007', '7998']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'hw_004_%s' % randint(100, 999)
        today = datetime.date.today()
        start = randint(0, 6)
        finish = start + randint(1, 5)
        begin = (today + datetime.timedelta(days=start)) \
            .strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=finish)) \
            .strftime('%m/%d/%Y')

        # Create a draft homework
        self.teacher.add_assignment(
            assignment='homework',
            args={
                'title': assignment_name,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'problems': {'1.1': (2, 3), },
                'status': 'draft',
                'feedback': 'immediate',
            }
        )

        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'month-wrapper')
            )
        )
        self.teacher.find(
            By.XPATH, '//label[contains(text(),"{0}")]'.format(assignment_name)
        ).click()

        # Publish the draft homework
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"-publish")]')
            )
        ).click()
        try:
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(assignment_name)
            )
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH,
                '//a[contains(@class,"header-control next")]'
            ).click()
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(assignment_name)
            )

        self.ps.test_updates['passed'] = True

    # Case C305 - Teacher | Cancel new homework before changes
    @pytest.mark.skipif(str(305) not in TESTS, reason="Excluded")
    def test_teacher_cancel_new_homework_before_changes(self):
        """
        Steps:
        Click on the Add Assignment menu on the user dashboard, OR click on a calendar date at least one day later than the current date
        Click on the 'Add Homework' button
        Click on the 'Cancel' button
        (The teacher is returned to the dashboard.)

        Click on the Add Assignment menu on the user dashboard, OR click on a calendar date at least one day later than the current date
        Click on the 'Add Homework' button
        Click on the X button

        Result
        The teacher is returned to the dashboard on which no changes have been made.
        """
        self.ps.test_updates['name'] = 't1.14.008' \
                                       + inspect.currentframe().f_code.co_name[
                                         4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.008', '7999']
        self.ps.test_updates['passed'] = False

        # Open "Add Homework' page
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Homework').click()
        assert ('homework/new' in self.teacher.current_url()), \
            'not at Add Homework screen'

        # Cancel a homework with "Cancel" button
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'builder-cancel-button')
            )
        ).click()
        assert ('month' in self.teacher.current_url()), \
            'not back at calendar after cancelling homework'

        # Open "Add Homework" page
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Homework').click()
        assert ('homework/new' in self.teacher.current_url()), \
            'not at add homework screen'

        # Cancel a homework with "X" button
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class,"openstax-close-x")]')
            )
        ).click()

        assert ('month' in self.teacher.current_url()), \
            'not back at calendar after cancelling homework'
        self.ps.test_updates['passed'] = True

    # Case C306 - Teacher | Cancel a new homework after changes
    @pytest.mark.skipif(str(306) not in TESTS, reason="Excluded")
    def test_teacher_cancel_new_homework_after_changes(self):
        """
        Steps
        Click on the 'Add Homework' button
        Do at least one of the following:
        - Give the homework a name in the 'Assignment name' text box
        - Select a due date (individually or collectively) for the assignment using the calendar element
        - Click the '+ Select Problems' button
        - Select at least one chapter or section to use for the homework
        - Click the 'Show Problems' button, and select a problem
        Click the 'Cancel' button
        Click the 'Yes' button

        Click on the 'Add Homework' button
        Do at least one of the following:
        - Give the homework a name in the 'Assignment name' text box
        - Give the homework a description in the 'Assignment description' text box
        - Select a due date (individually or collectively) for the assignment using the calendar element
        - Click the '+ Select Problems' button and select a problem
        Click the X button
        Click the 'Yes' button

        Result:
        The teacher is taken back to the dashboard with no changes being made
        """
        self.ps.test_updates['name'] = 't1.14.008' \
                                       + inspect.currentframe().f_code.co_name[
                                         4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.008', '7999']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'hw_006_%d' % (randint(100, 999))

        # Open "Add Homework" page
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Homework').click()
        assert ('homework/new' in self.teacher.current_url()), \
            'not at add homework screen'

        # Add title
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        ).send_keys(assignment_name)
        sleep(1)

        # Cancel with "Cancel" button
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'builder-cancel-button')
            )
        ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class,"ok")]')
            )
        ).click()

        # Check if back at user dashboard
        assert ('month' in self.teacher.current_url()), \
            'not back at calendar after cancelling homework'

        # Open "Add homework" page
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Homework').click()
        self.teacher.page.wait_for_page_load()
        assert ('homework/new' in self.teacher.current_url()), \
            'not at add homework screen'
        sleep(1)

        # Add title
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        ).send_keys(assignment_name)

        # Cancel with "X" button
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class,"openstax-close-x")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"ok")]')
            )
        ).click()

        assert ('month' in self.teacher.current_url()), \
            'not back at calendar after cancelling homework'

        self.ps.test_updates['passed'] = True

    # Case C307 - Teacher | Cancel draft homework after changes
    @pytest.mark.skipif(str(307) not in TESTS, reason="Excluded")
    def test_teacher_cancel_draft_homework_before_changes(self):
        """
        Steps
        Go to https://tutor-qa.openstax.org/
        Login as a teacher user
        If the user has more than one course, select a Tutor course

        From the user dashboard, click on a draft assignment
        Click on the 'Cancel' button

        From the user dashboard, click on a draft assignment
        Click on the X button

        Result
        The teacher returned to the dashboard and no changes have been made
        """
        self.ps.test_updates['name'] = 't1.14.012' \
                                       + inspect.currentframe().f_code.co_name[
                                         4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.012', '8003']
        self.ps.test_updates['passed'] = False

        # Test steps and verification
        assignment_name_1 = "hw_007_%d" % (randint(100, 999))
        assignment_name_2 = "hw_007_%d" % (randint(100, 999))
        today = datetime.date.today()
        start = randint(0, 6)
        finish = start + randint(1, 5)
        begin = (today + datetime.timedelta(days=start)) \
            .strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=finish)) \
            .strftime('%m/%d/%Y')

        # Create a draft homework
        self.teacher.add_assignment(
            assignment='homework',
            args={
                'title': assignment_name_1,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'problems': {'1.1': (2, 3), },
                'status': 'draft',
                'feedback': 'immediate',
            }
        )

        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'month-wrapper')
            )
        )
        self.teacher.find(
            By.XPATH, '//label[contains(text(),"{0}")]'.format(assignment_name_1)
        ).click()
        sleep(1)

        # Cancel with "Cancel" button
        cancel_button = self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'builder-cancel-button')
            )
        )
        self.teacher.scroll_to(cancel_button)
        cancel_button.click()

        # Check if teacher is taken back to user dashboard
        self.teacher.page.wait_for_page_load()
        assert ('month' in self.teacher.current_url()), \
            'not back at calendar after cancelling homework'

        # Create a draft homework
        self.teacher.add_assignment(
            assignment='homework',
            args={
                'title': assignment_name_2,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'problems': {'1.1': (2, 3), },
                'status': 'draft',
                'feedback': 'immediate',
            }
        )

        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'month-wrapper')
            )
        )
        self.teacher.find(
            By.XPATH,
            '//label[contains(text(),"{0}")]'.format(assignment_name_2)
        ).click()
        sleep(1)

        # Cancel with "X" button
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class,"openstax-close-x")]')
            )
        ).click()

        # Check if the teacher is back to user dashboard
        assert ('month' in self.teacher.current_url()), \
            'not back at calendar after cancelling homework'

        self.ps.test_updates['passed'] = True

    # Case C308 - Teacher | Cancel draft homework after changes
    @pytest.mark.skipif(str(308) not in TESTS, reason="Excluded")
    def test_teacher_cancel_draft_homework_after_changes(self):
        """
        Steps:
        From the user dashboard, click on a draft assignment
        Change the homework name in the 'Assignment name' text box
        Click on the 'Cancel' button
        Click on the 'Yes' button

        From the user dashboard, click on a draft assignment
        Change the homework name in the 'Assignment name' text box
        Click on the X button
        Click on the 'Yes' button

        Result:
        The teacher is returned to the dashboard
        """
        self.ps.test_updates['name'] = 't1.14.012' \
                                       + inspect.currentframe().f_code.co_name[
                                         4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.012', '8003']
        self.ps.test_updates['passed'] = False

        # Test steps and verification
        assignment_name_1 = "hw_007_%d" % (randint(100, 999))
        assignment_name_2 = "hw_007_%d" % (randint(100, 999))
        today = datetime.date.today()
        start = randint(0, 6)
        finish = start + randint(1, 5)
        begin = (today + datetime.timedelta(days=start)) \
            .strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=finish)) \
            .strftime('%m/%d/%Y')

        # Create a draft homework
        self.teacher.add_assignment(
            assignment='homework',
            args={
                'title': assignment_name_1,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'problems': {'1.1': (2, 3), },
                'status': 'draft',
                'feedback': 'immediate',
            }
        )

        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'month-wrapper')
            )
        )

        # Open a draft homework
        self.teacher.find(
            By.XPATH,
            '//label[contains(text(),"{0}")]'.format(assignment_name_1)
        ).click()

        # Change title
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        ).send_keys("changed")
        sleep(1)

        # Cancel with "Cancel" button
        cancel_button = self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'builder-cancel-button')
            )
        )
        self.teacher.scroll_to(cancel_button)
        cancel_button.click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class,"ok")]')
            )
        ).click()

        # Check if teacher is taken to user dashboard
        self.teacher.page.wait_for_page_load()
        assert ('month' in self.teacher.current_url()), \
            'not back at calendar after cancelling homework'

        # Create a draft homework
        self.teacher.add_assignment(
            assignment='homework',
            args={
                'title': assignment_name_2,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'problems': {'1.1': (2, 3), },
                'status': 'draft',
                'feedback': 'immediate',
            }
        )

        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'month-wrapper')
            )
        )

        # Open a draft homework
        self.teacher.find(
            By.XPATH,
            '//label[contains(text(),"{0}")]'.format(assignment_name_2)
        ).click()

        # Change title
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        ).send_keys("changed")
        sleep(1)

        # Cancel with "X" button
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class,"openstax-close-x")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class,"ok")]')
            )
        ).click()

        # Check if the teacher is back to user dashboard
        assert ('month' in self.teacher.current_url()), \
            'not back at calendar after cancelling reading'

        self.ps.test_updates['passed'] = True

    # Case C30 - Teacher | Attempt to save homework with empty required fields
    @pytest.mark.skipif(str(309) not in TESTS, reason="Excluded")
    def test_teacher_attempt_to_save_homework_with_empty_required_fields(self):
        """
        Steps:
        Click on the Add Assignment drop down on the user dashboard if it's not active, OR click on a calendar date at least one day later than the current date
        Click on the 'Add Homework' button
        Click on the 'Save As Draft' button
        (Red text appears next to every blank required field.)

        Click on the course name to go back to user dashboard
        Click on the Add Assignment menu on the user dashboard if it's not active, OR click on a calendar date at least one day later than the current date
        Click on the 'Add Homework' button
        Click on the 'Publish' button

        Result
        Red text appears next to every blank required field.
        """
        self.ps.test_updates['name'] = 't1.14.016' \
                                       + inspect.currentframe().f_code.co_name[
                                         4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.016', '8007']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Homework').click()
        assert ('homework/new' in self.teacher.current_url()), \
            'not at add readings screen'

        # Publish without filling in any fields
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class,"-publish")]')
            )
        ).click()

        self.teacher.find(
            By.XPATH, '//div[contains(text(),"Required field")]')
        assert ('homework' in self.teacher.current_url()), \
            'went back to calendar even though required fields were left blank'

        # Refresh the page
        self.teacher.driver.refresh()
        sleep(3)

        # Save without filling in any fields
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class, "save")]')
            )
        ).click()

        self.teacher.find(
            By.XPATH, '//div[contains(text(),"Required field")]')
        assert ('homework' in self.teacher.current_url()), \
            'went back to calendar even though required fields were left blank'

        self.ps.test_updates['passed'] = True

    # Case C310 - Teacher | Delete a draft homework
    @pytest.mark.skipif(str(310) not in TESTS, reason="Excluded")
    def test_teacher_delete_a_draft_homework(self):
        """
        Steps
        Go to https://tutor-qa.openstax.org/
        Login as a teacher user
        If the user has more than one course, select a Tutor course

        Click on a draft assignment on the calendar
        Click on the 'Delete' button
        Click "Yes" on the dialog box that appears

        Result:
        The teacher is returned to the dashboard and the draft assignment is
        removed from the calendar.
        """
        self.ps.test_updates['name'] = 't1.14.007' \
                                       + inspect.currentframe().f_code.co_name[
                                         4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.007', '7998']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'hw_010_%s' % randint(100, 999)
        today = datetime.date.today()
        start = randint(0, 6)
        finish = start + randint(1, 5)
        begin = (today + datetime.timedelta(days=start)) \
            .strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=finish)) \
            .strftime('%m/%d/%Y')

        # Create a draft homework
        self.teacher.add_assignment(
            assignment='homework',
            args={
                'title': assignment_name,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'problems': {'1.1': (2, 3), },
                'status': 'draft',
                'feedback': 'immediate',
            }
        )

        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'month-wrapper')
            )
        )

        # Open the draft homework
        self.teacher.find(
            By.XPATH, '//label[contains(text(),"{0}")]'.format(assignment_name)
        ).click()
        sleep(1)

        # Delete the draft reading
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"delete-link")]')
            )
        ).click()
        self.teacher.find(
            By.XPATH, '//button[contains(text(),"Yes")]'
        ).click()

        assert ('month' in self.teacher.current_url()), \
            'not returned to calendar after deleting an assignment'
        self.teacher.driver.refresh()
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'month-wrapper')
            )
        )
        deleted_hw = self.teacher.find_all(
            By.XPATH, '//label[@data-title="{0}"]'.format(assignment_name)
        )
        assert len(deleted_hw) == 0, 'draft reading not deleted'

        self.ps.test_updates['passed'] = True


    # Case C311 - Teacher | Delete an unopened homework
    @pytest.mark.skipif(str(311) not in TESTS, reason="Excluded")
    def test_teacher_delete_an_unopened_homework(self):
        pass

    # Case C312 - Teacher | Delete an open homework
    @pytest.mark.skipif(str(312) not in TESTS, reason="Excluded")
    def test_teacher_delete_an_open_homework(self):
        pass

    # Case C30 - Teacher | Change an open homework
    @pytest.mark.skipif(str(313) not in TESTS, reason="Excluded")
    def teacher_change_an_open_homework(self):
        pass

    # Case C30 - Teacher | Change a draft homework
    @pytest.mark.skipif(str(314) not in TESTS, reason="Excluded")
    def test_teacher_change_a_draft_homework(self):
        pass

    # Case C30 - Teacher | Change an unopen homework
    @pytest.mark.skipif(str(315) not in TESTS, reason="Excluded")
    def test_change_an_unopen_homework(self):
        pass

    # Case C30 - Teacher | Show available problems
    @pytest.mark.skipif(str(316) not in TESTS, reason="Excluded")
    def test_show_available_problems(self):
        pass

    # Case C30 - Teacher | Select problems
    @pytest.mark.skipif(str(317) not in TESTS, reason="Excluded")
    def test_select_problems(self):
        pass

    # Case C30 - Teacher | Preview feedback and report error
    @pytest.mark.skipif(str(318) not in TESTS, reason="Excluded")
    def test_preview_feedback_and_report_error(self):
        pass

    # Case C30 - Teacher | Cancel assessment selection before changes
    @pytest.mark.skipif(str(319) not in TESTS, reason="Excluded")
    def test_cancel_assessment_selection_before_changes(self):
        pass

    # Case C30 - Teacher | Cancel assessment selection after changes
    @pytest.mark.skipif(str(320) not in TESTS, reason="Excluded")
    def test_cancel_assessment_selection_after_changes(self):
        pass

    # Case C30 - Teacher | Order problems and view problem list
    @pytest.mark.skipif(str(321) not in TESTS, reason="Excluded")
    def test_order_problems_and_view_problem_list(self):
        pass

    # Case C30 - Teacher | Add and Remove problems
    @pytest.mark.skipif(str(322) not in TESTS, reason="Excluded")
    def test_add_and_remove_problems(self):
        pass

    # Case C30 - Teacher | Add a homework by dragging and dropping
    @pytest.mark.skipif(str(323) not in TESTS, reason="Excluded")
    def test_add_a_homework_by_dragging_and_dropping(self):
        pass

class Actions(ActionChains):
    """Add wait to action chains."""

    def wait(self, time: float):
        """Extend monad."""
        self._actions.append(lambda: sleep(float(time)))
        return self











