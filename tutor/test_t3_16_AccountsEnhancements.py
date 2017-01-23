"""Tutor v3, Epic 16 - AccountsEnhancements."""

import inspect
import json
import os
import pytest
import unittest
import datetime

from pastasauce import PastaSauce, PastaDecorator
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
# from staxing.assignment import Assignment
from staxing.helper import Teacher
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.action_chains import ActionChains


basic_test_env = json.dumps([
    {
        'platform': 'Windows 10',
        'browserName': 'chrome',
        'version': 'latest',
        'screenResolution': "1024x768",
    }
])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
LOCAL_RUN = os.getenv('LOCALRUN', 'false').lower() == 'true'
TESTS = os.getenv(
    'CASELIST',
    str([
        105592, 105593, 105594, 105595, 105596,
        105597, 105598, 105599, 105600, 105601,
        105602, 107581, 107586, 107587, 107588,
        107589, 107590, 107591, 107592, 107593,
        107594
    ])
)

@PastaDecorator.on_platforms(BROWSERS)
class TestViewTheCalendarDashboard(unittest.TestCase):
    """T3.16 - Accounts Enhancements."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        if not LOCAL_RUN:
            self.teacher = Teacher(
                use_env_vars=True,
                pasta_user=self.ps,
                capabilities=self.desired_capabilities
            )
        else:
            self.teacher = Teacher(
                use_env_vars=True
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

    # Case C105592 - 001 - Student | Cannot use the same email for more than
    # one account
    @pytest.mark.skipif(str(105592) not in TESTS, reason='Excluded')
    def test_student_cannot_use_the_same_email_for_more_than_one_105592(self):
        """Cannot use the same email for more than one account.

        Steps:
        If the user has more than one course, click on a Tutor course name

        Expected Result:
        The teacher is presented their calendar dashboard.
        """
        self.ps.test_updates['name'] = 't3.16.001' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t3', 't3.16', 't3.16.001', '105592']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
