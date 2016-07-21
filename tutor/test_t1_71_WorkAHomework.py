"""Tutor v1, Epic 71 - Work a Homework."""

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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Student, Teacher  # NOQA

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': '50.0',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([8362, 8363, 8364, 8365, 8366,
         8367, 8368, 8369, 8370, 8371,
         8372, 8373, 8374, 8375, 8376,
         8377, 8378, 8379, 8380, 8381,
         8382, 8383, 8384, 8385, 8386])  # NOQA
)


@PastaDecorator.on_platforms(BROWSERS)
class TestWorkAHomework(unittest.TestCase):
    """T1.71 - Work a Homework."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.student = Student(
            use_env_vars=True#,
            #pasta_user=self.ps,
            #capabilities=self.desired_capabilities
        )
        self.student = Student(
            use_env_vars=True#,
            #pasta_user=self.ps,
            #capabilities=self.desired_capabilities
        )
        self.teacher = Teacher(
            existing_driver = self.student.driver,
            username = 'teacher01',
            password = 'password'
            #use_env_vars=True#,
            #pasta_user=self.ps,
            #capabilities=self.desired_capabilities
        )
        self.teacher.driver = self.student.driver
        self.wait = WebDriverWait(self.student.driver, Assignment.WAIT_TIME)
        self.teacher.login()

    def tearDown(self):
        """Test destructor."""
        self.ps.update_job(job_id=str(self.student.driver.session_id),
                           **self.ps.test_updates)
        try:
            self.student.delete()
        except:
            pass

    # Case C8362 - 001 - Student | Start an open homework assignment
    @pytest.mark.skipif(str(8362) not in TESTS, reason='Excluded')  # NOQA
    def test_student_start_an_open_homework_assignemnt_8362(self):
        """Start an open homework assignment.

        Steps:
        Click on a homework assignment on the list dashboard

        Expected Result:
        The user is presented with the first question of the homework
        assignment

        """
        self.ps.test_updates['name'] = 't1.71.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.71','t1.71.001','8362']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'hw001'
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
        #non-immediate feedback
        self.teacher.add_assignment(assignemnt = 'homework',
                                    args = {
                                        'title' : assignment_name,
                                        'description' : 'description',
                                        'periods' : {'all':(begin,end)},
                                        'status' : 'publish'
                                    })
        self.teacher.logout()
        self.student.login()
        self.student.select_course(appearance='physics')
        homework = self.student.driver.find_element(
            By.XPATH,'//div[contains(@class,"homework") and not(contains(@class,"deleted"))]'\
            '//span[contains(text,"'+assignment_name+'")]')
        self.student.driver.execute_script('return arguments[0].scrollIntoView();', homework)
        self.student.driver.execute_script('window.scrollBy(0, -80);')
        homework.click()
        wait = WebDriverWait(self.student.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"question-stem")]')
            )
        )
        self.ps.test_updates['passed'] = True


    # Case C8363 - 002 - Student | Hover over the information icon to view the description
    @pytest.mark.skipif(str(8363) not in TESTS, reason='Excluded')  # NOQA
    def test_student_hover_over_the_information_icon_to_view_the_description(self):
        """Hover over the information icon in the footer to view the assignment description.

        Steps:
        Hover the cursor over the information icon in right corner of the footer

        Expected Result:
        The user is presented with the assignment description/instructions
        """
        self.ps.test_updates['name'] = 't1.71.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.71','t1.71.002','8363']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'hw002'
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
        # non-immediate feedback
        self.teacher.add_assignment(assignemnt = 'homework',
                                    args = {
                                        'title' : assignment_name,
                                        'description' : 'description',
                                        'periods' : {'all':(begin,end)},
                                        'status' : 'publish'
                                        'problems' : {'ch1':5}
                                        'feedback' : 'non-immediate'
                                    })
        self.teacher.logout()
        self.student.login()
        self.student.select_course(appearance='physics')
        homework = self.student.driver.find_element(
            By.XPATH,'//div[contains(@class,"homework") and not(contains(@class,"deleted"))]'\
            '//span[contains(text,"'+assignment_name+'")]')
        self.student.driver.execute_script('return arguments[0].scrollIntoView();', homework)
        self.student.driver.execute_script('window.scrollBy(0, -80);')
        icon = self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"homeowrk")]//button[contains(@class,"task-details")]')
            )
        )
        ActionChains(self.student.driver).move_to_element(icon).perform()
        self.student.driver.find_element(
            By.XPATH, '//div[contains(@id,"task-details-popover")]')
        self.ps.test_updates['passed'] = True

    # Case C8364 - 003 - Student | Navigate between questions using the
    # breadcrumbs
    @pytest.mark.skipif(str(8364) not in TESTS, reason='Excluded')  # NOQA
    def test_student_navigate_between_questions_using_breadcrumbs_8364(self):
        """Navigate between questions using the breadcrumbs.

        Steps:
        Click on the next breadcrumb

        Expected Result:
        The user is presented with the next question
        """
        self.ps.test_updates['name'] = 't1.71.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.71','t1.71.003','8364']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'hw003'
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
        # non-immediate feedback
        self.teacher.add_assignment(assignemnt = 'homework',
                                    args = {
                                        'title' : assignment_name,
                                        'description' : 'description',
                                        'periods' : {'all':(begin,end)},
                                        'status' : 'publish'
                                        'problems' : {'ch1':5}
                                        'feedback' : 'non-immediate'
                                    })
        self.teacher.logout()
        self.student.login()
        self.student.select_course(appearance='physics')
        homework = self.student.driver.find_element(
            By.XPATH,'//div[contains(@class,"homework") and not(contains(@class,"deleted"))]'\
            '//span[contains(text,"'+assignment_name+'")]')
        self.student.driver.execute_script('return arguments[0].scrollIntoView();', homework)
        self.student.driver.execute_script('window.scrollBy(0, -80);')
        homework.click()
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[contains(@data-reactid,"breadcrumb-step-1")]')
            )
        ).click()
        self.student.driver.find_element(
            By.XPATH,'//div[@data-question-number="2"]')
        self.ps.test_updates['passed'] = True

    # Case C8365 - 004 - Student | Inputting a free response activates the Answer button
    @pytest.mark.skipif(str(8365) not in TESTS, reason='Excluded')  # NOQA
    def test_student_inputting_a_free_response_activates_the_answer_button(self):
        """Inputting a free response into a free response textblock activates the Answer button.

        Steps:
        If the assessment has a free response text box,
        enter a free response into the free response text box

        Expected Result:
        The Answer button is activated
        """
        self.ps.test_updates['name'] = 't1.71.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.71','t1.71.004','8365']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'hw004'
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
        # non-immediate feedback
        self.teacher.add_assignment(assignemnt = 'homework',
                                    args = {
                                        'title' : assignment_name,
                                        'description' : 'description',
                                        'periods' : {'all':(begin,end)},
                                        'status' : 'publish'
                                        'problems' : {'ch1':5}
                                        'feedback' : 'non-immediate'
                                    })
        self.teacher.logout()
        self.student.login()
        self.student.select_course(appearance='physics')
        homework = self.student.driver.find_element(
            By.XPATH,'//div[contains(@class,"homework") and not(contains(@class,"deleted"))]'\
            '//span[contains(text,"'+assignment_name+'")]')
        self.student.driver.execute_script('return arguments[0].scrollIntoView();', homework)
        self.student.driver.execute_script('window.scrollBy(0, -80);')
        homework.click()
        sections = self.student.driver.find_elements(
            By.XPATH,'//span[contains(@class,"breadcrumbs")]')
        count = 0
        while(True):
            try:
                element = self.student.driver.find_element(
                    By.TAG_NAME,'textarea')
                for i in 'hello':
                    element.send_keys(i)
                self.wait.until(
                    expect.element_to_be_clickable(
                        ( By.XPATH,'//button/span[contains(text(),"Answer")]')
                    )
                )
                break
            except:
                count+=1
                if count >= len(sections):
                    print('no questions in this homework with free respnse')
                    raise Exception
                sections[count].click()

        self.ps.test_updates['passed'] = True


    # Case C8366 - 005 - Student |  Submit a free response answer
    @pytest.mark.skipif(str(8366) not in TESTS, reason='Excluded')  # NOQA
    def test_student_submit_a_free_response_answer(self):
        """ Submit a free response answer.

        Steps:
        If the assessment has a free response text box,
        enter a free response into the free response text box
        Click "Answer"

        Expected Result:
        A free response answer is submitted
        """
        self.ps.test_updates['name'] = 't1.71.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.71','t1.71.005','8366']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'hw005'
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
        # non-immediate feedback
        self.teacher.add_assignment(assignemnt = 'homework',
                                    args = {
                                        'title' : assignment_name,
                                        'description' : 'description',
                                        'periods' : {'all':(begin,end)},
                                        'status' : 'publish'
                                        'problems' : {'ch1':5}
                                        'feedback' : 'non-immediate'
                                    })
        self.teacher.logout()
        self.student.login()
        self.student.select_course(appearance='physics')
        homework = self.student.driver.find_element(
            By.XPATH,'//div[contains(@class,"homework") and not(contains(@class,"deleted"))]'\
            '//span[contains(text,"'+assignment_name+'")]')
        self.student.driver.execute_script('return arguments[0].scrollIntoView();', homework)
        self.student.driver.execute_script('window.scrollBy(0, -80);')
        homework.click()
        sections = self.student.driver.find_elements(
            By.XPATH,'//span[contains(@class,"breadcrumbs")]')
        count = 0
        answer_text = "hello"
        while(True):
            try:
                element = self.student.driver.find_element(
                    By.TAG_NAME,'textarea')
                for i in answer_text:
                    element.send_keys(i)
                self.wait.until(
                    expect.element_to_be_clickable(
                        ( By.XPATH,'//button/span[contains(text(),"Answer")]')
                    )
                ).click()
                break
            except:
                count+=1
                if count >= len(sections):
                    print('no questions in this homework with free respnse')
                    raise Exception
                sections[count].click()
        self.student.driver.find_element(
            By.XPATH,'//div[@class="free-response" and contains(text(),"'+answer_text+'")]')
        self.student.driver.find_element(
            By.XPATH,'//div[@class="answer-letter"]')
        self.ps.test_updates['passed'] = True

    # Case C8367 - 006 - Student | Selecting a multiple choice answer activates the Submit button
    @pytest.mark.skipif(str(8367) not in TESTS, reason='Excluded')  # NOQA
    def test_student_seleting_a_multiple_choice_activates_the_submit_button(self):
        """Selecting a multiple choice answer activates the Submit button.

        Steps:
        Click on a homework assignment on the list dashboard
        If the assessment has a free response text box,
        enter a free response into the free response text box
        Click "Answer"
        Select a multiple choice answer

        Expected Result:
        The Submit button is activated
        """
        self.ps.test_updates['name'] = 't1.71.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.71','t1.71.006','8367']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'hw006'
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
        # non-immediate feedback
        self.teacher.add_assignment(assignemnt = 'homework',
                                    args = {
                                        'title' : assignment_name,
                                        'description' : 'description',
                                        'periods' : {'all':(begin,end)},
                                        'status' : 'publish'
                                        'problems' : {'ch1':5}
                                        'feedback' : 'non-immediate'
                                    })
        self.teacher.logout()
        self.student.login()
        self.student.select_course(appearance='physics')
        homework = self.student.driver.find_element(
            By.XPATH,'//div[contains(@class,"homework") and not(contains(@class,"deleted"))]'\
            '//span[contains(text,"'+assignment_name+'")]')
        self.student.driver.execute_script('return arguments[0].scrollIntoView();', homework)
        self.student.driver.execute_script('window.scrollBy(0, -80);')
        homework.click()
        try:
            #if the question is two part must answer free response to get to mc
            element = self.student.driver.find_element(
                By.TAG_NAME,'textarea')
            answer_text = "hello"
            for i in answer_text:
                element.send_keys(i)
            self.wait.until(
                expect.visibility_of_element_located(
                    ( By.XPATH,'//button/span[contains(text(),"Answer")]')
                )
            ).click()
        except:
            pass
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,'//div[contains(@class,"question-stem")]')
            )
        )
        element = self.student.driver.find_element(
            By.XPATH,'//div[@class="answer-letter"]')
        self.student.driver.execute_script('return arguments[0].scrollIntoView();', element)
        self.student.driver.execute_script('window.scrollBy(0, -150);')
        element.click()
        self.wait.until(
            expect.element_to_be_clickable(
                ( By.XPATH,'//button/span[contains(text(),"Submit")]')
            )
        )
        self.ps.test_updates['passed'] = True


    # Case C8368 - 007 - Student | Submit a multiple choice answer
    @pytest.mark.skipif(str(8368) not in TESTS, reason='Excluded')  # NOQA
    def test_student_submit_A_multiple_choice_answer(self):
        """Submit a multiple choice answer.

        Steps:
        Click on a homework assignment on the list dashboard
        If the assessment has a free response text box,
        enter a free response into the free response text box
        Click "Answer"
        Select a multiple choice answer
        Click "Submit"

        Expected Result:
        A multiple choice answer is submitted
        """
        self.ps.test_updates['name'] = 't1.71.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.71','t1.71.007','8368']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'hw007'
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
        # non-immediate feedback
        self.teacher.add_assignment(assignemnt = 'homework',
                                    args = {
                                        'title' : assignment_name,
                                        'description' : 'description',
                                        'periods' : {'all':(begin,end)},
                                        'status' : 'publish'
                                        'problems' : {'ch1':5}
                                        'feedback' : 'non-immediate'
                                    })
        self.teacher.logout()
        self.student.login()
        self.student.select_course(appearance='physics')
        homework = self.student.driver.find_element(
            By.XPATH,'//div[contains(@class,"homework") and not(contains(@class,"deleted"))]'\
            '//span[contains(text,"'+assignment_name+'")]')
        homework = self.student.driver.find_element(
            By.XPATH,'//div[contains(@class,"homework") and not(contains(@class,"deleted"))]'\
            '//i[contains(@class,"icon-homework")]')
        self.student.driver.execute_script('return arguments[0].scrollIntoView();', homework)
        self.student.driver.execute_script('window.scrollBy(0, -80);')
        homework.click()

        try:
            #if the question is two part must answer free response to get to mc
            element = self.student.driver.find_element(
                By.TAG_NAME,'textarea')
            answer_text = "hello"
            for i in answer_text:
                element.send_keys(i)
            self.wait.until(
                expect.visibility_of_element_located(
                    ( By.XPATH,'//button/span[contains(text(),"Answer")]')
                )
            ).click()
        except:
            pass
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,'//div[contains(@class,"question-stem")]')
            )
        )
        element = self.student.driver.find_element(
            By.XPATH,'//div[@class="answer-letter"]')
        self.student.driver.execute_script('return arguments[0].scrollIntoView();', element)
        self.student.driver.execute_script('window.scrollBy(0, -150);')
        element.click()
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,'//button/span[contains(text(),"Submit")]')
            )
        ).click()
        # non immediate freedback goes straigt to the next question
        self.student.driver.find_element(
            By.XPATH,'//div[@data-question-number="2"]')
        self.ps.test_updates['passed'] = True


    # Case C8369 - 008 - Student | Verify the free response saved
    @pytest.mark.skipif(str(8369) not in TESTS, reason='Excluded')  # NOQA
    def test_student_verify_the_free_response_saved(self):
        """Verify the free response saved after entering it into the assessment.

        Steps:
        If the assessment has a free response text box,
        enter a free response into the free response text box
        Click on the next breadcrumb to get to the next assessment
        Click back to the original assessment


        Expected Result:
        The free response on the original assessment is saved
        """
        self.ps.test_updates['name'] = 't1.71.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.71','t1.71.008','8369']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'hw008'
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
        # non-immediate feedback
        self.teacher.add_assignment(assignemnt = 'homework',
                                    args = {
                                        'title' : assignment_name,
                                        'description' : 'description',
                                        'periods' : {'all':(begin,end)},
                                        'status' : 'publish'
                                        'problems' : {'ch1':5}
                                        'feedback' : 'non-immediate'
                                    })
        self.teacher.logout()
        self.student.login()
        self.student.select_course(appearance='physics')
        homework = self.student.driver.find_element(
            By.XPATH,'//div[contains(@class,"homework") and not(contains(@class,"deleted"))]'\
            '//span[contains(text,"'+assignment_name+'")]')
        self.student.driver.execute_script('return arguments[0].scrollIntoView();', homework)
        self.student.driver.execute_script('window.scrollBy(0, -80);')
        homework.click()

        sections = self.student.driver.find_elements(
            By.XPATH,'//span[contains(@class,"breadcrumbs")]')
        count = 0
        answer_text = "hello"
        while(True):
            try:
                element = self.student.driver.find_element(
                    By.TAG_NAME,'textarea')
                for i in answer_text:
                    element.send_keys(i)
                break
            except:
                count+=1
                if count >= len(sections):
                    print('no questions in this homework with free respnse')
                    raise Exception
                sections[count].click()
        sections[count+1].click()
        sections[count].click()
        self.student.driver.find_element(
            By.XPATH,'//textarea[text()="'+answer_text+'"]')

        self.ps.test_updates['passed'] = True


    # Case C8370 - 009 - Student | Verify the mutliple choice answer saved
    @pytest.mark.skipif(str(8370) not in TESTS, reason='Excluded')  # NOQA
    def test_student_verify_the_multiple_choice_answer_saved(self):
        """Verify the multiple choice answer saved.

        Steps:
        Select a multiple choice answer
        Click on the next breadcrumb to get to the next assessment
        Click back to the original assessment

        Expected Result:
        The multiple choice answer on the original assessment is saved
        """
        self.ps.test_updates['name'] = 't1.71.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.71','t1.71.009','8370']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'hw009'
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
        # non-immediate feedback
        self.teacher.add_assignment(assignemnt = 'homework',
                                    args = {
                                        'title' : assignment_name,
                                        'description' : 'description',
                                        'periods' : {'all':(begin,end)},
                                        'status' : 'publish'
                                        'problems' : {'ch1':5}
                                        'feedback' : 'non-immediate'
                                    })
        self.teacher.logout()
        self.student.login()
        self.student.select_course(appearance='physics')
        homework = self.student.driver.find_element(
            By.XPATH,'//div[contains(@class,"homework") and not(contains(@class,"deleted"))]'\
            '//span[contains(text,"'+assignment_name+'")]')
        self.student.driver.execute_script('return arguments[0].scrollIntoView();', homework)
        self.student.driver.execute_script('window.scrollBy(0, -80);')
        homework.click()

        sections = self.student.driver.find_elements(
            By.XPATH,'//span[contains(@class,"breadcrumbs")]')
        count = 0
        while(True):
            try:
                element = self.student.driver.find_element(
                    By.TAG_NAME,'textarea')
                for i in 'hello':
                    element.send_keys(i)
                self.wait.until(
                    expect.element_to_be_clickable(
                        ( By.XPATH,'//button/span[contains(text(),"Answer")]')
                    )
                ).click()
                break
            except:
                count+=1
                if count >= len(sections):
                    print('no questions in this homework with free respnse')
                    raise Exception
                sections[count].click()
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,'//div[contains(@class,"question-stem")]')
            )
        )
        #answer multple choice
        element = self.student.driver.find_element(
            By.XPATH,'//div[@class="answer-letter"]')
        self.student.driver.execute_script('return arguments[0].scrollIntoView();', element)
        self.student.driver.execute_script('window.scrollBy(0, -150);')
        element.click()
        #check that it saved
        sections[count+1].click()
        sections[count].click()
        self.student.driver.find_element(
            By.XPATH,'//div[contains(@data-reactid,"option-0")]'\
            '//div[contains(@class,"answer-checked")]')
        self.ps.test_updates['passed'] = True


    # Case C8371 - 010 - Student | Verify the assignment progress changed
    @pytest.mark.skipif(str(8371) not in TESTS, reason='Excluded')  # NOQA
    def test_student_verify_the_assignemnt_progress_changed(self):
        """Verify the assignment progress changed.

        Steps:
        If the assessment has a free response text box,
        enter a free response into the free response text box
        Click "Answer"
        If the assessment has multiple choices, select a multiple choice answer
        Click "Submit"
        Click on the course name in the left corner of the header

        Expected Result:
        The user returns to dashboard
        assignment progress shows the number of questions answered
        """
        self.ps.test_updates['name'] = 't1.71.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.71','t1.71.010','8371']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'hw010'
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
        # non-immediate feedback
        self.teacher.add_assignment(assignemnt = 'homework',
                                    args = {
                                        'title' : assignment_name,
                                        'description' : 'description',
                                        'periods' : {'all':(begin,end)},
                                        'status' : 'publish'
                                        'problems' : {'ch1':5}
                                        'feedback' : 'non-immediate'
                                    })
        self.teacher.logout()
        self.student.login()
        self.student.select_course(appearance='physics')
        homework = self.student.driver.find_element(
            By.XPATH,'//div[contains(@class,"homework") and not(contains(@class,"deleted"))]'\
            '//span[contains(text,"'+assignment_name+'")]')
        self.student.driver.execute_script('return arguments[0].scrollIntoView();', homework)
        self.student.driver.execute_script('window.scrollBy(0, -80);')
        homework.click()

        sections = self.student.driver.find_elements(
            By.XPATH,'//span[contains(@class,"breadcrumbs")]')
        stop_point = len(sections)//2

        for q in range(stop_point):
            try:
                #if the question is two part must answer free response to get to mc
                element = self.student.driver.find_element(
                    By.TAG_NAME,'textarea')
                answer_text = "hello"
                for i in answer_text:
                    element.send_keys(i)
                self.wait.until(
                    expect.visibility_of_element_located(
                        ( By.XPATH,'//button/span[contains(text(),"Answer")]')
                    )
                ).click()
            except:
                pass
            #answer the multiple choice  portion
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH,'//div[contains(@class,"question-stem")]')
                )
            )
            element = self.student.driver.find_element(
                By.XPATH,'//div[@class="answer-letter"]')
            self.student.driver.execute_script('return arguments[0].scrollIntoView();', element)
            self.student.driver.execute_script('window.scrollBy(0, -150);')
            element.click()
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH,'//button/span[contains(text(),"Submit")]')
                )
            ).click()
        self.student.driver.execute_script('window.scrollTo(0,0)')
        self.student.driver.find_element(By.XPATH,'//div[contains(@class,"course-name")]').click()
        self.student.driver.find_element(
            By.XPATH,'//div[contains(@class,"homework") and not(contains(@class,"deleted"))]'\
            '//span[contains(text(),"'+str(stop_point)+'/'+str(len(sections)-1)+' answered")]')
        self.ps.test_updates['passed'] = True


    # Case C8372 - 011 - Student | Answer all assessments in an assignment and view the completion report
    @pytest.mark.skipif(str(8372) not in TESTS, reason='Excluded')  # NOQA
    def test_student_answer_all_assesments_in_an_assignemnt_and_view_the_completion_report(self):
        """Answer all of the assessments in an assignment and view the completion report.

        Steps:
        answer all assesments in an assignment

        Expected Result:
        The user is presented with the completion report at the end of the assignment
        """
        self.ps.test_updates['name'] = 't1.71.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.71','t1.71.011','8372']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'hw011'
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
        # non-immediate feedback
        self.teacher.add_assignment(assignemnt = 'homework',
                                    args = {
                                        'title' : assignment_name,
                                        'description' : 'description',
                                        'periods' : {'all':(begin,end)},
                                        'status' : 'publish'
                                        'problems' : {'ch1':5}
                                        'feedback' : 'non-immediate'
                                    })
        self.teacher.logout()
        self.student.login()
        self.student.select_course(appearance='physics')
        homework = self.student.driver.find_element(
            By.XPATH,'//div[contains(@class,"homework") and not(contains(@class,"deleted"))]'\
            '//span[contains(text,"'+assignment_name+'")]')
        self.student.driver.execute_script('return arguments[0].scrollIntoView();', homework)
        self.student.driver.execute_script('window.scrollBy(0, -80);')
        homework.click()

        sections = self.student.driver.find_elements(
            By.XPATH,'//span[contains(@class,"breadcrumbs")]')
        for q in range(len(sections)-1):
            try:
                #if the question is two part must answer free response to get to mc
                element = self.student.driver.find_element(
                    By.TAG_NAME,'textarea')
                answer_text = "hello"
                for i in answer_text:
                    element.send_keys(i)
                self.wait.until(
                    expect.visibility_of_element_located(
                        ( By.XPATH,'//button/span[contains(text(),"Answer")]')
                    )
                ).click()
            except:
                pass
            #answer the multiple choice  portion
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH,'//div[contains(@class,"question-stem")]')
                )
            )
            element = self.student.driver.find_element(
                By.XPATH,'//div[@class="answer-letter"]')
            self.student.driver.execute_script('return arguments[0].scrollIntoView();', element)
            self.student.driver.execute_script('window.scrollBy(0, -150);')
            element.click()
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH,'//button/span[contains(text(),"Submit")]')
                )
            ).click()
        self.student.driver.find_element(
            By.XPATH,'//div[contains(@class,"completed-message")]')
        self.student.driver.find_element(
            By.XPATH,'//h1[contains(text(),"You are done")]')
        self.ps.test_updates['passed'] = True


    # Case C8373 - 012 - Student | Before the due date, change a mutliple choice answer
    @pytest.mark.skipif(str(8373) not in TESTS, reason='Excluded')  # NOQA
    def test_student_before_the_due_date_change_a_multiple_choice_answer(self):
        """Before the due date, change a mutliple choice answer.

        Steps:
        Click on a homework assignment on the list dashboard (that does not have instant feedback)
        If the assessment has a free response text box,
        enter a free response into the free response text box
        Click "Answer"
        If the assessment has multiple choices, select a multiple choice answer
        Click "Submit"

        Click on the course name in the left corner of the header
        Click on the same homework assignment
        Change a multiple choice answer on an assessment
        Click "Submit"

        Expected Result:
        A multiple choice answer is changed on an assessment
        """
        self.ps.test_updates['name'] = 't1.71.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.71','t1.71.012','8373']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'hw012'
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
        # non-immediate feedback
        self.teacher.add_assignment(assignemnt = 'homework',
                                    args = {
                                        'title' : assignment_name,
                                        'description' : 'description',
                                        'periods' : {'all':(begin,end)},
                                        'status' : 'publish'
                                        'problems' : {'ch1':5}
                                        'feedback' : 'non-immediate'
                                    })
        self.teacher.logout()
        self.student.login()
        self.student.select_course(appearance='physics')
        homework = self.student.driver.find_element(
            By.XPATH,'//div[contains(@class,"homework") and not(contains(@class,"deleted"))]'\
            '//span[contains(text,"'+assignment_name+'")]')
        self.student.driver.execute_script('return arguments[0].scrollIntoView();', homework)
        self.student.driver.execute_script('window.scrollBy(0, -80);')
        homework.click()

        try:
            #if the question is two part must answer free response to get to mc
            element = self.student.driver.find_element(
                By.TAG_NAME,'textarea')
            answer_text = "hello"
            for i in answer_text:
                element.send_keys(i)
            self.wait.until(
                expect.visibility_of_element_located(
                    ( By.XPATH,'//button/span[contains(text(),"Answer")]')
                )
            ).click()
        except:
            pass
        # answer mc portion
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,'//div[contains(@class,"question-stem")]')
            )
        )
        element = self.student.driver.find_element(
            By.XPATH,'//div[@class="answer-letter"]')
        self.student.driver.execute_script('return arguments[0].scrollIntoView();', element)
        self.student.driver.execute_script('window.scrollBy(0, -150);')
        element.click()
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,'//button/span[contains(text(),"Submit")]')
            )
        ).click()
        #go back to dashboard and reopen homework
        self.student.driver.execute_script('window.scrollTo(0,0)')
        self.student.driver.find_element(By.XPATH,'//div[contains(@class,"course-name")]').click()
        homework = self.student.driver.find_element(
            By.XPATH,'//div[contains(@class,"homework") and not(contains(@class,"deleted"))]'\
            '//i[contains(@class,"icon-homework")]')
        self.student.driver.execute_script('return arguments[0].scrollIntoView();', homework)
        self.student.driver.execute_script('window.scrollBy(0, -80);')
        homework.click()
        # reanswer mc portion
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,'//div[contains(@class,"question-stem")]')
            )
        )
        element = self.student.driver.find_element(
            By.XPATH,'//div[contains(@class,"answers-answer") and not(contains(@class,"checked"))]')
        self.student.driver.execute_script('return arguments[0].scrollIntoView();', element)
        self.student.driver.execute_script('window.scrollBy(0, -150);')
        element.click()
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,'//button/span[contains(text(),"Submit")]')
            )
        ).click()

        self.ps.test_updates['passed'] = True


    # Case C8374 - 013 - Student | View the completion report and return to the dashboard
    @pytest.mark.skipif(str(8374) not in TESTS, reason='Excluded')  # NOQA
    def test_student_view_the_completion_report_and_return_to_the_dashboard(self):
        """View the completion report and return to the dashboard.

        Steps:
        Click on a homework assignment on the list dashboard
        If the assessment has a free response text box
        enter a free response into the free response text box
        Click "Answer"
        If the assessment has multiple choices, select a multiple choice answer
        Click "Submit"
        Continue answering all assessments
        Click "Back To Dashboard"

        Expected Result:
        The user is returned to the dashboard
        """
        self.ps.test_updates['name'] = 't1.71.013' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.71','t1.71.013','8374']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'hw013'
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
        # non-immediate feedback/ or immeditae feedback
        self.teacher.add_assignment(assignemnt = 'homework',
                                    args = {
                                        'title' : assignment_name,
                                        'description' : 'description',
                                        'periods' : {'all':(begin,end)},
                                        'status' : 'publish'
                                        'problems' : {'ch1':5}
                                        'feedback' : 'non-immediate'
                                    })
        self.teacher.logout()
        self.student.login()
        self.student.select_course(appearance='physics')
        homework = self.student.driver.find_element(
            By.XPATH,'//div[contains(@class,"homework") and not(contains(@class,"deleted"))]'\
            '//span[contains(text,"'+assignment_name+'")]')
        self.student.driver.execute_script('return arguments[0].scrollIntoView();', homework)
        self.student.driver.execute_script('window.scrollBy(0, -80);')
        homework.click()

        sections = self.student.driver.find_elements(
            By.XPATH,'//span[contains(@class,"breadcrumbs")]')
        for q in range(len(sections)-1):
            try:
                #if the question is two part must answer free response to get to mc
                element = self.student.driver.find_element(
                    By.TAG_NAME,'textarea')
                answer_text = "hello"
                for i in answer_text:
                    element.send_keys(i)
                self.student.driver.find_element(
                    By.XPATH,'//button/span[contains(text(),"Answer")]').click()
            except:
                pass
            #answer the multiple choice  portion
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH,'//div[contains(@class,"question-stem")]')
                )
            )
            element = self.student.driver.find_element(
                By.XPATH,'//div[@class="answer-letter"]')
            self.student.driver.execute_script('return arguments[0].scrollIntoView();', element)
            self.student.driver.execute_script('window.scrollBy(0, -150);')
            element.click()
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH,'//button/span[contains(text(),"Submit")]')
                )
            ).click()
            try:
                # only click next question for assignemtns with immediate feedback
                self.student.driver.find_element(
                        By.XPATH,'//button/span[contains(text(),"Next Question")]').click()
            except:
                pass
        self.student.driver.find_element(
            By.XPATH,'//div[contains(@class,"completed-message")]')
        self.student.driver.find_element(
            By.XPATH,"//a[contains(text(),'Back to Dashboard')]").click()
        assert('list' in self.student.current_url()),\
            'Not back at dashboard'
        self.ps.test_updates['passed'] = True


    # # is this really needed, can it just be added to 011
    # # Case C8375 - 014 - Student | A completed homework shows "You are done" in completion report
    # @pytest.mark.skipif(str(8375) not in TESTS, reason='Excluded')  # NOQA
    # def test_student_a_shows_you_are_done_in_the_completion_report(self):
    #     """A completed homework should show "You are done" in the completion report.

    #     Steps:
    #     Click on a homework assignment on the list dashboard
    #     If the assessment has a free response text box,
    #     enter a free response into the free response text box
    #     Click "Answer"
    #     If the assessment has multiple choices, select a multiple choice answer
    #     Click "Submit"
    #     Continue answering all assessments

    #     Expected Result:
    #     The user is presented with the completion report that shows "You are done"

    #     """
    #     self.ps.test_updates['name'] = 't1.71.014' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = ['t1','t1.71','t1.71.014','8375']
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # Case C8376 - 015 - Student | A completed homework should show X/X answered in the dashboard
    @pytest.mark.skipif(str(8376) not in TESTS, reason='Excluded')  # NOQA
    def test_student_a_completed_homework_shows_x_out_of_x_in_the_dashbaord(self):
        """A completed homework should show X/X answered in the dashboard progress column.

        Steps:
        answer all assessments in a homework
        Click "Back To Dashboard"

        Expected Result:
        The user is returned to the dashboard.
        The completed homework shows X/X answered in the dashboard progress column.
        """
        self.ps.test_updates['name'] = 't1.71.015' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.71','t1.71.015','8376']
        self.ps.test_updates['passed'] = False

        assignment_name = 'hw015'
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
        # non-immediate feedback
        self.teacher.add_assignment(assignemnt = 'homework',
                                    args = {
                                        'title' : assignment_name,
                                        'description' : 'description',
                                        'periods' : {'all':(begin,end)},
                                        'status' : 'publish'
                                        'problems' : {'ch1':5}
                                        'feedback' : 'non-immediate'
                                    })
        self.teacher.logout()
        self.student.login()
        self.student.select_course(appearance='physics')
        homework = self.student.driver.find_element(
            By.XPATH,'//div[contains(@class,"homework") and not(contains(@class,"deleted"))]'\
            '//span[contains(text,"'+assignment_name+'")]')
        self.student.driver.execute_script('return arguments[0].scrollIntoView();', homework)
        self.student.driver.execute_script('window.scrollBy(0, -80);')
        homework.click()
        sections = self.student.driver.find_elements(
            By.XPATH,'//span[contains(@class,"breadcrumbs")]')
        for q in range( len(sections)-1 ):
            try:
                element = self.student.driver.find_element(
                    By.TAG_NAME,'textarea')
                answer_text = "hello"
                for i in answer_text:
                    element.send_keys(i)
                self.student.driver.find_element(
                    By.XPATH,'//button/span[contains(text(),"Answer")]').click()
            except:
                pass
            #answer the multiple choice  portion
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH,'//div[contains(@class,"question-stem")]')
                )
            )
            element = self.student.driver.find_element(
                By.XPATH,'//div[@class="answer-letter"]')
            self.student.driver.execute_script('return arguments[0].scrollIntoView();', element)
            self.student.driver.execute_script('window.scrollBy(0, -150);')
            element.click()
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH,'//button/span[contains(text(),"Submit")]')
                )
            ).click()
        self.student.driver.find_element(
            By.XPATH,'//a[contains(text(),"Back to Dashboard")]').click()
        self.student.driver.find_element(
            By.XPATH,'//div[contains(@class,"homework") and not(contains(@class,"deleted"))]'\
            '//span[contains(text(),"'+str(len(sections)-1)+'/'+str(len(sections)-1)+' answered")]')

        self.ps.test_updates['passed'] = True



    # # how to test this if it only happens sometimes? just keep looking at hw's until you find one?
    # # Case C8377 - 016 - Student | A homework may have a Review assessment
    # @pytest.mark.skipif(str(8377) not in TESTS, reason='Excluded')  # NOQA
    # def test_student_a_homework_may_have_a_review_assesment(self):
    #     """ A homework may have a Review assessment.

    #     Steps:

    #     Click on a homework assignment on the list dashboard
    #     If the assessment has a free response text box,
    #     enter a free response into the free response text box
    #     Click "Answer"
    #     If the assessment has multiple choices, select a multiple choice answer
    #     Click "Submit"
    #     Continue answering all assessments

    #     Expected Result:
    #     A homework may have a Review assessment toward the end
    #     """
    #     self.ps.test_updates['name'] = 't1.71.016' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = ['t1','t1.71','t1.71.016','8377']
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # how to test this if it only happens sometimes? just keep looking at hw's until you find one?
    # # Case C8378 - 017 - Student | A homework may have a Personalized assessment
    # @pytest.mark.skipif(str(8378) not in TESTS, reason='Excluded')  # NOQA
    # def test_student_a_homework_may_have_a_personalized_question(self):
    #     """A homework may have a Personalized assessment.

    #     Steps:
    #     Click on a homework assignment on the list dashboard
    #     If the assessment has a free response text box,
    #     enter a free response into the free response text box
    #     Click "Answer"
    #     If the assessment has multiple choices, select a multiple choice answer
    #     Click "Submit"
    #     Continue answering all assessments


    #     Expected Result:
    #     A homework may have a Personalized assessment toward the end
    #     """
    #     self.ps.test_updates['name'] = 't1.71.017' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = ['t1','t1.71','t1.71.017','8378']
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # Case C8379 - 018 - Student | Start a late homework assignment
    @pytest.mark.skipif(str(8379) not in TESTS, reason='Excluded')  # NOQA
    def test_student_start_a_late_homework_assignment(self):
        """A homework may have a Personalized assessment.

        Steps:
        Click on the "All Past Work" tab on the dashboard
        Click on a homework assignment

        Expected Result:
        The user starts a late homework assignment
        """
        self.ps.test_updates['name'] = 't1.71.018' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.71','t1.71.018','8379']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        # how to make a past due assignemnt, need to assume that one exists?
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,'//a[contains(text(),"All Past Work")]')
            )
        ).click()
        homework = self.student.driver.find_element(
            By.XPATH,'//div[contains(@aria-hidden,"false")]'\
            '//div[contains(@class,"homework") and not(contains(@class,"deleted"))]'\
            '//span[contains(text(),"0/")]')
        self.student.driver.execute_script('return arguments[0].scrollIntoView();', homework)
        self.student.driver.execute_script('window.scrollBy(0, -150);')
        ActionChains(self.student.driver).move_to_element(homework).perform()
        homework.click()
        wait = WebDriverWait(self.student.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"question-stem")]')
            )
        )

        self.ps.test_updates['passed'] = True


    # Case C8380 - 019 - Student | Submit a multiple choice answer on a late homework
    @pytest.mark.skipif(str(8380) not in TESTS, reason='Excluded')  # NOQA
    def test_stuednt_submit_a_multiple_choice_answer_on_a_late_homework(self):
        """Submit a multiple choice answer.

        Steps:
        Click on the "All Past Work" tab on the dashboard
        Click on a homework assignment
        Enter a free response into the free response text box
        Click "Answer"
        Select a multiple choice answer
        Click "Submit"

        Expected Result:
        A multiple choice answer is submitted
        """
        self.ps.test_updates['name'] = 't1.71.019' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.71','t1.71.019','8380']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        # how to make a past due assignemnt, need to assume that one exists?
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,'//a[contains(text(),"All Past Work")]')
            )
        ).click()
        homework = self.student.driver.find_element(
            By.XPATH,'//div[contains(@aria-hidden,"false")]'\
            '//div[contains(@class,"homework") and not(contains(@class,"deleted"))]'\
            '//span[contains(text(),"0/")]')
        self.student.driver.execute_script('return arguments[0].scrollIntoView();', homework)
        self.student.driver.execute_script('window.scrollBy(0, -150);')
        ActionChains(self.student.driver).move_to_element(homework).perform()
        homework.click()
        wait = WebDriverWait(self.student.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"question-stem")]')
            )
        )
        try:
            #if the question is two part must answer free response to get to mc
            element = self.student.driver.find_element(
                By.TAG_NAME,'textarea')
            answer_text = "hello"
            for i in answer_text:
                element.send_keys(i)
            self.wait.until(
                expect.visibility_of_element_located(
                    ( By.XPATH,'//button/span[contains(text(),"Answer")]')
                )
            ).click()
        except:
            pass
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,'//div[contains(@class,"question-stem")]')
            )
        )
        element = self.student.driver.find_element(
            By.XPATH,'//div[@class="answer-letter"]')
        self.student.driver.execute_script('return arguments[0].scrollIntoView();', element)
        self.student.driver.execute_script('window.scrollBy(0, -150);')
        element.click()
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,'//button/span[contains(text(),"Submit")]')
            )
        ).click()
        self.student.driver.find_element(
            By.XPATH,'//button/span[contains(text(),"Next Question")]')

        self.ps.test_updates['passed'] = True


    # Case C8381 - 020 - Student | Answer feedback is presented for a late homework
    @pytest.mark.skipif(str(8381) not in TESTS, reason='Excluded')  # NOQA
    def test_student_answer_feedback_is_presented_for_a_late_homework(self):
        """Answer feedback is presented on a late assignemnt.

        Steps:
        Click on the "All Past Work" tab on the dashboard
        Click on a homework assignment
        Enter a free response into the free response text box
        Click "Answer"
        Select a multiple choice answer
        Click "Submit"

        Expected Result:
        The multiple choice answer is submitted and answer feedback is presented
        """
        self.ps.test_updates['name'] = 't1.71.020' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.71','t1.71.020','8381']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        # how to make a late assignemnt, assuse one exisits?
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,'//a[contains(text(),"All Past Work")]')
            )
        ).click()
        homework = self.student.driver.find_element(
            By.XPATH,'//div[contains(@aria-hidden,"false")]'\
            '//div[contains(@class,"homework") and not(contains(@class,"deleted"))]'\
            '//span[contains(text(),"0/")]')
        self.student.driver.execute_script('return arguments[0].scrollIntoView();', homework)
        self.student.driver.execute_script('window.scrollBy(0, -150);')
        ActionChains(self.student.driver).move_to_element(homework).perform()
        homework.click()
        wait = WebDriverWait(self.student.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"question-stem")]')
            )
        )
        try:
            #if the question is two part must answer free response to get to mc
            element = self.student.driver.find_element(
                By.TAG_NAME,'textarea')
            answer_text = "hello"
            for i in answer_text:
                element.send_keys(i)
            self.wait.until(
                expect.visibility_of_element_located(
                    ( By.XPATH,'//button/span[contains(text(),"Answer")]')
                )
            ).click()
        except:
            pass
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,'//div[contains(@class,"question-stem")]')
            )
        )
        element = self.student.driver.find_element(
            By.XPATH,'//div[@class="answer-letter"]')
        self.student.driver.execute_script('return arguments[0].scrollIntoView();', element)
        self.student.driver.execute_script('window.scrollBy(0, -150);')
        element.click()
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,'//button/span[contains(text(),"Submit")]')
            )
        ).click()
        self.student.driver.find_element(
            By.XPATH,'//div[contains(@class,"question-feedback-content")]')
        self.ps.test_updates['passed'] = True


    # Case C8382 - 021 - Student | Correctness is displayed in the breadcrumbs for a late homework
    @pytest.mark.skipif(str(8382) not in TESTS, reason='Excluded')  # NOQA
    def test_student_corectness_is_displayed_in_the_breadcrumbs_for_A_late_homework(self):
        """Correctness for a completed assessment is displayed in the breadcrumbs.
        for a late homework

        Steps:
        Click on the "All Past Work" tab on the dashboard
        Click on a homework assignment
        Enter a free response into the free response text box
        Click "Answer"
        Select a multiple choice answer
        Click "Submit"

        Expected Result:
        Correctness for a completed assessment is displayed in the breadcrumbs
        """
        self.ps.test_updates['name'] = 't1.71.021' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.71','t1.71.021','8382']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        #how to create a late hw
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,'//a[contains(text(),"All Past Work")]')
            )
        ).click()
        homework = self.student.driver.find_element(
            By.XPATH,'//div[contains(@aria-hidden,"false")]'\
            '//div[contains(@class,"homework") and not(contains(@class,"deleted"))]'\
            '//span[contains(text(),"0/")]')
        self.student.driver.execute_script('return arguments[0].scrollIntoView();', homework)
        self.student.driver.execute_script('window.scrollBy(0, -150);')
        ActionChains(self.student.driver).move_to_element(homework).perform()
        homework.click()
        wait = WebDriverWait(self.student.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"question-stem")]')
            )
        )
        try:
            #if the question is two part must answer free response to get to mc
            element = self.student.driver.find_element(
                By.TAG_NAME,'textarea')
            answer_text = "hello"
            for i in answer_text:
                element.send_keys(i)
            self.wait.until(
                expect.visibility_of_element_located(
                    ( By.XPATH,'//button/span[contains(text(),"Answer")]')
                )
            ).click()
        except:
            pass
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,'//div[contains(@class,"question-stem")]')
            )
        )
        element = self.student.driver.find_element(
            By.XPATH,'//div[@class="answer-letter"]')
        self.student.driver.execute_script('return arguments[0].scrollIntoView();', element)
        self.student.driver.execute_script('window.scrollBy(0, -150);')
        element.click()
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,'//button/span[contains(text(),"Submit")]')
            )
        ).click()
        self.student.driver.find_element(
            By.XPATH,'//span[contains(@class,"breadcrumb")]'\
            '//i[contains(@class,"correct") or contains(@class,"incorrect")]')
        self.ps.test_updates['passed'] = True


    # Case C8383 - 022 - Student | Start an open homework assignment with immediate feedback
    @pytest.mark.skipif(str(8383) not in TESTS, reason='Excluded')  # NOQA
    def test_student_start_an_open_homework_assignemnt_with_immediate_feedback(self):
        """Start an open homework assignment with immediate feedback.

        Steps:
        (in set up create a hw with immeditae feedback)
        Click on a homework assignment on the list dashboard

        Expected Result:
        The user starts an open homework assignment
        """
        self.ps.test_updates['name'] = 't1.71.022' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.71','t1.71.022','8383']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'hw022'
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
        # immediate feedback
        self.teacher.add_assignment(assignemnt = 'homework',
                                    args = {
                                        'title' : assignment_name,
                                        'description' : 'description',
                                        'periods' : {'all':(begin,end)},
                                        'status' : 'publish'
                                        'problems' : {'ch1':5}
                                        'feedback' : 'immediate'
                                    })
        self.teacher.logout()
        self.student.login()
        self.student.select_course(appearance='physics')
        homework = self.student.driver.find_element(
            By.XPATH,'//div[contains(@class,"homework") and not(contains(@class,"deleted"))]'\
            '//span[contains(text,"'+assignment_name+'")]')
        self.student.driver.execute_script('return arguments[0].scrollIntoView();', homework)
        self.student.driver.execute_script('window.scrollBy(0, -150);')
        ActionChains(self.student.driver).move_to_element(homework).perform()
        homework.click()

        self.ps.test_updates['passed'] = True


    # Case C8384 - 023 - Student | Submit a multiple choice answer for a homework with immediate feedback
    @pytest.mark.skipif(str(8384) not in TESTS, reason='Excluded')  # NOQA
    def test_student_submit_a_multiple_choice_answer_for_a_homework_with_immediate_feedback(self):
        """Submit a multiple choice answer for a hoemwork with imediate feedback

        Steps:
        Click on a homework assignment on the list dashboard
        Enter a free response into the free response text box
        Click "Answer"
        Select a multiple choice answer
        Click "Submit"

        Expected Result:
        A multiple choice answer is submitted
        """
        self.ps.test_updates['name'] = 't1.71.023' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.71','t1.71.023','8384']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'hw023'
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
        # non-immediate feedback
        self.teacher.add_assignment(assignemnt = 'homework',
                                    args = {
                                        'title' : assignment_name,
                                        'description' : 'description',
                                        'periods' : {'all':(begin,end)},
                                        'status' : 'publish'
                                        'problems' : {'ch1':5}
                                        'feedback' : 'immediate'
                                    })
        self.teacher.logout()
        self.student.login()
        self.student.select_course(appearance='physics')
        homework = self.student.driver.find_element(
            By.XPATH,'//div[contains(@class,"homework") and not(contains(@class,"deleted"))]'\
            '//span[contains(text,"'+assignment_name+'")]')
        self.student.driver.execute_script('return arguments[0].scrollIntoView();', homework)
        self.student.driver.execute_script('window.scrollBy(0, -150);')
        ActionChains(self.student.driver).move_to_element(homework).perform()
        homework.click()
        wait = WebDriverWait(self.student.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"question-stem")]')
            )
        )
        try:
            #if the question is two part must answer free response to get to mc
            element = self.student.driver.find_element(
                By.TAG_NAME,'textarea')
            answer_text = "hello"
            for i in answer_text:
                element.send_keys(i)
            self.wait.until(
                expect.visibility_of_element_located(
                    ( By.XPATH,'//button/span[contains(text(),"Answer")]')
                )
            ).click()
        except:
            pass
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,'//div[contains(@class,"question-stem")]')
            )
        )
        element = self.student.driver.find_element(
            By.XPATH,'//div[@class="answer-letter"]')
        self.student.driver.execute_script('return arguments[0].scrollIntoView();', element)
        self.student.driver.execute_script('window.scrollBy(0, -150);')
        element.click()
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,'//button/span[contains(text(),"Submit")]')
            )
        ).click()
        self.student.driver.find_element(
            By.XPATH,'//button/span[contains(text(),"Next Question")]')
        self.ps.test_updates['passed'] = True


    # Case C8385 - 024 - Student | Answer feedback is presented for a homework with immediate feedback
    @pytest.mark.skipif(str(8385) not in TESTS, reason='Excluded')  # NOQA
    def test_student_answer_feedback_is_presented_for_a_homework_with_immediate_feedback(self):
        """Answer feedback is presented for a homework with immediate feedback.

        Steps:
        Click on a homework assignment on the list dashboard
        Enter a free response into the free response text box
        Click "Answer"
        Select a multiple choice answer
        Click "Submit"

        Expected Result:
        Answer feedback is presented
        """
        self.ps.test_updates['name'] = 't1.71.024' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.71','t1.71.024','8385']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'hw0024'
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
        # immediate feedback
        self.teacher.add_assignment(assignemnt = 'homework',
                                    args = {
                                        'title' : assignment_name,
                                        'description' : 'description',
                                        'periods' : {'all':(begin,end)},
                                        'status' : 'publish'
                                        'problems' : {'ch1':5}
                                        'feedback' : 'immediate'
                                    })
        self.teacher.logout()
        self.student.login()
        self.student.select_course(appearance='physics')
        homework = self.student.driver.find_element(
            By.XPATH,'//div[contains(@class,"homework") and not(contains(@class,"deleted"))]'\
            '//span[contains(text,"'+assignment_name+'")]')
        self.student.driver.execute_script('return arguments[0].scrollIntoView();', homework)
        self.student.driver.execute_script('window.scrollBy(0, -150);')
        ActionChains(self.student.driver).move_to_element(homework).perform()
        homework.click()
        wait = WebDriverWait(self.student.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"question-stem")]')
            )
        )
        try:
            #if the question is two part must answer free response to get to mc
            element = self.student.driver.find_element(
                By.TAG_NAME,'textarea')
            answer_text = "hello"
            for i in answer_text:
                element.send_keys(i)
            self.wait.until(
                expect.visibility_of_element_located(
                    ( By.XPATH,'//button/span[contains(text(),"Answer")]')
                )
            ).click()
        except:
            pass
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,'//div[contains(@class,"question-stem")]')
            )
        )
        element = self.student.driver.find_element(
            By.XPATH,'//div[@class="answer-letter"]')
        self.student.driver.execute_script('return arguments[0].scrollIntoView();', element)
        self.student.driver.execute_script('window.scrollBy(0, -150);')
        element.click()
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,'//button/span[contains(text(),"Submit")]')
            )
        ).click()
        self.student.driver.find_element(
            By.XPATH,'//div[contains(@class,"question-feedback-content")]')
        self.ps.test_updates['passed'] = True


    # Case C8386 - 025 - Student | Correctness displayed in the breadcrumbs for a homework with immediate feedback
    @pytest.mark.skipif(str(8386) not in TESTS, reason='Excluded')  # NOQA
    def test_student_correctness_displayed_in_the_breadcrumbs_for_a_homeowrk_with_immediate_feedback(self):
        """Correctness for a completed assessment is displayed in the breadcrumbs
        for a homework with immediate feedback .

        Steps:
        Click on a homework assignment on the list dashboard
        Enter a free response into the free response text box
        Click "Answer"
        Select a multiple choice answer
        Click "Submit"

        Expected Result:
        Correctness for a completed assessment is displayed in the breadcrumbs
        """
        self.ps.test_updates['name'] = 't1.71.025' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.71','t1.71.025','8386']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'hw025'
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
        # immediate feedback
        self.teacher.add_assignment(assignemnt = 'homework',
                                    args = {
                                        'title' : assignment_name,
                                        'description' : 'description',
                                        'periods' : {'all':(begin,end)},
                                        'status' : 'publish'
                                        'problems' : {'ch1':5}
                                        'feedback' : 'immediate'
                                    })
        self.teacher.logout()
        self.student.login()
        self.student.select_course(appearance='physics')
        homework = self.student.driver.find_element(
            By.XPATH,'//div[contains(@class,"homework") and not(contains(@class,"deleted"))]'\
            '//span[contains(text,"'+assignment_name+'")]')
        self.student.driver.execute_script('return arguments[0].scrollIntoView();', homework)
        self.student.driver.execute_script('window.scrollBy(0, -150);')
        ActionChains(self.student.driver).move_to_element(homework).perform()
        homework.click()
        wait = WebDriverWait(self.student.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"question-stem")]')
            )
        )
        try:
            #if the question is two part must answer free response to get to mc
            element = self.student.driver.find_element(
                By.TAG_NAME,'textarea')
            answer_text = "hello"
            for i in answer_text:
                element.send_keys(i)
            self.wait.until(
                expect.visibility_of_element_located(
                    ( By.XPATH,'//button/span[contains(text(),"Answer")]')
                )
            ).click()
        except:
            pass
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,'//div[contains(@class,"question-stem")]')
            )
        )
        element = self.student.driver.find_element(
            By.XPATH,'//div[@class="answer-letter"]')
        self.student.driver.execute_script('return arguments[0].scrollIntoView();', element)
        self.student.driver.execute_script('window.scrollBy(0, -150);')
        element.click()
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,'//button/span[contains(text(),"Submit")]')
            )
        ).click()
        self.student.driver.find_element(
            By.XPATH,'//span[contains(@class,"breadcrumb")]'\
            '//i[contains(@class,"correct") or contains(@class,"incorrect")]')
        self.ps.test_updates['passed'] = True


