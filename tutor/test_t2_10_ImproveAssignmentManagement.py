"""Tutor v2, Epic 10 - Improve Assignment Management."""

import inspect
import json
import os
import pytest
import unittest
import datetime

from pastasauce import PastaSauce, PastaDecorator
from random import randint  # NOQA
from selenium.webdriver.common.by import By  # NOQA
from selenium.webdriver.support import expected_conditions as expect  # NOQA
from staxing.assignment import Assignment  # NOQA
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.action_chains import ActionChains

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Teacher, Student  # NOQA

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': '50.0',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    # str([14675, 14676, 14677, 14678, 14800,
    #      14680, 14681, 14682, 14683, 14801,
    #      14802, 14803, 14804, 14805, 14685,
    #      14686, 14687, 14688, 14689])  # NOQA
    # these test cases work
    # str([14675, 14676, 14677, 14678, 14683,
    #      14801, 14803, 14804, 14805, 14686,
    #      14688])
    # thses have issues with scrolling in the table
    str([14800, 14680, 14681])
    # these are not implemented features
    # str([14682, 14802, 14685, 14689])
    # thses aren't tested because issues with the add hw helper
    # str([14687])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestImproveAssignmentManagement(unittest.TestCase):
    """T2.10 - Improve Assignment Management."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.teacher = Teacher(
            use_env_vars=True,
            # pasta_user=self.ps,
            # capabilities=self.desired_capabilities
        )
        self.student = Student(
            username=os.getenv('STUDENT_USER'),
            password=os.getenv('STUDENT_PASSWORD'),
            site='https://tutor-qa.openstax.org',
            existing_driver=self.teacher.driver,
            # pasta_user=self.ps,
            # capabilities=self.desired_capabilities
        )

    def tearDown(self):
        """Test destructor."""
        self.ps.update_job(job_id=str(self.teacher.driver.session_id),
                           **self.ps.test_updates)
        try:
            self.teacher.delete()
        except:
            pass

    # 14675 - 001 - Teacher | Set when feedback is available
    @pytest.mark.skipif(str(14675) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_set_when_feedback_is_available_14675(self):
        """Set when feedback is available.

        Steps:
        Login as a teacher
        If the user has more than one course, click on a Tutor course name
        Create a new homework assignment
        Click on the bar under "Show Feedback"
        Select an option

        Expected Result:
        The user is able to set when feedback is available
        """
        self.ps.test_updates['name'] = 't2.10.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t2', 't2.10', 't2.10.001', '14675']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.select_course(appearance='biology')
        self.teacher.driver.find_element(
            By.XPATH, '//button[contains(@class,"dropdown-toggle")]').click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        self.teacher.sleep(1)
        feedback_option = self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'feedback-select')
            )
        )
        feedback_option.click()
        self.teacher.driver.find_element(
            By.XPATH, '//select/option[@value="immediate"]').click()
        feedback_option.click()
        self.teacher.driver.find_element(
            By.XPATH, '//select/option[@value="due_at"]').click()
        self.ps.test_updates['passed'] = True

    # 14676 - 002 - Teacher | Set open and due times for a reading assignment
    @pytest.mark.skipif(str(14676) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_set_open_and_due_times_for_reading_assignment_14676(self):
        """Set open and due times for a reading assignment.

        Steps:
        Login as a teacher
        If the user has more than one course, click on a Tutor course name
        Create a new reading assignment
        Click on the text box for the open time
        Enter desired time
        Click on the text box for the due time
        Enter desired time

        Expected Result:
        The user is able to set open and due times
        """
        self.ps.test_updates['name'] = 't2.10.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t2', 't2.10', 't2.10.002', '14676']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.select_course(appearance='biology')
        self.teacher.driver.find_element(
            By.XPATH, '//button[contains(@class,"dropdown-toggle")]').click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Reading').click()
        self.teacher.sleep(1)
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        open_time = self.teacher.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"-assignment-open-time")]' +
            '//input[@name="time"]'
        )
        open_time.clear()
        open_time.send_keys('12:34a')
        close_time = self.teacher.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"-assignment-due-time")]' +
            '//input[@name="time"]'
        )
        close_time.clear()
        close_time.send_keys('5:67p')
        self.ps.test_updates['passed'] = True

    # 14677 - 003 - Teacher | Set open and due times for a homework assignment
    @pytest.mark.skipif(str(14677) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_set_open_and_due_times_for_hw_assignment_14677(self):
        """Set open and due times for a homework assignment.

        Steps:
        Login as a teacher
        If the user has more than one course, click on a Tutor course name
        Create a new homework assignment
        Click on the text box for the open time
        Enter desired time
        Click on the text box for the due time
        Enter desired time

        Expected Result:
        The user is able to set open and due times
        """
        self.ps.test_updates['name'] = 't2.10.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t2', 't2.10', 't2.10.003', '14677']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.select_course(appearance='biology')
        self.teacher.driver.find_element(
            By.XPATH, '//button[contains(@class,"dropdown-toggle")]').click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        self.teacher.sleep(1)
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        open_time = self.teacher.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"-assignment-open-time")]' +
            '//input[@name="time"]'
        )
        open_time.clear()
        open_time.send_keys('12:34a')
        close_time = self.teacher.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"-assignment-due-time")]' +
            '//input[@name="time"]'
        )
        close_time.clear()
        close_time.send_keys('5:67p')
        self.ps.test_updates['passed'] = True

    # 14678 - 004 - Teacher | Set open and due times for an external assignment
    @pytest.mark.skipif(str(14678) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_set_open_and_due_time_for_external_assignment_14678(self):
        """Set open and due times for an external assignment.

        Steps:
        Login as a teacher
        If the user has more than one course, click on a Tutor course name
        Create a new external assignment
        Click on the text box for the open time
        Enter desired time
        Click on the text box for the due time
        Enter desired time

        Expected Result:
        The user is able to set open and due times
        """
        self.ps.test_updates['name'] = 't2.10.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t2', 't2.10', 't2.10.004', '14678']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.select_course(appearance='biology')
        self.teacher.driver.find_element(
            By.XPATH, '//button[contains(@class,"dropdown-toggle")]').click()
        self.teacher.driver.find_element(
            By.LINK_TEXT, 'Add External Assignment').click()
        self.teacher.sleep(1)
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        open_time = self.teacher.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"-assignment-open-time")]' +
            '//input[@name="time"]'
        )
        open_time.clear()
        open_time.send_keys('12:34a')
        close_time = self.teacher.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"-assignment-due-time")]' +
            '//input[@name="time"]'
        )
        close_time.clear()
        close_time.send_keys('5:67p')
        self.ps.test_updates['passed'] = True

    # element doesn't exist until scrolled into view.
    # But scrolling is messing up the table
    # 14800 - 005 - Teacher | Make an assignment on time for a specific student
    @pytest.mark.skipif(str(14800) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_make_assignment_on_time_for_specific_student_14800(self):
        """Make an assignment on time for a specific student.

        Steps:
        Login as a teacher
        If the user has more than one course, click on a Tutor course name
        Click "Student Scores" from calendar dashboard
        Click on the orange triangle in the upper right corner of a progress
        cell
        Click "Accept late score"

        Expected Result:
        The late score replaces the score at due date
        """
        self.ps.test_updates['name'] = 't2.10.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t2', 't2.10', 't2.10.005', '14800']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.select_course(appearance='college_physics')
        self.teacher.driver.find_element(
            By.LINK_TEXT, 'Student Scores').click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="course-scores-container"]')
            )
        )
        assignments = self.teacher.driver.find_elements(
            By.XPATH,
            "//span[contains(@aria-describedby,'header-cell-title')]")
        for i in range(len(assignments)//4):
            try:
                self.teacher.driver.find_element(
                    By.XPATH, '//div[@class="late-caret"]'
                ).click()
                self.teacher.driver.find_element(
                    By.XPATH,
                    '//button[contains(text(),"Accept late score")]'
                ).click()
                break
            except (NoSuchElementException, ElementNotVisibleException):
                if i >= (len(assignments)//4)-1:
                    print("No Late assignments for this class :(")
                    raise Exception
                # try to drag scroll bar instead of scrolling
                scroll_bar = self.teacher.driver.find_element(
                    By.XPATH,
                    '//div[contains(@class,"ScrollbarLayout_faceHorizontal")]')
                actions = ActionChains(self.teacher.driver)
                actions.move_to_element(scroll_bar)
                actions.click_and_hold()
                actions.move_by_offset(50, 0)
                actions.release()
                actions.perform()
        self.ps.test_updates['passed'] = True

    # scrolling is messing up the table
    # 14680 - 006 - Teacher | View score at due date
    @pytest.mark.skipif(str(14680) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_view_score_at_due_date_14680(self):
        """View score at due date.

        Steps:
        Login as a teacher
        If the user has more than one course, click on a Tutor course name
        Click "Student Scores" from the calendar dashboard
        (Teacher may also accept late score, and then view score at due date by
        clicking gray triangle in the corner of the table cell)

        Expected Result:
        The user is presented with scores at due date
        """
        self.ps.test_updates['name'] = 't2.10.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t2', 't2.10', 't2.10.006', '14680']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.select_course(appearance='college_physics')
        self.teacher.driver.find_element(
            By.LINK_TEXT, 'Student Scores').click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="course-scores-container"]')
            )
        )
        assignments = self.teacher.driver.find_elements(
            By.XPATH,
            "//span[contains(@aria-describedby,'header-cell-title')]")
        for i in range(len(assignments)//4): ##########
            try:
                self.teacher.driver.find_element(
                    By.XPATH, '//div[@class="late-caret accepted"]'
                ).click()
                self.teacher.driver.find_element(
                    By.XPATH,
                    '//div[contains(@class,"late-status")]' +
                    '//span[contains(text(),"due date")]'
                )
                break
            except (NoSuchElementException, ElementNotVisibleException):
                if i >= (len(assignments)//4)-1:
                    print("No Late assignments for this class :(")
                    raise Exception
                # try to drag scroll bar instead of scrolling
                scroll_bar = self.teacher.driver.find_element(
                    By.XPATH,
                    '//div[contains(@class,"ScrollbarLayout_faceHorizontal")]')
                actions = ActionChains(self.teacher.driver)
                actions.move_to_element(scroll_bar)
                actions.click_and_hold()
                actions.move_by_offset(50, 0)
                actions.release()
                actions.perform()
        self.ps.test_updates['passed'] = True

    # scrolling is messing up the table
    # 14681 - 007 - Teacher | View current score
    @pytest.mark.skipif(str(14681) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_view_current_score_14681(self):
        """View current score.

        Steps:
        Login as a teacher
        If the user has more than one course, click on a Tutor course name
        Click "Student Scores" from the calendar dashboard
        Click on the orange flag in the upper right corner of a progress cell
        for the desired student

        Expected Result:
        The user is presented with current score
        """
        self.ps.test_updates['name'] = 't2.10.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t2', 't2.10', 't2.10.007', '14681']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.ps.test_updates['name'] = 't2.10.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t2', 't2.10', 't2.10.006', '14680']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.select_course(appearance='college_physics')
        self.teacher.driver.find_element(
            By.LINK_TEXT, 'Student Scores').click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="course-scores-container"]')
            )
        )
        assignments = self.teacher.driver.find_elements(
            By.XPATH,
            "//span[contains(@aria-describedby,'header-cell-title')]")
        for i in range(len(assignments)//4):
            try:
                self.teacher.driver.find_element(
                    By.XPATH, '//div[@class="score"]')
                break
            except (NoSuchElementException):
                if i >= (len(assignments)//4)-1:
                    print("No Late assignments for this class :(")
                    raise Exception
                # try to drag scroll bar instead of scrolling
                scroll_bar = self.teacher.driver.find_element(
                    By.XPATH,
                    '//div[contains(@class,"ScrollbarLayout_faceHorizontal")]')
                actions = ActionChains(self.teacher.driver)
                actions.move_to_element(scroll_bar)
                actions.click_and_hold()
                actions.move_by_offset(50, 0)
                actions.release()
                actions.perform()
        self.ps.test_updates['passed'] = True

    # 14682 - 008 - Teacher | Set points per problem based on difficulty
    @pytest.mark.skipif(str(14682) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_set_points_per_problem_based_on_difficulty_14682(self):
        """Set points per problem based on difficulty.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['passed'] = False

        # # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 14683 - 009 - Teacher | Delete an open assignment
    @pytest.mark.skipif(str(14683) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_delete_an_open_assignment_14683(self):
        """Delete an open assignment.

        Steps:
        Login as a teacher
        If the user has more than one course, click on a Tutor course name
        Click on an open assignment
        Click "Edit Assignment"
        Click "Delete Assignment"
        Click "Yes"

        Expected Result:
        The open assignment is deleted
        """
        self.ps.test_updates['name'] = 't2.10.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t2', 't2.10', 't2.10.009', '14683']
        self.ps.test_updates['passed'] = False

        # create an open event
        self.teacher.login()
        self.teacher.select_course(appearance='physics')
        assignment_name = "event_to_delete"
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

    # 14801 - 010 - Student | A deleted open assignment that the student has
    # not worked on is grayed out and is marked "Withdrawn"
    @pytest.mark.skipif(str(14801) not in TESTS, reason='Excluded')  # NOQA
    def test_student_deleted_open_assignment_that_student_has_not_14801(self):
        """Deleted open assignment is grayed out and is marked "Withdrawn".

        Steps:
        Login as a student
        If the user has more than one course, click on a Tutor course name

        Expected Result:
        On the student dashboard, a deleted open assignment that the student
        has not worked on is grayed out and is marked "Withdrawn"
        """
        self.ps.test_updates['name'] = 't2.10.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t2', 't2.10', 't2.10.010', '14801']
        self.ps.test_updates['passed'] = False

        # create a homework assignement
        self.teacher.login()
        self.teacher.select_course(appearance='physics')
        assignment_name = "event-010"
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
        # delete the assignment
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
        self.teacher.logout()
        # login as a student to view the assignment
        self.student.login()
        self.teacher.select_course(appearance='physics')
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.XPATH,
                 '//div[@class="task row event deleted"]' +
                 '//span[contains(text(),"' + assignment_name + '")]')
            )
        )
        self.ps.test_updates['passed'] = True

    # this case is not an implemented feature?
    # 14802 - 011 - Student | A deleted open assignment that the student has
    # worked on is not grayed out but is marked "Withdrawn"
    @pytest.mark.skipif(str(14802) not in TESTS, reason='Excluded')  # NOQA
    def test_student_deleted_open_assignment_that_student_has_work_14802(self):
        """Deleted open assignment is not grayed out but is marked "Withdrawn".

        Steps:
        Login as a student
        If the user has more than one course, click on a Tutor course name

        Expected Result:
        On the student dashboard, a deleted open assignment that the student
        has worked on is not grayed out but is marked "Withdrawn"
        """
        # self.ps.test_updates['name'] = 't2.10.011' \
        #     + inspect.currentframe().f_code.co_name[4:]
        # self.ps.test_updates['tags'] = ['t2', 't2.10', 't2.10.011', '14802']
        self.ps.test_updates['passed'] = False

        # # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 14803 - 012 - Student | Delete withdrawn assignments
    @pytest.mark.skipif(str(14803) not in TESTS, reason='Excluded')  # NOQA
    def test_student_delete_withdrawn_assignments_14803(self):
        """Delete withdrawn assignments.

        Steps:
        Login as a student
        If the user has more than one course, click on a Tutor course name
        Click on the X for the withdrawn assignment

        Expected Result:
        Withdrawn assignment is deleted
        """
        self.ps.test_updates['name'] = 't2.10.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t2', 't2.10', 't2.10.012', '14803']
        self.ps.test_updates['passed'] = False

        # create a homework assignement
        self.teacher.login()
        self.teacher.select_course(appearance='physics')
        assignment_name = "event-010"
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
        # delete the assignment
        try:
            self.teacher.driver.find_element(
                By.XPATH,
                '//label[contains(@data-title,"' + assignment_name + '")]'
            ).click()
        except NoSuchElementException:
            self.teacher.driver.find_element(
                By.XPATH,
                '//a[contains(@class,"calendar-header-control next")]'
            ).click()
            self.teacher.driver.find_element(
                By.XPATH,
                '//label[contains(@data-title,"' + assignment_name + '")]'
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
        self.teacher.logout()
        # login as a student to view the assignment
        self.student.login()
        self.teacher.select_course(appearance='physics')
        # delete a deleted event (not necessarily the one just created)
        initial_deleted = self.student.driver.find_elements(
            By.XPATH, '//button[contains(@class,"-hide-button")]')
        self.student.driver.find_element(
            By.XPATH,
            '//button[contains(@class,"-hide-button")]'
        ).click()
        self.student.sleep(0.5)
        final_deleted = self.student.driver.find_elements(
            By.XPATH, '//button[contains(@class,"-hide-button")]')
        assert(len(initial_deleted) == len(final_deleted) + 1), \
            'withdrawn event not deleted'
        self.ps.test_updates['passed'] = True

    # 14804 - 013 - Teacher | Move the due date to a later date for an open
    # assignment
    @pytest.mark.skipif(str(14804) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_move_the_due_date_to_a_later_date_for_an_open_14804(self):
        """Move the due date to a later date for an open assignment.

        Steps:
        Login as a teacher
        If the user has more than one course, click on a Tutor course name
        Click on an open assignment
        Click on the text box for due date
        Select a later date on the calendar

        Expected Result:
        The user is able to move the due date to a later date for an open
        assignment
        """
        self.ps.test_updates['name'] = 't2.10.013' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t2', 't2.10', 't2.10.013', '14804']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.select_course(appearance='physics')
        assignment_name = "event_to_delete"
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
        # change date
        today = datetime.date.today()
        closes_on = (today + datetime.timedelta(days=10)).strftime('%m/%d/%Y')
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
        self.ps.test_updates['passed'] = True

    # 14805 - 014 - Teacher | Move the due date to an earlier date for an open
    # assignment
    @pytest.mark.skipif(str(14805) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_move_the_due_date_to_an_earlier_date_for_open_14805(self):
        """Move the due date to an earlier date for an open assignment.

        Steps:
        Login as a teacher
        If the user has more than one course, click on a Tutor course name
        Click on an open assignment
        Click on the text box for the due date
        Select an earlier date on the calendar (but after the open date)

        Expected Result:
        The assignment is moved to an earlier date
        """
        self.ps.test_updates['name'] = 't2.10.014' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t2', 't2.10', 't2.10.014', '14805']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.select_course(appearance='physics')
        assignment_name = "event_to_delete"
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=10)).strftime('%m/%d/%Y')
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
        # change date
        today = datetime.date.today()
        closes_on = (today + datetime.timedelta(days=6)).strftime('%m/%d/%Y')
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
        self.ps.test_updates['passed'] = True

    # 14685 - 015 - Student | View inital quiz about 2-step questions and
    # spaced practice
    @pytest.mark.skipif(str(14685) not in TESTS, reason='Excluded')  # NOQA
    def test_student_view_initial_quiz_about_2_step_questions_and_14685(self):
        """View inital quiz about 2-step questions and spaced practice.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['passed'] = False

        # # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 14686 - 016 - Student | A help link explains why two-step problems
    @pytest.mark.skipif(str(14686) not in TESTS, reason='Excluded')  # NOQA
    def test_student_a_help_link_explains_why_two_step_problems_14686(self):
        """A help link explains why two-step problems.

        Steps:
        Login as a student
        If the user has more than one course, click on a Tutor course name
        Click on a homework, reading assignment, or practice
        Enter text into the free response text box
        Click "Answer"
        Click on "Why?" next to the message "Now choose from one of the
        following options"

        Expected Result:
        The user is presented with information about why two-step problems
        """
        self.ps.test_updates['name'] = 't2.10.016' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t2', 't2.10', 't2.10.016', '14686']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.login()
        self.student.select_course(appearance='physics')
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//button[contains(@aria-describedby,' +
                 '"progress-bar-tooltip")]')
            )
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[contains(@class,"task-breadcrumbs")]')
            )
        )
        # work homework until a free response problem is found.
        sections = self.student.driver.find_elements(
            By.XPATH, '//span[contains(@class,"openstax-breadcrumbs-step")]'
        )
        for i in range(len(sections)):
            try:
                # if the question is two part must answer free response first
                element = self.student.driver.find_element(
                    By.TAG_NAME, 'textarea')
            except NoSuchElementException:
                # click on the next breadcrumb
                if i == len(sections):
                    print("no two part questions in the homework")
                    raise Exception
                else:
                    sections_new = self.student.driver.find_elements(
                        By.XPATH, '//div[@class="openstax-breadcrumbs-step"]')
                    sections_new[i+1].click()
            else:
                answer_text = "answer"
                for i in answer_text:
                    element.send_keys(i)
                self.student.wait.until(
                    expect.element_to_be_clickable(
                        (By.XPATH, '//button/span[contains(text(),"Answer")]')
                    )
                ).click()
                actions = ActionChains(self.student.driver)
                why = self.teacher.driver.find_element(
                    By.XPATH, '//span[@class="text-info"]')
                self.teacher.driver.execute_script(
                    'return arguments[0].scrollIntoView();', why)
                self.teacher.driver.execute_script('window.scrollBy(0, -80);')
                actions.move_to_element(why)
                actions.perform()
                self.teacher.driver.find_element(
                    By.XPATH,
                    '//div[@class="popover-content"]' +
                    '//b[contains(text(),' +
                    '"Why do you ask me to answer twice?")]')
                break
        self.ps.test_updates['passed'] = True

    # NOT DONE
    # 14687 - 017 - System | Include info about two step problems and spaced
    # practice
    @pytest.mark.skipif(str(14687) not in TESTS, reason='Excluded')  # NOQA
    def test_system_include_info_about_two_step_problems_and_space_14687(self):
        """Include information about two step problems and spaced practice.

        Steps:
        Login as a student
        If the user has more than one course, click on a Tutor course name
        Click on a homework or reading assignment
        Enter text into the free response text box
        Click "Answer"
        Click "Why?" next to the message "Now choose from one of the following
        options"
        Then continue working the homework until a spaced practice question
        comes up
        click on the info icon in the top right of the question box next to
        spaced practice

        Expected Result:
        The message "We ask for your own response first because recalling an
        answer from memory helps your learning last longer.
        Then, we give you multiple-choice options so you can get immediate
        feedback" is displayed
        For spaced practice a separate message is displayed
        """
        self.ps.test_updates['name'] = 't2.10.017' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t2', 't2.10', 't2.10.017', '14687']
        self.ps.test_updates['passed'] = False

        # create a homework
        self.teacher.login()
        self.teacher.select_course(appearance='physics')
        assignment_name = "homework-017"
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=10)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(assignment='homework',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'status': 'publish',
                                        'problems': {'1.1': (1, 2), },
                                        'feedback': 'non-immeditae',
                                    })
        self.teacher.logout()
        # login as student to work the homework
        self.student.login()
        self.student.select_course(appearance='physics')
        self.student.driver.find_element(
            By.XPATH, '//span[contains(text(), "'+assignment_name+'")]'
        ).click()
        # work problems untill a free response question is found
        sections = self.student.driver.find_elements(
            By.XPATH, '//span[contains(@class,"openstax-breadcrumbs-step")]'
        )
        for i in range(len(sections)):
            try:
                # if the question is two part must answer free response first
                element = self.student.driver.find_element(
                    By.TAG_NAME, 'textarea')
                answer_text = "answer"
                for i in answer_text:
                    element.send_keys(i)
                self.student.wait.until(
                    expect.element_to_be_clickable(
                        (By.XPATH, '//button/span[contains(text(),"Answer")]')
                    )
                ).click()
                actions = ActionChains(self.student.driver)
                why = self.teacher.driver.find_element(
                    By.XPATH, '//span[@class="text-info"]')
                actions.move_to_element(why)
                actions.perform()
                self.teacher.driver.find_element(
                    By.XPATH,
                    '//div[@class="popover-content"]' +
                    '//b[contains(text(),' +
                    '"Why do you ask me to answer twice?")]')
                break
            except NoSuchElementException:
                # click on the next breadcrumb
                if i == len(sections):
                    print("no two part questions in the homework")
                    raise Exception
                sections_new = self.student.driver.find_elements(
                    By.XPATH, '//div[@class="openstax-breadcrumbs-step"]')
                sections_new[i+1].click()
        # click on the last problems to find a spaced practice
        sections = self.student.driver.find_elements(
            By.XPATH, '//div[@class="openstax-breadcrumbs-step"]'
        )
        sections[-2].click()

        self.ps.test_updates['passed'] = True

    # 14688 - 018 - Student | When working a question there is a link back to
    # the content for help
    @pytest.mark.skipif(str(14688) not in TESTS, reason='Excluded')  # NOQA
    def test_student_when_working_a_question_there_is_a_link_back_14688(self):
        """When working a question there is a link back to the content for help.

        Steps:
        Login as a student
        If the user has more than one course, click on a Tutor course name
        Click on a section to practice
        Scroll down to the very bottom of the assessment card

        Expected Result:
        The user is presented with a link back to the content
        """
        self.ps.test_updates['name'] = 't2.10.018' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t2', 't2.10', 't2.10.018', '14688']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.login()
        self.student.select_course(appearance='physics')
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//button[contains(@aria-describedby,' +
                 '"progress-bar-tooltip")]')
            )
        ).click()
        chapter = self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//a[@class="view-reference-guide"]//span[1]')
            )
        )
        chapter_num = chapter.text
        self.teacher.driver.execute_script(
            'return arguments[0].scrollIntoView();', chapter)
        chapter.click()
        window_with_book = self.student.driver.window_handles[1]
        self.student.driver.switch_to_window(window_with_book)
        book = self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//span[contains(@class,"chapter-section")]')
            )
        )
        assert('book' in self.teacher.current_url()), \
            'Not viewing the textbook PDF'
        assert(chapter_num == book.get_attribute("data-chapter-section")), \
            'Not viewing the textbook PDF'
        self.ps.test_updates['passed'] = True

    # 14689 - 019 - Student | Ask for credit for late work
    @pytest.mark.skipif(str(14689) not in TESTS, reason='Excluded')  # NOQA
    def test_student_ask_for_credit_for_late_work_14689(self):
        """Ask for credit for late work.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['passed'] = False

        # # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
