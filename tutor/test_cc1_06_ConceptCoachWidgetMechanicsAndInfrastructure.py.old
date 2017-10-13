"""Concept Coach v1, Epic 6.

Concept Coach Widget Mechanics and Infrastructure.
"""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
# from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
# from staxing.assignment import Assignment

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
        7748, 7749, 7750
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestConceptCoachWidgetMechanicsAndInfrastructure(unittest.TestCase):
    """CC1.06 - Concept Coach Widget Mechanics and Infrastructure."""

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
            self.student = Student(
                use_env_vars=True,
                pasta_user=self.ps,
                capabilities=self.desired_capabilities,
                existing_driver=self.teacher.driver
            )
        else:
            self.teacher = Teacher(
                use_env_vars=True
            )
            self.student = Student(
                use_env_vars=True,
                existing_driver=self.teacher.driver
            )

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

    # Case C7748 - 001 - Student | View a Concept Coach book and see the widget
    @pytest.mark.skipif(str(7748) not in TESTS, reason='Excluded')
    def test_student_view_a_cc_book_and_see_the_widget_7748(self):
        """View a Concept Coach book and see the widget.

        Steps:
        go to tutor-qa
        login as a student
        click on a concept coach book
        Click on the 'Contents +' button
        Click on the a chapter in the contents
        Click on a section other than the introduction
        Scroll down

        Expected Result:
        Concept Coach widget visible
        """
        self.ps.test_updates['name'] = 'cc1.06.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.06',
            'cc1.06.001',
            '7748'
        ]
        self.ps.test_updates['passed'] = False

        # login and go to cc course
        self.student.login()
        self.student.driver.find_element(
            By.XPATH, '//p[contains(text(),"OpenStax Concept Coach")]'
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//a[@class="go-now"]')
            )
        ).click()
        # go to section 1.1 then cc widget
        self.student.page.wait_for_page_load()
        self.student.driver.find_element(
            By.XPATH,
            '//button[@class="toggle btn"]//span[contains(text(),"Contents")]'
        ).click()
        self.student.sleep(0.5)
        self.student.driver.find_element(
            By.XPATH,
            '//span[@class="chapter-number" and text()="1.1"]'
        ).click()
        self.student.page.wait_for_page_load()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'Jump to Concept Coach')
            )
        ).click()
        self.student.driver.find_element(
            By.XPATH,
            '//div[@class="concept-coach-launcher"]'
        )
        self.student.delete()
        self.ps.test_updates['passed'] = True

    # Case C7749 - 002 - Teacher | View a Concept Coach book and see the widget
    @pytest.mark.skipif(str(7749) not in TESTS, reason='Excluded')
    def test_teacher_view_a_cc_book_and_see_the_widget_7749(self):
        """View a Concept Coach book and see the widget.

        Steps:
        Go to Tutor
        Login as a teacher
        Click on a concept coach book
        Click on 'Online Book' in the header
        Click on the 'Contents +' button
        Click on the a chapter in the contents
        Click on a section other than the introduction
        Scroll down

        Expected Result:
        Concept Coach widget visible
        """
        self.ps.test_updates['name'] = 'cc1.06.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.06',
            'cc1.06.002',
            '7749'
        ]
        self.ps.test_updates['passed'] = False

        # login and go to cc course
        self.teacher.login()
        self.teacher.driver.find_element(
            By.XPATH, '//p[contains(text(),"OpenStax Concept Coach")]'
        ).click()
        # open online book
        self.teacher.page.wait_for_page_load()
        self.teacher.driver.find_element(
            By.XPATH, '//a[contains(text(),"Online Book")]'
        ).click()
        window_with_book = self.teacher.driver.window_handles[1]
        self.teacher.driver.switch_to_window(window_with_book)
        assert('cnx' in self.teacher.current_url()), \
            'Not viewing the textbook PDF'
        # go to section 1.1 then cc widget
        self.teacher.page.wait_for_page_load()
        self.teacher.driver.find_element(
            By.XPATH,
            '//button[@class="toggle btn"]//span[contains(text(),"Contents")]'
        ).click()
        self.teacher.sleep(0.5)
        self.teacher.driver.find_element(
            By.XPATH,
            '//span[@class="chapter-number" and text()="1.1"]'
        ).click()
        self.teacher.page.wait_for_page_load()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'Jump to Concept Coach')
            )
        ).click()
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[@class="concept-coach-launcher"]'
        )
        self.ps.test_updates['passed'] = True

    # Case C7750 - 003 - Student | Doesn't see end-of-page exercise sections
    @pytest.mark.skipif(str(7750) not in TESTS, reason='Excluded')
    def test_student_doesnt_see_end_of_page_exercise_sections_7750(self):
        """Doesn't see end-of-page exercise sections.

        Steps:
        Go to Tutor
        Login as a student
        Click on a concept coach book
        Click on the 'Contents +' button
        Click on the a chapter in the contents
        Click on a section other than the introduction
        Scroll down

        Expected Result:
        End-of-page exercise sections are not displayed.
        """
        self.ps.test_updates['name'] = 'cc1.06.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.06',
            'cc1.06.003',
            '7750'
        ]
        self.ps.test_updates['passed'] = False

        # login and go to cc course
        self.student.login()
        self.student.driver.find_element(
            By.XPATH, '//p[contains(text(),"OpenStax Concept Coach")]'
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//a[@class="go-now"]')
            )
        ).click()
        # go to section 1.1 then cc widget
        self.student.page.wait_for_page_load()
        self.student.driver.find_element(
            By.XPATH,
            '//button[@class="toggle btn"]//span[contains(text(),"Contents")]'
        ).click()
        self.student.sleep(0.5)
        self.student.driver.find_element(
            By.XPATH,
            '//span[@class="chapter-number" and text()="1.1"]'
        ).click()
        self.student.page.wait_for_page_load()
        questions = self.student.driver.find_elements(
            By.XPATH,
            '//section[@data-depth="1" and not(@class)]' +
            '//div[@data-type="exercise"]'
        )
        assert(len(questions) == 0), "questions found at the end of chapter"
        self.student.delete()
        self.ps.test_updates['passed'] = True
