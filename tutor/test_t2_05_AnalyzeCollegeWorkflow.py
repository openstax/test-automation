"""Tutor v2, Epic 5 - Analyze College Workflow."""

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
from staxing.helper import Teacher, Student  # NOQA

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': '50.0',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([14645, 14646, 14647, 14648, 14649, 14650])  # NOQA
)


@PastaDecorator.on_platforms(BROWSERS)
class TestAnalyzeCollegeWorkflow(unittest.TestCase):
    """T2.05 - Analyze College Workflow."""

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

    # 14645 - 001 - Student | All work is visible for college students
    # not just "This Week"
    @pytest.mark.skipif(str(14645) not in TESTS, reason='Excluded')  # NOQA
    def test_student_all_work_is_visible_for_college_students_14645(self):
        """All work is visible for college students, not just 'This Week'.

        Steps:

        Log into tutor-qa as student
        Click on a college course


        Expected Result:

        Can view assignments due later than this week


        """
        self.ps.test_updates['name'] = 't2.05.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.05',
            't2.05.001',
            '14645'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14646 - 002 - Teacher | Create a link to the OpenStax Dashboard
    @pytest.mark.skipif(str(14646) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_create_a_link_to_the_openstax_dashboard_14646(self):
        """Create a link to the OpenStax Dashboard.

        Steps:



        Expected Result:


        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # 14647 - 003 - Teacher | Create a link to the OpenStax Dashboard
    @pytest.mark.skipif(str(14647) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_create_a_link_to_the_openstax_dashboard_14647(self):
        """Create a link to the OpenStax Dashboard.

        Steps:



        Expected Result:


        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # 14648 - 004 - Teacher | Create links to assigned readings in their LMS
    @pytest.mark.skipif(str(14648) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_create_links_to_assigned_readings_in_lms_14648(self):
        """Create links to assigned readings in their LMS.

        Steps:

        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a CC course name

        Click on a published reading assignment on the calendar dashboard
        Click "Get Assignment Link"


        Expected Result:

        The user is presented with links to assigned readings


        """
        self.ps.test_updates['name'] = 't2.05.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.05',
            't2.05.004',
            '14648'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14649 - 005 - Teacher | Create links to assigned homework in their LMS
    @pytest.mark.skipif(str(14649) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_create_links_to_assigned_homework_in_lms_14649(self):
        """Create links to assigned homework in their LMS.

        Steps:

        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a CC course name

        Click on a published homework assignment on the calendar dashboard
        Click "Get Assignment Link"


        Expected Result:

        The user is presented with links to assigned homework


        """
        self.ps.test_updates['name'] = 't2.05.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.05',
            't2.05.005',
            '14649'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14650 - 006 - Teacher | View instructions on how to export summary grade
    # for my student's OpenStax practice to my LMS
    @pytest.mark.skipif(str(14650) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_view_instructions_on_how_to_export_summary_14650(self):
        """View instructions on how to export summary grade into LMS.

        Steps:



        Expected Result:


        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)
