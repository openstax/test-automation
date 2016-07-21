"""Concept Coach v1, Epic 5 - CNX Navigation."""

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
from staxing.helper import Student, Teacher, Admin  # NOQA

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': '50.0',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([7625, 7626, 7627, 7628, 7629, 7630])  # NOQA
)


@PastaDecorator.on_platforms(BROWSERS)
class TestCNXNavigation(unittest.TestCase):
    """CC1.05 - CNX Navigation."""

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

    # Case C7625 - 001 - Student | Log into Concept Coach for a course on CNX
    @pytest.mark.skipif(str(7625) not in TESTS, reason='Excluded')  # NOQA
    def test_student_log_into_cc_for_a_course_on_cnx_7625(self):
        """Log into Concept Coach for a course on CNX.

        Steps:

        Go to tutor-qa
        Click on the 'Login' button
        Enter the student user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a CC course name


        Expected Result:

        The student logs into Concept Coach

        """
        self.ps.test_updates['name'] = 'cc1.05.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.05',
            'cc1.05.001',
            '7625'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C7626 - 002 - Student | Following CC login author links are not seen
    @pytest.mark.skipif(str(7626) not in TESTS, reason='Excluded')  # NOQA
    def test_student_following_cc_login_author_links_are_not_seen_7626(self):
        """Following Concept Coach login author links are not seen.

        Steps:

        Go to tutor-qa
        Click on the 'Login' button
        Enter the student user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a CC course name


        Expected Result:

        Author links should not be seen

        """
        self.ps.test_updates['name'] = 'cc1.05.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.05',
            'cc1.05.002',
            '7626'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C7627 - 003 - Student | Able to use the table of contents to
    # navigate the book without impacting the reading assignment
    @pytest.mark.skipif(str(7627) not in TESTS, reason='Excluded')  # NOQA
    def test_student_able_to_use_the_table_of_contents_to_navigate_7627(self):
        """Navigate the book without impacting the reading assignment.

        Steps:

        Click on the "Contents" button


        Expected Result:

        The user is able to navigate the book without impacting the reading
        assignment

        """
        self.ps.test_updates['name'] = 'cc1.05.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.05',
            'cc1.05.003',
            '7627'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C7628 - 004 - Student | Able to search within the book
    @pytest.mark.skipif(str(7628) not in TESTS, reason='Excluded')  # NOQA
    def test_student_able_to_search_within_the_book_7628(self):
        """Able to search within the book.

        Steps:

        Enter search words into the search engine next to the "Contents" button


        Expected Result:

        The search word is highlighted in yellow within the text and is bolded
        within the table of contents

        """
        self.ps.test_updates['name'] = 'cc1.05.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.05',
            'cc1.05.004',
            '7628'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C7629 - 005 - Teacher | Able to search within the book
    @pytest.mark.skipif(str(7629) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_able_to_search_within_the_book_7629(self):
        """Able to search within the book.

        Steps:

        Go to tutor-qa
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a CC course name

        Click "Online Book" in the header
        Enter search words into the search engine next to the "Contents" button


        Expected Result:

        The search word is highlighted in yellow within the text and is bolded
        within the table of contents

        """
        self.ps.test_updates['name'] = 'cc1.05.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.05',
            'cc1.05.005',
            '7629'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C7630 - 006 - Admin | CNX URLs are shorter
    @pytest.mark.skipif(str(7630) not in TESTS, reason='Excluded')  # NOQA
    def test_admin_cnx_urls_are_shorter_7630(self):
        """CNX URLs are shorter.

        Steps:

        Go to https://demo.cnx.org/scripts/settings.js
        Scroll down to the bottom of the page under "conceptCoach"



        Expected Result:

        CNX URLs are shorter than the first URL

        """
        self.ps.test_updates['name'] = 'cc1.05.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.05',
            'cc1.05.006',
            '7630'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True
