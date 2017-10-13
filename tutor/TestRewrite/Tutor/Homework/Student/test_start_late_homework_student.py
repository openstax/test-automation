"""
Title: Tutor Rewrite, Work a Late Homework.
User(s): student, teacher
C148108

Jacob Diaz
7/26/17


Corresponding Case(s):
t1.71.18 --> 21

Progress:
Pretty much done

Work to be done/Questions:

Setup the helper functions/methods:
-current_tutor_term()
-get_new_set_time()
-teacher_make_late_assignment()
So that we can call them without having to have them in-file


Merge-able with any scripts? If so, which? :

"""

# import inspect
import json
import os
import pytest
import unittest
import datetime

from pastasauce import PastaSauce, PastaDecorator
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from staxing.assignment import Assignment
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver import ActionChains
from datetime import date, timedelta


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
        1, 2
    ])
)


# NEW FUNCTIONS TO HELP#########
def current_tutor_term(target_date=None):
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
    if target_date is None:
        target_date = date.today().strftime('%m/%d/%Y')

    month, day, year = [int(x) for x in target_date.split('/')]
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


def get_new_set_time(seconds_added=60):
    """
    -Helper function used in order to create
    an assignment that will be due very soon (late assignmnet)

    -Should be a very easy process for most cases, but deals with all the
    difficulties for you
    -The new time computed is calculated from the local time

    Uses datetime.datetime

    :param seconds_added: number of seconds from
    now that you want the due date of the assignment to be
    :return:
    string of format HHMMpm/am which you can enter directly into the due time
    textbox in order to set the due time
    """
    # get current time and time at which to make it due
    time_now = datetime.now()
    time_now = time_now + timedelta(seconds=seconds_added)
    time_string = str(time_now.hour) + str(time_now.minute)

    time_structure = datetime.strptime(time_string, "%H%M")
    # time_structure is a datetime.datetime object

    time_string_reform = time_structure.strftime("%I%M%p")
    # ^ set_time comes in format "HH MM am/pm"

    return time_string_reform


################

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

    def teacher_make_late_assignment(self, assignment_type="homework",
                                     course_title=None, course_no="394",
                                     assignment_name=None):
        """
        Expects that you're starting from the teacher dashboard

        Uses: datetime, time.strftime

        Makes a late assignment --> usually due within a very short
        period of time from when it was made

        :param hw_name: (str) --> name that we're gonna give the assignment
        :param assignment_type: (str) --> type of assignment we want to make
            (options: homework, reading, external, event)
        :param course_title: (str) --> identifier for the course
        :param
        :return:
        """
        # Navigate to course

        if course_title is None:  # if no specific course has been specified
            open_course_xpath = "//div[contains(@data-course-id,%s)]" % \
                course_no

        else:
            current_term = current_tutor_term()
            course_title = course_title.lower()
            open_course_xpath = '//div[contains(@data-appearance,"{0}") and ' \
                'contains(@data-term,"{1}")]//a'.format(
                    course_title,
                    current_term
                )

        # we do the above in order to ensure that the course is open right now
        target_course = self.teacher.find(By.XPATH, open_course_xpath)

        # for reference later as student
        course_number = target_course.get_attribute('data-course-id')
        print(course_number)
        target_course.click()

        #
        today_date = date.today()
        begin = (today_date + timedelta(days=0)).strftime('%m/%d/%Y')
        # begin and end dates will be the same

        if assignment_type.lower() == 'reading':
            heading = 'Read'

        if assignment_type.lower() == 'homework':
            heading = 'HW'

        if assignment_type.lower() == 'external':
            heading = 'Ext'

        if assignment_type.lower() == 'event':
            heading = 'Event'

        if assignment_name is None:
            assignment_name = '{0} no.{1}: {2}'.format(
                heading,
                str(randint(0, 100)),
                str(today_date)
            )

        # create assignment
        new_due_time = get_new_set_time(60)

        begin_tuple = (begin, "1201am")
        end_tuple = (begin, new_due_time)
        # PROBLEM --> for some reason, the begin tuples are correct and give
        # today's date
        # but during the add assignment page, the begin date is set as tomorrow

        self.teacher.add_assignment(
            assignment=assignment_type,
            args={
                'title': assignment_name,
                'description': 'description',
                'periods': {'all': (begin_tuple, end_tuple)},
                'status': 'publish',
                'problems': {'ch1': 5},
                'feedback': 'non-immediate'
            })

    @pytest.mark.skipif(str(2) not in TESTS, reason='Excluded')
    def test_late_homework(self):
        """
        Go to https://tutor-qa.openstax.org/
        Login with student account
        If the user has more than one course, select a Tutor course

        Click on the "All Past Work" tab on the dashboard
        Click on a homework assignment
        Expected Result
        ***The user starts a late homework assignment (t1.71.18)***

        Enter a free response into the free response text box
        Click "Answer"
        Select a multiple choice answer
        Click "Submit"
        *** A multiple choice answer is submitted (t1.71.19)***
        *** answer feedback is presented (t1.71.20) ***
        *** Correctness for a completed assessment is displayed in the
        breadcrumbs (t1.71.21)***

        Corresponds to...
        t1.71.18 --> 21
        """
        self.teacher.login()

        course_number = str(160)
        self.teacher_make_late_assignment(assignment_type='homework',
                                          course_no=course_number)

        self.teacher.logout()

        # THE STUDENT PART -->
        self.student.login()

        # t1.71.18 --> The user starts a late homework assignment

        try:
            late_icon = self.student.find(By.XPATH,
                                          "//i[contains(@class,'info late')]")
            late_icon.click()  # should direct you to homework

        except:
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//a[contains(text(),"All Past Work")]')
                )
            ).click()
            homework = self.student.driver.find_element(
                By.XPATH,
                '//div[contains(@aria-hidden,"false")]' +
                '//div[contains(@class,"homework") and ' +
                'not(contains(@class,"deleted"))]' +
                '//span[contains(text(),"0/")]'
            )

            self.student.driver.execute_script(
                'return arguments[0].scrollIntoView();',
                homework
            )

            homework.click()

        # t1.71.20 --> A multiple choice answer is submitted and answer
        # feedback is presented
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

        # t1.71.21 --> Correctness for a completed assessment is displayed in
        # the breadcrumbs
        self.student.driver.find_element(
            By.XPATH,
            '//span[contains(@class,"breadcrumb")]' +
            '//i[contains(@class,"correct") or contains(@class,"incorrect")]'
        )

        # t1.71.19 --> A multiple choice answer is submitted
        self.student.driver.find_element(
            By.XPATH, '//button/span[contains(text(),"Next Question")]')
