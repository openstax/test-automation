"""Tutor v2, Epic 18 - Guide, Monitor, Support, and Train Users."""

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

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Teacher, Admin

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
        58319
    ])
)

"""
14752, 14751, 58279, 58280, 58284,
        58352, 58288, 58313, 58314, 58315,
        58322, 58316, 58318, 58319, 14755,
        14750, 58336, 58337, 58338, 58353,
        58339, 58340, 58341, 58342, 58343,
        58344, 58346, 58347, 58348
"""


@PastaDecorator.on_platforms(BROWSERS)
class TestGuideMonitorSupportAndTrainUsers(unittest.TestCase):
    """T2.18 - Guide, Monitor, Support, and Train Users."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        #self.teacher = Teacher(
        #    use_env_vars=True,
        #    pasta_user=self.ps,
        #    capabilities=self.desired_capabilities
        #)

        self.teacher = Teacher(use_env_vars=True)
        #self.teacher.login()

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

    # 14752 - 001 - User | In-app Notification of downtime
    @pytest.mark.skipif(str(14752) not in TESTS, reason='Excluded')
    def test_user_inapp_notification_of_downtime_14752(self):
        """In-app Notification of downtime.

        Steps:

        Go to Tutor
        Log in as admin
        Click "Admin" from the user menu
        Click "System Setting"
        Click "Notifications"
        Enter a new notification into the text box
        Click "Add"
        Log out of admin
        Log in as teacher01

        Expected Result:
        An orange header with the notification pops up when you sign in
        """
        self.ps.test_updates['name'] = 't2.18.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.18',
            't2.18.001',
            '14752'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        admin = Admin(use_env_vars=True)
        admin.login()
        admin.goto_admin_control()

        # Create the notification
        admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'System Setting')
            )
        ).click()
        admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Notifications')
            )
        ).click()
        admin.sleep(5)

        admin.find(By.XPATH, "//input[@id='message']").send_keys(
            'automated test')

        admin.find(By.XPATH, "//input[@class='btn btn-default']").click()

        admin.sleep(5)

        # View the notification
        self.teacher.driver.refresh()
        self.teacher.find(By.XPATH, "//div[@class='notification system']")

        # Delete the notification
        notif = admin.driver.find_elements_by_xpath(
            "//div[@class='col-xs-12']")

        for index, n in enumerate(notif):
            if n.text.find('automated test') >= 0:
                admin.driver.find_elements_by_xpath(
                    "//a[@class='btn btn-warning']")[index].click()
                admin.sleep(5)
                admin.driver.switch_to_alert().accept()
                admin.sleep(5)
                self.ps.test_updates['passed'] = True
                break

        admin.delete()

        # self.ps.test_updates['passed'] = True

    # 14751 - 002 - Teacher | Directed to a "No Courses" page when not in any
    # courses yet
    @pytest.mark.skipif(str(14751) not in TESTS, reason='Excluded')
    def test_teacher_directed_to_a_no_courses_page_when_not_in_any_14751(self):
        """Directed to a "No Courses" page when not in any courses yet.

        Steps:
        Go to tutor-qa.openstax.org
        Sign in as demo_teacher; password

        Expected Result:
        The message "We cannot find an OpenStax course associated with your
        account" displays with help links below
        """
        self.ps.test_updates['name'] = 't2.18.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.18',
            't2.18.002',
            '14751'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.username = 'demo_teacher'
        self.teacher.login()

        self.teacher.find(
            By.XPATH, "//div[@class='-course-list-empty panel panel-default']")

        self.ps.test_updates['passed'] = True

    # 58279 - 003 - Teacher | View "Getting Started with Tutor" Guide
    @pytest.mark.skipif(str(58279) not in TESTS, reason='Excluded')
    def test_teacher_view_getting_started_with_tutor_guide_58279(self):
        """View "Getting Started with Tutor" Guide.

        Steps:
        Click "Tutor Instructors. Get help"

        Expected Result:
        Tutor Help Center opens in another tab with the Getting Started guide
        """
        self.ps.test_updates['name'] = 't2.18.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.18',
            't2.18.003',
            '58279'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.username = 'demo_teacher'
        self.teacher.login()

        self.teacher.find(
            By.XPATH, "//div[@class='-course-list-empty panel panel-default']")

        # View the article
        self.teacher.find(By.PARTIAL_LINK_TEXT, "Tutor Instructors.").click()
        self.teacher.driver.switch_to.window(
            self.teacher.driver.window_handles[-1])

        title = self.teacher.find(
            By.XPATH, "//h1[@class='pageType noSecondHeader']")

        assert(title.text == "Getting Started with Tutor Guide -Teachers"), \
            "Not viewing the getting started article"

        self.teacher.sleep(5)

        self.ps.test_updates['passed'] = True

    # 58280 - 004 - Teacher | Access Tutor Help Center after registering for
    # a course
    @pytest.mark.skipif(str(58280) not in TESTS, reason='Excluded')
    def test_teacher_access_tutor_help_center_after_registering_58280(self):
        """Access Tutor Help Center after registering for a course.

        Steps:
        Go to Tutor
        Sign in as teacher01
        Click on a Tutor course if the user is in more than one
        Click "Get Help" from the user menu in the upper right corner of the
            screen

        Expected Result:
        The user is presented with the Tutor Help Center
        """
        self.ps.test_updates['name'] = 't2.18.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.18',
            't2.18.004',
            '58280'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.open_user_menu()
        self.teacher.find(By.LINK_TEXT, "Get Help").click()

        self.teacher.driver.switch_to.window(
            self.teacher.driver.window_handles[-1])

        assert(self.teacher.driver.current_url.find(
            "openstax.force.com") >= 0
        ), \
            "Not on the get help page"

        self.ps.test_updates['passed'] = True

    # 58284 - 005 - Teacher | Submit a question
    @pytest.mark.skipif(str(58284) not in TESTS, reason='Excluded')
    def test_teacher_submit_a_question_58284(self):
        """Submit a question.

        Steps:
        Click "Get Help" from the user menu in the upper right corner of the
            screen
        Enter a question or search words into the search engine
        Click "Search" or press enter

        Expected Result:
        The user is presented with search results
        """
        self.ps.test_updates['name'] = 't2.18.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.18',
            't2.18.005',
            '58284'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.open_user_menu()
        self.teacher.find(By.LINK_TEXT, "Get Help").click()

        self.teacher.driver.switch_to.window(
            self.teacher.driver.window_handles[-1])

        assert(self.teacher.driver.current_url.find(
            "openstax.force.com") >= 0
        ), \
            "Not on the get help page"

        # Ask a question
        self.teacher.find(
            By.XPATH, "//textarea[@id='searchAskInput']").send_keys("help")

        self.teacher.find(By.XPATH, "//a[@id='searchAskButton']").click()

        self.teacher.find(By.XPATH, "//div[@id='results']")
        self.teacher.sleep(3)

        self.ps.test_updates['passed'] = True

    # 58352 - 006 - Teacher | View "Contact Us" button after submitting a
    # question
    @pytest.mark.skipif(str(58352) not in TESTS, reason='Excluded')
    def test_teacher_view_contact_us_button_after_submitting_quest_58352(self):
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
        self.ps.test_updates['name'] = 't2.18.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.18',
            't2.18.006',
            '58352'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.open_user_menu()
        self.teacher.find(By.LINK_TEXT, "Get Help").click()

        self.teacher.driver.switch_to.window(
            self.teacher.driver.window_handles[-1])

        assert(self.teacher.driver.current_url.find(
            "openstax.force.com") >= 0
        ), \
            "Not on the get help page"

        # Ask a question
        self.teacher.find(
            By.XPATH, "//textarea[@id='searchAskInput']").send_keys("help")

        self.teacher.find(By.XPATH, "//a[@id='searchAskButton']").click()

        self.teacher.find(By.XPATH, "//div[@id='results']")
        self.teacher.sleep(3)

        self.teacher.find(By.XPATH, "//div[@id='contactUs']/a")

        self.ps.test_updates['passed'] = True

    # 58288 - 007 - Teacher | View an article after submitting a question
    @pytest.mark.skipif(str(58288) not in TESTS, reason='Excluded')
    def test_teacher_view_an_article_after_submitting_a_question_58288(self):
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
        self.ps.test_updates['name'] = 't2.18.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.18',
            't2.18.007',
            '58288'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.open_user_menu()
        self.teacher.find(By.LINK_TEXT, "Get Help").click()

        self.teacher.driver.switch_to.window(
            self.teacher.driver.window_handles[-1])

        assert(self.teacher.driver.current_url.find(
            "openstax.force.com") >= 0
        ), \
            "Not on the get help page"

        # Ask a question
        self.teacher.find(
            By.XPATH, "//textarea[@id='searchAskInput']").send_keys("help")

        self.teacher.find(By.XPATH, "//a[@id='searchAskButton']").click()

        self.teacher.find(By.XPATH, "//div[@id='results']")
        self.teacher.sleep(3)

        if len(
            self.teacher.driver.find_elements_by_xpath(
                "//div[@class='article']/a")
        ) == 0:
            self.teacher.find(By.XPATH, "//div[@class='article ']/a").click()

        else:
            self.teacher.find(By.XPATH, "//div[@class='article']/a").click()
        self.teacher.sleep(3)

        assert(self.teacher.driver.current_url.find("articles") >= 0), \
            "Not viewing an article"

        self.ps.test_updates['passed'] = True

    # 58313 - 008 - Teacher | Indicate that the article was helpful
    @pytest.mark.skipif(str(58313) not in TESTS, reason='Excluded')
    def test_teacher_indicate_that_the_article_was_helpful_58313(self):
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
        self.ps.test_updates['name'] = 't2.18.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.18',
            't2.18.008',
            '58313'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.open_user_menu()
        self.teacher.find(By.LINK_TEXT, "Get Help").click()

        self.teacher.driver.switch_to.window(
            self.teacher.driver.window_handles[-1])

        assert(self.teacher.driver.current_url.find(
            "openstax.force.com") >= 0
        ), \
            "Not on the get help page"

        # Ask a question
        self.teacher.find(
            By.XPATH, "//textarea[@id='searchAskInput']").send_keys("help")

        self.teacher.find(By.XPATH, "//a[@id='searchAskButton']").click()

        self.teacher.find(By.XPATH, "//div[@id='results']")
        self.teacher.sleep(3)

        if len(
            self.teacher.driver.find_elements_by_xpath(
                "//div[@class='article']/a")
        ) == 0:
            self.teacher.find(By.XPATH, "//div[@class='article ']/a").click()

        else:
            self.teacher.find(By.XPATH, "//div[@class='article']/a").click()
        self.teacher.sleep(3)

        assert(self.teacher.driver.current_url.find("articles") >= 0), \
            "Not viewing an article"

        self.teacher.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        self.teacher.find(
            By.XPATH, "//input[contains(@id, 'feedbackYesButton')]").click()

        self.teacher.sleep(10)
        self.teacher.find(By.XPATH, "//div[@id='feedback']")

        self.ps.test_updates['passed'] = True

    # 58314 - 009 - Teacher | Negative feedback renders a feedback popup box
    @pytest.mark.skipif(str(58314) not in TESTS, reason='Excluded')
    def test_teacher_negative_feedback_renders_feedback_popup_box_58314(self):
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
        self.ps.test_updates['name'] = 't2.18.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.18',
            't2.18.009',
            '58314'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.open_user_menu()
        self.teacher.find(By.LINK_TEXT, "Get Help").click()

        self.teacher.driver.switch_to.window(
            self.teacher.driver.window_handles[-1])

        assert(self.teacher.driver.current_url.find(
            "openstax.force.com") >= 0
        ), \
            "Not on the get help page"

        # Ask a question
        self.teacher.find(
            By.XPATH, "//textarea[@id='searchAskInput']").send_keys("help")

        self.teacher.find(By.XPATH, "//a[@id='searchAskButton']").click()

        self.teacher.find(By.XPATH, "//div[@id='results']")
        self.teacher.sleep(3)

        if len(
            self.teacher.driver.find_elements_by_xpath(
                "//div[@class='article']/a")
        ) == 0:
            self.teacher.find(By.XPATH, "//div[@class='article ']/a").click()

        else:
            self.teacher.find(By.XPATH, "//div[@class='article']/a").click()
        self.teacher.sleep(3)

        assert(self.teacher.driver.current_url.find("articles") >= 0), \
            "Not viewing an article"

        self.teacher.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        self.teacher.find(
            By.XPATH, "//input[contains(@id, 'feedbackNoButton')]").click()

        self.teacher.sleep(2)
        self.teacher.find(By.XPATH, "//div[@id='feedbackDialog']")

        self.ps.test_updates['passed'] = True

    # 58315 - 010 - Teacher | Submit feedback for an article
    @pytest.mark.skipif(str(58315) not in TESTS, reason='Excluded')
    def test_teacher_submit_feedback_for_an_article_58315(self):
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
        self.ps.test_updates['name'] = 't2.18.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.18',
            't2.18.010',
            '58315'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.open_user_menu()
        self.teacher.find(By.LINK_TEXT, "Get Help").click()

        self.teacher.driver.switch_to.window(
            self.teacher.driver.window_handles[-1])

        assert(self.teacher.driver.current_url.find(
            "openstax.force.com") >= 0
        ), \
            "Not on the get help page"

        # Ask a question
        self.teacher.find(
            By.XPATH, "//textarea[@id='searchAskInput']").send_keys("help")

        self.teacher.find(By.XPATH, "//a[@id='searchAskButton']").click()

        self.teacher.find(By.XPATH, "//div[@id='results']")
        self.teacher.sleep(3)

        if len(
            self.teacher.driver.find_elements_by_xpath(
                "//div[@class='article']/a")
        ) == 0:
            self.teacher.find(By.XPATH, "//div[@class='article ']/a").click()

        else:
            self.teacher.find(By.XPATH, "//div[@class='article']/a").click()
        self.teacher.sleep(3)

        assert(self.teacher.driver.current_url.find("articles") >= 0), \
            "Not viewing an article"

        self.teacher.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        self.teacher.find(
            By.XPATH, "//input[contains(@id, 'feedbackNoButton')]").click()

        self.teacher.sleep(2)
        self.teacher.find(
            By.XPATH, "//textarea[@id='feedbackTextArea']").send_keys("test")

        self.teacher.find(
            By.XPATH, "//input[contains(@id, 'feedbackForm:j')]").click()

        self.teacher.find(By.XPATH, "//div/p[1]")
        self.teacher.sleep(3)

        self.ps.test_updates['passed'] = True

    # 58322 - 011 - Teacher | Close window after submitting feedback for an
    # article
    @pytest.mark.skipif(str(58322) not in TESTS, reason='Excluded')
    def test_teacher_close_window_after_submitting_feedback_for_58322(self):
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
        self.ps.test_updates['name'] = 't2.18.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.18',
            't2.18.011',
            '58322'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.open_user_menu()
        self.teacher.find(By.LINK_TEXT, "Get Help").click()

        self.teacher.driver.switch_to.window(
            self.teacher.driver.window_handles[-1])

        assert(self.teacher.driver.current_url.find(
            "openstax.force.com") >= 0
        ), \
            "Not on the get help page"

        # Ask a question
        self.teacher.find(
            By.XPATH, "//textarea[@id='searchAskInput']").send_keys("help")

        self.teacher.find(By.XPATH, "//a[@id='searchAskButton']").click()

        self.teacher.find(By.XPATH, "//div[@id='results']")
        self.teacher.sleep(3)

        if len(
            self.teacher.driver.find_elements_by_xpath(
                "//div[@class='article']/a")
        ) == 0:
            self.teacher.find(By.XPATH, "//div[@class='article ']/a").click()

        else:
            self.teacher.find(By.XPATH, "//div[@class='article']/a").click()
        self.teacher.sleep(3)

        assert(self.teacher.driver.current_url.find("articles") >= 0), \
            "Not viewing an article"

        self.teacher.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        self.teacher.find(
            By.XPATH, "//input[contains(@id, 'feedbackNoButton')]").click()

        self.teacher.sleep(2)
        self.teacher.find(
            By.XPATH, "//textarea[@id='feedbackTextArea']").send_keys("test")

        self.teacher.find(
            By.XPATH, "//input[contains(@id, 'feedbackForm:j')]").click()

        self.teacher.find(By.XPATH, "//div/p[1]")
        self.teacher.sleep(3)
        self.teacher.find(By.LINK_TEXT, "close window").click()
        self.teacher.sleep(3)

        self.ps.test_updates['passed'] = True

    # 58316 - 012 - Teacher | Cancel feedback
    @pytest.mark.skipif(str(58316) not in TESTS, reason='Excluded')
    def test_teacher_cancel_feedback_before_making_changes_58316(self):
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
        self.ps.test_updates['name'] = 't2.18.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.18',
            't2.18.012',
            '58316'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.open_user_menu()
        self.teacher.find(By.LINK_TEXT, "Get Help").click()

        self.teacher.driver.switch_to.window(
            self.teacher.driver.window_handles[-1])

        assert(self.teacher.driver.current_url.find(
            "openstax.force.com") >= 0
        ), \
            "Not on the get help page"

        # Ask a question
        self.teacher.find(
            By.XPATH, "//textarea[@id='searchAskInput']").send_keys("help")

        self.teacher.find(By.XPATH, "//a[@id='searchAskButton']").click()

        self.teacher.find(By.XPATH, "//div[@id='results']")
        self.teacher.sleep(3)

        if len(
            self.teacher.driver.find_elements_by_xpath(
                "//div[@class='article']/a")
        ) == 0:
            self.teacher.find(By.XPATH, "//div[@class='article ']/a").click()

        else:
            self.teacher.find(By.XPATH, "//div[@class='article']/a").click()
        self.teacher.sleep(3)

        assert(self.teacher.driver.current_url.find("articles") >= 0), \
            "Not viewing an article"

        self.teacher.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        self.teacher.find(
            By.XPATH, "//input[contains(@id, 'feedbackNoButton')]").click()

        self.teacher.sleep(2)
        self.teacher.find(
            By.XPATH, "//textarea[@id='feedbackTextArea']").send_keys("test")

        self.teacher.find(
            By.XPATH, "//div[contains(@id, 'feedbackForm:j')]/input[2]"
        ).click()

        self.teacher.sleep(3)

        self.ps.test_updates['passed'] = True

    # 58318 - 013 - Teacher | View related articles
    @pytest.mark.skipif(str(58318) not in TESTS, reason='Excluded')
    def test_teacher_view_related_articles_58318(self):
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
        self.ps.test_updates['name'] = 't2.18.013' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.18',
            't2.18.013',
            '58318'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.open_user_menu()
        self.teacher.find(By.LINK_TEXT, "Get Help").click()

        self.teacher.driver.switch_to.window(
            self.teacher.driver.window_handles[-1])

        assert(self.teacher.driver.current_url.find(
            "openstax.force.com") >= 0
        ), \
            "Not on the get help page"

        # Ask a question
        self.teacher.find(
            By.XPATH, "//textarea[@id='searchAskInput']").send_keys("help")

        self.teacher.find(By.XPATH, "//a[@id='searchAskButton']").click()

        self.teacher.find(By.XPATH, "//div[@id='results']")
        self.teacher.sleep(3)

        if len(
            self.teacher.driver.find_elements_by_xpath(
                "//div[@class='article']/a")
        ) == 0:
            self.teacher.find(By.XPATH, "//div[@class='article ']/a").click()

        else:
            self.teacher.find(By.XPATH, "//div[@class='article']/a").click()
        self.teacher.sleep(3)

        assert(self.teacher.driver.current_url.find("articles") >= 0), \
            "Not viewing an article"

        related = self.teacher.driver.find_elements_by_xpath(
            "//a[@class='relatedLink']")

        if len(related) > 1:
            old = self.teacher.driver.current_url
            related[1].click()
            self.teacher.sleep(3)
            assert(self.teacher.driver.current_url != old), \
                "Not viewing an article"

        self.ps.test_updates['passed'] = True

    # 58319 - 014 - Teacher | Submit a question to Customer Support
    @pytest.mark.skipif(str(58319) not in TESTS, reason='Excluded')
    def test_teacher_submit_a_question_to_customer_support_58319(self):
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
        self.ps.test_updates['name'] = 't2.18.014' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.18',
            't2.18.014',
            '58319'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.open_user_menu()
        self.teacher.find(By.LINK_TEXT, "Get Help").click()

        self.teacher.driver.switch_to.window(
            self.teacher.driver.window_handles[-1])

        assert(self.teacher.driver.current_url.find(
            "openstax.force.com") >= 0
        ), \
            "Not on the get help page"

        # Ask a question
        self.teacher.find(
            By.XPATH, "//textarea[@id='searchAskInput']").send_keys("help")

        self.teacher.find(By.XPATH, "//a[@id='searchAskButton']").click()

        self.teacher.find(By.XPATH, "//div[@id='results']")
        self.teacher.sleep(3)

        if len(
            self.teacher.driver.find_elements_by_xpath(
                "//div[@class='article']/a")
        ) == 0:
            self.teacher.find(By.XPATH, "//div[@class='article ']/a").click()

        else:
            self.teacher.find(By.XPATH, "//div[@class='article']/a").click()
        self.teacher.sleep(3)

        assert(self.teacher.driver.current_url.find("articles") >= 0), \
            "Not viewing an article"

        self.teacher.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        self.teacher.find(By.LINK_TEXT, "Email Us").click()
        self.teacher.sleep(3)

        self.teacher.find(By.XPATH, "//input[@id='j_id0:j_id1:contactUsForm:firstName']").send_keys("automated")
        self.teacher.find(By.XPATH, "//input[@id='j_id0:j_id1:contactUsForm:lastName']").send_keys("test")
        self.teacher.find(By.XPATH, "//input[@id='j_id0:j_id1:contactUsForm:email']").send_keys("automated@test.com")
        self.teacher.find(By.XPATH, "//input[@id='j_id0:j_id1:contactUsForm:subject']").send_keys("automated test")
        self.teacher.find(By.XPATH, "//textarea[@id='j_id0:j_id1:contactUsForm:message']").send_keys("help")

        self.teacher.find(By.XPATH, "//input[@id='j_id0:j_id1:contactUsForm:j_id440']").click()

        self.teacher.sleep(5)
        assert(self.teacher.find(By.XPATH, "//p").text == "Thank you for your message! We’ll be back to you within one business day."), \
            "No confirmation message"

        self.ps.test_updates['passed'] = True

    # 14755 - 015 - Teacher | View guided tutorials of Tutor
    @pytest.mark.skipif(str(14755) not in TESTS, reason='Excluded')
    def test_teacher_view_guided_tutorials_of_concept_coach_14755(self):
        """View guided tutorials of Tutor.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.18.015' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.18',
            't2.18.015',
            '14755'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 14750 - 016 - Student | Directed to a "No Courses" page when not in any
    # courses yet
    @pytest.mark.skipif(str(14750) not in TESTS, reason='Excluded')
    def test_student_directed_to_a_no_courses_page_when_not_in_any_14750(self):
        """Directed to a "No Courses" page when not in any courses yet.

        Steps:
        Go to Tutor
        Log in as qa_student_37003

        Expected Result:
        The message "We cannot find an OpenStax course associated with your
        account" displays with help links
        """
        self.ps.test_updates['name'] = 't2.18.016' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.18',
            't2.18.016',
            '14750'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 58336 - 017 - Student | View "Getting Started with Tutor" Guide
    @pytest.mark.skipif(str(58336) not in TESTS, reason='Excluded')
    def test_student_view_getting_started_with_tutor_guide_58336(self):
        """View "Getting Started with Tutor" Guide.

        Steps:
        Click "Tutor Students. Get help"

        Expected Result:
        Tutor Help Center opens in another tab with the Getting Started guide
        """
        self.ps.test_updates['name'] = 't2.18.017' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.18',
            't2.18.017',
            '58336'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 58337 - 018 - Student | Access Tutor Help Center after registering for a
    # course
    @pytest.mark.skipif(str(58337) not in TESTS, reason='Excluded')
    def test_student_access_tutor_help_center_after_registering_58337(self):
        """Access Tutor Help Center after registering for a course.

        Steps:
        Go to Tutor
        Sign in as student01
        Click on a Tutor course if the user is in more than one
        Click "Get Help" from the user menu in the upper right corner of the
            screen

        Expected Result:
        The user is presented with the Tutor Help Center
        """
        self.ps.test_updates['name'] = 't2.18.018' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.18',
            't2.18.018',
            '58337'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 58338 - 019 - Student | Submit a question
    @pytest.mark.skipif(str(58338) not in TESTS, reason='Excluded')
    def test_student_submit_a_question_58338(self):
        """Submit a question.

        Steps:
        Click "Get Help" from the user menu in the upper right corner of the
            screen
        Enter a question or search words into the search engine
        Click "Search" or press enter

        Expected Result:
        The user is presented with search results
        """
        self.ps.test_updates['name'] = 't2.18.019' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.18',
            't2.18.019',
            '58338'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 58353 - 020 - Student | View "Contact Us" button after submitting a
    # question
    @pytest.mark.skipif(str(58353) not in TESTS, reason='Excluded')
    def test_student_view_contact_us_button_after_submitting_quest_58353(self):
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
        self.ps.test_updates['name'] = 't2.18.020' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.18',
            't2.18.020',
            '58353'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 58339 - 021 - Student | View an article after submitting a question
    @pytest.mark.skipif(str(58339) not in TESTS, reason='Excluded')
    def test_student_view_an_article_after_submitting_a_question_58339(self):
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
        self.ps.test_updates['name'] = 't2.18.021' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.18',
            't2.18.021',
            '58339'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 58340 - 022 - Student | Indicate that the article was helpful
    @pytest.mark.skipif(str(58340) not in TESTS, reason='Excluded')
    def test_student_indicate_that_the_article_was_helpful_58340(self):
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
        self.ps.test_updates['name'] = 't2.18.022' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.18',
            't2.18.022',
            '58340'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 58341 - 023 - Student | Negative feedback renders a feedback popup box
    @pytest.mark.skipif(str(58341) not in TESTS, reason='Excluded')
    def test_student_negative_feedback_renders_feedback_popup_box_58341(self):
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
        self.ps.test_updates['name'] = 't2.18.023' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.18',
            't2.18.023',
            '58341'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 58342 - 024 - Student | Submit feedback for an article
    @pytest.mark.skipif(str(58342) not in TESTS, reason='Excluded')
    def test_student_submit_feedback_for_an_article_58342(self):
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
        self.ps.test_updates['name'] = 't2.18.024' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.18',
            't2.18.024',
            '58342'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 58343 - 025 - Student | Close window after submitting feedback for an
    # article
    @pytest.mark.skipif(str(58343) not in TESTS, reason='Excluded')
    def test_student_close_window_after_submitting_feedback_for_58343(self):
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
        self.ps.test_updates['name'] = 't2.18.025' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.18',
            't2.18.025',
            '58343'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 58344 - 026 - Student | Cancel feedback
    @pytest.mark.skipif(str(58344) not in TESTS, reason='Excluded')
    def test_student_cancel_feedback_58344(self):
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
        self.ps.test_updates['name'] = 't2.18.026' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.18',
            't2.18.026',
            '58344'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 58346 - 027 - Student | View related articles
    @pytest.mark.skipif(str(58346) not in TESTS, reason='Excluded')
    def test_student_view_related_articles_58346(self):
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
        self.ps.test_updates['name'] = 't2.18.027' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.18',
            't2.18.027',
            '58346'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 58347 - 028 - Student | Submit a question to Customer Support
    @pytest.mark.skipif(str(58347) not in TESTS, reason='Excluded')
    def test_student_submit_a_question_to_customer_support_58347(self):
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
        self.ps.test_updates['name'] = 't2.18.028' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.18',
            't2.18.028',
            '58347'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 58348 - 029 - Student | View guided tutorials of Tutor
    @pytest.mark.skipif(str(58348) not in TESTS, reason='Excluded')
    def test_student_view_guided_tutorials_of_concept_coach_58348(self):
        """View guided tutorial of Tutor.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.18.029' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.18',
            't2.18.029',
            '58348'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
