"""Product, Epic 18 - CreateAnExternalAssignment."""

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
    str([8085, 8086, 8087, 8088, 8089,
         8090, 8091, 8092, 8093, 8094,
         8095, 8096, 8097, 8098, 8099,
         8100, 8101, 8102, 8103, 8104,
         8105, 8106, 8107, 8108, 8109,
         8110, 8111, 8112, 8113, 8114,
         8115, 8116])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestCreateAnExternalAssignment(unittest.TestCase):
    """T1.18 - Epic TextCreate an external assignment."""

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

    # Case C8085 - 001 - Teacher | Add an external assignment using the Add Assignment menu
    @pytest.mark.skipif(str(8085) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_add_an_external_assignemnt_using_the_add_assignment_menu(self):
        """Add an external assignment using the Add Assignment menu

        Steps:
        Click on the Add Assignment drop down menu
        Click on the Add External Assignemnt option
        Enter an assignemnt name into the Assignemnt Name text box
        Enter date into the Due Date text feild as MM/DD/YYYY
        Enter a URL into the Assignment URL text box
        Click on the Publish button

        Expected Result:
        New external assignment appears on the calendar dashboard on its due date
        """
        self.ps.test_updates['name'] = 't1.18.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.001', '8085']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8086 - 002 - Teacher | Add an external assignment using the calendar_date
    @pytest.mark.skipif(str(8086) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_add_an_external_assignemnt_using_the_calendar_date(self):
        """Add an external assignment using the calendar_date

        Steps:
        Click on a calendar date
        Click on the Add External Assignemnt option
        Enter an assignemnt name into the Assignemnt Name text box
        Enter date into the Due Date text feild as MM/DD/YYYY
        Enter a URL into the Assignment URL text box
        Click on the Publish button

        Expected Result:
        New external assignment appears on the calendar dashboard on its due date
        """
        self.ps.test_updates['name'] = 't1.18.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.002', '8086']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8087 - 003 - Teacher | Set open and due dates for all periods collectively
    @pytest.mark.skipif(str(8087) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_set_open_and_due_dates_for_all_periods_collectively(self):
        """Set open and due dates for all periods collectively

        Steps:
        Click on the Add Assignment drop down menu
        Click on the Add External Assignemnt option
        Enter an assignemnt name into the Assignemnt Name text box
        Enter date into the Open Date text feild as MM/DD/YYYY
        Enter date into the Due Date text feild as MM/DD/YYYY
        Enter a URL into the Assignment URL text box
        Click on the Publish button

        Expected Result:
        New external assignment appears on the calendar dashboard on its due date
        """
        self.ps.test_updates['name'] = 't1.18.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.003', '8087']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8088 - 004 - Teacher | Set open and due dates for  periods individually
    @pytest.mark.skipif(str(8088) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_set_open_and_due_dates_for_periods_individually(self):
        """Set open and due dates for periods individually

        Steps:
        Click on the Add Assignment drop down menu
        Click on the Add External Assignemnt option
        Enter an assignemnt name into the Assignemnt Name text box
        Click on the Individual periods radio button
        For each period:
        -Enter date into the Open Date text feild as MM/DD/YYYY
        -Enter date into the Due Date text feild as MM/DD/YYYY
        Enter a URL into the Assignment URL text box
        Click on the Publish button

        Expected Result:
        New external assignment appears on the calendar dashboard across its due dates
        """
        self.ps.test_updates['name'] = 't1.18.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.004', '8088']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8089 - 005 - Teacher | Save a draft external assignemnt
    @pytest.mark.skipif(str(8089) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_save_a_draft_external_assignment(self):
        """ Save a draft external assignemnt

        Steps:
        Click on the Add Assignment drop down menu
        Click on the Add External Assignemnt option
        Enter an assignemnt name into the Assignemnt Name text box
        Enter date into the Due Date text feild as MM/DD/YYYY
        Enter a URL into the Assignment URL text box
        Click on the Save As Draft button

        Expected Result:
        Draft external assignment appears on the calendar dashboard on its due date
        """
        self.ps.test_updates['name'] = 't1.18.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.005', '8089']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8090 - 006 - Teacher | Publish a new external assignemnt
    @pytest.mark.skipif(str(8090) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_publish_a_new_external_assignment(self):
        """ Publish a new external assignemnt

        Steps:
        Click on the Add Assignment drop down menu
        Click on the Add External Assignemnt option
        Enter an assignemnt name into the Assignemnt Name text box
        Enter date into the Due Date text feild as MM/DD/YYYY
        Enter a URL into the Assignment URL text box
        Click on the Publish button

        Expected Result:
        New external assignment appears on the calendar dashboard on its due date
        """
        self.ps.test_updates['name'] = 't1.18.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.006', '8090']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8091 - 007 - Teacher | Publish a draft external assignemnt
    @pytest.mark.skipif(str(8089) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_publish_a_draft_external_assignment(self):
        """ Publish a draft external assignemnt

        Steps:
        Click on the Add Assignment drop down menu
        Click on the Add External Assignemnt option
        Enter an assignemnt name into the Assignemnt Name text box
        Enter date into the Due Date text feild as MM/DD/YYYY
        Enter a URL into the Assignment URL text box
        Click on the Save As Draft button
        Click on the draft on the calendar dashboard
        Chick on the Publish button

        Expected Result:
        Draft external assignment appears on the calendar dashboard on its due date
        """
        self.ps.test_updates['name'] = 't1.18.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.007', '8091']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8092 - 008 - Teacher | Cancel a new external assignemnt before changes using Cancel button
    @pytest.mark.skipif(str(8092 not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_cancel_a_new_external_assignemnt_before_changes_using_cancel_button(self):
        """ Cancel a new external assignemnt before changes using Cancel button

        Steps:
        Click on the Add Assignment drop down menu
        Click on the Add External Assignemnt option
        Click on the Cancel button

        Expected Result:
        No changes to calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.18.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.008', '8092']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8093 - 009 - Teacher | Cancel a new external assignemnt after changes using Cancel button
    @pytest.mark.skipif(str(8093 not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_cancel_a_new_external_assignemnt_after_changes_using_cancel_button(self):
        """ Cancel a new external assignemnt after changes using Cancel button

        Steps:
        Click on the Add Assignment drop down menu
        Click on the Add External Assignemnt option
        Enter an assignemnt name into the Assignemnt Name text box
        Click on the Cancel button
        Click on the OK button

        Expected Result:
        No changes to calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.18.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.009', '8093']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8094 - 010 - Teacher | Cancel a new external assignemnt before changes using the X
    @pytest.mark.skipif(str(8094 not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_cancel_a_new_external_assignemnt_before_changes_using_the_x(self):
        """ Cancel a new external assignemnt before changes using the X

        Steps:
        Click on the Add Assignment drop down menu
        Click on the Add External Assignemnt option
        Click on the X

        Expected Result:
        No changes to calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.18.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.010', '8094']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8095 - 011 - Teacher | Cancel a new external assignemnt after changes using the X
    @pytest.mark.skipif(str(8095 not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_cancel_a_new_external_assignemnt_after_changes_using_the_x(self):
        """ Cancel a new external assignemnt after changes using the X

        Steps:
        Click on the Add Assignment drop down menu
        Click on the Add External Assignemnt option
        Enter an assignemnt name into the Assignemnt Name text box
        Click on the X
        Click on the OK button

        Expected Result:
        No changes to calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.18.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.011', '8095']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8096 - 012 - Teacher | Cancel a draft external assignemnt before changes using Cancel button
    @pytest.mark.skipif(str(8096 not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_cancel_a_draft_external_assignemnt_before_changes_using_cancel_button(self):
        """ Cancel a draft external assignemnt before changes using Cancel button

        Steps:
        ####create a draft external assignemnt---helper function
        Click on the draft external assignment
        Click on the Cancel button
        Click on the OK button

        Expected Result:
        No changes to calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.18.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.012', '8096']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8097 - 013 - Teacher | Cancel a draft external assignemnt after changes using Cancel button
    @pytest.mark.skipif(str(8097 not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_cancel_a_draft_external_assignemnt_after_changes_using_cancel_button(self):
        """ Cancel a draft external assignemnt after changes using Cancel button

        Steps:
        ####create a draft external assignemnt---helper function
        Click on the draft external assignment
        Enter an assignemnt name into the Assignment Name text box
        Click on the Cancel button
        Click on the OK button

        Expected Result:
        No changes to calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.18.013' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.013', '8097']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8098 - 014 - Teacher | Cancel a draft external assignemnt before changes using the X
    @pytest.mark.skipif(str(8098 not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_cancel_a_draft_external_assignemnt_before_changes_using_the_x(self):
        """ Cancel a draft external assignemnt before changes using the X

        Steps:
        ####create a draft external assignemnt---helper function
        Click on the draft external assignment
        Click on the X button
        Click on the OK button

        Expected Result:
        No changes to calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.18.014' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.014', '8098']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8099 - 015 - Teacher | Cancel a draft external assignemnt after changes using the X
    @pytest.mark.skipif(str(8099 not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_cancel_a_draft_external_assignemnt_after_changes_using_the_x(self):
        """ Cancel a draft external assignemnt after changes using the X

        Steps:
        ####create a draft external assignemnt---helper function
        Click on the draft external assignment
        Enter an assignemnt name into the Assignment Name text box
        Click on the Cancel button
        Click on the OK button

        Expected Result:
        No changes to calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.18.015' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.015', '8099']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8100 - 016 - Teacher | Attempt to publish an external assignment with blank required feilds
    @pytest.mark.skipif(str(8100 not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_attempt_to_publish_an_external_assignemnt_with_blank_reqired_feilds(self):
        """ Attempt to publish an external assignment with blank required feilds

        Steps:
        Click on the Add Assignment drop down menu
        Click on the Add External Assignemnt option
        Click on the Publish button

        Expected Result:
        Blank required feilds are highlighted in red, assignemnt is not published
        """
        self.ps.test_updates['name'] = 't1.18.016' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.016', '8100']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8101 - 017 - Teacher | Attempt to save a draft external assignment with blank required feilds
    @pytest.mark.skipif(str(8101 not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_attempt_to_save_a_draft_external_assignemnt_with_blank_reqired_feilds(self):
        """ Attempt to save a draft external assignment with blank required feilds

        Steps:
        Click on the Add Assignment drop down menu
        Click on the Add External Assignemnt option
        Click on the Save As Draft button

        Expected Result:
        Blank required feilds are highlighted in red, assignemnt is not saved
        """
        self.ps.test_updates['name'] = 't1.18.017' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.017', '8101']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8102 - 018 - Teacher | Delete an unopened external assignment
    @pytest.mark.skipif(str(8102 not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_delete_an_unopened_external_assignment(self):
        """ Delete an unopened external assignemnt

        Steps:
        ####Create an unopened assignemnt -- helper function
        Click on the unopened external assignment
        Click on the Edit Assignemnt button
        Click on the Delete Assignemnt
        Click on OK on the dialouge box

        Expected Result:
        Assignment has been removed from the calendar view
        """
        self.ps.test_updates['name'] = 't1.18.018' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.018', '8102']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8103 - 019 - Teacher | Attempt to delete an opened external assignment
    @pytest.mark.skipif(str(8103 not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_attempt_to_delete_an_opened_external_assignment(self):
        """ Attempt to delete an opened external assignemnt

        Steps:
        ####Create an opened assignemnt -- helper function
        Click on the opened external assignment
        Click on the Edit Assignemnt button

        Expected Result:
        No Delete Assignment button is found
        """
        self.ps.test_updates['name'] = 't1.18.019' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.019', '8103']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8104 - 020 - Teacher | Delete a draft external assignment
    @pytest.mark.skipif(str(8104 not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_delete_a_draft_external_assignment(self):
        """ Delete a draft external assignemnt

        Steps:
        ####Create a draft assignemnt -- helper function
        Click on the draft
        Click on the Delete Assignment buttom
        Click OK in the dialouge box

        Expected Result:
        Draft assignment is removed from calendar dasboard
        """
        self.ps.test_updates['name'] = 't1.18.020' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.020', '8104']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8105 - 021 - Teacher | Add a description to an external assignment
    @pytest.mark.skipif(str(8105 not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_add_a_destcription_to_an_external_assignemnt(self):
        """ Add a description to an external assignemnt

        Steps:
        Click on the Add Assignment drop down menu
        Click on the Add External Assignemnt option
        Enter an assignemnt name into the Assignemnt Name text box
        Enter a description into the Description or special instructions text box
        Enter date into the Due Dte text feild as MM/DD/YYYY
        Enter a URL into the Assignment URL text box
        Click on the Publish button

        Expected Result:
        Assignemnt is on calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.18.021' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.021', '8105']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8106 - 022 - Teacher | Change a description for a draft external assignment
    @pytest.mark.skipif(str(8106 not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_change_a_destcription_for_a_draft_external_assignemnt(self):
        """ Change a description for a draft external assignment

        Steps:
        #####create a draft assignemnt -- helper function
        Click on the draft assignment
        Enter a new description into the Description or special instructions text box
        Click on the Save as Draft button

        Expected Result:
        Assignemnt has been updated on the calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.18.022' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.022', '8106']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8107 - 023 - Teacher | Change a description for an open external assignment
    @pytest.mark.skipif(str(8107 not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_change_a_destcription_for_an_open_external_assignemnt(self):
        """ Change a description for an open external assignment

        Steps:
        #####create an open assignemnt -- helper function
        Click on the open assignment
        Click on the Edit Assignment button
        Enter a new description into the Description or special instructions text box
        Click on the Publish button

        Expected Result:
        Assignemnt has been updated on the calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.18.023' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.023', '8107']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8108 - 024 - Teacher | Add a name to an external assignment
    @pytest.mark.skipif(str(8108 not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_add_a_name_to_an_external_assignemnt(self):
        """ Add a name to an external assignment

        Steps:
        Click on the Add Assignment drop down menu
        Click on the Add External Assignemnt option
        Enter an assignemnt name into the Assignemnt Name text box
        Enter date into the Due Date text feild as MM/DD/YYYY
        Enter a URL into the Assignment URL text box
        Click on the Publish button

        Expected Result:
        New external assignment appears on the calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.18.024' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.024', '8108']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8109 - 025 - Teacher | Change a name for a draft external assignment
    @pytest.mark.skipif(str(8109 not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_change_a_name_for_a_draft_external_assignemnt(self):
        """ Change a name for a draft external assignment

        Steps:
        ###create a draft --helper
        Click on the draft assignment
        Enter a new assignment name into the assignment name text box
        Click on the Save As Draft button

        Expected Result:
        Draft external assignment appears on the calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.18.025' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.025', '8109']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8110 - 026 - Teacher | Change a name for an open external assignment
    @pytest.mark.skipif(str(8110 not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_change_a_name_for_an_open_external_assignemnt(self):
        """ Change a name for an open external assignment

        Steps:
        ###create an open assignment  --helper
        Click on the open assignment on the calendar
        Enter a new assignment name into the assignment name text box
        Click on the Publish button

        Expected Result:
        External assignment appears on the calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.18.026' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.026', '8110']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8111 - 027 - Teacher | Add an assignemnt URL
    @pytest.mark.skipif(str(8112 not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_add_an_assignment_url(self):
        """ Add an assignment URL

        Steps:
        Click on the Add Assignment drop down menu
        Click on the Add External Assignemnt option
        Enter an assignemnt name into the Assignemnt Name text box
        Enter date into the Due Date text feild as MM/DD/YYYY
        Enter a URL into the Assignment URL text box
        Click on the Publish button

        Expected Result:
        External assignment appears on the calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.18.027' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.027', '8111']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8112 - 028 - Teacher | Change the assignemnt URL for a draft external assignemnt
    @pytest.mark.skipif(str(8112 not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_change_the_assignment_url_for_a_draft_external_assignment(self):
        """ Change the assignemnt URL for a draft external assignemnt

        Steps:
        ##create a draft assignemnt -- helper function
        Click on the draft assignment
        Enter a new URL into the Assignemtn URL text box
        Click on the Save As Draft button

        Expected Result:
        Updated external assignment appears on the calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.18.028' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.028', '8112']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8113 - 029 - Teacher | Info icon shows definitions for the status bar
    @pytest.mark.skipif(str(8113 not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_info_icon_shows_definitions_for_the_status_bar(self):
        """ Info icon shows definitions for the status bar

        Steps:
        Click on the Add Assignment drop down menu
        Click on the Add External Assignemnt option
        Click on the info icon

        Expected Result:
        Definitions of the statuses are dispalayed
        """
        self.ps.test_updates['name'] = 't1.18.029' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.029', '8113']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8114 - 030 - Teacher | Change all feilds in an unopened External Assignemnt
    @pytest.mark.skipif(str(8114 not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_change_all_feilds_in_an_unopened_external_assignment(self):
        """ Change all feilds in an unopened External Assignemnt

        Steps:
        #####create an unopened assignement -- helper
        Click on the unopoened assignemnt on the calendar
        Enter an assignemnt name into the Assignemnt Name text box
        Enter a description into the Description or special instructions text box
        Enter date into the Open Date text feild as MM/DD/YYYY
        Enter date into the Due Date text feild as MM/DD/YYYY
        Enter a URL into the Assignment URL text box
        Click on the Publish button

        Expected Result:
        Updated assignment is displayed on the calendar
        """
        self.ps.test_updates['name'] = 't1.18.030' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.030', '8114']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8115 - 031 - Teacher | Change all feilds in a draft External Assignemnt
    @pytest.mark.skipif(str(8115 not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_change_all_feilds_in_a_draft_external_assignment(self):
        """ Change all feilds in a draft External Assignemnt

        Steps:
        #####create a draft assignement -- helper
        Click on the draft assignemnt on the calendar
        Enter an assignemnt name into the Assignemnt Name text box
        Enter a description into the Description or special instructions text box
        Enter date into the Open Date text feild as MM/DD/YYYY
        Enter date into the Due Date text feild as MM/DD/YYYY
        Enter a URL into the Assignment URL text box
        Click on the Save As Draft button

        Expected Result:
        Updated assignment is displayed on the calendar
        """
        self.ps.test_updates['name'] = 't1.18.031' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.031', '8115']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8116 - 032 - Teacher | Change all possible feilds in an open External Assignemnt
    @pytest.mark.skipif(str(8116 not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_change_all_possible_feilds_in_an_open_external_assignment(self):
        """ Change all possible feilds in an open External Assignemnt

        Steps:
        #####create an open assignement -- helper
        Click on the open assignemnt on the calendar
        Enter an assignemnt name into the Assignemnt Name text box
        Enter a description into the Description or special instructions text box
        Enter date into the Due Date text feild as MM/DD/YYYY
        Click on the Save As Draft button

        Expected Result:
        Updated assignment is displayed on the calendar
        """
        self.ps.test_updates['name'] = 't1.18.032' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.18', 't1.18.032', '8116']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True
