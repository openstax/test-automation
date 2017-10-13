"""Tutor External Assignment Teacher"""

import datetime
import inspect
import json
import os
import pytest
# import random
import unittest

from pastasauce import PastaSauce, PastaDecorator
from random import randint
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
# from selenium.webdriver.support.ui import WebDriverWait
from staxing.assignment import Assignment
from time import sleep

# select user types: Teacher
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
        146489, 146490, 146491, 146492, 146493,
        146494, 146495, 146496, 146497, 146498,
        146499, 146500, 146501, 146502, 146503,
        146504, 146505, 146506
        # 146504

    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestCreateAnExternalAssignment(unittest.TestCase):
    """T1.14 - Create a Reading."""

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

    # Case C146489 001 - Teacher | Add a new open external assignment for all
    # periods
    @pytest.mark.skipif(str(146489) not in TESTS, reason='Excluded')
    def test_teacher_add_new_open_external_assignment_all_periods_146489(self):
        """
        Add a new open external assignment for all periods

        Steps:
        Click on the 'Add Assignment' menu
        Click on the 'Add External Assignment' option
        (The teacher is taken to the page where they create the assignment.)

        Enter a name to the 'Assignment name' text box
        Enter a description in the 'Description or special instructions'

        [Select the 'All Periods' radio button if not selected by default]
        Type or select today's date for the assignment using the calendar
        element
        Type 00:00am as the the open time for the assignment using the calendar
        element
        Type or select a due date in the future for the assignment using the
        calendar element
        Enter an assignment URL to the 'Assignment URL' text box
        Click "Publish"

        Expected result:
        Takes user back to calendar dashboard.
        An open external assignment appears on user calendar dashboard on due
        date.
        """
        self.ps.test_updates['name'] = 'tutor_external_teacher' \
                                       + inspect.currentframe().f_code.co_name[
                                         4:]
        self.ps.test_updates['tags'] = [
            'tutor',
            'external',
            'teacher',
            '146489'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'external_001_%d' % (randint(100, 999))
        assignment = Assignment()

        # Open Add Reading page
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add External Assignment').click()
        assert ('external/new' in self.teacher.current_url()), \
            'not at add external assignment screen'

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

        # Set date
        today = datetime.date.today()
        end = randint(1, 5)
        opens_on = today.strftime(
            '%m/%d/%Y')  # make the start date today so it will be open
        closes_on = (today + datetime.timedelta(days=end)) \
            .strftime('%m/%d/%Y')
        assignment.assign_periods(
            self.teacher.driver, {'all': (opens_on, closes_on)})

        # add external link to the assignment
        self.teacher.find(
            By.ID, "external-url"
        ).send_keys("www.openstax.org")

        # publish
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

    # Case C146490 002 - Teacher | Save a draft external assignment for
    # individual periods
    @pytest.mark.skipif(str(146490) not in TESTS, reason='Excluded')
    def test_teacher_save_draft_external_assignment_indiv_periods_146490(self):
        """
        Save a draft external assignment for individual periods

        Steps:
        Click on the Add Assignment drop down menu on the user dashboard, OR
        click a calendar date that is at least one day later than the current
        date
        Click on the 'Add External Assignment' button
        Select the 'Individual Periods' radio button
        Select the periods that should be required to complete the assignment
        Type in or select open and due dates for each period using the calendar
        element

        Enter an assignment URL into the Assignment URL text box
        Click on the "Save As Draft" button

        Expected result:
        Takes user back to calendar dashboard.
        Assignment appears on user calendar dashboard on due date. 'draft'
        should appear before the assignment name.
        """
        self.ps.test_updates['name'] = 'tutor_external_teacher' \
                                       + inspect.currentframe().f_code.co_name[
                                         4:]
        self.ps.test_updates['tags'] = ['tutor', 'external', 'teacher',
                                        '146490']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'external_002_%d' % (randint(100, 999))
        assignment = Assignment()

        # Open Add Reading page
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add External Assignment').click()
        assert ('external/new' in self.teacher.current_url()), \
            'not at add readings screen'

        # Find and fill in title
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        ).send_keys(assignment_name)

        # Set date
        today = datetime.date.today()
        start = randint(0, 6)
        end = start + randint(1, 5)
        opens_on = (today + datetime.timedelta(days=start)) \
            .strftime('%m/%d/%Y')
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

        # add assignment url
        self.teacher.find(
            By.ID, "external-url"
        ).send_keys("www.openstax.org")

        # Save as draft
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'builder-draft-button')
            )
        ).click()

        # Check if the draft is on the dashboard
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

    # Case C146491 003 - Teacher | Add a new unopened external assignment from
    # calendar
    @pytest.mark.skipif(str(146491) not in TESTS, reason='Excluded')
    def test_teacher_add_new_unopened_extern_assignment_calendar_146491(self):
        """
        Add a new unopened external assignment from calendar

        Steps:
        Click on a date at least one day after the current date on the calendar
        From the menu that appears, click on 'Add Homework'

        Select the 'All Periods' radio button if it is not selected by default]
        Type or select an open date in the future for the assignment using the
        calendar element
        Type or select a due date in the future for the assignment using the
        calendar element

        Enter the assignment URL into the Assignment URL text box
        Click "Publish"

        Expected result:
        Takes user back to calendar dashboard.
        An unopened external assignment appears on user calendar dashboard on
        due date.
        """
        self.ps.test_updates['name'] = 'tutor_external_teacher' \
                                       + inspect.currentframe().f_code.co_name[
                                         4:]
        self.ps.test_updates['tags'] = ['tutor', 'external', 'teacher',
                                        '146491']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        calendar_date = self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//div[contains(@class,"Day--upcoming")]')
            )
        )
        self.teacher.driver.execute_script(
            'return arguments[0].scrollIntoView();',
            calendar_date
        )
        self.teacher.sleep(1)
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(calendar_date)
        actions.move_by_offset(0, -35)
        actions.click()
        actions.move_by_offset(30, 75)
        actions.click()
        actions.perform()

        assert ('external/new' in self.teacher.current_url()), \
            'not at Add External Assignment page'

        assignment_name = 'external_003_%d' % (randint(100, 999))
        assignment = Assignment()

        # Find and fill in title
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        ).send_keys(assignment_name)

        # Fill in description
        self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]' +
            '//textarea[contains(@class,"form-control")]'
        ).send_keys('description')
        # or change it to span .assignment-description > .form-control

        # Set date
        today = datetime.date.today()
        start = randint(1, 5)
        end = start + randint(1, 5)

        # the open date should be in the future for the assignment to be
        # unopened
        opens_on = (today + datetime.timedelta(days=start)) \
            .strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=end)) \
            .strftime('%m/%d/%Y')
        assignment.assign_periods(
            self.teacher.driver, {'all': (opens_on, closes_on)})

        # Add assignment url
        self.teacher.find(
            By.ID, "external-url"
        ).send_keys("www.openstax.org")
        # Publish
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class, "-publish")]')
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
                '//label[contains(text(),"{0}")]'.format(assignment_name))

        self.ps.test_updates['passed'] = True

    # Case C146492 004 - Teacher | Publish a draft external assignment
    @pytest.mark.skipif(str(146492) not in TESTS, reason='Excluded')
    def test_teacher_publish_a_draft_external_assignment_146492(self):
        """
        Publish a draft external assignment

        Steps:
        Go to https://tutor-qa.openstax.org/
        Login with teacher username and password
        If the user has more than one course, click on a Tutor course name

        On the calendar click on an assignment that is currently a draft
        Click on the 'Publish' button

        Expected result:
        Takes user back to calendar dashboard.
        Assignment appears on user calendar dashboard on due date.
        """
        self.ps.test_updates['name'] = 'tutor_external_teacher' \
                                       + inspect.currentframe().f_code.co_name[
                                         4:]
        self.ps.test_updates['tags'] = ['tutor', 'external', 'teacher',
                                        '146492']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'external_004_%s' % randint(100, 999)
        today = datetime.date.today()
        start = randint(0, 6)
        finish = start + randint(1, 5)
        begin = (today + datetime.timedelta(days=start)) \
            .strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=finish)) \
            .strftime('%m/%d/%Y')
        self.teacher.add_assignment(
            assignment='external',
            args={
                'title': assignment_name,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'url': 'www.openstax.org',
                'status': 'draft',
            }
        )

        # Find the draft external assignment on the calendar
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'month-wrapper')
            )
        )
        self.teacher.find(
            By.XPATH, '//label[contains(text(),"{0}")]'.format(assignment_name)
        ).click()

        # Publish the draft assignment
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

    # Case C146493 005 - Teacher | Cancel a new external assignment before
    # changes
    @pytest.mark.skipif(str(146493) not in TESTS, reason='Excluded')
    def test_teacher_cancel_new_extern_assignment_before_changes_146493(self):
        """
        Cancel a new external assignment before changes

        Steps:
        Click on the 'Add Assignment' menu
        Click on the 'Add External Assignment' option

        Click on the 'Cancel' button
        (User is taken back to calendar dashboard. No changes have been made)

        Click on the 'Add Assignment' menu
        Click on the 'Add External Assignment' option

        Click on the 'X' button

        Expected result:
        Takes user back to calendar dashboard. No changes have been made to the
        calendar on the dashboard
        """
        self.ps.test_updates['name'] = 'tutor_external_teacher' \
                                       + inspect.currentframe().f_code.co_name[
                                         4:]
        self.ps.test_updates['tags'] = ['tutor', 'external', 'teacher',
                                        '146493']
        self.ps.test_updates['passed'] = False

        # Open "Add External Assignment" page
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add External Assignment').click()
        assert ('external/new' in self.teacher.current_url()), \
            'not at add external assignment screen'

        # Cancel a reading with "Cancel" button
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'builder-cancel-button')
            )
        ).click()
        assert ('month' in self.teacher.current_url()), \
            'not back at calendar after cancelling external assignment'

        # Open "Add External Assignment" page
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add External Assignment').click()
        assert ('external/new' in self.teacher.current_url()), \
            'not at add external assignment screen'

        # Cancel an external assignment with "X" button
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class,"openstax-close-x")]')
            )
        ).click()
        assert ('month' in self.teacher.current_url()), \
            'not back at calendar after cancelling external assignment'

        self.ps.test_updates['passed'] = True

    # Case C146494 006 - Teacher | Cancel a new external assignment after
    # changes
    @pytest.mark.skipif(str(146494) not in TESTS, reason='Excluded')
    def test_teacher_cancel_new_external_assignment_after_changes_146494(self):
        """
        Cancel a new external assignment after changes

        Steps:
        Click on the 'Add Assignment' menu
        Click on the 'Add External Assignment' option

        Enter an assignment name into the Assignment name text box
        [user decision]
        Click the 'Cancel' button
        Click the 'Yes' button
        (Takes user back to calendar dashboard. No changes have been made to
        the calendar on the dashboard)

        Click on the 'Add Assignment' menu
        Click on the 'Add External Assignment' option

        Enter an assignment name into the Assignment name text box
        [user decision]
        Click the 'X' button
        Click the 'Yes' button

        Expected result:
        Takes user back to calendar dashboard.
        No changes have been made to the calendar on the dashboard
        """
        self.ps.test_updates['name'] = 'tutor_external_teacher' \
                                       + inspect.currentframe().f_code.co_name[
                                         4:]
        self.ps.test_updates['tags'] = ['tutor', 'external', 'teacher',
                                        '146494']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'external_006_%d' % (randint(100, 999))

        # Open "Add External Assignment" page
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add External Assignment').click()
        assert ('external/new' in self.teacher.current_url()), \
            'not at add external assignment screen'

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
            'not back at calendar after cancelling external assignment'

        # Open "Add External Assignment" page
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add External Assignment').click()
        assert ('external/new' in self.teacher.current_url()), \
            'not at add external assignment screen'

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
            'not back at calendar after cancelling external assignment'

        self.ps.test_updates['passed'] = True

    # Case C146495 007 - Teacher | Cancel a draft external assignment before
    # changes
    @pytest.mark.skipif(str(146495) not in TESTS, reason='Excluded')
    def test_teacher_cancel_draft_extern_assignment_before_change_146495(self):
        """
        Cancel a draft external assignment before changes

        Steps:
        On the calendar click on a draft external assignment
        Click on the 'Cancel' button

        On the calendar click on a draft external assignment
        Click on the 'X' button

        Expected result:
        Takes user back to calendar dashboard.
        No changes have been made to the chosen draft on the calendar dashboard
        """
        self.ps.test_updates['name'] = 'tutor_external_teacher' \
                                       + inspect.currentframe().f_code.co_name[
                                         4:]
        self.ps.test_updates['tags'] = ['tutor', 'external', 'teacher',
                                        '146495']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name_1 = 'external_007_%s' % randint(100, 500)
        assignment_name_2 = 'external_007_%s' % randint(500, 999)

        today = datetime.date.today()
        finish = randint(1, 5)
        begin = today.strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=finish)) \
            .strftime('%m/%d/%Y')

        # Create a draft assignment
        self.teacher.add_assignment(
            assignment='external',
            args={
                'title': assignment_name_1,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'url': 'www.openstax.org',
                'status': 'draft',
            }
        )

        # Find the draft external assignment on the calendar
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

        # Check if teacher is taken to user dashboard
        self.teacher.page.wait_for_page_load()
        assert ('month' in self.teacher.current_url()), \
            'not back at calendar after cancelling external assignment'

        # Add a draft external assignment
        self.teacher.add_assignment(
            assignment='external',
            args={
                'title': assignment_name_2,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'url': 'www.openstax.org',
                'status': 'draft',
            }
        )

        # Find the draft external assignment on the calendar
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
            'not back at calendar after cancelling external assignment'

        self.ps.test_updates['passed'] = True

    # Case C146496 008 - Teacher | Cancel a draft external assignment after
    # changes
    @pytest.mark.skipif(str(146496) not in TESTS, reason='Excluded')
    def test_teacher_cancel_draft_extern_assignment_after_change_146496(self):
        """
        Cancel a draft external assignment after chagnes

        Steps:
        On the Calendar Click on a draft external assignment

        Enter an assignment name into the Assignment name text box
        Click the 'Cancel' button
        Click the 'Yes' button

        On the calendar click on a draft external assignment
        Enter an assignment name into the Assignment name text box
        Click on the 'X' button
        Click on the 'Yes' button

        Expected result:
        Takes user back to calendar dashboard.
        No changes have been made to the chosen draft on the calendar dashboard
        """
        self.ps.test_updates['name'] = 'tutor_external_teacher' \
                                       + inspect.currentframe().f_code.co_name[
                                         4:]
        self.ps.test_updates['tags'] = ['tutor', 'external', 'teacher',
                                        '146496']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name_1 = 'external_008_%s' % randint(100, 500)
        assignment_name_2 = 'external_008_%s' % randint(500, 999)

        today = datetime.date.today()
        finish = randint(1, 5)
        begin = today.strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=finish)) \
            .strftime('%m/%d/%Y')

        # Create a draft assignment
        self.teacher.add_assignment(
            assignment='external',
            args={
                'title': assignment_name_1,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'url': 'www.openstax.org',
                'status': 'draft',
            }
        )

        # Find the draft external assignment on the calendar
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

        # Edit the assignment
        self.teacher.find(
            By.ID, "reading-title"
        ).send_keys('changed')

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
            'not back at calendar after cancelling external assignment'

        # Create a draft assignment
        self.teacher.add_assignment(
            assignment='external',
            args={
                'title': assignment_name_2,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'url': 'www.openstax.org',
                'status': 'draft',
            }
        )

        # Find the draft external assignment on the calendar
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

        # Edit the assignment
        self.teacher.find(
            By.ID, "reading-title"
        ).send_keys('changed')

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
            'not back at calendar after cancelling external assignment'

        self.ps.test_updates['passed'] = True

    # Case C146497 009 - Teacher | Attempt to save/publish an external
    # assignment with blank required fields
    @pytest.mark.skipif(str(146497) not in TESTS, reason='Excluded')
    def test_teacher_attempt_publish_or_save_with_blank_req_field_146497(self):
        """
        Attempt to save or publish an external assignment with blank required
        fields

        Steps:
        Click on the 'Add Assignment' menu
        Click on the 'Add External Assignment' option
        Click on the 'Publish' button
        (Remains on the Add External Assignment page. Does not allow user to
        publish assignments. All required fields that were left blank become
        red, and specify that they are required fields.)

        Refresh the browser
        Click on the 'Save As Draft' button

        Expected result:
        Remains on the Add External Assignment page. Does not allow user to
        save assignments.
        All required fields that were left blank become red, and specify that
        they are required fields
        """
        self.ps.test_updates['name'] = 'tutor_external_teacher' \
                                       + inspect.currentframe().f_code.co_name[
                                         4:]
        self.ps.test_updates['tags'] = ['tutor', 'external', 'teacher',
                                        '146497']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add External Assignment').click()
        assert ('external/new' in self.teacher.current_url()), \
            'not at add external assignment screen'

        # Publish without filling in any fields
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class,"-publish")]')
            )
        ).click()

        # Required field reminder
        self.teacher.find(
            By.XPATH, '//div[contains(text(),"Required field")]')
        assert ('external' in self.teacher.current_url()), \
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

        # Required field reminder
        self.teacher.find(
            By.XPATH, '//div[contains(text(),"Required field")]')
        assert ('external' in self.teacher.current_url()), \
            'went back to calendar even though required fields were left blank'

        self.ps.test_updates['passed'] = True

    # Case C146498 010 - Teacher | Delete a draft external assignment
    @pytest.mark.skipif(str(146498) not in TESTS, reason='Excluded')
    def test_teacher_delete_a_draft_external_assignment_146498(self):
        """
        Delete a draft external assignment

        Steps:
        On the calendar click on a draft external assignment
        Click on the 'Delete Assignment' button
        Click "Yes" on the dialog box that appears

        Expected result:
        Takes user back to calendar dashboard.
        Chosen assignment no longer appears on teacher calendar dashboard
        """
        self.ps.test_updates['name'] = 'tutor_external_teacher' \
                                       + inspect.currentframe().f_code.co_name[
                                         4:]
        self.ps.test_updates['tags'] = ['tutor', 'external', 'teacher',
                                        '146498']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'external_010_%s' % randint(100, 500)

        today = datetime.date.today()
        finish = randint(1, 5)
        begin = today.strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=finish)) \
            .strftime('%m/%d/%Y')

        # Create a draft assignment
        self.teacher.add_assignment(
            assignment='external',
            args={
                'title': assignment_name,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'url': 'www.openstax.org',
                'status': 'draft',
            }
        )

        # Find the draft external assignment on the calendar
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'month-wrapper')
            )
        )
        self.teacher.find(
            By.XPATH,
            '//label[contains(text(),"{0}")]'.format(assignment_name)
        ).click()
        sleep(1)

        # Delete the draft assignment
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"delete-link")]')
            )
        ).click()
        self.teacher.find(
            By.XPATH, '//button[contains(text(),"Yes")]'
        ).click()
        sleep(3)

        assert ('month' in self.teacher.current_url()), \
            'not returned to calendar after deleting an assignment'

        # have to refresh to remove the assignment tab from calendar
        self.teacher.driver.refresh()
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'month-wrapper')
            )
        )
        deleted_external = self.teacher.find_all(
            By.XPATH, '//label[@data-title="{0}"]'.format(assignment_name)
        )
        assert (len(deleted_external) == 0), 'external assignment not deleted'

        self.ps.test_updates['passed'] = True

    # Case C146499 011 - Teacher | Delete an unopened external assignment
    @pytest.mark.skipif(str(146499) not in TESTS, reason='Excluded')
    def test_teacher_delete_an_unopened_external_assignment_146499(self):
        """
        Delete an unopened external assignment

        Steps:
        On the calendar click on an external assignment that is unopened
        Click on the 'Edit Assignment' button
        Click on the 'Delete Assignment' button
        Click "Yes" on the dialog box that appears

        Expected result:
        Takes user back to calendar dashboard.
        Chosen assignment no longer appears on teacher calendar dashboard
        """
        self.ps.test_updates['name'] = 'tutor_external_teacher' \
                                       + inspect.currentframe().f_code.co_name[
                                         4:]
        self.ps.test_updates['tags'] = ['tutor', 'external', 'teacher',
                                        '146499']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'external_011_%s' % randint(100, 500)

        today = datetime.date.today()
        start = randint(2, 3)
        finish = start + randint(1, 5)
        begin = (today + datetime.timedelta(days=start))\
            .strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=finish)) \
            .strftime('%m/%d/%Y')

        # Create an unopened assignment
        self.teacher.add_assignment(
            assignment='external',
            args={
                'title': assignment_name,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'url': 'www.openstax.org',
                'status': 'publish',
            }
        )

        # Find the unopened external assignment on the calendar
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'month-wrapper')
            )
        )
        self.teacher.find(
            By.XPATH,
            '//label[contains(text(),"{0}")]'.format(assignment_name)
        ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'edit-assignment-button')
            )
        ).click()

        # Delete the assignment
        delete_button = self.teacher.find(
            By.XPATH, '//button[contains(@class,"delete-link")]'
        )
        self.teacher.scroll_to(delete_button)
        delete_button.click()
        sleep(3)
        confirm_button = self.teacher.find(
            By.XPATH, '//button[contains(text(),"Yes")]'
        )
        self.teacher.scroll_to(confirm_button)
        confirm_button.click()
        sleep(3)

        assert ('month' in self.teacher.current_url()), \
            'not returned to calendar after deleting an assignment'

        # Have to refresh the browser to remove assignment tab from calendar
        self.teacher.driver.refresh()
        deleted_unopened = self.teacher.find_all(
            By.XPATH, '//label[@data-title="{0}"]'.format(assignment_name)
        )
        assert len(deleted_unopened) == 0, 'unopened reading not deleted'

        self.ps.test_updates['passed'] = True

    # Case C146500 012 - Teacher | Delete an open external assignment
    @pytest.mark.skipif(str(146500) not in TESTS, reason='Excluded')
    def test_teacher_delete_an_open_external_assignment_146500(self):
        """
        Delete an open external assignment

        Steps:
        On the calendar click on an open external assignment
        Click on the 'Edit Assignment' button
        Click "Delete Assignment"
        Click "Yes"

        Expected result:
        Takes user back to calendar dashboard.
        Chosen assignment no longer appears on teacher calendar dashboard
        """
        self.ps.test_updates['name'] = 'tutor_external_teacher' \
                                       + inspect.currentframe().f_code.co_name[
                                         4:]
        self.ps.test_updates['tags'] = ['tutor', 'external', 'teacher',
                                        '146500']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'external_012_%s' % randint(100, 500)

        today = datetime.date.today()
        finish = randint(1, 5)
        begin = today.strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=finish)) \
            .strftime('%m/%d/%Y')

        # Create an unopened assignment
        self.teacher.add_assignment(
            assignment='external',
            args={
                'title': assignment_name,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'url': 'www.openstax.org',
                'status': 'publish',
            }
        )

        # Find the open external assignment on the calendar
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'month-wrapper')
            )
        )
        self.teacher.find(
            By.XPATH,
            '//label[contains(text(),"{0}")]'.format(assignment_name)
        ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'edit-assignment-button')
            )
        ).click()

        # Delete the assignment
        delete_button = self.teacher.find(
            By.XPATH, '//button[contains(@class,"delete-link")]'
        )
        self.teacher.scroll_to(delete_button)
        delete_button.click()
        sleep(3)
        confirm_button = self.teacher.find(
            By.XPATH, '//button[contains(text(),"Yes")]'
        )
        self.teacher.scroll_to(confirm_button)
        confirm_button.click()
        sleep(3)

        assert ('month' in self.teacher.current_url()), \
            'not returned to calendar after deleting an assignment'

        # Have to refresh the browser to remove assignment tab from calendar
        self.teacher.driver.refresh()
        deleted_unopened = self.teacher.find_all(
            By.XPATH, '//label[@data-title="{0}"]'.format(assignment_name)
        )
        assert len(deleted_unopened) == 0, \
            'open external assignment not deleted'

        self.ps.test_updates['passed'] = True

    # Case C146501 013 - Teacher | Change a draft external assignment
    @pytest.mark.skipif(str(146501) not in TESTS, reason='Excluded')
    def test_teacher_change_a_draft_external_assignment_146501(self):
        """
        Change a draft assignment

        Steps:
        Click on a draft external assignment on the calendar

        Enter a new assignment name into the Assignment name text box
        [user decision]
        Enter a new assignment description into the Assignment description or
        special instructions text box
        Click on the Open Date text field, and click on a new Open Date on the
        calendar
        Click on the Due Date text field and click on a new Due Date on the
        calendar
        Enter a new assignment URL into the Assignment URL text
        Click the 'Save As Draft' button

        Expected result:
        Takes user back to the calendar dashboard.
        The name, description, due dates, and assignment URL of the external
        assignment have been updated.
        The draft external assignment now appears on its new due date on the
        calendar.
        """
        self.ps.test_updates['name'] = 'tutor_external_teacher' \
                                       + inspect.currentframe().f_code.co_name[
                                         4:]
        self.ps.test_updates['tags'] = ['tutor', 'external', 'teacher',
                                        '146501']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'external_013_%s' % randint(100, 500)
        assignment = Assignment()
        today = datetime.date.today()
        finish = randint(1, 5)
        begin = today.strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=finish)) \
            .strftime('%m/%d/%Y')

        # Create a draft assignment
        self.teacher.add_assignment(
            assignment='external',
            args={
                'title': assignment_name,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'url': 'www.openstax.org',
                'status': 'draft',
            }
        )

        # Find the draft external assignment on the calendar
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'month-wrapper')
            )
        )
        self.teacher.find(
            By.XPATH,
            '//label[contains(text(),"{0}")]'.format(assignment_name)
        ).click()
        sleep(1)

        # Change the title
        self.teacher.find(
            By.ID, "reading-title"
        ).send_keys("changed")

        # Change the description
        self.teacher.find(
            By.CSS_SELECTOR, ".assignment-description>.form-control"
        ).send_keys("changed")

        # Set new due dates
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

        # Change external assignment url
        url_form = self.teacher.find(By.ID, "external-url")
        url_form.clear()
        url_form.send_keys("https://cnx.org")

        # Save as draft
        self.teacher.find(
            By.XPATH, '//button[contains(@class,"-save")]'
        ).click()
        sleep(1)

        # Find the new title on the calendar
        try:
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(
                    assignment_name + 'changed')
            )
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH,
                '//a[contains(@class,"header-control next")]'
            ).click()
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(
                    assignment_name + 'changed')
            )

        self.ps.test_updates['passed'] = True

    # Case C146502 014 - Teacher | Change an unopened external assignment
    @pytest.mark.skipif(str(146502) not in TESTS, reason='Excluded')
    def test_teacher_change_an_unopened_external_assignment_146502(self):
        """
        Change an unopened external assignment

        Steps:
        Click on an unopened, published external assignment on the calendar
        Click on the 'Edit Assignment' option

        Enter a new assignment name into the Assignment name text box
        Enter a new assignment description into the Assignment description or
        special instructions text box
        Click on the Open Date text field, and click on a new Open Date on the
        calendar
        Click on the Due Date text field, and click on a new Due Date on the
        calendar
        Enter a new assignment URL into the Assignment URL text box

        Click the 'Save' button

        Expected result:
        Takes user bak to the calendar dashboard.
        The name, description, due dates, and assignment URL of the external
        assignment have been updated.
        The external assignment now appears on its new due date on the
        calendar.
        """
        self.ps.test_updates['name'] = 'tutor_external_teacher' \
                                       + inspect.currentframe().f_code.co_name[
                                         4:]
        self.ps.test_updates['tags'] = ['tutor', 'external', 'teacher',
                                        '146502']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'external_014_%s' % randint(100, 500)
        assignment = Assignment()

        today = datetime.date.today()
        start = randint(2, 3)
        finish = start + randint(1, 5)
        begin = (today + datetime.timedelta(days=start)) \
            .strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=finish)) \
            .strftime('%m/%d/%Y')

        # Create an unopened assignment
        self.teacher.add_assignment(
            assignment='external',
            args={
                'title': assignment_name,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'url': 'www.openstax.org',
                'status': 'publish',
            }
        )

        # Find the unopened external assignment on the calendar
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'month-wrapper')
            )
        )
        self.teacher.find(
            By.XPATH,
            '//label[contains(text(),"{0}")]'.format(assignment_name)
        ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'edit-assignment-button')
            )
        ).click()

        # Change the title
        self.teacher.find(
            By.ID, "reading-title"
        ).send_keys("changed")

        # Change the description
        self.teacher.find(
            By.CSS_SELECTOR, ".assignment-description>.form-control"
        ).send_keys("changed")

        # Set new due dates
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

        # Publish
        self.teacher.find(
            By.XPATH, '//button[contains(@class,"-publish")]'
        ).click()
        sleep(1)

        # Find the new title on the calendar
        try:
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(
                    assignment_name + 'changed')
            )
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH,
                '//a[contains(@class,"header-control next")]'
            ).click()
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(
                    assignment_name + 'changed')
            )

        self.ps.test_updates['passed'] = True

    # Case C146503 015 - Teacher | Change an open external assignment
    @pytest.mark.skipif(str(146503) not in TESTS, reason='Excluded')
    def test_teacher_change_an_open_external_assignment_146503(self):
        """
        Change an open external assignment

        Steps:
        Click on an open external assignment on the calendar
        Click on the 'Edit Assignment' option

        Enter a new assignment name into the Assignment name text box
        [user decision]
        Enter a new assignment description into the Assignment description or
        special instructions text box
        Click on the Due Date text field, and click on a new Due Date on the
        calendar
        Click the 'Save' button

        Expected result:
        Takes user back to the calendar dashboard.
        The name, description and due dates of the external assignment have
        been updated.
        The external assignment now appears on its new due date on the
        calendar.
        """
        self.ps.test_updates['name'] = 'tutor_external_teacher' \
                                       + inspect.currentframe().f_code.co_name[
                                         4:]
        self.ps.test_updates['tags'] = ['tutor', 'external', 'teacher',
                                        '146503']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'external_015_%s' % randint(100, 500)
        assignment = Assignment()

        today = datetime.date.today()
        finish = randint(1, 5)
        begin = today.strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=finish)) \
            .strftime('%m/%d/%Y')

        # Create an open assignment
        self.teacher.add_assignment(
            assignment='external',
            args={
                'title': assignment_name,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'url': 'www.openstax.org',
                'status': 'publish',
            }
        )

        # Find the open external assignment on the calendar
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'month-wrapper')
            )
        )
        self.teacher.find(
            By.XPATH,
            '//label[contains(text(),"{0}")]'.format(assignment_name)
        ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'edit-assignment-button')
            )
        ).click()

        # Change the title
        self.teacher.find(
            By.ID, "reading-title"
        ).send_keys("changed")

        # Change the description
        self.teacher.find(
            By.CSS_SELECTOR, ".assignment-description>.form-control"
        ).send_keys("changed")

        # Set new due dates
        end = randint(1, 5)
        closes_on = (today + datetime.timedelta(days=end)) \
            .strftime('%m/%d/%Y')
        assignment.assign_date(
            driver=self.teacher.driver, date=closes_on, is_all=True,
            target='due'
        )

        # Publish
        self.teacher.find(
            By.XPATH, '//button[contains(@class,"-publish")]'
        ).click()
        sleep(1)

        # Find the new title on the calendar
        try:
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(
                    assignment_name + 'changed')
            )
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH,
                '//a[contains(@class,"header-control next")]'
            ).click()
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(
                    assignment_name + 'changed')
            )

        self.ps.test_updates['passed'] = True

    # Case C146504 016 - Teacher | Add an external assignment by dragging and
    # dropping
    @pytest.mark.skipif(str(146504) not in TESTS, reason='Excluded')
    def test_teacher_add_an_ext_assignment_by_drag_and_drop_146504(self):
        """
        Steps:
        Click on the 'Add Assignment' menu
        Click and Drag 'Add External Assignment' to a chosen due date

        Expected result:
        User is taken to 'Add External Assignment' page, and due date is filled
        in as date dragged to
        """
        self.ps.test_updates['name'] = 'tutor_external_teacher' \
                                       + inspect.currentframe().f_code.co_name[
                                         4:]
        self.ps.test_updates['tags'] = ['tutor', 'external', 'teacher',
                                        '146504']
        self.ps.test_updates['passed'] = False

        # Test verification
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        external_tab = self.teacher.find(
            By.LINK_TEXT, 'Add External Assignment'
        )

        due_date = self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//div[contains(@class,"Day--upcoming")]')
            )
        )
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(external_tab)

        actions.drag_and_drop(external_tab, due_date).perform()
        sleep(3)

        assert ('external/new' in self.teacher.current_url()), \
            'not at Add External Assignment page'

        self.ps.test_updates['passed'] = True

    # Case C146505 017 - Teacher | Info Icons
    @pytest.mark.skipif(str(146505) not in TESTS, reason='Excluded')
    def test_teacher_info_icons_146505(self):
        """
        Test info icons

        Steps:
        Click on the 'Add Assignment' sidebar menu
        Click on the "Add External Assignment" option

        Click on the info icon at the bottom

        Expected result:
        Displays description of Publish, Cancel, and Save As Draft statuses.
        """
        self.ps.test_updates['name'] = 'tutor_external_teacher' \
                                       + inspect.currentframe().f_code.co_name[
                                         4:]
        self.ps.test_updates['tags'] = ['tutor', 'external', 'teacher',
                                        '146505']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'external_017_%d' % (randint(100, 999))
        print(assignment_name)
        assignment = Assignment()

        # Open Add External Assignment page
        assignment.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add External Assignment').click()
        assert ('external/new' in self.teacher.current_url()), \
            'not at add external assignment screen'

        # Test info icon
        self.teacher.find(
            By.XPATH, '//button[contains(@class, "footer-instructions")]'
        ).click()
        self.teacher.find(By.ID, 'plan-footer-popover')

        self.ps.test_updates['passed'] = True

    # Case C146506 018 - Teacher | Get assignment links and review metrics
    @pytest.mark.skipif(str(146506) not in TESTS, reason='Excluded')
    def test_teacher_get_assignment_links_and_review_metrics_146506(self):
        """
        Get assignment link and review metrics

        Steps:
        Click on an existing homework on the calendar
        Click "Get assignment link"
        (A link for the reading assignment pops up)

        Click on "Review metrics" button
        (The teacher is taken to a page that shows problems with answers in the
        assigned reading chapters and students' progress in this reading
        assignment)
        Click on "Back to Dashboard" button

        Expected result:
        The teacher is taken to the external assignment summary page
        """
        self.ps.test_updates['name'] = 'tutor_external_teacher' \
                                       + inspect.currentframe().f_code.co_name[
                                         4:]
        self.ps.test_updates['tags'] = ['tutor', 'external', 'teacher',
                                        '146506']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        open_title = 'open_external018_%s' % (randint(100, 999))
        today = datetime.date.today()
        start = randint(2, 6)
        finish = start + randint(1, 5)
        begin_today = today.strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=finish)).strftime('%m/%d/%Y')

        self.teacher.add_assignment(
            assignment='external',
            args={
                'title': open_title,
                'description': 'description',
                'periods': {'all': (begin_today, end)},
                'url': 'www.openstax.org',
                'status': 'publish'
            }
        )

        # View assignment summary
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'month-wrapper')
            )
        )
        self.teacher.find(
            By.XPATH, '//label[contains(text(),"{0}")]'.format(open_title)
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
