"""Tutor v1, Epic 57 - CourseMaintenance."""

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
from staxing.helper import Admin  # NOQA


basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': '50.0',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([8311, 8312, 8313, 8314, 8315])  # NOQA
)


@PastaDecorator.on_platforms(BROWSERS)
class TestCourseMaintenance(unittest.TestCase):
    """T1.57 - Course Maintenance."""

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

    # Case C8311 - 001 - Admin | Import courses from Salesforece
    @pytest.mark.skipif(str(8311) not in TESTS, reason='Excluded')  # NOQA
    def test_admin_import_courses_from_salesforce(self):
        """Import courses from Salesforce

        Steps:
        Click on the user menu
        Click on the Admin option
        Click on Salesforce on the header
        Click on the Import Courses button

        Expected Result:

        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # Case C8312 - 002 - Admin | Update Salesforce Staistics
    @pytest.mark.skipif(str(8312) not in TESTS, reason='Excluded')  # NOQA
    def test_admin_update_salesforce_statistice(self):
        """Update Salesforce statistics

        Steps:
        Click on the user menu
        Click on the Admin option
        Click on Salesforce on the header
        Click on Update Salesforce

        Expected Result:

        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # Case C8313 - 003 - Admin | Exclude assesments from all courses
    @pytest.mark.skipif(str(8313) not in TESTS, reason='Excluded')  # NOQA
    def test_admin_exclude_assesments_from_all_courses(self):
        """Exclude assesments from all courses

        Steps:

        Expected Result:
        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # Case C8314 - 004 - Admin | Add a system notification
    @pytest.mark.skipif(str(8314) not in TESTS, reason='Excluded')  # NOQA
    def test_admin_add_a_system_notification(self):
        """Add a system notification

        Steps:
        Click on the user menu
        Click on the Admin option
        Click on System Setting on the header
        Click on the Notifications option
        Enter a notification into the New Notification text box
        Click on the Add button

        Expected Result:
        A system notification is added
        """
        self.ps.test_updates['name'] = 't1.57.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.57', 't1.57.004', '8314']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8315 - 005 - Admin | Delete a system notification
    @pytest.mark.skipif(str(8315) not in TESTS, reason='Excluded')  # NOQA
    def test_admin_delete_a_system_notification(self):
        """Delete a system notification

        Steps:
        Click on the user menu
        Click on the Admin option
        Click on System Setting on the header
        Click on the Notifications option
        Click on the Remove button next to a notification
        Click OK on the dialouge box

        Expected Result:
        A system notification is deleted
        """
        self.ps.test_updates['name'] = 't1.57.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.57', 't1.57.005', '8315']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True
