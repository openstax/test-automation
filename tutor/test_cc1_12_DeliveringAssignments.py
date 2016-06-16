"""Concept Coach v1, Epic 12 - Delivering Assignments."""

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
from staxing.helper import Teacher, Student, User, System  # NOQA

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': '50.0',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([7738, 7739, 7740, 7741, 7742,
         7743, 7744, 7745, 7746, 7747])  # NOQA
)


@PastaDecorator.on_platforms(BROWSERS)
class TestEpicName(unittest.TestCase):
    """CC1.12 - Delivering Assignments."""

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

    # Case C7738 - 001 - System | PDF is available for download for a Concept Coach derived copy
    @pytest.mark.skipif(str(7738) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """PDF is available for download for a Concept Coach derived copy. 

        Steps: 

        Login as teacher:

        Go to https://tutor-staging.openstax.org/
        Click on the 'Login' button
        Enter the teacher user account [ teacher05 | password ] in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a Concept Coach course name
        Click on the 'Online Book' button
        Click on the 'Get This Book!' button
        Click on the 'PDF' link
        Click on 'Download for Free'

        Login as student:

        Go to https://tutor-staging.openstax.org/
        Click on the 'Login' button
        Enter the teacher user account [ student01 | password ] in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a Concept Coach course name
        Click on the 'Get This Book!' button
        Click on the 'PDF' link
        Click on 'Download for Free'


        Expected Result:

        The book is downloaded as a PDF.

        """
        self.ps.test_updates['name'] = 'cc1.12.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.12',
            'cc1.12.001',
            '7738'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C7739 - 002 - Teacher | Assign readings with the PDF open
    @pytest.mark.skipif(str(7739) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Assign readings with the PDF open

        Steps:


        Expected Result:


        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)


    # Case C7740 - 003 - Teacher | Assign readings with Webview open
    @pytest.mark.skipif(str(7740) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Assign readings with Webview open

        Steps:


        Expected Result:


        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)


    # Case C7741 - 004 - System | Webview table of contents matches the PDF numbering
    @pytest.mark.skipif(str(7741) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Webview table of contents matches the PDF numbering

        Steps: 

        Go to https://tutor-staging.openstax.org/
        Click on the 'Login' button
        Enter the teacher user account [ teacher05 | password ] in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a Concept Coach course name
        Click the 'Online Book' button
        Return to initial tab/window with tutor
        Click on 'HW PDF' -- a pdf will be downloaded


        Expected Result:

        The table of content numberings match between the web view and PDF.

        """
        self.ps.test_updates['name'] = 'cc1.12.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.12',
            'cc1.12.004',
            '7741'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C7742 - 005 - Student | Find the Concept Coach book from an online search
    @pytest.mark.skipif(str(7742) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Find the Concept Coach book from an online search

        Steps: 

        Search the title of the book, along with 'openstax' through a search engine


        Expected Result:

        The search returns a link to the book

        """
        self.ps.test_updates['name'] = 'cc1.12.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.12',
            'cc1.12.005',
            '7742'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C7743 - 006 - Student | Find the Concept Coach book from CNX
    @pytest.mark.skipif(str(7743) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Find the Concept Coach book from CNX

        Steps: 

        Go to https://legacy.cnx.org
        Search the name of the book in the 'Search Content' text box with ' with Concept Coach' added to the search


        Expected Result:

        The book is displayed in the results

        """
        self.ps.test_updates['name'] = 'cc1.12.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.12',
            'cc1.12.006',
            '7743'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C7744 - 007 - Teacher | Assign standard problems from the homework PDF
    @pytest.mark.skipif(str(7744) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Assign standard problems from the homework PDF

        Steps:


        Expected Result:


        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)


    # Case C7745 - 008 - Teacher | Assign standard problems from Webview
    @pytest.mark.skipif(str(7745) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Assign standard problems from the homework PDF

        Steps:


        Expected Result:


        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)


    # Case C7746 - 009 - User | View the chapter and section number before the CNX page module title
    @pytest.mark.skipif(str(7746) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """View the chapter and section number before the CNX page module title

        Steps:

        Go to a concept coach book
        If the contents is not already open, Click on contents
        Click on a chapter
        Click on a section


        Expected Result:

        The chapter and section appear before the name of the module.


        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)


    # Case C7747 - 010 - System | Display correct PDF numbering when the print style is CCAP
    @pytest.mark.skipif(str(7747) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Display correct PDF numbering when the print style is CCAP

        Steps:


        Expected Result:


        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)


