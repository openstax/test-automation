"""Tutor v1, Epic 59 - ManageDistricsSchoolsAndCourses."""

import inspect
import json
import os
import pytest
import unittest
import datetime

from pastasauce import PastaSauce, PastaDecorator
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
# from staxing.assignment import Assignment
from selenium.webdriver.common.keys import Keys

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Admin

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': 'latest',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
LOCAL_RUN = os.getenv('LOCALRUN', 'false').lower() == 'true'
TESTS = os.getenv(
    'CASELIST',
    str([
        8341, 8342, 8343, 8344, 8345,
        8346, 8347, 8348, 8349, 8350,
        8351, 8352, 8353, 8354, 8355,
        8356, 8357, 8358, 8359, 8360,
        100135, 100136, 100137, 100138, 100139,
        100140
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestManageDistricsSchoolsAndCourses(unittest.TestCase):
    """T1.59 - Manage districts, schools, and courses."""

    def setUp(self):
        """Pretest settings."""
        # login as admin, go to user menu, click admin option
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        if not LOCAL_RUN:
            self.admin = Admin(
                use_env_vars=True,
                pasta_user=self.ps,
                capabilities=self.desired_capabilities
            )
        else:
            self.admin = Admin(
                use_env_vars=True,
            )
        self.admin.login()
        self.admin.goto_admin_control()

    def tearDown(self):
        """Test destructor."""
        if not LOCAL_RUN:
            self.ps.update_job(
                job_id=str(self.admin.driver.session_id),
                **self.ps.test_updates
            )
        try:
            self.admin.delete()
        except:
            pass

    # Case C8341 - 001 - Admin | Add a new district
    @pytest.mark.skipif(str(8341) not in TESTS, reason='Excluded')
    def test_admin_add_a_new_district_8341(self):
        """Add a new district.

        Steps:
        Click Course Organization in the header
        Click on Districts
        Click on Add district
        Enter a name for the district in the Name Text box
        Click Save

        Expected Result:
        A new district is added
        """
        self.ps.test_updates['name'] = 't1.59.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.001', '8341']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Districts')
            )
        ).click()

        self.admin.find(By.XPATH, "//a[text()='Add district']").click()
        self.admin.find(
            By.ID, "district_name"
        ).send_keys('automated test district')
        self.admin.find(
            By.XPATH, "//input[@value='Save']").click()

        # Delete the district
        district = self.admin.find(
            By.XPATH, "//tr/td[text()='automated test district']")
        district.find_element(
            By.XPATH, '..//a[text()="delete"]'
        ).click()
        self.admin.sleep(0.5)
        self.admin.driver.switch_to_alert().accept()
        self.admin.sleep(0.5)
        self.ps.test_updates['passed'] = True

    # Case C8342 - 002 - Admin | Change a district's name
    @pytest.mark.skipif(str(8342) not in TESTS, reason='Excluded')
    def test_admin_change_a_districts_name_8342(self):
        """Change a district's name.

        Steps:
        Click Course Organization in the header
        Click on Districts
        Click on edit next to a district
        Enter a name into the Name text box
        Click Save

        Expected Result:
        A district's name is changed
        """
        self.ps.test_updates['name'] = 't1.59.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.002', '8342']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Districts')
            )
        ).click()

        self.admin.find(By.XPATH, '//a[text()="Add district"]').click()
        self.admin.find(
            By.ID, "district_name"
        ).send_keys('automated test district')
        self.admin.find(
            By.XPATH, '//input[@value="Save"]').click()

        # Edit the district name
        district = self.admin.find(
            By.XPATH, '//tr/td[text()="automated test district"]')
        district.find_element(
            By.XPATH, '..//a[text()="edit"]'
        ).click()
        self.admin.find(By.ID, "district_name").send_keys(' edit')
        self.admin.find(
            By.XPATH, '//input[@value="Save"]').click()

        # Delete the district
        district = self.admin.find(
            By.XPATH, '//tr/td[text()="automated test district edit"]')
        district.find_element(
            By.XPATH, '..//a[text()="delete"]'
        ).click()
        self.admin.sleep(0.5)
        self.admin.driver.switch_to_alert().accept()
        self.admin.sleep(0.5)
        self.ps.test_updates['passed'] = True

    # Case C8343 - 003 - Admin | Delete an exisiting district
    @pytest.mark.skipif(str(8343) not in TESTS, reason='Excluded')
    def test_admin_delete_an_existing_district_8343(self):
        """Delete an existing district.

        Steps:
        Click Course Organization in the header
        Click on Districts
        Click on delete next to a district
        Click OK in the dialouge box

        Expected Result:
        A district is deleted
        """
        self.ps.test_updates['name'] = 't1.59.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.003', '8343']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Districts')
            )
        ).click()

        self.admin.find(By.XPATH, "//a[text()='Add district']").click()
        self.admin.find(
            By.ID, "district_name"
        ).send_keys('automated test district')
        self.admin.find(
            By.XPATH, "//input[@value='Save']").click()

        # Delete the district
        district = self.admin.find(
            By.XPATH, "//tr/td[text()='automated test district']")
        district.find_element(
            By.XPATH, '..//a[text()="delete"]'
        ).click()
        self.admin.sleep(0.5)
        self.admin.driver.switch_to_alert().accept()
        self.admin.sleep(0.5)
        self.ps.test_updates['passed'] = True

    # Case C8344 - 004 - Admin | Add a new school
    @pytest.mark.skipif(str(8344) not in TESTS, reason='Excluded')
    def test_admin_add_a_new_school_8344(self):
        """Add a new school.

        Steps:
        Click Course Organization in the header
        Click on Schools
        Click on Add School
        Enter a name into the Name text box
        Select a district
        Click Save

        Expected Result:
        A school is added
        """
        self.ps.test_updates['name'] = 't1.59.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.004', '8344']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Schools')
            )
        ).click()

        # add a school
        self.admin.find(By.XPATH, "//a[text()='Add school']").click()
        self.admin.find(
            By.ID, "school_name"
        ).send_keys('automated test school')
        self.admin.find(
            By.XPATH, '//input[@value="Save"]').click()

        # Delete the school
        school = self.admin.find(
            By.XPATH, "//tr/td[text()='automated test school']")
        school.find_element(
            By.XPATH, '..//a[text()="delete"]'
        ).click()
        self.admin.sleep(0.5)
        self.admin.driver.switch_to_alert().accept()
        self.admin.sleep(0.5)
        self.ps.test_updates['passed'] = True

    # Case C8345 - 005 - Admin | Change a school's name
    @pytest.mark.skipif(str(8345) not in TESTS, reason='Excluded')
    def test_admin_change_a_schools_name_8345(self):
        """Change a school's name.

        Steps:
        Click Course Organization in the header
        Click on Schools
        Click edit next to a school
        Enter a new name in the Name text box
        Click Save

        Expected Result:
        A school's name is changed
        """
        self.ps.test_updates['name'] = 't1.59.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.005', '8345']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Schools')
            )
        ).click()

        self.admin.find(By.XPATH, "//a[text()='Add school']").click()
        self.admin.find(
            By.ID, "school_name"
        ).send_keys('automated test school')
        self.admin.find(
            By.XPATH, "//input[@value='Save']").click()

        # Edit the school name
        district = self.admin.find(
            By.XPATH, "//tr/td[text()='automated test school']")
        district.find_element(
            By.XPATH, '..//a[text()="edit"]'
        ).click()
        self.admin.find(By.ID, "school_name").send_keys(' edit')
        self.admin.find(
            By.XPATH, "//input[@value='Save']").click()

        # Delete the school
        school = self.admin.find(
            By.XPATH, "//tr/td[text()='automated test school edit']")
        school.find_element(
            By.XPATH, '..//a[text()="delete"]'
        ).click()
        self.admin.sleep(0.5)
        self.admin.driver.switch_to_alert().accept()
        self.admin.sleep(0.5)
        self.ps.test_updates['passed'] = True

    # Case C8346 - 006 - Admin | Change a school's district
    @pytest.mark.skipif(str(8346) not in TESTS, reason='Excluded')
    def test_admin_change_a_schools_district_8346(self):
        """Change a school's district.

        Steps:
        Click Course Organization in the header
        Click on Schools
        Click edit next to a school
        Select a new district
        Click Save

        Expected Result:
        A school's district is changed
        """
        self.ps.test_updates['name'] = 't1.59.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.006', '8346']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Schools')
            )
        ).click()

        self.admin.find(By.XPATH, "//a[text()='Add school']").click()
        self.admin.find(
            By.ID, "school_name"
        ).send_keys('automated test school')
        self.admin.find(
            By.XPATH, "//input[@value='Save']").click()

        # Edit the school district
        district = self.admin.find(
            By.XPATH, "//tr/td[text()='automated test school']")
        district.find_element(
            By.XPATH, '..//a[text()="edit"]'
        ).click()
        self.admin.find(
            By.ID, "school_school_district_district_id"
        ).click()
        self.admin.find(
            By.XPATH, "//select/option[2]"
        ).click()
        self.admin.find(
            By.XPATH, "//input[@value='Save']").click()

        # Delete the school
        school = self.admin.find(
            By.XPATH, "//tr/td[text()='automated test school']")
        school.find_element(
            By.XPATH, '..//a[text()="delete"]'
        ).click()
        self.admin.sleep(0.5)
        self.admin.driver.switch_to_alert().accept()
        self.admin.sleep(0.5)
        self.ps.test_updates['passed'] = True

    # Case C8347 - 007 - Admin | Delete an exisiting school
    @pytest.mark.skipif(str(8347) not in TESTS, reason='Excluded')
    def test_admin_delete_an_existing_school_8347(self):
        """Delete an exisitng school.

        Steps:
        Click Course Organization in the header
        Click on Schools
        Click delete next to a school
        Click OK on the dialouge box

        Expected Result:
        A school is deleted
        """
        self.ps.test_updates['name'] = 't1.59.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.007', '8347']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Schools')
            )
        ).click()

        # Create the school
        self.admin.find(By.XPATH, "//a[text()='Add school']").click()
        self.admin.find(
            By.ID, "school_name"
        ).send_keys('automated test school')
        self.admin.find(
            By.XPATH, "//input[@value='Save']").click()

        # Delete the school
        school = self.admin.find(
            By.XPATH, "//tr/td[text()='automated test school']")
        school.find_element(
            By.XPATH, '..//a[text()="delete"]'
        ).click()
        self.admin.sleep(0.5)
        self.admin.driver.switch_to_alert().accept()
        self.admin.sleep(0.5)
        self.ps.test_updates['passed'] = True

    # Case C8348 - 008 - Admin | Add a new course
    @pytest.mark.skipif(str(8348) not in TESTS, reason='Excluded')
    def test_admin_add_a_new_course_8348(self):
        """Add a new course.

        Steps:
        Click Course Organization in the header
        Click on Courses
        Click Add Course at the bottom of the page
        Enter a name into the Name text box
        Select a school
        Select a catalog offering
        Click Save

        Expected Result:
        A new school is added
        """
        self.ps.test_updates['name'] = 't1.59.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.008', '8348']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Courses')
            )
        ).click()

        # Create the course
        self.admin.find(By.XPATH, "//a[text()='Add Course']").click()
        self.admin.find(By.XPATH, "//input[@id='course_name']").send_keys(
            "automated test course")
        self.admin.find(By.XPATH, "//input[@value='Save']").click()

        # Delete the course
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="pagination"]//a[not(@rel)][last()]')
            )
        ).click()
        course = self.admin.find(
            By.XPATH,
            "//div[@class='stats-card']" +
            "//span[text()=' automated test course']")
        course.find_element(
            By.XPATH, '../..//a[text()="Delete"]'
        ).click()
        self.admin.sleep(0.5)
        self.admin.driver.switch_to_alert().accept()
        self.admin.sleep(0.5)
        self.ps.test_updates['passed'] = True

    # Case C8349 - 009 - Admin | Edit course settings
    @pytest.mark.skipif(str(8349) not in TESTS, reason='Excluded')
    def test_admin_edit_course_settings_8349(self):
        """Edit course settings.

        Steps:
        Click Course Organization in the header
        Click on Courses
        Click Edit next to a course
        Change information in the Name textbox
        Change selected School and catalog offering
        Click the Save button

        Expected Result:
        Course is edited
        """
        self.ps.test_updates['name'] = 't1.59.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.009', '8349']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Courses')
            )
        ).click()
        self.admin.sleep(0.5)
        # Create the course
        self.admin.find(By.XPATH, "//a[text()='Add Course']").click()
        self.admin.find(By.XPATH, "//input[@id='course_name']").send_keys(
            "automated test course")
        self.admin.find(By.XPATH, "//input[@value='Save']").click()

        # Edit the course
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="pagination"]//a[not(@rel)][last()]')
            )
        ).click()
        course = self.admin.find(
            By.XPATH,
            "//div[@class='stats-card']" +
            "//span[text()=' automated test course']")
        course.find_element(
            By.XPATH, '../..//a[text()="Edit"]'
        ).click()
        self.admin.find(By.ID, "course_name").send_keys(
            " edit")
        self.admin.find(
            By.ID, "course_term").click()
        self.admin.find(
            By.XPATH,
            "//select[@id='course_term']/option[2]"
        ).click()
        self.admin.find(By.XPATH, "//input[@id='course_year']").send_keys(
            (Keys.DELETE * 4) + str(datetime.date.today().year))
        self.admin.find(
            By.ID, "course_catalog_offering_id").click()
        self.admin.find(
            By.XPATH,
            "//select[@id='course_catalog_offering_id']/option[2]"
        ).click()
        self.admin.find(
            By.ID, "course_school_district_school_id").click()
        self.admin.find(
            By.XPATH,
            "//select[@id='course_school_district_school_id']/option[2]"
        ).click()
        self.admin.find(By.XPATH, "//input[@value='Save']").click()

        # Delete the course
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="pagination"]//a[not(@rel)][last()]')
            )
        ).click()
        course = self.admin.find(
            By.XPATH,
            "//div[@class='stats-card']" +
            "//span[text()=' automated test course edit']")
        course.find_element(
            By.XPATH, '../..//a[text()="Delete"]'
        ).click()
        self.admin.sleep(0.5)
        self.admin.driver.switch_to_alert().accept()
        self.admin.sleep(0.5)
        self.ps.test_updates['passed'] = True

    # Case C8350 - 010 - Admin | Add a teacher to a course
    @pytest.mark.skipif(str(8350) not in TESTS, reason='Excluded')
    def test_admin_add_a_teacher_to_a_course_8350(self):
        """Add a teacher to a course.

        Steps:
        Click Course Organization in the header
        Click on Courses
        Click Edit next to a course
        Click on the Teacher tab
        Enter a teachers name or username into the search box
        Click on the name of selected teacher

        Expected Result:
        A teacher is added to the course
        """
        self.ps.test_updates['name'] = 't1.59.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.010', '8350']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Courses')
            )
        ).click()

        # Create the course
        self.admin.find(By.XPATH, "//a[text()='Add Course']").click()
        self.admin.find(By.XPATH, "//input[@id='course_name']").send_keys(
            "automated test course")
        self.admin.find(By.XPATH, "//input[@value='Save']").click()

        # Edit the course
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="pagination"]//a[not(@rel)][last()]')
            )
        ).click()
        course = self.admin.find(
            By.XPATH,
            "//div[@class='stats-card']" +
            "//span[text()=' automated test course']")
        course.find_element(
            By.XPATH, '../..//a[text()="Edit"]'
        ).click()
        # Add a Teacher
        self.admin.find(
            By.XPATH, '//a[@role="tab" and @aria-controls="teachers"]'
        ).click()
        self.admin.find(
            By.ID, 'course_teacher').send_keys("teacher")
        self.admin.sleep(1)
        self.admin.find(
            By.ID, 'course_teacher').send_keys(Keys.RETURN)
        # assert that a teacher was added
        self.admin.find(
            By.XPATH, '//div[@id="teachers"]//tbody/tr')
        # delete the teacher
        self.admin.find(
            By.XPATH, '//a[text()="Remove from course"]').click()
        self.admin.sleep(0.5)
        self.admin.driver.switch_to_alert().accept()
        self.admin.sleep(0.5)

        # Delete the course
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Courses')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="pagination"]//a[not(@rel)][last()]')
            )
        ).click()
        course = self.admin.find(
            By.XPATH,
            "//div[@class='stats-card']" +
            "//span[text()=' automated test course']")
        course.find_element(
            By.XPATH, '../..//a[text()="Delete"]'
        ).click()
        self.admin.sleep(0.5)
        self.admin.driver.switch_to_alert().accept()
        self.admin.sleep(0.5)
        self.ps.test_updates['passed'] = True

    # Case C8351 - 011 - Admin | Remove a teacher from a course
    @pytest.mark.skipif(str(8351) not in TESTS, reason='Excluded')
    def test_admin_remove_a_teacher_from_a_course_8351(self):
        """Remove a teacher from a course.

        Steps:
        Click Course Organization in the header
        Click on Courses
        Click Edit next to a course
        Click on the Teacher tab
        Click Remove from course for desired teacher
        Click OK in the dialogue box

        Expected Result:
        A teacher is revmoved from the course
        """
        self.ps.test_updates['name'] = 't1.59.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.011', '8351']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Courses')
            )
        ).click()

        # Create the course
        self.admin.find(By.XPATH, "//a[text()='Add Course']").click()
        self.admin.find(By.XPATH, "//input[@id='course_name']").send_keys(
            "automated test course")
        self.admin.find(By.XPATH, "//input[@value='Save']").click()

        # Edit the course
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="pagination"]//a[not(@rel)][last()]')
            )
        ).click()
        course = self.admin.find(
            By.XPATH,
            "//div[@class='stats-card']" +
            "//span[text()=' automated test course']")
        course.find_element(
            By.XPATH, '../..//a[text()="Edit"]'
        ).click()
        # Add a Teacher
        self.admin.find(
            By.XPATH, '//a[@role="tab" and @aria-controls="teachers"]'
        ).click()
        self.admin.find(
            By.ID, 'course_teacher').send_keys("teacher")
        self.admin.sleep(1)
        self.admin.find(
            By.ID, 'course_teacher').send_keys(Keys.RETURN)
        # assert that a teacher was added
        self.admin.find(
            By.XPATH, '//div[@id="teachers"]//tbody/tr')
        # delete the teacher
        self.admin.find(
            By.XPATH, '//a[text()="Remove from course"]').click()
        self.admin.sleep(0.5)
        self.admin.driver.switch_to_alert().accept()
        self.admin.sleep(0.5)

        # Delete the course
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Courses')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="pagination"]//a[not(@rel)][last()]')
            )
        ).click()
        course = self.admin.find(
            By.XPATH,
            "//div[@class='stats-card']" +
            "//span[text()=' automated test course']")
        course.find_element(
            By.XPATH, '../..//a[text()="Delete"]'
        ).click()
        self.admin.sleep(0.5)
        self.admin.driver.switch_to_alert().accept()
        self.admin.sleep(0.5)
        self.ps.test_updates['passed'] = True

    # Case C8352 - 012 - Admin | Set the course ecosystem
    @pytest.mark.skipif(str(8352) not in TESTS, reason='Excluded')
    def test_admin_set_the_course_ecosystem_8352(self):
        """Set the course ecosystem.

        Steps:
        Click Course Organization in the header
        Click on Courses
        Click Edit next to a course
        Click on the Course Content tab
        Select a course ecosystem
        Click Submit

        Expected Result:
        Request for a course ecosystem update submited and message displayed
        """
        self.ps.test_updates['name'] = 't1.59.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.012', '8352']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Courses')
            )
        ).click()

        # Create the course
        self.admin.find(By.XPATH, "//a[text()='Add Course']").click()
        self.admin.find(By.XPATH, "//input[@id='course_name']").send_keys(
            "automated test course")
        self.admin.find(By.XPATH, "//input[@value='Save']").click()

        # Edit the course
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="pagination"]//a[not(@rel)][last()]')
            )
        ).click()
        course = self.admin.find(
            By.XPATH,
            "//div[@class='stats-card']" +
            "//span[text()=' automated test course']")
        course.find_element(
            By.XPATH, '../..//a[text()="Edit"]'
        ).click()
        # Set Ecosystem
        self.admin.find(
            By.XPATH, '//a[@role="tab" and @aria-controls="content"]'
        ).click()
        self.admin.find(
            By.ID, 'ecosystem_id').click()
        self.admin.find(
            By.XPATH,
            "//select[@id='ecosystem_id']/option[2]"
        ).click()
        self.admin.find(
            By.XPATH, '//input[@value="Submit"]').click()
        # assert that that ecostystem was queued
        self.admin.find(
            By.XPATH, '//div[contains(@class,"alert")]')

        # Delete the course
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Courses')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="pagination"]//a[not(@rel)][last()]')
            )
        ).click()
        course = self.admin.find(
            By.XPATH,
            "//div[@class='stats-card']" +
            "//span[text()=' automated test course']")
        course.find_element(
            By.XPATH, '../..//a[text()="Delete"]'
        ).click()
        self.admin.sleep(0.5)
        self.admin.driver.switch_to_alert().accept()
        self.admin.sleep(0.5)
        self.ps.test_updates['passed'] = True

    # Case C8353 - 013 - Admin | Update the course ecosystem
    @pytest.mark.skipif(str(8353) not in TESTS, reason='Excluded')
    def test_admin_update_the_course_ecosystem_8353(self):
        """Update the course ecosystem.

        Steps:
        Click Course Organization in the header
        Click on Courses
        Click Edit next to a course
        Click on the Course Content tab
        Select a course ecosystem
        Click Submit

        Expected Result:
        The course ecosystem is queued for the course
        """
        self.ps.test_updates['name'] = 't1.59.013' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.013', '8353']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Courses')
            )
        ).click()

        # Create the course
        self.admin.find(By.XPATH, "//a[text()='Add Course']").click()
        self.admin.find(By.XPATH, "//input[@id='course_name']").send_keys(
            "automated test course")
        self.admin.find(By.XPATH, "//input[@value='Save']").click()

        # Edit the course
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="pagination"]//a[not(@rel)][last()]')
            )
        ).click()
        course = self.admin.find(
            By.XPATH,
            "//div[@class='stats-card']" +
            "//span[text()=' automated test course']")
        course.find_element(
            By.XPATH, '../..//a[text()="Edit"]'
        ).click()
        # Set Ecosystem
        self.admin.find(
            By.XPATH, '//a[@role="tab" and @aria-controls="content"]'
        ).click()
        self.admin.find(
            By.ID, 'ecosystem_id').click()
        self.admin.find(
            By.XPATH,
            "//select[@id='ecosystem_id']/option[2]"
        ).click()
        self.admin.find(
            By.XPATH, '//input[@value="Submit"]').click()
        # assert that that ecostystem was queued
        self.admin.find(
            By.XPATH, '//div[contains(@class,"alert")]')
        # Set a new Ecosystem
        self.admin.find(
            By.XPATH,
            "//select[@id='ecosystem_id']/option[3]"
        ).click()
        self.admin.find(
            By.XPATH, '//input[@value="Submit"]').click()

        # Delete the course
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Courses')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="pagination"]//a[not(@rel)][last()]')
            )
        ).click()
        course = self.admin.find(
            By.XPATH,
            "//div[@class='stats-card']" +
            "//span[text()=' automated test course']")
        course.find_element(
            By.XPATH, '../..//a[text()="Delete"]'
        ).click()
        self.admin.sleep(0.5)
        self.admin.driver.switch_to_alert().accept()
        self.admin.sleep(0.5)
        self.ps.test_updates['passed'] = True

    # Case C8354 - 014 - Admin | Add a period
    @pytest.mark.skipif(str(8354) not in TESTS, reason='Excluded')
    def test_admin_add_a_period_8354(self):
        """Add a period.

        Steps:
        Click Course Organization in the header
        Click on Courses
        Click Edit next to a course
        Click on the Periods tab
        Click Add Period
        Enter a name into the Name text box
        Click Save

        Expected Result:
        A new period is added
        """
        self.ps.test_updates['name'] = 't1.59.014' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.014', '8354']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Courses')
            )
        ).click()

        # Create the course
        self.admin.find(By.XPATH, "//a[text()='Add Course']").click()
        self.admin.find(By.XPATH, "//input[@id='course_name']").send_keys(
            "automated test course")
        self.admin.find(By.XPATH, "//input[@value='Save']").click()

        # Edit the course
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="pagination"]//a[not(@rel)][last()]')
            )
        ).click()
        course = self.admin.find(
            By.XPATH,
            "//div[@class='stats-card']" +
            "//span[text()=' automated test course']")
        course.find_element(
            By.XPATH, '../..//a[text()="Edit"]'
        ).click()
        # Add a period
        self.admin.find(
            By.XPATH, '//a[@role="tab" and @aria-controls="periods"]'
        ).click()
        self.admin.find(
            By.XPATH, '//div[@id="periods"]//a[text()="Add period"]').click()
        self.admin.find(
            By.ID, "period_name").send_keys("period test")
        self.admin.find(
            By.XPATH, '//input[@value="Save"]').click()
        # assert that that period was added
        self.admin.find(
            By.XPATH, '//div[@id="periods"]//td[text()="period test"]')
        # archive the period
        self.admin.find(
            By.XPATH,
            '//div[@id="periods"]//td[text()="period test"]' +
            '/..//a[text()="Archive"]'
        ).click()

        # Delete the course
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Courses')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="pagination"]//a[not(@rel)][last()]')
            )
        ).click()
        course = self.admin.find(
            By.XPATH,
            "//div[@class='stats-card']" +
            "//span[text()=' automated test course']")
        course.find_element(
            By.XPATH, '../..//a[text()="Delete"]'
        ).click()
        self.admin.sleep(0.5)
        self.admin.driver.switch_to_alert().accept()
        self.admin.sleep(0.5)
        self.ps.test_updates['passed'] = True

    # Case C8355 - 015 - Admin | Edit a period
    @pytest.mark.skipif(str(8355) not in TESTS, reason='Excluded')
    def test_admin_edit_a_period_8355(self):
        """Edit a period.

        Steps:
        Click Course Organization in the header
        Click on Courses
        Click Edit next to a course
        Click on the Periods tab
        Click Edit next to a period
        Enter a new information into the Name and enrollment code text boxes
        Click Save

        Expected Result:
        A period is edited
        """
        self.ps.test_updates['name'] = 't1.59.015' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.015', '8355']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Courses')
            )
        ).click()

        # Create the course
        self.admin.find(By.XPATH, "//a[text()='Add Course']").click()
        self.admin.find(By.XPATH, "//input[@id='course_name']").send_keys(
            "automated test course")
        self.admin.find(By.XPATH, "//input[@value='Save']").click()

        # Edit the course
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="pagination"]//a[not(@rel)][last()]')
            )
        ).click()
        course = self.admin.find(
            By.XPATH,
            "//div[@class='stats-card']" +
            "//span[text()=' automated test course']")
        course.find_element(
            By.XPATH, '../..//a[text()="Edit"]'
        ).click()
        # Add a period
        self.admin.find(
            By.XPATH, '//a[@role="tab" and @aria-controls="periods"]'
        ).click()
        self.admin.find(
            By.XPATH, '//div[@id="periods"]//a[text()="Add period"]').click()
        self.admin.find(
            By.ID, "period_name").send_keys("period test")
        self.admin.find(
            By.XPATH, '//input[@value="Save"]').click()
        # assert that that period was added
        self.admin.find(
            By.XPATH, '//div[@id="periods"]//td[text()="period test"]')
        # Edit the period
        self.admin.find(
            By.XPATH,
            '//div[@id="periods"]//td[text()="period test"]' +
            '/..//a[text()="Edit"]'
        ).click()
        self.admin.find(
            By.ID, "period_name").send_keys(" edit")
        self.admin.find(
            By.XPATH, '//input[@value="Save"]').click()
        # assert that that period was edited
        self.admin.find(
            By.XPATH, '//div[@id="periods"]//td[text()="period test edit"]')
        # archive the period
        self.admin.find(
            By.XPATH,
            '//div[@id="periods"]//td[text()="period test edit"]' +
            '/..//a[text()="Archive"]'
        ).click()

        # Delete the course
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Courses')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="pagination"]//a[not(@rel)][last()]')
            )
        ).click()
        course = self.admin.find(
            By.XPATH,
            "//div[@class='stats-card']" +
            "//span[text()=' automated test course']")
        course.find_element(
            By.XPATH, '../..//a[text()="Delete"]'
        ).click()
        self.admin.sleep(0.5)
        self.admin.driver.switch_to_alert().accept()
        self.admin.sleep(0.5)
        self.ps.test_updates['passed'] = True

    # Case C8356 - 016 - Admin | Archive an empty period
    @pytest.mark.skipif(str(8356) not in TESTS, reason='Excluded')
    def test_admin_archive_an_empty_period_8356(self):
        """Archive an empty period.

        Steps:
        Click Course Organization in the header
        Click on Courses
        Click Edit next to a course
        Click on the Periods tab
        Click Edit next to a period
        Click Archive for an empty period

        Expected Result:
        A period is archived
        """
        self.ps.test_updates['name'] = 't1.59.016' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.016', '8356']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Courses')
            )
        ).click()

        # Create the course
        self.admin.find(By.XPATH, "//a[text()='Add Course']").click()
        self.admin.find(By.XPATH, "//input[@id='course_name']").send_keys(
            "automated test course")
        self.admin.find(By.XPATH, "//input[@value='Save']").click()

        # Edit the course
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="pagination"]//a[not(@rel)][last()]')
            )
        ).click()
        course = self.admin.find(
            By.XPATH,
            "//div[@class='stats-card']" +
            "//span[text()=' automated test course']")
        course.find_element(
            By.XPATH, '../..//a[text()="Edit"]'
        ).click()
        # Add a period
        self.admin.find(
            By.XPATH, '//a[@role="tab" and @aria-controls="periods"]'
        ).click()
        self.admin.find(
            By.XPATH, '//div[@id="periods"]//a[text()="Add period"]').click()
        self.admin.find(
            By.ID, "period_name").send_keys("period test")
        self.admin.find(
            By.XPATH, '//input[@value="Save"]').click()
        # assert that that period was added
        self.admin.find(
            By.XPATH, '//div[@id="periods"]//td[text()="period test"]')
        # archive the period
        self.admin.find(
            By.XPATH,
            '//div[@id="periods"]//td[text()="period test"]' +
            '/..//a[text()="Archive"]'
        ).click()

        # Delete the course
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Courses')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="pagination"]//a[not(@rel)][last()]')
            )
        ).click()
        course = self.admin.find(
            By.XPATH,
            "//div[@class='stats-card']" +
            "//span[text()=' automated test course']")
        course.find_element(
            By.XPATH, '../..//a[text()="Delete"]'
        ).click()
        self.admin.sleep(0.5)
        self.admin.driver.switch_to_alert().accept()
        self.admin.sleep(0.5)
        self.ps.test_updates['passed'] = True

    # Case C8357 - 017 - Admin | Archive an non-empty period
    @pytest.mark.skipif(str(8357) not in TESTS, reason='Excluded')
    def test_admin_archive_a_non_empty_period_8357(self):
        """Archive a non-empty period.

        Steps:
        Click Course Organization in the header
        Click on Courses
        Click Edit next to a course
        Click on the Periods tab
        Click Edit next to a period
        Click Delete for a non-empty period

        Expected Result:
        A red text box that says 'Students must be moved to another
        period before this period can be deleted' pops up, and the
        period cannot be deleted
        """
        self.ps.test_updates['name'] = 't1.59.017' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.017', '8357']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        course_name = "automated test course%d" % randint(1000, 1999)
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Courses')
            )
        ).click()

        # Create the course
        self.admin.find(By.XPATH, "//a[text()='Add Course']").click()
        self.admin.find(By.XPATH, "//input[@id='course_name']").send_keys(
            course_name)
        self.admin.find(By.XPATH, "//input[@value='Save']").click()

        # Edit the course
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="pagination"]//a[not(@rel)][last()]')
            )
        ).click()
        course = self.admin.find(
            By.XPATH,
            "//div[@class='stats-card']" +
            "//span[text()=' %s']" % course_name)
        course.find_element(
            By.XPATH, '../..//a[text()="Edit"]'
        ).click()
        # Add a period
        self.admin.find(
            By.XPATH, '//a[@role="tab" and @aria-controls="periods"]'
        ).click()
        self.admin.find(
            By.XPATH, '//div[@id="periods"]//a[text()="Add period"]').click()
        self.admin.find(
            By.ID, "period_name").send_keys("period test")
        self.admin.find(
            By.XPATH, '//input[@value="Save"]').click()
        # Create a file to upload to roster
        roster_file = open(os.getenv("HOME") + "/roster.csv", "w")
        roster_file.seek(0)
        roster_file.truncate()
        roster_file.write(
            "first_name,last_name,username,password\n" +
            "Charles,Mayfare,s_01,password")
        roster_file.close()
        # upload the file to the roster
        self.admin.find(
            By.XPATH, '//a[@role="tab" and @aria-controls="roster"]'
        ).click()
        self.admin.find(
            By.ID, 'student_roster'
        ).send_keys(os.getenv("HOME") + "/roster.csv")
        self.admin.find(
            By.XPATH, '//input[@value="Upload"]').click()

        # archive the period, and delete the teacher
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Courses')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="pagination"]//a[not(@rel)][last()]')
            )
        ).click()
        course = self.admin.find(
            By.XPATH,
            "//div[@class='stats-card']" +
            "//span[text()=' %s']" % course_name)
        course.find_element(
            By.XPATH, '../..//a[text()="Edit"]'
        ).click()
        self.admin.find(
            By.XPATH, '//a[@role="tab" and @aria-controls="periods"]'
        ).click()
        self.admin.find(
            By.XPATH,
            '//div[@id="periods"]//td[text()="period test"]' +
            '/..//a[text()="Archive"]'
        ).click()
        self.ps.test_updates['passed'] = True

    # Case C8358 - 018 - Admin | Upload a student roster to a period
    @pytest.mark.skipif(str(8358) not in TESTS, reason='Excluded')
    def test_admin_upload_a_student_roster_to_a_period_8358(self):
        """Upload a student roster to a period.

        Steps:
        Click Course Organization in the header
        Click on Courses
        Click Edit next to a course
        Click on the Student Roster tab
        Select a period
        Click the Choose File button
        Select a file
        Click Upload

        Expected Result:
        A student roster is uploaded, confirmation message displayed
        """
        self.ps.test_updates['name'] = 't1.59.018' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.018', '8358']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        course_name = "automated test course%d" % randint(100, 999)
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Courses')
            )
        ).click()

        # Create the course
        self.admin.find(By.XPATH, "//a[text()='Add Course']").click()
        self.admin.find(By.XPATH, "//input[@id='course_name']").send_keys(
            course_name)
        self.admin.find(By.XPATH, "//input[@value='Save']").click()

        # Edit the course
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="pagination"]//a[not(@rel)][last()]')
            )
        ).click()
        course = self.admin.find(
            By.XPATH,
            "//div[@class='stats-card']" +
            "//span[text()=' %s']" % course_name)
        course.find_element(
            By.XPATH, '../..//a[text()="Edit"]'
        ).click()
        # Add a period
        self.admin.find(
            By.XPATH, '//a[@role="tab" and @aria-controls="periods"]'
        ).click()
        self.admin.find(
            By.XPATH, '//div[@id="periods"]//a[text()="Add period"]').click()
        self.admin.find(
            By.ID, "period_name").send_keys("period test")
        self.admin.find(
            By.XPATH, '//input[@value="Save"]').click()
        # Create a file to upload to roster
        roster_file = open(os.getenv("HOME") + "/roster.csv", "w")
        roster_file.seek(0)
        roster_file.truncate()
        roster_file.write(
            "first_name,last_name,username,password\n" +
            "Charles,Mayfare,s_01,password")
        roster_file.close()
        # upload the file to the roster
        self.admin.find(
            By.XPATH, '//a[@role="tab" and @aria-controls="roster"]'
        ).click()
        self.admin.find(
            By.ID, 'student_roster'
        ).send_keys(os.getenv("HOME") + "/roster.csv")
        self.admin.find(
            By.XPATH, '//input[@value="Upload"]').click()
        # add a teacher to the course
        self.admin.find(
            By.XPATH, '//a[@role="tab" and @aria-controls="teachers"]'
        ).click()
        self.admin.find(
            By.ID, 'course_teacher').send_keys("teacher01")
        self.admin.sleep(1)
        self.admin.find(
            By.ID, 'course_teacher').send_keys(Keys.RETURN)

        # login as that teacher and check that the student has been added
        self.admin.find(
            By.XPATH, '//a[@class="dropdown-toggle" and text()="admin "]'
        ).click()
        self.admin.find(By.LINK_TEXT, 'Sign out!').click()
        self.admin.login(username="teacher01")
        self.admin.sleep(3)
        self.admin.find(
            By.XPATH, '//div[@data-title="' + course_name + '"]'
        ).click()
        self.admin.open_user_menu()
        self.admin.sleep(0.5)
        self.admin.find(
            By.LINK_TEXT, 'Course Settings and Roster'
        ).click()
        self.admin.find(
            By.XPATH,
            '//table//td[text()="Charles"]/../td[text()="Mayfare"]' +
            '/..//a[@aria-describedby="drop-student"]'
        ).click()
        self.admin.find(
            By.XPATH, '//div[@id="drop-student"]//button'
        ).click()
        self.admin.logout()
        self.admin.login()

        # archive the period, and delete the teacher
        self.admin.goto_admin_control()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Courses')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="pagination"]//a[not(@rel)][last()]')
            )
        ).click()
        course = self.admin.find(
            By.XPATH,
            "//div[@class='stats-card']" +
            "//span[text()=' %s']" % course_name)
        course.find_element(
            By.XPATH, '../..//a[text()="Edit"]'
        ).click()
        self.admin.find(
            By.XPATH, '//a[@role="tab" and @aria-controls="periods"]'
        ).click()
        self.admin.find(
            By.XPATH,
            '//div[@id="periods"]//td[text()="period test"]' +
            '/..//a[text()="Archive"]'
        ).click()
        self.admin.find(
            By.XPATH, '//a[@role="tab" and @aria-controls="teachers"]'
        ).click()
        self.admin.find(
            By.XPATH, '//a[text()="Remove from course"]').click()
        self.admin.sleep(0.5)
        self.admin.driver.switch_to_alert().accept()
        self.admin.sleep(0.5)
        self.ps.test_updates['passed'] = True

    # Case C8359 - 019 - Admin | Bulk update course ecosystems
    @pytest.mark.skipif(str(8359) not in TESTS, reason='Excluded')
    def test_admin_bulk_update_course_ecosystems_8359(self):
        """Bulk update course ecosystems.

        Steps:
        Click Course Organization in the header
        Click on Courses
        Check the checkboxes for selected courses
        Scroll to the bottom of the page
        Select an ecosystem
        Click Set ecosystem

        Expected Result:
        The message 'Course ecosystem update background jobs queued'
        is displayed
        """
        self.ps.test_updates['name'] = 't1.59.019' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.019', '8359']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        course_name = "automated test course%d" % randint(100, 999)
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Courses')
            )
        ).click()

        # Create the course
        self.admin.find(By.XPATH, "//a[text()='Add Course']").click()
        self.admin.find(By.XPATH, "//input[@id='course_name']").send_keys(
            course_name)
        self.admin.find(By.XPATH, "//input[@value='Save']").click()

        # Uncheck the select all box if it is selected
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="pagination"]//a[not(@rel)][last()]')
            )
        ).click()
        self.admin.find(By.ID, "courses_select_all").click()
        course = self.admin.find(
            By.XPATH,
            "//div[@class='stats-card']" +
            "//span[text()=' %s']" % course_name)
        course.find_element(
            By.XPATH, '../input[@type="checkbox"]'
        ).click()

        # Choose the ecosystem to use for the course, update the course
        self.admin.find(By.ID, "ecosystem_id").click()
        self.admin.find(
            By.XPATH, "//select[@id='ecosystem_id']/option[2]"
        ).click()
        self.admin.find(By.XPATH, "//input[@value='Set Ecosystem']").click()

        # Delete the course
        self.admin.page.wait_for_page_load()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="pagination"]//a[not(@rel)][last()]')
            )
        ).click()
        course = self.admin.find(
            By.XPATH,
            "//div[@class='stats-card']" +
            "//span[text()=' " + course_name + "']")
        course.find_element(
            By.XPATH, '../..//a[text()="Delete"]'
        ).click()
        self.admin.sleep(0.5)
        self.admin.driver.switch_to_alert().accept()
        self.admin.sleep(0.5)
        self.ps.test_updates['passed'] = True

    # Case C8360 - 020 - Admin | View the Tutor course counts
    @pytest.mark.skipif(str(8360) not in TESTS, reason='Excluded')
    def test_admin_view_the_tutor_course_counts_8360(self):
        """View the Tutor course counts.

        Steps:
        Click Stats in the header
        Click on Courses

        Expected Result:
        """
        self.ps.test_updates['name'] = 't1.59.020' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.020', '8360']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Stats')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Courses')
            )
        ).click()
        assert('stats/courses' in self.admin.current_url()), \
            'Not on stats page'

        self.ps.test_updates['passed'] = True

    # Case C100135 - 021 - Admin | Set the course scholastic year
    @pytest.mark.skipif(str(100135) not in TESTS, reason='Excluded')
    def test_admin_set_the_course_scholastic_year_100135(self):
        """Set the course scholastic year.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 't1.59.021' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.021', '100135']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Courses')
            )
        ).click()

        # Create the course
        self.admin.find(By.XPATH, "//a[text()='Add Course']").click()
        self.admin.find(
            By.ID, "course_year"
        ).send_keys((Keys.DELETE * 4) + str(datetime.date.today().year))

        self.ps.test_updates['passed'] = True

    # Case C100136 - 022 - Admin | Set the number of sections
    @pytest.mark.skipif(str(100136) not in TESTS, reason='Excluded')
    def test_admin_set_the_number_of_sections_100136(self):
        """Set the number of sections.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 't1.59.022' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.022', '100136']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Courses')
            )
        ).click()

        # Create the course
        self.admin.find(By.XPATH, "//a[text()='Add Course']").click()
        self.admin.find(
            By.ID, "course_num_sections"
        ).send_keys((Keys.DELETE) + str(1))

        self.ps.test_updates['passed'] = True

    # Case C100137 - 023 - Admin | Set the course start date and time
    @pytest.mark.skipif(str(100137) not in TESTS, reason='Excluded')
    def test_admin_set_the_course_start_date_and_time_100137(self):
        """Set the course start date and time.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 't1.59.023' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.023', '100137']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Courses')
            )
        ).click()

        # Choose start date and time
        today = datetime.date.today()
        self.admin.find(By.XPATH, "//a[text()='Add Course']").click()
        self.admin.find(By.ID, "course_starts_at").click()
        self.admin.sleep(1)
        self.admin.find(
            By.XPATH,
            '//div[contains(@class,"datepicker")]' +
            '//button[contains(@class,"_next")]'
        ).click()
        self.admin.find(
            By.XPATH,
            '//div[contains(@class,"calendar")]' +
            '//td[@data-date="1" and @data-month="' +
            str(today.replace(month=today.month + 1).month) + '"]'
        ).click()
        # Choose end date
        self.admin.find(
            By.XPATH,
            '//div[contains(@class,"timepicker")]//div[@data-hour="17"]'
        ).click()

        self.ps.test_updates['passed'] = True

    # Case C100138 - 024 - Admin | Set the course end date and time
    @pytest.mark.skipif(str(100138) not in TESTS, reason='Excluded')
    def test_admin_set_the_course_end_date_and_time_100138(self):
        """Set the course end date and time.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 't1.59.024' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.024', '100138']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Courses')
            )
        ).click()

        # Choose end date and time
        today = datetime.date.today()
        self.admin.find(By.XPATH, "//a[text()='Add Course']").click()
        self.admin.find(By.ID, "course_ends_at").click()
        self.admin.sleep(1)
        self.admin.find(
            By.XPATH,
            '//div[contains(@class,"datepicker")]' +
            '//button[contains(@class,"_next")]'
        ).click()
        self.admin.find(
            By.XPATH,
            '//div[contains(@class,"calendar")]' +
            '//td[@data-date="1" and @data-month="' +
            str(today.replace(month=today.month + 1).month) + '"]'
        ).click()
        # Choose end date
        self.admin.find(
            By.XPATH,
            '//div[contains(@class,"timepicker")]//div[@data-hour="17"]'
        ).click()

        self.ps.test_updates['passed'] = True

    # Case C100139 - 025 - Admin | Set the course offering
    @pytest.mark.skipif(str(100139) not in TESTS, reason='Excluded')
    def test_admin_set_the_course_offering_100139(self):
        """Set the course offering.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 't1.59.025' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.025', '100139']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Courses')
            )
        ).click()

        # Set the course offering
        self.admin.find(By.XPATH, "//a[text()='Add Course']").click()
        self.admin.find(By.ID, "course_catalog_offering_id").click()
        self.admin.find(
            By.XPATH,
            '//select[@id="course_catalog_offering_id"]/option[2]'
        ).click()

        self.ps.test_updates['passed'] = True

    # Case C100140 - 026 - Admin | Set the course appearance code
    @pytest.mark.skipif(str(100140) not in TESTS, reason='Excluded')
    def test_admin_set_the_course_appearance_code_100140(self):
        """Set the course appearance code.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 't1.59.026' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.59', 't1.59.026', '100140']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Courses')
            )
        ).click()

        # Set the course appearance code
        self.admin.find(By.XPATH, "//a[text()='Add Course']").click()
        self.admin.find(By.ID, "course_appearance_code").click()
        self.admin.find(
            By.XPATH,
            '//select[@id="course_appearance_code"]/option[2]'
        ).click()

        self.ps.test_updates['passed'] = True
