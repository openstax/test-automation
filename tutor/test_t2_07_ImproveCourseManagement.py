"""Tutor v2, Epic 7 - Improve Course Management."""

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

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Admin, Teacher

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
        14651, 14652, 14653, 14655, 14656,
        14657, 14850, 14658, 14660, 14661
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestImproveCourseManagement(unittest.TestCase):
    """T2.07 - Improve Course Management."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.teacher = Teacher(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        self.admin = Admin(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities,
            existing_driver=self.teacher.driver
        )

    def tearDown(self):
        """Test destructor."""
        if not LOCAL_RUN:
            self.ps.update_job(
                job_id=str(self.teacher.driver.session_id),
                **self.ps.test_updates
            )
        self.admin = None
        try:
            self.teacher.delete()
        except:
            pass

    # 14651 - 001 - Admin | View Student Use Statistics for Concept Coach
    # college assessments
    @pytest.mark.skipif(str(14651) not in TESTS, reason='Excluded')
    def test_admin_view_student_use_statistics_for_cc_college_asse_14651(self):
        """View Student Use Statistics for Concept Coach college assessments.

        Steps:
        Go to Tutor
        Click on the 'Login' button
        Enter the admin account in the username and password text boxes
        Click on the 'Sign in' button
        Click "Admin" in the user menu
        Click "Stats"
        Click "Concept Coach"

        Expected Result:
        The user is presented with Concept Coach statistics
        """
        self.ps.test_updates['name'] = 't2.07.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.07',
            't2.07.001',
            '14651'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.login()
        self.admin.goto_admin_control()
        self.admin.sleep(5)
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Stats')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Concept Coach')
            )
        ).click()

        assert('/stats/concept_coach' in self.admin.current_url()), \
            'Not viewing Concept Coach stats'

        self.ps.test_updates['passed'] = True

    # 14652 - 002 - Teacher | Delegate teaching tasks to supporting instructors
    @pytest.mark.skipif(str(14652) not in TESTS, reason='Excluded')
    def test_teacher_delegate_teaching_tasks_to_supporting_instruc_14652(self):
        """Delegate teaching tasks to supporting instructors.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.07.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.07',
            't2.07.002',
            '14652'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 14653 - 003 - Teacher | Move a student and their data to a new section
    @pytest.mark.skipif(str(14653) not in TESTS, reason='Excluded')
    def test_teacher_move_a_student_and_their_data_to_new_section_14653(self):
        """Move a student and their data to a new section.

        Steps:
        If the user has more than one course, click on a Tutor course name
        Click "Course Settings and Roster" from the user menu
        Click "Change Period" for the desired student and select a period

        Expected Result:
        Student is moved to new section with their data
        """
        self.ps.test_updates['name'] = 't2.07.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.07',
            't2.07.003',
            '14653'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.select_course(appearance='physics')
        self.teacher.open_user_menu()
        self.teacher.find(
            By.PARTIAL_LINK_TEXT, "Course Settings and Roster").click()
        self.teacher.sleep(5)

        # Move the student to another period
        first = self.teacher.find(
            By.XPATH,
            "//div[@class='period']/table[@class='roster table table-striped" +
            " table-bordered table-condensed table-hover']/tbody/tr[1]/td[1]"
        ).text
        last = self.teacher.find(
            By.XPATH,
            "//div[@class='period']/table[@class='roster table table-striped" +
            " table-bordered table-condensed table-hover']/tbody/tr[1]/td[2]"
        ).text

        self.teacher.find(By.PARTIAL_LINK_TEXT, "Change Period").click()
        self.teacher.sleep(1)
        self.teacher.find(
            By.XPATH, "//ul[@class='nav nav-pills nav-stacked']/li/a").click()

        self.teacher.sleep(5)

        # Verify the move, then move the student back to the original period
        self.teacher.find(
            By.XPATH,
            "//div[@class='roster']/div[@class='settings-section periods']" +
            "/ul[@class='nav nav-tabs']/li[2]/a").click()
        roster = self.teacher.driver.find_elements_by_xpath(
            "//div[@class='period']/table[@class='roster table table-striped" +
            " table-bordered table-condensed table-hover']/tbody/tr")
        index = 0
        for student in roster:
            if student.text.find(first) >= 0 and student.text.find(last) >= 0:
                self.teacher.driver.find_elements_by_partial_link_text(
                    "Change Period")[index].click()
                self.teacher.sleep(1)
                self.teacher.find(
                    By.XPATH,
                    "//ul[@class='nav nav-pills nav-stacked']/li/a").click()
                break
            index += 1

        self.teacher.sleep(2)
        self.teacher.find(
            By.XPATH,
            "//div[@class='roster']/div[@class='settings-section periods']" +
            "/ul[@class='nav nav-tabs']/li[1]/a").click()
        roster = self.teacher.driver.find_elements_by_xpath(
            "//div[@class='period']/table[@class='roster table table-striped" +
            " table-bordered table-condensed table-hover']/tbody/tr")

        assert(first in roster[0].text and last in roster[0].text), \
            'error'

        self.ps.test_updates['passed'] = True

    # 14655 - 004 - Teacher | Drop a student from a section and hide their data
    @pytest.mark.skipif(str(14655) not in TESTS, reason='Excluded')
    def test_teacher_drop_student_from_section_and_hide_their_data_14655(self):
        """Drop a student from a section and hide their data.

        Steps:
        If the user has more than one course, click on a Tutor course name
        Click "Course Settings and Roster" from the user menu
        Click "Drop" for the desired student

        Expected Result:
        The student appears under the "Dropped Students" section
        """
        self.ps.test_updates['name'] = 't2.07.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.07',
            't2.07.004',
            '14655'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.select_course(appearance='physics')
        self.teacher.open_user_menu()
        self.teacher.find(
            By.PARTIAL_LINK_TEXT, "Course Settings and Roster").click()
        self.teacher.sleep(5)

        # Drop the student
        first = self.teacher.find(
            By.XPATH,
            "//div[@class='period']/table[@class='roster table table-striped" +
            " table-bordered table-condensed table-hover']/tbody/tr[1]/td[1]"
        ).text
        last = self.teacher.find(
            By.XPATH,
            "//div[@class='period']/table[@class='roster table table-striped" +
            " table-bordered table-condensed table-hover']/tbody/tr[1]/td[2]"
        ).text
        self.teacher.find(By.PARTIAL_LINK_TEXT, "Drop").click()
        self.teacher.sleep(1)
        self.teacher.find(
            By.XPATH,
            "//button[@class='-drop-student btn btn-danger']").click()

        self.teacher.sleep(5)

        # Verify the student was dropped and add back to active roster
        dropped = self.teacher.driver.find_elements_by_xpath(
            "//div[@class='settings-section dropped-students']/table[@class" +
            "='roster table table-striped table-bordered table-condensed " +
            "table-hover']/tbody/tr")
        index = 0
        for student in dropped:
            if student.text.find(first) >= 0 and student.text.find(last) >= 0:
                self.teacher.driver.find_elements_by_partial_link_text(
                    "Add Back to Active Roster")[index].click()
                self.teacher.sleep(1)
                self.teacher.find(
                    By.XPATH,
                    "//button[@class='-undrop-student btn btn-success']"
                ).click()
                self.teacher.sleep(20)
                break
            index += 1

        self.ps.test_updates['passed'] = True

    # 14656 - 005 - Teacher | Drop a student from a section and don't hide
    # their data
    @pytest.mark.skipif(str(14656) not in TESTS, reason='Excluded')
    def test_teacher_drop_a_student_from_section_and_dont_hide_dat_14656(self):
        """Drop a student from a section and don't hide their data.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.07.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.07',
            't2.07.005',
            '14656'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 14657 - 006 - Teacher | In Student Scores dropped students are not
    # displayed
    @pytest.mark.skipif(str(14657) not in TESTS, reason='Excluded')
    def test_teacher_in_student_scores_dropped_students_are_not_14657(self):
        """In Student Scores dropped students are not displayed.

        Steps:
        If the user has more than one course, click on a Tutor course name
        Click "Course Settings and Roster" from the calendar dashboard
        Click "Drop" for the desired student
        Click "Student Scores" from the user menu
        Click on the period from which you have dropped the student

        Expected Result:
        Dropped student should not be displayed in Student Scores
        """
        self.ps.test_updates['name'] = 't2.07.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.07',
            't2.07.006',
            '14657'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.select_course(appearance='physics')
        self.teacher.open_user_menu()
        self.teacher.find(
            By.PARTIAL_LINK_TEXT, "Course Settings and Roster").click()
        self.teacher.sleep(5)

        # Drop the student
        first = self.teacher.find(
            By.XPATH,
            "//div[@class='period']/table[@class='roster table table-striped" +
            " table-bordered table-condensed table-hover']/tbody/tr[1]/td[1]"
        ).text
        last = self.teacher.find(
            By.XPATH,
            "//div[@class='period']/table[@class='roster table table-striped" +
            " table-bordered table-condensed table-hover']/tbody/tr[1]/td[2]"
        ).text

        self.teacher.find(By.PARTIAL_LINK_TEXT, "Drop").click()
        self.teacher.sleep(1)
        self.teacher.find(
            By.XPATH,
            "//button[@class='-drop-student btn btn-danger']").click()

        self.teacher.sleep(5)

        # Go to student scores, verify the student is not seen
        self.teacher.open_user_menu()
        self.teacher.find(
            By.PARTIAL_LINK_TEXT, "Student Scores").click()
        self.teacher.sleep(10)

        odd_scores = self.teacher.driver.find_elements_by_xpath(
            "//div[@class='fixedDataTableRowLayout_main public_fixedData" +
            "TableRow_main public_fixedDataTableRow_even public_fixedDataTa" +
            "ble_bodyRow']/div[@class='fixedDataTableRowLayout_body']/div" +
            "[@class='fixedDataTableCellGroupLayout_cellGroupWrapper'][1]/d" +
            "iv[@class='fixedDataTableCellGroupLayout_cellGroup']/div[@clas" +
            "s='fixedDataTableCellLayout_main public_fixedDataTableCell_" +
            "main'][1]/div[@class='fixedDataTableCellLayout_wrap1 public_fi" +
            "xedDataTableCell_wrap1']/div[@class='fixedDataTableCellLayout_w" +
            "rap2 public_fixedDataTableCell_wrap2']/div[@class='fixedDataTab" +
            "leCellLayout_wrap3 public_fixedDataTableCell_wrap3']/div[@class" +
            "='name-cell']/a[@class='student-name public_fixedDataTableCell" +
            "_cellContent']")
        even_scores = self.teacher.driver.find_elements_by_xpath(
            "//div[@class='fixedDataTableRowLayout_main public_fixedDataTab" +
            "leRow_main public_fixedDataTableRow_highlighted public_fixedDa" +
            "taTableRow_odd public_fixedDataTable_bodyRow']/div[@class='fix" +
            "edDataTableRowLayout_body']/div[@class='fixedDataTableCellGrou" +
            "pLayout_cellGroupWrapper'][1]/div[@class='fixedDataTableCellGr" +
            "oupLayout_cellGroup']/div[@class='fixedDataTableCellLayout_mai" +
            "n public_fixedDataTableCell_main'][1]/div[@class='fixedDataTab" +
            "leCellLayout_wrap1 public_fixedDataTableCell_wrap1']/div[@clas" +
            "s='fixedDataTableCellLayout_wrap2 public_fixedDataTableCell_wr" +
            "ap2']/div[@class='fixedDataTableCellLayout_wrap3 public_fixedD" +
            "ataTableCell_wrap3']/div[@class='name-cell']/a[@class='student" +
            "-name public_fixedDataTableCell_cellContent']")

        found = False
        for student in odd_scores:
            if student.text.find(first) >= 0 and student.text.find(last) >= 0:
                found = True
                break

        if not found:
            for stud in even_scores:
                if stud.text.find(first) >= 0 and stud.text.find(last) >= 0:
                    found = True
                    break

        # Add back to active roster
        self.teacher.open_user_menu()
        self.teacher.find(
            By.PARTIAL_LINK_TEXT, "Course Settings and Roster").click()
        dropped = self.teacher.driver.find_elements_by_xpath(
            "//div[@class='settings-section dropped-students']/table[@class" +
            "='roster table table-striped table-bordered table-condensed ta" +
            "ble-hover']/tbody/tr")
        index = 0
        for student in dropped:
            if student.text.find(first) >= 0 and student.text.find(last) >= 0:
                self.teacher.driver.find_elements_by_partial_link_text(
                    "Add Back to Active Roster")[index].click()
                self.teacher.sleep(1)
                self.teacher.find(
                    By.XPATH,
                    "//button[@class='-undrop-student btn btn-success']"
                ).click()
                self.teacher.sleep(20)
                break
            index += 1

        if not found:
            self.ps.test_updates['passed'] = True

    # 14850 - 007 - Teacher | In Student Scores view moved students
    @pytest.mark.skipif(str(14850) not in TESTS, reason='Excluded')
    def test_teacher_in_student_scores_view_moved_students_14850(self):
        """In Student Scores view moved students.

        Steps:
        If the user has more than one course, click on a Tutor course name
        Click "Course Settings and Roster" from the calendar dashboard
        Click "Change Period" for the desired student
        Click on the desired period
        Click "Student Scores" from the user menu
        Click on the period to which the student was moved

        Expected Result:
        The user is presented with the moved student under their new period
        """
        self.ps.test_updates['name'] = 't2.07.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.07',
            't2.07.007',
            '14850'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.select_course(appearance='physics')
        self.teacher.open_user_menu()
        self.teacher.find(
            By.PARTIAL_LINK_TEXT, "Course Settings and Roster").click()
        self.teacher.sleep(5)

        # Move the student to another period
        first = self.teacher.find(
            By.XPATH,
            "//div[@class='period']/table[@class='roster table table-striped" +
            " table-bordered table-condensed table-hover']/tbody/tr[1]/td[1]"
        ).text
        last = self.teacher.find(
            By.XPATH,
            "//div[@class='period']/table[@class='roster table table-striped" +
            " table-bordered table-condensed table-hover']/tbody/tr[1]/td[2]"
        ).text

        self.teacher.find(By.PARTIAL_LINK_TEXT, "Change Period").click()
        self.teacher.sleep(1)
        self.teacher.find(
            By.XPATH, "//ul[@class='nav nav-pills nav-stacked']/li/a").click()

        self.teacher.sleep(5)

        # Go to student scores, verify the student is seen
        self.teacher.open_user_menu()
        self.teacher.find(
            By.PARTIAL_LINK_TEXT, "Student Scores").click()
        self.teacher.sleep(10)
        self.teacher.find(
            By.XPATH,
            "//nav[@class='collapse in']/ul[@class='nav nav-tabs']/li[2]/a"
        ).click()

        odd_scores = self.teacher.driver.find_elements_by_xpath(
            "//div[@class='fixedDataTableRowLayout_main public_fixedData" +
            "TableRow_main public_fixedDataTableRow_even public_fixedDataTa" +
            "ble_bodyRow']/div[@class='fixedDataTableRowLayout_body']/div" +
            "[@class='fixedDataTableCellGroupLayout_cellGroupWrapper'][1]/d" +
            "iv[@class='fixedDataTableCellGroupLayout_cellGroup']/div[@clas" +
            "s='fixedDataTableCellLayout_main public_fixedDataTableCell_" +
            "main'][1]/div[@class='fixedDataTableCellLayout_wrap1 public_fi" +
            "xedDataTableCell_wrap1']/div[@class='fixedDataTableCellLayout_w" +
            "rap2 public_fixedDataTableCell_wrap2']/div[@class='fixedDataTab" +
            "leCellLayout_wrap3 public_fixedDataTableCell_wrap3']/div[@class" +
            "='name-cell']/a[@class='student-name public_fixedDataTableCell" +
            "_cellContent']")
        even_scores = self.teacher.driver.find_elements_by_xpath(
            "//div[@class='fixedDataTableRowLayout_main public_fixedDataTab" +
            "leRow_main public_fixedDataTableRow_highlighted public_fixedDa" +
            "taTableRow_odd public_fixedDataTable_bodyRow']/div[@class='fix" +
            "edDataTableRowLayout_body']/div[@class='fixedDataTableCellGrou" +
            "pLayout_cellGroupWrapper'][1]/div[@class='fixedDataTableCellGr" +
            "oupLayout_cellGroup']/div[@class='fixedDataTableCellLayout_mai" +
            "n public_fixedDataTableCell_main'][1]/div[@class='fixedDataTab" +
            "leCellLayout_wrap1 public_fixedDataTableCell_wrap1']/div[@clas" +
            "s='fixedDataTableCellLayout_wrap2 public_fixedDataTableCell_wr" +
            "ap2']/div[@class='fixedDataTableCellLayout_wrap3 public_fixedD" +
            "ataTableCell_wrap3']/div[@class='name-cell']/a[@class='student" +
            "-name public_fixedDataTableCell_cellContent']")

        found = False
        for student in odd_scores:
            if student.text.find(first) >= 0 and student.text.find(last) >= 0:
                found = True
                break

        if found:
            for stud in even_scores:
                if stud.text.find(first) >= 0 and stud.text.find(last) >= 0:
                    found = True
                    break

        # Add student back to original period
        self.teacher.open_user_menu()
        self.teacher.find(
            By.PARTIAL_LINK_TEXT, "Course Settings and Roster").click()
        self.teacher.sleep(10)
        self.teacher.find(
            By.XPATH,
            "//div[@class='roster']/div[@class='settings-section periods']" +
            "/ul[@class='nav nav-tabs']/li[2]/a").click()
        roster = self.teacher.driver.find_elements_by_xpath(
            "//div[@class='period']/table[@class='roster table table-striped" +
            " table-bordered table-condensed table-hover']/tbody/tr")
        index = 0
        for student in roster:
            if student.text.find(first) >= 0 and student.text.find(last) >= 0:
                self.teacher.driver.find_elements_by_partial_link_text(
                    "Change Period")[index].click()
                self.teacher.sleep(1)
                self.teacher.find(
                    By.XPATH,
                    "//ul[@class='nav nav-pills nav-stacked']/li/a").click()
                break
            index += 1

        if found:
            self.ps.test_updates['passed'] = True

    # 14658 - 008 - Teacher | Require emails for all students for roster import
    @pytest.mark.skipif(str(14658) not in TESTS, reason='Excluded')
    def test_teacher_require_emails_for_all_students_for_roster_14658(self):
        """Require emails for all students for roster imports.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.07.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.07',
            't2.07.008',
            '14658'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 14660 - 009 - Teacher | Set time zone for a course
    @pytest.mark.skipif(str(14660) not in TESTS, reason='Excluded')
    def test_teacher_set_time_zone_for_a_course_14660(self):
        """Set time zone for a course.

        Steps:
        If the user has more than one course, click on a Tutor course name
        Click "Course Settings and Roster"
        Click "Change Course Timezone"
        Select the desired timezone
        Click Save

        Expected Result:
        The time zone is set
        """
        self.ps.test_updates['name'] = 't2.07.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.07',
            't2.07.009',
            '14660'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.select_course(appearance='physics')
        self.teacher.open_user_menu()
        self.teacher.find(
            By.PARTIAL_LINK_TEXT, "Course Settings and Roster").click()
        self.teacher.sleep(5)

        # Change the timezone
        self.teacher.driver.find_elements_by_xpath(
            "//button[@class='edit-course btn btn-link']")[1].click()
        self.teacher.sleep(2)
        self.teacher.find(
            By.XPATH, "//div[@class='tutor-radio']/label").click()
        self.teacher.find(
            By.XPATH,
            "//button[@class='async-button -edit-course-" +
            "confirm btn btn-default']").click()
        self.teacher.sleep(5)

        # Verify the change and change the time back to Central
        self.teacher.driver.find_elements_by_xpath(
            "//button[@class='edit-course btn btn-link']")[1].click()

        assert('Central Time' not in self.teacher.find(
            By.XPATH, "//div[@class='tutor-radio active']/label").text), \
            'Not viewing Concept Coach stats'

        self.teacher.sleep(2)
        options = self.teacher.driver.find_elements_by_xpath(
            "//div[@class='tutor-radio']/label")

        for timezone in options:
            if timezone.text.find('Central Time') >= 0:
                timezone.click()
                break

        self.teacher.find(
            By.XPATH,
            "//button[@class='async-button -edit-course-" +
            "confirm btn btn-default']").click()

        self.ps.test_updates['passed'] = True

    # 14661 - 010 - System | Distinguish between high school and college
    # courses
    @pytest.mark.skipif(str(14661) not in TESTS, reason='Excluded')
    def test_system_distinguish_between_hs_and_college_courses_14661(self):
        """Distinguish between high school and college courses.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.07.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.07',
            't2.07.010',
            '14661'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
