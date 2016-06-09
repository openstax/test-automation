"""Tutor v1, Epic 42 - Edit Course Settings and Roster."""

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
    str([8258, 8259, 8260, 8261, 8262, 
         8263, 8264, 8265, 8266, 8267])  # NOQA
)


@PastaDecorator.on_platforms(BROWSERS)
class TestEpicName(unittest.TestCase):
    """T1.42 - Edit Course Settings and Roster."""

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

    # Case C8258 - 001 - Teacher | Edit the course name
    @pytest.mark.skipif(str(8258) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Edit the course name.

        Steps:

        Click on the user menu in the upper right corner of the page
        Click "Course Roster"
        Click the "Rename Course" button that is next to the course name
        Enter a new course name 
        Click the "Rename" button
        Click the X that is on the upper right corner of the dialogue box


        Expected Result:

        The course name is edited.

        """
        self.ps.test_updates['name'] = 't1.42.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.42',
            't1.42.001',
            '8258'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8259 - 002 - Teacher | Remove an instructor from the course
    @pytest.mark.skipif(str(8259) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Remove an instructor from the course.

        Steps:

        Click on the user menu in the upper right corner of the page
        Click "Course Roster"
        Click the "Remove" button for an instructor under the Instructors section 
        Click "Remove" on the box that pops up


        Expected Result:

        The instructor is removed from the Instructors list.

        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)


    # Case C8260 - 003 - Teacher | Remove the last instructor from the course
    @pytest.mark.skipif(str(8260) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Remove the last instructor from the course.

        Steps:

        Click on the user menu in the upper right corner of the page
        Click "Course Roster"
        Click the "Remove" button for an instructor under the Instructors section 
        Click "Remove" on the box that pops up


        Expected Result:

        The instructor is removed from the Instructors list.

        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)


    # Case C8261 - 004 - Teacher | Add a period
    @pytest.mark.skipif(str(8261) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Add a period.

        Steps:

        Click on the user menu in the upper right corner of the page
        Click "Course Roster"
        Click "+ Add Period" 
        Enter a period name into the Period Name text box
        Click "Add"


        Expected Result:

        A new period is added.

        """
        self.ps.test_updates['name'] = 't1.42.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.42',
            't1.42.004',
            '8261'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8262 - 005 - Teacher | Rename a period 
    @pytest.mark.skipif(str(8262) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Rename a period.

        Steps:

        Click on the user menu in the upper right corner of the page
        Click "Course Roster"
        Click "Rename Period"
        Enter a new period name into the Period Name text box
        Click "Rename"


        Expected Result:

        A period is renamed.

        """
        self.ps.test_updates['name'] = 't1.42.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.42',
            't1.42.005',
            '8262'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8263 - 006 - Teacher | Delete an empty period
    @pytest.mark.skipif(str(8263) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Delete an empty period.

        Steps:

        Click on the user menu in the upper right corner of the page
        Click "Course Roster"
        Click on an empty period 
        Click "Delete Period" 
        Click "Delete" on the dialogue box


        Expected Result:

        An empty period is deleted.

        """
        self.ps.test_updates['name'] = 't1.42.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.42',
            't1.42.006',
            '8263'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8263 - 006 - Teacher | Delete an empty period
    @pytest.mark.skipif(str(8263) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Delete an empty period.

        Steps:

        Click on the user menu in the upper right corner of the page
        Click "Course Roster"
        Click on an empty period 
        Click "Delete Period" 
        Click "Delete" on the dialogue box


        Expected Result:

        An empty period is deleted.

        """
        self.ps.test_updates['name'] = 't1.42.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.42',
            't1.42.006',
            '8263'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8264 - 007 - Teacher | Attempt to delete a non-empty period 
    @pytest.mark.skipif(str(8264) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Attempt to delete a non-empty period.

        Steps:

        Click on the user menu in the upper right corner of the page
        Click "Course Roster"
        Click on a non-empty period 
        Click "Delete Period"


        Expected Result:

        A dialogue box that says "Only periods without students enrolled can be deleted" pops up. 
        The user is unable to delete non-empty periods

        """
        self.ps.test_updates['name'] = 't1.42.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.42',
            't1.42.007',
            '8264'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8265 - 008 - Teacher | Move a student to another period
    @pytest.mark.skipif(str(8265) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Move a student to another period.

        Steps:

        Click on the user menu in the upper right corner of the page
        Click "Course Roster"
        Click "Change Period" for a student under the Roster section
        Click the desired period to move a student


        Expected Result:

        A student is moved to another period

        """
        self.ps.test_updates['name'] = 't1.42.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.42',
            't1.42.008',
            '8265'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8266 - 009 - Teacher | Drop a student
    @pytest.mark.skipif(str(8266) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Drop a student.

        Steps:

        Click on the user menu in the upper right corner of the page
        Click "Course Roster"
        Click "Drop" for a student under the Roster section
        Click "Drop" in the box that pops up


        Expected Result:

        A student is dropped from the course and is put under the Dropped Students section

        """
        self.ps.test_updates['name'] = 't1.42.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.42',
            't1.42.009',
            '8266'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8267 - 010 - Teacher | Readd a dropped student
    @pytest.mark.skipif(str(8267) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Readd a dropped student.

        Steps:

        Click on the user menu in the upper right corner of the page
        Click "Course Roster"
        Click "Add Back to Active Roster" for a student under the Dropped Students section
        Click "Add" on the box that pops up


        Expected Result:

        A student is added back to the course

        """
        self.ps.test_updates['name'] = 't1.42.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.42',
            't1.42.010',
            '8267'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True