"""Tutor v1, Epic 14 - Create a Reading."""

import datetime
import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
from random import randint
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from staxing.assignment import Assignment

# select user types: Admin, ContentQA, Teacher, and/or Student
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
        7992, 7993, 7994, 7995, 7996,
        7997, 7998, 7999, 8000, 8001,
        8002, 8003, 8004, 8005, 8006,
        8007, 8008, 8009, 8010, 8011,
        8012, 8013, 8014, 8015, 8016,
        8017, 8018, 8019, 8020, 8021,
        8022, 8023, 8024, 8025, 8026,
        8027, 111246
    ])
    # 7993 - calendar date still not working
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
        self.teacher.select_course(appearance='biology')

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

    # Case C7992 - 001 - Teacher | Add a reading using the Add Assignment
    # dropdown menu
    @pytest.mark.skipif(str(7992) not in TESTS, reason='Excluded')
    def test_teacher_add_reading_using_add_assignemnt_dropdown_menu_7992(self):
        """Add a reading using the Add Assignment drop down menu.

        Steps:
        Click on the 'Add Assignment' menu
        Click on the 'Add Reading' option

        Expected Result:
        Takes user to Add Reading screen
        """
        self.ps.test_updates['name'] = 't1.14.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.001', '7992']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.ID,
            'add-assignment'
        )
        # if the Add Assignment menu is not open
        if assignment_menu.get_attribute('aria-expanded') == 'false':
            assignment_menu.click()
        self.teacher.find(By.LINK_TEXT, 'Add Reading').click()
        assert('readings/new' in self.teacher.current_url()), \
            'not at add readings screen'

        self.ps.test_updates['passed'] = True

    # Case C7993 - 002 - Teacher | Add a reading using the calendar date
    @pytest.mark.skipif(str(7993) not in TESTS, reason='Excluded')
    def test_teacher_add_a_reading_using_the_calendar_date_7993(self):
        """Add a reading using the calendar date.

        Steps:
        Click on calendar date for desired due date
        Click on the 'Add Reading' option

        Expected Result:
        Takes user to Add Reading screen
        """
        self.ps.test_updates['name'] = 't1.14.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.002', '7993']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        # # self.teacher.sleep(10)
        # calendar_dates = wait.until(
        #     expect.presence_of_all_elements_located(
        #         (By.CLASS_NAME, 'Day--upcoming')
        #     )
        # )
        # if len(calendar_dates) == 1:
        #     calendar_dates = [calendar_dates]
        calendar_date = self.teacher.find(
            By.XPATH, '//div[contains(@class,"Day--upcoming")]/span'
        )
        self.teacher.driver.execute_script(
            'return arguments[0].scrollIntoView();', calendar_date)
        self.teacher.driver.execute_script('window.scrollBy(0, -80);')
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(calendar_date)
        actions.click()
        # don't know how to add wait, just testing
        for _ in range(1000):
            actions.send_keys('slow')
        self.teacher.sleep(3)

        # It just clicks that is behing the add assignement menu?
        actions.move_by_offset(2, 15)
        actions.click()
        actions.perform()
        self.teacher.sleep(1)
        # self.teacher.find(
        #     By.XPATH, '//a[contains(text(),"Add Reading")]').click()
        # self.teacher.sleep(3)
        assert('readings/new/' in self.teacher.current_url()), \
            'not at add reading page'

        self.ps.test_updates['passed'] = True

    # Case C7994 - 003 - Teacher | Set open and due dates for all periods
    # collectively
    @pytest.mark.skipif(str(7994) not in TESTS, reason='Excluded')
    def test_teacher_set_open_and_due_dates_for_all_periods_collect_7994(self):
        """Set open and due dates for all periods collectively.

        Steps:
        Click on the 'Add Assignment' menu
        Click on the 'Add Reading' option
        Enter an assignment name into the Assignment name text box
        Enter an assignment description into the Assignment description textbox
        Click on calendar icon next to text field and select desired open date
        Click on calendar icon next to text field and select desired due date
        Click on the "+ Add Readings" button
        Click on section(s) to add to assignment
        Scroll to bottom
        Click on the "Add Readings" button
        Click on the "Publish" button

        Expected Result:
        Takes user back to calendar dashboard.
        Assignment appears on user calendar dashboard on due date with correct
        readings.
        """
        self.ps.test_updates['name'] = 't1.14.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.003', '7994']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading003_' + str(randint(100, 999))
        assignment = Assignment()
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"dropdown-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.find_element(By.XPATH, '..'). \
                get_attribute('class'):
            assignment_menu.click()
        self.teacher.find(By.LINK_TEXT, 'Add Reading').click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.find(
            By.ID, 'reading-title').send_keys(assignment_name)
        self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]//textarea' +
            '[contains(@class,"form-control")]'). \
            send_keys('description')
        # set due dates
        self.teacher.find(By.ID, "hide-periods-radio").click()
        today = datetime.date.today()
        opens_on = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"-due-date")]' +
            '//div[contains(@class,"datepicker__input")]'
        ).click()
        # get calendar to correct month
        month = today.month
        year = today.year
        while (month != int(closes_on[:2]) or year != int(closes_on[6:])):
            self.teacher.find(
                By.XPATH, '//a[contains(@class,"navigation--next")]').click()
            if month != 12:
                month += 1
            else:
                month = 1
                year += 1
        self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"datepicker__day")' +
            'and text()="' + (closes_on[3: 5]).lstrip('0') + '"]'
        ).click()
        self.teacher.sleep(0.5)
        self.teacher.find(
            By.CLASS_NAME, 'assign-to-label').click()
        self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"-open-date")]' +
            '//div[contains(@class,"datepicker__input")]'
        ).click()
        # get calendar to correct month
        month = today.month
        year = today.year
        while (month != int(opens_on[:2]) or year != int(opens_on[6:])):
            self.teacher.find(
                By.XPATH, '//a[contains(@class,"navigation--next")]').click()
            if month != 12:
                month += 1
            else:
                month = 1
                year += 1
        self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"datepicker__day")' +
            'and text()="' + (opens_on[3: 5]).lstrip('0') + '"]'
        ).click()
        self.teacher.sleep(0.5)
        self.teacher.find(
            By.CLASS_NAME, 'assign-to-label').click()
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
        try:
            self.teacher.find(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"')]")
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, "//a[contains(@class, 'header-control next')]"
            ).click()
            self.teacher.find(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"')]")

        self.ps.test_updates['passed'] = True

    # Case C7995 - 004 - Teacher | Set open and due dates for periods
    # individually
    @pytest.mark.skipif(str(7995) not in TESTS, reason='Excluded')
    def test_teacher_set_open_and_due_dates_for_periods_individuall_7995(self):
        """Set open and due dates for periods individually.

        Steps:
        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Reading' option
        Enter an assignment name into the Assignment name text box
        Enter an assignment description into the Assignment description textbox
        Select 'Individual Periods' radio button
        For each period reading is being assigned to:
        Click on calendar icon next to text field and select desired open date
        Click on calendar icon next to text field and select desired due date
        Click on the "+ Add Readings" button
        Click on section(s) to add to assignment
        Scroll to bottom
        Click on the "Add Readings" button
        Click "Publish"

        Expected Result:
        Takes user back to calendar dashboard.
        Assignment appears on user calendar dashboard on due date with correct
        readings.
        """
        self.ps.test_updates['name'] = 't1.14.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.004', '7995']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment = Assignment()
        assignment_name = 'reading004_' + str(randint(100, 999))
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"dropdown-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.find_element(By.XPATH, '..'). \
                get_attribute('class'):
            assignment_menu.click()
        self.teacher.find(By.LINK_TEXT, 'Add Reading').click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.find(
            By.ID, 'reading-title').send_keys(assignment_name)
        self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]//textarea' +
            '[contains(@class,"form-control")]'). \
            send_keys('description')
        # set date
        today = datetime.date.today()
        self.teacher.find(By.ID, 'show-periods-radio').click()
        periods = self.teacher.find_all(
            By.XPATH, '//div[contains(@class,"tasking-plan")]')
        today = datetime.date.today()
        for x in range(len(periods)):
            opens_on = (today + datetime.timedelta(days=x)). \
                strftime('%m/%d/%Y')
            closes_on = (today + datetime.timedelta(days=(len(periods)+5))). \
                strftime('%m/%d/%Y')
            element = self.teacher.find(
                By.XPATH,
                '//div[contains(@class,"tasking-plan")' +
                'and contains(@data-reactid,":'+str(x+1)+'")]' +
                '//div[contains(@class,"-due-date")]' +
                '//div[contains(@class,"datepicker__input")]')
            self.teacher.driver.execute_script(
                'window.scrollBy(0,'+str(element.size['height']+50)+');')
            self.teacher.sleep(0.5)
            element.click()
            # get calendar to correct month
            month = today.month
            year = today.year
            while (month != int(closes_on[:2]) or year != int(closes_on[6:])):
                self.teacher.find(
                    By.XPATH, '//a[contains(@class,"navigation--next")]'
                ).click()
                if month != 12:
                    month += 1
                else:
                    month = 1
                    year += 1
            self.teacher.find(
                By.XPATH,
                '//div[contains(@class,"datepicker__day")' +
                'and text()="' + (closes_on[3: 5]).lstrip('0') + '"]'
            ).click()
            self.teacher.sleep(0.5)
            self.teacher.find(
                By.XPATH,
                '//div[contains(@class,"tasking-plan") and' +
                ' contains(@data-reactid,":'+str(x+1)+'")]' +
                '//div[contains(@class,"-open-date")]' +
                '//div[contains(@class,"datepicker__input")]'
            ).click()
            # get calendar to correct month
            month = today.month
            year = today.year
            while (month != int(opens_on[:2]) or year != int(opens_on[6:])):
                self.teacher.find(
                    By.XPATH, '//a[contains(@class,"navigation--next")]'
                ).click()
                if month != 12:
                    month += 1
                else:
                    month = 1
                    year += 1
            self.teacher.find(
                By.XPATH,
                '//div[contains(@class,"datepicker__day")' +
                'and text()="' + (opens_on[3: 5]).lstrip('0') + '"]'
            ).click()
            self.teacher.sleep(0.5)
        # add reading sections to the assignment
        self.teacher.driver.execute_script("window.scrollTo(0, 0);")
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
                (By.XPATH, '//button[contains(@class, "-publish")]')
            )
        ).click()
        try:
            self.teacher.find(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"')]")
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, "//a[contains(@class, 'header-control next')]"
            ).click()
            self.teacher.find(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"')]")

        self.ps.test_updates['passed'] = True

    # Case C7996 - 005 - Teacher | Save a draft reading
    @pytest.mark.skipif(str(7996) not in TESTS, reason='Excluded')
    def test_teacher_save_a_draft_reading_7996(self):
        """Save a draft reading.

        Steps:
        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Reading' option
        Enter an assignment name into the Assignment name text box
        Enter an assignment description into the Assignment description textbox
        Click on calendar icon next to text field and select desired open date
        Click on calendar icon next to text field and select desired due date
        Click on the "+ Add Readings" button
        Click on section(s) to add to assignment
        Scroll to bottom
        Click on the "Add Readings" button
        Click "Save As Draft"

        Expected Result:
        Takes user back to calendar dashboard.
        Assignment appears on user calendar dashboard on due date with correct
        readings. 'draft' should appear before the assignment name.
        """
        self.ps.test_updates['name'] = 't1.14.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.005', '7996']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading005_' + str(randint(100, 999))
        assignment = Assignment()
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"dropdown-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.find_element(By.XPATH, '..'). \
                get_attribute('class'):
            assignment_menu.click()
        self.teacher.find(By.LINK_TEXT, 'Add Reading').click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.find(
            By.ID, 'reading-title').send_keys(assignment_name)
        self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]//textarea' +
            '[contains(@class,"form-control")]'). \
            send_keys('description')
        # set date
        today = datetime.date.today()
        opens_on = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=4)).strftime('%m/%d/%Y')
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
                (By.XPATH, '//button[contains(@class,"-save")]')
            )
        ).click()
        try:
            self.teacher.find(
                By.XPATH, "//a/label[contains(text(), '"+assignment_name+"')]")
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, "//a[contains(@class, 'header-control next')]"
            ).click()
            self.teacher.find(
                By.XPATH, "//a/label[contains(text(), '"+assignment_name+"')]")

        self.ps.test_updates['passed'] = True

    # Case C7997 - 006 - Teacher | Publish a new reading
    @pytest.mark.skipif(str(7997) not in TESTS, reason='Excluded')
    def test_teacher_publish_a_new_reading_7997(self):
        """Publish a new reading.

        Steps:
        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Reading' option
        Enter an assignment name into the Assignment name text box
        Enter an assignment description into the Assignment description textbox
        Click on the Open Date field and click on an date on calendar element
        Click on the Due Date field and click on a date on calendar element
        Click on the "+ Add Readings" button
        Click on section(s) to add to assignment
        Scroll to bottom
        Click on the "Add Readings" button
        Click "Publish"

        Expected Result:
        Takes user back to calendar dashboard.
        Assignment appears on user calendar dashboard on due date with correct
        readings.
        """
        self.ps.test_updates['name'] = 't1.14.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.006', '7997']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading006_' + str(randint(100, 999))
        assignment = Assignment()
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"dropdown-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.find_element(By.XPATH, '..'). \
                get_attribute('class'):
            assignment_menu.click()
        self.teacher.find(By.LINK_TEXT, 'Add Reading').click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.find(
            By.ID, 'reading-title').send_keys(assignment_name)
        self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]//textarea' +
            '[contains(@class,"form-control")]'). \
            send_keys('description')
        # set date
        today = datetime.date.today()
        opens_on = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=4)).strftime('%m/%d/%Y')
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
            By.XPATH, '//button[text()="Add Readings"]').click()
        # publish
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"-publish")]')
            )
        ).click()
        try:
            self.teacher.find(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"')]")
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, "//a[contains(@class, 'header-control next')]"
            ).click()
            self.teacher.find(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"')]")

        self.ps.test_updates['passed'] = True

    # Case C7998 - 007 - Teacher | Publish a draft reading
    @pytest.mark.skipif(str(7998) not in TESTS, reason='Excluded')
    def test_teacher_publish_a_draft_reading_7998(self):
        """Publish a draft reading.

        Steps:
        On the calendar click on a reading assignment that is currently a draft
        Click on the 'Publish' button

        Expected Result:
        Takes user back to calendar dashboard.
        Assignment appears on user calendar dashboard on due date with correct
        readings. 'draft' should no longer be before the assignment name.
        """
        self.ps.test_updates['name'] = 't1.14.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.007', '7998']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'Reading-%s' % randint(100, 999)
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=4)).strftime('%m/%d/%Y')
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
        try:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="calendar-container container-fluid"]')
                )
            )
            self.teacher.find(
                By.XPATH, '//a/label[contains(text(),"%s")]' % assignment_name
            ).click()
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH,
                '//a[contains(@class,"header-control next")]'
            ).click()
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="calendar-container container-fluid"]')
                )
            )
            self.teacher.find(
                By.XPATH, '//label[contains(text(),"%s")]' % assignment_name
            ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"-publish")]')
            )
        ).click()
        try:
            self.teacher.find(
                By.XPATH, '//label[contains(text(),"%s")]' % assignment_name)
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, '//a[contains(@class,"header-control next")]'
            ).click()
            self.teacher.find(
                By.XPATH, '//label[contains(text(),"%s")]' % assignment_name)

        self.ps.test_updates['passed'] = True

    # Case C7999 - 008 - Teacher | Cancel a new reading before making changes
    # using the Cancel button
    @pytest.mark.skipif(str(7999) not in TESTS, reason='Excluded')
    def test_teacher_cancel_new_reading_before_changes_cancel_7999(self):
        """Cancel a new reading before making changes using the Cancel button.

        Steps:
        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Reading' option
        Click on the 'Cancel' button

        Expected Result:
        Takes user back to calendar dashboard.
        No changes have been made on the calendar dashboard.
        """
        self.ps.test_updates['name'] = 't1.14.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.008', '7999']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"dropdown-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.find_element(By.XPATH, '..'). \
                get_attribute('class'):
            assignment_menu.click()
        self.teacher.find(By.LINK_TEXT, 'Add Reading').click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH,
                 '//button[@aria-role="close" and ' +
                 '@type="button" and text()="Cancel"]')
            )
        ).click()
        assert ('calendar' in self.teacher.current_url()),\
            'not back at calendar after canceling reading'

        self.ps.test_updates['passed'] = True

    # Case C8000 - 009 - Teacher | Cancel a new reading after making changes
    # using the Cancel button
    @pytest.mark.skipif(str(8000) not in TESTS, reason='Excluded')
    def test_teacher_cancel_new_reading_after_changes_cancel_button_8000(self):
        """Cancel a new reading after making changes using the Cancel button.

        Steps:
        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Reading' option
        Enter an assignment name into the Assignment name text box
        Click the 'Cancel' button
        Click on the "ok" button

        Expected Result:
        Takes user back to calendar dashboard.
        No changes have been made to the calendar dashboard.
        """
        self.ps.test_updates['name'] = 't1.14.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.009', '8000']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading009_' + str(randint(100, 999))
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"dropdown-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.find_element(By.XPATH, '..'). \
                get_attribute('class'):
            assignment_menu.click()
        self.teacher.find(By.LINK_TEXT, 'Add Reading').click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.find(By.ID, 'reading-title'). \
            send_keys(assignment_name)
        self.teacher.find(
            By.XPATH,
            '//button[@aria-role="close" and ' +
            '@type="button" and text()="Cancel"]'
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"ok")]')
            )
        ).click()
        assert ('calendar' in self.teacher.current_url()),\
            'not back at calendar after making changes, then canceling reading'

        self.ps.test_updates['passed'] = True

    # Case C8001 - 010 - Teacher | Cancel a new reading before making changes
    # using the X
    @pytest.mark.skipif(str(8001) not in TESTS, reason='Excluded')
    def test_teacher_cancel_new_reading_before_changes_using_the_x_8001(self):
        """Cancel a new reading before making any changes using the X.

        Steps:
        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Reading' option
        Click on the 'X' button

        Expected Result:
        Takes user back to calendar dashboard.
        No changes have been made to the calendar dashboard.
        """
        self.ps.test_updates['name'] = 't1.14.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.010', '8001']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"dropdown-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.find_element(By.XPATH, '..'). \
                get_attribute('class'):
            assignment_menu.click()
        self.teacher.find(By.LINK_TEXT, 'Add Reading').click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH,
                 '//button[@aria-role="close" and contains(@class,"close-x")]')
            )
        ).click()
        assert ('calendar' in self.teacher.current_url()),\
            'not back at calendar after canceling reading with x'

        self.ps.test_updates['passed'] = True

    # Case C8002 - 011 - Teacher | Cancel a new reading after making changes
    # using the X
    @pytest.mark.skipif(str(8002) not in TESTS, reason='Excluded')
    def test_cancel_a_new_reading_after_making_changes_using_the_x_8002(self):
        """Cancel a new reading after making changes using the X.

        Steps:
        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Reading' option
        Enter an assignment name into the Assignment name text box
        Click the 'X' button
        Click the "ok" button

        Expected Result:
        Takes user back to calendar dashboard.
        No changes have been made to the calendar dashboard.
        """
        self.ps.test_updates['name'] = 't1.14.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.011', '8002']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading011_' + str(randint(100, 999))
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"dropdown-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.find_element(By.XPATH, '..'). \
                get_attribute('class'):
            assignment_menu.click()
        self.teacher.find(By.LINK_TEXT, 'Add Reading').click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.find(By.ID, 'reading-title'). \
            send_keys(assignment_name)
        self.teacher.find(
            By.XPATH,
            '//button[@aria-role="close" and contains(@class,"close-x")]'
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"ok")]')
            )
        ).click()
        assert ('calendar' in self.teacher.current_url()),\
            'not back at calendar. canceling with x after making changes'

        self.ps.test_updates['passed'] = True

    # Case C8003 - 012 - Teacher | Cancel a draft reading before making changes
    # using the Cancel button
    @pytest.mark.skipif(str(8003) not in TESTS, reason='Excluded')
    def test_teacher_cancel_draft_reading_before_chages_cancel_8003(self):
        """Cancel draft reading before changes using the Cancel button.

        Steps:
        On the calendar click on a draft assignment
        Click on the 'Cancel' button

        Expected Result:
        Takes user back to calendar dashboard.
        No changes have been made to the chosen draft on the calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.14.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.012', '8003']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading012_' + str(randint(100, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=4)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='reading',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'reading_list': ['1.1'],
                                        'status': 'draft'
                                    })
        try:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="calendar-container container-fluid"]')
                )
            )
            self.teacher.find(
                By.XPATH, "//a/label[contains(text(), '"+assignment_name+"')]"
            ).click()
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, "//a[contains(@class, 'header-control next')]"
            ).click()
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="calendar-container container-fluid"]')
                )
            )
            self.teacher.find(
                By.XPATH, "//a/label[contains(text(), '"+assignment_name+"')]"
            ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//button[@aria-role="close" and ' +
                 '@type="button" and text()="Cancel"]')
            )
        ).click()
        assert ('calendar' in self.teacher.current_url()),\
            'not back at calendar after canceling draft reading'

        self.ps.test_updates['passed'] = True

    # Case C8004 - 013 - Teacher | Cancel a draft reading after making changes
    # using the Cancel button
    @pytest.mark.skipif(str(8004) not in TESTS, reason='Excluded')
    def test_teacher_cancel_draft_reading_after_changes_cancel_8004(self):
        """Cancel a draft reading after making changes using the Cancel button.

        Steps:
        On the calendar click on a assignment that is currently a draft
        Do at least one of the following:
        Enter an assignment name into the Assignment name text box
        Click on the 'Cancel' button
        Click on the 'ok' button

        Expected Result:
        Takes user back to calendar dashboard.
        No changes have been made to the chosen draft on the calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.14.013' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.013', '8004']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading013_' + str(randint(100, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=4)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='reading',
                                    args={
                                         'title': assignment_name,
                                         'description': 'description',
                                         'periods': {'all': (begin, end)},
                                         'reading_list': ['1.1'],
                                         'status': 'draft'
                                     })
        try:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="calendar-container container-fluid"]')
                )
            )
            self.teacher.find(
                By.XPATH, "//a/label[contains(text(), '"+assignment_name+"')]"
            ).click()
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, "//a[contains(@class, 'header-control next')]"
            ).click()
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="calendar-container container-fluid"]')
                )
            )
            self.teacher.find(
                By.XPATH, "//a/label[contains(text(), '"+assignment_name+"')]"
            ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.find(By.ID, 'reading-title'). \
            send_keys('EDIT')
        self.teacher.find(
            By.XPATH,
            '//button[@aria-role="close" and ' +
            '@type="button" and text()="Cancel"]'
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"ok")]')
            )
        ).click()
        assert ('calendar' in self.teacher.current_url()),\
            'not back at calendar after making changes, then canceling reading'

        self.ps.test_updates['passed'] = True

    # Case C8005 - 014 - Teacher | Cancel a draft reading before making changes
    # using the X
    @pytest.mark.skipif(str(8005) not in TESTS, reason='Excluded')
    def test_teacher_cancel_draft_reading_before_changes_using_x_8005(self):
        """Cancel a draft reading before making any changes using the X.

        Steps:
        On the calendar click on a draft assignment
        Click on the 'X' button

        Expected Result:
        Takes user back to calendar dashboard.
        No changes have been made to the chosen draft on the calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.14.014' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.014', '8005']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading007_' + str(randint(100, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=4)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='reading',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'reading_list': ['1.1'],
                                        'status': 'draft'
                                    })
        try:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="calendar-container container-fluid"]')
                )
            )
            self.teacher.find(
                By.XPATH,
                "//a/label[contains(text(), '"+assignment_name+"')]"
            ).click()
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, "//a[contains(@class, 'header-control next')]"
            ).click()
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="calendar-container container-fluid"]')
                )
            )
            self.teacher.find(
                By.XPATH,
                "//a/label[contains(text(), '"+assignment_name+"')]"
            ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH,
                 '//button[@aria-role="close" and contains(@class,"close-x")]')
            )
        ).click()
        assert ('calendar' in self.teacher.current_url()),\
            'not back at calendar after canceling reading with x'

        self.ps.test_updates['passed'] = True

    # Case C8006 - 015 - Teacher | Cancel a draft reading after making changes
    # using the X
    @pytest.mark.skipif(str(8006) not in TESTS, reason='Excluded')
    def test_teacher_cancel_a_draft_reading_after_changes_using_X_8006(self):
        """Cancel a draft reading after making changes using the X.

        Steps:
        On the calendar click on a assignment that is currently a draft
        Enter an assignment name into the Assignment name text box
        Click on the 'X' button
        Click on the "ok" button

        Expected Result:
        Takes user back to calendar dashboard.
        No changes have been made to the chosen draft on the calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.14.015' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.015', '8006']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading015_' + str(randint(100, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=4)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='reading',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'reading_list': ['1.1'],
                                        'status': 'draft'
                                    })
        try:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="calendar-container container-fluid"]')
                )
            )
            self.teacher.find(
                By.XPATH,
                "//a/label[contains(text(), '"+assignment_name+"')]"
            ).click()
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, "//a[contains(@class, 'header-control next')]"
            ).click()
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="calendar-container container-fluid"]')
                )
            )
            self.teacher.find(
                By.XPATH,
                "//a/label[contains(text(), '"+assignment_name+"')]"
            ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.find(By.ID, 'reading-title'). \
            send_keys('EDIT')
        self.teacher.find(
            By.XPATH,
            '//button[@aria-role="close" and contains(@class,"close-x")]'
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"ok")]')
            )
        ).click()
        assert ('calendar' in self.teacher.current_url()),\
            'not back at calendar. canceling reading with x after changes'

        self.ps.test_updates['passed'] = True

    # Case C8007 - 016 - Teacher | Attempt to publish a reading with blank
    # required fields
    @pytest.mark.skipif(str(8007) not in TESTS, reason='Excluded')
    def test_teacher_attempt_to_publish_reading_blank_required_8007(self):
        """Attempt to publish a reading with blank required fields.

        Steps:
        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Reading' option
        Click on the 'Publish' button

        Expected Result:
        Remains on the Add Assignment page.
        Does not allow user to publish assignments.
        All required fields that were left blank become red,
        and specify that they are required fields.
        """
        self.ps.test_updates['name'] = 't1.14.016' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.016', '8007']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"dropdown-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.find_element(By.XPATH, '..'). \
                get_attribute('class'):
            assignment_menu.click()
        self.teacher.find(By.LINK_TEXT, 'Add Reading').click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class,"-publish")]')
            )
        ).click()
        self.teacher.find(
            By.XPATH, '//span[contains(text(),"Required Field")]')
        assert ('readings' in self.teacher.current_url()),\
            'went back to calendar even though required feilds were left blank'

        self.ps.test_updates['passed'] = True

    # Case C8008 - 017 - Teacher | Attempt to save a draft reading with blank
    # required fields
    @pytest.mark.skipif(str(8008) not in TESTS, reason='Excluded')
    def test_teacher_attempt_save_draft_reading_blank_required_8008(self):
        """Attempt to save a draft reading with blank required fields.

        Steps:
        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Reading' option
        Click on the 'Save As Draft' button

        Expected Result:
        Remains on the Add Assignment page.
        Does not allow user to save assignments.
        All required fields that were left blank become red,
        and specify that they are required fields
        """
        self.ps.test_updates['name'] = 't1.14.017' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.017', '8008']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"dropdown-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.find_element(By.XPATH, '..'). \
                get_attribute('class'):
            assignment_menu.click()
        self.teacher.find(By.LINK_TEXT, 'Add Reading').click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class,"-save")]')
            )
        ).click()
        self.teacher.find(
            By.XPATH, '//span[contains(text(),"Required Field")]')
        assert ('readings' in self.teacher.current_url()),\
            'went back to calendar even though required feilds were left blank'

        self.ps.test_updates['passed'] = True

    # Case C8009 - 018 - Teacher | Delete an unopened reading
    @pytest.mark.skipif(str(8009) not in TESTS, reason='Excluded')
    def test_teacher_delete_an_unopened_reading_8009(self):
        """Delete an unopened reading.

        Steps:
        On the calendar click on a reading that is unopened
        Click on the 'Edit Assignment' button
        Click on the 'Delete Assignment' button
        Click on the "Yes" button

        Expected Result:
        Takes user back to calendar dashboard.
        Chosen assignment no longer appears on teacher calendar dashboard.
        """
        self.ps.test_updates['name'] = 't1.14.018' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.018', '8009']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading018_' + str(randint(0, 999))
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
                     '//div[@class="calendar-container container-fluid"]')
                )
            )
            self.teacher.find(
                By.XPATH,
                "//label[contains(text(), '"+assignment_name+"')]"
            ).click()
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, "//a[contains(@class, 'header-control next')]"
            ).click()
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="calendar-container container-fluid"]')
                )
            )
            self.teacher.find(
                By.XPATH,
                "//label[contains(text(), '"+assignment_name+"')]"
            ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(@class,"-edit-assignment")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class,"delete-link")]')
            )
        ).click()
        self.teacher.find(
            By.XPATH, '//button[contains(text(),"Yes")]').click()
        assert ('calendar' in self.teacher.current_url()), \
            'not returned to calendar after deleting an assignment'
        counter = 0
        while counter < 6:
            self.teacher.get(self.teacher.current_url())
            deleted_reading = self.teacher.find_all(
                By.XPATH, '//label[@data-title="' + assignment_name + '"]')
            if len(deleted_reading) == 0:
                break
            else:
                counter += 1
        # assert it broke out of loop before just maxing out
        assert(counter < 6), "reading not deleted"

        self.ps.test_updates['passed'] = True

    # Case C8010 - 019 - Teacher | Delete an open reading
    @pytest.mark.skipif(str(8010) not in TESTS, reason='Excluded')
    def test_teacher_delete_an_open_reading_8010(self):
        """Delete an open reading.

        Steps:
        On the calendar click on a reading that is opened
        Click on the 'Edit Assignment' button
        Click on the 'Delete Assignment' button
        Click on the "Yes" button

        Expected Result:
        Takes user back to calendar dashboard.
        Chosen assignment no longer appears on teacher calendar dashboard.
        """
        self.ps.test_updates['name'] = 't1.14.019' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.019', '8010']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading019_' + str(randint(0, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
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
                     '//div[@class="calendar-container container-fluid"]')
                )
            )
            self.teacher.find(
                By.XPATH,
                "//label[contains(text(), '"+assignment_name+"')]"
            ).click()
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, "//a[contains(@class, 'header-control next')]"
            ).click()
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="calendar-container container-fluid"]')
                )
            )
            self.teacher.find(
                By.XPATH,
                "//label[contains(text(), '"+assignment_name+"')]"
            ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(@class,"-edit-assignment")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class,"delete-link")]')
            )
        ).click()
        self.teacher.find(
            By.XPATH, '//button[contains(text(),"Yes")]').click()
        assert ('calendar' in self.teacher.current_url()), \
            'not returned to calendar after deleting an assignment'
        counter = 0
        while counter < 6:
            self.teacher.get(self.teacher.current_url())
            deleted_reading = self.teacher.find_all(
                By.XPATH, '//label[@data-title="' + assignment_name + '"]')
            if len(deleted_reading) == 0:
                break
            else:
                counter += 1
        # assert it broke out of loop before just maxing out
        assert(counter < 6), "reading not deleted"

        self.ps.test_updates['passed'] = True

    # Case C8011 - 020 - Teacher | Delete a draft reading
    @pytest.mark.skipif(str(8011) not in TESTS, reason='Excluded')
    def test_teacher_delete_a_draft_reading_8011(self):
        """Delete a draft reading.

        Steps:
        On the calendar click on a draft
        Click on the 'Delete Assignment' button
        Click on the 'Yes' button

        Expected Result:
        Takes user back to calendar dashboard.
        Chosen assignment no longer appears on teacher calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.14.020' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.020', '8011']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading020_' + str(randint(0, 999))
        original_readings = self.teacher.find_all(
            By.XPATH, '//label[@data-title="'+assignment_name+'"]')
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=4)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='reading',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'reading_list': ['1.1'],
                                        'status': 'draft'
                                    })
        try:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="calendar-container container-fluid"]')
                )
            )
            self.teacher.find(
                By.XPATH,
                "//a/label[contains(text(), '"+assignment_name+"')]"
            ).click()
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, "//a[contains(@class, 'header-control next')]"
            ).click()
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="calendar-container container-fluid"]')
                )
            )
            self.teacher.find(
                By.XPATH,
                "//a/label[contains(text(), '"+assignment_name+"')]"
            ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class,"delete-link")]')
            )
        ).click()
        self.teacher.find(
            By.XPATH, '//button[contains(text(),"Yes")]').click()
        assert ('calendar' in self.teacher.current_url()), \
            'not returned to calendar after deleting an assignment'
        self.teacher.get(self.teacher.current_url())
        deleted_reading = self.teacher.find_all(
            By.XPATH, '//label[@data-title="'+assignment_name+'"]')
        assert (len(deleted_reading) == len(original_readings)), \
            'assignment not deleted'

        self.ps.test_updates['passed'] = True

    # Case C8012 - 021 - Teacher | Add a description to a reading
    @pytest.mark.skipif(str(8012) not in TESTS, reason='Excluded')
    def test_teacher_add_a_description_to_a_reading_8012(self):
        """Add a description to a reading.

        Steps:
        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Reading' option
        Enter an assignment name into the Assignment name text box
        Enter an assignment description into the Assignment description box
        Click on the Due Date field and click on a date on calendar element
        Click on the 'Publish' button

        Expected Result:
        Takes user back to calendar dashboard.
        Assignment with description should be on calendar on its due date.
        """
        self.ps.test_updates['name'] = 't1.14.021' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.021', '8012']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading021_' + str(randint(100, 999))
        assignment = Assignment()
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"dropdown-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.find_element(By.XPATH, '..'). \
                get_attribute('class'):
            assignment_menu.click()
        self.teacher.find(By.LINK_TEXT, 'Add Reading').click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.find(
            By.ID, 'reading-title').send_keys(assignment_name)
        self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]//textarea' +
            '[contains(@class,"form-control")]'). \
            send_keys('description')
        # set date
        today = datetime.date.today()
        opens_on = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=4)).strftime('%m/%d/%Y')
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
            By.XPATH, '//button[text()="Add Readings"]').click()
        # publish
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"-publish")]')
            )
        ).click()
        try:
            self.teacher.find(
                By.XPATH,
                "//label[contains(text(), '"+assignment_name+"')]"
            )
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, "//a[contains(@class, 'header-control next')]"
            ).click()
            self.teacher.find(
                By.XPATH,
                "//label[contains(text(), '"+assignment_name+"')]"
            )
        self.ps.test_updates['passed'] = True

    # Case C8013 - 022 - Teacher | Change a description for a draft reading
    @pytest.mark.skipif(str(8013) not in TESTS, reason='Excluded')
    def test_teacher_change_a_description_for_a_draft_reading_8013(self):
        """Change a description for a draft reading.

        Steps:
        On the calendar click on a draft assignment
        Enter a new assignment description into the Assignment description box
        CLick on the 'Save As Draft' button

        Expected Result:
        Takes user back to calendar dashboard.
        Assignment description of the chosen draft has the new description.
        """
        self.ps.test_updates['name'] = 't1.14.022' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.022', '8013']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading-022_' + str(randint(100, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=4)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='reading',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'reading_list': ['1.1'],
                                        'status': 'draft'
                                    })
        try:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="calendar-container container-fluid"]')
                )
            )
            self.teacher.find(
                By.XPATH,
                "//a/label[contains(text(), '"+assignment_name+"')]"
            ).click()
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, "//a[contains(@class, 'header-control next')]"
            ).click()
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="calendar-container container-fluid"]')
                )
            )
            self.teacher.find(
                By.XPATH,
                "//a/label[contains(text(), '"+assignment_name+"')]"
            ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]//textarea' +
            '[contains(@class,"form-control")]'). \
            send_keys('NEW description')
        # no more save option, only publish
        self.teacher.find(
            By.XPATH, '//button[contains(@class,"-publish")]').click()
        try:
            self.teacher.find(
                By.XPATH,
                "//label[contains(text(), '"+assignment_name+"')]"
            )
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, "//a[contains(@class, 'header-control next')]"
            ).click()
            self.teacher.find(
                By.XPATH,
                "//label[contains(text(), '"+assignment_name+"')]"
            )
        assert('calendar' in self.teacher.current_url()),\
            'not returned to calendar after updating description'

        self.ps.test_updates['passed'] = True

    # Case C8014 - 023 - Teacher | Change a description for an open reading
    @pytest.mark.skipif(str(8014) not in TESTS, reason='Excluded')
    def test_teacher_change_a_description_for_an_open_reading_8014(self):
        """Change a description for an open reading.

        Steps:
        On the calendar click on an open reading assignment
        Click on the "Edit Assignment" button
        Enter a new assignment description into the Assignment description box
        Click on the 'Publish' button

        Expected Result:
        Takes user back to calendar dashboard.
        Assignment description of the chosen reading has the new description.
        """
        self.ps.test_updates['name'] = 't1.14.023' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.023', '8014']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading-023_' + str(randint(100, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
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
                     '//div[@class="calendar-container container-fluid"]')
                )
            )
            self.teacher.find(
                By.XPATH,
                "//label[contains(text(), '"+assignment_name+"')]"
            ).click()
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, "//a[contains(@class, 'header-control next')]"
            ).click()
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="calendar-container container-fluid"]')
                )
            )
            self.teacher.find(
                By.XPATH,
                "//label[contains(text(), '"+assignment_name+"')]"
            ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(@class,"-edit-assignment")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]//textarea' +
            '[contains(@class,"form-control")]'). \
            send_keys('NEW description')
        self.teacher.find(
            By.XPATH, '//button[contains(@class,"-publish")]').click()
        try:
            self.teacher.find(
                By.XPATH,
                "//label[contains(text(), '"+assignment_name+"')]"
            )
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, "//a[contains(@class, 'header-control next')]"
            ).click()
            self.teacher.find(
                By.XPATH,
                "//label[contains(text(), '"+assignment_name+"')]"
            )
        assert('calendar' in self.teacher.current_url()),\
            'not returned to calendar after updating description'

        self.ps.test_updates['passed'] = True

    # Case C8015 - 024 - Teacher | Add a name to a reading
    @pytest.mark.skipif(str(8015) not in TESTS, reason='Excluded')
    def test_teacher_add_a_name_to_a_reading_8015(self):
        """Add a name to a reading.

        Steps:
        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Reading' option
        Enter an assignment name into the Assignment name text box
        Click on the Open Date field and click on an date on calendar element
        Click on the Due Date field and click on a date on calendar element
        Click on the "+ Add Readings" button
        Click on section(s) to add to assignment
        scroll to bottom
        Click on the "Add Readings" button
        Click on the Publish' button

        Expected Result:
        Takes user back to calendar dashboard.
        Assignment appears on its due date with its given name.
        """
        self.ps.test_updates['name'] = 't1.14.024' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.024', '8015']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading024_' + str(randint(100, 999))
        assignment = Assignment()
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"dropdown-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.find_element(By.XPATH, '..'). \
                get_attribute('class'):
            assignment_menu.click()
        self.teacher.find(By.LINK_TEXT, 'Add Reading').click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.find(
            By.ID, 'reading-title').send_keys(assignment_name)
        self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]//textarea' +
            '[contains(@class,"form-control")]'). \
            send_keys('description')
        # set date
        today = datetime.date.today()
        opens_on = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=4)).strftime('%m/%d/%Y')
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
            By.XPATH, '//button[text()="Add Readings"]').click()
        # publish
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"-publish")]')
            )
        ).click()
        try:
            self.teacher.find(
                By.XPATH,
                "//label[contains(text(), '"+assignment_name+"')]"
            )
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, "//a[contains(@class, 'header-control next')]"
            ).click()
            self.teacher.find(
                By.XPATH,
                "//label[contains(text(), '"+assignment_name+"')]"
            )

        self.ps.test_updates['passed'] = True

    # Case C8016 - 025 - Teacher | Change a name for a draft reading
    @pytest.mark.skipif(str(8016) not in TESTS, reason='Excluded')
    def test_teacher_change_a_name_for_a_draft_reading_8016(self):
        """Change a name for a draft reading.

        Steps:
        On the calendar click on a draft
        Enter a new name into the Assignment name text box
        Click on the 'Save As Draft' button

        Expected Result:
        Takes user back to calendar dashboard.
        Assignment description of the chosen draft should have the new name.
        """
        self.ps.test_updates['name'] = 't1.14.025' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.025', '8016']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading-025_' + str(randint(100, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=4)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='reading',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'reading_list': ['1.1'],
                                        'status': 'draft'
                                    })
        try:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="calendar-container container-fluid"]')
                )
            )
            self.teacher.find(
                By.XPATH,
                "//a/label[contains(text(), '"+assignment_name+"')]"
            ).click()
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, "//a[contains(@class, 'header-control next')]"
            ).click()
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="calendar-container container-fluid"]')
                )
            )
            self.teacher.find(
                By.XPATH,
                "//a/label[contains(text(), '"+assignment_name+"')]"
            ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.find(
            By.ID, 'reading-title').send_keys('NEW')
        # only publish option now, no more save
        self.teacher.find(
            By.XPATH, '//button[contains(@class,"-publish")]').click()
        try:
            self.teacher.find(
                By.XPATH,
                "//label[contains(text(), '"+assignment_name+"NEW')]"
            )
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, "//a[contains(@class, 'header-control next')]"
            ).click()
            self.teacher.find(
                By.XPATH,
                "//label[contains(text(), '"+assignment_name+"NEW')]"
            )
        assert('calendar' in self.teacher.current_url()),\
            'not returned to calendar after updating description'

        self.ps.test_updates['passed'] = True

    # Case C8017 - 026 - Teacher | Change a name for an open reading
    @pytest.mark.skipif(str(8017) not in TESTS, reason='Excluded')
    def test_teacher_change_a_name_for_an_open_reading_8017(self):
        """Change a name for an open reading.

        Steps:
        On the calendar click on an open reading assignment
        click on the "Edit Assignment" button
        Enter a new assignment name into the Assignment name text box
        Click on the 'Publish' button

        Expected Result:
        Takes user back to calendar dashboard, with chosen assignment open.
        Assignment name of the chosen reading should have the new name.
        """
        self.ps.test_updates['name'] = 't1.14.026' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.026', '8017']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading-026_' + str(randint(100, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
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
                     '//div[@class="calendar-container container-fluid"]')
                )
            )
            self.teacher.find(
                By.XPATH,
                "//label[contains(text(), '"+assignment_name+"')]"
            ).click()
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, "//a[contains(@class, 'header-control next')]"
            ).click()
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="calendar-container container-fluid"]')
                )
            )
            self.teacher.find(
                By.XPATH,
                "//label[contains(text(), '"+assignment_name+"')]"
            ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(@class,"-edit-assignment")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.find(
            By.ID, 'reading-title').send_keys('NEW')
        # only publish option now, no more save
        self.teacher.find(
            By.XPATH, '//button[contains(@class,"-publish")]').click()
        try:
            self.teacher.find(
                By.XPATH,
                "//label[contains(text(), '"+assignment_name+"NEW')]"
            )
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, "//a[contains(@class, 'header-control next')]"
            ).click()
            self.teacher.find(
                By.XPATH,
                "//label[contains(text(), '"+assignment_name+"NEW')]"
            )
        assert('calendar' in self.teacher.current_url()),\
            'not returned to calendar after updating description'

        self.ps.test_updates['passed'] = True

    # Case C8018 - 027 - Teacher | Add a single section to a reading
    @pytest.mark.skipif(str(8018) not in TESTS, reason='Excluded')
    def test_teacher_add_a_single_section_to_a_reading_8018(self):
        """Add a single section to a reading.

        Steps:
        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Reading' option
        Enter an assignment name into the Assignment name text box
        Click on the Due Date field and click on a date on calendar element
        Click on the '+ Add More Readings' button
        Click on a chapter heading (not the check box)
        Click on a single section within that chapter
        Scroll to the bottom
        Click on the "Add Readings" button
        Click on the 'Publish' button

        Expected Result:
        Takes user back to calendar dashboard, with chosen assignment open.
        Reading assignment has been updated to have the new single section.
        """
        self.ps.test_updates['name'] = 't1.14.027' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.027', '8018']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading-027_' + str(randint(100, 999))
        assignment = Assignment()
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"dropdown-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.find_element(By.XPATH, '..'). \
                get_attribute('class'):
            assignment_menu.click()
        self.teacher.find(By.LINK_TEXT, 'Add Reading').click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.find(By.ID, 'reading-title'). \
            send_keys(assignment_name)
        self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]//textarea' +
            '[contains(@class,"form-control")]'
        ).send_keys('description')
        # set due dates
        self.teacher.find(By.ID, "hide-periods-radio").click()
        today = datetime.date.today()
        opens_on = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=4)).strftime('%m/%d/%Y')
        assignment.assign_periods(
            self.teacher.driver, {'all': [opens_on, closes_on]})
        # add reading sections to the assignment
        self.teacher.find(By.ID, 'reading-select').click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"reading-plan")]')
            )
        )
        section = '2.1'
        chapter = section.split('.')[0]
        data_chapter = self.teacher.find(
            By.XPATH,
            '//h2[contains(@data-chapter-section,"%s")]/a' % chapter
        )
        if data_chapter.get_attribute('aria-expanded') == 'false':
            data_chapter.click()
        marked = self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 ('//span[contains(@data-chapter-section' +
                  ',"{s}") and text()="{s}"]').format(s=section) +
                 '/preceding-sibling::span/input')
            )
        )
        if not marked.is_selected():
            marked.click()
        self.teacher.find(
            By.XPATH, '//button[text()="Add Readings"]'
        ).click()
        # publish
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"-publish")]')
            )
        ).click()
        try:
            self.teacher.find(
                By.XPATH,
                "//label[contains(text(), '"+assignment_name+"')]"
            )
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, "//a[contains(@class, 'header-control next')]"
            ).click()
            self.teacher.find(
                By.XPATH,
                "//label[contains(text(), '"+assignment_name+"')]"
            )

        self.ps.test_updates['passed'] = True

    # Case C8019 - 028 - Teacher | Add a complete chapter to a reading
    @pytest.mark.skipif(str(8019) not in TESTS, reason='Excluded')
    def test_teacher_add_a_complete_chapter_to_a_reading_8019(self):
        """Add a complete chapter to a reading.

        Steps:
        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Reading' option
        Enter an assignment name into the Assignment name text box
        Click on the Due Date field and click on a date on calendar element
        Click on the '+ Add More Readings' button
        Click on a chapter checkbox
        Scroll to the bottom
        Click on the "Add Readings" button
        Click on the 'Publish' button

        Expected Result:
        Takes user back to the calendar dashboard,
        the new reading assignment is displayed
        """
        self.ps.test_updates['name'] = 't1.14.028' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.028', '8019']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading-028_' + str(randint(100, 999))
        assignment = Assignment()
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"dropdown-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.find_element(By.XPATH, '..'). \
                get_attribute('class'):
            assignment_menu.click()
        self.teacher.find(By.LINK_TEXT, 'Add Reading').click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.find(By.ID, 'reading-title'). \
            send_keys(assignment_name)
        self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]//textarea' +
            '[contains(@class,"form-control")]'). \
            send_keys('description')
        # set due dates
        self.teacher.find(By.ID, "hide-periods-radio").click()
        today = datetime.date.today()
        opens_on = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=4)).strftime('%m/%d/%Y')
        assignment.assign_periods(
            self.teacher.driver, {'all': [opens_on, closes_on]})
        # add reading sections to the assignment
        self.teacher.find(By.ID, 'reading-select').click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"reading-plan")]')
            )
        )
        chapter_num = '2'
        chapter = self.teacher.find(
            By.XPATH,
            '//h2[@data-chapter-section="%s"]' % chapter_num +
            '//i[contains(@class,"tutor-icon")]'
        )
        self.teacher.sleep(0.5)
        if not chapter.is_selected():
            chapter.click()
        element = self.teacher.find(
            By.XPATH, '//button[text()="Add Readings"]')
        Assignment.scroll_to(self.teacher.driver, element)
        self.teacher.driver.execute_script('window.scrollBy(0, -80);')
        element.click()
        # publish
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"-publish")]')
            )
        ).click()
        try:
            self.teacher.find(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"')]"
            )
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, "//a[contains(@class, 'header-control next')]"
            ).click()
            self.teacher.find(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"')]"
            )

        self.ps.test_updates['passed'] = True

    # Case C8020 - 029 - Teacher | Remove a single section from a reading from
    # the Select Readings screen
    @pytest.mark.skipif(str(8020) not in TESTS, reason='Excluded')
    def test_teacher_remove_single_section_select_readings_screen_8020(self):
        """Remove a single section from the Select Readings screen.

        Steps:
        On the calendar click on a closed reading
        Click on the 'Edit Assignment' button
        Click on the '+ Add More Readings" button
        click on the check box next to a section that is currently selected
        Click on the 'Add Readings" button
        Click on the "Publish" button

        Expected Result:
        Takes user back to the calendar dashboard.
        Reading assignment has been updated to have the single section removed.
        """
        self.ps.test_updates['name'] = 't1.14.029' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.029', '8020']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading-029_' + str(randint(100, 999))
        section_to_remove = '1.2'
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=4)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='reading',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'reading_list': ['1.1',
                                                         section_to_remove,
                                                         '2.1'],
                                        'status': 'publish'
                                    })
        try:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="calendar-container container-fluid"]')
                )
            )
            self.teacher.find(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"')]"
            ).click()
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, "//a[contains(@class, 'header-control next')]"
            ).click()
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="calendar-container container-fluid"]')
                )
            )
            self.teacher.find(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"')]"
            ).click()
        self.teacher.sleep(3)       # ##########
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(@class,"-edit-assignment")]')
            )
        ).click()
        # remove section
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-select')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"reading-plan")]')
            )
        )
        chapter = section_to_remove.split('.')[0]
        data_chapter = self.teacher.find(
            By.XPATH,
            '//h2[contains(@data-chapter-section,"%s")]/a' % chapter
        )
        if data_chapter.get_attribute('aria-expanded') == 'false':
            data_chapter.click()
        marked = self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 ('//span[contains(@data-chapter-section' +
                  ',"{s}") and text()="{s}"]').format(s=section_to_remove) +
                 '/preceding-sibling::span/input')
            )
        )
        if marked.is_selected():
            marked.click()
        self.teacher.find(
            By.XPATH, '//button[text()="Add Readings"]'
        ).click()
        # check that it has been removed
        removed_sections = self.teacher.find_all(
            By.XPATH, '//span[@class="chapter-section" and' +
            '@data-chapter-section="' + section_to_remove + '"]')
        assert(len(removed_sections) == 0), \
            'section has net been removed'
        # publish
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"-publish")]')
            )
        ).click()
        try:
            self.teacher.find(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"')]"
            )
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, "//a[contains(@class, 'header-control next')]"
            ).click()
            self.teacher.find(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"')]"
            )

        self.ps.test_updates['passed'] = True

    # Case C8021 - 030 - Teacher | Remove a complete chapter from a reading
    # from the Select Readings screen
    @pytest.mark.skipif(str(8021) not in TESTS, reason='Excluded')
    def test_teacher_remove_complete_chapter_select_readings_screen_8021(self):
        """Remove a complete chapter from the Select Readings screen.

        Steps:
        On the calendar click on a closed reading
        Click on the 'Edit Assignment' button
        Click on the '+ Add More Readings' button
        Click on the checkbox next to a chapter heading that is included
        Scroll to the bottom
        Click on the "Add Readings" button
        Click on the "Publish" button

        Expected Result:
        Takes user back to the calendar dashboard.
        Reading assignment has been updated to have the chapter removed.
        """
        self.ps.test_updates['name'] = 't1.14.030' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.030', '8021']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading-030_' + str(randint(100, 999))
        section_to_remove = 'ch2'
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=4)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='reading',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'reading_list': ['ch1',
                                                         section_to_remove, ],
                                        'status': 'publish'
                                    })
        try:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="calendar-container container-fluid"]')
                )
            )
            self.teacher.find(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"')]"
            ).click()
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, "//a[contains(@class, 'header-control next')]"
            ).click()
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="calendar-container container-fluid"]')
                )
            )
            self.teacher.find(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"')]"
            ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(@class,"-edit-assignment")]')
            )
        ).click()
        # remove section
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-select')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"reading-plan")]')
            )
        )
        chapter_num = section_to_remove[2:]
        chapter = self.teacher.find(
            By.XPATH,
            '//h2[@data-chapter-section="%s"]' % chapter_num +
            '//i[contains(@class,"tutor-icon")]'
        )
        self.teacher.sleep(0.5)
        chapter.click()
        # print(chapter.is_selected())
        # raise Exception
        # if chapter.is_selected():
        #     chapter.click()
        element = self.teacher.find(
            By.XPATH, '//button[text()="Add Readings"]')
        Assignment.scroll_to(self.teacher.driver, element)
        self.teacher.driver.execute_script('window.scrollBy(0, -80);')
        element.click()
        # check that it has been removed
        removed_sections = self.teacher.find_all(
            By.XPATH,
            '//span[@class="chapter-section" and ' +
            'contains(@data-chapter-section,"'+chapter_num+'.")]')
        assert (len(removed_sections) == 0), \
            'section has net been removed'
        # publish
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"-publish")]')
            )
        ).click()
        try:
            self.teacher.find(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"')]"
            )
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, "//a[contains(@class, 'header-control next')]"
            ).click()
            self.teacher.find(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"')]"
            )

        self.ps.test_updates['passed'] = True

    # Case C8022 - 031 - Teacher | Remove a single section from a reading from
    # the Add Reading Assignment screen
    @pytest.mark.skipif(str(8022) not in TESTS, reason='Excluded')
    def test_teacher_remove_single_section_from_add_readings_screen_8022(self):
        """Remove a single section from the Add Reading Assignment screen.

        Steps:
        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Reading' option
        Enter an assignment name into the Assignment name text box
        Enter an assignment description into the Assignment description box
        Click on the Open Date field and click on an date on calendar element
        Click on the Due Date field and click on a date on calendar element
        Click on the "+ Add Readings" button
        Click on sections to add to assignment
        Scroll to bottom
        Click on the "Add Readings" button
        Click on the "x" button next to selected reading assignment to remove
        Click on the Publish' button

        Expected Result:
        Takes user back to the calendar dashboard.
        Reading assignment has been updated to have the single section removed.
        """
        self.ps.test_updates['name'] = 't1.14.031' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.031', '8022']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading-031_' + str(randint(100, 999))
        assignment = Assignment()
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"dropdown-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.find_element(By.XPATH, '..'). \
                get_attribute('class'):
            assignment_menu.click()
        self.teacher.find(By.LINK_TEXT, 'Add Reading').click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.find(By.ID, 'reading-title'). \
            send_keys(assignment_name)
        self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]//textarea' +
            '[contains(@class,"form-control")]'). \
            send_keys('description')
        # set due dates
        self.teacher.find(By.ID, "hide-periods-radio").click()
        today = datetime.date.today()
        opens_on = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=4)).strftime('%m/%d/%Y')
        assignment.assign_periods(
            self.teacher.driver, {'all': [opens_on, closes_on]})
        # add reading sections to the assignment
        self.teacher.find(By.ID, 'reading-select').click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"reading-plan")]')
            )
        )
        assignment.select_sections(self.teacher.driver, ['2.1', '3.1'])
        element = self.teacher.find(
            By.XPATH, '//button[text()="Add Readings"]')
        Assignment.scroll_to(self.teacher.driver, element)
        self.teacher.driver.execute_script('window.scrollBy(0, -80);')
        element.click()
        # publish
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"-publish")]')
            )
        )
        sections = self.teacher.find_all(
            By.XPATH, '//li[@class="selected-section"]')
        self.teacher.find(
            By.XPATH, '//button[contains(@class,"remove-topic")]').click()
        sections_new = self.teacher.find_all(
            By.XPATH, '//li[@class="selected-section"]')
        assert (len(sections) == len(sections_new)+1), 'section not removed'
        self.teacher.find(
            By.XPATH, '//button[contains(@class,"-publish")]').click()
        try:
            self.teacher.find(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"')]"
            )
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, "//a[contains(@class, 'header-control next')]"
            ).click()
            self.teacher.find(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"')]"
            )

        self.ps.test_updates['passed'] = True

    # Case C8023 - 032 - Teacher | Reorder the selected reading sections
    @pytest.mark.skipif(str(8023) not in TESTS, reason='Excluded')
    def test_teacher_reorder_the_selected_reading_sections_8023(self):
        """Reorder the selected reading sections.

        Steps:
        On the calendar click on a closed reading
        Click on the 'Edit Assignment' button
        Click on the up or down arrow buttons next to the selected readings
        Click on the "Publish" button

        Expected Result:
        Takes user back to the calendar dashboard.
        Reading assignment has been updated to have the readings in new order
        """
        self.ps.test_updates['name'] = 't1.14.032' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.032', '8023']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading-032_' + str(randint(100, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=4)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='reading',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'reading_list': ['ch1'],
                                        'status': 'publish'
                                        })
        try:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="calendar-container container-fluid"]')
                )
            )
            self.teacher.find(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"')]"
            ).click()
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, "//a[contains(@class, 'header-control next')]"
            ).click()
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="calendar-container container-fluid"]')
                )
            )
            self.teacher.find(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"')]"
            ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(@class,"-edit-assignment")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        sections = self.teacher.find_all(
            By.XPATH,
            '//li[@class="selected-section"]//span[@class="chapter-section"]')
        second_sec = sections[1].get_attribute('data-chapter-section')
        self.teacher.find(
            By.XPATH,
            '//button[contains(@class,"move-reading-up")]').click()
        sections_new = self.teacher.find_all(
            By.XPATH,
            '//li[@class="selected-section"]//span[@class="chapter-section"]')
        new_first_sec = sections_new[0].get_attribute('data-chapter-section')
        assert(second_sec == new_first_sec),\
            'did not rearrange sections'
        self.teacher.find(
            By.XPATH, '//button[contains(@class,"-publish")]').click()
        try:
            self.teacher.find(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"')]"
            )
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, "//a[contains(@class, 'header-control next')]"
            ).click()
            self.teacher.find(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"')]"
            )

        self.ps.test_updates['passed'] = True

    # Case C8024 - 033 - Teacher | Change all fields in an unopened, published
    # reading
    @pytest.mark.skipif(str(8024) not in TESTS, reason='Excluded')
    def test_teacher_change_all_feilds_unopened_published_reading_8024(self):
        """Change all fields in an unopened, published reading.

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
        self.ps.test_updates['name'] = 't1.14.033' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.033', '8024']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading-033_' + str(randint(100, 999))
        assignment = Assignment()
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=4)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='reading',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'reading_list': ['1.1', '1.2'],
                                        'status': 'publish'
                                    })
        try:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="calendar-container container-fluid"]')
                )
            )
            self.teacher.find(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"')]"
            ).click()
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, "//a[contains(@class, 'header-control next')]"
            ).click()
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="calendar-container container-fluid"]')
                )
            )
            self.teacher.find(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"')]"
            ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(@class,"-edit-assignment")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.find(
            By.ID, 'reading-title').send_keys('NEW')
        self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]//textarea' +
            '[contains(@class,"form-control")]'
        ).send_keys('new_description')
        # set new due dates
        self.teacher.find(By.ID, "hide-periods-radio").click()
        today = datetime.date.today()
        opens_on = (today + datetime.timedelta(days=2)).strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=4)).strftime('%m/%d/%Y')
        assignment.assign_periods(
            self.teacher.driver, {'all': [opens_on, closes_on]})
        # remove reading section from the assignment
        self.teacher.find(
            By.XPATH, '//button[contains(@class,"remove-topic")]').click()
        # publish
        self.teacher.find(
            By.XPATH, '//button[contains(@class,"-publish")]').click()
        try:
            self.teacher.find(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"NEW')]"
            )
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, "//a[contains(@class, 'header-control next')]"
            ).click()
            self.teacher.find(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"NEW')]"
            )

        self.ps.test_updates['passed'] = True

    # Case C8025 - 034 - Teacher | Change all fields in a draft reading
    @pytest.mark.skipif(str(8025) not in TESTS, reason='Excluded')
    def test_teacher_change_all_feilds_in_a_draft_reading_8025(self):
        """Change all fields in a draft reading.

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
        self.ps.test_updates['name'] = 't1.14.034' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.034', '8025']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading-034_' + str(randint(100, 999))
        assignment = Assignment()
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=4)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='reading',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'reading_list': ['1.1', '1.2'],
                                        'status': 'draft'
                                    })
        try:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="calendar-container container-fluid"]')
                )
            )
            self.teacher.find(
                By.XPATH, "//a/label[contains(text(), '"+assignment_name+"')]"
            ).click()
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, "//a[contains(@class, 'header-control next')]"
            ).click()
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="calendar-container container-fluid"]')
                )
            )
            self.teacher.find(
                By.XPATH, "//a/label[contains(text(), '"+assignment_name+"')]"
            ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.find(By.ID, 'reading-title'). \
            send_keys('NEW')
        self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]//textarea' +
            '[contains(@class,"form-control")]'). \
            send_keys('new_description')
        # set new due dates
        self.teacher.find(By.ID, "hide-periods-radio").click()
        today = datetime.date.today()
        opens_on = (today + datetime.timedelta(days=2)).strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=4)).strftime('%m/%d/%Y')
        assignment.assign_periods(
            self.teacher.driver, {'all': [opens_on, closes_on]})
        # remove reading section from the assignment
        self.teacher.find(
            By.XPATH, '//button[contains(@class,"remove-topic")]').click()
        # save
        self.teacher.find(
            By.XPATH, '//button[contains(@class,"-save")]').click()
        try:
            self.teacher.find(
                By.XPATH,
                "//a/label[contains(text(), '%sNEW')]" % assignment_name
            )
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, "//a[contains(@class, 'header-control next')]"
            ).click()
            self.teacher.find(
                By.XPATH,
                "//a/label[contains(text(), '%sNEW')]" % assignment_name
            )

        self.ps.test_updates['passed'] = True

    # Case C8026 - 035 - Teacher | Change the name, description and due dates
    # in an opened reading
    @pytest.mark.skipif(str(8026) not in TESTS, reason='Excluded')
    def test_teacher_change_name_description_due_date_open_reading_8026(self):
        """Change the name, description and due dates in an opened reading.

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
        self.ps.test_updates['name'] = 't1.14.035' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.035', '8026']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading-035_' + str(randint(100, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
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
                     '//div[@class="calendar-container container-fluid"]')
                )
            )
            self.teacher.find(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"')]"
            ).click()
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, "//a[contains(@class, 'header-control next')]"
            ).click()
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="calendar-container container-fluid"]')
                )
            )
            self.teacher.find(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"')]"
            ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(@class,"-edit-assignment")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.find(By.ID, 'reading-title'). \
            send_keys('NEW')
        self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]//textarea' +
            '[contains(@class,"form-control")]'
        ).send_keys('new_description')
        # set new due date
        self.teacher.find(By.ID, "hide-periods-radio").click()
        today = datetime.date.today()
        closes_on = (today + datetime.timedelta(days=4)).strftime('%m/%d/%Y')
        self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"-due-date")]' +
            '//div[contains(@class,"datepicker__input")]').click()
        month = today.month
        year = today.year
        while (month != int(closes_on[:2]) or year != int(closes_on[6:])):
            self.teacher.find(
                By.XPATH, '//a[contains(@class,"navigation--next")]').click()
            if month != 12:
                month += 1
            else:
                month = 1
                year += 1
        self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"datepicker__day")' +
            'and text()="' + (closes_on[3: 5]).lstrip('0') + '"]'
        ).click()
        self.teacher.sleep(0.5)
        self.teacher.find(
            By.CLASS_NAME, 'assign-to-label').click()
        self.teacher.find(
            By.XPATH, '//button[contains(@class,"-publish")]').click()
        try:
            self.teacher.find(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"NEW')]"
            )
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, "//a[contains(@class, 'header-control next')]"
            ).click()
            self.teacher.find(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"NEW')]"
            )

        self.ps.test_updates['passed'] = True

    # Case C8027 - 036 - Teacher | Info icon shows definitions for the status
    # bar buttons
    @pytest.mark.skipif(str(8027) not in TESTS, reason='Excluded')
    def test_teacher_info_icon_shows_definitions_for_status_buttons_8027(self):
        """Info icon shows definitions for the status bar buttons.

        Steps:
        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Reading' option
        Click on the info icon

        Expected Result:
        Instructions about the Publish, Cancel, and Save As Draft appear
        """
        self.ps.test_updates['name'] = 't1.14.036' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.036', '8027']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading-035_' + str(randint(100, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
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
                     '//div[@class="calendar-container container-fluid"]')
                )
            )
            self.teacher.find(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"')]"
            ).click()
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, "//a[contains(@class, 'header-control next')]"
            ).click()
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="calendar-container container-fluid"]')
                )
            )
            self.teacher.find(
                By.XPATH, "//label[contains(text(), '"+assignment_name+"')]"
            ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(@class,"-edit-assignment")]')
            )
        ).click()
        self.teacher.find(
            By.XPATH, '//button[contains(@class,"footer-instructions")]'
        ).click()
        self.teacher.find(By.ID, 'plan-footer-popover')

        self.ps.test_updates['passed'] = True

    # Case C111246 - 004 - Teacher | Add reading by dragging Add Reading to
    # calendar date
    @pytest.mark.skipif(str(111246) not in TESTS, reason='Excluded')
    def test_teacher_add_reading_by_dragging_add_reading_to_calen_111246(self):
        """Add reading by dragging Add Reading to calendar date.

        Steps:
        Click on the Add Assignment Menu
        Click and drag "Add Reading" to desired due date

        Expected Result:
        User taken to Add Reading page with due date filled in
        """
        self.ps.test_updates['name'] = 't1.14.037' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.037', '111246']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
