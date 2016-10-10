"""Concept Coach v2, Epic 8 - Improves Scores Reporting."""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
# from random import randint  # NOQA
from selenium.webdriver.common.by import By  # NOQA
from selenium.webdriver.support import expected_conditions as expect  # NOQA
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
# from staxing.assignment import Assignment  # NOQA
from selenium.webdriver.common.action_chains import ActionChains
from openpyxl import load_workbook, Workbook


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
    # str([14806, 14807, 14808, 14810,
    #      14811, 14668, 14670, 14669,
    #      14812, 14813, 14814, 14815,
    #      14816])  # NOQA
    # str([, 14670, 14812, 14813])
    str([14670, 14668])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestImprovesScoresReporting(unittest.TestCase):
    """CC2.08 - Improves Scores Reporting."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.teacher = Teacher(
            use_env_vars=True,
            # pasta_user=self.ps,
            # capabilities=self.desired_capabilities,
        )
        self.teacher.login()
        self.teacher.driver.find_element(
            By.XPATH, '//a[contains(@href,"/cc-dashboard")]'
        ).click()

    def tearDown(self):
        """Test destructor."""
        self.ps.update_job(job_id=str(self.teacher.driver.session_id),
                           **self.ps.test_updates)
        try:
            self.teacher.delete()
        except:
            pass

    # 14806 - 001 - Teacher | View student scores as percent complete
    @pytest.mark.skipif(str(14806) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_view_student_scores_as_percent_complete_14806(self):
        """View student scores as percent complete.

        Steps:
        Click View Detailed Scores
        Click on percentage

        Expected Result:
        Student Scores are presented as percent complete
        """
        self.ps.test_updates['name'] = 'cc2.08.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.08', 'cc2.08.001', '14806']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[contains(text(),"View Detailed Scores")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[contains(text(),"Student Scores")]')
            )
        )
        self.teacher.driver.find_element(
            By.XPATH, '//button[contains(text(),"percentage")]'
        ).click()
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"score")]//a[contains(text(),"%")]')
        self.ps.test_updates['passed'] = True

    # 14807 - 002 - Teacher | View student scores as number of total
    @pytest.mark.skipif(str(14807) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_view_student_scores_as_number_of_total_14807(self):
        """View student scores as number of total.

        Steps:
        Click View Detailed Scores
        Click "Number"

        Expected Result:
        Student Scores are presented as "Number of Total"
        """
        self.ps.test_updates['name'] = 'cc2.08.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.08', 'cc2.08.002', '14807']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[contains(text(),"View Detailed Scores")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[contains(text(),"Student Scores")]')
            )
        )
        self.teacher.driver.find_element(
            By.XPATH, '//button[contains(text(),"number")]'
        ).click()
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"score")]//a[contains(text()," of ")]')

        self.ps.test_updates['passed'] = True

    # 14808 - 003 - Teacher | View tooltips on hover
    @pytest.mark.skipif(str(14808) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_view_tooltips_on_hover_14808(self):
        """View tooltips on hover.

        Steps:
        Click View Detailed Scores
        Hover over the info icons

        Expected Result:
        The user is presented with tooltips
        """
        self.ps.test_updates['name'] = 'cc2.08.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.08', 'cc2.08.003', '14808']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[contains(text(),"View Detailed Scores")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[contains(text(),"Student Scores")]')
            )
        )
        self.teacher.driver.find_element(
            By.XPATH, '//i[@type="info-circle"]').click()
        self.teacher.driver.find_element(
            By.XPATH,
            '//h3[@class="popover-title" and ' +
            'contains(text(), "Class and Overall Averages")]')
        self.ps.test_updates['passed'] = True

    # 14810 - 004 - Teacher | Sort student scores based on score
    @pytest.mark.skipif(str(14810) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_sort_student_scores_based_on_score_14810(self):
        """Sort student scores based on score.

        Steps:
        Click View Detailed Scores
        Click "Score" for the desired assignment

        Expected Result:
        Students are sorted based on score
        """
        self.ps.test_updates['name'] = 'cc2.08.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.08', 'cc2.08.004', '14810']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[contains(text(),"View Detailed Scores")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[contains(text(),"Student Scores")]')
            )
        )
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"sortable")]//div[text()="Score"]'
        ).click()
        self.teacher.sleep(0.75)
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"is-descending")]//div[text()="Score"]'
        ).click()
        self.teacher.sleep(0.75)
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"is-ascending")]//div[text()="Score"]'
        )
        self.ps.test_updates['passed'] = True

    # 14811 - 005 - Teacher | Sort student scores based on number complete
    @pytest.mark.skipif(str(14811) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_sort_student_scores_based_on_number_completed_14811(self):
        """Sort student scores based on number complete.

        Steps:
        Click View Detailed Scores
        Click "Progress" for the desired assignment

        Expected Result:
        Students are sorted based on number completed

        """
        self.ps.test_updates['name'] = 'cc2.08.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.08', 'cc2.08.005', '14811']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[contains(text(),"View Detailed Scores")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[contains(text(),"Student Scores")]')
            )
        )
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"sortable")]//div[text()="Progress"]'
        ).click()
        self.teacher.sleep(0.75)
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"is-descending")]//div[text()="Progress"]'
        ).click()
        self.teacher.sleep(0.75)
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"is-ascending")]//div[text()="Progress"]'
        )
        self.ps.test_updates['passed'] = True

    # 14668 - 006 - Teacher | All popups in the roster have an X button
    @pytest.mark.skipif(str(14668) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_all_popups_in_the_roster_have_an_x_button_14668(self):
        """All popups in the roster have an X button.

        Steps:
        Click "Course Settings and Roster" from the user menu
        Click "Rename Course," "Change Course Timezone,"
        "Add Period," "Rename," "Get Student Enrollment Code,"
        and "View archived period"
        Expected Result:
        All pop ups have an X button
        """
        self.ps.test_updates['name'] = 'cc2.08.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.08', 'cc2.08.006', '14668']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.open_user_menu()
        self.teacher.driver.find_element(
            By.XPATH, '//a[text()="Course Settings and Roster"]'
        ).click()
        self.teacher.sleep(1)
        # rename couse
        self.teacher.driver.find_element(
            By.XPATH,
            '//button//span[contains(text(),"Rename Course")]'
        ).click()
        self.teacher.sleep(0.75)
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[@class="modal-content"]//button[@class="close"]'
        ).click()
        self.teacher.sleep(0.75)
        # course timezone
        self.teacher.driver.find_element(
            By.XPATH,
            '//button//span[contains(text(),"Change Course Timezone")]'
        ).click()
        self.teacher.sleep(1)
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[@class="modal-content"]//button[@class="close"]'
        ).click()
        self.teacher.sleep(0.75)
        # add period/section
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"add-period")]//button'
        ).click()
        self.teacher.sleep(0.75)
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[@class="modal-content"]//button[@class="close"]'
        ).click()
        self.teacher.sleep(0.75)
        # rename period
        self.teacher.driver.find_element(
            By.XPATH,
            '//span[contains(@class,"rename-period")]//button'
        ).click()
        self.teacher.sleep(0.75)
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[@class="modal-content"]//button[@class="close"]'
        ).click()
        self.teacher.sleep(0.75)
        # student enrollemnt code
        self.teacher.driver.find_element(
            By.XPATH,
            '//button//span[contains(text(),"Your student enrollment code")]'
        ).click()
        self.teacher.sleep(0.75)
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[@class="modal-content"]//button[@class="close"]'
        ).click()
        self.teacher.sleep(0.75)
        # View Archived periods
        self.teacher.driver.find_element(
            By.XPATH,
            '//button//span[contains(text(),"View Archived ")]'
        ).click()
        self.teacher.sleep(0.75)
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[@class="modal-content"]//button[@class="close"]'
        ).click()
        self.ps.test_updates['passed'] = True

    # 14670 - 007 - Teacher | Close popup with X button
    @pytest.mark.skipif(str(14670) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_close_popup_with_x_button_14670(self):
        """Close popup with X button.

        Steps:
        Click "Course Settings and Roster" from the user menu
        Click each of the following then click X on the pop up:
        - Rename Course
        - Change Course Timezone
        - Add Period
        - Rename
        - Get Student Enrollment Code
        - View Archived Periods

        Expected Result:
        Popup is closed
        """
        self.ps.test_updates['name'] = 'cc2.08.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.08', 'cc2.08.007', '14670']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.open_user_menu()
        self.teacher.driver.find_element(
            By.XPATH, '//a[text()="Course Settings and Roster"]'
        ).click()
        self.teacher.sleep(1)
        # rename couse
        self.teacher.driver.find_element(
            By.XPATH,
            '//button//span[contains(text(),"Rename Course")]'
        ).click()
        self.teacher.sleep(0.75)
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[@class="modal-content"]//button[@class="close"]'
        ).click()
        self.teacher.sleep(1)
        with self.assertRaises(NoSuchElementException):
            self.teacher.driver.find_element(
                By.XPATH, '//div[@class="modal-content"]')
        # course timezone
        self.teacher.driver.find_element(
            By.XPATH,
            '//button//span[contains(text(),"Change Course Timezone")]'
        ).click()
        self.teacher.sleep(1)
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[@class="modal-content"]//button[@class="close"]'
        ).click()
        self.teacher.sleep(1)
        with self.assertRaises(NoSuchElementException):
            self.teacher.driver.find_element(
                By.XPATH, '//div[@class="modal-content"]')
        # add period/section
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"add-period")]//button'
        ).click()
        self.teacher.sleep(0.75)
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[@class="modal-content"]//button[@class="close"]'
        ).click()
        self.teacher.sleep(1)
        with self.assertRaises(NoSuchElementException):
            self.teacher.driver.find_element(
                By.XPATH, '//div[@class="modal-content"]')
        # rename period
        self.teacher.driver.find_element(
            By.XPATH,
            '//span[contains(@class,"rename-period")]//button'
        ).click()
        self.teacher.sleep(0.75)
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[@class="modal-content"]//button[@class="close"]'
        ).click()
        self.teacher.sleep(1)
        with self.assertRaises(NoSuchElementException):
            self.teacher.driver.find_element(
                By.XPATH, '//div[@class="modal-content"]')
        # student enrollemnt code
        self.teacher.driver.find_element(
            By.XPATH,
            '//button//span[contains(text(),"Your student enrollment code")]'
        ).click()
        self.teacher.sleep(0.75)
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[@class="modal-content"]//button[@class="close"]'
        ).click()
        self.teacher.sleep(1)
        with self.assertRaises(NoSuchElementException):
            self.teacher.driver.find_element(
                By.XPATH, '//div[@class="modal-content"]')
        # View Archived Periods
        self.teacher.driver.find_element(
            By.XPATH,
            '//button//span[contains(text(),"View Archived")]'
        ).click()
        self.teacher.sleep(0.75)
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[@class="modal-content"]//button[@class="close"]'
        ).click()
        self.teacher.sleep(1)
        with self.assertRaises(NoSuchElementException):
            self.teacher.driver.find_element(
                By.XPATH, '//div[@class="modal-content"]')

        self.ps.test_updates['passed'] = True

    # 14669 - 008 - Teacher | The icon in the progress column shows info on
    # percentage complete, attempted out of total possible questions, and
    # the date last worked
    @pytest.mark.skipif(str(14669) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_the_icon_in_the_progress_column_shows_info_14669(self):
        """The icon in the progress column shows info.

        Steps:
        Click "View Detailed Scores"
        Click on the icon in the progress column for a completed assignment

        Expected Result:
        shows information on percentage complete, attempted out of total
        possible questions as well as the date last worked
        """
        self.ps.test_updates['name'] = 'cc2.08.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.08', 'cc2.08.008', '14669']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[contains(text(),"View Detailed Scores")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[contains(text(),"Student Scores")]')
            )
        )
        icon = self.teacher.driver.find_element(
            By.XPATH,
            '//span[contains(@aria-describedby,"scores-cell-info-popover")]')
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(icon)
        actions.perform()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[contains(@id,"scores-cell-info-popover")]')
            )
        ).click()
        # more on each individial thing
        self.ps.test_updates['passed'] = True

    # 14812 - 009 - Teacher | Import CC Student Scores export into an LMS
    @pytest.mark.skipif(str(14812) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_import_cc_student_scores_export_into_an_lms_14812(self):
        """Import CC student scores export into an LMS.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 'cc2.08.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.08', 'cc2.08.009', '14812']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 14813 - 010 - Teacher | View zeros in exported scores instead of blank
    # cells for incomplete assignments
    @pytest.mark.skipif(str(14813) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_view_zeros_in_exported_scores_instead_of_blan_14813(self):
        """View zeros in exported scores for incomplete assignments.

        Steps:
        Click "View Detailed Scores"
        Click "Export"
        Open the excel file

        Expected Result:
        For incomplete assignments or assignments that are not started,
        there are zeros instead of blank cells
        """
        self.ps.test_updates['name'] = 'cc2.08.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.08', 'cc2.08.010', '14813']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[contains(text(),"View Detailed Scores")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[contains(text(),"Student Scores")]')
            )
        )
        self.teacher.driver.find_element(
            By.XPATH, '//div[@class="export-button"]//button'
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[@class="export-button"]//button' +
                 '/span[text()="Export"]')
            )
        )
        self.teacher.sleep(1)
        coursename = self.teacher.driver.find_element(
             By.XPATH, '//div[@class="course-name"]').text
        coursename = coursename.replace(' ', '_') + "_Scores"
        home = os.getenv("HOME")
        files = os.listdir(home + '/Downloads')
        file_name = ''
        for i in range(len(files)):
            if (coursename in files[i]) and (files[i][-5:] == '.xlsx'):
                file_name = files[i]
                break
            else:
                if i == len(files)-1:
                    raise Exception
        period = self.teacher.driver.find_element(
            By.XPATH, '//span[contains(@class,"tab-item-period-name")]').text
        wb = load_workbook(str(home + '/Downloads/' + file_name))
        sheet = wb[period + ' - %']
        rows = sheet.rows
        start_row = float("inf")
        for i in range(len(sheet.rows)):
            if rows[i][0].value == 'First Name':
                start_row = i
            if i >= start_row:
                if rows[i][4].value == 0:
                    # found that 0% is being used istead of blanks
                    break
                elif rows[i+1][4].value == None:
                    print('empty cell instead of 0%')
                    raise Exception

        self.ps.test_updates['passed'] = True

    # 14814 - 011 - Teacher | Green check icon is displayed for completed
    # assignments
    @pytest.mark.skipif(str(14814) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_green_check_icon_is_displayed_for_completed_14814(self):
        """Green check icon is displayed for completed assignments.

        Steps:
        If the user has more than one course, click on a CC course name
        Click "View Detailed Scores

        Expected Result:
        Green check icon is displayed for completed assignments
        """
        self.ps.test_updates['name'] = 'cc2.08.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.08', 'cc2.08.011', '14814']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[contains(text(),"View Detailed Scores")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[contains(text(),"Student Scores")]')
            )
        )
        # scroll to find a green checkmark
        assignments = self.teacher.driver.find_elements(
            By.XPATH,
            "//span[contains(@aria-describedby,'header-cell-title')]")

        for i in range(len(assignments)//4):
            try:
                self.teacher.driver.find_element(
                    By.XPATH,
                    '//span[contains(@class,"trig")]' +
                    '//*[contains(@class,"finished")]')
                break
            except (NoSuchElementException, ElementNotVisibleException):
                if i >= (len(assignments)//4)-1:
                    print("completed assignments for this period")
                    raise Exception
                # try to drag scroll bar instead of scrolling
                scroll_bar = self.teacher.find(
                    By.XPATH,
                    '//div[contains(@class,"ScrollbarLayout_faceHorizontal")]')
                actions = ActionChains(self.teacher.driver)
                actions.move_to_element(scroll_bar)
                actions.click_and_hold()
                actions.move_by_offset(50, 0)
                actions.release()
                actions.perform()
        self.ps.test_updates['passed'] = True

    # 14815 - 012 - Teacher | The class average info icon displays a definition
    # about scores from completed assignments
    @pytest.mark.skipif(str(14815) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_class_average_info_icon_displays_definition_14815(self):
        """The class average info icon displays a definition.

        Steps:
        Click "View Detailed Scores
        Click on the info icon next to "Class Average"

        Expected Result:
        The class average info icon displays a definition about scores from
        completed assignments

        """
        self.ps.test_updates['name'] = 'cc2.08.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.08', 'cc2.08.012', '14815']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[contains(text(),"View Detailed Scores")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[contains(text(),"Student Scores")]')
            )
        )
        self.teacher.driver.find_element(
            By.XPATH, '//i[@type="info-circle"]').click()
        self.teacher.driver.find_element(
            By.XPATH,
            '//h3[@class="popover-title" and ' +
            'contains(text(), "Class and Overall Averages")]')

        self.ps.test_updates['passed'] = True

    # 14816 - 013 - Teacher | View the overall score column
    @pytest.mark.skipif(str(14816) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_view_the_overall_score_column_14816(self):
        """View the overall score column.

        Steps:
        Click "View Detailed Scores

        Expected Result:
        User is presented with the overall score column next to student names
        """
        self.ps.test_updates['name'] = 'cc2.08.013' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc2', 'cc2.08', 'cc2.08.013', '14816']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[contains(text(),"View Detailed Scores")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[contains(text(),"Student Scores")]')
            )
        )
        self.teacher.driver.find_element(
            By.XPATH, '//div[contains(@class,"overall-header-cell")]')

        self.ps.test_updates['passed'] = True
