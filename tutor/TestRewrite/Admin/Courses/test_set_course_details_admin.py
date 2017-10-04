"""
System: ??
Title: test set course details
User(s): Admin
Testrail ID: C148074


Jacob Diaz
7/26/17


Corresponding Case(s):
t1.59 21 --> 26

Progress:
Written, works


Work to be done/Questions:
Way by which we work with the calendar is a little screwy,
given that both the end and start date calendars
have the exact same XPATH here

Merge-able with any scripts? If so, which? :
Maybe with other admin scripts? They all start out at the admin control
console, so we could make
the setup start them there

"""
# import inspect
import json
import os
# import pytest
import unittest
import datetime

from pastasauce import PastaSauce, PastaDecorator
# from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from staxing.assignment import Assignment
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Admin

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
        8341, 8342, 8343, 8344, 8345,
        8346, 8347, 8348, 8349, 8350,
        8351, 8352, 8353, 8354, 8355,
        8356, 8357, 8358, 8359, 8360,
        100135, 100136, 100137, 100138, 100139,
        100140
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestManageDistricsSchoolsAndCourses(unittest.TestCase):
    """T1.59 - Manage districts, schools, and courses."""

    def setUp(self):
        """Pretest settings."""
        # login as admin, go to user menu, click admin option
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        if not LOCAL_RUN:
            self.admin = Admin(
                use_env_vars=True,
                pasta_user=self.ps,
                capabilities=self.desired_capabilities
            )
        else:
            self.admin = Admin(
                use_env_vars=True,
            )
        self.wait = WebDriverWait(self.admin.driver, Assignment.WAIT_TIME)
        self.admin.login()
        self.admin.goto_admin_control()

    def tearDown(self):
        """Test destructor."""
        if not LOCAL_RUN:
            self.ps.update_job(
                job_id=str(self.admin.driver.session_id),
                **self.ps.test_updates
            )
        try:
            self.admin.delete()
        except:
            pass

    def test_set_course_details_admin(self):
        """
        Pre-req: "Course-Navigate"

        Log into Admin
        Click on user name for drop down
        Click on 'Admin' option in menu
        Click on 'Course Organization' for dropdown menu
        Click on 'Courses'
        Click on 'Edit'

        Type new course scholastic year into 'Year' text-book
        ***(t1.59.21)***

        Type new number into number of sections
        ***(t1.59.22)***

        Set the course start date and time under the 'Starts at' text box
        ***(t1.59.23)***

        Set the course end date and time under the 'Ends at' textbox
        ***(t1.59.24)***

        Set the course offering under the 'Catalog Offering' dropdown
        ***(t1.59.25)***

        Set the course offering appearance code under the 'Appearance Code'
        dropdown
        ***(t1.59.26)***

        Click 'Course duration'
        ***End and start dates should be displayed (t2.07.11)***

        Corresponds to...
        t1.59 21 --> 26
        :return:
        """
        # t1.59.21 --> Type new course scholastic year into 'Year' text-book

        # Setup() leaves you at the admin control
        self.admin.goto_course_list()

        # Create the course
        create_new_course = self.admin.find(
            By.XPATH,
            "//a[text()='Add Course']"
        )

        self.admin.driver.execute_script(
            'return arguments[0].scrollIntoView();',
            create_new_course
        )

        create_new_course.click()

        self.admin.find(
            By.ID, "course_year"
        ).send_keys((Keys.DELETE * 4) + str(datetime.date.today().year))

        # t1.59.22 --> Type new number into number of sections

        self.admin.find(
            By.ID, "course_num_sections"
        ).send_keys((Keys.DELETE) + str(1))

        # t1.59.23 -->Set the course start date and time under the 'Starts at'
        # text box

        self.admin.find(By.ID, "course_starts_at").click()
        self.admin.sleep(1)
        next_calendar_arrows = self.admin.find_all(
            By.XPATH,
            '//div[contains(@class,"datepicker")]' +
            '//button[contains(@class,"_next")]'
        )
        # next_calendar_arrows[0].click() # have to find all because the two
        # right arrows for the
        # start and end date have identical xpath's --> doing this allows us to
        # pick the first or second

        # get the date
        right_now = datetime.datetime.now()
        hour_plus_one = str(right_now.replace(hour=right_now.hour + 1).hour)
        month_now = str(right_now.replace(month=right_now.month-1).month)
        # months are 1 minus their actual number
        month_plus_one = str(right_now.month)
        print(right_now)
        print(month_now)
        print(hour_plus_one)
        print(month_plus_one)

        self.admin.find(
            By.XPATH,
            '//div[contains(@class,"calendar")]' +
            '//td[@data-date="1" and @data-month="{0}"]'.format(month_now)
        ).click()

        # Choose start date
        self.wait.until(
            expect.visibility_of_element_located((
                By.XPATH,
                '//div[contains(@class,"timepicker")]' +
                '//div[@data-hour="{0}"]'.format(hour_plus_one)
            ))
        ).click()

        # t1.59.24 --> Set the course end date and time under the 'Ends at'
        # textbox
        # Choose end date

        self.admin.find(By.ID, "course_ends_at").click()
        self.admin.sleep(1)
        next_calendar_arrows[-1].click()
        self.admin.find_all(
            By.XPATH,
            '//div[contains(@class,"calendar")]' +
            '//td[@data-date="1" and @data-month="{0}"]'.format(month_plus_one)
        )[-1].click()

        self.admin.sleep(5)
        # choose end time
        self.admin.find_all(
            By.XPATH,
            '//div[contains(@class,"timepicker")]' +
            '//div[@data-hour="{0}"]'.format(hour_plus_one)
        )[-1].click()

        # t1.59.25 --> Set the course offering under the 'Catalog Offering'
        # dropdown

        self.admin.find(By.ID, "course_catalog_offering_id").click()
        self.admin.find(
            By.XPATH,
            '//select[@id="course_catalog_offering_id"]/option[2]'
        ).click()

        # t1.59.26 -->Set the course offering appearance code under the
        # 'Appearance Code' dropdown

        self.admin.find(By.ID, "course_appearance_code").click()
        self.admin.find(
            By.XPATH,
            '//select[@id="course_appearance_code"]/option[2]'
        ).click()
