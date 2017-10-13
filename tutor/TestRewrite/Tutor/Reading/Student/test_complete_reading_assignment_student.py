"""
System: exercises
Title: TEST COMPLETE READING ASSIGNMENT
User: STUDENT
Testrail ID: C148102


Jacob Diaz
7/26/17

Corresponding Case(s):
t1.28 01 —> 09, 14, 16 —> 20


Progress:
Not all written yet
Write and then test

Write the following:
t1.28.16,17
T2.13 03

Merge-able with any scripts? If so, which? :


Work to be done/Questions:
Test it for completion
Is it necessary to have method finish_reading_assignment()? -- would you wanna
I feel like it's useful to have to modularize the code and clean it up a bit

"""

# import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
from random import randint
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from staxing.assignment import Assignment
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys


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


@PastaDecorator.on_platforms(BROWSERS)
class TestWorkAReading(unittest.TestCase):

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
                use_env_vars=True,
                pasta_user=self.ps,
                existing_driver=self.student.driver,
                capabilities=self.desired_capabilities
            )
        else:
            self.student = Student(
                use_env_vars=True,
            )
            self.teacher = Teacher(
                existing_driver=self.student.driver,
                use_env_vars=True
            )
        self.wait = WebDriverWait(self.student.driver, Assignment.WAIT_TIME)

    def tearDown(self):
        """Test destructor."""
        if not LOCAL_RUN:
            self.ps.update_job(
                job_id=str(self.student.driver.session_id),
                **self.ps.test_updates
            )
        try:
            # Delete the assignment
            assert('calendar' in self.teacher.current_url()), \
                'Not viewing the calendar dashboard'

            spans = self.teacher.driver.find_elements_by_tag_name('span')
            for element in spans:
                if element.text.endswith('2016'):
                    month = element

            # Change the calendar date if necessary
            while (month.text != 'December 2016'):
                self.teacher.find(
                    By.XPATH,
                    "//a[@class = 'calendar-header-control next']").click()

            # Select the newly created assignment and delete it
            assignments = self.teacher.driver.find_elements_by_tag_name(
                'label')
            for assignment in assignments:
                if assignment.text == 'Epic 28':
                    assignment.click()
                    self.teacher.find(
                        By.XPATH,
                        "//a[@class='btn btn-default -edit-assignment']"
                    ).click()
                    self.teacher.find(
                        By.XPATH,
                        "//button[@class='async-button delete-link " +
                        "pull-right btn btn-default']").click()
                    self.teacher.find(
                        By.XPATH, "//button[@class='btn btn-primary']").click()
                    self.teacher.sleep(5)
                    break
        except:
            pass
        try:
            self.teacher.driver.refresh()
            self.teacher.sleep(5)

            self.teacher = None
            self.student.delete()
        except:
            pass

    # NOT CERTAIN IF FINISH_READING_ASSIGNMENT WORKS
    def finish_reading_assignment(self, assignment_identifier):
        """
        HELPER FUNCTION
        Arguments:
        -assignment_identifier : a string that will identify the assignment
        (can either be the whole name or portion the name)

        Will complete the assignment, so that we get to the completion report

        :param assignment_identifier: (string) name or identifier that we
        can use to find the assignment of interest on the student course
        dashboard
        """
        while (True):

            # this is for progressing through the actual reading itself
            while ('arrow right' in self.student.driver.page_source):
                self.student.find(By.XPATH, "//a[contains(@class,'arrow') " +
                                  "and contains(@class,'right')]").click()

            # come here if multiple choice question
            if ('exercise-multiple-choice' in self.student.driver.page_source):

                answers = self.student.find(
                    By.CLASS_NAME, 'answer-letter')
                self.student.sleep(0.8)
                rand = randint(0, len(answers) - 1)
                answer = chr(ord('a') + rand)
                Assignment.scroll_to(self.student.driver, answers[0])
                if answer == 'a':
                    self.student.driver.execute_script(
                        'window.scrollBy(0, -160);')
                elif answer == 'd':
                    self.student.driver.execute_script(
                        'window.scrollBy(0, 160);')
                answers[rand].click()

                self.student.wait.until(
                    expect.element_to_be_clickable(
                        (By.XPATH, '//button[contains(@class,"async-button")' +
                         ' and contains(@class,"continue")]')
                    )
                ).click()
                self.student.sleep(5)
                page = self.student.driver.page_source
                assert ('question-feedback bottom' in page), \
                    'Did not submit MC'

            # come here if free response question
            elif ('textarea' in self.student.driver.page_source):
                self.student.find(
                    By.TAG_NAME, 'textarea').send_keys(
                    'An answer for this textarea')
                self.student.sleep(1)
                self.student.wait.until(
                    expect.element_to_be_clickable(
                        (By.XPATH, '//button[contains(@class,"async-button")' +
                         ' and contains(@class,"continue")]')
                    )
                )

    @pytest.mark.skipif(str(1) not in TESTS, reason='Excluded')
    def test_make_reading_teacher(self):
        """This is to make a reading assignment for the student to work"""
        self.teacher.login()

        # Create a reading for the student to work
        self.teacher.select_course(appearance='physics')
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'add-assignment')
            )
        ).click()
        self.teacher.find(
            By.PARTIAL_LINK_TEXT, 'Add Reading').click()
        assert('readings/new' in self.teacher.current_url()), \
            'Not on the add a reading page'

        self.teacher.find(
            By.XPATH, "//input[@id = 'reading-title']").send_keys('Epic 28')
        self.teacher.find(
            By.XPATH, "//textarea[@class='form-control empty']").send_keys(
            "instructions go here")
        self.teacher.find(
            By.XPATH, "//input[@id = 'hide-periods-radio']").click()

        # Choose the first date calendar[0], second is calendar[1]
        # and set the open date to today
        self.teacher.driver.find_elements_by_xpath(
            "//div[@class = 'datepicker__input-container']")[0].click()
        self.teacher.driver.find_element_by_xpath(
            "//div[@class = 'datepicker__day datepicker__day--today']").click()

        # Choose the second date calendar[1], first is calendar[0]
        self.teacher.driver.find_elements_by_xpath(
            "//div[@class = 'datepicker__input-container']")[1].click()
        while(self.teacher.find(
                By.XPATH,
                "//span[@class = 'datepicker__current-month']"
        ).text != 'December 2016'):
            self.teacher.find(
                By.XPATH,
                "//a[@class = 'datepicker__navigation datepicker__" +
                "navigation--next']").click()

        # Choose the due date of December 31, 2016
        weekends = self.teacher.driver.find_elements_by_xpath(
            "//div[@class = 'datepicker__day datepicker__day--weekend']")
        for day in weekends:
            if day.text == '31':
                due = day
                due.click()
                break

        self.teacher.find(
            By.XPATH, "//button[@id='reading-select']").click()
        self.teacher.driver.find_elements_by_xpath(
            "//span[@class='chapter-checkbox']")[5].click()
        self.teacher.find(
            By.XPATH,
            "//button[@class='-show-problems btn btn-primary']").click()
        self.teacher.sleep(10)

        # Publish the assignment
        self.teacher.find(
            By.XPATH,
            "//button[@class='async-button -publish btn btn-primary']").click()
        # wait for it to publish
        self.teacher.sleep(20)

    # IN THE CASE THAT WE NEED TO MAKE A READING ASSIGNMENT THAT WE WANT TO
    # WORK (AND THAT
    # WE WON'T ALREADY HAVE ONE, WE MUST USE THE TEACHER MAKE READING SCRIPT
    # ABOVE )

    @pytest.mark.skipif(str(2) not in TESTS, reason='Excluded')
    def test_complete_reading_assignment_student(self):
        """
        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Login with student account that has an unopened reading assignment
        Click 'Next'
        Enter the student password [ password ] in the password text box
        Click on the 'Login' button
        If the user has more than one course, click on a Tutor course name
        Click on a reading assignment under the tab "This Week" on the
        dashboard
        ***the user is presented with the first page of the reading assignment
        (t1.28.01)***

        Hover over the calendar in the header
        ***The user is presented with the due date/time in a popup box
        (t1.28.02)***

        Click on the arrow on the right
        ***The user is presented with the next reading section (t1.28.03)***

        Click the "Continue" button
        On a card with a free response assessment, enter a free response into
        the free response assessment text box
        ***The "Answer" button is activated (t1.28.04)***

        Click the "Answer" button
        ***A free response answer is submitted and the multiple choice is
        presented to the user (t1.28.05)***

        Select a multiple choice answer
        ***The "Submit" button is activated (t1.28.06)***

        Click the "Submit" button in the left corner of the footer
        ***A multiple choice answer is submitted and feedback is presented
        (t1.28.07)***
        ***Answer feedback is presented to the user (t1.28.08)***
        ***Correctness for a completed assessment is displayed in the
        milestones (t1.28.09)***

        Keep navigating thru cards until you've found
        On a card with a video, click the play button
        ***The video should play (t1.28.14)***

        Continue to the end of the reading assignment
        ***The user may be presented with a Review assessment at the end of the
        reading assignment (t1.28.16)***
        ***A user may be presented with a personalized assessment at the end of
        the reading assignment (t1.28.17)***
        ***Once finished with the reading, the user is presented with the
        completion report that shows "You are done" (t1.28.19)***

        After you have completed reading the sections you get to the spaced
        practice problem
        ***The reading review card should appear before the first spaced
        practice question (t2.13.03)***

        At the end of the reading, click the "Back to Dashboard" button
        ***The user views the completion report and return to the dashboard
        (t1.28.18)***
        ***The reading is marked "Complete" in the dashboard progress column
        (t1.28.20)***

        Corresponds to...
        t1.28 01 —> 09, 14, 16 —> 20
        T2.13 003
        :return:
        """
        self.student.login()

        # t1.28.01 --> the user is presented with the first page of the reading
        # assignment
        # Test steps and verification assertions

        # self.student.select_course(appearance='physics') ### MAYBE USE THIS
        course_number = str(394)

        self.wait.until(
            expect.element_to_be_clickable((
                By.XPATH,
                "//div[contains(@data-course-id,%s)]" % course_number
            ))
        ).click()

        assignment_identifier = 'aaa'  # COME BACK TO EDIT THIS!
        # ^ should be some string designating the reading that you should be
        # working on

        reading = self.wait.until(expect.presence_of_element_located(
            (By.XPATH,
             "//a[contains(@aria-labelledby,'%s') and "
             "contains(@class,'reading')]" % assignment_identifier))
        )
        assert (course_number in self.student.current_url()), \
            'Not viewing the calendar dashboard'
        reading.click()

        name = self.student.find(By.CLASS_NAME, 'center-control-assignment')

        assert (assignment_identifier in name.text), \
            'Not viewing the reading'
        assert ('steps/1' in self.student.current_url()), \
            'Not on the first page of the reading'

        # t1.28.02 --> The user is presented with the due date/time in a popup
        # box
        reading_calendar = self.student.find(
            By.XPATH,
            "//button[contains(@class,'fa-calendar-o')]"
        )
        ActionChains(self.student.driver) \
            .move_to_element(reading_calendar) \
            .perform()

        due_date_tooltip = self.student.driver.find_element(
            By.XPATH,
            "//*[contains(@id,'tooltip')]"
        )
        due_text = due_date_tooltip.text

        assert('Due' in due_text), \
            "Due date tooltip not showing when hovering over calendar"

        past_url = self.student.driver.current_url
        # for comparison's sake later

        # t1.28.03 --> The user is presented with the next reading section
        ActionChains(self.student.driver).send_keys(Keys.ARROW_RIGHT)
        new_url = self.student.driver.current_url

        assert(past_url != new_url), \
            "Right arrow didn't navigate to new page"
        assert ('steps/2' in self.student.current_url()), \
            'Not on the second page of the reading'
        # NOT SURE WHETHER TO ASSUME THAT WE BEGIN ON THE FIRST PAGE

        answer_text = 'undefined'
        while(True):
            try:
                question = self.student.find(
                    By.XPATH,
                    "//textarea[contains(@aria-labelledby,'text box')]"
                )
                for i in answer_text:
                    question.send_keys(i)
                answer_btn = self.wait.until(
                    expect.element_to_be_clickable(
                        (By.XPATH, '//button[contains(@class,"continue")]')
                    )
                )

            except:
                # section_title = self.student.find(
                #     By.XPATH, "//textarea[contains(@class,'title')]")

                ActionChains(self.student.driver).send_keys(Keys.ARROW_RIGHT)
                # Navigate through the reading if you don't find a question

        # t1.28.04 -->  The "Answer" button is activated
        answer_btn.click()

        # t1.28.05 --> A free response answer is
        # submitted and the multiple choice is presented to the user
        mc_choice = self.student.find(
            By.XPATH, '//div[@class="answer-letter"]')
        self.student.driver.execute_script(
            'return arguments[0].scrollIntoView();',
            mc_choice
        )

        # t1.28.06 --> The "Submit" button is activated
        mc_choice.click()
        submit_btn = self.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class,'continue')]")
            )
        )

        # make sure that submit button can be clicked

        # t1.28.07 -->  multiple choice answer is
        # submitted and feedback is presented
        submit_btn.click()

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

        # t1.28.08 -->  Answer feedback is presented to the user
        # HOW IS THIS DIFFERENT FROM THE PREVIOUS TEST? (T1.28.07)

        # t1.28.09 --> Correctness for a completed
        # assessment is displayed in the milestones
        milestone_toggle = self.student.find(
            By.XPATH,
            "//a[contains(@class,'milestones')]"
        )
        milestone_toggle.click()

        self.student.find(
            By.XPATH,
            "//span[contains(@class,'openstax-breadcrumbs')"
            "and contains(@class,'correct')]"
        )
        milestone_toggle.click()

        # # t1.28.14 --> an embedded video should play when clicked
        # ### BEST WAY TO DEAL WITH THIS? SHOULD I JUST ALWAYS LOOK FOR AN
        # EMBEDDED VIDEO WHEN
        # ### COMPLETING THE OTHER TEST CASES? OR SHOULD I JUST DO THIS
        # SEPARATELY?
        #
        # # After readings are completed, will navigate through the reading
        # with the arrow keys
        # # will keep going until a video is found
        # while(True):
        #     try:
        #         video_play_btn = self.student.find(
        #             By.XPATH, "//button[contains(@class,'play-button')]")
        #         video_play_btn.click()
        #
        #     except:
        #         # section_title = self.student.find(
        #         #     By.XPATH, "//textarea[contains(@class,'title')]")
        #
        #         ActionChains(self.student.driver).send_keys(Keys.ARROW_RIGHT)
        #         # Navigate through the reading if you don't find a question
        #
        # self.wait.until(expect.presence_of_element_located(
        #         (By.XPATH,"//div[contains(@id,'playing-mode')]"
        #         )
        #     )
        # )
        # # if failed, then video didn't play upon clicking the play button

        # t1.28.16 -->The user may be presented with
        # a Review assessment at the end of the reading assignment
        # BY THIS DOES IT MEAN "SPACED PRACTICE"?

        # t1.28.17 -->A user may be presented with a personalized
        # assessment at the end of the reading assignment
        # HOW DO I DEAL WITH TEST CASES THAT MIGHT NOT TURN OUT TRUE?

        # t2.13.03 --> the reading review card should
        # appear before the first spaced practice question
        # WHAT'S READING REVIEW?

        # t1.28.19 --> Once finished with the reading, the
        # user is presented with the completion report
        # that shows "You are done"
        completed_message = self.student.find(
            By.XPATH,
            "//div[contains(@class,'completed-message')]"
        )
        completed_message.find_element(By.XPATH, "//h1")
        assert('You are done' in completed_message.text), \
            "Completion report doesn't say 'You are done'"

        # t1.28.18 --> The user views the completion
        # report and return to the dashboard
        dashboard_button = self.student.find(
            By.XPATH,
            "//a[contains(@class,'btn-primary')]"
        )
        dashboard_button.click()

        # t1.28.20 --> The reading is marked "Complete" in the dashboard
        # progress column
        self.wait.until(
            expect.presence_of_element_located(
                (By.XPATH, "//")
            )
        )
        reading = self.wait.until(
            expect.presence_of_element_located((
                By.XPATH,
                "//a[contains(@aria-labelledby,'%s') and " +
                "contains(@class,'reading')]" % assignment_identifier))
            )
        reading.find_element(
            By.XPATH,
            "//span[contains(text(),'Complete')]"
        )
