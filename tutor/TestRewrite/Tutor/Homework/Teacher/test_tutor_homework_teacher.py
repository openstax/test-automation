"""Tutor Homework Teacher"""

import datetime
import inspect
import json
import os
import pytest
import unittest
# import random

from pastasauce import PastaSauce, PastaDecorator
from random import randint
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
# from selenium.webdriver.support.ui import WebDriverWait
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
    str([
        301, 302, 303, 304, 305,
        306, 307, 308, 309, 310,
        311, 312, 313, 314, 315,
        316, 317, 318, 319, 320,
        321
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
                use_env_vars=True
            )
        self.teacher.login()
        self.teacher.select_course(appearance='college_biology')

    def tearDown(self):
        """Test Destructor"""
        if not LOCAL_RUN:
            self.ps.update_job(
                job_id=str(self.teacher.driver.session_id),
                **self.ps.test_updates
            )
        try:
            self.teacher.delete()
        except:
            pass

    # Case C - Teacher | Create a new open homework from sidebar
    @pytest.mark.skipif(str(301) not in TESTS, reason="Excluded")
    def test_teacher_create_and_publish_a_new_open_homework_from_sidebar(self):
        """
        Click on the Add Assignment menu on the user dashboard
        Click on the 'Add Homework' button
        ***The teacher is taken to the page where they create the assignment.**

        Edit the text box named 'Assignment name'
        ***Text is visible in the 'Assignment name' text box.***

        Edit the text box named 'Description or special instructions'
        ***Text is visible in the 'Description or special instructions' text
        box.***

        Select the 'All Periods' radio button if it is not selected by default
        Select an today's date as the open date for the assignment using the
        calendar element
        Type 00:00am as the open time for the assignment
        Select a due date in the future for the assignment using the calendar
        element

        Select an option on the 'Show feedback' drop down menu
        ***The option chosen is shown on the drop down menu.***

        Click the '+ Select Problems' button
        Select at least one chapter or section to use for the homework
        Click the 'Show Problems' button
        Click at least one problem to be used for My Selections
        Click the 'Next' button
        Click the 'Publish' button

        #Expected result
        ***The teacher is returned to the dashboard where the new assignment is
        displayed.***
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

    # Case C - Teacher | Save a draft for individual periods
    @pytest.mark.skipif(str(302) not in TESTS, reason="Excluded")
    def test_teacher_save_a_draft_for_individual_periods(self):
        """
        # Steps
        Go to https://tutor-qa.openstax.org/
        Login with the user account
        If the user has more than one course, select a Tutor course

        Click on the Add Assignment drop down menu on the user dashboard, OR
        click on a calendar date at least one day later than the current date
        Click on the 'Add Homework' button
        ***The teacher is taken to the page where they create the assignment.**

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

    # Case C - Teacher | Add a new unopened homework from calendar
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
        The teacher is returned to the dashboard where the new assignment is
        displayed.***
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

    # PROBLEMATIC Case C30 - Teacher | Add a homework by dragging and dropping
    @pytest.mark.skipif(str(322) not in TESTS, reason="Excluded")
    def test_add_a_homework_by_dragging_and_dropping(self):
        """
        If the user has more than one course, select a Tutor course

        Click on the Add Assignment menu
        Click and drag Add Homework to a chosen due date.
        :return:
        """
        self.ps.test_updates['name'] = 't1.14.037' \
                                       + inspect.currentframe().f_code.co_name[
                                         4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.037', '111246']
        self.ps.test_updates['passed'] = False

        # Test steps and verification
        self.teacher.assign.open_assignment_menu(self.teacher.driver)

        # chain setup
        drag_tile = self.teacher.driver.find_element(
            By.ID,
            '//div[@data-assignment-type="homework" and @draggable="true"]'
        )
        print(drag_tile)

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
        Click on the Add Assignment menu on the user dashboard, OR click on a
        calendar date at least one day later than the current date
        Click on the 'Add Homework' button
        Click on the 'Cancel' button
        (The teacher is returned to the dashboard.)

        Click on the Add Assignment menu on the user dashboard, OR click on a
        calendar date at least one day later than the current date
        Click on the 'Add Homework' button
        Click on the X button

        Result
        The teacher is returned to the dashboard on which no changes have been
        made.
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
        - Select a due date (individually or collectively) for the assignment
        using the calendar element
        - Click the '+ Select Problems' button
        - Select at least one chapter or section to use for the homework
        - Click the 'Show Problems' button, and select a problem
        Click the 'Cancel' button
        Click the 'Yes' button

        Click on the 'Add Homework' button
        Do at least one of the following:
        - Give the homework a name in the 'Assignment name' text box
        - Give the homework a description in the 'Assignment description' text
        box
        - Select a due date (individually or collectively) for the assignment
        using the calendar element
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

    # Case C307 - Teacher | Cancel draft homework before changes
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
            By.XPATH,
            '//label[contains(text(),"{0}")]'.format(assignment_name_1)
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

    # Case C30 - Teacher | Attempt to save a homework with empty required field
    @pytest.mark.skipif(str(309) not in TESTS, reason="Excluded")
    def test_teacher_attempt_to_save_homework_with_empty_required_fields(self):
        """
        Steps:
        Click on the Add Assignment drop down on the user dashboard if it's not
        active, OR click on a calendar date at least one day later than the
        current date
        Click on the 'Add Homework' button
        Click on the 'Save As Draft' button
        (Red text appears next to every blank required field.)

        Click on the course name to go back to user dashboard
        Click on the Add Assignment menu on the user dashboard if it's not
        active, OR click on a calendar date at least one day later than the
        current date
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

        # Delete the draft homework
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
        """
        Steps
        Click on a published assignment that has not yet been opened for
        students
        Click on the 'Edit Assignment' button
        Click on the 'Delete' button
        Click 'Yes' on the dialog box that pops up

        Results:
        The teacher is returned to the dashboard and the assignment is removed
        from the calendar.
        """
        self.ps.test_updates['name'] = 't1.16.018' \
                                       + inspect.currentframe().f_code.co_name[
                                         4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.018', '8045']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'hw_011_%s' % randint(100, 999)
        today = datetime.date.today()
        start = randint(0, 6)
        finish = start + randint(1, 5)
        begin = (today + datetime.timedelta(days=start)) \
            .strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=finish)) \
            .strftime('%m/%d/%Y')

        # Create an unopened homework
        self.teacher.add_assignment(
            assignment='homework',
            args={
                'title': assignment_name,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'problems': {'1.1': (2, 3), },
                'status': 'publish',
                'feedback': 'immediate',
            }
        )

        # Open the unopened homework
        self.teacher.find(
            By.XPATH, '//label[contains(text(),"{0}")]'.format(assignment_name)
        ).click()
        self.teacher.find(
            By.ID, 'edit-assignment-button'
        ).click()
        sleep(1)

        # Delete the unopened homework
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

    # Case C312 - Teacher | Delete an open homework
    @pytest.mark.skipif(str(312) not in TESTS, reason="Excluded")
    def test_teacher_delete_an_open_homework(self):
        """
        Steps:
        Click on a published assignment that has not yet been opened for
        students
        Click on the 'Edit Assignment' button
        Click on the 'Delete' button
        Click 'Yes' on the dialog box that pops up

        Result:
        The teacher is returned to the dashboard and the assignment is removed
        from the calendar.
        """
        self.ps.test_updates['name'] = 't1.16.018' \
                                       + inspect.currentframe().f_code.co_name[
                                         4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.018', '8045']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'hw_011_%s' % randint(100, 999)
        today = datetime.date.today()
        finish = randint(1, 5)
        begin = today.strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=finish)) \
            .strftime('%m/%d/%Y')

        # Create an open homework
        self.teacher.add_assignment(
            assignment='homework',
            args={
                'title': assignment_name,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'problems': {'1.1': (2, 3), },
                'status': 'publish',
                'feedback': 'immediate',
            }
        )

        # Open edit homework page
        self.teacher.find(
            By.XPATH, '//label[contains(text(),"{0}")]'.format(assignment_name)
        ).click()
        self.teacher.find(
            By.ID, 'edit-assignment-button'
        ).click()
        sleep(1)

        # Delete the open homework
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

    # Case C313 - Teacher | Change a draft homework
    @pytest.mark.skipif(str(313) not in TESTS, reason="Excluded")
    def test_teacher_change_a_draft_homework(self):
        """
        Steps:
        From the dashboard, click on a draft homework
        Edit the text in the text box named 'Assignment name'
        Edit the text in the text box named 'Description or special
        instructions'
        Edit the open and due dates for the assignment
        Edit the 'Show feedback' drop down menu option
        Click the 'Save As Draft' button

        Result:
        The user is returned to the dashboard. Changes to the draft are seen.
        """
        self.ps.test_updates['name'] = 't1.14.034' \
                                       + inspect.currentframe().f_code.co_name[
                                         4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.034', '8025']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'hw_013%d' % (randint(100, 999))
        assignment = Assignment()
        today = datetime.date.today()
        finish = randint(1, 6)
        begin = today.strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=finish)).strftime('%m/%d/%Y')

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

        # Locate the draft homework
        try:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH, '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(assignment_name)
            ).click()
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH,
                '//a[contains(@class,"header-control next")]'
            ).click()
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH, '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(assignment_name)
            ).click()
        sleep(1)

        # Change the title
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        ).send_keys('new')

        # Change the description
        self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]' +
            '//textarea[contains(@class,"form-control")]'
        ).send_keys('new')

        # set new due dates
        today = datetime.date.today()
        start = randint(1, 6)
        end = start + randint(1, 5)
        opens_on = (today + datetime.timedelta(days=start)) \
            .strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=end)) \
            .strftime('%m/%d/%Y')
        assignment.assign_periods(
            self.teacher.driver,
            {'all': (opens_on, closes_on)}
        )

        # Remove problems from the assignment
        self.teacher.find(
            By.XPATH, "//button[contains(@class,'-remove-exercise')]"
        ).click()
        self.teacher.find(
            By.XPATH, '//button[text()="Remove"]'
        ).click()

        # Change show feedback
        feedback = self.teacher.find(By.ID, 'feedback-select')
        Assignment.scroll_to(self.teacher.driver, feedback)
        feedback.click()
        self.teacher.find(
            By.XPATH, '//option[@value="due_at"]'
        ).click()

        # Save
        self.teacher.find(
            By.XPATH,
            '//button[contains(@class,"-save")]'
        ).click()

        try:
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(
                    assignment_name + 'new')
            )
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH,
                '//a[contains(@class,"header-control next")]'
            ).click()
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(
                    assignment_name + 'new')
            )
        self.ps.test_updates['passed'] = True

    # Case C314 - Teacher | Change an unopened homework
    @pytest.mark.skipif(str(314) not in TESTS, reason="Excluded")
    def test_change_an_unopened_homework(self):
        """
        Steps;
        From the dashboard, click on a published, unopened homework
        Click on the 'Edit Assignment' button
        Edit the text in the text box named 'Assignment name'
        Edit the text in the text box named 'Description or special
        instructions'
        Edit the open and due dates for the assignment
        Edit the 'Show feedback' drop down menu option
        Click the 'Save' button

        Result:
        The user is returned to the dashboard. Changes to the homework are
        seen.
        """
        self.ps.test_updates['name'] = 't1.14.034' \
                                       + inspect.currentframe().f_code.co_name[
                                         4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.034', '8025']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'hw_014_%s' % randint(100, 999)
        assignment = Assignment()
        today = datetime.date.today()
        start = randint(0, 3)
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
                'status': 'publish',
                'feedback': 'immediate',
            }
        )

        # Locate the draft homework
        try:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH, '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(assignment_name)
            ).click()
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH,
                '//a[contains(@class,"header-control next")]'
            ).click()
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH, '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(assignment_name)
            ).click()
        self.teacher.find(By.ID, 'edit-assignment-button').click()
        sleep(1)

        # Change the title
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        ).send_keys('new')

        # Change the description
        self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]' +
            '//textarea[contains(@class,"form-control")]'
        ).send_keys('new')

        # set new due dates
        today = datetime.date.today()
        start = randint(1, 3)
        end = start + randint(1, 6)
        opens_on = (today + datetime.timedelta(days=start)) \
            .strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=end)) \
            .strftime('%m/%d/%Y')
        assignment.assign_periods(
            self.teacher.driver,
            {'all': (opens_on, closes_on)}
        )
        sleep(3)

        # Change show feedback
        feedback = self.teacher.find(By.ID, 'feedback-select')
        Assignment.scroll_to(self.teacher.driver, feedback)
        feedback.click()
        self.teacher.find(
            By.XPATH, '//option[@value="due_at"]'
        ).click()

        # Remove problems from the assignment
        self.teacher.find(
            By.XPATH, "//button[contains(@class,'-remove-exercise')]"
        ).click()
        self.teacher.find(
            By.XPATH, '//button[text()="Remove"]'
        ).click()
        sleep(3)

        # Save
        self.teacher.find(
            By.XPATH,
            '//button[contains(@class,"-publish")]'
        ).click()

        try:
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(
                    assignment_name + 'new')
            )
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH,
                '//a[contains(@class,"header-control next")]'
            ).click()
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(
                    assignment_name + 'new')
            )
        self.ps.test_updates['passed'] = True

    # Case C315 - Teacher | Change an open homework
    @pytest.mark.skipif(str(315) not in TESTS, reason="Excluded")
    def test_change_an_open_homework(self):
        """
        Steps:
        From the dashboard, click on an opened homework
        Click on the 'Edit Assignment' button
        Edit the text in the text box named 'Assignment name'
        Edit the text in the text box named 'Description or special
        instructions'
        Edit the due date for the assignment
        Edit the 'Show feedback' drop down menu option
        Click the 'Save' button

        Result:
        User is returned to the dashboard. Changes to the homework are seen.
        """
        self.ps.test_updates['name'] = 't1.14.034' \
                                       + inspect.currentframe().f_code.co_name[
                                         4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.034', '8025']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'hw_015_%s' % randint(100, 999)
        assignment = Assignment()
        today = datetime.date.today()
        finish = randint(1, 5)
        begin = today.strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=finish)) \
            .strftime('%m/%d/%Y')

        # Create an open homework
        self.teacher.add_assignment(
            assignment='homework',
            args={
                'title': assignment_name,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'problems': {'1.1': (2, 3), },
                'status': 'publish',
                'feedback': 'immediate',
            }
        )

        # Open edit homework page
        self.teacher.find(
            By.XPATH, '//label[contains(text(),"{0}")]'.format(assignment_name)
        ).click()
        self.teacher.find(
            By.ID, 'edit-assignment-button'
        ).click()
        sleep(1)

        # Change the title
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        ).send_keys('new')

        # Change the description
        self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]' +
            '//textarea[contains(@class,"form-control")]'
        ).send_keys('new')

        # Set new due dates
        end = randint(1, 5)
        closes_on = (today + datetime.timedelta(days=end)) \
            .strftime('%m/%d/%Y')
        assignment.assign_date(
            driver=self.teacher.driver, date=closes_on, is_all=True,
            target='due'
        )
        # assignment.assign_periods(
        #     self.teacher.driver,
        #     {'all': (opens_on, closes_on)}
        # )

        # Change show feedback
        feedback = self.teacher.find(By.ID, 'feedback-select')
        Assignment.scroll_to(self.teacher.driver, feedback)
        feedback.click()
        self.teacher.find(
            By.XPATH, '//option[@value="due_at"]'
        ).click()

        # Publish
        self.teacher.find(
            By.ID, 'builder-save-button'
        ).click()

        try:
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(
                    assignment_name + 'new')
            )
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH,
                '//a[contains(@class,"header-control next")]'
            ).click()
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(
                    assignment_name + 'new')
            )
        self.ps.test_updates['passed'] = True

    # Case C316 - Teacher | Show available problems and IDs
    @pytest.mark.skipif(str(316) not in TESTS, reason="Excluded")
    def test_show_available_problems_and_id(self):
        """
        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and
        select 'Add Homework'
        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select the introduction section of the chapter
        Click the 'Show Problems' button
        (No problems are displayed. The text 'No exercises found in the
        selected sections)

        Select one of the sections in one chapter that is not an introduction
        section
        Click the 'Show Problems' button
        (The problems for the selected section are displayed. For every
        displayed problem the ID# is displayed as ID#@Version. Tags for each
        displayed problem exist.)

        Select one of the chapters
        Click the 'Show Problems' button

        Result:
        Problems for the whole chapter are displayed
        """
        self.ps.test_updates['name'] = 't1.14.027' \
                                       + inspect.currentframe().f_code.co_name[
                                         4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.027', '8018']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'hw_16_%d' % (randint(100, 999))
        # assignment = Assignment()
        today = datetime.date.today()
        finish = randint(1, 6)
        end = (today + datetime.timedelta(days=finish)).strftime('%m/%d/%Y')
        print(end)

        # Open Add Homework page
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Homework').click()

        # Fill in title
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        ).send_keys(assignment_name)

        # Select the introduction section of a chapter
        self.teacher.find(By.ID, 'problems-select').click()
        intro_section = '2'
        chapter = intro_section.split('.')[0]
        data_chapter = self.teacher.find(
            By.XPATH,
            '//a//span[@data-chapter-section="%s"]' % chapter
        )
        if data_chapter.find_element(By.XPATH, "../.."). \
                get_attribute('aria-expanded') == 'false':
            data_chapter.click()

        data_section = self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"section")]' +
            '/span[@data-chapter-section="%s"]' % intro_section
        )
        if not ('selected' in data_section.find_element(By.XPATH, "..").
                get_attribute('class')):
            data_section.click()
        element = self.teacher.find(
            By.XPATH, '//button[text()="Show Problems"]')
        Assignment.scroll_to(self.teacher.driver, element)
        element.click()

        # No problems in the intro section
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 "//p[@class='no-exercises-found']")
            )
        )
        sleep(3)

        # Verify problems show exercise ID and version
        section = '1.1'
        self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"section")]' +
            '/span[@data-chapter-section="%s"]' % section
        ).click()
        element = self.teacher.find(
            By.XPATH, '//button[text()="Show Problems"]')
        Assignment.scroll_to(self.teacher.driver, element)
        element.click()
        # find IDs
        ids = self.teacher.driver.find_elements(
            By.XPATH,
            "//span[@class='exercise-tag' and " +
            "contains(text(),'ID: ') and contains(text(),'@')]")
        cards = self.teacher.driver.find_elements(
            By.XPATH,
            "//div[@data-exercise-id]")

        # Verify that each visible card has an ID
        assert (len(ids) == len(cards)), \
            'Number of IDs does not match number of visible assessment cards'

        self.ps.test_updates['passed'] = True

    # HAVING TROUBLE DESELECTING PROBLEMS Case C317 - Teacher | Select problems
    @pytest.mark.skipif(str(317) not in TESTS, reason="Excluded")
    def test_select_problems_including_tutor_selection(self):
        """
        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and
        select 'Add Homework'
        Click the '+ Select Problems' button
        Select at least one chapter
        Click the 'Show Problems' button
        On the section marked 'Tutor Selections', change the number of
        assignments by clicking on the up or down arrow
        (The number of total problems and tutor selections changes.)

        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select one of the non-introductory sections in one chapter
        Click the 'Show Problems' button
        Click "Add question" on at least one of the displayed problems
        (The question is shaded blue. Number of total problems and the number
        of my selections increases.)
        Click "Remove question" on at least one of the problems that have been
        selected.

        Result:
        The question turns back to white. The number of my selections and total
        problems decreases.
        """
        self.ps.test_updates['name'] = 't1.14.027' \
                                       + inspect.currentframe().f_code.co_name[
                                         4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.027', '8018']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'hw_17_%d' % (randint(100, 999))
        # assignment = Assignment()
        # today = datetime.date.today()
        # finish = randint(1, 6)
        # end = (today + datetime.timedelta(days=finish)).strftime('%m/%d/%Y')

        # Open Add Homework page
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Homework').click()

        # Fill in title
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        ).send_keys(assignment_name)

        # Open problem selection menu
        self.teacher.find(By.ID, 'problems-select').click()
        section = '1.1'
        self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"section")]' +
            '/span[@data-chapter-section="%s"]' % section
        ).click()
        element = self.teacher.find(
            By.XPATH, '//button[text()="Show Problems"]')
        Assignment.scroll_to(self.teacher.driver, element)
        element.click()

        # Select 2 problems and observe problem number increase
        orig_total = self.teacher.find(
            By.XPATH, '//div[contains(@class,"total")]/h2'
        ).text
        orig_mine = self.teacher.find(
            By.XPATH, '//div[contains(@class,"mine")]/h2'
        ).text
        problems = self.teacher.find_all(
            By.XPATH, '//div[@class="controls-overlay"]'
        )
        self.teacher.scroll_to(problems[2])
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//div[contains(@class, "include")]')
            )
        ).click()
        sleep(1)
        self.teacher.scroll_to(problems[1])
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//div[contains(@class, "include")]')
            )
        ).click()

        new_total = self.teacher.find(
            By.XPATH, '//div[contains(@class,"total")]/h2'
        ).text
        new_mine = self.teacher.find(
            By.XPATH, '//div[contains(@class,"mine")]/h2'
        ).text
        assert (int(orig_total) == int(new_total) - 2), \
            "total problem number not changed"
        assert (int(orig_mine) == int(new_mine) - 2), \
            "my selections number not changed"

        # Deselect a problem from menu bar
        # self.teacher.scroll_to(prob_2)
        # self.teacher.wait.until(
        #     expect.element_to_be_clickable(
        #         (By.XPATH, '//div[@class="selected-mask"]/..//div[
        # contains(@class, "exclude")]')
        #     )
        # ).click()
        # updated_total = self.teacher.find(
        #     By.XPATH, '//div[contains(@class,"total")]/h2'
        # ).text
        # updated_mine = self.teacher.find(
        #     By.XPATH, '//div[contains(@class,"mine")]/h2'
        # ).text
        # assert (int(updated_total) == int(new_total) - 1), \
        #     "total problem number not changed"
        # assert (int(updated_mine) == int(new_mine) - 1), \
        #     "my selections number not changed"

        # Change tutor selection
        orig_num = self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 "//div[@class='tutor-selections']//h2")
            )
        ).text
        self.teacher.sleep(3)
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH,
                 "//div[@class='tutor-selections']//i[@type='chevron-up']")
            )
        ).click()
        new_num = self.teacher.find(
            By.XPATH, "//div[@class='tutor-selections']//h2"
        ).text

        assert (int(orig_num) == int(new_num) - 1), \
            "tutor selections not changed"

        self.ps.test_updates['passed'] = True

    # Case C318 - Teacher | View question details and report error
    @pytest.mark.skipif(str(318) not in TESTS, reason="Excluded")
    def test_view_question_details_and_report_error(self):
        """
        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and
        select 'Add Homework'
        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select one of the non-introductory sections in one chapter

        Click the 'Show Problems' button
        Click "Question Details"
        Select the 'Preview Feedback' checkbox for at least one problem
        (Explanations for each answer are displayed as well as a detailed
        solution.)

        Click the 'Report an error' link on one of the questions.

        Result:
        A new tab is opened to a Google form for reporting errors
        """
        self.ps.test_updates['name'] = 't1.14.027' \
                                       + inspect.currentframe().f_code.co_name[
                                         4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.027', '8018']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'hw_17_%d' % (randint(100, 999))
        # assignment = Assignment()
        # today = datetime.date.today()
        # finish = randint(1, 6)
        # end = (today + datetime.timedelta(days=finish)).strftime('%m/%d/%Y')

        # Open Add Homework page
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Homework').click()

        # Fill in title
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        ).send_keys(assignment_name)

        # Open problem selection menu
        self.teacher.find(By.ID, 'problems-select').click()
        section = '1.1'
        self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"section")]' +
            '/span[@data-chapter-section="%s"]' % section
        ).click()
        element = self.teacher.find(
            By.XPATH, '//button[text()="Show Problems"]')
        Assignment.scroll_to(self.teacher.driver, element)
        element.click()

        problems = self.teacher.find_all(
            By.XPATH, '//div[@class="controls-overlay"]'
        )
        self.teacher.scroll_to(problems[1])
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//div[contains(@class,"details")]')
            )
        ).click()

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class, "feedback")]')
            )
        ).click()

        # Solutions are present
        self.teacher.find(By.XPATH, '//div[@class="detailed-solution"]')

        # Report an error
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class, "report-error")]')
            )
        ).click()
        error_page = self.teacher.driver.window_handles[1]
        self.teacher.driver.switch_to_window(error_page)
        sleep(1)
        assert('errata/form' in self.teacher.current_url()), \
            "Not at errata page "

    # Case C319 - Teacher | Cancel assessment selection before changes
    @pytest.mark.skipif(str(319) not in TESTS, reason="Excluded")
    def test_cancel_assessment_selection_before_changes(self):
        """
        Steps:
        If the user has more than one course, select a Tutor course
        From the dashboard, click on the 'Add Assignment' drop down menu and
        select 'Add Homework'
        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select one of the non-introductory sections in one chapter
        Click the 'Show Problems' button
        Click the 'Cancel' button
        Click the 'OK' button
        (The user is returned to the page where the assignment name,
        description, and open/due dates are set.)

        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select one of the non-introductory sections in one chapter
        Click the 'Show Problems' button
        Click the X button
        Click the 'OK' button

        Result:
        The user is returned to the page where the assignment name,
        description, and open/due dates are set.
        """
        self.ps.test_updates['name'] = 't1.14.027' \
                                       + inspect.currentframe().f_code.co_name[
                                         4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.027', '8018']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'hw_20_%d' % (randint(100, 999))
        # assignment = Assignment()
        # today = datetime.date.today()
        # finish = randint(1, 6)
        # end = (today + datetime.timedelta(days=finish)).strftime('%m/%d/%Y')

        # Open Add Homework page
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Homework').click()

        # Fill in title
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        ).send_keys(assignment_name)

        # Cancel with cancel button
        self.teacher.find(By.ID, 'problems-select').click()
        self.teacher.find(By.XPATH, '//button[@aria-role="close"]').click()

        # Cancel with "X" button
        self.teacher.find(By.ID, 'problems-select').click()
        x_button = self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH,
                 "//div[contains(@class,'select-topics')]" +
                 "//button[contains(@class,'openstax-close-x')]")
            )
        )
        self.teacher.scroll_to(x_button)
        x_button.click()

        assert "homework/new" in self.teacher.current_url(), \
            "not at add homework page"

        self.ps.test_updates['passed'] = True

    # Case C30 - Teacher | Cancel assessment selection after changes
    @pytest.mark.skipif(str(320) not in TESTS, reason="Excluded")
    def test_cancel_assessment_selection_after_changes(self):
        """
        Steps:
        If the user has more than one course, select a Tutor course
        From the dashboard, click on the 'Add Assignment' drop down menu and
        select 'Add Homework'
        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select one of the non-introductory sections in one chapter
        Click the 'Show Problems' button
        Select at least one of the displayed problems
        Click the 'Cancel' button adjacent to the 'Next' button, OR click the
        'Cancel' button adjacent to the 'Show Problems' button and then hit the
        'OK' button
        Click the 'OK' button
        (User is taken back to the page where the assignment name, description,
        and open/due dates can be set.)

        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select one of the non-introductory sections in one chapter
        Click the 'Show Problems' button
        Select at least one of the displayed problems
        Click the X button
        Click the 'OK' button
        (User is taken back to the page where the assignment name, description,
        and open/due dates are set.)

        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select one of the non-introductory sections in one chapter
        Click the 'Show Problems' button
        Select at least one of the displayed problems
        Click the 'Cancel' button adjacent to the 'Next' button

        Result:
        User is taken back to the page where the assignment name, description,
        and open/due dates are set.
        """
        self.ps.test_updates['name'] = 't1.14.027' \
                                       + inspect.currentframe().f_code.co_name[
                                         4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.027', '8018']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'hw_20_%d' % (randint(100, 999))
        # assignment = Assignment()
        # today = datetime.date.today()
        # finish = randint(1, 6)
        # end = (today + datetime.timedelta(days=finish)).strftime('%m/%d/%Y')

        # Open Add Homework page
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Homework').click()

        # Fill in title
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        ).send_keys(assignment_name)

        # Select a problem
        self.teacher.find(By.ID, 'problems-select').click()
        sections = self.teacher.find_all(By.XPATH, '//input[@type="checkbox"]')
        self.teacher.scroll_to(sections[1])
        sections[1].click()
        element = self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.XPATH,
                 '//button[contains(@class, "show-problems")]')
            )
        )
        element.click()
        sleep(1)
        problems = self.teacher.find_all(
            By.XPATH, '//div[@class="controls-overlay"]'
        )
        self.teacher.scroll_to(problems[1])
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//div[contains(@class, "include")]')
            )
        ).click()
        sleep(1)

        # Cancel with "cancel" button
        cancel = self.teacher.find(
            By.XPATH,
            '//button[contains(@class,"show-problems")]'
            '/..//button[text()="Cancel"]'
        )
        self.teacher.scroll_to(cancel)
        cancel.click()

        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.XPATH, '//button[contains(@class, "ok")]')
            )
        ).click()
        assert "homework/new" in self.teacher.current_url(), \
            "not back to add homework page"

        # Select a problem
        self.teacher.find(By.ID, 'problems-select').click()
        sections = self.teacher.find_all(By.XPATH, '//input[@type="checkbox"]')
        self.teacher.scroll_to(sections[1])
        sections[1].click()
        element = self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.XPATH,
                 '//button[contains(@class, "show-problems")]')
            )
        )
        element.click()
        sleep(1)
        problems = self.teacher.find_all(
            By.XPATH, '//div[@class="controls-overlay"]'
        )
        self.teacher.scroll_to(problems[1])
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//div[contains(@class, "include")]')
            )
        ).click()
        sleep(1)

        # Cancel with "X" button
        x_button = self.teacher.find(
            By.XPATH,
            '//span[contains(text(),"Add Questions")]'
            '/..//button[contains(@class,"close-x")]'
        )
        self.teacher.scroll_to(x_button)
        sleep(1)
        x_button.click()

        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.XPATH, '//button[contains(@class, "ok")]')
            )
        ).click()

        # Select a problem
        self.teacher.find(By.ID, 'problems-select').click()
        sections = self.teacher.find_all(By.XPATH, '//input[@type="checkbox"]')
        self.teacher.scroll_to(sections[1])
        sections[1].click()
        element = self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.XPATH,
                 '//button[contains(@class, "show-problems")]')
            )
        )
        element.click()
        sleep(1)
        problems = self.teacher.find_all(
            By.XPATH, '//div[@class="controls-overlay"]'
        )
        self.teacher.scroll_to(problems[1])
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//div[contains(@class, "include")]')
            )
        ).click()
        sleep(1)

        # Cancel with "cancel" button next to "next" button
        add_cancel = self.teacher.find(
            By.XPATH,
            '//button[contains(@class,"cancel-add")]'
        )
        self.teacher.scroll_to(add_cancel)
        sleep(1)
        add_cancel.click()

        assert "homework/new" in self.teacher.current_url(), \
            "not at add homework page"

        self.ps.test_updates['passed'] = True

    # Case C30 - Teacher | View and reorder problems
    @pytest.mark.skipif(str(321) not in TESTS, reason="Excluded")
    def test_view_and_reorder_problems(self):
        """
        Steps:
        If the user has more than one course, select a Tutor course
        From the dashboard, click on the 'Add Assignment' drop down menu and
        select 'Add Homework'
        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select one of the non-introductory sections in one chapter
        Click the 'Show Problems' button
        Select at least one of the displayed problems
        Click the 'Next' button
        (User is returned to the page where assignment name, description, and
        open/due dates are set. Selected problems are displayed in the order
        they will appear.)

        Click one of the arrows on at least one problem
        (The ordering of the problems changes and the Problem Question list
        reflects the change the problem ordering.)

        Result:
        The number of total problems, my selections, and tutor selections in
        the Tutor Selection bar matches what the Problem Question list
        displays.

        """
        self.ps.test_updates['name'] = 't1.14.027' \
                                       + inspect.currentframe().f_code.co_name[
                                         4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.027', '8018']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'hw_20_%d' % (randint(100, 999))
        assignment = Assignment()
        today = datetime.date.today()
        finish = randint(1, 6)
        end = (today + datetime.timedelta(days=finish)).strftime('%m/%d/%Y')

        # Open Add Homework page
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Homework').click()

        # Fill in title
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        ).send_keys(assignment_name)
        sleep(1)

        # Set due date
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

        # Select a problem
        problems = {'1.1': (3)}
        assignment.add_homework_problems(self.teacher.driver, problems)
        sleep(3)

        # Reorder homework problems
        sections = self.teacher.find_all(
            By.XPATH, '//div[@class="lo-tag"]'
        )
        print(sections)
        second_sec = sections[1].text
        up_button = self.teacher.find(
            By.XPATH, '//button[contains(@class,"-move-exercise-up")]'
        )
        self.teacher.scroll_to(up_button)
        sleep(3)
        up_button.click()
        sections_new = self.teacher.find_all(
            By.XPATH, '//div[@class="lo-tag"]'
        )
        print(sections_new)
        new_first_sec = sections_new[0].text
        assert (second_sec == new_first_sec), \
            "problems not rearranged"

        # Publish and verify published status
        publish_button = self.teacher.find(
            By.XPATH,
            '//button[contains(@class,"-publish")]'
        )
        self.teacher.scroll_to(publish_button)
        sleep(3)
        publish_button.click()

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

    # Case C30 - Teacher | Test info icon and training wheels
    @pytest.mark.skipif(str(323) not in TESTS, reason="Excluded")
    def test_info_icon_and_training_wheels(self):
        """
        Steps:
        Click on the 'Add Assignment' sidebar menu
        Click on the "Add Homework" option
        Click on the info icon at the bottom
        (Instructions about the Publish, Cancel, and Save As Draft statuses
        appear)

        Click on the question mark dropdown menu in the navbar
        Select "Page Tips"
        (A training wheel appears)
        Click "Next" until the user exits the training wheel

        Click on the "?Help" dropdown menu in the navbar
        Select "Page Tips"
        Click "X" button on the top right corner of the training wheel
        (User exits the training wheel)

        Click on "What do students see" at the bottom of the page

        Result:
        A Youtube video window pops up, showing the student view of your
        assignment
        """
        self.ps.test_updates['name'] = 't1.14.001' \
                                       + inspect.currentframe().f_code.co_name[
                                         4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.001', '7992']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        # assignment_name = 'hw_23_%d' % (randint(100, 999))
        assignment = Assignment()

        # Open Add Homework page
        assignment.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Homework').click()
        assert ('homework/new' in self.teacher.current_url()), \
            'not at add homework screen'

        # Test info icon
        self.teacher.find(
            By.XPATH, '//button[contains(@class, "footer-instructions")]'
        ).click()
        self.teacher.find(By.ID, 'plan-footer-popover')

        # Test training wheel
        self.teacher.find(
            By.ID, 'support-menu'
        ).click()
        self.teacher.find(
            By.ID, 'menu-option-page-tips'
        ).click()

        # Walk through training wheel
        self.teacher.find(By.CLASS_NAME, 'joyride-overlay')
        while self.teacher.find_all(
                By.XPATH, '//button[contains(@data-type, "next")]'):
            self.teacher.find(By.XPATH,
                              '//button[contains(@data-type, "next")]').click()
            print(self.teacher.find_all(
                By.XPATH, '//button[contains(@data-type, "next")]'))

        # Exit training wheel halfway
        sleep(3)
        self.teacher.find(
            By.ID, 'support-menu'
        ).click()
        self.teacher.find(
            By.ID, 'menu-option-page-tips'
        ).click()
        self.teacher.find(
            By.XPATH, '//button[contains(@data-type, "next")]'
        ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contains(@data-type, "close")]')
            )
        ).click()

        # Test "What do students see" button
        self.teacher.find(
            By.XPATH, '//button[contains(@class, "preview-btn")]'
        ).click()
        video_window = self.teacher.driver.window_handles[1]
        self.teacher.driver.switch_to_window(video_window)
        self.teacher.find(
            By.XPATH, '//div[contains(@class, "student-preview")]'
        )
        sleep(2)
        self.ps.test_updates['passed'] = True

    # Case C324 - Teacher | Get assignment link and review metrics
    @pytest.mark.skipif(str(324) not in TESTS, reason="Excluded")
    def test_get_assignment_link_and_review_metrics(self):
        """
        Steps:
        Click on an existing homework on the calendar
        Click "Get assignment link"
        (A link for the reading assignment pops up)

        Click on "Review metrics" button
        (The teacher is taken to a page that shows problems with answers in the
        assigned reading chapters and students' progress in this reading
        assignment )

        Click on "Back to Dashboard" button

        Result:
        The teacher is taken to the homework summary page
        """
        self.ps.test_updates['name'] = 't1.14.018' \
                                       + inspect.currentframe().f_code.co_name[
                                         4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.018', '8009']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'hw_024_%s' % randint(100, 999)
        today = datetime.date.today()
        finish = randint(1, 5)
        begin = today.strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=finish)) \
            .strftime('%m/%d/%Y')

        # Create an open homework
        self.teacher.add_assignment(
            assignment='homework',
            args={
                'title': assignment_name,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'problems': {'1.1': (2, 3), },
                'status': 'publish',
                'feedback': 'immediate',
            }
        )

        # View assignment summary
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'month-wrapper')
            )
        )
        self.teacher.find(
            By.XPATH, '//label[contains(text(),"{0}")]'.format(assignment_name)
        ).click()

        # Get assignment link
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'lms-info-link')
            )
        ).click()
        sleep(3)
        self.teacher.find(
            By.XPATH, '//div[contains(@id, "sharable-link-popover")]'
        )

        # Review metrics
        self.teacher.find(
            By.ID, 'view-metrics'
        ).click()
        assert ("metrics/" in self.teacher.current_url()), \
            "not at Review Metrics page"

        self.ps.test_updates['passed'] = True
