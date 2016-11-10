"""Tutor v2, Epic 11.

Question Work: Faculty Reviews, Excludes, Edits, Creates Assignments
"""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
# from random import randint
from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver import ActionChains
# from staxing.assignment import Assignment

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Teacher, ContentQA, Student

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': 'latest',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([
        14695, 14696, 14691, 14692, 14693,
        14694, 14699, 14700, 14702, 14718,
        14715, 14717, 14710, 14711, 14712,
        14723, 14722, 14705, 14704, 14703,
        15903, 14719, 14714, 14716, 14709,
        14713, 14721, 14720, 14707, 14706,
        15902, 14724, 14725, 14735, 14799,
        14727, 14734, 14728, 14729, 14798,
        14730, 14731, 14732, 14736, 14737
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestQuestionWork(unittest.TestCase):
    """T2.11. Question Work: Faculty Reviews, Exclude, Edit, Creates Assign."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.teacher = Teacher(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        self.content = ContentQA(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities,
            existing_driver=self.teacher.driver
        )
        self.student = Student(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities,
            existing_driver=self.teacher.driver
        )

    def tearDown(self):
        """Test destructor."""
        self.ps.update_job(
            job_id=str(self.teacher.driver.session_id),
            **self.ps.test_updates
        )
        self.content = None
        self.student = None
        try:
            self.teacher.delete()
        except:
            pass

    # 14695 - 001 - Teacher | Review all questions
    @pytest.mark.skipif(str(14695) not in TESTS, reason='Excluded')
    def test_teacher_review_all_questions_14695(self):
        """Review all questions.

        Steps:
        Go to Tutor
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a Tutor course name
        Click "Question Library" from the user menu
        Select a section or chapter
        Click "Show Questions"

        Expected Result:
        The user is presented with all the questions for the section or chapter
        """
        self.ps.test_updates['name'] = 't2.11.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.001',
            '14695'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.select_course(appearance='physics')
        self.teacher.sleep(5)

        self.teacher.open_user_menu()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Question Library').click()
        self.teacher.sleep(5)

        # Open the assessment cards
        self.teacher.find(
            By.XPATH,
            "//span[@class='chapter-checkbox']/span[@class='tri-state-check" +
            "box unchecked']/i[@class='tutor-icon fa fa-square-o']").click()
        self.teacher.find(
            By.XPATH, "//button[@class='btn btn-primary']").click()
        self.teacher.sleep(5)
        self.teacher.find(
            By.XPATH,
            "//div[@class='openstax-exercise-preview exercise-card has-acti" +
            "ons non-interactive is-vertically-truncated panel panel-defau" +
            "lt']/div[@class='panel-body']")

        self.ps.test_updates['passed'] = True

    # 14696 - 002 - Teacher | Exclude certain questions
    @pytest.mark.skipif(str(14696) not in TESTS, reason='Excluded')
    def test_teacher_exclude_certain_questions_14696(self):
        """Exclude certain questions.

        Steps:
        If the user has more than one course, click on a Tutor course name
        Click "Question Library" from the user menu
        Select a section or chapter
        Click "Show Questions"
        Hover over the desired question and click "Exclude question"

        Expected Result:
        Question is excluded
        """
        self.ps.test_updates['name'] = 't2.11.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.002',
            '14696'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.select_course(appearance='physics')
        self.teacher.sleep(5)

        self.teacher.open_user_menu()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Question Library').click()
        self.teacher.sleep(5)

        # Open the assessment cards
        self.teacher.find(
            By.XPATH,
            "//span[@class='chapter-checkbox']/span[@class='tri-state-check" +
            "box unchecked']/i[@class='tutor-icon fa fa-square-o']").click()
        self.teacher.find(
            By.XPATH, "//button[@class='btn btn-primary']").click()
        self.teacher.sleep(5)

        # Click the exclude question button, then click include question button
        element = self.teacher.find(
            By.XPATH, "//div[@class = 'controls-overlay'][1]")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(element)
        actions.perform()
        self.teacher.sleep(2)
        self.teacher.find(By.XPATH, "//div[@class = 'action exclude']").click()
        self.teacher.sleep(2)
        self.teacher.find(By.XPATH, "//div[@class = 'action include']").click()
        self.teacher.sleep(2)

        self.ps.test_updates['passed'] = True

    # 14691 - 003 - Teacher | Tabs filter exercises into 'Reading'
    @pytest.mark.skipif(str(14691) not in TESTS, reason='Excluded')
    def test_teacher_tabs_filter_exercises_into_reading_14691(self):
        """Tab filters exercises into 'Reading'.

        Steps:
        If the user has more than one course, click on a Tutor course name
        Click "Question Library" from the user menu
        Select a section or chapter
        Click "Show Questions"
        Click on the "Reading" tab

        Expected Result:
        Exercises that are only for Reading appear
        """
        self.ps.test_updates['name'] = 't2.11.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.003',
            '14691'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.select_course(appearance='physics')
        self.teacher.sleep(5)

        self.teacher.open_user_menu()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Question Library').click()
        self.teacher.sleep(5)

        # Open the assessment cards
        self.teacher.find(
            By.XPATH,
            "//span[@class='chapter-checkbox']/span[@class='tri-state-check" +
            "box unchecked']/i[@class='tutor-icon fa fa-square-o']").click()
        self.teacher.find(
            By.XPATH, "//button[@class='btn btn-primary']").click()
        self.teacher.sleep(5)

        # Count the total number of cards
        total = len(self.teacher.driver.find_elements_by_xpath(
            "//div[@class='openstax-exercise-preview exercise-card has-acti" +
            "ons non-interactive is-vertically-truncated panel panel-defaul" +
            "t']/div[@class='panel-body']"))
        self.teacher.sleep(2)

        # Limit assessments to reading, count the total number of cards
        self.teacher.find(
            By.XPATH, "//button[@class='reading btn btn-default']").click()
        self.teacher.sleep(1)
        reading = len(self.teacher.driver.find_elements_by_xpath(
            "//div[@class='openstax-exercise-preview exercise-card has-ac" +
            "tions non-interactive is-vertically-truncated panel panel-de" +
            "fault']/div[@class='panel-body']"))
        self.teacher.sleep(2)

        # Reading assessments should not outnumber total assessments
        assert(total >= reading), \
            'More reading assessments than total assessments'

        self.ps.test_updates['passed'] = True

    # 14692 - 004 - Teacher | Tabs filter exercises into 'Practice'
    @pytest.mark.skipif(str(14692) not in TESTS, reason='Excluded')
    def test_teacher_tabs_filter_exercises_into_practice_14692(self):
        """Tab filters exercises into 'Practice'.

        Steps:
        If the user has more than one course, click on a Tutor course name
        Click "Question Library" from the user menu
        Select a section or chapter
        Click "Show Questions"
        Click on the "Practice" tab

        Expected Result:
        Exercises that are only for practice appear
        """
        self.ps.test_updates['name'] = 't2.11.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.004',
            '14692'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.select_course(appearance='physics')
        self.teacher.sleep(5)

        self.teacher.open_user_menu()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Question Library').click()
        self.teacher.sleep(5)

        # Open the assessment cards
        self.teacher.find(
            By.XPATH,
            "//span[@class='chapter-checkbox']/span[@class='tri-state-check" +
            "box unchecked']/i[@class='tutor-icon fa fa-square-o']").click()
        self.teacher.find(
            By.XPATH, "//button[@class='btn btn-primary']").click()
        self.teacher.sleep(5)

        # Count the total number of cards
        total = len(self.teacher.driver.find_elements_by_xpath(
            "//div[@class='openstax-exercise-preview exercise-card has-act" +
            "ions non-interactive is-vertically-truncated panel panel-defa" +
            "ult']/div[@class='panel-body']"))
        self.teacher.sleep(2)

        # Limit assessments to practice, count the total number of cards
        self.teacher.find(
            By.XPATH, "//button[@class='homework btn btn-default']").click()
        self.teacher.sleep(1)
        practice = len(self.teacher.driver.find_elements_by_xpath(
            "//div[@class='openstax-exercise-preview exercise-card has-act" +
            "ions non-interactive is-vertically-truncated panel panel-defa" +
            "ult']/div[@class='panel-body']"))
        self.teacher.sleep(2)

        # Practice assessments should not outnumber total assessments
        assert(total >= practice), \
            'More practice assessments than total assessments'

        self.ps.test_updates['passed'] = True

    # 14693 - 005 - Teacher | Pin tabs to top of screen when scrolled
    @pytest.mark.skipif(str(14693) not in TESTS, reason='Excluded')
    def test_teacher_pin_tabs_to_top_of_screen_when_scrolled_14693(self):
        """Pin tabs to top of screen when scrolled.

        Steps:
        If the user has more than one course, click on a Tutor course name
        Click "Question Library" from the user menu
        Select a section or chapter
        Click "Show Questions"
        Scroll down

        Expected Result:
        Tabs are pinned to the top of the screen when scrolled
        """
        self.ps.test_updates['name'] = 't2.11.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.005',
            '14693'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.select_course(appearance='physics')
        self.teacher.sleep(5)

        self.teacher.open_user_menu()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Question Library').click()
        self.teacher.sleep(5)

        # Open the assessment cards
        self.teacher.find(
            By.XPATH,
            "//span[@class='chapter-checkbox']/span[@class='tri-state-check" +
            "box unchecked']/i[@class='tutor-icon fa fa-square-o']").click()
        self.teacher.find(
            By.XPATH, "//button[@class='btn btn-primary']").click()
        self.teacher.sleep(10)

        # Scroll to bottom of page and verify that the tabs are still visible
        self.teacher.driver.execute_script("window.scrollTo(0, 0);")
        self.teacher.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        self.teacher.sleep(3)
        self.teacher.find(By.XPATH, "//div[@class='section active']")
        self.teacher.find(
            By.XPATH, "//button[@class='homework btn btn-default']")
        self.teacher.find(
            By.XPATH, "//button[@class='reading btn btn-default']")
        self.teacher.sleep(3)

        self.ps.test_updates['passed'] = True

    # 14694 - 006 - Teacher | Make section links jumpable
    @pytest.mark.skipif(str(14694) not in TESTS, reason='Excluded')
    def test_teacher_make_section_links_jumpable_14694(self):
        """Make section links jumpable.

        Steps:
        If the user has more than one course, click on a Tutor course name
        Click "Question Library" from the user menu
        Select a section or chapter
        Click "Show Questions"
        Click on the section links at the top of the screen

        Expected Result:
        The screen scrolls to the selected screen
        """
        self.ps.test_updates['name'] = 't2.11.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.006',
            '14694'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.select_course(appearance='physics')
        self.teacher.sleep(5)

        self.teacher.open_user_menu()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Question Library').click()
        self.teacher.sleep(5)

        # Open the assessment cards
        self.teacher.find(
            By.XPATH,
            "//span[@class='chapter-checkbox']/span[@class='tri-" +
            "state-checkbox unchecked']/i[@class='tutor-icon fa fa-square-o']"
        ).click()
        self.teacher.find(
            By.XPATH, "//button[@class='btn btn-primary']").click()
        self.teacher.sleep(10)

        sections = self.teacher.driver.find_elements_by_xpath(
            "//div[@class='exercise-sections']/label[@class='exercises-secti" +
            "on-label']/span[3]")
        sections.pop(0)

        jumps = self.teacher.driver.find_elements_by_xpath(
            "//div[@class='sectionizer']/div[@class='section']")

        assert(len(sections) == len(jumps)), \
            'Number of section jumps does not equal number of section titles'

        # Click the section links and verify the page is scrolled
        position = self.teacher.driver.execute_script("return window.scrollY;")
        for button in jumps:
            button.click()
            self.teacher.sleep(2)
            assert(position < self.teacher.driver.execute_script(
                "return window.scrollY;")), \
                'Section link did not jump to next section'

            position = self.teacher.driver.execute_script(
                "return window.scrollY;")

        self.teacher.sleep(3)

        self.ps.test_updates['passed'] = True

    # 14699 - 007 - Teacher | Report errata about assessments in Tutor
    @pytest.mark.skipif(str(14699) not in TESTS, reason='Excluded')
    def test_teacher_report_errata_about_assessments_in_tutor_14699(self):
        """Report errata about assessments in Tutor.

        Steps:
        If the user has more than one course, click on a Tutor course name
        Click "Question Library" from the user menu
        Select a section or chapter
        Click "Show Questions"
        Hover over the desired question and click "Question details"
        Click "Report an error"

        Expected Result:
        A new tab with the assessment errata form appears, with the assessment
        ID already filled in
        """
        self.ps.test_updates['name'] = 't2.11.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.007',
            '14699'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.select_course(appearance='physics')
        self.teacher.sleep(5)

        self.teacher.open_user_menu()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Question Library').click()
        self.teacher.sleep(5)

        # Open the assessment cards
        self.teacher.find(
            By.XPATH,
            "//span[@class='chapter-checkbox']/span[@class='tri-state-check" +
            "box unchecked']/i[@class='tutor-icon fa fa-square-o']").click()
        self.teacher.find(
            By.XPATH, "//button[@class='btn btn-primary']").click()
        self.teacher.sleep(5)

        # Click the question detail button, then click report an error button
        element = self.teacher.find(
            By.XPATH, "//div[@class = 'controls-overlay'][1]")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(element)
        actions.perform()
        self.teacher.sleep(2)
        self.teacher.find(By.XPATH, "//div[@class='action details']").click()
        self.teacher.sleep(2)
        self.teacher.find(
            By.XPATH, "//div[@class='action report-error']").click()
        self.teacher.sleep(3)
        self.teacher.driver.switch_to_window(
            self.teacher.driver.window_handles[-1])

        assert('docs.google' in self.teacher.current_url()), \
            'Not viewing the errata page'

        self.ps.test_updates['passed'] = True

    # 14700 - 008 - Student | Report errata about assessments in Tutor
    @pytest.mark.skipif(str(14700) not in TESTS, reason='Excluded')
    def test_student_report_errata_about_assessments_in_tutor_14700(self):
        """Report errata about assessments in Tutor.

        Steps:
        If the user has more than one course, click on a Tutor course name
        Click on an assignment
        On an assessment card, click on the "Report an error" link in the
        bottom right corner

        Expected Result:
        A new tab with the assessment errata form appears, with the assessment
        ID already filled in
        """
        self.ps.test_updates['name'] = 't2.11.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.008',
            '14700'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.login()
        self.student.select_course(appearance='physics')
        self.student.sleep(5)

        # Find a homework from past work
        self.student.find(
            By.XPATH, "//ul[@class='nav nav-tabs']/li[2]/a").click()
        self.student.find(
            By.XPATH,
            "//div[@class='-weeks-events panel panel-default']/div[@class" +
            "='panel-body']/div[@class='task row homework workable']").click()
        self.student.sleep(3)

        # Go to the errata form
        self.student.driver.execute_script("window.scrollTo(0, 0);")
        self.student.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        self.student.find(
            By.XPATH, "//span[@class='exercise-identifier-link']/a").click()
        self.student.sleep(3)
        self.student.driver.switch_to_window(
            self.student.driver.window_handles[-1])

        assert('docs.google' in self.student.current_url()), \
            'Not viewing the errata page'

        self.ps.test_updates['passed'] = True

    # 14702 - 009 - Teacher | Exclude a question from already worked
    # assignments
    @pytest.mark.skipif(str(14702) not in TESTS, reason='Excluded')
    def test_teacher_exclude_a_question_from_already_worked_assign_14702(self):
        """Exclude a question from already worked assignments.

        Steps:
        If the user has more than one course, click on a Tutor course name
        Go to an open assignment that has already been worked
        Click the X on the upper right corner of an assessment card
        Click "Remove"

        Expected Result:
        A question is excluded from already worked assignments
        """
        self.ps.test_updates['name'] = 't2.11.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.009',
            '14702'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 14718 - 010 - Content Analyst | Create a brand new multiple choice
    # question
    @pytest.mark.skipif(str(14718) not in TESTS, reason='Excluded')
    def test_content_analyst_create_a_brand_new_multiple_choice_qu_14718(self):
        """Create a brand new multiple choice question.

        Steps:
        Go to Exercises
        Click on the 'Login' button
        Enter the content analyst account
        Click on the 'Sign in' button
        Click "Write a new exercise"
        Click on the "Multiple Choice" radio button if it is not already
            selected
        Fill out the required fields
        Click "Publish"

        Expected Result:
        The user gets a confirmation that says "Exercise [exercise ID] has
        published successfully"
        """
        self.ps.test_updates['name'] = 't2.11.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.010',
            '14718'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.content.login()
        self.content.sleep(2)
        self.content.driver.get("https://exercises-qa.openstax.org/")
        self.content.sleep(2)
        self.content.find(By.PARTIAL_LINK_TEXT, "SIGN IN").click()
        self.content.sleep(2)
        self.content.find(By.PARTIAL_LINK_TEXT, "WRITE A NEW EXERCISE").click()
        self.content.sleep(5)

        # Select Multiple Choice radio if not already selected
        if not self.content.find(
            By.XPATH, "//div[@class='form-group'][1]/div[@class='radio']"
        ).is_selected():
            self.content.find(
                By.XPATH,
                "//div[@class='form-group'][1]/div[@class='radio']" +
                "/label/span").click()

        self.content.sleep(3)

        # Fill in required fields
        self.content.find(By.XPATH, "//div[4]/textarea").send_keys('Stem')
        self.content.find(
            By.XPATH,
            "//li[@class='correct-answer']/textarea[1]").send_keys(
            'Distractor')
        self.content.find(
            By.XPATH,
            "//li[@class='correct-answer']/textarea[2]").send_keys('Feedback')
        self.content.find(By.XPATH, "//div[6]/textarea").send_keys('Solution')

        # Save draft and publish
        self.content.find(
            By.XPATH,
            "//button[@class='async-button draft btn btn-info']").click()
        self.content.sleep(3)
        self.content.find(
            By.XPATH,
            "//button[@class='async-button publish btn btn-primary']").click()
        self.content.find(
            By.XPATH,
            "//div[@class='popover-content']/div[@class='controls']/button" +
            "[@class='btn btn-primary']").click()
        self.content.sleep(3)

        # Verify
        page = self.content.driver.page_source
        assert('has published successfully' in page), \
            'Exercise not successfully published'

        self.content.find(
            By.XPATH, "//button[@class='btn btn-primary']").click()

        self.content.sleep(3)

        self.ps.test_updates['passed'] = True

    # 14715 - 011 - Content Analyst | Preserve the order of choices for
    # questions where the choice order matters
    @pytest.mark.skipif(str(14715) not in TESTS, reason='Excluded')
    def test_content_analyst_preserve_the_order_of_choices_for_que_14715(self):
        """Preserve order of choices for questions where choice order matters.

        Steps:
        Click "Write a new exercise"
        Click on the box "Order Matters"

        Expected Result:
        The user is able to preserve the order of choices
        """
        self.ps.test_updates['name'] = 't2.11.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.011',
            '14715'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.content.login()
        self.content.sleep(2)
        self.content.driver.get("https://exercises-qa.openstax.org/")
        self.content.sleep(2)
        self.content.find(By.PARTIAL_LINK_TEXT, "SIGN IN").click()
        self.content.sleep(2)
        self.content.find(By.PARTIAL_LINK_TEXT, "WRITE A NEW EXERCISE").click()
        self.content.sleep(5)

        # Select the Order Matters checkbox
        checkbox = self.content.find(
            By.XPATH,
            "//div[@class='question']/div[@class='form-group']/div[@class" +
            "='checkbox']/label/span")
        checkbox.click()
        self.content.sleep(5)

        if checkbox.is_selected():
            self.ps.test_updates['passed'] = True

    # 14717 - 012 - Content Analyst | Edit detailed solutions
    @pytest.mark.skipif(str(14717) not in TESTS, reason='Excluded')
    def test_content_analyst_edit_detailed_solutions_14717(self):
        """Edit detailed solutions.

        Steps:
        Click "Search"
        Enter the desired exercise ID
        Scroll down to "Detailed Solutions"
        Edit text in the "Detailed Solutions" text box
        Click "Publish"

        Expected Result:
        The user is able to edit detailed solutions and the changes are
        reflected in the box to the right
        """
        self.ps.test_updates['name'] = 't2.11.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.012',
            '14717'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.content.login()
        self.content.sleep(2)
        self.content.driver.get("https://exercises-qa.openstax.org/")
        self.content.sleep(2)
        self.content.find(By.PARTIAL_LINK_TEXT, "SIGN IN").click()
        self.content.sleep(2)
        self.content.find(By.PARTIAL_LINK_TEXT, "WRITE A NEW EXERCISE").click()
        self.content.sleep(5)

        # Select Multiple Choice radio if not already selected
        if not self.content.find(
            By.XPATH,
            "//div[@class='form-group'][1]/div[@class='radio']"
        ).is_selected():
            self.content.find(
                By.XPATH,
                "//div[@class='form-group'][1]/div[@class='radio']/label/span"
            ).click()

        self.content.sleep(3)

        # Fill in required fields
        self.content.find(By.XPATH, "//div[4]/textarea").send_keys('Stem')
        self.content.find(
            By.XPATH,
            "//li[@class='correct-answer']/textarea[1]").send_keys(
            'Distractor')
        self.content.find(
            By.XPATH,
            "//li[@class='correct-answer']/textarea[2]").send_keys('Feedback')
        self.content.find(By.XPATH, "//div[6]/textarea").send_keys('Solution')

        # Save draft and publish
        self.content.find(
            By.XPATH,
            "//button[@class='async-button draft btn btn-info']").click()
        self.content.sleep(3)
        self.content.find(
            By.XPATH,
            "//button[@class='async-button publish btn btn-primary']").click()
        self.content.find(
            By.XPATH,
            "//div[@class='popover-content']/div[@class='controls']/butt" +
            "on[@class='btn btn-primary']").click()
        self.content.sleep(3)

        # Verify
        page = self.content.driver.page_source
        assert('has published successfully' in page), \
            'Exercise not successfully published'

        self.content.find(
            By.XPATH, "//button[@class='btn btn-primary']").click()

        self.content.sleep(3)

        detailed = self.content.find(
            By.XPATH, "//div[@class='openstax-has-html solution']")
        assert(detailed.text == 'Solution'), \
            'Detailed solution text is not what is expected'

        self.ps.test_updates['passed'] = True

    # 14710 - 013 - Content Analyst | Reference an embedded video
    @pytest.mark.skipif(str(14710) not in TESTS, reason='Excluded')
    def test_content_analyst_reference_an_embedded_video_14710(self):
        """Reference an embedded video.

        Steps:
        Click "Write a new exercise"
        Enter the video embed link into the Question Stem text box

        Expected Result:
        The video should appear in the box to the right
        """
        self.ps.test_updates['name'] = 't2.11.013' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.013',
            '14710'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.content.login()
        self.content.sleep(2)
        self.content.driver.get("https://exercises-qa.openstax.org/")
        self.content.sleep(2)
        self.content.find(By.PARTIAL_LINK_TEXT, "SIGN IN").click()
        self.content.sleep(2)
        self.content.find(By.PARTIAL_LINK_TEXT, "WRITE A NEW EXERCISE").click()
        self.content.sleep(5)

        # Select Multiple Choice radio if not already selected
        if not self.content.find(
            By.XPATH,
            "//div[@class='form-group'][1]/div[@class='radio']"
        ).is_selected():
            self.content.find(
                By.XPATH,
                "//div[@class='form-group'][1]/div[@class='radio']/label/span"
            ).click()

        self.content.sleep(3)

        # Fill in required fields
        vid = '<iframe width="420" height="315" src="https://www.youtube.com'
        vid += '/embed/jNQXAC9IVRw" frameborder="0" allowfullscreen></iframe>'
        self.content.find(By.XPATH, "//div[4]/textarea").send_keys(vid)
        self.content.find(
            By.XPATH,
            "//li[@class='correct-answer']/textarea[1]").send_keys(
            'Distractor')
        self.content.find(
            By.XPATH,
            "//li[@class='correct-answer']/textarea[2]").send_keys('Feedback')
        self.content.find(By.XPATH, "//div[6]/textarea").send_keys('Solution')

        # Save draft and publish
        self.content.find(
            By.XPATH,
            "//button[@class='async-button draft btn btn-info']").click()
        self.content.sleep(3)
        self.content.find(
            By.XPATH,
            "//button[@class='async-button publish btn btn-primary']").click()
        self.content.find(
            By.XPATH,
            "//div[@class='popover-content']/div[@class='controls']/butt" +
            "on[@class='btn btn-primary']").click()
        self.content.sleep(3)

        # Verify
        page = self.content.driver.page_source
        assert('has published successfully' in page), \
            'Exercise not successfully published'

        self.content.find(
            By.XPATH, "//button[@class='btn btn-primary']").click()

        self.content.sleep(3)

        # Find the embedded video
        self.content.find(
            By.XPATH,
            "//div[@class='frame-wrapper embed-responsive embed-responsive-" +
            "4by3']/iframe")

        self.ps.test_updates['passed'] = True

    # 14711 - 014 - Content Analyst | Pull out the dropdown tags
    @pytest.mark.skipif(str(14711) not in TESTS, reason='Excluded')
    def test_content_analyst_pull_out_the_dropdown_tags_14711(self):
        """Pull out the dropdown tags.

        Steps:
        Click "Write a new exercise"
        Click "Tags"
        Click "Question Type," "DOK," "Blooms," and/or "Time"

        Expected Result:
        The user is able to pull out the dropdown tags
        """
        self.ps.test_updates['name'] = 't2.11.014' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.014',
            '14711'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.content.login()
        self.content.sleep(2)
        self.content.driver.get("https://exercises-qa.openstax.org/")
        self.content.sleep(2)
        self.content.find(By.PARTIAL_LINK_TEXT, "SIGN IN").click()
        self.content.sleep(2)
        self.content.find(By.PARTIAL_LINK_TEXT, "WRITE A NEW EXERCISE").click()
        self.content.sleep(5)

        # Switch to Tags tab and find the dropdown elements
        self.content.find(
            By.XPATH, "//ul[@class='nav nav-tabs']/li[2]/a").click()
        self.content.sleep(1)
        dropdowns = self.content.driver.find_elements_by_xpath(
            "//select[@class='form-control']")
        self.content.sleep(1)

        # Select values for the dropdown menus
        dropdowns[0].send_keys('Con')
        dropdowns[1].send_keys('1')
        dropdowns[2].send_keys('3')
        dropdowns[3].send_keys('Long')

        self.content.sleep(5)

        self.ps.test_updates['passed'] = True

    # 14712 - 015 - Content Analyst | Use drop down choices from tagging legend
    @pytest.mark.skipif(str(14712) not in TESTS, reason='Excluded')
    def test_content_analyst_use_dropdown_choices_from_tagging_leg_14712(self):
        """Use drop down choices from tagging legend.

        Steps:
        Click "Write a new exercise"
        Click "Tags"
        Click "Question Type," "DOK," "Blooms," and/or "Time"
        Select a choice from the dropdown tags

        Expected Result:
        The user is able to select a specific tag from the dropdown choices and
        the tag(s) appear in the box to the right
        """
        self.ps.test_updates['name'] = 't2.11.015' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.015',
            '14712'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.content.login()
        self.content.sleep(2)
        self.content.driver.get("https://exercises-qa.openstax.org/")
        self.content.sleep(2)
        self.content.find(By.PARTIAL_LINK_TEXT, "SIGN IN").click()
        self.content.sleep(2)
        self.content.find(By.PARTIAL_LINK_TEXT, "WRITE A NEW EXERCISE").click()
        self.content.sleep(5)

        # Switch to Tags tab and find the dropdown elements
        self.content.find(
            By.XPATH, "//ul[@class='nav nav-tabs']/li[2]/a").click()
        self.content.sleep(1)
        dropdowns = self.content.driver.find_elements_by_xpath(
            "//select[@class='form-control']")
        self.content.sleep(1)

        # Select values for the dropdown menus
        dropdowns[0].send_keys('Con')
        dropdowns[1].send_keys('1')
        dropdowns[2].send_keys('3')
        dropdowns[3].send_keys('Long')

        self.content.sleep(5)

        self.ps.test_updates['passed'] = True

    # 14723 - 016 - Content Analyst | Specify whether context is required for a
    # question
    @pytest.mark.skipif(str(14723) not in TESTS, reason='Excluded')
    def test_content_analyst_specify_whether_context_is_required_14723(self):
        """Specify whether context is required for a question.

        Steps:
        Click "Write a new exercise"
        Click "Tags"
        Check the box that says "Requires Context"

        Expected Result:
        The tag "requires-contact:true" appears in the box to the right
        """
        self.ps.test_updates['name'] = 't2.11.016' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.016',
            '14723'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.content.login()
        self.content.sleep(2)
        self.content.driver.get("https://exercises-qa.openstax.org/")
        self.content.sleep(2)
        self.content.find(By.PARTIAL_LINK_TEXT, "SIGN IN").click()
        self.content.sleep(2)
        self.content.find(By.PARTIAL_LINK_TEXT, "WRITE A NEW EXERCISE").click()
        self.content.sleep(5)

        # Switch to Tags tab and check Requires Context
        self.content.find(
            By.XPATH, "//ul[@class='nav nav-tabs']/li[2]/a").click()
        self.content.sleep(1)
        self.content.find(By.XPATH, "//div[@class='tag']/input").click()
        self.content.sleep(3)

        if self.content.find(
            By.XPATH, "//div[@class='tag']/input"
        ).is_selected():
            self.ps.test_updates['passed'] = True

    # 14722 - 017 - Content Analyst | Add context to a question
    @pytest.mark.skipif(str(14722) not in TESTS, reason='Excluded')
    def test_content_analyst_add_context_to_a_question_14722(self):
        """Add context to a question.

        Steps:
        Click "Write a new exercise"
        Click "Tags"
        Check the box that says "Requires Context"
        Click "+" next to "CNX Module"
        Enter the CNX Module number

        Expected Result:
        The user is able to add context to a question
        """
        self.ps.test_updates['name'] = 't2.11.017' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.017',
            '14722'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.content.login()
        self.content.sleep(2)
        self.content.driver.get("https://exercises-qa.openstax.org/")
        self.content.sleep(2)
        self.content.find(By.PARTIAL_LINK_TEXT, "SIGN IN").click()
        self.content.sleep(2)
        self.content.find(By.PARTIAL_LINK_TEXT, "WRITE A NEW EXERCISE").click()
        self.content.sleep(5)

        # Switch to Tags tab and click CNX Module
        self.content.find(
            By.XPATH, "//ul[@class='nav nav-tabs']/li[2]/a").click()
        self.content.sleep(1)
        self.content.driver.find_elements_by_xpath(
            "//i[@class='fa fa-plus-circle']")[2].click()
        self.content.sleep(3)

        self.content.find(By.XPATH, "//input[@class='form-control']")

        self.ps.test_updates['passed'] = True

    # 14705 - 018 - Content Analyst | Add the image
    @pytest.mark.skipif(str(14705) not in TESTS, reason='Excluded')
    def test_content_analyst_add_the_image_14705(self):
        """Add the image.

        Steps:
        Click "Write a new exercise"
        Enter text into Question Stem, Distractor, and Detailed Solution
        Click "Save Draft"
        Click "Assets"
        Click "Add new image"
        Select an image

        Expected Result:
        The image and the options "Choose different image" and "Upload" should
        come up
        """
        self.ps.test_updates['name'] = 't2.11.018' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.018',
            '14705'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.content.login()
        self.content.sleep(2)
        self.content.driver.get("https://exercises-qa.openstax.org/")
        self.content.sleep(2)
        self.content.find(By.PARTIAL_LINK_TEXT, "SIGN IN").click()
        self.content.sleep(2)
        self.content.find(By.PARTIAL_LINK_TEXT, "WRITE A NEW EXERCISE").click()
        self.content.sleep(5)

        # Select Multiple Choice radio if not already selected
        if not self.content.find(
            By.XPATH,
            "//div[@class='form-group'][1]/div[@class='radio']"
        ).is_selected():
            self.content.find(
                By.XPATH,
                "//div[@class='form-group'][1]/div[@class='radio']/label/span"
            ).click()

        self.content.sleep(3)

        # Fill in required fields
        self.content.find(By.XPATH, "//div[4]/textarea").send_keys('Stem')
        self.content.find(
            By.XPATH,
            "//li[@class='correct-answer']/textarea[1]").send_keys(
            'Distractor')
        self.content.find(
            By.XPATH,
            "//li[@class='correct-answer']/textarea[2]").send_keys('Feedback')
        self.content.find(By.XPATH, "//div[6]/textarea").send_keys('Solution')

        # Save draft and publish
        self.content.find(
            By.XPATH,
            "//button[@class='async-button draft btn btn-info']").click()
        self.content.sleep(3)

        # Move to Assets and upload image
        self.content.find(
            By.XPATH, "//ul[@class='nav nav-tabs']/li[3]/a").click()
        self.content.sleep(3)
        self.content.find(
            By.ID, "file"
        ).send_keys(
            "/Users/openstaxii/desktop/Screen Shot 2016-06-17 at 1.15.39 PM" +
            ".png")
        self.content.sleep(5)

        # Find the Upload and Choose different image buttons
        self.content.find(By.XPATH, "//label[@class='selector']")
        self.content.find(By.XPATH, "//button[@class='btn btn-default']")

        self.ps.test_updates['passed'] = True

    # 14704 - 019 - Content Analyst | Upload an image
    @pytest.mark.skipif(str(14704) not in TESTS, reason='Excluded')
    def test_content_analyst_upload_the_image_14704(self):
        """Add the image.

        Steps:
        Click "Write a new exercise"
        Enter text into Question Stem, Distractor, and Detailed Solution
        Click "Save Draft"
        Click "Assets"
        Click "Add new image"
        Select an image
        Click "Upload"

        Expected Result:
        There should be a URL and a "Delete" button
        """
        self.ps.test_updates['name'] = 't2.11.019' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.019',
            '14704'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.content.login()
        self.content.sleep(2)
        self.content.driver.get("https://exercises-qa.openstax.org/")
        self.content.sleep(2)
        self.content.find(By.PARTIAL_LINK_TEXT, "SIGN IN").click()
        self.content.sleep(2)
        self.content.find(By.PARTIAL_LINK_TEXT, "WRITE A NEW EXERCISE").click()
        self.content.sleep(5)

        # Select Multiple Choice radio if not already selected
        if not self.content.find(
            By.XPATH,
            "//div[@class='form-group'][1]/div[@class='radio']"
        ).is_selected():
            self.content.find(
                By.XPATH,
                "//div[@class='form-group'][1]/div[@class='radio']/label/span"
            ).click()

        self.content.sleep(3)

        # Fill in required fields
        self.content.find(By.XPATH, "//div[4]/textarea").send_keys('Stem')
        self.content.find(
            By.XPATH,
            "//li[@class='correct-answer']/textarea[1]").send_keys(
            'Distractor')
        self.content.find(
            By.XPATH,
            "//li[@class='correct-answer']/textarea[2]").send_keys('Feedback')
        self.content.find(By.XPATH, "//div[6]/textarea").send_keys('Solution')

        # Save draft and publish
        self.content.find(
            By.XPATH,
            "//button[@class='async-button draft btn btn-info']").click()
        self.content.sleep(3)

        # Move to Assets and upload image
        self.content.find(
            By.XPATH, "//ul[@class='nav nav-tabs']/li[3]/a").click()
        self.content.sleep(3)
        self.content.find(
            By.ID, "file"
        ).send_keys(
            "/Users/openstaxii/desktop/Screen Shot 2016-06-17 at 1.15.39 PM" +
            ".png")
        self.content.sleep(5)
        self.content.find(
            By.XPATH, "//button[@class='btn btn-default']").click()

        # Wait for upload and find the Delete button
        self.content.sleep(30)
        self.content.find(
            By.XPATH, "//button[@class='btn btn-default']").click()
        self.content.sleep(5)

        self.ps.test_updates['passed'] = True

    # 14703 - 020 - Content Analyst | Show uploaded URL in the HTML snippet
    @pytest.mark.skipif(str(14703) not in TESTS, reason='Excluded')
    def test_content_analyst_show_uploaded_url_in_the_html_snippet_14703(self):
        """Show uploaded URL in the HTML snippet.

        Steps:
        Click "Write a new exercise"
        Enter text into Question Stem, Distractor, and Detailed Solution
        Click "Save Draft"
        Click "Assets"
        Click "Add new image"
        Select an image
        Click "Upload"

        Expected Result:
        The user is presented with uploaded URL in the HTML snippet
        """
        self.ps.test_updates['name'] = 't2.11.020' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.020',
            '14703'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.content.login()
        self.content.sleep(2)
        self.content.driver.get("https://exercises-qa.openstax.org/")
        self.content.sleep(2)
        self.content.find(By.PARTIAL_LINK_TEXT, "SIGN IN").click()
        self.content.sleep(2)
        self.content.find(By.PARTIAL_LINK_TEXT, "WRITE A NEW EXERCISE").click()
        self.content.sleep(5)

        # Select Multiple Choice radio if not already selected
        if not self.content.find(
            By.XPATH,
            "//div[@class='form-group'][1]/div[@class='radio']"
        ).is_selected():
            self.content.find(
                By.XPATH,
                "//div[@class='form-group'][1]/div[@class='radio']/label/span"
            ).click()

        self.content.sleep(3)

        # Fill in required fields
        self.content.find(By.XPATH, "//div[4]/textarea").send_keys('Stem')
        self.content.find(
            By.XPATH,
            "//li[@class='correct-answer']/textarea[1]").send_keys(
            'Distractor')
        self.content.find(
            By.XPATH,
            "//li[@class='correct-answer']/textarea[2]").send_keys('Feedback')
        self.content.find(By.XPATH, "//div[6]/textarea").send_keys('Solution')

        # Save draft and publish
        self.content.find(
            By.XPATH,
            "//button[@class='async-button draft btn btn-info']").click()
        self.content.sleep(3)

        # Move to Assets and upload image
        self.content.find(
            By.XPATH, "//ul[@class='nav nav-tabs']/li[3]/a").click()
        self.content.sleep(3)
        self.content.find(
            By.ID, "file"
        ).send_keys(
            "/Users/openstaxii/desktop/Screen Shot 2016-06-17 at 1.15.39 PM" +
            ".png")
        self.content.sleep(5)
        self.content.find(
            By.XPATH, "//button[@class='btn btn-default']").click()

        # Wait for upload and find URL snippet
        self.content.sleep(30)
        self.content.find(By.XPATH, "//textarea[@class='copypaste']")
        self.content.find(
            By.XPATH, "//button[@class='btn btn-default']").click()
        self.content.sleep(5)

        self.ps.test_updates['passed'] = True

    # 15903 - 021 - Content Analyst | Delete an image
    @pytest.mark.skipif(str(15903) not in TESTS, reason='Excluded')
    def test_content_analyst_delete_an_image_15903(self):
        """Delete an image.

        Steps:
        Click "Write a new exercise"
        Enter text into Question Stem, Distractor, and Detailed Solution
        Click "Save Draft"
        Click "Assets"
        Click "Add new image"
        Select an image
        Click "Upload"
        Click "Delete"

        Expected Result:
        The image is deleted
        """
        self.ps.test_updates['name'] = 't2.11.021' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.021',
            '15903'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.content.login()
        self.content.sleep(2)
        self.content.driver.get("https://exercises-qa.openstax.org/")
        self.content.sleep(2)
        self.content.find(By.PARTIAL_LINK_TEXT, "SIGN IN").click()
        self.content.sleep(2)
        self.content.find(By.PARTIAL_LINK_TEXT, "WRITE A NEW EXERCISE").click()
        self.content.sleep(5)

        # Select Multiple Choice radio if not already selected
        if not self.content.find(
            By.XPATH,
            "//div[@class='form-group'][1]/div[@class='radio']"
        ).is_selected():
            self.content.find(
                By.XPATH,
                "//div[@class='form-group'][1]/div[@class='radio']/label/span"
            ).click()

        self.content.sleep(3)

        # Fill in required fields
        self.content.find(By.XPATH, "//div[4]/textarea").send_keys('Stem')
        self.content.find(
            By.XPATH,
            "//li[@class='correct-answer']/textarea[1]").send_keys(
            'Distractor')
        self.content.find(
            By.XPATH,
            "//li[@class='correct-answer']/textarea[2]").send_keys('Feedback')
        self.content.find(By.XPATH, "//div[6]/textarea").send_keys('Solution')

        # Save draft and publish
        self.content.find(
            By.XPATH,
            "//button[@class='async-button draft btn btn-info']").click()
        self.content.sleep(3)

        # Move to Assets and upload image
        self.content.find(
            By.XPATH, "//ul[@class='nav nav-tabs']/li[3]/a").click()
        self.content.sleep(3)
        self.content.find(
            By.ID, "file"
        ).send_keys(
            "/Users/openstaxii/desktop/Screen Shot 2016-06-17 at 1.15.39 PM" +
            ".png")
        self.content.sleep(5)
        self.content.find(
            By.XPATH, "//button[@class='btn btn-default']").click()

        # Wait for upload and find the Delete button
        self.content.sleep(30)
        self.content.find(
            By.XPATH, "//button[@class='btn btn-default']").click()
        self.content.sleep(5)

        # Verify image is deleted
        assert len(self.content.driver.find_elements_by_xpath(
            "//button[@class='btn btn-default']")) == 0, \
            'Image not deleted'

        self.ps.test_updates['passed'] = True

    # 14719 - 022 - Teacher | Create a brand new multiple choice question
    @pytest.mark.skipif(str(14719) not in TESTS, reason='Excluded')
    def test_content_analyst_delete_an_image_14719(self):
        """Create a brand new multiple choice question.

        Steps:
        Go to Exercises
        Click on the 'Login' button
        Enter the teacher account in the username and password text boxes
        Click on the 'Sign in' button
        Click "Write a new exercise"
        Click on the "Multiple Choice" radio button if it is not already
            selected
        Fill out the required fields
        Click "Publish"

        Expected Result:
        The user gets a confirmation that says "Exercise [exercise ID] has
        published successfully"
        """
        self.ps.test_updates['name'] = 't2.11.022' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.022',
            '14719'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.sleep(2)
        self.teacher.driver.get("https://exercises-qa.openstax.org/")
        self.teacher.sleep(2)
        self.teacher.find(By.PARTIAL_LINK_TEXT, "SIGN IN").click()
        self.teacher.sleep(2)
        self.teacher.find(By.PARTIAL_LINK_TEXT, "WRITE A NEW EXERCISE").click()
        self.teacher.sleep(5)

        # Select Multiple Choice radio if not already selected
        if not self.teacher.find(
            By.XPATH,
            "//div[@class='form-group'][1]/div[@class='radio']"
        ).is_selected():
            self.teacher.find(
                By.XPATH,
                "//div[@class='form-group'][1]/div[@class='radio']/label/span"
            ).click()

        self.teacher.sleep(3)

        # Fill in required fields
        self.teacher.find(By.XPATH, "//div[4]/textarea").send_keys('Stem')
        self.teacher.find(
            By.XPATH,
            "//li[@class='correct-answer']/textarea[1]").send_keys(
            'Distractor')
        self.teacher.find(
            By.XPATH,
            "//li[@class='correct-answer']/textarea[2]").send_keys('Feedback')
        self.teacher.find(By.XPATH, "//div[6]/textarea").send_keys('Solution')

        # Save draft and publish
        self.teacher.find(
            By.XPATH,
            "//button[@class='async-button draft btn btn-info']").click()
        self.teacher.sleep(3)
        self.teacher.find(
            By.XPATH,
            "//button[@class='async-button publish btn btn-primary']").click()
        self.teacher.find(
            By.XPATH,
            "//div[@class='popover-content']/div[@class='controls']/butt" +
            "on[@class='btn btn-primary']").click()
        self.teacher.sleep(3)

        # Verify
        page = self.teacher.driver.page_source
        assert('has published successfully' in page), \
            'Exercise not successfully published'

        self.teacher.find(
            By.XPATH, "//button[@class='btn btn-primary']").click()

        self.teacher.sleep(3)

        self.ps.test_updates['passed'] = True

    # 14714 - 023 - Teacher | Preserve the order of choices for questions where
    # the choice order matters
    @pytest.mark.skipif(str(14714) not in TESTS, reason='Excluded')
    def test_teacher_preserve_the_order_of_choices_for_questions_14714(self):
        """Preserve order of choices for questions where choice order matters.

        Steps:
        Click "Write a new exercise"
        Click on the box "Order Matters"

        Expected Result:
        The user is able to preserve the order of choices
        """
        self.ps.test_updates['name'] = 't2.11.023' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.023',
            '14714'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.sleep(2)
        self.teacher.driver.get("https://exercises-qa.openstax.org/")
        self.teacher.sleep(2)
        self.teacher.find(By.PARTIAL_LINK_TEXT, "SIGN IN").click()
        self.teacher.sleep(2)
        self.teacher.find(By.PARTIAL_LINK_TEXT, "WRITE A NEW EXERCISE").click()
        self.teacher.sleep(5)

        # Select the Order Matters checkbox
        checkbox = self.teacher.find(
            By.XPATH,
            "//div[@class='question']/div[@class='form-group']/div[@class" +
            "='checkbox']/label/span")
        checkbox.click()
        self.teacher.sleep(5)

        if checkbox.is_selected():
            self.ps.test_updates['passed'] = True

    # 14716 - 024 - Teacher | Edit detailed solutions
    @pytest.mark.skipif(str(14716) not in TESTS, reason='Excluded')
    def test_teacher_edit_detailed_solutions_14716(self):
        """Edit detailed solutions.

        Steps:
        Click "Search"
        Enter the desired exercise ID
        Scroll down to "Detailed Solutions"
        Edit text in the "Detailed Solutions" text box
        Click "Publish"

        Expected Result:
        The user is able to edit detailed solutions and the change is reflected
        in the box to the right
        """
        self.ps.test_updates['name'] = 't2.11.024' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.024',
            '14716'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.sleep(2)
        self.teacher.driver.get("https://exercises-qa.openstax.org/")
        self.teacher.sleep(2)
        self.teacher.find(By.PARTIAL_LINK_TEXT, "SIGN IN").click()
        self.teacher.sleep(2)
        self.teacher.find(By.PARTIAL_LINK_TEXT, "WRITE A NEW EXERCISE").click()
        self.teacher.sleep(5)

        # Select Multiple Choice radio if not already selected
        if not self.teacher.find(
            By.XPATH,
            "//div[@class='form-group'][1]/div[@class='radio']"
        ).is_selected():
            self.teacher.find(
                By.XPATH,
                "//div[@class='form-group'][1]/div[@class='radio']/label/span"
            ).click()

        self.teacher.sleep(3)

        # Fill in required fields
        self.teacher.find(By.XPATH, "//div[4]/textarea").send_keys('Stem')
        self.teacher.find(
            By.XPATH,
            "//li[@class='correct-answer']/textarea[1]").send_keys(
            'Distractor')
        self.teacher.find(
            By.XPATH,
            "//li[@class='correct-answer']/textarea[2]").send_keys('Feedback')
        self.teacher.find(By.XPATH, "//div[6]/textarea").send_keys('Solution')

        # Save draft and publish
        self.teacher.find(
            By.XPATH,
            "//button[@class='async-button draft btn btn-info']").click()
        self.teacher.sleep(3)
        self.teacher.find(
            By.XPATH,
            "//button[@class='async-button publish btn btn-primary']").click()
        self.teacher.find(
            By.XPATH,
            "//div[@class='popover-content']/div[@class='controls']/butt" +
            "on[@class='btn btn-primary']").click()
        self.teacher.sleep(3)

        # Verify
        page = self.teacher.driver.page_source
        assert('has published successfully' in page), \
            'Exercise not successfully published'

        self.teacher.find(
            By.XPATH, "//button[@class='btn btn-primary']").click()

        self.teacher.sleep(3)

        detailed = self.teacher.find(
            By.XPATH, "//div[@class='openstax-has-html solution']")
        assert(detailed.text == 'Solution'), \
            'Detailed solution text is not what is expected'

        self.ps.test_updates['passed'] = True

    # 14709 - 025 - Teacher | Reference an embedded video
    @pytest.mark.skipif(str(14709) not in TESTS, reason='Excluded')
    def test_teacher_reference_an_embedded_video_14709(self):
        """Reference an embedded video.

        Steps:
        Click "Search"
        Enter the desired exercise ID
        Scroll down to "Detailed Solutions"
        Edit text in the "Detailed Solutions" text box
        Click "Publish"

        Expected Result:
        The user is able to edit detailed solutions and the change is reflected
        in the box to the right
        """
        self.ps.test_updates['name'] = 't2.11.025' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.025',
            '14709'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.sleep(2)
        self.teacher.driver.get("https://exercises-qa.openstax.org/")
        self.teacher.sleep(2)
        self.teacher.find(By.PARTIAL_LINK_TEXT, "SIGN IN").click()
        self.teacher.sleep(2)
        self.teacher.find(By.PARTIAL_LINK_TEXT, "WRITE A NEW EXERCISE").click()
        self.teacher.sleep(5)

        # Select Multiple Choice radio if not already selected
        if not self.teacher.find(
            By.XPATH,
            "//div[@class='form-group'][1]/div[@class='radio']"
        ).is_selected():
            self.teacher.find(
                By.XPATH,
                "//div[@class='form-group'][1]/div[@class='radio']/label/span"
            ).click()

        self.teacher.sleep(3)

        # Fill in required fields
        vid = '<iframe width="420" height="315" src="https://www.youtube.com'
        vid += '/embed/jNQXAC9IVRw" frameborder="0" allowfullscreen></iframe>'
        self.teacher.find(By.XPATH, "//div[4]/textarea").send_keys(vid)
        self.teacher.find(
            By.XPATH,
            "//li[@class='correct-answer']/textarea[1]").send_keys(
            'Distractor')
        self.teacher.find(
            By.XPATH,
            "//li[@class='correct-answer']/textarea[2]").send_keys('Feedback')
        self.teacher.find(By.XPATH, "//div[6]/textarea").send_keys('Solution')

        # Save draft and publish
        self.teacher.find(
            By.XPATH,
            "//button[@class='async-button draft btn btn-info']").click()
        self.teacher.sleep(3)
        self.teacher.find(
            By.XPATH,
            "//button[@class='async-button publish btn btn-primary']").click()
        self.teacher.find(
            By.XPATH,
            "//div[@class='popover-content']/div[@class='controls']/butt" +
            "on[@class='btn btn-primary']").click()
        self.teacher.sleep(3)

        # Verify
        page = self.teacher.driver.page_source
        assert('has published successfully' in page), \
            'Exercise not successfully published'

        self.teacher.find(
            By.XPATH, "//button[@class='btn btn-primary']").click()

        self.teacher.sleep(3)

        # Find the embedded video
        self.teacher.find(
            By.XPATH,
            "//div[@class='frame-wrapper embed-responsive embed-responsive-" +
            "4by3']/iframe")

        self.ps.test_updates['passed'] = True

    # 14713 - 026 - Teacher | Use drop down choices from tagging legend
    @pytest.mark.skipif(str(14713) not in TESTS, reason='Excluded')
    def test_teacher_use_dropdown_choices_from_tagging_legend_14713(self):
        """Use drop down choices from tagging legend.

        Steps:
        Click "Write a new exercise"
        Click "Tags"
        Click "Question Type," "DOK," "Blooms," and/or "Time"
        Select a choice from the dropdown tags

        Expected Result:
        The user is able to select a specific tag from the dropdown choices and
        the tags appear on the box to the right
        """
        self.ps.test_updates['name'] = 't2.11.026' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.026',
            '14713'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.sleep(2)
        self.teacher.driver.get("https://exercises-qa.openstax.org/")
        self.teacher.sleep(2)
        self.teacher.find(By.PARTIAL_LINK_TEXT, "SIGN IN").click()
        self.teacher.sleep(2)
        self.teacher.find(By.PARTIAL_LINK_TEXT, "WRITE A NEW EXERCISE").click()
        self.teacher.sleep(5)

        # Switch to Tags tab and find the dropdown elements
        self.teacher.find(
            By.XPATH, "//ul[@class='nav nav-tabs']/li[2]/a").click()
        self.teacher.sleep(1)
        dropdowns = self.teacher.driver.find_elements_by_xpath(
            "//select[@class='form-control']")
        self.teacher.sleep(1)

        # Select values for the dropdown menus
        dropdowns[0].send_keys('Con')
        dropdowns[1].send_keys('1')
        dropdowns[2].send_keys('3')
        dropdowns[3].send_keys('Long')

        self.teacher.sleep(5)

        self.ps.test_updates['passed'] = True

    # 14721 - 027 - Teacher | Specify whether context is required for question
    @pytest.mark.skipif(str(14721) not in TESTS, reason='Excluded')
    def test_teacher_specify_whether_context_is_required_for_quest_14721(self):
        """Specify whether context is required for a question.

        Steps:
        Click "Write a new exercise"
        Click "Tags"
        Check the box that says "Requires Context"

        Expected Result:
        The user is able to specify whether context is required for a question
        and the tag "requires-context:true" appears in the box to the right
        """
        self.ps.test_updates['name'] = 't2.11.027' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.027',
            '14721'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.sleep(2)
        self.teacher.driver.get("https://exercises-qa.openstax.org/")
        self.teacher.sleep(2)
        self.teacher.find(By.PARTIAL_LINK_TEXT, "SIGN IN").click()
        self.teacher.sleep(2)
        self.teacher.find(By.PARTIAL_LINK_TEXT, "WRITE A NEW EXERCISE").click()
        self.teacher.sleep(5)

        # Switch to Tags tab and check Requires Context
        self.teacher.find(
            By.XPATH, "//ul[@class='nav nav-tabs']/li[2]/a").click()
        self.teacher.sleep(1)
        self.teacher.find(By.XPATH, "//div[@class='tag']/input").click()
        self.teacher.sleep(3)

        if self.teacher.find(
            By.XPATH, "//div[@class='tag']/input"
        ).is_selected():
            self.ps.test_updates['passed'] = True

    # 14720 - 028 - Teacher | Add context to a question
    @pytest.mark.skipif(str(14720) not in TESTS, reason='Excluded')
    def test_teacher_add_context_to_a_question_14720(self):
        """Add context to a question.

        Steps:
        Click "Write a new exercise"
        Click "Tags"
        Check the box that says "Requires Context"
        Click "+" next to "CNX Module"
        Enter the CNX Module number

        Expected Result:
        The user is able to add context to a question
        """
        self.ps.test_updates['name'] = 't2.11.028' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.028',
            '14720'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.sleep(2)
        self.teacher.driver.get("https://exercises-qa.openstax.org/")
        self.teacher.sleep(2)
        self.teacher.find(By.PARTIAL_LINK_TEXT, "SIGN IN").click()
        self.teacher.sleep(2)
        self.teacher.find(By.PARTIAL_LINK_TEXT, "WRITE A NEW EXERCISE").click()
        self.teacher.sleep(5)

        # Switch to Tags tab and click CNX Module
        self.teacher.find(
            By.XPATH, "//ul[@class='nav nav-tabs']/li[2]/a").click()
        self.teacher.sleep(1)
        self.teacher.driver.find_elements_by_xpath(
            "//i[@class='fa fa-plus-circle']")[2].click()
        self.teacher.sleep(3)

        self.teacher.find(By.XPATH, "//input[@class='form-control']")

        self.ps.test_updates['passed'] = True

    # 14707 - 029 - Teacher | Add an image
    @pytest.mark.skipif(str(14707) not in TESTS, reason='Excluded')
    def test_teacher_add_an_image_14707(self):
        """Add an image.

        Steps:
        Click "Write a new exercise"
        Enter text into Question Stem, Distractor, and Detailed Solution
        Click "Save Draft"
        Click "Assets"
        Click "Add new image"
        Select an image

        Expected Result:
        The image and the options "Choose different image" and "Upload" should
        come up
        """
        self.ps.test_updates['name'] = 't2.11.029' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.029',
            '14707'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.sleep(2)
        self.teacher.driver.get("https://exercises-qa.openstax.org/")
        self.teacher.sleep(2)
        self.teacher.find(By.PARTIAL_LINK_TEXT, "SIGN IN").click()
        self.teacher.sleep(2)
        self.teacher.find(By.PARTIAL_LINK_TEXT, "WRITE A NEW EXERCISE").click()
        self.teacher.sleep(5)

        # Select Multiple Choice radio if not already selected
        if not self.teacher.find(
            By.XPATH,
            "//div[@class='form-group'][1]/div[@class='radio']"
        ).is_selected():
            self.teacher.find(
                By.XPATH,
                "//div[@class='form-group'][1]/div[@class='radio']/label/span"
            ).click()

        self.teacher.sleep(3)

        # Fill in required fields
        self.teacher.find(By.XPATH, "//div[4]/textarea").send_keys('Stem')
        self.teacher.find(
            By.XPATH,
            "//li[@class='correct-answer']/textarea[1]").send_keys(
            'Distractor')
        self.teacher.find(
            By.XPATH,
            "//li[@class='correct-answer']/textarea[2]").send_keys('Feedback')
        self.teacher.find(By.XPATH, "//div[6]/textarea").send_keys('Solution')

        # Save draft and publish
        self.teacher.find(
            By.XPATH,
            "//button[@class='async-button draft btn btn-info']").click()
        self.teacher.sleep(3)

        # Move to Assets and upload image
        self.teacher.find(
            By.XPATH, "//ul[@class='nav nav-tabs']/li[3]/a").click()
        self.teacher.sleep(3)
        self.teacher.find(
            By.ID, "file"
        ).send_keys(
            "/Users/openstaxii/desktop/Screen Shot 2016-06-17 at 1.15.39 PM" +
            ".png")
        self.teacher.sleep(5)

        # Find the Upload and Choose different image buttons
        self.teacher.find(By.XPATH, "//label[@class='selector']")
        self.teacher.find(By.XPATH, "//button[@class='btn btn-default']")

        self.ps.test_updates['passed'] = True

    # 14706 - 030 - Teacher | Upload an image
    @pytest.mark.skipif(str(14706) not in TESTS, reason='Excluded')
    def test_teacher_upload_an_image_14706(self):
        """Upload an image.

        Steps:
        Click "Write a new exercise"
        Enter text into Question Stem, Distractor, and Detailed Solution
        Click "Save Draft"
        Click "Assets"
        Click "Add new image"
        Select an image
        Click "Upload"

        Expected Result:
        There should be a URL and a "Delete" button
        """
        self.ps.test_updates['name'] = 't2.11.030' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.030',
            '14706'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.sleep(2)
        self.teacher.driver.get("https://exercises-qa.openstax.org/")
        self.teacher.sleep(2)
        self.teacher.find(By.PARTIAL_LINK_TEXT, "SIGN IN").click()
        self.teacher.sleep(2)
        self.teacher.find(By.PARTIAL_LINK_TEXT, "WRITE A NEW EXERCISE").click()
        self.teacher.sleep(5)

        # Select Multiple Choice radio if not already selected
        if not self.teacher.find(
            By.XPATH,
            "//div[@class='form-group'][1]/div[@class='radio']"
        ).is_selected():
            self.teacher.find(
                By.XPATH,
                "//div[@class='form-group'][1]/div[@class='radio']/label/span"
            ).click()

        self.teacher.sleep(3)

        # Fill in required fields
        self.teacher.find(By.XPATH, "//div[4]/textarea").send_keys('Stem')
        self.teacher.find(
            By.XPATH,
            "//li[@class='correct-answer']/textarea[1]").send_keys(
            'Distractor')
        self.teacher.find(
            By.XPATH,
            "//li[@class='correct-answer']/textarea[2]").send_keys('Feedback')
        self.teacher.find(By.XPATH, "//div[6]/textarea").send_keys('Solution')

        # Save draft and publish
        self.teacher.find(
            By.XPATH,
            "//button[@class='async-button draft btn btn-info']").click()
        self.teacher.sleep(3)

        # Move to Assets and upload image
        self.teacher.find(
            By.XPATH, "//ul[@class='nav nav-tabs']/li[3]/a").click()
        self.teacher.sleep(3)
        self.teacher.find(
            By.ID, "file"
        ).send_keys(
            "/Users/openstaxii/desktop/Screen Shot 2016-06-17 at 1.15.39 PM" +
            ".png")
        self.teacher.sleep(5)
        self.teacher.find(
            By.XPATH, "//button[@class='btn btn-default']").click()

        # Wait for upload and find the Delete button
        self.teacher.sleep(30)
        self.teacher.find(
            By.XPATH, "//button[@class='btn btn-default']").click()
        self.teacher.sleep(5)

        self.ps.test_updates['passed'] = True

    # 15902 - 031 - Teacher | Delete an image
    @pytest.mark.skipif(str(15902) not in TESTS, reason='Excluded')
    def test_teacher_delete_an_image_15902(self):
        """Delete an image.

        Steps:
        Click "Write a new exercise"
        Enter text into Question Stem, Distractor, and Detailed Solution
        Click "Save Draft"
        Click "Assets"
        Click "Add new image"
        Select an image
        Click "Upload"
        Click "Delete"

        Expected Result:
        The image is deleted
        """
        self.ps.test_updates['name'] = 't2.11.031' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.031',
            '15902'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.sleep(2)
        self.teacher.driver.get("https://exercises-qa.openstax.org/")
        self.teacher.sleep(2)
        self.teacher.find(By.PARTIAL_LINK_TEXT, "SIGN IN").click()
        self.teacher.sleep(2)
        self.teacher.find(By.PARTIAL_LINK_TEXT, "WRITE A NEW EXERCISE").click()
        self.teacher.sleep(5)

        # Select Multiple Choice radio if not already selected
        if not self.teacher.find(
            By.XPATH,
            "//div[@class='form-group'][1]/div[@class='radio']"
        ).is_selected():
            self.teacher.find(
                By.XPATH,
                "//div[@class='form-group'][1]/div[@class='radio']/label/span"
            ).click()

        self.teacher.sleep(3)

        # Fill in required fields
        self.teacher.find(By.XPATH, "//div[4]/textarea").send_keys('Stem')
        self.teacher.find(
            By.XPATH,
            "//li[@class='correct-answer']/textarea[1]").send_keys(
            'Distractor')
        self.teacher.find(
            By.XPATH,
            "//li[@class='correct-answer']/textarea[2]").send_keys('Feedback')
        self.teacher.find(By.XPATH, "//div[6]/textarea").send_keys('Solution')

        # Save draft and publish
        self.teacher.find(
            By.XPATH,
            "//button[@class='async-button draft btn btn-info']").click()
        self.teacher.sleep(3)

        # Move to Assets and upload image
        self.teacher.find(
            By.XPATH, "//ul[@class='nav nav-tabs']/li[3]/a").click()
        self.teacher.sleep(3)
        self.teacher.find(
            By.ID, "file"
        ).send_keys(
            "/Users/openstaxii/desktop/Screen Shot 2016-06-17 at 1.15.39 PM" +
            ".png")
        self.teacher.sleep(5)
        self.teacher.find(
            By.XPATH, "//button[@class='btn btn-default']").click()

        # Wait for upload and find the Delete button
        self.teacher.sleep(30)
        self.teacher.find(
            By.XPATH, "//button[@class='btn btn-default']").click()
        self.teacher.sleep(5)

        # Verify image is deleted
        assert len(self.teacher.driver.find_elements_by_xpath(
            "//button[@class='btn btn-default']")) == 0, \
            'Image not deleted'

        self.ps.test_updates['passed'] = True

    # 14724 - 032 - Content Analyst | Add a vocabulary question
    @pytest.mark.skipif(str(14724) not in TESTS, reason='Excluded')
    def test_content_analyst_add_a_vocabulary_question_14724(self):
        """Add a vocabulary question.

        Steps:
        Click "Write a new exercise"
        Click "New Vocabulary Term" from the header
        Fill out the required fields
        Click "Save Draft"
        Click "Publish"

        Expected Result:
        The "Publish" button is whited out and the exercise ID appears in the
        box to the right
        """
        self.ps.test_updates['name'] = 't2.11.032' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.032',
            '14724'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.content.login()
        self.content.sleep(2)
        self.content.driver.get("https://exercises-qa.openstax.org/")
        self.content.sleep(2)
        self.content.find(By.PARTIAL_LINK_TEXT, "SIGN IN").click()
        self.content.sleep(2)
        self.content.find(By.PARTIAL_LINK_TEXT, "WRITE A NEW EXERCISE").click()
        self.content.sleep(5)

        # Fill in required fields
        self.content.find(
            By.XPATH, "//a[@class='btn btn-success vocabulary blank']").click()
        self.content.sleep(1)
        self.content.find(
            By.XPATH,
            "//div[@class='form-group'][1]/input[@class='form-control']"
        ).send_keys('term')
        self.content.find(
            By.XPATH, "//div[@class='values']/input[@class='form-control']"
        ).send_keys('distractor')
        self.content.find(
            By.XPATH, "//textarea[@class='form-control']"
        ).send_keys('definition')

        # Save draft and publish
        self.content.find(
            By.XPATH,
            "//button[@class='async-button draft btn btn-info']").click()
        self.content.sleep(3)
        self.content.find(
            By.XPATH,
            "//button[@class='async-button publish btn btn-primary']").click()
        self.content.find(
            By.XPATH,
            "//div[@class='popover-content']/div[@class='controls']/butt" +
            "on[@class='btn btn-primary']").click()
        self.content.sleep(3)

        self.ps.test_updates['passed'] = True

    # 14725 - 033 - Content Analyst | Edit a vocabulary question
    @pytest.mark.skipif(str(14725) not in TESTS, reason='Excluded')
    def test_content_analyst_edit_a_vocabulary_question_14725(self):
        """Edit a vocabulary question.

        Steps:
        Click "Write a new exercise"
        Click "New Vocabulary Term" from the header
        Enter text into "Key Term," "Key Term Definition," and "Distractors"
        Click "Save Draft"
        Click "Publish"
        Copy the exercise ID
        Click "Back"
        Paste the exercise ID
        Enter new text into the aforementioned text boxes and the rest of the
            fields if desired
        Click "Save Draft"
        Click "Publish"

        Expected Result:
        The user is able to edit and save a vocabulary question
        """
        self.ps.test_updates['name'] = 't2.11.033' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.033',
            '14725'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.content.login()
        self.content.sleep(2)
        self.content.driver.get("https://exercises-qa.openstax.org/")
        self.content.sleep(2)
        self.content.find(By.PARTIAL_LINK_TEXT, "SIGN IN").click()
        self.content.sleep(2)
        self.content.find(By.PARTIAL_LINK_TEXT, "WRITE A NEW EXERCISE").click()
        self.content.sleep(5)

        # Fill in required fields
        self.content.find(
            By.XPATH, "//a[@class='btn btn-success vocabulary blank']").click()
        self.content.sleep(2)
        self.content.find(
            By.XPATH,
            "//div[@class='form-group'][1]/input[@class='form-control']"
        ).send_keys('term')
        self.content.sleep(2)
        self.content.find(
            By.XPATH,
            "//div[@class='values']/input[@class='form-control']"
        ).send_keys('distractor')
        self.content.find(
            By.XPATH, "//textarea[@class='form-control']"
        ).send_keys('definition')

        # Save draft and publish
        self.content.find(
            By.XPATH,
            "//button[@class='async-button draft btn btn-info']").click()
        self.content.sleep(3)
        self.content.find(
            By.XPATH,
            "//button[@class='async-button publish btn btn-primary']").click()
        self.content.find(
            By.XPATH,
            "//div[@class='popover-content']/div[@class='controls']/butt" +
            "on[@class='btn btn-primary']").click()
        self.content.sleep(3)

        # Get exercise ID
        exercise = self.content.current_url().split('/')[-1].split('@')[0]

        # Go back and search for the exercise
        self.content.find(
            By.XPATH, "//a[@class='btn btn-danger back']").click()
        self.content.sleep(3)
        self.content.find(
            By.XPATH, "//input[@class='form-control']").send_keys(exercise)
        self.content.find(
            By.XPATH, "//button[@class='btn btn-default load']").click()
        self.content.sleep(5)

        # Edit
        self.content.find(
            By.XPATH,
            "//div[@class='form-group'][1]/input[@class='form-control']"
        ).send_keys('term')
        self.content.sleep(2)
        self.content.find(
            By.XPATH,
            "//div[@class='values']/input[@class='form-control']"
        ).send_keys('distractor')
        self.content.find(
            By.XPATH, "//textarea[@class='form-control']"
        ).send_keys('definition')

        # Save draft and publish
        self.content.find(
            By.XPATH,
            "//button[@class='async-button draft btn btn-info']").click()
        self.content.sleep(3)
        self.content.find(
            By.XPATH,
            "//button[@class='async-button publish btn btn-primary']").click()
        self.content.find(
            By.XPATH,
            "//div[@class='popover-content']/div[@class='controls']/butt" +
            "on[@class='btn btn-primary']").click()
        self.content.sleep(3)

        self.ps.test_updates['passed'] = True

    # 14735 - 034 - Content Analyst | Review a vocabulary question
    @pytest.mark.skipif(str(14735) not in TESTS, reason='Excluded')
    def test_content_analyst_review_a_vocabulary_question_14735(self):
        """Review a vocabulary question.

        Steps:
        Click "Search"
        Enter the desired exercise ID

        Expected Result:
        The vocabulary question loads and user is able to review it
        """
        self.ps.test_updates['name'] = 't2.11.034' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.034',
            '14735'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.content.login()
        self.content.sleep(2)
        self.content.driver.get("https://exercises-qa.openstax.org/")
        self.content.sleep(2)
        self.content.find(By.PARTIAL_LINK_TEXT, "SIGN IN").click()
        self.content.sleep(2)
        self.content.driver.get("https://exercises-qa.openstax.org/search")
        self.content.sleep(5)

        # Search for a vocabulary exercise
        self.content.sleep(3)
        self.content.find(
            By.XPATH, "//input[@class='form-control']").send_keys('16535')
        self.content.find(
            By.XPATH, "//button[@class='btn btn-default load']").click()
        self.content.sleep(5)

        # Verify
        stem = self.content.find(
            By.XPATH, "//div[@class='openstax-has-html question-stem']/strong")

        assert(stem.text == 'v'), \
            'Question stem not as expected'

        self.ps.test_updates['passed'] = True

    # 14799 - 035 - Teacher | Add vocabulary question
    @pytest.mark.skipif(str(14799) not in TESTS, reason='Excluded')
    def test_teacher_add_a_vocabulary_question_14799(self):
        """Add vocabulary question.

        Steps:
        Go to Exercises
        Click on the 'Login' button
        Enter the teacher account in the username and password text boxes
        Click on the 'Sign in' button
        Click "Write a new exercise"
        Click "New Vocabulary Term" from the header
        Fill in the required fields
        Click "Save Draft"
        Click "Publish"

        Expected Result:
        The "Publish" button is whited out and the exercise ID appears in the
        box to the right
        """
        self.ps.test_updates['name'] = 't2.11.035' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.035',
            '14799'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.sleep(2)
        self.teacher.driver.get("https://exercises-qa.openstax.org/")
        self.teacher.sleep(2)
        self.teacher.find(By.PARTIAL_LINK_TEXT, "SIGN IN").click()
        self.teacher.sleep(2)
        self.teacher.find(By.PARTIAL_LINK_TEXT, "WRITE A NEW EXERCISE").click()
        self.teacher.sleep(5)

        # Fill in required fields
        self.teacher.find(
            By.XPATH, "//a[@class='btn btn-success vocabulary blank']").click()
        self.teacher.sleep(1)
        self.teacher.find(
            By.XPATH,
            "//div[@class='form-group'][1]/input[@class='form-control']"
        ).send_keys('term')
        self.teacher.find(
            By.XPATH, "//div[@class='values']/input[@class='form-control']"
        ).send_keys('distractor')
        self.teacher.find(
            By.XPATH, "//textarea[@class='form-control']"
        ).send_keys('definition')

        # Save draft and publish
        self.teacher.find(
            By.XPATH,
            "//button[@class='async-button draft btn btn-info']").click()
        self.teacher.sleep(3)
        self.teacher.find(
            By.XPATH,
            "//button[@class='async-button publish btn btn-primary']").click()
        self.teacher.find(
            By.XPATH,
            "//div[@class='popover-content']/div[@class='controls']/butt" +
            "on[@class='btn btn-primary']").click()
        self.teacher.sleep(3)

        self.ps.test_updates['passed'] = True

    # 14727 - 036 - Teacher | Edit vocabulary questions
    @pytest.mark.skipif(str(14727) not in TESTS, reason='Excluded')
    def test_teacher_edit_vocabulary_questions_14727(self):
        """Edit vocabulary questions.

        Steps:
        Click "Write a new exercise"
        Click "New Vocabulary Term" from the header
        Enter text into "Key Term," "Key Term Definition," and "Distractors"
        Click "Save Draft"
        Click "Publish"
        Copy the exercise ID
        Click "Back"
        Paste the exercise ID
        Enter new text into the aforementioned text boxes and the rest of the
            fields if desired
        Click "Save Draft"
        Click "Publish"

        Expected Result:
        The user is able to edit and save a vocabulary question
        """
        self.ps.test_updates['name'] = 't2.11.036' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.036',
            '14727'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.sleep(2)
        self.teacher.driver.get("https://exercises-qa.openstax.org/")
        self.teacher.sleep(2)
        self.teacher.find(By.PARTIAL_LINK_TEXT, "SIGN IN").click()
        self.teacher.sleep(2)
        self.teacher.find(By.PARTIAL_LINK_TEXT, "WRITE A NEW EXERCISE").click()
        self.teacher.sleep(5)

        # Fill in required fields
        self.teacher.find(
            By.XPATH, "//a[@class='btn btn-success vocabulary blank']").click()
        self.teacher.sleep(2)
        self.teacher.find(
            By.XPATH,
            "//div[@class='form-group'][1]/input[@class='form-control']"
        ).send_keys('term')
        self.teacher.sleep(2)
        self.teacher.find(
            By.XPATH,
            "//div[@class='values']/input[@class='form-control']"
        ).send_keys('distractor')
        self.teacher.find(
            By.XPATH, "//textarea[@class='form-control']"
        ).send_keys('definition')

        # Save draft and publish
        self.teacher.find(
            By.XPATH,
            "//button[@class='async-button draft btn btn-info']").click()
        self.teacher.sleep(3)
        self.teacher.find(
            By.XPATH,
            "//button[@class='async-button publish btn btn-primary']").click()
        self.teacher.find(
            By.XPATH,
            "//div[@class='popover-content']/div[@class='controls']/butt" +
            "on[@class='btn btn-primary']").click()
        self.teacher.sleep(3)

        # Get exercise ID
        exercise = self.teacher.current_url().split('/')[-1].split('@')[0]

        # Go back and search for the exercise
        self.teacher.find(
            By.XPATH, "//a[@class='btn btn-danger back']").click()
        self.teacher.sleep(3)
        self.teacher.find(
            By.XPATH, "//input[@class='form-control']").send_keys(exercise)
        self.teacher.find(
            By.XPATH, "//button[@class='btn btn-default load']").click()
        self.teacher.sleep(5)

        # Edit
        self.teacher.find(
            By.XPATH,
            "//div[@class='form-group'][1]/input[@class='form-control']"
        ).send_keys('term')
        self.teacher.sleep(2)
        self.teacher.find(
            By.XPATH,
            "//div[@class='values']/input[@class='form-control']"
        ).send_keys('distractor')
        self.teacher.find(
            By.XPATH, "//textarea[@class='form-control']"
        ).send_keys('definition')

        # Save draft and publish
        self.teacher.find(
            By.XPATH,
            "//button[@class='async-button draft btn btn-info']").click()
        self.teacher.sleep(3)
        self.teacher.find(
            By.XPATH,
            "//button[@class='async-button publish btn btn-primary']").click()
        self.teacher.find(
            By.XPATH,
            "//div[@class='popover-content']/div[@class='controls']/butt" +
            "on[@class='btn btn-primary']").click()
        self.teacher.sleep(3)

        self.ps.test_updates['passed'] = True

    # 14734 - 037 - Teacher | Review vocabulary questions
    @pytest.mark.skipif(str(14734) not in TESTS, reason='Excluded')
    def test_teacher_review_vocabulary_questions_14734(self):
        """Review vocabulary questions.

        Steps:
        Click "Search"
        Enter the desired exercise ID

        Expected Result:
        The vocabulary question loads and user is able to review it
        """
        self.ps.test_updates['name'] = 't2.11.037' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.037',
            '14734'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.sleep(2)
        self.teacher.driver.get("https://exercises-qa.openstax.org/")
        self.teacher.sleep(2)
        self.teacher.find(By.PARTIAL_LINK_TEXT, "SIGN IN").click()
        self.teacher.sleep(2)
        self.teacher.driver.get("https://exercises-qa.openstax.org/search")
        self.teacher.sleep(5)

        # Search for a vocabulary exercise
        self.teacher.sleep(3)
        self.teacher.find(
            By.XPATH, "//input[@class='form-control']").send_keys('16535')
        self.teacher.find(
            By.XPATH, "//button[@class='btn btn-default load']").click()
        self.teacher.sleep(5)

        # Verify
        stem = self.teacher.find(
            By.XPATH, "//div[@class='openstax-has-html question-stem']/strong")

        assert(stem.text == 'v'), \
            'Question stem not as expected'

        self.ps.test_updates['passed'] = True

    # 14728 - 038 - Content Analyst | "Show 2-Step Preview" checkbox and free-
    # response or multiple-choice are displaye
    @pytest.mark.skipif(str(14728) not in TESTS, reason='Excluded')
    def test_content_analyst_show_2_step_preview_checkbox_and_free_14728(self):
        """Review vocabulary questions.

        Steps:
        Go to Tutor
        Click on the 'Login' button
        Enter the content analyst user account in the username and password
            text boxes
        Click on the 'Sign in' button
        Click "QA Content" from the user menu
        Click on a non-introductory section
        Check the box that says "Show 2-Step Preview"

        Expected Result:
        The user is presented with a free response text box and multiple choice
        question
        """
        self.ps.test_updates['name'] = 't2.11.038' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.038',
            '14728'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.content.login()
        self.content.open_user_menu()
        self.content.find(By.PARTIAL_LINK_TEXT, "QA Content").click()
        self.content.sleep(8)

        # Click the 2 step preview checkbox, find the free response text box
        self.content.find(
            By.XPATH,
            "//ul[@class='section'][1]/li[3]/ul[@class='section']/li/a"
        ).click()
        self.content.find(
            By.XPATH, "//div[@class='heading']/label/span").click()
        self.content.find(
            By.XPATH, "//div[@class='exercise-free-response-preview']")
        self.content.sleep(3)

        self.ps.test_updates['passed'] = True

    # 14729 - 039 - Content Analyst | Multiple choice and True/False do not
    # have a free response
    @pytest.mark.skipif(str(14729) not in TESTS, reason='Excluded')
    def test_content_analyst_multiple_choice_and_true_false_do_not_14729(self):
        """Review vocabulary questions.

        Steps:
        Click "QA Content" from the user menu
        Click on a non-introductory section
        Check the box that says "Show 2-Step Preview"
        Scroll to a multiple choice only question or true/false question

        Expected Result:
        If the question is only multiple choice or true/false, it does not have
        a free response box
        """
        self.ps.test_updates['name'] = 't2.11.039' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.039',
            '14729'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        # //div[@class='exercise-free-response-preview']
        self.content.login()
        self.content.open_user_menu()
        self.content.find(By.PARTIAL_LINK_TEXT, "QA Content").click()
        self.content.sleep(8)

        # Click the 2 step preview checkbox
        self.content.find(
            By.XPATH,
            "//ul[@class='section'][1]/li[3]/ul[@class='section']/li/a"
        ).click()
        self.content.find(
            By.XPATH, "//div[@class='heading']/label/span").click()

        # Count the number of free responses and total questions
        free = self.content.driver.find_elements_by_xpath(
            "//div[@class='exercise-free-response-preview']")
        q = self.content.driver.find_elements_by_xpath(
            "//div[@class='detailed-solution']/div[@class='header']")
        self.content.sleep(3)

        assert(len(free) < len(q)), \
            'No MC questions to check against'

        self.ps.test_updates['passed'] = True

    # 14798 - 040 - Content Analyst | Filter assessments by type
    @pytest.mark.skipif(str(14798) not in TESTS, reason='Excluded')
    def test_content_analyst_filter_assessments_by_type_14798(self):
        """Filter assessments by type.

        Steps:
        Click "QA Content" from the user menu
        Click on a non-introductory section
        Click "Exercise Types"
        Select the options that you do not want

        Expected Result:
        The user is able to filter assessments by type
        """
        self.ps.test_updates['name'] = 't2.11.040' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.040',
            '14798'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.content.login()
        self.content.open_user_menu()
        self.content.find(By.PARTIAL_LINK_TEXT, "QA Content").click()
        self.content.sleep(8)

        # Uncheck all of the exercise types
        self.content.find(
            By.XPATH,
            "//ul[@class='section'][1]/li[3]/ul[@class='section']/li/a"
        ).click()

        for index, num in enumerate(range(5)):
            self.content.find(By.XPATH, "//button[@id='multi-select']").click()
            check = self.content.driver.find_elements_by_xpath(
                "//a/span[@class='title']")
            check[index].click()
            self.content.sleep(2)

        # Zero exercises should be visible
        q = self.content.driver.find_elements_by_xpath(
            "//div[@class='detailed-solution']/div[@class='header']")

        assert(len(q) == 0), \
            'Exercises should not be visible'

        self.content.sleep(3)

        self.ps.test_updates['passed'] = True

    # 14730 - 041 - Content Analyst | View human-created question IDs
    @pytest.mark.skipif(str(14730) not in TESTS, reason='Excluded')
    def test_content_analyst_view_human_created_question_ids_14730(self):
        """View human-created question IDs.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.11.041' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.041',
            '14730'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 14731 - 042 - Content Analyst | Hide the non-visible tags for faculty and
    # students
    @pytest.mark.skipif(str(14731) not in TESTS, reason='Excluded')
    def test_content_analyst_hide_the_nonvisible_tags_for_faculty_14731(self):
        """Hide the non-visible tags for faculty and students.

        Steps:
        Click "QA Content" from the user menu
        Click on a non-introductory section
        Open an incognito window
        Sign in as teacher01
        Click on the same course that you are viewing in QA Content as content
            analyst
        Go to Question Library
        Click on the same section that you are viewing in QA Content as content
            analyst
        Pick an assessment

        Expected Result:
        The assessment in the teacher view should not have the tags that the
        assessment has in QA Content view
        """
        self.ps.test_updates['name'] = 't2.11.042' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.042',
            '14731'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.content.login()
        self.content.open_user_menu()
        self.content.find(By.PARTIAL_LINK_TEXT, "QA Content").click()
        self.content.sleep(8)

        # Go to a non introductory section
        self.content.find(
            By.XPATH,
            "//ul[@class='section'][1]/li[3]/ul[@class='section']/li/a"
        ).click()
        self.content.sleep(10)

        # Verify the book is physics
        title = self.content.find(By.XPATH, "//li[@class='title']").text
        if title.find('Physics') < 0:
            self.content.find(
                By.XPATH, "//a[@id='available-books']/span[1]").click()
            books = self.content.driver.find_elements_by_xpath(
                "//a[@class='book']/div[@class='title-version']")
            for book in books:
                if book.text.find('Physics') >= 0:
                    book.click()
                    self.content.sleep(10)
                    self.content.find(
                        By.XPATH,
                        "//ul[@class='section'][1]/li[3]/ul" +
                        "[@class='section']/li/a"
                    ).click()
                    break

        qa_tags = len(self.content.driver.find_elements_by_xpath(
            "//span[@class='exercise-tag']"))
        qa_tags += len(self.content.driver.find_elements_by_xpath(
            "//span[@class='lo-tag']"))
        self.content.sleep(3)

        # Login as teacher and go to question library
        self.teacher.login()
        self.teacher.select_course(appearance='physics')
        self.teacher.sleep(5)

        self.teacher.open_user_menu()
        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Question Library').click()
        self.teacher.sleep(5)

        # Open the assessment cards
        self.teacher.find(
            By.XPATH,
            "//div[@class='panel-group'][1]" +
            "/div[@class='panel panel-default']" +
            "/div[@class='panel-collapse collapse in']" +
            "/div[@class='panel-body']/div[@class='section'][2]" +
            "/span[@class='section-checkbox']").click()
        self.teacher.find(
            By.XPATH, "//button[@class='btn btn-primary']").click()
        self.teacher.sleep(5)

        # Go to question details
        element = self.teacher.find(
            By.XPATH, "//div[@class = 'controls-overlay'][1]")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(element)
        actions.perform()
        self.teacher.sleep(2)
        self.teacher.find(By.XPATH, "//div[@class='action details']").click()
        self.teacher.sleep(2)

        tags = 0
        # Ensure looking at the first question card
        while "fa fa-angle-left" in self.teacher.driver.page_source:
            self.teacher.find(
                By.XPATH, "//i[@class='tutor-icon fa fa-angle-left']").click()

        # Go through each assessment card and count the tags
        while "fa fa-angle-right" in self.teacher.driver.page_source:
            tags += len(self.teacher.driver.find_elements_by_xpath(
                "//span[@class='exercise-tag']"))
            tags += len(self.teacher.driver.find_elements_by_xpath(
                "//span[@class='lo-tag']"))
            self.teacher.find(
                By.XPATH, "//i[@class='tutor-icon fa fa-angle-right']").click()

        self.teacher.sleep(5)

        assert(qa_tags > tags), \
            'There should be more visible tags for content'

        self.ps.test_updates['passed'] = True

    # 14732 - 043 - Content Analyst | View all tags in the Assesment QA View
    @pytest.mark.skipif(str(14732) not in TESTS, reason='Excluded')
    def test_content_analyst_view_all_tags_in_assessment_qa_view_14732(self):
        """View all tags in the Assesment QA View.

        Steps:
        Click "QA Content" from the user menu
        Click on a non-introductory section
        Scroll/look to the bottom of an assessment card

        Expected Result:
        The user is presented with all the tags for an assessment
        """
        self.ps.test_updates['name'] = 't2.11.043' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.043',
            '14732'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.content.login()
        self.content.open_user_menu()
        self.content.find(By.PARTIAL_LINK_TEXT, "QA Content").click()
        self.content.sleep(8)

        # Go to a non introductory section
        self.content.find(
            By.XPATH,
            "//ul[@class='section'][1]/li[3]/ul[@class='section']/li/a"
        ).click()
        self.content.sleep(10)

        # Verify the book is physics
        title = self.content.find(By.XPATH, "//li[@class='title']").text
        if title.find('Physics') < 0:
            self.content.find(
                By.XPATH, "//a[@id='available-books']/span[1]").click()
            books = self.content.driver.find_elements_by_xpath(
                "//a[@class='book']/div[@class='title-version']")
            for book in books:
                if book.text.find('Physics') >= 0:
                    book.click()
                    self.content.sleep(10)
                    self.content.find(
                        By.XPATH,
                        "//ul[@class='section'][1]/li[3]/ul" +
                        "[@class='section']/li/a"
                    ).click()
                    break

        qa_tags = len(self.content.driver.find_elements_by_xpath(
            "//span[@class='exercise-tag']"))
        qa_tags += len(self.content.driver.find_elements_by_xpath(
            "//span[@class='lo-tag']"))
        self.content.sleep(3)

        assert(qa_tags > 0), \
            'No tags found'

        self.ps.test_updates['passed'] = True

    # 14736 - 044 - Content Analyst | Create a new multi-part question
    @pytest.mark.skipif(str(14736) not in TESTS, reason='Excluded')
    def test_content_analyst_create_a_new_multipart_question_14736(self):
        """Create a new multi-part question.

        Steps:
        Click "Write a new exercise"
        Check the box that says "Exercise contains multiple parts"
        Fill out the required fields
        Click "Save Draft"
        Click "Publish"

        Expected Result:
        The user gets a confirmation that says "Exercise [exercise ID] has
        published successfully"
        """
        self.ps.test_updates['name'] = 't2.11.044' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.044',
            '14736'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.content.login()
        self.content.sleep(2)
        self.content.driver.get("https://exercises-qa.openstax.org/")
        self.content.sleep(2)
        self.content.find(By.PARTIAL_LINK_TEXT, "SIGN IN").click()
        self.content.sleep(2)
        self.content.find(By.PARTIAL_LINK_TEXT, "WRITE A NEW EXERCISE").click()
        self.content.sleep(5)

        # Select Multiple Choice radio if not already selected
        if not self.content.find(
            By.XPATH,
            "//div[@class='form-group'][1]/div[@class='radio']"
        ).is_selected():
            self.content.find(
                By.XPATH,
                "//div[@class='form-group'][1]/div[@class='radio']/label/span"
            ).click()

        self.content.sleep(3)

        # Fill in required fields
        self.content.find(By.XPATH, "//div[4]/textarea").send_keys('Stem')
        self.content.find(
            By.XPATH,
            "//li[@class='correct-answer']/textarea[1]").send_keys(
            'Distractor')
        self.content.find(
            By.XPATH,
            "//li[@class='correct-answer']/textarea[2]").send_keys('Feedback')
        self.content.find(By.XPATH, "//div[6]/textarea").send_keys('Solution')
        self.content.sleep(2)

        # Check multiple parts box, move to Question 2 tab
        self.content.find(
            By.XPATH,
            "//div[@class='mpq-toggle']/div[@class='checkbox']/label/span"
        ).click()
        self.content.find(By.XPATH, "//li[3]/a").click()
        self.content.sleep(2)

        # Fill in the required fields
        self.content.find(By.XPATH, "//div[5]/textarea").send_keys('Stem')
        self.content.find(
            By.XPATH,
            "//div[6]/ol/li[@class='correct-answer']/textarea[1]").send_keys(
            'Distractor')
        self.content.find(
            By.XPATH,
            "//div[6]/ol/li[@class='correct-answer']/textarea[2]"
        ).send_keys('Feedback')
        self.content.find(By.XPATH, "//div[7]/textarea").send_keys('Solution')
        self.content.sleep(2)

        # Save draft and publish
        self.content.find(
            By.XPATH,
            "//button[@class='async-button draft btn btn-info']").click()
        self.content.sleep(3)
        self.content.find(
            By.XPATH,
            "//button[@class='async-button publish btn btn-primary']").click()
        self.content.find(
            By.XPATH,
            "//div[@class='popover-content']/div[@class='controls']/butt" +
            "on[@class='btn btn-primary']").click()
        self.content.sleep(3)

        # Verify
        page = self.content.driver.page_source
        assert('has published successfully' in page), \
            'Exercise not successfully published'

        self.content.find(
            By.XPATH, "//button[@class='btn btn-primary']").click()

        self.content.sleep(3)

        self.ps.test_updates['passed'] = True

    # 14737 - 045 - Teacher | Create a new multi-part question
    @pytest.mark.skipif(str(14737) not in TESTS, reason='Excluded')
    def test_teacher_create_a_new_multipart_question_14737(self):
        """Create a new multi-part question.

        Steps:
        Go to Exercises
        Click on the 'Login' button
        Enter the teacher account in the username and password text boxes
        Click on the 'Sign in' button
        Click "Write a new exercise"
        Check the box that says "Exercise contains multiple parts"
        Fill out the required fields
        Click "Publish"

        Expected Result:
        The user gets a confirmation that says "Exercise [exercise ID] has
        published successfully"
        """
        self.ps.test_updates['name'] = 't2.11.045' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.045',
            '14737'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.sleep(2)
        self.teacher.driver.get("https://exercises-qa.openstax.org/")
        self.teacher.sleep(2)
        self.teacher.find(By.PARTIAL_LINK_TEXT, "SIGN IN").click()
        self.teacher.sleep(2)
        self.teacher.find(By.PARTIAL_LINK_TEXT, "WRITE A NEW EXERCISE").click()
        self.teacher.sleep(5)

        # Select Multiple Choice radio if not already selected
        if not self.teacher.find(
            By.XPATH,
            "//div[@class='form-group'][1]/div[@class='radio']"
        ).is_selected():
            self.teacher.find(
                By.XPATH,
                "//div[@class='form-group'][1]/div[@class='radio']/label/span"
            ).click()

        self.teacher.sleep(3)

        # Fill in required fields
        self.teacher.find(By.XPATH, "//div[4]/textarea").send_keys('Stem')
        self.teacher.find(
            By.XPATH,
            "//li[@class='correct-answer']/textarea[1]").send_keys(
            'Distractor')
        self.teacher.find(
            By.XPATH,
            "//li[@class='correct-answer']/textarea[2]").send_keys('Feedback')
        self.teacher.find(By.XPATH, "//div[6]/textarea").send_keys('Solution')
        self.teacher.sleep(2)

        # Check multiple parts box, move to Question 2 tab
        self.teacher.find(
            By.XPATH,
            "//div[@class='mpq-toggle']/div[@class='checkbox']/label/span"
        ).click()
        self.teacher.find(By.XPATH, "//li[3]/a").click()
        self.teacher.sleep(2)

        # Fill in the required fields
        self.teacher.find(By.XPATH, "//div[5]/textarea").send_keys('Stem')
        self.teacher.find(
            By.XPATH,
            "//div[6]/ol/li[@class='correct-answer']/textarea[1]").send_keys(
            'Distractor')
        self.teacher.find(
            By.XPATH,
            "//div[6]/ol/li[@class='correct-answer']/textarea[2]"
        ).send_keys('Feedback')
        self.teacher.find(By.XPATH, "//div[7]/textarea").send_keys('Solution')
        self.teacher.sleep(2)

        # Save draft and publish
        self.teacher.find(
            By.XPATH,
            "//button[@class='async-button draft btn btn-info']").click()
        self.teacher.sleep(3)
        self.teacher.find(
            By.XPATH,
            "//button[@class='async-button publish btn btn-primary']").click()
        self.teacher.find(
            By.XPATH,
            "//div[@class='popover-content']/div[@class='controls']/butt" +
            "on[@class='btn btn-primary']").click()
        self.teacher.sleep(3)

        # Verify
        page = self.teacher.driver.page_source
        assert('has published successfully' in page), \
            'Exercise not successfully published'

        self.teacher.find(
            By.XPATH, "//button[@class='btn btn-primary']").click()

        self.teacher.sleep(3)

        self.ps.test_updates['passed'] = True
