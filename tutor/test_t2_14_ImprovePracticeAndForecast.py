"""Tutor v2, Epic 14 - Improve Practice and Forecast."""

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
    str([14747, 14748, 14749])  # NOQA
)


@PastaDecorator.on_platforms(BROWSERS)
class TestImprovePracticeAndForecast(unittest.TestCase):
    """T2.14 - Improve Practice and Forecast."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.Teacher = Teacher(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )

    def tearDown(self):
        """Test destructor."""
        self.ps.update_job(job_id=str(self.teacher.driver.session_id),
                           **self.ps.test_updates)
        try:
            self.teacher.delete()
        except:
            pass

    # 14747 - 001 - Teacher | View how much students have practiced
    @pytest.mark.skipif(str(14747) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_view_how_much_students_have_practiced_14747(self):
        """View how much students have practiced.

        Steps:


        Expected Result:



        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # 14748 - 002 - Student | View changes in Performance Forecast at the end
    # of a retrieval practice in readings, hw, and previous practice
    @pytest.mark.skipif(str(14748) not in TESTS, reason='Excluded')  # NOQA
    def test_student_view_changes_in_performance_forecast_at_the_14748(self):
        """View changes in Performance Forecast at end of retrieval practice.

        Steps:



        Expected Result:


        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # 14749 - 003 - Teacher | Assign practice
    @pytest.mark.skipif(str(14749) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_assign_practice_14749(self):
        """Assign practice.

        Steps:



        Expected Result:


        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)
