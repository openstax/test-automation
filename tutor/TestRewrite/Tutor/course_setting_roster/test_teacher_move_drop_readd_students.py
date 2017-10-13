"""Tutor, Course Settings and Roster - Move, Drop and Readd Students."""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
# from random import randint
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as expect

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Teacher  # , Admin

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
        162189
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestEditCourseSettingsAndRoster(unittest.TestCase):
    """T1.42 - Edit Course Settings and Roster."""

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

    # Case 162189 - 002 - Teacher | Move, Drop, and Readd a Student
    @pytest.mark.skipif(str(162189) not in TESTS, reason='Excluded')
    def test_teacher_mover_a_student_to_another_period_162189(self):
        """

        #STEPS
        Go to Tutor
        Click on the 'Login' button
        Enter the teacher username [ ] in the username text box
        Click 'Next'
        Enter the teacher password [ ] in the password text box
        Click on the 'Login' button
        Click on a Tutor course name
        ***The user selects a course and is presented with the calendar
        dashboard.***

        Click on the user menu in the upper right corner of the page
        Click "Course Settings and Roster"
        Click "Change Section" for a student under the student section
        Click the desired section to move a student
        Click the section the student was moved to
        ***A student is moved to another section***

        Click "Drop" for a student under the student section
        Click "Drop" in the box that pops up
        ***A student is dropped from the course and is put under the Dropped
        Students section***

        Click "Add Back to Active Roster" for a student under the Dropped
        Students section
        Click "Add" on the box that pops up

        # EXPECTED RESULT
        ***A student is added back to the course***

        """
        # Test steps and verification assertions
        self.ps.test_updates['name'] = 't1.42.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.42', 't1.42.008', '162189']
        self.ps.test_updates['passed'] = False

        # Select a course and see the calendar dashboard
        self.teacher.select_course(appearance='intro_sociology')
        self.teacher.open_user_menu()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Course Settings and Roster')
            )
        ).click()
        self.teacher.page.wait_for_page_load()

        # Move Students
        self.teacher.find(
            By.XPATH, '//a[@aria-describedby="change-period"]').click()
        student_name = self.teacher.find(
            By.XPATH, '//div[@class="roster"]//td').text
        element = self.teacher.find(
            By.XPATH, '//div[@class="popover-content"]//a')
        period_name = element.text
        element.click()
        self.teacher.sleep(1)
        self.teacher.find(
            By.XPATH, '//a/h2[contains(text(),"'+period_name+'")]').click()
        self.teacher.driver.find_element(
            By.XPATH, '//td[contains(text(),"%s")]' % student_name)

        # Drop Student
        student_name = self.teacher.find(
            By.XPATH, '//div[@class="roster"]//td').text
        self.teacher.find(
            By.XPATH, '//a[@aria-describedby="drop-student"]').click()
        self.teacher.find(
            By.XPATH, '//div[@class="popover-content"]//button').click()
        self.teacher.sleep(1)
        # check that student was dropped
        self.teacher.find(
            By.XPATH, '//div[contains(@class,"dropped-students")]' +
            '//td[contains(text(),"%s")]' % student_name
        )

        # Readd Student
        # add a student back (not necessarily the same student)
        self.teacher.find(
            By.XPATH,
            '//a[@aria-describedby="drop-student-popover-1216"]'
        ).click()
        self.teacher.find(
            By.XPATH, '//div[@class="popover-content"]//button').click()
        self.teacher.sleep(1)
        # check that student was added back
        self.teacher.find(
            By.XPATH,
            '//div[@class="roster"]//td[contains(text(),"%s")]' % student_name)

        self.ps.test_updates['passed'] = True
