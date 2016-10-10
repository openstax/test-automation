"""Concept Coach v2, Epic 8 - Improves Scores Reporting."""

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
        14806, 14807, 14808, 14810, 14811,
        14668, 14670, 14669, 14812, 14813,
        14814, 14815, 14816
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestImprovesScoresReporting(unittest.TestCase):
    """CC2.08 - Improves Scores Reporting."""

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

    # 14806 - 001 - Teacher | View student scores as percent complete
    @pytest.mark.skipif(str(14806) not in TESTS, reason='Excluded')
    def test_teacher_view_student_scores_as_percent_complete_14806(self):
        """View student scores as percent complete.

        Steps:
        Go to Tutor
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a CC course name
        Click "View Detailed Scores"
        Click on the icon in the progress column

        Expected Result:
        Student Scores are presented as percent complete
        """
        self.ps.test_updates['name'] = 'cc2.08.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc2',
            'cc2.08',
            'cc2.08.001',
            '14806'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 14807 - 002 - Teacher | View student scores as number of total
    @pytest.mark.skipif(str(14807) not in TESTS, reason='Excluded')
    def test_teacher_view_student_scores_as_number_of_total_14807(self):
        """View student scores as number of total.

        Steps:
        If the user has more than one course, click on a CC course name
        Click "View Detailed Scores"
        Click "Number"

        Expected Result:
        Student Scores are presented as "Number of Total"
        """
        self.ps.test_updates['name'] = 'cc2.08.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc2',
            'cc2.08',
            'cc2.08.002',
            '14807'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 14808 - 003 - Teacher | View tooltips on hover
    @pytest.mark.skipif(str(14808) not in TESTS, reason='Excluded')
    def test_teacher_view_tooltips_on_hover_14808(self):
        """View tooltips on hover.

        Steps:
        If the user has more than one course, click on a CC course name
        Hover over the info icons

        Expected Result:
        The user is presented with tooltips
        """
        self.ps.test_updates['name'] = 'cc2.08.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc2',
            'cc2.08',
            'cc2.08.003',
            '14808'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 14810 - 004 - Teacher | Sort student scores based on score
    @pytest.mark.skipif(str(14810) not in TESTS, reason='Excluded')
    def test_teacher_sort_student_scores_based_on_score_14810(self):
        """Sort student scores based on score.

        Steps:
        If the user has more than one course, click on a CC course name
        Click "View Detailed Scores"
        Click "Score" for the desired assignment

        Expected Result:
        Students are sorted based on score
        """
        self.ps.test_updates['name'] = 'cc2.08.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc2',
            'cc2.08',
            'cc2.08.004',
            '14810'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 14811 - 005 - Teacher | Sort student scores based on number complete
    @pytest.mark.skipif(str(14811) not in TESTS, reason='Excluded')
    def test_teacher_sort_student_scores_based_on_number_completed_14811(self):
        """Sort student scores based on number complete.

        Steps:
        If the user has more than one course, click on a CC course name
        Click "View Detailed Scores"
        Click "Progress" for the desired assignment

        Expected Result:
        Students are sorted based on number completed
        """
        self.ps.test_updates['name'] = 'cc2.08.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc2',
            'cc2.08',
            'cc2.08.005',
            '14811'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 14668 - 006 - Teacher | All popups in the roster have an X button
    @pytest.mark.skipif(str(14668) not in TESTS, reason='Excluded')
    def test_teacher_all_popups_in_the_roster_have_an_x_button_14668(self):
        """All popups in the roster have an X button.

        Steps:
        If the user has more than one course, click on a CC course name
        Click "Course Settings and Roster" from the user menu
        Click "Rename Course," "Change Course Timezone,"
        "View Archived Period," "Add Period," "Rename," and "Get Student
            Enrollment Code"

        Expected Result:
        All pop ups have an X button
        """
        self.ps.test_updates['name'] = 'cc2.08.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc2',
            'cc2.08',
            'cc2.08.006',
            '14668'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 14670 - 007 - Teacher | Close popup with X button
    @pytest.mark.skipif(str(14670) not in TESTS, reason='Excluded')
    def test_teacher_close_popup_with_x_button_14670(self):
        """Close popup with X button.

        Steps:
        If the user has more than one course, click on a CC course name
        Click "Course Settings and Roster" from the user menu
        Click ONE of the following:
        * Rename Course
        * Change Course Timezone
        * View Archived Period
        * Add Period
        * Rename
        * Get Student Enrollment Code
        Click the X on the pop up

        Expected Result:
        Popup is closed
        """
        self.ps.test_updates['name'] = 'cc2.08.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc2',
            'cc2.08',
            'cc2.08.007',
            '14670'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 14669 - 008 - Teacher | The icon in the progress column shows info on
    # percentage complete, attempted out of total possible questions, and
    # the date last worked
    @pytest.mark.skipif(str(14669) not in TESTS, reason='Excluded')
    def test_teacher_the_icon_in_the_progress_column_shows_info_14669(self):
        """The icon in the progress column shows info.

        Steps:
        If the user has more than one course, click on a CC course name
        Click "View Detailed Scores"
        Click on the icon in the progress column for a completed assignment

        Expected Result:
        Shows information on percentage complete, attempted out of total
        possible questions as well as the date last worked
        """
        self.ps.test_updates['name'] = 'cc2.08.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc2',
            'cc2.08',
            'cc2.08.008',
            '14669'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 14812 - 009 - Teacher | Import CC Student Scores export into an LMS
    @pytest.mark.skipif(str(14812) not in TESTS, reason='Excluded')
    def test_teacher_import_cc_student_scores_export_into_an_lms_14812(self):
        """Import CC student scores export into an LMS.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 'cc2.08.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc2',
            'cc2.08',
            'cc2.08.009',
            '14812'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 14813 - 010 - Teacher | View zeros in exported scores instead of blank
    # cells for incomplete assignments
    @pytest.mark.skipif(str(14813) not in TESTS, reason='Excluded')
    def test_teacher_view_zeros_in_exported_scores_instead_of_blan_14813(self):
        """View zeros in exported scores for incomplete assignments.

        Steps:
        If the user has more than one course, click on a CC course name
        Click "View Detailed Scores"
        Click "Export"
        Open the excel file

        Expected Result:
        For incomplete assignments or assignments that are not started,
        there are zeros instead of blank cells
        """
        self.ps.test_updates['name'] = 'cc2.08.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc2',
            'cc2.08',
            'cc2.08.010',
            '14813'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 14814 - 011 - Teacher | Green check icon is displayed for completed
    # assignments
    @pytest.mark.skipif(str(14814) not in TESTS, reason='Excluded')
    def test_teacher_green_check_icon_is_displayed_for_completed_14814(self):
        """Green check icon is displayed for completed assignments.

        Steps:
        If the user has more than one course, click on a CC course name
        Click "View Detailed Scores

        Expected Result:
        Green check icon is displayed for completed assignments
        """
        self.ps.test_updates['name'] = 'cc2.08.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc2',
            'cc2.08',
            'cc2.08.011',
            '14814'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 14815 - 012 - Teacher | The class average info icon displays a definition
    # about scores from completed assignments
    @pytest.mark.skipif(str(14815) not in TESTS, reason='Excluded')
    def test_teacher_class_average_info_icon_displays_definition_14815(self):
        """The class average info icon displays a definition.

        Steps:
        If the user has more than one course, click on a CC course name
        Click "View Detailed Scores
        Click on the info icon next to "Class Average"

        Expected Result:
        The class average info icon displays a definition about scores from
        completed assignments
        """
        self.ps.test_updates['name'] = 'cc2.08.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc2',
            'cc2.08',
            'cc2.08.012',
            '14815'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 14816 - 013 - Teacher | View the overall score column
    @pytest.mark.skipif(str(14816) not in TESTS, reason='Excluded')
    def test_teacher_view_the_overall_score_column_14816(self):
        """View the overall score column.

        Steps:
        If the user has more than one course, click on a CC course name
        Click "View Detailed Scores

        Expected Result:
        User is presented with the overall score column next to student names
        """
        self.ps.test_updates['name'] = 'cc2.08.013' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc2',
            'cc2.08',
            'cc2.08.013',
            '14816'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
