"""Concept Coach v1, Epic 4 - Exercise Editing and QA."""

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
from staxing.helper import Admin, ContentQA

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
        7651, 7652, 7653, 7654, 7655,
        7656, 7657, 7658, 7659, 7660,
        7661, 7662, 7663, 7665, 7667,
        7669, 7670, 7672, 7673, 7674,
        7675, 7676, 7677, 7678, 7679,
        7681, 7682, 7683, 7686, 7687
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestExerciseEditingAndQA(unittest.TestCase):
    """CC1.04 - Exercise Editing and QA."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.admin = Admin(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        self.content = ContentQA(
            use_env_vars=True,
            existing_driver=self.admin.driver
        )

    def tearDown(self):
        """Test destructor."""
        self.ps.update_job(
            job_id=str(self.teacher.driver.session_id),
            **self.ps.test_updates
        )
        try:
            self.admin.delete()
        except:
            pass

    # Case C7651 - 001 - Content Analyst | See the full error list from a
    # failed book import
    @pytest.mark.skipif(str(7651) not in TESTS, reason='Excluded')
    def test_content_analyst_see_full_error_list_from_failed_book_7651(self):
        """See the full error list from a failed book import.

        Steps:
        Log into Tutor as a content analyst user
        From the User Menu select 'Content Analyst'
        Click on 'Ecosystems' in the header
        Click on the 'Failed Imports' tab
        Click on a Job ID

        Expected Result:
        The error report is displayed
        """
        self.ps.test_updates['name'] = 'cc1.04.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.001',
            '7651'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7652 - 002 - Admin | See the full error list from a
    # failed book import
    @pytest.mark.skipif(str(7652) not in TESTS, reason='Excluded')
    def test_admin_see_the_full_error_list_from_failed_book_import_7652(self):
        """See the full error list from a failed book import.

        Steps:
        Log into Tutor as an administrative user
        From the User Menu select 'Admin'
        Select 'Content' from the header
        Click on 'Ecosystems'
        Click on the 'Failed Imports' tab
        Click on a Job ID

        Expected Result:
        The error report is displayed
        """
        self.ps.test_updates['name'] = 'cc1.04.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.002',
            '7652'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7653 - 003 - Admin | Add the Content Analyst role to a user
    @pytest.mark.skipif(str(7653) not in TESTS, reason='Excluded')
    def test_admin_add_the_content_analyst_role_to_a_user_7653(self):
        """Add the Content Analyst role to a user.

        Steps:
        Log into Tutor as an administrator
        From the User Menu select 'Admin'
        Click on 'Users' in the header
        Locate the user in the list
        Click on the 'Edit' button to the right of the text columns
        Check the box to the right of 'Content analyst'
        Click on the 'Save' button

        Expected Result:
        The role is saved to the user
        """
        self.ps.test_updates['name'] = 'cc1.04.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.003',
            '7653'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7654 - 004 - Admin | Add the Customer Service role to a user
    @pytest.mark.skipif(str(7654) not in TESTS, reason='Excluded')
    def test_admin_add_the_customer_service_role_to_a_user_7654(self):
        """Add the Exercise Editor role to a user.

        Steps:
        Log into Tutor as an administrator
        From the User Menu select 'Admin'
        Click on 'Users' in the header
        Locate the user in the list
        Click on the 'Edit' button to the right of the text columns
        Check the box to the right of 'Customer Service'
        Click on the 'Save' button

        Expected Result:
        The role is saved to the user
        """
        self.ps.test_updates['name'] = 'cc1.04.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.004',
            '7654'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7655 - 005 - Admin | Add the Administrator role to a user
    @pytest.mark.skipif(str(7655) not in TESTS, reason='Excluded')
    def test_admin_add_the_administrator_role_to_a_user_7655(self):
        """Add the Exercise Editor role to a user.

        Steps:
        Log into Tutor as an administrator
        From the User Menu select 'Admin'
        Click on 'Users' in the header
        Locate the user in the list
        Click on the 'Edit' button to the right of the text columns
        Check the box to the right of 'Administrator'
        Click on the 'Save' button

        Expected Result:
        The role is saved to the user
        """
        self.ps.test_updates['name'] = 'cc1.04.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.005',
            '7655'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7656 - 006 - Content Analyst | Add an ecosystem comment
    @pytest.mark.skipif(str(7656) not in TESTS, reason='Excluded')
    def test_content_analyst_add_an_ecosystem_comment_7656(self):
        """Add an ecosystem comment.

        Steps:
        Log into Tutor as a content analyst user
        Select 'Customer Analyst' from the User Menu
        Select 'Ecosystems' from the menu
        In the Comments Column change a comment and click on Save.

        Expected Result:
        The comment is displayed on the ecosystem to the right of
        the book title
        """
        self.ps.test_updates['name'] = 'cc1.04.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.006',
            '7656'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7657 - 007 - Admin | Add an ecosystem comment
    @pytest.mark.skipif(str(7657) not in TESTS, reason='Excluded')
    def test_admin_add_an_ecosystem_comment_7657(self):
        """Add an ecosystem comment.

        Steps:
        Log into Tutor as an administrative user
        Select 'Admin' from the User Menu
        Click on the 'Content' heading
        Select 'Ecosystems' from the menu
        In the Comments column edit a comment. Click on Save.

        Expected Result:
        The comment is displayed on the ecosystem to the right of
        the book title
        """
        self.ps.test_updates['name'] = 'cc1.04.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.007',
            '7657'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7658 - 008 - Content Analyst | Delete an unused ecosystem
    @pytest.mark.skipif(str(7658) not in TESTS, reason='Excluded')
    def test_content_analyst_delete_an_unused_ecosystem_7658(self):
        """Delete an unused ecosystem.

        Steps:
        Log into Tutor as Content Analyst
        From the user menu select 'Customer Analyst'
        Select 'Ecosystems'
        Scroll and find a course that has the delete button in the last column
        Click on the course
        This should delete the ecosystem

        Expected Result:
        The unassigned ecosystem is removed from the system
        """
        self.ps.test_updates['name'] = 'cc1.04.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.008',
            '7658'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7659 - 009 - Admin | Delete an unused ecosystem
    @pytest.mark.skipif(str(7659) not in TESTS, reason='Excluded')
    def test_admin_delete_an_unused_ecosystem_7659(self):
        """Delete an unused ecosystem.

        Steps:
        Log into Tutor as Admin
        From the user menu select 'Admin'
        From the 'Content' menu select 'Ecosystems'
        Scroll and find a course that has the delete button in the last column
        Click on the desired course
        This should delete the ecosystem

        Expected Result:
        The unassigned ecosystem is removed from the system
        """
        self.ps.test_updates['name'] = 'cc1.04.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.009',
            '7659'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7660 - 010 - Content Analyst | Unable to delete an assigned
    # ecosystem
    @pytest.mark.skipif(str(7660) not in TESTS, reason='Excluded')
    def test_content_analyst_unable_to_delete_an_assigned_ecosystem_7660(self):
        """Unable to delete an assigned ecosystem.

        Steps:
        Log into Tutor as Content Analyst
        From the user menu select 'Customer Analyst'
        From the header select 'Ecosystems'
        In the last column ensure that for some books the delete option is
        not available.

        Expected Result:
        There should be no way for people to delete the assignment
        """
        self.ps.test_updates['name'] = 'cc1.04.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.010',
            '7660'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7661 - 011 - Admin | Unable to delete an assigned ecosystem
    @pytest.mark.skipif(str(7661) not in TESTS, reason='Excluded')
    def test_admin_unable_to_delete_an_assigned_ecosystem_7661(self):
        """Unable to delete an assigned ecosystem.

        Steps:
        Log into Tutor as Admin
        From the user menu select 'Admin'
        From the 'Content' menu select 'Ecosystems'
        In the last column ensure that for some books the delete option
        is not available.

        Expected Result:
        There should be no way for people to delete the assignment
        """
        self.ps.test_updates['name'] = 'cc1.04.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.011',
            '7661'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7662 - 012 - Content Analyst | View all exercises for a CNX page
    # module/Tutor section
    @pytest.mark.skipif(str(7662) not in TESTS, reason='Excluded')
    def test_content_analyst_view_all_exercises_for_a_cnx_page_modu_7662(self):
        """View all exercises for a CNX page module / Tutor section.

        Steps:
        Log into Tutor as a content analyst user
        Select 'QA Content' from the User Menu
        Click on any non-introductory section on the left-side bar

        Expected Result:
        Exercises for that section is displayed
        """
        self.ps.test_updates['name'] = 'cc1.04.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.012',
            '7662'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7663 - 013 - Content Analyst | From the QA exercise view open
    # an exercise for editing in a new tab
    @pytest.mark.skipif(str(7663) not in TESTS, reason='Excluded')
    def test_content_analyst_from_the_qa_view_open_an_exercise_for_7663(self):
        """From the QA exercise view open an exercise for editing in a new tab.

        Steps:
        Log into Tutor as a content analyst user
        Select 'QA Content' from the User Menu
        Click on any non-introductory section on the left-side bar
        Click on 'edit' on the lower right corner of the exercise
        Click "Close" on the popup box
        Sign in as exercise editor

        Expected Result:
        View a new tab of OpenStax Exercises editing page for
        the corresponding exercise
        """
        self.ps.test_updates['name'] = 'cc1.04.013' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.013',
            '7663'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7665 - 014 - Content Analyst | Able to filter exercises in the
    # QA exercise viewer
    @pytest.mark.skipif(str(7665) not in TESTS, reason='Excluded')
    def test_content_analyst_able_to_filter_exercises_in_the_qa_exe_7665(self):
        """Able to filter exercises in the QA exercise viewer.

        Steps:
        Click 'Exercise Types'
        Leave one type checked and others unchecked

        Expected Result:
        Only the exercises of checked type is listed
        """
        self.ps.test_updates['name'] = 'cc1.04.014' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.014',
            '7665'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7667 - 015 - Content Analyst | Display the QA view of book sections
    @pytest.mark.skipif(str(7667) not in TESTS, reason='Excluded')
    def test_content_analyst_display_the_qa_view_of_book_sections_7667(self):
        """Display the QA view of a book section.

        Steps:
        Log into Tutor as a content analyst user
        Select 'QA Content' from the User Menu
        Select 'Show Content' from the menu

        Expected Result:
        See the QA view of a book section
        """
        self.ps.test_updates['name'] = 'cc1.04.015' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.015',
            '7667'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7669 - 016 - Content Analyst | Able to navigate between book
    # sections in the QA view
    @pytest.mark.skipif(str(7669) not in TESTS, reason='Excluded')
    def test_content_analyst_able_to_navigate_between_book_sections_7669(self):
        """Able to navigate between book sections in the QA view.

        Steps:
        Log into Tutor as a content analyst user
        Select 'QA Content' from the User Menu
        Select 'Show Content' from the menu
        Click on the bars in upper-left corner of the page to show
        table of contents
        Click on any section to view

        Expected Result:
        Chosen section is displayed
        """
        self.ps.test_updates['name'] = 'cc1.04.016' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.016',
            '7669'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7670 - 017 - Admin | Add the Content Analyst role to DMS user
    # accounts
    @pytest.mark.skipif(str(7670) not in TESTS, reason='Excluded')
    def test_admin_add_the_content_analyst_role_to_dms_user_account_7670(self):
        """Add the Content Analyst role to DMS user accounts.

        Steps:
        Log into Tutor as an administrator
        From the User Menu select 'Admin'
        Click on 'Users' in the header
        Locate the user in the list
        Click on the 'Edit' button to the right of the text columns
        Check the box to the right of 'Content analyst'
        Click on the 'Save' button

        Expected Result:
        The role is saved to the DMS user account
        """
        self.ps.test_updates['name'] = 'cc1.04.017' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.017',
            '7670'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7672 - 018 - Content Analyst | In the QA exercise view render
    # the LaTex
    @pytest.mark.skipif(str(7672) not in TESTS, reason='Excluded')
    def test_content_analyst_in_the_qa_exercise_view_render_latex_7672(self):
        """In the QA exercise view render the LaTex.

        Steps:
        Log into Tutor as a content analyst user (content : password)
        Select 'QA Content' from the User Menu
        Select 'Physics' from Available Books Menu
        From the side bar on the left choose section
        '6.1 Angle of Rotation and Angular Velocity'
        Scroll to the 4th exercise: What equation defines angular velocity?

        Expected Result:
        View equations that are render of LaTex
        """
        self.ps.test_updates['name'] = 'cc1.04.018' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.018',
            '7672'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7673 - 019 - Content Analyst | In the QA exercise view verify that
    # the exercise ID is shown
    @pytest.mark.skipif(str(7673) not in TESTS, reason='Excluded')
    def test_content_analyst_verify_that_the_exercise_id_is_shown_7673(self):
        """In the QA exercise view verify that the exercise ID is shown.

        Steps:
        Log into Tutor as a content analyst user (content : password)
        Select 'QA Content' from the User Menu
        Select a book from Available Books Menu
        From the side bar on the left select a section to view exercises
        For an exercise look at the last row of the section

        Expected Result:
        View the ID# of the exercise
        """
        self.ps.test_updates['name'] = 'cc1.04.019' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.019',
            '7673'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7674 - 020 - Content Analyst | Able to publish an exercise
    @pytest.mark.skipif(str(7674) not in TESTS, reason='Excluded')
    def test_content_analyst_able_to_publish_an_exercise_7674(self):
        """Able to publish an exercise.

        Steps:
        Open a new page of OpenStax Exercises
        Sign with username 'openstax' and password 'password'
        Go back to exercises on OpenStax Tutor page
        For an exercise, click on 'edit' button on the lower right corner
        Edit the exercise
        Click on Save at bottom of the page
        Click OK when asked if sure want to save
        Click on Publish at bottom of the page
        Click OK when asked if sure want to publish

        Expected Result:
        View the edited exercise
        """
        self.ps.test_updates['name'] = 'cc1.04.020' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.020',
            '7674'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7675 - 021 - Teacher | Able to publish an exercise
    @pytest.mark.skipif(str(7675) not in TESTS, reason='Excluded')
    def test_teacher_able_to_publish_an_exercise_7675(self):
        """Able to publish an exercise.

        Steps:
        Log into Tutor as a teacher
        View exercises
        Open a new page of OpenStax Exercises
        Sign with username 'openstax' and password 'password'
        Go back to exercises on OpenStax Tutor page
        For an exercise, click on 'edit' button on the lower right corner
        Edit the exercise
        Click on Save at bottom of the page
        Click OK when asked if sure want to save
        Click on Publish at bottom of the page
        Click OK when asked if sure want to publish

        Expected Result:
        The exercise is published
        """
        self.ps.test_updates['name'] = 'cc1.04.021' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.021',
            '7675'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7676 - 022 - Admin | Able to publish an exercise
    @pytest.mark.skipif(str(7676) not in TESTS, reason='Excluded')
    def test_admin_able_to_publish_an_exercise_7676(self):
        """Able to publish an exercise.

        Steps:
        Log into Tutor as an admin
        View exercises
        Open a new page of OpenStax Exercises
        Sign with username 'openstax' and password 'password'
        Go back to exercises on OpenStax Tutor page
        For an exercise, click on 'edit' button on the lower right corner
        Edit the exercise
        Click on Save at bottom of the page
        Click OK when asked if sure want to save
        Click on Publish at bottom of the page
        Click OK when asked if sure want to publish

        Expected Result:
        The exercise is published
        """
        self.ps.test_updates['name'] = 'cc1.04.022' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.022',
            '7676'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7677 - 023 - Content Analyst | Able to save an exercise as a draft
    @pytest.mark.skipif(str(7677) not in TESTS, reason='Excluded')
    def test_content_analyst_able_to_save_an_exercise_as_a_draft_7677(self):
        """Able to save an exercise as a draft.

        Steps:
        Open a new page of OpenStax Exercises
        Sign with username 'openstax' and password 'password'
        Go back to exercises on OpenStax Tutor page
        For an exercise, click on 'edit' button on the lower right corner
        Edit the exercise
        Click on Save at bottom of the page
        Click OK when asked if sure want to save

        Expected Result:
        The exercise is saved as a draft
        After refreshing the page, the changes made were saved
        """
        self.ps.test_updates['name'] = 'cc1.04.023' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.023',
            '7677'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7678 - 024 - Teacher | Able to save an exercise as a draft
    @pytest.mark.skipif(str(7678) not in TESTS, reason='Excluded')
    def test_teacher_able_to_save_an_exercise_as_a_draft_7678(self):
        """Able to save an exercise as a draft.

        Steps:
        Log into Tutor as a teacher
        View exercises
        Open a new page of OpenStax Exercises
        Sign with username 'openstax' and password 'password'
        Go back to exercises on OpenStax Tutor page
        For an exercise, click on 'edit' button on the lower right corner
        Edit the exercise
        Click on Save at bottom of the page
        Click OK when asked if sure want to save

        Expected Result:
        The exercise is saved as a draft
        After refreshing the page, the changes made were saved
        """
        self.ps.test_updates['name'] = 'cc1.04.024' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.024',
            '7678'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7679 - 025 - Admin | Able to save an exercise as a draft
    @pytest.mark.skipif(str(7679) not in TESTS, reason='Excluded')
    def test_admin_able_to_save_an_exercise_as_a_draft_7679(self):
        """Able to save an exercise as a draft.

        Steps:
        Log into Tutor as an admin
        View exercises
        Open a new page of OpenStax Exercises
        Sign with username 'openstax' and password 'password'
        Go back to exercises on OpenStax Tutor page
        For an exercise, click on 'edit' button on the lower right corner
        Edit the exercise
        Click on Save at bottom of the page
        Click OK when asked if sure want to save

        Expected Result:
        The exercise is saved as a draft
        After refreshing the page, the changes made were saved
        """
        self.ps.test_updates['name'] = 'cc1.04.025' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.025',
            '7679'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7681 - 026 - Student | Denied access to exercise solutions
    # on Exercises
    @pytest.mark.skipif(str(7681) not in TESTS, reason='Excluded')
    def test_student_denied_access_to_solutions_on_exercises_7681(self):
        """Denied access to exercise solutions on Exercises.

        Steps:
        Log into OpenStax Exercise as a student
        Click "Search"
        Enter exercise ID

        Expected Result:
        Information and concent of the exercises is shown
        but not the correct answer
        """
        self.ps.test_updates['name'] = 'cc1.04.026' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.026',
            '7681'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7682 - 027 - Non-user | Denied access to exercise solutions
    # on Exercises
    @pytest.mark.skipif(str(7682) not in TESTS, reason='Excluded')
    def test_nonuser_denied_access_to_exercise_solutions_7682(self):
        """Denied access to exercise solutions on Exercises.

        Steps:
        Log out current OpenStax Exercise account
        In the URL bar, type in:
        "https://exercises-dev.openstax.org/api/exercises?q=<exercise ID>",
        <exercise ID> is the ID of the exercise to search at

        Expected Result:
        Information and content of the exercises is shown
        but not the correct answer
        """
        self.ps.test_updates['name'] = 'cc1.04.027' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.027',
            '7682'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7683 - 028 - Content Analyst | Able to repair content errata
    # submitted by users
    @pytest.mark.skipif(str(7683) not in TESTS, reason='Excluded')
    def test_content_analyst_able_to_repair_content_errata_7683(self):
        """Able to repair content errata submitted by users.

        Steps:
        Login to http://openstaxcollege.org/ with a staff account.
        Click the 'Staff' at the top left.
        Click 'Errata' from the menu.
        Select 'all' for the following: Book, Severity, Priority, Format
        Select 'New' for Status.
        Click on the numbers to review a report.
        Fix tickets with typos and minor issues, then change the ticket status
        to 'Published'.

        Expected Result:
        Correct module is published
        """
        self.ps.test_updates['name'] = 'cc1.04.028' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.028',
            '7683'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7686 - 029 - Content Analyst | Publish reviewed content
    # from content creators
    @pytest.mark.skipif(str(7686) not in TESTS, reason='Excluded')
    def test_content_analyst_publish_reviewed_content_from_content_7686(self):
        """Publish reviewed content from content creators.

        Steps:
        Login to http://openstaxcollege.org/ with a staff account.
        Click the 'Staff' at the top left.
        Click 'Errata' from the menu.
        Select 'all' for the following: Book, Severity, Priority, Format
        Select 'Approved for Publish' for Status
        Change status of the Errata to 'Published'

        Expected Result:
        Reviewed content is published
        """
        self.ps.test_updates['name'] = 'cc1.04.029' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.029',
            '7686'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7687 - 030 - Content Analyst | In the QA exercise view
    # render the Markdown
    @pytest.mark.skipif(str(7687) not in TESTS, reason='Excluded')
    def test_content_analyst_in_the_qa_view_render_the_markdown_7687(self):
        """In the QA exercise view render the Markdown.

        Steps:
        Log into Tutor as a content analyst user
        Select 'QA Content' from the User Menu
        Select 'Physics' from Available Books Menu
        From the side bar on the left choose section
        '2.4 Velocity vs. Time Graphs'
        Scroll down to the third exercise:
        'For the position versus time graph above what would the corresponding
            velocity graph look like?''

        Expected Result:
        View a graph titled 'Position vs. Time', which is a render of Markdown
        """
        self.ps.test_updates['name'] = 'cc1.04.030' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.030',
            '7687'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
