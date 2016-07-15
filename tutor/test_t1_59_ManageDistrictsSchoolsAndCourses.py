"""Tutor v1, Epic 59 - ManageDistricsSchoolsAndCourses."""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
from random import randint  # NOQA
from selenium.webdriver.common.by import By  # NOQA
from selenium.webdriver.support import expected_conditions as expect  # NOQA
from staxing.assignment import Assignment  # NOQA

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Admin  # NOQA

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': '50.0',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([8341, 8342, 8343, 8344, 8345, 
    	 8346, 8347, 8348, 8349, 8350,
	 8351, 8352, 8353, 8354, 8355,
	 8356, 8357, 8358, 8359, 8360])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestManageDistricsSchoolsAndCourses(unittest.TestCase):
    """T1.59 - Manage districts, schools, and courses."""

    def setUp(self):
        """Pretest settings."""
	##login as admin, go to user menu, click admin option
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.Teacher = Teacher(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )

    def tearDown(self):
        """Test destructor."""
        self.ps.update_job(job_id=str(self.teacher.driver.session_id),
                           **self.ps.test_updates)
        try:
            self.teacher.delete()
        except:
            pass

    # Case C8341 - 001 - Admin | Add a new district
    @pytest.mark.skipif(str(8341) not in TESTS, reason='Excluded')  # NOQA
    def test_admin_add_a_new_district(self):
        """Add a new district

        Steps:
	Click Course Organization in the header
	Click on Districts
	Click on Add district
	Enter a name for the district in the Name Text box
	Click Save

        Expected Result:
	A new district is added
        """
        self.ps.test_updates['name'] = 't1.59.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.001', '8341']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8342 - 002 - Admin | Change a district's name
    @pytest.mark.skipif(str(8342) not in TESTS, reason='Excluded')  # NOQA
    def test_admin_change_a_districts_name(self):
        """Change a district's name

        Steps:
	Click Course Organization in the header
	Click on Districts
	Click on edit next to a district
	Enter a name into the Name text box
	Click Save

        Expected Result:
	A district's name is changed
        """
        self.ps.test_updates['name'] = 't1.59.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.002', '8342']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8343 - 003 - Admin | Delete an exisiting district
    @pytest.mark.skipif(str(8343) not in TESTS, reason='Excluded')  # NOQA
    def test_admin_delete_an_existing_district(self):
        """Delete an existing district

        Steps:
	Click Course Organization in the header
	Click on Districts
	Click on delete next to a district
	Click OK in the dialouge box

        Expected Result:
	A district is deleted
        """
        self.ps.test_updates['name'] = 't1.59.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.003', '8343']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8344 - 004 - Admin | Add a new school
    @pytest.mark.skipif(str(8344) not in TESTS, reason='Excluded')  # NOQA
    def test_admin_add_a_new_school(self):
        """Add a new school

        Steps:
	Click Course Organization in the header
	Click on Schools
	Click on Add School
	Enter a name into the Name text box
	Select a district
	Click Save

        Expected Result:
	A school is added
        """
        self.ps.test_updates['name'] = 't1.59.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.004', '8344']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8345 - 005 - Admin | Change a school's name
    @pytest.mark.skipif(str(8345) not in TESTS, reason='Excluded')  # NOQA
    def test_admin_change_a_schools_name(self):
        """Change a school's name

        Steps:
	Click Course Organization in the header
	Click on Schools
	Click edit next to a school
	Enter a new name in the Name text box
	Click Save

        Expected Result:
	A school's name is changed
        """
        self.ps.test_updates['name'] = 't1.59.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.005', '8345']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8346 - 006 - Admin | Change a school's district
    @pytest.mark.skipif(str(8346) not in TESTS, reason='Excluded')  # NOQA
    def test_admin_change_a_schools_district(self):
        """Change a school's district

        Steps:
	Click Course Organization in the header
	Click on Schools
	Click edit next to a school
	Select a new district
	Click Save

        Expected Result:
	A school's district is changed
        """
        self.ps.test_updates['name'] = 't1.59.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.006', '8346']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8347 - 007 - Admin | Delete an exisiting school
    @pytest.mark.skipif(str(8347) not in TESTS, reason='Excluded')  # NOQA
    def test_admin_delete_an_existing_school(self):
        """Delete an exisitng school

        Steps:
	Click Course Organization in the header
	Click on Schools
	Click delete next to a school
	Click OK on the dialouge box

        Expected Result:
	A school is deleted
        """
        self.ps.test_updates['name'] = 't1.59.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.007', '8347']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8348 - 008 - Admin | Add a new course
    @pytest.mark.skipif(str(8348) not in TESTS, reason='Excluded')  # NOQA
    def test_admin_add_a_new_course(self):
        """Add a new course

        Steps:
	Click Course Organization in the header
	Click on Courses
        Click Add Course at the bottom of the page
	Enter a name into the Name text box
	Select a school
	Select a catalog offering
	Click Save
        
        Expected Result:
	A new school is added
        """
        self.ps.test_updates['name'] = 't1.59.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.008', '8348']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8349 - 009 - Admin | Edit course settings
    @pytest.mark.skipif(str(8349) not in TESTS, reason='Excluded')  # NOQA
    def test_admin_edit_course_settings(self):
        """Edit course settings

        Steps:
	Click Course Organization in the header
	Click on Courses
        Click Edit next to a course
	Change information in the Name textbox
	Change selected School and catalog offering
	Click the Save button
        
        Expected Result:
	Course is edited
        """
        self.ps.test_updates['name'] = 't1.59.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.009', '8349']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8350 - 010 - Admin | Add a teacher to a course
    @pytest.mark.skipif(str(8350) not in TESTS, reason='Excluded')  # NOQA
    def test_admin_add_a_teacher_to_a_course(self):
        """Add a teacher to a course

        Steps:
	Click Course Organization in the header
	Click on Courses
        Click Edit next to a course
	Click on the Teacher tab
	Enter a teachers name or username into the search box
	Click on the name of selected teacher
        
        Expected Result:
	A teacher is added to the course
        """
        self.ps.test_updates['name'] = 't1.59.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.010', '8350']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8351 - 011 - Admin | Remove a teacher from a course
    @pytest.mark.skipif(str(8351) not in TESTS, reason='Excluded')  # NOQA
    def test_admin_remove_a_teacher_from_a_course(self):
        """Remove a teacher from a course

        Steps:
	Click Course Organization in the header
	Click on Courses
        Click Edit next to a course
	Click on the Teacher tab
	Click Remove from course for desired teacher
	Click OK in the dialogue box
        
        Expected Result:
	A teacher is revmoved from the course
        """
        self.ps.test_updates['name'] = 't1.59.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.011', '8351']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8352 - 012 - Admin | Set the course ecosystem
    @pytest.mark.skipif(str(8352) not in TESTS, reason='Excluded')  # NOQA
    def test_admin_set_the_course_ecosystem(self):
        """Set the course ecosystem

        Steps:
	Click Course Organization in the header
	Click on Courses
        Click Edit next to a course
	Click on the Course Content tab
	Select a course ecosystem
	Click Submit
        
        Expected Result:
	Request for a course ecosystem update submited and message displayed
        """
        self.ps.test_updates['name'] = 't1.59.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.012', '8352']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8353 - 013 - Admin | Update the course ecosystem
    @pytest.mark.skipif(str(8353) not in TESTS, reason='Excluded')  # NOQA
    def test_admin_update_the_course_ecosystem(self):
        """Update the course ecosystem

        Steps:
	Click Course Organization in the header
	Click on Courses
        Click Edit next to a course
	Click on the Course Content tab
	Select a course ecosystem
	Click Submit
        
        Expected Result:
	The course ecosystem is queued for the course
        """
        self.ps.test_updates['name'] = 't1.59.013' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.013', '8353']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8354 - 014 - Admin | Add a period
    @pytest.mark.skipif(str(8354) not in TESTS, reason='Excluded')  # NOQA
    def test_admin_add_a_period(self):
        """Add a period

        Steps:
	Click Course Organization in the header
	Click on Courses
        Click Edit next to a course
	Click on the Periods tab
	Click Add Period
	Enter a name into the Name text box
	Click Save
        
        Expected Result:
	A new period is added
        """
        self.ps.test_updates['name'] = 't1.59.014' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.014', '8354']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8355 - 015 - Admin | Edit a period
    @pytest.mark.skipif(str(8355) not in TESTS, reason='Excluded')  # NOQA
    def test_admin_edit_a_period(self):
        """Edit a period

        Steps:
	Click Course Organization in the header
	Click on Courses
        Click Edit next to a course
	Click on the Periods tab
	Click Edit next to a period
	Enter a new information into the Name and enrollment code text boxes
	Click Save
        
        Expected Result:
	A period is edited
        """
        self.ps.test_updates['name'] = 't1.59.015' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.015', '8355']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8356 - 016 - Admin | Delete an empty period
    @pytest.mark.skipif(str(8356) not in TESTS, reason='Excluded')  # NOQA
    def test_admin_delete_an_empty_period(self):
        """Delete an empty period

        Steps:
	Click Course Organization in the header
	Click on Courses
        Click Edit next to a course
	Click on the Periods tab
	Click Edit next to a period
	Click Delete for an empty period
        
        Expected Result:
	A period is deleted
        """
        self.ps.test_updates['name'] = 't1.59.016' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.016', '8356']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8357 - 017 - Admin | Delete an non-empty period
    @pytest.mark.skipif(str(8357) not in TESTS, reason='Excluded')  # NOQA
    def test_admin_delete_a_non_empty_period(self):
        """Delete a non-empty period

        Steps:
	Click Course Organization in the header
	Click on Courses
        Click Edit next to a course
	Click on the Periods tab
	Click Edit next to a period
	Click Delete for a non-empty period
        
        Expected Result:
	A red text box that says 'Students must be moved to another
	period before this period can be deleted' pops up, and the
	period cannot be deleted
        """
        self.ps.test_updates['name'] = 't1.59.017' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.017', '8357']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8358 - 018 - Admin | Upload a student roster to a period
    @pytest.mark.skipif(str(8358) not in TESTS, reason='Excluded')  # NOQA
    def test_admin_upload_a_student_roster_to_a_period(self):
        """Upload a student roster to a period

        Steps:
	Click Course Organization in the header
	Click on Courses
        Click Edit next to a course
	Click on the Student Roster tab
	Select a period
	Click the Choose File button
	Select a file
	Click Upload
        
        Expected Result:
	A student roster is uploaded, confirmation message displayed
        """
        self.ps.test_updates['name'] = 't1.59.018' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.018', '8358']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8359 - 019 - Admin | Bulk update course ecosystems
    @pytest.mark.skipif(str(8359) not in TESTS, reason='Excluded')  # NOQA
    def test_admin_bulk_update_course_ecosystems(self):
        """Bulk update course ecosystems

        Steps:
	Click Course Organization in the header
	Click on Courses
        Check the checkboxes for selected courses
	Scroll to the bottom of the page
	Select an ecosystem
	Click Set ecosystem
        
        Expected Result:
	The message 'Course ecosystem update background jobs queued' is displayed
        """
        self.ps.test_updates['name'] = 't1.59.019' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.019', '8359']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8360 - 020 - Admin | View the Tutor course counts
    @pytest.mark.skipif(str(8320) not in TESTS, reason='Excluded')  # NOQA
    def test_admin_view_the_tutor_course_counts(self):
        """View the Tutor course counts

        Steps:
	Click Stats in the header
	Click on Courses
        
	Expected Result:
        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)
