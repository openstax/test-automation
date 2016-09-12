"""Concept Coach v1, Epic 9 - Student Progress Views."""

import inspect
import json
import os
import pytest
import unittest

from autochomsky import chomsky
from pastasauce import PastaSauce, PastaDecorator
from random import randint
from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as expect
from staxing.assignment import Assignment

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Student

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': '50.0',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([
        7732, 7733, 7735, 7737  # 7736,
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestStudentProgressViews(unittest.TestCase):
    """CC1.09 - Student Progress Views."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.student = Student(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        self.student.username = os.getenv('STUDENT_USER_CC')
        self.student.login()
        self.student.sleep(5)  # for CNX redirect

    def tearDown(self):
        """Test destructor."""
        self.ps.update_job(
            job_id=str(self.student.driver.session_id),
            **self.ps.test_updates
        )
        try:
            self.student.delete()
        except:
            pass

    # Case C7732 - 001 - Student | View section completion report
    @pytest.mark.skipif(str(7732) not in TESTS, reason='Excluded')
    def test_student_view_section_completion_report_7732(self):
        """View section completion report.

        Steps:
        Go to Tutor
        Click on the 'Login' button
        Enter the student user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a CC course name
        Click on "Contents"
        Select a section
        Scroll to bottom of the section
        Click "Launch Concept Coach"
        Enter a response into the free response text box
        Click "Answer"
        Select a multiple choice answer
        Click "Submit"
        Click "Next question"
        Continue answering questions

        Expected Result:
        The user is presented with section completion report
        that shows "You're done"
        """
        self.ps.test_updates['name'] = 'cc1.09.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.09',
            'cc1.09.001',
            '7732'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.sleep(5)
        self.student.find(By.XPATH, "//button[@class='toggle btn']").click()
        self.student.sleep(3)
        self.student.find(
            By.XPATH,
            "//div/ul/li[2]/ul/li[2]/div/span[@class='name-wrapper']" +
            "/a/span[@class='title']").click()
        self.student.sleep(1)
        self.student.find(
            By.XPATH, "//div[@class='jump-to-cc']/a[@class='btn']").click()
        self.student.sleep(1)
        self.student.find(
            By.XPATH, "//button[@class='btn btn-lg btn-primary']").click()

        self.student.sleep(5)
        page = self.student.driver.page_source

        # Work through Concept Coach
        while 'or review your work below.' not in page:
            action = False

            # Free response
            if self.student.find(
                    By.XPATH,
                    "//button[@class='async-button continue btn btn-primary']"
                    ).text == 'Answer':
                self.student.find(
                    By.XPATH,
                    "//textarea"
                ).send_keys('An answer for this textarea')
                self.student.find(
                    By.XPATH,
                    "//button[@class='async-button continue btn btn-primary']"
                ).click()
                self.student.sleep(3)
                action = True

            # Multiple Choice
            elif self.student.find(
                    By.XPATH,
                    "//button[@class='async-button continue btn btn-primary']"
                    ).text == 'Submit':
                answers = self.student.driver.find_elements(
                    By.CLASS_NAME,
                    'answer-letter'
                )
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

                self.student.find(
                    By.XPATH,
                    "//button[@class='async-button continue btn btn-primary']"
                ).click()
                self.student.sleep(3)
                self.student.find(
                    By.XPATH,
                    "//button[@class='async-button continue btn btn-primary']"
                ).click()
                action = True

            # Advance to next page
            if not action:
                self.student.find(
                    By.XPATH,
                    "//button[@class='async-button continue btn btn-primary']"
                ).click()
                self.student.sleep(3)

            self.student.sleep(2)
            page = self.student.driver.page_source
        self.student.sleep(5)

        self.ps.test_updates['passed'] = True

    # Case C7733 - 002 - Student | Completion report shows the section status
    # of started and completed modules
    @pytest.mark.skipif(str(7733) not in TESTS, reason='Excluded')
    def test_student_completion_report_shows_the_section_status_of_7733(self):
        """Completion report shows the section status.

        Steps:
        Click on "Contents"
        Select a section
        Scroll to bottom of the section
        Click "Launch Concept Coach"
        Enter a response into the free response text box
        Click "Answer"
        Select a multiple choice answer
        Click "Submit"
        Click "Next question"
        Continue answering questions

        Expected Result:
        The user is presented with the completion report, which shows the
        section status of completed modules
        """
        self.ps.test_updates['name'] = 'cc1.09.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.09',
            'cc1.09.002',
            '7733'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.find(By.CSS_SELECTOR, 'div.media-nav button').click()
        self.student.sleep(1)
        self.student.find(By.XPATH, '//a[span[text()="1.2"]]').click()
        self.student.sleep(1)
        self.student.find(By.CSS_SELECTOR, 'div.jump-to-cc a').click()
        self.student.sleep(0.5)
        self.student.find(
            By.CSS_SELECTOR,
            'div.concept-coach-launcher button'
        ).click()
        try:
            self.student.find(By.XPATH, '//button[text()="Continue"]').click()
        except:
            print('Two-step message not seen.')

        # Work through Concept Coach
        page = self.student.driver.page_source
        while 'or review your work below.' not in page:

            action = False

            # Free response
            try:
                self.student.find(By.TAG, 'textarea').send_keys(chomsky())
                self.student.find(By.CSS_SELECTOR, 'button.continue').click()
                self.student.sleep(0.3)
            except:
                pass
            try:
                answers = self.student.find_all(By.CSS_SELECTOR,
                                                'div.answer-letter')
                if not isinstance(answers, list):
                    answers.click()
                else:
                    answers[randint(0, len(answers) - 1)].click()
                self.student.sleep(0.2)
                self.student.find(By.CSS_SELECTOR, 'button.continue').click()
                self.student.sleep(0.3)
            except:
                pass
            if self.student.find(
                    By.XPATH,
                    "//button[@class='async-button continue btn btn-primary']"
                    ).text == 'Answer':
                self.student.find(
                    By.XPATH,
                    "//textarea"
                ).send_keys('An answer for this textarea')
                self.student.find(
                    By.XPATH,
                    "//button[@class='async-button continue btn btn-primary']"
                ).click()
                self.student.sleep(3)
                action = True

            # Multiple choice
            elif self.student.find(
                    By.XPATH,
                    "//button[@class='async-button continue btn btn-primary']"
                    ).text == 'Submit':
                answers = self.student.driver.find_elements(
                    By.CLASS_NAME,
                    'answer-letter'
                )
                self.student.sleep(0.8)
                rand = randint(0, len(answers) - 1)
                answer = chr(ord('a') + rand)
                Assignment.scroll_to(self.student.driver, answers[0])
                if answer == 'a':
                    self.student.driver.execute_script(
                        'window.scrollBy(0, -160);'
                    )
                elif answer == 'd':
                    self.student.driver.execute_script(
                        'window.scrollBy(0, 160);'
                    )
                answers[rand].click()

                self.student.find(
                    By.XPATH,
                    "//button[@class='async-button continue btn btn-primary']"
                ).click()
                self.student.sleep(3)
                self.student.find(
                    By.XPATH,
                    "//button[@class='async-button continue btn btn-primary']"
                ).click()
                action = True

            # Go to next page
            if not action:
                self.student.find(
                    By.XPATH,
                    "//button[@class='async-button continue btn btn-primary']"
                ).click()
                self.student.sleep(3)

            self.student.sleep(2)
            page = self.student.driver.page_source
        self.student.sleep(5)

        crumbs = len(self.student.driver.find_elements_by_xpath(
            "//i[@class='icon-lg icon-correct']"))
        crumbs += len(self.student.driver.find_elements_by_xpath(
            "//i[@class='icon-lg icon-incorrect']"))

        ids = len(
            self.student.driver.find_elements_by_xpath(
                "//div[@class='reactive reactive-loaded']/div[@class='exerci" +
                "se-wrapper']/div[@class='card-body openstax-multipart-exerc" +
                "ise-card']/div[@class='card-body task-step openstax-exerci" +
                "se-card']/div/span[@class='exercise-identifier-link']/span[2]"
            )
        )

        assert(crumbs == ids), \
            'IDs do not match number of answered questions'

        self.ps.test_updates['passed'] = True

    # Case C7735 - 003 - Student | Access the progress views at any point
    @pytest.mark.skipif(str(7735) not in TESTS, reason='Excluded')
    def test_student_access_the_progress_views_at_any_point_7735(self):
        """Able to access the progress views at any point.

        Steps:
        Click on "Contents"
        Select a section
        Scroll to bottom of the section
        Click "Launch Concept Coach"
        Click "My Progress" in the header

        Expected Result:
        The user is presented with the progress view
        """
        self.ps.test_updates['name'] = 'cc1.09.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.09',
            'cc1.09.003',
            '7735'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.find(By.CSS_SELECTOR, 'div.media-nav button').click()
        self.student.sleep(1)
        self.student.find(By.XPATH, '//a[span[text()="1.2"]]').click()
        self.student.sleep(1)
        self.student.find(By.CSS_SELECTOR, 'div.jump-to-cc a').click()
        self.student.sleep(0.5)
        self.student.find(
            By.CSS_SELECTOR,
            'div.concept-coach-launcher button'
        ).click()
        try:
            self.student.find(By.XPATH, '//button[text()="Continue"]').click()
        except:
            print('Two-step message not seen.')
        self.student.find(By.LINK_TEXT, 'My Progress').click()

        assert('progress' in self.student.current_url()), \
            'Not viewing the My Progress page'

        self.ps.test_updates['passed'] = True

    # Case C7736 - 004 - Student | Return to current position in an assignment
    '''@pytest.mark.skipif(str(7736) not in TESTS, reason='Excluded')
    def test_student_return_to_current_position_in_an_assignment_7736(self):
        """Return to current position in an assignment.

        Steps:
        Click on "Contents"
        Select a section
        Scroll to bottom of the section
        Click "Launch Concept Coach"
        Enter a response into the free response text box
        Click "Answer"
        Select a multiple choice answer
        Click "Submit"
        Click "Next question"
        Click "Close" in the right corner of the header
        Click "Launch Concept Coach"

        Expected Result:
        The user is presented with their current position in the assignment
        """
        self.ps.test_updates['name'] = 'cc1.09.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.09',
            'cc1.09.004',
            '7736'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
    '''

    # Case C7737 - 005 - Student | Able to review previous modules
    @pytest.mark.skipif(str(7737) not in TESTS, reason='Excluded')
    def test_student_able_to_review_previous_modules_7737(self):
        """Able to review previous modules.

        Steps:
        Click on "Contents"
        Select a section
        Scroll to bottom of the section
        Click "Launch Concept Coach"
        Click "My Progress" in the header
        Click on the desired module under the "Previous" section

        Expected Result:
        The user is presented with a previous module
        """
        self.ps.test_updates['name'] = 'cc1.09.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.09',
            'cc1.09.005',
            '7737'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.find(By.CSS_SELECTOR, 'div.media-nav button').click()
        self.student.sleep(1)
        self.student.find(By.XPATH, '//a[span[text()="1.2"]]').click()
        self.student.sleep(1)
        self.student.find(By.CSS_SELECTOR, 'div.jump-to-cc a').click()
        self.student.sleep(0.5)
        self.student.find(
            By.CSS_SELECTOR,
            'div.concept-coach-launcher button'
        ).click()
        try:
            self.student.find(By.XPATH, '//button[text()="Continue"]').click()
        except:
            print('Two-step message not seen.')
        first = self.student.find(
            By.XPATH, '//h3[@class="chapter-section-prefix"]').text
        self.student.find(By.LINK_TEXT, 'My Progress').click()

        assert('progress' in self.student.current_url()), \
            'Not viewing the My Progress page'

        self.student.sleep(3)
        self.student.find(By.XPATH, '//div[@data-section="1.1"]').click()
        self.student.sleep(0.5)
        second = self.student.find(
            By.XPATH, "//h3[@class='chapter-section-prefix']").text

        assert(first != second), 'Not at new section'

        self.ps.test_updates['passed'] = True
