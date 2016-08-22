"""Concept Coach v1, Epic 10 - Admin and Teacher Course Setup."""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
# from random import randint
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as expect
# from staxing.assignment import Assignment

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Admin, Teacher

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
        7715, 7716, 7717, 7718, 7719,
        7720, 7721, 7722, 7723, 7724,
        7725, 7726, 7727, 7728, 7729,
        7730, 7731
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestAdminAndTeacherCourseSetup(unittest.TestCase):
    """CC1.10 - Admin and Teacher Course Setup."""

    def setUp(self):
        """Pretest settings."""
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.teacher = Teacher(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        self.admin = Admin(
            use_env_vars=True,
            existing_driver=self.teacher.driver
        )

    def tearDown(self):
        """Test destructor."""
        self.ps.update_job(
            job_id=str(self.teacher.driver.session_id),
            **self.ps.test_updates
        )
        try:
            self.admin.driver = None
            self.teacher.delete()
        except:
            pass

    # Case C7715 - 001 - Admin | Send course setup data from Sales Force
    @pytest.mark.skipif(str(7715) not in TESTS, reason='Excluded')
    def test_admin_send_course_setup_data_from_sales_force_7715(self):
        """Send course setup data from Sales Force.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 'cc1.10.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.10',
            'cc1.10.001',
            '7715'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7716 - 002 - System | Course registration codes are emailed to the
    # teacher once the course is set up
    @pytest.mark.skipif(str(7716) not in TESTS, reason='Excluded')
    def test_system_registration_codes_are_emailed_to_teacher_7716(self):
        """Registration codes are emailed to teacher once the course is set up.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 'cc1.10.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.10',
            'cc1.10.002',
            '7716'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7717 - 003 - Teacher | Use a teacher registration code to access
    # their course
    @pytest.mark.skipif(str(7717) not in TESTS, reason='Excluded')
    def test_teacher_use_teacher_registration_code_to_access_course_7717(self):
        """Use a teacher registration code to access their course.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 'cc1.10.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.10',
            'cc1.10.003',
            '7717'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7718 - 004 - Teacher | Create course periods
    @pytest.mark.skipif(str(7718) not in TESTS, reason='Excluded')
    def test_teacher_create_course_periods_7718(self):
        """Create course periods.

        Steps:
        go to Tutor
        Log in as a teacher
        Click on a Concept Coach book
        Click on the user menu
        Select course roster
        Click "+ Add section"
        Enter a section name into the section Name text box

        Expected Result:
        New course section created
        """
        self.ps.test_updates['name'] = 'cc1.10.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.10',
            'cc1.10.004',
            '7718'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7719 - 005 - Teacher | View student enrollment code for
    # course period
    @pytest.mark.skipif(str(7719) not in TESTS, reason='Excluded')
    def test_teacher_view_student_enrollment_code_for_course_period_7719(self):
        """View the student enrollment code for a course period.

        Steps:
        Go to Tutor
        Log in as a teacher
        Click on a Concept Coach book
        Click on the user menu
        Select course roster
        Click on tab for selected section
        Click 'Get Student Enrollment Code'

        Expected Result:
        Student Enrollment code displayed along with instruction teacher can
        send to students on how to use enrollment code
        """
        self.ps.test_updates['name'] = 'cc1.10.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.10',
            'cc1.10.005',
            '7719'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7720 - 006 - Teacher | Rename a course period
    @pytest.mark.skipif(str(7720) not in TESTS, reason='Excluded')
    def test_teacher_rename_a_course_period_7720(self):
        """Rename a course period.

        Steps:
        Go to Tutor
        Log in as a teacher
        Click on a Concept Coach book
        Click on the user menu
        Select course roster
        Click on tab for selected section
        Click 'Rename section'
        Enter new section name into the section Name text box
        Click on the 'Rename' button

        Expected Result:
        Section is renamed
        """
        self.ps.test_updates['name'] = 'cc1.10.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.10',
            'cc1.10.006',
            '7720'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7721 - 007 - Teacher | Archive an empty period
    @pytest.mark.skipif(str(7721) not in TESTS, reason='Excluded')
    def test_teacher_remove_an_empty_period_7721(self):
        """Remove an empty period.

        Steps:
        Go to Tutor
        Log in as a teacher
        Click on a Concept Coach book
        Click on the user menu
        Select course roster
        Click on tab for selected empty section
        Click 'Archive section'
        Click on the 'Archive' button

        Expected Result:
        Section is archived
        """
        self.ps.test_updates['name'] = 'cc1.10.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.10',
            'cc1.10.007',
            '7721'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7722 - 008 - Teacher | Archive a non-empty period
    @pytest.mark.skipif(str(7722) not in TESTS, reason='Excluded')
    def test_teacher_archive_a_nonempty_periods_7722(self):
        """Error message displayed if attempting to remove a non-empty period.

        Steps:
        Go to Tutor
        Log in as a teacher
        Click on a Concept Coach book
        Click on the user menu
        Select course roster
        Click on tab for selected non-empty section
        Click 'Archive section'
        Click Archive

        Expected Result:
        Section is archived
        """
        self.ps.test_updates['name'] = 'cc1.10.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.10',
            'cc1.10.008',
            '7722'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7723 - 009 - Teacher | Rename the course
    @pytest.mark.skipif(str(7723) not in TESTS, reason='Excluded')
    def test_teacher_rename_the_course_7723(self):
        """Rename the course.

        Steps:
        Go to Tutor
        Log in as a teacher
        Click on a Concept Coach book
        Click on the user menu
        Select course roster
        Click 'Rename Course'
        Enter a new Course name into the Course Name text box
        Click on the 'Rename' button

        Expected Result:
        Course is renamed.
        """
        self.ps.test_updates['name'] = 'cc1.10.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.10',
            'cc1.10.009',
            '7723'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7724 - 010 - Teacher | Remove other teachers from the course
    @pytest.mark.skipif(str(7724) not in TESTS, reason='Excluded')
    def test_teacher_remove_other_teachers_from_the_course_7724(self):
        """Remove other teachers from the course.

        Steps:
        Go to Tutor
        Log in as a teacher
        Click on a Concept Coach book
        Click on the user menu
        Select course roster
        Click on 'Remove' on the same row as selected teacher
        Click on the 'Remove' button

        Expected Result:
        Instructor is removed from the course
        """
        self.ps.test_updates['name'] = 'cc1.10.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.10',
            'cc1.10.010',
            '7724'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7725 - 011 - Teacher | Remove themself from the course
    @pytest.mark.skipif(str(7725) not in TESTS, reason='Excluded')
    def test_teacher_remove_themself_from_the_course_7725(self):
        """Remove themself from the course.

        Steps:
        Go to Tutor
        Log in as a teacher
        Click on a Concept Coach book
        Click on the user menu
        Select course roster
        Click on 'Remove' on the same row as themselves
        Click on the 'Remove' button

        Expected Result:
        Teacher is removed from course and taken back to dashboard
        """
        self.ps.test_updates['name'] = 'cc1.10.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.10',
            'cc1.10.011',
            '7725'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7726 - 012 - Teacher | Transfer a student to another period
    @pytest.mark.skipif(str(7726) not in TESTS, reason='Excluded')
    def test_teacher_transfer_a_student_to_another_period_7726(self):
        """Transfer a student to another period.

        Steps:
        Go to Tutor
        Log in as a teacher
        Click on a Concept Coach book
        Click on the user menu
        Select course roster
        Click on tab for section selected student is currently enrolled in
        Click on 'Change Section' on the row of the selected student
        Click on section to move student to

        Expected Result:
        Student is moved to chosen section
        """
        self.ps.test_updates['name'] = 'cc1.10.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.10',
            'cc1.10.012',
            '7726'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7727 - 013 - Teacher | Remove a student from a course
    @pytest.mark.skipif(str(7727) not in TESTS, reason='Excluded')
    def test_teacher_remove_a_student_from_a_course_7727(self):
        """Remove a student from a course.

        Steps:
        Go to Tutor
        Log in as a teacher
        Click on a Concept Coach book
        Click on the user menu
        Select course roster
        Click on tab for section selected student is currently enrolled in
        Click on 'Drop' on the row of the selected student
        Click on the 'Drop' button

        Expected Result:
        Student is dropped from the course
        """
        self.ps.test_updates['name'] = 'cc1.10.013' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.10',
            'cc1.10.013',
            '7727'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7728 - 014 - Admin | Impersonate a teacher
    @pytest.mark.skipif(str(7728) not in TESTS, reason='Excluded')
    def test_admin_impersonate_a_teacher_7728(self):
        """Impersonate a teacher.

        Steps:
        Go to Tutor
        Click on the 'Login' button
        Enter the admin user account in the username and password text boxes
        Click on the 'Sign in' button
        Click on the user's name in the top right corner to open drop down menu
        Click on the 'Admin' option of the drop down menu
        Click on 'Users' on the bar across the top
        [optional] Enter a teacher name into the search here text box
        Click on the 'Search' button
        Click on the 'Sign in as' button next to chosen teacher

        Expected Result:
        Signs in as chosen chosen teacher.
        Goes to chosen teacher's initial screen after login
        If multiple courses list of textbooks
        If one course straight to dashboard
        """
        self.ps.test_updates['name'] = 'cc1.10.014' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.10',
            'cc1.10.014',
            '7728'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7729 - 015 - Admin | Change a course ecosystem
    @pytest.mark.skipif(str(7729) not in TESTS, reason='Excluded')
    def test_admin_change_a_course_ecosystem_7729(self):
        """Change a course ecosystem.

        Steps:
        Go to Tutor
        Click on the 'Login' button
        Enter the admin user account in the username and password text boxes
        Click on the 'Sign in' button
        Click on the 'Admin' button from the user menu
        Open the drop down menu by clicking 'Course Organization'
        Click the 'Courses' option
        Click the 'Edit' link for the desired course
        Click on the 'Course content' tab
        Select a different option in the 'Ecosystem' drop down menu
        Click the 'Submit' button

        Expected Result:
        Course ecosystem change is put on a queue
        """
        self.ps.test_updates['name'] = 'cc1.10.015' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.10',
            'cc1.10.015',
            '7729'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7730 - 016 - Admin | Change multiple course ecosystems in bulk
    @pytest.mark.skipif(str(7730) not in TESTS, reason='Excluded')
    def test_admin_change_multiple_course_ecosystems_in_bulk_7730(self):
        """Change multiple course ecosystems in bulk.

        Steps:
        Go to Tutor
        Click on the 'Login' button
        Enter the admin user account in the username and password text boxes
        Click on the 'Sign in' button
        Click on the 'Admin' button from the user menu
        Open the drop down menu by clicking 'Course Organization'
        Click the 'Courses' option
        Check the checkboxes next to selected courses
        Select an option in the 'Select an ecosystem' drop down menu
        Click the 'Set Ecosystem' button

        Expected Result:
        Course ecosystem change is put on a queue
        """
        self.ps.test_updates['name'] = 'cc1.10.016' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.10',
            'cc1.10.016',
            '7730'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7731 - 017 - Teacher | Receive a notice when students register
    @pytest.mark.skipif(str(7731) not in TESTS, reason='Excluded')
    def test_teacher_receive_a_notice_when_students_register_7731(self):
        """Receive a notice when students register.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 'cc1.10.017' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.10',
            'cc1.10.017',
            '7731'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
