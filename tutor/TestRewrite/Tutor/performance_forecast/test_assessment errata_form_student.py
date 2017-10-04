"""
Title: test assessment errata form
User(s): student
Domain: Exercises
Testrail ID: C148106


Jacob Diaz
7/26/17


Corresponding Case(s):
t1.55.11,12


Progress:
Written, Not tested yet

Work to be done/Questions:
Test it, add/update code where necessary

Merge-able with any scripts? If so, which? :


"""

# import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
# from random import randint
# from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from staxing.assignment import Assignment
from selenium.webdriver.support.ui import WebDriverWait
# from random import randint


# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Student  # , Teacher

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
        1, 2
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestPractice(unittest.TestCase):

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        if not LOCAL_RUN:
            self.student = Student(
                use_env_vars=True,
                pasta_user=self.ps,
                capabilities=self.desired_capabilities
            )
        else:
            self.student = Student(
                use_env_vars=True
            )
        self.student.login()
        self.student.select_course(title='College Physics with Courseware')
        self.wait = WebDriverWait(self.student.driver, Assignment.WAIT_TIME)
        self.wait.until(
            expect.visibility_of_element_located((
                By.XPATH,
                '//button[contains(@class,"practice")]'
            ))
        ).click()
        self.wait = WebDriverWait(self.student.driver, Assignment.WAIT_TIME)
        self.student.login()

    def tearDown(self):
        """Test destructor."""
        if not LOCAL_RUN:
            self.ps.update_job(
                job_id=str(self.student.driver.session_id),
                **self.ps.test_updates
            )
        try:
            self.student.delete()
        except:
            pass

    # IN THE CASE THAT CLICKING THE ERRATA LINK OPENS UP A NEW WINDOW, YOU CAN
    # IMPLEMENT THIS TO BE PART OF performance_practice_student()
    @pytest.mark.skipif(str(1) not in TESTS, reason='Excluded')
    def test_assessment_errata_form(self):
        '''
        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Login with student account
        Click on the 'Sign in' button
        If the user has more than one course, select a Tutor course

        Click one of the section performance bars from the dashboard
        OR
        Click on the user menu
        Click "Performance Forecast"
        Click one of the section performance bars

        Click the 'Report an error' link
        ***The user is taken to the Assessment Errata Form and the ID is
        prefilled.(t1.55.11)***

        Fill out the fields
        Click the 'Submit' button
        ***The form is submitted and the message that says "Your response has
        been recorded" is displayed (t1.55.12)***

        Corresponds to...
        t1.55.11,12
        '''
        # Test steps and verification assertions
        # t1.55.11 --> The user is taken to the Assessment Errata Form and the
        # ID is prefilled
        # Navigate to performance forecast
        self.student.select_course(title='zPhysics w Courseware')

        # Go to practice
        practice_text = self.student.find(
            By.XPATH,
            "//div[contains(text(),'Practice more')]"
        )
        practice_text.click()
        # practice exercises take a realllly long time to load
        self.student.driver.wait(20)
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, "//div[contains(@class,'card-body')]")
            )
        )

        # find the identifier
        id_num = self.student.find(
            By.XPATH,
            '//span[@class="exercise-identifier-link"]'
        ).text.split(" |")[0]
        self.wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'Report an error')
            )
        ).click()

        window_with_form = self.student.driver.window_handles[1]
        self.student.driver.switch_to_window(window_with_form)
        self.student.page.wait_for_page_load()
        assert("errata" in self.student.current_url()), \
            'not taken to assesment errata form'
        text_box = self.student.find(
            By.XPATH, '//input[@name="location"]')
        assert(id_num[4:] in text_box.get_attribute('value')), \
            'form not prefilled correctly'

        # t1.55.12 --> The form is submitted and the message that
        # says "Your response has been recorded" is displayed

        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//h1[contains(text(),"Suggest a Correction")]')
            )
        )
        self.student.find(
            By.XPATH, '//input[@type="radio" and @value="Typo"]').click()
        self.student.find(
            By.XPATH,
            '//textarea[@name="detail"]'
        ).send_keys('automated qa test')
        self.student.find(
            By.XPATH, '//input[@type="submit"]').click()
        # find submitted message
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//h1[contains(text(),"Thanks for your help!")]')
            )
        )
