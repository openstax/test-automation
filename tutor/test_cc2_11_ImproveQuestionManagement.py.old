"""Concept Coach v2, Epic 11 - Improve Question Management."""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
# from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver import ActionChains
from staxing.assignment import Assignment

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Teacher, Student

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
        14851, 14852, 14856, 14858, 14859,
        # not implemented
        # 100129, 100130
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestIImproveQuestionManagement(unittest.TestCase):
    """CC2.11 - Improve Question Management."""

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
            self.student = Student(
                use_env_vars=True,
                existing_driver=self.teacher.driver,
                pasta_user=self.ps,
                capabilities=self.desired_capabilities
            )
        else:
            self.teacher = Teacher(
                use_env_vars=True
            )
            self.student = Student(
                use_env_vars=True,
                existing_driver=self.teacher.driver,
            )

    def tearDown(self):
        """Test destructor."""
        if not LOCAL_RUN:
            self.ps.update_job(
                job_id=str(self.teacher.driver.session_id),
                **self.ps.test_updates
            )
        self.student = None
        try:
            self.teacher.delete()
        except:
            pass

    # 14851 - 001 - Teacher | Review all questions
    @pytest.mark.skipif(str(14851) not in TESTS, reason='Excluded')
    def test_teacher_review_all_questions_14851(self):
        """Review all questions.

        Steps:
        Go to Tutor
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a CC course name
        Click "Question Library" from the user menu
        Select a section or chapter
        Click "Show Questions"

        Expected Result:
        The user is presented with all the questions for the section or chapter
        """
        self.ps.test_updates['name'] = 'cc2.11.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.11', 'cc2.11.001', '14851']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.find(
            By.XPATH, '//a[contains(@href,"/cc-dashboard")]'
        ).click()
        self.teacher.open_user_menu()
        self.teacher.find(
            By.LINK_TEXT, 'Question Library'
        ).click()
        self.teacher.find(
            By.XPATH,
            '//div[@class="section"]//span[@class="chapter-section" ' +
            'and @data-chapter-section="1.1"]'
        ).click()
        self.teacher.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        self.teacher.find(
            By.XPATH, '//button[text()="Show Questions"]'
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="exercises"]')
            )
        )
        self.ps.test_updates['passed'] = True

    # 14852 - 002 - Teacher | Exclude certain questions
    @pytest.mark.skipif(str(14852) not in TESTS, reason='Excluded')
    def test_teacher_exclude_certain_questions_14852(self):
        """Exclude certain quesitons.

        Steps:
        If the user has more than one course, click on a CC course name
        Click "Question Library" from the user menu
        Select a section or chapter
        Click "Show Questions"
        Hover over the desired question and click "Exclude question"

        Expected Result:
        Question is grayed out
        """
        self.ps.test_updates['name'] = 'cc2.11.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.11', 'cc2.11.002', '14852']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.find(
            By.XPATH, '//a[contains(@href,"/cc-dashboard")]'
        ).click()
        self.teacher.open_user_menu()
        self.teacher.find(
            By.LINK_TEXT, 'Question Library'
        ).click()
        self.teacher.find(
            By.XPATH,
            '//div[@class="section"]//span[@class="chapter-section" ' +
            'and @data-chapter-section="1.2"]'
        ).click()
        self.teacher.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        self.teacher.find(
            By.XPATH, '//button[text()="Show Questions"]'
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="exercises"]')
            )
        )
        self.teacher.sleep(1)
        i = 1
        question = None
        # loop finding a question that is not yet excleded
        # there are 9 question in the exact textbook and chpater this test
        # is searching. limiting loop at 7 incase questions are removed.
        while i < 8:
            question = self.teacher.find(
                By.XPATH,
                '//div[@class="exercises"]/div[' + str(i) + ']'
            )
            if ('is-selected' not in question.get_attribute('class')):
                break
            i += 1
        Assignment.scroll_to(self.teacher.driver, question)
        self.teacher.sleep(1)
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(question)
        # way to stall because not sure how to add wait in action chain
        for _ in range(50):
            actions.move_by_offset(-1, 0)
        actions.click()
        actions.move_by_offset(-50, -300)
        actions.perform()
        self.teacher.sleep(0.5)
        question_excluded = self.teacher.find(
            By.XPATH, '//div[@class="exercises"]/div[' + str(i) + ']'
        ).get_attribute('class')
        assert('is-selected' in question_excluded), 'question not excluded'
        self.ps.test_updates['passed'] = True

    '''
    # 14855 - 003 - Teacher | Pin tabs on top of screen when scrolled
    @pytest.mark.skipif(str(14855) not in TESTS, reason='Excluded')
    def test_teacher_pin_tabs_on_top_of_screen_when_scrolled_14855(self):
        """Pin tabs on top of screen when scrolled.

        Steps:
        If the user has more than one course, click on a CC course name
        Click "Question Library" from the user menu
        Select a section or chapter
        Click "Show Questions"
        Scroll down

        Expected Result:
        Tabs are pinned to top of the screen when scrolled
        """
        self.ps.test_updates['name'] = 'cc2.11.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.11', 'cc2.11.003', '14855']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.find(
            By.XPATH, '//a[contains(@href,"/cc-dashboard")]'
        ).click()
        self.teacher.open_user_menu()
        self.teacher.find(
            By.LINK_TEXT, 'Question Library'
        ).click()
        self.teacher.find(
            By.XPATH,
            '//div[@class="section"]//span[@class="chapter-section" ' +
            'and @data-chapter-section="1.2"]'
        ).click()
        self.teacher.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        self.teacher.find(
            By.XPATH, '//button[text()="Show Questions"]'
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="exercises"]')
            )
        )
        self.teacher.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="pinned-header"]')
            )
        )
        self.ps.test_updates['passed'] = True
    '''

    # 14856 - 004 - Teacher | Make section links jumpable
    @pytest.mark.skipif(str(14856) not in TESTS, reason='Excluded')
    def test_teacher_make_section_links_jumpable_14856(self):
        """Make section links jumpable.

        Steps:
        If the user has more than one course, click on a CC course name
        Click "Question Library" from the user menu
        Select a section or chapter
        Click "Show Questions"
        Click on the section links at the top of the screen

        Expected Result:
        The screen scrolls to the selected questions
        """
        self.ps.test_updates['name'] = 'cc2.11.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.11', 'cc2.11.004', '14856']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.find(
            By.XPATH, '//a[contains(@href,"/cc-dashboard")]'
        ).click()
        self.teacher.open_user_menu()
        self.teacher.find(
            By.LINK_TEXT, 'Question Library'
        ).click()
        self.teacher.find(
            By.XPATH,
            '//div[@class="section"]//span[@class="chapter-section" ' +
            'and @data-chapter-section="1.2"]'
        ).click()
        self.teacher.find(
            By.XPATH,
            '//div[@class="section"]//span[@class="chapter-section" ' +
            'and @data-chapter-section="1.1"]'
        ).click()

        self.teacher.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        self.teacher.find(
            By.XPATH, '//button[text()="Show Questions"]'
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="exercises"]')
            )
        )
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[@class="pinned-header"]'
                 '//div[@class="section" and text()="1.2"]')
            )
        ).click()
        self.teacher.sleep(1)
        # click the heading as simple way to find that it is on screen
        # and not just visible but scrolled off screen
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[@class="exercise-sections"]' +
                 '//span[@class="chapter-section" ' +
                 'and @data-chapter-section="1.2"]')
            )
        ).click()
        self.ps.test_updates['passed'] = True

    # 14858 - 005 - Teacher | Report errata about assessments in Concept Coach
    @pytest.mark.skipif(str(14858) not in TESTS, reason='Excluded')
    def test_teacher_report_errata_about_assessments_in_cc_14858(self):
        """Report errata about assessments in Concept Coach.

        Steps:
        If the user has more than one course, click on a CC course name
        Click "Question Library" from the user menu
        Select a section or chapter
        Click "Show Questions"
        Hover over the desired question and click "Question details"
        Click "Report an error"

        Expected Result:
        A new tab with the assessment errata form appears, with the assessment
        ID already filled in
        """
        self.ps.test_updates['name'] = 'cc2.11.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.11', 'cc2.11.005', '14858']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.find(
            By.XPATH, '//a[contains(@href,"/cc-dashboard")]'
        ).click()
        self.teacher.open_user_menu()
        self.teacher.find(
            By.LINK_TEXT, 'Question Library'
        ).click()
        self.teacher.find(
            By.XPATH,
            '//div[@class="section"]//span[@class="chapter-section" ' +
            'and @data-chapter-section="1.2"]'
        ).click()
        self.teacher.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        self.teacher.find(
            By.XPATH, '//button[text()="Show Questions"]'
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="exercises"]')
            )
        )
        self.teacher.sleep(1)
        question = self.teacher.find(
            By.XPATH, '//div[@class="exercises"]/div[1]'
        )
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(question)
        # way to stall because not sure how to add wait in action chain
        for _ in range(50):
            actions.move_by_offset(1, 0)
        actions.click()
        actions.perform()
        self.teacher.sleep(0.5)
        exercise_id = self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//span[@class="exercise-tag" and contains(text(),"ID:")]')
            )
        ).text
        question = self.teacher.find(
            By.XPATH, '//div[@class="action report-error"]'
        ).click()
        window_with_form = self.teacher.driver.window_handles[1]
        self.teacher.driver.switch_to_window(window_with_form)
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[text()="Report Content Errors"]')
            )
        )
        self.teacher.find(
            By.XPATH, '//input[@value="' + exercise_id[4:] + '"]')

        self.ps.test_updates['passed'] = True

    # 14859 - 006 - Student | Report errata about assessments in Concept Coach
    @pytest.mark.skipif(str(14859) not in TESTS, reason='Excluded')
    def test_student_report_errata_about_assessments_in_cc_14859(self):
        """Report errata about assessments in Concept Coach.

        Steps:
        Click on a CC course, if there are more than one
        Click on a non-introductory section
        Click "Jump to Concept Coach"
        Click "Launch Concept Coach"
        Click "Report an error" on an assessment

        Expected Result:
        A new tab with the assessment errata form appears, with the assessment
        ID already filled in
        """
        self.ps.test_updates['name'] = 'cc2.11.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.11', 'cc2.11.006', '14859']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.login()
        self.teacher.find(
            By.XPATH, '//a[contains(@href,"cnx.org/contents/")]'
        ).click()
        # get to non-into section
        self.student.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button//span[text()="Contents"]')
            )
        ).click()
        self.student.sleep(0.5)
        self.student.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//span[@class="chapter-number" and text()="1.1"]')
            )
        ).click()
        # open concept coach
        self.student.wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Jump to Concept Coach')
            )
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[text()="Launch Concept Coach"]')
            )
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//span[contains(@class,"core breadcrumb-exercise")]')
            )
        ).click()
        exercise_id = self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//span[@class="exercise-identifier-link"]' +
                 '/span[contains(text(),"@")]')
            )
        ).text
        self.teacher.find(By.LINK_TEXT, 'Report an error').click()
        window_with_form = self.teacher.driver.window_handles[1]
        self.teacher.driver.switch_to_window(window_with_form)
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[text()="Report Content Errors"]')
            )
        )
        self.teacher.find(
            By.XPATH, '//input[@value="' + exercise_id + '"]')
        self.ps.test_updates['passed'] = True

    # 100129 - 007 - Admin | View list of excluded assesments
    @pytest.mark.skipif(str(100129) not in TESTS, reason='Excluded')
    def test_admin_view_list_of_excluded_assesments_100129(self):
        """View list of excluded assesments.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 'cc2.11.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc2',
            'cc2.11',
            'cc2.11.007',
            '100129'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 100130 - 008 - Admin | Export the list of excluded assesments to CSV
    @pytest.mark.skipif(str(100130) not in TESTS, reason='Excluded')
    def test_admin_export_the_list_of_excluded_assesments_to_csv_100130(self):
        """Export the list of excluded assesments to CSV.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 'cc2.11.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc2',
            'cc2.11',
            'cc2.11.008',
            '100130'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
