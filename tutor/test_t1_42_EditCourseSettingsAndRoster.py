"""Tutor v1, Epic 42 - Edit Course Settings and Roster."""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
# from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.common.keys import Keys

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Teacher, Admin

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': '50.0',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([
        8258, 8259, 8260, 8261, 8262,
        8263, 8264, 8265, 8266, 8267,
        58356
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestEditCourseSettingsAndRoster(unittest.TestCase):
    """T1.42 - Edit Course Settings and Roster."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.teacher = Teacher(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
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
        self.ps.update_job(
            job_id=str(self.teacher.driver.session_id),
            **self.ps.test_updates
        )
        try:
            self.teacher.delete()
        except:
            pass

    # Case C8258 - 001 - Teacher | Edit the course name
    @pytest.mark.skipif(str(8258) not in TESTS, reason='Excluded')
    def test_teacher_edit_the_course_name_8258(self):
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
        self.ps.test_updates['tags'] = ['t1', 't1.42', 't1.42.001', '8258']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        course_name = self.teacher.driver.find_element(
            By.XPATH,
            '//div[@class="course-settings-title"]/span'
        ).text
        print(course_name)
        self.teacher.find(
            By.XPATH, '//button[contains(@class,"edit-course")]' +
            '//span[contains(text(),"Rename Course")]'
        ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//input[contains(@class,"form-control")]')
            )
        ).send_keys('_EDIT')
        self.teacher.find(
            By.XPATH,
            '//button[contains(@class,"edit-course-confirm")]'
        ).click()
        # check that it was edited
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="course-settings-title"]' +
                 '/span[contains(text(),"%s_EDIT")]' % course_name)
            )
        )
        # set it back
        self.teacher.sleep(1)
        self.teacher.driver.find_element(
            By.XPATH,
            '//button[contains(@class,"edit-course")]' +
            '//span[contains(text(),"Rename Course")]'
        ).click()
        for _ in range(len('_EDIT')):
            self.teacher.wait.until(
                expect.element_to_be_clickable(
                    (By.XPATH, '//input[contains(@class,"form-control")]')
                )
            ).send_keys(Keys.BACK_SPACE)
        self.teacher.find(
            By.XPATH,
            '//button[contains(@class,"edit-course-confirm")]'
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[@class="course-settings-title"]' +
                 '/span[text()="%s"]' % course_name)
            )
        )

        self.ps.test_updates['passed'] = True

    # Case C8259 - 002 - Teacher | Remove an instructor from the course
    @pytest.mark.skipif(str(8259) not in TESTS, reason='Excluded')
    def test_teacher_remove_an_instructor_from_a_course_8259(self):
        """Remove an instructor from the course.

        Steps:
        Click "Remove" for an instructor under the Instructors section
        Click "Remove" on the box that pops up

        Expected Result:
        The instructor is removed from the Instructors list.
        """
        self.ps.test_updates['name'] = 't1.42.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.42', 't1.42.002', '8259']
        self.ps.test_updates['passed'] = False

        self.teacher.logout()
        # add extra instructor through admin first
        admin = Admin(
            use_env_vars=True,
            existing_driver=self.teacher.driver
        )
        admin.login()
        admin.get('https://tutor-qa.openstax.org/admin/courses/1/edit')
        admin.page.wait_for_page_load()
        teacher_name = 'Trent'
        admin.find(
            By.XPATH, '//a[contains(text(),"Teachers")]').click()
        admin.find(
            By.ID, 'course_teacher').send_keys(teacher_name)
        admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//li[contains(text(),"%s")]' % teacher_name)
            )
        ).click()
        admin.sleep(1)
        admin.find(
            By.LINK_TEXT, 'Main Dashboard').click()
        admin.page.wait_for_page_load()
        admin.logout()
        # redo set-up, but make sure to go to course 1
        self.teacher.login()
        self.teacher.get('https://tutor-qa.openstax.org/courses/1')
        self.teacher.open_user_menu()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Course Settings and Roster')
            )
        ).click()
        self.teacher.page.wait_for_page_load()
        # delete teacher
        teachers_list = self.teacher.find_all(
            By.XPATH, '//div[@class="teachers-table"]//tbody//tr')
        for x in range(len(teachers_list)):
            temp_first = self.teacher.find(
                By.XPATH,
                '//div[@class="teachers-table"]//tbody//tr[' +
                str(x + 1) + ']/td'
            ).text
            if temp_first == teacher_name:
                self.teacher.find(
                    By.XPATH,
                    '//div[@class="teachers-table"]//tbody//tr[' +
                    str(x + 1) + ']//td//span[contains(text(),"Remove")]'
                ).click()
                self.teacher.sleep(1)
                self.teacher.find(
                    By.XPATH, '//div[@class="popover-content"]//button'
                ).click()
                break
            if x == len(teachers_list) - 1:
                print('added teacher was not found, and not deleted')
                raise Exception
        deleted_teacher = self.teacher.driver.find_elements(
            By.XPATH, '//td[contains(text(),"%s")]' % teacher_name)
        assert(len(deleted_teacher) == 0), 'teacher not deleted'

        self.ps.test_updates['passed'] = True

    # Case C8260 - 003 - Teacher | Remove the last instructor from the course
    @pytest.mark.skipif(str(8260) not in TESTS, reason='Excluded')
    def test_teacher_remove_the_last_instructor_from_the_course_8260(self):
        """Remove the last instructor from the course.

        Steps:
        Click on the user menu in the upper right corner of the page
        Click "Course Roster"
        Click "Remove" for an instructor under the Instructors section
        Click "Remove" on the box that pops up

        Expected Result:
        The instructor is removed from the Instructors list.
        """
        self.ps.test_updates['name'] = 't1.42.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.42', 't1.42.003', '8260']
        self.ps.test_updates['passed'] = False

        raise NotImplementedError(inspect.currentframe().f_code.co_name)
        self.teacher.logout()
        # add extra instructor through admin first
        admin = Admin(
            use_env_vars=True,
            existing_driver=self.teacher.driver
        )
        admin.login()
        admin.get('https://tutor-qa.openstax.org/admin/courses/1/edit')
        admin.page.wait_for_page_load()
        teacher_name = 'Trent'
        admin.find(
            By.XPATH, '//a[contains(text(),"Teachers")]').click()
        admin.find(
            By.ID, 'course_teacher').send_keys(teacher_name)
        admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//li[contains(text(),"%s")]' % teacher_name)
            )
        ).click()
        admin.sleep(1)
        admin.find(
            By.LINK_TEXT, 'Main Dashboard').click()
        admin.page.wait_for_page_load()
        admin.logout()
        # redo set-up, but make sure to go to course 1
        self.teacher.login()
        self.teacher.get('https://tutor-qa.openstax.org/courses/1')
        self.teacher.open_user_menu()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Course Settings and Roster')
            )
        ).click()
        self.teacher.page.wait_for_page_load()
        # delete teacher
        teachers_list = self.teacher.find_all(
            By.XPATH, '//div[@class="teachers-table"]//tbody//tr')
        for x in range(len(teachers_list)):
            temp_first = self.teacher.find(
                By.XPATH,
                '//div[@class="teachers-table"]//tbody//tr[' +
                str(x + 1) + ']/td'
            ).text
            if temp_first == teacher_name:
                self.teacher.find(
                    By.XPATH,
                    '//div[@class="teachers-table"]//tbody//tr[' +
                    str(x + 1) + ']//td//span[contains(text(),"Remove")]'
                ).click()
                self.teacher.sleep(1)
                self.teacher.find(
                    By.XPATH, '//div[@class="popover-content"]//button'
                ).click()
                break
            if x == len(teachers_list) - 1:
                print('added teacher was not found, and not deleted')
                raise Exception
        deleted_teacher = self.teacher.driver.find_elements(
            By.XPATH, '//td[contains(text(),"%s")]' % teacher_name)
        assert(len(deleted_teacher) == 0), 'teacher not deleted'

        self.ps.test_updates['passed'] = True

    # Case C8261 - 004 - Teacher | Add a period
    @pytest.mark.skipif(str(8261) not in TESTS, reason='Excluded')
    def test_teacher_add_a_period_8261(self):
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
        self.ps.test_updates['tags'] = ['t1', 't1.42', 't1.42.004', '8261']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        period_name = 'automated_' + str(randint(0, 999))
        self.teacher.find(
            By.XPATH, '//div[contains(@class,"add-period")]//button').click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//input[contains(@class,"form-control")]')
            )
        ).send_keys(period_name)
        self.teacher.find(
            By.XPATH,
            '//button[contains(@class,"edit-period-confirm")]'
        ).click()
        self.teacher.sleep(1)
        self.teacher.find(
            By.XPATH, '//a[contains(text(),"'+period_name+'")]')

        self.ps.test_updates['passed'] = True

    # Case C8262 - 005 - Teacher | Rename a period
    @pytest.mark.skipif(str(8262) not in TESTS, reason='Excluded')
    def test_teacher_rename_a_period_8262(self):
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
        self.ps.test_updates['tags'] = ['t1', 't1.42', 't1.42.005', '8262']
        self.ps.test_updates['passed'] = False

        # create a period
        period_name = 'automated_' + str(randint(0, 999))
        self.teacher.find(
            By.XPATH, '//div[contains(@class,"add-period")]//button').click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//input[contains(@class,"form-control")]')
            )
        ).send_keys(period_name)
        self.teacher.find(
            By.XPATH,
            '//button[contains(@class,"edit-period-confirm")]'
        ).click()
        self.teacher.sleep(1)
        # edit the period
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(text(),"'+period_name+'")]')
            )
        ).click()
        self.teacher.find(
            By.XPATH, '//span[contains(@class,"rename-period")]/button'
        ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//input[contains(@class,"form-control")]')
            )
        ).send_keys('_EDIT')
        self.teacher.find(
            By.XPATH,
            '//button[contains(@class,"edit-period-confirm")]'
        ).click()
        self.teacher.sleep(1)
        self.teacher.find(
            By.XPATH, '//a[contains(text(),"'+period_name+'_EDIT")]')

        self.ps.test_updates['passed'] = True

    # Case C8263 - 006 - Teacher | Archive an empty period
    @pytest.mark.skipif(str(8263) not in TESTS, reason='Excluded')
    def test_teacher_archive_an_empt_period_8263(self):
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
        self.ps.test_updates['tags'] = ['t1', 't1.42', 't1.42.006', '8263']
        self.ps.test_updates['passed'] = False

        # create a period
        period_name = 'automated_' + str(randint(0, 999))
        self.teacher.find(
            By.XPATH, '//div[contains(@class,"add-period")]//button').click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//input[contains(@class,"form-control")]')
            )
        ).send_keys(period_name)
        self.teacher.find(
            By.XPATH,
            '//button[contains(@class,"edit-period-confirm")]'
        ).click()
        self.teacher.sleep(1)
        # edit the period
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(text(),"'+period_name+'")]')
            )
        ).click()
        self.teacher.find(
            By.XPATH, '//a[contains(@class,"archive-period")]').click()
        self.teacher.find(
            By.XPATH, '//div[contains(@class,"popover-content")]' +
            '//button[contains(@class,"archive")]').click()
        self.teacher.sleep(2)
        archived_period = self.teacher.find_all(
            By.XPATH, '//a[contains(text(),"'+period_name+'")]')
        assert(len(archived_period) == 0), 'period not archived'

        self.ps.test_updates['passed'] = True

    # Case C8264 - 007 - Teacher | Archive a non-empty period
    @pytest.mark.skipif(str(8264) not in TESTS, reason='Excluded')
    def test_teacher_archive_a_non_empty_period_8264(self):
        """Archive a non-empty period.

        Steps:
        Click on a non-empty period
        Click "Archive Period"
        Click Archive

        Expected Result:
        Period is archived
        """
        self.ps.test_updates['name'] = 't1.42.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.42', 't1.42.007', '8264']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        period_name = self.teacher.find(
            By.XPATH, '//ul[@role="tablist"]//a[@role="tab"]').text
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(text(),"'+period_name+'")]')
            )
        ).click()
        self.teacher.find(
            By.XPATH, '//a[contains(@class,"archive-period")]').click()
        self.teacher.find(
            By.XPATH, '//div[contains(@class,"popover-content")]' +
            '//button[contains(@class,"archive")]').click()
        self.teacher.find(
            By.XPATH, '//span[contains(text(),"View Archived")]').click()
        self.teacher.find(
            By.XPATH, '//div[@class="modal-body"]//td[contains(text(),"' +
            period_name + '")]')
        # add the section back
        periods = self.teacher.find_all(
            By.XPATH, '//div[@class="modal-body"]//table//tbody//tr')
        for x in range(len(periods)):
            temp_period = self.teacher.find(
                By.XPATH, '//div[@class="modal-body"]//table//tbody' +
                '//tr['+str(x+1)+']/td').text
            if temp_period == period_name:
                self.teacher.find(
                    By.XPATH,
                    '//div[@class="modal-body"]//table//tbody//tr[' +
                    str(x+1) + ']//button//span[contains(text(),"Unarchive")]'
                ).click()
                break

        self.ps.test_updates['passed'] = True

    # Case C8265 - 008 - Teacher | Move a student to another period
    @pytest.mark.skipif(str(8265) not in TESTS, reason='Excluded')
    def test_teacher_mover_a_student_to_another_period_8265(self):
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
        self.ps.test_updates['tags'] = ['t1', 't1.42', 't1.42.008', '8265']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.find(
            By.XPATH, '//a[@aria-describedby="change-period"]').click()
        student_name = self.teacher.find(
            By.XPATH, '//div[@class="roster"]//td').text
        element = self.teacher.find(
            By.XPATH, '//div[@class="popover-content"]//a')
        period_name = element.text
        element.click()
        self.teacher.sleep(1)
        self.teacher.find(
            By.XPATH, '//li/a[contains(text(),"'+period_name+'")]').click()
        self.teacher.driver.find_element(
            By.XPATH, '//td[contains(text(),"%s")]' % student_name)

        self.ps.test_updates['passed'] = True

    # Case C8266 - 009 - Teacher | Drop a student
    @pytest.mark.skipif(str(8266) not in TESTS, reason='Excluded')
    def test_teacher_drop_a_student_8266(self):
        """Drop a student.

        Steps:
        Click on the user menu in the upper right corner of the page
        Click "Course Roster"
        Click "Drop" for a student under the Roster section
        Click "Drop" in the box that pops up

        Expected Result:
        A student is dropped from the course and
        is put under the Dropped Students section
        """
        self.ps.test_updates['name'] = 't1.42.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.42', 't1.42.009', '8266']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        student_name = self.teacher.find(
            By.XPATH, '//div[@class="roster"]//td').text
        self.teacher.find(
            By.XPATH, '//a[@aria-describedby="drop-student"]').click()
        self.teacher.find(
            By.XPATH, '//div[@class="popover-content"]//button').click()
        self.teacher.sleep(1)
        # check that student was droped
        print(student_name)
        self.teacher.find(
            By.XPATH, '//div[contains(@class,"dropped-students")]' +
            '//td[contains(text(),"%s")]' % student_name
        )

        self.ps.test_updates['passed'] = True

    # Case C8267 - 010 - Teacher | Readd a dropped student
    @pytest.mark.skipif(str(8267) not in TESTS, reason='Excluded')
    def test_teacher_readd_a_dropped_student_8267(self):
        """Readd a dropped student.

        Steps:
        Click "Add Back to Active Roster" for a student under
            the Dropped Students section
        Click "Add" on the box that pops up

        Expected Result:
        A student is added back to the course
        """
        self.ps.test_updates['name'] = 't1.42.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.42', 't1.42.010', '8267']
        self.ps.test_updates['passed'] = False

        # drop a student (to make sure there is someone to add back)
        student_name = self.teacher.find(
            By.XPATH, '//div[@class="roster"]//td').text
        self.teacher.find(
            By.XPATH, '//a[@aria-describedby="drop-student"]').click()
        self.teacher.find(
            By.XPATH, '//div[@class="popover-content"]//button').click()
        self.teacher.sleep(1)
        # add a student back (not necessarily the same student)
        element = self.teacher.find(
            By.XPATH, '//div[contains(@class,"dropped-students")]' +
            '//span[contains(text(),"Add Back to Active Roster")]')
        self.teacher.driver.execute_script(
            'return arguments[0].scrollIntoView();', element)
        self.teacher.driver.execute_script('window.scrollBy(0, -80);')
        element.click()
        self.teacher.find(
            By.XPATH, '//div[@class="popover-content"]//button').click()
        # check that student was added back
        self.teacher.find(
            By.XPATH,
            '//div[@class="roster"]//td[contains(text(),"%s")]' % student_name)

        self.ps.test_updates['passed'] = True

    # Case C58356 - 011 - Teacher | Unarchive an empty period
    @pytest.mark.skipif(str(58356) not in TESTS, reason='Excluded')
    def test_teacher_unarchive_an_empty_period_58356(self):
        """Unarchive an empty period.

        Steps:
        Go to Tutor
        Click on the 'Login' button
        Enter the teacher user account [ teacher001 ] and password in the boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a Tutor course name
        Click on the user menu in the upper right corner of the page
        Click "Course Settings and Roster"
        Click "View Archived Period(s)"
        Click Unarchived period next to selected course

        Expected Result:
        Period is made active.
        """
        self.ps.test_updates['name'] = 't1.42.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.42', 't1.42.011', '58356']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
