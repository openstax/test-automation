"""Tutor v1, Epic 21 - Create an event."""

import inspect
import json
import os
import pytest
import unittest
import datetime
import time

from pastasauce import PastaSauce, PastaDecorator
# from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from staxing.assignment import Assignment
from selenium.webdriver.support.ui import WebDriverWait
from staxing.helper import Teacher
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException

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
        8117, 8118, 8119, 8120, 8121,
        8122, 8123, 8124, 8125, 8126,
        8127, 8128, 8129, 8130, 8131,
        8132, 8133, 8134, 8135, 8136,
        8137, 8138, 8139, 8140, 8141,
        8142, 8143, 8144, 8145, 8146,
        8147
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestCreateAnEvent(unittest.TestCase):
    """T1.21 - Create an event."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.teacher = Teacher(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        self.teacher.login()
        self.teacher.select_course(appearance='biology')

    def tearDown(self):
        """Test destructor."""
        self.ps.update_job(
            job_id=str(self.teacher.driver.session_id),
            **self.ps.test_updates
        )
        try:
            self.teacher.delete()
        except:
            pass

    # Case C8117 - 001 - Teacher | Teacher creates an event
    @pytest.mark.skipif(str(8117) not in TESTS, reason='Excluded')
    def test_teacher_create_an_event_8177(self):
        """Teacher creates an event.

        Steps:
        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Event' option
        Enter an event name into the Event name text box [user decision]
        Enter an assignment description into the Assignment description box
        Enter into Open Date text field date as MM/DD/YYYY
        Enter into Due Date text field date as MM/DD/YYYY
        Click on the Publish' button

        Expected Result:
        Takes user back to calendar dashboard.
        Event appears on its due date
        """
        self.ps.test_updates['name'] = 't1.21.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.21', 't1.21.001', '8117']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment = Assignment()
        assignment_name = 'event001'
        assignment.open_assignment_menu(self.teacher.driver)
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Event').click()
        time.sleep(1)
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.driver.find_element(
            By.ID, 'reading-title').send_keys(assignment_name)
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]//textarea' +
            '[contains(@class,"form-control")]'). \
            send_keys('description')
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        assignment.assign_periods(self.teacher.driver, {'all': [begin, end]})
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"-publish")]')
            )
        ).click()
        try:
            self.teacher.driver.find_element(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"')]")
        except NoSuchElementException:
            self.teacher.driver.find_element(
                By.XPATH, '//a[@class="calendar-header-control next"]').click()
            self.teacher.driver.find_element(
                By.XPATH,
                "//label[contains(text(), '" + assignment_name + "')]")

        self.ps.test_updates['passed'] = True

    # Case C8118 - 002 - Teacher | Add an event using the Add Assignment
    # drop down menu
    @pytest.mark.skipif(str(8118) not in TESTS, reason='Excluded')
    def test_teacher_add_an_event_using_the_add_assignment_menu_8188(self):
        """Add an event using the Add Assignment drop down menu.

        Steps:
        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Event' option

        Expected Result:
        User is taken to the add event page
        """
        self.ps.test_updates['name'] = 't1.21.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.21', 't1.21.002', '8118']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.driver.find_element(
            By.ID, 'add-assignment').click()
        self.teacher.driver.find_element(
            By.LINK_TEXT, 'Add Event').click()
        assert('events/new' in self.teacher.current_url()),\
            'not at Add Event Assignment page'

        self.ps.test_updates['passed'] = True

    # Case C8119 - 003 - Teacher | Add an event using the calendar date
    @pytest.mark.skipif(str(8119) not in TESTS, reason='Excluded')
    def test_teacher_add_event_using_the_calendar_date_8119(self):
        """Add an event using the calendar date.

        Steps:
        Click on a calendar date
        Click on the 'Add Event' option

        Expected Result:
        user taken to add ecent page with due date filled in
        """
        self.ps.test_updates['name'] = 't1.21.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.21', 't1.21.003', '8119']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        calendar_date = self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//div[contains(@class,"Day--upcoming")]/span')
            )
        )
        self.teacher.driver.execute_script(
            'return arguments[0].scrollIntoView();', calendar_date)
        self.teacher.driver.execute_script('window.scrollBy(0, -80);')
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(calendar_date)
        actions.click()
        self.teacher.sleep(3)
        actions.move_by_offset(30, 90)
        actions.click()
        actions.perform()
        assert('events/new' in self.teacher.current_url()),\
            'not at Add Event page'

        self.ps.test_updates['passed'] = True

    # Case C8120 - 004 - Teacher | Set open and due dates for all periods
    # collectively
    @pytest.mark.skipif(str(8120) not in TESTS, reason='Excluded')
    def test_teacher_set_dates_for_all_periods_collectively_8120(self):
        """Set open and due dates for all periods collectively.

        Steps:
        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Event' option
        Enter an event name into the Event name text box [user decision]
        Enter an assignment description into the Assignment description box
        [the All Periods radio button should be selected by default]
        Enter into Open Date text field date as MM/DD/YYYY
        Enter into Due Date text field date as MM/DD/YYYY
        Click on the 'Publish' button

        Expected Result:
        Takes user back to calendar dashboard.
        Event appears on its due date
        """
        self.ps.test_updates['name'] = 't1.21.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.21', 't1.21.004', '8120']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'event004'
        assignment_menu = self.teacher.driver.find_element(
            By.XPATH, '//button[contains(@class,"dropdown-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.find_element(By.XPATH, '..'). \
                get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Event').click()
        time.sleep(1)
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.driver.find_element(
            By.ID, 'reading-title').send_keys(assignment_name)
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]//textarea' +
            '[contains(@class,"form-control")]'). \
            send_keys('description')
        # assign to periods collectively
        self.teacher.driver.find_element(By.ID, 'hide-periods-radio').click()
        today = datetime.date.today()
        opens_on = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"-due-date")]' +
            '//div[contains(@class,"datepicker__input")]').click()
        # get calendar to correct month
        month = today.month
        year = today.year
        while month != int(closes_on[:2]) or year != int(closes_on[6:]):
            self.teacher.driver.find_element(
                By.XPATH, '//a[contains(@class,"navigation--next")]').click()
            if month != 12:
                month += 1
            else:
                month = 1
                year += 1
        self.teacher.driver.find_element(
            By.XPATH, '//div[contains(@class,"datepicker__day")' +
            'and contains(text(),"' + (closes_on[3:5]).lstrip('0') + '")]'
        ).click()
        time.sleep(0.5)
        self.teacher.driver.find_element(
            By.CLASS_NAME, 'assign-to-label').click()
        self.teacher.driver.find_element(
            By.XPATH, '//div[contains(@class,"-open-date")]' +
            '//div[contains(@class,"datepicker__input")]').click()
        # get calendar to correct month
        month = today.month
        year = today.year
        while month != int(opens_on[:2]) or year != int(opens_on[6:]):
            self.teacher.driver.find_element(
                By.XPATH, '//a[contains(@class,"navigation--next")]').click()
            if month != 12:
                month += 1
            else:
                month = 1
                year += 1
        self.teacher.driver.find_element(
            By.XPATH, '//div[contains(@class,"datepicker__day")' +
            'and contains(text(),"' + (opens_on[3:5]).lstrip('0') + '")]'
        ).click()
        time.sleep(0.5)
        self.teacher.driver.find_element(
            By.CLASS_NAME, 'assign-to-label').click()

        self.teacher.driver.find_element(
            By.XPATH, '//button[contains(@class,"-publish")]').click()
        try:
            self.teacher.driver.find_element(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"')]")
        except NoSuchElementException:
            self.teacher.driver.find_element(
                By.XPATH, '//a[@class="calendar-header-control next"]').click()
            self.teacher.driver.find_element(
                By.XPATH,
                "//label[contains(text(), '" + assignment_name + "')]")

        self.ps.test_updates['passed'] = True

    # Case C8121 - 005 - Teacher | Set open and due dates for periods
    # individually
    @pytest.mark.skipif(str(8121) not in TESTS, reason='Excluded')
    def test_teacher_set_dates_for_periods_individually_8121(self):
        """Set open and due dates for periods individually.

        Steps:
        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Event' option
        Enter an event name into the Event name text box
        Enter an assignment description into the text box
        Click on the "Individual Periods" radio button
        For each period
        * Enter into Open Date text field date as MM/DD/YYYY
        * Enter into Due Date text field date as MM/DD/YYYY
        Click on the Publish' button

        Expected Result:
        Takes user back to calendar dashboard.
        If there are multiple due dates event appears across all dates,
        starting at earliest due date, through latest due date.
        """
        self.ps.test_updates['name'] = 't1.21.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.21', 't1.21.005', '8121']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'event005'
        assignment_menu = self.teacher.driver.find_element(
            By.XPATH, '//button[contains(@class,"dropdown-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.find_element(By.XPATH, '..'). \
                get_attribute('class'):
            assignment_menu.click()

        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Event').click()
        time.sleep(1)
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.driver.find_element(
            By.ID, 'reading-title').send_keys('event005')
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]//textarea' +
            '[contains(@class,"form-control")]'). \
            send_keys('event description')
        # assign to periods individually
        self.teacher.driver.find_element(By.ID, 'show-periods-radio').click()
        periods = self.teacher.driver.find_elements(
            By.XPATH, '//div[contains(@class,"tasking-plan")]')
        today = datetime.date.today()
        for x in range(len(periods)):
            opens_on = (
                today + datetime.timedelta(days=x)).strftime('%m/%d/%Y')
            closes_on = (
                today + datetime.timedelta(days=(len(periods)+5))
            ).strftime('%m/%d/%Y')
            element = self.teacher.driver.find_element(
                By.XPATH, '//div[contains(@class,"tasking-plan")' +
                'and contains(@data-reactid,":'+str(x+1)+'")]' +
                '//div[contains(@class,"-due-date")]' +
                '//div[contains(@class,"datepicker__input")]')
            self.teacher.driver.execute_script(
                'window.scrollBy(0,'+str(element.size['height']+50)+');')
            time.sleep(0.5)
            element.click()
            # get calendar to correct month
            month = today.month
            year = today.year
            while month != int(closes_on[:2]) or year != int(closes_on[6:]):
                self.teacher.driver.find_element(
                    By.XPATH, '//a[contains(@class,"navigation--next")]'
                ).click()
                if month != 12:
                    month += 1
                else:
                    month = 1
                    year += 1
            self.teacher.driver.find_element(
                By.XPATH, '//div[contains(@class,"datepicker__day")' +
                'and contains(text(),"' + (closes_on[3:5]).lstrip('0') + '")]'
            ).click()
            time.sleep(0.5)
            self.teacher.driver.find_element(
                By.XPATH, '//div[contains(@class,"tasking-plan") and' +
                ' contains(@data-reactid,":'+str(x+1)+'")]' +
                '//div[contains(@class,"-open-date")]' +
                '//div[contains(@class,"datepicker__input")]').click()
            # get calendar to correct month
            month = today.month
            year = today.year
            while month != int(opens_on[:2]) or year != int(opens_on[6:]):
                self.teacher.driver.find_element(
                    By.XPATH, '//a[contains(@class,"navigation--next")]'
                ).click()
                if month != 12:
                    month += 1
                else:
                    month = 1
                    year += 1
            self.teacher.driver.find_element(
                By.XPATH, '//div[contains(@class,"datepicker__day")' +
                'and contains(text(),"' + (opens_on[3:5]).lstrip('0') + '")]'
            ).click()
            time.sleep(0.5)
        self.teacher.driver.find_element(
            By.XPATH, '//button[contains(@class,"-publish")]').click()
        try:
            self.teacher.driver.find_element(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"')]")
        except NoSuchElementException:
            self.teacher.driver.find_element(
                By.XPATH, '//a[@class="calendar-header-control next"]').click()
            self.teacher.driver.find_element(
                By.XPATH,
                "//label[contains(text(), '" + assignment_name + "')]")

        self.ps.test_updates['passed'] = True

    # Case C8122 - 006 - Teacher | Save a draft event
    @pytest.mark.skipif(str(8122) not in TESTS, reason='Excluded')
    def test_teacher_save_a_draft_event_8122(self):
        """Save a draft event.

        Steps:
        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Event' option
        Enter an event name into the Event name text box [user decision]
        Enter an assignment description into the text box
        [optional] Enter into Open Date text field date as MM/DD/YYYY
        Enter into Due Date text field date as MM/DD/YYYY
        Click on the 'Save As Draft' button

        Expected Result:
        Takes user back to calendar dashboard.
        Event appears on its due date with the word 'draft' before its name
        """
        self.ps.test_updates['name'] = 't1.21.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.21', 't1.21.006', '8122']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment = Assignment()
        assignment_name = 'event006'
        assignment.open_assignment_menu(self.teacher.driver)
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Event').click()
        time.sleep(1)
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.driver.find_element(
            By.ID, 'reading-title').send_keys(assignment_name)
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]//textarea' +
            '[contains(@class,"form-control")]'). \
            send_keys('description')
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        assignment.assign_periods(self.teacher.driver, {'all': [begin, end]})
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class," -save")]')
            )
        ).click()
        try:
            self.teacher.driver.find_element(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"')]")
        except NoSuchElementException:
            self.teacher.driver.find_element(
                By.XPATH, '//a[@class="calendar-header-control next"]').click()
            self.teacher.driver.find_element(
                By.XPATH,
                "//label[contains(text(), '" + assignment_name + "')]")

        self.ps.test_updates['passed'] = True

    # Case C8123 - 007 - Teacher | Publish a new event
    @pytest.mark.skipif(str(8123) not in TESTS, reason='Excluded')
    def test_teacher_publish_a_new_event_8123(self):
        """Publish a new event.

        Steps:
        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Event' option
        Enter an event name into the Event name text box [user decision]
        Enter an assignment description into the text box
        [optional] Enter into Open Date text field date as MM/DD/YYYY
        Enter into Due Date text field date as MM/DD/YYYY
        Click on the Publish' button

        Expected Result:
        Takes user back to calendar dashboard.
        Event appears on its due date
        """
        self.ps.test_updates['name'] = 't1.21.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.21', 't1.21.007', '8123']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment = Assignment()
        assignment_name = 'event007'
        assignment.open_assignment_menu(self.teacher.driver)
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Event').click()
        time.sleep(1)
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.driver.find_element(
            By.ID, 'reading-title').send_keys(assignment_name)
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]//textarea' +
            '[contains(@class,"form-control")]'). \
            send_keys('description')
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        assignment.assign_periods(self.teacher.driver, {'all': [begin, end]})
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class," -publish")]')
            )
        ).click()
        try:
            self.teacher.driver.find_element(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"')]")
        except NoSuchElementException:
            self.teacher.driver.find_element(
                By.XPATH, '//a[@class="calendar-header-control next"]').click()
            self.teacher.driver.find_element(
                By.XPATH,
                "//label[contains(text(), '" + assignment_name + "')]")

        self.ps.test_updates['passed'] = True

    # Case C8124 - 008 - Teacher | Publish a draft event
    @pytest.mark.skipif(str(8124) not in TESTS, reason='Excluded')
    def test_teacher_publish_a_draft_event_8124(self):
        """Publish a draft event.

        Steps:
        On the calendar dashboard click on a draft assignment
        Click on the 'Publish' button

        Expected Result:
        Takes user back to calendar dashboard.
        Event appears on its due date ('draft' in no longer before its name).
        """
        self.ps.test_updates['name'] = 't1.21.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.21', 't1.21.008', '8124']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "event008"
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='event',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'status': 'draft'
                                    })
        # click on the assignment
        try:
            self.teacher.driver.find_element(
                By.XPATH,
                '//a/label[contains(@data-title,"'+assignment_name+'")]'
            ).click()
        except NoSuchElementException:
            self.teacher.driver.find_element(
                By.XPATH,
                '//a[contains(@class,"calendar-header-control next")]'
            ).click()
            self.teacher.driver.find_element(
                By.XPATH,
                '//a/label[contains(@data-title,"'+assignment_name+'")]'
            ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class,"-publish")]')
            )
        ).click()
        try:
            self.teacher.driver.find_element(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"')]")
        except NoSuchElementException:
            self.teacher.driver.find_element(
                By.XPATH, '//a[@class="calendar-header-control next"]').click()
            self.teacher.driver.find_element(
                By.XPATH,
                "//label[contains(text(), '" + assignment_name + "')]")

        self.ps.test_updates['passed'] = True

    # Case C8125 - 009 - Teacher | Cancel a new event before making changes
    # using the Cancel button
    @pytest.mark.skipif(str(8125) not in TESTS, reason='Excluded')
    def test_teacher_canel_new_event_before_changes_using_cancel_8125(self):
        """Cancel a new event before making any changes using the Cancel button

        Steps:
        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Event' option
        Click on the "Cancel" button

        Expected Result:
        Takes user back to calendar dashboard.
        No changes have been made.
        """
        self.ps.test_updates['name'] = 't1.21.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.21', 't1.21.009', '8125']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment = Assignment()
        assignment.open_assignment_menu(self.teacher.driver)
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Event').click()
        time.sleep(1)
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.driver.find_element(
            By.XPATH,
            '//button[contains(@aria-role,"close") and text()="Cancel"]'
        ).click()
        assert('calendar' in self.teacher.current_url()),\
            'not back at calendar dashboard after canceling assignment'

        self.ps.test_updates['passed'] = True

    # Case C8126 - 010 - Teacher | Cancel a new event after making changes
    # using the Cancel button
    @pytest.mark.skipif(str(8126) not in TESTS, reason='Excluded')
    def test_teacher_cancel_new_event_after_changes_using_cancel_8126(self):
        """Cancel a new event after making any changes using the Cancel button

        Steps:
        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Event' option
        Enter an event name into the Event name text box
        Click on the "Cancel" button
        Click on the "ok" button

        Expected Result:
        Takes user back to calendar dashboard.
        No changes have been made.
        """
        self.ps.test_updates['name'] = 't1.21.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.21', 't1.21.010', '8126']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment = Assignment()
        assignment.open_assignment_menu(self.teacher.driver)
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Event').click()
        time.sleep(1)
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.driver.find_element(
            By.ID, 'reading-title').send_keys('event name')
        self.teacher.driver.find_element(
            By.XPATH,
            '//button[contains(@aria-role,"close") and text()="Cancel"]'
        ).click()
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"ok")]')
            )
        ).click()
        assert('calendar' in self.teacher.current_url()),\
            'not back at calendar dashboard after canceling assignment'

        self.ps.test_updates['passed'] = True

    # Case C8127 - 011 - Teacher | Cancel a new event before making changes
    # using the X
    @pytest.mark.skipif(str(8127) not in TESTS, reason='Excluded')
    def test_teacher_cancel_new_event_before_changes_using_the_X_8127(self):
        """Cancel a new event before making any changes using the X.

        Steps:
        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Event' option
        Click on the "x" button

        Expected Result:
        Takes user back to calendar dashboard.
        No changes have been made.
        """
        self.ps.test_updates['name'] = 't1.21.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.21', 't1.21.011', '8127']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment = Assignment()
        assignment.open_assignment_menu(self.teacher.driver)
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Event').click()
        time.sleep(1)
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.driver.find_element(
            By.XPATH,
            '//button[contains(@aria-role,"close") and ' +
            'contains(@class,"close-x")]'
        ).click()
        assert('calendar' in self.teacher.current_url()),\
            'not back at calendar dashboard after canceling assignment'

        self.ps.test_updates['passed'] = True

    # Case C8128 - 012 - Teacher | Cancel a new event after making any changes
    # using the X
    @pytest.mark.skipif(str(8128) not in TESTS, reason='Excluded')
    def test_teacher_cancel_new_event_after_changes_using_the_x_8128(self):
        """Cancel a new event after making any changes using the X.

        Steps:
        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Event' option
        Click on the "x" button

        Expected Result:
        Takes user back to calendar dashboard.
        No changes have been made.
        """
        self.ps.test_updates['name'] = 't1.21.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.21', 't1.21.012', '8128']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment = Assignment()
        assignment.open_assignment_menu(self.teacher.driver)
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Event').click()
        time.sleep(1)
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.driver.find_element(
            By.ID, 'reading-title').send_keys('event name')
        self.teacher.driver.find_element(
            By.XPATH,
            '//button[contains(@aria-role,"close") and ' +
            'contains(@class,"close-x")]'
        ).click()
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"ok")]')
            )
        ).click()
        assert('calendar' in self.teacher.current_url()),\
            'not back at calendar dashboard after canceling assignment'

        self.ps.test_updates['passed'] = True

    # Case C8129 - 013 - Teacher | Cancel a draft event before making changes
    # using the Cancel button
    @pytest.mark.skipif(str(8129) not in TESTS, reason='Excluded')
    def test_teacher_cancel_draft_event_before_changes_using_cancel_8129(self):
        """Cancel a draft event before changes using the Cancel button.

        Steps:
        Click on a draft event on the calendar dashboard
        Click on the "Cancel" button

        Expected Result:
        Takes user back to calendar dashboard.
        No changes have been made.
        """
        self.ps.test_updates['name'] = 't1.21.013' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.21', 't1.21.013', '8129']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'event013'
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='event',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'status': 'draft'
                                    })
        # click on the assignment
        try:
            self.teacher.driver.find_element(
                By.XPATH,
                '//a/label[contains(@data-title,"'+assignment_name+'")]'
            ).click()
        except NoSuchElementException:
            self.teacher.driver.find_element(
                By.XPATH,
                '//a[contains(@class,"calendar-header-control next")]'
            ).click()
            self.teacher.driver.find_element(
                By.XPATH,
                '//a/label[contains(@data-title,"'+assignment_name+'")]'
            ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH,
                 '//button[contains(@aria-role,"close") and text()="Cancel"]')
            )
        ).click()
        assert('calendar' in self.teacher.current_url()),\
            'not back at calendar dashboard after canceling draft'

        self.ps.test_updates['passed'] = True

    # Case C8130 - 014 - Teacher | Cancel a draft event after making changes
    # using the Cancel button
    @pytest.mark.skipif(str(8130) not in TESTS, reason='Excluded')
    def test_teacher_cancel_draft_event_after_changes_using_cancel_8130(self):
        """Cancel a draft event after making changes using the Cancel button.

        Steps:
        Click on a draft event on the calendar dashboard
        Click on the "Cancel" button
        click on the "ok" button

        Expected Result:
        Takes user back to calendar dashboard.
        No changes have been made.
        """
        self.ps.test_updates['name'] = 't1.21.014' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.21', 't1.21.014', '8130']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'event014'
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='event',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'status': 'draft'
                                    })
        # click on the assignment
        try:
            self.teacher.driver.find_element(
                By.XPATH,
                '//a/label[contains(@data-title,"'+assignment_name+'")]'
            ).click()
        except NoSuchElementException:
            self.teacher.driver.find_element(
                By.XPATH,
                '//a[contains(@class,"calendar-header-control next")]'
            ).click()
            self.teacher.driver.find_element(
                By.XPATH,
                '//a/label[contains(@data-title,"'+assignment_name+'")]'
            ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.driver.find_element(
            By.ID, 'reading-title').send_keys('event name')
        self.teacher.driver.find_element(
            By.XPATH,
            '//button[contains(@aria-role,"close") and text()="Cancel"]'
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"ok")]')
            )
        ).click()
        assert('calendar' in self.teacher.current_url()),\
            'not back at calendar dashboard after canceling assignment'

        self.ps.test_updates['passed'] = True

    # Case C8131 - 015 - Teacher | Cancel a draft event before making any
    # changes using the X
    @pytest.mark.skipif(str(8131) not in TESTS, reason='Excluded')
    def test_teacher_cancel_draft_event_before_changes_using_the_x_8131(self):
        """Cancel the draft event before making any changes using the X.

        Steps:
        Click on a draft event
        Click on the "x" button

        Expected Result:
        Takes user back to calendar dashboard.
        No changes have been made.
        """
        self.ps.test_updates['name'] = 't1.21.015' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.21', 't1.21.015', '8131']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "event015"
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='event',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'status': 'draft'
                                    })
        # click on the assignment
        try:
            self.teacher.driver.find_element(
                By.XPATH,
                '//a/label[contains(@data-title,"'+assignment_name+'")]'
            ).click()
        except NoSuchElementException:
            self.teacher.driver.find_element(
                By.XPATH,
                '//a[contains(@class,"calendar-header-control next")]'
            ).click()
            self.teacher.driver.find_element(
                By.XPATH,
                '//a/label[contains(@data-title,"'+assignment_name+'")]'
            ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.driver.find_element(
            By.XPATH,
            '//button[contains(@aria-role,"close") and ' +
            'contains(@class,"close-x")]'
        ).click()
        assert('calendar' in self.teacher.current_url()),\
            'not back at calendar dashboard after canceling draft'

        self.ps.test_updates['passed'] = True

    # Case C8132 - 016 - Teacher | Cancel a draft event after making changes
    # using the X
    @pytest.mark.skipif(str(8132) not in TESTS, reason='Excluded')
    def test_teacher_cancel_draft_evernt_After_changes_using_the_x_8132(self):
        """Cancel a draft event after making changes using the X.

        Steps:
        Click on a draft event
        Do at least one of the following:
        Enter an event name into the Event name text box
        Click on the "x" button
        click on the "ok" button

        Expected Result:
        Takes user back to calendar dashboard.
        No changes have been made.
        """
        self.ps.test_updates['name'] = 't1.21.016' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.21', 't1.21.016', '8132']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "event016"
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='event',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'status': 'draft'
                                    })
        # click on the assignment
        try:
            self.teacher.driver.find_element(
                By.XPATH,
                '//a/label[contains(@data-title,"'+assignment_name+'")]'
            ).click()
        except NoSuchElementException:
            self.teacher.driver.find_element(
                By.XPATH,
                '//a[contains(@class,"calendar-header-control next")]'
            ).click()
            self.teacher.driver.find_element(
                By.XPATH,
                '//a/label[contains(@data-title,"'+assignment_name+'")]'
            ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.driver.find_element(
            By.ID, 'reading-title').send_keys('event name')
        self.teacher.driver.find_element(
            By.XPATH,
            '//button[contains(@aria-role,"close") and ' +
            'contains(@class,"close-x")]'
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"ok")]')
            )
        ).click()
        assert('calendar' in self.teacher.current_url()),\
            'not back at calendar dashboard after canceling draft'

        self.ps.test_updates['passed'] = True

    # Case C8133 - 017 - Teacher | Attempt to publish a event with blank
    # required fields
    @pytest.mark.skipif(str(8133) not in TESTS, reason='Excluded')
    def test_teacher_attempt_to_publish_event_blank_reqired_fields_8133(self):
        """Attempt to publish a event with blank required fields.

        Steps:
        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Event' option
        Click on the "Publish" button

        Expected Result:
        Remains on the Add Event page.
        Does not allow user to publish event.
        Event name field becomes red, specifies that it is a required field
        """
        self.ps.test_updates['name'] = 't1.21.017' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.21', 't1.21.017', '8133']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment = Assignment()
        assignment.open_assignment_menu(self.teacher.driver)
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Event').click()
        time.sleep(1)
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.driver.find_element(
            By.XPATH, '//button[contains(@class,"-publish")]').click()
        assert('events/new' in self.teacher.current_url()),\
            'left add event page despite blank required feilds'
        self.teacher.driver.find_element(
            By.XPATH, '//span[contains(text(),"Required Field")]')

        self.ps.test_updates['passed'] = True

    # Case C8134 - 018 - Teacher | Attempt to save a draft event with blank
    # required fields
    @pytest.mark.skipif(str(8134) not in TESTS, reason='Excluded')
    def test_teacher_attempt_to_save_event_blank_required_feilds_8134(self):
        """Attempt to save a draft event with blank required fields

        Steps:
        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Event' option
        Click on the "Save As Draft" button

        Expected Result:
        Remains on the Add Event page.
        Does not allow user to publish event.
        Event name field becomes red, specifies that it is a required field
        """
        self.ps.test_updates['name'] = 't1.21.018' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.21', 't1.21.018', '8134']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment = Assignment()
        assignment.open_assignment_menu(self.teacher.driver)
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Event').click()
        time.sleep(1)
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.driver.find_element(
            By.XPATH, '//button[contains(@class,"-save")]').click()
        assert('events/new' in self.teacher.current_url()),\
            'left add event page despite blank required feilds'
        self.teacher.driver.find_element(
            By.XPATH, '//span[contains(text(),"Required Field")]')

        self.ps.test_updates['passed'] = True

    # Case C8135 - 019 - Teacher | Delete an unopened event
    @pytest.mark.skipif(str(8135) not in TESTS, reason='Excluded')
    def test_teacher_delete_an_unopened_event_8135(self):
        """Delete an unopened event.

        Steps:
        Click on an unopened event on the calendar
        Click on the 'Edit Event' button
        Click on the "Delete Assignment" button
        Click on the "ok" button

        Expected Result:
        Takes user back to calendar dashboard.
        Event has been removed.
        """
        self.ps.test_updates['name'] = 't1.21.019' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.21', 't1.21.019', '8135']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "event019"
        events = self.teacher.driver.find_elements(
            By.XPATH, '//label[contains(@data-title,"'+assignment_name+'")]')
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='event',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'status': 'publish'
                                    })
        # click on the assignment
        try:
            self.teacher.driver.find_element(
                By.XPATH,
                '//label[contains(@data-title,"'+assignment_name+'")]'
            ).click()
        except NoSuchElementException:
            self.teacher.driver.find_element(
                By.XPATH,
                '//a[contains(@class,"calendar-header-control next")]'
            ).click()
            self.teacher.driver.find_element(
                By.XPATH,
                '//label[contains(@data-title,"'+assignment_name+'")]'
            ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(@class,"edit-assignment")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class,"delete-link")]')
            )
        ).click()
        self.teacher.driver.find_element(
            By.XPATH, '//button[contains(text(),"Yes")]').click()
        assert('calendar' in self.teacher.current_url()),\
            'not back at calendar after deleting an event'
        self.teacher.driver.get(self.teacher.current_url())
        self.teacher.page.wait_for_page_load()
        events_new = self.teacher.driver.find_elements(
            By.XPATH, '//label[contains(@data-title,"'+assignment_name+'")]')
        assert(len(events) == len(events_new)),\
            'unopen event not deleted'

        self.ps.test_updates['passed'] = True

    # Case C8136 - 020 - Teacher | Delete an open event
    @pytest.mark.skipif(str(8136) not in TESTS, reason='Excluded')
    def test_teacher_delete_an_open_event_8136(self):
        """Delete an open event.

        Steps:
        Click on an open event on the calendar
        Click on the 'Edit Event' button
        Click on the "Delete Assignment" button
        Click on the "ok" button

        Expected Result:
        Takes user back to calendar dashboard.
        Event has been removed.
        """
        self.ps.test_updates['name'] = 't1.21.020' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.21', 't1.21.020', '8136']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "event020"
        events = self.teacher.driver.find_elements(
            By.XPATH, '//label[contains(@data-title,"'+assignment_name+'")]')
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='event',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'status': 'publish'
                                    })
        # click on the assignment
        try:
            self.teacher.driver.find_element(
                By.XPATH,
                '//label[contains(@data-title,"'+assignment_name+'")]'
            ).click()
        except NoSuchElementException:
            self.teacher.driver.find_element(
                By.XPATH,
                '//a[contains(@class,"calendar-header-control next")]'
            ).click()
            self.teacher.driver.find_element(
                By.XPATH,
                '//label[contains(@data-title,"'+assignment_name+'")]'
            ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(@class,"edit-assignment")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class,"delete-link")]')
            )
        ).click()
        self.teacher.driver.find_element(
            By.XPATH, '//button[contains(text(),"Yes")]').click()
        assert('calendar' in self.teacher.current_url()),\
            'not back at calendar after deleting an event'
        self.teacher.driver.get(self.teacher.current_url())
        self.teacher.page.wait_for_page_load()
        events_new = self.teacher.driver.find_elements(
            By.XPATH, '//label[contains(@data-title,"'+assignment_name+'")]')
        assert(len(events) == len(events_new)),\
            'unopen event not deleted'

        self.ps.test_updates['passed'] = True

    # Case C8137 - 021 - Teacher | Delete a draft event
    @pytest.mark.skipif(str(8137) not in TESTS, reason='Excluded')
    def test_teacher_delete_a_draft_event_8137(self):
        """Delete a draft event.

        Steps:
        Click on a draft event on the calendar
        Click on the "Delete Assignment" button
        Click on the "ok" button

        Expected Result:
        Takes user back to calendar dashboard.
        Draft Event has been removed.
        """
        self.ps.test_updates['name'] = 't1.21.021' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.21', 't1.21.021', '8137']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "event021"
        events = self.teacher.driver.find_elements(
            By.XPATH, '//label[contains(@data-title,"'+assignment_name+'")]')
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='event',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'status': 'draft'
                                    })
        # click on the assignment
        try:
            self.teacher.driver.find_element(
                By.XPATH,
                '//a/label[contains(@data-title,"'+assignment_name+'")]'
            ).click()
        except NoSuchElementException:
            self.teacher.driver.find_element(
                By.XPATH,
                '//a[contains(@class,"calendar-header-control next")]'
            ).click()
            self.teacher.driver.find_element(
                By.XPATH,
                '//a/label[contains(@data-title,"'+assignment_name+'")]'
            ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class,"delete-link")]')
            )
        ).click()
        self.teacher.driver.find_element(
            By.XPATH, '//button[contains(text(),"Yes")]').click()
        assert('calendar' in self.teacher.current_url()),\
            'not back at calendar after deleting an event'
        self.teacher.driver.get(self.teacher.current_url())
        self.teacher.page.wait_for_page_load()
        events_new = self.teacher.driver.find_elements(
            By.XPATH, '//label[contains(@data-title,"'+assignment_name+'")]')
        assert(len(events) == len(events_new)),\
            'draft event not deleted'

        self.ps.test_updates['passed'] = True

    # Case C8138 - 022 - Teacher | Add a description to an event
    @pytest.mark.skipif(str(8138) not in TESTS, reason='Excluded')
    def test_teacher_add_a_description_to_an_event_8138(self):
        """Add a description to an event.

        Steps:
        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Event' option
        Enter an event name into the Event name text box
        Enter an assignment description into the text box
        [optional] Enter into Open Date text field date as MM/DD/YYYY
        Enter into Due Date text field date as MM/DD/YYYY
        Click on the "Publish" button

        Expected Result:
        Takes user back to calendar dashboard.
        Event appears on due date, with correct description.
        """
        self.ps.test_updates['name'] = 't1.21.022' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.21', 't1.21.022', '8138']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment = Assignment()
        assignment_name = 'event022'
        assignment.open_assignment_menu(self.teacher.driver)
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Event').click()
        time.sleep(1)
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.driver.find_element(
            By.ID, 'reading-title').send_keys(assignment_name)
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]//textarea' +
            '[contains(@class,"form-control")]'). \
            send_keys('description')
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        assignment.assign_periods(self.teacher.driver, {'all': [begin, end]})
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"-publish")]')
            )
        ).click()
        try:
            self.teacher.driver.find_element(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"')]")
        except NoSuchElementException:
            self.teacher.driver.find_element(
                By.XPATH, '//a[@class="calendar-header-control next"]').click()
            self.teacher.driver.find_element(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"')]")

        self.ps.test_updates['passed'] = True

    # Case C8139 - 023 - Teacher | Change a description for a draft event
    @pytest.mark.skipif(str(8139) not in TESTS, reason='Excluded')
    def test_teacher_change_a_description_for_a_draft_event_8139(self):
        """Change a description for a draft event.

        Steps:
        Click on a draft event
        Enter a new event description into the Assignment description text box
        Click on the "Save As Draft" button

        Expected Result:
        Takes user back to calendar dashboard.
        The description of the draft event has been updated.
        """
        self.ps.test_updates['name'] = 't1.21.023' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.21', 't1.21.023', '8139']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "event023"
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='event',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'status': 'draft'
                                    })
        # click on the assignment
        try:
            self.teacher.driver.find_element(
                By.XPATH,
                '//a/label[contains(@data-title,"'+assignment_name+'")]'
            ).click()
        except NoSuchElementException:
            self.teacher.driver.find_element(
                By.XPATH,
                '//a[contains(@class,"calendar-header-control next")]'
            ).click()
            self.teacher.driver.find_element(
                By.XPATH,
                '//a/label[contains(@data-title,"'+assignment_name+'")]'
            ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]//textarea' +
            '[contains(@class,"form-control")]'). \
            send_keys('New description')
        # option for save as draft not here, change if brough back
        self.teacher.driver.find_element(
            By.XPATH, '//button[contains(@class,"-publish")]').click()
        self.teacher.sleep(3)
        assert('calendar' in self.teacher.current_url()),\
            'not taken back to calendar after updating description'

        self.ps.test_updates['passed'] = True

    # Case C8140 - 024 - Teacher | Change a description for an open event
    @pytest.mark.skipif(str(8140) not in TESTS, reason='Excluded')
    def test_teacher_change_a_description_for_an_open_event_8140(self):
        """Change a description for an open event.

        Steps:
        Click on an open event
        Click on the "Edit Event" button
        Enter a new event description into the Assignment description text box
        Click on the "Publish" button

        Expected Result:
        Takes user back to calendar dashboard.
        Event has been updated to have new description.
        """
        self.ps.test_updates['name'] = 't1.21.024' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.21', 't1.21.024', '8140']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "event024"
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='event',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'status': 'publish'
                                    })
        # click on the assignment
        try:
            self.teacher.driver.find_element(
                By.XPATH,
                '//label[contains(@data-title,"'+assignment_name+'")]'
            ).click()
        except NoSuchElementException:
            self.teacher.driver.find_element(
                By.XPATH,
                '//a[contains(@class,"calendar-header-control next")]'
            ).click()
            self.teacher.driver.find_element(
                By.XPATH,
                '//label[contains(@data-title,"'+assignment_name+'")]'
            ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(@class,"edit-assignment")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]//textarea' +
            '[contains(@class,"form-control")]'). \
            send_keys('New description')
        self.teacher.driver.find_element(
            By.XPATH, '//button[contains(@class,"-publish")]').click()
        self.teacher.sleep(3)
        assert('calendar' in self.teacher.current_url()),\
            'not taken back to calendar after updating description'

        self.ps.test_updates['passed'] = True

    # Case C8141 - 025 - Teacher | Add a name to an event
    @pytest.mark.skipif(str(8141) not in TESTS, reason='Excluded')
    def test_teacher_add_a_name_to_an_event_8141(self):
        """Add a name to an event.

        Steps:
        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Event' option
        Enter an event name into the Event name text box [user decision]
        Enter an assignment description into the text box
        [optional] Enter into Open Date text field date as MM/DD/YYYY
        Enter into Due Date text field date as MM/DD/YYYY
        Click on the Publish' button

        Expected Result:
        Takes user back to calendar dashboard.
        Event appears on its due date
        """
        self.ps.test_updates['name'] = 't1.21.025' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.21', 't1.21.025', '8141']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment = Assignment()
        assignment_name = 'event025'
        assignment.open_assignment_menu(self.teacher.driver)
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Event').click()
        time.sleep(1)
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.driver.find_element(
            By.ID, 'reading-title').send_keys(assignment_name)
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]//textarea' +
            '[contains(@class,"form-control")]'). \
            send_keys('description')
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        assignment.assign_periods(self.teacher.driver, {'all': [begin, end]})
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"-publish")]')
            )
        ).click()
        try:
            self.teacher.driver.find_element(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"')]")
        except NoSuchElementException:
            self.teacher.driver.find_element(
                By.XPATH, '//a[@class="calendar-header-control next"]').click()
            self.teacher.driver.find_element(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"')]")

        self.ps.test_updates['passed'] = True

    # Case C8142 - 026 - Teacher | Change a name for a draft event
    @pytest.mark.skipif(str(8142) not in TESTS, reason='Excluded')
    def test_teacher_change_a_name_for_a_draft_event_8142(self):
        """Change a name for a draft event.

        Steps:
        Click on the calendar click on a draft event
        Enter a new event name into the Event name text box
        Click on the 'Save As Draft' button

        Expected Result:
        Takes user back to calendar dashboard.
        Draft event name has been updated.
        """
        self.ps.test_updates['name'] = 't1.21.026' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.21', 't1.21.026', '8142']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "event026"
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='event',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'status': 'draft'
                                    })
        # click on the assignment
        try:
            self.teacher.driver.find_element(
                By.XPATH,
                '//a/label[contains(@data-title,"'+assignment_name+'")]'
            ).click()
        except NoSuchElementException:
            self.teacher.driver.find_element(
                By.XPATH,
                '//a[contains(@class,"calendar-header-control next")]'
            ).click()
            self.teacher.driver.find_element(
                By.XPATH,
                '//a/label[contains(@data-title,"'+assignment_name+'")]'
            ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.driver.find_element(
            By.ID, 'reading-title').send_keys('NEW'+assignment_name)
        self.teacher.driver.find_element(
            By.XPATH, '//button[contains(@class,"-publish")]').click()
        self.teacher.sleep(2)
        assert('calendar' in self.teacher.current_url()),\
            'not taken back to calendar after updating description'
        self.teacher.driver.find_element(
            By.XPATH, '//label[contains(text(),"NEW'+assignment_name+'")]')

        self.ps.test_updates['passed'] = True

    # Case C8143 - 027 - Teacher | Change a name for an open event
    @pytest.mark.skipif(str(8143) not in TESTS, reason='Excluded')
    def test_teacher_change_a_name_for_an_open_event_8143(self):
        """Change a name for an open event.

        Steps:
        Click on the open event on the calendar
        Click on the 'Edit Event' button
        Enter a new name into the Event name text box
        Click on the "Publish" button

        Expected Result:
        Takes user back to calendar dashboard.
        Event has been updated to have its new name.
        """
        self.ps.test_updates['name'] = 't1.21.027' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.21', 't1.21.027', '8143']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "event027"
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='event',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'status': 'publish'
                                    })
        # click on the assignment
        try:
            self.teacher.driver.find_element(
                By.XPATH,
                '//label[contains(@data-title,"'+assignment_name+'")]'
            ).click()
        except NoSuchElementException:
            self.teacher.driver.find_element(
                By.XPATH,
                '//a[contains(@class,"calendar-header-control next")]'
            ).click()
            self.teacher.driver.find_element(
                By.XPATH,
                '//label[contains(@data-title,"'+assignment_name+'")]'
            ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(@class,"edit-assignment")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.driver.find_element(
            By.ID, 'reading-title').send_keys('NEW'+assignment_name)
        self.teacher.driver.find_element(
            By.XPATH, '//button[contains(@class,"-publish")]').click()
        self.teacher.sleep(2)
        assert('calendar' in self.teacher.current_url()),\
            'not taken back to calendar after updating description'
        self.teacher.driver.find_element(
            By.XPATH, '//label[contains(text(),"NEW'+assignment_name+'")]')

        self.ps.test_updates['passed'] = True

    # Case C8144 - 028 - Teacher | Info icon shows definitions for the status
    # bar buttons
    @pytest.mark.skipif(str(8144) not in TESTS, reason='Excluded')
    def test_teacher_info_icon_shows_definitions_for_the_status_bar_8144(self):
        """Info icon shows definitions for the Add Event status bar buttons.

        Steps:
        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Event' option
        Click on the info icon

        Expected Result:
        Displays description of Publish, Cancel, and Save As Draft statuses.
        """
        self.ps.test_updates['name'] = 't1.21.028' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.21', 't1.21.028', '8144']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment = Assignment()
        assignment.open_assignment_menu(self.teacher.driver)
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Event').click()
        time.sleep(1)
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class,"footer-instructions")]')
            )
        ).click()
        self.teacher.driver.find_element(By.ID, 'plan-footer-popover')

        self.ps.test_updates['passed'] = True

    # Case C8145 - 029 - Teacher | Change all fields in an unopened,
    # published event
    @pytest.mark.skipif(str(8145) not in TESTS, reason='Excluded')
    def test_teacher_change_all_fields_in_an_unopened_event_8145(self):
        """Change all fields in an unopened, published event.

        Steps:
        Click on the calendar click on an unopened event
        Click on the "Edit Event" button
        Enter a new event name into the Event name text box
        Enter a new assignment description into the text box
        Enter into Open Date text field a new date as MM/DD/YYYY
        Enter into Due Date text field a new date as MM/DD/YYYY
        Click on the Publish' button

        Expected Result:
        Takes user back to calendar dashboard.
        Event appears on its new due date with updated information.
        """
        self.ps.test_updates['name'] = 't1.21.029' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.21', 't1.21.029', '8145']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment = Assignment()
        assignment_name = "event029"
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='event',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'status': 'publish'
                                    })
        try:
            self.teacher.driver.find_element(
                By.XPATH,
                '//label[contains(@data-title,"'+assignment_name+'")]'
            ).click()
        except NoSuchElementException:
            self.teacher.driver.find_element(
                By.XPATH,
                '//a[contains(@class,"calendar-header-control next")]'
            ).click()
            self.teacher.driver.find_element(
                By.XPATH,
                '//label[contains(@data-title,"'+assignment_name+'")]'
            ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(@class,"edit-assignment")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.driver.find_element(
            By.ID, 'reading-title').send_keys('NEW'+assignment_name)
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]//textarea' +
            '[contains(@class,"form-control")]'). \
            send_keys('NEWdescription')
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        assignment.assign_periods(self.teacher.driver, {'all': [begin, end]})
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"-publish")]')
            )
        ).click()
        try:
            self.teacher.driver.find_element(
                By.XPATH,
                "//label[contains(text(), 'NEW"+assignment_name+"')]")
        except NoSuchElementException:
            self.teacher.driver.find_element(
                By.XPATH, '//a[@class="calendar-header-control next"]').click()
            self.teacher.driver.find_element(
                By.XPATH,
                "//label[contains(text(), 'NEW"+assignment_name+"')]")

        self.ps.test_updates['passed'] = True

    # Case C8146 - 030 - Teacher | Change all fields in a draft event
    @pytest.mark.skipif(str(8146) not in TESTS, reason='Excluded')
    def test_teacher_change_all_feilds_in_a_draft_event_8146(self):
        """Change all fields in a draft event.

        Steps:
        Click on the calendar click on a draft event
        Enter a new event name into the Event name text box
        Enter a new assignment description into text box
        Enter into Open Date text field a new date as MM/DD/YYYY
        Enter into Due Date text field a new date as MM/DD/YYYY
        Click on the 'Save As Draft' button

        Expected Result:
        Takes user back to calendar dashboard.
        Event appears on its new due date with updated information.
        """
        self.ps.test_updates['name'] = 't1.21.030' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.21', 't1.21.030', '8146']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment = Assignment()
        assignment_name = "event030"
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='event',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'status': 'draft'
                                    })
        try:
            self.teacher.driver.find_element(
                By.XPATH,
                '//a/label[contains(@data-title,"'+assignment_name+'")]'
            ).click()
        except NoSuchElementException:
            self.teacher.driver.find_element(
                By.XPATH,
                '//a[contains(@class,"calendar-header-control next")]'
            ).click()
            self.teacher.driver.find_element(
                By.XPATH,
                '//a/label[contains(@data-title,"'+assignment_name+'")]'
            ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.driver.find_element(
            By.ID, 'reading-title').send_keys('NEW'+assignment_name)
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]//textarea' +
            '[contains(@class,"form-control")]'). \
            send_keys('NEWdescription')
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=7)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=8)).strftime('%m/%d/%Y')
        assignment.assign_periods(self.teacher.driver, {'all': [begin, end]})
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"-publish")]')
            )
        ).click()
        try:
            self.teacher.driver.find_element(
                By.XPATH,
                "//label[contains(text(), 'NEW"+assignment_name+"')]")
        except NoSuchElementException:
            self.teacher.driver.find_element(
                By.XPATH, '//a[@class="calendar-header-control next"]').click()
            self.teacher.driver.find_element(
                By.XPATH,
                "//label[contains(text(), 'NEW"+assignment_name+"')]")

        self.ps.test_updates['passed'] = True

    # Case C8147 - 031 - Teacher | Change the name, description, and due dates
    # in an opened event
    @pytest.mark.skipif(str(8147) not in TESTS, reason='Excluded')
    def test_teacher_change_possible_fields_in_an_open_event_8147(self):
        """Change the name, description, and due dates in an opened event.

        Steps:
        Click on the calendar click on an open event
        Click on the "Edit Event" button
        Enter a new event name into the Event name text box
        Enter a new assignment description into text box
        Enter into Due Date text field a new date as MM/DD/YYYY
        Click on the 'Publish' button

        Expected Result:
        Takes user back to calendar dashboard.
        Event appears on its new due date with updated information.
        """
        self.ps.test_updates['name'] = 't1.21.031' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.21', 't1.21.031', '8147']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "event031"
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='event',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'status': 'publish'
                                    })
        try:
            self.teacher.driver.find_element(
                By.XPATH,
                '//label[contains(@data-title,"'+assignment_name+'")]'
            ).click()
        except NoSuchElementException:
            self.teacher.driver.find_element(
                By.XPATH,
                '//a[contains(@class,"calendar-header-control next")]'
            ).click()
            self.teacher.driver.find_element(
                By.XPATH,
                '//label[contains(@data-title,"'+assignment_name+'")]'
            ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(@class,"edit-assignment")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.driver.find_element(
            By.ID, 'reading-title').send_keys('NEW'+assignment_name)
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]//textarea' +
            '[contains(@class,"form-control")]'). \
            send_keys('NEWdescription')
        # set new due date
        today = datetime.date.today()
        closes_on = (today + datetime.timedelta(days=7)).strftime('%m/%d/%Y')
        self.teacher.driver.find_element(
            By.XPATH, '//div[contains(@class,"-due-date")]' +
            '//div[contains(@class,"datepicker__input")]').click()
        # get calendar to correct month
        month = today.month
        year = today.year
        while month != int(closes_on[:2]) or year != int(closes_on[6:]):
            self.teacher.driver.find_element(
                By.XPATH, '//a[contains(@class,"navigation--next")]').click()
            if month != 12:
                month += 1
            else:
                month = 1
                year += 1
        self.teacher.driver.find_element(
            By.XPATH, '//div[contains(@class,"datepicker__day")' +
            'and contains(text(),"' + (closes_on[3:5]).lstrip('0') + '")]'
        ).click()
        time.sleep(0.5)
        self.teacher.driver.find_element(
            By.CLASS_NAME, 'assign-to-label').click()
        # publish changes
        self.teacher.driver.find_element(
            By.XPATH, '//button[contains(@class,"-publish")]').click()
        try:
            self.teacher.driver.find_element(
                By.XPATH, "//label[contains(text(), 'NEW" +
                assignment_name + "')]")
        except NoSuchElementException:
            self.teacher.driver.find_element(
                By.XPATH, '//a[@class="calendar-header-control next"]').click()
            self.teacher.driver.find_element(
                By.XPATH, "//label[contains(text(), 'NEW" +
                assignment_name + "')]")

        self.ps.test_updates['passed'] = True
