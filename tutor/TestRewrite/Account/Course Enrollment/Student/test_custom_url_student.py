"""
System: Accounts
User(s): Student
Title: TEST CUSTOM URL
Testrail ID: C148110

Jacob Diaz
7/26/17


Corresponding Case(s):
# t2.09 04,33

Progress:
Almost

Work to be done/Questions:
Test it, add code to those parts not working
Also add code to the parts where I've commented

Merge-able with any scripts? If so, which? :
I don't believe so

"""


# import inspect
import json
import os
# import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
# from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
# from staxing.assignment import Assignment
from selenium.webdriver.common.keys import Keys
# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Teacher, Student, Admin

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
        14761, 14796, 85292
        # not implemented
        # 14762, 14763, 14764, 14767,
        # 14768, 14783, 14784, 14787, 14789,
        # 14790, 14791, 14792, 14793, 14794,
        # 14795,
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestImproveLoginREgistrationEnrollment(unittest.TestCase):
    """T2.09 - Improve Login, Registration, Enrollment."""

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
                capabilities=self.desired_capabilities
            )
            self.admin = Admin(
                use_env_vars=True,
                pasta_user=self.ps,
                capabilities=self.desired_capabilities
            )
        else:
            self.teacher = Teacher(
                use_env_vars=True,
            )
            self.student = Student(
                use_env_vars=True,
                existing_driver=self.teacher.driver
            )
            self.admin = Admin(
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

    def test_custom_url_student(self):
        """
        Enter the custom URL into the search bar
        Sign in or sign up as student
        Enter a school-issued ID or skip the step for now

        ***The user is presented with the student dashboard with the message
        "Enrollment successful!
        It may take a few minutes to build your assignments."
        (If student is already enrolled in course message notifies student of
        this)(t2.09.04)***

        Click on a course
        Open the user menu
        click on "Change Student ID"
        Enter an new Student ID
        Click save
        ***Student ID changed (t2.09.33)***

        Corresponds to...
        t2.09 04,33
        """
        # t2.09.04 -->The user is presented with the
        # student dashboard with the message "Enrollment successful!
        # It may take a few minutes to build your assignments."
        # If student is already enrolled in course message notifies student of
        # this)(t2.09.04)***

        self.teacher.login()
        # self.teacher.find(By.XPATH, '//p[@data-is-beta="true"]').click()
        # self.teacher.open_user_menu()
        # self.teacher.find(By.LINK_TEXT, 'Course Settings and Roster').click()
        # IDK if above code is necessary for going to Course settings ^
        # make sure class is tutor
        self.teacher.find(
            By.XPATH,
            "//p[contains(text(),'Tutor')]"
        ).click()

        # get name of course for later reference by the student
        enrollment_course_name = self.teacher.find(
            By.XPATH,
            "//a[contains(@class,'course-name')]"
        ).text
        print(enrollment_course_name)

        # go to roster
        self.teacher.goto_course_roster()
        enrollment_url = self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//span[@class="enrollment-code-link"]//input')
            )
        ).get_attribute("value")
        self.teacher.logout()

        # use the url as a student
        self.student.login()
        custom_url = self.student.get(enrollment_url)
        print(custom_url)
        self.student.sleep(5)
        try:
            get_started = self.student.find(
                By.XPATH,
                "//a[contains(text(),'Get started')]"
            )
            get_started.click()

            # student id "Add Later"
            add_later = self.student.find(
                By.XPATH,
                "//button[contains(text(),'later')]"
            )
            add_later.click()
        except:
            pass

        # NOT FINISHED --> NEED TO WORK ON THE CODE THAT'LL ENROLL THE STUDENT
        # AND CLICK THROUGH THE ENROLLMENT FLOW

        # t2.09.33 --> Student ID changed
        self.student.find(By.XPATH, '//p[@data-is-beta="true"]').click()
        self.student.open_user_menu()
        self.student.find(By.LINK_TEXT, 'Change Student ID').click()
        old_id = self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//input[@placeholder="School issued ID"]')
            )
        ).get_attribute("value")

        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//input[@placeholder="School issued ID"]')
            )
        ).send_keys("new_student_id")

        self.student.find(
            By.XPATH, '//button[text()="Save"]'
        ).click()

        # change the student ID back
        self.student.sleep(3)
        self.student.open_user_menu()
        self.student.find(By.LINK_TEXT, 'Change Student ID').click()
        new_id = self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//input[@placeholder="School issued ID"]')
            )
        ).get_attribute("value")

        assert(old_id+"new_student_id" == new_id), "ID not changed"

        for _ in range(14):
            self.student.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//input[@placeholder="School issued ID"]')
                )
            ).send_keys(Keys.BACKSPACE)
        self.student.find(
            By.XPATH, '//button[text()="Save"]'
        ).click()
