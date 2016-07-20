"""Concept Coach v1, Epic 6.

Concept Coach Widget Mechanics and Infrastructure.
"""

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
from staxing.helper import Student, Teacher  # NOQA

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': '50.0',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([7748, 7749, 7750])  # NOQA
)


@PastaDecorator.on_platforms(BROWSERS)
class TestConceptCoachWidgetMechanicsAndInfrastructure(unittest.TestCase):
    """CC1.06 - Concept Coach Widget Mechanics and Infrastructure."""

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

    # Case C7748 - 001 - Student | View a Concept Coach book and see the widget
    @pytest.mark.skipif(str(7748) not in TESTS, reason='Excluded')  # NOQA
    def test_student_view_a_cc_book_and_see_the_widget_7748(self):
        """View a Concept Coach book and see the widget.

        Steps:

        go to tutor-qa
        login as a student
        click on a concept coach book
        Click on the 'Contents +' button
        Click on the a chapter in the contents
        Click on a section other than the introduction
        Scroll down



        Expected Result:

        Concept Coach widget visible

        """
        self.ps.test_updates['name'] = 'cc1.06.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.06',
            'cc1.06.001',
            '7748'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C7749 - 002 - Teacher | View a Concept Coach book and see the widget
    @pytest.mark.skipif(str(7749) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_view_a_cc_book_and_see_the_widget_7749(self):
        """View a Concept Coach book and see the widget.

        Steps:

        go to tutor-qa
        login as a teacher
        Click on a concept coach book
        Click on 'Online Book' in the header
        Click on the 'Contents +' button
        Click on the a chapter in the contents
        Click on a section other than the introduction
        Scroll down


        Expected Result:

        Concept Coach widget visible

        """
        self.ps.test_updates['name'] = 'cc1.06.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.06',
            'cc1.06.002',
            '7749'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C7750 - 003 - Student | Doesn't see end-of-page exercise sections
    @pytest.mark.skipif(str(7750) not in TESTS, reason='Excluded')  # NOQA
    def test_student_doesnt_see_end_of_page_exercise_sections_7750(self):
        """Doesn't see end-of-page exercise sections.

        Steps:

        go to tutor-qa
        login as a student
        click on a concept coach book
        Click on the 'Contents +' button
        Click on the a chapter in the contents
        Click on a section other than the introduction
        Scroll down


        Expected Result:

        End-of-page exercise sections are not displayed.

        """
        self.ps.test_updates['name'] = 'cc1.06.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.06',
            'cc1.06.003',
            '7750'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True
