"""Concept Coach v1, Epic 10 - Admin and Teacher Course Setup."""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
# from staxing.assignment import Assignment
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Admin, Teacher

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': '50.0',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    # str([
    #     7715, 7716, 7717, 7718, 7719,
    #     7720, 7721, 7722, 58354, 7723,
    #     7724, 7725, 7726, 7727, 7728,
    #     7729, 7730, 7731
    # ])
    str([7729])
    # 7724, 7725, 7729, 7730 -- still need to do
    # 7715, 7716, 7717, 7731 -- not implemented on tutor
)


@PastaDecorator.on_platforms(BROWSERS)
class TestAdminAndTeacherCourseSetup(unittest.TestCase):
    """CC1.10 - Admin and Teacher Course Setup."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.teacher = Teacher(
            use_env_vars=True,
            # pasta_user=self.ps,
            # capabilities=self.desired_capabilities
        )
        self.admin = Admin(
            use_env_vars=True,
            existing_driver=self.teacher.driver,
            # pasta_user=self.ps,
            # capabilities=self.desired_capabilities

        )

    def tearDown(self):
        """Test destructor."""
        self.ps.update_job(
            job_id=str(self.teacher.driver.session_id),
            **self.ps.test_updates
        )
        try:
            self.admin.driver = None
            self.teacher.delete()
        except:
            pass

    # Case C7715 - 001 - Admin | Send course setup data from Sales Force
    @pytest.mark.skipif(str(7715) not in TESTS, reason='Excluded')
    def test_admin_send_course_setup_data_from_sales_force_7715(self):
        """Send course setup data from Sales Force.

        Steps:
        Go to tutor-staging.openstax.org and login as admin
        Click on the user menu
        Select the Admin option
        Click on Salesforce on the header

        Expected Result:
        """
        self.ps.test_updates['name'] = 'cc1.10.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.10',
            'cc1.10.001',
            '7715'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)
        #  ## maybe put in real code

        self.ps.test_updates['passed'] = True

    # Case C7716 - 002 - System | Course registration codes are emailed to the
    # teacher once the course is set up
    @pytest.mark.skipif(str(7716) not in TESTS, reason='Excluded')
    def test_system_registration_codes_are_emailed_to_teacher_7716(self):
        """Registration codes are emailed to teacher once the course is set up.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 'cc1.10.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.10',
            'cc1.10.002',
            '7716'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7717 - 003 - Teacher | Use a teacher registration code to access
    # their course
    @pytest.mark.skipif(str(7717) not in TESTS, reason='Excluded')
    def test_teacher_use_teacher_registration_code_to_access_course_7717(self):
        """Use a teacher registration code to access their course.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 'cc1.10.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.10',
            'cc1.10.003',
            '7717'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7718 - 004 - Teacher | Create course periods
    @pytest.mark.skipif(str(7718) not in TESTS, reason='Excluded')
    def test_teacher_create_course_periods_7718(self):
        """Create course periods.

        Steps:
        go to Tutor
        Log in as a teacher
        Click on a Concept Coach book
        Click on the user menu
        Select course roster
        Click "+ Add section"
        Enter a section name into the section Name text box

        Expected Result:
        New course section created
        """
        self.ps.test_updates['name'] = 'cc1.10.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.10',
            'cc1.10.004',
            '7718'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.driver.find_element(
            By.XPATH, '//a[contains(@href,"/cc-dashboard")]'
        ).click()
        self.teacher.page.wait_for_page_load()
        self.teacher.open_user_menu()
        self.teacher.driver.find_element(
            By.LINK_TEXT, 'Course Settings and Roster'
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"add-period")]//button')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[@class="modal-content"]//input[@type="text"]')
            )
        ).send_keys('test_period')
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[@class="modal-content"]//button/span[text()="Add"]'
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//li//a[@role="tab" and text()="test_period"]')
            )
        )
        self.ps.test_updates['passed'] = True

    # Case C7719 - 005 - Teacher | View student enrollment code for
    # course period
    @pytest.mark.skipif(str(7719) not in TESTS, reason='Excluded')
    def test_teacher_view_student_enrollment_code_for_course_period_7719(self):
        """View the student enrollment code for a course period.

        Steps:
        Go to Tutor
        Log in as a teacher
        Click on a Concept Coach book
        Click on the user menu
        Select course roster
        Click on tab for selected section
        Click 'Get Student Enrollment Code'

        Expected Result:
        Student Enrollment code displayed along with instruction teacher can
        send to students on how to use enrollment code
        """
        self.ps.test_updates['name'] = 'cc1.10.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.10',
            'cc1.10.005',
            '7719'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.driver.find_element(
            By.XPATH, '//a[contains(@href,"/cc-dashboard")]'
        ).click()
        self.teacher.page.wait_for_page_load()
        self.teacher.open_user_menu()
        self.teacher.driver.find_element(
            By.LINK_TEXT, 'Course Settings and Roster'
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//button[contains(@class,"show-enrollment-code")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[@class="enrollment-code"]')
            )
        )
        self.ps.test_updates['passed'] = True

    # Case C7720 - 006 - Teacher | Rename a course period
    @pytest.mark.skipif(str(7720) not in TESTS, reason='Excluded')
    def test_teacher_rename_a_course_period_7720(self):
        """Rename a course period.

        Steps:
        Go to Tutor
        Log in as a teacher
        Click on a Concept Coach book
        Click on the user menu
        Select course roster
        Click on tab for selected section
        Click 'Rename section'
        Enter new section name into the section Name text box
        Click on the 'Rename' button

        Expected Result:
        Section is renamed
        """
        self.ps.test_updates['name'] = 'cc1.10.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.10',
            'cc1.10.006',
            '7720'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.driver.find_element(
            By.XPATH, '//a[contains(@href,"/cc-dashboard")]'
        ).click()
        self.teacher.page.wait_for_page_load()
        self.teacher.open_user_menu()
        self.teacher.driver.find_element(
            By.LINK_TEXT, 'Course Settings and Roster'
        ).click()
        period_name = self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//li//a[@role="tab"]')
            )
        ).text
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[contains(@class,"rename-period")]//button')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[@class="modal-content"]//input[@type="text"]')
            )
        ).send_keys('_EDIT')
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[@class="modal-content"]//button/span[text()="Rename"]'
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//li//a[@role="tab" and text()="' + period_name + '_EDIT"]')
            )
        )
        # then set it back to what it was before
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[contains(@class,"rename-period")]//button')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[@class="modal-content"]//input[@type="text"]')
            )
        ).send_keys(Keys.BACK_SPACE * 5)
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[@class="modal-content"]//button/span[text()="Rename"]'
        ).click()

        self.ps.test_updates['passed'] = True

    # Case C7721 - 007 - Teacher | Archive an empty period
    @pytest.mark.skipif(str(7721) not in TESTS, reason='Excluded')
    def test_teacher_remove_an_empty_period_7721(self):
        """Remove an empty period.

        Steps:
        Go to Tutor
        Log in as a teacher
        Click on a Concept Coach book
        Click on the user menu
        Select course roster
        Click on tab for selected empty section
        Click 'Archive section'
        Click on the 'Archive' button

        Expected Result:
        Section is archived
        """
        self.ps.test_updates['name'] = 'cc1.10.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.10',
            'cc1.10.007',
            '7721'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        section_name = 'test_' + str(randint(0, 1000))
        self.teacher.login()
        self.teacher.driver.find_element(
            By.XPATH, '//a[contains(@href,"/cc-dashboard")]'
        ).click()
        self.teacher.page.wait_for_page_load()
        self.teacher.open_user_menu()
        self.teacher.driver.find_element(
            By.LINK_TEXT, 'Course Settings and Roster'
        ).click()
        # create an empty section
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"add-period")]//button')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[@class="modal-content"]//input[@type="text"]')
            )
        ).send_keys(section_name)
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[@class="modal-content"]//button/span[text()="Add"]'
        ).click()
        # archive the section just created
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//li//a[@role="tab" and text()="' + section_name + '"]')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//a[contains(@class,"archive-period")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[@role="tooltip"]//button' +
                 '//span[contains(text(),"Archive")]')
            )
        ).click()
        self.teacher.sleep(2)
        archived = self.teacher.driver.find_elements(
            By.XPATH, '//li//a[@role="tab" and text()="' + section_name + '"]')
        assert(len(archived) == 0), ' not archived'
        self.ps.test_updates['passed'] = True

    # Case C7722 - 008 - Teacher | Archive a non-empty period
    @pytest.mark.skipif(str(7722) not in TESTS, reason='Excluded')
    def test_teacher_archive_a_nonempty_periods_7722(self):
        """Error message displayed if attempting to remove a non-empty period.

        Steps:
        Go to Tutor
        Log in as a teacher
        Click on a Concept Coach book
        Click on the user menu
        Select course roster
        Click on tab for selected non-empty section
        Click 'Archive section'
        Click Archive

        Expected Result:
        Section is archived
        """
        self.ps.test_updates['name'] = 'cc1.10.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.10',
            'cc1.10.008',
            '7722'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.driver.find_element(
            By.XPATH, '//a[contains(@href,"/cc-dashboard")]'
        ).click()
        self.teacher.page.wait_for_page_load()
        self.teacher.open_user_menu()
        self.teacher.driver.find_element(
            By.LINK_TEXT, 'Course Settings and Roster'
        ).click()
        # name of period to archive (first tab)
        period_name = self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//li//a[@role="tab"]')
            )
        ).text
        # archive the section
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//li//a[@role="tab" and text()="' + period_name + '"]')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//a[contains(@class,"archive-period")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[@role="tooltip"]//button' +
                 '//span[contains(text(),"Archive")]')
            )
        ).click()
        self.teacher.sleep(2)
        archived = self.teacher.driver.find_elements(
            By.XPATH, '//li//a[@role="tab" and text()="' + section_name + '"]')
        assert(len(archived) == 0), ' not archived'
        # add the archived period back
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[contains(@class,"view-archived-periods")]//button')
            )
        ).click()
        periods = self.teacher.driver.find_elements(
            By.XPATH, '//div[@class="modal-content"]//tbody//tr'
        )
        print(period_name)
        print(len(periods))
        for period in periods:
            try:
                print('here')
                period.find_element(
                    By.XPATH, ".//td[text()='" + period_name + "']")
                print('here22222222')
                period.find_element(
                    By.XPATH,
                    ".//td//span[contains(@class,'restore-period')]//button"
                ).click()
                break
            except NoSuchElementException:
                if period == periods[-1]:
                    print('archived period not found')
                    raise Exception
        self.teacher.sleep(2)
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//li//a[@role="tab" and text()="' + period_name + '"]')
            )
        )
        self.ps.test_updates['passed'] = True

    # Case C58354 - 009 - Teacher | Unarchive a section
    @pytest.mark.skipif(str(58354) not in TESTS, reason='Excluded')
    def test_teacher_unarchive_a_section_58354(self):
        """Unarchive a section.

        Steps:
        go to tutor-qa.openstax.org
        log in as a teacher
        click on a Concept Coach book
        click on the user menu
        select course roster
        Click "View Archived Section"
        Click "Unarchive" for the desired section

        Expected Result:
        section is unarchived
        """
        self.ps.test_updates['name'] = 'cc1.10.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.10',
            'cc1.10.009',
            '58354'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.driver.find_element(
            By.XPATH, '//a[contains(@href,"/cc-dashboard")]'
        ).click()
        self.teacher.page.wait_for_page_load()
        self.teacher.open_user_menu()
        self.teacher.driver.find_element(
            By.LINK_TEXT, 'Course Settings and Roster'
        ).click()
        # name of period to archive (first tab)
        period_name = self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//li//a[@role="tab"]')
            )
        ).text
        # archive the section
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//li//a[@role="tab" and text()="' + period_name + '"]')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//a[contains(@class,"archive-period")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[@role="tooltip"]//button' +
                 '//span[contains(text(),"Archive")]')
            )
        ).click()
        self.teacher.sleep(2)
        archived = self.teacher.driver.find_elements(
            By.XPATH, '//li//a[@role="tab" and text()="' + section_name + '"]')
        assert(len(archived) == 0), ' not archived'
        # add the archived period back
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[contains(@class,"view-archived-periods")]//button')
            )
        ).click()
        periods = self.teacher.driver.find_elements(
            By.XPATH, '//div[@class="modal-content"]//tbody//tr'
        )
        print(period_name)
        print(len(periods))
        for period in periods:
            try:
                print('here')
                period.find_element(
                    By.XPATH, ".//td[text()='" + period_name + "']")
                print('here22222222')
                period.find_element(
                    By.XPATH,
                    ".//td//span[contains(@class,'restore-period')]//button"
                ).click()
                break
            except NoSuchElementException:
                if period == periods[-1]:
                    print('archived period not found')
                    raise Exception
        self.teacher.sleep(2)
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//li//a[@role="tab" and text()="' + period_name + '"]')
            )
        )
        self.ps.test_updates['passed'] = True

    # Case C7723 - 010 - Teacher | Rename the course
    @pytest.mark.skipif(str(7723) not in TESTS, reason='Excluded')
    def test_teacher_rename_the_course_7723(self):
        """Rename the course.

        Steps:
        Go to Tutor
        Log in as a teacher
        Click on a Concept Coach book
        Click on the user menu
        Select course roster
        Click 'Rename Course'
        Enter a new Course name into the Course Name text box
        Click on the 'Rename' button

        Expected Result:
        Course is renamed.
        """
        self.ps.test_updates['name'] = 'cc1.10.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.10',
            'cc1.10.010',
            '7723'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.driver.find_element(
            By.XPATH, '//a[contains(@href,"/cc-dashboard")]'
        ).click()
        self.teacher.page.wait_for_page_load()
        self.teacher.open_user_menu()
        self.teacher.driver.find_element(
            By.LINK_TEXT, 'Course Settings and Roster'
        ).click()
        # rename section
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[@class="-rename-course-link"]//button')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[@class="modal-content"]//input[@type="text"]')
            )
        ).send_keys("_EDIT")
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[@class="modal-content"]//button/span[text()="Rename"]'
        ).click()
        # check that the name was changed
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[@class="course-settings-title"]' +
                 '//span[contains(text(),"_EDIT")]')
            )
        )
        # change it back
        self.teacher.sleep(1)
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[@class="-rename-course-link"]//button')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[@class="modal-content"]//input[@type="text"]')
            )
        ).send_keys(Keys.BACK_SPACE * 5)
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[@class="modal-content"]//button/span[text()="Rename"]'
        ).click()

        self.ps.test_updates['passed'] = True

    # come back to this because need to login as admin
    # and add an extra teacher first
    # Case C7724 - 011 - Teacher | Remove other teachers from the course
    @pytest.mark.skipif(str(7724) not in TESTS, reason='Excluded')
    def test_teacher_remove_other_teachers_from_the_course_7724(self):
        """Remove other teachers from the course.

        Steps:
        Go to Tutor
        Log in as a teacher
        Click on a Concept Coach book
        Click on the user menu
        Select course roster
        Click on 'Remove' on the same row as selected teacher
        Click on the 'Remove' button

        Expected Result:
        Instructor is removed from the course
        """
        self.ps.test_updates['name'] = 'cc1.10.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.10',
            'cc1.10.011',
            '7724'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # come back to this because adding teacher through admin first
    # Case C7725 - 012 - Teacher | Remove themself from the course
    @pytest.mark.skipif(str(7725) not in TESTS, reason='Excluded')
    def test_teacher_remove_themself_from_the_course_7725(self):
        """Remove themself from the course.

        Steps:
        Go to Tutor
        Log in as a teacher
        Click on a Concept Coach book
        Click on the user menu
        Select course roster
        Click on 'Remove' on the same row as themselves
        Click on the 'Remove' button

        Expected Result:
        Teacher is removed from course and taken back to dashboard
        """
        self.ps.test_updates['name'] = 'cc1.10.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.10',
            'cc1.10.012',
            '7725'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7726 - 013 - Teacher | Transfer a student to another period
    @pytest.mark.skipif(str(7726) not in TESTS, reason='Excluded')
    def test_teacher_transfer_a_student_to_another_period_7726(self):
        """Transfer a student to another period.

        Steps:
        Go to Tutor
        Log in as a teacher
        Click on a Concept Coach book
        Click on the user menu
        Select course roster
        Click on tab for section selected student is currently enrolled in
        Click on 'Change Section' on the row of the selected student
        Click on section to move student to

        Expected Result:
        Student is moved to chosen section
        """
        self.ps.test_updates['name'] = 'cc1.10.013' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.10',
            'cc1.10.013',
            '7726'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.driver.find_element(
            By.XPATH, '//a[contains(@href,"/cc-dashboard")]'
        ).click()
        self.teacher.page.wait_for_page_load()
        self.teacher.open_user_menu()
        self.teacher.driver.find_element(
            By.LINK_TEXT, 'Course Settings and Roster'
        ).click()
        # move student
        first_student = self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[@class="period"]//tbody/tr[1]')
            )
        )
        student_name = first_student.find_element(
            By.XPATH, './/td[1]').text
        first_student.find_element(
            By.XPATH,
            './/td[@class="actions"]/a[@aria-describedby="change-period"]'
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[@class="popover-content"]//li[1]')
            )
        ).click()
        # check that student was moved
        self.teacher.sleep(2)
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//li[@tabindex="1"]//a[@role="tab"]')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[@class="period"]//tbody/tr' +
                 '//td[text()="' + student_name + '"]')
            )
        )
        self.ps.test_updates['passed'] = True

    # Case C7727 - 014 - Teacher | Remove a student from a course
    @pytest.mark.skipif(str(7727) not in TESTS, reason='Excluded')
    def test_teacher_remove_a_student_from_a_course_7727(self):
        """Remove a student from a course.

        Steps:
        Go to Tutor
        Log in as a teacher
        Click on a Concept Coach book
        Click on the user menu
        Select course roster
        Click on tab for section selected student is currently enrolled in
        Click on 'Drop' on the row of the selected student
        Click on the 'Drop' button

        Expected Result:
        Student is dropped from the course
        """
        self.ps.test_updates['name'] = 'cc1.10.014' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.10',
            'cc1.10.014',
            '7727'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.driver.find_element(
            By.XPATH, '//a[contains(@href,"/cc-dashboard")]'
        ).click()
        self.teacher.page.wait_for_page_load()
        self.teacher.open_user_menu()
        self.teacher.driver.find_element(
            By.LINK_TEXT, 'Course Settings and Roster'
        ).click()
        # drop student
        first_student = self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[@class="period"]//tbody/tr[1]')
            )
        )
        student_name = first_student.find_element(
            By.XPATH, './/td[1]').text
        first_student.find_element(
            By.XPATH,
            './/td[@class="actions"]/a[@aria-describedby="drop-student"]'
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[@id="drop-student"]//button')
            )
        ).click()
        # check that student was removed
        self.teacher.sleep(2)
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[contains(@class,"dropped-students")]//tbody/tr' +
                 '//td[text()="' + student_name + '"]')
            )
        )
        self.ps.test_updates['passed'] = True

    # Case C7728 - 015 - Admin | Impersonate a teacher
    @pytest.mark.skipif(str(7728) not in TESTS, reason='Excluded')
    def test_admin_impersonate_a_teacher_7728(self):
        """Impersonate a teacher.

        Steps:
        Go to Tutor
        Click on the 'Login' button
        Enter the admin user account in the username and password text boxes
        Click on the 'Sign in' button
        Click on the user's name in the top right corner to open drop down menu
        Click on the 'Admin' option of the drop down menu
        Click on 'Users' on the bar across the top
        [optional] Enter a teacher name into the search here text box
        Click on the 'Search' button
        Click on the 'Sign in as' button next to chosen teacher

        Expected Result:
        Signs in as chosen chosen teacher.
        Goes to chosen teacher's initial screen after login
        If multiple courses list of textbooks
        If one course straight to dashboard
        """
        self.ps.test_updates['name'] = 'cc1.10.015' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.10',
            'cc1.10.015',
            '7728'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.login()
        self.admin.open_user_menu()
        self.admin.driver.find_element(
            By.LINK_TEXT, 'Admin'
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'Users')
            )
        ).click()
        self.admin.page.wait_for_page_load()
        self.admin.driver.find_element(By.ID, 'query').send_keys('teacher01')
        self.admin.driver.find_element(
            By.XPATH, '//input[@value="Search"]').click()
        self.admin.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(text(),"Sign in as")]')
            )
        ).click()
        self.admin.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//span[contains(text(),"Charles Morris")]')
            )
        )

        self.ps.test_updates['passed'] = True

    # Case C7729 - 016 - Admin | Change a course ecosystem
    @pytest.mark.skipif(str(7729) not in TESTS, reason='Excluded')
    def test_admin_change_a_course_ecosystem_7729(self):
        """Change a course ecosystem.

        Steps:
        Go to Tutor
        Click on the 'Login' button
        Enter the admin user account in the username and password text boxes
        Click on the 'Sign in' button
        Click on the 'Admin' button from the user menu
        Open the drop down menu by clicking 'Course Organization'
        Click the 'Courses' option
        Click the 'Edit' link for the desired course
        Click on the 'Course content' tab
        Select a different option in the 'Ecosystem' drop down menu
        Click the 'Submit' button

        Expected Result:
        Course ecosystem change is put on a queue
        """
        self.ps.test_updates['name'] = 'cc1.10.016' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.10',
            'cc1.10.016',
            '7729'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.admin.login()
        self.admin.open_user_menu()
        self.teacher.driver.find_element(
            By.LINK_TEXT, 'Admin'
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'Courses')
            )
        ).click()
        self.admin.page.wait_for_page_load()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'Edit')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'Course content')
            )
        ).click()

        self.ps.test_updates['passed'] = True

    # Case C7730 - 017 - Admin | Change multiple course ecosystems in bulk
    @pytest.mark.skipif(str(7730) not in TESTS, reason='Excluded')
    def test_admin_change_multiple_course_ecosystems_in_bulk_7730(self):
        """Change multiple course ecosystems in bulk.

        Steps:
        Go to Tutor
        Click on the 'Login' button
        Enter the admin user account in the username and password text boxes
        Click on the 'Sign in' button
        Click on the 'Admin' button from the user menu
        Open the drop down menu by clicking 'Course Organization'
        Click the 'Courses' option
        Check the checkboxes next to selected courses
        Select an option in the 'Select an ecosystem' drop down menu
        Click the 'Set Ecosystem' button

        Expected Result:
        Course ecosystem change is put on a queue
        """
        self.ps.test_updates['name'] = 'cc1.10.017' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.10',
            'cc1.10.017',
            '7730'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7731 - 018 - Teacher | Receive a notice when students register
    @pytest.mark.skipif(str(7731) not in TESTS, reason='Excluded')
    def test_teacher_receive_a_notice_when_students_register_7731(self):
        """Receive a notice when students register.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 'cc1.10.018' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.10',
            'cc1.10.018',
            '7731'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
