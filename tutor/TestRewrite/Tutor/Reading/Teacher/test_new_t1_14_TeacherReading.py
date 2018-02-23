"""Tutor v1, Epic 14 - Create a Reading."""

import datetime
import inspect
import json
import os
import pytest
import random
import unittest

from pastasauce import PastaSauce, PastaDecorator
from random import randint
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.ui import WebDriverWait
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
        132519, 132520, 132521, 132522, 132523,
        132560, 132524, 132561, 132525, 132528,
        132527, 132526, 132530, 132531, 132529,
        132532, 132533, 132534, 132577,
        # 132526

    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestCreateAReading(unittest.TestCase):
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
        self.teacher.select_course(appearance='intro_sociology')

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

    # Case C132519 001 - Teacher | Create and publish a new open reading for
    # all periods
    @pytest.mark.skipif(str(132519) not in TESTS, reason='Excluded')
    def test_teacher_create_and_publish_a_new_open_reading_132519(self):
        """
        Create and publish a new open reading for all periods

        Steps:
        Click on the 'Add Assignment' button
        Click on the 'Add Reading' option
        (The teacher is taken to the Add Reading Assignment page)
        Enter an assignment name into the Assignment name text box
        Enter an assignment description into the Assignment description
          or special instructions text box
        ['All Sections' should be selected by default]
        Click on the Open Date text field and click on today's date on
        calendar pop-up
        Click on the Open Time text field and enter 12:01am.
        Click on the Due Date text field and click on desired due date on
        calendar pop-up
        Click on the "+ Add Readings" button
        Click on section(s) to add to assignment
        Scroll to bottom of the page
        Click on the "Add Readings" button
        Click on the "Publish" button

        Expected result:
        Takes user back to calendar dashboard.
        An opened assignment appears on user calendar dashboard on due date
        with correct readings
        """
        self.ps.test_updates['name'] = 'tutor_teacher_reading' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = \
            ['tutor', 'teacher', 'reading', '132519']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading_001_%d' % (randint(100, 999))
        assignment = Assignment()

        # Open Add Reading page
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Reading').click()
        assert('reading/new' in self.teacher.current_url()), \
            'not at add readings screen'

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
        # use staxing function to send_keys

        # Set date
        today = datetime.date.today()
        end = randint(1, 5)
        # make the start date today so it will be open
        opens_on = today.strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=end)) \
            .strftime('%m/%d/%Y')
        assignment.assign_periods(
            self.teacher.driver, {'all': (opens_on, closes_on)})

        # add reading sections to the assignment
        self.teacher.find(By.ID, 'reading-select').click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"reading-plan")]')
            )
        )
        assignment.select_sections(self.teacher.driver, ['1.1'])
        self.teacher.find(
            By.XPATH, '//button[text()="Add Readings"]'
        ).click()

        # publish
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"-publish")]')
            )
        ).click()

        sleep(5)

        # locate the published assignment
        try:
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(assignment_name)
            )
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(assignment_name)
            )

            '''
            self.teacher.find(
                By.XPATH,
                '//a[contains(@class,"header-control next")]'
            ).click()
            sleep(10)
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(assignment_name)
            )
            '''

        self.ps.test_updates['passed'] = True

    # Case C132520 002 - Teacher | Save a draft for individual periods
    @pytest.mark.skipif(str(132520) not in TESTS, reason='Excluded')
    def test_teacher_save_a_draft_reading_for_individual_sections_132520(self):
        """
        Save a draft for individual periods

        Steps:
        Click on the Add Assignment sidebar menu on the user dashboard if it
        is not already open
        Click on the 'Add Reading' button
        (The teacher is taken to the Add Reading Assignment page)

        Enter an assignment name into the Assignment name text box
        [optional] Enter an assignment description into the Assignment
        description or special instructions text box
        Click the 'Individual Sections' radio button
        For each period reading is being assigned to:
        - Click on the Open Date text field and click on desired open date on
        calendar pop-up
        - Click on the Due Date text field and click on desired due date in
        the future on calendar pop-up
        Click on the "+ Add Readings" button
        Click on section(s) to add to assignment
        Scroll to bottom of the page
        Click on the "Add Readings" button
        Click on the "Save As Draft" button

        Expected result:
        Takes user back to calendar dashboard.
        Assignment appears on user calendar dashboard on due date with correct
        readings.
        'draft' should appear before the assignment name.
        """
        self.ps.test_updates['name'] = \
            'tutor_teacher_reading' + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = \
            ['tutor', 'teacher', 'reading', '132520']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading_002_%d' % (randint(100, 999))
        assignment = Assignment()

        # Open Add Reading page
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Reading').click()
        assert ('reading/new' in self.teacher.current_url()), \
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
                    '//label[contains(@for, "%s")]' %
                    period.get_attribute('id')).text
            ] = (opens_on, closes_on)

        assignment.assign_periods(self.teacher.driver, period_assignment)

        # add reading sections to the assignment
        self.teacher.find(By.ID, 'reading-select').click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"reading-plan")]')
            )
        )
        assignment.select_sections(self.teacher.driver, ['1.1'])
        self.teacher.find(
            By.XPATH, '//button[text()="Add Readings"]'
        ).click()

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

    # Case C132521 003 - Teacher | Create and publish a new unopened reading
    # from calendar
    @pytest.mark.skipif(str(132521) not in TESTS, reason='Excluded')
    def test_teacher_create_publish_new_unopened_reading_from_cal_132521(self):
        """
        Create and publish a new unopened reading from calendar

        Steps:
        Click on calendar date for desired due date
        Click on the 'Add Reading' option
        (The teacher is taken to the Add Reading Assignment page)
        Enter an assignment name into the Assignment name text box [user
        decision]
        ['All Sections' should be selected by default]
        Click on the Open Date text field and click on a date in the future in
        calendar pop-up
        Click on the "+ Add Readings" button
        Click on section(s) to add to assignment
        Scroll to bottom of the page
        Click on the "Add Readings" button
        Click on the "Publish" button

        # Expected result
        Takes user back to calendar dashboard.
        An unopened assignment appears on user calendar dashboard on due date
        with correct readings
        """
        self.ps.test_updates['name'] = 'tutor_teacher_reading' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = \
            ['tutor', 'teacher', 'reading', '132521']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        dates = self.teacher.find_all(By.CSS_SELECTOR, '.rc-Day--upcoming')
        calendar_date = dates[randint(1, 2)]
        self.teacher.scroll_to(calendar_date)
        '''
        dates = self.teacher.find_all(By.CSS_SELECTOR, '.rc-Day--upcoming')
        calendar_date = dates[randint(0, len(dates))]
        self.teacher.scroll_to(calendar_date)

        calendar_date = self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//div[contains(@class,"Day--upcoming")]')
            )
        )
        '''
        sleep(10)
        self.teacher.driver.execute_script(
            'return arguments[0].scrollIntoView();',
            (calendar_date)
        )

        height = calendar_date.find_element(By.XPATH, '../..').size['height']
        height = float(height) / 2.0

        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(calendar_date)
        actions.move_by_offset(height * -1, 0)
        actions.click()
        actions.move_by_offset(30, 15)
        actions.click()
        actions.perform()

        '''
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
        actions.move_by_offset(30, 15)
        actions.click()
        actions.perform()
        '''

        assert ('reading/new' in self.teacher.current_url()), \
            'not at Add Reading page'

        assignment_name = 'reading_003_%d' % (randint(100, 999))
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
        start = 0
        # start = randint(1, 5)
        end = start + randint(1, 5)

        # the open date should be in the future for the assignment to be
        # unopened
        closes_on = (today + datetime.timedelta(days=end))\
            .strftime('%m/%d/%Y')
        opens_on = (today + datetime.timedelta(days=start))\
            .strftime('%m/%d/%Y')
        assignment.assign_periods(
            self.teacher.driver, {'all': (opens_on, closes_on)})

        # Add reading sections to the assignment
        self.teacher.find(By.ID, 'reading-select').click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class, "reading-plan")]')
            )
        )
        assignment.select_sections(self.teacher.driver, ['1.1'])
        self.teacher.find(
            By.XPATH, '//button[text()="Add Readings"]'
        ).click()

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

    # Case C132522 004 - Teacher | Publish a draft reading
    @pytest.mark.skipif(str(132522) not in TESTS, reason='Excluded')
    def test_teacher_publish_a_draft_reading_132522(self):
        """
        Publish a draft reading

        Steps:
        On the calendar click on a reading assignment that is currently a draft
        Click on the 'Publish' button

        Expected Result:
        Takes user back to calendar dashboard.
        Assignment appears on user calendar dashboard on due date with correct
        readings. 'draft' should no longer be before the assignment name.
        """
        self.ps.test_updates['name'] = \
            'tutor_teacher_reading' + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = \
            ['tutor', 'teacher', 'reading', '132522']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading_004_%s' % randint(100, 999)
        today = datetime.date.today()
        start = randint(0, 6)
        finish = start + randint(1, 5)
        begin = (today + datetime.timedelta(days=start)) \
            .strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=finish)) \
            .strftime('%m/%d/%Y')

        assignment = Assignment()
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Reading').click()
        assert ('reading/new' in self.teacher.current_url()), \
            'not at add readings screen'

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
        # use staxing function to send_keys

        # Set date
        today = datetime.date.today()
        # make the start date today so it will be open
        opens_on = begin
        closes_on = end
        assignment.assign_periods(
            self.teacher.driver, {'all': (opens_on, closes_on)})

        # add reading sections to the assignment
        self.teacher.find(By.ID, 'reading-select').click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"reading-plan")]')
            )
        )
        assignment.select_sections(self.teacher.driver, ['1.1'])
        self.teacher.find(
            By.XPATH, '//button[text()="Add Readings"]'
        ).click()

        # Save as draft
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'builder-draft-button')
            )
        ).click()

        '''
        self.teacher.add_assignment(
            assignment='reading',
            args={
                'title': assignment_name,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'reading_list': ['1.1'],
                'status': 'draft',
            }
        )
        '''

        # Find the draft reading on the calendar
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'month-wrapper')
            )
        )
        self.teacher.find(
            By.XPATH, '//label[contains(text(),"{0}")]'.format(assignment_name)
        ).click()

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

    # Case C132523 005 - Teacher | Cancel a new reading before making any
    # changes
    @pytest.mark.skipif(str(132523) not in TESTS, reason="Excluded")
    def test_teacher_cancel_new_reading_before_making_any_changes_132523(self):
        """
        Cancel a new reading before making any changes

        Steps:
        Click on the 'Add Assignment' sidebar menu
        Click on the 'Add Reading' option
        Click on the 'Cancel' button
        (Takes user back to calendar dashboard. No changes have been made)

        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Reading' option
        Click on the 'X' button

        Expected result
        Takes user back to calendar dashboard.
        No changes have been made to the calendar on the dashboard
        """
        self.ps.test_updates['name'] = \
            'tutor_teacher_reading' + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = \
            ['tutor', 'teacher', 'reading', '132523']
        self.ps.test_updates['passed'] = False

        # Open "Add Reading" page
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Reading').click()
        assert ('reading/new' in self.teacher.current_url()), \
            'not at add readings screen'

        # Cancel a reading with "Cancel" button
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'builder-cancel-button')
            )
        ).click()
        assert ('month' in self.teacher.current_url()), \
            'not back at calendar after cancelling reading'

        # Open "Add Reading" page
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Reading').click()
        assert ('reading/new' in self.teacher.current_url()), \
            'not at add readings screen'

        # Cancel a reading with "X" button
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class,"openstax-close-x")]')
            )
        ).click()
        assert ('month' in self.teacher.current_url()), \
            'not back at calendar after cancelling reading'

        self.ps.test_updates['passed'] = True

    # Case C132560 006 - Teacher | Cancel a new reading AFTER making changes
    @pytest.mark.skipif(str(132560) not in TESTS, reason="Excluded")
    def test_teacher_cancel_a_new_reading_after_making_changes_132560(self):
        """
        Cancel a new reading after making changes

        Steps:
        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Reading' option
        Enter an assignment name into the Assignment name text box
        Click the 'Cancel' button
        Click on the "Yes" button
        (Takes user back to calendar dashboard. No changes have been made to
        the calendar on the dashboard)
        Click on the 'Add Assignment' drop down menu

        Click on the 'Add Reading' option
        Enter an assignment name into the Assignment name text box
        Click the 'X' button
        Click the "Yes" button

        Expected result:
        Takes user back to calendar dashboard.
        No changes have been made to the calendar on the dashboard
        """
        self.ps.test_updates['name'] = \
            'tutor_teacher_reading' + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = \
            ['tutor', 'teacher', 'reading', '132560']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading_006_%d' % (randint(100, 999))

        # Open "Add reading" page
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Reading').click()
        assert ('reading/new' in self.teacher.current_url()), \
            'not at add readings screen'

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
            'not back at calendar after cancelling reading'

        # Open "Add reading" page
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Reading').click()
        assert ('reading/new' in self.teacher.current_url()), \
            'not at add readings screen'

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
            'not back at calendar after cancelling reading'

        self.ps.test_updates['passed'] = True

    # Case C132524 007 - Teacher | Cancel draft reading before making changes
    @pytest.mark.skipif(str(132524) not in TESTS, reason="Excluded")
    def test_teacher_cancel_a_draft_reading_before_making_changes_132524(self):
        """
        Cancel a draft reading before making changes

        Steps:
        On the calendar click on a assignment that is currently a draft
        Click on the 'Cancel' button
        Takes user back to calendar dashboard. no changes have been
        made to the chosen draft on the calendar dashboard***

        On the calendar click on a assignment that is currently a draft
        Click on the 'X' button
        ***Takes user back to calendar dashboard. No changes have been
        made to the chosen draft on the calendar dashboard***

        Expected result:
        Takes user back to calendar dashboard.
        No changes have been made to the chosen draft on the calendar dashboard
        """
        self.ps.test_updates['name'] = \
            'tutor_teacher_reading' + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = \
            ['tutor', 'teacher', 'reading', '132524']
        self.ps.test_updates['passed'] = False

        # Test steps and verification
        assignment_name_1 = "reading_007_%d" % (randint(100, 500))
        assignment_name_2 = "reading_007_%d" % (randint(501, 999))
        today = datetime.date.today()
        start = randint(0, 6)
        finish = start + randint(1, 5)
        begin = (today + datetime.timedelta(days=start))\
            .strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=finish))\
            .strftime('%m/%d/%Y')

        assignment = Assignment()
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Reading').click()
        assert ('reading/new' in self.teacher.current_url()), \
            'not at add readings screen'

        # Find and fill in title
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        ).send_keys(assignment_name_1)

        # Fill in description
        self.teacher.find(
            By.XPATH, '//textarea[contains(@class, "form-control")]'
        ).send_keys('description')
        # use staxing function to send_keys

        # Set date
        today = datetime.date.today()
        # make the start date today so it will be open
        opens_on = begin
        closes_on = end
        assignment.assign_periods(
            self.teacher.driver, {'all': (opens_on, closes_on)})

        # add reading sections to the assignment
        self.teacher.find(By.ID, 'reading-select').click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"reading-plan")]')
            )
        )
        assignment.select_sections(self.teacher.driver, ['1.1'])
        self.teacher.find(
            By.XPATH, '//button[text()="Add Readings"]'
        ).click()

        # Save as draft
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'builder-draft-button')
            )
        ).click()

        '''
        # Add a draft reading
        self.teacher.add_assignment(
            assignment='reading',
            args={
                'title': assignment_name_1,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'reading_list': ['1.1'],
                'status': 'draft'
            }
        )
        '''

        # Open a draft reading
        try:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH, '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(assignment_name_1)
            ).click()
        except:
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
            'not back at calendar after cancelling reading'

        assignment = Assignment()
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Reading').click()
        assert ('reading/new' in self.teacher.current_url()), \
            'not at add readings screen'

        # Find and fill in title
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        ).send_keys(assignment_name_2)

        # Fill in description
        self.teacher.find(
            By.XPATH, '//textarea[contains(@class, "form-control")]'
        ).send_keys('description')
        # use staxing function to send_keys

        # Set date
        today = datetime.date.today()
        # make the start date today so it will be open
        opens_on = begin
        closes_on = end
        assignment.assign_periods(
            self.teacher.driver, {'all': (opens_on, closes_on)})

        # add reading sections to the assignment
        self.teacher.find(By.ID, 'reading-select').click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"reading-plan")]')
            )
        )
        assignment.select_sections(self.teacher.driver, ['1.1'])
        self.teacher.find(
            By.XPATH, '//button[text()="Add Readings"]'
        ).click()

        # Save as draft
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'builder-draft-button')
            )
        ).click()

        '''
        # Add a draft reading
        self.teacher.add_assignment(
            assignment='reading',
            args={
                'title': assignment_name_2,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'reading_list': ['1.2'],
                'status': 'draft'
            }
        )
        '''

        # Open a draft reading
        try:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH, '//div[@class="month-wrapper"]')
                )
            )
            sleep(3)
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(assignment_name_2)
            ).click()
        except:
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
            'not back at calendar after cancelling reading'

        self.ps.test_updates['passed'] = True

    # Case C132561 008 - Teacher | Cancel draft reading after making changes
    @pytest.mark.skipif(str(132561) not in TESTS, reason="Excluded")
    def test_teacher_cancel_a_draft_reading_after_making_changes_132561(self):
        """
        Cancel a draft reading after making changes

        Steps:
        On the calendar click on a assignment that is currently a draft
        Enter an assignment name into the Assignment name text box [user
        decision]
        Click on the 'Cancel' button
        Click on the "Yes" button
        (Takes user back to calendar dashboard. no changes have been made to
        the chosen draft on the calendar dashboard)

        On the calendar click on a assignment that is currently a draft
        Enter an assignment name into the Assignment name text box
        Click on the 'X' button
        Click on the 'Yes' button

        Expected result:
        Takes user back to calendar dashboard.
        No changes have been made to the chosen draft on the calendar dashboard
        """
        self.ps.test_updates['name'] = \
            'tutor_teacher_reading' + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = \
            ['tutor', 'teacher', 'reading', '132561']
        self.ps.test_updates['passed'] = False

        # Test steps and verification
        assignment_name_1 = "reading_008_%d" % (randint(100, 500))
        assignment_name_2 = "reading_008_%d" % (randint(501, 999))
        today = datetime.date.today()
        start = randint(0, 6)
        finish = start + randint(1, 5)
        begin = (today + datetime.timedelta(days=start)) \
            .strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=finish)) \
            .strftime('%m/%d/%Y')

        assignment = Assignment()

        # Open Add Reading page
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Reading').click()
        assert ('reading/new' in self.teacher.current_url()), \
            'not at add readings screen'

        # Find and fill in title
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        ).send_keys(assignment_name_1)

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
                    '//label[contains(@for, "%s")]' %
                    period.get_attribute('id')).text
            ] = (opens_on, closes_on)

        assignment.assign_periods(self.teacher.driver, period_assignment)

        # add reading sections to the assignment
        self.teacher.find(By.ID, 'reading-select').click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"reading-plan")]')
            )
        )
        assignment.select_sections(self.teacher.driver, ['1.1'])
        self.teacher.find(
            By.XPATH, '//button[text()="Add Readings"]'
        ).click()

        # Save as draft
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'builder-draft-button')
            )
        ).click()

        '''
        # Add a draft reading
        self.teacher.add_assignment(
            assignment='reading',
            args={
                'title': assignment_name_1,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'reading_list': ['1.1'],
                'status': 'draft'
            }
        )
        '''

        # Open a draft reading
        try:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH, '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(assignment_name_1)
            ).click()
        except:
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
            'not back at calendar after cancelling reading'

        assignment = Assignment()

        # Open Add Reading page
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Reading').click()
        assert ('reading/new' in self.teacher.current_url()), \
            'not at add readings screen'

        # Find and fill in title
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        ).send_keys(assignment_name_2)

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
                    '//label[contains(@for, "%s")]' %
                    period.get_attribute('id')).text
            ] = (opens_on, closes_on)

        assignment.assign_periods(self.teacher.driver, period_assignment)

        # add reading sections to the assignment
        self.teacher.find(By.ID, 'reading-select').click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"reading-plan")]')
            )
        )
        assignment.select_sections(self.teacher.driver, ['1.1'])
        self.teacher.find(
            By.XPATH, '//button[text()="Add Readings"]'
        ).click()

        # Save as draft
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'builder-draft-button')
            )
        ).click()

        '''
        # Add a draft reading
        self.teacher.add_assignment(
            assignment='reading',
            args={
                'title': assignment_name_2,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'reading_list': ['1.2'],
                'status': 'draft'
            }
        )
        '''

        # Open a draft reading
        try:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH, '//div[@class="month-wrapper"]')
                )
            )
            sleep(2)
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(assignment_name_2)
            ).click()
        except:
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
                '//label[contains(text(),"{0}")]'.format(assignment_name_2)
            ).click()
        sleep(1)

        # Change the reading title
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

    # Case C132525 009 - Teacher | Attempt to save/publish a reading with blank
    # required fields
    @pytest.mark.skipif(str(132525) not in TESTS, reason="Excluded")
    def test_teacher_attempt_publish_a_reading_with_blank_req_132525(self):
        """
        Attempt to save/publish a reading with blank required fields

        Steps:
        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Reading' option
        Click on the 'Save As Draft' button
        All required fields that were left blank become red, and specify that
        they are required fields***

        Click on the course name to return to dashboard
        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Reading' option
        Click on the 'Publish' button

        Expected result:
        Remains on the Add Assignment page. Does not allow user to publish
        assignments.
        All required fields that were left blank become red, and specify that
        they are required fields.***
        """
        self.ps.test_updates['name'] = \
            'tutor_teacher_reading' + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = \
            ['tutor', 'teacher', 'reading', '132525']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Reading').click()
        assert ('reading/new' in self.teacher.current_url()), \
            'not at add readings screen'

        # Publish without filling in any fields
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class,"-publish")]')
            )
        ).click()

        # Required field reminder
        self.teacher.find(
            By.XPATH, '//div[contains(text(),"Required field")]')
        assert ('reading' in self.teacher.current_url()), \
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
        assert ('reading' in self.teacher.current_url()), \
            'went back to calendar even though required fields were left blank'

        self.ps.test_updates['passed'] = True

    # Case C132528 010 - Teacher | Delete a draft reading
    @pytest.mark.skipif(str(132528) not in TESTS, reason="Excluded")
    def test_teacher_delete_a_draft_reading_132528(self):
        """
        Delete a draft reading

        Steps:
        On the calendar click on a draft
        Click on the 'Delete Assignment' button
        Click on the "Yes" button
        [Takes user back to calendar dashboard. Chosen assignment no longer
        appears on teacher calendar dashboard]

        On the calendar click on a reading that is unopened
        Click on the 'Edit Assignment' button
        Click on the 'Delete Assignment' button
        Click on the "Yes" button

        Expected result:
        Takes user back to calendar dashboard. Chosen assignment no longer
        appears on teacher calendar dashboard***
        """
        self.ps.test_updates['name'] = \
            'tutor_teacher_reading' + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = \
            ['tutor', 'teacher', 'reading', '132528']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        draft_title = 'draft_reading_%s' % (randint(100, 999))
        today = datetime.date.today()
        start = randint(2, 6)
        finish = start + randint(1, 5)
        begin = (today + datetime.timedelta(days=start)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=finish)).strftime('%m/%d/%Y')

        assignment = Assignment()
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Reading').click()
        assert ('reading/new' in self.teacher.current_url()), \
            'not at add readings screen'

        # Find and fill in title
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        ).send_keys(draft_title)

        # Fill in description
        self.teacher.find(
            By.XPATH, '//textarea[contains(@class, "form-control")]'
        ).send_keys('description')
        # use staxing function to send_keys

        # Set date
        today = datetime.date.today()
        # make the start date today so it will be open
        opens_on = begin
        closes_on = end
        assignment.assign_periods(
            self.teacher.driver, {'all': (opens_on, closes_on)})

        # add reading sections to the assignment
        self.teacher.find(By.ID, 'reading-select').click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"reading-plan")]')
            )
        )
        assignment.select_sections(self.teacher.driver, ['1.1'])
        self.teacher.find(
            By.XPATH, '//button[text()="Add Readings"]'
        ).click()

        # Save as draft
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'builder-draft-button')
            )
        ).click()

        '''
        # Create a draft reading
        self.teacher.add_assignment(
            assignment='reading',
            args={
                'title': draft_title,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'reading_list': ['1.1', '1.2'],
                'status': 'draft'
            }
        )
        '''

        # Delete the draft reading
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'month-wrapper')
            )
        )
        self.teacher.find(
            By.XPATH, '//label[contains(text(),"{0}")]'.format(draft_title)
        ).click()
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

        # have to refresh to remove the reading tab from calendar
        self.teacher.driver.refresh()
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'month-wrapper')
            )
        )
        deleted_draft = self.teacher.find_all(
            By.XPATH, '//label[@data-title="{0}"]'.format(draft_title)
        )
        assert (len(deleted_draft) == 0), 'draft reading not deleted'

        self.ps.test_updates['passed'] = True

    # Case C132527 011 - Teacher | Delete an unopened reading
    @pytest.mark.skipif(str(132527) not in TESTS, reason="Excluded")
    def test_teacher_delete_an_unopened_reading_132527(self):
        """
        Delete an unopened reading

        Steps:
        On the calendar click on an unopened reading
        Click on the 'Edit Assignment' button
        Click "Delete Assignment"
        Click "Yes"

        Expected result:
        An open reading is deleted
        """
        self.ps.test_updates['name'] = \
            'tutor_teacher_reading' + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = \
            ['tutor', 'teacher', 'reading', '132527']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        unopened_title = 'unopened_reading_%s' % (randint(100, 999))
        today = datetime.date.today()
        start = randint(2, 6)
        finish = start + randint(1, 5)
        begin = (today + datetime.timedelta(days=start)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=finish)).strftime('%m/%d/%Y')

        assignment = Assignment()
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Reading').click()
        assert ('reading/new' in self.teacher.current_url()), \
            'not at add readings screen'

        # Find and fill in title
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        ).send_keys(unopened_title)

        # Fill in description
        self.teacher.find(
            By.XPATH, '//textarea[contains(@class, "form-control")]'
        ).send_keys('description')
        # use staxing function to send_keys

        # Set date
        today = datetime.date.today()
        # make the start date today so it will be open
        opens_on = begin
        closes_on = end
        assignment.assign_periods(
            self.teacher.driver, {'all': (opens_on, closes_on)})

        # add reading sections to the assignment
        self.teacher.find(By.ID, 'reading-select').click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"reading-plan")]')
            )
        )
        assignment.select_sections(self.teacher.driver, ['1.1', '1.2'])
        self.teacher.find(
            By.XPATH, '//button[text()="Add Readings"]'
        ).click()

        # publish
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"-publish")]')
            )
        ).click()
            
        '''
        # Create an unopened reading
        self.teacher.add_assignment(
            assignment='reading',
            args={
                'title': unopened_title,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'reading_list': ['1.1', '1.2'],
                'status': 'publish'
            }
        )
        '''

        # Delete the unopened reading
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'month-wrapper')
            )
        )
        self.teacher.find(
            By.XPATH, '//label[contains(text(),"{0}")]'.format(unopened_title)
        ).click()
        '''
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'edit-assignment-button')
            )
        ).click()
        '''
        self.teacher.wait.until(
            expect.element_to_be_clickable((
                By.XPATH,
                '//a[contains(text(),"Edit")]'
            ))
        ).click()
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

        # self.teacher.wait.until(
        #     expect.visibility_of_element_located(
        #         (By.XPATH, '//button[contains(@class,"delete-link")]')
        #     )
        # ).click()
        # self.teacher.find(
        #     By.XPATH, '//button[contains(text(),"Yes")]'
        # ).click()
        sleep(3)

        assert ('month' in self.teacher.current_url()), \
            'not returned to calendar after deleting an assignment'

        # have to refresh to remove assignment tab from calendar
        self.teacher.driver.refresh()
        # self.teacher.wait.until(
        #     expect.presence_of_element_located(
        #         (By.CLASS_NAME, 'rc-Week-days')
        #     )
        # )
        WebDriverWait(self.teacher.driver, 10).until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'rc-Week-days')
            )
        )
        deleted_unopened = self.teacher.find_all(
            By.XPATH, '//label[@data-title="{0}"]'.format(unopened_title)
        )
        assert len(deleted_unopened) == 0, 'unopened reading not deleted'

        self.ps.test_updates['passed'] = True

    # Case C132526 012 - Teacher | Delete an open reading
    @pytest.mark.skipif(str(132526) not in TESTS, reason="Excluded")
    def test_teacher_delete_an_open_reading_132526(self):
        """
        Delete an open reading

        Steps:
        On the calendar click on a reading that is opened
        Click on the 'Edit Assignment' button
        Click "Delete Assignment"
        Click "Yes"

        Expected result:
        An open reading is deleted
        """
        # Create an open reading
        self.ps.test_updates['name'] = \
            'tutor_teacher_reading' + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = \
            ['tutor', 'teacher', 'reading', '132526']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        open_title = 'open_reading_%s' % (randint(100, 999))
        today = datetime.date.today()
        finish = randint(1, 5)
        begin_today = today.strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=finish)).strftime('%m/%d/%Y')

        assignment = Assignment()
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Reading').click()
        assert ('reading/new' in self.teacher.current_url()), \
            'not at add readings screen'

        # Find and fill in title
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        ).send_keys(open_title)

        # Fill in description
        self.teacher.find(
            By.XPATH, '//textarea[contains(@class, "form-control")]'
        ).send_keys('description')
        # use staxing function to send_keys

        # Set date
        today = datetime.date.today()
        # make the start date today so it will be open
        opens_on = begin_today
        closes_on = end
        assignment.assign_periods(
            self.teacher.driver, {'all': (opens_on, closes_on)})

        # add reading sections to the assignment
        self.teacher.find(By.ID, 'reading-select').click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"reading-plan")]')
            )
        )
        assignment.select_sections(self.teacher.driver, ['1.1', '1.2'])
        self.teacher.find(
            By.XPATH, '//button[text()="Add Readings"]'
        ).click()

        # publish
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"-publish")]')
            )
        ).click()

        '''
        self.teacher.add_assignment(
            assignment='reading',
            args={
                'title': open_title,
                'description': 'description',
                'periods': {'all': (begin_today, end)},
                'reading_list': ['1.1', '1.2'],
                'status': 'publish'
            }
        )
        '''

        # Delete the open reading
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'month-wrapper')
            )
        )
        self.teacher.find(
            By.XPATH, '//label[contains(text(),"{0}")]'.format(open_title)
        ).click()
        '''
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'edit-assignment-button')
            )
        '''
        self.teacher.wait.until(
            expect.element_to_be_clickable((
                By.XPATH,
                '//a[contains(text(),"View")]'
            ))
        ).click()
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
        # self.teacher.wait.until(
        #     expect.visibility_of_element_located(
        #         (By.XPATH, '//button[contains(@class,"delete-link")]')
        #     )
        # ).click()
        # self.teacher.find(
        #     By.XPATH, '//button[contains(text(),"Yes")]'
        # ).click()
        sleep(3)

        assert ('month' in self.teacher.current_url()), \
            'not returned to calendar after deleting an assignment'

        # have to refresh to remove reading tab from calendar
        self.teacher.driver.refresh()
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'month-wrapper')
            )
        )
        sleep(3)
        deleted_open = self.teacher.find_all(
            By.XPATH, '//label[@data-title="{0}"]'.format(open_title)
        )
        assert len(deleted_open) == 0, 'open reading not deleted'

        self.ps.test_updates['passed'] = True

    # Case C132530 C013 - Teacher | Change a draft reading
    @pytest.mark.skipif(str(132530) not in TESTS, reason="Excluded")
    def test_teacher_change_a_draft_reading_132530(self):
        """
        Change all fields in a draft reading.

        Steps:
        Click on an existing draft reading on the calendar
        Enter a new assignment name into the Assignment name text box
        Enter a new assignment description into the Assignment description box
        Click on the Open Date field and click on an date on calendar element
        Click on the Due Date field and click on a date on calendar element
        Click on the x next to a selected section
        Click the 'Save As Draft' button

        Expected Result:
        Takes user back to the calendar dashboard.
        The name, description, due dates, and chapters/sections of the reading
        have been updated.
        The draft reading now appears on its new due date on the calendar.
        """
        self.ps.test_updates['name'] = \
            'tutor_teacher_reading' + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = \
            ['tutor', 'teacher', 'reading', '132530']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading_013%d' % (randint(100, 999))
        assignment = Assignment()
        today = datetime.date.today()
        start = randint(0, 6)
        finish = start + randint(1, 6)
        '''
        begin = (today + datetime.timedelta(days=start)).strftime('%m/%d/%Y')
        '''
        end = (today + datetime.timedelta(days=finish)).strftime('%m/%d/%Y')

        assignment = Assignment()

        # Open Add Reading page
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Reading').click()
        assert ('reading/new' in self.teacher.current_url()), \
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
                    '//label[contains(@for, "%s")]' %
                    period.get_attribute('id')).text
            ] = (opens_on, closes_on)

        assignment.assign_periods(self.teacher.driver, period_assignment)

        # add reading sections to the assignment
        self.teacher.find(By.ID, 'reading-select').click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"reading-plan")]')
            )
        )
        assignment.select_sections(self.teacher.driver, ['1.1', '1.2'])
        self.teacher.find(
            By.XPATH, '//button[text()="Add Readings"]'
        ).click()

        # Save as draft
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'builder-draft-button')
            )
        ).click()

        '''
        # Create a draft reading
        self.teacher.add_assignment(
            assignment='reading',
            args={
                'title': assignment_name,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'reading_list': ['1.1', '1.2'],
                'status': 'draft'
            }
        )
        '''

        # Locate the draft reading
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

        # remove reading section from the assignment
        self.teacher.find(
            By.XPATH,
            '//button[contains(@class,"remove-topic")]'
        ).click()
        # save
        self.teacher.find(
            By.XPATH,
            '//button[contains(@class,"-save")]'
        ).click()
        try:
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'
                .format(assignment_name + 'new')
            )
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH,
                '//a[contains(@class,"header-control next")]'
            ).click()
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'
                .format(assignment_name + 'new')
            )
        # note: only changed title is checked. changed description and due
        # dates are unchecked

        self.ps.test_updates['passed'] = True

    # Case C132531 014  - Teacher | Change an unopened reading
    @pytest.mark.skipif(str(132531) not in TESTS, reason="Excluded")
    def test_teacher_change_an_unopened_reading_132531(self):
        """
        Change all fields in an unopened, published reading.

        Steps:
        Click on an existing reading on the calendar
        Click on the 'Edit' option
        Enter a new assignment name into the Assignment name text box
        Enter a new assignment description into the Assignment description box
        Click on the Open Date field and click on an date on calendar element
        Click on the Due Date field and click on a date on calendar element
        Remove a section from the readings
        Click the 'Publish' button

        Expected Result:
        Takes user back to the calendar dashboard.
        The name, description, due dates, and chapters/sections of the reading
        have been updated.
        The reading appears on its new due date on the calendar.
        """
        self.ps.test_updates['name'] = \
            'tutor_teacher_reading' + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = \
            ['tutor', 'teacher', 'reading', '132531']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading_014%d' % (randint(100, 999))
        assignment = Assignment()
        today = datetime.date.today()
        start = randint(0, 6)
        finish = start + randint(1, 6)
        begin = (today + datetime.timedelta(days=start)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=finish)).strftime('%m/%d/%Y')

        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Reading').click()
        assert ('reading/new' in self.teacher.current_url()), \
            'not at add readings screen'

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
        # use staxing function to send_keys

        # Set date
        today = datetime.date.today()
        # make the start date today so it will be open
        opens_on = begin
        closes_on = end
        assignment.assign_periods(
            self.teacher.driver, {'all': (opens_on, closes_on)})

        # add reading sections to the assignment
        self.teacher.find(By.ID, 'reading-select').click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"reading-plan")]')
            )
        )
        assignment.select_sections(self.teacher.driver, ['1.1', '1.2'])
        self.teacher.find(
            By.XPATH, '//button[text()="Add Readings"]'
        ).click()

        # publish
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"-publish")]')
            )
        ).click()

        sleep(5)

        '''
        # Create an unopened reading
        self.teacher.add_assignment(
            assignment='reading',
            args={
                'title': assignment_name,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'reading_list': ['1.1', '1.2'],
                'status': 'publish'
            }
        )
        '''

        # Locate the unopened reading
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

        '''
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'edit-assignment-button')
            )
        ).click()
        '''
        Metrics_Button = self.teacher.driver.find_element(
                By.XPATH, '//a[contains(., "Metrics")]')
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(Metrics_Button)
        actions.move_by_offset(100, 0)
        actions.click()
        actions.perform()

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

        # set new open and due dates
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

        # remove reading section from the assignment
        self.teacher.find(
            By.XPATH,
            '//button[contains(@class,"remove-topic")]'
        ).click()
        # save
        self.teacher.find(
            By.XPATH,
            '//button[contains(@class,"publish")]'
        ).click()
        try:
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'
                .format(assignment_name + 'new')
            )
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH,
                '//a[contains(@class,"header-control next")]'
            ).click()
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'
                .format(assignment_name + 'new')
            )
        # note: only changed title is checked. changed description and due
        # dates are unchecked

        self.ps.test_updates['passed'] = True

    # Case C132529 015 - Teacher | Change an open reading
    @pytest.mark.skipif(str(132529) not in TESTS, reason="Excluded")
    def test_teacher_change_an_open_reading_132529(self):
        """
        Change the name, description and due dates in an opened reading.

        Steps:
        Click on an existing open reading on the calendar
        Click on the 'Edit' option
        Enter a new assignment name into the Assignment name text box
        Enter a new assignment description into the Assignment description box
        Click on the Due Date field and click on a date on calendar element
        Click the 'Publish' button

        Expected Result:
        Takes user back to the calendar dashboard.
        The name, description, due dates, and chapters/sections of the reading
        have been updated.
        The reading now appears on its new due date on the calendar
        """
        self.ps.test_updates['name'] = \
            'tutor_teacher_reading' + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = \
            ['tutor', 'teacher', 'reading', '132529']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading_015%d' % (randint(100, 999))
        today = datetime.date.today()
        finish = randint(1, 6)
        today_begin = today.strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=finish)).strftime('%m/%d/%Y')

        assignment = Assignment()
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Reading').click()
        assert ('reading/new' in self.teacher.current_url()), \
            'not at add readings screen'

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
        # use staxing function to send_keys

        # Set date
        today = datetime.date.today()
        # make the start date today so it will be open
        opens_on = today_begin
        closes_on = end
        assignment.assign_periods(
            self.teacher.driver, {'all': (opens_on, closes_on)})

        # add reading sections to the assignment
        self.teacher.find(By.ID, 'reading-select').click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"reading-plan")]')
            )
        )
        assignment.select_sections(self.teacher.driver, ['1.1', '1.2'])
        self.teacher.find(
            By.XPATH, '//button[text()="Add Readings"]'
        ).click()

        # publish
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"-publish")]')
            )
        ).click()

        '''
        # Create an open reading
        self.teacher.add_assignment(
            assignment='reading',
            args={
                'title': assignment_name,
                'description': 'description',
                'periods': {'all': (today_begin, end)},
                'reading_list': ['1.1', '1.2'],
                'status': 'publish'
            }
        )
        '''

        # Locate the open reading
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

        self.teacher.wait.until(
            expect.element_to_be_clickable((
                By.XPATH,
                '//a[contains(text(),"View")]'
            ))
        ).click()
        sleep(5)

        '''
        self.teacher.find(
            By.ID, 'edit-assignment-button'
        '''

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
        end = randint(1, 5)
        closes_on = (today + datetime.timedelta(days=end)) \
            .strftime('%m/%d/%Y')
        assignment.assign_date(
            driver=self.teacher.driver,
            date=closes_on,
            is_all=True,
            target='due'
        )
        # self.teacher.find(By.ID, 'hide-periods-radio').click()

        # assignment.assign_periods(
        #     self.teacher.driver,
        #     {'all': (opens_on, closes_on)}
        # )

        # Save the changes
        self.teacher.find(
            By.XPATH,
            '//button[contains(@class,"publish")]'
        ).click()
        try:
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'
                .format(assignment_name + 'new')
            )
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH,
                '//a[contains(@class,"header-control next")]'
            ).click()
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'
                .format(assignment_name + 'new')
            )
        # note: only changed title is checked. changed description and due
        # dates are unchecked

        self.ps.test_updates['passed'] = True

    # Case C132532 016 - Teacher | Add/Remove/Reorder reading sections and
    # chapters
    @pytest.mark.skipif(str(132532) not in TESTS, reason="Excluded")
    def test_teacher_rearrange_reading_sections_132532(self):
        """
        Add/Remove/Reorder reading sections and chapters

        Steps:
        Click on the 'Add Assignment' button
        Click on the 'Add Reading' option
        Click on the '+ Add Readings' button
        Click on a chapter heading (not the check box)
        Click on a single section within that chapter
        Scroll to the bottom
        Click on the "Add Readings" button
        (A single reading section is displayed under Currently Selected)

        Click on the '+ Add More Readings' button
        Click on the checkbox next to a chapter heading
        Scroll to the bottom
        Click on the "Add Readings" button
        (Each section of the chapter is displayed under Currently Selected)

        Click on the 'x' next to a section
        (Section is removed from currently selected list)

        Click on the '+ Add More Readings" button
        Click on a section that is added to deselect it
        Click on the "Add Readings" button
        (Removed section doesn't appear under Currently Selected)

        Click on the '+ Add More Readings" button
        Click on at least two sections from two different chapters
        Click on the 'Add Readings" button
        Click on the '+ Add More Readings" button
        Click on the checkbox next to a chapter heading to deselect all the
        sections in it
        Click on the "Add Readings" button
        (No sections from the chapter are displayed under Currently Selected)

        Click on the arrow next to a section

        Expected result:
        Section is reordered, and moved accordingly under Currently Selected
        list
        """
        self.ps.test_updates['name'] = \
            'tutor_teacher_reading' + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = \
            ['tutor', 'teacher', 'reading', '132532']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading_016%d' % (randint(100, 999))
        assignment = Assignment()
        today = datetime.date.today()
        finish = randint(1, 6)
        # today_begin = today.strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=finish)).strftime('%m/%d/%Y')

        # Open Add Reading page
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Reading').click()

        # Fill in title
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        ).send_keys(assignment_name)

        # Set due date
        assignment.assign_date(
            driver=self.teacher.driver,
            date=end,
            is_all=True,
            target='due'
        )

        # Add single reading sections
        section = ["1.1", "1.2", "1", "3.1"]
        self.teacher.find(By.ID, 'reading-select').click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"reading-plan")]')
            )
        )
        assignment.select_sections(self.teacher.driver, section)
        self.teacher.find(
            By.XPATH, '//button[text()="Add Readings"]'
        ).click()

        # Verify the single section is selected
        for single_section in section:
            self.teacher.find(
                By.XPATH,
                '//li[@class="selected-section"]'
                '/span[@data-chapter-section="%s"]' % single_section
            )

        # Add a complete chapter
        chapter = '2'
        self.teacher.find(By.ID, 'reading-select').click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"reading-plan")]')
            )
        )

        # Find the number of sections within a chapter
        chapter_sections = self.teacher.find_all(
            By.XPATH,
            '//div[@class="panel-heading"]'
            '//div[@data-chapter-section="%s"]/../..//div[@class="section"]'
            % chapter
        )
        section_num = len(chapter_sections)

        data_chapter = self.teacher.find(
            By.XPATH,
            '//a//span[@data-chapter-section="%s"]' % chapter
        )
        data_chapter.find_element(
            By.XPATH,
            '../../span[@class="chapter-checkbox"]'
        ).click()
        self.teacher.find(
            By.XPATH, '//button[text()="Add Readings"]'
        ).click()

        # Verify the whole chapter is selected
        selected = self.teacher.find_all(
            By.XPATH, '//li[@class="selected-section"]'
            '/span[starts-with(@data-chapter-section,%s)]' % chapter
        )
        assert len(selected) == section_num, 'The whole chapter not selected'

        # Remove a single section from "Select Reading" page
        self.teacher.find(
            By.ID, 'reading-select'
        ).click()
        self.teacher.find(
            By.XPATH, '//span[@data-chapter-section=%s]' % section[0]
        ).click()
        self.teacher.find(
            By.XPATH, '//button[text()="Add Readings"]'
        ).click()
        removed_section = self.teacher.find_all(
            By.XPATH, '//span[@data-chapter-section=%s]' % section[0]
        )
        assert (len(removed_section) == 0), 'section not removed'

        # Remove a complete chapter from a reading
        self.teacher.find(
            By.ID, 'reading-select'
        ).click()
        data_chapter = self.teacher.find(
            By.XPATH,
            '//a//span[@data-chapter-section="%s"]' % chapter
        )
        data_chapter.find_element(
            By.XPATH,
            '../../span[@class="chapter-checkbox"]'
        ).click()
        self.teacher.find(
            By.XPATH, '//button[text()="Add Readings"]'
        ).click()

        # Verify the whole chapter is removed
        removed_chapter = self.teacher.find_all(
            By.XPATH,
            '//span[starts-with(@data-chapter-section, %s)]' % chapter
        )
        assert(len(removed_chapter) == 0), 'whole chapter not removed'

        # Remove a section with "x" button
        selected_sections = self.teacher.find_all(
            By.XPATH,
            '//li[@class="selected-section"]'
        )
        self.teacher.find(
            By.XPATH, '//button[contains(@class,"remove-topic")]'
        ).click()
        selected_new = self.teacher.find_all(
            By.XPATH,
            '//li[@class="selected-section"]'
        )
        assert (len(selected_sections) == len(selected_new) + 1), \
            'section not removed'

        # Reorder the reading sections
        sections = self.teacher.find_all(
            By.XPATH, '//li[@class="selected-section"]'
        )
        second_sec = sections[1].get_attribute('data-chapter-section')
        self.teacher.find(
            By.XPATH,
            '//button[contains(@class,"-move-reading-up")]'
        ).click()
        sections_new = self.teacher.find_all(
            By.XPATH, '//li[@class="selected-section"]'
        )
        new_first_sec = sections_new[0].get_attribute('data-chapter-section')
        assert (second_sec == new_first_sec), \
            'did not rearrange sections'

        # Publish and verify published status
        self.teacher.find(
            By.XPATH,
            '//button[contains(@class,"-publish")]'
        ).click()
        sleep(5)
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

    # Case C132533 017 - Teacher | Add a reading by dragging and dropping from
    # the calendar
    @pytest.mark.skipif(str(132533) not in TESTS, reason="Excluded")
    def test_teacher_add_a_reading_by_dragging_and_dropping_132533(self):
        """
        Add reading by dragging 'Add Reading' to calendar date.

        Steps:
        Click on the Add Assignment Menu
        Click and drag "Add Reading" to desired due date

        Expected Result:
        User taken to Add Reading page with due date filled in
        """
        self.ps.test_updates['name'] = \
            'tutor_teacher_reading' + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = \
            ['tutor', 'teacher', 'reading', '132533']
        self.ps.test_updates['passed'] = False

        # Test steps and verification
        self.teacher.assign.open_assignment_menu(self.teacher.driver)

        # chain setup
        print('Assignment drag tile')
        drag_tile = self.teacher.driver.find_element(
            By.ID,
            '//div[@data-assignment-type="reading" and @draggable="true"]'
        )
        # '//div[@data-assignment-type="reading"]'
        # '//div[@data-assignment-type="reading" and @draggable="true"]'

        # Select a random future date on the calendar
        try:
            day_options = self.teacher.driver.find_elements(
                By.CSS_SELECTOR, '.rc-Day--upcoming'
            )
            calendar_dest = random.choice(day_options)
        except:
            self.teacher.find(
                By.CSS_SELECTOR, '.calendar-header-control.next'
            ).click()
            day_options = self.teacher.driver.find_elements(
                By.CSS_SELECTOR, '.rc-Day--upcoming'
            )
            # calendar_dest = random.choice(day_options)
        calendar_dest = self.teacher.driver.find_element(
            By.XPATH,
            './/*[@id="ox-react-root-container"]/div/div'
            '/div/div/span/span/div/div[3]/div[2]/div[2]'
            '/div[2]/div[1]/div[6]/div/div[6]'
        )
        print('Start Action')
        try:
            actions = ActionChains(self.teacher.driver)
            # actions.drag_and_drop(drag_tile, calendar_dest).perform()
            actions \
                .click_and_hold(drag_tile) \
                .move_to_element(calendar_dest) \
                .release() \
                .perform()
            print("drop successful")
        except:
            print("drag and drop failed")

        # ActionChains(self.teacher.driver) \
        #     .move_to_element(drag_tile) \
        #     .wait(0.5) \
        #     .click_and_hold() \
        #     .wait(1)
        # ActionChains(self.teacher.driver).drag_and_drop(drag_tile,
        # calendar_dest).perform()
        # sleep(3)
        # print (self.teacher.current_url())
        assert('reading' in self.teacher.current_url()), \
            'not at Add Reading Assignment page'

        self.ps.test_updates['passed'] = True

    # Case C132534 018 - Teacher | Info icon and training wheel
    @pytest.mark.skipif(str(132534) not in TESTS, reason="Excluded")
    def test_teacher_reading_info_icon_and_training_wheel_132534(self):
        """
        Test info icon and training wheel

        Steps:
        Click on the 'Add Assignment' sidebar menu
        Click on the "Add Reading" option
        Click on the info icon at the bottom
        (Instructions about the Publish, Cancel, and Save As Draft statuses
        appear)

        Click on the question mark dropdown menu in the navbar
        Select "Page Tips"
        (A Super training wheel on "How to build a reading assignment" pops up)
        Click on "Next"
        (User is taken to training wheels)
        Click "Next" until the user exits the training wheel

        Click on the question mark dropdown menu in the navbar
        Select "Page Tips"
        Click on "Next"
        Click "X" button on the top right corner of the training wheel
        (User exits the training wheel)

        Click on "What do students see" at the bottom of the page

        Expected result:
        A Youtube video window pops up, showing the student view of your
        assignment
        """
        self.ps.test_updates['name'] = \
            'tutor_teacher_reading' + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = \
            ['tutor', 'teacher', 'reading', '132534']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        # assignment_name = 'reading_018_%d' % (randint(100, 999))
        assignment = Assignment()

        # Open Add Reading page
        assignment.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Reading').click()
        assert ('reading/new' in self.teacher.current_url()), \
            'not at add readings screen'

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

        # Super training wheel is present
        self.teacher.find(
            By.XPATH, '//div[contains(@class, "joyride-tooltip__main")]'
        )
        self.teacher.find(
            By.XPATH, '//button[contains(@data-type, "next")]'
        ).click()

        # Walk through training wheel
        self.teacher.find(By.CLASS_NAME, 'joyride-overlay')
        while self.teacher.find_all(
                By.XPATH, '//button[contains(@data-type, "next")]'):
            self.teacher.find(
                By.XPATH,
                '//button[contains(@data-type, "next")]'
            ).click()
            print(self.teacher.find_all(
                By.XPATH,
                '//button[contains(@data-type, "next")]'
            ))

        # Exit training wheel halfway
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

    # Case C132577 019 - Teacher | Get assignment link and review metrics
    @pytest.mark.skipif(str(132577) not in TESTS, reason="Excluded")
    def test_teacher_get_assignment_link_and_review_metrics_132577(self):
        """
        Get assignment link and review metrics

        Steps:
        Click on an existing reading on the calendar
        Click "Get assignment link"
        (A link for the reading assignment pops up)

        Click on "Review metrics" button
        (The teacher is taken to a page that shows problems with answers in the
        assigned reading chapters and students' progress in this reading
        assignment )

        Click on "Return to Dashboard" button

        Expected result:
        The teacher is taken to the reading summary page
        """
        self.ps.test_updates['name'] = \
            'tutor_teacher_reading' + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = \
            ['tutor', 'teacher', 'reading', '132577']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        open_title = 'open_reading019_%s' % (randint(100, 999))
        today = datetime.date.today()
        start = randint(2, 6)
        finish = start + randint(1, 5)
        begin_today = today.strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=finish)).strftime('%m/%d/%Y')

        assignment = Assignment()

        # Open Add Reading page
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Reading').click()
        assert('reading/new' in self.teacher.current_url()), \
            'not at add readings screen'

        # Find and fill in title
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        ).send_keys(open_title)

        # Fill in description
        self.teacher.find(
            By.XPATH, '//textarea[contains(@class, "form-control")]'
        ).send_keys('description')
        # use staxing function to send_keys

        # Set date
        today = datetime.date.today()
        end = randint(1, 5)
        # make the start date today so it will be open
        opens_on = today.strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=end)) \
            .strftime('%m/%d/%Y')
        assignment.assign_periods(
            self.teacher.driver, {'all': (opens_on, closes_on)})

        # add reading sections to the assignment
        self.teacher.find(By.ID, 'reading-select').click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"reading-plan")]')
            )
        )
        assignment.select_sections(self.teacher.driver, ['1.1'])
        self.teacher.find(
            By.XPATH, '//button[text()="Add Readings"]'
        ).click()

        # publish
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"-publish")]')
            )
        ).click()

        '''
        self.teacher.add_assignment(
            assignment='reading',
            args={
                'title': open_title,
                'description': 'description',
                'periods': {'all': (begin_today, end)},
                'reading_list': ['1.1', '1.2'],
                'status': 'publish'
            }
        )
        '''

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
        '''
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'lms-info-link')
            )
        ).click()
        sleep(3)
        '''
        Metrics_Button = self.teacher.driver.find_element(
                By.XPATH, '//a[contains(., "Metrics")]')
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(Metrics_Button)
        actions.move_by_offset(300, 0)
        actions.click()
        actions.perform()
        sleep(3)

        '''
        self.teacher.find(
            By.XPATH, '//div[contains(@id, "sharable-link-popover")]'
        )
        '''

        # get the value of the assignment URL
        URL = self.teacher.driver.find_element_by_class_name('copy-on-focus')
        newURL = str(URL)

        Back_Button = self.teacher.driver.find_element(
                By.CLASS_NAME, 'back')
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(Back_Button)
        actions.click()
        actions.perform()
        sleep(3)

        # Review metrics
        '''
        self.teacher.find(
            By.ID, 'view-metrics'
        ).click()
        '''
        Metrics_Button = self.teacher.driver.find_element(
                By.XPATH, '//a[contains(., "Metrics")]')
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(Metrics_Button)
        actions.click()
        actions.perform()
        assert ("metrics/" in self.teacher.current_url()), \
            "not at Review Metrics page"
        if 'http' in newURL:
            self.ps.test_updates['passed'] = True


class Actions(ActionChains):
    """Add wait to action chains."""

    def wait(self, time: float):
        """Extend monad."""
        self._actions.append(lambda: sleep(float(time)))
        return self
