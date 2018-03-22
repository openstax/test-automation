"""Tutor v2, Epic 12 - Create New Question and Assignment Types."""

import inspect
import json
import os
import pytest
import unittest
import datetime

from pastasauce import PastaSauce, PastaDecorator
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
# from staxing.assignment import Assignment
from selenium.common.exceptions import NoSuchElementException

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Teacher, Student

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
        14739, 14741, 14743, 14744
        # not implemented
        # 14742
    ])
)
# 14743, 14744 - rely on add hw helpwer which has bugs
# 14742 - tessting out of date feature?


@PastaDecorator.on_platforms(BROWSERS)
class TestCreateNewQuestionAndAssignmentTypes(unittest.TestCase):
    """T2.12 - Create New Question and Assignment Types."""

    def setUp(self):
        """Pretest settings."""

        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.teacher = Teacher(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        self.student = Student(
            use_env_vars=True,
            existing_driver=self.teacher.driver,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )

    def tearDown(self):
        """Test destructor."""
        if not LOCAL_RUN:
            self.ps.update_job(
                job_id=str(self.teacher.driver.session_id),
                **self.ps.test_updates
            )
        self.student = None
        try:
            self.teacher.delete()
        except:
            pass

    # 14739 - 001 - Teacher | Vocabulary question is a question type
    @pytest.mark.skipif(str(14739) not in TESTS, reason='Excluded')
    def test_teacher_vocabulary_question_is_a_question_type_14739(self):
        """Vocabulary question is a question type.

        Steps:
        Go to Tutor
        Click on the 'Login' button
        Enter the teacher account in the username and password text boxes
        Click on the 'Sign in' button
        Click "Write a new exercise"
        Click "New Vocabulary Term"

        Expected Result:
        The user is presented with a page where a new vocabulary question can
        be created
        """
        self.ps.test_updates['name'] = 't2.12.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t2', 't2.12', 't2.12.001', '14739']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.get("https://exercises-qa.openstax.org/")
        # login
        self.teacher.find(
            By.XPATH, '//div[@id="account-bar-content"]//a[text()="Sign in"]'
        ).click()
        self.teacher.page.wait_for_page_load()
        self.teacher.find(
            By.ID, 'auth_key'
        ).send_keys(self.teacher.username)
        self.teacher.find(
            By.ID, 'password'
        ).send_keys(self.teacher.password)
        self.teacher.find(
            By.XPATH, '//button[text()="Sign in"]'
        ).click()
        # create new vocab
        self.teacher.page.wait_for_page_load()
        self.teacher.find(
            By.XPATH, '//a[@href="/exercises/new"]'
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[text()="New Vocabulary Term"]')
            )
        ).click()
        assert('/vocabulary/new' in self.teacher.current_url()), \
            'not at new vocab page'

        self.ps.test_updates['passed'] = True

    # 14741 - 002 - Teacher | True/False is a question type
    @pytest.mark.skipif(str(14741) not in TESTS, reason='Excluded')
    def test_teacher_truefalse_is_a_question_type_14741(self):
        """True/False is a question type.

        Steps:
        Click "Write a new exercise"
        Click on the "True/False" radio button

        Expected Result:
        The user is presented with a page where a True/False question can be
        created
        """
        self.ps.test_updates['name'] = 't2.12.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t2', 't2.12', 't2.12.002', '14741']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.get("https://exercises-qa.openstax.org/")
        # login
        self.teacher.find(
            By.XPATH, '//div[@id="account-bar-content"]//a[text()="Sign in"]'
        ).click()
        self.teacher.page.wait_for_page_load()
        self.teacher.find(
            By.ID, 'auth_key'
        ).send_keys(self.teacher.username)
        self.teacher.find(
            By.ID, 'password'
        ).send_keys(self.teacher.password)
        self.teacher.find(
            By.XPATH, '//button[text()="Sign in"]'
        ).click()
        # create new vocab
        self.teacher.page.wait_for_page_load()
        self.teacher.find(
            By.XPATH, '//a[@href="/exercises/new"]'
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//input[@label="True/False"]')
            )
        ).click()
        self.teacher.find(
            By.XPATH, '//span[text()="True/False"]'
        )
        self.ps.test_updates['passed'] = True

    # possibly changed implementation on site
    # no info icon found
    # 14742 - 003 - System | Display embedded videos with attribution and link
    # back to author
    @pytest.mark.skipif(str(14742) not in TESTS, reason='Excluded')
    def test_system_display_embedded_videos_with_attribution_14742(self):
        """Display embedded videos with attribution and a link back to author.

        Steps:
        Go to Tutor
        Click Login
        Sign in as student01
        Click "HS AP Physics LG"
        Click on a homework assignment
        Click through it until you get to a video
        Click on the info icon on the video

        Expected Result:
        Attribution and links are displayed
        """
        self.ps.test_updates['name'] = 't2.12.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t2', 't2.12', 't2.12.003', '14742']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # NOT DONE
    # create hw helper still not working
    # but works for manually created assignemnt, add assignemnt commented out
    # 14743 - 004 - Teacher | Each part of a multi-part question counts as a
    # seperate problem when scored
    @pytest.mark.skipif(str(14743) not in TESTS, reason='Excluded')
    def test_teacher_each_part_of_a_multipart_question_counts_as_14743(self):
        """Multi-part questions count as seperate problems when scored.

        Steps:
        Go to Tutor
        Click on the 'Login' button
        Log in as teacher03
        Click "College Introduction to Sociology"
        Go to "Student Scores"
        Pick a homework that has multipart question
        Click "Review"

        Expected Result:
        There is a breadcrumb for each part of a multipart question
        """
        self.ps.test_updates['name'] = 't2.12.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t2', 't2.12', 't2.12.004', '14743']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        # create a hw with a multi part question, and gice it a randomized name
        # ID: 12061@6 is multi part
        self.teacher.login()
        self.teacher.find(
            By.XPATH,
            '//div[@data-appearance="intro_sociology"]' +
            '//a[not(contains(@href,"/cc-dashboard"))]'
        ).click()
        assignment_name = "homework-%s" % randint(100, 999)
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=100)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(
            assignment='homework',
            args={
                'title': assignment_name,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'problems': {'1.1': ['12024@10'], },
                'status': 'publish',
            }
        )
        self.teacher.open_user_menu()
        self.teacher.find(
            By.LINK_TEXT, 'Student Scores'
        ).click()
        self.teacher.page.wait_for_page_load()
        # can just click the first review because assignemnt just created
        # and should be the most recent one
        self.teacher.find(
            By.LINK_TEXT, 'Review'
        ).click()
        cards = self.teacher.find_all(
            By.XPATH, '//div[contains(@class,"card-body")]')
        questions = self.teacher.find_all(
            By.XPATH, '//div[contains(@class,"openstax-question")]')
        breadcrumbs = self.teacher.find_all(
            By.XPATH, '//span[contains(@class,"openstax-breadcrumb")]')
        assert(len(questions) == len(breadcrumbs)), \
            'breadcrumbs and questions not equal'
        assert(len(cards) < len(breadcrumbs)), \
            'multipart question card has multiple questions,' + \
            'not matching up with  breadcrumbs'

        self.ps.test_updates['passed'] = True

    # NOT DONE
    # same issue as above w/ add_homework helper
    # but works for manually created assignemnt
    # (add assignemnt gets commented out, manual assignemnt name added)
    # 14744 - 005 - Student | Each part of a multi-part question counts as a
    # seperate problem when scored
    @pytest.mark.skipif(str(14744) not in TESTS, reason='Excluded')
    def test_student_each_part_of_a_multipart_question_counts_as_14744(self):
        """Multi-part questions count as seperate problems when scored.

        Steps:
        Go to Tutor
        Click on the 'Login' button
        Log in as abarnes
        Click "College Introduction to Sociology"
        Click on a homework assignment
        Go through the questions

        Expected Result:
        There is a breadcrumb for each part in the multipart question and the
        progress/score is out of the total number of questions, rather than
        counting the multipart question as one question
        """
        self.ps.test_updates['name'] = 't2.12.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t2', 't2.12', 't2.12.005', '14744']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        # create a hw with a multi part question, and give it a randomized name
        # ID: 12252@5 is multi part
        self.teacher.login()
        self.teacher.find(
            By.XPATH,
            '//div[@data-appearance="intro_sociology"]' +
            '//a[not(contains(@href,"/cc-dashboard"))]'
        ).click()
        assignment_name = "homework-%s" % randint(100, 999)
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=100)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(
            assignment='homework',
            args={
                'title': assignment_name,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'problems': {'1.1': ['12024@10'], },
                'status': 'publish',
            }
        )
        self.teacher.logout()
        # assignemnt name put here for manual testing
        # assignment_name = 'hw w/ video and multi part question'
        # login as student and go to same class
        self.student.login()
        self.teacher.find(
            By.XPATH,
            '//div[@data-appearance="intro_sociology"]' +
            '//a[not(contains(@href,"/cc-dashboard"))]'
        ).click()
        self.student.page.wait_for_page_load()
        # go to assignment (find my assignemnt_name)
        self.student.find(
            By.XPATH,
            '//a[contains(@class,"homework workable")]' +
            '//span[text()="' + assignment_name + '"]'
        ).click()
        # go through all questions
        breadcrumbs = self.teacher.find_all(
            By.XPATH,
            '//span[contains(@class,"openstax-breadcrumb")' +
            ' and not(contains(@class,"intro"))' +
            ' and not(contains(@class,"personalized"))'
            ' and not(contains(@class,"end"))]')
        total_questions = 0
        found_multipart = False
        i = 0
        while i < len(breadcrumbs):
            breadcrumbs[i].click()
            try:
                self.student.find(
                    By.XPATH, '//span[text()="Multi-part question"]')
                found_multipart = True
                questions = self.teacher.find_all(
                    By.XPATH, '//div[contains(@class,"openstax-question")]')
                total_questions += len(questions)
                i += len(questions)
            except NoSuchElementException:
                i += 1
                questions = self.teacher.find_all(
                    By.XPATH, '//div[contains(@class,"openstax-question")]')
                total_questions += len(questions)
        # check that everything worked out
        assert(found_multipart), 'no multipart question found'
        assert(total_questions == len(breadcrumbs)), \
            'breadcrumbs and questions not equal'

        self.ps.test_updates['passed'] = True
