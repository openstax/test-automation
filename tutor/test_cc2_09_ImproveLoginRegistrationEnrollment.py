"""Concept Coach v2, Epic 9 - Improve Login, Registration, Enrollment."""

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
from selenium.common.exceptions import NoSuchElementException

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Teacher, Student, User

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': 'latest',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([
        14819
        # 14820, 14819, 14759, 14862, 14771,
        # 14821, 14822
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestImproveLoginRegistrationEnrollment(unittest.TestCase):
    """CC2.09 - Improve Login, Registration, Enrollment."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.teacher = Teacher(
            use_env_vars=True,
            # pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        self.student = Student(
            use_env_vars=True,
            existing_driver=self.teacher.driver,
            # pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        # self.user = User(
        #     use_env_vars=True,
        #     existing_driver=self.teacher.driver,
        #     # pasta_user=self.ps,
        #     # capabilities=self.desired_capabilities
        # )

    def tearDown(self):
        """Test destructor."""
        self.ps.update_job(
            job_id=str(self.teacher.driver.session_id),
            **self.ps.test_updates
        )
        try:
            self.student.driver = None
            self.user.driver = None
            self.teacher.delete()
        except:
            pass

    # 14820 - 001 - Teacher | Register for teaching a CC course as new faculty
    @pytest.mark.skipif(str(14820) not in TESTS, reason='Excluded')
    def test_teacher_register_for_teaching_cc_course_as_new_facult_14820(self):
        """Register for teaching a CC course as new faculty.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 'cc2.09.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.09', 'cc2.09.001', '14820']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 14819 - 002 - Teacher | Register for teaching a CC course as
    # returning faculty for the same book
    @pytest.mark.skipif(str(14819) not in TESTS, reason='Excluded')
    def test_teacher_register_for_teaching_cc_course_as_returning_14819(self):
        """Register for teaching a CC course as returning faculty.

        Steps:
        Go to Tutor
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a CC course name
        Click "Course Settings and Roster" from the user menu
        Click "Add Section"
        Create a name when prompted
        Click "Add"
        Click on the sections from previous semesters
        Click "Archive Section"

        Expected Result:
        A new section is added and the old sections are archived
        """
        self.ps.test_updates['name'] = 'cc2.09.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.09', 'cc2.09.002', '14819']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.driver.find_element(
            By.XPATH, '//a[contains(@href,"/cc-dashboard")]'
        ).click()
        self.teacher.open_user_menu()
        self.teacher.driver.find_element(
            By.LINK_TEXT, 'Course Settings and Roster'
        ).click()
        # add a new section
        new_section_name = "new_section_" + str(randint(100, 999))
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
        ).send_keys(new_section_name)
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[@class="modal-content"]//button/span[text()="Add"]'
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//li//a[@role="tab" and text()="' + new_section_name + '"]')
            )
        )
        # revove old section
        old_section_name = self.teacher.find(By.XPATH, '//a[@role="tab"]').text
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//li//a[@role="tab" and text()="' + old_section_name + '"]')
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
            By.XPATH,
            '//li//a[@role="tab" and text()="' + old_section_name + '"]')
        assert(len(archived) == 0), ' not archived'

        # arhive new section and re-add old section as clean-up
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//li//a[@role="tab" and text()="' + new_section_name + '"]')
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

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[contains(@class,"view-archived-periods")]//button')
            )
        ).click()
        periods = self.teacher.driver.find_elements(
            By.XPATH, '//div[@class="modal-content"]//tbody//tr'
        )
        for period in periods:
            try:
                period.find_element(
                    By.XPATH, ".//td[text()='" + old_section_name + "']")
                period.find_element(
                    By.XPATH,
                    ".//td//span[contains(@class,'restore-period')]//button"
                ).click()
                break
            except NoSuchElementException:
                if period == periods[-1]:
                    raise Exception

        self.ps.test_updates['passed'] = True

    # 14759 - 003 - Student | Sign up and enroll in a CC course
    @pytest.mark.skipif(str(14759) not in TESTS, reason='Excluded')
    def test_teacher_sign_up_and_enroll_in_a_cc_course_14759(self):
        """Sign up and enroll in a CC course.

        Steps:
        Sign in as teacher
        Click on a Concept Coach course
        Click on "Course Settings and Roster" from the user menu
        Click "Your Student Enrollment Code"
        Copy and paste the URL into an incognito window
        Click "Jump to Concept Coach"
        Click "Launch Concept Coach"
        Click Sign Up
        Click Sign up with a password
        Fill in the required fields
        Click "Create Account"
        Enter the numerical enrollment code you get from the teacher
        Click "Enroll"
        Enter school issued ID, OR skip this step for now

        Expected Result:
        The user is presented with a message that confirms enrollment
        Is redirected to the CC assignment
        """
        self.ps.test_updates['name'] = 'cc2.09.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.09', 'cc2.09.003', '14759']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 14862 - 004 - Student | Sign in and enroll in a CC course
    @pytest.mark.skipif(str(14862) not in TESTS, reason='Excluded')
    def test_teacher_sign_in_and_enroll_in_a_cc_course_14862(self):
        """Sign in and enroll in a CC course.

        Steps:
        Sign in as teacher100
        Click on a Concept Coach course
        Click on "Course Settings and Roster" from the user menu
        Click "Your Student Enrollment Code"
        Copy and paste the URL into an incognito window
        Click "Jump to Concept Coach"
        Click "Launch Concept Coach"
        Click Sign In
        Sign in as student71
        Enter the numerical enrollment code you get from the teacher
        Click "Enroll"
        Enter school issued ID, OR skip this step for now

        Expected Result:
        The user is presented with a message that confirms enrollment
        Is redirected to the CC assignment
        """
        self.ps.test_updates['name'] = 'cc2.09.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.09', 'cc2.09.004', '14862']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 14771 - 005 - User | View a message that says you need an enrollment code
    # before signing up
    @pytest.mark.skipif(str(14771) not in TESTS, reason='Excluded')
    def test_user_view_a_message_that_says_you_need_an_enrollment_14771(self):
        """View a message that says you need an enrollment code before signing up.

        Steps:
        Go to the link provided by instructor to a cc book
        ex: https://demo.cnx.org/contents/meEn-Pci@1.1:XpgHmEe6@1/CC-Derived-
        AnP-Preface
        Click "Jump to Concept Coach"
        Click "Launch Concept Coach"

        Expected Result:
        The user is presented with a message that says "Sign up with your
        enrollment code. If you don't have an enrollment code, contact your
        instructor."
        """
        self.ps.test_updates['name'] = 'cc2.09.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.09', 'cc2.09.005', '14771']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 14821 - 006 - Student | Jump to CC from the top of the reading
    @pytest.mark.skipif(str(14821) not in TESTS, reason='Excluded')
    def test_student_jump_to_cc_from_the_top_of_the_reading_14821(self):
        """Jump to CC from the top of the reading.

        Steps:
        If the user has more than one course, click on a CC course name
        Click on a non-introductory section
        Click "Jump to Concept Coach"

        Expected Result:
        The screen jumps to the "Launch Concept Coach" button
        """
        self.ps.test_updates['name'] = 'cc2.09.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.09', 'cc2.09.006', '14821']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 14822 - 007 - Teacher | Jump to CC from the top of the reading
    @pytest.mark.skipif(str(14822) not in TESTS, reason='Excluded')
    def test_teacher_jump_to_cc_from_the_top_of_the_reading_14822(self):
        """Jump to CC from the top of the reading.

        Steps:
        If the user has more than one course, click on a CC course name
        Click "Online Book"
        Click on a non-introductory section
        Click "Jump to Concept Coach"

        Expected Result:
        The screen jumps to the "Launch Concept Coach" button
        """
        self.ps.test_updates['name'] = 'cc2.09.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.09', 'cc2.09.007', '14822']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
