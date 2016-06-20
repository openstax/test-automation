"""Tutor v1, Epic 14 - Create a Reading."""

import inspect
import json
import os
import pytest
import unittest
import datetime

from pastasauce import PastaSauce, PastaDecorator
from random import randint  # NOQA
from selenium.webdriver.common.by import By  # NOQA
from selenium.webdriver.support import expected_conditions as expect  # NOQA
from staxing.assignment import Assignment  # NOQA
from selenium.webdriver.support.ui import WebDriverWait

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
    str([7992, 7993, 7994, 7995, 
    	 7996, 7997, 7998, 7999, 
    	 8000, 8001, 8002, 8003, 
    	 8004, 8005, 8006, 8007, 
    	 8008, 8009, 8010, 8011, 
         8012, 8013, 8014, 8015, 
         8016, 8017, 8018, 8019, 
         8020, 8021, 8022, 8023, 
         8024, 8025, 8026, 8027])  # NOQA
)


@PastaDecorator.on_platforms(BROWSERS)
class TestEpicName(unittest.TestCase):
    """T1.14 - Create a Reading."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.teacher = Teacher(
            use_env_vars=True#,
            #pasta_user=self.ps,
            #capabilities=self.desired_capabilities
        )
        self.teacher.login()
        self.teacher.select_course(appearance='physics')

    def tearDown(self):
        """Test destructor."""
        self.ps.update_job(job_id=str(self.teacher.driver.session_id),
                           **self.ps.test_updates)
        try:
            self.teacher.delete()
        except:
            pass

    # Case C7992 - 001 - Teacher | Add a reading using the Add Assignment drop down menu
    @pytest.mark.skipif(str(7992) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_add_a_reading_using_the_add_assignemnt_drop_down_menu(self):
        """Add a reading using the Add Assignment drop down menu.

        Steps: 
        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Reading' option
        Enter an assignment name into the Assignment name text box
        Enter into Due Date text field date as MM/DD/YYYY
        Click on the "+ Add Readings" button
        Click on section(s) to add to assignment [user decision]
        scroll to bottom
        Click on the "Add Readings" button
        Click on the Publish' button

        Expected Result:
        Takes user back to calendar dashboard. 
        Assignment appears on user calendar dashboard on due date with correct readings.
        """
        self.ps.test_updates['name'] = 't1.14.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.14','t1.14.001','7992']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        today = datetime.date.today()
        assignment_menu = self.teacher.driver.find_element(
            By.XPATH, '//button[contains(@class,"dropdown-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.find_element(By.XPATH, '..').get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Reading').click()
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.driver.find_element(By.ID, 'reading-title').send_keys('reading-001')
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]//textarea' +
            '[contains(@class,"form-control")]'). \
            send_keys('description')
        #does this need to be done manually, or is it okay to use helper

        end = (today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
        #close_xpath = '//div[contains(@class,"-assignment-due-date")]'\
        #              '//div[contains(@class,"datepicker__input")]//input[@type="text"]'
        close_xpath = '//*[@id="react-root-container"]/div/div/div/div/div[2]/div/div[1]/div[5]/div[2]/div[2]/div/div[1]/div/div[3]/div/input'
        self.teacher.driver.find_element(By.XPATH, close_xpath).clear()
        self.teacher.driver.find_element(By.XPATH, close_xpath).send_keys(end)

        # add reading sections to the assignment
        self.teacher.driver.find_element(By.ID, 'reading-select').click()
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"sections-chooser")]'\
                 '//input[contains(@type,"checkbox")]')
            )
        ).click()
        add_readings = self.teacher.driver.find_element(By.XPATH,
                            '//button[text()="Add Readings"]')
        self.student.driver.execute_script('return arguments[0].scrollIntoView();',add_readings)
        self.student.driver.execute_script('window.scrollBy(0, -80);')
        add_readings.click()
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[text()="Publish"]')
            )
        )
        self.teacher.driver.find_element(
                By.XPATH, '//button[contains(@class,"-publish")]').click()
        self.teacher.driver.find_elements_by_xpath("//*[contains(text(), 'reading-001')]")

        self.ps.test_updates['passed'] = True


    # # Case C7993 - 002 - Teacher | Add a reading using the calendar date
    # @pytest.mark.skipif(str(7993) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Add a reading using the calendar date.

    #     Steps: 

    #     Click on calendar date for desired due date
    #     Click on the 'Add Reading' option

    #     Enter an assignment name into the Assignment name text box [user decision]
    #     [optional] Enter an assignment description into the Assignment description or special instructions text box
    #     [optional] Enter into Open Date text field date as MM/DD/YYYY
    #     Click on the "+ Add Readings" button
    #     Click on section(s) to add to assignment [user decision]
    #     scroll to bottom
    #     Click on the "Add Readings" button
    #     Click on the "Publish" button

    #     Expected Result:

    #     Takes user back to calendar dashboard. 
    #     Assignment appears on user calendar dashboard on due date with correct readings.

    #     """
    #     self.ps.test_updates['name'] = 't1.14.002' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.14',
    #         't1.14.002',
    #         '7993'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C7994 - 003 - Teacher | Set open and due dates for all periods collectively
    # @pytest.mark.skipif(str(7994) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Set open and due dates for all periods collectively.

    #     Steps: 

    #     Click on the 'Add Assignment' drop down menu
    #     Click on the 'Add Reading' option

    #     Enter an assignment name into the Assignment name text box [user decision]
    #     [optional] Enter an assignment description into the Assignment description or special instructions text box
    #     ['All Periods' should be selected by default]
    #     Enter into Open Date text field date as MM/DD/YYYY 
    #     OR 
    #     click on calendar icon next to text field and click on desired open date

    #     Enter into Due Date text field date as MM/DD/YYYY 
    #     OR 
    #     click on calendar icon next to text field and click on desired due date

    #     Click on the "+ Add Readings" button
    #     Click on section(s) to add to assignment [user decision]
    #     scroll to bottom
    #     Click on the "Add Readings" button
    #     Click on the "Publish" button


    #     Expected Result:

    #     Takes user back to calendar dashboard. 
    #     Assignment appears on user calendar dashboard on due date with correct readings.

    #     """
    #     self.ps.test_updates['name'] = 't1.14.003' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.14',
    #         't1.14.003',
    #         '7994'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C7995 - 004 - Teacher | Set open and due dates for periods individually
    # @pytest.mark.skipif(str(7995) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Set open and due dates for periods individually.

    #     Steps: 

    #     Click on the 'Add Assignment' drop down menu
    #     Click on the 'Add Reading' option

    #     Enter an assignment name into the Assignment name text box [user decision]
    #     [optional] Enter an assignment description into the Assignment description or special instructions text box
    #     Select 'Individual Periods' radio button
    #     [optional] For each period that the user doesn't want the reading assigned to, 
    #     click the check box next to the period to unselect it

    #     For each period reading is being assigned to:
    #     - [optional] Enter into Open Date text field date as MM/DD/YYYY 
    #     OR 
    #     click on calendar icon next to text field and click on desired open date
    #     - Enter into Due Date text field date as MM/DD/YYYY 
    #     OR 
    #     click on calendar icon next to text field and click on desired due date

    #     Click on the "+ Add Readings" button
    #     Click on section(s) to add to assignment [user decision]
    #     Scroll to bottom
    #     Click on the "Add Readings" button
    #     Click "Publish"


    #     Expected Result:

    #     Takes user back to calendar dashboard. 
    #     Assignment appears on user calendar dashboard on due date with correct readings.

    #     """
    #     self.ps.test_updates['name'] = 't1.14.004' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.14',
    #         't1.14.004',
    #         '7995'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C7996 - 005 - Teacher | Save a draft reading
    # @pytest.mark.skipif(str(7996) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Save a draft reading.

    #     Steps: 

    #     Click on the 'Add Assignment' drop down menu
    #     Click on the 'Add Reading' option

    #     Enter an assignment name into the Assignment name text box [user decision]
    #     [optional] Enter an assignment description into the Assignment description or special instructions text box
    #     [optional] Enter into Open Date text field date as MM/DD/YYYY 
    #     OR 
    #     click on calendar icon next to text field and click on desired open date
        
    #     Enter into Due Date text field date as MM/DD/YYYY 
    #     OR 
    #     click on calendar icon next to text field and click on desired due date
        
    #     Click on the "+ Add Readings" button
    #     Click on section(s) to add to assignment [user decision]
    #     Scroll to bottom
    #     Click on the "Add Readings" button
    #     Click "Save As Draft"


    #     Expected Result:

    #     Takes user back to calendar dashboard. 
    #     Assignment appears on user calendar dashboard on due date with correct readings.
    #     'draft' should appear before the assignment name.

    #     """
    #     self.ps.test_updates['name'] = 't1.14.005' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.14',
    #         't1.14.005',
    #         '7996'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C7997 - 006 - Teacher | Publish a new reading
    # @pytest.mark.skipif(str(7997) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Publish a new reading.

    #     Steps: 

    #     Click on the 'Add Assignment' drop down menu
    #     Click on the 'Add Reading' option

    #     Enter an assignment name into the Assignment name text box [user decision]
    #     [optional] Enter an assignment description into the Assignment description or special instructions text box
    #     [optional] Enter into Open Date text field date as MM/DD/YYYY
    #     Enter into Due Date text field date as MM/DD/YYYY
    #     Click on the "+ Add Readings" button
    #     Click on section(s) to add to assignment [user decision]
    #     Scroll to bottom
    #     Click on the "Add Readings" button
    #     Click "Publish"


    #     Expected Result:

    #     Takes user back to calendar dashboard. 
    #     Assignment appears on user calendar dashboard on due date with correct readings.

    #     """
    #     self.ps.test_updates['name'] = 't1.14.006' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.14',
    #         't1.14.006',
    #         '7997'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C7998 - 007 - Teacher | Publish a draft reading
    # @pytest.mark.skipif(str(7998) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Publish a draft reading.

    #     Steps: 

    #     On the calendar click on a reading assignment that is currently a draft
    #     Click on the 'Publish' button
        

    #     Expected Result:

    #     Takes user back to calendar dashboard. 
    #     Assignment appears on user calendar dashboard on due date with correct readings.
    #     (draft should no longer be before the assignment name)

    #     """
    #     self.ps.test_updates['name'] = 't1.14.007' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.14',
    #         't1.14.007',
    #         '7998'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C7999 - 008 - Teacher | Cancel a new reading before making any changes using the Cancel button
    # @pytest.mark.skipif(str(7998) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Cancel a new reading before making any changes using the Cancel button.

    #     Steps: 

    #     Click on the 'Add Assignment' drop down menu
    #     Click on the 'Add Reading' option

    #     Click on the 'Cancel' button
        

    #     Expected Result:

    #     Takes user back to calendar dashboard. 
    #     No changes have been made on the calendar dashboard. 

    #     """
    #     self.ps.test_updates['name'] = 't1.14.008' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.14',
    #         't1.14.008',
    #         '7999'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C8000 - 009 - Teacher | Cancel a new reading after making changes using the Cancel button
    # @pytest.mark.skipif(str(8000) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Cancel a new reading after making changes using the Cancel button.

    #     Steps: 

    #     Click on the 'Add Assignment' drop down menu
    #     Click on the 'Add Reading' option

    #     Do at least one of the following:
    #     - Enter an assignment name into the Assignment name text box [user decision]
    #     - Enter an assignment description into the Assignment description or special instructions text box
    #     - Enter into Open Date text field date as MM/DD/YYYY
    #     - Enter into Due Date text field date as MM/DD/YYYY
    #     - Click on the "+ Add Readings" button
    #     --- Click on section(s) to add to assignment [user decision]
    #     --- scroll to bottom
    #     --- Click on the "Add Readings" button

    #     Click the 'Cancel' button
    #     Click on the "ok" button


    #     Expected Result:

    #     Takes user back to calendar dashboard. 
    #     No changes have been made to the calendar dashboard. 

    #     """
    #     self.ps.test_updates['name'] = 't1.14.009' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.14',
    #         't1.14.009',
    #         '8000'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C8001 - 010 - Teacher | Cancel a new reading before making any changes using the X
    # @pytest.mark.skipif(str(8001) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Cancel a new reading before making any changes using the X.

    #     Steps: 

    #     Click on the 'Add Assignment' drop down menu
    #     Click on the 'Add Reading' option

    #     Click on the 'X' button


    #     Expected Result:

    #     Takes user back to calendar dashboard. 
    #     No changes have been made to the calendar dashboard. 

    #     """
    #     self.ps.test_updates['name'] = 't1.14.010' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.14',
    #         't1.14.010',
    #         '8001'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C8002 - 011 - Teacher | Cancel a new reading after making changes using the X
    # @pytest.mark.skipif(str(8002) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Cancel a new reading after making changes using the X.

    #     Steps: 

    #     Click on the 'Add Assignment' drop down menu
    #     Click on the 'Add Reading' option

    #     Do at least one of the following:
    #     - Enter an assignment name into the Assignment name text box [user decision]
    #     - Enter an assignment description into the Assignment description or special instructions text box
    #     - Enter into Open Date text field date as MM/DD/YYYY
    #     - Enter into Due Date text field date as MM/DD/YYYY
    #     - Click on the "+ Add Readings" button
    #     --- Click on section(s) to add to assignment [user decision]
    #     --- Scroll to bottom
    #     --- Click on the "Add Readings" button

    #     Click the 'X' button
    #     Click the "ok" button

    #     Expected Result:

    #     Takes user back to calendar dashboard. 
    #     No changes have been made to the calendar dashboard. 

    #     """
    #     self.ps.test_updates['name'] = 't1.14.011' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.14',
    #         't1.14.011',
    #         '8002'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True= True


    # # Case C8003 - 012 - Teacher | Cancel a draft reading before making any changes using the Cancel button
    # @pytest.mark.skipif(str(8003) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Cancel a draft reading before making any changes using the Cancel button.

    #     Steps: 

    #     On the calendar click on a draft assignment
    #     Click on the 'Cancel' button
    #     Click on the 'ok' button


    #     Expected Result:

    #     Takes user back to calendar dashboard. 
    #     No changes have been made to the chosen draft on the calendar dashboard. 

    #     """
    #     self.ps.test_updates['name'] = 't1.14.012' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.14',
    #         't1.14.012',
    #         '8003'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C8004 - 013 - Teacher | Cancel a draft reading after making changes using the Cancel button
    # @pytest.mark.skipif(str(8004) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Cancel a draft reading after making changes using the Cancel button.

    #     Steps: 

    #     On the calendar click on a assignment that is currently a draft
    #     Do at least one of the following:
    #     - Enter an assignment name into the Assignment name text box [user decision]
    #     - Enter an assignment description into the Assignment description or special instructions text box
    #     - Enter into Open Date text field date as MM/DD/YYYY
    #     - Enter into Due Date text field date as MM/DD/YYYY
    #     - Click on the "+ Add Readings" button
    #     --- Click on section(s) to add to assignment [user decision]
    #     --- scroll to bottom
    #     --- Click on the "Add Readings" button

    #     Click on the 'Cancel' button
    #     Click on the 'ok' button


    #     Expected Result:

    #     Takes user back to calendar dashboard. 
    #     No changes have been made to the chosen draft on the calendar dashboard. 

    #     """
    #     self.ps.test_updates['name'] = 't1.14.013' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.14',
    #         't1.14.013',
    #         '8004'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C8005 - 014 - Teacher | Cancel a draft reading before making any changes using the X
    # @pytest.mark.skipif(str(8005) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Cancel a draft reading before making any changes using the X.

    #     Steps: 

    #     On the calendar click on a draft assignment 
    #     Click on the 'X' button
    #     Click on the 'ok' button


    #     Expected Result:

    #     Takes user back to calendar dashboard. 
    #     No changes have been made to the chosen draft on the calendar dashboard. 

    #     """
    #     self.ps.test_updates['name'] = 't1.14.014' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.14',
    #         't1.14.014',
    #         '8005'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C8006 - 015 - Teacher | Cancel a draft reading after making changes using the X
    # @pytest.mark.skipif(str(8006) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Cancel a draft reading after making changes using the X.

    #     Steps: 

    #     On the calendar click on a assignment that is currently a draft
    #     Do at least one of the following:
    #     - Enter an assignment name into the Assignment name text box [user decision]
    #     - Enter an assignment description into the Assignment description or special instructions text box
    #     - Enter into Open Date text field date as MM/DD/YYYY
    #     - Enter into Due Date text field date as MM/DD/YYYY
    #     - Click on the "+ Add Readings" button
    #     --- Click on section(s) to add to assignment [user decision]
    #     --- scroll to bottom
    #     --- Click on the "Add Readings" button

    #     Click on the 'X' button
    #     Click on the "ok" button

    #     Expected Result:

    #     Takes user back to calendar dashboard. 
    #     No changes have been made to the chosen draft on the calendar dashboard. 

    #     """
    #     self.ps.test_updates['name'] = 't1.14.015' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.14',
    #         't1.14.015',
    #         '8006'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C8007 - 016 - Teacher | Attempt to publish a reading with blank required fields
    # @pytest.mark.skipif(str(8007) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Attempt to publish a reading with blank required fields.

    #     Steps: 

    #     Click on the 'Add Assignment' drop down menu
    #     Click on the 'Add Reading' option
    #     Click on the 'Publish' button

    #     Expected Result:

    #     Remains on the Add Assignment page. 
    #     Does not allow user to publish assignments. 
    #     All required fields that were left blank become red, and specify that they are required fields.

    #     """
    #     self.ps.test_updates['name'] = 't1.14.016' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.14',
    #         't1.14.016',
    #         '8007'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C8008 - 017 - Teacher | Attempt to save a draft reading with blank required fields
    # @pytest.mark.skipif(str(8008) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Attempt to save a draft reading with blank required fields.

    #     Steps: 

    #     Click on the 'Add Assignment' drop down menu
    #     Click on the 'Add Reading' option
    #     Click on the 'Save As Draft' button

    #     Expected Result:

    #     Remains on the Add Assignment page. 
    #     Does not allow user to save assignments. 
    #     All required fields that were left blank become red, and specify that they are required fields

    #     """
    #     self.ps.test_updates['name'] = 't1.14.017' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.14',
    #         't1.14.017',
    #         '8008'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C8009 - 018 - Teacher | Delete an unopened reading
    # @pytest.mark.skipif(str(8009) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Delete an unopened reading.

    #     Steps: 

    #     On the calendar click on a reading that is unopened
    #     Click on the 'Edit Assignment' button
    #     Click on the 'Delete Assignment' button
    #     Click on the "ok" button
        
    #     Expected Result:

    #     Takes user back to calendar dashboard. 
    #     Chosen assignment no longer appears on teacher calendar dashboard.

    #     """
    #     self.ps.test_updates['name'] = 't1.14.018' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.14',
    #         't1.14.018',
    #         '8009'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C8010 - 019 - Teacher | Attempt to delete an open reading
    # @pytest.mark.skipif(str(8010) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Attempt to delete an open reading.

    #     Steps: 

    #     On the calendar click on an open reading
    #     Click on the 'View Assignment' button
        
    #     Expected Result:

    #     No "Delete Assignment" button found.

    #     """
    #     self.ps.test_updates['name'] = 't1.14.019' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.14',
    #         't1.14.019',
    #         '8010'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C8011 - 020 - Teacher | Delete a draft reading
    # @pytest.mark.skipif(str(8011) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Delete a draft reading.

    #     Steps: 

    #     On the calendar click on a draft
    #     Click on the 'Delete Assignment' button
    #     Click on the 'ok' button
        
    #     Expected Result:

    #     Takes user back to calendar dashboard. 
    #     Chosen assignment no longer appears on teacher calendar dashboard

    #     """
    #     self.ps.test_updates['name'] = 't1.14.020' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.14',
    #         't1.14.020',
    #         '8011'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C8012 - 021 - Teacher | Add a description to a reading 
    # @pytest.mark.skipif(str(8012) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Add a description to a reading.

    #     Steps: 

    #     Click on the 'Add Assignment' drop down menu
    #     Click on the 'Add Reading' option
    #     Enter an assignment name into the Assignment name text box
    #     Enter an assignment description into the Assignment description or special instructions text box
    #     Enter into Due Date text field date as MM/DD/YYYY
    #     Click on the 'Publish' button
        
    #     Expected Result:

    #     Takes user back to calendar dashboard. 
    #     Assignment with description should be on calendar on its due date.

    #     """
    #     self.ps.test_updates['name'] = 't1.14.021' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.14',
    #         't1.14.021',
    #         '8012'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C8013 - 022 - Teacher | Change a description for a draft reading
    # @pytest.mark.skipif(str(8013) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Change a description for a draft reading.

    #     Steps: 

    #     On the calendar click on a draft assignment 
    #     Enter a new assignment description into the Assignment description or special instructions text box
    #     CLick on the 'Save As Draft' button
        
    #     Expected Result:

    #     Takes user back to calendar dashboard. 
    #     Assignment description of the chosen draft should have the new description.

    #     """
    #     self.ps.test_updates['name'] = 't1.14.022' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.14',
    #         't1.14.022',
    #         '8013'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C8014 - 023 - Teacher | Change a description for an open reading
    # @pytest.mark.skipif(str(8014) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Change a description for an open reading.

    #     Steps: 

    #     On the calendar click on an open reading assignment 
    #     Click on the "Edit Assignment" button
    #     Enter a new assignment description into the Assignment description or special instructions text box
    #     Click on the 'Publish' button
        
    #     Expected Result:

    #     Takes user back to calendar dashboard. 
    #     Assignment description of the chosen reading should have the new description.

    #     """
    #     self.ps.test_updates['name'] = 't1.14.023' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.14',
    #         't1.14.023',
    #         '8014'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C8015 - 024 - Teacher | Add a name to a reading
    # @pytest.mark.skipif(str(8015) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Add a name to a reading.

    #     Steps: 

    #     Click on the 'Add Assignment' drop down menu
    #     Click on the 'Add Reading' option

    #     Enter an assignment name into the Assignment name text box [user decision]
    #     [optional] Enter an assignment description into the Assignment description or special instructions text box
    #     [optional] Enter into Open Date text field date as MM/DD/YYYY
    #     Enter into Due Date text field date as MM/DD/YYYY
    #     Click on the "+ Add Readings" button
    #     Click on section(s) to add to assignment [user decision]
    #     scroll to bottom
    #     Click on the "Add Readings" button
    #     Click on the Publish' button
        
    #     Expected Result:

    #     Takes user back to calendar dashboard. 
    #     Assignment appears on its due date with its given name.

    #     """
    #     self.ps.test_updates['name'] = 't1.14.024' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.14',
    #         't1.14.024',
    #         '8015'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C8016 - 025 - Teacher | Change a name for a draft reading
    # @pytest.mark.skipif(str(8016) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Change a name for a draft reading.

    #     Steps: 

    #     On the calendar click on a draft
    #     Enter a new name into the Assignment name text box
    #     Click on the 'Save As Draft' button
        
    #     Expected Result:

    #     Takes user back to calendar dashboard. 
    #     Assignment description of the chosen draft should have the new name.

    #     """
    #     self.ps.test_updates['name'] = 't1.14.025' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.14',
    #         't1.14.025',
    #         '8016'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C8017 - 026 - Teacher | Change a name for an open reading
    # @pytest.mark.skipif(str(8017) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Change a name for an open reading.

    #     Steps: 

    #     On the calendar click on an open reading assignment
    #     click on the "Edit Assignment" button
    #     Enter a new assignment name into the Assignment name text box
    #     Click on the 'Publish' button
        
    #     Expected Result:

    #     Takes user back to calendar dashboard, with chosen assignment open. 
    #     Assignment name of the chosen reading should have the new name.

    #     """
    #     self.ps.test_updates['name'] = 't1.14.026' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.14',
    #         't1.14.026',
    #         '8017'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C8018 - 027 - Teacher | Add a single section to a reading
    # @pytest.mark.skipif(str(8018) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Add a single section to a reading.

    #     Steps: 

    #     Click on the 'Add Assignment' drop down menu
    #     Click on the 'Add Reading' option
    #     Enter an assignment name into the Assignment name text box [user decision]
    #     Enter into Due Date text field date as MM/DD/YYYY
    #     Click on the '+ Add More Readings' button
    #     Click on a chapter heading (not the check box)
    #     Click on a single section within that chapter
    #     Scroll to the bottom
    #     Click on the "Add Readings" button
    #     Click on the 'Publish' button
        
    #     Expected Result:

    #     Takes user back to calendar dashboard, with chosen assignment open. 
    #     Reading assignment has been updated to have the new single section.

    #     """
    #     self.ps.test_updates['name'] = 't1.14.027' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.14',
    #         't1.14.027',
    #         '8018'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C8019 - 028 - Teacher | Add a complete chapter to a reading
    # @pytest.mark.skipif(str(8019) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Add a complete chapter to a reading.

    #     Steps: 

    #     On the calendar click on a closed reading
    #     	Click on the 'Edit Assignment' button
    #     	Click on the '+ Add More Readings' button
    #     	Click on the checkbox next to a chapter heading
    #     	Scroll to the bottom
    #     	Click on the "Add Readings" button
    #     	Click on the 'Publish' button
        
    #     Expected Result:

    #     Takes user back to the calendar dashboard, with the chosen question open. 
    #     Reading assignment has been updated to have the new chapter.

    #     """
    #     self.ps.test_updates['name'] = 't1.14.028' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.14',
    #         't1.14.028',
    #         '8019'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C8020 - 029 - Teacher | Remove a single section from a reading from the Select Readings screen
    # @pytest.mark.skipif(str(8020) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Remove a single section from a reading from the Select Readings screen.

    #     Steps: 

    #     On the calendar click on a closed reading
    #     	Click on the 'Edit Assignment' button
    #     	Click on the '+ Add More Readings" button
    #     	click on the check box next to a section that is currently added, but to be removed
    #     	Click on the 'Add Readings" button
    #     	Click on the "Publish" button
        
    #     Expected Result:

    #     Takes user back to the calendar dashboard. 
    #     Reading assignment has been updated to have the single section removed.

    #     """
    #     self.ps.test_updates['name'] = 't1.14.029' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.14',
    #         't1.14.029',
    #         '8020'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C8021 - 030 - Teacher | Remove a complete chapter from a reading from the Select Readings screen
    # @pytest.mark.skipif(str(8021) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Remove a complete chapter from a reading from the Select Readings screen.

    #     Steps: 

    #     On the calendar click on a closed reading
    #     	Click on the 'Edit Assignment' button
    #     	Click on the '+ Add More Readings' button
    #     	Click on the checkbox next to a chapter heading that is currently included, and to be removed
    #     	Scroll to the bottom
    #     	Click on the "Add Readings" button
    #     	Click on the "Publish" button
        
    #     Expected Result:

    #     Takes user back to the calendar dashboard. 
    #     Reading assignment has been updated to have the chapter removed.

    #     """
    #     self.ps.test_updates['name'] = 't1.14.030' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.14',
    #         't1.14.030',
    #         '8021'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C8022 - 031 - Teacher | Remove a single section from a reading from the Add Reading Assignment screen
    # @pytest.mark.skipif(str(8022) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Remove a single section from a reading from the Add Reading Assignment screen.

    #     Steps: 

    #     Click on the 'Add Assignment' drop down menu
    #     	Click on the 'Add Reading' option

    #     	Enter an assignment name into the Assignment name text box [user decision]
    #     	[optional] Enter an assignment description into the Assignment description or special instructions text box
    #     	[optional] Enter into Open Date text field date as MM/DD/YYYY
    #     	Enter into Due Date text field date as MM/DD/YYYY
    #     	Click on the "+ Add Readings" button
    #     	Click on sections to add to assignment [user decision]
    #     	scroll to bottom
    #     	Click on the "Add Readings" button

    #     	Click on the "x" button next to selected reading assignment to remove
    #     	Click on the Publish' button
        
    #     Expected Result:

    #     Takes user back to the calendar dashboard. 
    #     Reading assignment has been updated to have the single section removed.

    #     """
    #     self.ps.test_updates['name'] = 't1.14.031' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.14',
    #         't1.14.031',
    #         '8022'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C8023 - 032 - Teacher | Reorder the selected reading sections
    # @pytest.mark.skipif(str(8023) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Reorder the selected reading sections.

    #     Steps: 

    #     On the calendar click on a closed reading
    #     	Click on the 'Edit Assignment' button
    #     	Click on the up or down arrow buttons next to the selected readings
    #     	Click on the "Publish" button
        
    #     Expected Result:

    #     Takes user back to the calendar dashboard. 
    #     Reading assignment has been updated to have the readings in the new order

    #     """
    #     self.ps.test_updates['name'] = 't1.14.032' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.14',
    #         't1.14.032',
    #         '8023'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C8024 - 033 - Teacher | Change all fields in an unopened, published reading
    # @pytest.mark.skipif(str(8024) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Change all fields in an unopened, published reading.

    #     Steps: 

    #     Click on an existing reading on the calendar
    #     	Click on the 'Edit' option

    #     	Do all of the following:
    #     	- Enter a new assignment name into the Assignment name text box [user decision]
    #     	- Enter a new assignment description into the Assignment description or special instructions text box
    #     	- Enter into Open Date text field a new date as MM/DD/YYYY
    #     	- Enter into Due Date text field a new date as MM/DD/YYYY
    #     	- Click on the "+ Add Readings" button
    #     	--- Click on new section(s) to add to assignment [user decision]
    #     	--- scroll to bottom
    #     	--- Click on the "Add Readings" button

    #     	Click the 'Publish' button
        
    #     Expected Result:

    #     Takes user back to the calendar dashboard. 
    #     The name, description, due dates, and chapters/sections of the reading have been updated. 
    #     The reading now appears on its new due date on the calendar.

    #     """
    #     self.ps.test_updates['name'] = 't1.14.033' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.14',
    #         't1.14.033',
    #         '8024'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C8025 - 034 - Teacher | Change all fields in a draft reading
    # @pytest.mark.skipif(str(8025) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Change all fields in a draft reading.

    #     Steps: 

    #     Click on an existing draft reading on the calendar

    #     	Do all of the following:
    #     	- Enter a new assignment name into the Assignment name text box [user decision]
    #     	- Enter a new assignment description into the Assignment description or special instructions text box
    #     	- Enter into Open Date text field a new date as MM/DD/YYYY
    #     	- Enter into Due Date text field a new date as MM/DD/YYYY
    #     	- Click on the "+ Add Readings" button
    #     	--- Click on new section(s) to add to assignment [user decision]
    #     	--- scroll to bottom
    #     	--- Click on the "Add Readings" button

    #     	Click the 'Save As Draft' button
        
    #     Expected Result:

    #     Takes user back to the calendar dashboard. 
    #     The name, description, due dates, and chapters/sections of the reading have been updated. 
    #     The draft reading now appears on its new due date on the calendar.

    #     """
    #     self.ps.test_updates['name'] = 't1.14.034' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.14',
    #         't1.14.034',
    #         '8025'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C8026 - 035 - Teacher | Change the name, description and due dates in an opened reading
    # @pytest.mark.skipif(str(8026) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Change the name, description and due dates in an opened reading.

    #     Steps: 

    #     Click on an existing open reading on the calendar
    #     	Click on the 'Edit' option

    #     	Do all of the following:
    #     	- Enter a new assignment name into the Assignment name text box [user decision]
    #     	- Enter a new assignment description into the Assignment description or special instructions text box
    #     	- Enter into Due Date text field a new date as MM/DD/YYYY

    #     	Click the 'Publish' button
        
    #     Expected Result:

    #     Takes user back to the calendar dashboard. 
    #     The name, description, due dates, and chapters/sections of the reading have been updated. 
    #     The reading now appears on its new due date on the calendar

    #     """
    #     self.ps.test_updates['name'] = 't1.14.035' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.14',
    #         't1.14.035',
    #         '8026'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C8027 - 036 - Teacher | Info icon shows definitions for the Add Homework Assignment status bar buttons
    # @pytest.mark.skipif(str(8027) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Info icon shows definitions for the Add Homework Assignment status bar buttons.

    #     Steps: 

    #     Click on the 'Add Assignment' drop down menu
    #     	Click on the 'Add Reading' option
    #     	Click on the info icon
        
    #     Expected Result:

    #     Instructions about the Publish, Cancel, and Save As Draft statuses appear
        
    #     """
    #     self.ps.test_updates['name'] = 't1.14.036' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = [
    #         't1',
    #         't1.14',
    #         't1.14.036',
    #         '8027'
    #     ]
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True
