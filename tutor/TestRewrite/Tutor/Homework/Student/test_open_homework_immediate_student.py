"""
Title: test_open_homework_immediate_feedback
User(s): student
Testrail ID: C148109

Jacob Diaz
7/26/17


Corresponding Case(s):
-t1.71 22 --> 24

Progress:
Pretty much done

Work to be done/Questions:
Needs to use the current_tutor_term helper function in
supplementary_functions.py
Set it up so that it can use that function without having to keep the function
in the same doc as I did below
Once you do that, you can delete the current_tutor_term() function (the
original is stored in supplementary_functions.py)

Also make sure that the code is running correctly (it should be)

Merge-able with any scripts? If so, which? :
Other work a homework scripts

"""

# import inspect
import json
import os
import pytest
import unittest
import datetime

from pastasauce import PastaSauce, PastaDecorator
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from staxing.assignment import Assignment
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from random import randint

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Student, Teacher

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
        2
    ])
)


def current_tutor_term(current_date):
    """
    Returns the current scholastic tutor term, which we can use in order to
    pick a course that's currently in session
    :param current_date:
    Today's date, in string format "mm/dd/year"
    :return:
        Current term:
        "Fall 2017" or "Summer 2018", for example
        Possible: Winter, Spring, Summer, Fall
    """
    month, day, year = [int(x) for x in current_date.split('/')]
    if month >= 1 and month <= 3:
        if month == 3 and day < 21 or month == 6 and day > 21:
            pass
        else:
            season = "Winter"

    if month >= 3 and month <= 6:
        if month == 3 and day < 21 or month == 6 and day > 21:
            pass
        else:
            season = "Spring"

    if month >= 6 and month <= 9:
        if month == 3 and day < 21 or month == 6 and day > 21:
            pass
        else:
            season = "Summer"

    if month >= 9 and month <= 12:
        if month == 9 and day < 21 or month == 12 and day > 21:
            pass
        else:
            season = "Fall"
    return season + ' ' + str(year)


@PastaDecorator.on_platforms(BROWSERS)
class TestWorkAHomework(unittest.TestCase):

    def setUp(self):
        """Pretest settings."""
        if not LOCAL_RUN:
            self.ps = PastaSauce()
            self.desired_capabilities['name'] = self.id()
            self.student = Student(
                use_env_vars=True,
                pasta_user=self.ps,
                capabilities=self.desired_capabilities
            )
            self.teacher = Teacher(
                existing_driver=self.student.driver,
                use_env_vars=True,
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
        self.wait = WebDriverWait(self.student.driver, Assignment.WAIT_TIME)

    def tearDown(self):
        """Test destructor."""
        if not LOCAL_RUN:
            self.ps.update_job(
                job_id=str(self.student.driver.session_id),
                **self.ps.test_updates
            )
        self.teacher = None
        try:
            self.student.delete()
        except:
            pass

    @pytest.mark.skipif(str(1) not in TESTS, reason='Excluded')
    def test_teacher_make_homework_immediate(self):
        """
        Go to https://tutor-qa.openstax.org/
        Login with student account
        If the user has more than one course, select a Tutor course

        Click on a homework assignment (with immediate feedback) on the list
        dashboard
        ***The user starts an open homework assignment (t1.71.22)***

        Enter a free response into the free response text box
        Click "Answer"
        Select a multiple choice answer
        Click "Submit"
        ***A multiple choice answer is submitted (t1.71.23)***
        ***Answer feedback is presented
        (t1.71.24)***

        Expected results:

        Corresponds to...
        t1.71 22 --> 24

        :return:
        """
        # go to course
        self.teacher.login()

        # t1.71 22 --> The user starts an open homework assignment

        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
        assignment_name = 'hw no.{0}: {1}'.format(
            str(randint(0, 100)),
            str(today)
        )

        # get course name and term
        course_title = "Physics"  # name of course or part of the name
        current_term = current_tutor_term(begin)

        open_course_xpath = '//div[contains(@data-title,"{0}") and ' \
            'contains(@data-term,"{1}")]//a'.format(
                course_title,
                current_term
            )

        # we do the above in order to ensure that the course is open right now
        target_course = self.teacher.find(By.XPATH, open_course_xpath)

        # for reference later as student
        course_number = target_course.get_attribute('data-course-id')
        target_course.click()
        # immediate feedback
        self.teacher.add_assignment(assignment='homework',
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'status': 'publish',
                                        'problems': {'ch1': 5},
                                        'feedback': 'immediate'
                                    })
        self.teacher.logout()

        self.student.login()
        self.wait.until(
            expect.element_to_be_clickable((
                By.XPATH,
                "//div[contains(@data-course-id,%s)]" % course_number
            ))
        ).click()

        assert (course_number in self.student.current_url()), \
            "Not at the desired course %s page!" % course_number

        homework = self.student.find(
            By.XPATH,
            '//a[contains(@aria-labelledby, "%s")]' % assignment_name
        )

        self.student.driver.execute_script(
            'return arguments[0].scrollIntoView();',
            homework
        )
        ActionChains(self.student.driver).move_to_element(homework).perform()
        homework.click()

        # make sure that we're at the HW

        # t1.71 24 --> Answer feedback is presented
        wait = WebDriverWait(self.student.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"question-stem")]')
            )
        )

        try:
            # if the question is two part must answer free response to get mc
            text_box = self.student.find(
                By.TAG_NAME, 'textarea')
            self.teacher.driver.execute_script(
                "arguments[0].scrollIntoView(true);",
                text_box
            )

            answer_text = "hello"
            for i in answer_text:
                text_box.send_keys(i)
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//button[contains(@class,"continue")]')
                )
            ).click()
        except:
            pass

        mc_choice = self.student.find(
            By.XPATH, '//div[@class="answer-letter"]')
        self.student.driver.execute_script(
            'return arguments[0].scrollIntoView();',
            mc_choice
        )

        self.student.driver.execute_script('window.scrollBy(0, -150);')
        mc_choice.click()
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"continue")]')
            )
        ).click()

        try:
            # this is looking for question feedback -- though not all questions
            # might have
            self.student.find(
                By.XPATH,
                '//div[contains(@class,"question-feedback-content")]'
            )

        except:
            correct_answer = self.student.find(
                By.XPATH,
                "//div[contains(@class,'disabled answer-correct')]"
            )
            print(correct_answer)

        # you should expect to see the answer feedback

        # t1.71 23 --> A multiple choice answer is submitted and
        # you can navigate to the next assessment
        self.student.find(
            By.XPATH, '//button[contains(text(),"Next")]')
        # should present option to navigate to next questions
