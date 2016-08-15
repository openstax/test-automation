"""Tutor v1, Epic 55 - Practice."""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
# from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from staxing.assignment import Assignment
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
# from selenium.common.exceptions import TimeoutException

from staxing.helper import Student

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
        8297, 8298, 8299, 8300, 8301,
        8302, 8303, 8304, 8305, 8306,
        8307, 8308, 8309, 8310
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestPractice(unittest.TestCase):
    """T1.55 - Practice."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.student = Student(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        self.student.login()
        self.student.select_course(appearance='biology')
        self.wait = WebDriverWait(self.student.driver, Assignment.WAIT_TIME)
        self.wait.until(
            expect.visibility_of_element_located((
                By.XPATH,
                '//button[contains(@aria-describedby,"progress-bar-tooltip")]'
            ))
        ).click()

    def tearDown(self):
        """Test destructor."""
        self.ps.update_job(
            job_id=str(self.student.driver.session_id),
            **self.ps.test_updates
        )
        try:
            self.student.delete()
        except:
            pass

    # Case C8297 - 001 - Student | Click on a section performance forecast bar
    # to start practice session
    @pytest.mark.skipif(str(8297) not in TESTS, reason='Excluded')
    def test_student_click_on_a_section__bar_to_start_practice_8297(self):
        """Click on a section performance forecast bar to start a practice

        Steps:
        Click one of the section performance bars from the dashboard (in setup)

        Expected Result:
        The user is taken to a practice session for the section.
        """
        self.ps.test_updates['name'] = 't1.55.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.55', 't1.55.001', '8297']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assert('practice' in self.student.current_url()), \
            'Not in practice assignment'

        self.ps.test_updates['passed'] = True

    # Case C8298 - 002 - Student | Navigate between questions using breadcrumbs
    @pytest.mark.skipif(str(8298) not in TESTS, reason='Excluded')
    def test_student_navigate_between_questions_using_breadcrumbs_8298(self):
        """Navigate between questions using the breadcrumbs.

        Steps:
        Click a breadcrumb

        Expected Result:
        The student is taken to a different question in the practice session.
        """
        self.ps.test_updates['name'] = 't1.55.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.55', 't1.55.002', '8298']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        sections = self.student.driver.find_elements(
            By.XPATH, '//span[contains(@class,"breadcrumbs")]')
        section = sections[-2]
        chapter = section.get_attribute("data-reactid")
        section.click()
        self.student.driver.find_element(
            By.XPATH,
            '//div[contains(@data-question-number,"%s")]' %
            (int(chapter[-1]) + 1)
        )

        self.ps.test_updates['passed'] = True

    # Case C8299 - 003 - Student | Scrolling the window up reveals the header
    @pytest.mark.skipif(str(8299) not in TESTS, reason='Excluded')
    def test_student_scrolling_the_window_up_reveals_the_header_bar_8299(self):
        """Scrolling the window up reveals the header bar.

        Steps:
        Scroll down
        Scroll to the top of the page

        Expected Result:
        The header bar, containing the course name, OpenStax logo,
        and user menu link is visible.
        """
        self.ps.test_updates['name'] = 't1.55.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.55', 't1.55.003', '8299']
        self.ps.test_updates['passed'] = False

        # answer free response first
        # so that mc questions appear and there is enough text to scroll
        try:
            self.student.driver.find_element(
                By.TAG_NAME, 'textarea').send_keys("hello")
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//button/span[contains(text(),"Answer")]')
                )
            ).click()
        except NoSuchElementException:
            pass
        # scroll page
        self.student.driver.execute_script("window.scrollTo(0, 100);")
        self.student.driver.execute_script("window.scrollTo(0, 0);")
        self.student.driver.find_element(By.CLASS_NAME, 'ui-brand-logo')

        self.ps.test_updates['passed'] = True

    # Case C8300 - 004 - Student | Inputting a free response activates the
    # Answer button
    @pytest.mark.skipif(str(8300) not in TESTS, reason='Excluded')
    def test_student_inputting_a_free_response_activates_the_button_8300(self):
        """Inputting a free response into activates the Answer button.

        Steps:
        If there is a text box: input text
            OR
        Click on the next breadcrumb until a textbox is available

        Expected Result:
        The "Answer" button is click-able.
        """
        self.ps.test_updates['name'] = 't1.55.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.55', 't1.55.004', '8300']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        sections = self.student.driver.find_elements(
            By.XPATH, '//span[contains(@class,"breadcrumbs")]')
        for x in range(len(sections)):
            try:
                element = self.student.driver.find_element(
                    By.TAG_NAME, 'textarea')
                for i in 'hello':
                    element.send_keys(i)
                self.wait.until(
                    expect.element_to_be_clickable(
                        (By.XPATH, '//button/span[contains(text(),"Answer")]')
                    )
                )
                break
            except NoSuchElementException:
                if x >= len(sections)-1:
                    print('no questions in this practice with free respnse')
                    raise Exception
                sections_new = self.student.driver.find_elements(
                    By.XPATH, '//span[contains(@class,"breadcrumbs")]')
                sections_new[x].click()

        self.ps.test_updates['passed'] = True

    # Case C8301 - 005 - Student | Answer a free reponse question
    @pytest.mark.skipif(str(8301) not in TESTS, reason='Excluded')
    def test_student_answer_a_free_response_question_8301(self):
        """Answer a free reponse question.

        Steps:
        If there is a text box, input text
        Click the "Answer" button

        Expected Result:
        The text box disappears and the multiple choice answer appear.
        """
        self.ps.test_updates['name'] = 't1.55.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.55', 't1.55.005', '8301']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        sections = self.student.driver.find_elements(
            By.XPATH, '//span[contains(@class,"breadcrumbs")]')
        answer_text = "hello"
        for x in range(len(sections)):
            try:
                element = self.student.driver.find_element(
                    By.TAG_NAME, 'textarea')
                for i in answer_text:
                    element.send_keys(i)
                self.wait.until(
                    expect.element_to_be_clickable(
                        (By.XPATH, '//button/span[contains(text(),"Answer")]')
                    )
                ).click()
                break
            except NoSuchElementException:
                if x >= len(sections) - 1:
                    print('no questions in this homework with free respnse')
                    raise Exception
                sections_new = self.student.driver.find_elements(
                    By.XPATH, '//span[contains(@class,"breadcrumbs")]')
                sections_new[x].click()

        self.student.driver.find_element(
            By.XPATH,
            '//div[@class="free-response" and contains(text(),"' +
            answer_text + '")]')
        self.student.driver.find_element(
            By.XPATH, '//div[@class="answer-letter"]')

        self.ps.test_updates['passed'] = True

    # Case C8302 - 006 - Student | Selecting a multiple choice answer activates
    # the Submit button
    @pytest.mark.skipif(str(8302) not in TESTS, reason='Excluded')
    def test_student_selecting_a_mc_answer_activates_submit_button_8302(self):
        """Selecting a multiple choice answer activates the Submit button.

        Steps:
        If there is a text box, input text
        Click the "Answer" button
        Select a multiple choice answer

        Expected Result:
        The "Submit" button can now be clicked
        """
        self.ps.test_updates['name'] = 't1.55.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.55', 't1.55.006', '8302']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        try:
            # if the question is two part must answer free response first
            element = self.student.driver.find_element(
                By.TAG_NAME, 'textarea')
            answer_text = "hello"
            for i in answer_text:
                element.send_keys(i)
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//button/span[contains(text(),"Answer")]')
                )
            ).click()
        except NoSuchElementException:
            pass
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"question-stem")]')
            )
        )
        element = self.student.driver.find_element(
            By.XPATH, '//div[@class="answer-letter"]')
        self.student.driver.execute_script(
            'return arguments[0].scrollIntoView();', element)
        self.student.driver.execute_script('window.scrollBy(0, -150);')
        element.click()
        self.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button/span[contains(text(),"Submit")]')
            )
        )

        self.ps.test_updates['passed'] = True

    # Case C8303 - 007 - Student | Submit the assessment
    @pytest.mark.skipif(str(8303) not in TESTS, reason='Excluded')
    def test_student_submit_the_assesment_8303(self):
        """Submit the assessment.

        Steps:
        If there is a text box, input text
        Click the "Answer" button
        Select a multiple choice answer
        Click the "Submit" button

        Expected Result:
        The answer is submitted and the 'Next Question' button appears.
        """
        self.ps.test_updates['name'] = 't1.55.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.55', 't1.55.007', '8303']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        try:
            # if the question is two part must answer free response first
            element = self.student.driver.find_element(By.TAG_NAME, 'textarea')
            answer_text = "hello"
            for i in answer_text:
                element.send_keys(i)
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//button/span[contains(text(),"Answer")]')
                )
            ).click()
        except NoSuchElementException:
            pass
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"question-stem")]')
            )
        )
        element = self.student.driver.find_element(
            By.XPATH, '//div[@class="answer-letter"]')
        self.student.driver.execute_script(
            'return arguments[0].scrollIntoView();', element)
        self.student.driver.execute_script('window.scrollBy(0, -150);')
        element.click()
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button/span[contains(text(),"Submit")]')
            )
        ).click()
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button/span[contains(text(),"Next Question")]')
            )
        )

        self.ps.test_updates['passed'] = True

    # Case C8304 - 008 - Student | Answer feedback is presented
    @pytest.mark.skipif(str(8304) not in TESTS, reason='Excluded')
    def test_student_answer_feedback_is_presented_8304(self):
        """Answer feedback is presented.

        Steps:
        If there is a text box, input text
        Click the "Answer" button
        Select a multiple choice answer
        Click the "Submit" button

        Expected Result:
        The answer is submitted, the correct answer is displayed,
        and feedback on the answer is given.
        """
        self.ps.test_updates['name'] = 't1.55.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.55', 't1.55.008', '8304']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        try:
            # if the question is two part must answer free response first
            element = self.student.driver.find_element(By.TAG_NAME, 'textarea')
            answer_text = "hello"
            for i in answer_text:
                element.send_keys(i)
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//button/span[contains(text(),"Answer")]')
                )
            ).click()
        except NoSuchElementException:
            pass
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"question-stem")]')
            )
        )
        element = self.student.driver.find_element(
            By.XPATH, '//div[@class="answer-letter"]')
        self.student.driver.execute_script(
            'return arguments[0].scrollIntoView();', element)
        self.student.driver.execute_script('window.scrollBy(0, -150);')
        element.click()
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button/span[contains(text(),"Submit")]')
            )
        ).click()
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//span[contains(@class,"breadcrumbs")]' +
                 '//i[contains(@class,"correct") or ' +
                 'contains(@class,"incorrect")]')
            )
        )

        self.ps.test_updates['passed'] = True

    # Case C8305 - 009 - Student | Correctness for a completed assesment is
    # displayed in the breadcrumbs
    @pytest.mark.skipif(str(8305) not in TESTS, reason='Excluded')
    def test_student_correctness_is_displayed_in_the_breadcrumbs_8305(self):
        """Correctness for a completed assessment is displayed in breadcrumbs

        Steps:
        If there is a text box, input text
        Click the "Answer" button
        Select a multiple choice answer
        Click the "Submit" button

        Expected Result:
        The correctness for the completed question is visible in the breadcrumb
        """
        self.ps.test_updates['name'] = 't1.55.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.55', 't1.55.009', '8305']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        try:
            # if the question is two part must answer free response first
            element = self.student.driver.find_element(By.TAG_NAME, 'textarea')
            answer_text = "hello"
            for i in answer_text:
                element.send_keys(i)
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//button/span[contains(text(),"Answer")]')
                )
            ).click()
        except NoSuchElementException:
            pass
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"question-stem")]')
            )
        )
        element = self.student.driver.find_element(
            By.XPATH, '//div[@class="answer-letter"]')
        self.student.driver.execute_script(
            'return arguments[0].scrollIntoView();', element)
        self.student.driver.execute_script('window.scrollBy(0, -150);')
        element.click()
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button/span[contains(text(),"Submit")]')
            )
        ).click()
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"question-feedback")]')
            )
        )

        self.ps.test_updates['passed'] = True

    # Case C8306 - 010 - Student | The assessment identification number and
    # version are visible
    @pytest.mark.skipif(str(8306) not in TESTS, reason='Excluded')
    def test_student_assesment_id_number_and_version_are_visible_8306(self):
        """The assessment id number and version are visible for each assessment

        Steps:
        Navigate through each question in the assessment

        Expected Result:
        Each question's identification number and version are visible.
        """
        self.ps.test_updates['name'] = 't1.55.0010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.55', 't1.55.010', '8306']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[contains(text(),"ID#")]')
            )
        )
        self.student.driver.find_element(
            By.XPATH, '//span[contains(text(),"@")]')

        self.ps.test_updates['passed'] = True

    # Case C8307 - 011 - Student | Clicking on Report an error renders the
    # Assessment Errata Form and prefills the assessment
    @pytest.mark.skipif(str(8307) not in TESTS, reason='Excluded')
    def test_student_clicking_on_report_an_error_renders_form_8307(self):
        """Clicking on Report an error renders the Assessment Errata Form

        Steps:
        Click the "Report an error" link

        Expected Result:
        The user is taken to the Assessment Errata Form and the ID is prefilled
        """
        self.ps.test_updates['name'] = 't1.55.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.55', 't1.55.011', '8307']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        id_num = self.student.driver.find_element(
            By.XPATH,
            '//span[contains(@class,"exercise-identifier-link")]//span[2]'
        ).text
        self.wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'Report an error')
            )
        ).click()
        window_with_form = self.student.driver.window_handles[1]
        self.student.driver.switch_to_window(window_with_form)
        self.student.page.wait_for_page_load()
        self.student.driver.find_element(
            By.XPATH, '//h1[contains(text(),"Errata Form")]')
        text_box = self.student.driver.find_element(
            By.XPATH, '//input[contains(@aria-label,"Example:")]')
        assert(text_box.get_attribute('value') == id_num), \
            'form not prefilled correctly'

        self.ps.test_updates['passed'] = True

    # Case C8308 - 012 - Student | Submit the Assessment Errata Form
    @pytest.mark.skipif(str(8308) not in TESTS, reason='Excluded')
    def test_student_submit_the_assesment_errata_form_8308(self):
        """Submit the Assessment Errata Form.

        Steps:
        Click the "Report an error" link
        Fill out the fields
        Click the "Submit" button

        Expected Result:
        The form is submitted
        """
        self.ps.test_updates['name'] = 't1.55.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.55', 't1.55.011', '8307']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'Report an error')
            )
        ).click()
        window_with_form = self.student.driver.window_handles[1]
        self.student.driver.switch_to_window(window_with_form)
        self.student.page.wait_for_page_load()
        self.student.driver.find_element(
            By.XPATH, '//h1[contains(text(),"Assessment Errata Form")]')
        # fill out form
        self.student.driver.find_element(
            By.TAG_NAME, 'textarea').send_keys('qa test')
        self.student.driver.find_element(
            By.XPATH, '//input[contains(@value,"Minor")]').click()
        self.student.driver.find_element(
            By.XPATH, '//input[contains(@value,"other")]').click()
        self.student.driver.find_element(
            By.XPATH, '//input[contains(@value,"Biology with Courseware")]'
        ).click()
        self.student.driver.find_element(
            By.XPATH, '//input[contains(@value,"Safari")]').click()
        self.student.driver.find_element(
            By.XPATH, '//input[contains(@value,"Submit")]').click()
        # find submitted message
        self.student.driver.find_element(
            By.XPATH,
            '//div[contains(text(),"Your response has been recorded")]')

        self.ps.test_updates['passed'] = True

    # Case C8309 - 013 - Student | End of practice shows the number of
    # assessments answered
    @pytest.mark.skipif(str(8309) not in TESTS, reason='Excluded')
    def test_student_end_of_practice_shows_the_number_answered_8309(self):
        """End of practice shows the number of assessments answered.

        Steps:
        Answer some of the assesments
        Click on the last breadcrumb

        Expected Result:
        End of practice shows the number of assessments answered
        """
        self.ps.test_updates['name'] = 't1.55.013' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.55', 't1.55.013', '8309']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        sections = self.student.driver.find_elements(
            By.XPATH, '//span[contains(@class,"breadcrumbs")]')
        stop_point = len(sections)//2

        for _ in range(stop_point):
            try:
                # if the question is two part must answer free response first
                element = self.student.driver.find_element(
                    By.TAG_NAME, 'textarea')
                answer_text = "hello"
                for i in answer_text:
                    element.send_keys(i)
                self.wait.until(
                    expect.visibility_of_element_located(
                        (By.XPATH, '//button/span[contains(text(),"Answer")]')
                    )
                ).click()
            except NoSuchElementException:
                pass
            # answer the mc portion
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//div[contains(@class,"question-stem")]')
                )
            )
            element = self.student.driver.find_element(
                By.XPATH, '//div[@class="answer-letter"]')
            self.student.driver.execute_script(
                'return arguments[0].scrollIntoView();', element)
            self.student.driver.execute_script('window.scrollBy(0, -150);')
            element.click()
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//button/span[contains(text(),"Submit")]')
                )
            ).click()
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH,
                     '//button/span[contains(text(),"Next Question")]')
                )
            ).click()
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[contains(@class,"breadcrumb-end")]')
            )
        ).click()
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"completed-message")]')
            )
        ).click()
        self.student.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"completed-message")]' +
            '//span[contains(@data-reactid,"0.1") and contains(text(),"' +
            str(stop_point) + '")]')
        self.student.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"completed-message")]' +
            '//span[contains(@data-reactid,"0.3") and contains(text(),"' +
            str(len(sections) - 1) + '")]')

        self.ps.test_updates['passed'] = True

    # Case C8310 - 014 - Student | Back To Dashboard button returns the user
    # to the dashboard
    @pytest.mark.skipif(str(8310) not in TESTS, reason='Excluded')
    def test_student_back_to_dashboard_button_returns_to_dashboard_8310(self):
        """Clicking the Back To Dashboard button returns user to the dashboard.

        Steps:
        Answer all the assessments
        Click the "Back To Dashboard" button

        Expected Result:
        The user is returned to the dashboard
        """
        self.ps.test_updates['name'] = 't1.55.014' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.55', 't1.55.014', '8310']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        sections = self.student.driver.find_elements(
            By.XPATH, '//span[contains(@class,"breadcrumbs")]')
        for _ in range(len(sections) - 1):
            try:
                # if the question is two part must answer free response first
                element = self.student.driver.find_element(
                    By.TAG_NAME, 'textarea')
                answer_text = "hello"
                for i in answer_text:
                    element.send_keys(i)
                self.wait.until(
                    expect.visibility_of_element_located(
                        (By.XPATH, '//button/span[contains(text(),"Answer")]')
                    )
                ).click()
            except NoSuchElementException:
                pass
            # answer the free response portion
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//div[contains(@class,"question-stem")]')
                )
            )
            element = self.student.driver.find_element(
                By.XPATH, '//div[@class="answer-letter"]')
            self.student.driver.execute_script(
                'return arguments[0].scrollIntoView();', element)
            self.student.driver.execute_script('window.scrollBy(0, -150);')
            element.click()
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//button/span[contains(text(),"Submit")]')
                )
            ).click()
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH,
                     '//button/span[contains(text(),"Next Question")]')
                )
            ).click()
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[contains(text(),"Back to Dashboard")]')
            )
        ).click()
        assert('list' in self.student.current_url()), \
            'Not returned to list dashboard'

        self.ps.test_updates['passed'] = True
