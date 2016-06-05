"""Tutor v1, Epic 08 - StudentsWorkAssignments."""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
from random import randint  # NOQA
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as expect
# from staxing.assignment import Assignment
# from staxing.helper import Teacher, Student
from staxing.helper import Teacher

basic_test_env = json.dumps([
    {
        'platform': 'Windows 10',
        'browserName': 'chrome',
        'version': '50.0',
        'screenResolution': "1024x768",
    },
    {
        'platform': 'Windows 7',
        'browserName': 'firefox',
        'version': 'latest',
        'screenResolution': '1024x768',
    },
])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([7978])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestViewTheCalendarDashboard(unittest.TestCase):
    """T1.13 - View the calendar."""

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
        self.ps.update_job(job_id=str(self.teacher.driver.session_id),
                           **self.ps.test_updates)
        try:
            self.teacher.delete()
        except:
            pass

    # Case C7978 - 001 - Teacher | View the calendar dashboard
    @pytest.mark.skipif(str(7978) not in TESTS, reason='Excluded')
    def test_teacher_view_the_calendar_dashboard_7978(self):
        """View the calendar dashboard.

        Steps:
        Go to https://tutor-XXXX.openstax.org/
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a Tutor course name

        Expected Result:
        The teacher is presented their calendar dashboard.
        """
        self.ps.test_updates['name'] = 't1.13.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.001', '7978']
        self.ps.test_updates['passed'] = False

        self.teacher.select_course(appearance='physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.ps.test_updates['passed'] = True
