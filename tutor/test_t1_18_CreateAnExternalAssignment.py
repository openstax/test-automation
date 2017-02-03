"""Product, Epic 18 - CreateAnExternalAssignment."""

import datetime
import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
from random import randint
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.ui import WebDriverWait
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
        8085, 8086, 8087, 8088, 8089,
        8090, 8091, 8092, 8093, 8094,
        8095, 8096, 8097, 8098, 8099,
        8100, 8101, 8102, 8103, 8104,
        8105, 8106, 8107, 8108, 8109,
        8110, 8111, 8112, 8113, 8114,
        8115, 8116, 111248
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestCreateAnExternalAssignment(unittest.TestCase):
    """T1.18 - Epic TextCreate an external assignment."""

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

    # Case C8085 - 001 - Teacher | Add an external assignment using the
    # Add Assignment menu drop down menu
    @pytest.mark.skipif(str(8085) not in TESTS, reason='Excluded')
    def test_teacher_add_external_assignment_using_drop_down_menu_8085(self):
        """Add an external assignment using the Add Assignment menu.

        Steps:
        Click on the Add Assignment drop down menu
        Click on the Add External Assignment option

        Expected Result:
        User taken to Add External Assignment Page
        """
        self.ps.test_updates['name'] = 't1.18.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.001', '8085']
        self.ps.test_updates['passed'] = False

        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.find(
            By.LINK_TEXT, 'Add External Assignment').click()
        assert('external/new' in self.teacher.current_url()),\
            'not at Add External Assignment page'

        self.ps.test_updates['passed'] = True

    # Case C8086 - 002 - Teacher | Add an external assignment using the
    # calendar date
    @pytest.mark.skipif(str(8086) not in TESTS, reason='Excluded')
    def test_teacher_add_external_assignment_using_calendar_date_8086(self):
        """Add an external assignment using the calendar date.

        Steps:
        Click on a calendar date
        Click on the Add External Assignment option

        Expected Result:
        User taken to Add External Assignment page with due date filled in
        """
        self.ps.test_updates['name'] = 't1.18.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.002', '8086']
        self.ps.test_updates['passed'] = False

        # click on calendar date
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
        actions.move_by_offset(30, 70)
        actions.click()
        actions.perform()
        assert('external/new' in self.teacher.current_url()),\
            'not at Add External Assignment page'

        self.ps.test_updates['passed'] = True

    # Case C8087 - 003 - Teacher | Set open and due dates for all periods
    # collectively
    @pytest.mark.skipif(str(8087) not in TESTS, reason='Excluded')
    def test_teacher_dates_for_all_periods_collectively_8087(self):
        """Set open and due dates for all periods collectively.

        Steps:
        Click on the Add Assignment drop down menu
        Click on the Add External Assignment option
        Enter an Assignment name into the Assignment Name text box
        Enter date into the Open Date text feild as MM/DD/YYYY
        Enter date into the Due Date text feild as MM/DD/YYYY
        Enter a URL into the Assignment URL text box
        Click on the Publish button

        Expected Result:
        External assignment appears on the calendar dashboard on its due date
        """
        self.ps.test_updates['name'] = 't1.18.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.003', '8087']
        self.ps.test_updates['passed'] = False

        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.find(
            By.LINK_TEXT, 'Add External Assignment').click()
        self.teacher.sleep(1)
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.find(
            By.ID, 'reading-title').send_keys('ext003')
        self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]//textarea' +
            '[contains(@class,"form-control")]'). \
            send_keys('external assignment description')
        # set date
        self.teacher.find(By.ID, 'hide-periods-radio').click()
        today = datetime.date.today()
        # start = randint(1, 10)
        opens_on = (today + datetime.timedelta(days=0)) \
            .strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=1)) \
            .strftime('%m/%d/%Y')
        self.teacher.find(
            By.XPATH, '//div[contains(@class,"-due-date")]' +
            '//div[contains(@class,"datepicker__input")]').click()
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
            ' and not(contains(@class,"disabled")) ' +
            ' and text()="' + (closes_on[3:5]).lstrip('0') + '"]'
        ).click()
        self.teacher.sleep(0.5)
        self.teacher.find(
            By.CLASS_NAME, 'assign-to-label').click()
        self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"-open-date")]' +
            '//div[contains(@class,"datepicker__input")]').click()
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
            ' and not(contains(@class,"disabled")) ' +
            ' and text()="' + (opens_on[3:5]).lstrip('0') + '"]'
        ).click()
        self.teacher.sleep(0.5)
        self.teacher.find(
            By.CLASS_NAME, 'assign-to-label').click()
        self.teacher.find(
            By.ID, 'external-url').send_keys('website.com')
        self.teacher.find(
            By.XPATH, '//button[contains(@class,"-publish")]').click()
        try:
            self.teacher.find(
                By.XPATH, "//label[contains(text(), 'ext003')]")
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, '//a[@class="calendar-header-control next"]').click()
            self.teacher.find(
                By.XPATH, "//label[contains(text(), 'ext003')]")

        self.ps.test_updates['passed'] = True

    # Case C8088 - 004 - Teacher | Set open and due dates for  periods
    # individually
    @pytest.mark.skipif(str(8088) not in TESTS, reason='Excluded')
    def test_teacher_dates_for_periods_individually_8088(self):
        """Set open and due dates for periods individually.

        Steps:
        Click on the Add Assignment drop down menu
        Click on the Add External Assignment option
        Enter an Assignment name into the Assignment Name text box
        Click on the Individual periods radio button
        For each period:
        * Enter date into the Open Date text feild as MM/DD/YYYY
        * Enter date into the Due Date text feild as MM/DD/YYYY
        Enter a URL into the Assignment URL text box
        Click on the Publish button

        Expected Result:
        New external assignment appears on the calendar dashboard
        appears across its due dates
        """
        self.ps.test_updates['name'] = 't1.18.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.004', '8088']
        self.ps.test_updates['passed'] = False

        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()

        self.teacher.find(
            By.LINK_TEXT, 'Add External Assignment').click()
        self.teacher.sleep(1)
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.find(
            By.ID, 'reading-title').send_keys('ext004')
        self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]//textarea' +
            '[contains(@class,"form-control")]'). \
            send_keys('external assignment description')

        # assign to periods individually
        self.teacher.find(By.ID, 'show-periods-radio').click()
        periods = self.teacher.find_all(
            By.XPATH, '//div[contains(@class,"tasking-plan")]')
        today = datetime.date.today()
        for x in range(len(periods)):
            opens_on = (
                today + datetime.timedelta(days=x + 1)).strftime('%m/%d/%Y')
            closes_on = (
                today + datetime.timedelta(days=len(periods) + 5)
            ).strftime('%m/%d/%Y')
            element = self.teacher.find(
                By.XPATH,
                '//div[contains(@class,"tasking-plan")][%s]' % (x + 1) +
                '//div[contains(@class,"-due-date")]' +
                '//div[contains(@class,"datepicker__input")]')
            self.teacher.driver.execute_script(
                'window.scrollBy(0,' + str(element.size['height'] + 50) + ');')
            self.teacher.sleep(0.5)
            element.click()
            # get calendar to correct month
            month = today.month
            year = today.year
            while (month != int(closes_on[:2]) or year != int(closes_on[6:])):
                self.teacher.find(
                    By.XPATH,
                    '//a[contains(@class,"navigation--next")]'
                ).click()
                if month != 12:
                    month += 1
                else:
                    month = 1
                    year += 1
            self.teacher.find(
                By.XPATH, '//div[contains(@class,"datepicker__day") ' +
                ' and not(contains(@class,"disabled")) ' +
                ' and text()="' + (closes_on[3:5]).lstrip('0') + '"]'
            ).click()
            self.teacher.sleep(0.5)
            self.teacher.find(
                By.XPATH,
                '//div[contains(@class,"tasking-plan")][%s]' % (x + 1) +
                '//div[contains(@class,"-open-date")]' +
                '//div[contains(@class,"datepicker__input")]').click()
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
                By.XPATH, '//div[contains(@class,"datepicker__day")' +
                ' and not(contains(@class,"disabled")) ' +
                ' and text()="' + (opens_on[3:5]).lstrip('0') + '"]'
            ).click()
            self.teacher.sleep(0.5)
        self.teacher.find(
            By.ID, 'external-url').send_keys('website.com')
        self.teacher.find(
            By.XPATH, '//button[contains(@class,"-publish")]').click()
        try:
            self.teacher.find(
                By.XPATH, "//label[contains(text(), 'ext004')]")
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, '//a[@class="calendar-header-control next"]').click()
            self.teacher.find(
                By.XPATH, "//label[contains(text(), 'ext004')]")

        self.ps.test_updates['passed'] = True

    # Case C8089 - 005 - Teacher | Save a draft external Assignment
    @pytest.mark.skipif(str(8089) not in TESTS, reason='Excluded')
    def test_teacher_save_a_draft_external_assignment_8089(self):
        """Save a draft external Assignment.

        Steps:
        Click on the Add Assignment drop down menu
        Click on the Add External Assignment option
        Enter an Assignment name into the Assignment Name text box
        Enter date into the Due Date text feild as MM/DD/YYYY
        Enter a URL into the Assignment URL text box
        Click on the Save As Draft button

        Expected Result:
        Draft external assignment appears on the calendar dashboard
        on its due date with the word draft before te title
        """
        self.ps.test_updates['name'] = 't1.18.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.005', '8089']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment = Assignment()
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()

        self.teacher.find(
            By.LINK_TEXT, 'Add External Assignment').click()
        self.teacher.sleep(1)
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.find(
            By.ID, 'reading-title').send_keys('ext005')
        self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]//textarea' +
            '[contains(@class,"form-control")]'). \
            send_keys('external Assignment description')
        today = datetime.date.today()
        opens_on = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        print("open date: %s" % opens_on)
        print("due date: %s" % closes_on)
        assignment.assign_periods(
            self.teacher.driver, {'all': (opens_on, closes_on)})
        self.teacher.find(
            By.ID, 'external-url').send_keys('website.com')
        self.teacher.find(
            By.XPATH, '//button[contains(@class,"-save")]').click()
        self.teacher.sleep(4)
        try:
            self.teacher.find(
                By.XPATH, "//label[contains(text(), 'ext005')]")
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, '//a[@class="calendar-header-control next"]').click()
            self.teacher.find(
                By.XPATH, "//label[contains(text(), 'ext005')]")

        self.ps.test_updates['passed'] = True

    # Case C8090 - 006 - Teacher | Publish a new external Assignment
    @pytest.mark.skipif(str(8090) not in TESTS, reason='Excluded')
    def test_teacher_publish_a_new_external_assignment_8090(self):
        """Publish a new external Assignment.

        Steps:
        Click on the Add Assignment drop down menu
        Click on the Add External Assignment option
        Enter an Assignment name into the Assignment Name text box
        Enter date into the Due Date text feild as MM/DD/YYYY
        Enter a URL into the Assignment URL text box
        Click on the Publish button

        Expected Result:
        External assignment appears on the calendar dashboard on its due date
        """
        self.ps.test_updates['name'] = 't1.18.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.006', '8090']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "ext006_" + str(randint(0, 999))
        assignment = Assignment()
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()

        self.teacher.find(
            By.LINK_TEXT, 'Add External Assignment').click()
        self.teacher.sleep(1)
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
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
            send_keys('external Assignment description')
        today = datetime.date.today()
        opens_on = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        assignment.assign_periods(
            self.teacher.driver, {'all': (opens_on, closes_on)})
        self.teacher.find(
            By.ID, 'external-url').send_keys('website.com')
        self.teacher.find(
            By.XPATH, '//button[contains(@class,"-publish")]').click()
        self.teacher.sleep(4)
        try:
            self.teacher.find(
                By.XPATH,
                "//label[contains(text(), '" + assignment_name + "')]")
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, '//a[@class="calendar-header-control next"]').click()
            self.teacher.find(
                By.XPATH,
                "//label[contains(text(), '" + assignment_name + "')]")

        self.ps.test_updates['passed'] = True

    # Case C8091 - 007 - Teacher | Publish a draft external Assignment
    @pytest.mark.skipif(str(8091) not in TESTS, reason='Excluded')
    def test_teacher_publish_a_draft_external_assignment_8091(self):
        """Publish a draft external Assignment.

        Steps:
        Click on the Add Assignment drop down menu
        Click on the Add External Assignment option
        Enter an Assignment name into the Assignment Name text box
        Enter date into the Due Date text feild as MM/DD/YYYY
        Enter a URL into the Assignment URL text box
        Click on the Save As Draft button
        Click on the draft on the calendar dashboard
        Chick on the Publish button

        Expected Result:
        Draft external assignment appears on the calendar dashboard on
        its due date with the word draft before the title
        """
        self.ps.test_updates['name'] = 't1.18.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.007', '8091']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        # assignment_name = 't1.18.007 external-%s' % randint(100, 999)
        assignment_name = "ext007_" + str(randint(0, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='external',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'url': 'website.com',
                                        'status': 'draft'
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
                '//a[contains(@href,"external")]' +
                '//label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        except NoSuchElementException:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH, '//a[@class="calendar-header-control next"]').click()
            self.teacher.find(
                By.XPATH,
                '//a[contains(@href,"external")]' +
                '//label[contains(@data-title,"' + assignment_name + '")]'
            ).click()

        self.teacher.page.wait_for_page_load()
        self.teacher.find(
            By.XPATH, '//button[contains(@class,"-publish")]').click()
        # self.teacher.sleep(50)
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.XPATH,
                 '//div/label[contains(@data-title,"' + assignment_name + '")]'
                 )
            )
        )

        self.ps.test_updates['passed'] = True

    # Case C8092 - 008 - Teacher | Cancel a new external Assignment before
    # making changes using Cancel button
    @pytest.mark.skipif(str(8092) not in TESTS, reason='Excluded')
    def test_teacher_cancel_new_external_before_change_using_cancel_8092(self):
        """Cancel a new external Assignment before changes using Cancel button.

        Steps:
        Click on the Add Assignment drop down menu
        Click on the Add External Assignment option
        Click on the Cancel button

        Expected Result:
        No changes to calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.18.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.008', '8092']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()

        self.teacher.find(
            By.LINK_TEXT, 'Add External Assignment').click()
        self.teacher.sleep(1)
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[text()="Cancel"]')
            )
        ).click()
        assert('month' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard, after caneling assignment 008'

        self.ps.test_updates['passed'] = True

    # Case C8093 - 009 - Teacher | Cancel a new external Assignment after
    # making changes using Cancel button
    @pytest.mark.skipif(str(8093) not in TESTS, reason='Excluded')
    def test_teacher_cancel_new_external_after_changes_using_cancel_8093(self):
        """Cancel a new external Assignment after changes using Cancel button.

        Steps:
        Click on the Add Assignment drop down menu
        Click on the Add External Assignment option
        Enter an Assignment name into the Assignment Name text box
        Click on the Cancel button
        Click on the OK button

        Expected Result:
        No changes to calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.18.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.009', '8093']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()

        self.teacher.find(
            By.LINK_TEXT, 'Add External Assignment').click()
        self.teacher.sleep(1)
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.find(
            By.ID, 'reading-title').send_keys('new_name009')
        self.teacher.find(
            By.XPATH, '//button[text()="Cancel"]'
        ).click()
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"ok")]')
            )
        ).click()

        assert('month' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard, after caneling assignment 009'

        self.ps.test_updates['passed'] = True

    # Case C8094 - 010 - Teacher | Cancel a new external Assignment before
    # making changes using the X
    @pytest.mark.skipif(str(8094) not in TESTS, reason='Excluded')
    def test_teacher_cancel_new_external_before_changes_using_the_x_8094(self):
        """Cancel a new external Assignment before changes using the X.

        Steps:
        Click on the Add Assignment drop down menu
        Click on the Add External Assignment option
        Click on the X

        Expected Result:
        No changes to calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.18.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.010', '8094']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()

        self.teacher.find(
            By.LINK_TEXT, 'Add External Assignment').click()
        self.teacher.sleep(1)
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
            expect.element_to_be_clickable(
                (By.XPATH,
                 '//button[contains(@class,"openstax-close-x")]')
            )
        ).click()
        assert('month' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard, after caneling assignment 010'

        self.ps.test_updates['passed'] = True

    # Case C8095 - 011 - Teacher | Cancel a new external Assignment after
    # making changes using the X
    @pytest.mark.skipif(str(8095) not in TESTS, reason='Excluded')
    def test_teacher_cancel_new_external_after_changes_using_the_x_8095(self):
        """Cancel a new external Assignment after changes using the X.

        Steps:
        Click on the Add Assignment drop down menu
        Click on the Add External Assignment option
        Enter an Assignment name into the Assignment Name text box
        Click on the X
        Click on the OK button

        Expected Result:
        No changes to calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.18.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.011', '8095']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()

        self.teacher.find(
            By.LINK_TEXT, 'Add External Assignment').click()
        self.teacher.sleep(1)
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.find(
            By.ID, 'reading-title').send_keys('new_name011')
        self.teacher.find(
            By.XPATH,
            '//button[contains(@class,"openstax-close-x")]').click()
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"ok")]')
            )
        ).click()

        assert('month' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard, after caneling assignment 011'

        self.ps.test_updates['passed'] = True

    # Case C8096 - 012 - Teacher | Cancel a draft external Assignment before
    # making changes using Cancel button
    @pytest.mark.skipif(str(8096) not in TESTS, reason='Excluded')
    def test_teacher_cancel_draft_external_before_change_use_cancel_8096(self):
        """Cancel draft external Assignment before changes using Cancel button.

        Steps:
        create a draft external Assignment
        Click on the draft external assignment
        Click on the Cancel button

        Expected Result:
        No changes to calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.18.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.012', '8096']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        # create a draft external assignment
        assignment_name = "ext012_" + str(randint(0, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='external',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'url': 'website.com',
                                        'status': 'draft'
                                    })
        # click on draft
        try:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH,
                '//a[contains(@href, "external")]' +
                '//label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        except NoSuchElementException:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH, '//a[@class="calendar-header-control-next"]').click()
            self.teacher.find(
                By.XPATH,
                '//a[contains(@href,"external")]' +
                '//label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        # cancel editing the draft
        self.teacher.sleep(1)
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[text()="Cancel"]')
            )
        ).click()
        assert('month' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard, after caneling assignment 012'

        self.ps.test_updates['passed'] = True

    # Case C8097 - 013 - Teacher | Cancel a draft external assignment after
    # making changes using Cancel button
    @pytest.mark.skipif(str(8097) not in TESTS, reason='Excluded')
    def test_teacher_cancel_draft_external_after_changes_use_cancel_8097(self):
        """Cancel draft external assignment after changes using Cancel button.

        Steps:
        create a draft external assignment
        Click on the draft external assignment
        Enter an Assignment name into the Assignment Name text box
        Click on the Cancel button
        Click on the OK button

        Expected Result:
        No changes to calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.18.013' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.013', '8097']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        # create a draft external assignment
        assignment_name = "ext013_" + str(randint(0, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='external',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'url': 'website.com',
                                        'status': 'draft'
                                    })
        # click on draft
        try:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH,
                '//a[contains(@href,"external")]' +
                '//label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        except NoSuchElementException:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH, '//a[@class="calendar-header-control-next"]').click()
            self.teacher.find(
                By.XPATH,
                '//a[contains(@href,"external")]' +
                '//label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        # edit draft then cancel
        self.teacher.sleep(1)
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.find(
            By.ID, 'reading-title').send_keys('new_name013')
        self.teacher.find(
            By.XPATH, '//button[text()="Cancel"]'
        ).click()
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"ok")]')
            )
        ).click()
        assert('month' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard, after canceling assignment 13'

        self.ps.test_updates['passed'] = True

    # Case C8098 - 014 - Teacher | Cancel a draft external assignment before
    # making changes using the X
    @pytest.mark.skipif(str(8098) not in TESTS, reason='Excluded')
    def test_teacher_cancel_draft_external_before_changes_use_the_x_8098(self):
        """Cancel a draft external Assignment before changes using the X.

        Steps:
        create a draft external Assignment
        Click on the draft external assignment
        Click on the X button
        Click on the OK button

        Expected Result:
        No changes to calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.18.014' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.014', '8098']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "ext014_" + str(randint(0, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='external',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'url': 'website.com',
                                        'status': 'draft'
                                    })
        # click on draft
        try:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH, '//a[contains(@href,"external")]' +
                '//label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        except NoSuchElementException:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH, '//a[@class="calendar-header-control next"]').click()
            self.teacher.find(
                By.XPATH,
                '//a[contains(@href,"external")]' +
                '//label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        # cancel editing the draft
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
            expect.element_to_be_clickable(
                (By.XPATH,
                 '//button[contains(@class,"openstax-close-x")]')
            )
        ).click()
        assert('month' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard, after canceling assignment 14'

        self.ps.test_updates['passed'] = True

    # Case C8099 - 015 - Teacher | Cancel a draft external Assignment after
    # making changes using the X
    @pytest.mark.skipif(str(8099) not in TESTS, reason='Excluded')
    def test_teacher_cancel_draft_external_after_changes_use_the_x_8099(self):
        """Cancel a draft external Assignment after changes using the X.

        Steps:
        create a draft external Assignment
        Click on the draft external assignment
        Enter an Assignment name into the Assignment Name text box
        Click on the Cancel button
        Click on the OK button

        Expected Result:
        No changes to calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.18.015' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.015', '8099']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "ext015_" + str(randint(0, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='external',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'url': 'website.com',
                                        'status': 'draft'
                                    })
        # click on draft
        try:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH,
                '//a[contains(@href,"external")]' +
                '//label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        except NoSuchElementException:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH, '//a[@class="calendar-header-control next"]').click()
            self.teacher.find(
                By.XPATH,
                '//a[contains(@href,"external")]' +
                '//label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        # make change and cancel editing
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.find(
            By.ID, 'reading-title').send_keys('external assignment-015')
        self.teacher.find(
            By.XPATH,
            '//button[contains(@class,"openstax-close-x")]').click()
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"ok")]')
            )
        ).click()
        assert('month' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard, after canceling assignment 15'

        self.ps.test_updates['passed'] = True

    # Case C8100 - 016 - Teacher | Attempt to publish an external assignment
    # with blank required feilds
    @pytest.mark.skipif(str(8100) not in TESTS, reason='Excluded')
    def test_teacher_attempt_to_publish_external_with_blank_reqired_8100(self):
        """Attempt to publish an external with blank required feilds.

        Steps:
        Click on the Add Assignment drop down menu
        Click on the Add External Assignment option
        Click on the Publish button

        Expected Result:
        Blank required feilds are highlighted in red
        Assignment is not published
        """
        self.ps.test_updates['name'] = 't1.18.016' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.016', '8100']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.find(
            By.LINK_TEXT, 'Add External Assignment').click()
        self.teacher.sleep(1)
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.find(
            By.XPATH, '//button[contains(@class,"-publish")]').click()
        assert('external/new' in self.teacher.current_url()), \
            'Not stopped from publishing an external with empty reqired feilds'

        self.ps.test_updates['passed'] = True

    # Case C8101 - 017 - Teacher | Attempt to save a draft external assignment
    # with blank required feilds
    @pytest.mark.skipif(str(8101) not in TESTS, reason='Excluded')
    def test_teacher_attempt_to_save_external_with_blank_reqired_8101(self):
        """Attempt to save external assignment with blank required feilds.

        Steps:
        Click on the Add Assignment drop down menu
        Click on the Add External Assignment option
        Click on the Save As Draft button

        Expected Result:
        Blank required feilds are highlighted in red, Assignment is not saved
        """
        self.ps.test_updates['name'] = 't1.18.017' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.017', '8101']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.find(
            By.LINK_TEXT, 'Add External Assignment').click()
        self.teacher.sleep(1)
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.find(
            By.XPATH, '//button[contains(@class,"-save")]').click()
        assert('external/new' in self.teacher.current_url()), \
            'Not stopped from saving an external with empty reqired feilds'

        self.ps.test_updates['passed'] = True

    # Case C8102 - 018 - Teacher | Delete an unopened external assignment
    @pytest.mark.skipif(str(8102) not in TESTS, reason='Excluded')
    def test_teacher_delete_an_unopened_external_assignment_8102(self):
        """Delete an unopened external Assignment.

        Steps:
        Create an unopened Assignment
        Click on the unopened external assignment
        Click on the Edit Assignment button
        Click on the Delete Assignment
        Click on OK on the dialouge box

        Expected Result:
        Assignment has been removed from the calendar view
        """
        self.ps.test_updates['name'] = 't1.18.018' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.018', '8102']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        # create an unopened assignment
        assignment_name = "ext018_" + str(randint(0, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=2)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='external',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'url': 'website.com',
                                        'status': 'publish'
                                    })
        # click on the unopened assignment
        try:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH,
                '//label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        except NoSuchElementException:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH, '//a[@class="calendar-header-control next"]').click()
            self.teacher.find(
                By.XPATH,
                '//label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        # edit the assignment
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[contains(@class,"edit-assignment")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"delete-link")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[@class="popover-content"]//button[text()="Yes"]')
            )
        ).click()
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

    # Case C8103 - 019 - Teacher | Delete an opened external assignment
    @pytest.mark.skipif(str(8103) not in TESTS, reason='Excluded')
    def test_teacher_delete_an_opened_external_assignment_8103(self):
        """Delete an opened external Assignment.

        Steps:
        Create an opened Assignment
        Click on the opened external assignment
        Click on the Edit Assignment button
        Click on the Delete Assignment
        Click on OK on the dialouge box

        Expected Result:
        Assignment has been removed from the calendar view
        """
        self.ps.test_updates['name'] = 't1.18.019' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.019', '8103']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        # create an opened assignment
        assignment_name = "ext019_" + str(randint(0, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='external',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'url': 'website.com',
                                        'status': 'publish'
                                    })
        # click in the open assignment
        try:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH,
                '//label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        except NoSuchElementException:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH, '//a[@class="calendar-header-control next"]').click()
            self.teacher.find(
                By.XPATH,
                '//label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[contains(@class,"edit-assignment")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"delete-link")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[@class="popover-content"]//button[text()="Yes"]')
            )
        ).click()
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

    # Case C8104 - 020 - Teacher | Delete a draft external assignment
    @pytest.mark.skipif(str(8104) not in TESTS, reason='Excluded')
    def test_teacher_delete_a_draft_external_assignment_8104(self):
        """Delete a draft external Assignment.

        Steps:
        Create a draft Assignment
        Click on the draft
        Click on the Delete Assignment buttom
        Click OK in the dialouge box

        Expected Result:
        Draft assignment is removed from calendar dasboard
        """
        self.ps.test_updates['name'] = 't1.18.020' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.020', '8104']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        # create an opened assignment
        assignment_name = "ext020_" + str(randint(0, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        externals_old = self.teacher.find_all(
            By.XPATH,
            '//label[contains(@data-title,"' + assignment_name + '")]')
        self.teacher.add_assignment(assignment='external',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'url': 'website.com',
                                        'status': 'draft'
                                    })
        # click on the open assignment
        try:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH, '//a[contains(@href,"external")]' +
                '//label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        except NoSuchElementException:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH, '//a[@class="calendar-header-control next"]').click()
            self.teacher.find(
                By.XPATH, '//a[contains(@href,"external")]' +
                '//label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"delete-link")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[@class="popover-content"]//button[text()="Yes"]')
            )
        ).click()
        self.teacher.sleep(2)
        externals = self.teacher.find_all(
            By.XPATH,
            '//label[contains(@data-title,"' + assignment_name + '")]')
        assert(len(externals) == len(externals_old)), \
            'draft external not deleted'

        self.ps.test_updates['passed'] = True

    # Case C8105 - 021 - Teacher | Add a description to an external assignment
    @pytest.mark.skipif(str(8105) not in TESTS, reason='Excluded')
    def test_teacher_add_a_destcription_to_an_external_Assignment_8105(self):
        """Add a description to an external Assignment.

        Steps:
        Click on the Add Assignment drop down menu
        Click on the Add External Assignment option
        Enter an Assignment name into the Assignment Name text box
        Enter a description into the Description text box
        Enter date into the Due Dte text feild as MM/DD/YYYY
        Enter a URL into the Assignment URL text box
        Click on the Publish button

        Expected Result:
        Assignment is on calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.18.021' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.021', '8105']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "ext021_" + str(randint(0, 999))
        assignment = Assignment()
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()

        self.teacher.find(
            By.LINK_TEXT, 'Add External Assignment').click()
        self.teacher.sleep(1)
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
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
            send_keys('external Assignment description')
        today = datetime.date.today()
        opens_on = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        assignment.assign_periods(
            self.teacher.driver, {'all': (opens_on, closes_on)})
        self.teacher.find(
            By.ID, 'external-url').send_keys('website.com')
        self.teacher.find(
            By.XPATH, '//button[contains(@class,"-publish")]').click()
        try:
            self.teacher.find(
                By.XPATH,
                "//label[contains(text(), '" + assignment_name + "')]")
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, '//a[@class="calendar-header-control next"]').click()
            self.teacher.find(
                By.XPATH,
                "//label[contains(text(), '" + assignment_name + "')]")

        self.ps.test_updates['passed'] = True

    # Case C8106 - 022 - Teacher | Change a description for a draft external
    # assignment
    @pytest.mark.skipif(str(8106) not in TESTS, reason='Excluded')
    def test_teacher_change_a_description_for_a_draft_external_8106(self):
        """Change a description for a draft external assignment.

        Steps:
        create a draft Assignment
        Click on the draft assignment
        Enter a new description into the Description text box
        Click on the Save as Draft button

        Expected Result:
        Assignment has been updated on the calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.18.022' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.022', '8106']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        # create an open assignment
        assignment_name = "ext022_" + str(randint(0, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='external',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'url': 'website.com',
                                        'status': 'draft'
                                    })

        # click in the open assignment
        try:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH, '//a[contains(@href,"external")]' +
                '//label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        except NoSuchElementException:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH, '//a[@class="calendar-header-control next"]').click()
            self.teacher.find(
                By.XPATH, '//a[contains(@href,"external")]' +
                '//label[contains(@data-title,"' + assignment_name + '")]'
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
            send_keys('NEW external Assignment description')
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"-save")]')
            )
        ).click()

        self.ps.test_updates['passed'] = True

    # Case C8107 - 023 - Teacher | Change a description for an open external
    # assignment
    @pytest.mark.skipif(str(8107) not in TESTS, reason='Excluded')
    def test_teacher_change_a_destcription_for_an_open_external_8107(self):
        """Change a description for an open external assignment.

        Steps:
        create an open Assignment
        Click on the open assignment
        Click on the Edit Assignment button
        Enter a new description into the Description text box
        Click on the Publish button

        Expected Result:
        Assignment has been updated on the calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.18.023' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.023', '8107']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        # create an open assignment
        assignment_name = "ext023_" + str(randint(0, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='external',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'url': 'website.com',
                                        'status': 'publish'
                                    })
        # click in the open assignment
        try:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH,
                '//label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        except NoSuchElementException:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH, '//a[@class="calendar-header-control next"]').click()
            self.teacher.find(
                By.XPATH,
                '//label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[contains(@class,"edit-assignment")]')
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
            send_keys('NEW external Assignment description')
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"-publish")]')
            )
        ).click()

        self.ps.test_updates['passed'] = True

    # Case C8108 - 024 - Teacher | Add a name to an external assignment
    @pytest.mark.skipif(str(8108) not in TESTS, reason='Excluded')
    def test_teacher_add_a_name_to_an_external_Assignment_8108(self):
        """Add a name to an external assignment.

        Steps:
        Click on the Add Assignment drop down menu
        Click on the Add External Assignment option
        Enter an Assignment name into the Assignment Name text box
        Enter date into the Due Date text feild as MM/DD/YYYY
        Enter a URL into the Assignment URL text box
        Click on the Publish button

        Expected Result:
        New external assignment appears on the calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.18.024' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.024', '8108']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "ext024_" + str(randint(0, 999))
        assignment = Assignment()
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()

        self.teacher.find(
            By.LINK_TEXT, 'Add External Assignment').click()
        self.teacher.sleep(1)
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
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
            send_keys('external Assignment description')
        today = datetime.date.today()
        opens_on = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        assignment.assign_periods(
            self.teacher.driver, {'all': (opens_on, closes_on)})
        self.teacher.find(
            By.ID, 'external-url').send_keys('website.com')
        self.teacher.find(
            By.XPATH, '//button[contains(@class,"-publish")]').click()
        try:
            self.teacher.find(
                By.XPATH,
                "//label[contains(text(), '" + assignment_name + "')]")
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, '//a[@class="calendar-header-control-next"]').click()
            self.teacher.find(
                By.XPATH,
                "//label[contains(text(), '" + assignment_name + "')]")

        self.ps.test_updates['passed'] = True

    # Case C8109 - 025 - Teacher | Change name for a draft external assignment
    @pytest.mark.skipif(str(8109) not in TESTS, reason='Excluded')
    def test_teacher_change_a_name_for_a_draft_external_assignment_8109(self):
        """Change a name for a draft external assignment.

        Steps:
        create a draft
        Click on the draft assignment
        Enter a new assignment name into the assignment name text box
        Click on the Save As Draft button

        Expected Result:
        Draft external assignment appears on the calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.18.025' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.025', '8109']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "ext025_" + str(randint(0, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='external',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'url': 'website.com',
                                        'status': 'draft'
                                    })
        # click on the open assignment
        try:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH, '//a[contains(@href,"external")]' +
                '//label[@data-title="' + assignment_name + '"]').click()
        except NoSuchElementException:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH, '//a[@class="calendar-header-control next"]').click()
            self.teacher.find(
                By.XPATH, '//a[contains(@href,"external")]' +
                '//label[@data-title="' + assignment_name + '"]').click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.find(
            By.ID, 'reading-title').send_keys("NEW")
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"-save")]')
            )
        ).click()
        self.teacher.sleep(2)
        try:
            self.teacher.find(
                By.XPATH, "//label[text()= '" + assignment_name + "NEW']")
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, '//a[@class="calendar-header-control next"]').click()
            self.teacher.find(
                By.XPATH, "//label[text()= 'NEW" + assignment_name + "']")

        self.ps.test_updates['passed'] = True

    # Case C8110 - 026 - Teacher | Change name for an open external assignment
    @pytest.mark.skipif(str(8110) not in TESTS, reason='Excluded')
    def test_teacher_change_a_name_for_an_open_external_assignment_8110(self):
        """Change a name for an open external assignment.

        Steps:
        create an open assignment
        Click on the open assignment on the calendar
        Enter a new assignment name into the assignment name text box
        Click on the Publish button

        Expected Result:
        External assignment appears on the calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.18.026' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.026', '8110']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "ext026_" + str(randint(0, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='external',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'url': 'website.com',
                                        'status': 'publish'
                                    })
        # click in the open assignment
        try:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH,
                '//label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        except NoSuchElementException:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH, '//a[@class="calendar-header-control next"]').click()
            self.teacher.find(
                By.XPATH,
                '//label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[contains(@class,"edit-assignment")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.find(
            By.ID, 'reading-title').send_keys("NEW")
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"-publish")]')
            )
        ).click()
        self.teacher.sleep(3)
        try:
            self.teacher.find(
                By.XPATH,
                "//label[contains(text(), '" + assignment_name + "NEW')]")
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, '//a[@class="calendar-header-control next"]').click()
            self.teacher.find(
                By.XPATH,
                "//label[contains(text(), 'NEW" + assignment_name + "')]")

        self.ps.test_updates['passed'] = True

    # Case C8111 - 027 - Teacher | Add an Assignment URL
    @pytest.mark.skipif(str(8111) not in TESTS, reason='Excluded')
    def test_teacher_add_an_assignment_url_8111(self):
        """Add an assignment URL.

        Steps:
        Click on the Add Assignment drop down menu
        Click on the Add External Assignment option
        Enter an Assignment name into the Assignment Name text box
        Enter date into the Due Date text feild as MM/DD/YYYY
        Enter a URL into the Assignment URL text box
        Click on the Publish button

        Expected Result:
        External assignment appears on the calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.18.027' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.027', '8111']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "ext027_" + str(randint(0, 999))
        assignment = Assignment()
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()

        self.teacher.find(
            By.LINK_TEXT, 'Add External Assignment').click()
        self.teacher.sleep(1)
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
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
            send_keys('external Assignment description')
        today = datetime.date.today()
        opens_on = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        assignment.assign_periods(
            self.teacher.driver, {'all': (opens_on, closes_on)})
        self.teacher.find(
            By.ID, 'external-url').send_keys('website.com')
        self.teacher.find(
            By.XPATH, '//button[contains(@class,"-publish")]').click()
        try:
            self.teacher.find(
                By.XPATH,
                "//label[contains(text(), '" + assignment_name + "')]")
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, '//a[@class="calendar-header-control next"]').click()
            self.teacher.find(
                By.XPATH,
                "//label[contains(text(), '" + assignment_name + "')]")

        self.ps.test_updates['passed'] = True

    # Case C8112 - 028 - Teacher | Change the Assignment URL for a draft
    # external Assignment
    @pytest.mark.skipif(str(8112) not in TESTS, reason='Excluded')
    def test_teacher_change_the_assignment_url_for_a_draft_external_8112(self):
        """Change the Assignment URL for a draft external Assignment.

        Steps:
        create a draft Assignment
        Click on the draft assignment
        Enter a new URL into the assignment URL text box
        Click on the Save As Draft button

        Expected Result:
        Updated external assignment appears on the calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.18.028' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.028', '8112']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "ext026_" + str(randint(0, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(
            assignment='external',
            args={
                'title': assignment_name,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'url': 'website.com',
                'status': 'draft'
            }
        )
        # click in the open assignment
        try:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH, '//a[contains(@href,"external")]' +
                '//label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        except NoSuchElementException:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH, '//a[@class="calendar-header-control next"]').click()
            self.teacher.find(
                By.XPATH, '//a[contains(@href,"external")]' +
                '//label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.find(
            By.ID, 'external-url').send_keys('new_site.com')
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"-save")]')
            )
        ).click()

        self.ps.test_updates['passed'] = True

    # Case C8113 - 029 - Teacher | Info icon shows definitions for status bar
    @pytest.mark.skipif(str(8113) not in TESTS, reason='Excluded')
    def test_teacher_info_icon_shows_definitions_for_the_status_bar_8113(self):
        """Info icon shows definitions for the status bar.

        Steps:
        Create and publish an External Assignment
        Click on the External Assignment
        Click on the info icon

        Expected Result:
        Definitions of the statuses are dispalayed
        """
        self.ps.test_updates['name'] = 't1.18.029' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.029', '8113']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "ext019_" + str(randint(0, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='external',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'url': 'website.com',
                                        'status': 'publish'
                                    })
        # click in the open assignment
        try:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH,
                '//label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        except NoSuchElementException:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH, '//a[@class="calendar-header-control next"]').click()
            self.teacher.find(
                By.XPATH,
                '//label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[contains(@class,"edit-assignment")]')
            )
        ).click()
        self.teacher.find(
            By.XPATH, '//button[contains(@class,"-instructions")]').click()
        self.teacher.find(
            By.CLASS_NAME, 'popover-content')

        self.ps.test_updates['passed'] = True

    # Case C8114 - 030 - Teacher | Change all feilds in an unopened
    # External Assignment
    @pytest.mark.skipif(str(8114) not in TESTS, reason='Excluded')
    def test_teacher_change_all_feilds_in_an_unopened_external_8114(self):
        """Change all feilds in an unopened External Assignment.

        Steps:
        Create an unopened assignment
        Click on the unopoened Assignment on the calendar
        Enter an Assignment name into the Assignment Name text box
        Enter a description into the Description text box
        Enter date into the Open Date text feild as MM/DD/YYYY
        Enter date into the Due Date text feild as MM/DD/YYYY
        Enter a URL into the Assignment URL text box
        Click on the Publish button

        Expected Result:
        Updated assignment is displayed on the calendar
        """
        self.ps.test_updates['name'] = 't1.18.030' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.030', '8114']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        # create draft
        assignment_name = "ext030_" + str(randint(0, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='external',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'url': 'website.com',
                                        'status': 'publish'
                                    })
        # click in the open assignment
        try:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH,
                '//label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        except NoSuchElementException:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH, '//a[@class="calendar-header-control next"]').click()
            self.teacher.find(
                By.XPATH,
                '//label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        # edit draft
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[contains(@class,"edit-assignment")]')
            )
        ).click()
        assignment = Assignment()
        self.teacher.sleep(1)
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
            '[contains(@class,"form-control")]'). \
            send_keys('NEW external Assignment description')
        today = datetime.date.today()
        opens_on = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=9)).strftime('%m/%d/%Y')
        assignment.assign_periods(
            self.teacher.driver, {'all': (opens_on, closes_on)})
        self.teacher.find(
            By.ID, 'external-url').send_keys('new')
        self.teacher.find(
            By.XPATH, '//button[contains(@class,"-publish")]').click()
        try:
            self.teacher.find(
                By.XPATH,
                "//label[contains(text(), '" + assignment_name + "NEW')]")
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, '//a[@class="calendar-header-control next"]').click()
            self.teacher.find(
                By.XPATH,
                "//label[contains(text(), '" + assignment_name + "NEW')]")

        self.ps.test_updates['passed'] = True

    # Case C8115 - 031 - Teacher | Change all feilds in a draft External
    # Assignment
    @pytest.mark.skipif(str(8115) not in TESTS, reason='Excluded')
    def test_teacher_change_all_feilds_in_a_draft_external_8115(self):
        """Change all feilds in a draft External Assignment.

        Steps:
        Create a draft assignment
        Click on the draft Assignment on the calendar
        Enter an Assignment name into the Assignment Name text box
        Enter a description into the Description text box
        Enter date into the Open Date text feild as MM/DD/YYYY
        Enter date into the Due Date text feild as MM/DD/YYYY
        Enter a URL into the Assignment URL text box
        Click on the Save As Draft button

        Expected Result:
        Updated assignment is displayed on the calendar
        """
        self.ps.test_updates['name'] = 't1.18.031' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.031', '8115']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        # create draft
        assignment_name = "ext031_" + str(randint(0, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='external',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'url': 'website.com',
                                        'status': 'draft'
                                    })
        # click in the open assignment
        try:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH, '//a[contains(@href,"external")]' +
                '//label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        except NoSuchElementException:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH, '//a[@class="calendar-header-control next"]').click()
            self.teacher.find(
                By.XPATH, '//a[contains(@href,"external")]' +
                '//label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        # edit draft
        assignment = Assignment()
        self.teacher.sleep(1)
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
            '[contains(@class,"form-control")]'). \
            send_keys('NEW external Assignment description')
        today = datetime.date.today()
        opens_on = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=9)).strftime('%m/%d/%Y')
        assignment.assign_periods(
            self.teacher.driver, {'all': (opens_on, closes_on)})
        self.teacher.find(
            By.ID, 'external-url').send_keys('new')
        self.teacher.find(
            By.XPATH, '//button[contains(@class,"-save")]').click()
        try:
            self.teacher.find(
                By.XPATH,
                "//label[contains(text(), '" + assignment_name + "NEW')]")
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, '//a[@class="calendar-header-control next"]').click()
            self.teacher.find(
                By.XPATH,
                "//label[contains(text(), '" + assignment_name + "NEW')]")

        self.ps.test_updates['passed'] = True

    # Case C8116 - 032 - Teacher | Change all possible feilds in an open
    # External Assignment
    @pytest.mark.skipif(str(8116) not in TESTS, reason='Excluded')
    def test_teacher_change_all_possible_feilds_in_an_open_external_8116(self):
        """Change all possible feilds in an open External Assignment.

        Steps:
        Create an open assignment
        Click on the open Assignment on the calendar
        Enter an Assignment name into the Assignment Name text box
        Enter a description into the Description text box
        Enter date into the Due Date text feild as MM/DD/YYYY
        Click on the Save As Draft button

        Expected Result:
        Updated assignment is displayed on the calendar
        """
        self.ps.test_updates['name'] = 't1.18.032' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.032', '8116']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        # create draft
        assignment_name = "ext032_" + str(randint(0, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='external',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'url': 'website.com',
                                        'status': 'publish'
                                    })
        # click in the open assignment
        try:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH,
                '//label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        except NoSuchElementException:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH, '//a[@class="calendar-header-control next"]').click()
            self.teacher.find(
                By.XPATH,
                '//label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        # edit draft
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[contains(@class,"edit-assignment")]')
            )
        ).click()
        # assignment = Assignment()
        self.teacher.sleep(1)
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
            '[contains(@class,"form-control")]'). \
            send_keys('NEW external Assignment description')
        today = datetime.date.today()
        closes_on = (today + datetime.timedelta(days=9)).strftime('%m/%d/%Y')
        self.teacher.find(
            By.XPATH, '//div[contains(@class,"-due-date")]' +
            '//div[contains(@class,"datepicker__input")]').click()
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
            'and text()="' + (closes_on[3:5]).lstrip('0') + '"]'
        ).click()
        self.teacher.sleep(0.5)
        self.teacher.find(
            By.CLASS_NAME, 'assign-to-label').click()
        self.teacher.find(
            By.XPATH, '//button[contains(@class,"-publish")]').click()
        try:
            self.teacher.find(
                By.XPATH,
                "//label[contains(text(), '" + assignment_name + "NEW')]")
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, '//a[@class="calendar-header-control next"]').click()
            self.teacher.find(
                By.XPATH,
                "//label[contains(text(), '" + assignment_name + "NEW')]")

        self.ps.test_updates['passed'] = True

    # Case C111248 - 033 - Teacher | Add an external assignment by dragging Add
    # External Assignment to calendar date
    @pytest.mark.skipif(str(111248) not in TESTS, reason='Excluded')
    def test_teacher_add_external_assignment_by_dragging_add_exte_111248(self):
        """Add an external assignment by dragging to calendar date.

        Steps:
        Click on the Add Assignment Menu
        Click and drag "Add External Assignment" to desired due date

        Expected Result:
        User taken to Add External Assignment page with due date filled in
        """
        self.ps.test_updates['name'] = 't1.14.033' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.14', 't1.14.033', '111248']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        add_external_bar = self.teacher.find(
            By.LINK_TEXT, 'Add External Assignment')
        calendar_date = self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//div[contains(@class,"Day--upcoming")]')
            )
        )
        self.teacher.driver.execute_script(
            'return arguments[0].scrollIntoView();', add_external_bar)
        self.teacher.sleep(1)
        actions = ActionChains(self.teacher.driver)
        actions.drag_and_drop(add_external_bar, calendar_date)
        actions.perform()
        self.teacher.sleep(3)
        assert('external/new' in self.teacher.current_url()),\
            'not at Add External Assignment page'

        self.ps.test_updates['passed'] = True
