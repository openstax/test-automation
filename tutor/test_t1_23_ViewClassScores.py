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
    str([8156, 8157, 8158, 8159, 
         8160, 8161, 8162, 8163,
         8164, 8165, 8166, 8167,
         8168, 8169, 8170, 8171,
         8172, 8173, 8174, 8175, 
         8176, 8177, 8178, 8179,
         8180, 8181])  # NOQA
)


@PastaDecorator.on_platforms(BROWSERS)
class TestEpicName(unittest.TestCase):
    """T1.14 - Create a Reading."""

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

    # Case C7992 - 001 - Teacher | Add a reading using the Add Assignment drop down menu
    @pytest.mark.skipif(str(7992) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Add a reading using the Add Assignment drop down menu.

        Steps: 

        Click on the 'Add Assignment' drop down menu
        Click on the 'Add Reading' option

        Enter an assignment name into the Assignment name text box [user decision]
        [optional] Enter an assignment description into the Assignment description or special instructions text box
        [optional] Enter into Open Date text field date as MM/DD/YYYY
        Enter into Due Date text field date as MM/DD/YYYY
        Click on the "+ Add Readings" button
        Click on section(s) to add to assignment [user decision]
        scroll to bottom
        Click on the "Add Readings" button
        Click on the Publish' button

        Expected Result:

        Takes user back to calendar dashboard. 
        Assignment appears on user calendar dashboard on due date with correct readings.

        """
        self.ps.test_updates['name'] = 't1.14.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.14',
            't1.14.001',
            '7992'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True
