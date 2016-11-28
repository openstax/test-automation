"""Tutor v1, Epic 59 - ManageDistricsSchoolsAndCourses."""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
# from random import randint
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
        8356, 8357, 8358, 8359, 8360
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
        self.admin = Admin(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        self.admin.login()
        self.admin.goto_admin_control()
        self.admin.sleep(5)

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

        self.admin.find(By.XPATH, "//a[@class='btn btn-primary']").click()
        self.admin.find(By.XPATH, "//input[@id='district_name']").send_keys(
            'automated test')
        self.admin.find(
            By.XPATH, "//form/input[@class='btn btn-primary']").click()

        # Delete the district
        districts = self.admin.driver.find_elements_by_xpath("//tr")
        for index, district in enumerate(districts):
            if district.text.find('automated test edit') >= 0:
                self.admin.sleep(2)
                self.admin.driver.find_elements_by_partial_link_text(
                    'delete')[index - 1].click()
                self.admin.sleep(5)
                self.admin.driver.switch_to_alert().accept()
                self.admin.sleep(2)
                self.ps.test_updates['passed'] = True
                break

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

        self.admin.find(By.XPATH, "//a[@class='btn btn-primary']").click()
        self.admin.find(By.XPATH, "//input[@id='district_name']").send_keys(
            'automated test')
        self.admin.find(
            By.XPATH, "//form/input[@class='btn btn-primary']").click()

        # Edit the district name
        districts = self.admin.driver.find_elements_by_xpath("//tr")
        for index, district in enumerate(districts):
            if district.text.find('automated test') >= 0:
                self.admin.sleep(2)
                self.admin.driver.find_elements_by_link_text(
                    'edit')[index - 1].click()
                self.admin.sleep(5)
                self.admin.find(
                    By.XPATH, "//input[@id='school_name']").send_keys(' edit')
                self.admin.find(
                    By.XPATH, "//input[@class='btn btn-primary']").click()
                self.admin.sleep(5)
                break

        # Delete the district
        districts = self.admin.driver.find_elements_by_xpath("//tr")
        for index, district in enumerate(districts):
            if district.text.find('automated test edit') >= 0:
                self.admin.sleep(2)
                self.admin.driver.find_elements_by_partial_link_text(
                    'delete')[index - 1].click()
                self.admin.sleep(5)
                self.admin.driver.switch_to_alert().accept()
                self.admin.sleep(2)
                self.ps.test_updates['passed'] = True
                break

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

        self.admin.find(By.XPATH, "//a[@class='btn btn-primary']").click()
        self.admin.find(By.XPATH, "//input[@id='district_name']").send_keys(
            'automated test')
        self.admin.find(
            By.XPATH, "//form/input[@class='btn btn-primary']").click()

        # Delete the district
        districts = self.admin.driver.find_elements_by_xpath("//tr")
        for index, district in enumerate(districts):
            if district.text.find('automated test edit') >= 0:
                self.admin.sleep(2)
                self.admin.driver.find_elements_by_partial_link_text(
                    'delete')[index - 1].click()
                self.admin.sleep(5)
                self.admin.driver.switch_to_alert().accept()
                self.admin.sleep(2)
                self.ps.test_updates['passed'] = True
                break

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

        self.admin.find(By.XPATH, "//a[@class='btn btn-primary']").click()
        self.admin.find(By.XPATH, "//input[@id='school_name']").send_keys(
            'automated test')
        self.admin.find(By.XPATH, "//input[@class='btn btn-primary']").click()

        # Delete the school
        schools = self.admin.driver.find_elements_by_xpath("//tr")
        for index, school in enumerate(schools):
            if school.text.find('automated test') >= 0:
                self.admin.sleep(2)
                self.admin.driver.find_elements_by_partial_link_text(
                    'delete')[index - 1].click()
                self.admin.sleep(5)
                self.admin.driver.switch_to_alert().accept()
                self.admin.sleep(2)
                self.ps.test_updates['passed'] = True
                break

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

        self.admin.find(By.XPATH, "//a[@class='btn btn-primary']").click()
        self.admin.find(
            By.XPATH,
            "//input[@id='school_name']"
        ).send_keys('automated test')
        self.admin.find(By.XPATH, "//input[@class='btn btn-primary']").click()

        # Edit the school's name
        schools = self.admin.driver.find_elements_by_xpath("//tr")
        for index, school in enumerate(schools):
            if school.text.find('automated test') >= 0:
                self.admin.sleep(2)
                self.admin.driver.find_elements_by_link_text(
                    'edit')[index - 1].click()
                self.admin.sleep(5)
                self.admin.find(
                    By.XPATH, "//input[@id='school_name']").send_keys(' edit')
                self.admin.find(
                    By.XPATH, "//input[@class='btn btn-primary']").click()
                self.admin.sleep(5)
                break

        # Delete the school
        schools = self.admin.driver.find_elements_by_xpath("//tr")
        for index, school in enumerate(schools):
            if school.text.find('automated test edit') >= 0:
                self.admin.sleep(2)
                self.admin.driver.find_elements_by_partial_link_text(
                    'delete')[index - 1].click()
                self.admin.sleep(5)
                self.admin.driver.switch_to_alert().accept()
                self.admin.sleep(2)
                self.ps.test_updates['passed'] = True
                break

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

        self.admin.find(By.XPATH, "//a[@class='btn btn-primary']").click()
        self.admin.find(By.XPATH, "//input[@id='school_name']").send_keys(
            'automated test')
        self.admin.find(By.XPATH, "//input[@class='btn btn-primary']").click()

        # Edit the school's district
        schools = self.admin.driver.find_elements_by_xpath("//tr")
        for index, school in enumerate(schools):
            if school.text.find('automated test') >= 0:
                self.admin.sleep(2)
                self.admin.driver.find_elements_by_link_text(
                    'edit')[index - 1].click()
                self.admin.sleep(5)
                self.admin.find(
                    By.XPATH,
                    "//select[@id='school_school_district_district_id']"
                ).send_keys("OpenStax")
                self.admin.find(
                    By.XPATH, "//input[@class='btn btn-primary']").click()
                self.admin.sleep(5)
                break

        # Delete the school
        schools = self.admin.driver.find_elements_by_xpath("//tr")
        for index, school in enumerate(schools):
            if school.text.find('automated test') >= 0:
                self.admin.sleep(2)
                self.admin.driver.find_elements_by_partial_link_text(
                    'delete')[index - 1].click()
                self.admin.sleep(5)
                self.admin.driver.switch_to_alert().accept()
                self.admin.sleep(2)
                self.ps.test_updates['passed'] = True
                break

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
        self.admin.find(By.XPATH, "//a[@class='btn btn-primary']").click()
        self.admin.find(
            By.XPATH,
            "//input[@id='school_name']"
        ).send_keys('automated test')
        self.admin.find(By.XPATH, "//input[@class='btn btn-primary']").click()

        # Delete the school
        schools = self.admin.driver.find_elements_by_xpath("//tr")
        for index, school in enumerate(schools):
            if school.text.find('automated test') >= 0:
                self.admin.sleep(2)
                self.admin.driver.find_elements_by_partial_link_text(
                    'delete')[index - 1].click()
                self.admin.sleep(5)
                self.admin.driver.switch_to_alert().accept()
                self.admin.sleep(2)
                self.ps.test_updates['passed'] = True
                break

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

        self.admin.sleep(2)

        # Create the course
        self.admin.find(By.XPATH, "//a[@class='btn btn-primary']").click()
        self.admin.find(By.XPATH, "//input[@id='course_name']").send_keys(
            "automated test")
        self.admin.find(
            By.XPATH,
            "//select[@id='course_school_district_school_id']"
        ).send_keys("Denver University")
        self.admin.find(
            By.XPATH,
            "//select[@id='course_catalog_offering_id']").send_keys("Calculus")
        self.admin.find(By.XPATH, "//input[@class='btn btn-primary']").click()

        # Delete the course
        delete = 0
        courses = self.admin.driver.find_elements_by_xpath("//tr")
        for course in courses:
            if course.text.find('automated test') >= 0:
                self.admin.sleep(2)
                self.admin.driver.find_elements_by_link_text(
                    'Delete')[delete].click()
                self.admin.sleep(12)
                self.admin.driver.switch_to_alert().accept()
                self.admin.sleep(5)
                self.ps.test_updates['passed'] = True
                break

            else:
                if course.text.find('Delete') >= 0:
                    delete += 1

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

        self.admin.sleep(2)

        # Create the course
        self.admin.find(By.XPATH, "//a[@class='btn btn-primary']").click()
        self.admin.find(By.XPATH, "//input[@id='course_name']").send_keys(
            "automated test")
        self.admin.find(
            By.XPATH,
            "//select[@id='course_school_district_school_id']").send_keys(
            "Denver University")
        self.admin.find(
            By.XPATH,
            "//select[@id='course_catalog_offering_id']").send_keys("Calculus")
        self.admin.find(By.XPATH, "//input[@class='btn btn-primary']").click()

        # Edit the course
        schools = self.admin.driver.find_elements_by_xpath("//tr")
        for index, school in enumerate(schools):
            if school.text.find('automated test') >= 0:
                self.admin.sleep(2)
                self.admin.driver.find_elements_by_link_text(
                    'Edit')[index - 1].click()
                self.admin.sleep(5)
                self.admin.find(
                    By.XPATH, "//input[@id='course_name']").send_keys(' edit')
                self.admin.find(
                    By.XPATH,
                    "//select[@id='course_school_district_school_id']"
                ).send_keys("OpenStax Ed")
                self.admin.find(
                    By.XPATH,
                    "//select[@id='course_catalog_offering_id']").send_keys(
                    "CC Biology")
                self.admin.find(
                    By.XPATH, "//input[@class='btn btn-primary']").click()
                self.admin.sleep(5)
                break

        # Delete the course
        delete = 0
        courses = self.admin.driver.find_elements_by_xpath("//tr")
        for course in courses:
            if course.text.find('automated test edit') >= 0:
                self.admin.sleep(2)
                self.admin.driver.find_elements_by_link_text(
                    'Delete')[delete].click()
                self.admin.sleep(5)
                self.admin.driver.switch_to_alert().accept()
                self.admin.sleep(10)
                self.ps.test_updates['passed'] = True
                break

            else:
                if course.text.find('Delete') >= 0:
                    delete += 1

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

        self.admin.sleep(2)

        # Create the course
        self.admin.find(By.XPATH, "//a[@class='btn btn-primary']").click()
        self.admin.find(By.XPATH, "//input[@id='course_name']").send_keys(
            "automated test")
        self.admin.find(
            By.XPATH,
            "//select[@id='course_school_district_school_id']").send_keys(
            "Denver University")
        self.admin.find(
            By.XPATH, "//select[@id='course_catalog_offering_id']").send_keys(
            "Calculus")
        self.admin.find(By.XPATH, "//input[@class='btn btn-primary']").click()

        # Edit the course
        schools = self.admin.driver.find_elements_by_xpath("//tr")
        for index, school in enumerate(schools):
            if school.text.find('automated test') >= 0:
                self.admin.sleep(2)
                self.admin.driver.find_elements_by_link_text(
                    'Edit')[index - 1].click()
                self.admin.sleep(5)
                self.admin.find(By.PARTIAL_LINK_TEXT, "Teachers").click()
                self.admin.find(
                    By.XPATH, "//input[@id='course_teacher']").send_keys(
                    'teacher01')
                self.admin.sleep(5)
                self.admin.find(
                    By.XPATH,
                    "//input[@id='course_teacher']").send_keys(
                    Keys.RETURN)
                self.admin.find(
                    By.PARTIAL_LINK_TEXT, "Remove from course").click()
                self.admin.driver.switch_to_alert().accept()
                self.admin.sleep(2)
                self.admin.find(By.PARTIAL_LINK_TEXT, "Edit course").click()
                self.admin.find(
                    By.XPATH, "//input[@class='btn btn-primary']").click()
                self.admin.sleep(5)
                break

        # Delete the course
        delete = 0
        courses = self.admin.driver.find_elements_by_xpath("//tr")
        for course in courses:
            if course.text.find('automated test') >= 0:
                self.admin.sleep(2)
                self.admin.driver.find_elements_by_link_text(
                    'Delete')[delete].click()
                self.admin.sleep(5)
                self.admin.driver.switch_to_alert().accept()
                self.admin.sleep(10)
                self.ps.test_updates['passed'] = True
                break

            else:
                if course.text.find('Delete') >= 0:
                    delete += 1

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

        self.admin.sleep(2)

        # Create the course
        self.admin.find(By.XPATH, "//a[@class='btn btn-primary']").click()
        self.admin.find(By.XPATH, "//input[@id='course_name']").send_keys(
            "automated test")
        self.admin.find(
            By.XPATH,
            "//select[@id='course_school_district_school_id']").send_keys(
            "Denver University")
        self.admin.find(
            By.XPATH, "//select[@id='course_catalog_offering_id']").send_keys(
            "Calculus")
        self.admin.find(By.XPATH, "//input[@class='btn btn-primary']").click()

        # Edit the course
        schools = self.admin.driver.find_elements_by_xpath("//tr")
        for index, school in enumerate(schools):
            if school.text.find('automated test') >= 0:
                self.admin.sleep(2)
                self.admin.driver.find_elements_by_link_text(
                    'Edit')[index - 1].click()
                self.admin.sleep(5)
                self.admin.find(By.PARTIAL_LINK_TEXT, "Teachers").click()
                self.admin.find(
                    By.XPATH, "//input[@id='course_teacher']").send_keys(
                    'teacher01')
                self.admin.sleep(5)
                self.admin.find(
                    By.XPATH, "//input[@id='course_teacher']").send_keys(
                    Keys.RETURN)

                # Remove teacher01 as instructor
                self.admin.find(
                    By.PARTIAL_LINK_TEXT, "Remove from course").click()
                self.admin.driver.switch_to_alert().accept()
                self.admin.sleep(2)
                self.admin.find(By.PARTIAL_LINK_TEXT, "Edit course").click()
                self.admin.find(
                    By.XPATH, "//input[@class='btn btn-primary']").click()
                self.admin.sleep(5)
                break

        # Delete the course
        delete = 0
        courses = self.admin.driver.find_elements_by_xpath("//tr")
        for course in courses:
            if course.text.find('automated test') >= 0:
                self.admin.sleep(2)
                self.admin.driver.find_elements_by_link_text(
                    'Delete')[delete].click()
                self.admin.sleep(5)
                self.admin.driver.switch_to_alert().accept()
                self.admin.sleep(10)
                self.ps.test_updates['passed'] = True
                break

            else:
                if course.text.find('Delete') >= 0:
                    delete += 1

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

        self.admin.sleep(2)

        # Create the course
        self.admin.find(By.XPATH, "//a[@class='btn btn-primary']").click()
        self.admin.find(By.XPATH, "//input[@id='course_name']").send_keys(
            "automated test")
        self.admin.find(
            By.XPATH,
            "//select[@id='course_school_district_school_id']").send_keys(
            "Denver University")
        self.admin.find(
            By.XPATH, "//select[@id='course_catalog_offering_id']").send_keys(
            "Calculus")
        self.admin.find(By.XPATH, "//input[@class='btn btn-primary']").click()

        # Delete the course
        delete = 0
        courses = self.admin.driver.find_elements_by_xpath("//tr")
        for course in courses:
            if course.text.find('automated test') >= 0:
                self.admin.sleep(2)
                self.admin.driver.find_elements_by_link_text(
                    'Delete')[delete].click()
                self.admin.sleep(12)
                self.admin.driver.switch_to_alert().accept()
                self.admin.sleep(5)
                self.ps.test_updates['passed'] = True
                break

            else:
                if course.text.find('Delete') >= 0:
                    delete += 1

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

        self.admin.sleep(2)

        # Create the course
        self.admin.find(By.XPATH, "//a[@class='btn btn-primary']").click()
        self.admin.find(By.XPATH, "//input[@id='course_name']").send_keys(
            "automated test")
        self.admin.find(
            By.XPATH,
            "//select[@id='course_school_district_school_id']").send_keys(
            "Denver University")
        self.admin.find(
            By.XPATH, "//select[@id='course_catalog_offering_id']").send_keys(
            "Calculus")
        self.admin.find(By.XPATH, "//input[@class='btn btn-primary']").click()

        # Edit the course
        schools = self.admin.driver.find_elements_by_xpath("//tr")
        for index, school in enumerate(schools):
            if school.text.find('automated test') >= 0:
                self.admin.sleep(2)
                self.admin.driver.find_elements_by_link_text(
                    'Edit')[index - 1].click()
                self.admin.sleep(5)
                self.admin.find(
                    By.XPATH, "//input[@id='course_name']").send_keys(' edit')
                self.admin.find(
                    By.XPATH,
                    "//select[@id='course_school_district_school_id']"
                ).send_keys("OpenStax Ed")
                self.admin.find(
                    By.XPATH,
                    "//select[@id='course_catalog_offering_id']").send_keys(
                    "CC Biology")
                self.admin.find(
                    By.XPATH, "//input[@class='btn btn-primary']").click()
                self.admin.sleep(5)
                break

        # Delete the course
        delete = 0
        courses = self.admin.driver.find_elements_by_xpath("//tr")
        for course in courses:
            if course.text.find('automated test edit') >= 0:
                self.admin.sleep(2)
                self.admin.driver.find_elements_by_link_text(
                    'Delete')[delete].click()
                self.admin.sleep(5)
                self.admin.driver.switch_to_alert().accept()
                self.admin.sleep(10)
                self.ps.test_updates['passed'] = True
                break
            else:
                if course.text.find('Delete') >= 0:
                    delete += 1

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

        self.admin.sleep(2)

        # Add a period
        schools = self.admin.driver.find_elements_by_xpath("//tr")
        for index, school in enumerate(schools):
            if school.text.find('automated test period') >= 0:
                self.admin.sleep(2)
                self.admin.driver.find_elements_by_link_text(
                    'Edit')[index - 1].click()
                self.admin.sleep(5)
                self.admin.find(By.PARTIAL_LINK_TEXT, "Periods").click()
                self.admin.find(
                    By.XPATH, "//a[@class='btn btn-primary']").click()
                self.admin.sleep(2)
                self.admin.find(
                    By.XPATH, "//input[@id='period_name']").send_keys('1')
                self.admin.find(
                    By.XPATH, "//input[@class='btn btn-primary']").click()
                self.admin.sleep(2)
                self.admin.find(
                    By.XPATH,
                    "//a[@class='btn btn-xs btn-primary'][2]").click()
                self.admin.sleep(2)
                self.admin.find(By.PARTIAL_LINK_TEXT, "Edit course").click()
                self.admin.find(
                    By.XPATH, "//input[@class='btn btn-primary']").click()
                self.admin.sleep(5)
                break

        assert('courses' in self.admin.current_url()), 'Not on courses page'

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

        self.admin.sleep(2)

        # Add a period
        schools = self.admin.driver.find_elements_by_xpath("//tr")
        for index, school in enumerate(schools):
            if school.text.find('automated test period') >= 0:
                self.admin.sleep(2)
                self.admin.driver.find_elements_by_link_text(
                    'Edit')[index - 1].click()
                self.admin.sleep(5)
                self.admin.find(By.PARTIAL_LINK_TEXT, "Periods").click()
                self.admin.find(
                    By.XPATH, "//a[@class='btn btn-primary']").click()
                self.admin.sleep(2)
                self.admin.find(
                    By.XPATH, "//input[@id='period_name']").send_keys('1')
                self.admin.find(
                    By.XPATH, "//input[@class='btn btn-primary']").click()
                self.admin.sleep(2)
                self.admin.find(
                    By.XPATH,
                    "//a[@class='btn btn-xs btn-primary'][1]").click()
                self.admin.sleep(2)

                # Edit the period
                self.admin.find(
                    By.XPATH, "//input[@id='period_name']").send_keys(' edit')
                self.admin.find(
                    By.XPATH, "//input[@class='btn btn-primary']").click()
                self.admin.sleep(2)
                self.admin.find(
                    By.XPATH,
                    "//a[@class='btn btn-xs btn-primary'][2]").click()
                self.admin.find(By.PARTIAL_LINK_TEXT, "Edit course").click()
                self.admin.find(
                    By.XPATH, "//input[@class='btn btn-primary']").click()
                self.admin.sleep(5)
                break

        assert('courses' in self.admin.current_url()), 'Not on courses page'

        self.ps.test_updates['passed'] = True

    # Case C8356 - 016 - Admin | Archive a period
    @pytest.mark.skipif(str(8356) not in TESTS, reason='Excluded')
    def test_admin_delete_an_empty_period_8356(self):
        """Delete an empty period.

        Steps:
        Click Course Organization in the header
        Click on Courses
        Click Edit next to a course
        Click on the Periods tab
        Click Edit next to a period
        Click Delete for an empty period

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

        self.admin.sleep(2)

        # Add a period
        schools = self.admin.driver.find_elements_by_xpath("//tr")
        for index, school in enumerate(schools):
            if school.text.find('automated test period') >= 0:
                self.admin.sleep(2)
                self.admin.driver.find_elements_by_link_text(
                    'Edit')[index - 1].click()
                self.admin.sleep(5)
                self.admin.find(By.PARTIAL_LINK_TEXT, "Periods").click()
                self.admin.find(
                    By.XPATH, "//a[@class='btn btn-primary']").click()
                self.admin.sleep(2)
                self.admin.find(
                    By.XPATH, "//input[@id='period_name']").send_keys('1')
                self.admin.find(
                    By.XPATH, "//input[@class='btn btn-primary']").click()
                self.admin.sleep(2)
                self.admin.find(
                    By.XPATH,
                    "//a[@class='btn btn-xs btn-primary'][2]").click()
                self.admin.sleep(2)
                self.admin.find(By.PARTIAL_LINK_TEXT, "Edit course").click()
                self.admin.find(
                    By.XPATH, "//input[@class='btn btn-primary']").click()
                self.admin.sleep(5)
                break

        assert('courses' in self.admin.current_url()), 'Not on courses page'

        self.ps.test_updates['passed'] = True

    # Case C8357 - 017 - Admin | Delete an non-empty period
    @pytest.mark.skipif(str(8357) not in TESTS, reason='Excluded')
    def test_admin_delete_a_non_empty_period_8357(self):
        """Delete a non-empty period.

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
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

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

        self.admin.sleep(2)

        # Add a period
        schools = self.admin.driver.find_elements_by_xpath("//tr")
        for index, school in enumerate(schools):
            if school.text.find('automated test period') >= 0:
                self.admin.sleep(2)
                self.admin.driver.find_elements_by_link_text(
                    'Edit')[index - 1].click()
                self.admin.sleep(5)
                self.admin.find(By.PARTIAL_LINK_TEXT, "Periods").click()
                self.admin.find(
                    By.XPATH, "//a[@class='btn btn-primary']").click()
                self.admin.sleep(2)
                self.admin.find(
                    By.XPATH, "//input[@id='period_name']").send_keys('1')
                self.admin.find(
                    By.XPATH, "//input[@class='btn btn-primary']").click()
                self.admin.sleep(2)

                self.admin.find(By.PARTIAL_LINK_TEXT, "Student Roster").click()
                self.admin.find(
                    By.XPATH, "//input[@id='student_roster']").send_keys(
                    '/Users/openstaxii/documents/roster.csv')
                self.admin.driver.find_elements_by_xpath(
                    "//input[@class='btn btn-primary']")[2].click()
                self.admin.sleep(3)

                page = self.admin.driver.page_source
                assert('Student roster has been uploaded.' in page), \
                    'Roster not uploaded'

                self.admin.find(By.PARTIAL_LINK_TEXT, "Periods").click()
                self.admin.find(
                    By.XPATH,
                    "//a[@class='btn btn-xs btn-primary'][2]").click()
                self.admin.sleep(2)
                self.admin.find(By.PARTIAL_LINK_TEXT, "Edit course").click()
                self.admin.find(
                    By.XPATH, "//input[@class='btn btn-primary']").click()
                self.admin.sleep(5)
                break

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

        # //input[contains(@id, 'course_id')]
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

        self.admin.sleep(2)

        # Create the course
        self.admin.find(By.XPATH, "//a[@class='btn btn-primary']").click()
        self.admin.find(By.XPATH, "//input[@id='course_name']").send_keys(
            "automated test")
        self.admin.find(
            By.XPATH,
            "//select[@id='course_school_district_school_id']"
        ).send_keys("Denver University")
        self.admin.find(
            By.XPATH,
            "//select[@id='course_catalog_offering_id']").send_keys("Calculus")
        self.admin.find(By.XPATH, "//input[@class='btn btn-primary']").click()

        # Uncheck the select all box if it is selected
        if self.admin.find(
                By.XPATH,
                "//input[@id='courses_select_all']"
        ).is_selected():
            self.admin.find(
                By.XPATH, "//input[@id='courses_select_all']").click()

        # Check the box of the newly created course
        delete = 0
        courses = self.admin.driver.find_elements_by_xpath("//tr")
        for course in courses:
            if course.text.find('automated test') >= 0:
                self.admin.sleep(2)
                num = self.admin.driver.find_elements_by_link_text(
                    'Delete')[delete].get_attribute('href')
                self.admin.sleep(5)
                break

            else:
                if course.text.find('Delete') >= 0:
                    delete += 1

        check = num.split('/')[-1]
        xpath = "//input[contains(@id, 'course_id_"
        xpath += check
        xpath += "')]"

        self.admin.find(By.XPATH, xpath).click()

        self.admin.sleep(5)

        # Choose the ecosystem to use for the course, update the course
        self.admin.find(By.XPATH, "//select[@id='ecosystem_id']").send_keys(
            '1')
        self.admin.driver.find_elements_by_xpath(
            "//input[@class='btn btn-primary']")[1].click()
        self.admin.sleep(5)

        page = self.admin.driver.page_source
        assert('Course ecosystem update background jobs queued.' in page), \
            'Ecosystem update not queued'

        # Delete the course
        delete = 0
        courses = self.admin.driver.find_elements_by_xpath("//tr")
        for course in courses:
            if course.text.find('automated test') >= 0:
                self.admin.sleep(2)
                self.admin.driver.find_elements_by_link_text(
                    'Delete')[delete].click()
                self.admin.sleep(12)
                self.admin.driver.switch_to_alert().accept()
                self.admin.sleep(5)
                self.ps.test_updates['passed'] = True
                break

            else:
                if course.text.find('Delete') >= 0:
                    delete += 1

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

        self.admin.sleep(2)

        assert('stats/courses' in self.admin.current_url()), \
            'Not on stats page'

        self.ps.test_updates['passed'] = True
