"""Tutor v2, Epic 18 - Guide, Monitor, Support, and Train Users."""

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
    'version': '50.0',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([14750, 14751, 14752, 14755, 14756])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestGuideMonitorSupportAndTrainUsers(unittest.TestCase):
    """T2.18 - Guide, Monitor, Support, and Train Users."""

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
        self.ps.update_job(
            job_id=str(self.teacher.driver.session_id),
            **self.ps.test_updates
        )
        try:
            self.teacher.delete()
        except:
            pass

    # 14750 - 001 - Student | Directed to a "No Courses" page when not in any
    # courses yet
    @pytest.mark.skipif(str(14750) not in TESTS, reason='Excluded')
    def test_student_directed_to_a_no_courses_page_when_not_in_any_14750(self):
        """Directed to a "No Courses" page when not in any courses yet.

        Steps:
        Go to tutor-qa.openstax.org
        Log in as qa_student_37003

        Expected Result:
        The message "We cannot find an OpenStax course associated with your
        account" displays with help links
        """
        self.ps.test_updates['name'] = 't2.18.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.18',
            't2.18.001',
            '14750'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 14751 - 002 - Teacher | Directed to a "No Courses" page when not in any
    # courses yet
    @pytest.mark.skipif(str(14751) not in TESTS, reason='Excluded')
    def test_teacher_directed_to_a_no_courses_page_when_not_in_any_14751(self):
        """Directed to a "No Courses" page when not in any courses yet.

        Steps:
        Go to tutor-qa.openstax.org
        Log in as demo_teacher

        Expected Result:
        The message "We cannot find an OpenStax course associated with your
        account" displays with help links
        """
        self.ps.test_updates['name'] = 't2.18.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.18',
            't2.18.002',
            '14751'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 14752 - 003 - User | In-app Notification of downtime
    @pytest.mark.skipif(str(14752) not in TESTS, reason='Excluded')
    def test_user_inapp_notification_of_downtime_14752(self):
        """In-app Notification of downtime.

        Steps:
        Go to tutor-qa
        Log in as admin [admin:password]
        Click "Admin" from the user menu
        Click "System Setting"
        Click "Notifications"
        Enter a new notification into the text box
        Click "Add"
        Log out of admin account
        Log in as teacher01

        Expected Result:
        An orange header with the notification pops up when you sign in
        """
        self.ps.test_updates['name'] = 't2.18.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.18',
            't2.18.003',
            '14752'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 14755 - 004 - Teacher | Guided tutorial of Tutor in Tutor
    @pytest.mark.skipif(str(14755) not in TESTS, reason='Excluded')
    def test_teacher_guided_tutorial_of_tutor_in_tutor_14755(self):
        """Guided tutorial of Tutor in Tutor.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.18.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.18',
            't2.18.004',
            '14755'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # 14756 - 005 - Student | Guided tutorial of Tutor in Tutor
    @pytest.mark.skipif(str(14756) not in TESTS, reason='Excluded')
    def test_student_guided_tutorial_of_tutor_in_tutor_14756(self):
        """Guided tutorial of Tutor in Tutor.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 't2.18.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.18',
            't2.18.005',
            '14756'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
