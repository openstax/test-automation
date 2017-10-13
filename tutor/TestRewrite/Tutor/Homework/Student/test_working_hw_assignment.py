"""
System: Exercises
User(s): Student
Title: Test Working HW Assignment
Testrail ID: C148107


Jacob Diaz
7/26/17

Corresponding Case(s):
Corresponds to t1.71 01 --> 15


Progress:
Almost done -- should run successfully for all the tests that were written

Work to be done/Questions:
Write code for t1.71.16
Run the script, update any places where it might not work

Merge-able with any scripts? If so, which? :


"""

import json
import os
import pytest
import unittest
import datetime

from pastasauce import PastaSauce, PastaDecorator
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
# from selenium.common.exceptions import NoSuchElementException
# from selenium.common.exceptions import ElementNotVisibleException
# from selenium.common.exceptions import WebDriverException
from staxing.assignment import Assignment
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Teacher
from staxing.helper import Student

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
        1
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestWorkAHomework(unittest.TestCase):
    """"""
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
            self.teacher = Teacher(
                existing_driver=self.student.driver,
                use_env_vars=True,
                pasta_user=self.ps,
                capabilities=self.desired_capabilities
            )
        else:
            self.student = Student(
                use_env_vars=True
            )
            self.teacher = Teacher(
                use_env_vars=True,
                existing_driver=self.student.driver
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
    def test_working_hw(self):
        '''
        Go to https://tutor-qa.openstax.org/
        Login with the account
        If the user has more than one course, select a Tutor course

        Click on a homework assignment on the list dashboard
        ***The user is presented with the first question of the homework
        assignment (t1.71.01)***

        Hover the cursor over the information icon in right corner of the
        footer
        ***The user is presented with the assignment description/instructions
        (t1.71.02)***

        [Navigate through the questions sequentially using the breadcrumbs
        until a free response question is found]
        Enter a free response into the free response text box
        ***The Answer button is activated
        (t1.71.04)***
        ***The user is presented with the next question when clicking the
        breadcrumb(t1.71.03)***

        Click on another breadcrumb to get to the next assessment
        Click back to the original assessment
        ***The free response on the original assessment is saved (t1.71.08)***

        Click 'Answer' (which should be activated)
        ***A free response answer is submitted and multiple choice is shown
        (t1.71.05)***

        Select a multiple choice answer
        ***The Submit button is activated
        (t1.71.06)***

        Click on the next breadcrumb to get to the next assessment
        Click back to the original assessment
        ***The multiple choice answer on the original assessment is saved
        (t1.71.09)***

        Click "Submit"
        ***A multiple choice answer is submitted (t1.71.07)***

        Click on the course name in the left corner of the header
        OR
        Click "Dashboard" in the user menu
        ***The user returns to dashboard and the assignment progress shows the
        number of questions answered (t1.71.10)***

        Click on the same homework assignment
        Change a multiple choice answer on an assessment
        ***The button in the lower left corner says "Saving" with a loading
        circle
        A multiple choice answer is changed on an assessment (t1.71.12)***

        Continue answering all assessments
        ***The user is presented with the completion report at the end of the
        assignment (t1.71.11,14)***
        ***A homework may have a Spaced Practice assessment toward the end
        (t1.71.16)***
        ***A homework may have a Personalized assessment toward the end
        (t1.71.17)***

        Click "Back To Dashboard"
        ***The user is returned to the dashboard (t1.71.13)***
        ***The user is returned to the dashboard and the completed homework
        shows X/X answered in the dashboard progress column (t1.71.15)***

        Expected Results:

        Corresponds to t1.71 01 --> 15
        :return:
        '''
        # t1.71.01 --> The user is presented with the first question of the
        # homework assignment
        self.teacher.login()

        target_course = self.teacher.find(
            By.XPATH,
            "//div[contains(@data-title,'College Physics with Courseware')"
            "and not(contains(@data-title,'Debshila'))]"
        )
        # for reference later as student
        course_number = target_course.get_attribute('data-course-id')
        target_course.click()

        # IMPORTANT -- get the course number of the course that you're in -->
        # this will let you identify the course later (in case there's any
        # similarly-named courses)
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
        # non-immediate feedback

        assignment_name = 'hw no.{0}: {1}'.format(str(randint(0, 100)),
                                                  str(today))
        self.wait.until(expect.visibility_of_element_located((
            By.XPATH, '//div[contains(@class,"calendar-header")]'))
        )
        self.teacher.add_assignment(assignment='homework',  # CHANGED THIS TOO
                                    args={
                                        'title': assignment_name,
                                        'description': 'description',
                                        'periods': {'all': (begin, end)},
                                        'status': 'publish',
                                        'problems': {'1.1': 5}
                                    })
        # check add_assignment() method for information on structuring of args
        # NOTE: exercises hard-coded to chapter 1.1 only --> might cause
        # problems
        self.wait.until(expect.visibility_of_element_located((
            By.XPATH, '//*[contains(@data-title,"%s")]' % assignment_name))
        )
        self.teacher.logout()
        assert('https://tutor-qa.openstax.org' in self.teacher.current_url()),\
            'NOT BACK AT TUTOR HOMEPAGE'

        self.student.login()

        self.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH,
                 "//div[contains(@data-course-id,%s)]" % course_number))
            ).click()

        assert(course_number in self.student.current_url()),\
            "Not at the desired course %s page!" % course_number

        homework = self.wait.until(
            expect.presence_of_element_located((
                By.XPATH,
                '//div[contains(text(),"%s")]' % assignment_name
            ))
        )
        self.student.driver.execute_script(
            'return arguments[0].scrollIntoView();',
            homework
        )

        self.student.driver.execute_script('window.scrollBy(0, -80);')
        homework.click()
        self.wait.until(
            expect.presence_of_element_located(
                (By.XPATH, '//div[contains(@class,"question-stem")]')
            )
        )
        assert('task' in self.student.current_url()),\
            "Not currently working %s!" % assignment_name

        # t1.71.02 --> The user is presented with the assignment
        # description/instructions
        self.student.driver.execute_script('window.scrollBy(0, -80);')
        icon = self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[contains(@class,"homework")]' +
                 '//button[contains(@class,"task-details")]')
            )
        )  # check that task-details icon is there

        ActionChains(self.student.driver).move_to_element(icon).perform()
        self.student.driver.find_element(
            By.XPATH, '//div[contains(@id,"task-details-popover")]')
        # when hovering over the icon, a popover should come up

        # t1.71.03 --> The user is presented with the next question when
        # clicking the breadcrumb
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[contains(@class,"openstax-breadcrumbs")]')
            )
        )

        sections = self.student.driver.find_elements(
            By.XPATH, '//span[contains(@class,"openstax-breadcrumbs")]')
        count = 0  # by default it starts at the first exercises

        sections[count+1].click()
        self.student.driver.find_element(
            By.XPATH, '//div[@data-question-number="%s"]' % str(count+2)
        )
        self.student.sleep(1)
        sections[count].click()

        # t1.71.04
        # sections is a list of all the breadcrumbs in the homework
        answer_text = 'hello'

        while(True):
            try:
                element = self.student.driver.find_element(
                    By.TAG_NAME, 'textarea')
                for i in answer_text:
                    element.send_keys(i)
                answer_btn = self.wait.until(
                    expect.element_to_be_clickable(
                        (By.XPATH, '//button[contains(@class,"btn-primary")]')
                    )
                )

                if answer_btn.get_attribute("disabled") is None:
                    # if the answer button is activated, then you can move on
                    break
            except:
                count += 1
                if count >= len(sections):
                    print('no questions in this homework with free response')
                    raise Exception
                sections[count].click()

        # t1.71.08 --> The free response on the original assessment is saved
        # currently this test might not always work
        if count == len(sections) - 1:
            increment = -1
        else:
            increment = 1

        # because of a bug that doesn't allow saving when navigating to review
        # questions
        ###
        print('count', count)
        sections[count+increment].click()
        self.student.sleep(1)
        sections[count].click()
        self.student.driver.find_element(
            By.XPATH, '//textarea[text()= "%s"]' % answer_text)

        # t1.71.05 --> A free response answer is submitted and multiple choice
        # is shown
        self.wait.until(
                    expect.element_to_be_clickable(
                        (By.XPATH, '//button[contains(@class,"btn-primary")]'))
        ).click()
        # this should answer the free response question

        # print('about to get multiple choice')

        # WHAT DO WE DO IF WE DON'T GET TO A FREE CHOICE QUESTION UNTIL WE'RE
        # AT THE LAST QUESTION?
        mc_choices = self.wait.until(expect.presence_of_all_elements_located(
            (By.XPATH, '//div[contains(@class,"answers-answer")]'))
        )

        # print('got list of all multiple choice')
        # gives list of all the possible multiple choice options
        answer_ind = 0  # we are by default picking the first option

        mc_choices[answer_ind].click()

        # gives list of all the possible multiple choice options
        print(mc_choices[answer_ind].get_attribute('class'))
        children = mc_choices[answer_ind].find_elements(By.XPATH, './/label')
        print(len(children))
        print(children[0].get_attribute('class'))

        # t1.71.09 --> The multiple choice answer on the original assessment is
        # saved check that multiple choice answer saved
        sections[count+increment].click()
        sections[count].click()
        mc_choices = self.wait.until(expect.presence_of_all_elements_located(
            (By.XPATH, '//div[contains(@class,"answers-answer")]'))
        )
        # mc_choices reassigned to get rid of stale elements
        curr_choice_status = mc_choices[answer_ind].get_attribute('class')
        assert('answer-checked' in curr_choice_status),\
            'Selected answer was not saved upon navigating breadcrumbs'
        # checking that the answer that we selected is registered as checked

        # t1.71.06 --> The Submit button is activated
        print('got here')
        self.student.driver.execute_script('window.scrollBy(0, -150);')
        submit_btn = self.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class,"continue btn")]')
            )
        )

        # t1.71.07 --> A multiple choice answer is submitted

        submit_btn.click()
        self.student.driver.find_element(
            By.XPATH, '//div[@data-question-number="%s"]' % str(count+2)
        )
        # next element will be two more than the offset index of the current
        # problem

        # t1.71.10 --> The user returns to dashboard and the assignment
        # progress shows the number of questions answered
        # WHERE IS THIS GONNA START? WILL IT START AFTER THE FIRST QUESTION?
        # VERIFY THAT ALL THE TESTS BEFORE THIS END ON THE FIRST QUESTION
        # DOES THIS TEST RUN ANY RISK OF OVERSHOOTING?
        # AS FOR T1.71.16, HOW DO YOU VERIFY THAT THE REVIEW QUESTIONS COMES

        stop_point = len(sections) // 2
        print('stop point', stop_point)
        sections[0].click()
        self.wait.until(
            expect.presence_of_element_located(
                (By.XPATH, '//div[contains(@class,"question-stem")]')
            )
        )

        for q in range(stop_point):
            try:
                # if the question is two part must answer free response to get
                # to mc
                element = self.student.driver.find_element(
                    By.TAG_NAME, 'textarea')
                answer_text = "hello"
                for i in answer_text:
                    element.send_keys(i)
                self.wait.until(
                    expect.visibility_of_element_located(
                        (By.XPATH, '//button[contains(@class,"continue btn")]')
                    )
                ).click()
            except:
                pass
            # answer the multiple choice portion
            self.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH, '//div[contains(@class,"question-stem")]')
                )
            )
            mc_answer = self.wait.until(expect.presence_of_element_located((
                By.XPATH, '//div[contains(@class,"answer-letter")]')))
            print('THis is the choice' + mc_answer.text)
            print('this section'+str(q))
            # self.student.driver.execute_script('window.scrollBy(0, 0);')
            # Assignment.scroll_to(self.student.driver, mc_answer)
            self.student.driver.execute_script(
                'return arguments[0].scrollIntoView();', mc_answer
            )

            mc_answer.click()
            # pass in the case that the answer is already selected

            self.wait.until(
                expect.element_to_be_clickable(
                    (By.XPATH, '//button[contains(@class,"continue btn")]')
                )
            ).click()  # click to submit

        # curr_question_num = int(self.student.find(
        # By.XPATH,"//div[contains(@class,'openstax-question')]"
        # ).get_attribute("data-question-number")
        #                         )
        # assert(curr_question_num == stop_point),Not
        # NOT SURE IF WE NEED THIS ASSERT POINT HERE --> asserts that current
        # question number is at the stop point

        curr_question_num = self.wait.until(expect.presence_of_element_located(
            (By.CSS_SELECTOR, '.openstax-question'))
        ).get_attribute('data-question-number')
        assert(str(stop_point+1) in curr_question_num),\
            'Not on the question after the designated stop point'

        self.wait.until(
            expect.presence_of_element_located(
                (By.XPATH, '//a[contains(@class,"course-name")]')
            )
        ).click()
        # brings you back to the class page

        # T1.71.11 --> The user is presented with the completion report at the
        # end of the assignment
        # Verify the assignment progress changed.
        # - this is supposed to answer all the questions
        # test that partial completion report does show on the course home
        locator = '//div[contains(text(),"%s")]/..//span' % assignment_name
        print('locator,' + locator)
        partial_complete = self.wait.until(expect.presence_of_element_located(
            (By.XPATH, locator)))
        assert("%s/%s" % (str(stop_point), str(len(sections) - 1)) in
               partial_complete.text), \
            "Partial completion report doesn't show"

        # NOTE: /.. designates the parent of an element
        homework = partial_complete.find_elements(By.XPATH, '/..')
        print(homework.get_attribute('class') + "HERE")
        self.student.driver.execute_script(
            'return arguments[0].scrollIntoView();', homework
        )
        self.student.driver.execute_script('window.scrollBy(0, -80);')
        homework.click()

        # click on the breadcrumb start from the beginning
        # this is so this test can be independent of the partial completion one
        sections = self.wait.until(expect.presence_of_all_elements_located((
            By.XPATH, '//span[contains(@class,"openstax-breadcrumbs")]'))
        )
        sections[0].click()

        for q in range(len(sections)):
            try:
                # if the question is two part must answer free response to get
                # to mc
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
            except:
                pass
            if 'end' in \
                    sections[q] \
                    .find_element(By.XPATH, '//i') \
                    .get_attribute('class'):
                pass
            # answer the multiple choice  portion
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//div[contains(@class,"question-stem")]')
                )
            )
            element = self.student.driver.find_element(
                By.XPATH, '//div[@class="answer-letter"]')
            self.student.driver.execute_script(
                'return arguments[0].scrollIntoView();',
                element
            )
            self.student.driver.execute_script('window.scrollBy(0, -150);')
            element.click()
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//button/span[contains(text(),"Submit")]')
                )
            ).click()

        self.student.driver.find_element(
            By.XPATH, '//div[contains(@class,"completed-message")]')
        self.student.driver.find_element(
            By.XPATH, '//h1[contains(text(),"You are done")]')

        # t1.71.12 --> The button in the lower left corner says "Saving" with a
        # loading circle and A multiple choice answer is changed on an
        # assessment (t1.71.12)***

        # this is expected to change a multiple choice question
        # that has already been answered
        self.student.driver.execute_script('window.scrollTo(0,0)')
        self.student.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"course-name")]'
        ).click()
        homework = self.student.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"homework") and ' +
            'not(contains(@class,"deleted"))]' +
            '//i[contains(@class,"icon-homework")]')
        self.student.driver.execute_script(
            'return arguments[0].scrollIntoView();',
            homework
        )
        self.student.driver.execute_script('window.scrollBy(0, -80);')
        homework.click()
        # reanswer mc portion
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"question-stem")]')
            )
        )
        element = self.student.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"answers-answer") and ' +
            'not(contains(@class,"checked"))]'
        )
        self.student.driver.execute_script(
            'return arguments[0].scrollIntoView();',
            element
        )

        self.student.driver.execute_script('window.scrollBy(0, -150);')
        element.click()
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button/span[contains(text(),"Submit")]')
            )
        ).click()

        # t1.71.14 -->The user is presented with the completion report at the
        # end of the assignment (same as t1.71.11)

        # Completed homework shows "You are done" in the completion report
        self.student.find(By.XPATH, "//div[@class='completed-message']")

        # t1.71.17 -->A homework may have a Personalized assessment toward the
        # end

        # FOR PERSONALIZED LOOK UNDER PERFORMANCE FORECAST --> WEAKEST SUBJECTS

        # T1.71.16 --> A homework may have a Spaced Practice assessment toward
        # the end

        # ACCOUNTS NEED MORE HISTORY FOR THESE --> MAYBE WORK THROUGH A COUPLE
        # ASSIGNMNETS FOR THESE
        # HOW CAN YOU MAKE SURE THAT THIS STARTS WHERE YOU LEFT OFF FROM AND
        # ANSWERS FULLY THROUGH?
        # MAYBE USE A WHILE LOOP?
        # HOW DO YOU CHECK FOR REVIEW ASSIGNMENT?

        # t1.71.13 --> The user is returned to the dashboard

        self.student.driver.find_element(
            By.XPATH, '//div[contains(@class,"completed-message")]')
        self.student.driver.find_element(
            By.XPATH, "//a[contains(text(),'Back to Dashboard')]").click()
        self.student.find(By.XPATH, "//div[contains(text(),'This Week')]")

        # t1.71.15 --> The user is returned to the dashboard and the completed
        # homework
        # shows X/X answered in the dashboard progress column (t1.71.15)

        self.student.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"homework") and ' +
            'not(contains(@class,"deleted"))]' +
            '//span[contains(text(),"%s/%s answered")]' %
            (len(sections) - 1, len(sections) - 1)
        )

if __name__ == '__main__':
    unittest.main(verbosity=2)
