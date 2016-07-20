"""Tutor v1, Epic 28 - Work a reading."""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
from random import randint  # NOQA
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By  # NOQA
from selenium.webdriver.support import expected_conditions as expect  # NOQA
from staxing.assignment import Assignment  # NOQA

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Teacher  # NOQA
from staxing.helper import Student

# for template command line testing only
# - replace list_of_cases on line 31 with all test case IDs in this file
# - replace CaseID on line 52 with the actual cass ID
# - delete lines 17 - 22
list_of_cases = 0
CaseID = 0

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': '50.0',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([8206])  # NOQA
)
'''
8184, 8185, 8186, 8187, 8188, 8189, 
        8190, 8191, 8192, 8193, 8194, 8195, 
        8196, 8197, 8198, 8199, 8200, 8201, 
        8202, 8203, 8204, 8205, 8206
'''

# Use the long reading for 8189, 8190, 8191, 8192, and 8206
# May need to make the long reading shorter, five chapters still causes hanging

@PastaDecorator.on_platforms(BROWSERS)
class TestEpicName(unittest.TestCase):
    """T1.28 - Work a reading."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        # self.Student = Student(
        #    use_env_vars=True,
        #    pasta_user=self.ps,
        #    capabilities=self.desired_capabilities
        # )
        self.student = Student(use_env_vars=True)
        self.student.login()

    def tearDown(self):
        """Test destructor."""
        self.ps.update_job(job_id=str(self.student.driver.session_id),
                           **self.ps.test_updates)
        try:
            self.student.delete()
        except:
            pass

    # Case C8184 - 001 - Student | Start a reading assignment
    @pytest.mark.skipif(str(8184) not in TESTS, reason='Excluded')  # NOQA
    def test_student_start_a_reading_assignment(self):
        """Start a reading assignment

        Steps:
        Click on a reading assignment under the tab "This Week" on the dashboard

        Expected Result:
        The user is presented with the first page of the reading assignment
        """
        self.ps.test_updates['name'] = 't1.28.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.28',
            't1.28.001',
            '8184'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.select_course(appearance='physics')
        assert('list' in self.student.current_url()), \
            'Not viewing the calendar dashboard'

        assignments = self.student.driver.find_elements_by_tag_name("time")
        for assignment in assignments:
            if (assignment.text == 'Dec 31, 8:54am'):
                assignment.click()
                break

        name = self.student.find(By.CLASS_NAME, 'center-control-assignment')

        assert('December Reading' in name.text), \
            'Not viewing the reading'
        
        self.student.sleep(5)

        self.ps.test_updates['passed'] = True

    # Case C8185 - 002 - Student | Due date is listed in the footer
    @pytest.mark.skipif(str(8185) not in TESTS, reason='Excluded')  # NOQA
    def test_student_due_date_is_listed_in_the_footer(self):
        """Due date is listed in the footer

        Steps:
        Click on a reading assignment under the tab "This Week" on the dashboard

        Expected Result:
        The user is presented with the due date in the right corner of the footer.
        
        self.ps.test_updates['name'] = 't1.28.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.28',
            't1.28.002',
            '8185'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True
        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # Case C8186 - 003 - Student | Reading sections are listed in the footer
    @pytest.mark.skipif(str(8186) not in TESTS, reason='Excluded')  # NOQA
    def test_student_reading_sections_are_listed_in_the_footer(self):
        """Reading sections are listed in the footer

        Steps:
        Click on a reading assignment under the tab "This Week" on the dashboard

        Expected Result:
        The user is presented with the reading sections in the footer.
        
        self.ps.test_updates['name'] = 't1.28.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.28',
            't1.28.003',
            '8186'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True
        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # Case C8187 - 004 - Student | Reading sections in the footer link to the respective section in the reference book
    @pytest.mark.skipif(str(8187) not in TESTS, reason='Excluded')  # NOQA
    def test_student_reading_sections_in_the_footer_link_to_the_respective_section_in_the_reference_book(self):
        """Reading sections in the footer link to the respective section in the reference book

        Steps:
        Click on a reading assignment under the tab "This Week" on the dashboard
        Click on one of the reading sections in the footer

        Expected Result:
        The user is presented with that reading section in the reference book
        
        self.ps.test_updates['name'] = 't1.28.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.28',
            't1.28.004',
            '8187'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True
        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # Case C8188 - 005 - Student | Click the Continue button in the footer to go to the next reading section
    @pytest.mark.skipif(str(8188) not in TESTS, reason='Excluded')  # NOQA
    def test_student_click_the_continue_button_in_the_footer_to_go_to_the_next_reading_section(self):
        """Click the Continue button in the footer to go to the next reading section

        Steps:
        Click on a reading assignment under the tab "This Week" on the dashboard
        Click on the "Continue" button in the left corner of the footer

        Expected Result:
        The user is presented with the next reading section
        """
        self.ps.test_updates['name'] = 't1.28.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.28',
            't1.28.005',
            '8188'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.select_course(appearance='physics')
        assert('list' in self.student.current_url()), \
            'Not viewing the calendar dashboard'

        assignments = self.student.driver.find_elements_by_tag_name("time")
        for assignment in assignments:
            if (assignment.text == 'Dec 31, 8:54am'):
                assignment.click()
                break

        name = self.student.find(By.CLASS_NAME, 'center-control-assignment')

        assert('December Reading' in name.text), \
            'Not viewing the reading'

        assert('/steps/1/' in self.student.current_url()), \
            'Not on the first page of the reading'

        self.student.find(By.XPATH, "//a[contains(@class,'arrow') and contains(@class,'right')]").click()

        assert('/steps/2/' in self.student.current_url()), \
            'Not on the first page of the reading'

        self.student.sleep(2)
        self.ps.test_updates['passed'] = True
        

        #raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # Case C8189 - 006 - Student | If a card has a assessment free response textbox, inputting a free response activates the Answer button
    @pytest.mark.skipif(str(8189) not in TESTS, reason='Excluded')  # NOQA
    def test_student_inputting_free_repsponse_activates_answer_button(self):
        """If a card has a assessment free response textbox, inputting a free response activates the Answer button

        Steps:
        Click on a reading assignment under the tab "This Week" on the dashboard
        Click the "Continue" button 
        On a card with a free response assessment, enter a free response into the free response assessment text box

        Expected Result:
        The "Continue" button is activated
        """
        self.ps.test_updates['name'] = 't1.28.story' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.28',
            't1.28.story',
            '8189'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.select_course(appearance='physics')
        assert('list' in self.student.current_url()), \
            'Not viewing the calendar dashboard'

        assignments = self.student.driver.find_elements_by_tag_name("time")
        for assignment in assignments:
            if (assignment.text == 'Dec 31, 8:54am'):
                assignment.click()
                break

        name = self.student.find(By.CLASS_NAME, 'center-control-assignment')

        assert('December Reading' in name.text), \
            'Not viewing the reading'

        #self.student.driver.find_elements_by_link_text('')[3].click()
        while (1):
            while ('arrow right' in self.student.driver.page_source):
                self.student.find(By.XPATH, "//a[contains(@class,'arrow') and contains(@class,'right')]").click()
            #self.student.find(By.XPATH, "//a[contains(@class,'arrow') and contains(@class,'right')]").click()
            #self.student.find(By.XPATH, "//a[contains(@class,'arrow') and contains(@class,'right')]").click()
            
            # multiple choice case
            if('exercise-multiple-choice' in self.student.driver.page_source):
                

                answers = self.student.driver.find_elements(By.CLASS_NAME, 'answer-letter')
                self.student.sleep(0.8)
                rand = randint(0, len(answers) - 1)
                answer = chr(ord('a') + rand)
                #print('Selecting %s' % answer)
                Assignment.scroll_to(self.student.driver, answers[0])
                if answer == 'a':
                    self.student.driver.execute_script('window.scrollBy(0, -160);')
                elif answer == 'd':
                    self.student.driver.execute_script('window.scrollBy(0, 160);')
                answers[rand].click()


                self.student.wait.until(
                    expect.element_to_be_clickable(
                        (By.XPATH, '//button[contains(@class,"async-button") and contains(@class,"continue")]')
                    )
                ).click()
                self.student.sleep(5)
                assert('question-feedback bottom' in self.student.driver.page_source), \
                    'Did not submit MC'


            # free response case
            elif('textarea' in self.student.driver.page_source):
                self.student.find(By.TAG_NAME, 'textarea').send_keys('An answer for this textarea')
                self.student.sleep(2)
                self.student.wait.until(
                    expect.element_to_be_clickable(
                        (By.XPATH, '//button[contains(@class,"async-button") and contains(@class,"continue")]')
                    )
                )
                self.student.sleep(3)
                break

        


        self.ps.test_updates['passed'] = True

    # Case C8190 - 007 - Student | Submit a free response answer
    @pytest.mark.skipif(str(8190) not in TESTS, reason='Excluded')  # NOQA
    def test_student_submit_a_free_response_answer(self):
        """Submit a free response answer

        Steps:
        Click on a reading assignment under the tab "This Week" on the dashboard
        Click the "Continue" button 
        On a card with a free response assessment, enter a free response into the free response assessment text box
        Click the "Continue" button

        Expected Result:
        A free response answer is submitted and the multiple choice is presented to the user
        """
        self.ps.test_updates['name'] = 't1.28.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.28',
            't1.28.007',
            '8190'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.select_course(appearance='physics')
        assert('list' in self.student.current_url()), \
            'Not viewing the calendar dashboard'

        assignments = self.student.driver.find_elements_by_tag_name("time")
        for assignment in assignments:
            if (assignment.text == 'Dec 31, 8:54am'):
                assignment.click()
                break

        name = self.student.find(By.CLASS_NAME, 'center-control-assignment')

        assert('December Reading' in name.text), \
            'Not viewing the reading'

        while(1):
            while ('arrow right' in self.student.driver.page_source):
                self.student.find(By.XPATH, "//a[contains(@class,'arrow') and contains(@class,'right')]").click()

            # multiple choice case
            if('exercise-multiple-choice' in self.student.driver.page_source):
                

                answers = self.student.driver.find_elements(By.CLASS_NAME, 'answer-letter')
                self.student.sleep(0.8)
                rand = randint(0, len(answers) - 1)
                answer = chr(ord('a') + rand)
                #print('Selecting %s' % answer)
                Assignment.scroll_to(self.student.driver, answers[0])
                if answer == 'a':
                    self.student.driver.execute_script('window.scrollBy(0, -160);')
                elif answer == 'd':
                    self.student.driver.execute_script('window.scrollBy(0, 160);')
                answers[rand].click()


                self.student.wait.until(
                    expect.element_to_be_clickable(
                        (By.XPATH, '//button[contains(@class,"async-button") and contains(@class,"continue")]')
                    )
                ).click()
                self.student.sleep(5)
                assert('question-feedback bottom' in self.student.driver.page_source), \
                    'Did not submit MC'

            # free response case
            elif('textarea' in self.student.driver.page_source):
                self.student.find(By.TAG_NAME, 'textarea').send_keys('An answer for this textarea')
                self.student.sleep(2)
                self.student.wait.until(
                    expect.element_to_be_clickable(
                        (By.XPATH, '//button[contains(@class,"async-button") and contains(@class,"continue")]')
                    )
                ).click()

                self.student.wait.until(
                    expect.visibility_of_element_located(
                        (By.CLASS_NAME, 'exercise-multiple-choice')
                    )
                )

                self.student.sleep(2)
                break

        self.ps.test_updates['passed'] = True

    # Case C8191 - 008 - Student | Selecting a multiple choice answer activates the Submit button
    @pytest.mark.skipif(str(8191) not in TESTS, reason='Excluded')  # NOQA
    def test_student_selecting_a_multiple_choice_answer_activates_the_submit_button(self):
        """Selecting a multiple choice answer activates the Submit button

        Steps:
        Click on a reading assignment under the tab "This Week" on the dashboard
        Click the "Continue" button 
        On a card with a free response assessment, enter a free response into the free response assessment text box
        Click the "Continue" button
        Select a multiple choice answer

        Expected Result:
        The "Continue" button is activated
        """
        self.ps.test_updates['name'] = 't1.28.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.28',
            't1.28.008',
            '8191'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.select_course(appearance='physics')
        assert('list' in self.student.current_url()), \
            'Not viewing the calendar dashboard'

        assignments = self.student.driver.find_elements_by_tag_name("time")
        for assignment in assignments:
            if (assignment.text == 'Dec 31, 8:54am'):
                assignment.click()
                break

        name = self.student.find(By.CLASS_NAME, 'center-control-assignment')

        assert('December Reading' in name.text), \
            'Not viewing the reading'

        while(1):
            while ('arrow right' in self.student.driver.page_source):
                self.student.find(By.XPATH, "//a[contains(@class,'arrow') and contains(@class,'right')]").click()

            # multiple choice case
            if('exercise-multiple-choice' in self.student.driver.page_source):
                

                answers = self.student.driver.find_elements(By.CLASS_NAME, 'answer-letter')
                self.student.sleep(0.8)
                rand = randint(0, len(answers) - 1)
                answer = chr(ord('a') + rand)
                #print('Selecting %s' % answer)
                Assignment.scroll_to(self.student.driver, answers[0])
                if answer == 'a':
                    self.student.driver.execute_script('window.scrollBy(0, -160);')
                elif answer == 'd':
                    self.student.driver.execute_script('window.scrollBy(0, 160);')
                answers[rand].click()


                self.student.wait.until(
                    expect.element_to_be_clickable(
                        (By.XPATH, '//button[contains(@class,"async-button") and contains(@class,"continue")]')
                    )
                )
                self.student.sleep(5)
                break

            # free response case
            elif('textarea' in self.student.driver.page_source):
                self.student.find(By.TAG_NAME, 'textarea').send_keys('An answer for this textarea')
                self.student.sleep(2)
                self.student.wait.until(
                    expect.element_to_be_clickable(
                        (By.XPATH, '//button[contains(@class,"async-button") and contains(@class,"continue")]')
                    )
                ).click()

                self.student.wait.until(
                    expect.visibility_of_element_located(
                        (By.CLASS_NAME, 'exercise-multiple-choice')
                    )
                )

                self.student.sleep(2)
                

        self.ps.test_updates['passed'] = True

    # Case C8192 - 009 - Student | Submit a multiple choice answer
    @pytest.mark.skipif(str(8192) not in TESTS, reason='Excluded')  # NOQA
    def test_student_submit_a_multiple_choice_answer(self):
        """Submit a multiple choice answer

        Steps:
        Click on a reading assignment under the tab "This Week" on the dashboard
        Click the "Continue" button 
        On a card with a free response assessment, enter a free response into the free response assessment text box
        Click the "Continue" button
        Select a multiple choice answer
        Click the "Continue" button in the left corner of the footer

        Expected Result:
        A multiple choice answer is submitted
        """
        self.ps.test_updates['name'] = 't1.28.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.28',
            't1.28.009',
            '8192'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.select_course(appearance='physics')
        assert('list' in self.student.current_url()), \
            'Not viewing the calendar dashboard'

        assignments = self.student.driver.find_elements_by_tag_name("time")
        for assignment in assignments:
            if (assignment.text == 'Dec 31, 8:54am'):
                assignment.click()
                break

        name = self.student.find(By.CLASS_NAME, 'center-control-assignment')

        assert('December Reading' in name.text), \
            'Not viewing the reading'

        while(1):
            while ('arrow right' in self.student.driver.page_source):
                self.student.find(By.XPATH, "//a[contains(@class,'arrow') and contains(@class,'right')]").click()

            # multiple choice case
            if('exercise-multiple-choice' in self.student.driver.page_source):
                

                answers = self.student.driver.find_elements(By.CLASS_NAME, 'answer-letter')
                self.student.sleep(0.8)
                rand = randint(0, len(answers) - 1)
                answer = chr(ord('a') + rand)
                #print('Selecting %s' % answer)
                Assignment.scroll_to(self.student.driver, answers[0])
                if answer == 'a':
                    self.student.driver.execute_script('window.scrollBy(0, -160);')
                elif answer == 'd':
                    self.student.driver.execute_script('window.scrollBy(0, 160);')
                answers[rand].click()


                self.student.wait.until(
                    expect.element_to_be_clickable(
                        (By.XPATH, '//button[contains(@class,"async-button") and contains(@class,"continue")]')
                    )
                ).click()
                self.student.sleep(5)

                assert('question-feedback bottom' in self.student.driver.page_source), \
                    'Did not submit MC'

                break

            # free response case
            elif('textarea' in self.student.driver.page_source):
                self.student.find(By.TAG_NAME, 'textarea').send_keys('An answer for this textarea')
                self.student.sleep(2)
                self.student.wait.until(
                    expect.element_to_be_clickable(
                        (By.XPATH, '//button[contains(@class,"async-button") and contains(@class,"continue")]')
                    )
                ).click()

                self.student.wait.until(
                    expect.visibility_of_element_located(
                        (By.CLASS_NAME, 'exercise-multiple-choice')
                    )
                )

                self.student.sleep(2)

        self.ps.test_updates['passed'] = True

    # Case C8193 - 010 - Student | Answer feedback is presented
    @pytest.mark.skipif(str(8193) not in TESTS, reason='Excluded')  # NOQA
    def test_student_answer_feedback_is_presented(self):
        """Answer feedback is presented

        Steps:
        Click on a reading assignment under the tab "This Week" on the dashboard
        Click the "Continue" button 
        On a card with a free response assessment, enter a free response into the free response assessment text box
        Click the "Answer" button
        Select a multiple choice answer
        Click the "Submit" button in the left corner of the footer

        Expected Result:
        Answer feedback is presented to the user
        """
        self.ps.test_updates['name'] = 't1.28.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.28',
            't1.28.010',
            '8193'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.select_course(appearance='physics')
        assert('list' in self.student.current_url()), \
            'Not viewing the calendar dashboard'

        assignments = self.student.driver.find_elements_by_tag_name("time")
        for assignment in assignments:
            if (assignment.text == 'Dec 31, 8:54am'):
                assignment.click()
                break

        name = self.student.find(By.CLASS_NAME, 'center-control-assignment')

        assert('December Reading' in name.text), \
            'Not viewing the reading'

        while(1):
            while ('arrow right' in self.student.driver.page_source):
                self.student.find(By.XPATH, "//a[contains(@class,'arrow') and contains(@class,'right')]").click()

            # multiple choice case
            if('exercise-multiple-choice' in self.student.driver.page_source):
                

                answers = self.student.driver.find_elements(By.CLASS_NAME, 'answer-letter')
                self.student.sleep(0.8)
                rand = randint(0, len(answers) - 1)
                answer = chr(ord('a') + rand)
                #print('Selecting %s' % answer)
                Assignment.scroll_to(self.student.driver, answers[0])
                if answer == 'a':
                    self.student.driver.execute_script('window.scrollBy(0, -160);')
                elif answer == 'd':
                    self.student.driver.execute_script('window.scrollBy(0, 160);')
                answers[rand].click()


                self.student.wait.until(
                    expect.element_to_be_clickable(
                        (By.XPATH, '//button[contains(@class,"async-button") and contains(@class,"continue")]')
                    )
                ).click()
                self.student.sleep(5)

                assert('question-feedback bottom' in self.student.driver.page_source), \
                    'Did not submit MC'
                    
                break

            # free response case
            elif('textarea' in self.student.driver.page_source):
                self.student.find(By.TAG_NAME, 'textarea').send_keys('An answer for this textarea')
                self.student.sleep(2)
                self.student.wait.until(
                    expect.element_to_be_clickable(
                        (By.XPATH, '//button[contains(@class,"async-button") and contains(@class,"continue")]')
                    )
                ).click()

                self.student.wait.until(
                    expect.visibility_of_element_located(
                        (By.CLASS_NAME, 'exercise-multiple-choice')
                    )
                )

                self.student.sleep(2)

        self.ps.test_updates['passed'] = True

    # Case C8194 - 011 - Student | Correctness for a completed assessment is displayed in the breadcrumbs
    @pytest.mark.skipif(str(8194) not in TESTS, reason='Excluded')  # NOQA
    def test_student_correctness_displayed_in_breadcrumb(self):
        """Correctness for a completed assessment is displayed in the breadcrumbs

        Steps:
        Click on a reading assignment under the tab "This Week" on the dashboard
        Click the "Continue" button 
        On a card with a free response assessment, enter a free response into the free response assessment text box
        Click the "Answer" button
        Select a multiple choice answer
        Click the "Submit" button

        Expected Result:

        
        self.ps.test_updates['name'] = 't1.28.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.28',
            't1.28.011',
            '8194'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True
        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # Case C8195 - 012 - Student | If an assessment follows a Grasp Check, answering correctly activates the Continue button
    @pytest.mark.skipif(str(8195) not in TESTS, reason='Excluded')  # NOQA
    def test_student_correct_grasp_check_activates_continue_button(self):
        """If an assessment follows a Grasp Check, answering correctly activates the Continue button

        Steps:
        Click on a reading assignment under the tab "This Week" on the dashboard
        Click the "Continue" button 
        On a card with a free response assessment that follows a Grasp Check, enter a free response into the free response assessment text box
        Click the "Answer" button
        Select a multiple choice answer
        Click the "Submit" button

        Expected Result:
        Correct answer activates the "Continue" button
        
        self.ps.test_updates['name'] = 't1.28.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.28',
            't1.28.012',
            '8195'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True
        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # Case C8196 - 013 - Student | If an assessment follows a Grasp Check, answering incorrectly activates the Try Another and Move On buttons
    @pytest.mark.skipif(str(8196) not in TESTS, reason='Excluded')  # NOQA
    def test_student_incorrect_grasp_check_activates_try_another_move_on(self):
        """If an assessment follows a Grasp Check, answering incorrectly activates the Try Another and Move On buttons

        Steps:
        Click on a reading assignment under the tab "This Week" on the dashboard
        Click the "Continue" button 
        On a card with a free response assessment that follows a Grasp Check, enter a free response into the free response assessment text box
        Click the "Answer" button
        Select a multiple choice answer
        Click the "Submit" button

        Expected Result:
        Incorrect answer activates the Try Another and Move On buttons
        
        self.ps.test_updates['name'] = 't1.28.013' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.28',
            't1.28.013',
            '8196'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True
        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # Case C8197 - 014 - Student | Select Try Another to receive a new assessment
    @pytest.mark.skipif(str(8197) not in TESTS, reason='Excluded')  # NOQA
    def test_student_select_try_another_to_receive_new_assessment(self):
        """Select Try Another to receive a new assessment

        Steps:
        Click on a reading assignment under the tab "This Week" on the dashboard
        Click the "Continue" button 
        On a card with a free response assessment that follows a Grasp Check, enter a free response into the free response assessment text box
        Click the "Answer" button
        Select a multiple choice answer
        Click the "Submit" button
        After selecting an incorrect answer, click the "Try Another" button

        Expected Result:
        The user receives a new assessment
        
        self.ps.test_updates['name'] = 't1.28.014' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.28',
            't1.28.014',
            '8197'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True
        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # Case C8198 - 015 - Student | Select Move On
    @pytest.mark.skipif(str(8198) not in TESTS, reason='Excluded')  # NOQA
    def test_student_select_move_on(self):
        """Select Move On

        Steps:
        Click on a reading assignment under the tab "This Week" on the dashboard
        Click the "Continue" button 
        On a card with a free response assessment that follows a Grasp Check, enter a free response into the free response assessment text box
        Click the "Answer" button
        Select a multiple choice answer
        Click the "Submit" button
        After selecting an incorrect answer, click the "Move On" button

        Expected Result:
        The user is presented with the next part in the reading section
        
        self.ps.test_updates['name'] = 't1.28.015' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.28',
            't1.28.015',
            '8198'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True
        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # Case C8199 - 016 - Student | If a card has a video, play the video
    @pytest.mark.skipif(str(8199) not in TESTS, reason='Excluded')  # NOQA
    def test_student_if_a_card_has_a_video_play_the_videio(self):
        """If a card has a video, play the video

        Steps:
        Click on a reading assignment under the tab "This Week" on the dashboard
        Click the "Continue" button 
        On a card with a video, click the play button

        Expected Result:
        The video plays
        """
        self.ps.test_updates['name'] = 't1.28.016' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.28',
            't1.28.016',
            '8199'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.select_course(appearance='physics')
        assert('list' in self.student.current_url()), \
            'Not viewing the calendar dashboard'

        assignments = self.student.driver.find_elements_by_tag_name("time")
        for assignment in assignments:
            if (assignment.text == 'Dec 31, 8:54am'):
                assignment.click()
                break

        name = self.student.find(By.CLASS_NAME, 'center-control-assignment')

        assert('December Reading' in name.text), \
            'Not viewing the reading'

        while(1):
            while ('arrow right' in self.student.driver.page_source and 'video-step' not in self.student.driver.page_source):
                self.student.find(By.XPATH, "//a[contains(@class,'arrow') and contains(@class,'right')]").click()

            # multiple choice case
            if('exercise-multiple-choice' in self.student.driver.page_source):
                

                answers = self.student.driver.find_elements(By.CLASS_NAME, 'answer-letter')
                self.student.sleep(0.8)
                rand = randint(0, len(answers) - 1)
                answer = chr(ord('a') + rand)
                #print('Selecting %s' % answer)
                Assignment.scroll_to(self.student.driver, answers[0])
                if answer == 'a':
                    self.student.driver.execute_script('window.scrollBy(0, -160);')
                elif answer == 'd':
                    self.student.driver.execute_script('window.scrollBy(0, 160);')
                answers[rand].click()


                self.student.wait.until(
                    expect.element_to_be_clickable(
                        (By.XPATH, '//button[contains(@class,"async-button") and contains(@class,"continue")]')
                    )
                ).click()
                self.student.sleep(5)

                assert('question-feedback bottom' in self.student.driver.page_source), \
                    'Did not submit MC'

            # free response case
            elif('textarea' in self.student.driver.page_source):
                self.student.find(By.TAG_NAME, 'textarea').send_keys('An answer for this textarea')
                self.student.sleep(2)
                self.student.wait.until(
                    expect.element_to_be_clickable(
                        (By.XPATH, '//button[contains(@class,"async-button") and contains(@class,"continue")]')
                    )
                ).click()

                self.student.wait.until(
                    expect.visibility_of_element_located(
                        (By.CLASS_NAME, 'exercise-multiple-choice')
                    )
                )

                self.student.sleep(2)

            elif('video-step' in self.student.driver.page_source):
                self.student.find(By.TAG_NAME, "iframe").click()
                self.student.sleep(5)
                break

        self.ps.test_updates['passed'] = True

    # Case C8200 - 017 - Student | A Concept Coach card preceeds the question review
    @pytest.mark.skipif(str(8200) not in TESTS, reason='Excluded')  # NOQA
    def test_student_concept_coach_precedes_question_review(self):
        """A Concept Coach card preceeds the question review

        Steps:
        Click on a reading assignment under the tab "This Week" on the dashboard
        Click the "Continue" button

        Expected Result:
        At the end of the reading, the user is presented with a Concept Coach card that precedes the question review.
        """
        self.ps.test_updates['name'] = 't1.28.017' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.28',
            't1.28.017',
            '8200'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.select_course(appearance='physics')
        assert('list' in self.student.current_url()), \
            'Not viewing the calendar dashboard'

        assignments = self.student.driver.find_elements_by_tag_name("time")
        for assignment in assignments:
            if (assignment.text == 'Dec 31, 8:54am'):
                assignment.click()
                break

        name = self.student.find(By.CLASS_NAME, 'center-control-assignment')

        assert('December Reading' in name.text), \
            'Not viewing the reading'

        while(1):
            while ('arrow right' in self.student.driver.page_source and 'Concept Coach' not in self.student.driver.page_source):
                self.student.find(By.XPATH, "//a[contains(@class,'arrow') and contains(@class,'right')]").click()

            # multiple choice case
            if('exercise-multiple-choice' in self.student.driver.page_source):
                

                answers = self.student.driver.find_elements(By.CLASS_NAME, 'answer-letter')
                self.student.sleep(0.8)
                rand = randint(0, len(answers) - 1)
                answer = chr(ord('a') + rand)
                #print('Selecting %s' % answer)
                Assignment.scroll_to(self.student.driver, answers[0])
                if answer == 'a':
                    self.student.driver.execute_script('window.scrollBy(0, -160);')
                elif answer == 'd':
                    self.student.driver.execute_script('window.scrollBy(0, 160);')
                answers[rand].click()


                self.student.wait.until(
                    expect.element_to_be_clickable(
                        (By.XPATH, '//button[contains(@class,"async-button") and contains(@class,"continue")]')
                    )
                ).click()
                self.student.sleep(5)

                assert('question-feedback bottom' in self.student.driver.page_source), \
                    'Did not submit MC'

            # free response case
            elif('textarea' in self.student.driver.page_source):
                self.student.find(By.TAG_NAME, 'textarea').send_keys('An answer for this textarea')
                self.student.sleep(2)
                self.student.wait.until(
                    expect.element_to_be_clickable(
                        (By.XPATH, '//button[contains(@class,"async-button") and contains(@class,"continue")]')
                    )
                ).click()

                self.student.wait.until(
                    expect.visibility_of_element_located(
                        (By.CLASS_NAME, 'exercise-multiple-choice')
                    )
                )

                self.student.sleep(2)

            # Reached Concept Coach card
            elif('Concept Coach' in self.student.driver.page_source and 'spacer-step' in self.student.driver.page_source):
                self.student.sleep(5)
                break

        self.ps.test_updates['passed'] = True

    # Case C8201 - 018 - Student | A reading may have a Review assessment
    @pytest.mark.skipif(str(8201) not in TESTS, reason='Excluded')  # NOQA
    def test_student_reading_may_have_review_assessment(self):
        """A reading may have a Review assessment

        Steps:
        Click on a reading assignment under the tab "This Week" on the dashboard
        Click the "Continue" button

        Expected Result:
        The user may be presented with a Review assessment at the end of the reading assignment
        """
        self.ps.test_updates['name'] = 't1.28.018' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.28',
            't1.28.018',
            '8201'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.select_course(appearance='physics')
        assert('list' in self.student.current_url()), \
            'Not viewing the calendar dashboard'

        assignments = self.student.driver.find_elements_by_tag_name("time")
        for assignment in assignments:
            if (assignment.text == 'Dec 31, 8:54am'):
                assignment.click()
                break

        name = self.student.find(By.CLASS_NAME, 'center-control-assignment')

        assert('December Reading' in name.text), \
            'Not viewing the reading'

        flag = False

        while(1):
            while ('arrow right' in self.student.driver.page_source):
                if 'openstax-step-group-label' in self.student.driver.page_source:
                    if self.student.find(By.CLASS_NAME, 'openstax-step-group-label').text == 'Review':
                        flag = True
                        break
                self.student.find(By.XPATH, "//a[contains(@class,'arrow') and contains(@class,'right')]").click()

            if flag:
                break

            # multiple choice case
            if('exercise-multiple-choice' in self.student.driver.page_source):

                if 'openstax-step-group-label' in self.student.driver.page_source:
                    if self.student.find(By.CLASS_NAME, 'openstax-step-group-label').text == 'Review':
                        break

                answers = self.student.driver.find_elements(By.CLASS_NAME, 'answer-letter')
                self.student.sleep(0.8)
                rand = randint(0, len(answers) - 1)
                answer = chr(ord('a') + rand)
                #print('Selecting %s' % answer)
                Assignment.scroll_to(self.student.driver, answers[0])
                if answer == 'a':
                    self.student.driver.execute_script('window.scrollBy(0, -160);')
                elif answer == 'd':
                    self.student.driver.execute_script('window.scrollBy(0, 160);')
                answers[rand].click()


                self.student.wait.until(
                    expect.element_to_be_clickable(
                        (By.XPATH, '//button[contains(@class,"async-button") and contains(@class,"continue")]')
                    )
                ).click()
                self.student.sleep(5)

                assert('question-feedback bottom' in self.student.driver.page_source), \
                    'Did not submit MC'

            # free response case
            elif('textarea' in self.student.driver.page_source):

                if 'openstax-step-group-label' in self.student.driver.page_source:
                    if self.student.find(By.CLASS_NAME, 'openstax-step-group-label').text == 'Review':
                        break

                self.student.find(By.TAG_NAME, 'textarea').send_keys('An answer for this textarea')
                self.student.sleep(2)
                self.student.wait.until(
                    expect.element_to_be_clickable(
                        (By.XPATH, '//button[contains(@class,"async-button") and contains(@class,"continue")]')
                    )
                ).click()

                self.student.wait.until(
                    expect.visibility_of_element_located(
                        (By.CLASS_NAME, 'exercise-multiple-choice')
                    )
                )

                self.student.sleep(2)


        self.student.sleep(5)
        self.ps.test_updates['passed'] = True

    # Case C8202 - 019 - Student | A reading may have a Personalized assessment
    @pytest.mark.skipif(str(8202) not in TESTS, reason='Excluded')  # NOQA
    def test_student_reading_may_have_personalized_assessment(self):
        """A reading may have a Personalized assessment

        Steps:
        Click on a homework assignment under the tab "This Week" on the dashboard
        Click the "Continue" button

        Expected Result:
        A user may be presented with a personalized assessment at the end of the reading assignment
        """
        self.ps.test_updates['name'] = 't1.28.019' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.28',
            't1.28.019',
            '8202'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertionsself.student.select_course(appearance='physics')
        self.student.select_course(appearance='physics')
        assert('list' in self.student.current_url()), \
            'Not viewing the calendar dashboard'

        assignments = self.student.driver.find_elements_by_tag_name("time")
        for assignment in assignments:
            if (assignment.text == 'Dec 31, 8:54am'):
                assignment.click()
                break

        name = self.student.find(By.CLASS_NAME, 'center-control-assignment')

        assert('December Reading' in name.text), \
            'Not viewing the reading'

        flag = False

        while(1):
            while ('arrow right' in self.student.driver.page_source):
                if 'openstax-step-group-label' in self.student.driver.page_source:
                    if self.student.find(By.CLASS_NAME, 'openstax-step-group-label').text == 'Personalized':
                        flag = True
                        break
                self.student.find(By.XPATH, "//a[contains(@class,'arrow') and contains(@class,'right')]").click()

            if flag:
                break

            # multiple choice case
            if('exercise-multiple-choice' in self.student.driver.page_source):

                if 'openstax-step-group-label' in self.student.driver.page_source:
                    if self.student.find(By.CLASS_NAME, 'openstax-step-group-label').text == 'Personalized':
                        break

                answers = self.student.driver.find_elements(By.CLASS_NAME, 'answer-letter')
                self.student.sleep(0.8)
                rand = randint(0, len(answers) - 1)
                answer = chr(ord('a') + rand)
                #print('Selecting %s' % answer)
                Assignment.scroll_to(self.student.driver, answers[0])
                if answer == 'a':
                    self.student.driver.execute_script('window.scrollBy(0, -160);')
                elif answer == 'd':
                    self.student.driver.execute_script('window.scrollBy(0, 160);')
                answers[rand].click()


                self.student.wait.until(
                    expect.element_to_be_clickable(
                        (By.XPATH, '//button[contains(@class,"async-button") and contains(@class,"continue")]')
                    )
                ).click()
                self.student.sleep(5)

                assert('question-feedback bottom' in self.student.driver.page_source), \
                    'Did not submit MC'

            # free response case
            elif('textarea' in self.student.driver.page_source):

                if 'openstax-step-group-label' in self.student.driver.page_source:
                    if self.student.find(By.CLASS_NAME, 'openstax-step-group-label').text == 'Personalized':
                        break

                self.student.find(By.TAG_NAME, 'textarea').send_keys('An answer for this textarea')
                self.student.sleep(2)
                self.student.wait.until(
                    expect.element_to_be_clickable(
                        (By.XPATH, '//button[contains(@class,"async-button") and contains(@class,"continue")]')
                    )
                ).click()

                self.student.wait.until(
                    expect.visibility_of_element_located(
                        (By.CLASS_NAME, 'exercise-multiple-choice')
                    )
                )

                self.student.sleep(2)

        self.student.sleep(2)
        self.ps.test_updates['passed'] = True

    # Case C8203 - 020 - Student | View the completion report and click the Back To Dashboard button to return to the dashboard
    @pytest.mark.skipif(str(8203) not in TESTS, reason='Excluded')  # NOQA
    def test_student_view_completion_report(self):
        """View the completion report and click the Back To Dashboard button to return to the dashboard

        Steps:
        Click on a reading assignment under the tab "This Week" on the dashboard
        Click the "Continue" button 
        At the end of the reading, click the "Back to Dashboard" button

        Expected Result:
        The user views the completion report and return to the dashboard
        """
        self.ps.test_updates['name'] = 't1.28.020' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.28',
            't1.28.020',
            '8203'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.select_course(appearance='physics')
        assert('list' in self.student.current_url()), \
            'Not viewing the calendar dashboard'

        assignments = self.student.driver.find_elements_by_tag_name("time")
        for assignment in assignments:
            if (assignment.text == 'Dec 31, 8:54am'):
                assignment.click()
                break

        name = self.student.find(By.CLASS_NAME, 'center-control-assignment')

        assert('December Reading' in name.text), \
            'Not viewing the reading'

        while(1):
            while ('arrow right' in self.student.driver.page_source):
                self.student.find(By.XPATH, "//a[contains(@class,'arrow') and contains(@class,'right')]").click()

            # multiple choice case
            if('exercise-multiple-choice' in self.student.driver.page_source):

                answers = self.student.driver.find_elements(By.CLASS_NAME, 'answer-letter')
                self.student.sleep(0.8)
                rand = randint(0, len(answers) - 1)
                answer = chr(ord('a') + rand)
                #print('Selecting %s' % answer)
                Assignment.scroll_to(self.student.driver, answers[0])
                if answer == 'a':
                    self.student.driver.execute_script('window.scrollBy(0, -160);')
                elif answer == 'd':
                    self.student.driver.execute_script('window.scrollBy(0, 160);')
                answers[rand].click()


                self.student.wait.until(
                    expect.element_to_be_clickable(
                        (By.XPATH, '//button[contains(@class,"async-button") and contains(@class,"continue")]')
                    )
                ).click()
                self.student.sleep(5)

                assert('question-feedback bottom' in self.student.driver.page_source), \
                    'Did not submit MC'

            # free response case
            elif('textarea' in self.student.driver.page_source):

                self.student.find(By.TAG_NAME, 'textarea').send_keys('An answer for this textarea')
                self.student.sleep(2)
                self.student.wait.until(
                    expect.element_to_be_clickable(
                        (By.XPATH, '//button[contains(@class,"async-button") and contains(@class,"continue")]')
                    )
                ).click()

                self.student.wait.until(
                    expect.visibility_of_element_located(
                        (By.CLASS_NAME, 'exercise-multiple-choice')
                    )
                )

                self.student.sleep(2)

            # Reached the end of the reading assignment
            elif('task task-completed' in self.student.driver.page_source):
                self.student.sleep(2)

                # May need to change 'to' to 'To'
                self.student.find(By.LINK_TEXT, 'Back To Dashboard').click()
                assert('list' in self.student.current_url()), \
                        'Not at the dashboard'

                self.student.sleep(2)
                break

        self.ps.test_updates['passed'] = True
        
        # raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # Case C8204 - 021 - Student | A completed reading should show You are done. in the completion report
    @pytest.mark.skipif(str(8204) not in TESTS, reason='Excluded')  # NOQA
    def test_student_completed_reading_shows_you_are_done(self):
        """A completed reading should show You are done. in the completion report

        Steps:
        Click on a reading assignment under the tab "This Week" on the dashboard
        Click the "Continue" button 
        Keep clicking the "Continue" button until the reading is over

        Expected Result:
        Once finished with the reading, the user is presented with the completion report that shows "You are done"
        """
        self.ps.test_updates['name'] = 't1.28.021' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.28',
            't1.28.021',
            '8204'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.select_course(appearance='physics')
        assert('list' in self.student.current_url()), \
            'Not viewing the calendar dashboard'

        assignments = self.student.driver.find_elements_by_tag_name("time")
        for assignment in assignments:
            if (assignment.text == 'Dec 31, 8:54am'):
                assignment.click()
                break

        name = self.student.find(By.CLASS_NAME, 'center-control-assignment')

        assert('December Reading' in name.text), \
            'Not viewing the reading'

        while(1):
            while ('arrow right' in self.student.driver.page_source):
                self.student.find(By.XPATH, "//a[contains(@class,'arrow') and contains(@class,'right')]").click()

            # multiple choice case
            if('exercise-multiple-choice' in self.student.driver.page_source):

                answers = self.student.driver.find_elements(By.CLASS_NAME, 'answer-letter')
                self.student.sleep(0.8)
                rand = randint(0, len(answers) - 1)
                answer = chr(ord('a') + rand)
                #print('Selecting %s' % answer)
                Assignment.scroll_to(self.student.driver, answers[0])
                if answer == 'a':
                    self.student.driver.execute_script('window.scrollBy(0, -160);')
                elif answer == 'd':
                    self.student.driver.execute_script('window.scrollBy(0, 160);')
                answers[rand].click()


                self.student.wait.until(
                    expect.element_to_be_clickable(
                        (By.XPATH, '//button[contains(@class,"async-button") and contains(@class,"continue")]')
                    )
                ).click()
                self.student.sleep(5)

                assert('question-feedback bottom' in self.student.driver.page_source), \
                    'Did not submit MC'

            # free response case
            elif('textarea' in self.student.driver.page_source):

                self.student.find(By.TAG_NAME, 'textarea').send_keys('An answer for this textarea')
                self.student.sleep(2)
                self.student.wait.until(
                    expect.element_to_be_clickable(
                        (By.XPATH, '//button[contains(@class,"async-button") and contains(@class,"continue")]')
                    )
                ).click()

                self.student.wait.until(
                    expect.visibility_of_element_located(
                        (By.CLASS_NAME, 'exercise-multiple-choice')
                    )
                )

                self.student.sleep(2)

            # Reached the end of the reading assignment
            elif('task task-completed' in self.student.driver.page_source):
                self.student.sleep(2)

                done = self.student.find(By.TAG_NAME, 'h1')
                steps = self.student.find(By.TAG_NAME, 'h3')

                assert(done.text == 'You are done.' and steps.text == 'Great job completing all the steps.'), \
                        'Not viewing the completion page'

                self.student.sleep(2)
                break

        self.ps.test_updates['passed'] = True

    # Case C8205 - 022 - Student | A completed reading should show Complete in the dashboard progress column
    @pytest.mark.skipif(str(8205) not in TESTS, reason='Excluded')  # NOQA
    def test_student_completed_reading_shows_complete_in_dashboard(self):
        """A completed reading should show Complete in the dashboard progress column

        Steps:
        Click on a reading assignment under the tab "This Week" on the dashboard
        Click the "Continue" button 
        At the end of the reading, click the "Back to Dashboard" button

        Expected Result:
        The reading is marked "Complete" in the dashboard progress column
        """
        self.ps.test_updates['name'] = 't1.28.022' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.28',
            't1.28.022',
            '8205'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.select_course(appearance='physics')
        assert('list' in self.student.current_url()), \
            'Not viewing the calendar dashboard'

        assignments = self.student.driver.find_elements_by_xpath("//div[@class='-upcoming panel panel-default']/div[@class='panel-body']/div[@class='task row reading workable']")
        for assignment in assignments:
            if (assignment.text.find('Dec 31, 8:54am') >= 0 and assignment.text.find('December Reading') >= 0 and assignment.text.find("Complete") >= 0):
                self.ps.test_updates['passed'] = True
                break

    # Case C8206 - 023 - Student | Answer an assessment, return to the dashboard and verify the assignment progress is In progress
    @pytest.mark.skipif(str(8206) not in TESTS, reason='Excluded')  # NOQA
    def test_student_verify_started_assignment_shows_in_progress_on_dashboard(self):
        """Answer an assessment, return to the dashboard and verify the assignment progress is In progress

        Steps:
        Click on a reading assignment under the tab "This Week" on the dashboard
        Click the "Continue" button 
        On a card with a free response assessment, enter a free response into the free response assessment text box
        Click the "Answer" button
        Select a multiple choice answer
        Click the "Submit" button in the left corner of the footer
        Click on the course name in the upper left corner of the page OR Click the user menu
        Click the "Dashboard" button

        Expected Result:
        The user returns to dashboard and the reading is marked "In Progress" in the dashboard progress column
        """
        self.ps.test_updates['name'] = 't1.28.023' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.28',
            't1.28.023',
            '8206'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.select_course(appearance='physics')
        assert('list' in self.student.current_url()), \
            'Not viewing the calendar dashboard'

        home = self.student.current_url()

        assignments = self.student.driver.find_elements_by_xpath("//div[@class='-upcoming panel panel-default']/div[@class='panel-body']/div[@class='task row reading workable']")
        for assignment in assignments:
            if (assignment.text.find('Dec 29, 8:42am') >= 0 and assignment.text.find('Long Automation Reading') >= 0 and assignment.text.find("In progress") >= 0):
                self.ps.test_updates['passed'] = True
                break

            elif (assignment.text.find('Dec 29, 8:42am') >= 0 and assignment.text.find('Long Automation Reading') >= 0 and assignment.text.find("Not started") >= 0):
                assignment.click()
                name = self.student.find(By.CLASS_NAME, 'center-control-assignment')

                assert('Long Automation Reading' in name.text), \
                    'Not viewing the reading'

                while(1):
                    while ('arrow right' in self.student.driver.page_source):
                        self.student.find(By.XPATH, "//a[contains(@class,'arrow') and contains(@class,'right')]").click()

                    # multiple choice case
                    if('exercise-multiple-choice' in self.student.driver.page_source):
                        

                        answers = self.student.driver.find_elements(By.CLASS_NAME, 'answer-letter')
                        self.student.sleep(0.8)
                        rand = randint(0, len(answers) - 1)
                        answer = chr(ord('a') + rand)
                        #print('Selecting %s' % answer)
                        Assignment.scroll_to(self.student.driver, answers[0])
                        if answer == 'a':
                            self.student.driver.execute_script('window.scrollBy(0, -160);')
                        elif answer == 'd':
                            self.student.driver.execute_script('window.scrollBy(0, 160);')
                        answers[rand].click()


                        self.student.wait.until(
                            expect.element_to_be_clickable(
                                (By.XPATH, '//button[contains(@class,"async-button") and contains(@class,"continue")]')
                            )
                        ).click()
                        self.student.sleep(5)

                        assert('question-feedback bottom' in self.student.driver.page_source), \
                            'Did not submit MC'

                        break

                    # free response case
                    elif('textarea' in self.student.driver.page_source):
                        self.student.find(By.TAG_NAME, 'textarea').send_keys('An answer for this textarea')
                        self.student.sleep(2)
                        self.student.wait.until(
                            expect.element_to_be_clickable(
                                (By.XPATH, '//button[contains(@class,"async-button") and contains(@class,"continue")]')
                            )
                        ).click()

                        self.student.wait.until(
                            expect.visibility_of_element_located(
                                (By.CLASS_NAME, 'exercise-multiple-choice')
                            )
                        )

                        self.student.sleep(2)

                self.student.sleep(20)
                self.student.driver.get(home)

                assignments = self.student.driver.find_elements_by_xpath("//div[@class='-upcoming panel panel-default']/div[@class='panel-body']/div[@class='task row reading workable']")
                for assignment in assignments:
                    if (assignment.text.find('Dec 29, 8:42am') >= 0 and assignment.text.find('Long Automation Reading') >= 0 and assignment.text.find("In progress") >= 0):
                        self.ps.test_updates['passed'] = True
                        break