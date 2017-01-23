"""Tutor v3, Epic 09 - Course Adoption and Readoption."""

import datetime
import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
from random import randint
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from staxing.assignment import Assignment

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Teacher

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
        106450, 106451, 106452, 106453, 106454,
        106455, 106456, 106457, 106458, 106459,
        106460, 106461, 106462, 107476, 107477,
        107478, 107479, 107480, 107482, 107483,
        107484, 107495, 107495
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestCreateAReading(unittest.TestCase):
    """T1.14 - Create a Reading."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.teacher = Teacher(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        self.teacher.login()
        self.teacher.select_course(appearance='biology')

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

    # Case C106450 - 001 - Teacher | Add a course via MyOpenstax
    @pytest.mark.skipif(str(106450) not in TESTS, reason='Excluded')
    def test_teacher_add_a_course_via_my_openstax_106450(self):
        """Add a course via my openstax.

        Steps:
        Log in to openstax.org
        Go to “My openstax” page
        Click “+ add courses” under “Courses”
        Choose semester/quarter and year and click continue
        Choose “New or copy”.
        “Cancel” button can bring user back to the main page at any time.

        Expected Result:
        User is directed to Tutor Dashboard'
        """
        self.ps.test_updates['name'] = 't3.09.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.09', 't3.09.001', '106450']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C106451 - 002 - Teacher | Add a course via the course picker page
    @pytest.mark.skipif(str(106451) not in TESTS, reason='Excluded')
    def test_teacher_add_a_course_via_the_course_picker_page_106451(self):
        """Add a course via the course picker page.

        Steps:
        Log in to tutor.openstax.org
        If there is no current course, a message “no current course” will be
            shown, and below it there is an “add a course” gray box.
        If there is a current course, the current course box followed by an
            “add a course” box appears.
        Click “Add a Course”
        Select a tutor or a concept coach course
        Select year, enter name and section number for the course.
        “Cancel” button can bring user back to the main page at any time.

        Expected Result:
        User is directed to Tutor Dashboard
        """
        self.ps.test_updates['name'] = 't3.09.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.09', 't3.09.002', '106451']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C106452 - 003 - Teacher | Add a course via the Tutor dashboard
    @pytest.mark.skipif(str(106452) not in TESTS, reason='Excluded')
    def test_teacher_add_a_course_via_the_tutor_dashboard_106452(self):
        """Add a course via the Tutor dashboard.

        Steps:
        Log in to tutor.openstax.org
        Go to dashboard.
        In the upper panel, there is a message asking whether user wishes to
            teach again. Select “Yes”.
        Select whether to copy question library, and select semester.
        “Cancel” directs users back to the Course Picker Page in any step
        “Continue” directs to the next step
        The color of the selected option is grey
        “Back” directs users to last page

        Expected Result:
        User is taken to a new course dashboard, with old course data copied
        """
        self.ps.test_updates['name'] = 't3.09.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.09', 't3.09.003', '106452']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C106453 - 004 - Teacher | A past course is available for cloning
    @pytest.mark.skipif(str(106453) not in TESTS, reason='Excluded')
    def test_teacher_apast_course_is_available_for_cloning_106453(self):
        """A past course is available for cloning.

        Steps:
        Login to tutor
        Select “Copy a past course” from the user menu
        Select Tutor or Concept Coach
        Select a course
        Select a semester
        Select "Copy a past Course"


        Expected Result:
        Past courses appears in the following section
        """
        self.ps.test_updates['name'] = 't3.09.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.09', 't3.09.004', '106453']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C106454 - 005 - Teacher | Able to copy the question library during
    # cloning
    @pytest.mark.skipif(str(106454) not in TESTS, reason='Excluded')
    def test_teacher_able_to_copy_the_question_library_during_clo_106454(self):
        """Able to copy the question library during cloning.

        Steps:
        Log in to tutor.openstax.org
        Click “Add a Course”
        Select a tutor or a concept coach course
        Select “Copy a past course”
        Select a past course from the next page.

        Expected Result:
        Message “Choose whether to copy the question library” appears
        """
        self.ps.test_updates['name'] = 't3.09.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.09', 't3.09.005', '106454']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C106455 - 006 - Teacher | Able to select the name for a new course
    @pytest.mark.skipif(str(106455) not in TESTS, reason='Excluded')
    def test_teacher_able_to_select_the_name_for_a_new_course_106455(self):
        """Able to select the name for a new course.

        Steps:
        Log in to tutor.openstax.org
        Click “Add a Course”
        Select a tutor or a concept coach course
        Select “Copy a past course”
        Select a past course.
        Select “Copy question library”.
        Enter a name for the tutor course

        Expected Result:
        Text could be entered into the text box.
        """
        self.ps.test_updates['name'] = 't3.09.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.09', 't3.09.006', '106455']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C106456 - 007 - Teacher | Specify the number of sections for a new
    # course
    @pytest.mark.skipif(str(106456) not in TESTS, reason='Excluded')
    def test_teacher_specify_the_number_of_sections_for_a_new_cou_106456(self):
        """Specify the number of sections for a new course.

        Steps:
        Log in to tutor.openstax.org
        Click “Add a Course”
        Select a tutor or a concept coach course
        Select “Copy a past course”
        Select a past course.
        Select “Copy question library”.
        Enter a number into the tutor course sections panel

        Expected Result:
        Number could be entered. The page won’t proceed if anything else is
        entered into the number panel
        """
        self.ps.test_updates['name'] = 't3.09.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.09', 't3.09.007', '106456']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C106457 - 008 - Teacher | A course's setting match those selected
    # during the cloning process
    @pytest.mark.skipif(str(106457) not in TESTS, reason='Excluded')
    def test_teacher_a_courses_settings_match_those_selected_duri_106457(self):
        """A course's setting match those selected during the cloning process.

        Steps:
        Log in to tutor.openstax.org
        Click “Add a Course”
        Select a tutor or a concept coach course
        Select “Copy a past course”
        Select a past course.
        Select “Copy question library”.
        Enter a name for the tutor course
        Enter a number into the tutor course sections

        Expected Result:
        Course dashboard appears with the name and section number user entered
        """
        self.ps.test_updates['name'] = 't3.09.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.09', 't3.09.008', '106457']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C106458 - 009 - Teacher | Add a new course
    @pytest.mark.skipif(str(106458) not in TESTS, reason='Excluded')
    def test_teacher_add_a_new_course_106458(self):
        """Add a new course.

        Steps:
        Log in to tutor.openstax.org
        Click “Add a Course”
        Select a tutor or a concept coach course
        Select “Create a new course”.
        Enter the name and number of sections for the new course.
        Click “create course”.

        Expected Result:
        User is taken to a dashboard with a blank calendar, with the
        corresponding course name and section number
        """
        self.ps.test_updates['name'] = 't3.09.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.09', 't3.09.009', '106458']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C106459 - 010 - Teacher | Copy a homework
    @pytest.mark.skipif(str(106459) not in TESTS, reason='Excluded')
    def test_teacher_copy_a_homework_106459(self):
        """Copy a homework.

        Steps:
        Log in to tutor.openstax.org
        Click “Add a Course”
        Select a tutor or a concept coach course
        Select “Copy an old course”
        Select the course user wishes to copy.
        Select “Copy” when system asks “Do you want to copy past questions?”
        Enter course name and number of sections in the new pop-up.
        User is taken to dashboard, with past assignments appearing on the left

        Expected Result:
        When user clicks on a past assignment on the left panel, An auto-filled
        assignment creation form appeared
        """
        self.ps.test_updates['name'] = 't3.09.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.09', 't3.09.010', '106459']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C106460 - 011 - Teacher | Copy an event
    @pytest.mark.skipif(str(106460) not in TESTS, reason='Excluded')
    def test_teacher_copy_an_event_106460(self):
        """Copy an event.

        Steps:
        Log in to tutor.openstax.org
        Click “Add a Course”
        Select a tutor or a concept coach course
        Select “Copy an old course”
        Select the course user wishes to copy.
        Select “Copy” when system prompts “Do you want to copy past questions?”
        Enter course name and number of sections in the new pop-up.
        User is taken to dashboard, with past assignments appearing on the left

        Expected Result:
        When user clicks on a past Event on the left panel, An auto-filled
        event creation form appeared
        """
        self.ps.test_updates['name'] = 't3.09.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.09', 't3.09.011', '106460']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C106461 - 012 - Teacher | Copy a reading
    @pytest.mark.skipif(str(106461) not in TESTS, reason='Excluded')
    def test_teacher_copy_a_reading_106461(self):
        """Copy a reading.

        Steps:
        Log in to tutor.openstax.org
        Click “Add a Course”
        Select a tutor or a concept coach course
        Select “Copy an old course”
        Select the course user wishes to copy.
        Select “Copy” when system asks “Do you want to copy past questions?”
        Enter course name and number of sections in the new pop-up.
        User is taken to dashboard, with past assignments appearing on the left

        Expected Result:
        When user clicks on a past reading on the left panel, An auto-filled
        reading creation form appeared
        """
        self.ps.test_updates['name'] = 't3.09.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.09', 't3.09.012', '106461']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C106462 - 013 - Teacher | Copy an external assignment
    @pytest.mark.skipif(str(106462) not in TESTS, reason='Excluded')
    def test_teacher_copy_an_external_assignment_106462(self):
        """Copy an external assignment.

        Steps:
        Log in to tutor.openstax.org
        Click “Add a Course”
        Select a tutor or a concept coach course
        Select “Copy an old course”
        Select the course user wishes to copy.
        Select “Copy” when system asks “Do you want to copy past questions?”
        Enter course name and number of sections in the new pop-up.
        User is taken to dashboard, with past assignments appearing on the left

        Expected Result:
        When user clicks on a past assignment on the left panel, An auto-filled
        external assignment creation form appeared
        """
        self.ps.test_updates['name'] = 't3.09.013' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.09', 't3.09.013', '106462']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C107576 - 014 - Admin | Change the course term
    @pytest.mark.skipif(str(107576) not in TESTS, reason='Excluded')
    def test_admin_change_the_course_term_107576(self):
        """Change the course term.

        Steps:
        Log in as an Admin
        Go to the course management page
        Edit a course
        Change the term
        Click Save

        Expected Result:
        Start and end dates should reflect the new term's timeframe
        """
        self.ps.test_updates['name'] = 't3.09.014' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.09', 't3.09.014', '107576']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C107577 - 015 - Admin | Change the course year
    @pytest.mark.skipif(str(107577) not in TESTS, reason='Excluded')
    def test_admin_change_the_course_year_107576(self):
        """Change the course year.

        Steps:
        Log in as an Admin
        Go to the course management page
        Edit a course
        Change the year
        Click Save

        Expected Result:
        Start and end dates should reflect the new year's timeframe
        """
        self.ps.test_updates['name'] = 't3.09.015' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.09', 't3.09.015', '107577']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C107578 - 016 - Admin | Change the course start date
    @pytest.mark.skipif(str(107578) not in TESTS, reason='Excluded')
    def test_admin_change_the_course_start_date_107578(self):
        """Change the course start date.

        Steps:
        Log in as an Admin
        Go to the course management page
        Edit a course
        Change the Starts at date
        Click Save

        Expected Result:
        Start date is changed
        """
        self.ps.test_updates['name'] = 't3.09.016' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.09', 't3.09.016', '107578']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C107579 - 017 - Admin | Change the course end date
    @pytest.mark.skipif(str(107579) not in TESTS, reason='Excluded')
    def test_admin_change_the_course_end_date_107579(self):
        """Change the course end_date.

        Steps:
        Log in as an Admin
        Go to the course management page
        Edit a course
        Change the Ends at date
        Click Save

        Expected Result:
        End date is changed
        """
        self.ps.test_updates['name'] = 't3.09.017' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.09', 't3.09.017', '107579']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C107580 - 018 - Teacher | Provide a registration link to co-teachers
    @pytest.mark.skipif(str(107580) not in TESTS, reason='Excluded')
    def test_teacher_provide_a_registration_link_to_co_teachers_107580(self):
        """Provide a registration link to co-teachers.

        Steps:
        Log in as a teacher
        Go to a course dashboard
        Go to the course roster
        Click Add an instructor
        Copy the link provided
        Log out
        Log in as a different teacher
        Go to the link

        Expected Result:
        New teacher is at the course dashboard
        """
        self.ps.test_updates['name'] = 't3.09.018' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.09', 't3.09.018', '107580']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C107582 - 019 - Teacher | Add a section to a course
    @pytest.mark.skipif(str(107582) not in TESTS, reason='Excluded')
    def test_teacher_add_a_section_to_a_course_107582(self):
        """Add a section to a course.

        Steps:
        Log in as a teacher
        Click on a tutor course
        Click on Course Settings and roster in the user menu
        Click "+ Add Section"
        Enter a new section name into into the "Section Name" text field
        Click Add

        Expected Result:
        A new section is created and its tab is displayed
        """
        self.ps.test_updates['name'] = 't3.09.019' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.09', 't3.09.019', '107582']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C107583 - 020 - Teacher | Delete a section to a course
    @pytest.mark.skipif(str(107583) not in TESTS, reason='Excluded')
    def test_teacher_delete_a_section_to_a_course_107583(self):
        """Delete a section to a course.

        Steps:
        Log in as a teacher
        Click on a tutor course
        Click on "Course Settings and Roster" in the user menu
        Click on period tab for period to delete
        Click "Delete Section"
        Click "Delete" in the pop up box

        Expected Result:
        The period is deleted and its tab is removed
        """
        self.ps.test_updates['name'] = 't3.09.020' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.09', 't3.09.020', '107583']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C107584 - 021 - Teacher | A course with zero sections displays a
    # message to add at leat one section to the class
    @pytest.mark.skipif(str(107584) not in TESTS, reason='Excluded')
    def test_teacher_a_course_with_zero_sections_displays_a_messa_107584(self):
        """A course with zero sections displays a message to add at leat one
        section to the clas.

        Steps:
        Log in as a teacher
        Click on tutor course with zero sections, or create one
        Click on "Course Settings and Roster" in the user menu

        Expected Result:
        A message to add at least one section to the course is displayed with a
        button to do so
        """
        self.ps.test_updates['name'] = 't3.09.021' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.09', 't3.09.021', '107584']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C107595 - 022 - Teacher | Unable to create an assignment prior to
    # the start of term
    @pytest.mark.skipif(str(107595) not in TESTS, reason='Excluded')
    def test_teacher_unable_to_create_an_assignment_prior_to_star_107595(self):
        """Unable to create an assignment prior to the start of term.

        Steps:
        Login as a teacher
        Click on a course with a start date after the current date, or create one
        Click on the add assignment menu
        Click on the add event option
        Click on the open date text field
        Click on the due date text field

        Expected Result:
        A due date or open date cannot be set to before the start of term. The
        calendars cannot be rotated to view months prior to the start of course
        """
        self.ps.test_updates['name'] = 't3.09.022' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.09', 't3.09.022', '107595']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C107596 - 023 - Teacher | Unable to create an assignment after the
    # end of term
    @pytest.mark.skipif(str(107596) not in TESTS, reason='Excluded')
    def test_teacher_unable_to_create_an_assignment_after_the_end_107596(self):
        """Unable to create an assignment after the end of term.

        Steps:
        Login as a teacher
        Click on a current tutor course
        Click on the Add Assignment menu
        Click on Add Event
        Click on the Open Date text field
        Click the forward arrow to rotate the calendar to the course end date
        Click on the Due Date text field
        Click the forward arrow to rotate the calendar to the course end date

        Expected Result:
        A due date or open date cannot be set to after the end of term. The
        calendars cannot be rotated to view months after to the end of course.
        """
        self.ps.test_updates['name'] = 't3.09.023' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.09', 't3.09.023', '107596']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
