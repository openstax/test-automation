"""Concept Coach v1, Epic 4 - Content Preparation and Import."""

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
from staxing.helper import Admin, ContentQA, Student, Exercise Editor, Exercise Author  # NOQA

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': '50.0',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([7651, 7652, 7653, 7654, 7655, 
         7656, 7657, 7658, 7659, 7660, 
         7661, 7662, 7663, 7665, 7667, 
         7669, 7670, 7672, 7673, 7674, 
         7675, 7676, 7677, 7678, 7679, 
         7681, 7682, 7683, 7686, 7687])  # NOQA
)


@PastaDecorator.on_platforms(BROWSERS)
class TestEpicName(unittest.TestCase):
    """CC1.04 - Exercise Editing and QA."""

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

    # Case C7651 - 001 - Content Analyst | See the full error list from a failed book import
    @pytest.mark.skipif(str(7651) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
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

        self.ps.test_updates['passed'] = True


    # Case C7652 - 002 - Admin | See the full error list from a failed book import
    @pytest.mark.skipif(str(7652) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
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

        self.ps.test_updates['passed'] = True


    # Case C7653 - 003 - Admin | Add the Content Analyst role to a user
    @pytest.mark.skipif(str(7653) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
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

        self.ps.test_updates['passed'] = True


    # Case C7654 - 004 - Admin | Add the Exercise Editor role to a user
    @pytest.mark.skipif(str(7654) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Add the Exercise Editor role to a user.

        Steps: 

        Log into Tutor as an administrator 
        From the User Menu select 'Admin'
        Click on 'Users' in the header
        Locate the user in the list
        Click on the 'Edit' button to the right of the text columns
        Check the box to the right of 'Exercise editor'
        Click on the 'Save' button


        Expected Result:

        The role is saved to the user

        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)


    # Case C7655 - 005 - Admin | Add the Exercise Author role to a user
    @pytest.mark.skipif(str(7655) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Add the Exercise Editor role to a user.

        Steps: 

        Log into Tutor as an administrator 
        From the User Menu select 'Admin'
        Click on 'Users' in the header
        Locate the user in the list
        Click on the 'Edit' button to the right of the text columns
        Check the box to the right of 'Exercise author'
        Click on the 'Save' button


        Expected Result:

        The role is saved to the user

        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)


    # Case C7656 - 006 - Content Analyst | Add an ecosystem comment
    @pytest.mark.skipif(str(7656) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Add an ecosystem comment.

        Steps: 

        Log into Tutor as a content analyst user 
        Select 'Customer Analyst' from the User Menu
        Select 'Ecosystems' from the menu
        In the Comments Column change a comment and click on Save.


        Expected Result:

        The comment is displayed on the ecosystem to the right of the book title

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

        self.ps.test_updates['passed'] = True


    # Case C7657 - 007 - Admin | Add an ecosystem comment
    @pytest.mark.skipif(str(7657) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Add an ecosystem comment.

        Steps: 

        Log into Tutor as an administrative user 
        Select 'Admin' from the User Menu
        Click on the 'Content' heading
        Select 'Ecosystems' from the menu
        In the Comments column edit a comment. Click on Save.


        Expected Result:

        The comment is displayed on the ecosystem to the right of the book title

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

        self.ps.test_updates['passed'] = True


    # Case C7658 - 008 - Content Analyst | Delete an unused ecosystem
    @pytest.mark.skipif(str(7658) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Delete an unused ecosystem.

        Steps: 

        Log into Tutor as Content Analyst 
        From the user menu select 'Customer Analyst'
        Select 'Ecosystems'
        Scroll a bit and find a course that has the delete button in the last column. Click on it.
        This should delete the ecosystem.


        Expected Result:

        The unassigned ecosystem is removed from the system

        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)


    # Case C7659 - 009 - Admin | Delete an unused ecosystem
    @pytest.mark.skipif(str(7659) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Delete an unused ecosystem.

        Steps: 

        Log into Tutor as Admin 
        From the user menu select 'Admin'
        From the 'Content' menu select 'Ecosystems'
        Scroll a bit and find a course that has the delete button in the last column. Click on it.
        This should delete the ecosystem.


        Expected Result:

        The unassigned ecosystem is removed from the system

        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)


    # Case C7660 - 010 - Content Analyst | Unable to delete an assigned ecosystem
    @pytest.mark.skipif(str(7660) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Unable to delete an assigned ecosystem.

        Steps: 

        Log into Tutor as Content Analyst 
        From the user menu select 'Customer Analyst'
        From the header select 'Ecosystems'
        In the last column ensure that for some books the delete option is not available.


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

        self.ps.test_updates['passed'] = True


    # Case C7661 - 012 - Admin | Unable to delete an assigned ecosystem
    @pytest.mark.skipif(str(7661) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Unable to delete an assigned ecosystem.

        Steps: 

        Log into Tutor as Admin 
        From the user menu select 'Admin'
        From the 'Content' menu select 'Ecosystems'
        In the last column ensure that for some books the delete option is not available.


        Expected Result:

        There should be no way for people to delete the assignment

        """
        self.ps.test_updates['name'] = 'cc1.04.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.012',
            '7661'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C7662 - 013 - Content Analyst | View all exercises for a CNX page module / Tutor section
    @pytest.mark.skipif(str(7662) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """View all exercises for a CNX page module / Tutor section.

        Steps: 

        Log into Tutor as a content analyst user 
        Select 'QA Content' from the User Menu
        Click on any non-introductory section on the left-side bar


        Expected Result:

        Exercises for that section is displayed

        """
        self.ps.test_updates['name'] = 'cc1.04.013' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.013',
            '7662'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C7663 - 014 - Content Analyst | From the QA exercise view open an exercise for editing in a new tab
    @pytest.mark.skipif(str(7663) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """From the QA exercise view open an exercise for editing in a new tab.

        Steps: 

        Log into Tutor as a content analyst user 
        Select 'QA Content' from the User Menu
        Click on any non-introductory section on the left-side bar

        Click on 'edit' on the lower right corner of the exercise
        Click "Close" on the popup box 
        Sign in as exercise editor


        Expected Result:

        View a new tab of OpenStax Exercises editing page for corresponding exercise

        """
        self.ps.test_updates['name'] = 'cc1.04.014' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.014',
            '7663'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C7665 - 015 - Content Analyst | Able to filter exercises in the QA exercise viewer
    @pytest.mark.skipif(str(7665) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Able to filter exercises in the QA exercise viewer.

        Steps: 

        Click 'Exercise Types', view the list of exercise types with check box ahead
        Leave one type checked and others unchecked


        Expected Result:

        Only the exercises of checked type is listed

        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)


    # Case C7667 - 016 - Content Analyst | Display the QA view of a book section
    @pytest.mark.skipif(str(7667) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Display the QA view of a book section.

        Steps: 

        Log into Tutor as a content analyst user
        Select 'QA Content' from the User Menu
        Select 'Show Content' from the menu


        Expected Result:

        See the QA view of a book section

        """
        self.ps.test_updates['name'] = 'cc1.04.016' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.016',
            '7667'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C7669 - 017 - Content Analyst | Able to navigate between book sections in the QA view
    @pytest.mark.skipif(str(7669) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Able to navigate between book sections in the QA view.

        Steps: 

        Log into Tutor as a content analyst user
        Select 'QA Content' from the User Menu
        Select 'Show Content' from the menu

        Click on the content sign on upper-left corner of the page to show table of contents
        Click on any section to view


        Expected Result:

        Chosen section is displayed

        """
        self.ps.test_updates['name'] = 'cc1.04.017' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.017',
            '7669'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C7670 - 018 - Admin | Add the Content Analyst role to DMS user accounts
    @pytest.mark.skipif(str(7670) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
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
        self.ps.test_updates['name'] = 'cc1.04.018' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.018',
            '7670'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C7672 - 019 - Content Analyst | In the QA exercise view render the LaTex
    @pytest.mark.skipif(str(7672) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """In the QA exercise view render the LaTex.

        Steps: 

        Log into Tutor as a content analyst user (content : password)
        Select 'QA Content' from the User Menu
        Select 'Physics' from Available Books Menu
        From the side bar on the left choose section '6.1 Angle of Rotation and Angular Velocity'
        Scroll down to the 4th exercise: What equation defines angular velocity?

        Expected Result:

        View equations that are render of LaTex

        """
        self.ps.test_updates['name'] = 'cc1.04.019' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.019',
            '7672'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C7673 - 020 - Content Analyst | In the QA exercise view verify that the exercise ID is shown
    @pytest.mark.skipif(str(7673) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
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
        self.ps.test_updates['name'] = 'cc1.04.020' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.020',
            '7673'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C7674 - 021 - Content Analyst | Able to publish an exercise
    @pytest.mark.skipif(str(7674) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Able to publish an exercise. 

        Steps: 

        Open a new page of OpenStax Exercises
        Sign with username 'openstax' and password 'password'
        Go back to exercises on OpenStax Tutor page
        For an exercise, click on 'edit' button on the lower right corner, you are directed to a new page of editing exercise
        Edit the exercise
        Click on Save at bottom of the page
        Click OK when asked if sure want to save
        Click on Publish at bottom of the page
        Click OK when asked if sure want to publish


        Expected Result:

        View the edited exercise

        """
        self.ps.test_updates['name'] = 'cc1.04.021' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.021',
            '7674'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C7675 - 022 - Exercise Editor | Able to publish an exercise
    @pytest.mark.skipif(str(7675) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Able to publish an exercise. 

        Steps: 

        Log into Tutor as an Exercise Editor
        View exercises

        Open a new page of OpenStax Exercises
        Sign with username 'openstax' and password 'password'
        Go back to exercises on OpenStax Tutor page
        For an exercise, click on 'edit' button on the lower right corner, you are directed to a new page of editing exercise
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
            '7675'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C7676 - 023 - Exercise Author | Able to publish an exercise
    @pytest.mark.skipif(str(7676) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Able to publish an exercise. 

        Steps: 

        Log into Tutor as an Exercise Author
        View exercises

        Open a new page of OpenStax Exercises
        Sign with username 'openstax' and password 'password'
        Go back to exercises on OpenStax Tutor page
        For an exercise, click on 'edit' button on the lower right corner, you are directed to a new page of editing exercise
        Edit the exercise
        Click on Save at bottom of the page
        Click OK when asked if sure want to save
        Click on Publish at bottom of the page
        Click OK when asked if sure want to publish


        Expected Result:

        The exercise is published

        """
        self.ps.test_updates['name'] = 'cc1.04.023' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.023',
            '7676'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C7677 - 024 - Content Analyst | Able to save an exercise as a draft
    @pytest.mark.skipif(str(7677) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Able to save an exercise as a draft. 

        Steps: 

        Open a new page of OpenStax Exercises
        Sign with username 'openstax' and password 'password'
        Go back to exercises on OpenStax Tutor page
        For an exercise, click on 'edit' button on the lower right corner, you are directed to a new page of editing exercise
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
            '7677'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C7678 - 025 - Exercise Editor | Able to save an exercise as a draft
    @pytest.mark.skipif(str(7678) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Able to save an exercise as a draft. 

        Steps: 

        Log into Tutor as an Exercise Editor
        View exercises

        Open a new page of OpenStax Exercises
        Sign with username 'openstax' and password 'password'
        Go back to exercises on OpenStax Tutor page
        For an exercise, click on 'edit' button on the lower right corner, you are directed to a new page of editing exercise
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
            '7678'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C7679 - 026 - Exercise Author | Able to save an exercise as a draft
    @pytest.mark.skipif(str(7679) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Able to save an exercise as a draft. 

        Steps: 

        Log into Tutor as an Exercise Author
        View exercises

        Open a new page of OpenStax Exercises
        Sign with username 'openstax' and password 'password'
        Go back to exercises on OpenStax Tutor page
        For an exercise, click on 'edit' button on the lower right corner, you are directed to a new page of editing exercise
        Edit the exercise
        Click on Save at bottom of the page
        Click OK when asked if sure want to save


        Expected Result:

        The exercise is saved as a draft
        After refreshing the page, the changes made were saved

        """
        self.ps.test_updates['name'] = 'cc1.04.026' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.026',
            '7679'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C7681 - 027 - Student | Denied access to exercise solutions on Exercises
    @pytest.mark.skipif(str(7681) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Denied access to exercise solutions on Exercises. 

        Steps: 

        Log into OpenStax Exercise (https://exercises-qa.openstax.org) as a student 
        Click "Search" 
        Enter exercise ID


        Expected Result:

        View information and content of the exercises but no correct answer is shown

        """
        self.ps.test_updates['name'] = 'cc1.04.027' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.027',
            '7681'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C7682 - 028 - Non-user | Denied access to exercise solutions on Exercises
    @pytest.mark.skipif(str(7682) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Denied access to exercise solutions on Exercises. 

        Steps: 

        Log out current OpenStax Exercise account
        In the URL bar, type in: "https://exercises-dev.openstax.org/api/exercises?q=<exercise ID>", 
        <exercise ID> is the ID of the exercise to search at


        Expected Result:

        View information and content of the exercises but now correct answer is shown

        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)


    # Case C7683 - 029 - Content Analyst | Able to repair content errata submitted by users
    @pytest.mark.skipif(str(7683) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Able to repair content errata submitted by users. 

        Steps: 

        Login to http://openstaxcollege.org/ with a staff account. 
        Click the “Staff” at the top left.
        Click “Errata” from the menu.
        Select “all” for the following: Book, Severity, Priority, Format
        Select “New” for Status. 
        Click on the numbers to review a report. 
        Fix tickets with typos and minor issues, then change the ticket status to “Published”.


        Expected Result:

        Correct module is published

        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)


    # Case C7686 - 030 - Content Analyst | Publish reviewed content from content creators
    @pytest.mark.skipif(str(7686) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Publish reviewed content from content creators. 

        Steps: 

        Login to http://openstaxcollege.org/ with a staff account. 
        Click the “Staff” at the top left.
        Click “Errata” from the menu.
        Select “all” for the following: Book, Severity, Priority, Format
        Select “Approved for Publish” for Status
        Change status of the Errata to “Published”.


        Expected Result:

        Reviewed content is published

        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)


    # Case C7687 - 031 - Content Analyst | In the QA exercise view render the Markdown
    @pytest.mark.skipif(str(7687) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """In the QA exercise view render the Markdown. 

        Steps: 

        Log into Tutor as a content analyst user (content : password)
        Select 'QA Content' from the User Menu
        Select 'Physics' from Available Books Menu
        From the side bar on the left choose section '2.4 Velocity vs. Time Graphs'
        Scroll down to the third exercise: 
        'For the position versus time graph above what would the corresponding velocity graph look like?''



        Expected Result:

        View a graph titled 'Position vs. Time', which is a render of Markdown

        """
        self.ps.test_updates['name'] = 'cc1.04.031' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.04',
            'cc1.04.031',
            '7687'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

