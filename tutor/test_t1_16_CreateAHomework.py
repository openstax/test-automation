"""Tutor v1, Epic 16 - Create A Homework."""

import inspect
import json
import os
import pytest
import unittest
import datetime

from pastasauce import PastaSauce, PastaDecorator
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from staxing.helper import Teacher  # , Student
from staxing.assignment import Assignment

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
        8028, 8029, 8030, 8031, 8032,
        8033, 8034, 8035, 8036, 8037,
        8038, 8039, 8040, 8041, 8042,
        8043, 8044, 8045, 8046, 8047,
        8048, 8049, 8050, 8051, 8052,
        8053, 8054, 8055, 8056, 8057,
        8058, 8059, 8060, 8061, 8062,
        8063, 8064, 8065, 8066, 8067,
        8068, 8069, 8070, 8071, 8072,
        8073, 8074, 8075, 8076, 8077,
        8078, 8080, 8081, 8082, 8083,
        8084, 111247

        # 8075, 8076, 8077, 8078, 8080, 8081, 111247 - not working

    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestCreateAHomework(unittest.TestCase):
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

    # Case C8028 - 001 - Teacher | Add a homework using the Add Assignment menu
    @pytest.mark.skipif(str(8028) not in TESTS, reason='Excluded')
    def test_teacher_add_homework_using_add_assignment_drop_menu_8028(self):
        """Add a homework using the Add Assignment drop down menu.

        Steps:
        Click on the Add Assignment drop down menu on the user dashboard
        Click on the 'Add Homework' button

        Expected Result:
        The teacher is taken to the page where they create the assignment.
        """
        self.ps.test_updates['name'] = 't1.16.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.001', '8028']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        assert('homework/new' in self.teacher.current_url()), \
            'Not on the add a homework page'

        self.teacher.sleep(5)

        self.ps.test_updates['passed'] = True

    # Case C8029 - 002 - Teacher | Add a homework using the calendar date
    @pytest.mark.skipif(str(8029) not in TESTS, reason='Excluded')
    def test_teacher_add_a_homework_using_the_calendar_date_8029(self):
        """Add a homework using the calendar date.

        Steps:
        Click on a date at least one day later than current date on calendar
        From the menu that appears, click on 'Add Homework'

        Expected Result:
        The teacher is taken to a page where they create the assignment.
        """
        self.ps.test_updates['name'] = 't1.16.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.002', '8028']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        calendar_date = self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//div[contains(@class,"Day--upcoming")]')
            )
        )
        self.teacher.driver.execute_script(
            'return arguments[0].scrollIntoView();', calendar_date)
        self.teacher.driver.execute_script('window.scrollBy(0, -80);')
        self.teacher.sleep(2)
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(calendar_date)
        actions.move_by_offset(0, -35)
        actions.click()
        actions.move_by_offset(30, 45)
        actions.click()
        actions.perform()
        assert('homework/new' in self.teacher.current_url()),\
            'not at Add Homework page'

        self.ps.test_updates['passed'] = True

    # Case C8030 - 003 - Teacher | Set open/due dates for periods collectively
    @pytest.mark.skipif(str(8030) not in TESTS, reason='Excluded')
    def test_teacher_set_open_and_due_date_for_periods_collectively_8030(self):
        """Set open and due dates for all periods collectively.

        Steps:
        Click on the Add Assignment drop down menu on the user dashboard, OR
        Click a calendar date that is at least one day later than current date
        Click on the 'Add Homework' button
        Select the 'All Periods' radio button if it is not selected by default
        Select an open date for the assignment using the calendar element
        Select a due date for the assignment using the calendar element

        Expected Result:
        A due date is assigned for all periods collectively.
        """
        self.ps.test_updates['name'] = 't1.16.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.003', '8030']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
            )
        )
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        assert('homework/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        # set close date
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
        self.teacher.sleep(0.5)
        # set open date
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
        self.teacher.sleep(3)

        new_close = self.teacher.driver.find_element(
            By.XPATH,
            "//div[contains(@class, 'due-date')]" +
            "//input[@type='text' and @value]"
        ).get_attribute("value")
        new_open = self.teacher.driver.find_element(
            By.XPATH,
            "//div[contains(@class, 'open-date')]" +
            "//input[@type='text' and @value]"
        ).get_attribute("value")

        assert(new_close == closes_on), "start date not set"
        assert(new_open == opens_on), "start date not set"

        self.ps.test_updates['passed'] = True

    # Case C8031 - 004 - Teacher | Set open and due dates periods individually
    @pytest.mark.skipif(str(8031) not in TESTS, reason='Excluded')
    def test_teacher_set_open_and_due_date_for_periods_individually_8031(self):
        """Set open and due dates for all periods individually.

        Steps:
        Click on the Add Assignment drop down menu on the user dashboard, OR
        click a calendar date that's at least one day later than current date
        Click on the 'Add Homework' button
        Select the 'Individual Periods' radio button
        Select the periods that should be required to complete the assignment
        Select open and due dates for each section using the calendar element

        Expected Result:
        Each section that is assigned the homework has an individual open and
        due date.
        """
        self.ps.test_updates['name'] = 't1.16.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.004', '8031']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        assert('homework/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        # assign for each period individually
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
            new_close = self.teacher.driver.find_element(
                By.XPATH,
                "//div[contains(@class,'tasking-plan')][%s]" % (x + 1) +
                "//div[contains(@class, 'due-date')]" +
                "//input[@type='text' and @value]"
            ).get_attribute("value")
            new_open = self.teacher.driver.find_element(
                By.XPATH,
                "//div[contains(@class,'tasking-plan')][%s]" % (x + 1) +
                "//div[contains(@class, 'open-date')]" +
                "//input[@type='text' and @value]"
            ).get_attribute("value")
            assert(new_close == closes_on), "start date not set"
            assert(new_open == opens_on), "start date not set"

        self.ps.test_updates['passed'] = True

    # Case C8032 - 005 - Teacher | Save a draft homework
    @pytest.mark.skipif(str(8032) not in TESTS, reason='Excluded')
    def test_teacher_save_a_draft_homework_8032(self):
        """Save a draft homework.

        Steps:
        Click on the 'Add Assignment' button, OR
        Click on a calendar date at least one day later than the current date
        From the drop down menu, click on the 'Add Homework' option
        Enter a name in the 'Assignment name' text box
        Choose a due date for the assignment using the calendar element
        Click the '+ Select Problems' button
        Select at least one chapter or section to assign problems from
        Click the 'Show problems' button
        Click on at least one problem to be used for My Selections
        Click the 'Next' button
        Click 'Save As Draft'

        Expected Result:
        The teacher is returned to the dashboard where the draft assignment is
        now displayed on the calendar.
        """
        self.ps.test_updates['name'] = 't1.16.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.005', '8032']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "hw006_" + str(randint(0, 999))
        assignment = Assignment()
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        self.teacher.sleep(1)
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
            send_keys('homework Assignment description')
        today = datetime.date.today()
        opens_on = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        assignment.assign_periods(
            self.teacher.driver, {'all': (opens_on, closes_on)})
        assignment.add_homework_problems(
            self.teacher.driver, {'1.1': (2, 3), })
        self.teacher.sleep(1)
        element = self.teacher.find(
            By.XPATH, '//button[contains(@class,"-save")]')
        Assignment.scroll_to(self.teacher.driver, element)
        element.click()
        self.teacher.sleep(4)
        try:
            self.teacher.find(
                By.XPATH,
                "//a/label[contains(text(), '" + assignment_name + "')]")
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH, '//a[@class="calendar-header-control next"]').click()
            self.teacher.find(
                By.XPATH,
                "//a/label[contains(text(), '" + assignment_name + "')]")
        self.ps.test_updates['passed'] = True

    # Case C8033 - 006 - Teacher | Publish a new homework
    @pytest.mark.skipif(str(8033) not in TESTS, reason='Excluded')
    def test_teacher_publish_a_new_homework_8033(self):
        """Publish a new homework.

        Steps:
        Click on the Add Assignment drop down menu on the user dashboard, OR
        click on a calendar date at least one day later than the current date
        Click on the 'Add Homework' button
        Give the homework a name in the 'Assignment name' text box
        Select a due date (individually or collectively) for the assignment
            using the calendar element
        Click the '+ Select Problems' button
        Select at least one chapter or section to use for the homework
        Click the 'Show Problems' button
        Click at least one problem to be used for My Selections
        Click the 'Next' button
        Click the 'Publish' button

        Expected Result:
        The teacher is returned to dashboard where new assignment is displayed.
        """
        self.ps.test_updates['name'] = 't1.16.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.006', '8033']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "hw006_" + str(randint(0, 999))
        assignment = Assignment()
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        self.teacher.sleep(1)
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
            send_keys('homework Assignment description')
        today = datetime.date.today()
        opens_on = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        assignment.assign_periods(
            self.teacher.driver, {'all': (opens_on, closes_on)})
        assignment.add_homework_problems(
            self.teacher.driver, {'1.1': (2, 3), })
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

    # Case C8034 - 007 - Teacher | Publish a draft homework
    @pytest.mark.skipif(str(8034) not in TESTS, reason='Excluded')
    def test_teacher_publish_a_draft_homework_8034(self):
        """Publish a draft homework.

        Steps:
        From the user dashboard, click on a draft assignment
        Click the 'Publish' button

        Expected Result:
        A draft homework is published.
        """
        self.ps.test_updates['name'] = 't1.16.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.007', '8034']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "hw007_" + str(randint(0, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='homework',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'problems': {'1.1': (2, 3), },
                                        'status': 'draft',
                                        'feedback': 'immediate'
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
                '//a[contains(@href,"homework")]' +
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
                '//a[contains(@href,"homework")]' +
                '//label[contains(@data-title,"' + assignment_name + '")]'
            ).click()

        self.teacher.page.wait_for_page_load()
        self.teacher.find(
            By.XPATH, '//button[contains(@class,"-publish")]').click()
        self.teacher.sleep(4)
        try:
            self.teacher.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="month-wrapper"]')
                )
            )
            self.teacher.find(
                By.XPATH,
                '//div/label[contains(@data-title,"' + assignment_name + '")]'
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
                '//div/label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        assert('/plan/' in self.teacher.current_url()), \
            'assignment did not publish'
        self.teacher.sleep(4)
        self.ps.test_updates['passed'] = True

    # Case C8035 - 008 - Teacher | Cancel a new homework before making any
    # changes using the Cancel button
    @pytest.mark.skipif(str(8035) not in TESTS, reason='Excluded')
    def test_teacher_cancel_new_hw_before_change_using_cancel_btn_8035(self):
        """Cancel new homework before making changes using the Cancel button.

        Steps:
        Click on the Add Assignment drop down menu on the user dashboard, OR
            click on a calendar date at least one day later than the current
            date
        Click on the 'Add Homework' button
        Click on the 'Cancel' button

        Expected Result:
        The teacher is returned to the dashboard.
        """
        self.ps.test_updates['name'] = 't1.16.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.008', '8035']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        assert('homework/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH,
                 '//button[text()="Cancel"]')
            )
        ).click()
        assert('month' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard, after caneling assignment 008'

        self.ps.test_updates['passed'] = True

    # Case C8036 - 009 - Teacher | Cancel new hw after any changes w/Cancel
    @pytest.mark.skipif(str(8036) not in TESTS, reason='Excluded')
    def test_teacher_cancel_hw_after_making_changes_with_cancel_btn_8036(self):
        """Cancel a homework after making any changes using the Cancel button.

        Steps:
        Click on the Add Assignment drop down menu on the user dashboard, OR
        click on a calendar date at least one day later than the current date
        Click on the 'Add Homework' button
        Give the homework a name in the 'Assignment name' text box
        Select a due date (individually or collectively) for the assignment
            using the calendar element
        Click the '+ Select Problems' button
        Select at least one chapter or section to use for the homework
        Click the 'Show Problems' button
        Click at least one problem to be used for My Selections
        Click the 'Next' button
        Click the 'Cancel' button
        Click the 'OK' button

        Expected Result:
        The tracher is returned to the dashboard.
        """
        self.ps.test_updates['name'] = 't1.16.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.009', '8036']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        assert('homework/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.find(
            By.ID, 'reading-title').send_keys('new_name008')
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH,
                 '//button[text()="Cancel"]')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[text()="Yes"]')
            )
        ).click()
        assert('month' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard, after caneling assignment 008'

        self.ps.test_updates['passed'] = True

    # Case C8037 - 010 - Teacher | Cancel hw before making changes using the X
    @pytest.mark.skipif(str(8037) not in TESTS, reason='Excluded')
    def test_teacher_cancel_hw_before_making_any_changes_using_x_8037(self):
        """Cancel a new homework before making any changes using the X.

        Steps:
        Click on the Add Assignment drop down menu on the user dashboard, OR
        click on a calendar date at least one day later than the current date
        Click on the 'Add Homework' button
        Click on the X button

        Expected Result:
        The teacher is returned to the dashboard.
        """
        self.ps.test_updates['name'] = 't1.16.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.010', '8037']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        assert('homework/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH,
                 '//button[contains(@class,"openstax-close-x")]')
            )
        ).click()
        assert('month' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard, after caneling assignment 009'

        self.ps.test_updates['passed'] = True

    # Case C8038 - 011 - Teacher | Cancel a homework after making changes w/ X
    @pytest.mark.skipif(str(8038) not in TESTS, reason='Excluded')
    def test_teacher_canecel_hw_after_making_any_changes_using_x_8038(self):
        """Cancel a new homework after making any changes using the X.

        Steps:
        Click on the Add Assignment drop down menu on the user dashboard, OR
        click on a calendar date at least one day later than the current date
        Click on the 'Add Homework' button
        Give the homework a name in the 'Assignment name' text box
        Select a due date (individually or collectively) for the assignment
            using the calendar element
        Click the '+ Select Problems' button
        Select at least one chapter or section to use for the homework
        Click the 'Show Problems' button
        Click at least one problem to be used for My Selections
        Click the 'Next' button
        Click the X button
        Click the 'OK' button

        Expected Result:
        The teacher is returned to the dashboard.
        """
        self.ps.test_updates['name'] = 't1.16.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.011', '8038']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        assert('homework/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.find(
            By.ID, 'reading-title').send_keys('new_name008')
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH,
                 '//button[contains(@class,"openstax-close-x")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[text()="Yes"]')
            )
        ).click()
        assert('month' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard, after caneling assignment 010'

        self.ps.test_updates['passed'] = True

    # Case C8039 - 012 - Teacher | Cancel a draft homework before making any
    # changes using the Cancel button
    @pytest.mark.skipif(str(8039) not in TESTS, reason='Excluded')
    def test_teacher_cancel_draft_hw_before_making_changes_w_cancel_8039(self):
        """Cancel a draft hw before making changes using the Cancel button.

        Steps:
        From the user dashboard, click on a draft assignment
        Click on the 'Cancel' button
        Click on the 'OK' button

        Expected Result:
        The teacher is returned to the dashboard.
        """
        self.ps.test_updates['name'] = 't1.16.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.012', '8039']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "hw012_" + str(randint(0, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='homework',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'problems': {'1.1': (2, 3), },
                                        'status': 'draft',
                                        'feedback': 'immediate'
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
                '//a[contains(@href,"homework")]' +
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
                '//a[contains(@href,"homework")]' +
                '//label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH,
                 '//button[text()="Cancel"]')
            )
        ).click()
        assert('month' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard, after caneling assignment 012'
        self.ps.test_updates['passed'] = True

    # Case C8040 - 013 - Teacher | Cancel a draft homework after making
    # changes using the Cancel button
    @pytest.mark.skipif(str(8040) not in TESTS, reason='Excluded')
    def test_teacher_cancel_draft_hw_after_making_changes_w_cancel_8040(self):
        """Cancel a draft homework after making changes using Cancel button.

        Steps:
        From the user dashboard, click on a draft assignment
        Change the homework name in the 'Assignment name' text box
        Click on the 'Cancel' button
        Click on the 'OK' button

        Expected Result:
        The teacher is returned to the dashboard.
        """
        self.ps.test_updates['name'] = 't1.16.013' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.013', '8040']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "hw013_" + str(randint(0, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='homework',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'problems': {'1.1': (2, 3), },
                                        'status': 'draft',
                                        'feedback': 'immediate'
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
                '//a[contains(@href,"homework")]' +
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
                '//a[contains(@href,"homework")]' +
                '//label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.find(
            By.ID, 'reading-title').send_keys(assignment_name)
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH,
                 '//button[text()="Cancel"]')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[text()="Yes"]')
            )
        ).click()
        assert('month' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard, after caneling assignment 013'
        self.ps.test_updates['passed'] = True

    # Case C8041 - 014 - Teacher | Cancel a draft hw before changes using the X
    @pytest.mark.skipif(str(8041) not in TESTS, reason='Excluded')
    def test_teacher_cancel_draft_hw_before_making_changes_using_x_8041(self):
        """Cancel a draft homework before making any changes using the X.

        Steps:
        From the user dashboard, click on a draft assignment
        Click on the X button
        Click on the 'OK' button

        Expected Result:
        The teacher is returned to the dashboard.
        """
        self.ps.test_updates['name'] = 't1.16.014' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.014', '8041']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "hw014_" + str(randint(0, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='homework',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'problems': {'1.1': (2, 3), },
                                        'status': 'draft',
                                        'feedback': 'immediate'
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
                '//a[contains(@href,"homework")]' +
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
                '//a[contains(@href,"homework")]' +
                '//label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        self.teacher.sleep(1)
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH,
                 '//button[contains(@class,"openstax-close-x")]')
            )
        ).click()
        assert('month' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard, after caneling assignment 014'
        self.ps.test_updates['passed'] = True

    # Case C8042 - 015 - Teacher | Cancel a draft homework after making
    # changes using the X
    @pytest.mark.skipif(str(8042) not in TESTS, reason='Excluded')
    def test_teacher_cancel_a_draft_hw_after_making_changes_using_x_8042(self):
        """Cancel a draft homework after making changes using the X.

        Steps:
        From the user dashboard, click on a draft assignment
        Change the homework name in the 'Assignment name' text box
        Edit the homework's name in the 'Assignment name' text box
        Click on the X button
        Click on the 'OK' button

        Expected Result:
        The teacher is returned to the dashboard.
        """
        self.ps.test_updates['name'] = 't1.16.015' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.015', '8042']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "hw015_" + str(randint(0, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='homework',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'problems': {'1.1': (2, 3), },
                                        'status': 'draft',
                                        'feedback': 'immediate'
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
                '//a[contains(@href,"homework")]' +
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
                '//a[contains(@href,"homework")]' +
                '//label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.find(
            By.ID, 'reading-title').send_keys(assignment_name)
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH,
                 '//button[contains(@class,"openstax-close-x")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[text()="Yes"]')
            )
        ).click()
        assert('month' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard, after caneling assignment 015'
        self.ps.test_updates['passed'] = True

    # Case C8043 - 016 - Teacher | Attempt to publish a homework with blank
    # required fields
    @pytest.mark.skipif(str(8043) not in TESTS, reason='Excluded')
    def test_teacher_attempt_to_publish_homework_with_blank_fields_8043(self):
        """Attempt to publish a homework with blank required fields.

        Steps:
        Click on the Add Assignment drop down menu on the user dashboard, OR
        click on a calendar date at least one day later than the current date
        Click on the 'Add Homework' button
        Click on the 'Publish' button

        Expected Result:
        Red text appears next to every blank required field.
        """
        self.ps.test_updates['name'] = 't1.16.016' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.016', '8043']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        assert('homework/new' in self.teacher.current_url()), \
            'Not on the add a homework page'

        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.find(
            By.XPATH, '//button[contains(@class,"-publish")]').click()
        assert('homework/new' in self.teacher.current_url()), \
            'Not stopped from publishing an external with empty reqired feilds'

        self.ps.test_updates['passed'] = True

    # Case C8044 - 017 - Teacher | Attempt to save a draft homework with blank
    # required fields
    @pytest.mark.skipif(str(8044) not in TESTS, reason='Excluded')
    def test_teacher_attempt_to_save_draft_hw_with_blank_fields_8044(self):
        """Attempt to save a draft homework with blank required fields.

        Steps:
        Click on the Add Assignment drop down menu on the user dashboard, OR
        Click on a calendar date at least one day later than the current date
        Click on the 'Add Homework' button
        Click on the 'Save As Draft' button

        Expected Result:
        Red text appears next to every blank required field.
        """
        self.ps.test_updates['name'] = 't1.16.017' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.017', '8044']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        assert('homework/new' in self.teacher.current_url()), \
            'Not on the add a homework page'

        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.find(
            By.XPATH, '//button[contains(@class,"-save")]').click()
        assert('homework/new' in self.teacher.current_url()), \
            'Not stopped from saving an external with empty reqired feilds'

        self.ps.test_updates['passed'] = True

    # Case C8045 - 018 - Teacher | Delete an unpoened homework
    @pytest.mark.skipif(str(8045) not in TESTS, reason='Excluded')
    def test_teacher_delete_an_unopened_homework_8045(self):
        """Delete an unopened homework.

        Steps:
        Click on published assignment that hasn't yet been opened for students
        Click on the 'Edit Assignment' button
        Click on the 'Delete Assignment' button
        Click 'Yes' on the dialog box that pops up

        Expected Result:
        The teacher is returned to the dashboard and the assignment is removed
        from the calendar.
        """
        self.ps.test_updates['name'] = 't1.16.018' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.018', '8045']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "hw018_" + str(randint(0, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=2)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=4)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='homework',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'problems': {'1.1': (2, 3), },
                                        'status': 'publish',
                                        'feedback': 'immediate'
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
                '//div/label[contains(@data-title,"' + assignment_name + '")]'
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
                '//div/label[contains(@data-title,"' + assignment_name + '")]'
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
        self.teacher.sleep(1)
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(text(),"Yes")]')
            )
        ).click()
        self.teacher.sleep(1)
        assert('month' in self.teacher.current_url()),\
            'not back at calendar after deleting an event'
        self.teacher.driver.get(self.teacher.current_url())
        self.teacher.page.wait_for_page_load()
        events_new = self.teacher.driver.find_elements(
            By.XPATH, '//label[contains(@data-title,"'+assignment_name+'")]')
        assert(len(events_new) == 0),\
            'unopen event not deleted'
        self.ps.test_updates['passed'] = True

    # Case C8046 - 019 - Teacher | Delete an open homework
    @pytest.mark.skipif(str(8046) not in TESTS, reason='Excluded')
    def test_teacher_delete_an_open_homework_8046(self):
        """ Delete an open homework.

        Steps:
        Click on published assignment that has been opened for students
        Click on the 'Edit Assignment' button
        Click on the 'Delete Assignment' button
        Click 'Yes' on the dialog box that pops up

        Expected Result:
        The teacher is returned to the dashboard and the assignment is removed
        from the calendar.
        """
        self.ps.test_updates['name'] = 't1.16.019' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.019', '8046']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "hw019_" + str(randint(0, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=4)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='homework',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'problems': {'1.1': (2, 3), },
                                        'status': 'publish',
                                        'feedback': 'immediate'
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
                '//div/label[contains(@data-title,"' + assignment_name + '")]'
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
                '//div/label[contains(@data-title,"' + assignment_name + '")]'
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
        self.teacher.sleep(1)
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(text(),"Yes")]')
            )
        ).click()
        self.teacher.sleep(1)
        assert('month' in self.teacher.current_url()),\
            'not back at calendar after deleting an event'
        self.teacher.driver.get(self.teacher.current_url())
        self.teacher.page.wait_for_page_load()
        events_new = self.teacher.driver.find_elements(
            By.XPATH, '//label[contains(@data-title,"'+assignment_name+'")]')
        assert(len(events_new) == 0),\
            'unopen event not deleted'
        self.ps.test_updates['passed'] = True

    # Case C8047 - 020 - Teacher | Delete a draft homework
    @pytest.mark.skipif(str(8047) not in TESTS, reason='Excluded')
    def test_teacher_delete_a_draft_homework_8047(self):
        """Delete a draft homework.

        Steps:
        Click on a draft assignment on the calendar
        Click on the 'Delete Assignment' button
        Click 'Yes' on the dialog box that appears

        Expected Result:
        The teacher is returned to the dashboard and the draft assignment is
        removed from the calendar.
        """
        self.ps.test_updates['name'] = 't1.16.020' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.020', '8047']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "hw020_" + str(randint(0, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=4)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='homework',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'problems': {'1.1': (2, 3), },
                                        'status': 'draft',
                                        'feedback': 'immediate'
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
                '//a/label[contains(@data-title,"' + assignment_name + '")]'
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
                '//a/label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"delete-link")]')
            )
        ).click()
        self.teacher.sleep(1)
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(text(),"Yes")]')
            )
        ).click()
        self.teacher.sleep(1)
        assert('month' in self.teacher.current_url()),\
            'not back at calendar after deleting an event'
        self.teacher.driver.get(self.teacher.current_url())
        self.teacher.page.wait_for_page_load()
        events_new = self.teacher.driver.find_elements(
            By.XPATH, '//label[contains(@data-title,"'+assignment_name+'")]')
        assert(len(events_new) == 0),\
            'unopen event not deleted'
        self.ps.test_updates['passed'] = True

    # Case C8048 - 021 - Teacher | Add a description to a homework
    @pytest.mark.skipif(str(8048) not in TESTS, reason='Excluded')
    def test_teacher_add_a_description_to_the_homework_8048(self):
        """Add a description to a homework.

        Steps:
        From the dashboard, click on the 'Add assignment' drop down menu
        Click on the 'Add Homework' button
        Edit the text box named 'Description or special instructions'

        Expected Result:
        Text is visible in the 'Description or special instructions' text box.
        """
        self.ps.test_updates['name'] = 't1.16.021' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.021', '8048']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        assert('homework/new' in self.teacher.current_url()), \
            'Not on the add a homework page'

        self.teacher.find(
            By.XPATH, "//textarea[contains(@class,'form-control')]"
        ).send_keys('test description')
        self.teacher.sleep(1)
        text = self.teacher.find(
            By.XPATH, "//textarea[contains(@class,'form-control')]"
        ).text
        assert(text == "test description"), "description not added"

        self.ps.test_updates['passed'] = True

    # Case C8049 - 022 - Teacher | Change a description for a draft homework
    @pytest.mark.skipif(str(8049) not in TESTS, reason='Excluded')
    def test_teacher_change_a_description_for_a_draft_homework_8049(self):
        """Change a description for a draft homework.

        Steps:
        From the dashboard, click on a draft assignment displayed on the
            calendar
        Edit the text box labeled 'Description or special instructions'
        Click on the 'Save As Draft' button

        Expected Result:
        The teacher is returned to the dashboard. The draft assignment's
        description has changed.
        """
        self.ps.test_updates['name'] = 't1.16.022' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.022', '8049']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "hw022_" + str(randint(0, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=4)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='homework',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'problems': {'1.1': (2, 3), },
                                        'status': 'draft',
                                        'feedback': 'immediate'
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
                '//a/label[contains(@data-title,"' + assignment_name + '")]'
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
                '//a/label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        self.teacher.sleep(1)
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.XPATH,
                 '//textarea[contains(@class,"form-control")]')
            )
        ).send_keys("-edit")
        text = self.teacher.find(
            By.XPATH, "//textarea[contains(@class,'form-control')]"
        ).text
        assert("-edit" in text), "description not added"

        self.ps.test_updates['passed'] = True

    # Case C8050 - 023 - Teacher | Change a description for an open homework
    @pytest.mark.skipif(str(8050) not in TESTS, reason='Excluded')
    def test_teacher_change_a_description_for_an_open_homework_8050(self):
        """Change a description for an open homework.

        Steps:
        From the dashboard, click on an open assignment displayed on calendar
        Click the 'Edit Assignment' button
        Edit the text box labeled 'Description or special instructions'
        Click on the 'Publish' button

        Expected Result:
        The teacher is returned to the dashboard.
        The open assignment's description has changed.
        """
        self.ps.test_updates['name'] = 't1.16.023' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.023', '8050']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "hw023_" + str(randint(0, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=4)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='homework',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'problems': {'1.1': (2, 3), },
                                        'status': 'publish',
                                        'feedback': 'immediate'
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
                '//div/label[contains(@data-title,"' + assignment_name + '")]'
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
                '//div/label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[contains(@class,"edit-assignment")]')
            )
        ).click()
        self.teacher.sleep(1)
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.XPATH,
                 '//textarea[contains(@class,"form-control")]')
            )
        ).send_keys("-edit")
        text = self.teacher.find(
            By.XPATH, "//textarea[contains(@class,'form-control')]"
        ).text
        assert("-edit" in text), "description not added"
        self.ps.test_updates['passed'] = True

    # Case C8051 - 024 - Teacher | Add a name to a homework
    @pytest.mark.skipif(str(8051) not in TESTS, reason='Excluded')
    def test_teacher_add_a_name_to_a_homework_8051(self):
        """Add a name to a homework.

        Steps:
        From the dashboard, click on the 'Add assignment' drop down menu
        Click on the 'Add Homework' button
        Edit the text box named 'Assignment name'

        Expected Result:
        Text is visible in the 'Assignment name' text box.
        """
        self.ps.test_updates['name'] = 't1.16.024' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.024', '8051']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        assert('homework/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.XPATH,
                 "//input[@id='reading-title']")
            )
        ).send_keys("test name")
        self.teacher.sleep(1)
        text = self.teacher.find(
            By.XPATH, "//input[@id='reading-title']"
        ).get_attribute("value")
        assert("test name" in text), "name not added"

        self.ps.test_updates['passed'] = True

    # Case C8052 - 025 - Teacher | Change a name for a draft homework
    @pytest.mark.skipif(str(8052) not in TESTS, reason='Excluded')
    def test_teacher_change_a_name_for_a_draft_homework_8052(self):
        """Change a name for a draft homework.

        Steps:
        From the dashboard, click on a draft assignment displayed on calendar
        Edit the text box labeled 'Assignment name'
        Click on the 'Save As Draft' button
        Expected Result:
        The teacher is returned to the dashboard.
        The draft assignment's name has changed.
        """
        self.ps.test_updates['name'] = 't1.16.025' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.025', '8052']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "hw025_" + str(randint(0, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=4)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='homework',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'problems': {'1.1': (2, 3), },
                                        'status': 'draft',
                                        'feedback': 'immediate'
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
                '//a/label[contains(@data-title,"' + assignment_name + '")]'
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
                '//a/label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        self.teacher.sleep(1)
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.XPATH,
                 "//input[@id='reading-title']")
            )
        ).send_keys("-edit")
        self.teacher.sleep(1)
        text = self.teacher.find(
            By.XPATH, "//input[@id='reading-title']"
        ).get_attribute("value")
        assert("-edit" in text), "description not added"
        self.ps.test_updates['passed'] = True

    # Case C8053 - 026 - Teacher | Change a name for an open homework
    @pytest.mark.skipif(str(8053) not in TESTS, reason='Excluded')
    def test_teacher_change_a_name_for_an_open_homework_8053(self):
        """Change a name for an open homework.

        Steps:
        From the dashboard, click on an open assignment displayed on calendar
        Click the 'Edit Assignment' button
        Edit the text box labeled 'Assignment name'
        Click on the 'Publish' button

        Expected Result:
        The name of an open homework is changed
        """
        self.ps.test_updates['name'] = 't1.16.026' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.026', '8053']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "hw026_" + str(randint(0, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=4)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='homework',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'problems': {'1.1': (2, 3), },
                                        'status': 'publish',
                                        'feedback': 'immediate'
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
                '//div/label[contains(@data-title,"' + assignment_name + '")]'
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
                '//div/label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[contains(@class,"edit-assignment")]')
            )
        ).click()
        self.teacher.sleep(1)
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.XPATH,
                 "//input[@id='reading-title']")
            )
        ).send_keys("-edit")
        self.teacher.sleep(1)
        text = self.teacher.find(
            By.XPATH, "//input[@id='reading-title']"
        ).get_attribute("value")
        assert("-edit" in text), "description not added"
        self.ps.test_updates['passed'] = True

    # Case C8054 - 027 - Teacher | Select when to show feedback to a student
    @pytest.mark.skipif(str(8054) not in TESTS, reason='Excluded')
    def test_teacher_select_when_to_show_feedback_to_a_student_8054(self):
        """Select when to show feedback to a student.

        Steps:
        From the dashboard, click on the 'Add assignment' drop down menu
        Click on the 'Add Homework' button
        Select an option on the 'Show feedback' drop down menu

        Expected Result:
        The option chosen is shown on the drop down menu.
        """
        self.ps.test_updates['name'] = 't1.16.027' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.027', '8054']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        assert('homework/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.ID, "feedback-select")
            )
        ).send_keys("instantly" + Keys.RETURN)

        self.ps.test_updates['passed'] = True

    # Case C8055 - 028 - Teacher | Change when to show feedback for draft hw
    @pytest.mark.skipif(str(8055) not in TESTS, reason='Excluded')
    def test_teacher_change_when_show_feedback_for_a_draft_homework_8055(self):
        """Change when to show feedback to a student for a draft homework.

        Steps:
        From the dashboard, click on a draft assignment displayed on calendar
        On the drop down menu named 'Show feedback' change the selected option
        Click on the 'Save As Draft' button

        Expected Result:
        The teacher is returned to the dashboard.
        The draft assignment's feedback settings have changed.
        """
        self.ps.test_updates['name'] = 't1.16.028' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.028', '8055']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "hw028_" + str(randint(0, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=4)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='homework',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'problems': {'1.1': (2, 3), },
                                        'status': 'draft',
                                        'feedback': 'immediate'
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
                '//a/label[contains(@data-title,"' + assignment_name + '")]'
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
                '//a/label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        self.teacher.sleep(1)
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.ID, "feedback-select")
            )
        ).send_keys("only after" + Keys.RETURN)
        self.ps.test_updates['passed'] = True

    # Case C8056 - 029 - Teacher | Change when to show feedback for unopened hw
    @pytest.mark.skipif(str(8056) not in TESTS, reason='Excluded')
    def test_teacher_change_when_to_show_feedback_for_unopened_hw_8056(self):
        """Change when to show feedback to a student for an unopened homework.

        Steps:
        If the user has more than one course, select a Tutor course
        From the dashboard, click an unopen assignment displayed on calendar
        Click the 'Edit Assignment' button
        On the drop down menu named 'Show feedback' change the selected option
        Click on the 'Publish' button

        Expected Result:
        The teacher is returned to the dashboard.
        The unopened assignment's show feedback settings are changed.
        """
        self.ps.test_updates['name'] = 't1.16.029' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.029', '8056']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "hw029_" + str(randint(0, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=2)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=4)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='homework',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'problems': {'1.1': (2, 3), },
                                        'status': 'publish',
                                        'feedback': 'immediate'
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
                '//div/label[contains(@data-title,"' + assignment_name + '")]'
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
                '//div/label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[contains(@class,"edit-assignment")]')
            )
        ).click()
        self.teacher.sleep(1)
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.ID, "feedback-select")
            )
        ).send_keys("only after" + Keys.RETURN)
        self.ps.test_updates['passed'] = True

    # Case C8057 - 030 - Teacher | Change when to show feedback for opened hw
    @pytest.mark.skipif(str(8057) not in TESTS, reason='Excluded')
    def test_teacher_change_when_show_feedback_for_opened_homework_8057(self):
        """Change when to show feedback to a student for an opened homework.

        Steps:
        From the dashboard, click on an open assignment displayed on calendar
        Click the 'Edit Assignment' button
        On the drop down menu named 'Show feedback' change the selected option
        Click on the 'Publish' button

        Expected Result:
        The teacher is returned to the dashboard.
        The open assignment's show feedback setting have changed.
        """
        self.ps.test_updates['name'] = 't1.16.030' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.030', '8057']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "hw030_" + str(randint(0, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=4)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='homework',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'problems': {'1.1': (2, 3), },
                                        'status': 'publish',
                                        'feedback': 'immediate'
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
                '//div/label[contains(@data-title,"' + assignment_name + '")]'
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
                '//div/label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[contains(@class,"edit-assignment")]')
            )
        ).click()
        self.teacher.sleep(1)
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.ID, "feedback-select")
            )
        ).send_keys("only after" + Keys.RETURN)
        self.ps.test_updates['passed'] = True

    # Case C8058 - 031 - Teacher | Info icon defines Add HW status bar buttons
    @pytest.mark.skipif(str(8058) not in TESTS, reason='Excluded')
    def test_teacher_info_icon_defines_add_hw_assignment_bar_btns_8058(self):
        """Info icon shows definitions for add homework assignment status bar.

        Steps:
        From the dashboard, click on an (open, unopen, or draft) assignment
        displayed on the calendar, OR create a new assignment
        Click on the info icon

        Expected Result:
        Definitions for the status bar buttons are displayed.
        """
        self.ps.test_updates['name'] = 't1.16.031' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.031', '8058']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        assert('homework/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.XPATH, "//button[contains(@class,'footer-instructions')]")
            )
        ).click()
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.ID, "plan-footer-popover")
            )
        ).click()
        self.ps.test_updates['passed'] = True

    # Case C8059 - 032 - Teacher | Show available problems for a single section
    @pytest.mark.skipif(str(8059) not in TESTS, reason='Excluded')
    def test_teacher_show_available_problems_for_a_single_section_8059(self):
        """Show available problems for a single section.

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and
            select 'Add Homework'
        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select one of the sections in one chapter that is not an introduction
            section
        Click the 'Show Problems' button

        Expected Result:
        The problems for the selected section are displayed.
        """
        self.ps.test_updates['name'] = 't1.16.032' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.032', '8059']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        assert('homework/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        # Open the select problem cards
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.ID, "problems-select")
            )
        ).click()
        section = '2.1'
        chapter = section.split('.')[0]
        data_chapter = self.teacher.find(
            By.XPATH,
            '//a//span[@data-chapter-section="%s"]' % chapter
        )
        if data_chapter.find_element(By.XPATH, "../..").\
                get_attribute('aria-expanded') == 'false':
            data_chapter.click()

        data_section = self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"section")]' +
            '/span[@data-chapter-section="%s"]' % section
        )
        if not('selected' in data_section.find_element(By.XPATH, "..").
                get_attribute('class')):
            data_section.click()
        element = self.teacher.find(
            By.XPATH, '//button[text()="Show Problems"]')
        Assignment.scroll_to(self.teacher.driver, element)
        element.click()

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                    "//div[@data-section='%s']" % section)
            )
        )

        self.ps.test_updates['passed'] = True

    # Case C8060 - 033 - Teacher | Show available problems for a single chapter
    @pytest.mark.skipif(str(8060) not in TESTS, reason='Excluded')
    def test_teacher_show_available_problems_for_a_single_chapter_8060(self):
        """Show available problems for a single chapter.

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and
            select 'Add Homework'
        Click the '+ Select Problems' button
        Select one of the chapters
        Click the 'Show Problems' button

        Expected Result:
        Problems for the whole chapter are displayed.
        """
        self.ps.test_updates['name'] = 't1.16.033' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.033', '8060']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        assert('homework/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.ID, "problems-select")
            )
        ).click()
        chapter = '2'
        self.teacher.find(
            By.XPATH,
            '//div[@data-chapter-section="%s"]' % chapter +
            '//span[@class="chapter-checkbox"]'
        ).click()
        data_sections = self.teacher.driver.find_elements(
            By.XPATH,
            '//div[@class="section selected"]'
        )
        element = self.teacher.find(
            By.XPATH, '//button[text()="Show Problems"]')
        Assignment.scroll_to(self.teacher.driver, element)
        element.click()

        for section in range(len(data_sections) - 1):
            self.teacher.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH,
                     "//div[@data-section='%s.%s']" %
                     (chapter, str(section + 1)))
                )
            )

        self.ps.test_updates['passed'] = True

    # Case C8061 - 034 - Teacher | No problems associated with an Intro section
    @pytest.mark.skipif(str(8061) not in TESTS, reason='Excluded')
    def test_teacher_no_problems_associated_with_an_intro_section_8061(self):
        """No problems should be associated with an Introduction section.

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and
            select 'Add Homework'
        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select the introduction section of the chapter
        Click the 'Show Problems' button

        Expected Result:
        No problems are displayed. The text 'The sections you selected have no
        exercises. Please select more sections.'
        """
        self.ps.test_updates['name'] = 't1.16.031' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.031', '8058']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        assert('homework/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        # Open the select problem cards
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.ID, "problems-select")
            )
        ).click()
        section = '2'
        chapter = section.split('.')[0]
        data_chapter = self.teacher.find(
            By.XPATH,
            '//a//span[@data-chapter-section="%s"]' % chapter
        )
        if data_chapter.find_element(By.XPATH, "../..").\
                get_attribute('aria-expanded') == 'false':
            data_chapter.click()

        data_section = self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"section")]' +
            '/span[@data-chapter-section="%s"]' % section
        )
        if not('selected' in data_section.find_element(By.XPATH, "..").
                get_attribute('class')):
            data_section.click()
        element = self.teacher.find(
            By.XPATH, '//button[text()="Show Problems"]')
        Assignment.scroll_to(self.teacher.driver, element)
        element.click()

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                    "//p[@class='no-exercises-found']")
            )
        )
        self.ps.test_updates['passed'] = True

    # Case C8062 - 035 - Teacher | Change number of Tutor-selected assessments
    @pytest.mark.skipif(str(8062) not in TESTS, reason='Excluded')
    def test_teacher_change_the_number_tutor_selected_assessments_8062(self):
        """Change the number of Tutor-selected assessments.

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and
            select 'Add Homework'
        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select one of the sections in one chapter that is not an introduction
            section
        Click the 'Show Problems' button
        On the section marked 'Tutor Selections', change the number of
            assignments by clicking on the up or down arrow

        Expected Result:
        The problems for the selected section are displayed.
        """
        self.ps.test_updates['name'] = 't1.16.032' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.032', '8059']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        assert('homework/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        # Open the select problem cards
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.ID, "problems-select")
            )
        ).click()
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

        orig_num = self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 "//div[@class='tutor-selections']//h2")
            )
        ).text
        self.teacher.sleep(0.5)
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH,
                    "//div[@class='tutor-selections']//i[@type='chevron-up']")
            )
        ).click()
        new_num = self.teacher.find(
            By.XPATH, "//div[@class='tutor-selections']//h2"
        ).text

        assert(int(orig_num) == int(new_num) - 1), \
            "tutor selections not changed"

        self.ps.test_updates['passed'] = True

    # Case C8063 - 036 - Teacher | Select assessments
    @pytest.mark.skipif(str(8063) not in TESTS, reason='Excluded')
    def test_teacher_select_assessments_8063(self):
        """Select assessments.

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and
            select 'Add Homework'
        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select one of the non-introductory sections in one chapter
        Click the 'Show Problems' button
        Click at least one of the displayed problems

        Expected Result:
        Number of total problems and the number of my selections increases.
        """
        self.ps.test_updates['name'] = 't1.16.036' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.036', '8063']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        assert('homework/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.ID, "problems-select")
            )
        ).click()
        # Open the select problem cards
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
        # keep track of inital problem counts
        total_inital = self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 "//div[@class='num total']//h2")
            )
        ).text
        my_inital = self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 "//div[@class='num mine']//h2")
            )
        ).text
        # select an assessment
        add_button = self.teacher.driver.find_element(
            By.XPATH,
            '//div[@data-exercise-id][2]//div[@class="controls-overlay"]')
        self.teacher.sleep(0.5)
        Assignment.scroll_to(self.teacher.driver, add_button)
        ac = ActionChains(self.teacher.driver)
        self.teacher.sleep(0.5)
        ac.move_to_element(add_button)
        for _ in range(60):
            ac.move_by_offset(-1, 0)
        ac.click()
        ac.perform()
        # assert that counts increased
        self.teacher.sleep(1)
        total_final = self.teacher.driver.find_element(
            By.XPATH, "//div[@class='num total']//h2"
        ).text
        my_final = self.teacher.driver.find_element(
            By.XPATH, "//div[@class='num mine']//h2"
        ).text
        assert(int(total_inital) == int(total_final) - 1), \
            'Total problems counter not increased'
        assert(int(my_inital) == int(my_final) - 1), \
            'My selections counter not increased'

        self.ps.test_updates['passed'] = True

    # Case C8064 - 037 - Teacher | Deselect assessments
    @pytest.mark.skipif(str(8064) not in TESTS, reason='Excluded')
    def test_teacher_deselect_assessments_8064(self):
        """Deselect assessments.

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and
            select 'Add Homework'
        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select one of the non-introductory sections in one chapter
        Click the 'Show Problems' button
        Click at least one of the displayed problems
        Click at least one of the problems that have been selected

        Expected Result:
        The number of my selections and total problems decreases.
        """
        self.ps.test_updates['name'] = 't1.16.037' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.037', '8064']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        assert('homework/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.ID, "problems-select")
            )
        ).click()
        # Open the select problem cards
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
        # keep track of inital problem counts
        total_inital = self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 "//div[@class='num total']//h2")
            )
        ).text
        my_inital = self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 "//div[@class='num mine']//h2")
            )
        ).text
        # select an assessment
        add_button = self.teacher.driver.find_element(
            By.XPATH,
            '//div[@data-exercise-id][2]//div[@class="controls-overlay"]')
        self.teacher.sleep(0.5)
        Assignment.scroll_to(self.teacher.driver, add_button)
        ac = ActionChains(self.teacher.driver)
        self.teacher.sleep(0.5)
        ac.move_to_element(add_button)
        for _ in range(60):
            ac.move_by_offset(-1, 0)
        ac.click()
        ac.perform()
        # assert that counts increased
        self.teacher.sleep(1)
        total_final = self.teacher.driver.find_element(
            By.XPATH, "//div[@class='num total']//h2"
        ).text
        my_final = self.teacher.driver.find_element(
            By.XPATH, "//div[@class='num mine']//h2"
        ).text
        assert(int(total_inital) == int(total_final) - 1), \
            'Total problems counter not increased'
        assert(int(my_inital) == int(my_final) - 1), \
            'My selections counter not increased'

        # de-select an assessment
        add_button = self.teacher.driver.find_element(
            By.XPATH,
            '//div[@data-exercise-id and contains(@class,"is-selected")]' +
            '//div[@class="controls-overlay"]')
        self.teacher.sleep(0.5)
        Assignment.scroll_to(self.teacher.driver, add_button)
        ac = ActionChains(self.teacher.driver)
        self.teacher.sleep(0.5)
        ac.move_to_element(add_button)
        for _ in range(60):
            ac.move_by_offset(-1, 0)
        ac.click()
        ac.perform()
        # assert that counts increased
        self.teacher.sleep(1)
        total_removed = self.teacher.driver.find_element(
            By.XPATH, "//div[@class='num total']//h2"
        ).text
        my_removed = self.teacher.driver.find_element(
            By.XPATH, "//div[@class='num mine']//h2"
        ).text
        assert(int(total_final) == int(total_removed) + 1), \
            'Total problems counter not reduced'
        assert(int(my_final) == int(my_removed) + 1), \
            'My selections counter not reduced'
        self.ps.test_updates['passed'] = True

    # Case C8065 - 038 - Teacher | View feedback by marking Feedback checkbox
    @pytest.mark.skipif(str(8065) not in TESTS, reason='Excluded')
    def test_teacher_view_assessment_feedback_w_preview_feedback_8065(self):
        """View the assessment feedback by marking Preview Feedback checkbox.

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and
            select 'Add Homework'
        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select one of the non-introductory sections in one chapter
        Click the 'Show Problems' button
        Select the 'Preview Feedback' checkbox for at least one problem

        Expected Result:
        Explanations for each answer are displayed as well as a detailed
        solution.
        """
        self.ps.test_updates['name'] = 't1.16.038' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.16', 't1.16.038', '8065']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        assert('homework/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.ID, "problems-select")
            )
        ).click()
        # Open the select problem cards
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
        # select to view details
        add_button = self.teacher.driver.find_element(
            By.XPATH,
            '//div[@data-exercise-id][2]//div[@class="controls-overlay"]')
        self.teacher.sleep(0.5)
        Assignment.scroll_to(self.teacher.driver, add_button)
        ac = ActionChains(self.teacher.driver)
        self.teacher.sleep(0.5)
        ac.move_to_element(add_button)
        for _ in range(60):
            ac.move_by_offset(1, 0)
        ac.click()
        ac.perform()
        # assert that counts increased
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.XPATH, "//span[text()='Preview Feedback']")
            )
        ).click()
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.XPATH,
                 "//div[contains(@class,'question-feedback-content')]")
            )
        ).click()

        self.ps.test_updates['passed'] = True

    # Case C8066 - 039 - Teacher | Assessments show their exercise ID + version
    @pytest.mark.skipif(str(8066) not in TESTS, reason='Excluded')
    def test_teacher_assessment_shows_their_exercise_id_and_version_8066(self):
        """Assessment show their exercise ID and exercise version.

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and
            select 'Add Homework'
        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select one of the non-introductory sections in one chapter
        Click the 'Show Problems' button

        Expected Result:
        For every displayed problem the ID# is displayed as ID#@Version
        """
        self.ps.test_updates['name'] = 't1.16.039' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.039',
            '8066'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        assert('homework/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.ID, "problems-select")
            )
        ).click()
        # Open the select problem cards
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
        assert(len(ids) == len(cards)), \
            'Number of IDs does not match number of visible assessment cards'

        self.ps.test_updates['passed'] = True

    # Case C8067 - 040 - Teacher | Report an error for an assessment
    @pytest.mark.skipif(str(8067) not in TESTS, reason='Excluded')
    def test_teacher_report_an_error_for_an_assessment_8067(self):
        """Report an error for an assessment.

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and
            select 'Add Homework'
        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select one of the non-introductory sections in one chapter
        Click the 'Show Problems' button
        Click the 'Report an error' link on one of the questions.

        Expected Result:
        A new tab is opened to a Google form for reporting errors.
        """
        self.ps.test_updates['name'] = 't1.16.040' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.040',
            '8067'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        assert('homework/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.ID, "problems-select")
            )
        ).click()
        # Open the select problem cards
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
        # Open question details
        add_button = self.teacher.driver.find_element(
            By.XPATH,
            '//div[@data-exercise-id][2]//div[@class="controls-overlay"]')
        self.teacher.sleep(0.5)
        Assignment.scroll_to(self.teacher.driver, add_button)
        ac = ActionChains(self.teacher.driver)
        self.teacher.sleep(0.5)
        ac.move_to_element(add_button)
        for _ in range(60):
            ac.move_by_offset(1, 0)
        ac.click()
        ac.perform()
        # find ID
        id_num = self.teacher.driver.find_element(
            By.XPATH,
            "//span[@class='exercise-tag' and contains(text(),'ID:')]"
        ).text.split(": ")[1]
        # Choose a problem for the assignment
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.XPATH, "//div[@class='action report-error']")
            )
        ).click()
        self.teacher.driver.switch_to_window(
            self.teacher.driver.window_handles[1])
        assert('errata/form' in self.teacher.current_url()), \
            'Not viewing the errata report form'
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.XPATH,
                 "//input[contains(@value,'%s')]" % id_num)
            )
        ).click()

        self.ps.test_updates['passed'] = True

    # Case C8068 - 041 - Teacher | Assessment tags are visible
    @pytest.mark.skipif(str(8068) not in TESTS, reason='Excluded')
    def test_teacher_assessment_tags_are_visible_8068(self):
        """Assessment tags are visible.

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and
            select 'Add Homework'
        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select one of the non-introductory sections in one chapter
        Click the 'Show Problems' button

        Expected Result:
        Tags for each displayed problem exist.
        """
        self.ps.test_updates['name'] = 't1.16.041' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.041',
            '8068'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        assert('homework/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.ID, "problems-select")
            )
        ).click()
        # Open the select problem cards
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
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.XPATH, "//div[@class='exercise-tags']")
            )
        )
        self.ps.test_updates['passed'] = True

    # Case C8069 - 042 - Teacher | Cancel assessment selection before
    # making any changes using the Cancel button
    @pytest.mark.skipif(str(8069) not in TESTS, reason='Excluded')
    def test_teacher_cancel_assessment_select_before_change_cancel_8069(self):
        """Cancel assessment selection before changes with Cancel button.

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and
            select 'Add Homework'
        Click the '+ Select Problems' button
        Click the 'Cancel' button

        Expected Result:
        User is taken back to the page where assignment name, description, and
        open/due dates can be set.
        """
        self.ps.test_updates['name'] = 't1.16.042' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.042',
            '8069'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        assert('homework/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, "problems-select")
            )
        ).click()
        cancel = self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH,
                 "//div[@class='panel-footer']/button[text()='Cancel']")
            )
        )
        Assignment.scroll_to(self.teacher.driver, cancel)
        cancel.click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, "//span[text()='Add Homework Assignment']")
            )
        )
        self.ps.test_updates['passed'] = True

    # Case C8070 - 043 - Teacher | Cancel assessment selection after
    # making any changes using the Cancel button
    @pytest.mark.skipif(str(8070) not in TESTS, reason='Excluded')
    def test_teacher_cancel_assessment_select_after_change_w_cancel_8070(self):
        """Cancel assessment selection after making changes with Cancel button.

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and
            select 'Add Homework'
        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select one of the non-introductory sections in one chapter
        Click the 'Show Problems' button
        Click the'Cancel' button adjacent to the 'Show Problems'
        Click the 'OK' button

        Expected Result:
        User is taken back to the page where the assignment name, description,
        and open/due dates can be set.
        """
        self.ps.test_updates['name'] = 't1.16.043' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.043',
            '8070'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        assert('homework/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, "problems-select")
            )
        ).click()
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
        cancel = self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.XPATH,
                 "//div[@class='panel-footer']/button[text()='Cancel']")
            )
        )
        Assignment.scroll_to(self.teacher.driver, cancel)
        cancel.click()
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.XPATH,
                 "//button[text()='OK']")
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, "//span[text()='Add Homework Assignment']")
            )
        )

        self.ps.test_updates['passed'] = True

    # Case C8071 - 044 - Teacher | Cancel assessment selection before making
    # any changes using the X
    @pytest.mark.skipif(str(8071) not in TESTS, reason='Excluded')
    def test_teacher_cancel_assessment_select_before_changes_w_x_8071(self):
        """Cancel assessment selection before making any changes using the X.

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and
            select 'Add Homework'
        Click the '+ Select Problems' button
        Click the X button

        Expected Result:
        The user is returned to the page where the assignment name,
        description, and open/due dates are set.
        """
        self.ps.test_updates['name'] = 't1.16.044' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.044',
            '8071'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        assert('homework/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, "problems-select")
            )
        ).click()
        x_button = self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH,
                 "//div[contains(@class,'select-topics')]" +
                 "//button[contains(@class,'close-x')]")
            )
        )
        Assignment.scroll_to(self.teacher.driver, x_button)
        x_button.click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, "//span[text()='Add Homework Assignment']")
            )
        )
        self.ps.test_updates['passed'] = True

    # Case C8072 - 045 - Teacher | Cancel assessment selection after
    # making any changes using the X
    @pytest.mark.skipif(str(8072) not in TESTS, reason='Excluded')
    def test_teacher_cancel_assessment_select_after_any_changes_w_x_8072(self):
        """Cancel assessment selection after making any changes using the X.

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and
            select 'Add Homework'
        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select one of the non-introductory sections in one chapter
        Click the 'Show Problems' button
        Select at least one of the displayed problems
        Click the X button
        Click the 'OK' button

        Expected Result:
        User is taken back to the page where the assignment name, description,
        and open/due dates are set.
        """
        self.ps.test_updates['name'] = 't1.16.045' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.045',
            '8072'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        assert('homework/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, "problems-select")
            )
        ).click()
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
        x_button = self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.XPATH,
                 "//div[contains(@class,'select-topics')]" +
                 "//button[contains(@class,'close-x')]")
            )
        )
        Assignment.scroll_to(self.teacher.driver, x_button)
        x_button.click()
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.XPATH,
                 "//button[text()='OK']")
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, "//span[text()='Add Homework Assignment']")
            )
        )
        self.ps.test_updates['passed'] = True

    # Case C8073 - 046 - Teacher | Cancel assessment selection using
    # the Tutor Selection bar Cancel button
    @pytest.mark.skipif(str(8073) not in TESTS, reason='Excluded')
    def test_teacher_cancel_assessment_selection_w_tutor_cancel_btn_8073(self):
        """Cancel assessment selection using Tutor Selection bar Cancel button.

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and
            select 'Add Homework'
        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select one of the non-introductory sections in one chapter
        Click the 'Show Problems' button
        Select at least one of the displayed problems
        Click the 'Cancel' button adjacent to the 'Next' button

        Expected Result:
        The user is taken back to the page where the assignment date,
        description, and open/due dates are set.
        """
        self.ps.test_updates['name'] = 't1.16.046' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.046',
            '8073'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        assert('homework/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.ID, "problems-select")
            )
        ).click()
        # Open the select problem cards
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
        # keep track of inital problem counts
        total_inital = self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 "//div[@class='num total']//h2")
            )
        ).text
        # select an assessment
        add_button = self.teacher.driver.find_element(
            By.XPATH,
            '//div[@data-exercise-id][2]//div[@class="controls-overlay"]')
        self.teacher.sleep(0.5)
        Assignment.scroll_to(self.teacher.driver, add_button)
        ac = ActionChains(self.teacher.driver)
        self.teacher.sleep(0.5)
        ac.move_to_element(add_button)
        for _ in range(60):
            ac.move_by_offset(-1, 0)
        ac.click()
        ac.perform()
        # assert that problem selected
        self.teacher.sleep(1)
        total_final = self.teacher.driver.find_element(
            By.XPATH, "//div[@class='num total']//h2"
        ).text
        assert(int(total_inital) == int(total_final) - 1), \
            'Total problems counter not increased'
        cancel = self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.XPATH,
                 "//div[@class='actions']/button[text()='Cancel']")
            )
        )
        Assignment.scroll_to(self.teacher.driver, cancel)
        cancel.click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, "//span[text()='Add Homework Assignment']")
            )
        )
        self.ps.test_updates['passed'] = True

    # Case C8074 - 047 - Teacher | Select assessments and view assessment order
    @pytest.mark.skipif(str(8074) not in TESTS, reason='Excluded')
    def test_teacher_select_assessments_and_view_assessment_order_8074(self):
        """Select assessments and view assessment ordering.

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and
            select 'Add Homework'
        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select one of the non-introductory sections in one chapter
        Click the 'Show Problems' button
        Select at least one of the displayed problems
        Click the 'Next' button

        Expected Result:
        User is returned to the page where assignment name, description
        and open/due dates are set. Selected problems are displayed in the
        order they will appear.
        """
        self.ps.test_updates['name'] = 't1.16.047' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.047',
            '8074'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        assert('homework/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.ID, "problems-select")
            )
        ).click()
        # Open the select problem cards
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
        # keep track of inital problem counts
        total_inital = self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 "//div[@class='num total']//h2")
            )
        ).text
        # select an assessment
        add_button = self.teacher.driver.find_element(
            By.XPATH,
            '//div[@data-exercise-id][2]//div[@class="controls-overlay"]')
        self.teacher.sleep(0.5)
        Assignment.scroll_to(self.teacher.driver, add_button)
        ac = ActionChains(self.teacher.driver)
        self.teacher.sleep(0.5)
        ac.move_to_element(add_button)
        for _ in range(60):
            ac.move_by_offset(-1, 0)
        ac.click()
        ac.perform()
        # assert that problem selected
        self.teacher.sleep(1)
        total_final = self.teacher.driver.find_element(
            By.XPATH, "//div[@class='num total']//h2"
        ).text
        assert(int(total_inital) == int(total_final) - 1), \
            'Total problems counter not increased'
        next_button = self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.XPATH,
                 "//div[@class='actions']/button[text()='Next']")
            )
        )
        Assignment.scroll_to(self.teacher.driver, next_button)
        next_button.click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, "//table[@class='exercise-table']")
            )
        )
        self.ps.test_updates['passed'] = True

    # Case C8075 - 048 - Teacher | Reorder selected assessments
    @pytest.mark.skipif(str(8075) not in TESTS, reason='Excluded')
    def test_teacher_reorder_selected_assessments_8075(self):
        """Reorder selected assessments.

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and
            select 'Add Homework'
        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select one of the non-introductory sections in one chapter
        Click the 'Show Problems' button
        Select at least two of the displayed problems
        Click the 'Next' button
        Click one of the arrows on at least one problem

        Expected Result:
        The ordering of the problems changes.
        """
        self.ps.test_updates['name'] = 't1.16.048' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.048',
            '8075'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        assert('homework/new' in self.teacher.current_url()), \
            'Not on the add a homework page'

        Assignment().add_homework_problems(self.teacher.driver, {'1.1': 4})

        # Open the select problem cards
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, "//table[@class='exercise-table']")
            )
        )
        card1 = self.teacher.driver.find_element(
            By.XPATH, '//div[contains(@class,"exercise-wrapper")][1]')
        card1_question = card1.find_element(
            By.XPATH, '//div[contains(@class,"question-stem")]'
        ).text
        card2 = self.teacher.driver.find_element(
            By.XPATH, '//div[contains(@class,"exercise-wrapper")][2]')
        card2_question = card2.find_element(
            By.XPATH, '//div[contains(@class,"question-stem")]'
        ).text
        # reorder cards
        card1.find_element(
            By.XPATH, '//i[@type="arrow-down"]').click()
        # Check new ordering of cards
        card1_new = self.teacher.driver.find_element(
            By.XPATH, '//div[contains(@class,"exercise-wrapper")][1]')
        card1_question_new = card1_new.find_element(
            By.XPATH, '//div[contains(@class,"question-stem")]'
        ).text
        card2_new = self.teacher.driver.find_element(
            By.XPATH, '//div[contains(@class,"exercise-wrapper")][2]')
        card2_question_new = card2_new.find_element(
            By.XPATH, '//div[contains(@class,"question-stem")]'
        ).text
        assert(card1_question == card2_question_new), "cards not switched"
        assert(card2_question == card1_question_new), "cards not switched"

        self.ps.test_updates['passed'] = True

    # Case C8076 - 049 - Teacher | Reordering assessments immediately changes
    # the Problem Question list
    @pytest.mark.skipif(str(8076) not in TESTS, reason='Excluded')
    def test_teacher_reordering_assessments_changes_problem_list_8076(self):
        """Reordering assessments immediately changes Problem Question list.

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and
            select 'Add Homework'
        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select one of the non-introductory sections in one chapter
        Click the 'Show Problems' button
        Select at least two of the displayed problems
        Click the 'Next' button
        Click one of the arrows on at least one problem

        Expected Result:
        The Problem Question list reflects the change the problem ordering.
        """
        self.ps.test_updates['name'] = 't1.16.049' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.049',
            '8076'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        assert('homework/new' in self.teacher.current_url()), \
            'Not on the add a homework page'

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

        assert('3' == self.teacher.find(
            By.XPATH, "//div[@class = 'num total']/h2").text), \
            'Default total selections does not equal 3'

        assert('0' == self.teacher.find(
            By.XPATH, "//div[@class = 'num mine']/h2").text), \
            'my selections does not equal 0'

        # Choose a problem for the assignment
        elements = self.teacher.driver.find_elements_by_xpath(
            "//div[@class = 'controls-overlay']")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(elements[0])
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action include']").click()

        self.teacher.driver.execute_script(
            "return arguments[0].scrollIntoView();", elements[1])
        self.teacher.driver.execute_script('window.scrollBy(0, -4500);')

        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(elements[1])
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action include']").click()
        self.teacher.sleep(2)

        assert('5' == self.teacher.find(
            By.XPATH, "//div[@class = 'num total']/h2").text), \
            'total selections does not equal 5'

        assert('2' == self.teacher.find(
            By.XPATH, "//div[@class = 'num mine']/h2").text), \
            'my selections does not equal 2'

        self.teacher.sleep(2)

        self.teacher.find(
            By.XPATH,
            "//button[@class='-review-exercises btn btn-primary']").click()
        self.teacher.sleep(5)

        self.teacher.find(By.XPATH, "//table[@class = 'exercise-table']")

        elem_1_text = self.teacher.find(
            By.XPATH,
            "//table/tbody/tr/td[@class = 'ellipses']/span[@class = 'openst" +
            "ax-has-html'][1]").text

        self.teacher.find(
            By.XPATH, "//button[@class='btn-xs -move-exercise-up circle b" +
            "tn btn-default']").click()

        table = self.teacher.find(
            By.XPATH, "//table[@class = 'exercise-table']")

        self.teacher.driver.execute_script(
            "return arguments[0].scrollIntoView();", table)
        self.teacher.driver.execute_script('window.scrollBy(0, -500);')

        rows = self.teacher.driver.find_elements_by_xpath(
            "//table/tbody/tr/td[@class = 'ellipses']/span[@class = 'open" +
            "stax-has-html']")

        assert(elem_1_text != rows[0].text), \
            'Assessment order was not changed'

        assert(elem_1_text == rows[1].text), \
            'Assessment order was not changed'

        self.ps.test_updates['passed'] = True

    # Case C8077 - 050 - Teacher | Add more assessments using the Add More...
    # button
    @pytest.mark.skipif(str(8077) not in TESTS, reason='Excluded')
    def test_teacher_add_more_assessments_using_the_add_more_button_8077(self):
        """Add more assessments using the Add More... button.

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and
            select 'Add Homework'
        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select one of the non-introductory sections in one chapter
        Click the 'Show Problems' button
        Select at least one of the displayed problems
        Click the 'Next' button
        Click the 'Add More...' button
        Click the 'Show Problems' button
        Select at least one more problem
        Click the 'Next' button

        Expected Result:
        User is returned to the page where the assignment name, description,
        and open/due dates can be set. More selected problems are displayed.
        """
        self.ps.test_updates['name'] = 't1.16.050' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.050',
            '8077'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        assert('homework/new' in self.teacher.current_url()), \
            'Not on the add a homework page'

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

        assert('3' == self.teacher.find(
            By.XPATH, "//div[@class = 'num total']/h2").text), \
            'Default total selections does not equal 3'

        assert('0' == self.teacher.find(
            By.XPATH, "//div[@class = 'num mine']/h2").text), \
            'my selections does not equal 0'

        # Choose a problem for the assignment
        element = self.teacher.find(
            By.XPATH, "//div[@class = 'controls-overlay'][1]")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(element)
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action include']").click()
        self.teacher.sleep(2)

        assert('4' == self.teacher.find(
            By.XPATH, "//div[@class = 'num total']/h2").text), \
            'total selections does not equal 4'

        assert('1' == self.teacher.find(
            By.XPATH, "//div[@class = 'num mine']/h2").text), \
            'my selections does not equal 1'

        self.teacher.sleep(2)

        self.teacher.find(
            By.XPATH,
            "//button[@class='-review-exercises btn btn-primary']").click()
        self.teacher.find(
            By.XPATH,
            "//button[@class='-add-exercises btn btn-default']").click()
        self.teacher.find(
            By.XPATH,
            "//button[@class='-show-problems btn btn-primary']").click()

        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(self.teacher.driver.find_elements_by_xpath(
            "//div[@class = 'controls-overlay']")[1])
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action include']").click()
        self.teacher.sleep(2)

        assert('5' == self.teacher.find(
            By.XPATH, "//div[@class = 'num total']/h2").text), \
            'total selections does not equal 5'

        assert('2' == self.teacher.find(
            By.XPATH, "//div[@class = 'num mine']/h2").text), \
            'my selections does not equal 2'

        self.teacher.find(
            By.XPATH,
            "//button[@class='-review-exercises btn btn-primary']").click()
        self.teacher.find(
            By.XPATH,
            "//div[@class='openstax exercise-wrapper'][2]/div[@class='open" +
            "stax-exercise-preview exercise-card non-interactive is-vertic" +
            "ally-truncated panel panel-default']/div[@class='panel-head" +
            "ing']/span[@class='panel-title -exercise-header']/span[@clas" +
            "s='exercise-number']")

        self.ps.test_updates['passed'] = True

    # Case C8078 - 051 - Teacher | Problem Question list is equal to the Tutor
    # Selection bar numbers
    @pytest.mark.skipif(str(8078) not in TESTS, reason='Excluded')
    def test_teacher_prob_question_list_equal_to_tutor_select_bar_8078(self):
        """Problem Question list is equal to the Tutor Selection bar numbers.

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and
            select 'Add Homework'
        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select one of the non-introductory sections in one chapter
        Click the 'Show Problems' button
        Select at least one of the displayed problems
        Click the 'Next' button

        Expected Result:
        The number of total problems, my selections, and tutor selections
        in the Tutor Selection bar matches what the Problem Question
        list displays.
        """
        self.ps.test_updates['name'] = 't1.16.051' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.051',
            '8078'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        assert('homework/new' in self.teacher.current_url()), \
            'Not on the add a homework page'

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

        assert('3' == self.teacher.find(
            By.XPATH, "//div[@class = 'num total']/h2").text), \
            'Default total selections does not equal 3'

        assert('0' == self.teacher.find(
            By.XPATH, "//div[@class = 'num mine']/h2").text), \
            'my selections does not equal 0'

        # Choose a problem for the assignment
        element = self.teacher.find(
            By.XPATH, "//div[@class = 'controls-overlay'][1]")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(element)
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action include']").click()
        self.teacher.sleep(2)

        assert('4' == self.teacher.find(
            By.XPATH, "//div[@class = 'num total']/h2").text), \
            'total selections does not equal 4'

        assert('1' == self.teacher.find(
            By.XPATH, "//div[@class = 'num mine']/h2").text), \
            'my selections does not equal 1'

        self.teacher.sleep(2)

        self.teacher.find(
            By.XPATH,
            "//button[@class='-review-exercises btn btn-primary']").click()

        self.teacher.sleep(2)

        problems = self.teacher.driver.find_elements_by_xpath(
            "//table[@class='exercise-table']/tbody/tr")
        total = int(self.teacher.find(
            By.XPATH, "//div[@class='num total']/h2").text)

        assert(total == len(problems)), \
            'Number of assessments does not match tutor bar'

        self.ps.test_updates['passed'] = True

    '''
    # Case C8079 - 052 - Teacher | Remove an assessment from the order list
    @pytest.mark.skipif(str(8079) not in TESTS, reason='Excluded')
    def test_teacher_remove_an_assessment_from_the_order_list_8079(self):
        """Remove an assessment from the order list.

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu
            and select 'Add Homework'
        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select one of the non-introductory sections in one chapter
        Click the 'Show Problems' button
        Select at least one of the displayed problems
        Click the 'Next' button
        Scroll down to the ordered list of assessments
        Click the X in the upper right corner of the card

        Expected Result:
        An assessment is removed from the order list
        """
        self.ps.test_updates['name'] = 't1.16.052' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.052',
            '8079'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        assert('homework/new' in self.teacher.current_url()), \
            'Not on the add a homework page'

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

        assert('3' == self.teacher.find(
            By.XPATH, "//div[@class = 'num total']/h2").text), \
            'Default total selections does not equal 3'

        assert('0' == self.teacher.find(
            By.XPATH, "//div[@class = 'num mine']/h2").text), \
            'my selections does not equal 0'

        # Choose a problem for the assignment
        element = self.teacher.find(
            By.XPATH, "//div[@class = 'controls-overlay'][1]")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(element)
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action include']").click()
        self.teacher.sleep(2)

        assert('4' == self.teacher.find(
            By.XPATH, "//div[@class = 'num total']/h2").text), \
            'total selections does not equal 4'

        assert('1' == self.teacher.find(
            By.XPATH, "//div[@class = 'num mine']/h2").text), \
            'my selections does not equal 1'

        self.teacher.sleep(2)

        self.teacher.find(
            By.XPATH,
            "//button[@class='-review-exercises btn btn-primary']").click()

        self.teacher.sleep(2)

        problems = self.teacher.driver.find_elements_by_xpath(
            "//table[@class='exercise-table']/tbody/tr")
        total = int(self.teacher.find(
            By.XPATH, "//div[@class='num total']/h2").text)

        assert(total == len(problems)), \
            'Number of assessments does not match tutor bar'

        self.teacher.find(
            By.XPATH,
            "//button[@class='btn-xs -remove-exercise circle btn btn-default']"
        ).click()
        self.teacher.find(
            By.XPATH,
            "//div[@class='popover-content']/div[@class='controls']/butto" +
            "n[@class='btn btn-primary']").click()

        assert('exercise-table' not in self.teacher.driver.page_source), \
            'Problem list should not be present'

        self.ps.test_updates['passed'] = True
    '''

    # Case C8080 - 053 - Teacher | Remove an assessment from a homework
    # from the Select Problems pane
    @pytest.mark.skipif(str(8080) not in TESTS, reason='Excluded')
    def test_teacher_remove_assessment_from_hw_from__problems_pane_8080(self):
        """Remove an assessment from a homework from the Select Problems pane.

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu
            and select 'Add Homework'
        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select one of the non-introductory sections in one chapter
        Click the 'Show Problems' button
        Select at least two of the displayed problems
        Click the 'Next' button
        Click the 'Add More...' button
        Click the 'Show Problems' button
        Click one of the selected problems
        Click the 'Next' button

        Expected Result:
        Fewer problems are displayed.
        """
        self.ps.test_updates['name'] = 't1.16.053' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.053',
            '8080'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.find(
            By.XPATH, '//button[contains(@class,"sidebar-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        assert('homework/new' in self.teacher.current_url()), \
            'Not on the add a homework page'

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

        assert('3' == self.teacher.find(
            By.XPATH, "//div[@class = 'num total']/h2").text), \
            'Default total selections does not equal 3'

        assert('0' == self.teacher.find(
            By.XPATH, "//div[@class = 'num mine']/h2").text), \
            'my selections does not equal 0'

        # Choose a problem for the assignment
        elements = self.teacher.driver.find_elements_by_xpath(
            "//div[@class = 'controls-overlay']")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(elements[0])
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action include']").click()

        self.teacher.driver.execute_script(
            "return arguments[0].scrollIntoView();", elements[1])
        self.teacher.driver.execute_script('window.scrollBy(0, -4500);')

        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(elements[1])
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action include']").click()
        self.teacher.sleep(2)

        self.teacher.find(
            By.XPATH,
            "//button[@class='-review-exercises btn btn-primary']").click()
        self.teacher.find(
            By.XPATH,
            "//button[@class='-add-exercises btn btn-default']").click()
        self.teacher.find(
            By.XPATH,
            "//button[@class='-show-problems btn btn-primary']").click()

        assert('5' == self.teacher.find(
            By.XPATH, "//div[@class = 'num total']/h2").text), \
            'total selections does not equal 5'

        assert('2' == self.teacher.find(
            By.XPATH, "//div[@class = 'num mine']/h2").text), \
            'my selections does not equal 2'

        element = self.teacher.find(
            By.XPATH, "//div[@class = 'controls-overlay'][1]")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(element)
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action exclude']").click()

        self.teacher.find(
            By.XPATH,
            "//button[@class='-review-exercises btn btn-primary']").click()
        self.teacher.sleep(5)

        assert('4' == self.teacher.find(
            By.XPATH, "//div[@class = 'num total']/h2").text), \
            'total selections does not equal 5'

        assert('1' == self.teacher.find(
            By.XPATH, "//div[@class = 'num mine']/h2").text), \
            'my selections does not equal 2'

        self.ps.test_updates['passed'] = True

    # Case C8081 - 054 - Teacher | Remove an assessment from a homework from
    # the Add Homework Assignment pane
    @pytest.mark.skipif(str(8081) not in TESTS, reason='Excluded')
    def test_teacher_remove_assessment_from_hw_add_homework_pane_8081(self):
        """Remove assessment from homework with Add Homework Assignment pane.

        Steps:
        From the dashboard, click on the 'Add Assignment'
            drop down menu and select 'Add Homework'
        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select one of the non-introductory sections in one chapter
        Click the 'Show Problems' button
        Select at least one of the displayed problems
        Click the 'Next' button
        Click the X button on at least one of the problems
        Click 'OK' on the dialog box that appears

        Expected Result:
        Changes are reflected on the page. If all problems are deleted,
        the Problem Question list disappears. Otherwise, the question
        is removed and the Problem Question list reflects the change.
        """
        self.ps.test_updates['name'] = 't1.16.054' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.054',
            '8081'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C8082 - 055 - Teacher | Change all fields in an unopened,
    # published homework
    @pytest.mark.skipif(str(8082) not in TESTS, reason='Excluded')
    def test_teacher_change_all_field_in_unopened_publish_homework_8082(self):
        """Change all fields in an unopened, published homework.

        Steps:
        From the dashboard, click on a published, unopened homework
        Click on the 'Edit Assignment' button
        Edit the text in the text box named 'Assignment name'
        Edit the text in text box named 'Description or special instructions'
        Edit the open and due dates for the assignment
        Edit the 'Show feedback' drop down menu option
        Click the 'Publish' button

        Expected Result:
        The user is returned to the dashboard. Changes to homework are seen.
        """
        self.ps.test_updates['name'] = 't1.16.055' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.055',
            '8082'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "hw055_" + str(randint(0, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='homework',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'problems': {'1.1': (2, 3), },
                                        'status': 'publish',
                                        'feedback': 'immediate'
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
                '//div/label[contains(@data-title,"' + assignment_name + '")]'
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
                '//div/label[contains(@data-title,"' + assignment_name + '")]'
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
        Assignment().assign_periods(
            self.teacher.driver, {'all': [opens_on, closes_on]})
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.ID, "feedback-select")
            )
        ).send_keys("only after" + Keys.RETURN)
        # remove a question from the assignment
        close_button = self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.XPATH, '//i[@type="close"]')
            )
        )
        Assignment.scroll_to(self.teacher.driver, close_button)
        self.teacher.driver.execute_script('window.scrollBy(0, -150);')
        close_button.click()
        # publish
        publish_button = self.teacher.find(
            By.XPATH, '//button[contains(@class,"-publish")]')
        Assignment.scroll_to(self.teacher.driver, publish_button)
        publish_button.click()
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

    # Case C8083 - 056 - Teacher | Change all fields in a draft homework
    @pytest.mark.skipif(str(8083) not in TESTS, reason='Excluded')
    def test_teacher_change_all_fields_in_a_draft_homework_8083(self):
        """Change all fields in a draft homework.

        Steps:
        From the dashboard, click on a draft homework
        Edit the text in the text box named 'Assignment name'
        Edit the text text box named 'Description or special instructions'
        Edit the open and due dates for the assignment
        Edit the 'Show feedback' drop down menu option
        Click the 'Save As Draft' button

        Expected Result:
        The user is returned to the dashboard. Changes to the draft are seen.
        """
        self.ps.test_updates['name'] = 't1.16.056' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.056',
            '8083'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "hw056_" + str(randint(0, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='homework',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'problems': {'1.1': (2, 3), },
                                        'status': 'draft',
                                        'feedback': 'immediate'
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
                '//a/label[contains(@data-title,"' + assignment_name + '")]'
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
                '//a/label[contains(@data-title,"' + assignment_name + '")]'
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
        Assignment().assign_periods(
            self.teacher.driver, {'all': [opens_on, closes_on]})
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.ID, "feedback-select")
            )
        ).send_keys("only after" + Keys.RETURN)
        # remove a question from the assignment
        close_button = self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.XPATH, '//i[@type="close"]')
            )
        )
        Assignment.scroll_to(self.teacher.driver, close_button)
        self.teacher.driver.execute_script('window.scrollBy(0, -150);')
        close_button.click()
        # publish
        publish_button = self.teacher.find(
            By.XPATH, '//button[contains(@class,"-save")]')
        Assignment.scroll_to(self.teacher.driver, publish_button)
        publish_button.click()
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

    # Case C8084 - 057 - Teacher | Change the name, description, due dates,
    # and feedback timing in an opened homework
    @pytest.mark.skipif(str(8084) not in TESTS, reason='Excluded')
    def test_teacher_change_name_descript_date_feedback_in_open_hw_8084(self):
        """Change name, description, due dates, and feedback in open homework.

        Steps:
        From the dashboard, click on an opened homework
        Click on the 'Edit Assignment' button
        Edit the text in the text box named 'Assignment name'
        Edit the text in text box named 'Description or special instructions'
        Edit the due date for the assignment
        Edit the 'Show feedback' drop down menu option
        Click the 'Publish' button

        Expected Result:
        User is returned to the dashboard. Changes to the homework are seen.
        """
        self.ps.test_updates['name'] = 't1.16.057' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.057',
            '8084'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = "hw057_" + str(randint(0, 999))
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='homework',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'problems': {'1.1': (2, 3), },
                                        'status': 'draft',
                                        'feedback': 'immediate'
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
                '//a/label[contains(@data-title,"' + assignment_name + '")]'
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
                '//a/label[contains(@data-title,"' + assignment_name + '")]'
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
        Assignment().assign_periods(
            self.teacher.driver, {'all': [opens_on, closes_on]})
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.ID, "feedback-select")
            )
        ).send_keys("only after" + Keys.RETURN)
        # publish
        publish_button = self.teacher.find(
            By.XPATH, '//button[contains(@class,"-publish")]')
        Assignment.scroll_to(self.teacher.driver, publish_button)
        publish_button.click()
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

    # Case C111247 - 058 - Teacher | Add a homework by dragging Add Homework
    # to a calendar date
    @pytest.mark.skipif(str(111247) not in TESTS, reason='Excluded')
    def test_teacher_add_homework_by_dragging_add_homework_to_a_c_111247(self):
        """Add a homework by dragging Add Homework to a calendar date.

        Steps:
        Click on the Add Assignment menu
        Click and drag Add Homework to a chosen due date.

        Expected Result:
        User is taken to Add Homework Assignment page with due date filled in.
        """
        self.ps.test_updates['name'] = 't1.16.058' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.058',
            '111247'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
