"""Concept Coach v2, Epic 18 - Guide, Monitor, Support, and Train Users."""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
# from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from staxing.assignment import Assignment
from selenium.common.exceptions import ElementNotVisibleException

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Teacher, Student

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': 'latest',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([
        58276, 58277, 58273, 58282, 58350,
        58286, 58290, 58291, 58292, 58320,
        58293, 58295, 58296, 14823, 14825,
        58275, 58311, 58274, 58283, 58351,
        58326, 58327, 58328, 58329, 58330,
        58331, 58333, 58334, 58335
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestGuideMonitorSupportAndTrainUsers(unittest.TestCase):
    """CC2.18 - Guide, Monitor, Support, and Train Users."""

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
        self.ps.update_job(
            job_id=str(self.teacher.driver.session_id),
            **self.ps.test_updates
        )
        try:
            self.teacher.delete()
        except:
            pass

    # 58276 - 001 - Teacher | Directed to a "No Courses" page when not in any
    # courses yet
    @pytest.mark.skipif(str(58276) not in TESTS, reason='Excluded')
    def test_teacher_directed_to_a_no_courses_page_when_not_in_any_58276(self):
        """Directed to a "No Courses" page when not in any courses yet.

        Steps:
        Go to Tutor
        Sign in as demo_teacher

        Expected Result:
        The message "We cannot find an OpenStax course associated with your
        account" displays with help links below
        """
        self.ps.test_updates['name'] = 'cc2.18.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.18', 'cc2.18.001', '58276']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login(username='demo_teacher')
        self.teacher.find(
            By.XPATH,
            '//p[contains(text(),' +
            '"cannot find an OpenStax course associated with your account")]')

        self.ps.test_updates['passed'] = True

    # 58277 - 002 - Teacher | View "Getting Started with Concept Coach" Guide
    @pytest.mark.skipif(str(58277) not in TESTS, reason='Excluded')
    def test_teacher_view_getting_started_with_concept_coach_guide_58277(self):
        """View "Getting Started with Concept Coach" Guide.

        Steps:
        Click on a Concept Coach course
        Click on Getting Started in the usermenu

        Expected Result:
        CC Help Center opens in another tab with the Getting Started guide
        """
        self.ps.test_updates['name'] = 'cc2.18.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.18', 'cc2.18.002', '58277']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.find(
            By.XPATH, '//a[contains(@href,"/cc-dashboard")]'
        ).click()
        self.teacher.open_user_menu()
        self.teacher.find(
            By.LINK_TEXT, 'Getting Started'
        ).click()
        self.teacher.find(
            By.XPATH, '//h3[text()="Getting Started"]'
        )
        self.ps.test_updates['passed'] = True

    # 58273 - 003 - Teacher | Access CC Help Center after registering for
    # a course
    @pytest.mark.skipif(str(58273) not in TESTS, reason='Excluded')
    def test_teacher_access_cc_help_center_after_registering_for_58273(self):
        """Access Concept Coach Help Center after registering for a course.

        Steps:
        Go to Tutor and sign in as teacher
        Click on a Concept Coach course if the user is in more than one
        Click "Get Help" from the user menu in the upper right corner of the
            screen

        Expected Result:
        The user is presented with the CC Help Center
        """
        self.ps.test_updates['name'] = 'cc2.18.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.18', 'cc2.18.003', '58273']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.find(
            By.XPATH, '//a[contains(@href,"/cc-dashboard")]'
        ).click()
        self.teacher.open_user_menu()
        self.teacher.find(
            By.LINK_TEXT, 'Get Help'
        ).click()
        window_with_help = self.teacher.driver.window_handles[1]
        self.teacher.driver.switch_to_window(window_with_help)
        self.teacher.find(
            By.XPATH, '//center[text()="Concept Coach Help Center"]'
        )

        self.ps.test_updates['passed'] = True

    # 58282 - 004 - Teacher | Submit a question
    @pytest.mark.skipif(str(58282) not in TESTS, reason='Excluded')
    def test_teacher_submit_a_question_58282(self):
        """Submit a question.

        Steps:
        Click "Get Help" from the user menu in the upper right corner of the
            screen
        Enter a question or search words into the search engine
        Click "Search" or press enter

        Expected Result:
        The user is presented with search results
        """
        self.ps.test_updates['name'] = 'cc2.18.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.18', 'cc2.18.004', '58282']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.find(
            By.XPATH, '//a[contains(@href,"/cc-dashboard")]'
        ).click()
        self.teacher.open_user_menu()
        self.teacher.find(
            By.LINK_TEXT, 'Get Help'
        ).click()
        window_with_help = self.teacher.driver.window_handles[1]
        self.teacher.driver.switch_to_window(window_with_help)
        self.teacher.find(By.ID, 'searchAskInput').send_keys('question')
        self.teacher.find(By.ID, 'searchAskButton').click()
        self.teacher.page.wait_for_page_load()
        self.teacher.find(By.ID, 'results')
        self.teacher.find(By.XPATH, '//div[@class="article "]')
        self.ps.test_updates['passed'] = True

    # 58350 - 005 - Teacher | View "Contact Us" button after submitting a
    # question
    @pytest.mark.skipif(str(58350) not in TESTS, reason='Excluded')
    def test_teacher_view_contact_us_button_after_submitting_quest_58350(self):
        """View "Contact Us" button after submitting a question.

        Steps:
        Click "Get Help" from the user menu in the upper right corner of the
            screen
        Enter a question or search words into the search engine
        Click "Search" or press enter
        Scroll to the bottom of the screen

        Expected Result:
        "Contact Us" button exists
        """
        self.ps.test_updates['name'] = 'cc2.18.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.18', 'cc2.18.005', '58350']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.find(
            By.XPATH, '//a[contains(@href,"/cc-dashboard")]'
        ).click()
        self.teacher.open_user_menu()
        self.teacher.find(
            By.LINK_TEXT, 'Get Help'
        ).click()
        window_with_help = self.teacher.driver.window_handles[1]
        self.teacher.driver.switch_to_window(window_with_help)
        self.teacher.find(By.ID, 'searchAskInput').send_keys('question')
        self.teacher.find(By.ID, 'searchAskButton').click()
        self.teacher.page.wait_for_page_load()
        self.teacher.find(By.XPATH, '//a[contains(text(),"Contact Us")]')
        self.ps.test_updates['passed'] = True

    # 58286 - 006 - Teacher | View an article after submitting a question
    @pytest.mark.skipif(str(58286) not in TESTS, reason='Excluded')
    def test_teacher_view_an_article_after_submitting_a_question_58286(self):
        """View an article after submitting a question.

        Steps:
        Click "Get Help" from the user menu in the upper right corner of the
            screen
        Enter a question or search words into the search engine
        Click "Search" or press enter
        Click on a search result

        Expected Result:
        The user is presented with an article containing answer to the question
        """
        self.ps.test_updates['name'] = 'cc2.18.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.18', 'cc2.18.006', '58286']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.find(
            By.XPATH, '//a[contains(@href,"/cc-dashboard")]'
        ).click()
        self.teacher.open_user_menu()
        self.teacher.find(
            By.LINK_TEXT, 'Get Help'
        ).click()
        window_with_help = self.teacher.driver.window_handles[1]
        self.teacher.driver.switch_to_window(window_with_help)
        self.teacher.find(By.ID, 'searchAskInput').send_keys('question')
        self.teacher.find(By.ID, 'searchAskButton').click()
        self.teacher.page.wait_for_page_load()
        self.teacher.find(By.XPATH, '//div[@class="article "]/a').click()
        self.teacher.find(By.ID, 'articleContainer')
        assert('articles' in self.teacher.current_url()), 'not at article'
        self.ps.test_updates['passed'] = True

    # 58290 - 007 - Teacher | Indicate that the article was helpful
    @pytest.mark.skipif(str(58290) not in TESTS, reason='Excluded')
    def test_teacher_indicate_that_the_article_was_helpful_58290(self):
        """Indicate that the article was helpful.

        Steps:
        Click "Get Help" from the user menu in the upper right corner of the
            screen
        Enter a question or search words into the search engine
        Click "Search" or press enter
        Click on a search result
        Scroll to "Feedback"
        Click "Yes"

        Expected Result:
        A message that says "Thanks for your feedback!" is displayed
        """
        self.ps.test_updates['name'] = 'cc2.18.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.18', 'cc2.18.007', '58290']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.find(
            By.XPATH, '//a[contains(@href,"/cc-dashboard")]'
        ).click()
        self.teacher.open_user_menu()
        self.teacher.find(
            By.LINK_TEXT, 'Get Help'
        ).click()
        window_with_help = self.teacher.driver.window_handles[1]
        self.teacher.driver.switch_to_window(window_with_help)
        self.teacher.find(By.ID, 'searchAskInput').send_keys('question')
        self.teacher.find(By.ID, 'searchAskButton').click()
        self.teacher.page.wait_for_page_load()
        self.teacher.find(By.XPATH, '//div[@class="article "]/a').click()
        assert('articles' in self.teacher.current_url()), 'not at article'
        self.teacher.find(
            By.XPATH, '//div[@id="feedback"]//input[@value="Yes"]'
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[text()="Thanks for your feedback!"]')
            )
        )
        self.ps.test_updates['passed'] = True

    # 58291 - 008 - Teacher | Negative feedback renders a feedback popup box
    @pytest.mark.skipif(str(58291) not in TESTS, reason='Excluded')
    def test_teacher_negative_feedback_renders_feedback_popup_box_58291(self):
        """Negative feedback renders a feedback popup box.

        Steps:
        Click "Get Help" from the user menu in the upper right corner of the
            screen
        Enter a question or search words into the search engine
        Click "Search" or press enter
        Click on a search result
        Scroll to "Feedback"
        Click "No"

        Expected Result:
        The user is presented with a popup box that allows them to input
        feedback
        """
        self.ps.test_updates['name'] = 'cc2.18.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.18', 'cc2.18.008', '58291']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.find(
            By.XPATH, '//a[contains(@href,"/cc-dashboard")]'
        ).click()
        self.teacher.open_user_menu()
        self.teacher.find(
            By.LINK_TEXT, 'Get Help'
        ).click()
        window_with_help = self.teacher.driver.window_handles[1]
        self.teacher.driver.switch_to_window(window_with_help)
        self.teacher.find(By.ID, 'searchAskInput').send_keys('question')
        self.teacher.find(By.ID, 'searchAskButton').click()
        self.teacher.page.wait_for_page_load()
        self.teacher.find(By.XPATH, '//div[@class="article "]/a').click()
        assert('articles' in self.teacher.current_url()), 'not at article'
        self.teacher.find(
            By.XPATH, '//div[@id="feedback"]//input[@value="No"]'
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'feedbackDialog')
            )
        )
        self.ps.test_updates['passed'] = True

    # 58292 - 009 - Teacher | Submit feedback for an article
    @pytest.mark.skipif(str(58292) not in TESTS, reason='Excluded')
    def test_teacher_submit_feedback_for_an_article_58292(self):
        """Submit feedback for an article.

        Steps:
        Click "Get Help" from the user menu in the upper right corner of the
            screen
        Enter a question or search words into the search engine
        Click "Search" or press enter
        Click on a search result
        Scroll to "Feedback"
        Click "No"
        Enter feedback into the box that pops up
        Click "Submit"

        Expected Result:
        A message that says "Thanks for your feedback!" is displayed in the box
        """
        self.ps.test_updates['name'] = 'cc2.18.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.18', 'cc2.18.009', '58292']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.find(
            By.XPATH, '//a[contains(@href,"/cc-dashboard")]'
        ).click()
        self.teacher.open_user_menu()
        self.teacher.find(
            By.LINK_TEXT, 'Get Help'
        ).click()
        window_with_help = self.teacher.driver.window_handles[1]
        self.teacher.driver.switch_to_window(window_with_help)
        self.teacher.find(By.ID, 'searchAskInput').send_keys('question')
        self.teacher.find(By.ID, 'searchAskButton').click()
        self.teacher.page.wait_for_page_load()
        self.teacher.find(By.XPATH, '//div[@class="article "]/a').click()
        assert('articles' in self.teacher.current_url()), 'not at article'
        self.teacher.find(
            By.XPATH, '//div[@id="feedback"]//input[@value="No"]'
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'feedbackDialog')
            )
        )
        self.teacher.find(
            By.ID, 'feedbackTextArea'
        ).send_keys('qa automated test feedback')
        self.teacher.find(By.XPATH, '//input[@value="Submit"]').click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//p[text()="Thanks for your feedback!"]')
            )
        )
        self.ps.test_updates['passed'] = True

    # 58320 - 010 - Teacher | Close window after submitting feedback for an
    # article
    @pytest.mark.skipif(str(58320) not in TESTS, reason='Excluded')
    def test_teacher_close_window_after_submitting_feedback_for_58320(self):
        """Close window after submitting feedback for an article.

        Steps:
        Click "Get Help" from the user menu in the upper right corner of the
            screen
        Enter a question or search words into the search engine
        Click "Search" or press enter
        Click on a search result
        Scroll to "Feedback"
        Click "No"
        Enter feedback into the box that pops up
        Click "Submit"
        Click "Close window"

        Expected Result:
        The popup box closes and the message "Thanks for your feedback"
        displays beneath "Feedback"
        """
        self.ps.test_updates['name'] = 'cc2.18.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.18', 'cc2.18.010', '58320']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.find(
            By.XPATH, '//a[contains(@href,"/cc-dashboard")]'
        ).click()
        self.teacher.open_user_menu()
        self.teacher.find(
            By.LINK_TEXT, 'Get Help'
        ).click()
        window_with_help = self.teacher.driver.window_handles[1]
        self.teacher.driver.switch_to_window(window_with_help)
        self.teacher.find(By.ID, 'searchAskInput').send_keys('question')
        self.teacher.find(By.ID, 'searchAskButton').click()
        self.teacher.page.wait_for_page_load()
        self.teacher.find(By.XPATH, '//div[@class="article "]/a').click()
        assert('articles' in self.teacher.current_url()), 'not at article'
        self.teacher.find(
            By.XPATH, '//div[@id="feedback"]//input[@value="No"]'
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'feedbackDialog')
            )
        )
        self.teacher.find(
            By.ID, 'feedbackTextArea'
        ).send_keys('qa automated test feedback')
        self.teacher.find(By.XPATH, '//input[@value="Submit"]').click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[text()="close window"]')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[text()="Thanks for your feedback!"]')
            )
        )
        self.ps.test_updates['passed'] = True

    # 58293 - 011 - Teacher | Cancel feedback
    @pytest.mark.skipif(str(58293) not in TESTS, reason='Excluded')
    def test_teacher_cancel_feedback_before_making_changes_58293(self):
        """Cancel feedback.

        Steps:
        Click "Get Help" from the user menu in the upper right corner of the
            screen
        Enter a question or search words into the search engine
        Click "Search" or press enter
        Click on a search result
        Scroll to "Feedback"
        Click "No"
        [optional] Enter feedback into the text box
        Click "Cancel"

        Expected Result:
        The popup box closes
        """
        self.ps.test_updates['name'] = 'cc2.18.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.18', 'cc2.18.011', '58293']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.find(
            By.XPATH, '//a[contains(@href,"/cc-dashboard")]'
        ).click()
        self.teacher.open_user_menu()
        self.teacher.find(
            By.LINK_TEXT, 'Get Help'
        ).click()
        window_with_help = self.teacher.driver.window_handles[1]
        self.teacher.driver.switch_to_window(window_with_help)
        self.teacher.find(By.ID, 'searchAskInput').send_keys('question')
        self.teacher.find(By.ID, 'searchAskButton').click()
        self.teacher.page.wait_for_page_load()
        self.teacher.find(By.XPATH, '//div[@class="article "]/a').click()
        assert('articles' in self.teacher.current_url()), 'not at article'
        self.teacher.find(
            By.XPATH, '//div[@id="feedback"]//input[@value="No"]'
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'feedbackDialog')
            )
        )
        self.teacher.find(By.XPATH, '//input[@value="Cancel"]').click()
        with self.assertRaises(ElementNotVisibleException):
            self.teacher.find(
                By.ID, 'feedbackDialog').click()
        self.ps.test_updates['passed'] = True

    # 58295 - 012 - Teacher | View related articles
    @pytest.mark.skipif(str(58295) not in TESTS, reason='Excluded')
    def test_teacher_view_related_articles_58295(self):
        """View related articles.

        Steps:
        Click "Get Help" from the user menu in the upper right corner of the
            screen
        Enter a question or search words into the search engine
        Click "Search" or press enter
        Click on a search result
        Scroll to "Related Articles"

        Expected Result:
        The user is presented with a list of related articles
        """
        self.ps.test_updates['name'] = 'cc2.18.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.18', 'cc2.18.012', '58295']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.find(
            By.XPATH, '//a[contains(@href,"/cc-dashboard")]'
        ).click()
        self.teacher.open_user_menu()
        self.teacher.find(
            By.LINK_TEXT, 'Get Help'
        ).click()
        window_with_help = self.teacher.driver.window_handles[1]
        self.teacher.driver.switch_to_window(window_with_help)
        self.teacher.find(By.ID, 'searchAskInput').send_keys('question')
        self.teacher.find(By.ID, 'searchAskButton').click()
        self.teacher.page.wait_for_page_load()
        self.teacher.find(By.XPATH, '//div[@class="article "]/a').click()
        assert('articles' in self.teacher.current_url()), 'not at article'
        self.teacher.find(By.XPATH, '//h2[text()="Related Articles"]')

        self.ps.test_updates['passed'] = True

    # 58296 - 013 - Teacher | Submit a question to Customer Support
    @pytest.mark.skipif(str(58296) not in TESTS, reason='Excluded')
    def test_teacher_submit_a_question_to_customer_support_58296(self):
        """Submit a question to Customer Support.

        Steps:
        Click "Get Help" from the user menu in the upper right corner of the
            screen
        Enter a question or search words into the search engine
        CLick "Search" or press enter
        Click on a search result
        Scroll to the bottom of the page
        CLick "Contact Us"
        Fill out the required fields
        Enter "Submit"

        Expected Result:
        The message "Thank you for your message! We'll be back to you within
        one business day" is displayed
        """
        self.ps.test_updates['name'] = 'cc2.18.013' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.18', 'cc2.18.013', '58296']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.find(
            By.XPATH, '//a[contains(@href,"/cc-dashboard")]'
        ).click()
        self.teacher.open_user_menu()
        self.teacher.find(
            By.LINK_TEXT, 'Get Help'
        ).click()
        window_with_help = self.teacher.driver.window_handles[1]
        self.teacher.driver.switch_to_window(window_with_help)
        self.teacher.find(By.ID, 'searchAskInput').send_keys('question')
        self.teacher.find(By.ID, 'searchAskButton').click()
        self.teacher.page.wait_for_page_load()
        contact = self.teacher.find(
            By.XPATH, '//a[contains(text(),"Contact Us")]'
        )
        Assignment.scroll_to(self.teacher.driver, contact)
        contact.click()
        self.teacher.page.wait_for_page_load()
        self.teacher.find(
            By.XPATH, '//input[contains(@name,"contactUsForm:firstName")]'
        ).send_keys('qa_test_first_name')
        self.teacher.find(
            By.XPATH, '//input[contains(@name,"contactUsForm:lastName")]'
        ).send_keys('qa_test_last_name')
        self.teacher.find(
            By.XPATH, '//input[contains(@name,"contactUsForm:email")]'
        ).send_keys('qa_test@email.com')
        self.teacher.find(By.XPATH, '//input[@value="Submit"]').click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//p[contains(text(),"Thank you for your message!")]')
            )
        )
        self.ps.test_updates['passed'] = True

    # 14823 - 014 - Teacher | View guided tutorials of Concept Coach
    @pytest.mark.skipif(str(14823) not in TESTS, reason='Excluded')
    def test_teacher_view_guided_tutorials_of_concept_coach_14823(self):
        """View guided tutorials of Concept Coach.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 'cc2.18.014' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.18', 'cc2.18.014', '14823']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 14825 - 015 - Teacher | CC assignments have links that can be added to
    # teacher's LMS
    @pytest.mark.skipif(str(14825) not in TESTS, reason='Excluded')
    def test_teacher_cc_assignments_have_links_that_can_be_added_14825(self):
        """CC assignments have links that can be added to teacher's LMS.

        Steps:
        Go to Tutor
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a CC course name
        Click "Assignment Links"

        Expected Result:
        The user is presented with links to CC assignments
        """
        self.ps.test_updates['name'] = 'cc2.18.015' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.18', 'cc2.18.015', '14825']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.find(
            By.XPATH, '//a[contains(@href,"/cc-dashboard")]'
        ).click()
        self.teacher.find(By.LINK_TEXT, 'Assignment Links').click()
        assert('assignment-links' in self.teacher.current_url()), \
            'not at assignemnt links page'
        self.ps.test_updates['passed'] = True

    # 58275 - 016 - Student | Directed to a "No Courses" page when not in any
    # courses yet
    @pytest.mark.skipif(str(58275) not in TESTS, reason='Excluded')
    def test_student_directed_to_a_no_courses_page_when_not_in_any_58275(self):
        """Directed to a "No Courses" page when not in any courses yet.

        Steps:
        Go to Tutor
        Log in as qa_student_37003

        Expected Result:
        The message "We cannot find an OpenStax course associated with your
        account" displays with help links
        """
        self.ps.test_updates['name'] = 'cc2.18.016' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.18', 'cc2.18.016', '58275']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.login(username='qa_student_37003')
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//p[contains(text(),' +
                 '"We cannot find an OpenStax course ' +
                 'associated with your account.")]')
            )
        )

        self.ps.test_updates['passed'] = True

    # 58311 - 017 - Student | View "Getting Started with Concept Coach" Guide
    @pytest.mark.skipif(str(58311) not in TESTS, reason='Excluded')
    def test_student_view_getting_started_with_cc_guide_58311(self):
        """View "Getting Started with Concept Coach" Guide.

        Steps:
        Click "Concept Coach Students. Get help"
        Search for 'getting started'
        Click 'Getting Started with Concept Coach Guide - Students'

        Expected Result:
        CC Help Center opens in another tab with the Getting Started guide
        """
        self.ps.test_updates['name'] = 'cc2.18.017' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.18', 'cc2.18.017', '58311']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.login()
        self.student.open_user_menu()
        self.student.find(
            By.LINK_TEXT, 'Get Help'
        ).click()
        window_with_help = self.student.driver.window_handles[1]
        self.student.driver.switch_to_window(window_with_help)
        self.student.find(By.ID, 'searchAskInput').send_keys('getting started')
        self.student.find(By.ID, 'searchAskButton').click()
        self.student.page.wait_for_page_load()
        self.student.find(
            By.LINK_TEXT, 'Getting Started with Concept Coach Guide - Students'
        ).click()
        assert('articles' in self.student.current_url()), 'not at article'
        self.student.find(
            By.XPATH,
            '//h1[text()="' +
            'Getting Started with Concept Coach Guide - Students"]'
        )
        self.ps.test_updates['passed'] = True

    # 58274 - 018 - Student | Access CC Help Center after registering for a
    # course
    @pytest.mark.skipif(str(58274) not in TESTS, reason='Excluded')
    def test_student_access_cc_help_center_after_registering_for_58274(self):
        """Access Concept Coach Help Center after registering for a course.

        Steps:
        Go to Tutor
        Sign in as student
        Click on a Concept Coach course if the user is in more than one
        Click "Get Help" from the user menu

        Expected Result:
        The user is presented with the CC Help Center
        """
        self.ps.test_updates['name'] = 'cc2.18.018' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.18', 'cc2.18.018', '58274']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.login()
        self.student.open_user_menu()
        self.student.find(
            By.LINK_TEXT, 'Get Help'
        ).click()
        window_with_help = self.student.driver.window_handles[1]
        self.student.driver.switch_to_window(window_with_help)
        self.student.page.wait_for_page_load()
        self.student.find(
            By.XPATH, '//center[text()="Concept Coach Help Center"]'
        )
        self.ps.test_updates['passed'] = True

    # 58283 - 018 - Student | Submit a question
    @pytest.mark.skipif(str(58283) not in TESTS, reason='Excluded')
    def test_student_submit_a_question_58283(self):
        """Submit a question.

        Steps:
        Click "Get Help" from the user menu in the upper right corner of the
            screen
        Enter a question or search words into the search engine
        Click "Search" or press enter

        Expected Result:
        The user is presented with search results
        """
        self.ps.test_updates['name'] = 'cc2.18.019' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.18', 'cc2.18.019', '58283']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.login()
        self.student.open_user_menu()
        self.student.find(
            By.LINK_TEXT, 'Get Help'
        ).click()
        window_with_help = self.student.driver.window_handles[1]
        self.student.driver.switch_to_window(window_with_help)
        self.student.find(By.ID, 'searchAskInput').send_keys('question')
        self.student.find(By.ID, 'searchAskButton').click()
        self.student.page.wait_for_page_load()
        self.student.find(By.ID, 'results')
        self.student.find(By.XPATH, '//div[@class="article "]')

        self.ps.test_updates['passed'] = True

    # 58351 - 020 - Student | View "Contact Us" button after submitting a
    # question
    @pytest.mark.skipif(str(58351) not in TESTS, reason='Excluded')
    def test_student_view_contact_us_button_after_submitting_quest_58351(self):
        """View "Contact Us" button after submitting a question.

        Steps:
        Click "Get Help" from the user menu in the upper right corner of the
            screen
        Enter a question or search words into the search engine
        Click "Search" or press enter
        Scroll to the bottom of the page

        Expected Result:
        "Contact Us" button exists
        """
        self.ps.test_updates['name'] = 'cc2.18.020' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.18', 'cc2.18.020', '58351']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.login()
        self.student.open_user_menu()
        self.student.find(
            By.LINK_TEXT, 'Get Help'
        ).click()
        window_with_help = self.student.driver.window_handles[1]
        self.student.driver.switch_to_window(window_with_help)
        self.student.find(By.ID, 'searchAskInput').send_keys('question')
        self.student.find(By.ID, 'searchAskButton').click()
        self.teacher.page.wait_for_page_load()
        self.teacher.find(By.XPATH, '//a[contains(text(),"Contact Us")]')
        self.ps.test_updates['passed'] = True

    # 58326 - 021 - Student | View an article after submitting a question
    @pytest.mark.skipif(str(58326) not in TESTS, reason='Excluded')
    def test_student_view_an_article_after_submitting_a_question_58326(self):
        """View an article after submitting a question.

        Steps:
        Click "Get Help" from the user menu in the upper right corner of the
            screen
        Enter a question or search words into the search engine
        Click "Search" or press enter
        Click on a search result

        Expected Result:
        The user is presented with an article containing answer to the question

        """
        self.ps.test_updates['name'] = 'cc2.18.021' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.18', 'cc2.18.021', '58326']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.login()
        self.student.open_user_menu()
        self.student.find(
            By.LINK_TEXT, 'Get Help'
        ).click()
        window_with_help = self.student.driver.window_handles[1]
        self.student.driver.switch_to_window(window_with_help)
        self.student.find(By.ID, 'searchAskInput').send_keys('question')
        self.student.find(By.ID, 'searchAskButton').click()
        self.student.page.wait_for_page_load()
        self.student.find(By.XPATH, '//div[@class="article "]/a').click()
        self.student.find(By.ID, 'articleContainer')
        assert('articles' in self.student.current_url()), 'not at article'

        self.ps.test_updates['passed'] = True

    # 58327 - 022 - Student | Indicate that the article was helpful
    @pytest.mark.skipif(str(58327) not in TESTS, reason='Excluded')
    def test_student_indicate_that_the_article_was_helpful_58327(self):
        """Indicate that the article was helpful.

        Steps:
        Click "Get Help" from the user menu in the upper right corner of the
            screen
        Enter a question or search words into the search engine
        Click "Search" or press enter
        Click on a search result
        Scroll to "Feedback"
        Click "Yes"

        Expected Result:
        A message that says "Thanks for your feedback!" is displayed
        """
        self.ps.test_updates['name'] = 'cc2.18.022' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.18', 'cc2.18.022', '58327']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.login()
        self.student.open_user_menu()
        self.student.find(
            By.LINK_TEXT, 'Get Help'
        ).click()
        window_with_help = self.student.driver.window_handles[1]
        self.student.driver.switch_to_window(window_with_help)
        self.student.find(By.ID, 'searchAskInput').send_keys('question')
        self.student.find(By.ID, 'searchAskButton').click()
        self.student.page.wait_for_page_load()
        self.student.find(By.XPATH, '//div[@class="article "]/a').click()
        assert('articles' in self.student.current_url()), 'not at article'
        self.student.find(
            By.XPATH, '//div[@id="feedback"]//input[@value="Yes"]'
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[text()="Thanks for your feedback!"]')
            )
        )
        self.ps.test_updates['passed'] = True

    # 58328 - 023 - Student | Negative feedback renders a feedback popup box
    @pytest.mark.skipif(str(58328) not in TESTS, reason='Excluded')
    def test_student_negative_feedback_renders_feedback_popup_box_58328(self):
        """Negative feedback renders a feedback popup box.

        Steps:
        Click "Get Help" from the user menu in the upper right corner of the
            screen
        Enter a question or search words into the search engine
        Click "Search" or press enter
        Click on a search result
        Scroll to "Feedback"
        Click "No"

        Expected Result:
        The user is presented with a popup box that allows them to input
        feedback
        """
        self.ps.test_updates['name'] = 'cc2.18.023' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.18', 'cc2.18.023', '58328']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.login()
        self.student.open_user_menu()
        self.student.find(
            By.LINK_TEXT, 'Get Help'
        ).click()
        window_with_help = self.student.driver.window_handles[1]
        self.student.driver.switch_to_window(window_with_help)
        self.student.find(By.ID, 'searchAskInput').send_keys('question')
        self.student.find(By.ID, 'searchAskButton').click()
        self.student.page.wait_for_page_load()
        self.student.find(By.XPATH, '//div[@class="article "]/a').click()
        assert('articles' in self.student.current_url()), 'not at article'
        self.student.find(
            By.XPATH, '//div[@id="feedback"]//input[@value="No"]'
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'feedbackDialog')
            )
        )
        self.ps.test_updates['passed'] = True

    # 58329 - 024 - Student | Submit feedback for an article
    @pytest.mark.skipif(str(58329) not in TESTS, reason='Excluded')
    def test_student_submit_feedback_for_an_article_58329(self):
        """Submit feedback for an article.

        Steps:
        Click "Get Help" from the user menu in the upper right corner of the
            screen
        Enter a question or search words into the search engine
        Click "Search" or press enter
        Click on a search result
        Scroll to "Feedback"
        Click "No"
        Enter feedback into the box that pops up
        Click "Submit"

        Expected Result:
        A message that says "Thanks for your feedback!" is displayed in the box
        """
        self.ps.test_updates['name'] = 'cc2.18.024' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.18', 'cc2.18.024', '58329']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.login()
        self.student.open_user_menu()
        self.student.find(
            By.LINK_TEXT, 'Get Help'
        ).click()
        window_with_help = self.student.driver.window_handles[1]
        self.student.driver.switch_to_window(window_with_help)
        self.student.find(By.ID, 'searchAskInput').send_keys('question')
        self.student.find(By.ID, 'searchAskButton').click()
        self.student.page.wait_for_page_load()
        self.student.find(By.XPATH, '//div[@class="article "]/a').click()
        assert('articles' in self.student.current_url()), 'not at article'
        self.student.find(
            By.XPATH, '//div[@id="feedback"]//input[@value="No"]'
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'feedbackDialog')
            )
        )
        self.student.find(
            By.ID, 'feedbackTextArea'
        ).send_keys('qa automated test feedback')
        self.student.find(By.XPATH, '//input[@value="Submit"]').click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//p[text()="Thanks for your feedback!"]')
            )
        )
        self.ps.test_updates['passed'] = True

    # 58330 - 025 - Student | Close window after submitting feedback for an
    # article
    @pytest.mark.skipif(str(58330) not in TESTS, reason='Excluded')
    def test_student_close_window_after_submitting_feedback_for_58330(self):
        """Close window after submitting feedback for an article.

        Steps:
        Click "Get Help" from the user menu in the upper right corner of the
            screen
        Enter a question or search words into the search engine
        Click "Search" or press enter
        Click on a search result
        Scroll to "Feedback"
        Click "No"
        Enter feedback into the box that pops up
        Click "Submit"
        Click "Close window"

        Expected Result:
        The popup box closes and the message "Thanks for your feedback"
        displays beneath "Feedback"
        """
        self.ps.test_updates['name'] = 'cc2.18.025' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.18', 'cc2.18.025', '58330']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.login()
        self.student.open_user_menu()
        self.student.find(
            By.LINK_TEXT, 'Get Help'
        ).click()
        window_with_help = self.student.driver.window_handles[1]
        self.student.driver.switch_to_window(window_with_help)
        self.student.find(By.ID, 'searchAskInput').send_keys('question')
        self.student.find(By.ID, 'searchAskButton').click()
        self.student.page.wait_for_page_load()
        self.student.find(By.XPATH, '//div[@class="article "]/a').click()
        assert('articles' in self.student.current_url()), 'not at article'
        self.student.find(
            By.XPATH, '//div[@id="feedback"]//input[@value="No"]'
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'feedbackDialog')
            )
        )
        self.student.find(
            By.ID, 'feedbackTextArea'
        ).send_keys('qa automated test feedback')
        self.student.find(By.XPATH, '//input[@value="Submit"]').click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[text()="close window"]')
            )
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[text()="Thanks for your feedback!"]')
            )
        )
        self.ps.test_updates['passed'] = True

    # 58331 - 026 - Student | Cancel feedback
    @pytest.mark.skipif(str(58331) not in TESTS, reason='Excluded')
    def test_student_cancel_feedback_58331(self):
        """Cancel feedback.

        Steps:
        Click "Get Help" from the user menu in the upper right corner of the
            screen
        Enter a question or search words into the search engine
        Click "Search" or press enter
        Click on a search result
        Scroll to "Feedback"
        Click "No"
        [optional] Enter feedback into text box
        Click "Cancel"

        Expected Result:
        The popup box closes
        """
        self.ps.test_updates['name'] = 'cc2.18.026' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.18', 'cc2.18.026', '58331']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.login()
        self.student.open_user_menu()
        self.student.find(
            By.LINK_TEXT, 'Get Help'
        ).click()
        window_with_help = self.student.driver.window_handles[1]
        self.student.driver.switch_to_window(window_with_help)
        self.student.find(By.ID, 'searchAskInput').send_keys('question')
        self.student.find(By.ID, 'searchAskButton').click()
        self.student.page.wait_for_page_load()
        self.student.find(By.XPATH, '//div[@class="article "]/a').click()
        assert('articles' in self.student.current_url()), 'not at article'
        self.student.find(
            By.XPATH, '//div[@id="feedback"]//input[@value="No"]'
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'feedbackDialog')
            )
        )
        self.student.find(By.XPATH, '//input[@value="Cancel"]').click()
        with self.assertRaises(ElementNotVisibleException):
            self.student.find(
                By.ID, 'feedbackDialog').click()

        self.ps.test_updates['passed'] = True

    # 58333 - 027 - Student | View related articles
    @pytest.mark.skipif(str(58333) not in TESTS, reason='Excluded')
    def test_student_view_related_articles_58333(self):
        """View related articles.

        Steps:
        Click "Get Help" from the user menu in the upper right corner of the
            screen
        Enter a question or search words into the search engine
        Click "Search" or press enter
        Click on a search result
        Scroll to "Related Articles"
        Click on one of the articles (if any)

        Expected Result:
        The user is presented with the related article
        """
        self.ps.test_updates['name'] = 'cc2.18.027' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.18', 'cc2.18.027', '58333']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.login()
        self.student.open_user_menu()
        self.student.find(
            By.LINK_TEXT, 'Get Help'
        ).click()
        window_with_help = self.student.driver.window_handles[1]
        self.student.driver.switch_to_window(window_with_help)
        self.student.find(By.ID, 'searchAskInput').send_keys('question')
        self.student.find(By.ID, 'searchAskButton').click()
        self.student.page.wait_for_page_load()
        self.student.find(By.XPATH, '//div[@class="article "]/a').click()
        assert('articles' in self.student.current_url()), 'not at article'
        self.student.find(By.XPATH, '//h2[text()="Related Articles"]')

        self.ps.test_updates['passed'] = True

    # 58334 - 028 - Student | Submit a question to Customer Support
    @pytest.mark.skipif(str(58334) not in TESTS, reason='Excluded')
    def test_student_submit_a_question_to_customer_support_58334(self):
        """Submit a question to Customer Support.

        Steps:
        Click "Get Help" from the user menu in the upper right corner of the
            screen
        Enter a question or search words into the search engine
        Click "Search" or press enter
        Click on a search result
        Scroll to the bottom of the page
        Click "Contact Us"
        Fill out the required fields
        Enter "Submit"

        Expected Result:
        The message "Thank you for your message! We'll be back to you within
        one business day" is displayed
        """
        self.ps.test_updates['name'] = 'cc2.18.028' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.18', 'cc2.18.028', '58334']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.login()
        self.student.open_user_menu()
        self.student.find(
            By.LINK_TEXT, 'Get Help'
        ).click()
        window_with_help = self.student.driver.window_handles[1]
        self.student.driver.switch_to_window(window_with_help)
        self.student.find(By.ID, 'searchAskInput').send_keys('question')
        self.student.find(By.ID, 'searchAskButton').click()
        self.student.page.wait_for_page_load()
        contact = self.student.find(
            By.XPATH, '//a[contains(text(),"Contact Us")]'
        )
        Assignment.scroll_to(self.student.driver, contact)
        contact.click()
        self.student.page.wait_for_page_load()
        self.student.find(
            By.XPATH, '//input[contains(@name,"contactUsForm:firstName")]'
        ).send_keys('qa_test_first_name')
        self.student.find(
            By.XPATH, '//input[contains(@name,"contactUsForm:lastName")]'
        ).send_keys('qa_test_last_name')
        self.student.find(
            By.XPATH, '//input[contains(@name,"contactUsForm:email")]'
        ).send_keys('qa_test@email.com')
        self.student.find(By.XPATH, '//input[@value="Submit"]').click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//p[contains(text(),"Thank you for your message!")]')
            )
        )
        self.ps.test_updates['passed'] = True

    # 58335 - 029 - Student | View guided tutorials of Concept Coach
    @pytest.mark.skipif(str(58335) not in TESTS, reason='Excluded')
    def test_student_view_guided_tutorials_of_concept_coach_58335(self):
        """View guided tutorial of Concept Coach.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 'cc2.18.029' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.18', 'cc2.18.029', '58335']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
