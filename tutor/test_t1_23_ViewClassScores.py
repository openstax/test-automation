"""Tutor v1, Epic 23 - View Class Scores."""

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
<<<<<<< HEAD
=======
from selenium.webdriver.support.ui import WebDriverWait
>>>>>>> 92f9fdbfce2e37bb7b040214379ebcf91b5b7461

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Teacher  # NOQA

<<<<<<< HEAD

=======
>>>>>>> 92f9fdbfce2e37bb7b040214379ebcf91b5b7461
basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': '50.0',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
<<<<<<< HEAD
    str([8156, 8157, 8158,
         8159, 8160, 8161, 
         8162, 8163, 8164, 
         8165, 8166, 8167, 
         8168, 8169, 8170, 
         8171, 8172, 8173,
         8174, 8175, 8176,
         8177, 8178, 8179, 
         8180, 8181])  # NOQA
=======
    str([8156, 8157, 8158, 8159, 
         8160, 8161, 8162, 8163,
         8164, 8165, 8166, 8167,
         8168, 8169, 8170, 8171,
         8172, 8173, 8174, 8175, 
         8176, 8177, 8178, 8179,
         8180, 8181])#NOQA
>>>>>>> 92f9fdbfce2e37bb7b040214379ebcf91b5b7461
)


@PastaDecorator.on_platforms(BROWSERS)
<<<<<<< HEAD
class TestEpicName(unittest.TestCase):
=======
class TestViewClassScores(unittest.TestCase):
>>>>>>> 92f9fdbfce2e37bb7b040214379ebcf91b5b7461
    """T1.23 - View Class Scores."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
<<<<<<< HEAD
        self.Teacher = Teacher(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
=======
        self.teacher = Teacher(
            use_env_vars=True#,
            #pasta_user=self.ps,
            #capabilities=self.desired_capabilities
        )
        self.teacher.login()
        self.teacher.select_course(appearance='physics')
        self.teacher.driver.find_element(
            By.LINK_TEXT, 'Student Scores').click()
>>>>>>> 92f9fdbfce2e37bb7b040214379ebcf91b5b7461

    def tearDown(self):
        """Test destructor."""
        self.ps.update_job(job_id=str(self.teacher.driver.session_id),
                           **self.ps.test_updates)
        try:
            self.teacher.delete()
        except:
            pass

    # Case C8156 - 001 - Teacher | View the period Student Scores
    @pytest.mark.skipif(str(8156) not in TESTS, reason='Excluded')  # NOQA
<<<<<<< HEAD
    def test_usertype_story_text(self):
        """View the period Student Scores.

        Steps:

        Click on the "Student Scores" button
        Click on the tab for the desired period


        Expected Result:

        Scores for selected period are displayed in a table

        """
        self.ps.test_updates['name'] = 't1.23.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.23',
            't1.23.001',
            '8156'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
=======
    def test_teacher_view_the_period_student_scores(self):
        """View the period Student Scores.

        Steps: 
        Click on the "Student Scores" button
        Click on the tab for the desired period

        Expected Result:
        Scores for selected period are displayed in a table
        """
        self.ps.test_updates['name'] = 't1.23.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.23', 't1.23.001', '8156']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assert('scores' in self.teacher.current_url()), \
            'Not viewing Student Scores'
>>>>>>> 92f9fdbfce2e37bb7b040214379ebcf91b5b7461

        self.ps.test_updates['passed'] = True


<<<<<<< HEAD
    # Case C8157 - 002 - Teacher | Period tabs are shown 
    @pytest.mark.skipif(str(8157) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Period tabs are shown.

        Steps:

        Click on the "Student Scores" button
        

        Expected Result:

        Period tabs are displayed

        """
        self.ps.test_updates['name'] = 't1.23.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.23',
            't1.23.002',
            '8157'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
=======
    # Case C8157 - 002 - Teacher | Period tabs are shown
    @pytest.mark.skipif(str(8157) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_period_tabs_are_shown(self):
        """Period tabs are shown.

        Steps: 
        Click on the "Student Scores" button

        Expected Result:
        Period tabs are displayed
        """
        self.ps.test_updates['name'] = 't1.23.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.23', 't1.23.002','8157']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[contains(@class, "tab-item-period-name")]')
            )
        ).click()         
>>>>>>> 92f9fdbfce2e37bb7b040214379ebcf91b5b7461

        self.ps.test_updates['passed'] = True


    # Case C8158 - 003 - Teacher | Generate a spreadsheet of class scores
    @pytest.mark.skipif(str(8158) not in TESTS, reason='Excluded')  # NOQA
<<<<<<< HEAD
    def test_usertype_story_text(self):
        """Generate a spreadsheet of class scores.

        Steps:

        Click on the "Student Scores" button
        Click on the "Export" button
        

        Expected Result:

        Spreadsheet of scores is generating

        """
        self.ps.test_updates['name'] = 't1.23.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.23',
            't1.23.003',
            '8158'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8159 - 004 - Teacher | Download a spreadsheet of class scores
    @pytest.mark.skipif(str(8159) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Download a spreadsheet of class scores.

        Steps:

        Click on the "Student Scores" button
        Click on the "Export" button
        Select destination for saved spreadsheet in the pop up
        Click on the "Save" Button on the pop up
        

        Expected Result:

        Spreadsheet of scores is saved to chosen destination as an xlsx file

        """
        self.ps.test_updates['name'] = 't1.23.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.23',
            't1.23.004',
            '8159'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
=======
    def test_teacher_generate_a_spreadsheet_of_class_scores(self):
        """Generate a spreadsheet of class scores.

        Steps: 
        Click on the "Student Scores" button
        Click on the "Export" button

        Expected Result:
        Spreadsheet of scores is generating
        """
        self.ps.test_updates['name'] = 't1.23.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.23','t1.23.003','8158']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"export-button-buttons")]//button')
            )
        ).click() 
        ##assert that it was gererated/downloaded
        self.ps.test_updates['passed'] = True

    # what's the differnece between generating, and downloading in terms of test
    # Case C8159 - 004 - Teacher | Download a spreadsheet of class scores
    @pytest.mark.skipif(str(8159) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_download_a_spread_sheet_of_class_scores(self):
        """Download a spreadsheet of class scores.

        Steps: 
        Click on the "Student Scores" button
        Click on the "Export" button
        Select destination for saved spreadsheet in the pop up
        Click on the "Save" button on the pop up

        Expected Result:
        Spreadsheet of scores is saved to chosen destination as an xlsx file
        """
        self.ps.test_updates['name'] = 't1.23.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.23','t1.23.004','8159']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"export-button-buttons")]//button')
            )
        ).click()             
        ##assert that it was gererated/downloaded
>>>>>>> 92f9fdbfce2e37bb7b040214379ebcf91b5b7461

        self.ps.test_updates['passed'] = True


    # Case C8160 - 005 - Teacher | View the Performance Forecast for a single student
    @pytest.mark.skipif(str(8160) not in TESTS, reason='Excluded')  # NOQA
<<<<<<< HEAD
    def test_usertype_story_text(self):
        """View the Performance Forecast for a single student.

        Steps:

        Click on the "Student Scores" button
        Click on the name of selected student
        

        Expected Result:

        Performance Forecast for selected student is displayed

        """
        self.ps.test_updates['name'] = 't1.23.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.23',
            't1.23.005',
            '8160'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
=======
    def test_teacher_view_the_performance_forecast_for_a_single_student(self):
        """View the Performance Forecast for a single student.

        Steps: 
        Click on the "Student Scores" button
        Click on the name of selected student

        Expected Result:
        Performance Forecast for selected student is displayed
        """
        self.ps.test_updates['name'] = 't1.23.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.23','t1.23.005','8160']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,'//a[contains(@class,"student-name")]')
            )
        ).click()             
        self.teacher.driver.find_element(
            By.XPATH,'//*[contains(text(), "Performance Forecast for")]')
>>>>>>> 92f9fdbfce2e37bb7b040214379ebcf91b5b7461

        self.ps.test_updates['passed'] = True


    # Case C8161 - 006 - Teacher | Select a student from the individual Performance Forecast drop down menu
    @pytest.mark.skipif(str(8161) not in TESTS, reason='Excluded')  # NOQA
<<<<<<< HEAD
    def test_usertype_story_text(self):
        """Select a student from the individual Performance Forecast drop down menu.

        Steps:

=======
    def test_teahcer_select_a_student_from_the_individual_performance_forecast_drop_down_menu(self):
        """Select a student from the individual Performance Forecast drop down menu.

        Steps: 
>>>>>>> 92f9fdbfce2e37bb7b040214379ebcf91b5b7461
        Click on the "Student Scores" button
        Click on the name of an arbitrary student
        Click on the name of the student to open a drop down menu
        In the drop down menu click the name of selected student
<<<<<<< HEAD
        

        Expected Result:

=======

        Expected Result:
>>>>>>> 92f9fdbfce2e37bb7b040214379ebcf91b5b7461
        Displays performance Forecast for selected student.

        """
        self.ps.test_updates['name'] = 't1.23.006' \
            + inspect.currentframe().f_code.co_name[4:]
<<<<<<< HEAD
        self.ps.test_updates['tags'] = [
            't1',
            't1.23',
            't1.23.006',
            '8161'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
=======
        self.ps.test_updates['tags'] = ['t1','t1.23','t1.23.006','8161']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,'//a[contains(@class,"student-name")]')
            )
        ).click()  
        self.teacher.driver.find_element(By.ID, 'student-selection').click()
        name = self.teacher.driver.find_element(
            By.XPATH, '//a[contains(@role, "menuitem")]//span[contains(@class,"-name")]').text
        wait.until(
            expect.visibility_of_element_located(
                ( By.XPATH, '//a[contains(@role, "menuitem")]//span[contains(@class,"-name")]')
            )
        ).click()  
        self.teacher.driver.find_element(
            By.XPATH,'//span[contains(text(), "'+name+'")]')
>>>>>>> 92f9fdbfce2e37bb7b040214379ebcf91b5b7461

        self.ps.test_updates['passed'] = True


    # Case C8162 - 007 - Teacher | Info icon shows an explanation of the data
    @pytest.mark.skipif(str(8162) not in TESTS, reason='Excluded')  # NOQA
<<<<<<< HEAD
    def test_usertype_story_text(self):
        """Info icon shows an explanation of the data.

        Steps:

        Click on the "Student Scores" button
        Click on the name of selected student
        Click on the info icon next to the student's name
        

        Expected Result:

        Information about Performance Forecast is displayed.

        """
        self.ps.test_updates['name'] = 't1.23.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.23',
            't1.23.007',
            '8162'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
=======
    def test_teacher_info_icon_shows_An_Explanation_of_the_data(self):
        """Info icon shows an explanation of the data.

        Steps: 
        Click on the "Student Scores" button
        Click on the name of selected student
        Click on the info icon next to the student's name

        Expected Result:
        Information about Performance Forecast is displayed.
        """
        self.ps.test_updates['name'] = 't1.23.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.23','t1.23.007','8162']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,'//a[contains(@class,"student-name")]')
            )
        ).click()  
        #technically this is a hover, but click seems to work too
        self.teacher.driver.find_element(
            By.XPATH, '//span[contains(@class,"info-link")]').click()
        self.teacher.driver.find_element(
            By.XPATH, '//div[contains(@class,"tooltip-inner")]')
>>>>>>> 92f9fdbfce2e37bb7b040214379ebcf91b5b7461

        self.ps.test_updates['passed'] = True


    # Case C8163 - 008 - Teacher | Return to the class scores using the Return To Scores button
    @pytest.mark.skipif(str(8163) not in TESTS, reason='Excluded')  # NOQA
<<<<<<< HEAD
    def test_usertype_story_text(self):
        """Return to the class scores using the Return To Scores button.

        Steps:

        Click on the "Student Scores" button
        Click on the name of selected student
        Click on the "Return to Scores" button
        

        Expected Result:

        User at Student scores page on the first tab

        """
        self.ps.test_updates['name'] = 't1.23.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.23',
            't1.23.008',
            '8163'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

=======
    def test_teacher_return_to_the_class_score_usifnt_the_return_to_scores_button(self):
        """Return to the class scores using the Return To Scores button.

        Steps: 
        Click on the "Student Scores" button
        Click on the name of selected student
        Click on the "Return to Scores" button

        Expected Result:
        User at Student scores page on the first tab.
        """
        self.ps.test_updates['name'] = 't1.23.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.23','t1.23.008','8163']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,'//a[contains(@class,"student-name")]')
            )
        ).click()  
        self.teacher.driver.find_element(
            By.LINK_TEXT, 'Return To Scores').click()
        assert('scores' in self.teacher.current_url()), \
            'Not viewing Student Scores'
     
>>>>>>> 92f9fdbfce2e37bb7b040214379ebcf91b5b7461
        self.ps.test_updates['passed'] = True


    # Case C8164 - 009 - Teacher | Sort the student list by last name
    @pytest.mark.skipif(str(8164) not in TESTS, reason='Excluded')  # NOQA
<<<<<<< HEAD
    def test_usertype_story_text(self):
        """Sort the student list by last name.

        Steps:

        Click on the "Student Scores" button
        [by default the students should be ordered by last name]
        Click on "Student Name" on the table [this will make the names in reverse alphabetical order by last name]
        Click on "Student Name" on the table again [this will make the names in alphabetical order by last name]
        

        Expected Result:

        The students are sorted alphabetically by last name.

        """
        self.ps.test_updates['name'] = 't1.23.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.23',
            't1.23.009',
            '8164'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
=======
    def test_teacher_sort_the_students_by_last_name(self):
        """Sort the student list by last name.

        Steps: 
        Click on the "Student Scores" button
        [by default the students should be ordered by last name]
        Click on "Student Name" on the table [makes names in reverse alphabetical order]
        Click on "Student Name" on the table again  [makes names in alphabetical order]

        Expected Result:
        The students are sorted alphabetically by last name.
        """
        self.ps.test_updates['name'] = 't1.23.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.23','t1.23.009','8164']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,'//div[contains(@class,"student-header")]')
            )
        ).click()  
        self.teacher.driver.find_element(
            By.XPATH, '//div[contains(@class,"student-header")]//div[contains(@class,"is-descending")]')
        self.teacher.driver.find_element(
            By.XPATH,'//div[contains(@class,"student-header")]').click()
        self.teacher.driver.find_element(
            By.XPATH, '//div[contains(@class,"student-header")]//div[contains(@class,"is-ascending")]')
>>>>>>> 92f9fdbfce2e37bb7b040214379ebcf91b5b7461

        self.ps.test_updates['passed'] = True


    # Case C8165 - 010 - Teacher | Sort an assignment by completion
    @pytest.mark.skipif(str(8165) not in TESTS, reason='Excluded')  # NOQA
<<<<<<< HEAD
    def test_usertype_story_text(self):
        """Sort an assignment by completion.

        Steps:

        Click on the "Student Scores" button
        Click on the name of the selected assignment
        

        Expected Result:

        Students are sorted by completion of selected assignment.

        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)
=======
    def test_teacher_sort_an_assignment_by_completion(self):
        """Sort an assignment by completion.

        Steps: 
        Click on the "Student Scores" button
        Click on the name of the selected assignment

        Expected Result:
        Students are sorted by completion of selected assignment.
        """
        self.ps.test_updates['name'] = 't1.23.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.23','t1.23.010','8165']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,'//div[contains(@class,"scores-cell")]//div[contains(text(),"Progress")]')
            )
        ).click()  
        self.teacher.driver.find_element(
            By.XPATH, '//div[contains(@class,"scores-cell")]//div[contains(@class,"is-descending")]')
        self.teacher.driver.find_element(
            By.XPATH,'//div[contains(@class,"scores-cell")]//div[contains(text(),"Progress")]').click()
        self.teacher.driver.find_element(
            By.XPATH, '//div[contains(@class,"scores-cell")]//div[contains(@class,"is-ascending")]')

        self.ps.test_updates['passed'] = True
>>>>>>> 92f9fdbfce2e37bb7b040214379ebcf91b5b7461


    # Case C8166 - 011 - Teacher | View the assignment due date for a particular section
    @pytest.mark.skipif(str(8166) not in TESTS, reason='Excluded')  # NOQA
<<<<<<< HEAD
    def test_usertype_story_text(self):
        """View the assignment due date for a particular section.

        Steps:

        Click on the "Student Scores" button
        Click on the tab for selected section
        

        Expected Result:

        Due date for selected assignment is displayed in the cell below the assignment name.

        """
        self.ps.test_updates['name'] = 't1.23.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.23',
            't1.23.011',
            '8166'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
=======
    def test_teacher_view_the_assignment_due_date_for_a_particular_section(self):
        """View the assignment due date for a particular section.

        Steps: 
        Click on the "Student Scores" button
        Click on the tab for selected section

        Expected Result:
        Due date for selected assignment is displayed in the cell below the assignment name.
        """
        self.ps.test_updates['name'] = 't1.23.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.23','t1.23.011','8166']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[contains(@class, "tab-item-period-name")]')
            )
        ).click()  
        self.teacher.driver.find_element(By.XPATH, '//div[contains(@class,"due")]')
>>>>>>> 92f9fdbfce2e37bb7b040214379ebcf91b5b7461

        self.ps.test_updates['passed'] = True


    # Case C8167 - 012 - Teacher | Review a reading assignment for a period
    @pytest.mark.skipif(str(8167) not in TESTS, reason='Excluded')  # NOQA
<<<<<<< HEAD
    def test_usertype_story_text(self):
        """Review a reading assignment for a period.

        Steps:

        Click on the "Student Scores" button
        Click on the tab for the chosen period
        Click on the "Review" button under the selected reading assignment.
        

        Expected Result:

        Displays students progress on chosen assignment for selected period, actual questions, and question results.

        """
        self.ps.test_updates['name'] = 't1.23.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.23',
            't1.23.012',
            '8167'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

=======
    def test_teacher_review_a_reading_assignemnt_for_a_period(self):
        """Review a reading assignment for a period.

        Steps: 
        Click on the "Student Scores" button
        Click on the tab for the chosen period
        Click on the "Review" button under the selected reading assignment.

        Expected Result:
        Displays students progress on chosen assignment for selected period,
        """
        self.ps.test_updates['name'] = 't1.23.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.23','t1.23.012','8167']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[contains(@class, "tab-item-period-name")]')
            )
        ).click()  
        ### that x-path works but seems bad, didn't know how to click the review in the
        ### column of a reading because not direct path
        self.teacher.driver.find_element(
            By.XPATH, '//span[contains(@class,"review-link wide")]//a[contains(text(),"Review")]').click()
        assert('summary' in self.teacher.current_url()), \
            'Not viewing reading assignment summary'
>>>>>>> 92f9fdbfce2e37bb7b040214379ebcf91b5b7461
        self.ps.test_updates['passed'] = True


    # Case C8168 - 013 - Teacher | Review a homework assignment for a period
    @pytest.mark.skipif(str(8168) not in TESTS, reason='Excluded')  # NOQA
<<<<<<< HEAD
    def test_usertype_story_text(self):
        """Review a homework assignment for a period.

        Steps:

        Click on the "Student Scores" button
        Click on the tab for the chosen period
        Click on the "Review" button under the selected homework assignment.
        

        Expected Result:

        Displays students progress on chosen assignment for selected period, actual questions, and question results.

        """
        self.ps.test_updates['name'] = 't1.23.013' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.23',
            't1.23.013',
            '8168'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
=======
    def test_teacher_review_a_hoemwork_assignment_for_a_period(self):
        """Review a homework assignment for a period.

        Steps: 
        Click on the "Student Scores" button
        Click on the tab for the chosen period
        Click on the "Review" button under the selected homework assignment.

        Expected Result:
        Displays students progress on chosen assignment for selected period,
        questions, results are shown.
        """
        self.ps.test_updates['name'] = 't1.23.013' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.23','t1.23.013','8168']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[contains(@class, "tab-item-period-name")]')
            )
        ).click()  
        ### that x-path works but seems bad, didn't know how to click the review in the
        ### column of a hoework because not direct path
        self.teacher.driver.find_element(
            By.XPATH, '//span[contains(@class,"review-link")]//a[contains(text(),"Review")]').click()
        assert('summary' in self.teacher.current_url()), \
            'Not viewing homework assignment summary'
>>>>>>> 92f9fdbfce2e37bb7b040214379ebcf91b5b7461

        self.ps.test_updates['passed'] = True


    # Case C8169 - 014 - Teacher | A homework with responses shows the period average
    @pytest.mark.skipif(str(8169) not in TESTS, reason='Excluded')  # NOQA
<<<<<<< HEAD
    def test_usertype_story_text(self):
        """A homework with responses shows the period average.

        Steps:

=======
    def test_teacher_a_homework_with_responses_shows_the_period_average(self):
        """A homework with responses shows the period average.

        Steps: 
>>>>>>> 92f9fdbfce2e37bb7b040214379ebcf91b5b7461
        Click on the "Student Scores" button
        Click on the tab for the chosen period
        Click on the "Review" button under the selected homework assignment.

<<<<<<< HEAD
        
        Expected Result:

        If students have worked the problem, the period average is displayed below the assignment due date or 
        in the box next to the questions under "Review"

        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)


    # Case C8170 - 015 - Teacher | An external assignment shows the number of students who have clicked on the assignment URL
    @pytest.mark.skipif(str(8170) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """An external assignment shows the number of students who have clicked on the assignment URL.

        Steps:

        Click on the "Student Scores" button

        
        Expected Result:

        For external assignments the fraction of students who have clicked on the assignment is displayed.

=======
        Expected Result:
        If students have worked the problem, the period average is displayed
        below the assignment due date or in the box next to the questions under "Review"
        """
        self.ps.test_updates['name'] = 't1.23.014' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.23','t1.23.014','8169']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[contains(@class, "tab-item-period-name")]')
            )
        ).click()  
        ### I think this might need a better test that it actually worked
        self.teacher.driver.find_element(
            By.XPATH,'//div[contains(@class,"average-cell")]//span[contains(@class,"average")]')

        self.ps.test_updates['passed'] = True


    # Case C8170 - 015 - Teacher | An external assignment shows the number of students who have clicked on it
    @pytest.mark.skipif(str(8170) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_an_external_assignment_shows_the_number_of_Students_who_have_clicked_on_it(self):
        """An external assignment shows the number of students who have clicked on the  URL.

        Steps: 
        Click on the "Student Scores" button

        Expected Result:
        For external assignments the fraction of students who have clicked on the assignment is displayed.
>>>>>>> 92f9fdbfce2e37bb7b040214379ebcf91b5b7461
        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)


    # Case C8171 - 016 - Teacher | Navigate a reading review using the section breadcrumbs
    @pytest.mark.skipif(str(8171) not in TESTS, reason='Excluded')  # NOQA
<<<<<<< HEAD
    def test_usertype_story_text(self):
        """Navigate a reading review using the section breadcrumbs.

        Steps:

=======
    def test_teacher_navigate_a_reading_using_the_section_breadcrumbs(self):
        """Navigate a reading review using the section breadcrumbs

        Steps: 
>>>>>>> 92f9fdbfce2e37bb7b040214379ebcf91b5b7461
        Click on the "Student Scores" button
        Click on the tab for the chosen period
        Click on the "Review" button under the selected reading assignment.
        Click on a breadcrumb of selected section of reading.
<<<<<<< HEAD
        

        Expected Result:

        Screen is moved down to selected section of reading. (scroll not shown, taken directly to chosen section)

        """
        self.ps.test_updates['name'] = 't1.23.016' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.23',
            't1.23.016',
            '8171'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
=======

        Expected Result:
        Screen is moved down to selected section of reading. 
        (scroll not shown, taken directly to chosen section)
        """
        self.ps.test_updates['name'] = 't1.23.016' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.23','t1.23.016','8171']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[contains(@class, "tab-item-period-name")]')
            )
        ).click()  
        ### that x-path works but seems bad, didn't know how to click the review in the
        ### column of a reading because not direct path
        self.teacher.driver.find_element(
            By.XPATH, '//span[contains(@class,"review-link wide")]//a[contains(text(),"Review")]').click()
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,'//span[contains(@class,"breadcrumbs")]')
            )
        ) 
        sections = self.teacher.driver.find_elements(By.XPATH,'//span[contains(@class,"breadcrumbs")]')
        section = sections[-1]
        section.click()
        chapter = section.get_attribute("data-chapter")
        assert(self.teacher.driver.find_element(
            By.XPATH,'//span[contains(text(),"'+chapter+'")]').is_displayed()), \
            'chapter not displayed'
>>>>>>> 92f9fdbfce2e37bb7b040214379ebcf91b5b7461

        self.ps.test_updates['passed'] = True


    # Case C8172 - 017 - Teacher | Navigate a homework review using the question breadcrumbs
    @pytest.mark.skipif(str(8172) not in TESTS, reason='Excluded')  # NOQA
<<<<<<< HEAD
    def test_usertype_story_text(self):
        """Navigate a homework review using the question breadcrumbs.

        Steps:

=======
    def test_teacher_naviget_a_homework_review_using_the_question_breadcrumbs(self):
        """Navigate a homework review using the question breadcrumbs

        Steps: 
>>>>>>> 92f9fdbfce2e37bb7b040214379ebcf91b5b7461
        Click on the "Student Scores" button
        Click on the tab for the chosen period
        Click on the "Review" button under the selected homework assignment.
        Click on a breadcrumb of selected section of homework.
<<<<<<< HEAD
        

        Expected Result:

        Screen is moved down to selected section of homework. 
        (scroll not shown, taken directly to chosen section)

        """
        self.ps.test_updates['name'] = 't1.23.017' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.23',
            't1.23.017',
            '8172'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
=======

        Expected Result:
        Screen is moved down to selected section of homework. 
        (scroll not shown, taken directly to chosen section)
        """
        self.ps.test_updates['name'] = 't1.23.017' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.23','t1.23.017','8172']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[contains(@class, "tab-item-period-name")]')
            )
        ).click()  
        ### that x-path works but seems bad, didn't know how to click the review in the
        ### column of a reading because not direct path
        self.teacher.driver.find_element(
            By.XPATH, '//span[contains(@class,"review-link")]//a[contains(text(),"Review")]').click()
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,'//span[contains(@class,"breadcrumbs")]')
            )
        ) 
        sections = self.teacher.driver.find_elements(By.XPATH,'//span[contains(@class,"breadcrumbs")]')
        section = sections[-1]
        section.click()
        chapter = section.get_attribute("data-chapter")
        assert(self.teacher.driver.find_element(
            By.XPATH,'//span[contains(text(),"'+chapter+'")]').is_displayed()), \
            'chapter not displayed'
>>>>>>> 92f9fdbfce2e37bb7b040214379ebcf91b5b7461

        self.ps.test_updates['passed'] = True


    # Case C8173 - 018 - Teacher | Period tabs are shown in the assignment review
    @pytest.mark.skipif(str(8173) not in TESTS, reason='Excluded')  # NOQA
<<<<<<< HEAD
    def test_usertype_story_text(self):
        """Period tabs are shown in the assignment review.

        Steps:

        Click on the "Student Scores" button
        Click on the tab for the chosen period
        Click on the "Review" button under the selected assignment.
        

        Expected Result:

        Period tabs are displayed.

        """
        self.ps.test_updates['name'] = 't1.23.018' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.23',
            't1.23.018',
            '8173'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
=======
    def test_teacher_period_tabs_are_shown_in_assignemnt_review(self):
        """Period tabs are shown in the assignment review
        
        Steps: 
        Click on the "Student Scores" button
        Click on the tab for the chosen period
        Click on the "Review" button under the selected assignment.

        Expected Result:
        Period tabs are displayed.
        """
        self.ps.test_updates['name'] = 't1.23.018' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.23','t1.23.018','8173']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[contains(@class, "tab-item-period-name")]')
            )
        ).click()  
        ### that x-path works but seems bad, didn't know how to click the review in the
        ### column of a reading because not direct path
        self.teacher.driver.find_element(
            By.XPATH, '//span[contains(@class,"review-link")]//a[contains(text(),"Review")]').click()
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,'//ul[contains(@role,"tablist")]//span[contains(@class,"tab-item-period-name")]')
            )
        )
>>>>>>> 92f9fdbfce2e37bb7b040214379ebcf91b5b7461

        self.ps.test_updates['passed'] = True


<<<<<<< HEAD
    # Case C8174 - 019 - Teacher | View the Complete, In Progress, and Not Started counts for a period
    @pytest.mark.skipif(str(8174) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """View the Complete, In Progress, and Not Started counts for a period

        Steps:

=======
    # Case C8174 - 019 - Teacher | View the Complete, In Progress, and Not Started counts
    @pytest.mark.skipif(str(8174) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_view_the_complete_in_progress_and_not_started_counts(self):
        """View the Complete, In Progress, and Not Started counts for a period

        Steps: 
>>>>>>> 92f9fdbfce2e37bb7b040214379ebcf91b5b7461
        Click on the "Student Scores" button
        Click on the tab for the chosen period
        Click on the "Review" button under the selected reading assignment.
        Click on tab for selected period

<<<<<<< HEAD

        Expected Result:

        Complete, In Progress, and Not Started counts for selected period are displayed

        """
        self.ps.test_updates['name'] = 't1.23.019' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.23',
            't1.23.019',
            '8174'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8175 - 020 - Teacher | When reviewing, the section numbers match the section breadcrumbs
    @pytest.mark.skipif(str(8175) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """When reviewing, the section numbers match the section breadcrumbs.

        Steps:

        Click on the "Student Scores" button
        Click on the tab for the chosen period
        Click on the "Review" button under the selected reading assignment.
        

        Expected Result:

        Current Topics Performance and Spaced Practice Performance section numbers match the section breadcrumbs

        """
        self.ps.test_updates['name'] = 't1.23.020' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.23',
            't1.23.020',
            '8175'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

=======
        Expected Result:
        Complete, In Progress, and Not Started counts for selected period are displayed
        """
        self.ps.test_updates['name'] = 't1.23.019' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.23','t1.23.019','8174']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[contains(@class, "tab-item-period-name")]')
            )
        ).click()  
        ### that x-path works but seems bad, didn't know how to click the review in the
        ### column of a reading because not direct path
        self.teacher.driver.find_element(
            By.XPATH, '//span[contains(@class,"review-link")]//a[contains(text(),"Review")]').click()
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,'//ul[contains(@role,"tablist")]//span[contains(@class,"tab-item-period-name")]')
            )
        )
        self.teacher.driver.find_element(
            By.XPATH, '//div[contains(@class,"reading-stats-complete")]'\
            '//label[contains(text(),"Complete")]')
        self.teacher.driver.find_element(
            By.XPATH, '//div[contains(@class,"reading-stats-in-progress")]'\
            '//label[contains(text(),"In Progress")]')
        self.teacher.driver.find_element(
            By.XPATH, '//div[contains(@class,"reading-stats-not-started")]'\
            '//label[contains(text(),"Not Started")]')
        
        self.ps.test_updates['passed'] = True


    # Case C8175 - 020 - Teacher | Section numbers in review match the section breadcrumbs
    @pytest.mark.skipif(str(8175) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_section_numbers_in_review_match_the_section_breadcrumbs(self):
        """Section numbers in review match the section breadcrumbs

        Steps: 
        Click on the "Student Scores" button
        Click on the tab for the chosen period
        Click on the "Review" button under the selected reading assignment.
        Click on tab for selected period

        Expected Result:
        Current Topics Performance and Spaced Practice Performance section numbers
        match the section breadcrumbs
        """
        self.ps.test_updates['name'] = 't1.23.020' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.23','t1.23.020','8175']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[contains(@class, "tab-item-period-name")]')
            )
        ).click()  
        ### that x-path works but seems bad, didn't know how to click the review in the
        ### column of a reading because not direct path
        self.teacher.driver.find_element(
            By.XPATH, '//span[contains(@class,"review-link")]//a[contains(text(),"Review")]').click()
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,'//ul[contains(@role,"tablist")]//span[contains(@class,"tab-item-period-name")]')
            )
        )
        sections = self.teacher.driver.find_elements(
            By.XPATH,'//div[contains(@class,"reading-progress")]//span[contains(@class,"text-success")]')
        section_breadcrumbs = self.teacher.driver.find_elements(
            By.XPATH,'//span[contains(@class,"breadcrumbs")]')
        section_nums = []
        for x in section_breadcrumbs:
            section_nums.append(x.get_attribute("data-chapter"))
        for x in sections:
            assert (x.text in section_nums), \
                ("section and breadcrumb don't match: " + x.text)
            
>>>>>>> 92f9fdbfce2e37bb7b040214379ebcf91b5b7461
        self.ps.test_updates['passed'] = True


    # Case C8176 - 021 - Teacher | Each assessment has a correct response displayed
    @pytest.mark.skipif(str(8176) not in TESTS, reason='Excluded')  # NOQA
<<<<<<< HEAD
    def test_usertype_story_text(self):
        """Each assessment has a correct response displayed.

        Steps:

        Click on the "Student Scores" button
        Click on the tab for the chosen period
        Click on the "Review" button under the selected reading assignment.
        

        Expected Result:

        Each question has a correct response displayed

        """
        self.ps.test_updates['name'] = 't1.23.021' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.23',
            't1.23.021',
            '8176'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8177 - 022 - Teacher | Open and view a list of student free response answers for an assessment
    @pytest.mark.skipif(str(8177) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Open and view a list of student free response answers for an assessment.

        Steps:

=======
    def test_teacher_each_assesment_has_a_correct_response_displayed(self):
        """Each assessment has a correct response displayed

        Steps: 
        Click on the "Student Scores" button
        Click on the tab for the chosen period
        Click on the "Review" button under the selected homework assignment.

        Expected Result:
        Each question has a correct response displayed
        """
        self.ps.test_updates['name'] = 't1.23.021' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.23','t1.23.021','8176']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[contains(@class, "tab-item-period-name")]')
            )
        ).click()  
        ### that x-path works but seems bad, didn't know how to click the review in the
        ### column of a reading because not direct path
        self.teacher.driver.find_element(
            By.XPATH, '//span[contains(@class,"review-link")]//a[contains(text(),"Review")]').click()
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,'//ul[contains(@role,"tablist")]//span[contains(@class,"tab-item-period-name")]')
            )
        )
        ###Might need a better test, couldn't identify the exact checkmark element
        correct_answers = self.teacher.driver.find_elements(
            By.XPATH,'//div[contains(@class,"answer-correct")]')
        questions = self.teacher.driver.find_elements(
            By.XPATH,'//span[contains(@class,"breadcrumbs")]')
        assert(len(correct_answers) == len(questions)),\
            "number of correct answers not equal to the number of questions"
        
        self.ps.test_updates['passed'] = True


    # Case C8177 - 022 - Teacher | Open and view a list of student free response answers
    @pytest.mark.skipif(str(8177) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_open_and_view_a_list_of_student_free_response_answers(self):
        """Open and view a list of student free response answers for an assessment

        Steps: 
>>>>>>> 92f9fdbfce2e37bb7b040214379ebcf91b5b7461
        Click on the "Student Scores" button
        Click on the tab for the chosen period
        Click on the "Review" button under the selected reading assignment.
        Click on "View Student Text Responses" button for selected question

<<<<<<< HEAD

        Expected Result:

        List of student text responses for selected question is displayed.

        """
        self.ps.test_updates['name'] = 't1.23.022' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.23',
            't1.23.022',
            '8177'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8178 - 023 - Teacher | Assessment pane shows interleaved class stats
    @pytest.mark.skipif(str(8178) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Assessment pane shows interleaved class stats.

        Steps:

        Click on the "Student Scores" button
        Click on the review button for a selected assignment


        Expected Result:

        Assessment pane shows interleaved class stats

        """
        self.ps.test_updates['name'] = 't1.23.023' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.23',
            't1.23.023',
            '8178'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8179 - 024 - Teacher | Teacher can view a student's work for a reading assignment
    @pytest.mark.skipif(str(8179) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Teacher can view a student's work for a reading assignment

        Steps:

=======
        Expected Result:
        List of student text responses for selected question is displayed.
        """
        self.ps.test_updates['name'] = 't1.23.022' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.23','t1.23.022','8177']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[contains(@class, "tab-item-period-name")]')
            )
        ).click()  
        ### that x-path works but seems bad, didn't know how to click the review in the
        ### column of a reading because not direct path
        self.teacher.driver.find_element(
            By.XPATH, '//span[contains(@class,"review-link")]//a[contains(text(),"Review")]').click()
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,'//a[contains(text(),"View student text responses")]')
            )
        ).click()
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,'//div[contains(@class,"teacher-review-answers")]'\
                 '//div[contains(@class,"free-response")]')
            )
        )            
        self.ps.test_updates['passed'] = True

    
    # # don't know what interleaved class stats are
    # # Case C8178 - 023 - Teacher | Assessment pane shows interleaved class stats
    # @pytest.mark.skipif(str(8178) not in TESTS, reason='Excluded')  # NOQA
    # def test_teacher_assesment_pane_shows_interleaved_class_stats(self):
    #     """Assessment pane shows interleaved class stats

    #     Steps: 
    #     Click on the "Student Scores" button
    #     Click on the review button for a selected assignment

    #     Expected Result:
    #     Assessment pane shows interleaved class stats
    #     """
    #     self.ps.test_updates['name'] = 't1.23.023' \
    #         + inspect.currentframe().f_code.co_name[4:]
    #     self.ps.test_updates['tags'] = ['t1','t1.23','t1.23.023','8178']
    #     self.ps.test_updates['passed'] = False

    #     # Test steps and verification assertions

    #     self.ps.test_updates['passed'] = True


    # Case C8179 - 024 - Teacher | Teacher can see a student's work for a reading assignment
    @pytest.mark.skipif(str(8179) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_see_a_steudents_work_for_a_reading_assignemnt(self):
        """Teacher can see a student's work for a reading assignment

        Steps: 
>>>>>>> 92f9fdbfce2e37bb7b040214379ebcf91b5b7461
        Click on the "Student Scores" button
        Click on the tab for the chosen period
        Click on cell for chosen student and reading assignment

<<<<<<< HEAD

        Expected Result:

        Teacher view of student work shown. 
        Teacher can go through different sections with either the "Continue" button, or breadcrumbs. 
        Only sections student has gone through are shown.

=======
        Expected Result:
        Teacher view of student work shown. 
        Teacher can go through different sections with either the "Continue" button, or breadcrumbs. 
        Only sections student has gone through are shown.
>>>>>>> 92f9fdbfce2e37bb7b040214379ebcf91b5b7461
        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)


    # Case C8180 - 025 - Teacher | Teacher can view a student's work for a homework assignment
<<<<<<< HEAD
    @pytest.mark.skipif(str(8179) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Teacher can view a student's work for a homework assignment

        Steps:

=======
    @pytest.mark.skipif(str(8180) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_view_a_students_work_for_a_homework_assignment(self):
        """Assessment pane shows interleaved class stats

        Steps: 
>>>>>>> 92f9fdbfce2e37bb7b040214379ebcf91b5b7461
        Click on the "Student Scores" button
        Click on the tab for the chosen period
        Click on cell for chosen student and homework assignment

<<<<<<< HEAD

        Expected Result:

        Teacher view of student work shown. 
        Teacher can go through different questions with either the "Next Question" button, or breadcrumbs. 
        Students answers are shown for questions they have worked. 
        Correct answers are shown.

        """
        self.ps.test_updates['name'] = 't1.23.025' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.23',
            't1.23.025',
            '8180'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
=======
        Expected Result:
        Teacher view of student work shown. 
        Teacher can go through different questions with either the "Next Question" button, or breadcrumbs. 
        Students answers are shown for questions they have worked. Correct answers are shown.
        """
        self.ps.test_updates['name'] = 't1.23.025' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.23','t1.23.025','8180']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[contains(@class, "tab-item-period-name")'\
                 ' and contains(@aria-describedby,"1")]')
            )
        ).click()  
        homework = self.teacher.driver.find_element(
            By.XPATH,'//div[contains(@class,"score")]//a[contains(text(),"%")]')
        self.teacher.driver.execute_script('return arguments[0].scrollIntoView();', homework)
        self.teacher.driver.execute_script('window.scrollBy(0, -80);')
        homework.click()
        assert('steps' in self.teacher.current_url()), \
            'Not viewing student work for homework'
>>>>>>> 92f9fdbfce2e37bb7b040214379ebcf91b5b7461

        self.ps.test_updates['passed'] = True


<<<<<<< HEAD
    # Case C8181 - 026 - Teacher | Teacher can view a student's work for an external assignment 
    @pytest.mark.skipif(str(8179) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Teacher can view a student's work for an external assignment 

        Steps:

=======
    # Case C8181 - 026 - Teacher | Teacher can view a student's work for an external assignment
    @pytest.mark.skipif(str(8181) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_view_a_students_work_for_an_external_assignemnt(self):
        """Teacher can view a student's work for an external assignment

        Steps: 
>>>>>>> 92f9fdbfce2e37bb7b040214379ebcf91b5b7461
        Click on the "Student Scores" button
        Click on the tab for the chosen period
        Click on cell for chosen student and external assignment assignment

<<<<<<< HEAD

        Expected Result:

        Teacher view of student work shown. 
        (Shows link to external assignment as a student would see it)

        """
        self.ps.test_updates['name'] = 't1.23.026' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.23',
            't1.23.026',
            '8181'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

=======
        Expected Result:
        Teacher view of student work shown.
        (Shows link to external assignment as a student would see it)
        """
        self.ps.test_updates['name'] = 't1.23.026' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1','t1.23','t1.23.026','8181']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        # Test steps and verification assertions
        wait = WebDriverWait(self.teacher.driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[contains(@class, "tab-item-period-name")'\
                 ' and contains(@aria-describedby,"1")]')
            )
        ).click()  
        external = self.teacher.driver.find_element(
            By.XPATH,'//a[contains(@data-assignment-type,"external")]//span[contains(text(),"-")]')
        self.teacher.driver.execute_script('return arguments[0].scrollIntoView();', external)
        self.teacher.driver.execute_script('window.scrollBy(0, -80);')
        external.click()
        assert('steps' in self.teacher.current_url()), \
            'Not viewing student "work" for external assignment'
        self.ps.test_updates['passed'] = True
>>>>>>> 92f9fdbfce2e37bb7b040214379ebcf91b5b7461
