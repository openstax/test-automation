"""Tutor v1, Epic 21 - Create an event."""

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
    str([8117, 8118, 8119, 8120, 
         8121, 8122, 8123, 8124, 
         8125, 8126, 8127, 8128, 
         8129, 8130, 8131, 8132, 
         8133, 8134, 8135, 8136
         8137, 8138, 8139, 8140
         8141, 8142, 8143, 8144
         8145, 8146, 8147])  # NOQA
)


@PastaDecorator.on_platforms(BROWSERS)
class TestEpicName(unittest.TestCase):
    """T1.21 - Create an event."""

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

    # Case C8117 - 001 - Teacher | Teacher creates an event
    @pytest.mark.skipif(str(8117) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Teacher creates an event.

        Steps:

        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Event' option

        Enter an event name into the Event name text box [user decision]
        [optional] Enter an assignment description into the Assignment description or special instructions text box
        [optional] Enter into Open Date text field date as MM/DD/YYYY
        Enter into Due Date text field date as MM/DD/YYYY
        Click on the Publish' button


        Expected Result:

        Takes user back to calendar dashboard. 
        Event appears on its due date

        """
        self.ps.test_updates['name'] = 't1.21.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.21',
            't1.21.001',
            '8117'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8118 - 002 - Teacher | Add an event using the Add Assignment drop down menu
    @pytest.mark.skipif(str(8118) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Add an event using the Add Assignment drop down menu.

        Steps:

        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Event' option

        Enter an event name into the Event name text box [user decision]
        [optional] Enter an assignment description into the Assignment description or special instructions text box
        [optional] Enter into Open Date text field date as MM/DD/YYYY
        Enter into Due Date text field date as MM/DD/YYYY
        Click on the Publish' button


        Expected Result:

        Takes user back to calendar dashboard. 
        Event appears on its due date

        """
        self.ps.test_updates['name'] = 't1.21.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.21',
            't1.21.002',
            '8118'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8119 - 003 - Teacher | Add an event using the calendar date
    @pytest.mark.skipif(str(8119) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Add an event using the calendar date.

        Steps:

        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Event' option

        Enter an event name into the Event name text box [user decision]
        [optional] Enter an assignment description into the Assignment description or special instructions text box
        [optional] Enter into Open Date text field date as MM/DD/YYYY
        Enter into Due Date text field date as MM/DD/YYYY
        Click on the Publish' button


        Expected Result:

        Takes user back to calendar dashboard. 
        Event appears on its due date

        """
        self.ps.test_updates['name'] = 't1.21.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.21',
            't1.21.003',
            '8119'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8120 - 004 - Teacher | Set open and due dates for all periods collectively
    @pytest.mark.skipif(str(8120) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Set open and due dates for all periods collectively.

        Steps:

        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Event' option

        Enter an event name into the Event name text box [user decision]
        [optional] Enter an assignment description into the Assignment description or special instructions text box
        [the All Periods radio button should be selected by default]
        Enter into Open Date text field date as MM/DD/YYYY
        Enter into Due Date text field date as MM/DD/YYYY
        Click on the 'Publish' button


        Expected Result:

        Takes user back to calendar dashboard. 
        Event appears on its due date

        """
        self.ps.test_updates['name'] = 't1.21.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.21',
            't1.21.004',
            '8120'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8121 - 005 - Teacher | Set open and due dates for periods individually
    @pytest.mark.skipif(str(8121) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Set open and due dates for periods individually.

        Steps:

        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Event' option

        Enter an event name into the Event name text box [user decision]
        [optional] Enter an assignment description into the Assignment description or special instructions text box
        Click on the "Individual Periods" radio button
        [optional] Click on the check boxes next to periods that the event is not for
        For each period that is checked off
        - Enter into Open Date text field date as MM/DD/YYYY
        - Enter into Due Date text field date as MM/DD/YYYY
        Click on the Publish' button


        Expected Result:

        Takes user back to calendar dashboard. 
        Event appears on its due date(s). 
        If there are multiple due dates event appears across all dates starting at earliest due date, through latest due date.

        """
        self.ps.test_updates['name'] = 't1.21.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.21',
            't1.21.005',
            '8121'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8122 - 006 - Teacher | Save a draft event
    @pytest.mark.skipif(str(8122) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Save a draft event.

        Steps:

        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Event' option

        Enter an event name into the Event name text box [user decision]
        [optional] Enter an assignment description into the Assignment description or special instructions text box
        [optional] Enter into Open Date text field date as MM/DD/YYYY
        Enter into Due Date text field date as MM/DD/YYYY
        Click on the 'Save As Draft' button


        Expected Result:

        Takes user back to calendar dashboard. 
        Event appears on its due date with the word 'draft' before its name

        """
        self.ps.test_updates['name'] = 't1.21.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.21',
            't1.21.006',
            '8122'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8123 - 007 - Teacher | Publish a new event
    @pytest.mark.skipif(str(8123) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Publish a new event.

        Steps:

        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Event' option

        Enter an event name into the Event name text box [user decision]
        [optional] Enter an assignment description into the Assignment description or special instructions text box
        [optional] Enter into Open Date text field date as MM/DD/YYYY
        Enter into Due Date text field date as MM/DD/YYYY
        Click on the Publish' button


        Expected Result:

        Takes user back to calendar dashboard. 
        Event appears on its due date

        """
        self.ps.test_updates['name'] = 't1.21.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.21',
            't1.21.007',
            '8123'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8124 - 008 - Teacher | Publish a draft event
    @pytest.mark.skipif(str(8124) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Publish a draft event.

        Steps:

        On the calendar dashboard click on a draft assignment
        Click on the 'Publish' button


        Expected Result:

        Takes user back to calendar dashboard. 
        Event appears on its due date (the word 'draft' in no longer before its name).

        """
        self.ps.test_updates['name'] = 't1.21.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.21',
            't1.21.008',
            '8124'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8125 - 009 - Teacher | Cancel a new event before making any changes using the Cancel button
    @pytest.mark.skipif(str(8125) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Cancel a new event before making any changes using the Cancel button.

        Steps:

        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Event' option
        Click on the "Cancel" button


        Expected Result:

        Takes user back to calendar dashboard. 
        No changes have been made.

        """
        self.ps.test_updates['name'] = 't1.21.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.21',
            't1.21.009',
            '8125'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8126 - 010 - Teacher | Cancel a new event after making any changes using the Cancel button
    @pytest.mark.skipif(str(8126) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Cancel a new event after making any changes using the Cancel button.

        Steps:

        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Event' option

        Do at least one of the following:
        - Enter an event name into the Event name text box
        - Enter an assignment description into the Assignment description or special instructions text box
        - Enter into Open Date text field date as MM/DD/YYYY
        - Enter into Due Date text field date as MM/DD/YYYY

        Click on the "Cancel" button
        Click on the "ok" button


        Expected Result:

        Takes user back to calendar dashboard. 
        No changes have been made.

        """
        self.ps.test_updates['name'] = 't1.21.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.21',
            't1.21.010',
            '8126'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8127 - 011 - Teacher | Cancel a new event before making any changes using the X
    @pytest.mark.skipif(str(8127) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Cancel a new event before making any changes using the X.

        Steps:

        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Event' option
        Click on the "x" button


        Expected Result:

        Takes user back to calendar dashboard. 
        No changes have been made.

        """
        self.ps.test_updates['name'] = 't1.21.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.21',
            't1.21.011',
            '8127'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8128 - 012 - Teacher | Cancel a new event after making any changes using the X
    @pytest.mark.skipif(str(8128) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Cancel a new event after making any changes using the X.

        Steps:

        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Event' option
        Click on the "x" button


        Expected Result:

        Takes user back to calendar dashboard. 
        No changes have been made.

        """
        self.ps.test_updates['name'] = 't1.21.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.21',
            't1.21.012',
            '8128'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8129 - 013 - Teacher | Cancel a draft event before making any changes using the Cancel button
    @pytest.mark.skipif(str(8129) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Cancel a draft event before making any changes using the Cancel button.

        Steps:

        Click on a draft event on the calendar dashboard
        Click on the "Cancel" button
        click on the "ok" button


        Expected Result:

        Takes user back to calendar dashboard. 
        No changes have been made.

        """
        self.ps.test_updates['name'] = 't1.21.013' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.21',
            't1.21.013',
            '8129'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8130 - 014 - Teacher | Cancel a draft event after making changes using the Cancel button
    @pytest.mark.skipif(str(8130) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Cancel a draft event after making changes using the Cancel button.

        Steps:

        Click on a draft event on the calendar dashboard
        Click on the "Cancel" button
        click on the "ok" button


        Expected Result:

        Takes user back to calendar dashboard. 
        No changes have been made.

        """
        self.ps.test_updates['name'] = 't1.21.014' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.21',
            't1.21.014',
            '8130'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8131 - 015 - Teacher | Cancel a draft event before making any changes using the X
    @pytest.mark.skipif(str(8131) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Cancel a draft event before making any changes using the X.

        Steps:

        Click on a draft event
        Click on the "x" button
        click on the "ok" button


        Expected Result:

        Takes user back to calendar dashboard. 
        No changes have been made.

        """
        self.ps.test_updates['name'] = 't1.21.015' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.21',
            't1.21.015',
            '8131'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8132 - 016 - Teacher | Cancel a draft event after making changes using the X
    @pytest.mark.skipif(str(8132) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Cancel a draft event after making changes using the X.

        Steps:

        Click on a draft event
        Do at least one of the following:
        - Enter an event name into the Event name text box
        - Enter an assignment description into the Assignment description or special instructions text box
        - Enter into Open Date text field date as MM/DD/YYYY
        - Enter into Due Date text field date as MM/DD/YYYY

        Click on the "x" button
        click on the "ok" button


        Expected Result:

        Takes user back to calendar dashboard. 
        No changes have been made.

        """
        self.ps.test_updates['name'] = 't1.21.016' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.21',
            't1.21.016',
            '8132'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8133 - 017 - Teacher | Attempt to publish a event with blank required fields
    @pytest.mark.skipif(str(8133) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Attempt to publish a event with blank required fields.

        Steps:

        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Event' option
        Click on the "Publish" button


        Expected Result:

        Remains on the Add Event page. 
        Does not allow user to publish event. 
        Event name field becomes red, and specifies that it is a required field.

        """
        self.ps.test_updates['name'] = 't1.21.017' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.21',
            't1.21.017',
            '8133'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8134 - 018 - Teacher | Attempt to save a draft event with blank required fields
    @pytest.mark.skipif(str(8134) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Attempt to save a draft event with blank required fields

        Steps:

        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Event' option
        Click on the "Save As Draft" button


        Expected Result:

        Remains on the Add Event page. 
        Does not allow user to publish event. 
        Event name field becomes red, and specifies that it is a required field.

        """
        self.ps.test_updates['name'] = 't1.21.018' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.21',
            't1.21.018',
            '8134'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8135 - 019 - Teacher | Delete an unopened event
    @pytest.mark.skipif(str(8135) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Delete an unopened event. 

        Steps:

        Click on an unopened event on the calendar
        Click on the 'Edit Event' button
        Click on the "Delete Assignment" button
        Click on the "ok" button


        Expected Result:

        Takes user back to calendar dashboard.
        Event has been removed. 

        """
        self.ps.test_updates['name'] = 't1.21.019' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.21',
            't1.21.019',
            '8135'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8136 - 020 - Teacher | Attempt to delete an open event
    @pytest.mark.skipif(str(8136) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Attempt to delete an open event. 

        Steps:

        Click on an open event on the calendar
        Click on the 'Edit Event' button


        Expected Result:

        There is no "Delete Assignment" found. 

        """
        self.ps.test_updates['name'] = 't1.21.020' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.21',
            't1.21.020',
            '8136'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8137 - 021 - Teacher | Delete a draft event
    @pytest.mark.skipif(str(8137) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Delete a draft event. 

        Steps:

        Click on a draft event on the calendar
        Click on the "Delete Assignemnt" button
        Click on the "ok" button


        Expected Result:

        Takes user back to calendar dashboard. 
        Draft Event has been removed.

        """
        self.ps.test_updates['name'] = 't1.21.021' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.21',
            't1.21.021',
            '8137'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8138 - 022 - Teacher | Add a description to an event 
    @pytest.mark.skipif(str(8138) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Add a description to an event. 

        Steps:

        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Event' option
        Enter an event name into the Event name text box
        Enter an assignment description into the Assignment description or special instructions text box
        [optional] Enter into Open Date text field date as MM/DD/YYYY
        Enter into Due Date text field date as MM/DD/YYYY
        Click on the "Publish" button


        Expected Result:

        Takes user back to calendar dashboard. 
        Event appears on due date, with correct description.

        """
        self.ps.test_updates['name'] = 't1.21.022' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.21',
            't1.21.022',
            '8138'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8139 - 023 - Teacher | Change a description for a draft event 
    @pytest.mark.skipif(str(8139) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Change a description for a draft event. 

        Steps:

        Click on a draft event
        Enter a new event description into the Assignment description or special instructions text box
        Click on the "Save As Draft" button


        Expected Result:

        Takes user back to calendar dashboard. 
        The description of the draft event has been updated.

        """
        self.ps.test_updates['name'] = 't1.21.023' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.21',
            't1.21.023',
            '8139'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8140 - 024 - Teacher | Change a description for an open event
    @pytest.mark.skipif(str(8140) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Change a description for an open event. 

        Steps:

        Click on an open event
        Click on the "Edit Event" button
        Enter a new event description into the Assignment description or special instructions text box
        Click on the "Publish" button


        Expected Result:

        Takes user back to calendar dashboard. 
        Event has been updated to have new description.

        """
        self.ps.test_updates['name'] = 't1.21.024' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.21',
            't1.21.024',
            '8140'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8141 - 025 - Teacher | Add a name to an event 
    @pytest.mark.skipif(str(8141) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Add a name to an event. 

        Steps:

        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Event' option

        Enter an event name into the Event name text box [user decision]
        [optional] Enter an assignment description into the Assignment description or special instructions text box
        [optional] Enter into Open Date text field date as MM/DD/YYYY
        Enter into Due Date text field date as MM/DD/YYYY
        Click on the Publish' button


        Expected Result:

        Takes user back to calendar dashboard. 
        Event appears on its due date

        """
        self.ps.test_updates['name'] = 't1.21.025' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.21',
            't1.21.025',
            '8141'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8142 - 026 - Teacher | Change a name for a draft event
    @pytest.mark.skipif(str(8142) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Change a name for a draft event. 

        Steps:

        Click on the calendar click on a draft event
        Enter a new event name into the Event name text box
        Click on the 'Save As Draft' button


        Expected Result:

        Takes user back to calendar dashboard. 
        Draft event name has been updated.

        """
        self.ps.test_updates['name'] = 't1.21.026' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.21',
            't1.21.026',
            '8142'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8143 - 027 - Teacher | Change a name for an open event
    @pytest.mark.skipif(str(8143) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Change a name for an open event. 

        Steps:

        Click on the open event on the calendar
        Click on the 'Edit Event' button
        Enter a new name into the Event name text box
        Click on the "Publish" button


        Expected Result:

        Takes user back to calendar dashboard. 
        Event has been updated to have its new name.

        """
        self.ps.test_updates['name'] = 't1.21.027' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.21',
            't1.21.027',
            '8143'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8144 - 028 - Teacher | Info icon shows definitions for the Add Event status bar buttons
    @pytest.mark.skipif(str(8144) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Info icon shows definitions for the Add Event status bar buttons. 

        Steps:

        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Event' option
        Click on the info icon


        Expected Result:

        Displays description of Publish, Cancel, and Save As Draft statuses.

        """
        self.ps.test_updates['name'] = 't1.21.028' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.21',
            't1.21.028',
            '8144'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8145 - 029 - Teacher | Change all fields in an unopened, published event
    @pytest.mark.skipif(str(8145) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Change all fields in an unopened, published event. 

        Steps:

        Click on the calendar click on an unopened event
        Click on the "Edit Event" button

        Enter a new event name into the Event name text box
        Enter a new assignment description into the Assignment description or special instructions text box
        Enter into Open Date text field a new date as MM/DD/YYYY
        Enter into Due Date text field a new date as MM/DD/YYYY
        Click on the Publish' button


        Expected Result:

        Takes user back to calendar dashboard. 
        Event appears on its new due date with updated information.

        """
        self.ps.test_updates['name'] = 't1.21.029' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.21',
            't1.21.029',
            '8145'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8146 - 030 - Teacher | Change all fields in a draft event
    @pytest.mark.skipif(str(8146) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Change all fields in a draft event. 

        Steps:

        Click on the calendar click on a draft event

        Enter a new event name into the Event name text box
        Enter a new assignment description into the Assignment description or special instructions text box
        Enter into Open Date text field a new date as MM/DD/YYYY
        Enter into Due Date text field a new date as MM/DD/YYYY
        Click on the 'Save As Draft' button


        Expected Result:
        
        Takes user back to calendar dashboard. 
        Event appears on its new due date with updated information.

        """
        self.ps.test_updates['name'] = 't1.21.030' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.21',
            't1.21.030',
            '8146'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8147 - 031 - Teacher | Change the name, description, and due dates in an opened event
    @pytest.mark.skipif(str(8147) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Change the name, description, and due dates in an opened event. 

        Steps:

        Click on the calendar click on an open event
        Click on the "Edit Event" button

        Enter a new event name into the Event name text box
        Enter a new assignment description into the Assignment description or special instructions text box
        Enter into Due Date text field a new date as MM/DD/YYYY
        Click on the 'Publish' button


        Expected Result:
        
        Takes user back to calendar dashboard. 
        Event appears on its new due date with updated information.

        """
        self.ps.test_updates['name'] = 't1.21.031' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.21',
            't1.21.031',
            '8147'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


