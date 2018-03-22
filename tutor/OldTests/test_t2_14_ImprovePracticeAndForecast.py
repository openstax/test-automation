"""Tutor v2, Epic 14 - Improve Practice and Forecast."""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
# from random import randint
# from selenium.webdriver.common.by import By
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
        # not implemented
        # 14748,
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestImprovePracticeAndForecast(unittest.TestCase):
    """T2.14 - Improve Practice and Forecast."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.teacher = Teacher(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )

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

    '''
    # 14747 - 001 - Teacher | View how much students have practiced
    @pytest.mark.skipif(str(14747) not in TESTS, reason='Excluded')
    def test_teacher_view_how_much_students_have_practiced_14747(self):
        """View how much students have practiced.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.14.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.14',
            't2.14.001',
            '14747'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
    '''

    # 14748 - 002 - Student | View changes in Performance Forecast at the end
    # of a retrieval practice in readings, hw, and previous practice
    @pytest.mark.skipif(str(14748) not in TESTS, reason='Excluded')
    def test_student_view_changes_in_performance_forecast_at_the_14748(self):
        """View changes in Performance Forecast at end of retrieval practice.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.14.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.14',
            't2.14.002',
            '14748'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    '''
    # 14749 - 003 - Teacher | Assign practice
    @pytest.mark.skipif(str(14749) not in TESTS, reason='Excluded')
    def test_teacher_assign_practice_14749(self):
        """Assign practice.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.14.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.14',
            't2.14.003',
            '14749'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
    '''
