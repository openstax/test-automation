"""
Title: test edit settings
Consists of:
-test district:  C148077
-test school: C148078
-test course: C148079
-test periods: C148081
-test teachers: C148080
-test course ecosystem: C148082
-test student roster: C148083

User(s): admin


Jacob Diaz
7/26/17


Corresponding Case(s):
T1.59 01 --> 20


Progress:
None

Work to be done/Questions:
Needs to be written. Code copied from t1.59 and worked together

Merge-able with any scripts? If so, which? :
not that I can think of

"""

# import inspect
import json
import os
# import pytest
import unittest
# import datetime

from pastasauce import PastaSauce, PastaDecorator
# from random import randint
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as expect
# from staxing.assignment import Assignment
# from selenium.webdriver.common.keys import Keys

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

# DECIDE WHICH OF THESE YOU WANT TO PUT TOGETHER --> YOU CAN COMPRESS A BIT


@PastaDecorator.on_platforms(BROWSERS)
class TestManageDistricsSchoolsAndCourses(unittest.TestCase):

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

    def test_district_admin(self):
        """
        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Login to admin account
        Click on the 'Sign in' button

        Click on the user menu in the right corner of the header
        Click "Admin"
        Click "Course Organization" in the header
        Click "Districts"
        Click "Add district"
        Enter a name for the district in the Name text box
        Click "Save"
        ***A new district is added and the user is returned to the 'Districts'
        section (t1.59.01)***

        Click "edit" for a district
        Enter a new name into the Name text box
        Click "Save"
        ***A district's name is changed (t1.59.02) and user should be returned
        to 'Districts' section***

        Click "delete" for the desired district
        Click "OK" on the dialogue box
        ***An existing district is deleted (t1.59.03)***

        Corresponds to...
        T1.59 01 --> 3
        :return:
        """

    def test_school_admin(self):
        """
        Go to https://tutor-qa.openstax.org/
        Login to admin account
        Click on the 'Sign in' button

        Click on the user menu in the right corner of the header
        Click "Admin"
        Click "Course Organization" in the header
        Click "Schools"
        Click "Add school"
        Enter a name for the school in the Name text box
        Click "Save"
        ***A new school is added and the user is returned to the 'Schools'
        section (t1.59.04)***

        Click "edit" for a school
        Enter a new name into the Name text box
        Click "Save"
        ***A school's name is changed (t1.59.05) and user should be returned
        to 'School' section***

        Click "edit" for the desired school
        Select a new district
        Click "Save"
        ***A school's district is changed (t1.59.06)***

        Click "delete" for the desired school
        Click "OK" on the dialogue box
        ***An existing school is deleted (t1.59.07)***

        Corresponds to...
        T1.59 04 --> 07
        :return:
        """

    def test_course_admin(self):
        """
        Pre-req: 'Course-Navigate'

        Click "Add course"
        Enter a name in the Name text box
        Click "Save"
        ***A new course is added and the user is returned to the 'Courses'
        section (t1.59.08)***


        Click "Edit" for a school
        Change information in desired text boxes
        Click "Save"
        ***The course is edited (t1.59.09) and user should be returned to list
        of all courses***


        Corresponds to...
        T1.59 08--> 9
        :return:
        """

    def test_periods_admin(self):
        """
        Pre-Req "Course-Navigate"

        Click "Edit" on the desired course
        Click the "Periods" tab
        Click "Add Period"
        Enter a name into the Name text box
        Click "Save"
        ***A new empty period is added (t1.59.14)***


        Click "Edit" on the desired course
        Click the "Periods" tab
        Click "Edit" for the desired period
        enter new information into the name and enrollment code text boxes
        Click on the "Save" button
        ***Period is edited (t1.59.15)***


        Click "Edit" on the desired course
        Click the "Periods" tab
        Click "Delete" for an empty period
        ***Empty period is deleted (t1.59.16)***

        Click "Edit" on the desired course
        Click the "Periods" tab
        Click "Delete" on a non-empty period
        ***A non-empty period is deleted (t1.59.17)***


        Corresponds to...
        t1.59 14 --> 17
        :return:
        """

    def test_teachers_admin(self):
        """
        Click "Edit" on the desired course
        Click the "Teachers" tab
        Enter the teacher's name or the username into the search engine
        Click on the name that matches the teacher's name or the username
        ***A teacher is added to a course
        (t1.59.10) and user directed back to the 'Courses' section***


        Click "Edit" on the desired course
        Click the "Teachers" tab
        Click "Remove from course" for the desired teacher
        Click "OK" on the dialogue box
        ***A teacher is removed from a course (t1.59.11)***


        Corresponds to...
        t1.59. 10,11
        :return:
        """

    def test_course_ecosystem_admin(self):
        """
        Pre-req: 'Course Navigate'

        Click "edit" on the desired course
        Click the "course content" tab
        Select a course ecosystem
        Click "Submit"
        ***Request for course ecosystem update submitted and message displayed
        (t1.59.12)***

        Click "edit" on the desired course
        Click the "course content" tab
        Select a course ecosystem
        Click "Submit"
        ***The course ecosystem is queued for the course (t1.59.13)***

        Check the desired courses to update
        Scroll to the bottom of the page
        Select an ecosystem
        Click "Set ecosystem"
        ***The message "Course ecosystem update background jobs queued"
        appears beneath the page title "Courses" (t1.59.19)***

        CORRESPONDS TO...
        T1.59 12,13,19
        :return:
        """

    def test_tutor_student_count_admin(self):
        """
        Pre-Req: Course Navigation

        Click "Edit" on the desired course
        Click the "Student Roster" tab
        If there are more than one period, select a period
        Click "Choose File"
        Select a file
        Click "Upload
        ***A student roster is uploaded to a period (t1.59.18)***
        NO IMPLEMENTATION CODED YET!!

        Click on the user menu in the right corner of the header
        Click "Admin"
        Click "Stats" in the header
        Click "Courses"
        ***The user views the Tutor course counts (t1.59.20)***

        Corresponds to. t1.59 (18,20)
        :return:
        """
