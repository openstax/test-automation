"""
System: Tutor
User(s): student
Title:TEST WORK IN PERFORMANCE FORECAST STUDENT
Testrail ID: C148105

Jacob Diaz
7/26/17


Corresponding Case(s):
t1.55. 2--> 10,13,14


Progress:
In revision


Work to be done/Questions:
Need to run it a couple times and fix the places where it fails

Merge-able with any scripts? If so, which? :

"""

# import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
# from random import randint
from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from staxing.assignment import Assignment
from selenium.webdriver.support.ui import WebDriverWait

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

    @pytest.mark.skipif(str(1) not in TESTS, reason='Excluded')
    def test_performance_practice_student(self):
        '''
        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the student user account [ student01 | password ] in the username
        and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, select a Tutor course

        Click one of the section performance bars from the dashboard
        OR
        Click on the user menu
        Click "Performance Forecast"
        Click one of the section performance bars

        Scroll to the top of the page
        ***The header bar, containing the course name, OpenStax logo, and user
        menu link are visible. (t1.55.03)***

        Click a breadcrumb
        ***The student is taken to a different question in the practice
        session. (t1.55.02)***

        If there is a text box, input text
        ***The 'Answer' button can now be clicked. (t1.55.04)***

        Click the 'Answer' button
        ***The text box disappears and the multiple choice answer appear
        (t1.55.05)***

        Select a multiple choice answer
        ***The 'Submit' button can now be clicked.(t1.55.06)***

        Click the 'Submit' button
        ***The answer is submitted and the 'Next Question' button appears.
        (t1.55.07)***
        ***The answer is submitted, the correct answer is displayed, and
        feedback on the answer is given. (t1.55.08)***
        ***The correctness for the completed question is visible in the
        breadcrumb. (t1.55.09)***

        Navigate through each question in the assessment and Answer the
        assessments
        ***Each question's identification number and version are visible.
        (t1.55.10)***
        ***End of practice shows the number of assessments answered
        (t1.55.13)***

        Click "Back To Dashboard"
        ***The user is returned to the dashboard (t1.55.14)***

        Corresponds to:
        t1.55. 2--> 10,13,14
        :return:
        '''
        # Navigate to performance forecast

        self.student.select_course(title='zPhysics w Courseware')
        # NOT SURE WHICH COURSE WE SHOULD USE --> DO WE USE ONE COURSE WHICH WE
        # ASSUME THE STUDENT HAS?
        # YOU REALLY CAN'T USE JUST ANY COURSE EITHER --> IT HAS TO HAVE
        # SUFFICIENT QUESITONS ANSWERED
        # AS TO ALLOW FOR PRACTICE

        # self.student.goto_performance_forecast()

        # Go to practice
        practice_text = self.student.find(
            By.XPATH,
            "//div[contains(text(),'Practice more')]"
        )
        # SHOULD WE ADD COMMAND  TO SCROLL TO THIS?
        practice_text.click()
        # practice exercises take a realllly long time to load
        self.student.driver.wait(20)
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, "//div[contains(@class,'card-body')]")
            )
        )

        # t1.55.03 --> The header bar, containing the course name, OpenStax
        # logo, and user menu link are visible
        navbar = self.student.find(
            By.XPATH,
            "//nav[contains(@class,'navbar')]"
        )
        # OS logo
        navbar.find_element(By.XPATH, "//i[contains(@class,'brand-logo')]")
        # course name
        navbar.find_element(By.XPATH, "//a[contains(@class,'course-name')]")
        # user menu
        navbar.find_element(By.XPATH, "//a[contains(@id,'user-actions')]")

        # DO WE NEED THIS PIECE OF CODE TO SEND KEYS? IT SEEMS THAT WE'RE DOING
        # THIS LATER

        # scroll page
        self.student.driver.execute_script("window.scrollTo(0, 100);")
        self.student.driver.execute_script("window.scrollTo(0, 0);")
        self.student.find(By.CLASS_NAME, 'ui-brand-logo')

        # t1.55.02 --> The student is taken to a different question in the
        # practice session.
        sections = self.student.find_all(
            By.XPATH, '//span[contains(@class,"breadcrumbs")]')
        section = sections[-2]
        section.click()
        self.student.find(
            By.XPATH,
            '//div[contains(@data-question-number,"%s")]' %
            (len(sections) - 1)
        )

        # t1.55.04 --> The 'Answer' button can now be clicked.

        for x in range(len(sections)):
            try:
                element = self.student.find(
                    By.TAG_NAME, 'textarea')
                for i in 'hello':
                    element.send_keys(i)
                self.wait.until(
                    expect.element_to_be_clickable(
                        (By.XPATH, '//button[contains(text(),"Answer")]')
                    )
                )
                break
            except NoSuchElementException:
                if x >= len(sections)-1:
                    print('no questions in this practice with free respnse')
                    raise Exception
                sections_new = self.student.find_all(
                    By.XPATH, '//span[contains(@class,"breadcrumbs")]')
                sections_new[x].click()

        # t1.55.05 --> The text box disappears and the multiple choice answer
        # appear
        answer_text = 'undefined'
        self.student.find(
            By.XPATH,
            '//div[@class="free-response" and contains(text(),"' +
            answer_text + '")]')
        mc_answer = self.student.find(
            By.XPATH, '//div[@class="answer-letter"]')

        # t1.55.06 --> The 'Submit' button can now be clicked
        self.student.driver.execute_script(
            'return arguments[0].scrollIntoView();', mc_answer)
        self.student.driver.execute_script('window.scrollBy(0, -150);')
        mc_answer.click()
        submit_btn = self.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contains(text(),"Submit")]')
            )
        )

        # t1.55.07 --> The answer is submitted and the 'Next Question' button
        # appears
        submit_btn.click()
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(text(),"Next Question")]')
            )
        )

        # t1.55.08 -->The answer is submitted, the correct answer is displayed,
        # and feedback on the answer is given
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"question-feedback")]')
            )
        )

        # t1.55.09 --> The correctness for the completed question is visible in
        # the breadcrumb
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//span[contains(@class,"breadcrumbs")]' +
                 '//i[contains(@class,"correct") or ' +
                 'contains(@class,"incorrect")]')
            )
        )

        # t1.55.10 --> Each question's identification number and version are
        # visible
        text = self.student.find(
            By.XPATH,
            '//span[@class="exercise-identifier-link"]').text

        assert("ID#" in text), "ID# not displayed"
        assert("@" in text), "version not displayed"

        # t1.55.13 --> End of practice shows the number of assessments answered
        sections_new = self.student.find_all(
            By.XPATH, '//span[contains(@class,"breadcrumbs")]')
        sections_new[0].click()
        for _ in range(len(sections_new) - 1):
            try:
                # if the question is two part must answer free response first
                element = self.student.find(
                    By.TAG_NAME, 'textarea')
                answer_text = "hello"
                for i in answer_text:
                    element.send_keys(i)
                self.wait.until(
                    expect.visibility_of_element_located(
                        (By.XPATH, '//button[contains(text(),"Answer")]')
                    )
                ).click()
            except:
                mc_answer = self.student.find(
                    By.XPATH, '//div[@class="answer-letter"]')
                self.student.driver.execute_script(
                    'return arguments[0].scrollIntoView();', mc_answer)
                self.student.driver.execute_script('window.scrollBy(0, -150);')
                mc_answer.click()
                try:
                    self.wait.until(
                        expect.visibility_of_element_located(
                            (By.XPATH, '//button[contains(text(),"Submit")]')
                        )
                    ).click()
                except:
                    self.wait.until(
                        expect.visibility_of_element_located(
                            (By.XPATH,
                             '//button[contains(text(),"Next Question")]')
                        )
                    ).click()
            # answer the free response portion

        # ^ THIS FOR LOOP WAS TAKEN FROM T1.55.14

        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[contains(@class,"breadcrumb-end")]')
            )
        ).click()
        text = self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"completed-message")]/h3')
            )
        ).text

        print(text)

        q_answered = text.lstrip("You have answered "). \
            rstrip(" questions.").split(" of ")
        # assert (str(stop_point) in q_answered[0]), "error"
        assert (str(len(sections) - 1) in q_answered[1]), "error"

        # t1.55.14 --> The user is returned to the dashboard

        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[contains(text(),"Back to Dashboard")]')
            )
        ).click()
        self.wait.until(
            expect.visibility_of_element_located(
                (By.CLASS_NAME, 'student-dashboard ')
            )
        ).click()
