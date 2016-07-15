"""Tutor v1, Epic 16 - Create A Homework."""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from staxing.assignment import Assignment
from staxing.helper import Teacher, Student
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': '50.0',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([8082])
)
# 8029, 8030-8034, 

# start on 8035 when qa is back up
# pick up on 8058
# 8068, currently only looks at the first assessment for a chapter/section, make it go through all
# 8066 chooses a random chapter/section to load problems from, use that for the other cases that require problems to be selected
# Replace textarea assertions with self.find(textarea)
# 8081 is a repeat of 8079
'''
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
        8078, 8079, 8080, 8081, 8082, 
        8083, 8084
'''


@PastaDecorator.on_platforms(BROWSERS)
class TestCreateAHomework(unittest.TestCase):

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        # self.teacher = Teacher(
        #    use_env_vars=True,
        #    pasta_user=self.ps,
        #    capabilities=self.desired_capabilities
        # )
        # self.teacher = Teacher(use_env_vars=True)
        self.teacher = Teacher(username='teacher01', password='password',
                            site='https://tutor-dev.openstax.org/')
        self.teacher.login()

    def tearDown(self):
        """Test destructor."""
        self.ps.update_job(job_id=str(self.teacher.driver.session_id),
                           **self.ps.test_updates)
        try:
            self.teacher.delete()
        except:
            pass

    # Case C8028 - 001 - Teacher | Add a homework using the Add Assignment drop down menu
    @pytest.mark.skipif(str(8028) not in TESTS, reason='Excluded')
    def test_teacher_add_a_homework_using_the_add_assignment_drop_down_menu(self):
        """Add a homework using the Add Assignment drop down menu.

        Steps:
        Click on the Add Assignment drop down menu on the user dashboard
        Click on the 'Add Homework' button
        
        Expected Result:
        The teacher is taken to the page where they create the assignment.
        """
        self.ps.test_updates['name'] = 't1.16.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.001',
            '8028'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'

        self.teacher.sleep(5)

        self.ps.test_updates['passed'] = True

    # Case C8029 - 002 - Teacher | Add a homework using the calendar date
    @pytest.mark.skipif(str(8029) not in TESTS, reason='Excluded')
    def test_teacher_add_a_homework_using_the_calendar_date(self):
        """Add a homework using the calendar date

        Steps:
        Click on a date at least one day later than the current date on the calendar
        From the menu that appears, click on 'Add Homework'

        Expected Result:
        The teacher is taken to a page where they create the assignment.
        """
        self.ps.test_updates['name'] = 't1.16.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.002',
            '8028'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.page.wait_for_page_load()

        self.teacher.find(By.XPATH, "/html/body/div[@id='react-root-container']/div[@class='tutor-app openstax-wrapper']/div[@class='openstax-debug-content']/div[@class='tutor-booksplash-background']/div[@class='list-courses panel panel-primary']/div[@class='panel-body']/div[@class='calendar-container container-fluid']/div[@class='calendar-body row']/div[@class='col-xs-12']/div[@class='rc-Month']/div[@class='rc-Week'][5]/div[@class='rc-Week-days']/div[@class='rc-Day rc-Day--upcoming'][2]")
        
        assert('passed' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        #self.teacher.find(By.CLASS_NAME, 'rc-Day rc-Day--upcoming').click()
        
        #self.teacher.find(By.LINK_TEXT, 'Add Homework').click()

        self.ps.test_updates['passed'] = True

    # Case C8030 - 003 - Teacher | Set open and due dates for all periods collectively
    @pytest.mark.skipif(str(8030) not in TESTS, reason='Excluded')
    def test_teacher_set_open_and_due_dates_for_periods_collectively(self):
        """Set open and due dates for all periods collectively

        Steps:
        Click on the Add Assignment drop down menu on the user dashboard, OR click a calendar date that is at least one day later than the current date
        Click on the 'Add Homework' button
        Select the 'All Periods' radio button if it is not selected by default
        Select an open date for the assignment using the calendar element
        Select a due date for the assignment using the calendar element

        Expected Result:
        A due date is assigned for all periods collectively.

        """
        self.ps.test_updates['name'] = 't1.16.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.003',
            '8030'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'

        self.teacher.driver.find_elements_by_class_name('datepicker__input-container')[1].click()
        self.teacher.sleep(5)
        self.teacher.driver.find_elements_by_class_name('datepicker__day')[0].click()
        self.teacher.sleep(5)
        #self.teacher.implicitly_wait(10)

        self.ps.test_updates['passed'] = True

    # Case C8031 - 004 - Teacher | Set open and due dates for periods individually
    @pytest.mark.skipif(str(8031) not in TESTS, reason='Excluded')
    def test_teacher_set_open_and_due_dates_for_all_periods_individually(self):
        """Set open and due dates for all periods individually

        Steps:
        Click on the Add Assignment drop down menu on the user dashboard, OR click a calendar date that is at least one day later than the current date
        Click on the 'Add Homework' button
        Select the 'Individual Periods' radio button
        Select the periods that should be required to complete the assignment
        Select open and due dates for each section using the calendar element

        Expected Result:
        Each section that is assigned the homework has an individual opena nd due date.
        """
        self.ps.test_updates['name'] = 't1.16.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.004',
            '8031'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8032 - 005 - Teacher | Save a draft homework
    @pytest.mark.skipif(str(8032) not in TESTS, reason='Excluded')
    def test_teacher_save_a_draft_homework(self):
        """Save a draft homework

        Steps:
        Click on the 'Add Assignment' button, OR click on a calendar date at least one day later than the current date
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
        The teacher is returned to the dashboard where the draft assignment is now displayed on the calendar.
        """
        self.ps.test_updates['name'] = 't1.16.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.005',
            '8032'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True  

    # Case C8033 - 006 - Teacher | Publish a new homework
    @pytest.mark.skipif(str(8033) not in TESTS, reason='Excluded')
    def test_teacher_publish_a_new_homework(self):
        """Publish a new homework

        Steps:
        Click on the Add Assignment drop down menu on the user dashboard, OR click on a calendar date at least one day later than the current date
        Click on the 'Add Homework' button
        Give the homework a name in the 'Assignment name' text box
        Select a due date (individually or collectively) for the assignment using the calendar element
        Click the '+ Select Problems' button
        Select at least one chapter or section to use for the homework
        Click the 'Show Problems' button
        Click at least one problem to be used for My Selections
        Click the 'Next' button
        Click the 'Publish' button

        Expected Result:
        The teacher is returned to the dashboard where the new assignment is displayed.
        """
        self.ps.test_updates['name'] = 't1.16.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.006',
            '8033'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8034 - 007 - Teacher | Publish a draft homework
    @pytest.mark.skipif(str(8034) not in TESTS, reason='Excluded')
    def test_teacher_publish_a_draft_homework(self):
        """Publish a draft homework

        Steps:
        From the user dashboard, click on a draft assignment
        Click the 'Publish' button

        Expected Result:
        A draft homework is published.
        """
        self.ps.test_updates['name'] = 't1.16.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.007',
            '8034'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8035 - 008 - Teacher | Cancel a new homework before making any changes using the Cancel button
    @pytest.mark.skipif(str(8035) not in TESTS, reason='Excluded')
    def test_teacher_cancel_a_new_homework_before_making_any_changes_using_the_cancel_button(self):
        """Cancel a new homework before making any changes using the Cancel button

        Steps:
        Click on the Add Assignment drop down menu on the user dashboard, OR click on a calendar date at least one day later than the current date
        Click on the 'Add Homework' button
        Click on the 'Cancel' button

        Expected Result:
        The teacher is returned to the dashboard.
        """
        self.ps.test_updates['name'] = 't1.16.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.008',
            '8035'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'

        self.teacher.find(By.XPATH, "//button[@class = 'btn btn-default']").click()
        #self.teacher.find(By.XPATH, "/html/body[@class='modal-open']/div[6]/div/div[@class='tutor-dialog fade in modal']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='modal-footer']/button[@class='cancel btn btn-default']").click()
        self.teacher.sleep(5)

        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.ps.test_updates['passed'] = True

    # Case C8036 - 009 - Teacher | Cancel a new homework after making any changes using the Cancel button
    @pytest.mark.skipif(str(8036) not in TESTS, reason='Excluded')
    def test_teacher_cancel_a_new_homework_after_making_any_changes_using_the_cancel_button(self):
        """Cancel a new homework after making any changes using the Cancel button

        Steps:
        Click on the Add Assignment drop down menu on the user dashboard, OR click on a calendar date at least one day later than the current date
        Click on the 'Add Homework' button
        Give the homework a name in the 'Assignment name' text box
        Select a due date (individually or collectively) for the assignment using the calendar element
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
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.009',
            '8036'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'

        self.teacher.find(By.XPATH, "//input[@id = 'reading-title']").send_keys('test title')
        self.teacher.sleep(5)
        self.teacher.find(By.XPATH, "//button[@class = 'btn btn-default']").click()
        self.teacher.find(By.XPATH, "//button[@class = 'ok btn btn-primary']").click()
        #self.teacher.find(By.XPATH, "/html/body[@class='modal-open']/div[6]/div/div[@class='tutor-dialog fade in modal']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='modal-footer']/button[@class='cancel btn btn-default']").click()
        self.teacher.sleep(2)

        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'


        self.ps.test_updates['passed'] = True

    # Case C8037 - 010 - Teacher | Cancel a new homework before making any changes using the X
    @pytest.mark.skipif(str(8037) not in TESTS, reason='Excluded')
    def test_teacher_cancel_a_new_homework_before_making_any_changes_using_the_X(self):
        """Cancel a new homework before making any changes using the X

        Steps:
        Click on the Add Assignment drop down menu on the user dashboard, OR click on a calendar date at least one day later than the current date
        Click on the 'Add Homework' button
        Click on the X button


        Expected Result:
        The teacher is returned to the dashboard.
        """
        self.ps.test_updates['name'] = 't1.16.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.010',
            '8037'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'

        self.teacher.find(By.XPATH, "//button[@class = 'openstax-close-x close pull-right']").click()
        #self.teacher.find(By.XPATH, "/html/body[@class='modal-open']/div[6]/div/div[@class='tutor-dialog fade in modal']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='modal-footer']/button[@class='cancel btn btn-default']").click()
        self.teacher.sleep(5)

        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.ps.test_updates['passed'] = True

    # Case C8038 - 011 - Teacher | Cancel a new homework after making any changes using the X
    @pytest.mark.skipif(str(8038) not in TESTS, reason='Excluded')
    def test_teacher_cancel_a_new_homework_after_making_any_changes_using_the_X(self):
        """Cancel a new homework after making any changes using the X

        Steps:
        Click on the Add Assignment drop down menu on the user dashboard, OR click on a calendar date at least one day later than the current date
        Click on the 'Add Homework' button
        Give the homework a name in the 'Assignment name' text box
        Select a due date (individually or collectively) for the assignment using the calendar element
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
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.011',
            '8038'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'

        self.teacher.find(By.XPATH, "//input[@id = 'reading-title']").send_keys('test title')
        self.teacher.sleep(5)
        self.teacher.find(By.XPATH, "//button[@class = 'openstax-close-x close pull-right']").click()
        self.teacher.find(By.XPATH, "//button[@class = 'ok btn btn-primary']").click()
        #self.teacher.find(By.XPATH, "/html/body[@class='modal-open']/div[6]/div/div[@class='tutor-dialog fade in modal']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='modal-footer']/button[@class='cancel btn btn-default']").click()
        self.teacher.sleep(2)

        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.ps.test_updates['passed'] = True

    # Case C8039 - 012 - Teacher | Cancel a draft homework before making any changes using the Cancel button
    @pytest.mark.skipif(str(8039) not in TESTS, reason='Excluded')
    def test_teacher_cancel_a_draft_homework_before_making_any_changes_using_the_cancel_button(self):
        """Cancel a draft homework before making any changes using the Cancel button

        Steps:
        From the user dashboard, click on a draft assignment
        Click on the 'Cancel' button
        Click on the 'OK' button

        Expected Result:
        The teacher is returned to the dashboard.
        """
        self.ps.test_updates['name'] = 't1.16.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.012',
            '8039'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8040 - 013 - Teacher | Cancel a draft homework after making changes using the Cancel button
    @pytest.mark.skipif(str(8040) not in TESTS, reason='Excluded')
    def test_teacher_cancel_a_draft_homework_after_making_changes_using_the_cancel_button(self):
        """Cancel a draft homework after making changes using the Cancel button

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
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.013',
            '8040'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8041 - 014 - Teacher | Cancel a draft homework before making any changes using the X
    @pytest.mark.skipif(str(8041) not in TESTS, reason='Excluded')
    def test_teacher_cancel_a_draft_homework_before_making_any_changes_using_the_X(self):
        """Cancel a draft homework before making any changes using the X

        Steps:
        From the user dashboard, click on a draft assignment
        Click on the X button
        Click on the 'OK' button

        Expected Result:
        The teacher is returned to the dashboard.
        """
        self.ps.test_updates['name'] = 't1.16.014' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.014',
            '8041'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8042 - 015 - Teacher | Cancel a draft homework after making changes using the X
    @pytest.mark.skipif(str(8042) not in TESTS, reason='Excluded')
    def test_teacher_cancel_a_draft_homework_after_making_changes_using_the_X(self):
        """Cancel a draft homework after making changes using the X

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
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.015',
            '8042'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8043 - 016 - Teacher | Attempt to publish a homework with blank required fields
    @pytest.mark.skipif(str(8043) not in TESTS, reason='Excluded')
    def test_teacher_attempt_to_publish_a_homework_with_blank_required_fields(self):
        """Attempt to publish a homework with blank required fields

        Steps:
        Click on the Add Assignment drop down menu on the user dashboard, OR click on a calendar date at least one day later than the current date
        Click on the 'Add Homework' button
        Click on the 'Publish' button

        Expected Result:
        Red text appears next to every blank required field.
        """
        self.ps.test_updates['name'] = 't1.16.016' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.016',
            '8043'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'

        self.teacher.sleep(2)
        self.teacher.find(By.XPATH, "//button[@class='async-button -publish btn btn-primary']").click()
        
        self.teacher.sleep(3)

        assert(self.teacher.find(By.XPATH, "//div[@class='hint required-hint']").text == 'Required Field'), \
            'Required field text not visible'


        self.ps.test_updates['passed'] = True

    # Case C8044 - 017 - Teacher | Attempt to save a draft homework with blank required fields
    @pytest.mark.skipif(str(8044) not in TESTS, reason='Excluded')
    def test_teacher_attempt_to_save_a_draft_homework_with_blank_required_fields(self):
        """Attempt to save a draft homework with blank required fields

        Steps:
        Click on the Add Assignment drop down menu on the user dashboard, OR click on a calendar date at least one day later than the current date
        Click on the 'Add Homework' button
        Click on the 'Save As Draft' button

        Expected Result:
        Red text appears next to every blank required field.
        """
        self.ps.test_updates['name'] = 't1.16.017' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.017',
            '8044'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='biology')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'

        self.teacher.sleep(2)
        self.teacher.find(By.XPATH, "//button[@class='async-button -save btn btn-default']").click()
        
        self.teacher.sleep(3)

        assert(self.teacher.find(By.XPATH, "//div[@class='hint required-hint']").text == 'Required Field'), \
            'Required field text not visible'


        self.ps.test_updates['passed'] = True

    # Case C8045 - 018 - Teacher | Delete an unpoened homework
    @pytest.mark.skipif(str(8045) not in TESTS, reason='Excluded')
    def test_teacher_delete_an_unopened_homework(self):
        """Delete an unopened homework

        Steps:
        Click on a published assignment that has not yet been opened for students
        Click on the 'Edit Assignment' button
        Click on the 'Delete Assignment' button
        Click 'OK' on the dialog box that pops up

        Expected Result:
        The teacher is returned to the dashboard and the assignment is removed from the calendar.
        """
        self.ps.test_updates['name'] = 't1.16.018' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.018',
            '8045'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'

        self.teacher.find(By.XPATH, "//input[@id = 'reading-title']").send_keys('Epic 16-18')

        # Choose the second date calendar[1], first is calendar[0]
        self.teacher.driver.find_elements_by_xpath("//div[@class = 'datepicker__input-container']")[1].click()
        while(self.teacher.find(By.XPATH, "//span[@class = 'datepicker__current-month']").text != 'December 2016'):
            self.teacher.find(By.XPATH, "//a[@class = 'datepicker__navigation datepicker__navigation--next']").click()

        # Choose the due date of December 31, 2016
        weekends = self.teacher.driver.find_elements_by_xpath("//div[@class = 'datepicker__day datepicker__day--weekend']")
        for day in weekends:
            if day.text == '31':
                due = day
                due.click()
                break
        
        self.teacher.sleep(3)

        # Open the select problem cards
        self.teacher.find(By.XPATH, "//button[@id = 'problems-select']").click()
        self.teacher.find(By.XPATH, "//span[@class = 'chapter-checkbox']").click()
        self.teacher.find(By.XPATH, "//button[@class='-show-problems btn btn-primary']").click()
        self.teacher.sleep(10)

        # Choose a problem for the assignment
        element = self.teacher.find(By.XPATH, "//div[@class = 'controls-overlay'][1]")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(element)
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action include']").click()
        self.teacher.find(By.XPATH, "//button[@class='-review-exercises btn btn-primary']").click()
        self.teacher.sleep(2)

        # Publish the assignment
        self.teacher.driver.execute_script('window.scrollBy(0, -20);')
        self.teacher.find(By.XPATH, "//button[@class='async-button -publish btn btn-primary']").click()
        
        # Give the assignment time to publish
        self.teacher.sleep(60)
        
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'


        spans = self.teacher.driver.find_elements_by_tag_name('span')
        for element in spans:
            if element.text.endswith('2016'):
                month = element

        # Change the calendar date if necessary
        while (month.text != 'December 2016'):
            self.teacher.find(By.XPATH, "//a[@class = 'calendar-header-control next']").click()

        # Select the newly created assignment and delete it
        assignments = self.teacher.driver.find_elements_by_tag_name('label')
        for assignment in assignments:
            if assignment.text == 'Epic 16-18':
                assignment.click()
                self.teacher.find(By.XPATH, "//a[@class='btn btn-default -edit-assignment']").click()
                self.teacher.find(By.XPATH, "//button[@class='async-button delete-link pull-right btn btn-default']").click()
                self.teacher.find(By.XPATH, "//button[@class='btn btn-primary']").click()
                self.teacher.sleep(5)
                break

        self.teacher.driver.refresh()
        deleted = True

        # Verfiy the assignment was deleted
        spans = self.teacher.driver.find_elements_by_tag_name('span')
        for element in spans:
            if element.text.endswith('2016'):
                month = element

        while (month.text != 'December 2016'):
            self.teacher.find(By.XPATH, "//a[@class = 'calendar-header-control next']").click()

        assignments = self.teacher.driver.find_elements_by_tag_name('label')
        for assignment in assignments:
            if assignment.text == 'Epic 16-18':
                deleted = False
                break

        if deleted:
            self.ps.test_updates['passed'] = True

    # Case C8046 - 019 - Teacher | Attempt to delete an open homework
    @pytest.mark.skipif(str(8046) not in TESTS, reason='Excluded')
    def test_teacher_attempt_to_delete_an_open_homework(self):
        """Attempt to delete an open homework

        Steps:
        Click on an assignment on the calendar that is open for student to work on
        Click on the 'Edit Assignment' button

        Expected Result:
        The 'Delete Assignment' button should not appear on the page.
        """
        self.ps.test_updates['name'] = 't1.16.019' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.019',
            '8046'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'

        self.teacher.find(By.XPATH, "//input[@id = 'reading-title']").send_keys('Epic 16-19')

        # Choose the first date calendar[0], second is calendar[1]
        # and set the open date to today
        self.teacher.driver.find_elements_by_xpath("//div[@class = 'datepicker__input-container']")[0].click()
        self.teacher.driver.find_element_by_xpath("//div[@class = 'datepicker__day datepicker__day--today']").click()

        # Choose the second date calendar[1], first is calendar[0]
        self.teacher.driver.find_elements_by_xpath("//div[@class = 'datepicker__input-container']")[1].click()
        while(self.teacher.find(By.XPATH, "//span[@class = 'datepicker__current-month']").text != 'December 2016'):
            self.teacher.find(By.XPATH, "//a[@class = 'datepicker__navigation datepicker__navigation--next']").click()

        # Choose the due date of December 31, 2016
        weekends = self.teacher.driver.find_elements_by_xpath("//div[@class = 'datepicker__day datepicker__day--weekend']")
        for day in weekends:
            if day.text == '31':
                due = day
                due.click()
                break
        
        self.teacher.sleep(3)

        # Open the select problem cards
        self.teacher.find(By.XPATH, "//button[@id = 'problems-select']").click()
        self.teacher.find(By.XPATH, "//span[@class = 'chapter-checkbox']").click()
        self.teacher.find(By.XPATH, "//button[@class='-show-problems btn btn-primary']").click()
        self.teacher.sleep(10)

        # Choose a problem for the assignment
        element = self.teacher.find(By.XPATH, "//div[@class = 'controls-overlay'][1]")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(element)
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action include']").click()
        self.teacher.find(By.XPATH, "//button[@class='-review-exercises btn btn-primary']").click()
        self.teacher.sleep(2)

        # Publish the assignment
        self.teacher.driver.execute_script('window.scrollBy(0, -20);')
        self.teacher.find(By.XPATH, "//button[@class='async-button -publish btn btn-primary']").click()
        
        # Give the assignment time to publish
        self.teacher.sleep(60)
        
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        spans = self.teacher.driver.find_elements_by_tag_name('span')
        for element in spans:
            if element.text.endswith('2016'):
                month = element

        # Change the calendar date if necessary
        while (month.text != 'December 2016'):
            self.teacher.find(By.XPATH, "//a[@class = 'calendar-header-control next']").click()

        # Select the newly created assignment and delete it
        assignments = self.teacher.driver.find_elements_by_tag_name('label')
        for assignment in assignments:
            if assignment.text == 'Epic 16-19':
                assignment.click()
                self.teacher.find(By.XPATH, "//a[@class='btn btn-default -edit-assignment']").click()
                self.teacher.find(By.XPATH, "//button[@class='async-button delete-link pull-right btn btn-default']").click()
                self.teacher.find(By.XPATH, "//button[@class='btn btn-primary']").click()
                self.teacher.sleep(5)
                break

        self.teacher.driver.refresh()
        deleted = True

        # Verfiy the assignment was deleted
        spans = self.teacher.driver.find_elements_by_tag_name('span')
        for element in spans:
            if element.text.endswith('2016'):
                month = element

        while (month.text != 'December 2016'):
            self.teacher.find(By.XPATH, "//a[@class = 'calendar-header-control next']").click()

        assignments = self.teacher.driver.find_elements_by_tag_name('label')
        for assignment in assignments:
            if assignment.text == 'Epic 16-19':
                deleted = False
                break

        if deleted:
            self.ps.test_updates['passed'] = True


    # Case C8047 - 020 - Teacher | Delete a draft homework
    @pytest.mark.skipif(str(8047) not in TESTS, reason='Excluded')
    def test_teacher_delete_a_draft_homework(self):
        """Delete a draft homework

        Steps:
        Click on a draft assignment on the calendar
        Click on the 'Delete Assignment' button
        Click OK on the dialog box that appears

        Expected Result:
        The teacher is returned to the dashboard and the draft assignment is removed from the calendar.
        """
        self.ps.test_updates['name'] = 't1.16.020' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.020',
            '8047'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'

        self.teacher.find(By.XPATH, "//input[@id = 'reading-title']").send_keys('Epic 16-20')

        # Choose the second date calendar[1], first is calendar[0]
        self.teacher.driver.find_elements_by_xpath("//div[@class = 'datepicker__input-container']")[1].click()
        while(self.teacher.find(By.XPATH, "//span[@class = 'datepicker__current-month']").text != 'December 2016'):
            self.teacher.find(By.XPATH, "//a[@class = 'datepicker__navigation datepicker__navigation--next']").click()

        # Choose the due date of December 31, 2016
        weekends = self.teacher.driver.find_elements_by_xpath("//div[@class = 'datepicker__day datepicker__day--weekend']")
        for day in weekends:
            if day.text == '31':
                due = day
                due.click()
                break
        
        self.teacher.sleep(3)

        # Open the select problem cards
        self.teacher.find(By.XPATH, "//button[@id = 'problems-select']").click()
        self.teacher.find(By.XPATH, "//span[@class = 'chapter-checkbox']").click()
        self.teacher.find(By.XPATH, "//button[@class='-show-problems btn btn-primary']").click()
        self.teacher.sleep(10)

        # Choose a problem for the assignment
        element = self.teacher.find(By.XPATH, "//div[@class = 'controls-overlay'][1]")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(element)
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action include']").click()
        self.teacher.find(By.XPATH, "//button[@class='-review-exercises btn btn-primary']").click()
        self.teacher.sleep(2)

        # Save the assignment as a draft
        self.teacher.driver.execute_script('window.scrollBy(0, -20);')
        self.teacher.find(By.XPATH, "//button[@class='async-button -save btn btn-default']").click()
        
        # Give the assignment time to publish
        self.teacher.sleep(60)
        
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'


        spans = self.teacher.driver.find_elements_by_tag_name('span')
        for element in spans:
            if element.text.endswith('2016'):
                month = element

        # Change the calendar date if necessary
        while (month.text != 'December 2016'):
            self.teacher.find(By.XPATH, "//a[@class = 'calendar-header-control next']").click()

        # Select the newly created assignment and delete it
        assignments = self.teacher.driver.find_elements_by_tag_name('label')
        for assignment in assignments:
            if assignment.text == 'Epic 16-20':
                assignment.click()
                self.teacher.find(By.XPATH, "//button[@class='async-button delete-link pull-right btn btn-default']").click()
                self.teacher.find(By.XPATH, "//button[@class='btn btn-primary']").click()
                self.teacher.sleep(5)
                break

        self.teacher.driver.refresh()
        deleted = True

        # Verfiy the assignment was deleted
        spans = self.teacher.driver.find_elements_by_tag_name('span')
        for element in spans:
            if element.text.endswith('2016'):
                month = element

        while (month.text != 'December 2016'):
            self.teacher.find(By.XPATH, "//a[@class = 'calendar-header-control next']").click()

        assignments = self.teacher.driver.find_elements_by_tag_name('label')
        for assignment in assignments:
            if assignment.text == 'Epic 16-20':
                deleted = False
                break

        if deleted:
            self.ps.test_updates['passed'] = True


    # Case C8048 - 021 - Teacher | Add a description to a homework
    @pytest.mark.skipif(str(8048) not in TESTS, reason='Excluded')
    def test_teacher_add_a_description_to_the_homework(self):
        """Add a description to a homework

        Steps:
        From the dashboard, click on the 'Add assignment' drop down menu
        Click on the 'Add Homework' button
        Edit the text box named 'Description or special instructions'

        Expected Result:
        Text is visible in the 'Description or special instructions' text box.
        """
        self.ps.test_updates['name'] = 't1.16.021' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.021',
            '8048'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'

        self.teacher.find(By.XPATH, "//textarea[@class='form-control empty']").send_keys('test description')
        
        self.teacher.sleep(2)

        self.teacher.find(By.XPATH, "//textarea[@class='form-control']")

        self.ps.test_updates['passed'] = True

    # Case C8049 - 022 - Teacher | Change a description for a draft homework
    @pytest.mark.skipif(str(8049) not in TESTS, reason='Excluded')
    def test_teacher_change_a_description_for_a_draft_homework(self):
        """Change a description for a draft homework

        Steps:
        From the dashboard, click on a draft assignment displayed on the calendar
        Edit the text box labeled 'Description or special instructions'
        Click on the 'Save As Draft' button

        Expected Result:
        The teacher is returned to the dashboard. The draft assignment's description has changed.
        """
        self.ps.test_updates['name'] = 't1.16.022' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.022',
            '8049'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'

        self.teacher.find(By.XPATH, "//input[@id = 'reading-title']").send_keys('Epic 16-22')

        # Choose the second date calendar[1], first is calendar[0]
        self.teacher.driver.find_elements_by_xpath("//div[@class = 'datepicker__input-container']")[1].click()
        while(self.teacher.find(By.XPATH, "//span[@class = 'datepicker__current-month']").text != 'December 2016'):
            self.teacher.find(By.XPATH, "//a[@class = 'datepicker__navigation datepicker__navigation--next']").click()

        # Choose the due date of December 31, 2016
        weekends = self.teacher.driver.find_elements_by_xpath("//div[@class = 'datepicker__day datepicker__day--weekend']")
        for day in weekends:
            if day.text == '31':
                due = day
                due.click()
                break
        
        self.teacher.sleep(3)

        # Open the select problem cards
        self.teacher.find(By.XPATH, "//button[@id = 'problems-select']").click()
        self.teacher.find(By.XPATH, "//span[@class = 'chapter-checkbox']").click()
        self.teacher.find(By.XPATH, "//button[@class='-show-problems btn btn-primary']").click()
        self.teacher.sleep(10)

        # Choose a problem for the assignment
        element = self.teacher.find(By.XPATH, "//div[@class = 'controls-overlay'][1]")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(element)
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action include']").click()
        self.teacher.find(By.XPATH, "//button[@class='-review-exercises btn btn-primary']").click()
        self.teacher.sleep(2)

        # Save the assignment as a draft
        self.teacher.driver.execute_script('window.scrollBy(0, -600);')
        self.teacher.find(By.XPATH, "//button[@class='async-button -save btn btn-default']").click()
        
        # Give the assignment time to publish
        self.teacher.sleep(60)
        
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'


        spans = self.teacher.driver.find_elements_by_tag_name('span')
        for element in spans:
            if element.text.endswith('2016'):
                month = element

        # Change the calendar date if necessary
        while (month.text != 'December 2016'):
            self.teacher.find(By.XPATH, "//a[@class = 'calendar-header-control next']").click()

        # Select the newly created assignment, change the description
        assignments = self.teacher.driver.find_elements_by_tag_name('label')
        for assignment in assignments:
            if assignment.text == 'Epic 16-22':
                assignment.click()
                self.teacher.find(By.XPATH, "//textarea").send_keys('new description')
                self.teacher.sleep(2)
                self.teacher.find(By.XPATH, "//textarea")
                self.teacher.find(By.XPATH, "//button[@class='async-button -save btn btn-default']").click()

        self.teacher.sleep(5)

        spans = self.teacher.driver.find_elements_by_tag_name('span')
        for element in spans:
            if element.text.endswith('2016'):
                month = element

        # Change the calendar date if necessary
        while (month.text != 'December 2016'):
            self.teacher.find(By.XPATH, "//a[@class = 'calendar-header-control next']").click()

        # Delete the draft
        assignments = self.teacher.driver.find_elements_by_tag_name('label')
        for assignment in assignments:
            if assignment.text == 'Epic 16-22':
                assignment.click()

                assert('new description' == self.teacher.find(By.XPATH, "//textarea[@class='form-control']").text), \
                    'Not viewing the calendar dashboard'

                self.teacher.find(By.XPATH, "//button[@class='async-button delete-link pull-right btn btn-default']").click()
                self.teacher.find(By.XPATH, "//button[@class='btn btn-primary']").click()
                self.teacher.sleep(5)
                break

        self.teacher.driver.refresh()
        deleted = True

        # Verfiy the assignment was deleted
        spans = self.teacher.driver.find_elements_by_tag_name('span')
        for element in spans:
            if element.text.endswith('2016'):
                month = element

        while (month.text != 'December 2016'):
            self.teacher.find(By.XPATH, "//a[@class = 'calendar-header-control next']").click()

        assignments = self.teacher.driver.find_elements_by_tag_name('label')
        for assignment in assignments:
            if assignment.text == 'Epic 16-22':
                deleted = False
                break

        if deleted:
            self.ps.test_updates['passed'] = True

    # Case C8050 - 023 - Teacher | Change a description for an open homework
    @pytest.mark.skipif(str(8050) not in TESTS, reason='Excluded')
    def test_teacher_change_a_description_for_an_open_homework(self):
        """Change a description for an open homework

        Steps:
        From the dashboard, click on an open assignment displayed on the calendar
        Click the 'Edit Assignment' button
        Edit the text box labeled 'Description or special instructions'
        Click on the 'Publish' button

        Expected Result:
        The teacher is returned to the dashboard. The open assignment's description has changed.
        """
        self.ps.test_updates['name'] = 't1.16.023' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.023',
            '8050'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'

        self.teacher.find(By.XPATH, "//input[@id = 'reading-title']").send_keys('Epic 16-23')

        # Choose the first date calendar[0], second is calendar[1]
        # and set the open date to today
        self.teacher.driver.find_elements_by_xpath("//div[@class = 'datepicker__input-container']")[0].click()
        self.teacher.driver.find_element_by_xpath("//div[@class = 'datepicker__day datepicker__day--today']").click()

        # Choose the second date calendar[1], first is calendar[0]
        self.teacher.driver.find_elements_by_xpath("//div[@class = 'datepicker__input-container']")[1].click()
        while(self.teacher.find(By.XPATH, "//span[@class = 'datepicker__current-month']").text != 'December 2016'):
            self.teacher.find(By.XPATH, "//a[@class = 'datepicker__navigation datepicker__navigation--next']").click()

        # Choose the due date of December 31, 2016
        weekends = self.teacher.driver.find_elements_by_xpath("//div[@class = 'datepicker__day datepicker__day--weekend']")
        for day in weekends:
            if day.text == '31':
                due = day
                due.click()
                break
        
        self.teacher.sleep(3)

        # Open the select problem cards
        self.teacher.find(By.XPATH, "//button[@id = 'problems-select']").click()
        self.teacher.find(By.XPATH, "//span[@class = 'chapter-checkbox']").click()
        self.teacher.find(By.XPATH, "//button[@class='-show-problems btn btn-primary']").click()
        self.teacher.sleep(10)

        # Choose a problem for the assignment
        element = self.teacher.find(By.XPATH, "//div[@class = 'controls-overlay'][1]")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(element)
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action include']").click()
        self.teacher.find(By.XPATH, "//button[@class='-review-exercises btn btn-primary']").click()
        self.teacher.sleep(2)

        # Publish the homework
        self.teacher.driver.execute_script('window.scrollBy(0, -600);')
        self.teacher.find(By.XPATH, "//button[@class='async-button -publish btn btn-primary']").click()
        
        # Give the assignment time to publish
        self.teacher.sleep(60)
        
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'


        spans = self.teacher.driver.find_elements_by_tag_name('span')
        for element in spans:
            if element.text.endswith('2016'):
                month = element

        # Change the calendar date if necessary
        while (month.text != 'December 2016'):
            self.teacher.find(By.XPATH, "//a[@class = 'calendar-header-control next']").click()

        # Select the newly created assignment, change the description
        assignments = self.teacher.driver.find_elements_by_tag_name('label')
        for assignment in assignments:
            if assignment.text == 'Epic 16-23':
                assignment.click()
                self.teacher.driver.execute_script('window.scrollBy(0, 1800);')
                self.teacher.find(By.XPATH, "//a[@class='btn btn-default -edit-assignment']").click()
                self.teacher.find(By.XPATH, "//textarea").send_keys('new description')
                self.teacher.sleep(2)
                self.teacher.find(By.XPATH, "//textarea")
                self.teacher.find(By.XPATH, "//button[@class='async-button -publish btn btn-primary']").click()

        self.teacher.sleep(5)

        # Delete the open assignment
        
        self.teacher.driver.execute_script('window.scrollBy(0, 9000);')
        self.teacher.find(By.XPATH, "//a[@class='btn btn-default -edit-assignment']").click()

        assert('new description' == self.teacher.find(By.XPATH, "//textarea[@class='form-control']").text), \
            'Not viewing the calendar dashboard'

        self.teacher.find(By.XPATH, "//button[@class='async-button delete-link pull-right btn btn-default']").click()
        self.teacher.find(By.XPATH, "//button[@class='btn btn-primary']").click()
        self.teacher.sleep(5)
       

        self.teacher.driver.refresh()
        deleted = True

        # Verfiy the assignment was deleted
        spans = self.teacher.driver.find_elements_by_tag_name('span')
        for element in spans:
            if element.text.endswith('2016'):
                month = element

        while (month.text != 'December 2016'):
            self.teacher.find(By.XPATH, "//a[@class = 'calendar-header-control next']").click()

        assignments = self.teacher.driver.find_elements_by_tag_name('label')
        for assignment in assignments:
            if assignment.text == 'Epic 16-23':
                deleted = False
                break

        if deleted:
            self.ps.test_updates['passed'] = True


    # Case C8051 - 024 - Teacher | Add a name to a homework
    @pytest.mark.skipif(str(8051) not in TESTS, reason='Excluded')
    def test_teacher_add_a_name_to_a_homework(self):
        """Add a name to a homework

        Steps:
        From the dashboard, click on the 'Add assignment' drop down menu
        Click on the 'Add Homework' button
        Edit the text box named 'Assignment name'

        Expected Result:
        Text is visible in the 'Assignment name' text box.
        """
        self.ps.test_updates['name'] = 't1.16.024' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.024',
            '8051'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'

        self.teacher.find(By.XPATH, "//input[@id='reading-title']").send_keys('test name')
        
        self.teacher.sleep(2)

        self.teacher.find(By.XPATH, "//input[@class='form-control' and @id='reading-title']")

        self.ps.test_updates['passed'] = True

    # Case C8052 - 025 - Teacher | Change a name for a draft homework
    @pytest.mark.skipif(str(8052) not in TESTS, reason='Excluded')
    def test_teacher_change_a_name_for_a_draft_homework(self):
        """Change a name for a draft homework

        Steps:
        From the dashboard, click on a draft assignment displayed on the calendar
        Edit the text box labeled 'Assignment name'
        Click on the 'Save As Draft' button

        Expected Result:
        The teacher is returned to the dashboard. The draft assignment's name has changed.
        """
        self.ps.test_updates['name'] = 't1.16.025' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.025',
            '8052'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'

        self.teacher.find(By.XPATH, "//input[@id = 'reading-title']").send_keys('Epic 16-25')

        # Choose the second date calendar[1], first is calendar[0]
        self.teacher.driver.find_elements_by_xpath("//div[@class = 'datepicker__input-container']")[1].click()
        while(self.teacher.find(By.XPATH, "//span[@class = 'datepicker__current-month']").text != 'December 2016'):
            self.teacher.find(By.XPATH, "//a[@class = 'datepicker__navigation datepicker__navigation--next']").click()

        # Choose the due date of December 31, 2016
        weekends = self.teacher.driver.find_elements_by_xpath("//div[@class = 'datepicker__day datepicker__day--weekend']")
        for day in weekends:
            if day.text == '31':
                due = day
                due.click()
                break
        
        self.teacher.sleep(3)

        # Open the select problem cards
        self.teacher.find(By.XPATH, "//button[@id = 'problems-select']").click()
        self.teacher.find(By.XPATH, "//span[@class = 'chapter-checkbox']").click()
        self.teacher.find(By.XPATH, "//button[@class='-show-problems btn btn-primary']").click()
        self.teacher.sleep(10)

        # Choose a problem for the assignment
        element = self.teacher.find(By.XPATH, "//div[@class = 'controls-overlay'][1]")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(element)
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action include']").click()
        self.teacher.find(By.XPATH, "//button[@class='-review-exercises btn btn-primary']").click()
        self.teacher.sleep(2)

        # Save the assignment as a draft
        self.teacher.driver.execute_script('window.scrollBy(0, -600);')
        self.teacher.find(By.XPATH, "//button[@class='async-button -save btn btn-default']").click()
        
        # Give the assignment time to publish
        self.teacher.sleep(60)
        
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'


        spans = self.teacher.driver.find_elements_by_tag_name('span')
        for element in spans:
            if element.text.endswith('2016'):
                month = element

        # Change the calendar date if necessary
        while (month.text != 'December 2016'):
            self.teacher.find(By.XPATH, "//a[@class = 'calendar-header-control next']").click()

        # Select the newly created assignment, change the name
        assignments = self.teacher.driver.find_elements_by_tag_name('label')
        for assignment in assignments:
            if assignment.text == 'Epic 16-25':
                assignment.click()
                assert('Epic 16-25' == self.teacher.find(By.XPATH, "//input[@id = 'reading-title']").get_attribute("value")), \
                    'Not on the add a homework page'
                self.teacher.find(By.XPATH, "//input[@id = 'reading-title']").send_keys('!')
                self.teacher.sleep(2)
                self.teacher.find(By.XPATH, "//button[@class='async-button -save btn btn-default']").click()

        self.teacher.sleep(5)

        spans = self.teacher.driver.find_elements_by_tag_name('span')
        for element in spans:
            if element.text.endswith('2016'):
                month = element

        # Change the calendar date if necessary
        while (month.text != 'December 2016'):
            self.teacher.find(By.XPATH, "//a[@class = 'calendar-header-control next']").click()

        # Delete the draft
        assignments = self.teacher.driver.find_elements_by_tag_name('label')
        for assignment in assignments:
            if assignment.text == 'Epic 16-25!':
                assignment.click()

                assert('Epic 16-25!' == self.teacher.find(By.XPATH, "//input[@id = 'reading-title']").get_attribute("value")), \
                    'Not on the add a homework page'

                self.teacher.find(By.XPATH, "//button[@class='async-button delete-link pull-right btn btn-default']").click()
                self.teacher.find(By.XPATH, "//button[@class='btn btn-primary']").click()
                self.teacher.sleep(5)
                break

        self.teacher.driver.refresh()
        deleted = True

        # Verfiy the assignment was deleted
        spans = self.teacher.driver.find_elements_by_tag_name('span')
        for element in spans:
            if element.text.endswith('2016'):
                month = element

        while (month.text != 'December 2016'):
            self.teacher.find(By.XPATH, "//a[@class = 'calendar-header-control next']").click()

        assignments = self.teacher.driver.find_elements_by_tag_name('label')
        for assignment in assignments:
            if assignment.text == 'Epic 16-25!':
                deleted = False
                break

        if deleted:
            self.ps.test_updates['passed'] = True

    # Case C8053 - 026 - Teacher | Change a name for an open homework
    @pytest.mark.skipif(str(8053) not in TESTS, reason='Excluded')
    def test_teacher_change_a_name_for_an_open_homework(self):
        """Change a name for an open homework

        Steps:
        From the dashboard, click on an open assignment displayed on the calendar
        Click the 'Edit Assignment' button
        Edit the text box labeled 'Assignment name'
        Click on the 'Publish' button

        Expected Result:
        The name of an open homework is changed
        """
        self.ps.test_updates['name'] = 't1.16.026' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.026',
            '8053'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'

        self.teacher.find(By.XPATH, "//input[@id = 'reading-title']").send_keys('Epic 16-26')

        # Choose the first date calendar[0], second is calendar[1]
        # and set the open date to today
        self.teacher.driver.find_elements_by_xpath("//div[@class = 'datepicker__input-container']")[0].click()
        self.teacher.driver.find_element_by_xpath("//div[@class = 'datepicker__day datepicker__day--today']").click()

        # Choose the second date calendar[1], first is calendar[0]
        self.teacher.driver.find_elements_by_xpath("//div[@class = 'datepicker__input-container']")[1].click()
        while(self.teacher.find(By.XPATH, "//span[@class = 'datepicker__current-month']").text != 'December 2016'):
            self.teacher.find(By.XPATH, "//a[@class = 'datepicker__navigation datepicker__navigation--next']").click()

        # Choose the due date of December 31, 2016
        weekends = self.teacher.driver.find_elements_by_xpath("//div[@class = 'datepicker__day datepicker__day--weekend']")
        for day in weekends:
            if day.text == '31':
                due = day
                due.click()
                break
        
        self.teacher.sleep(3)

        # Open the select problem cards
        self.teacher.find(By.XPATH, "//button[@id = 'problems-select']").click()
        self.teacher.find(By.XPATH, "//span[@class = 'chapter-checkbox']").click()
        self.teacher.find(By.XPATH, "//button[@class='-show-problems btn btn-primary']").click()
        self.teacher.sleep(10)

        # Choose a problem for the assignment
        element = self.teacher.find(By.XPATH, "//div[@class = 'controls-overlay'][1]")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(element)
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action include']").click()
        self.teacher.find(By.XPATH, "//button[@class='-review-exercises btn btn-primary']").click()
        self.teacher.sleep(2)

        # Publish the homework
        self.teacher.driver.execute_script('window.scrollBy(0, -600);')
        self.teacher.find(By.XPATH, "//button[@class='async-button -publish btn btn-primary']").click()
        
        # Give the assignment time to publish
        self.teacher.sleep(60)
        
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'


        spans = self.teacher.driver.find_elements_by_tag_name('span')
        for element in spans:
            if element.text.endswith('2016'):
                month = element

        # Change the calendar date if necessary
        while (month.text != 'December 2016'):
            self.teacher.find(By.XPATH, "//a[@class = 'calendar-header-control next']").click()

        # Select the newly created assignment, change the description
        assignments = self.teacher.driver.find_elements_by_tag_name('label')
        for assignment in assignments:
            if assignment.text == 'Epic 16-26':
                assignment.click()
                self.teacher.driver.execute_script('window.scrollBy(0, 1800);')
                self.teacher.find(By.XPATH, "//a[@class='btn btn-default -edit-assignment']").click()
                self.teacher.find(By.XPATH, "//input[@id = 'reading-title']").send_keys('!')
                self.teacher.sleep(2)
                self.teacher.find(By.XPATH, "//button[@class='async-button -publish btn btn-primary']").click()

        self.teacher.sleep(5)

        # Delete the open assignment
        
        self.teacher.driver.execute_script('window.scrollBy(0, 9000);')
        self.teacher.find(By.XPATH, "//a[@class='btn btn-default -edit-assignment']").click()

        assert('Epic 16-26!' == self.teacher.find(By.XPATH, "//input[@id = 'reading-title']").get_attribute("value")), \
            'Epic 16-26!'

        self.teacher.find(By.XPATH, "//button[@class='async-button delete-link pull-right btn btn-default']").click()
        self.teacher.find(By.XPATH, "//button[@class='btn btn-primary']").click()
        self.teacher.sleep(5)
       

        self.teacher.driver.refresh()
        deleted = True

        # Verfiy the assignment was deleted
        spans = self.teacher.driver.find_elements_by_tag_name('span')
        for element in spans:
            if element.text.endswith('2016'):
                month = element

        while (month.text != 'December 2016'):
            self.teacher.find(By.XPATH, "//a[@class = 'calendar-header-control next']").click()

        assignments = self.teacher.driver.find_elements_by_tag_name('label')
        for assignment in assignments:
            if assignment.text == 'Epic 16-26!':
                deleted = False
                break

        if deleted:
            self.ps.test_updates['passed'] = True


    # Case C8054 - 027 - Teacher | Select when to show feedback to a student
    @pytest.mark.skipif(str(8054) not in TESTS, reason='Excluded')
    def test_teacher_select_when_to_show_feedback_to_a_student(self):
        """Select when to show feedback to a student

        Steps:
        From the dashboard, click on the 'Add assignment' drop down menu
        Click on the 'Add Homework' button
        Select an option on the 'Show feedback' drop down menu

        Expected Result:
        The option chosen is shown on the drop down menu.
        """
        self.ps.test_updates['name'] = 't1.16.027' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.027',
            '8054'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'

        self.teacher.sleep(2)
        self.teacher.find(By.XPATH, "//select").send_keys('instantly after the student answers each question' + Keys.RETURN)
        
        self.teacher.sleep(2)

        self.ps.test_updates['passed'] = True

    # Case C8055 - 028 - Teacher | Change when to show feedback to a student for a draft homework
    @pytest.mark.skipif(str(8055) not in TESTS, reason='Excluded')
    def test_teacher_change_when_to_show_feedback_to_a_student_for_a_draft_homework(self):
        """Change when to show feedback to a student for a draft homework

        Steps:
        From the dashboard, click on a draft assignment displayed on the calendar
        On the drop down menu named 'Show feedback' change the selected option
        Click on the 'Save As Draft' button

        Expected Result:
        The teacher is returned to the dashboard. The draft assignment's feedback settings have changed.
        """
        self.ps.test_updates['name'] = 't1.16.028' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.028',
            '8055'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'

        self.teacher.find(By.XPATH, "//input[@id = 'reading-title']").send_keys('Epic 16-28')

        # Choose the second date calendar[1], first is calendar[0]
        self.teacher.driver.find_elements_by_xpath("//div[@class = 'datepicker__input-container']")[1].click()
        while(self.teacher.find(By.XPATH, "//span[@class = 'datepicker__current-month']").text != 'December 2016'):
            self.teacher.find(By.XPATH, "//a[@class = 'datepicker__navigation datepicker__navigation--next']").click()

        # Choose the due date of December 31, 2016
        weekends = self.teacher.driver.find_elements_by_xpath("//div[@class = 'datepicker__day datepicker__day--weekend']")
        for day in weekends:
            if day.text == '31':
                due = day
                due.click()
                break
        
        self.teacher.sleep(3)

        # Open the select problem cards
        self.teacher.find(By.XPATH, "//button[@id = 'problems-select']").click()
        self.teacher.find(By.XPATH, "//span[@class = 'chapter-checkbox']").click()
        self.teacher.find(By.XPATH, "//button[@class='-show-problems btn btn-primary']").click()
        self.teacher.sleep(10)

        # Choose a problem for the assignment
        element = self.teacher.find(By.XPATH, "//div[@class = 'controls-overlay'][1]")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(element)
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action include']").click()
        self.teacher.find(By.XPATH, "//button[@class='-review-exercises btn btn-primary']").click()
        self.teacher.sleep(2)

        # Save the assignment as a draft
        self.teacher.driver.execute_script('window.scrollBy(0, -600);')
        self.teacher.find(By.XPATH, "//button[@class='async-button -save btn btn-default']").click()
        
        # Give the assignment time to publish
        self.teacher.sleep(60)
        
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'


        spans = self.teacher.driver.find_elements_by_tag_name('span')
        for element in spans:
            if element.text.endswith('2016'):
                month = element

        # Change the calendar date if necessary
        while (month.text != 'December 2016'):
            self.teacher.find(By.XPATH, "//a[@class = 'calendar-header-control next']").click()

        # Select the newly created assignment, change the feedback
        assignments = self.teacher.driver.find_elements_by_tag_name('label')
        for assignment in assignments:
            if assignment.text == 'Epic 16-28':
                assignment.click()
                self.teacher.find(By.XPATH, "//select").send_keys('instantly after the student answers each question' + Keys.RETURN)
                self.teacher.sleep(2)
                self.teacher.find(By.XPATH, "//button[@class='async-button -save btn btn-default']").click()

        self.teacher.sleep(5)

        spans = self.teacher.driver.find_elements_by_tag_name('span')
        for element in spans:
            if element.text.endswith('2016'):
                month = element

        # Change the calendar date if necessary
        while (month.text != 'December 2016'):
            self.teacher.find(By.XPATH, "//a[@class = 'calendar-header-control next']").click()

        # Delete the draft
        assignments = self.teacher.driver.find_elements_by_tag_name('label')
        for assignment in assignments:
            if assignment.text == 'Epic 16-28':
                assignment.click()

                self.teacher.find(By.XPATH, "//button[@class='async-button delete-link pull-right btn btn-default']").click()
                self.teacher.find(By.XPATH, "//button[@class='btn btn-primary']").click()
                self.teacher.sleep(5)
                break

        self.teacher.driver.refresh()
        deleted = True

        # Verfiy the assignment was deleted
        spans = self.teacher.driver.find_elements_by_tag_name('span')
        for element in spans:
            if element.text.endswith('2016'):
                month = element

        while (month.text != 'December 2016'):
            self.teacher.find(By.XPATH, "//a[@class = 'calendar-header-control next']").click()

        assignments = self.teacher.driver.find_elements_by_tag_name('label')
        for assignment in assignments:
            if assignment.text == 'Epic 16-28':
                deleted = False
                break

        if deleted:
            self.ps.test_updates['passed'] = True

    # Case C8056 - 029 - Teacher | Change when to show feedback to a student for an unopened homework
    @pytest.mark.skipif(str(8056) not in TESTS, reason='Excluded')
    def test_teacher_change_when_to_show_feedback_to_a_student_for_an_unopened_homework(self):
        """Change when to show feedback to a student for an unopened homework

        Steps:
        If the user has more than one course, select a Tutor course
        From the dashboard, click on an unopen assignment displayed on the calendar
        Click the 'Edit Assignment' button
        On the drop down menu named 'Show feedback' change the selected option
        Click on the 'Publish' button

        Expected Result:
        The teacher is returned to the dashboard. The unopened assignment's show feedback settings are changed.
        """
        self.ps.test_updates['name'] = 't1.16.029' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.029',
            '8056'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'

        self.teacher.find(By.XPATH, "//input[@id = 'reading-title']").send_keys('Epic 16-29')

        # Choose the second date calendar[1], first is calendar[0]
        self.teacher.driver.find_elements_by_xpath("//div[@class = 'datepicker__input-container']")[1].click()
        while(self.teacher.find(By.XPATH, "//span[@class = 'datepicker__current-month']").text != 'December 2016'):
            self.teacher.find(By.XPATH, "//a[@class = 'datepicker__navigation datepicker__navigation--next']").click()

        # Choose the due date of December 31, 2016
        weekends = self.teacher.driver.find_elements_by_xpath("//div[@class = 'datepicker__day datepicker__day--weekend']")
        for day in weekends:
            if day.text == '31':
                due = day
                due.click()
                break
        
        self.teacher.sleep(3)

        # Open the select problem cards
        self.teacher.find(By.XPATH, "//button[@id = 'problems-select']").click()
        self.teacher.find(By.XPATH, "//span[@class = 'chapter-checkbox']").click()
        self.teacher.find(By.XPATH, "//button[@class='-show-problems btn btn-primary']").click()
        self.teacher.sleep(10)

        # Choose a problem for the assignment
        element = self.teacher.find(By.XPATH, "//div[@class = 'controls-overlay'][1]")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(element)
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action include']").click()
        self.teacher.find(By.XPATH, "//button[@class='-review-exercises btn btn-primary']").click()
        self.teacher.sleep(2)

        # Publish the homework
        self.teacher.driver.execute_script('window.scrollBy(0, -600);')
        self.teacher.find(By.XPATH, "//button[@class='async-button -publish btn btn-primary']").click()
        
        # Give the assignment time to publish
        self.teacher.sleep(60)
        
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'


        spans = self.teacher.driver.find_elements_by_tag_name('span')
        for element in spans:
            if element.text.endswith('2016'):
                month = element

        # Change the calendar date if necessary
        while (month.text != 'December 2016'):
            self.teacher.find(By.XPATH, "//a[@class = 'calendar-header-control next']").click()

        # Select the newly created assignment, change the feedback
        assignments = self.teacher.driver.find_elements_by_tag_name('label')
        for assignment in assignments:
            if assignment.text == 'Epic 16-29':
                assignment.click()
                self.teacher.driver.execute_script('window.scrollBy(0, 1800);')
                self.teacher.find(By.XPATH, "//a[@class='btn btn-default -edit-assignment']").click()
                self.teacher.find(By.XPATH, "//select").send_keys('instantly after the student answers each question' + Keys.RETURN)
                self.teacher.sleep(2)
                self.teacher.find(By.XPATH, "//button[@class='async-button -publish btn btn-primary']").click()

        self.teacher.sleep(5)

        # Delete the open assignment
        
        self.teacher.driver.execute_script('window.scrollBy(0, 9000);')
        self.teacher.find(By.XPATH, "//a[@class='btn btn-default -edit-assignment']").click()

        self.teacher.find(By.XPATH, "//button[@class='async-button delete-link pull-right btn btn-default']").click()
        self.teacher.find(By.XPATH, "//button[@class='btn btn-primary']").click()
        self.teacher.sleep(5)
       

        self.teacher.driver.refresh()
        deleted = True

        # Verfiy the assignment was deleted
        spans = self.teacher.driver.find_elements_by_tag_name('span')
        for element in spans:
            if element.text.endswith('2016'):
                month = element

        while (month.text != 'December 2016'):
            self.teacher.find(By.XPATH, "//a[@class = 'calendar-header-control next']").click()

        assignments = self.teacher.driver.find_elements_by_tag_name('label')
        for assignment in assignments:
            if assignment.text == 'Epic 16-29':
                deleted = False
                break

        if deleted:
            self.ps.test_updates['passed'] = True

    # Case C8057 - 030 - Teacher | Change when to show feedback to a student for an opened homework
    @pytest.mark.skipif(str(8057) not in TESTS, reason='Excluded')
    def test_teacher_change_when_to_show_feedback_to_a_student_for_an_opened_homework(self):
        """Change when to show feedback to a student for an opened homework

        Steps:
        From the dashboard, click on an open assignment displayed on the calendar
        Click the 'Edit Assignment' button
        On the drop down menu named 'Show feedback' change the selected option
        Click on the 'Publish' button

        Expected Result:
        The teacher is returned to the dashboard. The open assignment's show feedback setting have changed.
        """
        self.ps.test_updates['name'] = 't1.16.030' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.030',
            '8057'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'

        self.teacher.find(By.XPATH, "//input[@id = 'reading-title']").send_keys('Epic 16-30')

        # Choose the first date calendar[0], second is calendar[1]
        # and set the open date to today
        self.teacher.driver.find_elements_by_xpath("//div[@class = 'datepicker__input-container']")[0].click()
        self.teacher.driver.find_element_by_xpath("//div[@class = 'datepicker__day datepicker__day--today']").click()

        # Choose the second date calendar[1], first is calendar[0]
        self.teacher.driver.find_elements_by_xpath("//div[@class = 'datepicker__input-container']")[1].click()
        while(self.teacher.find(By.XPATH, "//span[@class = 'datepicker__current-month']").text != 'December 2016'):
            self.teacher.find(By.XPATH, "//a[@class = 'datepicker__navigation datepicker__navigation--next']").click()

        # Choose the due date of December 31, 2016
        weekends = self.teacher.driver.find_elements_by_xpath("//div[@class = 'datepicker__day datepicker__day--weekend']")
        for day in weekends:
            if day.text == '31':
                due = day
                due.click()
                break
        
        self.teacher.sleep(3)

        # Open the select problem cards
        self.teacher.find(By.XPATH, "//button[@id = 'problems-select']").click()
        self.teacher.find(By.XPATH, "//span[@class = 'chapter-checkbox']").click()
        self.teacher.find(By.XPATH, "//button[@class='-show-problems btn btn-primary']").click()
        self.teacher.sleep(10)

        # Choose a problem for the assignment
        element = self.teacher.find(By.XPATH, "//div[@class = 'controls-overlay'][1]")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(element)
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action include']").click()
        self.teacher.find(By.XPATH, "//button[@class='-review-exercises btn btn-primary']").click()
        self.teacher.sleep(2)

        # Publish the homework
        self.teacher.driver.execute_script('window.scrollBy(0, -600);')
        self.teacher.find(By.XPATH, "//button[@class='async-button -publish btn btn-primary']").click()
        
        # Give the assignment time to publish
        self.teacher.sleep(60)
        
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'


        spans = self.teacher.driver.find_elements_by_tag_name('span')
        for element in spans:
            if element.text.endswith('2016'):
                month = element

        # Change the calendar date if necessary
        while (month.text != 'December 2016'):
            self.teacher.find(By.XPATH, "//a[@class = 'calendar-header-control next']").click()

        # Select the newly created assignment, change the description
        assignments = self.teacher.driver.find_elements_by_tag_name('label')
        for assignment in assignments:
            if assignment.text == 'Epic 16-30':
                assignment.click()
                self.teacher.driver.execute_script('window.scrollBy(0, 1800);')
                self.teacher.find(By.XPATH, "//a[@class='btn btn-default -edit-assignment']").click()
                self.teacher.find(By.XPATH, "//select").send_keys('instantly after the student answers each question' + Keys.RETURN)
                self.teacher.sleep(2)
                self.teacher.find(By.XPATH, "//button[@class='async-button -publish btn btn-primary']").click()

        self.teacher.sleep(5)

        # Delete the open assignment
        
        self.teacher.driver.execute_script('window.scrollBy(0, 9000);')
        self.teacher.find(By.XPATH, "//a[@class='btn btn-default -edit-assignment']").click()
        self.teacher.find(By.XPATH, "//button[@class='async-button delete-link pull-right btn btn-default']").click()
        self.teacher.find(By.XPATH, "//button[@class='btn btn-primary']").click()
        self.teacher.sleep(5)
       

        self.teacher.driver.refresh()
        deleted = True

        # Verfiy the assignment was deleted
        spans = self.teacher.driver.find_elements_by_tag_name('span')
        for element in spans:
            if element.text.endswith('2016'):
                month = element

        while (month.text != 'December 2016'):
            self.teacher.find(By.XPATH, "//a[@class = 'calendar-header-control next']").click()

        assignments = self.teacher.driver.find_elements_by_tag_name('label')
        for assignment in assignments:
            if assignment.text == 'Epic 16-30':
                deleted = False
                break

        if deleted:
            self.ps.test_updates['passed'] = True

    # Case C8058 - 031 - Teacher | Info icon shows definitions for the Add Homework Assignment status bar buttons
    @pytest.mark.skipif(str(8058) not in TESTS, reason='Excluded')
    def test_teacher_info_icon_shows_definitions_for_the_add_homework_assignment_status_bar_buttons(self):
        """Info icon shows definitions for the add homework assignment status bar buttons

        Steps:
        From the dashboard, click on an (open, unopen, or draft) assignment displayed on the calendar, OR create a new assignment
        Click on the info icon

        Expected Result:
        Definitions for the status bar buttons are displayed.
        """
        self.ps.test_updates['name'] = 't1.16.031' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.031',
            '8058'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'

        self.teacher.find(By.XPATH, "//i[@class='fa fa-info-circle']").click()
        self.teacher.find(By.XPATH, "//div[@role = 'tooltip']")
        self.teacher.sleep(5)

        self.ps.test_updates['passed'] = True

    # Case C8059 - 032 - Teacher | Show available problems for a single section
    @pytest.mark.skipif(str(8059) not in TESTS, reason='Excluded')
    def test_teacher_show_available_problems_for_a_single_section(self):
        """Show available problems for a single section

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and select 'Add Homework'
        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select one of the sections in one chapter that is not an introduction section
        Click the 'Show Problems' button

        Expected Result:
        The problems for the selected section are displayed.
        """
        self.ps.test_updates['name'] = 't1.16.032' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.032',
            '8059'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'

        self.teacher.sleep(3)

        # Open the select problem cards
        self.teacher.find(By.XPATH, "//button[@id = 'problems-select']").click()
        self.teacher.find(By.XPATH, "//div[@class = 'section'][2]").click()
        self.teacher.find(By.XPATH, "//button[@class='-show-problems btn btn-primary']").click()
        self.teacher.sleep(10)

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, "//div[@class = 'openstax-exercise-preview exercise-card has-actions non-interactive is-vertically-truncated panel panel-default']")
            )
        )

        self.ps.test_updates['passed'] = True

    # Case C8060 - 033 - Teacher | Show available problems for a single chapter
    @pytest.mark.skipif(str(8060) not in TESTS, reason='Excluded')
    def test_teacher_show_available_problems_for_a_single_chapter(self):
        """Show available problems for a single chapter

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and select 'Add Homework'
        Click the '+ Select Problems' button
        Select one of the chapters
        Click the 'Show Problems' button

        Expected Result:
        Problems for the whole chapter are displayed.
        """
        self.ps.test_updates['name'] = 't1.16.033' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.033',
            '8060'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'

        self.teacher.sleep(3)

        # Open the select problem cards
        self.teacher.find(By.XPATH, "//button[@id = 'problems-select']").click()
        self.teacher.find(By.XPATH, "//span[@class = 'chapter-checkbox']").click()
        self.teacher.find(By.XPATH, "//button[@class='-show-problems btn btn-primary']").click()
        self.teacher.sleep(10)

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, "//div[@class = 'openstax-exercise-preview exercise-card has-actions non-interactive is-vertically-truncated panel panel-default']")
            )
        )

        self.ps.test_updates['passed'] = True

    # Case C8061 - 034 - Teacher | No problems should be associated with an Introduction section
    @pytest.mark.skipif(str(8061) not in TESTS, reason='Excluded')
    def test_teacher_no_problems_should_be_associated_with_an_introduction_section(self):
        """No problems should be associated with an Introduction section

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and select 'Add Homework'
        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select the introduction section of the chapter
        Click the 'Show Problems' button

        Expected Result:
        No problems are displayed. The text 'The sections you selected have no exercises. Please select more sections.'
        """
        self.ps.test_updates['name'] = 't1.16.034' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.034',
            '8061'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'

        self.teacher.sleep(3)

        # Open the select problem cards
        self.teacher.find(By.XPATH, "//button[@id = 'problems-select']").click()
        self.teacher.find(By.XPATH, "//div[@class = 'section']").click()
        self.teacher.find(By.XPATH, "//button[@class='-show-problems btn btn-primary']").click()
        self.teacher.sleep(10)

        assert('openstax-exercise-preview exercise-card has-actions non-interactive is-vertically-truncated panel panel-default' not in self.teacher.driver.page_source), \
            'Exercises should not be visible'

        self.ps.test_updates['passed'] = True

    # Case C8062 - 035 - Teacher | Change the number of Tutor-selected assessments
    @pytest.mark.skipif(str(8062) not in TESTS, reason='Excluded')
    def test_teacher_change_the_number_of_tutor_selected_assessments(self):
        """Change the number of Tutor-selected assessments

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and select 'Add Homework'
        Click the '+ Select Problems' button
        Select at least one chapter
        Click the 'Show Problems' button
        On the section marked 'Tutor Selections', change the number of assignments by clicking on the up or down arrow

        Expected Result:
        The number of total problems and tutor selections changes.
        """
        self.ps.test_updates['name'] = 't1.16.035' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.035',
            '8062'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'

        self.teacher.sleep(3)

        # Open the select problem cards
        self.teacher.find(By.XPATH, "//button[@id = 'problems-select']").click()
        self.teacher.find(By.XPATH, "//div[@class = 'section']").click()
        self.teacher.find(By.XPATH, "//button[@class='-show-problems btn btn-primary']").click()
        self.teacher.sleep(3)

        assert('3' == self.teacher.find(By.XPATH, "//div[@class = 'tutor-selections']/h2").text), \
            'Default tutor selections does not equal 3'

        self.teacher.find(By.XPATH, "//button[@class = 'btn-xs circle btn btn-default']").click()
        self.teacher.sleep(2)

        assert('2' == self.teacher.find(By.XPATH, "//div[@class = 'tutor-selections']/h2").text), \
            'tutor selections does not equal 2'

        self.ps.test_updates['passed'] = True

    # Case C8063 - 036 - Teacher | Select assessments
    @pytest.mark.skipif(str(8063) not in TESTS, reason='Excluded')
    def test_teacher_select_assessments(self):
        """Select assessments

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and select 'Add Homework'
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
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.036',
            '8063'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        
        self.teacher.sleep(3)

        # Open the select problem cards
        self.teacher.find(By.XPATH, "//button[@id = 'problems-select']").click()
        self.teacher.find(By.XPATH, "//span[@class = 'chapter-checkbox']").click()
        self.teacher.find(By.XPATH, "//button[@class='-show-problems btn btn-primary']").click()
        self.teacher.sleep(10)


        assert('3' == self.teacher.find(By.XPATH, "//div[@class = 'num total']/h2").text), \
            'Default total selections does not equal 3'

        assert('0' == self.teacher.find(By.XPATH, "//div[@class = 'num mine']/h2").text), \
            'my selections does not equal 0'

        # Choose a problem for the assignment
        element = self.teacher.find(By.XPATH, "//div[@class = 'controls-overlay'][1]")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(element)
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action include']").click()
        self.teacher.sleep(2)

        assert('4' == self.teacher.find(By.XPATH, "//div[@class = 'num total']/h2").text), \
            'total selections does not equal 4'

        assert('1' == self.teacher.find(By.XPATH, "//div[@class = 'num mine']/h2").text), \
            'my selections does not equal 1'

        self.teacher.sleep(2)

        self.ps.test_updates['passed'] = True

    # Case C8064 - 037 - Teacher | Deselect assessments
    @pytest.mark.skipif(str(8064) not in TESTS, reason='Excluded')
    def test_teacher_deselect_assessments(self):
        """Deselect assessments

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and select 'Add Homework'
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
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.037',
            '8064'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        
        self.teacher.sleep(3)

        # Open the select problem cards
        self.teacher.find(By.XPATH, "//button[@id = 'problems-select']").click()
        self.teacher.find(By.XPATH, "//span[@class = 'chapter-checkbox']").click()
        self.teacher.find(By.XPATH, "//button[@class='-show-problems btn btn-primary']").click()
        self.teacher.sleep(10)


        assert('3' == self.teacher.find(By.XPATH, "//div[@class = 'num total']/h2").text), \
            'Default total selections does not equal 3'

        assert('0' == self.teacher.find(By.XPATH, "//div[@class = 'num mine']/h2").text), \
            'my selections does not equal 0'

        # Choose a problem for the assignment
        element = self.teacher.find(By.XPATH, "//div[@class = 'controls-overlay'][1]")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(element)
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action include']").click()
        self.teacher.sleep(2)

        assert('4' == self.teacher.find(By.XPATH, "//div[@class = 'num total']/h2").text), \
            'total selections does not equal 4'

        assert('1' == self.teacher.find(By.XPATH, "//div[@class = 'num mine']/h2").text), \
            'my selections does not equal 1'

        self.teacher.sleep(2)

        self.teacher.find(By.XPATH, "//div[@class = 'action exclude']").click()

        assert('3' == self.teacher.find(By.XPATH, "//div[@class = 'num total']/h2").text), \
            'total selections does not equal 3'

        assert('0' == self.teacher.find(By.XPATH, "//div[@class = 'num mine']/h2").text), \
            'my selections does not equal 0'

        self.teacher.sleep(3)


        self.ps.test_updates['passed'] = True

    # Case C8065 - 038 - Teacher | View assessment feedback by marking the Preview Feedback checkbox
    @pytest.mark.skipif(str(8065) not in TESTS, reason='Excluded')
    def test_teacher_view_assessment_feedback_by_marking_the_preview_feedback_checkbox(self):
        """View the assessment feedback by marking the Preview Feedback checkbox

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and select 'Add Homework'
        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select one of the non-introductory sections in one chapter
        Click the 'Show Problems' button
        Select the 'Preview Feedback' checkbox for at least one problem

        Expected Result:
        Explanations for each answer are displayed as well as a detailed solution.
        """
        self.ps.test_updates['name'] = 't1.16.038' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.16',
            't1.16.038',
            '8065'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        
        self.teacher.sleep(3)

        # Open the select problem cards
        self.teacher.find(By.XPATH, "//button[@id = 'problems-select']").click()
        self.teacher.find(By.XPATH, "//span[@class = 'chapter-checkbox']").click()
        self.teacher.find(By.XPATH, "//button[@class='-show-problems btn btn-primary']").click()
        self.teacher.sleep(10)

        # Choose a problem for the assignment
        element = self.teacher.find(By.XPATH, "//div[@class = 'controls-overlay'][1]")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(element)
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action details']").click()
        self.teacher.find(By.XPATH, "//div[@class = 'action feedback-on']").click()

        self.teacher.sleep(2)

        self.teacher.find(By.XPATH, "//div[@class = 'openstax-exercise-preview exercise-card has-actions actions-on-side is-displaying-feedback panel panel-default']")

        self.ps.test_updates['passed'] = True

    # Case C8066 - 039 - Teacher | Assessments show their exercise ID and exercise version
    @pytest.mark.skipif(str(8066) not in TESTS, reason='Excluded')
    def test_teacher_assessments_show_their_exercise_id_and_exercise_version(self):
        """Assessments show their exercise ID and exercise version

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and select 'Add Homework'
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
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        
        self.teacher.sleep(3)

        # Open the select problem cards
        self.teacher.find(By.XPATH, "//button[@id = 'problems-select']").click()
        #self.teacher.find(By.XPATH, "//span[@class = 'chapter-checkbox']").click()
        chapters = self.teacher.driver.find_elements_by_xpath("//span[@class = 'chapter-checkbox']")
        chapters[randint(0, len(chapters))].click()
        self.teacher.find(By.XPATH, "//button[@class='-show-problems btn btn-primary']").click()
        self.teacher.sleep(10)

        ids = self.teacher.driver.find_elements_by_xpath("//div[@class = 'exercise-uid']")
        cards = self.teacher.driver.find_elements_by_xpath("//div[@class = 'openstax-exercise-preview exercise-card has-actions non-interactive is-vertically-truncated panel panel-default']")

        # Verify that each visible card has an ID
        assert(len(ids) == len(cards)), \
            'Number of visible IDs does not match the number of visible assessment cards'

        # Verify that the IDs match the expected format
        for num in ids:
            print (num.text)
            print (len(num.text))
            assert(num.text.startswith("Exercise ID: ") and num.text.split('@')[0][13:].isdigit() and num.text.split('@')[1].isdigit()), \
                'Exercise ID does not match what is expected'


        self.ps.test_updates['passed'] = True

    # Case C8067 - 040 - Teacher | Report an error for an assessment
    @pytest.mark.skipif(str(8067) not in TESTS, reason='Excluded')
    def test_teacher_report_an_Error_for_an_assessment(self):
        """Report an error for an assessment

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and select 'Add Homework'
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
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        
        self.teacher.sleep(3)

        # Open the select problem cards
        self.teacher.find(By.XPATH, "//button[@id = 'problems-select']").click()
        self.teacher.find(By.XPATH, "//span[@class = 'chapter-checkbox']").click()
        self.teacher.find(By.XPATH, "//button[@class='-show-problems btn btn-primary']").click()
        self.teacher.sleep(10)

        # Choose a problem for the assignment
        element = self.teacher.find(By.XPATH, "//div[@class = 'controls-overlay'][1]")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(element)
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action details']").click()
        self.teacher.find(By.XPATH, "//div[@class='action report-error']").click()

        self.teacher.sleep(2)

        self.teacher.driver.switch_to_window(self.teacher.driver.window_handles[-1])

        assert('docs.google' in self.teacher.current_url()), \
            'Not viewing the errata report form'

        self.teacher.sleep(3)


        self.ps.test_updates['passed'] = True

    # Case C8068 - 041 - Teacher | Assessment tags are visible
    @pytest.mark.skipif(str(8068) not in TESTS, reason='Excluded')
    def test_teacher_assessment_tags_are_visible(self):
        """Assessment tags are visible

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and select 'Add Homework'
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
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        
        self.teacher.sleep(3)

        # Open the select problem cards
        self.teacher.find(By.XPATH, "//button[@id = 'problems-select']").click()
        self.teacher.find(By.XPATH, "//span[@class = 'chapter-checkbox']").click()
        self.teacher.find(By.XPATH, "//button[@class='-show-problems btn btn-primary']").click()
        self.teacher.sleep(10)

        # Choose a problem for the assignment
        element = self.teacher.find(By.XPATH, "//div[@class = 'controls-overlay'][1]")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(element)
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action details']").click()

        self.teacher.find(By.XPATH, "//div[@class='exercise-tags']")

        """
        while "//div[@class='page-navigation next']" in self.teacher.driver.page_source:
            #self.teacher.find(By.XPATH, "//div[@class='page-navigation next']").click()
            
            actions = ActionChains(self.teacher.driver)
            actions.move_to_element(self.teacher.find(By.XPATH, "//div[@class='triangle']"))
            actions.click(self.teacher.find(By.XPATH, "//div[@class='triangle']"))
            actions.perform()
            self.teacher.find(By.XPATH, "//div[@class='exercise-tags']")
        """
        self.teacher.sleep(2)

        self.ps.test_updates['passed'] = True

    # Case C8069 - 042 - Teacher | Cancel assessment selection before making any changes using the Cancel button
    @pytest.mark.skipif(str(8069) not in TESTS, reason='Excluded')
    def test_teacher_cancel_assessment_selection_before_making_any_changes_using_the_cancel_button(self):
        """Cancel assessment selection before making any changes using the Cancel button

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and select 'Add Homework'
        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select one of the non-introductory sections in one chapter
        Click the 'Show Problems' button
        Click the 'Cancel' button
        Click the 'OK' button

        Expected Result:
        User is taken back to the page where assignment name, description, and open/due dates can be set.
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
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        
        self.teacher.sleep(3)

        # Open the select problem cards
        self.teacher.find(By.XPATH, "//button[@id = 'problems-select']").click()
        self.teacher.find(By.XPATH, "//span[@class = 'chapter-checkbox']").click()
        self.teacher.find(By.XPATH, "//button[@class='-show-problems btn btn-primary']").click()
        self.teacher.sleep(10)

        self.teacher.driver.execute_script('window.scrollBy(0, -9000);')
        self.teacher.find(By.XPATH, "//div[@class='panel-footer']/button[@class='btn btn-default']").click()
        self.teacher.sleep(2)
        
        self.teacher.find(By.XPATH, "//button[@class='ok btn btn-primary']").click()

        self.teacher.sleep(5)

        assert('textarea' in self.teacher.driver.page_source), \
            'Not on the add a homework page'

        self.ps.test_updates['passed'] = True

    # Case C8070 - 043 - Teacher | Cancel assessment selection after making any changes using the Cancel button
    @pytest.mark.skipif(str(8070) not in TESTS, reason='Excluded')
    def test_teacher_cancel_assessment_selection_after_making_any_changes_using_the_cancel_button(self):
        """Cancel assessment selection after making any changes using the Cancel button

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and select 'Add Homework'
        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select one of the non-introductory sections in one chapter
        Click the 'Show Problems' button
        Select at least one of the displayed problems
        Click the 'Cancel' button adjacent to the 'Next' button, OR click the 'Cancel' button adjacent to the 'Show Problems' button and then hit the 'OK' button
        Click the 'OK' button

        Expected Result:
        User is taken back to the page where the assignment name, description, and open/due dates can be set.
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
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        
        self.teacher.sleep(3)

        # Open the select problem cards
        self.teacher.find(By.XPATH, "//button[@id = 'problems-select']").click()
        self.teacher.find(By.XPATH, "//span[@class = 'chapter-checkbox']").click()
        self.teacher.find(By.XPATH, "//button[@class='-show-problems btn btn-primary']").click()
        self.teacher.sleep(10)


        assert('3' == self.teacher.find(By.XPATH, "//div[@class = 'num total']/h2").text), \
            'Default total selections does not equal 3'

        assert('0' == self.teacher.find(By.XPATH, "//div[@class = 'num mine']/h2").text), \
            'my selections does not equal 0'

        # Choose a problem for the assignment
        element = self.teacher.find(By.XPATH, "//div[@class = 'controls-overlay'][1]")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(element)
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action include']").click()
        self.teacher.sleep(2)

        assert('4' == self.teacher.find(By.XPATH, "//div[@class = 'num total']/h2").text), \
            'total selections does not equal 4'

        assert('1' == self.teacher.find(By.XPATH, "//div[@class = 'num mine']/h2").text), \
            'my selections does not equal 1'

        self.teacher.sleep(2)

        self.teacher.driver.execute_script('window.scrollBy(0, -9000);')
        self.teacher.find(By.XPATH, "//div[@class='panel-footer']/button[@class='btn btn-default']").click()
        self.teacher.sleep(2)
        
        self.teacher.find(By.XPATH, "//button[@class='ok btn btn-primary']").click()

        self.teacher.sleep(5)

        assert('textarea' in self.teacher.driver.page_source), \
            'Not on the add a homework page'

        self.ps.test_updates['passed'] = True

    # Case C8071 - 044 - Teacher | Cancel assessment selection before making any changes using the X
    @pytest.mark.skipif(str(8071) not in TESTS, reason='Excluded')
    def test_teacher_cancel_assessment_selection_before_making_any_changes_using_the_X(self):
        """Cancel assessment selection before making any changes using the X

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and select 'Add Homework'
        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select one of the non-introductory sections in one chapter
        Click the 'Show Problems' button
        Click the X button
        Click the 'OK' button

        Expected Result:
        The user is returned to the page where the assignment name, description, and open/due dates are set.
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
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        
        self.teacher.sleep(3)

        # Open the select problem cards
        self.teacher.find(By.XPATH, "//button[@id = 'problems-select']").click()
        self.teacher.find(By.XPATH, "//span[@class = 'chapter-checkbox']").click()
        self.teacher.find(By.XPATH, "//button[@class='-show-problems btn btn-primary']").click()
        self.teacher.sleep(10)

        #self.teacher.driver.execute_script('window.scrollBy(0, -9000);')
        element = self.teacher.find(By.XPATH, "//button[@class='openstax-close-x close']")
        self.teacher.driver.execute_script("return arguments[0].scrollIntoView();", element)
        self.teacher.driver.execute_script('window.scrollBy(0, -9000);')
        element.click()
        #self.teacher.find(By.XPATH, "//div[@class='panel-footer']/button[@class='btn btn-default']").click()
        self.teacher.sleep(5)
        
        self.teacher.find(By.XPATH, "//button[@class='ok btn btn-primary']").click()

        self.teacher.sleep(5)

        assert('textarea' in self.teacher.driver.page_source), \
            'Not on the add a homework page'

        self.ps.test_updates['passed'] = True

    # Case C8072 - 045 - Teacher | Cancel assessment selection after making any changes using the X
    @pytest.mark.skipif(str(8072) not in TESTS, reason='Excluded')
    def test_teacher_cancel_assessment_selection_after_making_any_changes_using_the_X(self):
        """Cancel assessment selection after making any changes using the X

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and select 'Add Homework'
        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select one of the non-introductory sections in one chapter
        Click the 'Show Problems' button
        Select at least one of the displayed problems
        Click the X button
        Click the 'OK' button

        Expected Result:
        User is taken back to the page where the assignment name, description, and open/due dates are set.
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
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        
        self.teacher.sleep(3)

        # Open the select problem cards
        self.teacher.find(By.XPATH, "//button[@id = 'problems-select']").click()
        self.teacher.find(By.XPATH, "//span[@class = 'chapter-checkbox']").click()
        self.teacher.find(By.XPATH, "//button[@class='-show-problems btn btn-primary']").click()
        self.teacher.sleep(10)


        assert('3' == self.teacher.find(By.XPATH, "//div[@class = 'num total']/h2").text), \
            'Default total selections does not equal 3'

        assert('0' == self.teacher.find(By.XPATH, "//div[@class = 'num mine']/h2").text), \
            'my selections does not equal 0'

        # Choose a problem for the assignment
        element = self.teacher.find(By.XPATH, "//div[@class = 'controls-overlay'][1]")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(element)
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action include']").click()
        self.teacher.sleep(2)

        assert('4' == self.teacher.find(By.XPATH, "//div[@class = 'num total']/h2").text), \
            'total selections does not equal 4'

        assert('1' == self.teacher.find(By.XPATH, "//div[@class = 'num mine']/h2").text), \
            'my selections does not equal 1'

        self.teacher.sleep(2)

        element = self.teacher.find(By.XPATH, "//button[@class='openstax-close-x close']")
        self.teacher.driver.execute_script("return arguments[0].scrollIntoView();", element)
        self.teacher.driver.execute_script('window.scrollBy(0, -9000);')
        element.click()
        #self.teacher.find(By.XPATH, "//div[@class='panel-footer']/button[@class='btn btn-default']").click()
        self.teacher.sleep(5)
        
        self.teacher.find(By.XPATH, "//button[@class='ok btn btn-primary']").click()

        self.teacher.sleep(5)

        assert('textarea' in self.teacher.driver.page_source), \
            'Not on the add a homework page'

        self.ps.test_updates['passed'] = True

    # Case C8073 - 046 - Teacher | Cancel assessment selection using the Tutor Selection bar Cancel button
    @pytest.mark.skipif(str(8073) not in TESTS, reason='Excluded')
    def test_teacher_cancel_assessment_selection_using_the_tutor_selection_bar_cancel_button(self):
        """Cancel assessment selection using the Tutor Selection bar Cancel button

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and select 'Add Homework'
        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select one of the non-introductory sections in one chapter
        Click the 'Show Problems' button
        Select at least one of the displayed problems
        Click the 'Cancel' button adjacent to the 'Next' button

        Expected Result:
        The user is taken back to the page where the assignment date, description, and open/due dates are set.
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
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        
        self.teacher.sleep(3)

        # Open the select problem cards
        self.teacher.find(By.XPATH, "//button[@id = 'problems-select']").click()
        self.teacher.find(By.XPATH, "//span[@class = 'chapter-checkbox']").click()
        self.teacher.find(By.XPATH, "//button[@class='-show-problems btn btn-primary']").click()
        self.teacher.sleep(10)


        assert('3' == self.teacher.find(By.XPATH, "//div[@class = 'num total']/h2").text), \
            'Default total selections does not equal 3'

        assert('0' == self.teacher.find(By.XPATH, "//div[@class = 'num mine']/h2").text), \
            'my selections does not equal 0'

        # Choose a problem for the assignment
        element = self.teacher.find(By.XPATH, "//div[@class = 'controls-overlay'][1]")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(element)
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action include']").click()
        self.teacher.sleep(2)

        assert('4' == self.teacher.find(By.XPATH, "//div[@class = 'num total']/h2").text), \
            'total selections does not equal 4'

        assert('1' == self.teacher.find(By.XPATH, "//div[@class = 'num mine']/h2").text), \
            'my selections does not equal 1'

        self.teacher.sleep(2)

        self.teacher.find(By.XPATH, "//button[@class='-cancel-add btn btn-default']").click()
        #self.teacher.find(By.XPATH, "//div[@class='panel-footer']/button[@class='btn btn-default']").click()

        self.teacher.sleep(5)

        assert('textarea' in self.teacher.driver.page_source), \
            'Not on the add a homework page'

        self.ps.test_updates['passed'] = True

    # Case C8074 - 047 - Teacher | Select assessments and view assessment ordering
    @pytest.mark.skipif(str(8074) not in TESTS, reason='Excluded')
    def test_teacher_select_assessments_and_view_assessment_ordering(self):
        """Select assessments and view assessment ordering

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and select 'Add Homework'
        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select one of the non-introductory sections in one chapter
        Click the 'Show Problems' button
        Select at least one of the displayed problems
        Click the 'Next' button

        Expected Result:
        User is returned to the page where assignment name, description, and open/due dates are set. Selected problems are displayed in the order they will appear.
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
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        
        self.teacher.sleep(3)

        # Open the select problem cards
        self.teacher.find(By.XPATH, "//button[@id = 'problems-select']").click()
        self.teacher.find(By.XPATH, "//span[@class = 'chapter-checkbox']").click()
        self.teacher.find(By.XPATH, "//button[@class='-show-problems btn btn-primary']").click()
        self.teacher.sleep(10)


        assert('3' == self.teacher.find(By.XPATH, "//div[@class = 'num total']/h2").text), \
            'Default total selections does not equal 3'

        assert('0' == self.teacher.find(By.XPATH, "//div[@class = 'num mine']/h2").text), \
            'my selections does not equal 0'

        # Choose a problem for the assignment
        element = self.teacher.find(By.XPATH, "//div[@class = 'controls-overlay'][1]")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(element)
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action include']").click()
        self.teacher.sleep(2)

        assert('4' == self.teacher.find(By.XPATH, "//div[@class = 'num total']/h2").text), \
            'total selections does not equal 4'

        assert('1' == self.teacher.find(By.XPATH, "//div[@class = 'num mine']/h2").text), \
            'my selections does not equal 1'

        self.teacher.sleep(2)

        self.teacher.find(By.XPATH, "//button[@class='-review-exercises btn btn-primary']").click()
        self.teacher.sleep(5)

        self.teacher.find(By.XPATH, "//table[@class = 'exercise-table']")

        self.ps.test_updates['passed'] = True

    # Case C8075 - 048 - Teacher | Reorder selected assessments
    @pytest.mark.skipif(str(8075) not in TESTS, reason='Excluded')
    def test_teacher_reorder_selected_assessments(self):
        """Reorder selected assessments

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and select 'Add Homework'
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
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        
        self.teacher.sleep(3)

        # Open the select problem cards
        self.teacher.find(By.XPATH, "//button[@id = 'problems-select']").click()
        self.teacher.find(By.XPATH, "//span[@class = 'chapter-checkbox']").click()
        self.teacher.find(By.XPATH, "//button[@class='-show-problems btn btn-primary']").click()
        self.teacher.sleep(10)


        assert('3' == self.teacher.find(By.XPATH, "//div[@class = 'num total']/h2").text), \
            'Default total selections does not equal 3'

        assert('0' == self.teacher.find(By.XPATH, "//div[@class = 'num mine']/h2").text), \
            'my selections does not equal 0'

        # Choose a problem for the assignment
        elements = self.teacher.driver.find_elements_by_xpath("//div[@class = 'controls-overlay']")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(elements[0])
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action include']").click()

        #element = self.teacher.find(By.XPATH, "//div[@class = 'controls-overlay'][]")
        self.teacher.driver.execute_script("return arguments[0].scrollIntoView();", elements[1])
        self.teacher.driver.execute_script('window.scrollBy(0, -4500);')

        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(elements[1])
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action include']").click()
        self.teacher.sleep(2)

        assert('5' == self.teacher.find(By.XPATH, "//div[@class = 'num total']/h2").text), \
            'total selections does not equal 5'

        assert('2' == self.teacher.find(By.XPATH, "//div[@class = 'num mine']/h2").text), \
            'my selections does not equal 2'

        self.teacher.sleep(2)

        self.teacher.find(By.XPATH, "//button[@class='-review-exercises btn btn-primary']").click()
        self.teacher.sleep(5)

        self.teacher.find(By.XPATH, "//table[@class = 'exercise-table']")

        elem_1_text = self.teacher.find(By.XPATH, "//div[@class = 'openstax exercise-wrapper'][1]/div[@class = 'openstax-exercise-preview exercise-card non-interactive is-vertically-truncated panel panel-default']/div[@class = 'panel-body']/div[@class = 'openstax-question openstax-question-preview']/div[@class = 'openstax-has-html question-stem']").text

        self.teacher.find(By.XPATH, "//button[@class='btn-xs -move-exercise-up circle btn btn-default']").click()

        assert(elem_1_text != self.teacher.find(By.XPATH, "//div[@class = 'openstax exercise-wrapper'][1]/div[@class = 'openstax-exercise-preview exercise-card non-interactive is-vertically-truncated panel panel-default']/div[@class = 'panel-body']/div[@class = 'openstax-question openstax-question-preview']/div[@class = 'openstax-has-html question-stem']").text), \
            'Assessment order was not changed'

        assert(elem_1_text == self.teacher.find(By.XPATH, "//div[@class = 'openstax exercise-wrapper'][2]/div[@class = 'openstax-exercise-preview exercise-card non-interactive is-vertically-truncated panel panel-default']/div[@class = 'panel-body']/div[@class = 'openstax-question openstax-question-preview']/div[@class = 'openstax-has-html question-stem']").text), \
            'Assessment order was not changed'

        self.ps.test_updates['passed'] = True

    # Case C8076 - 049 - Teacher | Reordering assessments immediately changes the Problem Question list
    @pytest.mark.skipif(str(8076) not in TESTS, reason='Excluded')
    def test_teacher_reordering_assessments_immediately_changes_the_problem_question_list(self):
        """Reordering assessments immediately changes the Problem Question list

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and select 'Add Homework'
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
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        
        self.teacher.sleep(3)

        # Open the select problem cards
        self.teacher.find(By.XPATH, "//button[@id = 'problems-select']").click()
        self.teacher.find(By.XPATH, "//span[@class = 'chapter-checkbox']").click()
        self.teacher.find(By.XPATH, "//button[@class='-show-problems btn btn-primary']").click()
        self.teacher.sleep(10)


        assert('3' == self.teacher.find(By.XPATH, "//div[@class = 'num total']/h2").text), \
            'Default total selections does not equal 3'

        assert('0' == self.teacher.find(By.XPATH, "//div[@class = 'num mine']/h2").text), \
            'my selections does not equal 0'

        # Choose a problem for the assignment
        elements = self.teacher.driver.find_elements_by_xpath("//div[@class = 'controls-overlay']")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(elements[0])
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action include']").click()

        #element = self.teacher.find(By.XPATH, "//div[@class = 'controls-overlay'][]")
        self.teacher.driver.execute_script("return arguments[0].scrollIntoView();", elements[1])
        self.teacher.driver.execute_script('window.scrollBy(0, -4500);')

        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(elements[1])
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action include']").click()
        self.teacher.sleep(2)

        assert('5' == self.teacher.find(By.XPATH, "//div[@class = 'num total']/h2").text), \
            'total selections does not equal 5'

        assert('2' == self.teacher.find(By.XPATH, "//div[@class = 'num mine']/h2").text), \
            'my selections does not equal 2'

        self.teacher.sleep(2)

        self.teacher.find(By.XPATH, "//button[@class='-review-exercises btn btn-primary']").click()
        self.teacher.sleep(5)

        self.teacher.find(By.XPATH, "//table[@class = 'exercise-table']")

        elem_1_text = self.teacher.find(By.XPATH, "//table/tbody/tr/td[@class = 'ellipses']/span[@class = 'openstax-has-html'][1]").text

        self.teacher.find(By.XPATH, "//button[@class='btn-xs -move-exercise-up circle btn btn-default']").click()

        table = self.teacher.find(By.XPATH, "//table[@class = 'exercise-table']")

        self.teacher.driver.execute_script("return arguments[0].scrollIntoView();", table)
        self.teacher.driver.execute_script('window.scrollBy(0, -500);')

        rows = self.teacher.driver.find_elements_by_xpath("//table/tbody/tr/td[@class = 'ellipses']/span[@class = 'openstax-has-html']")

        assert(elem_1_text != rows[0].text), \
            'Assessment order was not changed'

        assert(elem_1_text == rows[1].text), \
            'Assessment order was not changed'

        self.teacher.sleep(2)

        self.ps.test_updates['passed'] = True

    # Case C8077 - 050 - Teacher | Add more assessments using the Add More... button
    @pytest.mark.skipif(str(8077) not in TESTS, reason='Excluded')
    def test_teacher_add_more_assessments_using_the_add_more_button(self):
        """Add more assessments using the Add More... button

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and select 'Add Homework'
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
        User is returned to the page where the assignment name, description, and open/due dates can be set. More selected problems are displayed.
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
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        
        self.teacher.sleep(3)

        # Open the select problem cards
        self.teacher.find(By.XPATH, "//button[@id = 'problems-select']").click()
        self.teacher.find(By.XPATH, "//span[@class = 'chapter-checkbox']").click()
        self.teacher.find(By.XPATH, "//button[@class='-show-problems btn btn-primary']").click()
        self.teacher.sleep(10)


        assert('3' == self.teacher.find(By.XPATH, "//div[@class = 'num total']/h2").text), \
            'Default total selections does not equal 3'

        assert('0' == self.teacher.find(By.XPATH, "//div[@class = 'num mine']/h2").text), \
            'my selections does not equal 0'

        # Choose a problem for the assignment
        element = self.teacher.find(By.XPATH, "//div[@class = 'controls-overlay'][1]")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(element)
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action include']").click()
        self.teacher.sleep(2)

        assert('4' == self.teacher.find(By.XPATH, "//div[@class = 'num total']/h2").text), \
            'total selections does not equal 4'

        assert('1' == self.teacher.find(By.XPATH, "//div[@class = 'num mine']/h2").text), \
            'my selections does not equal 1'

        self.teacher.sleep(2)

        self.teacher.find(By.XPATH, "//button[@class='-review-exercises btn btn-primary']").click()
        self.teacher.find(By.XPATH, "//button[@class='-add-exercises btn btn-default']").click()
        self.teacher.find(By.XPATH, "//button[@class='-show-problems btn btn-primary']").click()



        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(self.teacher.driver.find_elements_by_xpath("//div[@class = 'controls-overlay']")[1])
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action include']").click()
        self.teacher.sleep(2)

        assert('5' == self.teacher.find(By.XPATH, "//div[@class = 'num total']/h2").text), \
            'total selections does not equal 5'

        assert('2' == self.teacher.find(By.XPATH, "//div[@class = 'num mine']/h2").text), \
            'my selections does not equal 2'

        self.teacher.find(By.XPATH, "//button[@class='-review-exercises btn btn-primary']").click()
        self.teacher.find(By.XPATH, "//div[@class='openstax exercise-wrapper'][2]/div[@class='openstax-exercise-preview exercise-card non-interactive is-vertically-truncated panel panel-default']/div[@class='panel-heading']/span[@class='panel-title -exercise-header']/span[@class='exercise-number']")
        self.teacher.sleep(5)

        self.ps.test_updates['passed'] = True

    # Case C8078 - 051 - Teacher | Problem Question list is equal to the Tutor Selection bar numbers
    @pytest.mark.skipif(str(8078) not in TESTS, reason='Excluded')
    def test_teacher_(self):
        """Problem Question list is equal to the Tutor Selection bar numbers

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and select 'Add Homework'
        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select one of the non-introductory sections in one chapter
        Click the 'Show Problems' button
        Select at least one of the displayed problems
        Click the 'Next' button

        Expected Result:
        The number of total problems, my selections, and tutor selections in the Tutor Selection bar matches what the Problem Question list displays.
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
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        
        self.teacher.sleep(3)

        # Open the select problem cards
        self.teacher.find(By.XPATH, "//button[@id = 'problems-select']").click()
        self.teacher.find(By.XPATH, "//span[@class = 'chapter-checkbox']").click()
        self.teacher.find(By.XPATH, "//button[@class='-show-problems btn btn-primary']").click()
        self.teacher.sleep(10)


        assert('3' == self.teacher.find(By.XPATH, "//div[@class = 'num total']/h2").text), \
            'Default total selections does not equal 3'

        assert('0' == self.teacher.find(By.XPATH, "//div[@class = 'num mine']/h2").text), \
            'my selections does not equal 0'

        # Choose a problem for the assignment
        element = self.teacher.find(By.XPATH, "//div[@class = 'controls-overlay'][1]")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(element)
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action include']").click()
        self.teacher.sleep(2)

        assert('4' == self.teacher.find(By.XPATH, "//div[@class = 'num total']/h2").text), \
            'total selections does not equal 4'

        assert('1' == self.teacher.find(By.XPATH, "//div[@class = 'num mine']/h2").text), \
            'my selections does not equal 1'

        self.teacher.sleep(2)

        self.teacher.find(By.XPATH, "//button[@class='-review-exercises btn btn-primary']").click()

        self.teacher.sleep(2)

        problems = self.teacher.driver.find_elements_by_xpath("//table[@class='exercise-table']/tbody/tr")
        total = int(self.teacher.find(By.XPATH, "//div[@class='num total']/h2").text)

        assert(total == len(problems)), \
            'Number of assessments does not match tutor bar'

        self.ps.test_updates['passed'] = True

    # Case C8079 - 052 - Teacher | Remove an assessment from the order list
    @pytest.mark.skipif(str(8079) not in TESTS, reason='Excluded')
    def test_teacher_remove_an_assessment_from_the_order_list(self):
        """Remove an assessment from the order list

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and select 'Add Homework'
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
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        
        self.teacher.sleep(3)

        # Open the select problem cards
        self.teacher.find(By.XPATH, "//button[@id = 'problems-select']").click()
        self.teacher.find(By.XPATH, "//span[@class = 'chapter-checkbox']").click()
        self.teacher.find(By.XPATH, "//button[@class='-show-problems btn btn-primary']").click()
        self.teacher.sleep(10)


        assert('3' == self.teacher.find(By.XPATH, "//div[@class = 'num total']/h2").text), \
            'Default total selections does not equal 3'

        assert('0' == self.teacher.find(By.XPATH, "//div[@class = 'num mine']/h2").text), \
            'my selections does not equal 0'

        # Choose a problem for the assignment
        element = self.teacher.find(By.XPATH, "//div[@class = 'controls-overlay'][1]")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(element)
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action include']").click()
        self.teacher.sleep(2)

        assert('4' == self.teacher.find(By.XPATH, "//div[@class = 'num total']/h2").text), \
            'total selections does not equal 4'

        assert('1' == self.teacher.find(By.XPATH, "//div[@class = 'num mine']/h2").text), \
            'my selections does not equal 1'

        self.teacher.sleep(2)

        self.teacher.find(By.XPATH, "//button[@class='-review-exercises btn btn-primary']").click()

        self.teacher.sleep(2)

        problems = self.teacher.driver.find_elements_by_xpath("//table[@class='exercise-table']/tbody/tr")
        total = int(self.teacher.find(By.XPATH, "//div[@class='num total']/h2").text)

        assert(total == len(problems)), \
            'Number of assessments does not match tutor bar'

        self.teacher.find(By.XPATH, "//button[@class='btn-xs -remove-exercise circle btn btn-default']").click()
        self.teacher.find(By.XPATH, "//div[@class='popover-content']/div[@class='controls']/button[@class='btn btn-primary']").click()

        assert('exercise-table' not in self.teacher.driver.page_source), \
            'Problem list should not be present'

        self.ps.test_updates['passed'] = True

    # Case C8080 - 053 - Teacher | Remove an assessment from a homework from the Select Problems pane
    @pytest.mark.skipif(str(8080) not in TESTS, reason='Excluded')
    def test_teacher_remove_an_assessment_from_a_homework_from_the_select_problems_pane(self):
        """Remove an assessment from a homework from the Select Problems pane

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and select 'Add Homework'
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
        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Add Homework').click()
        assert('homeworks/new' in self.teacher.current_url()), \
            'Not on the add a homework page'
        
        self.teacher.sleep(3)

        # Open the select problem cards
        self.teacher.find(By.XPATH, "//button[@id = 'problems-select']").click()
        self.teacher.find(By.XPATH, "//span[@class = 'chapter-checkbox']").click()
        self.teacher.find(By.XPATH, "//button[@class='-show-problems btn btn-primary']").click()
        self.teacher.sleep(10)


        assert('3' == self.teacher.find(By.XPATH, "//div[@class = 'num total']/h2").text), \
            'Default total selections does not equal 3'

        assert('0' == self.teacher.find(By.XPATH, "//div[@class = 'num mine']/h2").text), \
            'my selections does not equal 0'

        # Choose a problem for the assignment
        elements = self.teacher.driver.find_elements_by_xpath("//div[@class = 'controls-overlay']")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(elements[0])
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action include']").click()

        #element = self.teacher.find(By.XPATH, "//div[@class = 'controls-overlay'][]")
        self.teacher.driver.execute_script("return arguments[0].scrollIntoView();", elements[1])
        self.teacher.driver.execute_script('window.scrollBy(0, -4500);')

        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(elements[1])
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action include']").click()
        self.teacher.sleep(2)

        self.teacher.find(By.XPATH, "//button[@class='-review-exercises btn btn-primary']").click()
        self.teacher.find(By.XPATH, "//button[@class='-add-exercises btn btn-default']").click()
        self.teacher.find(By.XPATH, "//button[@class='-show-problems btn btn-primary']").click()

        assert('5' == self.teacher.find(By.XPATH, "//div[@class = 'num total']/h2").text), \
            'total selections does not equal 5'

        assert('2' == self.teacher.find(By.XPATH, "//div[@class = 'num mine']/h2").text), \
            'my selections does not equal 2'

        element = self.teacher.find(By.XPATH, "//div[@class = 'controls-overlay'][1]")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(element)
        actions.perform()
        self.teacher.find(By.XPATH, "//div[@class = 'action exclude']").click()

        self.teacher.find(By.XPATH, "//button[@class='-review-exercises btn btn-primary']").click()
        self.teacher.sleep(5)

        assert('4' == self.teacher.find(By.XPATH, "//div[@class = 'num total']/h2").text), \
            'total selections does not equal 5'

        assert('1' == self.teacher.find(By.XPATH, "//div[@class = 'num mine']/h2").text), \
            'my selections does not equal 2'

        self.ps.test_updates['passed'] = True

    # Case C8081 - 054 - Teacher | Remove an assessment from a homework from the Add Homework Assignment pane
    @pytest.mark.skipif(str(8081) not in TESTS, reason='Excluded')
    def test_teacher_remove_an_assessment_from_a_homework_from_the_add_homework_assignment_pane(self):
        """Remove an assessment from a homework from the Add Homework Assignment pane

        Steps:
        From the dashboard, click on the 'Add Assignment' drop down menu and select 'Add Homework'
        Click the '+ Select Problems' button
        Click on any of the chapters to display sections within the chapter
        Select one of the non-introductory sections in one chapter
        Click the 'Show Problems' button
        Select at least one of the displayed problems
        Click the 'Next' button
        Click the X button on at least one of the problems
        Click 'OK' on the dialog box that appears

        Expected Result:
        Changes are reflected on the page. If all problems are deleted, the Problem Question list disappears. Otherwise, the question is removed and the Problem Question list reflects the change.
        
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

        self.ps.test_updates['passed'] = True
        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # Case C8082 - 055 - Teacher | Change all fields in an unopened, published homework
    @pytest.mark.skipif(str(8082) not in TESTS, reason='Excluded')
    def test_teacher_change_all_fields_in_an_unopened_published_homework(self):
        """Change all fields in an unopened, published homework

        Steps:
        From the dashboard, click on a published, unopened homework
        Click on the 'Edit Assignment' button
        Edit the text in the text box named 'Assignment name'
        Edit the text in the text box named 'Description or special instructions'
        Edit the open and due dates for the assignment
        Edit the 'Show feedback' drop down menu option
        Click the 'Publish' button

        Expected Result:
        The user is returned to the dashboard. Changes to the homework are seen.
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

        self.ps.test_updates['passed'] = True

    # Case C8083 - 056 - Teacher | Change all fields in a draft homework
    @pytest.mark.skipif(str(8083) not in TESTS, reason='Excluded')
    def test_teacher_change_all_fields_in_a_draft_homework(self):
        """Change all fields in a draft homework

        Steps:
        From the dashboard, click on a draft homework
        Edit the text in the text box named 'Assignment name'
        Edit the text in the text box named 'Description or special instructions'
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

        self.ps.test_updates['passed'] = True

    # Case C8084 - 057 - Teacher | Change the name, description, due dtaes, and feedback timing in an opened homework
    @pytest.mark.skipif(str(8084) not in TESTS, reason='Excluded')
    def test_teacher_change_the_name_description_due_dates_and_feedback_timing_in_an_opened_homework(self):
        """Change the name, description, due dates, and feedback timing in an opened homework

        Steps:
        From the dashboard, click on an opened homework
        Click on the 'Edit Assignment' button
        Edit the text in the text box named 'Assignment name'
        Edit the text in the text box named 'Description or special instructions'
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

        self.ps.test_updates['passed'] = True

