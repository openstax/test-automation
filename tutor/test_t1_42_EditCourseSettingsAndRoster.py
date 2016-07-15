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
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

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
class TestEditCourseSettingsAndRoster(unittest.TestCase):
    """T1.42 - Edit Course Settings and Roster."""

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
        self.teacher.open_user_menu()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Course Settings and Roster')
            )
        ).click()
        self.teacher.page.wait_for_page_load()


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
    def test_teacher_edit_the_course_name(self):
        """Edit the course name.

        Steps:
        Click the "Rename Course" button that is next to the course name
        Enter a new course name 
        Click the "Rename" button
        Click the X that is on the upper right corner of the dialogue box


        Expected Result:
        The course name is edited.
        (then put it back at the end)
        """
        self.ps.test_updates['name'] = 't1.42.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.42','t1.42.001','8258']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        course_name = self.teacher.driver.find_element(
            By.XPATH,'//div[@class="course-settings-title"]/span').text
        print(course_name)
        self.teacher.driver.find_element(
            By.XPATH,'//button[contains(@class,"edit-course")]'\
            '//span[contains(text(),"Rename Course")]').click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                ( By.XPATH,'//input[contains(@class,"form-control")]')
            )
        ).send_keys('_EDIT')
        self.teacher.driver.find_element(
            By.XPATH,'//button[contains(@class,"edit-course-confirm")]').click()
        #check that it was edited
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                ( By.XPATH,'//div[@class="course-settings-title"]'\
                  '/span[contains(text(),"'+course_name+'_EDIT")]')
            )
        )
        # set it back
        self.teacher.sleep(1)
        self.teacher.driver.find_element(
            By.XPATH,'//button[contains(@class,"edit-course")]'\
            '//span[contains(text(),"Rename Course")]').click()
        for i in range(len('_EDIT')):
            self.teacher.wait.until(
                expect.element_to_be_clickable(
                    ( By.XPATH,'//input[contains(@class,"form-control")]')
                )
            ).send_keys(Keys.BACK_SPACE)
        self.teacher.driver.find_element(
            By.XPATH,'//button[contains(@class,"edit-course-confirm")]').click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                ( By.XPATH,'//div[@class="course-settings-title"]'\
                  '/span[text()="'+course_name+'"]')
            )
        )
        self.ps.test_updates['passed'] = True

    # need a way to add a second instructor who can then be droped
    # also caused error in manual testinf
    # Case C8259 - 002 - Teacher | Remove an instructor from the course
    @pytest.mark.skipif(str(8259) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_remove_an_instructor_from_a_course(self):
        """Remove an instructor from the course.

        Steps:
        Click the "Remove" button for an instructor under the Instructors section 
        Click "Remove" on the box that pops up

        Expected Result:
        The instructor is removed from the Instructors list.
        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)


    # Case C8260 - 003 - Teacher | Remove the last instructor from the course
    @pytest.mark.skipif(str(8260) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_remove_the_last_instructor_from_the_course(self):
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
    def test_teacher_add_a_period(self):
        """Add a period.

        Steps:
        Click "+ Add Period" 
        Enter a period name into the Period Name text box
        Click "Add"

        Expected Result:
        A new period is added.
        """
        self.ps.test_updates['name'] = 't1.42.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.42','t1.42.004','8261']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        period_name = 'automated_4'
        self.teacher.driver.find_element(
            By.XPATH,'//li[contains(@class,"add-period")]//button').click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH,'//input[contains(@class,"form-control")]')
            )
        ).send_keys(period_name)
        self.teacher.driver.find_element(
            By.XPATH,'//button[contains(@class,"edit-period-confirm")]').click()
        self.teacher.sleep(1)
        self.teacher.driver.find_element(
            By.XPATH,'//a[contains(text(),"'+period_name+'")]')
        self.ps.test_updates['passed'] = True


    # Case C8262 - 005 - Teacher | Rename a period 
    @pytest.mark.skipif(str(8262) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Rename a period.

        Steps:
        Click "Rename Period"
        Enter a new period name into the Period Name text box
        Click "Rename"

        Expected Result:
        A period is renamed.
        """
        self.ps.test_updates['name'] = 't1.42.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.42','t1.42.005','8262']
        self.ps.test_updates['passed'] = False

        # create a period
        period_name = 'automated_5'
        self.teacher.driver.find_element(
            By.XPATH,'//li[contains(@class,"add-period")]//button').click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH,'//input[contains(@class,"form-control")]')
            )
        ).send_keys(period_name)
        self.teacher.driver.find_element(
            By.XPATH,'//button[contains(@class,"edit-period-confirm")]').click()
        self.teacher.sleep(1)
        # edit the period
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                ( By.XPATH,'//a[contains(text(),"'+period_name+'")]')
            )
        ).click()
        self.teacher.driver.find_element(
            By.XPATH,'//span[contains(@class,"rename-period")]/button').click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH,'//input[contains(@class,"form-control")]')
            )
        ).send_keys('_EDIT')
        self.teacher.driver.find_element(
            By.XPATH,'//button[contains(@class,"edit-period-confirm")]').click()
        self.teacher.sleep(1)
        self.teacher.driver.find_element(
            By.XPATH,'//a[contains(text(),"'+period_name+'_EDIT")]')
        self.ps.test_updates['passed'] = True


    # Case C8263 - 006 - Teacher | Archive an empty period
    @pytest.mark.skipif(str(8263) not in TESTS, reason='Excluded')  # NOQA
    def test_archive_an_empt_period(self):
        """Archive an empty period.

        Steps:
        Click on an empty period 
        Click "Archive Period" 
        Click "Archive" on the dialogue box

        Expected Result:
        An empty period is archived.
        """
        self.ps.test_updates['name'] = 't1.42.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.42','t1.42.006','8263']
        self.ps.test_updates['passed'] = False

        # create a period
        period_name = 'automated_006'
        self.teacher.driver.find_element(
            By.XPATH,'//li[contains(@class,"add-period")]//button').click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH,'//input[contains(@class,"form-control")]')
            )
        ).send_keys(period_name)
        self.teacher.driver.find_element(
            By.XPATH,'//button[contains(@class,"edit-period-confirm")]').click()
        self.teacher.sleep(1)
        # edit the period
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                ( By.XPATH,'//a[contains(text(),"'+period_name+'")]')
            )
        ).click()
        self.teacher.driver.find_element(
            By.XPATH,'//a[contains(@class,"archive-period")]').click()
        self.teacher.driver.find_element(
            By.XPATH,'//div[contains(@class,"popover-content")]'\
            '//button[contains(@class,"archive")]').click()
        try:
            self.teacher.driver.find_element(
                By.XPATH,'//a[contains(text(),"'+period_name+'")]')
        except NoSuchElementException:
                self.ps.test_updates['passed'] = True

    # # how to create a non-empty period that can be used for testing archived
    # # Case C8264 - 007 - Teacher | Archive a non-empty period 
    # @pytest.mark.skipif(str(8264) not in TESTS, reason='Excluded')  # NOQA
    # def test_teacher_archive_a_non_empty_period(self):
    #     """Archive a non-empty period.

    #     Steps:
    #     Click on a non-empty period 
    #     Click "Archive Period"
    #     Click Archive

    #     Expected Result:
    #     period is archived
    #     """
    #     self.ps.test_updates['name'] = 't1.42.007' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = ['t1','t1.42','t1.42.007','8264']
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


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
        self.ps.test_updates['tags'] = ['t1','t1.42','t1.42.008','8265']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.driver.find_element(
            By.XPATH,'//a[@aria-describedby="change-period"]').click()
        student_name = self.teacher.driver.find_element(
            By.XPATH,'//div[@class="roster"]//td').text
        element = self.teacher.driver.find_element(
            By.XPATH,'//div[@class="popover-content"]//a')
        period_name = element.text
        element.click()
        self.teacher.sleep(1)
        self.teacher.driver.find_element(
            By.XPATH,'//li/a[contains(text(),"'+period_name+'")]').click()
        self.teacher.driver.find_element(
            By.XPATH,'//td[contains(text(),"'+student_name+'")]')            
        self.ps.test_updates['passed'] = True


    # Case C8266 - 009 - Teacher | Drop a student
    @pytest.mark.skipif(str(8266) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_drop_a_student(self):
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
        self.ps.test_updates['tags'] = ['t1','t1.42','t1.42.009','8266']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        student_name = self.teacher.driver.find_element(
            By.XPATH,'//div[@class="roster"]//td').text
        self.teacher.driver.find_element(
            By.XPATH,'//a[@aria-describedby="drop-student"]').click()
        self.teacher.driver.find_element(
            By.XPATH,'//div[@class="popover-content"]//button').click()
        self.teacher.sleep(1)
        # check that student was droped
        print(student_name)
        self.teacher.driver.find_element(
            By.XPATH,'//div[contains(@class,"dropped-students")]'\
            '//td[contains(text(),"'+student_name+'")]'
        )
        self.ps.test_updates['passed'] = True


    # Case C8267 - 010 - Teacher | Readd a dropped student
    @pytest.mark.skipif(str(8267) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_readd_a_dropped_student(self):
        """Readd a dropped student.

        Steps:
        Click "Add Back to Active Roster" for a student under the Dropped Students section
        Click "Add" on the box that pops up

        Expected Result:
        A student is added back to the course
        """
        self.ps.test_updates['name'] = 't1.42.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.42','t1.42.010','8267']
        self.ps.test_updates['passed'] = False

        # drop a student (to make sure there is someone to add back)
        student_name = self.teacher.driver.find_element(
            By.XPATH,'//div[@class="roster"]//td').text
        self.teacher.driver.find_element(
            By.XPATH,'//a[@aria-describedby="drop-student"]').click()
        self.teacher.driver.find_element(
            By.XPATH,'//div[@class="popover-content"]//button').click()
        self.teacher.sleep(1)
        #add a student back (not necessarily the same student that was just droped)
        element = self.teacher.driver.find_element(
            By.XPATH,'//div[contains(@class,"dropped-students")]'\
            '//span[contains(text(),"Add Back to Active Roster")]')
        self.teacher.driver.execute_script('return arguments[0].scrollIntoView();', element)
        self.teacher.driver.execute_script('window.scrollBy(0, -80);')
        element.click()
        self.teacher.driver.find_element(
            By.XPATH,'//div[@class="popover-content"]//button').click()
        # check that student was added back
        self.teacher.driver.find_element(
            By.XPATH,'//div[@class="roster"]//td[contains(text(),"'+student_name+'")]')

        self.ps.test_updates['passed'] = True
