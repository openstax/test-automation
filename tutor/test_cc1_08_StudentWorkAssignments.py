"""Concept Coach v1, Epic 08 - StudentsWorkAssignments."""

import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from staxing.assignment import Assignment
from staxing.helper import Teacher, Student

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': '48.0',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([7691, 7692, 7693, 7694, 7695,
         7696, 7697, 7698, 7699, 7700,
         7701, 7702, 7703])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestStudentsWorkAssignments(unittest.TestCase):
    """CC1.08 - Students Work Assignments."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        teacher = Teacher(username='teacher100', password='password',
                          site='https://tutor-qa.openstax.org/')
        teacher.login()
        courses = teacher.find_all(By.CLASS_NAME,
                                   'tutor-booksplash-course-item')
        assert(courses), 'No courses found.'
        if not isinstance(courses, list):
            courses = [courses]
        course_id = randint(0, len(courses) - 1)
        self.course = courses[course_id].get_attribute('data-title')
        teacher.select_course(title=self.course)
        teacher.goto_course_roster()
        section = '%s' % randint(100, 999)
        try:
            wait = teacher.wait_time
            teacher.change_wait_time(3)
            teacher.find(By.CLASS_NAME, '-no-periods-text')
            teacher.add_course_section(section)
        except:
            sections = teacher.find_all(
                By.XPATH,
                '//span[@class="tab-item-period-name"]'
            )
            section = sections[randint(0, len(sections) - 1)].text
        finally:
            teacher.change_wait_time(wait)
        self.code = teacher.get_enrollment_code(section)
        self.book_url = teacher.find(
            By.XPATH, '//a[span[text()="Online Book "]]'
        ).get_attribute('href')
        self.student = Student()
        self.first_name = Assignment.rword(6)
        self.last_name = Assignment.rword(8)
        self.email = self.first_name + '.' + self.last_name + \
            '@tutor.openstax.org'

    def tearDown(self):
        """Test destructor."""
        try:
            self.teacher.delete()
        except:
            pass
        try:
            self.student.delete()
        except:
            pass

    # Case C7691 - 002 - Student | Selects an exercise answer
    @pytest.mark.skipif(str(7691) not in TESTS, reason='Excluded')
    def test_select_an_exercise_answer(self):
        """Select an exercise answer."""
        self.student.get(self.book_url)
        self.student.sleep(2)
        self.student.find_all(By.XPATH, '//a[@class="nav next"]')[0].click()
        self.student.page.wait_for_page_load()
        try:
            widget = self.student.find(By.ID, 'coach-wrapper')
        except:
            self.student.find_all(By.XPATH,
                                  '//a[@class="nav next"]')[0].click()
            self.student.page.wait_for_page_load()
            try:
                self.student.sleep(1)
                widget = self.student.find(By.ID, 'coach-wrapper')
            except:
                self.student.find_all(By.XPATH,
                                      '//a[@class="nav next"]')[0].click()
                self.student.page.wait_for_page_load()
                self.student.sleep(1)
                widget = self.student.find(By.ID, 'coach-wrapper')
        Assignment.scroll_to(self.student.driver, widget)
        self.student.find(
            By.XPATH,
            '//button[contains(text(),"Launch Concept Coach")]'
        ).click()
        self.student.sleep(1.5)
        self.student.find(
            By.XPATH,
            '//input[contains(@label,"Enter the two-word enrollment code")]'
        ).send_keys(self.code)
        self.student.find(
            By.XPATH,
            '//div[contains(@class,"concept-coach")]' +
            '//button[contains(@class,"async-button")]'
        ).click()
        main_window = self.student.driver.window_handles[0]
        self.student.wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'click to begin login.')
            )
        ).click()
        accounts_window = self.student.driver.window_handles[1]
        self.student.sleep(3)
        self.student.driver.switch_to_window(accounts_window)
        self.student.sleep(2)
        print(main_window, accounts_window,
              self.student.driver.current_window_handle)
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'Sign up')
            )
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'signup_first_name')
            )
        ).send_keys(self.first_name)
        self.student.find(
            By.ID,
            'signup_last_name'
        ).send_keys(self.last_name)
        self.student.find(
            By.ID,
            'signup_email_address'
        ).send_keys(self.email)
        self.student.find(
            By.ID,
            'signup_username'
        ).send_keys(self.last_name)
        self.student.find(
            By.ID,
            'signup_password'
        ).send_keys(self.last_name)
        self.student.find(
            By.ID,
            'signup_password_confirmation'
        ).send_keys(self.last_name)
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'i_agree')
            )
        ).click()
        self.student.sleep(1)
        self.student.find(By.ID, 'agreement_submit').click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'i_agree')
            )
        ).click()
        self.student.sleep(1)
        self.student.find(By.ID, 'agreement_submit').click()
        self.student.driver.switch_to_window(main_window)
        self.student.find(
            By.XPATH,
            '//input[contains(@label,"Enter your school issued ID:")]'
        ).send_keys(self.last_name)
        self.student.find(
            By.XPATH,
            '//button[span[text()="Confirm"]]'
        ).click()
        self.student.sleep(5)
        self.student.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH,
                 '//div[@class="openstax-question"]//textarea')
            )
        ).send_keys(Assignment.rword(20))
        self.student.find(By.XPATH, '//button[span[text()="Answer"]]').click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '(//div[@class="answer-letter"])[1]')
            )
        ).click()
        self.student.find(By.XPATH, '//button[span[text()="Submit"]]').click()
