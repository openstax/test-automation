"""
System: Tutor
Title: view homework assignment from student scores
User(s): Teacher
Testrail ID: C148071


Jacob Diaz
7/28/17


Corresponding Case(s):
t1.23. 13,17,18,21,23,25


Progress:
Mostly written

Work to be done/Questions:
Keep testing, update where needed

Merge-able with any scripts? If so, which? :


"""
# import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
# from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from staxing.assignment import Assignment
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.common.exceptions import NoSuchElementException
# from selenium.common.exceptions import TimeoutException

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Teacher  # , Student

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
class TestViewClassScores(unittest.TestCase):
    """T1.23 - View Class Scores."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        if not LOCAL_RUN:
            self.teacher = Teacher(
                use_env_vars=True,
                pasta_user=self.ps,
                capabilities=self.desired_capabilities
            )
        else:
            self.teacher = Teacher(
                use_env_vars=True
            )

        self.wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME)

        self.teacher.login()

    def tearDown(self):
        """Test destructor."""
        if not LOCAL_RUN:
            self.ps.update_job(
                job_id=str(self.teacher.driver.session_id),
                **self.ps.test_updates
            )
        try:
            self.teacher.delete()
        except:
            pass

    @pytest.mark.skipif(str(1) not in TESTS, reason='Excluded')
    def test_homework_assignment_from_scores(self):
        '''
        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the teacher user account [ teacher01 | password ] in the username
        and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a Tutor course name

        Click on the "Student Scores" button
        Click on the tab for the chosen period
        Click on the "Review" button under the selected homework assignment.
        ***Displays students progress on chosen assignment for
        selected period, actual questions, and question results. (T1.23.13)***
        ***Period tabs are displayed. (t1.23.18)***
        ***Each question has a correct response displayed (t1.23.21)***
        ***Assessment pane shows interleaved class stats (t1.23.23)***
        ***Screen is moved down to selected section of homework. (t1.23.17)***


        Click "Back to Scores" button
        Click on score cell for chosen student and homework assignment (student
        must have started the hw)
        Click on a breadcrumb of selected section of homework.
        ***Teacher view of student work shown. Teacher can go through different
        questions with either the "Next Question"
        button, or breadcrumbs. Students answers are shown for questions they
        have worked. (t1.23.25)***

        Expected Results:

        Corresponds to...
        t1.23. 13,17,18,21,23,25
        '''
        # go to Student Scores
        # might have to change the course appearance
        self.teacher.select_course(appearance='college_physics')
        self.teacher.goto_student_scores()

        # self.teacher.find(
        #     By.LINK_TEXT, 'Student Scores').click()
        # self.teacher.wait.until(
        #     expect.visibility_of_element_located(
        #         (By.XPATH, '//span[contains(text(), "Student Scores")]')
        #     )
        # ).click()
        #  UNNECESSARY CODE COMMENTED? ^

        # (t1.23.13 --> Displays students progress on chosen assignment for
        # selected period, actual questions, and question results.

        # go to the Review Metrics of a HW by clicking 'Review'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[contains(@class, "tab-item-period-name")]')
            )
        ).click()

        bar = 0
        scroll_width = 1
        scroll_total_size = 1
        # scroll bar might not be there
        try:
            scroll_bar = self.teacher.find(
                By.XPATH,
                '//div[contains(@class,"ScrollbarLayout_faceHorizontal")]')
            scroll_width = scroll_bar.size['width']

            scroll_total_size = self.teacher.find(
                By.XPATH,
                '//div[contains(@class,"ScrollbarLayout_mainHorizontal")]'
            ).size['width']
            bar = scroll_width
        except:
            pass

        while (bar < scroll_total_size):
            try:
                self.teacher.find(
                    By.XPATH,
                    '//span[@class="review-link"]' +
                    '//a[contains(text(),"Review")]'
                ).click()
                assert ('metrics' in self.teacher.current_url()), \
                    'Not viewing homework assignment summary'
                break
            except:
                bar += scroll_width
                if scroll_total_size <= bar:
                    print("No HWs for this class :(")
                    raise Exception
                # drag scroll bar instead of scrolling
                actions = ActionChains(self.teacher.driver)
                actions.move_to_element(scroll_bar)
                actions.click_and_hold()
                actions.move_by_offset(scroll_width, 0)
                actions.release()
                actions.perform()

        # (t1.23.18) --> Period tabs are displayed.
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                    '//ul[contains(@role,"tablist")]' +
                    '//span[contains(@class,"tab-item-period-name")]')
            )
        )

        # (t1.23.21) --> Each question has a correct response displayed
        correct_answers = self.teacher.driver.find_elements(
            By.XPATH, '//div[contains(@class,"answer-correct")]')
        questions = self.teacher.driver.find_elements(
            By.XPATH, '//span[contains(@class,"openstax-breadcrumbs")]')
        assert (len(correct_answers) == len(questions)), \
            "number of correct answers not equal to the number of questions"

        # (t1.23.23) --> Assessment pane shows interleaved class stats
        # (t1.23.23)
        # PRETTY SURE T1.23.23 IS ALREADY COVERED

        # (t1.23.17) --> Screen is moved down to selected section of homework.
        # (t1.23.17)
        sections = self.teacher.driver.find_elements(
            By.XPATH, '//span[contains(@class,"breadcrumbs")]')
        sections[-1].click()
        self.teacher.sleep(2)
        assert(expect.visibility_of_element_located((
            By.XPATH,
            "//div[contains(@data-section,'%s')]" % str(len(sections) - 1))
        ))

        # (t1.23.25) --> Teacher view of student work shown. Teacher can go
        # through different
        # questions with either the "Next Question" button, or breadcrumbs.
        # Students answers are shown for questions they have worked. (t1.23.25)

        # GOT UP TO HERE ON TESTING! SUBSEQUENT CODE MIGHT NOT WORK

        # go back to student scores
        self.teacher.find(
            By.XPATH, '//span[contains(@title,"Menu")]').click()
        self.teacher.find(
            By.LINK_TEXT, 'Student Scores').click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[contains(text(), "Student Scores")]')
            )
        ).click()

        # look for a student that's worked a homework
        # click on their score to review the homework

        while (bar < scroll_total_size):
            try:
                self.teacher.find(
                    By.XPATH,
                    '//div[contains(@class,"score")]'
                    '//a[@data-assignment-type="homework"]'
                ).click()
                break

            # except (NoSuchElementException,
            #         ElementNotVisibleException,
            #         WebDriverException)

            except:
                bar += scroll_width
                if scroll_total_size <= bar:
                    print("No worked HWs for this class :(")
                    raise Exception
                # drag scroll bar instead of scrolling
                actions = ActionChains(self.teacher.driver)
                actions.move_to_element(scroll_bar)
                actions.click_and_hold()
                actions.move_by_offset(scroll_width, 0)
                actions.release()
                actions.perform()

        # make sure that we're reviewing the hw
        assert ('step' in self.teacher.current_url()), \
            'Not viewing student work for homework'

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[contains(@class,"breadcrumbs")]')
            )
        )
        sections = self.teacher.find_all(
            By.XPATH, '//span[contains(@class,"breadcrumbs")]')
        section = sections[-1]
        section.click()
        chapter = section.get_attribute("data-chapter")
        assert (self.teacher.driver.find_element(
            By.XPATH, '//span[contains(text(),"' +
                      chapter + '")]').is_displayed()), \
            'chapter not displayed'
