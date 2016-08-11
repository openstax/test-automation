"""Concept Coach v1, Epic 12 - Delivering Assignments."""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
# from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
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
    str([
        7738, 7741, 7742, 7743, 7744,
        7745, 7746, 7747
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestDeliveringAssignments(unittest.TestCase):
    """CC1.12 - Delivering Assignments."""

    def setUp(self):
        """Pretest settings."""
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

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

    # Case C7738 - 001 - System | PDF is available for download for
    # CC derived copy
    @pytest.mark.skipif(str(7738) not in TESTS, reason='Excluded')
    def test_system_pdf_is_available_for_download_7738(self):
        """PDF is available for download for a Concept Coach derived copy.

        Steps:
        got to https://openstax.org/subjects/
        select a textbook
        select online view
        Scroll to the bottom of the page
        Click on the 'Downloads' button
        Click on the 'PDF' link
        Click on 'Download for Free'

        Expected Result:
        The book is downloaded as a PDF.
        """
        self.ps.test_updates['name'] = 'cc1.12.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cc1', 'cc1.12', 'cc1.12.001', '7738']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.driver.get('https://openstax.org/subjects')
        self.teacher.page.wait_for_page_load()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"cover")]')

            )
        ).click()
        self.teacher.page.wait_for_page_load()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[contains(@class,"get-this-title")]' +
                 '//a[contains(@href,"http://cnx.org/")]')

            )
        ).click()
        window_with_book = self.teacher.driver.window_handles[1]
        self.teacher.driver.switch_to_window(window_with_book)
        self.teacher.page.wait_for_page_load()
        self.teacher.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        self.teacher.driver.find_element(
            By.XPATH, '//div[@class="media-footer"]//li[@id="downloads-tab"]'
        ).click()
        self.teacher.driver.find_element(
            By.XPATH,
            '//div[@class="downloads tab-content"]' +
            '//td/a[contains(text(),".pdf")]'
        ).click()
        self.teacher.page.wait_for_page_load()
        self.teacher.driver.find_element(
            By.XPATH,
            '//a[contains(text(),"Download for Free")]'
        ).click()

        self.ps.test_updates['passed'] = True

    # Case C7741 - 002 - System | Webview table of contents matches the PDF
    # numbering
    @pytest.mark.skipif(str(7741) not in TESTS, reason='Excluded')
    def test_system_webview_table_of_contents_matches_the_pdf_numbe_7741(self):
        """Webview table of contents matches the PDF numbering.

        Steps:
        Go to Tutor
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a CC course name
        Click the 'Online Book' button
        Return to initial tab/window with tutor
        Click on 'HW PDF' -- a pdf will be downloaded

        Expected Result:
        The table of content numberings match between the web view and PDF.
        """
        self.ps.test_updates['name'] = 'cc1.12.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.12',
            'cc1.12.002',
            '7741'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7742 - 003 - Student | Find the CC book from an online search
    @pytest.mark.skipif(str(7742) not in TESTS, reason='Excluded')
    def test_student_find_the_cc_book_from_an_online_search_7742(self):
        """Find the Concept Coach book from an online search.

        Steps:
        Search the title of the book, along with 'openstax' through a search
            engine

        Expected Result:
        The search returns a link to the book
        """
        self.ps.test_updates['name'] = 'cc1.12.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.12',
            'cc1.12.003',
            '7742'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7743 - 004 - Student | Find the Concept Coach book from CNX
    @pytest.mark.skipif(str(7743) not in TESTS, reason='Excluded')
    def test_student_find_the_cc_book_from_cnx_7743(self):
        """Find the Concept Coach book from CNX.

        Steps:
        Go to CNX
        Search the name of the book in the 'Search Content' text box with '
        with Concept Coach' added to the search

        Expected Result:
        The book is displayed in the results
        """
        self.ps.test_updates['name'] = 'cc1.12.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.12',
            'cc1.12.004',
            '7743'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7746 - 005 - User | View the chapter and section number before the
    # CNX page module title
    @pytest.mark.skipif(str(7746) not in TESTS, reason='Excluded')
    def test_user_view_the_chapter_and_section_number_before_cnx_7746(self):
        """View the chapter and section number before the CNX page module title.

        Steps:
        Go to a Concept Coach book
        If the contents is not already open, Click on contents
        Click on a chapter
        Click on a section

        Expected Result:
        The chapter and section appear before the name of the module.
        """
        self.ps.test_updates['name'] = 'cc1.12.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.12',
            'cc1.12.005',
            '7746'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7747 - 006 - System | Display correct PDF numbering when the print
    # style is CCAP
    @pytest.mark.skipif(str(7747) not in TESTS, reason='Excluded')
    def test_system_display_correct_pdf_numbering_when_the_print_7747(self):
        """Display correct PDF numbering when the print style is CCAP.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 'cc1.12.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.12',
            'cc1.12.006',
            '7747'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
