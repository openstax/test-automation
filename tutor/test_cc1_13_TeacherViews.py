"""Concept Coach v1, Epic 13 - Teacher Views."""

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
from staxing.helper import Teacher  # NOQA

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': '50.0',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([7609, 7610, 7611, 7612, 7613,
         7614, 7615, 7616, 7617, 7618,
         7619, 7620, 7622, 7624])  # NOQA
)


@PastaDecorator.on_platforms(BROWSERS)
class TestTeacherViews(unittest.TestCase):
    """CC1.13 - Teacher Views."""

    def setUp(self):
        """Pretest settings."""
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

    # Case C7609 - 001 - Teacher | View the Concept Coach dashboard
    @pytest.mark.skipif(str(7609) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_view_the_concept_coach_dashboard_7609(self):
        """View the Concept Coach dashboard.

        Steps:

        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a CC course name


        Expected Result:

        The user is presented with the Concept Coach dashbaord

        """
        self.ps.test_updates['name'] = 'cc1.13.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.13',
            'cc1.13.001',
            '7609'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C7610 - 002 - Teacher | Switch between concurrently running courses
    @pytest.mark.skipif(str(7610) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_switch_between_concurrently_running_courses_7610(self):
        """Able to switch between concurrently running courses.

        Steps:

        Click on the OpenStax logo in the left corner of the header


        Expected Result:

        The user is presented with a list of Concept Coach courses
        Is able to switch to another course

        """
        self.ps.test_updates['name'] = 'cc1.13.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.13',
            'cc1.13.002',
            '7610'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C7611 - 003 - Teacher | View links on dashboard to course materials
    @pytest.mark.skipif(str(7611) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_view_links_on_dashboard_to_course_materials_7611(self):
        """View links on dashboard to course materials.

        Steps:

        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a CC course name


        Expected Result:

        On header there is a link to 'Homework PDF', and 'Online Book'

        """
        self.ps.test_updates['name'] = 'cc1.13.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.13',
            'cc1.13.003',
            '7611'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C7612 - 004 - Teacher | Able to copy a system-generated message
    # with a student code, links, and other information
    @pytest.mark.skipif(str(7612) not in TESTS, reason='Excluded')  # NOQA
    def test_able_to_copy_a_system_generated_message_with_a_student_7612(self):
        """Copy a system-generated message with a student code, links, etc.

        Steps:

        Click on the user menu in the right corner of the header
        Click "Course Roster"
        Click "Get Student Enrollment Code"
        Copy the system generated message


        Expected Result:

        The user is able to copy the system generated message

        """
        self.ps.test_updates['name'] = 'cc1.13.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.13',
            'cc1.13.004',
            '7612'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C7613 - 005 - Teacher | Periods are relabeled as sections for all
    # courses
    @pytest.mark.skipif(str(7613) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_periods_are_relabeled_as_sections_for_all_cour_7613(self):
        """Period is relabeled as section for college courses.

        Steps:

        go to user menu
        click on course roster
        check that there is an '+ add section' button instead
        of an '+ add period' button


        Expected Result:

        There is an '+ add section' button instead of an '+ add period' button

        """
        self.ps.test_updates['name'] = 'cc1.13.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.13',
            'cc1.13.005',
            '7613'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C7614 - 006 - Teacher | View a score report
    @pytest.mark.skipif(str(7614) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_view_a_score_report_7614(self):
        """View a score report.

        Steps:

        Click the user menu in the right corner of the header
        Click "Student Scores"



        Expected Result:

        The user is presented with a score report

        """
        self.ps.test_updates['name'] = 'cc1.13.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.13',
            'cc1.13.006',
            '7614'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C7615 - 007 - Teacher | View a report showing an individual
    # student's work pages
    @pytest.mark.skipif(str(7615) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_view_a_report_showing_an_individual_students_7615(self):
        """View a report showing an individual student's work pages.

        Steps:

        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a CC course name

        Click the user menu in the right corner of the header
        Click "Student Scores"
        Click on the percentage in the "Score" column


        Expected Result:


        """
        self.ps.test_updates['name'] = 'cc1.13.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.13',
            'cc1.13.007',
            '7614'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C7616 - 008 - Teacher | View a summary report showing a class's work
    # pages
    @pytest.mark.skipif(str(7616) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_view_a_summary_report_showing_a_class_work_pag_7616(self):
        """View a summary report showing a class's work pages.

        Steps:

        Click on the desired period tab


        Expected Result:

        The user is presented with a summary report

        """
        self.ps.test_updates['name'] = 'cc1.13.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.13',
            'cc1.13.008',
            '7616'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C7617 - 009 - Teacher | View the aggregate student scores
    @pytest.mark.skipif(str(7617) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_view_the_aggregate_student_scores_7617(self):
        """View the aggregate student scores.

        Steps:

        Click the user menu in the right corner of the header
        Click "Student Scores"


        Expected Result:

        The user is presented with Student scores

        """
        self.ps.test_updates['name'] = 'cc1.13.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.13',
            'cc1.13.009',
            '7617'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C7618 - 010 - Teacher | View scores for an individual student's
    # scores
    @pytest.mark.skipif(str(7618) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_view_scores_for_an_individual_student_scores_7618(self):
        """View scores for an individual student's scores.

        Steps:

        Click the user menu in the right corner of the header
        Click "Student Scores"
        Scroll to the desired student


        Expected Result:

        The user is presented with scores for an individual student

        """
        self.ps.test_updates['name'] = 'cc1.13.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.13',
            'cc1.13.010',
            '7618'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C7619 - 011 - Teacher | View an individual student's question set
    # for an assignment
    @pytest.mark.skipif(str(7619) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_view_an_individual_student_question_set_7619(self):
        """View an individual student's question set for an assignment.

        Steps:

        Click the user menu in the right corner of the header
        Click "Student Scores"
        Click on a student's score for the desired assignment


        Expected Result:

        The user is presented with a student's question set for the assignment

        """
        self.ps.test_updates['name'] = 'cc1.13.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.13',
            'cc1.13.011',
            '7619'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C7620 - 012 - Teacher | View an assignment summary
    @pytest.mark.skipif(str(7620) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_view_an_assignment_summary_7620(self):
        """View an assignment summary.

        Steps:

        Click the user menu in the right corner of the header
        Click "Student Scores"
        Click on a student's score for the desired assignment
        Click "Summary"


        Expected Result:

        The user is presented with an assignmnent summary

        """
        self.ps.test_updates['name'] = 'cc1.13.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.13',
            'cc1.13.012',
            '7620'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C7622 - 013 - Teacher | Download student scores
    @pytest.mark.skipif(str(7622) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_download_student_scores_7622(self):
        """Download student scores.

        Steps:

        Click the user menu in the right corner of the header
        Click "Student Scores"
        Click "Export"


        Expected Result:

        Student scores are downloaded in an excel spreadsheet

        """
        self.ps.test_updates['name'] = 'cc1.13.013' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.13',
            'cc1.13.013',
            '7622'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C7624 - 014 - Teacher | Exercise IDs are shown for each assessment
    @pytest.mark.skipif(str(7624) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_exercise_ids_are_shown_for_each_assessment_7624(self):
        """Exercise IDs are shown for each assessment.

        Steps:

        Click the user menu in the right corner of the header
        Click "Question Library"
        Select a chapter
        Click "Show Questions"


        Expected Result:

        Exercise IDs are shown for each assessment in the bottom right hand
        corner of the box holding the question.

        """
        self.ps.test_updates['name'] = 'cc1.13.014' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.13',
            'cc1.13.014',
            '7624'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True
