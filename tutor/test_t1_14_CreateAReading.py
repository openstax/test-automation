"""Tutor v1, Epic 14 - Create a Reading."""

import inspect
import json
import os
import pytest
import unittest
import datetime
import time

from pastasauce import PastaSauce, PastaDecorator
from random import randint  # NOQA
from selenium.webdriver.common.by import By  # NOQA
from selenium.webdriver.support import expected_conditions as expect  # NOQA
from staxing.assignment import Assignment  # NOQA
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

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
class TestCreateAReading(unittest.TestCase):
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

    # # Case C7992 - 001 - Teacher | Add a reading using the Add Assignment drop down menu
    # @pytest.mark.skipif(str(7992) not in TESTS, reason='Excluded')  # NOQA
    # def test_teacher_add_a_reading_using_the_add_assignemnt_drop_down_menu(self):
    #     """Add a reading using the Add Assignment drop down menu.

    #     Steps: 
    #     Click on the 'Add Assignment' drop down menu
    #     Click on the 'Add Reading' option
    #     Enter an assignment name into the Assignment name text box
    #     Enter into Due Date text field date as MM/DD/YYYY
    #     Click on the "+ Add Readings" button
    #     Click on section(s) to add to assignment [user decision]
    #     scroll to bottom
    #     Click on the "Add Readings" button
    #     Click on the Publish' button

    #     Expected Result:
    #     Takes user back to calendar dashboard. 
    #     Assignment appears on user calendar dashboard on due date with correct readings.
    #     """
    #     self.ps.test_updates['name'] = 't1.14.001' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = ['t1','t1.14','t1.14.001','7992']
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions
    #     assignment = Assignment()
    #     assignment_menu = self.teacher.driver.find_element(
    #         By.XPATH, '//button[contains(@class,"dropdown-toggle")]')
    #     # if the Add Assignment menu is not open
    #     if 'open' not in assignment_menu.find_element(By.XPATH, '..').get_attribute('class'):
    #         assignment_menu.click()
    #     self.teacher.driver.find_element(By.LINK_TEXT, 'Add Reading').click()
    #     wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
    #     wait.until(
    #         expect.element_to_be_clickable(
    #             (By.ID, 'reading-title')
    #         )
    #     )
    #     self.teacher.driver.find_element(By.ID, 'reading-title').send_keys('reading-001')
    #     self.teacher.driver.find_element(
    #         By.XPATH,
    #         '//div[contains(@class,"assignment-description")]//textarea' +
    #         '[contains(@class,"form-control")]'). \
    #         send_keys('description')
    #     # set date
    #     today = datetime.date.today()
    #     opens_on = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
    #     closes_on = (today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
    #     assignment.assign_periods(self.teacher.driver, {'all':(opens_on,closes_on)})
    #     # add reading sections to the assignment
    #     self.teacher.driver.find_element(By.ID, 'reading-select').click()
    #     wait.until(
    #         expect.visibility_of_element_located(
    #             (By.XPATH, '//div[contains(@class,"reading-plan")]')
    #         )
    #     )
    #     assignment.select_sections(self.teacher.driver, ['1.3'])
    #     #assignment.select_sections(self.teacher.driver, ['2.1','12.2','9.1'])
    #     self.teacher.driver.find_element(By.XPATH,
    #                         '//button[text()="Add Readings"]').click()
    #     wait.until(
    #         expect.visibility_of_element_located(
    #             (By.XPATH, '//span[text()="Publish"]')
    #         )
    #     )
    #     # publish
    #     wait.until(
    #         expect.visibility_of_element_located(
    #             (By.XPATH, '//span[text()="Publish"]')
    #         )
    #     )
    #     self.teacher.driver.find_element(
    #             By.XPATH, '//button[contains(@class,"-publish")]').click()
    #     self.teacher.driver.find_element_by_xpath("//label[contains(text(), 'reading-001')]")

    #     self.ps.test_updates['passed'] = True


    # NOT DONE
    # # Case C7993 - 002 - Teacher | Add a reading using the calendar date
    # @pytest.mark.skipif(str(7993) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Add a reading using the calendar date.

    #     Steps: 
    #     Click on calendar date for desired due date
    #     Click on the 'Add Reading' option
    #     Enter an assignment name into the Assignment name text box [user decision]
    #     Enter an assignment description into the Assignment description text box
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
    #     self.ps.test_updates['tags'] = ['t1','t1.14','t1.14.002','7993']
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions
    #     today = datetime.date.today()
    #     opens_on = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
    #     closes_on = (today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
    
    #     wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
    #     self.teacher.sleep(10)
    #     calendar_date = wait.until(
    #         expect.element_to_be_clickable(
    #             ( By.XPATH,'//div[contains(@class,"Day--upcoming")]')
    #         )
    #     )
        
    #     self.teacher.driver.execute_script('return arguments[0].scrollIntoView();', calendar_date)
    #     self.teacher.driver.execute_script('window.scrollBy(0, -80);')
    #     #self.teacher.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    #     actions = ActionChains(self.teacher.driver)
    #     actions.move_to_element(calendar_date)
    #     actions.click()
    #     actions.perform()
    #     #self.teacher.sleep(3)
    #     add_readings = wait.until(
    #         expect.element_to_be_clickable(
    #             ( By.XPATH,'//li[@data-assignment-type="reading"]')
    #         )
    #     )            
    #     actions.move_by_offset(15,15)
    #     actions.click()
    #     actions.perform()
    #     self.ps.test_updates['passed'] = True


    # # Case C7994 - 003 - Teacher | Set open and due dates for all periods collectively
    # @pytest.mark.skipif(str(7994) not in TESTS, reason='Excluded')  # NOQA
    # def test_teacher_set_open_and_due_dates_for_all_periods_collectively(self):
    #     """Set open and due dates for all periods collectively.

    #     Steps: 
    #     Click on the 'Add Assignment' drop down menu
    #     Click on the 'Add Reading' option
    #     Enter an assignment name into the Assignment name text box [user decision]
    #     Enter an assignment description into the Assignment description text box
    #     click on calendar icon next to text field and click on desired open date
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
    #     self.ps.test_updates['tags'] = ['t1','t1.14','t1.14.003','7994']
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions
    #     assignment_name = 'reading-003'
    #     assignment = Assignment()
    #     assignment_menu = self.teacher.driver.find_element(
    #         By.XPATH, '//button[contains(@class,"dropdown-toggle")]')
    #     # if the Add Assignment menu is not open
    #     if 'open' not in assignment_menu.find_element(By.XPATH, '..').get_attribute('class'):
    #         assignment_menu.click()
    #     self.teacher.driver.find_element(By.LINK_TEXT, 'Add Reading').click()
    #     wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
    #     wait.until(
    #         expect.element_to_be_clickable(
    #             (By.ID, 'reading-title')
    #         )
    #     )
    #     self.teacher.driver.find_element(By.ID, 'reading-title').send_keys(assignment_name)
    #     self.teacher.driver.find_element(
    #         By.XPATH,
    #         '//div[contains(@class,"assignment-description")]//textarea' +
    #         '[contains(@class,"form-control")]'). \
    #         send_keys('description')
    #     #set due dates
    #     self.teacher.driver.find_element(By.ID,"hide-periods-radio").click()
    #     today = datetime.date.today()
    #     opens_on = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
    #     closes_on = (today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
    #     self.teacher.driver.find_element(
    #         By.XPATH, '//div[contains(@class,"-due-date")]'\
    #         '//div[contains(@class,"datepicker__input")]').click()
    #     # get calendar to correct month
    #     month = today.month
    #     year = today.year
    #     while (month != int(closes_on[:2]) or year != int(closes_on[6:])):
    #         self.teacher.driver.find_element(
    #             By.XPATH, '//a[contains(@class,"navigation--next")]').click()
    #         if month != 12:
    #             month += 1
    #         else:
    #             month = 1
    #             year += 1
    #     self.teacher.driver.find_element(
    #         By.XPATH, '//div[contains(@class,"datepicker__day")'\
    #         'and contains(text(),"'+ (closes_on[3:5]) +'")]').click()
    #     time.sleep(0.5)
    #     self.teacher.driver.find_element(By.CLASS_NAME, 'assign-to-label').click()
    #     self.teacher.driver.find_element(
    #         By.XPATH, '//div[contains(@class,"-open-date")]'\
    #         '//div[contains(@class,"datepicker__input")]').click()
    #     # get calendar to correct month
    #     month = today.month
    #     year = today.year
    #     while (month != int(opens_on[:2]) or year != int(opens_on[6:])):
    #         self.teacher.driver.find_element(
    #             By.XPATH, '//a[contains(@class,"navigation--next")]').click()
    #         if month != 12:
    #             month += 1
    #         else:
    #             month = 1
    #             year += 1
    #     self.teacher.driver.find_element(
    #         By.XPATH, '//div[contains(@class,"datepicker__day")'\
    #         'and contains(text(),"'+ (opens_on[3:5]) +'")]').click()
    #     time.sleep(0.5)
    #     self.teacher.driver.find_element(By.CLASS_NAME, 'assign-to-label').click()

    #     # add reading sections to the assignment
    #     self.teacher.driver.find_element(By.ID, 'reading-select').click()
    #     wait.until(
    #         expect.visibility_of_element_located(
    #             (By.XPATH, '//div[contains(@class,"select-reading-' +
    #              'dialog")]')
    #         )
    #     )
    #     assignment.select_sections(self.teacher.driver, ['ch1'])
    #     self.teacher.driver.find_element(By.XPATH,
    #                         '//button[text()="Add Readings"]').click()
    #     wait.until(
    #         expect.visibility_of_element_located(
    #             (By.XPATH, '//span[text()="Publish"]')
    #         )
    #     )
    #     # publish
    #     wait.until(
    #         expect.visibility_of_element_located(
    #             (By.XPATH, '//span[text()="Publish"]')
    #         )
    #     )
    #     self.teacher.driver.find_element(
    #             By.XPATH, '//button[contains(@class,"-publish")]').click()
    #     self.teacher.driver.find_element_by_xpath(
    #         "//label[contains(text(), '"+assignment_name+"')]")
    #     self.ps.test_updates['passed'] = True


    # # Case C7995 - 004 - Teacher | Set open and due dates for periods individually
    # @pytest.mark.skipif(str(7995) not in TESTS, reason='Excluded')  # NOQA
    # def test_teacher_set_open_and_due_dates_for_periods_individually(self):
    #     """Set open and due dates for periods individually.

    #     Steps: 
    #     Click on the 'Add Assignment' drop down menu
    #     Click on the 'Add Reading' option
    #     Enter an assignment name into the Assignment name text box [user decision]
    #     Enter an assignment description into the Assignment description text box
    #     Select 'Individual Periods' radio button
    #     For each period reading is being assigned to:
    #     click on calendar icon next to text field and click on desired open date
    #     click on calendar icon next to text field and click on desired due date
    #     Click on the "+ Add Readings" button
    #     Click on section(s) to add to assignment
    #     Scroll to bottom
    #     Click on the "Add Readings" button
    #     Click "Publish"

    #     Expected Result:
    #     Takes user back to calendar dashboard. 
    #     Assignment appears on user calendar dashboard on due date with correct readings.
    #     """
    #     self.ps.test_updates['name'] = 't1.14.004' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = ['t1','t1.14','t1.14.004','7995']
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions
    #     assignment = Assignment()
    #     assignment_menu = self.teacher.driver.find_element(
    #         By.XPATH, '//button[contains(@class,"dropdown-toggle")]')
    #     # if the Add Assignment menu is not open
    #     if 'open' not in assignment_menu.find_element(By.XPATH, '..').get_attribute('class'):
    #         assignment_menu.click()
    #     self.teacher.driver.find_element(By.LINK_TEXT, 'Add Reading').click()
    #     wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
    #     wait.until(
    #         expect.element_to_be_clickable(
    #             (By.ID, 'reading-title')
    #         )
    #     )
    #     self.teacher.driver.find_element(By.ID, 'reading-title').send_keys('reading-001')
    #     self.teacher.driver.find_element(
    #         By.XPATH,
    #         '//div[contains(@class,"assignment-description")]//textarea' +
    #         '[contains(@class,"form-control")]'). \
    #         send_keys('description')
    #     # set date
    #     today = datetime.date.today()
    #     self.teacher.driver.find_element(By.ID, 'show-periods-radio').click()
    #     periods = self.teacher.driver.find_elements(
    #         By.XPATH,'//div[contains(@class,"tasking-plan")]')
    #     today = datetime.date.today()
    #     for x in range(len(periods)):
    #         opens_on = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
    #         closes_on = (today + datetime.timedelta(days=(2))).strftime('%m/%d/%Y')
    #         element = self.teacher.driver.find_element(
    #             By.XPATH, '//div[contains(@class,"tasking-plan")'\
    #             'and contains(@data-reactid,":'+str(x+1)+'")]'\
    #             '//div[contains(@class,"-due-date")]'\
    #             '//div[contains(@class,"datepicker__input")]')
    #         self.teacher.driver.execute_script(
    #             'window.scrollBy(0,'+str(element.size['height']+50)+');')
    #         time.sleep(0.5)
    #         element.click()
    #         # get calendar to correct month
    #         month = today.month
    #         year = today.year
    #         while (month != int(closes_on[:2]) or year != int(closes_on[6:])):
    #             self.teacher.driver.find_element(
    #                 By.XPATH, '//a[contains(@class,"navigation--next")]').click()
    #             if month != 12:
    #                 month += 1
    #             else:
    #                 month = 1
    #                 year += 1
    #         self.teacher.driver.find_element(
    #             By.XPATH, '//div[contains(@class,"datepicker__day")'\
    #             'and contains(text(),"'+ (closes_on[3:5]) +'")]').click()
    #         time.sleep(0.5)
    #         #self.teacher.driver.find_element(By.CLASS_NAME, 'assign-to-label').click()
    #         self.teacher.driver.find_element(
    #             By.XPATH, '//div[contains(@class,"tasking-plan") and'\
    #             ' contains(@data-reactid,":'+str(x+1)+'")]'\
    #             '//div[contains(@class,"-open-date")]'\
    #             '//div[contains(@class,"datepicker__input")]').click()
    #         # get calendar to correct month
    #         month = today.month
    #         year = today.year
    #         while (month != int(opens_on[:2]) or year != int(opens_on[6:])):
    #             self.teacher.driver.find_element(
    #                 By.XPATH, '//a[contains(@class,"navigation--next")]').click()
    #             if month != 12:
    #                 month += 1
    #             else:
    #                 month = 1
    #                 year += 1
    #         self.teacher.driver.find_element(
    #             By.XPATH, '//div[contains(@class,"datepicker__day")'\
    #             'and contains(text(),"'+ (opens_on[3:5]) +'")]').click()
    #         time.sleep(0.5)
    #     # add reading sections to the assignment
    #     self.teacher.driver.find_element(By.ID, 'reading-select').click()
    #     wait.until(
    #         expect.visibility_of_element_located(
    #             (By.XPATH, '//div[contains(@class,"reading-plan")]')
    #         )
    #     )
    #     assignment.select_sections(self.teacher.driver, ['1.3'])
    #     self.teacher.driver.find_element(By.XPATH,
    #                         '//button[text()="Add Readings"]').click()
    #     wait.until(
    #         expect.visibility_of_element_located(
    #             (By.XPATH, '//span[text()="Publish"]')
    #         )
    #     )
    #     # publish
    #     wait.until(
    #         expect.visibility_of_element_located(
    #             (By.XPATH, '//span[text()="Publish"]')
    #         )
    #     )
    #     self.teacher.driver.find_element(
    #             By.XPATH, '//button[contains(@class,"-publish")]').click()
    #     self.teacher.driver.find_elements_by_xpath("//*[contains(text(), 'reading-001')]")

    #     self.ps.test_updates['passed'] = True
    #     self.ps.test_updates['passed'] = True


    # # Case C7996 - 005 - Teacher | Save a draft reading
    # @pytest.mark.skipif(str(7996) not in TESTS, reason='Excluded')  # NOQA
    # def test_teacher_save_a_draft_reading(self):
    #     """Save a draft reading.

    #     Steps: 
    #     Click on the 'Add Assignment' drop down menu
    #     Click on the 'Add Reading' option
    #     Enter an assignment name into the Assignment name text box [user decision]
    #     Enter an assignment description into the Assignment description  text box
    #     click on calendar icon next to text field and click on desired open date
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
    #     self.ps.test_updates['tags'] = ['t1','t1.14','t1.14.005','7996']
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions
    #     assignment = Assignment()
    #     assignment_menu = self.teacher.driver.find_element(
    #         By.XPATH, '//button[contains(@class,"dropdown-toggle")]')
    #     # if the Add Assignment menu is not open
    #     if 'open' not in assignment_menu.find_element(By.XPATH, '..').get_attribute('class'):
    #         assignment_menu.click()
    #     self.teacher.driver.find_element(By.LINK_TEXT, 'Add Reading').click()
    #     wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
    #     wait.until(
    #         expect.element_to_be_clickable(
    #             (By.ID, 'reading-title')
    #         )
    #     )
    #     self.teacher.driver.find_element(By.ID, 'reading-title').send_keys('reading-001')
    #     self.teacher.driver.find_element(
    #         By.XPATH,
    #         '//div[contains(@class,"assignment-description")]//textarea' +
    #         '[contains(@class,"form-control")]'). \
    #         send_keys('description')
    #     # set date
    #     today = datetime.date.today()
    #     opens_on = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
    #     closes_on = (today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
    #     assignment.assign_periods(self.teacher.driver, {'all':(opens_on,closes_on)})
    #     # add reading sections to the assignment
    #     self.teacher.driver.find_element(By.ID, 'reading-select').click()
    #     wait.until(
    #         expect.visibility_of_element_located(
    #             (By.XPATH, '//div[contains(@class,"reading-plan")]')
    #         )
    #     )
    #     assignment.select_sections(self.teacher.driver, ['1.3'])
    #     self.teacher.driver.find_element(By.XPATH,
    #                         '//button[text()="Add Readings"]').click()
    #     wait.until(
    #         expect.visibility_of_element_located(
    #             (By.XPATH, '//span[text()="Publish"]')
    #         )
    #     )
    #     # publish
    #     wait.until(
    #         expect.visibility_of_element_located(
    #             (By.XPATH, '//span[text()="Publish"]')
    #         )
    #     )
    #     self.teacher.driver.find_element(
    #             By.XPATH, '//button[contains(@class,"-save")]').click()
    #     self.teacher.driver.find_element_by_xpath(
    #         "//label[contains(text(), 'reading-001')]")

    #     self.ps.test_updates['passed'] = True

    # # exact same steps as 001
    # # Case C7997 - 006 - Teacher | Publish a new reading
    # @pytest.mark.skipif(str(7997) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Publish a new reading.

    #     Steps: 
    #     Click on the 'Add Assignment' drop down menu
    #     Click on the 'Add Reading' option
    #     Enter an assignment name into the Assignment name text box [user decision]
    #     Enter an assignment description into the Assignment description text box
    #     Enter into Open Date text field date as MM/DD/YYYY
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
    #     self.ps.test_updates['tags'] = ['t1','t1.14','t1.14.006','7997']
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # # Case C7998 - 007 - Teacher | Publish a draft reading
    # @pytest.mark.skipif(str(7998) not in TESTS, reason='Excluded')  # NOQA
    # def test_teacher_publish_a_draft_reading(self):
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
    #     self.ps.test_updates['tags'] = ['t1','t1.14','t1.14.007','7998']
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions
    #     assignment_name = 'reading-007'
    #     today = datetime.date.today()
    #     begin = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
    #     end = (today + datetime.timedelta(days=2)).strftime('%m/%d/%Y')
    #     self.teacher.add_assignment( assignment='reading',
    #                                  args={
    #                                      'title' : assignment_name,
    #                                      'description' : 'description',
    #                                      'periods' : {'all': (begin, end)},
    #                                      'reading_list' : ['ch1'],
    #                                      'status' : 'draft'
    #                                  })
    #     self.teacher.driver.find_element(
    #         By.XPATH,'//label[@data-title="'+assignemnt_name+'"]').click()
    #     wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
    #     wait.until(
    #         expect.visibility_of_element_located(
    #             (By.XPATH, '//span[text()="Publish"]')
    #         )
    #     )
    #     self.teacher.driver.find_element(
    #             By.XPATH, '//button[contains(@class,"-publish")]').click()
    #     self.teacher.driver.find_element_by_xpath(
    #         "//label[contains(text(), 'reading-001')]")


    #     self.ps.test_updates['passed'] = True


    # # Case C7999 - 008 - Teacher | Cancel a new reading before making changes using the Cancel button
    # @pytest.mark.skipif(str(7998) not in TESTS, reason='Excluded')  # NOQA
    # def test_teacher_cancel_a_new_reading_before_making_changes_using_the_cancel_buttom(self):
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
    #     self.ps.test_updates['tags'] = ['t1','t1.14','t1.14.008','7999']
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions
    #     assignment_menu = self.teacher.driver.find_element(
    #         By.XPATH, '//button[contains(@class,"dropdown-toggle")]')
    #     # if the Add Assignment menu is not open
    #     if 'open' not in assignment_menu.find_element(By.XPATH, '..').get_attribute('class'):
    #         assignment_menu.click()
    #     self.teacher.driver.find_element(By.LINK_TEXT, 'Add Reading').click()
    #     wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
    #     wait.until(
    #         expect.element_to_be_clickable(
    #             (By.XPATH,'//button[@aria-role="close" and @type="button" and text()="Cancel"]')
    #         )
    #     ).click()
    #     assert ('calendar' in self.teacher.current_url()),\
    #         'not back at calendar after canceling reading'

    #     self.ps.test_updates['passed'] = True


    # # Case C8000 - 009 - Teacher | Cancel a new reading after making changes using the Cancel button
    # @pytest.mark.skipif(str(8000) not in TESTS, reason='Excluded')  # NOQA
    # def test_teacher_cancel_a_new_reading_after_making_changes_using_the_cancel_button(self):
    #     """Cancel a new reading after making changes using the Cancel button.

    #     Steps: 
    #     Click on the 'Add Assignment' drop down menu
    #     Click on the 'Add Reading' option
    #     Enter an assignment name into the Assignment name text box
    #     Click the 'Cancel' button
    #     Click on the "ok" button

    #     Expected Result:
    #     Takes user back to calendar dashboard. 
    #     No changes have been made to the calendar dashboard. 
    #     """
    #     self.ps.test_updates['name'] = 't1.14.009' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = ['t1','t1.14','t1.14.009','8000']
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions
    #     assignment_menu = self.teacher.driver.find_element(
    #         By.XPATH, '//button[contains(@class,"dropdown-toggle")]')
    #     # if the Add Assignment menu is not open
    #     if 'open' not in assignment_menu.find_element(By.XPATH, '..').get_attribute('class'):
    #         assignment_menu.click()
    #     self.teacher.driver.find_element(By.LINK_TEXT, 'Add Reading').click()
    #     wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
    #     wait.until(
    #         expect.element_to_be_clickable(
    #             (By.ID, 'reading-title')
    #         )
    #     )
    #     self.teacher.driver.find_element(By.ID, 'reading-title').send_keys('reading-009')
    #     self.teacher.driver.find_element(
    #         By.XPATH,'//button[@aria-role="close" and @type="button" and text()="Cancel"]').click()
    #     wait.until(
    #         expect.visibility_of_element_located(
    #             (By.XPATH, '//button[contains(@class,"ok")]')
    #         )
    #     ).click()
    #     assert ('calendar' in self.teacher.current_url()),\
    #         'not back at calendar after making changes, then canceling reading'

    #     self.ps.test_updates['passed'] = True


    # # Case C8001 - 010 - Teacher | Cancel a new reading before making changes using the X
    # @pytest.mark.skipif(str(8001) not in TESTS, reason='Excluded')  # NOQA
    # def test_teacher_cancel_a_new_reading_before_making_changes_using_the_x(self):
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
    #     self.ps.test_updates['tags'] = ['t1','t1.14','t1.14.010','8001']
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions
    #     assignment_menu = self.teacher.driver.find_element(
    #         By.XPATH, '//button[contains(@class,"dropdown-toggle")]')
    #     # if the Add Assignment menu is not open
    #     if 'open' not in assignment_menu.find_element(By.XPATH, '..').get_attribute('class'):
    #         assignment_menu.click()
    #     self.teacher.driver.find_element(By.LINK_TEXT, 'Add Reading').click()
    #     wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
    #     wait.until(
    #         expect.element_to_be_clickable(
    #             (By.XPATH,
    #              '//button[@aria-role="close" and contains(@class,"close-x")]')
    #         )
    #     ).click()
    #     assert ('calendar' in self.teacher.current_url()),\
    #         'not back at calendar after canceling reading with x'

    #     self.ps.test_updates['passed'] = True


    # # Case C8002 - 011 - Teacher | Cancel a new reading after making changes using the X
    # @pytest.mark.skipif(str(8002) not in TESTS, reason='Excluded')  # NOQA
    # def test_cancel_a_new_reading_after_making_changes_using_the_x(self):
    #     """Cancel a new reading after making changes using the X.

    #     Steps: 
    #     Click on the 'Add Assignment' drop down menu
    #     Click on the 'Add Reading' option
    #     Enter an assignment name into the Assignment name text box [user decision]
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
    #     assignment_menu = self.teacher.driver.find_element(
    #         By.XPATH, '//button[contains(@class,"dropdown-toggle")]')
    #     # if the Add Assignment menu is not open
    #     if 'open' not in assignment_menu.find_element(By.XPATH, '..').get_attribute('class'):
    #         assignment_menu.click()
    #     self.teacher.driver.find_element(By.LINK_TEXT, 'Add Reading').click()
    #     wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
    #     wait.until(
    #         expect.element_to_be_clickable(
    #             (By.ID, 'reading-title')
    #         )
    #     )
    #     self.teacher.driver.find_element(By.ID, 'reading-title').send_keys('reading-011')
    #     self.teacher.driver.find_element(
    #         By.XPATH,
    #         '//button[@aria-role="close" and contains(@class,"close-x")]').click()
    #     wait.until(
    #         expect.visibility_of_element_located(
    #             (By.XPATH, '//button[contains(@class,"ok")]')
    #         )
    #     ).click()
    #     assert ('calendar' in self.teacher.current_url()),\
    #         'not back at calendar after making changes, then canceling reading with x'

    #     self.ps.test_updates['passed'] = True


    # # Case C8003 - 012 - Teacher | Cancel a draft reading before making changes using the Cancel button
    # @pytest.mark.skipif(str(8003) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Cancel a draft reading before making any changes using the Cancel button.

    #     Steps: 
    #     On the calendar click on a draft assignment
    #     Click on the 'Cancel' button

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
    #     assignment_name = 'reading-007'
    #     today = datetime.date.today()
    #     begin = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
    #     end = (today + datetime.timedelta(days=2)).strftime('%m/%d/%Y')
    #     self.teacher.add_assignment( assignment='reading',
    #                                  args={
    #                                      'title' : assignment_name,
    #                                      'description' : 'description',
    #                                      'periods' : {'all': (begin, end)},
    #                                      'reading_list' : ['ch1'],
    #                                      'status' : 'draft'
    #                                  })
    #     self.teacher.driver.find_element(
    #         By.XPATH,'//label[@data-title="'+assignemnt_name+'"]').click()
    #     wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
    #     wait.until(
    #         expect.visibility_of_element_located(
    #             (By.XPATH, '//span[text()="Publish"]')
    #         )
    #     )
    #     self.teacher.driver.find_element(
    #         By.XPATH,'//button[@aria-role="close" and @type="button" and text()="Cancel"]').click()
    #     assert ('calendar' in self.teacher.current_url()),\
    #         'not back at calendar after canceling draft reading'

    #     self.ps.test_updates['passed'] = True


    # # Case C8004 - 013 - Teacher | Cancel a draft reading after making changes using the Cancel button
    # @pytest.mark.skipif(str(8004) not in TESTS, reason='Excluded')  # NOQA
    # def test_teacher_cancel_a_draft_reading_after_making_changes_using_the_cancel_button(self):
    #     """Cancel a draft reading after making changes using the Cancel button.

    #     Steps: 
    #     On the calendar click on a assignment that is currently a draft
    #     Do at least one of the following:
    #     Enter an assignment name into the Assignment name text box
    #     Click on the 'Cancel' button
    #     Click on the 'ok' button

    #     Expected Result:
    #     Takes user back to calendar dashboard. 
    #     No changes have been made to the chosen draft on the calendar dashboard. 
    #     """
    #     self.ps.test_updates['name'] = 't1.14.013' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = ['t1','t1.14','t1.14.013','8004']
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions
    #     assignment_name = 'reading-007'
    #     today = datetime.date.today()
    #     begin = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
    #     end = (today + datetime.timedelta(days=2)).strftime('%m/%d/%Y')
    #     self.teacher.add_assignment( assignment='reading',
    #                                  args={
    #                                      'title' : assignment_name,
    #                                      'description' : 'description',
    #                                      'periods' : {'all': (begin, end)},
    #                                      'reading_list' : ['ch1'],
    #                                      'status' : 'draft'
    #                                  })
    #     self.teacher.driver.find_element(
    #         By.XPATH,'//label[@data-title="'+assignemnt_name+'"]').click()
    #     wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
    #     wait.until(
    #         expect.element_to_be_clickable(
    #             (By.ID, 'reading-title')
    #         )
    #     )
    #     self.teacher.driver.find_element(By.ID, 'reading-title').send_keys('reading-0013')
    #     self.teacher.driver.find_element(
    #         By.XPATH,'//button[@aria-role="close" and @type="button" and text()="Cancel"]').click()
    #     wait.until(
    #         expect.visibility_of_element_located(
    #             (By.XPATH, '//button[contains(@class,"ok")]')
    #         )
    #     ).click()
    #     assert ('calendar' in self.teacher.current_url()),\
    #         'not back at calendar after making changes, then canceling reading'

    #     self.ps.test_updates['passed'] = True


    # # Case C8005 - 014 - Teacher | Cancel a draft reading before making changes using the X
    # @pytest.mark.skipif(str(8005) not in TESTS, reason='Excluded')  # NOQA
    # def test_teacher_cancel_a_draft_reading_before_making_changes_using_the_x(self):
    #     """Cancel a draft reading before making any changes using the X.

    #     Steps: 
    #     On the calendar click on a draft assignment 
    #     Click on the 'X' button

    #     Expected Result:
    #     Takes user back to calendar dashboard. 
    #     No changes have been made to the chosen draft on the calendar dashboard. 
    #     """
    #     self.ps.test_updates['name'] = 't1.14.014' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = ['t1','t1.14','t1.14.014','8005']
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions
    #     assignment_name = 'reading-007'
    #     today = datetime.date.today()
    #     begin = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
    #     end = (today + datetime.timedelta(days=2)).strftime('%m/%d/%Y')
    #     self.teacher.add_assignment( assignment='reading',
    #                                  args={
    #                                      'title' : assignment_name,
    #                                      'description' : 'description',
    #                                      'periods' : {'all': (begin, end)},
    #                                      'reading_list' : ['ch1'],
    #                                      'status' : 'draft'
    #                                  })
    #     self.teacher.driver.find_element(
    #         By.XPATH,'//label[@data-title="'+assignemnt_name+'"]').click()
    #     wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
    #     wait.until(
    #         expect.element_to_be_clickable(
    #             (By.XPATH,
    #              '//button[@aria-role="close" and contains(@class,"close-x")]')
    #         )
    #     ).click()
    #     assert ('calendar' in self.teacher.current_url()),\
    #         'not back at calendar after canceling reading with x'

    #     self.ps.test_updates['passed'] = True


    # # Case C8006 - 015 - Teacher | Cancel a draft reading after making changes using the X
    # @pytest.mark.skipif(str(8006) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Cancel a draft reading after making changes using the X.

    #     Steps: 
    #     On the calendar click on a assignment that is currently a draft
    #     Enter an assignment name into the Assignment name text box [user decision]
    #     Click on the 'X' button
    #     Click on the "ok" button

    #     Expected Result:

    #     Takes user back to calendar dashboard. 
    #     No changes have been made to the chosen draft on the calendar dashboard. 

    #     """
    #     self.ps.test_updates['name'] = 't1.14.015' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = ['t1','t1.14','t1.14.015','8006']
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions
    #     assignment_name = 'reading-007'
    #     today = datetime.date.today()
    #     begin = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
    #     end = (today + datetime.timedelta(days=2)).strftime('%m/%d/%Y')
    #     self.teacher.add_assignment( assignment='reading',
    #                                  args={
    #                                      'title' : assignment_name,
    #                                      'description' : 'description',
    #                                      'periods' : {'all': (begin, end)},
    #                                      'reading_list' : ['ch1'],
    #                                      'status' : 'draft'
    #                                  })
    #     self.teacher.driver.find_element(
    #         By.XPATH,'//label[@data-title="'+assignemnt_name+'"]').click()
    #     wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
    #     wait.until(
    #         expect.element_to_be_clickable(
    #             (By.ID, 'reading-title')
    #         )
    #     )
    #     self.teacher.driver.find_element(By.ID, 'reading-title').send_keys('reading-015')
    #     self.teacher.driver.find_element(
    #         By.XPATH,
    #         '//button[@aria-role="close" and contains(@class,"close-x")]').click()
    #     wait.until(
    #         expect.visibility_of_element_located(
    #             (By.XPATH, '//button[contains(@class,"ok")]')
    #         )
    #     ).click()
    #     assert ('calendar' in self.teacher.current_url()),\
    #         'not back at calendar after making changes, then canceling reading with x'

    #     self.ps.test_updates['passed'] = True


    # Case C8007 - 016 - Teacher | Attempt to publish a reading with blank required fields
    @pytest.mark.skipif(str(8007) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_attempt_to_publish_a_reading_with_blank_required_feilds(self):
        """Attempt to publish a reading with blank required fields.

        Steps: 

        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Reading' option
        Click on the 'Publish' button

        Expected Result:

        Remains on the Add Assignment page. 
        Does not allow user to publish assignments. 
        All required fields that were left blank become red, and specify that they are required fields.

        """
        self.ps.test_updates['name'] = 't1.14.016' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.14','t1.14.016','8007']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.driver.find_element(
            By.XPATH, '//button[contains(@class,"dropdown-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.find_element(By.XPATH, '..').get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Reading').click()
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class,"-publish")]')
            )
        ).click()
        self.teacher.driver.find_element(
            By.XPATH,'//span[contains(text(),"Required Field")]')
        assert ('readings' in self.teacher.current_url()),\
            'went back to calendar even though required feilds were left blank'

        self.ps.test_updates['passed'] = True


    # Case C8008 - 017 - Teacher | Attempt to save a draft reading with blank required fields
    @pytest.mark.skipif(str(8008) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_attempt_to_save_a_draft_reading_with_blank_required_feilds(self):
        """Attempt to save a draft reading with blank required fields.

        Steps: 
        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Reading' option
        Click on the 'Save As Draft' button

        Expected Result:
        Remains on the Add Assignment page. 
        Does not allow user to save assignments. 
        All required fields that were left blank become red, and specify that they are required fields
        """
        self.ps.test_updates['name'] = 't1.14.017' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.14','t1.14.017','8008']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_menu = self.teacher.driver.find_element(
            By.XPATH, '//button[contains(@class,"dropdown-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.find_element(By.XPATH, '..').get_attribute('class'):
            assignment_menu.click()
        self.teacher.driver.find_element(By.LINK_TEXT, 'Add Reading').click()
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class,"-save")]')
            )
        ).click()
        self.teacher.driver.find_element(
            By.XPATH,'//span[contains(text(),"Required Field")]')
        assert ('readings' in self.teacher.current_url()),\
            'went back to calendar even though required feilds were left blank'

        self.ps.test_updates['passed'] = True
        self.ps.test_updates['passed'] = True


    # Case C8009 - 018 - Teacher | Delete an unopened reading
    @pytest.mark.skipif(str(8009) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_delete_an_unopened_reading(self):
        """Delete an unopened reading.

        Steps: 
        On the calendar click on a reading that is unopened
        Click on the 'Edit Assignment' button
        Click on the 'Delete Assignment' button
        Click on the "ok" button
        
        Expected Result:
        Takes user back to calendar dashboard. 
        Chosen assignment no longer appears on teacher calendar dashboard.
        """
        self.ps.test_updates['name'] = 't1.14.018' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.14','t1.14.018','8009']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading-018'
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=2)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
        self.teacher.add_assignment( assignment='reading',
                                     args={
                                         'title' : assignment_name,
                                         'description' : 'description',
                                         'periods' : {'all': (begin, end)},
                                         'reading_list' : ['ch1'],
                                         'status' : 'publish'
                                     })
        original_readings = self.teacher.driver.find_elements(
            By.XPATH,'//label[@data-title="'+assignemnt_name+'"]')
        self.teacher.driver.find_element(
            By.XPATH,'//label[@data-title="'+assignemnt_name+'"]').click()
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contians(@class,"-edit-assignment")]')
            )
        ).click()
        wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contians(@class,"deltete-link")]')
            )
        ).click()
        self.teacher.driver.find_element(
            By.XPATH,'//butto[contains(text(),"Yes")]').click()
        assert ('calendar' in self.teacher.current_url()), \
            'not returned to calendar after deleting an assignment'
        deleted_reading = self.teacher.driver.find_elements(
            By.XPATH,'//label[@data-title="'+assignemnt_name+'"]')
        assert ( len(deleted_reading) == len(original_reaings)-1 ), \
            'assignment not deleted'

        self.ps.test_updates['passed'] = True


    # Case C8010 - 019 - Teacher | Delete an open reading
    @pytest.mark.skipif(str(8010) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_delete_an_open_reading(self):
        """Delete an open reading.

        Steps: 
        On the calendar click on an open reading
        Click on the 'View Assignment' button
        
        Expected Result:
        No "Delete Assignment" button found.
        """
        self.ps.test_updates['name'] = 't1.14.019' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.14','t1.14.019','8010']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading-019'
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
        self.teacher.add_assignment( assignment='reading',
                                     args={
                                         'title' : assignment_name,
                                         'description' : 'description',
                                         'periods' : {'all': (begin, end)},
                                         'reading_list' : ['ch1'],
                                         'status' : 'publish'
                                     })
        original_readings = self.teacher.driver.find_elements(
            By.XPATH,'//label[@data-title="'+assignemnt_name+'"]')
        self.teacher.driver.find_element(
            By.XPATH,'//label[@data-title="'+assignemnt_name+'"]').click()
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contians(@class,"-edit-assignment")]')
            )
        ).click()
        wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contians(@class,"deltete-link")]')
            )
        ).click()
        self.teacher.driver.find_element(
            By.XPATH,'//butto[contains(text(),"Yes")]').click()
        assert ('calendar' in self.teacher.current_url()), \
            'not returned to calendar after deleting an assignment'
        deleted_reading = self.teacher.driver.find_elements(
            By.XPATH,'//label[@data-title="'+assignemnt_name+'"]')
        assert ( len(deleted_reading) == len(original_reaings)-1 ), \
            'assignment not deleted'

        self.ps.test_updates['passed'] = True


    # Case C8011 - 020 - Teacher | Delete a draft reading
    @pytest.mark.skipif(str(8011) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_delete_a_draft_reading(self):
        """Delete a draft reading.

        Steps: 
        On the calendar click on a draft
        Click on the 'Delete Assignment' button
        Click on the 'ok' button
        
        Expected Result:
        Takes user back to calendar dashboard. 
        Chosen assignment no longer appears on teacher calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.14.020' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.14','t1.14.020','8011']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading-020'
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
        self.teacher.add_assignment( assignment='reading',
                                     args={
                                         'title' : assignment_name,
                                         'description' : 'description',
                                         'periods' : {'all': (begin, end)},
                                         'reading_list' : ['ch1'],
                                         'status' : 'draft'
                                     })
        original_readings = self.teacher.driver.find_elements(
            By.XPATH,'//label[@data-title="'+assignemnt_name+'"]')
        self.teacher.driver.find_element(
            By.XPATH,'//label[@data-title="'+assignemnt_name+'"]').click()
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contians(@class,"deltete-link")]')
            )
        ).click()
        self.teacher.driver.find_element(
            By.XPATH,'//butto[contains(text(),"Yes")]').click()
        assert ('calendar' in self.teacher.current_url()), \
            'not returned to calendar after deleting an assignment'
        deleted_reading = self.teacher.driver.find_elements(
            By.XPATH,'//label[@data-title="'+assignemnt_name+'"]')
        assert ( len(deleted_reading) == len(original_reaings)-1 ), \
            'assignment not deleted'

        self.ps.test_updates['passed'] = True

    # #exact steps already in case 001, adding description also in many other cases with additional steps
    # # Case C8012 - 021 - Teacher | Add a description to a reading 
    # @pytest.mark.skipif(str(8012) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Add a description to a reading.

    #     Steps: 
    #     Click on the 'Add Assignment' drop down menu
    #     Click on the 'Add Reading' option
    #     Enter an assignment name into the Assignment name text box
    #     Enter an assignment description into the Assignment description text box
    #     Enter into Due Date text field date as MM/DD/YYYY
    #     Click on the 'Publish' button
        
    #     Expected Result:
    #     Takes user back to calendar dashboard. 
    #     Assignment with description should be on calendar on its due date.
    #     """
    #     self.ps.test_updates['name'] = 't1.14.021' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = ['t1','t1.14','t1.14.021','8012']
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # Case C8013 - 022 - Teacher | Change a description for a draft reading
    @pytest.mark.skipif(str(8013) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_change_a_description_for_a_draft_reading(self):
        """Change a description for a draft reading.

        Steps: 
        On the calendar click on a draft assignment 
        Enter a new assignment description into the Assignment description text box
        CLick on the 'Save As Draft' button
        
        Expected Result:
        Takes user back to calendar dashboard. 
        Assignment description of the chosen draft should have the new description.
        """
        self.ps.test_updates['name'] = 't1.14.022' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.14','t1.14.022','8013']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading-022'
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
        self.teacher.add_assignment( assignment='reading',
                                     args={
                                         'title' : assignment_name,
                                         'description' : 'description',
                                         'periods' : {'all': (begin, end)},
                                         'reading_list' : ['ch1'],
                                         'status' : 'draft'
                                     })
        self.teacher.driver.find_element(
            By.XPATH,'//label[@data-title="'+assignemnt_name+'"]').click()
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]//textarea' +
            '[contains(@class,"form-control")]'). \
            send_keys('NEW description')
        # no more save option, only publish
        self.teacher.driver.find_element(
            By.XPATH, '//button[contains(@class,"-publish")]').click()
        assert('calendar' in self.teacher.current_url()),\
            'not returned to caendar ater updating description'
        self.ps.test_updates['passed'] = True


    # Case C8014 - 023 - Teacher | Change a description for an open reading
    @pytest.mark.skipif(str(8014) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_change_a_description_for_an_open_reading(self):
        """Change a description for an open reading.

        Steps: 
        On the calendar click on an open reading assignment 
        Click on the "Edit Assignment" button
        Enter a new assignment description into the Assignment description text box
        Click on the 'Publish' button
        
        Expected Result:

        Takes user back to calendar dashboard. 
        Assignment description of the chosen reading should have the new description.

        """
        self.ps.test_updates['name'] = 't1.14.023' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.14','t1.14.023','8014']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading-023'
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
        self.teacher.add_assignment( assignment='reading',
                                     args={
                                         'title' : assignment_name,
                                         'description' : 'description',
                                         'periods' : {'all': (begin, end)},
                                         'reading_list' : ['ch1'],
                                         'status' : 'publisj'
                                     })
        self.teacher.driver.find_element(
            By.XPATH,'//label[@data-title="'+assignemnt_name+'"]').click()
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(@class,"-edit-assignment")]')
            )
        ).click()
        wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]//textarea' +
            '[contains(@class,"form-control")]'). \
            send_keys('NEW description')
        self.teacher.driver.find_element(
            By.XPATH, '//button[contains(@class,"-publish")]').click()
        assert('calendar' in self.teacher.current_url()),\
            'not returned to caendar ater updating description'

        self.ps.test_updates['passed'] = True

    
    # # exact same steps as 001 and other cases, not needed?
    # # Case C8015 - 024 - Teacher | Add a name to a reading
    # @pytest.mark.skipif(str(8015) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Add a name to a reading.

    #     Steps: 
    #     Click on the 'Add Assignment' drop down menu
    #     Click on the 'Add Reading' option
    #     Enter an assignment name into the Assignment name text box 
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
    #     self.ps.test_updates['tags'] = ['t1','t1.14','t1.14.024','8015']
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # Case C8016 - 025 - Teacher | Change a name for a draft reading
    @pytest.mark.skipif(str(8016) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Change a name for a draft reading.

        Steps: 

        On the calendar click on a draft
        Enter a new name into the Assignment name text box
        Click on the 'Save As Draft' button
        
        Expected Result:

        Takes user back to calendar dashboard. 
        Assignment description of the chosen draft should have the new name.

        """
        self.ps.test_updates['name'] = 't1.14.025' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.14','t1.14.025','8016']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading-025'
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
        self.teacher.add_assignment( assignment='reading',
                                     args={
                                         'title' : assignment_name,
                                         'description' : 'description',
                                         'periods' : {'all': (begin, end)},
                                         'reading_list' : ['ch1'],
                                         'status' : 'publish'
                                     })
        self.teacher.driver.find_element(
            By.XPATH,'//label[@data-title="'+assignemnt_name+'"]').click()
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.driver.find_element(
            By.ID, 'reading-title').send_keys('NEW'+assignemnt_name)
        # only publish option now, no more save
        self.teacher.driver.find_element(
            By.XPATH, '//button[contains(@class,"-publish")]').click()
        assert('calendar' in self.teacher.current_url()),\
            'not returned to caendar ater updating description'
        self.teacher.driver.find_element(
            By.XPATH,'//label[@data-title="NEW'+assignemnt_name+'"]')
        self.ps.test_updates['passed'] = True


    # Case C8017 - 026 - Teacher | Change a name for an open reading
    @pytest.mark.skipif(str(8017) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_change_a_name_for_an_open_reading(self):
        """Change a name for an open reading.

        Steps: 
        On the calendar click on an open reading assignment
        click on the "Edit Assignment" button
        Enter a new assignment name into the Assignment name text box
        Click on the 'Publish' button
        
        Expected Result:
        Takes user back to calendar dashboard, with chosen assignment open. 
        Assignment name of the chosen reading should have the new name.

        """
        self.ps.test_updates['name'] = 't1.14.026' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.14','t1.14.026','8017']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'reading-025'
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
        self.teacher.add_assignment( assignment='reading',
                                     args={
                                         'title' : assignment_name,
                                         'description' : 'description',
                                         'periods' : {'all': (begin, end)},
                                         'reading_list' : ['ch1'],
                                         'status' : 'publish'
                                     })
        self.teacher.driver.find_element(
            By.XPATH,'//label[@data-title="'+assignemnt_name+'"]').click()
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
        wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(@class,"-edit-assignment")]')
            )
        ).click()
        wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        self.teacher.driver.find_element(
            By.ID, 'reading-title').send_keys('NEW'+assignemnt_name)
        # only publish option now, no more save
        self.teacher.driver.find_element(
            By.XPATH, '//button[contains(@class,"-publish")]').click()
        assert('calendar' in self.teacher.current_url()),\
            'not returned to caendar ater updating description'
        self.teacher.driver.find_element(
            By.XPATH,'//label[@data-title="NEW'+assignemnt_name+'"]')

        self.ps.test_updates['passed'] = True

    # # Case C8018 - 027 - Teacher | Add a single section to a reading
    # @pytest.mark.skipif(str(8018) not in TESTS, reason='Excluded')  # NOQA
    # def test_teacher_add_a_single_section_to_a_reading(self):
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
    #     self.ps.test_updates['tags'] = ['t1','t1.14','t1.14.027','8018']
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions
    #     assignment_name = 'reading-027'
    #     assignment = Assignment()
    #     assignment_menu = self.teacher.driver.find_element(
    #         By.XPATH, '//button[contains(@class,"dropdown-toggle")]')
    #     # if the Add Assignment menu is not open
    #     if 'open' not in assignment_menu.find_element(By.XPATH, '..').get_attribute('class'):
    #         assignment_menu.click()
    #     self.teacher.driver.find_element(By.LINK_TEXT, 'Add Reading').click()
    #     wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
    #     wait.until(
    #         expect.element_to_be_clickable(
    #             (By.ID, 'reading-title')
    #         )
    #     )
    #     self.teacher.driver.find_element(By.ID, 'reading-title').send_keys(assignment_name)
    #     self.teacher.driver.find_element(
    #         By.XPATH,
    #         '//div[contains(@class,"assignment-description")]//textarea' +
    #         '[contains(@class,"form-control")]'). \
    #         send_keys('description')
    #     #set due dates
    #     self.teacher.driver.find_element(By.ID,"hide-periods-radio").click()
    #     today = datetime.date.today()
    #     opens_on = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
    #     closes_on = (today + datetime.timedelta(days=2)).strftime('%m/%d/%Y')
    #     assignment.assign_periods(self.teacher.driver,{'all':[opens_on,closes_on]})
    #     # add reading sections to the assignment
    #     self.teacher.driver.find_element(By.ID, 'reading-select').click()
    #     wait.until(
    #         expect.visibility_of_element_located(
    #             (By.XPATH, '//div[contains(@class,"reading-plan")]')
    #         )
    #     )
    #     section = '2.1'
    #     chapter = section.split('.')[0]
    #     data_chapter = self.teacher.driver.find_element(
    #         By.XPATH,
    #         '//h2[contains(@data-chapter-section,"%s")]/a' % chapter
    #     )
    #     if data_chapter.get_attribute('aria-expanded')=='false':
    #         data_chapter.click()
    #     wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME)
    #     marked = wait.until(
    #         expect.visibility_of_element_located(
    #             (By.XPATH,
    #              ('//span[contains(@data-chapter-section' +
    #               ',"{s}") and text()="{s}"]').format(s=section) +
    #              '/preceding-sibling::span/input')
    #         )
    #     )
    #     if not marked.is_selected():
    #         marked.click()

    #     self.teacher.driver.find_element(By.XPATH,
    #                         '//button[text()="Add Readings"]').click()
    #     # publish
    #     wait.until(
    #         expect.visibility_of_element_located(
    #             (By.XPATH, '//span[text()="Publish"]')
    #         )
    #     )
    #     self.teacher.driver.find_element(
    #             By.XPATH, '//button[contains(@class,"-publish")]').click()
    #     self.teacher.driver.find_element_by_xpath(
    #         "//label[contains(text(), '"+assignment_name+"')]")

    #     self.ps.test_updates['passed'] = True


    # # Case C8019 - 028 - Teacher | Add a complete chapter to a reading
    # @pytest.mark.skipif(str(8019) not in TESTS, reason='Excluded')  # NOQA
    # def test_teacher_add_a_coplete_chapter_to_a_reading(self):
    #     """Add a complete chapter to a reading.

    #     Steps: 
    #     Click on the 'Add Assignment' drop down menu
    #     Click on the 'Add Reading' option
    #     Enter an assignment name into the Assignment name text box [user decision]
    #     Enter into Due Date text field date as MM/DD/YYYY
    #     Click on the '+ Add More Readings' button
    #     Click on a chapter checkbox
    #     Scroll to the bottom
    #     Click on the "Add Readings" button
    #     Click on the 'Publish' button
        
    #     Expected Result:
    #     Takes user back to the calendar dashboard, with the new reading assignment

    #     """
    #     self.ps.test_updates['name'] = 't1.14.028' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = ['t1','t1.14','t1.14.028','8019']
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions
    #     assignment_name = 'reading-028'
    #     assignment = Assignment()
    #     assignment_menu = self.teacher.driver.find_element(
    #         By.XPATH, '//button[contains(@class,"dropdown-toggle")]')
    #     # if the Add Assignment menu is not open
    #     if 'open' not in assignment_menu.find_element(By.XPATH, '..').get_attribute('class'):
    #         assignment_menu.click()
    #     self.teacher.driver.find_element(By.LINK_TEXT, 'Add Reading').click()
    #     wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
    #     wait.until(
    #         expect.element_to_be_clickable(
    #             (By.ID, 'reading-title')
    #         )
    #     )
    #     self.teacher.driver.find_element(By.ID, 'reading-title').send_keys(assignment_name)
    #     self.teacher.driver.find_element(
    #         By.XPATH,
    #         '//div[contains(@class,"assignment-description")]//textarea' +
    #         '[contains(@class,"form-control")]'). \
    #         send_keys('description')
    #     #set due dates
    #     self.teacher.driver.find_element(By.ID,"hide-periods-radio").click()
    #     today = datetime.date.today()
    #     opens_on = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
    #     closes_on = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
    #     assignment.assign_periods(self.teacher.driver,{'all':[opens_on,closes_on]})
    #     # add reading sections to the assignment
    #     self.teacher.driver.find_element(By.ID, 'reading-select').click()
    #     wait.until(
    #         expect.visibility_of_element_located(
    #             (By.XPATH, '//div[contains(@class,"reading-plan")]')
    #         )
    #     )
    #     chapter_num = '2'
    #     chapter = self.teacher.driver.find_element(
    #         By.XPATH,
    #         '//h2[@data-chapter-section="%s"]' % chapter_num+
    #         '//i[contains(@class,"tutor-icon")]'
    #     )
    #     time.sleep(0.5)
    #     if not chapter.is_selected():
    #         chapter.click()
    #     element = self.teacher.driver.find_element(By.XPATH,
    #                         '//button[text()="Add Readings"]')
    #     self.teacher.driver.execute_script('return arguments[0].scrollIntoView();', element)
    #     self.teacher.driver.execute_script('window.scrollBy(0, -80);')
    #     element.click()
    #     # publish
    #     wait.until(
    #         expect.visibility_of_element_located(
    #             (By.XPATH, '//span[text()="Publish"]')
    #         )
    #     )
    #     self.teacher.driver.find_element(
    #             By.XPATH, '//button[contains(@class,"-publish")]').click()
    #     self.teacher.driver.find_element_by_xpath(
    #         "//label[contains(text(), '"+assignment_name+"')]")

    #     self.ps.test_updates['passed'] = True


    # # Case C8020 - 029 - Teacher | Remove a single section from a reading from the Select Readings screen
    # @pytest.mark.skipif(str(8020) not in TESTS, reason='Excluded')  # NOQA
    # def test_teacher_remove_a_single_section_from_a_reading_from_the_select_readings_screen(self):
    #     """Remove a single section from a reading from the Select Readings screen.

    #     Steps: 

    #     On the calendar click on a closed reading
    #     Click on the 'Edit Assignment' button
    #     Click on the '+ Add More Readings" button
    #     click on the check box next to a section that is currently added, but to be removed
    #     Click on the 'Add Readings" button
    #     Click on the "Publish" button
        
    #     Expected Result:

    #     Takes user back to the calendar dashboard. 
    #     Reading assignment has been updated to have the single section removed.
    #     """
    #     self.ps.test_updates['name'] = 't1.14.029' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = ['t1','t1.14','t1.14.029','8020']
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions
    #     assignment_name = 'reading-029'
    #     section_to_remove = '1.2'
    #     today = datetime.date.today()
    #     begin = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
    #     end = (today + datetime.timedelta(days=2)).strftime('%m/%d/%Y')
    #     self.teacher.add_assignment( assignment='reading',
    #                                  args={
    #                                      'title' : assignment_name,
    #                                      'description' : 'description',
    #                                      'periods' : {'all': (begin, end)},
    #                                      'reading_list' : ['1.1',section_to_remove,'1.3'],
    #                                      'status' : 'publish'
    #                                  })
    #     self.teacher.driver.find_element(
    #         By.XPATH,'//label[@data-title="'+assignemnt_name+'"]').click()
    #     wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
    #     wait.until(
    #         expect.element_to_be_clickable(
    #             (By.XPATH, '//a[contains(@class,"-edit-assignment")]')
    #         )
    #     ).click()
    #     # remove section
    #     self.teacher.driver.find_element(By.ID, 'reading-select').click()
    #     wait.until(
    #         expect.visibility_of_element_located(
    #             (By.XPATH, '//div[contains(@class,"reading-plan")]')
    #         )
    #     )
    #     chapter = section_to_remove.split('.')[0]
    #     data_chapter = self.teacher.driver.find_element(
    #         By.XPATH,
    #         '//h2[contains(@data-chapter-section,"%s")]/a' % chapter
    #     )
    #     if data_chapter.get_attribute('aria-expanded')=='false':
    #         data_chapter.click()
    #     wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME)
    #     marked = wait.until(
    #         expect.visibility_of_element_located(
    #             (By.XPATH,
    #              ('//span[contains(@data-chapter-section' +
    #               ',"{s}") and text()="{s}"]').format(s=section_to_remove) +
    #              '/preceding-sibling::span/input')
    #         )
    #     )
    #     if marked.is_selected():
    #         marked.click()
    #     self.teacher.driver.find_element(By.XPATH,
    #                         '//button[text()="Add Readings"]').click()
    #     # check that it has been removed
    #     assert (self.teacherdriver.findElements(
    #         By.XPATH,'//span[@class="chapter-section" and'\
    #         '@data-chapter-section="'+section_to_remove+'"]').size() == 0),\
    #     'section has net been removed'
    #     # publish
    #     wait.until(
    #         expect.visibility_of_element_located(
    #             (By.XPATH, '//span[text()="Publish"]')
    #         )
    #     )
    #     self.teacher.driver.find_element(
    #             By.XPATH, '//button[contains(@class,"-publish")]').click()
    #     self.teacher.driver.find_element_by_xpath(
    #         "//label[contains(text(), '"+assignment_name+"')]")

    #     self.ps.test_updates['passed'] = True


    # # Case C8021 - 030 - Teacher | Remove a complete chapter from a reading from the Select Readings screen
    # @pytest.mark.skipif(str(8021) not in TESTS, reason='Excluded')  # NOQA
    # def test_teacher_remove_a_complete_chapter_from_the_select_readings_screen(self):
    #     """Remove a complete chapter from a reading from the Select Readings screen.

    #     Steps: 

    #     On the calendar click on a closed reading
    #     Click on the 'Edit Assignment' button
    #     Click on the '+ Add More Readings' button
    #     Click on the checkbox next to a chapter heading that is currently included
    #     Scroll to the bottom
    #     Click on the "Add Readings" button
    #     Click on the "Publish" button
        
    #     Expected Result:
    #     Takes user back to the calendar dashboard. 
    #     Reading assignment has been updated to have the chapter removed.

    #     """
    #     self.ps.test_updates['name'] = 't1.14.030' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = ['t1','t1.14','t1.14.030','8021']
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions
    #     assignment_name = 'reading-029'
    #     section_to_remove = 'ch2'
    #     today = datetime.date.today()
    #     begin = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
    #     end = (today + datetime.timedelta(days=2)).strftime('%m/%d/%Y')
    #     self.teacher.add_assignment( assignment='reading',
    #                                  args={
    #                                      'title' : assignment_name,
    #                                      'description' : 'description',
    #                                      'periods' : {'all': (begin, end)},
    #                                      'reading_list' : ['ch1',section_to_remove,],
    #                                      'status' : 'publish'
    #                                  })
    #     self.teacher.driver.find_element(
    #         By.XPATH,'//label[@data-title="'+assignemnt_name+'"]').click()
    #     wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
    #     wait.until(
    #         expect.element_to_be_clickable(
    #             (By.XPATH, '//a[contains(@class,"-edit-assignment")]')
    #         )
    #     ).click()
    #     # remove section
    #     self.teacher.driver.find_element(By.ID, 'reading-select').click()
    #     wait.until(
    #         expect.visibility_of_element_located(
    #             (By.XPATH, '//div[contains(@class,"reading-plan")]')
    #         )
    #     )
    #     chapter_num = section_to_remove[2:]
    #     chapter = self.teacher.driver.find_element(
    #         By.XPATH,
    #         '//h2[@data-chapter-section="%s"]' % chapter_num+
    #         '//i[contains(@class,"tutor-icon")]'
    #     )
    #     time.sleep(0.5)
    #     if chapter.is_selected():
    #         chapter.click()
    #     element = self.teacher.driver.find_element(By.XPATH,
    #                         '//button[text()="Add Readings"]')
    #     self.teacher.driver.execute_script('return arguments[0].scrollIntoView();', element)
    #     self.teacher.driver.execute_script('window.scrollBy(0, -80);')
    #     element.click()

    #     # check that it has been removed
    #     assert (self.teacherdriver.findElements(
    #         By.XPATH,'//span[@class="chapter-section" and'\
    #         '@data-chapter-section="'+section_to_remove+'."]').size() == 0),\
    #     'section has net been removed'
    #     # publish
    #     wait.until(
    #         expect.visibility_of_element_located(
    #             (By.XPATH, '//span[text()="Publish"]')
    #         )
    #     )
    #     self.teacher.driver.find_element(
    #             By.XPATH, '//button[contains(@class,"-publish")]').click()
    #     self.teacher.driver.find_element_by_xpath(
    #         "//label[contains(text(), '"+assignment_name+"')]")
    #     self.ps.test_updates['passed'] = True


    # # Case C8022 - 031 - Teacher | Remove a single section from a reading from the Add Reading Assignment screen
    # @pytest.mark.skipif(str(8022) not in TESTS, reason='Excluded')  # NOQA
    # def test_usertype_story_text(self):
    #     """Remove a single section from a reading from the Add Reading Assignment screen.

    #     Steps: 

    #     Click on the 'Add Assignment' drop down menu
    #     Click on the 'Add Reading' option
    #     Enter an assignment name into the Assignment name text box
    #     Enter an assignment description into the Assignment description text box
    #     Enter into Open Date text field date as MM/DD/YYYY
    #     Enter into Due Date text field date as MM/DD/YYYY
    #     Click on the "+ Add Readings" button
    #     Click on sections to add to assignment [user decision]
    #     scroll to bottom
    #     Click on the "Add Readings" button
    #     Click on the "x" button next to selected reading assignment to remove
    #     Click on the Publish' button
        
    #     Expected Result:
    #     Takes user back to the calendar dashboard. 
    #     Reading assignment has been updated to have the single section removed.
    #     """
    #     self.ps.test_updates['name'] = 't1.14.031' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = ['t1','t1.14','t1.14.031','8022']
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions
    #     assignment_name = 'reading-028'
    #     assignment = Assignment()
    #     assignment_menu = self.teacher.driver.find_element(
    #         By.XPATH, '//button[contains(@class,"dropdown-toggle")]')
    #     # if the Add Assignment menu is not open
    #     if 'open' not in assignment_menu.find_element(By.XPATH, '..').get_attribute('class'):
    #         assignment_menu.click()
    #     self.teacher.driver.find_element(By.LINK_TEXT, 'Add Reading').click()
    #     wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
    #     wait.until(
    #         expect.element_to_be_clickable(
    #             (By.ID, 'reading-title')
    #         )
    #     )
    #     self.teacher.driver.find_element(By.ID, 'reading-title').send_keys(assignment_name)
    #     self.teacher.driver.find_element(
    #         By.XPATH,
    #         '//div[contains(@class,"assignment-description")]//textarea' +
    #         '[contains(@class,"form-control")]'). \
    #         send_keys('description')
    #     #set due dates
    #     self.teacher.driver.find_element(By.ID,"hide-periods-radio").click()
    #     today = datetime.date.today()
    #     opens_on = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
    #     closes_on = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
    #     assignment.assign_periods(self.teacher.driver,{'all':[opens_on,closes_on]})
    #     # add reading sections to the assignment
    #     self.teacher.driver.find_element(By.ID, 'reading-select').click()
    #     wait.until(
    #         expect.visibility_of_element_located(
    #             (By.XPATH, '//div[contains(@class,"reading-plan")]')
    #         )
    #     )
    #     assignment.select_sections(self.teacher.driver,['2.1','3.1'])
    #     element = self.teacher.driver.find_element(By.XPATH,
    #                         '//button[text()="Add Readings"]')
    #     self.teacher.driver.execute_script('return arguments[0].scrollIntoView();', element)
    #     self.teacher.driver.execute_script('window.scrollBy(0, -80);')
    #     element.click()
    #     # publish
    #     wait.until(
    #         expect.visibility_of_element_located(
    #             (By.XPATH, '//span[text()="Publish"]')
    #         )
    #     )
    #     sections = self.teacher.driver.find_elements(
    #         By.XPATH,'//li[@class="selected-section"]')
    #     self.teacher.driver.find_element(
    #         By.XPATH,'//button[contains(@class,"remove-topic")]').click()
    #     sections_new = self.teacher.driver.find_elements(
    #         By.XPATH,'//li[@class="selected-section"]')
    #     assert (len(sections) == len(sections_new)+1),'section not removed'

    #     self.teacher.driver.find_element(
    #             By.XPATH, '//button[contains(@class,"-publish")]').click()
    #     self.teacher.driver.find_element_by_xpath(
    #         "//label[contains(text(), '"+assignment_name+"')]")
    #     self.ps.test_updates['passed'] = True


    # # Case C8023 - 032 - Teacher | Reorder the selected reading sections
    # @pytest.mark.skipif(str(8023) not in TESTS, reason='Excluded')  # NOQA
    # def test_teacher_reorder_the_selected_reading_sections(self):
    #     """Reorder the selected reading sections.

    #     Steps: 
    #     On the calendar click on a closed reading
    #     Click on the 'Edit Assignment' button
    #     Click on the up or down arrow buttons next to the selected readings
    #     Click on the "Publish" button
        
    #     Expected Result:
    #     Takes user back to the calendar dashboard. 
    #     Reading assignment has been updated to have the readings in the new order
    #     """
    #     self.ps.test_updates['name'] = 't1.14.032' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = ['t1','t1.14','t1.14.032','8023']
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions
    #     assignment_name = 'reading-032'
    #     today = datetime.date.today()
    #     begin = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
    #     end = (today + datetime.timedelta(days=2)).strftime('%m/%d/%Y')
    #     self.teacher.add_assignment( assignment='reading',
    #                                  args={
    #                                      'title' : assignment_name,
    #                                      'description' : 'description',
    #                                      'periods' : {'all': (begin, end)},
    #                                      'reading_list' : ['ch1'],
    #                                      'status' : 'publish'
    #                                  })
    #     self.teacher.driver.find_element(
    #         By.XPATH,'//label[@data-title="'+assignemnt_name+'"]').click()
    #     wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
    #     wait.until(
    #         expect.element_to_be_clickable(
    #             (By.XPATH, '//a[contains(@class,"-edit-assignment")]')
    #         )
    #     ).click()

    #     sections = self.teacher.driver.find_elements(
    #         By.XPATH,'//li[@class="selected-section"]//span[@class="chapter-section"]')
    #     self.teacher.driver.find_element(
    #         By.XPATH,'//button[contains(@class,"move-reading-up")]')
    #     sections_new = self.teacher.driver.find_elements(
    #         By.XPATH,'//li[@class="selected-section"]//span[@class="chapter-section"]')
    #     assert (sections[1] == sections_new[0]),\
    #         'did not rearrange sections'

    #     self.ps.test_updates['passed'] = True


    # # Case C8024 - 033 - Teacher | Change all fields in an unopened, published reading
    # @pytest.mark.skipif(str(8024) not in TESTS, reason='Excluded')  # NOQA
    # def test_teacher_change_all_feilds_in_an_unopened_published_reading(self):
    #     """Change all fields in an unopened, published reading.

    #     Steps: 
    #     Click on an existing reading on the calendar
    #     Click on the 'Edit' option
    #     Enter a new assignment name into the Assignment name text box [user decision]
    #     Enter a new assignment description into the Assignment description text box
    #     Enter into Open Date text field a new date as MM/DD/YYYY
    #     Enter into Due Date text field a new date as MM/DD/YYYY
    #     Remove a section from the readings
    #     Click the 'Publish' button
        
    #     Expected Result:
    #     Takes user back to the calendar dashboard. 
    #     The name, description, due dates, and chapters/sections of the reading have been updated. 
    #     The reading appears on its new due date on the calendar.
    #     """
    #     self.ps.test_updates['name'] = 't1.14.033' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = ['t1','t1.14','t1.14.033','8024']
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions
    #     assignment_name = 'reading-033'
    #     assignment = Assignment()
    #     today = datetime.date.today()
    #     begin = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
    #     end = (today + datetime.timedelta(days=2)).strftime('%m/%d/%Y')
    #     self.teacher.add_assignment( assignment='reading',
    #                                  args={
    #                                      'title' : assignment_name,
    #                                      'description' : 'description',
    #                                      'periods' : {'all': (begin, end)},
    #                                      'reading_list' : ['ch1'],
    #                                      'status' : 'publish'
    #                                  })
    #     self.teacher.driver.find_element(
    #         By.XPATH,'//label[@data-title="'+assignemnt_name+'"]').click()
    #     wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
    #     wait.until(
    #         expect.element_to_be_clickable(
    #             (By.XPATH, '//a[contains(@class,"-edit-assignment")]')
    #         )
    #     ).click()
    #     new_assignment_name = 'reading-033.2'
    #     wait.until(
    #         expect.element_to_be_clickable(
    #             (By.ID, 'reading-title')
    #         )
    #     )
    #     self.teacher.driver.find_element(By.ID, 'reading-title').send_keys(new_assignment_name)
    #     self.teacher.driver.find_element(
    #         By.XPATH,
    #         '//div[contains(@class,"assignment-description")]//textarea' +
    #         '[contains(@class,"form-control")]'). \
    #         send_keys('new_description')
    #     #set new due dates
    #     self.teacher.driver.find_element(By.ID,"hide-periods-radio").click()
    #     today = datetime.date.today()
    #     opens_on = (today + datetime.timedelta(days=2)).strftime('%m/%d/%Y')
    #     closes_on = (today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
    #     assignment.assign_periods(self.teacher.driver,{'all':[opens_on,closes_on]})
    #     # remove reading section from the assignment
    #     self.teacher.driver.find_element(
    #         By.XPATH,'//button[contains(@class,"remove-topic")]').click()
    #     # publish
    #     self.teacher.driver.find_element(
    #         By.XPATH, '//button[contains(@class,"-publish")]').click()
    #     self.teacher.driver.find_element_by_xpath(
    #         "//label[contains(text(), '"+new_assignment_name+"')]")

    #     self.ps.test_updates['passed'] = True


    # # Case C8025 - 034 - Teacher | Change all fields in a draft reading
    # @pytest.mark.skipif(str(8025) not in TESTS, reason='Excluded')  # NOQA
    # def test_teacher_change_all_feilds_in_a_draft_reading(self):
    #     """Change all fields in a draft reading.

    #     Steps: 
    #     Click on an existing draft reading on the calendar
    #     Enter a new assignment name into the Assignment name text box
    #     Enter a new assignment description into the Assignment description text box
    #     Enter into Open Date text field a new date as MM/DD/YYYY
    #     Enter into Due Date text field a new date as MM/DD/YYYY
    #     Click on the x next to a selected section
    #     Click the 'Save As Draft' button
        
    #     Expected Result:
    #     Takes user back to the calendar dashboard. 
    #     The name, description, due dates, and chapters/sections of the reading have been updated. 
    #     The draft reading now appears on its new due date on the calendar.

    #     """
    #     self.ps.test_updates['name'] = 't1.14.034' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = ['t1','t1.14','t1.14.034','8025']
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions
    #     assignment_name = 'reading-034'
    #     assignment = Assignment()
    #     today = datetime.date.today()
    #     begin = (today + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
    #     end = (today + datetime.timedelta(days=2)).strftime('%m/%d/%Y')
    #     self.teacher.add_assignment( assignment='reading',
    #                                  args={
    #                                      'title' : assignment_name,
    #                                      'description' : 'description',
    #                                      'periods' : {'all': (begin, end)},
    #                                      'reading_list' : ['ch1'],
    #                                      'status' : 'draft'
    #                                  })
    #     self.teacher.driver.find_element(
    #         By.XPATH,'//label[@data-title="'+assignemnt_name+'"]').click()
    #     wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
    #     new_assignment_name = 'reading-034.2'
    #     wait.until(
    #         expect.element_to_be_clickable(
    #             (By.ID, 'reading-title')
    #         )
    #     )
    #     self.teacher.driver.find_element(By.ID, 'reading-title').send_keys(new_assignment_name)
    #     self.teacher.driver.find_element(
    #         By.XPATH,
    #         '//div[contains(@class,"assignment-description")]//textarea' +
    #         '[contains(@class,"form-control")]'). \
    #         send_keys('new_description')
    #     #set new due dates
    #     self.teacher.driver.find_element(By.ID,"hide-periods-radio").click()
    #     today = datetime.date.today()
    #     opens_on = (today + datetime.timedelta(days=2)).strftime('%m/%d/%Y')
    #     closes_on = (today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
    #     assignment.assign_periods(self.teacher.driver,{'all':[opens_on,closes_on]})
    #     # remove reading section from the assignment
    #     self.teacher.driver.find_element(
    #         By.XPATH,'//button[contains(@class,"remove-topic")]').click()
    #     # publish - beacuse can no longer save
    #     self.teacher.driver.find_element(
    #         By.XPATH, '//button[contains(@class,"-publish")]').click()
    #     self.teacher.driver.find_element_by_xpath(
    #         "//label[contains(text(), '"+new_assignment_name+"')]")

    #     self.ps.test_updates['passed'] = True


    # # Case C8026 - 035 - Teacher | Change the name, description and due dates in an opened reading
    # @pytest.mark.skipif(str(8026) not in TESTS, reason='Excluded')  # NOQA
    # def test_teacher_change_the_name_description_and_due_dates_in_an_open_reading(self):
    #     """Change the name, description and due dates in an opened reading.

    #     Steps: 

    #     Click on an existing open reading on the calendar
    #     Click on the 'Edit' option
    #     Enter a new assignment name into the Assignment name text box [user decision]
    #     Enter a new assignment description into the Assignment description text box
    #     Enter into Due Date text field a new date as MM/DD/YYYY
    #     Click the 'Publish' button
        
    #     Expected Result:
    #     Takes user back to the calendar dashboard. 
    #     The name, description, due dates, and chapters/sections of the reading have been updated. 
    #     The reading now appears on its new due date on the calendar

    #     """
    #     self.ps.test_updates['name'] = 't1.14.035' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = ['t1','t1.14','t1.14.035','8026']
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions
    #     assignment_name = 'reading-034'
    #     today = datetime.date.today()
    #     begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
    #     end = (today + datetime.timedelta(days=2)).strftime('%m/%d/%Y')
    #     self.teacher.add_assignment( assignment='reading',
    #                                  args={
    #                                      'title' : assignment_name,
    #                                      'description' : 'description',
    #                                      'periods' : {'all': (begin, end)},
    #                                      'reading_list' : ['ch1'],
    #                                      'status' : 'publish'
    #                                  })
    #     self.teacher.driver.find_element(
    #         By.XPATH,'//label[@data-title="'+assignemnt_name+'"]').click()
    #     wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
    #     new_assignment_name = 'reading-034.2'
    #     wait.until(
    #         expect.element_to_be_clickable(
    #             (By.ID, 'reading-title')
    #         )
    #     )
    #     self.teacher.driver.find_element(By.ID, 'reading-title').send_keys(new_assignment_name)
    #     self.teacher.driver.find_element(
    #         By.XPATH,
    #         '//div[contains(@class,"assignment-description")]//textarea' +
    #         '[contains(@class,"form-control")]'). \
    #         send_keys('new_description')
    #     #set new due date
    #     self.teacher.driver.find_element(By.ID,"hide-periods-radio").click()
    #     today = datetime.date.today()
    #     closes_on = (today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
    #     self.teacher.driver.find_element(
    #         By.XPATH, '//div[contains(@class,"-due-date")]'\
    #         '//div[contains(@class,"datepicker__input")]').click()
    #     month = today.month
    #     year = today.year
    #     while (month != int(closes_on[:2]) or year != int(closes_on[6:])):
    #         self.teacher.driver.find_element(
    #             By.XPATH, '//a[contains(@class,"navigation--next")]').click()
    #         if month != 12:
    #             month += 1
    #         else:
    #             month = 1
    #             year += 1
    #     self.teacher.driver.find_element(
    #         By.XPATH, '//div[contains(@class,"datepicker__day")'\
    #         'and contains(text(),"'+ (closes_on[3:5]) +'")]').click()
    #     time.sleep(0.5)
    #     self.teacher.driver.find_element(By.CLASS_NAME, 'assign-to-label').click()
    #     # publish - beacuse can no longer save?
    #     self.teacher.driver.find_element(
    #         By.XPATH, '//button[contains(@class,"-publish")]').click()
    #     self.teacher.driver.find_element_by_xpath(
    #         "//label[contains(text(), '"+new_assignment_name+"')]")
    #     self.ps.test_updates['passed'] = True


    # # Case C8027 - 036 - Teacher | Info icon shows definitions for the status bar buttons
    # @pytest.mark.skipif(str(8027) not in TESTS, reason='Excluded')  # NOQA
    # def test_teacher_info_icon_shows_definitions_for_the_status_bar_buttons(self):
    #     """Info icon shows definitions for the Add Homework Assignment status bar buttons.

    #     Steps: 
    #     Click on the 'Add Assignment' drop down menu
    #     Click on the 'Add Reading' option
    #     Click on the info icon
        
    #     Expected Result:
    #     Instructions about the Publish, Cancel, and Save As Draft statuses appear
    #     """
    #     self.ps.test_updates['name'] = 't1.14.036' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = ['t1','t1.14','t1.14.036','8027']
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions
    #     assignment = Assignment()
    #     assignment_menu = self.teacher.driver.find_element(
    #         By.XPATH, '//button[contains(@class,"dropdown-toggle")]')
    #     # if the Add Assignment menu is not open
    #     if 'open' not in assignment_menu.find_element(By.XPATH, '..').get_attribute('class'):
    #         assignment_menu.click()
    #     self.teacher.driver.find_element(By.LINK_TEXT, 'Add Reading').click()
    #     wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME * 3)
    #     wait.until(
    #         expect.element_to_be_clickable(
    #             (By.ID, 'reading-title')
    #         )
    #     )
    #     self.teacher.driver.find_element(
    #         By.XPATH,'//button[contains(@class,"footer-instructions"]').click()
    #     self.teacher.driver.find_element(By.ID,'plan-footer-popover')

    #     self.ps.test_updates['passed'] = True
