"""Tutor v3, Epic 09 - Course Adoption and Readoption."""

import datetime
import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
from random import randint
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from staxing.assignment import Assignment

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Teacher

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
        106450, 106451, 106452, 106453, 106454,
        106455, 106456, 106457, 106458, 106459,
        106460, 106461, 106462, 107476, 107477,
        107478, 107479, 107480, 107482, 107483,
        107484, 107495, 107495
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestCreateAReading(unittest.TestCase):
    """T1.14 - Create a Reading."""

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
        self.teacher.select_course(appearance='biology')

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

    # Case C106450 - 001 - Teacher | Add a course via MyOpenstax
    @pytest.mark.skipif(str(106450) not in TESTS, reason='Excluded')
    def test_teacher_add_a_course_via_my_openstax_106450(self):
        """Add a course via my openstax.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 't3.09.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.09', 't3.09.001', '106450']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C106451 - 002 - Teacher | Add a course via the course picker page
    @pytest.mark.skipif(str(106451) not in TESTS, reason='Excluded')
    def test_teacher_add_a_course_via_the_course_picker_page_106451(self):
        """Add a course via the course picker page.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 't3.09.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.09', 't3.09.002', '106451']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C106452 - 003 - Teacher | Add a course via the Tutor dashboard
    @pytest.mark.skipif(str(106452) not in TESTS, reason='Excluded')
    def test_teacher_add_a_course_via_the_tutor_dashboard_106452(self):
        """Add a course via the Tutor dashboard.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 't3.09.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.09', 't3.09.003', '106452']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C106453 - 004 - Teacher | A past course is available for cloning
    @pytest.mark.skipif(str(106453) not in TESTS, reason='Excluded')
    def test_teacher_apast_course_is_available_for_cloning_106453(self):
        """A past course is available for cloning.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 't3.09.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.09', 't3.09.004', '106453']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C106454 - 005 - Teacher | Able to copy the question library during
    # cloning
    @pytest.mark.skipif(str(106454) not in TESTS, reason='Excluded')
    def test_teacher_able_to_copy_the_question_library_during_clo_106454(self):
        """Able to copy the question library during cloning.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 't3.09.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.09', 't3.09.005', '106454']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C106455 - 006 - Teacher | Able to select the name for a new course
    @pytest.mark.skipif(str(106455) not in TESTS, reason='Excluded')
    def test_teacher_able_to_select_the_name_for_a_new_course_106455(self):
        """Able to select the name for a new course.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 't3.09.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.09', 't3.09.006', '106455']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C106456 - 007 - Teacher | Specify the number of sections for a new
    # course
    @pytest.mark.skipif(str(106456) not in TESTS, reason='Excluded')
    def test_teacher_specify_the_number_of_sections_for_a_new_cou_106456(self):
        """Specify the number of sections for a new course.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 't3.09.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.09', 't3.09.007', '106456']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C106457 - 008 - Teacher | A course's setting match those selected
    # during the cloning process
    @pytest.mark.skipif(str(106457) not in TESTS, reason='Excluded')
    def test_teacher_a_courses_settings_match_those_selected_duri_106457(self):
        """A course's setting match those selected during the cloning process.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 't3.09.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.09', 't3.09.008', '106457']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C106458 - 009 - Teacher | Add a new course
    @pytest.mark.skipif(str(106458) not in TESTS, reason='Excluded')
    def test_teacher_add_a_new_course_106458(self):
        """Add a new course.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 't3.09.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.09', 't3.09.009', '106458']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C106459 - 010 - Teacher | Copy a homework
    @pytest.mark.skipif(str(106459) not in TESTS, reason='Excluded')
    def test_teacher_copy_a_homework_106459(self):
        """Copy a homework.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 't3.09.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.09', 't3.09.010', '106459']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C106460 - 011 - Teacher | Copy an event
    @pytest.mark.skipif(str(106460) not in TESTS, reason='Excluded')
    def test_teacher_copy_an_event_106460(self):
        """Copy an event.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 't3.09.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.09', 't3.09.011', '106460']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C106461 - 012 - Teacher | Copy a reading
    @pytest.mark.skipif(str(106461) not in TESTS, reason='Excluded')
    def test_teacher_copy_a_reading_106461(self):
        """Copy a reading.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 't3.09.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.09', 't3.09.012', '106461']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C106462 - 013 - Teacher | Copy an external assignment
    @pytest.mark.skipif(str(106462) not in TESTS, reason='Excluded')
    def test_teacher_copy_an_external_assignment_106462(self):
        """Copy an external assignment.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 't3.09.013' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.09', 't3.09.013', '106462']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
