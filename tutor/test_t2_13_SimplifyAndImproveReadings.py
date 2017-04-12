"""Tutor v2, Epic 13 - Simplify and Improve Readings."""

import inspect
import json
import os
import pytest
import unittest
import datetime

from autochomsky import chomsky
from pastasauce import PastaSauce, PastaDecorator
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver import ActionChains
from staxing.assignment import Assignment

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
        14745, 14746, 85291, 100126, 100127,
        100128
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestSimplifyAndImproveReadings(unittest.TestCase):
    """T2.13 - Simplify and Improve Readings."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.teacher = Teacher(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        # create a reading for the student to work
        self.teacher.login()
        self.teacher.driver.execute_script("window.resizeTo(1920,1080)")
        self.teacher.select_course(appearance='ap_biology')
        self.assignment_name = 't1.18 reading-%s' % randint(100, 999)
        today = datetime.date.today()
        begin = today.strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=randint(1, 10))) \
            .strftime('%m/%d/%Y')
        self.teacher.add_assignment(
            assignment='reading',
            args={
                'title': self.assignment_name,
                'description': chomsky(),
                'periods': {'all': (begin, end)},
                'reading_list': ['1.1'],
                'status': 'publish',
            }
        )
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"calendar-container")]')
            )
        )
        self.teacher.logout()
        # login as a student to work the reading
        self.student = Student(
            existing_driver=self.teacher.driver,
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        self.student.login()
        self.student.select_course(appearance='ap_biology')
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'This Week')
            )
        )
        reading = self.student.driver.find_element(
            By.XPATH,
            '//div[text()="%s"]' % self.assignment_name
        )
        self.teacher.driver.execute_script(
            'return arguments[0].scrollIntoView();',
            reading
        )
        self.teacher.driver.execute_script('window.scrollBy(0, -80);')
        reading.click()
        self.student.driver.set_window_size(width=1300, height=1200)

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

    # 14745 - 001 - Student | Relative size and progress are displayed while
    # working a reading assignment
    @pytest.mark.skipif(str(14745) not in TESTS, reason='Excluded')
    def test_student_relative_size_and_progress_are_displayed_whil_14745(self):
        """Size and progress are displayed while working a reading.

        Steps:
        Go to Tutor
        Click on the 'Login' button
        Enter the student user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a Tutor course name
        Click on a reading assignment
        Click on the right arrow

        Expected Result:
        The progress bar at the top reflects how far along you are as you work
        through the reading assignment
        """
        self.ps.test_updates['name'] = 't2.13.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t2', 't2.13', 't2.13.001', '14745']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"progress-bar progress-bar-success")]')

        self.ps.test_updates['passed'] = True

    # 14746 - 002 - Student | Access prior milestones in the reading assignment
    # with breadcrumbs
    @pytest.mark.skipif(str(14746) not in TESTS, reason='Excluded')
    def test_student_access_prior_milestones_in_the_reading_assign_14746(self):
        """Access prior milestones in the reading assignment with breadcrumbs.

        Steps:
        If the user has more than one course, click on a Tutor course name
        Click on a reading assignment
        Click on the icon next to the calendar on the header

        Expected Result:
        The user is presented with prior milestones
        """
        self.ps.test_updates['name'] = 't2.13.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t2', 't2.13', 't2.13.002', '14746']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.find(By.CSS_SELECTOR, 'a.paging-control.next').click()
        self.student.sleep(1)
        self.student.find(By.CSS_SELECTOR, 'a.paging-control.next').click()
        self.student.sleep(1)
        self.student.find(By.CSS_SELECTOR, 'a.paging-control.next').click()
        self.student.sleep(1)
        self.student.find(By.CSS_SELECTOR, 'a.paging-control.next').click()
        self.student.sleep(5)
        self.student.driver.execute_script("window.scrollTo(0, 0);")
        element = self.student.find(
            By.XPATH, "//a[@class='milestones-toggle']")
        actions = ActionChains(self.student.driver)
        actions.move_to_element(element)
        actions.click()
        actions.perform()
        self.student.sleep(1)
        self.student.driver.execute_script("window.scrollTo(0, 0);")
        cards = self.student.find_all(
            By.XPATH,
            "//div[@class='milestone milestone-reading']"
        )
        # preview = ''
        if not isinstance(cards, list):
            # preview = cards.find_element(
            #    By.XPATH,
            #    "//div[@class='milestone milestone-reading']"
            # ).text
            cards.click()
        else:
            card = randint(0, len(cards))
            # preview = cards[card].find_element(
            #    By.XPATH,
            #    "//div[@class='milestone milestone-reading']"
            # ).text
            cards[card].click()

        string = "step/" + str(card + 1)

        assert(self.student.driver.current_url.find(string) >= 0), \
            'Something'

        self.ps.test_updates['passed'] = True

    # C85291 - 003 - Student | Reading Review card appears before the first
    # spaced practice question
    @pytest.mark.skipif(str(85291) not in TESTS, reason='Excluded')
    def test_student_reading_review_card_appears_before_first_spac_85291(self):
        """Reading Review card appears before first spaced practice question.

        Steps:
        Login as student
        Work the reading assignment
        After completing reading the sections you get a spaced practice problem

        Expected Result:
        The reading review card should appear before the first spaced practice
            question
        """
        self.ps.test_updates['name'] = 't2.08.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t2', 't2.08', 't2.08.003', '85291']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        while(1):
            while ('paging-control next' in self.student.driver.page_source and
                    'Concept Coach' not in self.student.driver.page_source and
                    'exercise-multiple-choice'
                    not in self.student.driver.page_source and
                    'textarea' not in self.student.driver.page_source):
                self.student.find(
                    By.XPATH,
                    "//a[@class='paging-control next']"
                ).click()

            # multiple choice case
            if('exercise-multiple-choice' in self.student.driver.page_source):

                answers = self.student.driver.find_elements(
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
                assert('question-feedback bottom' in page), \
                    'Did not submit MC'

                self.student.find(
                    By.XPATH,
                    "//button[@class='async-button continue btn btn-primary']"
                ).click()

            # free response case
            elif('textarea' in self.student.driver.page_source):
                self.student.find(
                    By.TAG_NAME, 'textarea').send_keys(
                    'An answer for this textarea')
                self.student.sleep(2)
                self.student.wait.until(
                    expect.element_to_be_clickable(
                        (By.XPATH, '//button[contains(@class,"async-button")' +
                            ' and contains(@class,"continue")]')
                    )
                ).click()

                self.student.wait.until(
                    expect.visibility_of_element_located(
                        (By.CLASS_NAME, 'exercise-multiple-choice')
                    )
                )

                self.student.sleep(2)

            # Reached Concept Coach card
            if('Spaced Practice' in self.student.driver.page_source and
                    'spaced-practice-intro'
                    in self.student.driver.page_source):
                self.student.sleep(5)
                break

            self.student.sleep(2)

        self.ps.test_updates['passed'] = True

    # C100126 - 004 - Student | Section number is seen at the beginning of each
    # new section in a reading assignment
    @pytest.mark.skipif(str(100126) not in TESTS, reason='Excluded')
    def test_student_section_number_is_seen_st_the_beginning_of_e_100126(self):
        """Section number seen at beginning of each new section in a reading.

        Steps:
        Login as a student
        Click on a tutor course
        Click on a reading assignment
        Continue to work through reading assignment

        Expected Result:
        At the start of each new section, the section number is displayed
        """
        self.ps.test_updates['name'] = 't2.08.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t2', 't2.08', 't2.08.004', '100126']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.find(By.XPATH, "//span[@class='section']")
        self.student.sleep(3)

        self.ps.test_updates['passed'] = True

    # C100127 - 005 - Teacher | Section numbers are listed at the top of each
    # section in reference view
    @pytest.mark.skipif(str(100127) not in TESTS, reason='Excluded')
    def test_student_section_numbers_listed_at_the_top_of_each_se_100127(self):
        """Section numbers listed at the top of each section in reference view.

        Steps:
        Login as teacher
        Click on a tutor course
        Click "Browse the Book" or select "Browse the Book" from the user menu
        Select a section from the contents

        Expected Result:
        Section number listed in header
        """
        self.ps.test_updates['name'] = 't2.08.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t2', 't2.08', 't2.08.005', '100127']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.logout()
        self.teacher.login()
        self.teacher.select_course(appearance='ap_biology')
        self.teacher.open_user_menu()
        self.teacher.find(By.LINK_TEXT, "Browse the Book").click()
        self.teacher.sleep(5)
        self.teacher.driver.switch_to_window(
            self.student.driver.window_handles[-1])
        self.teacher.find(
            By.XPATH, "//li[3]/ul[@class='section']/li/a").click()
        self.teacher.find(By.XPATH, "//span[@class='section']")
        self.teacher.sleep(3)

        self.ps.test_updates['passed'] = True

    # C100128 - 006 - Student | Section numbers are listed at the top of each
    # section in reference view
    @pytest.mark.skipif(str(100128) not in TESTS, reason='Excluded')
    def test_student_section_numbers_listed_at_the_top_of_each_se_100128(self):
        """Section numbers listed at the top of each section in reference view.

        Steps:
        Login as student
        Click on a tutor course
        Click "Browse the Book" or select "Browse the Book" from the user menu
        Select a section from the contents

        Expected Result:
        Section number listed in header
        """
        self.ps.test_updates['name'] = 't2.08.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t2', 't2.08', 't2.08.006', '100128']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.open_user_menu()
        self.student.find(By.LINK_TEXT, "Browse the Book").click()
        self.student.sleep(5)
        self.student.driver.switch_to_window(
            self.student.driver.window_handles[-1])
        self.student.find(
            By.XPATH, "//li[3]/ul[@class='section']/li/a").click()
        self.student.find(By.XPATH, "//span[@class='section']")
        self.student.sleep(3)

        self.ps.test_updates['passed'] = True
