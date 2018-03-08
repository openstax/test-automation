"""Course cloning and copying past assignments | Tutor: Teachers"""

import inspect
import json
import os
import pytest
import unittest
# import datetime

from helper import Teacher
from pastasauce import PastaSauce, PastaDecorator
from random import randint
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

basic_test_env = json.dumps([
    {
        'platform': 'Windows 10',
        'browserName': 'chrome',
        'version': 'latest',
        'screenResolution': "1024x768",
    }
])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
LOCAL_RUN = os.getenv('LOCALRUN', 'false').lower() == 'true'
TESTS = os.getenv(
    'CASELIST',
    str([
        # 162241,
        162246,
        # 162249,
        162247, 162250, 162251
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestTutorTeacher(unittest.TestCase):
    """Tutor | Teacher"""

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
        # self.teacher.login()
        # self.teacher.select_course(appearance='college_physics')

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

    # NOT FINISHED
    @pytest.mark.skipif(str(162241) not in TESTS, reason='Excluded')
    def test_course_cloning_and_copying_past_assignments_162241(self):
        """
        Clone courses and copy past assignments from the courses you cloned
        from.

        Go to tutor qa
        Log in to a teacher account
        In the dashboard, click "Add a Course"
        Select a Course
        Select a Semester
        Select Copy a past course
        Select a course to copy
        Enter a name for the tutor course
        ***Text should be able to be entered into box***

        Specify the number of sections for a new course
        ***Number could be entered. Page won't proceed if anything else is
        entered***

        Specify the number of students for the course
        ***Number could be entered. Page won't proceed if anything else is
        entered***

        Press "Continue"
        ***A course dashboard appears with the name and section number user
        entered***
        Copy a homework
        ***When user clicks on a past assignment on the left panel, An
        auto-filled assignment creation form appeared***

        Copy an event
        ***When user clicks on a past Event on the left panel, An auto-filled
        event creation form appeared***

        Copy a reading
        ***When user clicks on a past Reading on the left panel, An auto-filled
        event creation form appeared***
        Copy an external assignment

        EXPECTED RESULT:
        When user clicks on a past External Assignment on the left panel, An
        auto-filled event creation form appeared

        Corresponding test cases: T3.09 004, 005, 006, 007, 008, 010, 011, 012,
        013
        """

        self.ps.test_updates['name'] = \
            'tutor_course_creation_teacher_162241' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = \
            ['tutor', 'course creation', 'teacher', '162241']
        self.ps.test_updates['passed'] = False

        self.teacher.login()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.CSS_SELECTOR, '.user-actions-menu')
            )
        ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.CSS_SELECTOR, '#menu-option-createNewCourse')
            )
        ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable((
                By.XPATH,
                ".//*[@data-appearance='micro_economics' and " +
                "contains(text(), 'Econ')]"
            ))
        ).click()
        self.teacher.find(
            By.CSS_SELECTOR,
            '.next.btn.btn-primary'
        ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, ".//*[contains(text(), 'summer')]")
            )
        ).click()
        self.teacher.find(
            By.CSS_SELECTOR,
            '.next.btn.btn-primary'
        ).click()

        self.teacher.sleep(3)
        self.ps.test_updates['passed'] = True

    @pytest.mark.skipif(str(162246) not in TESTS, reason='Excluded')
    def test_tutor_help_center_162246(self):
        """
        Go to tutor qa and log in as a teacher
        Click on a Tutor course
        Click "Get Help" from the "Help" dropdown in the upper right corner
        ***User is presented with the Tutor Help Center***

        Enter a question or search words into search engine
        Click "search"
        ***User is presented with search results***

        Scroll to the bottom of the screen
        ***Email Us link works***

        Click on an article
        ***Article should pop up/be able to be viewed***
        Scroll to "Feedback"
        Click "Yes"
        ***Message that says "Thanks for your feedback!" is displayed***

        Click "<Back to search results"
        Click on another article
        Scroll to "Feedback"
        Click "No"
        ***User is presented with a popup box that allows them to input
        feedback***

        Click "Cancel"
        ***Popup box closes***

        Under "Feedback", Click "No"
        Enter feedback, click "Submit"
        ***Message that says "Thanks for your feedback!" is displayed in the
        box***

        Click "Close window"
        ***The popup box closes and the message "Thanks for your feedback"
        displays beneath "Feedback"***

        Scroll to bottom, under "Related Articles", click an article

        Expected Result:

        ***User is presented with the related article***

        Corresponding test cases: T2.18 004-013, 014

        https://trello.com/c/x6uE4Rcg/21-accessing-and-using-tutor-help-center
        """
        self.ps.test_updates['name'] = 'tutor_help_center_teacher_162246' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = \
            ['tutor', 'help_center', 'teacher', '162246']
        self.ps.test_updates['passed'] = False

        self.teacher.login()
        # goes to a random course
        self.teacher.random_course()
        # opens help menu and clicks Help Articles
        self.teacher.open_help_menu()
        self.teacher.find(By.LINK_TEXT, 'Help Articles').click()

        # switches active windows
        window_with_help = self.teacher.driver.window_handles[1]
        self.teacher.driver.switch_to_window(window_with_help)
        self.teacher.page.wait_for_page_load()
        # in search bar, search 'getting started'
        self.teacher.find(By.ID, 'searchAskInput') \
            .send_keys('getting started')
        self.teacher.find(By.ID, 'searchAskButton').click()
        self.teacher.page.wait_for_page_load()
        # check that Email Us button exists
        self.teacher.find(By.XPATH, '//a[contains(text(),"Email Us")]')
        # click on the FIRST article. Not random because for this test, I'm
        # choosing 2
        # different articles. Want them to be different, so choosing 1st then
        # 2nd articles
        self.teacher.find(By.CSS_SELECTOR, '.article a').click()
        # click feedback yes button
        self.teacher.find(By.XPATH, ".//*[@value='Yes']").click()
        # checks that "Thanks for your feedback" mesasge is displayed
        self.teacher.page.wait_for_page_load()
        self.teacher.find(
            By.XPATH, ".//*[contains(text(),'Thanks for your feedback!')]")

        # Back to search results
        self.teacher.find(
            By.XPATH,
            ".//*[contains(text(), 'Back to search results')]"
        ).click()
        # Click on a random article (not the first one)
        relatedArticles = self.teacher.find_all(
            By.CSS_SELECTOR, '.article a')
        relatedArticles[randint(1, len(relatedArticles) - 1)].click()
        self.teacher.sleep(1)
        # Click No
        self.teacher.find(By.XPATH, ".//*[@value='No']").click()
        self.teacher.find(By.CSS_SELECTOR, "#feedbackTextArea") \
            .send_keys('testing')
        self.teacher.find(By.XPATH, ".//*[@value='Submit']").click()
        self.teacher.find(
            By.XPATH,
            ".//*[contains(text(), 'Thanks for your feedback')]"
        )
        self.teacher.find(
            By.XPATH,
            ".//*[contains(text(), 'close window')]"
        ).click()
        self.teacher.find(
            By.XPATH,
            ".//*[contains(text(),'Thanks for your feedback!')]"
        )
        relatedlinks = self.teacher.find_all(
            By.CSS_SELECTOR, ".relatedLink")
        randnum = randint(1, len(relatedlinks) - 1)
        self.teacher.scroll_to(relatedlinks[randnum])
        relatedlinks[randnum].click()
        self.teacher.find(By.CSS_SELECTOR, ".mainTitle")

        self.ps.test_updates['passed'] = True

    # NOT IMPLEMENTED
    @pytest.mark.skipif(str(162249) not in TESTS, reason='Excluded')
    def test_setting_open_and_due_times_162249(self):
        """
        Go to tutor qa
        Log in as a teacher
        Click on a Tutor course name
        Click "Add Assignment"
        Click "Add Event"
        Click on the text box for the open time
        Enter desired time
        Click on the forward arrow to rotate the calendar to the course end
        date
        Click on the text box for the due time
        Enter desired time
        Click on the forward arrow to rotate the calendar to the course end
        date
        ***User is able to set open and due time. A due or open date cannot be
        set
        to after the end of term. The end of term can be viewed in Course
        Settings
        and Roster. The calendars cannot be rotated to view months after to
        the end of the course***

        Expected result:
        ***User is able to set open and due time. A due or open date cannot be
        set to after the end of term. The end of term can be viewed in Course
        Settings and Roster. The calendars cannot be rotated to view months
        after
         to the end of the course***

        Corresponding test cases: T3.09 023
        """
        self.ps.test_updates['name'] = 'tutor_event_teacher_162249 \
            + inspect.currentframe().f_code.co_name[4:]'
        self.ps.test_updates['tags'] = ['tutor', 'event', 'teacher', '162249']
        self.ps.test_updates['passed'] = False

        self.teacher.login()
        self.teacher.page.wait_for_page_load()
        # self.teacher.find(By.CSS_SELECTOR,
        # '.my-courses-item-title>a').click()
        # self.teacher.sleep(4)
        # length = self.teacher.get_course_list()
        courses = self.teacher.find_all(
            By.CSS_SELECTOR,
            '.my-courses-item-title>a'
        )
        courses[randint(0, len(courses) - 1)].click()
        """self.teacher.find_all(
            By.CSS_SELECTOR,
            '.my-courses-item-title>a')[randint(0,length)].click()"""
        try:
            self.admin.find(
                By.XPATH,
                './/*[contains(text(),"I don’t know yet")]'
            )
        except:
            pass
        self.teacher.find(By.CSS_SELECTOR, "a[href*='event']").click()

    @pytest.mark.skipif(str(162247) not in TESTS, reason='Excluded')
    def test_no_course_page_and_tutor_guides_162247(self):
        """
        Go to tutor qa as a teacher with 0 courses.
        ***See message "We cannot find an Openstax course associated with your
        account"***

        Click "Tutor Instructors. Get help >"

        Expected Result:

        ***Tutor Help Center opens in another tab with the Getting Started
        guide***

        Corresponding test cases: T2.18 002, 003

        https://trello.com/c/v6QAuJsB/17-teacher-not-in-any-courses-directed-to-a-no-courses-page-and-tutor-guides
        """
        self.ps.test_updates['name'] = 'tutor_help_center_teacher_162247' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = \
            ['tutor', 'help_center', 'teacher', '162247']
        self.ps.test_updates['passed'] = False

        # log in to demo teacher with 0 courses
        self.teacher.login(
            username=os.getenv('TEACHER_USER_DEMO'),
            password=os.getenv('TEACHER_DEMO_PASSWORD')
        )
        # check if the appropriate elements are present
        self.teacher.wait.until(
            expect.presence_of_element_located((
                By.XPATH,
                ".//*[@class='lead' and contains(text(), 'cannot find')]"
            ))
        )
        self.teacher.wait.until(
            expect.element_to_be_clickable((
                By.XPATH,
                ".//*[@target and contains(text(), 'Instructors.')]"
            ))
        ).click()

        self.ps.test_updates['passed'] = True

    # NEED TO TEST
    @pytest.mark.skipif(str(162250) not in TESTS, reason='Excluded')
    def test_editing_course_settings_162250(self):
        """
        Go to tutor qa
        Log in as a teacher
        If the user has more than one course, click on a Tutor course name
        Click on the user menu in the upper right corner of the page
        Click "Course Settings and Roster"
        Click a period tab
        Click the "Rename" button
        ***Observe that period is renamed***

        Enter a new course name
        Click the "Rename" button
        ***Observe that course name is editted***

        Click the "Remove" button for an instructor under the Instructors
        section

        Click "Remove" on the box that pops up

        Expected result:

        ***The instructor is removed from the Instructors list***

        Corresponding test cases: T1.42 001, 002, 005

        https://trello.com/c/Vix3YdiR/142-editting-course-settings
        """
        self.ps.test_updates['name'] = \
            'tutor_course_settings_and_roster_teacher_162250' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = \
            ['tutor', 'course_settings_and_roster', 'teacher', '162250']
        self.ps.test_updates['passed'] = False

        self.teacher.login()
        self.teacher.random_course()
        COURSETITLE = self.teacher.find(
                        By.CSS_SELECTOR,
                        '.book-title-text').get_attribute('innerHTML')
        self.teacher.goto_course_settings()

        # click rename period
        self.teacher.find(
            By.CSS_SELECTOR,
            '.control.rename-period.btn.btn-link'
        ).click()
        # store the current period name
        periodname = self.teacher.find(By.CSS_SELECTOR, '.form-control') \
            .get_attribute('value')
        # delete it
        self.teacher.find(By.CSS_SELECTOR, '.form-control') \
            .send_keys(Keys.BACKSPACE*10)
        self.teacher.sleep(.5)
        # rename the period as 'renamed'
        self.teacher.find(By.CSS_SELECTOR, '.form-control') \
            .send_keys('renamed')
        self.teacher.sleep(.5)
        # confirm renaming
        self.teacher.find(
            By.CSS_SELECTOR,
            '.async-button.-edit-period-confirm.btn.btn-default').click()
        self.teacher.sleep(2)

        # check that the editted name appears
        self.teacher.find(By.XPATH, './/*[contains(text(),"renamed")]')
        # rename period back to what it originally was
        self.teacher.find(By.XPATH, './/*[contains(text(),"renamed")]').click()
        self.teacher.find(
            By.CSS_SELECTOR,
            '.control.rename-period.btn.btn-link'
        ).click()
        self.teacher.find(By.CSS_SELECTOR, '.form-control') \
            .send_keys(Keys.BACKSPACE*10)
        self.teacher.find(By.CSS_SELECTOR, '.form-control') \
            .send_keys(periodname)
        self.teacher.find(
            By.CSS_SELECTOR,
            '.async-button.-edit-period-confirm.btn.btn-default'
        ).click()
        # check that original period name appears
        XPATHLINK = './/*[contains(text(),"%s")]' % (periodname)
        self.teacher.find(By.XPATH, XPATHLINK)
        self.teacher.find(
            By.CSS_SELECTOR,
            '.control.add-teacher.btn.btn-link'
        ).click()
        link = self.teacher.find(By.CSS_SELECTOR, '.copy-on-focus') \
            .get_attribute('value')
        self.teacher.find(By.CSS_SELECTOR, '.close').click()
        self.teacher.sleep(.5)
        # delete teacher
        self.teacher.find(
            By.XPATH,
            './/*[contains(text(),"Desiree")]/.././/*[@aria-describedby]'
        ).click()
        self.teacher.find(By.CSS_SELECTOR, '.async-button.btn.btn-danger') \
            .click()
        self.teacher.sleep(40)
        count = 0
        flag = True
        XPATHLINK = './/*[contains(text(),"%s")]' % (COURSETITLE)
        while count < 11 and flag:
            self.teacher.get(os.getenv('SERVER_URL') + '/dashboard')
            try:
                self.teacher.find(By.XPATH, XPATHLINK)
                flag = False
            except:
                count += 1
            self.teacher.sleep(5)
        self.teacher.get(link)

        self.ps.test_updates['passed'] = True

    @pytest.mark.skipif(str(162251) not in TESTS, reason='Excluded')
    def test_adding_and_deleting_instructors_162251(self):
        """
        Log in as a teacher
        Go to a course dashboard
        Go to the course roster
        Click Add an instructor
        Copy the link provided
        Log out
        Log in as a different teacher
        Go to the link
        ***New teacher is at the course dashboard***

        Click the "Remove" button for an instructor under the Instructors
        section
        Click "Remove" on the box that pops up

        Expected result:

        ***The instructor is removed from the Instructors list***


        Corresponding test case: T1.42 002, T3.09 018

        https://trello.com/c/Dl13SRCa/153-provide-a-registration-link-to-co-teachers
        """
        self.ps.test_updates['name'] = \
            'tutor_course_settings_and_roster_teacher_162251' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = \
            ['tutor', 'course_settings_and_roster', 'teacher', '162251']
        self.ps.test_updates['passed'] = False

        self.teacher.login(
            username=os.getenv('CONTENT_USER'),
            password=os.getenv('CONTENT_PASSWORD')
        )
        self.teacher.random_course()
        COURSETITLE = self.teacher.find(
                        By.CSS_SELECTOR,
                        '.book-title-text').get_attribute('innerHTML')
        self.teacher.goto_course_settings()
        # click add instructor
        self.teacher.find(
            By.CSS_SELECTOR,
            '.control.add-teacher.btn.btn-link'
        ).click()
        # get instructor link
        link = self.teacher.find(By.CSS_SELECTOR, '.copy-on-focus') \
            .get_attribute('value')
        self.teacher.find(By.CSS_SELECTOR, '.close').click()
        # log onto diff teacher
        self.teacher.logout()
        self.teacher.login()
        # enter instructor link
        self.teacher.get(link)
        self.teacher.goto_course_settings()
        # click on remove instructor corresponding to teacher name
        self.teacher.find(
            By.XPATH,
            './/*[contains(text(),"Desiree")]/.././/*[@aria-describedby]'
        ).click()
        self.teacher.find(By.CSS_SELECTOR, '.async-button.btn.btn-danger') \
            .click()
        count = 0
        XPATHLINK = './/*[contains(text(),"%s")]' % (COURSETITLE)
        # refresh dashboard 10 times every 5 seconds to see if course title of
        # course you deleted is there. If it is, break out of the for loop
        # if it doesn't then you fail
        flag = False
        while count < 11 and not flag:
            self.teacher.get(os.getenv('SERVER_URL') + '/dashboard')
            try:
                self.teacher.find(By.XPATH, XPATHLINK)
                count += 1
            except:
                flag = True
            self.teacher.sleep(5)
        # fails if you can still see course in dashboard
        assert(flag), 'flag still True'

        self.ps.test_updates['passed'] = True
