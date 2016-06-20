"""Tutor v1, Epic 55 - Practice."""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
from random import randint  # NOQA
from selenium.webdriver.common.by import By  # NOQA
from selenium.webdriver.support import expected_conditions as expect  # NOQA
from staxing.assignment import Assignment  # NOQA
from selenium.webdriver.support.ui import WebDriverWait

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Student  # NOQA

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': '50.0',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([8297, 8298, 8299, 8300, 
         8301, 8302, 8303, 8304, 
         8305, 8306, 8307, 8308, 
         8309, 8310])  # NOQA
)


@PastaDecorator.on_platforms(BROWSERS)
class TestPractice(unittest.TestCase):
    """T1.55 - Practice."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.student = Student(
            use_env_vars=True#,
            #pasta_user=self.ps,
            #capabilities=self.desired_capabilities
        )
        self.student.login()
        self.student.select_course(appearance='physics')
        self.wait = WebDriverWait(self.student.driver, Assignment.WAIT_TIME)
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@aria-describedby, "progress-bar-tooltip-")]')
            )
        ).click()         


    def tearDown(self):
        """Test destructor."""
        self.ps.update_job(job_id=str(self.student.driver.session_id),
                           **self.ps.test_updates)
        try:
            self.student.delete()
        except:
            pass

    # # Case C8297 - 001 - Student | Click on a section performance forecast bar to start practice
    # @pytest.mark.skipif(str(8297) not in TESTS, reason='Excluded')  # NOQA
    # def test_student_click_on_a_section_performance_forecast_bar_to_start_a_practice(self):
    #     """Click on a section performance forecast bar to start a practice session.

    #     Steps:
    #     Click one of the section performance bars from the dashboard (in setup)

    #     Expected Result:
    #     The user is taken to a practice session for the section. 
    #     """
    #     self.ps.test_updates['name'] = 't1.55.001' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = ['t1','t1.55','t1.55.001','8297']
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions
    #     assert('practice' in self.student.current_url()), \
    #         'Not in practice assignment'

    #     self.ps.test_updates['passed'] = True

    
    # # Not sure if this is working, there is a bug on tutor now, will go back
    # # Case C8298 - 002 - Student | Navigate between questions using the breadcrumbs
    # @pytest.mark.skipif(str(8298) not in TESTS, reason='Excluded')  # NOQA
    # def test_student_navigate_between_questions_using_the_breadcrumbs(self):
    #     """Navigate between questions using the breadcrumbs.

    #     Steps:
    #     Click a breadcrumb

    #     Expected Result:
    #     The student is taken to a different question in the practice session.
    #     """
    #     self.ps.test_updates['name'] = 't1.55.002' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = ['t1','t1.55','t1.55.002','8298']
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions
    #     sections = self.student.driver.find_elements(By.XPATH,'//span[contains(@class,"breadcrumbs")]')
    #     section = sections[-1]
    #     chapter = section.get_attribute("data-reactid")
    #     section.click()
    #     self.student.driver.find_element(
    #         By.XPATH,'//div[@data-question-number="'+chapter[-1]+'")]')
        
    #     self.ps.test_updates['passed'] = True


    # # Case C8299 - 003 - Student | Scrolling the window up reveals the header bar
    # @pytest.mark.skipif(str(8299) not in TESTS, reason='Excluded')  # NOQA
    # def test_student_scrolling_the_window_up_reveals_the_header_bar(self):
    #     """Scrolling the window up reveals the header bar.

    #     Steps:
    #     Scroll down
    #     Scroll to the top of the page

    #     Expected Result:
    #     The header bar, containing the course name, OpenStax logo, and user menu link are visible.
    #     """
    #     self.ps.test_updates['name'] = 't1.55.003' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = ['t1','t1.55','t1.55.003','8299']
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions
    #     # should this case have something about a question long enought to actually scroll
    #     self.student.driver.execute_script("window.scrollTo(0, 100);")
    #     self.student.driver.execute_script("window.scrollTo(0, 0);")
    #     self.student.driver.find_element(By.CLASS_NAME,'ui-brand-logo') #is visible?

    #     self.ps.test_updates['passed'] = True


    # Case C8300 - 004 - Student | Inputting a free response activates the Answer button
    @pytest.mark.skipif(str(8300) not in TESTS, reason='Excluded')  # NOQA
    def test_student_inputting_a_free_response_activates_the_answer_button(self):
        """Inputting a free response into activates the Answer button.

        Steps:
        If there is a text box: input text
        otherwise click on the next breadcrumb until a textbox is available

        Expected Result:
        The "Answer" button is click-able.
        """
        self.ps.test_updates['name'] = 't1.55.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.55','t1.55.004','8300']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.wait.until(
            expect.visibility_of_element_located(
                ( By.TAG_NAME,'textarea')
            )
        ).send_keys("hello")
        self.wait.until(
            expect.element_to_be_clickable(
                ( By.XPATH,'//button/span[contains(text(),"Answer")]')
            )
        )
        self.ps.test_updates['passed'] = True


    # Case C8301 - 005 - Student | Answer a free reponse question
    @pytest.mark.skipif(str(8301) not in TESTS, reason='Excluded')  # NOQA
    def test_student_answer_a_free_response_question(self):
        """Answer a free reponse question.

        Steps:
        If there is a text box, input text
        Click the "Answer" button 

        Expected Result:
        The text box disappears and the multiple choice answer appear.
        """
        self.ps.test_updates['name'] = 't1.55.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.55','t1.55.005','8301']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.wait.until(
            expect.visibility_of_element_located(
                ( By.TAG_NAME,'textarea')
            )
        ).send_keys("hello")
        self.wait.until(
            expect.visibility_of_element_located(
                ( By.XPATH,'//button/span[contains(text(),"Answer")]')
            )
        ).click()
        ###find multiple choice answers
        ###find text of initial free response answer on page
        self.ps.test_updates['passed'] = True


    # # Case C8302 - 006 - Student | Selecting a multiple choice answer activates the Submit button
    # @pytest.mark.skipif(str(8302) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Selecting a multiple choice answer activates the Submit button.

    #     Steps:

    #     Click one of the section performance bars from the dashboard
        
    #     OR
        
    #     Click on the user menu 
    #     Click "Performance Forecast"
    #     Click one of the section performance bars 

    #     If there is a text box, input text
    #     Click the "Answer" button
    #     Select a multiple choice answer 


    #     Expected Result:

    #     The "Submit" button can now be clicked

    #     """
    #     self.ps.test_updates['name'] = 't1.55.006' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.55',
    #         't1.55.006',
    #         '8302'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C8303 - 007 - Student | Submit the assessment
    # @pytest.mark.skipif(str(8303) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Submit the assessment.

    #     Steps:

    #     Click one of the section performance bars from the dashboard
        
    #     OR
        
    #     Click on the user menu 
    #     Click "Performance Forecast"
    #     Click one of the section performance bars 

    #     If there is a text box, input text
    #     Click the "Answer" button
    #     Select a multiple choice answer
    #     Click the "Submit" button 


    #     Expected Result:

    #     The answer is submitted and the 'Next Question' button appears.

    #     """
    #     self.ps.test_updates['name'] = 't1.55.007' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.55',
    #         't1.55.007',
    #         '8303'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C8304 - 008 - Student | Answer feedback is presented
    # @pytest.mark.skipif(str(8304) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Answer feedback is presented.

    #     Steps:

    #     Click one of the section performance bars from the dashboard
        
    #     OR
        
    #     Click on the user menu 
    #     Click "Performance Forecast"
    #     Click one of the section performance bars 

    #     If there is a text box, input text
    #     Click the "Answer" button
    #     Select a multiple choice answer
    #     Click the "Submit" button 


    #     Expected Result:

    #     The answer is submitted, the correct answer is displayed, and feedback on the answer is given.

    #     """
    #     self.ps.test_updates['name'] = 't1.55.008' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.55',
    #         't1.55.008',
    #         '8304'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True



    # # Case C8305 - 009 - Student | Correctness for a completed assessment is displayed in the breadcrumbs
    # @pytest.mark.skipif(str(8305) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Correctness for a completed assessment is displayed in the breadcrumbs.

    #     Steps:

    #     Click one of the section performance bars from the dashboard
        
    #     OR
        
    #     Click on the user menu 
    #     Click "Performance Forecast"
    #     Click one of the section performance bars 

    #     If there is a text box, input text
    #     Click the "Answer" button
    #     Select a multiple choice answer
    #     Click the "Submit" button 


    #     Expected Result:

    #     The correctness for the completed question is visible in the breadcrumb.

    #     """
    #     self.ps.test_updates['name'] = 't1.55.009' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.55',
    #         't1.55.009',
    #         '8305'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C8306 - 010 - Student | The assessment identification number and version are visible for each assessment
    # @pytest.mark.skipif(str(8306) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """The assessment identification number and version are visible for each assessment.

    #     Steps:

    #     Click one of the section performance bars from the dashboard
        
    #     OR
        
    #     Click on the user menu 
    #     Click "Performance Forecast"
    #     Click one of the section performance bars 

    #     Navigate through each question in the assessment


    #     Expected Result:

    #     Each question's identification number and version are visible.

    #     """
    #     self.ps.test_updates['name'] = 't1.55.010' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.55',
    #         't1.55.010',
    #         '8306'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C8307 - 011 - Student | Clicking on Report an error renders the Assessment Errata Form and prefills the assessment
    # @pytest.mark.skipif(str(8307) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Clicking on Report an error renders the Assessment Errata Form and prefills the assessment.

    #     Steps:

    #     Click one of the section performance bars from the dashboard
        
    #     OR
        
    #     Click on the user menu 
    #     Click "Performance Forecast"
    #     Click one of the section performance bars 

    #     Click the "Report an error" link


    #     Expected Result:

    #     The user is taken to the Assessment Errata Form and the ID is prefilled.

    #     """
    #     self.ps.test_updates['name'] = 't1.55.011' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.55',
    #         't1.55.011',
    #         '8307'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C8308 - 012 - Student | Submit the Assessment Errata Form
    # @pytest.mark.skipif(str(8308) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Submit the Assessment Errata Form.

    #     Steps:

    #     Click one of the section performance bars from the dashboard
        
    #     OR
        
    #     Click on the user menu 
    #     Click "Performance Forecast"
    #     Click one of the section performance bars 

    #     Click the "Report an error" link
    #     Fill out the fields
    #     Click the "Submit" button


    #     Expected Result:

    #     The form is submitted

    #     """
    #     self.ps.test_updates['name'] = 't1.55.012' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.55',
    #         't1.55.012',
    #         '8308'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C8309 - 013 - Student | End of practice shows the number of assessments answered
    # @pytest.mark.skipif(str(8309) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """End of practice shows the number of assessments answered.

    #     Steps:

    #     Click one of the section performance bars from the dashboard
        
    #     OR
        
    #     Click on the user menu 
    #     Click "Performance Forecast"
    #     Click one of the section performance bars 

    #     Answer the assessments


    #     Expected Result:

    #     End of practice shows the number of assessments answered

    #     """
    #     self.ps.test_updates['name'] = 't1.55.013' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.55',
    #         't1.55.013',
    #         '8309'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C8310 - 014 - Student | Clicking the Back To Dashboard button returns the user to the dashboard
    # @pytest.mark.skipif(str(8310) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Clicking the Back To Dashboard button returns the user to the dashboard.

    #     Steps:

    #     Click one of the section performance bars from the dashboard

    #     Answer the assessments
    #     Click "Back To Dashboard"


    #     Expected Result:

    #     The user is returned to the dashboard

    #     """
    #     self.ps.test_updates['name'] = 't1.55.014' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.55',
    #         't1.55.014',
    #         '8310'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True

