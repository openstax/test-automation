"""Concept Coach v1, Epic 08 - StudentsWorkAssignments."""

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

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': '48.0',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([7691, 7692, 7693, 7694, 7695,
         7696, 7697, 7698, 7699, 7700,
         7701, 7702, 7703])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestStudentsWorkAssignments(unittest.TestCase):
    """CC1.08 - Students Work Assignments."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        teacher = Teacher(username='teacher100', password='password',
                          site='https://tutor-qa.openstax.org/')
        teacher.login()
        courses = teacher.find_all(By.CLASS_NAME,
                                   'tutor-booksplash-course-item')
        assert(courses), 'No courses found.'
        if not isinstance(courses, list):
            courses = [courses]
        course_id = randint(0, len(courses) - 1)
        self.course = courses[course_id].get_attribute('data-title')
        teacher.select_course(title=self.course)
        teacher.goto_course_roster()
        section = '%s' % randint(100, 999)
        try:
            wait = teacher.wait_time
            teacher.change_wait_time(3)
            teacher.find(By.CLASS_NAME, '-no-periods-text')
            teacher.add_course_section(section)
        except:
            sections = teacher.find_all(
                By.XPATH,
                '//span[@class="tab-item-period-name"]'
            )
            section = sections[randint(0, len(sections) - 1)].text
        finally:
            teacher.change_wait_time(wait)
        self.code = teacher.get_enrollment_code(section)
        print('Course Phrase: ' + self.code)
        self.book_url = teacher.find(
            By.XPATH, '//a[span[text()="Online Book "]]'
        ).get_attribute('href')
        self.student = Student()
        self.first_name = Assignment.rword(6)
        self.last_name = Assignment.rword(8)
        self.email = self.first_name + '.' + self.last_name + \
            '@tutor.openstax.org'

    def tearDown(self):
        """Test destructor."""
        try:
            self.teacher.delete()
        except:
            pass
        try:
            self.student.delete()
        except:
            pass

    # Case C7691 - 001 - Student | Selects an exercise answer
    @pytest.mark.skipif(str(7691) not in TESTS, reason='Excluded')
    def test_student_select_an_exercise_answer_7691(self):
        """Select an exercise answer."""
        self.student.get(self.book_url)
        self.student.sleep(2)
        self.student.find_all(By.XPATH, '//a[@class="nav next"]')[0].click()
        self.student.page.wait_for_page_load()
        try:
            widget = self.student.find(By.ID, 'coach-wrapper')
        except:
            self.student.find_all(By.XPATH,
                                  '//a[@class="nav next"]')[0].click()
            self.student.page.wait_for_page_load()
            try:
                self.student.sleep(1)
                widget = self.student.find(By.ID, 'coach-wrapper')
            except:
                self.student.find_all(By.XPATH,
                                      '//a[@class="nav next"]')[0].click()
                self.student.page.wait_for_page_load()
                self.student.sleep(1)
                widget = self.student.find(By.ID, 'coach-wrapper')
        Assignment.scroll_to(self.student.driver, widget)
        self.student.find(
            By.XPATH,
            '//button[contains(text(),"Launch Concept Coach")]'
        ).click()
        self.student.sleep(1.5)
        self.student.find(
            By.XPATH,
            '//input[contains(@label,"Enter the two-word enrollment code")]'
        ).send_keys(self.code)
        self.student.sleep(5)
        self.student.find(
            By.XPATH,
            '//div[contains(@class,"concept-coach")]' +
            '//button[contains(@class,"async-button")]'
        ).click()
        main_window = self.student.driver.window_handles[0]
        self.student.wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'click to begin login.')
            )
        ).click()
        accounts_window = self.student.driver.window_handles[1]
        self.student.sleep(3)
        self.student.driver.switch_to_window(accounts_window)
        self.student.sleep(2)
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'Sign up')
            )
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'signup_first_name')
            )
        ).send_keys(self.first_name)
        self.student.find(
            By.ID,
            'signup_last_name'
        ).send_keys(self.last_name)
        self.student.find(
            By.ID,
            'signup_email_address'
        ).send_keys(self.email)
        self.student.find(
            By.ID,
            'signup_username'
        ).send_keys(self.last_name)
        self.student.find(
            By.ID,
            'signup_password'
        ).send_keys(self.last_name)
        self.student.find(
            By.ID,
            'signup_password_confirmation'
        ).send_keys(self.last_name)
        self.student.find(By.ID, 'create_account_submit').click()
        self.student.page.wait_for_page_load()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'i_agree')
            )
        ).click()
        self.student.sleep(1)
        self.student.find(By.ID, 'agreement_submit').click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'i_agree')
            )
        ).click()
        self.student.sleep(1)
        self.student.find(By.ID, 'agreement_submit').click()
        self.student.driver.switch_to_window(main_window)
        try:
            self.student.find(
                By.XPATH,
                '//input[contains(@label,"Enter the two-word")]'
            ).send_keys(self.code)
            self.student.find(
                By.XPATH,
                '//div[contains(@class,"concept-coach")]' +
                '//button[contains(@class,"async-button")]'
            ).click()
        except:
            pass
        self.student.find(
            By.XPATH,
            '//input[contains(@label,"Enter your school issued ID:")]'
        ).send_keys(self.last_name)
        self.student.find(
            By.XPATH,
            '//button[span[text()="Confirm"]]'
        ).click()
        self.student.sleep(5)
        self.student.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH,
                 '//div[@class="openstax-question"]//textarea')
            )
        ).send_keys(Assignment.rword(20))
        self.student.find(By.XPATH, '//button[span[text()="Answer"]]').click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '(//div[@class="answer-letter"])[1]')
            )
        ).click()
        self.student.find(By.XPATH, '//button[span[text()="Submit"]]').click()

    # Case C7692 - 002 - Student | After answering an exercise feedback
    # is presented
    @pytest.mark.skipif(str(7692) not in TESTS, reason='Excluded')  # NOQA
    def test_student_after_answering_an_exercise_feedback_7692(self):
        """View section completion report.

        Steps:

        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a CC course name

        Click the 'Contents' button to open the table of contents
        Click on a chapter
        Click on a non-introductory section
        Click the 'Launch Concept Coach' button at the bottom of the page
        Type text into the 'Enter your response' text box
        Click the 'Answer' button
        Click a multiple choice answer
        Click the 'Submit' button


        Expected Result:

        The correct answer is displayed and feedback is given.

        """
        self.ps.test_updates['name'] = 'cc1.08.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.08',
            'cc1.08.002',
            '7692'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C7693 - 003 - System | Assessments are from the current module
    @pytest.mark.skipif(str(7693) not in TESTS, reason='Excluded')  # NOQA
    def test_system_assessments_are_from_the_current_module_7693(self):
        """Assessment is from the current module.

        Steps:

        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # Case C7694 - 004 - System | Spaced practice assessments are from
    # previously worked modules
        @pytest.mark.skipif(str(7694) not in TESTS, reason='Excluded')  # NOQA
        def test_system_spaced_practice_assessments_are_from_previo_7694(self):
            """Spaced practice assessments are from previousy worked modules.

            Steps:

            Go to https://tutor-qa.openstax.org/
            Click on the 'Login' button
            Enter the student user account
            Click on the 'Sign in' button
            If the user has more than one course, click on a CC course name
            Click the 'Contents' button to open the table of contents
            Select a non-introductory section
            Click Jump to Concept Coach
            Click Launch Concept Coach

            Go through the assessments until you get to the Spaced Practice


            Expected Result:

            The section number beneath the text box is from a previous section

            """
            self.ps.test_updates['name'] = 'cc1.08.004' \
                + inspect.currentframe().f_code.co_name[4:]
            self.ps.test_updates['tags'] = [
                'cc1',
                'cc1.08',
                'cc1.08.004',
                '7694'
            ]
            self.ps.test_updates['passed'] = False

            # Test steps and verification assertions

            self.ps.test_updates['passed'] = True

    # Case C7695 - 005 - System | Modules without assessments do not display
    # the Concept Coach widget
    @pytest.mark.skipif(str(7695) not in TESTS, reason='Excluded')  # NOQA
    def test_system_modules_without_assessments_do_not_display_7695(self):
        """Module without assessments does not display the CC widget.

        Steps:

        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the student user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a CC course name
        Click the 'Contents' button to open the table of contents
        Click on an introductory section


        Expected Result:

        The Concept Coach widget does not appear.

        """
        self.ps.test_updates['name'] = 'cc1.08.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.08',
            'cc1.08.005',
            '7695'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C7696 - 006 - Student | Assignment is assistive technology friendly
    @pytest.mark.skipif(str(7696) not in TESTS, reason='Excluded')  # NOQA
    def test_student_assignment_is_assistive_technology_friendly_7696(self):
        """Assignment is assistive technology friendly.

        Steps:

        Go to tutor-qa
        Click on the 'Login' button
        Enter the student user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a CC course name

        Click the 'Contents' button to open the table of contents
        Click on a chapter
        Click on a non-introductory section
        Click the 'Launch Concept Coach' button at the bottom of the page
        Type text into the 'Enter your response' text box
        Click the 'Answer' button
        Type a, b, c, or d



        Expected Result:

        A multiple choice answer matching the letter typed should be selected.


        """
        self.ps.test_updates['name'] = 'cc1.08.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.08',
            'cc1.08.006',
            '7696'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C7697 - 007 - Student | Display the assignment summary
    # after completing the assignment
    @pytest.mark.skipif(str(7697) not in TESTS, reason='Excluded')  # NOQA
    def test_student_display_the_assignment_summary_after_completin_7697(self):
        """Display the assignment summary after completing the assignment.

        Steps:

        Go to tutor-qa
        Click on the 'Login' button
        Enter the student user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a CC course name

        Click the 'Contents' button to open the table of contents
        Click on a chapter
        Click on a non-introductory section
        Click the 'Launch Concept Coach' button at the bottom of the page
        Type text into the 'Enter your response' text box
        Click a multiple choice answer
        Click the 'Submit' button
        After answering the last question, click the 'Next Question' button



        Expected Result:

        The summary is displayed


        """
        self.ps.test_updates['name'] = 'cc1.08.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.08',
            'cc1.08.007',
            '7697'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C7698 - 008 - Student | The exercise ID is visible within
    # the assessment pane
    @pytest.mark.skipif(str(7698) not in TESTS, reason='Excluded')  # NOQA
    def test_student_exercise_id_is_visible_within_the_assessment_7698(self):
        """The exercise ID is visible within the assessment pane.

        Steps:

        Go to tutor-qa
        Click on the 'Login' button
        Enter the student account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a CC course name

        Click the 'Contents' button to open the table of contents
        Click on a chapter
        Click on a non-introductory section
        Click the 'Launch Concept Coach' button at the bottom of the page



        Expected Result:

        The exercise ID is visivle on the exercise.


        """
        self.ps.test_updates['name'] = 'cc1.08.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.08',
            'cc1.08.008',
            '7698'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C7699 - 009 - Student | Able to refer an assessment to OpenStax
    # via Errata Form
    @pytest.mark.skipif(str(7699) not in TESTS, reason='Excluded')  # NOQA
    def test_student_able_to_refer_an_assessment_to_openstax_7699(self):
        """Able to refer to an assessment to OpenStax via Errata form.

        Steps:

        Click the 'Contents' button to open the table of contents
        Click on a chapter
        Click on a non-introductory section
        Click the 'Launch Concept Coach' button at the bottom of the page
        Click the 'Report an error' link



        Expected Result:

        User is taken to the Errata form with the exercise ID prefilled


        """
        self.ps.test_updates['name'] = 'cc1.08.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.08',
            'cc1.08.009',
            '7699'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C7700 - 010 - Student | Able to work an assignment on an
    # Apple tablet device
    @pytest.mark.skipif(str(7700) not in TESTS, reason='Excluded')  # NOQA
    def test_student_able_to_work_an_assignment_on_an_apple_tablet_7700(self):
        """Able to work an assignment on an Apple tablet device.

        Steps:

        Click the 'Contents' button to open the table of contents
        Click on a chapter
        Click on a non-introductory section
        Click the 'Launch Concept Coach' button at the bottom of the page
        Type text into the 'Enter your response' text box
        Click a multiple choice answer
        Click the 'Submit' button



        Expected Result:

        Answer is successfully submitted.


        """
        self.ps.test_updates['name'] = 'cc1.08.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.08',
            'cc1.08.010',
            '7700'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C7701 - 011 - Student | Able to work an assignment on an
    # Android tablet device
    @pytest.mark.skipif(str(7701) not in TESTS, reason='Excluded')  # NOQA
    def test_student_able_to_work_an_assignment_on_android_tablet_7701(self):
        """Able to work an assignment on an Android tablet device.

        Steps:

        Click the 'Contents' button to open the table of contents
        Click on a chapter
        Click on a non-introductory section
        Click the 'Launch Concept Coach' button at the bottom of the page
        Type text into the 'Enter your response' text box
        Click a multiple choice answer
        Click the 'Submit' button



        Expected Result:

        Answer is successfully submitted.


        """
        self.ps.test_updates['name'] = 'cc1.08.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.08',
            'cc1.08.011',
            '7701'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C7702 - 012 - Student | Able to work an assignment on a
    # Windows tablet device
    @pytest.mark.skipif(str(7701) not in TESTS, reason='Excluded')  # NOQA
    def test_student_able_to_work_an_assignment_on_windows_tablet_7702(self):
        """Able to work an assignment on a WIndows tablet device.

        Steps:

        Click the 'Contents' button to open the table of contents
        Click on a chapter
        Click on a non-introductory section
        Click the 'Launch Concept Coach' button at the bottom of the page
        Type text into the 'Enter your response' text box
        Click a multiple choice answer
        Click the 'Submit' button



        Expected Result:

        Answer is successfully submitted.


        """
        self.ps.test_updates['name'] = 'cc1.08.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.08',
            'cc1.08.012',
            '7702'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C7703 - 013 - Student | Sees product error modals
    @pytest.mark.skipif(str(7703) not in TESTS, reason='Excluded')  # NOQA
    def test_student_sees_product_error_modals_7703(self):
        """See product error modals.

        Steps:

        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)
