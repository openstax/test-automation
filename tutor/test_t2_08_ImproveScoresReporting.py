"""Tutor v2, Epic 8 - Improve Scores Reporting."""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
# from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
# from selenium.webdriver.support import expected_conditions as expect
# from staxing.assignment import Assignment

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Teacher

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
        14827, 14828, 14830, 14831, 14832,
        14833,
        # not implemented
        # 14671, 14829, 14834, 14835, 14836
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestImproveScoresReporting(unittest.TestCase):
    """T2.08 - Improve Scores Reporting."""

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

    def tearDown(self):
        """Test destructor."""
        if not LOCAL_RUN:
            self.ps.update_job(
                job_id=str(self.teacher.driver.session_id),
                **self.ps.test_updates
            )
        try:
            self.teacher.delete()
        except:
            pass

    # 14671 - 001 - Teacher | View a Scores Export for my students' work
    @pytest.mark.skipif(str(14671) not in TESTS, reason='Excluded')
    def test_teacher_view_a_scores_export_for_my_students_work_14671(self):
        """View a Scores Export for my students' work.

        Steps:
        Go to Tutor
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a Tutor course name
        Click "Student Scores" from calendar dashboard
        Click "Export"

        Expected Result:
        The user is presented with a scores export
        """
        self.ps.test_updates['name'] = 't2.08.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.08',
            't2.08.001',
            '14671'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    '''
    # 14672 - 002 - Teacher | Import Tutor high school Student Scores export
    # into a gradebook
    @pytest.mark.skipif(str(14672) not in TESTS, reason='Excluded')
    def test_teacher_import_tutor_hs_student_scores_export_14672(self):
        """Import Tutor high school Student Scores export into a gradebook.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.08.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.08',
            't2.08.002',
            '14672'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
    '''

    '''
    # 14674 - 003 - Teacher | Import Tutor college Student Scores export into
    # an LMS
    @pytest.mark.skipif(str(14674) not in TESTS, reason='Excluded')
    def test_teacher_import_tutor_college_student_scores_14674(self):
        """Import Tutor college Student Scores export into an LMS.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.08.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.08',
            't2.08.003',
            '14674'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
    '''

    '''
    # 14826 - 004 - Teacher | Import Tutor college Student Scores into an LMS
    @pytest.mark.skipif(str(14826) not in TESTS, reason='Excluded')
    def test_teacher_import_tutor_college_student_scores_into_lms_14826(self):
        """Import Tutor college Student Scores into an LMS.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.08.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.08',
            't2.08.004',
            '14826'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
    '''

    # 14827 - 005 - Teacher | View the overall score column
    @pytest.mark.skipif(str(14827) not in TESTS, reason='Excluded')
    def test_teacher_view_the_overall_score_column_14827(self):
        """View the overall score column.

        Steps:
        If the user has more than one course, click on a Tutor course name
        Click "Student Scores" from calendar dashboard

        Expected Result:
        The user is presented with the overall score column
        """
        self.ps.test_updates['name'] = 't2.08.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.08',
            't2.08.005',
            '14827'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='college_physics')

        assert('course' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Student Scores').click()

        assert('scores' in self.teacher.current_url()), \
            'Not viewing Student Scores'

        self.teacher.sleep(5)

        self.teacher.find(By.XPATH, "//div[@class='overall-header-cell']")

        self.teacher.sleep(5)

        self.ps.test_updates['passed'] = True

    # 14828 - 006 - Teacher | Overall score percentage does not change format
    # when selecting Number in the Percentage/Number toggle
    @pytest.mark.skipif(str(14828) not in TESTS, reason='Excluded')
    def test_teacher_overall_score_percentage_does_not_change_form_14828(self):
        """Overall score percentage does not change format.

        Steps:
        If the user has more than one course, click on a Tutor course name
        Click "Student Scores" from calendar dashboard
        Click "Number"

        Expected Result:
        Overall score percentage does not change format when selecting Number
        in the Percentage/Number toggle
        """
        self.ps.test_updates['name'] = 't2.08.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.08',
            't2.08.006',
            '14828'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='college_physics')

        assert('course' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Student Scores').click()

        assert('scores' in self.teacher.current_url()), \
            'Not viewing Student Scores'

        self.teacher.sleep(5)

        average1 = self.teacher.find(By.XPATH, "//div[@class='average']").text
        self.teacher.find(
            By.XPATH, "//button[@class='btn btn-sm btn-default']").click()
        self.teacher.sleep(3)
        average2 = self.teacher.find(By.XPATH, "//div[@class='average']").text

        assert(average1 == average2), \
            'Overall average is not the same between percentage and number'

        self.ps.test_updates['passed'] = True

    # 14829 - 007 - Teacher | No score is displayed for readings
    @pytest.mark.skipif(str(14829) not in TESTS, reason='Excluded')
    def test_teacher_no_score_is_displayed_for_reading_14829(self):
        """No score is displayed for readings.

        Steps:
        If the user has more than one course, click on a Tutor course name
        Click "Student Scores" from calendar dashboard
        Look for a reading assignment

        Expected Result:
        The user is presented with progress icon but no score
        """
        self.ps.test_updates['name'] = 't2.08.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.08',
            't2.08.007',
            '14829'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 14830 - 008 - Teacher | The class average info icon displays a definition
    # of how class and overall scores are calculated
    @pytest.mark.skipif(str(14830) not in TESTS, reason='Excluded')
    def test_teacher_the_class_average_info_icon_displayed_a_defin_14830(self):
        """The class average info icon displays a definition.

        Steps:
        If the user has more than one course, click on a Tutor course name
        Click "Student Scores" from calendar dashboard
        Click on the info icon next to "Class Average"

        Expected Result:
        The class average info icon displays a definition of how class and
        overall scores are calculated
        """
        self.ps.test_updates['name'] = 't2.08.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.08',
            't2.08.008',
            '14830'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='college_physics')

        assert('course' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Student Scores').click()

        assert('scores' in self.teacher.current_url()), \
            'Not viewing Student Scores'

        self.teacher.sleep(5)
        self.teacher.find(
            By.XPATH,
            "//i[@class='tutor-icon fa fa-info-circle clickable']").click()
        self.teacher.sleep(2)
        self.teacher.find(By.XPATH, "//div[@class='popover-content']")

        self.ps.test_updates['passed'] = True

    # 14831 - 009 - Teacher | Accept late work
    @pytest.mark.skipif(str(14831) not in TESTS, reason='Excluded')
    def test_teacher_accept_late_work_14831(self):
        """Accept late work.

        Steps:
        If the user has more than one course, click on a Tutor course name
        Click "Student Scores" from calendar dashboard
        Click on the orange triangle in the upper right corner of a progress
            cell
        Click "Accept late score"

        Expected Result:
        The late score replaces the score at due date
        """
        self.ps.test_updates['name'] = 't2.08.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.08',
            't2.08.009',
            '14831'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='college_physics')

        assert('course' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Student Scores').click()

        assert('scores' in self.teacher.current_url()), \
            'Not viewing Student Scores'

        self.teacher.sleep(10)

        found = False

        scrollbar = self.teacher.find(
            By.XPATH,
            "//div[@class='ScrollbarLayout_main " +
            "ScrollbarLayout_mainHorizontal public_Scrollbar_main " +
            "public_Scrollbar_mainOpaque']")
        scrollbar.click()

        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(scrollbar)
        actions.click(scrollbar)
        actions.perform()

        newbar = self.teacher.find(
            By.XPATH,
            "//div[@class='ScrollbarLayout_main " +
            "ScrollbarLayout_mainHorizontal public_Scrollbar_main " +
            "public_Scrollbar_mainOpaque public_Scrollbar_mainActive']")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(newbar)
        actions.click(newbar)
        actions.perform()
        scrolls = 0
        # Four arrow rights bring a new assignment into view, try to bring
        # Bring three new assignments into view at a time
        for num in range(100):
            for num1 in range(12):
                newbar.send_keys(Keys.ARROW_RIGHT)
            if len(self.teacher.driver.find_elements_by_xpath(
                "//div[@class='late-caret']")
            ) > 0:
                for num2 in range(5):
                    newbar.send_keys(Keys.ARROW_RIGHT)
                while not found:
                    try:
                        caret = self.teacher.find(
                            By.XPATH, "//div[@class='late-caret']")

                        self.teacher.sleep(3)
                        caret.click()

                        self.teacher.find(
                            By.XPATH,
                            "//button[@class='late-button btn btn-default']"
                        ).click()

                        """
                        self.teacher.find_elements_by_xpath(
                            By.XPATH, "//div[@class='late-caret accepted']"
                        )[index].click()

                        self.teacher.find(
                            By.XPATH,
                            "//button[@class='late-button btn btn-default']"
                        ).click()
                        """
                        found = True
                        break

                    except:

                        if scrolls == 20:
                            break
                        try:
                            scrollbar = self.teacher.find(
                                By.XPATH,
                                "//div[@class='ScrollbarLayout_main " +
                                "ScrollbarLayout_mainVertical " +
                                "public_Scrollbar_main']")

                            scrollbar.click()

                        except:
                            pass

                        newbar = self.teacher.find(
                            By.XPATH,
                            "//div[@class='ScrollbarLayout_main " +
                            "ScrollbarLayout_mainVertical " +
                            "public_Scrollbar_main " +
                            "public_Scrollbar_mainActive']")

                        actions = ActionChains(self.teacher.driver)
                        actions.move_to_element(newbar)
                        actions.click(newbar)
                        actions.perform()
                        for i in range(3):
                            scrolls += 1
                            newbar.send_keys(Keys.ARROW_DOWN)

                break

        lates = self.teacher.driver.find_elements_by_xpath(
            "//div[@class='late-caret accepted']"
        )

        revert = False
        if found:
            for item in lates:
                try:
                    item.click()
                    self.teacher.find(
                        By.XPATH,
                        "//button[@class='late-button btn btn-default']"
                    ).click()
                    revert = True
                    break

                except:
                    pass

        self.teacher.sleep(5)
        assert(found), \
            'Not found'

        assert(revert), \
            'Didnt revert'

        self.ps.test_updates['passed'] = True

    # 14832 - 010 - Teacher | Un-accept late work
    @pytest.mark.skipif(str(14832) not in TESTS, reason='Excluded')
    def test_teacher_unaccept_late_work_14832(self):
        """Un-accept late work.

        Steps:
        If the user has more than one course, click on a Tutor course name
        Click "Student Scores" from calendar dashboard
        Click on the gray triangle in the upper right corner of a progress cell
        Click "Use this score"

        Expected Result:
        The score is converted back to the score at due date
        """
        self.ps.test_updates['name'] = 't2.08.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.08',
            't2.08.010',
            '14832'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='college_physics')

        assert('course' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Student Scores').click()

        assert('scores' in self.teacher.current_url()), \
            'Not viewing Student Scores'

        self.teacher.sleep(10)

        found = False

        scrollbar = self.teacher.find(
            By.XPATH,
            "//div[@class='ScrollbarLayout_main " +
            "ScrollbarLayout_mainHorizontal public_Scrollbar_main " +
            "public_Scrollbar_mainOpaque']")
        scrollbar.click()

        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(scrollbar)
        actions.click(scrollbar)
        actions.perform()

        newbar = self.teacher.find(
            By.XPATH,
            "//div[@class='ScrollbarLayout_main " +
            "ScrollbarLayout_mainHorizontal public_Scrollbar_main " +
            "public_Scrollbar_mainOpaque public_Scrollbar_mainActive']")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(newbar)
        actions.click(newbar)
        actions.perform()
        scrolls = 0
        # Four arrow rights bring a new assignment into view, try to bring
        # Bring three new assignments into view at a time
        for num in range(100):
            for num1 in range(12):
                newbar.send_keys(Keys.ARROW_RIGHT)
            if len(self.teacher.driver.find_elements_by_xpath(
                "//div[@class='late-caret accepted']")
            ) > 0:
                for num2 in range(3):
                    newbar.send_keys(Keys.ARROW_RIGHT)
                while not found:
                    try:

                        caret = self.teacher.find(
                            By.XPATH, "//div[@class='late-caret accepted']"
                        )
                        self.teacher.sleep(2)
                        caret.click()
                        self.teacher.sleep(5)

                        self.teacher.find(
                            By.XPATH,
                            "//button[@class='late-button btn btn-default']"
                        ).click()
                        self.teacher.sleep(5)

                        """
                        self.teacher.find_elements_by_xpath(
                            By.XPATH, "//div[@class='late-caret accepted']"
                        )[index].click()

                        self.teacher.find(
                            By.XPATH,
                            "//button[@class='late-button btn btn-default']"
                        ).click()
                        """
                        found = True
                        break

                    except:

                        if scrolls == 20:
                            break
                        try:
                            scrollbar = self.teacher.find(
                                By.XPATH,
                                "//div[@class='ScrollbarLayout_main " +
                                "ScrollbarLayout_mainVertical " +
                                "public_Scrollbar_main']")

                            scrollbar.click()

                        except:
                            pass

                        newbar = self.teacher.find(
                            By.XPATH,
                            "//div[@class='ScrollbarLayout_main " +
                            "ScrollbarLayout_mainVertical " +
                            "public_Scrollbar_main " +
                            "public_Scrollbar_mainActive']")

                        actions = ActionChains(self.teacher.driver)
                        actions.move_to_element(newbar)
                        actions.click(newbar)
                        actions.perform()
                        for i in range(1):
                            scrolls += 1
                            newbar.send_keys(Keys.ARROW_DOWN)

                break

        lates = self.teacher.driver.find_elements_by_xpath(
            "//div[@class='late-caret']"
        )

        revert = False
        if found:
            for item in lates:
                try:
                    item.click()
                    self.teacher.find(
                        By.XPATH,
                        "//button[@class='late-button btn btn-default']"
                    ).click()
                    revert = True
                    break

                except:
                    pass

        self.teacher.sleep(5)
        assert(found), \
            'Not found'

        assert(revert), \
            'Didnt revert'

        self.ps.test_updates['passed'] = True

    # 14833 - 011 - Teacher | When accepting late work, the progress icon
    # changes to reflect the last worked progress
    @pytest.mark.skipif(str(14833) not in TESTS, reason='Excluded')
    def test_teacher_when_accepting_late_work_the_progress_icon_ch_14833(self):
        """The progress icon changes to reflect the last worked progress.

        Steps:
        If the user has more than one course, click on a Tutor course name
        Click "Student Scores" from calendar dashboard
        Click on the orange triangle in the upper right corner of a
            progress cell
        Click "Accept late score"

        Expected Result:
        The progress icon changes to reflect the last worked progress
        """
        self.ps.test_updates['name'] = 't2.08.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.08',
            't2.08.011',
            '14833'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.select_course(appearance='college_physics')

        assert('course' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Student Scores').click()

        assert('scores' in self.teacher.current_url()), \
            'Not viewing Student Scores'

        self.teacher.sleep(10)

        found = False

        # Setup scrollbar for scrolling
        scrollbar = self.teacher.find(
            By.XPATH,
            "//div[@class='ScrollbarLayout_main " +
            "ScrollbarLayout_mainHorizontal public_Scrollbar_main " +
            "public_Scrollbar_mainOpaque']")
        scrollbar.click()

        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(scrollbar)
        actions.click(scrollbar)
        actions.perform()

        newbar = self.teacher.find(
            By.XPATH,
            "//div[@class='ScrollbarLayout_main " +
            "ScrollbarLayout_mainHorizontal public_Scrollbar_main " +
            "public_Scrollbar_mainOpaque public_Scrollbar_mainActive']")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(newbar)
        actions.click(newbar)
        actions.perform()
        scrolls = 0

        p = False
        for i in range(6):
            newbar.send_keys(Keys.PAGE_UP)
        self.teacher.sleep(3)
        # Four arrow rights bring a new assignment into view, try to bring
        # Bring three new assignments into view at a time
        for num in range(100):
            for num1 in range(12):
                newbar.send_keys(Keys.ARROW_RIGHT)
            if len(self.teacher.driver.find_elements_by_xpath(
                "//div[@class='late-caret']")
            ) > 0:
                for num2 in range(3):
                    newbar.send_keys(Keys.ARROW_RIGHT)

                while not found:
                    try:
                        caret = self.teacher.find(
                            By.XPATH, "//div[@class='late-caret']")

                        try:
                            parent = caret.find_element_by_xpath(
                                "..").find_element_by_xpath("..")
                        except:
                            pass
                        try:
                            worked = parent.find_element_by_class_name(
                                "worked")
                        except:
                            pass
                        try:
                            not_started = worked.find_elements_by_class_name(
                                "not-started")
                        except:
                            pass

                        try:
                            if len(worked.find_elements_by_tag_name(
                                'path')
                            ) > 0:
                                p = True

                        except:
                            pass

                        caret1 = caret.find_element_by_xpath("..")

                        caret1.click()
                        self.teacher.find(
                            By.XPATH,
                            "//button[@class='late-button btn btn-default']"
                        ).click()
                        found = True
                        break

                    # Scroll down if the late assignment is not immediately
                    # visible, continue to scroll until found
                    except:

                        if scrolls == 20:
                            break
                        try:
                            scrollbar = self.teacher.find(
                                By.XPATH,
                                "//div[@class='ScrollbarLayout_main " +
                                "ScrollbarLayout_mainVertical " +
                                "public_Scrollbar_main']")

                            scrollbar.click()

                        except:
                            pass

                        newbar = self.teacher.find(
                            By.XPATH,
                            "//div[@class='ScrollbarLayout_main " +
                            "ScrollbarLayout_mainVertical " +
                            "public_Scrollbar_main " +
                            "public_Scrollbar_mainActive']")

                        actions = ActionChains(self.teacher.driver)
                        actions.move_to_element(newbar)
                        actions.click(newbar)
                        actions.perform()
                        for i in range(1):
                            scrolls += 1
                            newbar.send_keys(Keys.ARROW_DOWN)

                break

        revert = False
        diff = False

        # Case if assignment was not started at all before due date
        if len(not_started) > 0:
            slice_late = worked.find_elements_by_tag_name('circle')
            assert(slice_late[0].get_attribute('class') == 'slice late'), \
                'No change'

            diff = True

        # Case if assignment was partially complete before due date
        else:
            assert(p)
            assert(len(worked.find_elements_by_tag_name('path')) == 0), \
                'No change'

            diff = True

        assert(diff), \
            'No change'

        item = worked.find_element_by_xpath(
            "//div[@class='late-caret accepted']")

        item.click()
        self.teacher.find(
            By.XPATH,
            "//button[@class='late-button btn btn-default']"
        ).click()
        revert = True

        self.teacher.sleep(5)
        assert(found), \
            'Not found'

        assert(revert), \
            'Didnt revert'

        self.ps.test_updates['passed'] = True

    # 14834 - 012 - Teacher | Assignments that are not due yet are not
    # displayed
    @pytest.mark.skipif(str(14834) not in TESTS, reason='Excluded')
    def test_teacher_assignments_that_are_not_due_yet_are_not_disp_14834(self):
        """Assignment that is not due yet is not displayed.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.08.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.08',
            't2.08.012',
            '14834'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 14835 - 013 - Teacher | Supress columns in Score Report
    @pytest.mark.skipif(str(14835) not in TESTS, reason='Excluded')
    def test_teacher_suppress_columns_in_score_report_14835(self):
        """Supress columns in Score Report.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.08.013' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.08',
            't2.08.013',
            '14835'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 14836 - 014 - Teacher | External assignments are not included in the
    # scores export
    @pytest.mark.skipif(str(14836) not in TESTS, reason='Excluded')
    def test_teacher_external_assignments_are_not_included_in_the_14836(self):
        """External assignments are not included in the scores export.

        Steps:
        If the user has more than one course, click on a Tutor course name
        Click "Student Scores" from calendar dashboard
        Click "Export"

        Expected Result:
        External assignments are not included in the scores export
        """
        self.ps.test_updates['name'] = 't2.08.014' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.08',
            't2.08.014',
            '14836'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
