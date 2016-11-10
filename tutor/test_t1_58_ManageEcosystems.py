"""Tutor v1, Epic 58 - Manage ecosystems."""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
# from staxing.assignment import Assignment
from selenium.webdriver.common.keys import Keys

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Admin

# for template command line testing only
# - replace list_of_cases on line 31 with all test case IDs in this file
# - replace CaseID on line 52 with the actual cass ID
# - delete lines 17 - 22
list_of_cases = None
CaseID = 'skip'

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': 'latest',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([
        8316, 8317, 8318, 8319, 8320,
        8321, 8322, 8323, 8324, 8325,
        8326, 8327, 8328, 8329, 8330,
        8331, 8332, 8333, 8334, 8335,
        8336, 8337, 8338, 8339, 8340
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestManageEcosystems(unittest.TestCase):
    """T1.58 - Manage ecosystems."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.admin = Admin(
           use_env_vars=True,
           pasta_user=self.ps,
           capabilities=self.desired_capabilities
        )
        self.admin.login()

    def tearDown(self):
        """Test destructor."""
        self.ps.update_job(
            job_id=str(self.admin.driver.session_id),
            **self.ps.test_updates
        )
        try:
            self.admin.delete()
        except:
            pass

    # Case C8316 - 001 - Admin | Add a new course offering
    @pytest.mark.skipif(str(8316) not in TESTS, reason='Excluded')
    def test_admin_add_a_new_course_offering_8316(self):
        """Add a new course offering.

        Steps:
        Open the drop down menu by clicking on the user menu link containing
            the user's name
        Click on the 'Admin' button
        Open the drop down menu by clicking 'Course Organization'
        Click the 'Catalog Offerings' button
        Click the 'Add offering' button
        Enter text into the 'Salesforce book name' text box
        Enter text into the 'Appearance code' text box
        Enter text into the 'Description' text box
        Choose an option in the 'Ecosystem' drop down menu
        Check either the 'Works for full Tutor?' or the 'Works for
        Concept Coach?' button
        Enter text into the 'Pdf url" text box
        Enter text into the 'Webview url' text box
        Enter text into the 'Default course name' text box
        Click the 'Save' button

        Expected Result:
        The user is returned to the Catalog Offerings page and the text
        'The offering has been created.' is displayed.
        """
        self.ps.test_updates['name'] = 't1.58.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.58',
            't1.58.001',
            '8316'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.goto_admin_control()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Catalog Offerings')
            )
        ).click()

        assert('catalog_offerings' in self.admin.current_url()), \
            'Not in catalog offerings'

        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Add offering')
            )
        ).click()

        assert('catalog_offerings/new' in self.admin.current_url()), \
            'Not in catalog offerings'

        # Create the new course offering
        self.admin.find(
            By.XPATH,
            "//select[@id='offering_salesforce_book_name']").send_keys('O')
        self.admin.find(By.NAME, 'offering[appearance_code]').send_keys(
            'TestAutomation')
        self.admin.find(By.NAME, 'offering[description]').send_keys(
            'TestAutomation')
        self.admin.find(By.NAME, 'offering[content_ecosystem_id]').send_keys(
            'P')
        self.admin.find(By.ID, 'offering_is_tutor').click()
        self.admin.find(By.ID, 'offering_is_concept_coach').click()
        self.admin.find(By.NAME, 'offering[pdf_url]').send_keys(
            'TestAutomation.com')
        self.admin.find(By.NAME, 'offering[webview_url]').send_keys(
            'TestAutomation.com')
        self.admin.find(By.NAME, 'offering[default_course_name]').send_keys(
            'TestAutomation')
        self.admin.sleep(5)
        self.admin.find(By.XPATH, "//input[@class='btn btn-primary']").click()

        assert('catalog_offerings' in self.admin.current_url()), \
            'Not in catalog offerings'

        assert('new' not in self.admin.current_url()), \
            'Not in catalog offerings'

        self.admin.sleep(5)

        self.ps.test_updates['passed'] = True

    # Case C8317 - 002 - Admin | Edit the course offering book information
    @pytest.mark.skipif(str(8317) not in TESTS, reason='Excluded')
    def test_admin_edit_the_course_offering_book_info_8317(self):
        """Edit the course offering book information.

        Steps:
        Open the drop down menu by clicking on the user menu link
            containing the user's name
        Click on the 'Admin' button
        Open the drop down menu by clicking 'Course Organization'
        Click the 'Catalog Offerings' button
        Click the 'Edit' link for the desired course
        Edit the text in the 'Salesforce book name' text box
        Click the 'Save' button

        Expected Result:
        The Catalog Offerings page is reloaded with the changes visible
        and the text 'The offering has been updated.' is visible.
        """
        self.ps.test_updates['name'] = 't1.58.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.58',
            't1.58.002',
            '8317'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        change = '%s' % randint(100, 999)
        self.admin.goto_admin_control()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Catalog Offerings')
            )
        ).click()

        assert('catalog_offerings' in self.admin.current_url()), \
            'Not in catalog offerings'

        self.admin.find(By.PARTIAL_LINK_TEXT, 'Edit').click()

        # catalog_offerings/21/edit#offering_21
        assert('#offering_21' in self.admin.current_url()), \
            'Not editing the Automation course'

        self.admin.find(By.NAME, 'offering[salesforce_book_name]').clear()
        self.admin.find(By.NAME, 'offering[salesforce_book_name]').send_keys(
            'Automation' + change)
        self.admin.find(By.NAME, 'offering[appearance_code]').clear()
        self.admin.find(By.NAME, 'offering[appearance_code]').send_keys(
            'Automation' + change)
        self.admin.find(By.NAME, 'offering[description]').clear()
        self.admin.find(By.NAME, 'offering[description]').send_keys(
            'Automation' + change)
        self.admin.find(By.NAME, 'commit').click()

        self.ps.test_updates['passed'] = True

    # Case C8318 - 003 - Admin | Edit the course offering ecosystem
    @pytest.mark.skipif(str(8318) not in TESTS, reason='Excluded')
    def test_admin_edit_the_course_offering_ecosystem_8318(self):
        """Edit the course offering ecosystem.

        Steps:
        Open the drop down menu by clicking on the user menu link
            containing the user's name
        Click on the 'Admin' button
        Open the drop down menu by clicking 'Course Organization'
        Click the 'Catalog Offerings' button
        Click the 'Edit' link for the desired course
        Select a different option in the 'Ecosystem' drop down menu
        Click the 'Save' button

        Expected Result:
        The Catalog Offerings page is reloaded with the changes to the course
        and the text 'The offering has been updated.' is visible.
        """
        self.ps.test_updates['name'] = 't1.58.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.58',
            't1.58.003',
            '8318'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        # change = '%s' % randint(100, 999)
        self.admin.goto_admin_control()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Catalog Offerings')
            )
        ).click()

        assert('catalog_offerings' in self.admin.current_url()), \
            'Not in catalog offerings'

        self.admin.find(By.PARTIAL_LINK_TEXT, 'Edit').click()
        # catalog_offerings/21/edit#offering_21
        assert('#offering_21' in self.admin.current_url()), \
            'Not editing the Automation course'

        dropdown = self.admin.find(By.NAME, 'offering[content_ecosystem_id]')
        ecos = dropdown.find_elements_by_tag_name('option')
        for option in ecos:
            if option.text == '':
                option.click()  # select() in earlier versions of webdriver
                ecos.remove(option)
                break

        num = randint(0, len(ecos) - 1)
        ecos[num].click()

        self.admin.find(By.NAME, 'commit').click()

        self.admin.sleep(5)

        assert('edit' not in self.admin.current_url()), \
            'Editing a course'

        assert('catalog_offerings' in self.admin.current_url()), \
            'Not in catalog offerings'

        self.ps.test_updates['passed'] = True

    # Case C8319 - 004 - Admin | Edit the course offering course type
    @pytest.mark.skipif(str(8319) not in TESTS, reason='Excluded')
    def test_admin_edit_the_course_offering_course_type_8319(self):
        """Edit the course offering course type.

        Steps:
        Open the drop down menu by clicking on the user menu link
            containing the user's name
        Click on the 'Admin' button
        Open the drop down menu by clicking 'Course Organization'
        Click the 'Catalog Offerings' button
        Click the 'Edit' link for the desired course
        Edit the checkboxes for 'Works for full Tutor?' and 'Works for
        Concept Coach?'
        Click the 'Save' button

        Expected Result:
        The user is returned to the Catalog Offerings page with the
        changes visible. The text 'The offering has been updated.' is visible.
        """
        self.ps.test_updates['name'] = 't1.58.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.58',
            't1.58.004',
            '8319'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        # change = '%s' % randint(100, 999)
        self.admin.goto_admin_control()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Catalog Offerings')
            )
        ).click()

        assert('catalog_offerings' in self.admin.current_url()), \
            'Not in catalog offerings'

        self.admin.find(By.PARTIAL_LINK_TEXT, 'Edit').click()
        # catalog_offerings/21/edit#offering_21
        assert('#offering_21' in self.admin.current_url()), \
            'Not editing the Automation course'

        self.admin.find(By.ID, 'offering_is_tutor').click()
        self.admin.find(By.ID, 'offering_is_concept_coach').click()
        self.admin.find(By.NAME, 'commit').click()

        self.ps.test_updates['passed'] = True

    # Case C8320 - 005 - Admin | Edit the course offering CNX links
    @pytest.mark.skipif(str(8320) not in TESTS, reason='Excluded')
    def test_admin_edit_the_course_offering_cnx_links_8320(self):
        """Edit the course offering CNX links.

        Steps:
        Open the drop down menu by clicking on the user menu link
            containing the user's name
        Click on the 'Admin' button
        Open the drop down menu by clicking 'Course Organization'
        Click the 'Catalog Offerings' button
        Click the 'Edit' link for the desired course
        Edit the text in the 'Pdf url' text box
        Edit the text in the 'Webview url' text box
        Click the 'Save' button

        Expected Result:
        The user is returned to the Catalog Offerings page with the
        changes made to the course visible. The text 'The offering has been
        updated.' is visible.
        """
        self.ps.test_updates['name'] = 't1.58.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.58',
            't1.58.005',
            '8320'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        change = '%s' % randint(100, 999)
        self.admin.goto_admin_control()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Catalog Offerings')
            )
        ).click()

        assert('catalog_offerings' in self.admin.current_url()), \
            'Not in catalog offerings'

        self.admin.find(By.PARTIAL_LINK_TEXT, 'Edit').click()
        # catalog_offerings/21/edit#offering_21
        assert('#offering_21' in self.admin.current_url()), \
            'Not editing the Automation course'

        self.admin.find(By.NAME, 'offering[pdf_url]').clear()
        self.admin.find(By.NAME, 'offering[pdf_url]').send_keys(
            'Automation' + change + '.com')
        self.admin.find(By.NAME, 'offering[webview_url]').clear()
        self.admin.find(By.NAME, 'offering[webview_url]').send_keys(
            'Automation' + change + '.com')
        self.admin.find(By.NAME, 'commit').click()

        self.ps.test_updates['passed'] = True

    # Case C8321 - 006 - Admin | Edit the course offering's default course name
    @pytest.mark.skipif(str(8321) not in TESTS, reason='Excluded')
    def test_admin_edit_the_course_offering_default_name_8321(self):
        """Edit the course offering's default course name.

        Steps:
        Open the drop down menu by clicking on the user menu link
            containing the user's name
        Click on the 'Admin' button
        Open the drop down menu by clicking 'Course Organization'
        Click the 'Catalog Offerings' button
        Click the 'Edit' link for the desired course
        Edit the text in the 'Default course name' text box
        Click the 'Save' button

        Expected Result:
        The user is returned to the Catalog Offerings page with the changes
        to the course visible. The text 'The offering has been updated.'
        is visible.
        """
        self.ps.test_updates['name'] = 't1.58.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.58',
            't1.58.006',
            '8321'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        change = '%s' % randint(100, 999)
        self.admin.goto_admin_control()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Catalog Offerings')
            )
        ).click()

        assert('catalog_offerings' in self.admin.current_url()), \
            'Not in catalog offerings'

        self.admin.find(By.PARTIAL_LINK_TEXT, 'Edit').click()
        # catalog_offerings/21/edit#offering_21
        assert('#offering_21' in self.admin.current_url()), \
            'Not editing the Automation course'

        self.admin.find(By.NAME, 'offering[default_course_name]').clear()
        self.admin.find(By.NAME, 'offering[default_course_name]').send_keys(
            'Automation' + change)
        self.admin.find(By.NAME, 'commit').click()

        self.ps.test_updates['passed'] = True

    # Case C8322 - 007 - Admin | Import an ecosystem
    @pytest.mark.skipif(str(8322) not in TESTS, reason='Excluded')
    def test_admin_import_an_ecosystem_8322(self):
        """Import an ecosystem.

        Steps:
        Open the drop down menu by clicking on the user menu link
            containing the user's name
        Click on the 'Admin' button
        Open the drop down menu by clicking 'Content'
        Click the 'Ecosystems' button
        Click the 'Import a new Ecosystem' button
        Submit a .yml file in the 'Ecosystem Manifest (.yml)' box
        Write text into the 'Comments' text box
        Click the 'Import' button

        Expected Result:
        The user is returned to the Ecosystems page and the imported
        ecosystem is now visible in the list.
        """
        self.ps.test_updates['name'] = 't1.58.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.58',
            't1.58.007',
            '8322'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.goto_admin_control()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Content')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Ecosystems')
            )
        ).click()

        assert('ecosystems' in self.admin.current_url()), \
            'Not in ecosystems'

        self.admin.find(By.LINK_TEXT, 'Import a new Ecosystem').click()

        assert('new' in self.admin.current_url()), \
            'Not creating new ecosystem'

        self.admin.find(
            By.ID,
            'ecosystem_manifest'
        ).send_keys(
            '/Users/openstaxii/downloads/Biology_For_AP_Courses_' +
            'd52e93f4-8653-4273-86da-3850001c0786_3.14_-_' +
            '2015-09-29_13_37_55_UTC.yml'
        )
        self.admin.find(
            By.ID,
            'ecosystem_comments'
        ).send_keys(
            'Automated test upload'
        )
        self.admin.find(By.NAME, 'commit').click()

        self.admin.sleep(10)

        assert('new' not in self.admin.current_url()), \
            'On creating new ecosystem page'

        assert('ecosystems' in self.admin.current_url()), \
            'Not in ecosystems'

        self.ps.test_updates['passed'] = True

    # Case C8323 - 008 - Content Analyst | Import an ecosystem
    @pytest.mark.skipif(str(8323) not in TESTS, reason='Excluded')
    def test_content_import_an_ecosystem_8323(self):
        """Import an ecosystem.

        Steps:
        Open the drop down menu by clicking on the user menu link containing
            the user's name
        Click on the 'Customer Analyst' button
        Click the 'Ecosystems' button
        Click the 'Import a new Ecosystem' button
        Submit a .yml file in the 'Ecosystem Manifest (.yml)' box
        Write text into the 'Comments' text box
        Click the 'Import' button

        Expected Result:
        The user is returned to the Ecosystems page where the imported
        ecosystem is now visible in the list.
        """
        self.ps.test_updates['name'] = 't1.58.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.58',
            't1.58.008',
            '8323'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (
                    By.XPATH, '%s%s' %
                    ('//li[contains(@class,"-hamburger-menu")]/',
                     'a[@type="button"]')
                )
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'Customer Analyst')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//h1[text()="Content Analyst Console"]')
            )
        )

        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Ecosystems')
            )
        ).click()

        assert('content_analyst/ecosystems' in self.admin.current_url()), \
            'Not in ecosystems'

        self.admin.find(By.LINK_TEXT, 'Import a new Ecosystem').click()

        assert('new' in self.admin.current_url()), \
            'Not creating new ecosystem'

        self.admin.find(
            By.ID,
            'ecosystem_manifest'
        ).send_keys(
            '/Users/openstaxii/downloads/Biology_For_AP_Courses_' +
            'd52e93f4-8653-4273-86da-3850001c0786_3.14_-_' +
            '2015-09-29_13_37_55_UTC.yml'
        )
        self.admin.find(By.ID, 'ecosystem_comments').send_keys(
            'Automated test upload')
        self.admin.find(By.NAME, 'commit').click()

        self.admin.sleep(10)

        assert('new' not in self.admin.current_url()), \
            'On creating new ecosystem page'

        assert('ecosystems' in self.admin.current_url()), \
            'Not in ecosystems'

        self.ps.test_updates['passed'] = True

    # Case C8324 - 009 - Admin | Edit an ecosystem comment
    @pytest.mark.skipif(str(8324) not in TESTS, reason='Excluded')
    def test_admin_edit_an_ecosystem_comment_8324(self):
        """Edit an ecosystem comment.

        Steps:
        Open the drop down menu by clicking on the user menu
            link containing the user's name
        Click on the 'Admin' button
        Open the drop down menu by clicking 'Content'
        Click the 'Ecosystems' button
        Edit the 'Comments' text box for an ecosystem
        Click the 'Save' button

        Expected Result:
        The Ecosystems page is reloaded with changes to the comment visible.
        """
        self.ps.test_updates['name'] = 't1.58.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.58',
            't1.58.009',
            '8324'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        # change = '%s' % randint(100, 999)
        self.admin.goto_admin_control()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Content')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Ecosystems')
            )
        ).click()

        assert('ecosystems' in self.admin.current_url()), \
            'Not in ecosystems'

        self.admin.find(By.NAME, 'ecosystem[comments]').send_keys('|auto test')
        self.admin.find(By.NAME, 'commit').click()

        self.ps.test_updates['passed'] = True

    # Case C8325 - 010 - Content Analyst | Edit an ecosystem comment
    @pytest.mark.skipif(str(8325) not in TESTS, reason='Excluded')
    def test_content_edit_an_ecosystem_comment_8325(self):
        """Edit an ecosystem comment.

        Steps:
        Open the drop down menu by clicking on the user menu link
            containing the user's name
        Click on the 'Customer Analyst' button
        Click the 'Ecosystems' button
        Edit the 'Comments' text box for an ecosystem
        Click the 'Save' button

        Expected Result:
        The Ecosystems page is reloaded with changes to the comment visible.
        """
        self.ps.test_updates['name'] = 't1.58.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.58',
            't1.58.010',
            '8325'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (
                    By.XPATH, '%s%s' %
                    ('//li[contains(@class,"-hamburger-menu")]/',
                     'a[@type="button"]')
                )
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'Customer Analyst')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//h1[text()="Content Analyst Console"]')
            )
        )

        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Ecosystems')
            )
        ).click()

        assert('content_analyst/ecosystems' in self.admin.current_url()), \
            'Not in ecosystems'

        self.admin.find(By.NAME, 'ecosystem[comments]').send_keys('|auto test')
        self.admin.find(By.NAME, 'commit').click()

        self.ps.test_updates['passed'] = True

    # Case C8326 - 011 - Admin | Access the book content archive
    @pytest.mark.skipif(str(8326) not in TESTS, reason='Excluded')
    def test_admin_access_the_book_content_archive_8326(self):
        """Access the book content archive.

        Steps:
        Open the drop down menu by clicking on the user menu
            link containing the user's name
        Click on the 'Admin' button
        Open the drop down menu by clicking 'Content'
        Click the 'Ecosystems' button
        Click the 'Archive' button for a particular book

        Expected Result:
        The archive for the book is loaded.
        """
        self.ps.test_updates['name'] = 't1.58.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.58',
            't1.58.011',
            '8326'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.goto_admin_control()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Content')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Ecosystems')
            )
        ).click()

        assert('ecosystems' in self.admin.current_url()), \
            'Not in ecosystems'

        # self.admin.find(By.LINK_TEXT, 'Archive').click()
        link = self.admin.find(By.LINK_TEXT, 'Archive')
        self.admin.driver.get(link.get_attribute('href'))

        self.admin.sleep(5)
        assert('/contents/' in self.admin.current_url()), \
            'Not in archive'

        self.ps.test_updates['passed'] = True

    # Case C8327 - 012 - Content Analyst | Access the book content archive
    @pytest.mark.skipif(str(8327) not in TESTS, reason='Excluded')
    def test_content_access_the_book_content_archive_8327(self):
        """Access the book content archive.

        Steps:
        Open the drop down menu by clicking on the user menu link
            containing the user's name
        Click on the 'Customer Analyst' button
        Click the 'Ecosystems' button
        Click the 'Archive' button for a particular book

        Expected Result:

        """
        self.ps.test_updates['name'] = 't1.58.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.58',
            't1.58.012',
            '8327'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (
                    By.XPATH, '%s%s' %
                    ('//li[contains(@class,"-hamburger-menu")]/',
                     'a[@type="button"]')
                )
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'Customer Analyst')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//h1[text()="Content Analyst Console"]')
            )
        )

        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Ecosystems')
            )
        ).click()

        assert('ecosystems' in self.admin.current_url()), \
            'Not in ecosystems'

        # self.admin.find(By.LINK_TEXT, 'Archive').click()
        link = self.admin.find(By.LINK_TEXT, 'Archive')
        self.admin.driver.get(link.get_attribute('href'))

        self.admin.sleep(5)
        assert('/contents/' in self.admin.current_url()), \
            'Not in archive'

        self.ps.test_updates['passed'] = True

    # Case C8328 - 013 - Admin | Display the book UUID
    @pytest.mark.skipif(str(8328) not in TESTS, reason='Excluded')
    def test_admin_display_the_book_uuid_8328(self):
        """Display the book UUID.

        Steps:
        Open the drop down menu by clicking on the user menu
            link containing the user's name
        Click on the 'Admin' button
        Open the drop down menu by clicking 'Content'
        Click the 'Ecosystems' button
        Click the 'Show UUID' link for a particular book

        Expected Result:
        The UUID for the book is displayed
        """
        self.ps.test_updates['name'] = 't1.58.013' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.58',
            't1.58.013',
            '8328'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.goto_admin_control()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Content')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Ecosystems')
            )
        ).click()

        assert('ecosystems' in self.admin.current_url()), \
            'Not in ecosystems'

        self.admin.find(By.LINK_TEXT, 'Show UUID').click()

        self.admin.find(By.CLASS_NAME, 'popover-content')

        self.ps.test_updates['passed'] = True

    # Case C8329 - 014 - Content Analyst | Display the book UUID
    @pytest.mark.skipif(str(8329) not in TESTS, reason='Excluded')
    def test_content_display_the_book_uuid_8329(self):
        """Display the book UUID.

        Steps:
        Open the drop down menu by clicking on the user menu link containing
            the user's name
        Click on the 'Customer Analyst' button
        Click the 'Ecosystems' button
        Click the 'Show UUID' link for a particular book

        Expected Result:
        The UUID for the book is displayed.
        """
        self.ps.test_updates['name'] = 't1.58.014' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.58',
            't1.58.014',
            '8329'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (
                    By.XPATH, '%s%s' %
                    ('//li[contains(@class,"-hamburger-menu")]/',
                     'a[@type="button"]')
                )
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'Customer Analyst')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//h1[text()="Content Analyst Console"]')
            )
        )

        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Ecosystems')
            )
        ).click()

        assert('content_analyst/ecosystems' in self.admin.current_url()), \
            'Not in ecosystems'

        self.admin.find(By.LINK_TEXT, 'Show UUID').click()

        self.admin.find(By.CLASS_NAME, 'popover-content')

        self.ps.test_updates['passed'] = True

    # Case C8330 - 015 - Admin | Download an ecosystem manifest
    @pytest.mark.skipif(str(8330) not in TESTS, reason='Excluded')
    def test_admin_download_an_ecosystem_manifest_8330(self):
        """Download an ecosystem manifest.

        Steps:
        Open the drop down menu by clicking on the user menu link
            containing the user's name
        Click on the 'Admin' button
        Open the drop down menu by clicking 'Content'
        Click the 'Ecosystems' button
        Click the 'Download Manifest' link for a particular book

        Expected Result:
        The ecosystem's manifest is downloaded.
        """
        self.ps.test_updates['name'] = 't1.58.015' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.58',
            't1.58.015',
            '8330'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.goto_admin_control()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Content')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Ecosystems')
            )
        ).click()

        assert('ecosystems' in self.admin.current_url()), \
            'Not in ecosystems'

        self.admin.find(By.LINK_TEXT, 'Download Manifest').click()
        self.admin.sleep(5)
        pf = os.path.isfile(
            os.path.expanduser(
                "~/Downloads/College_Physics_031da8d3-b525-" +
                "429c-80cf-6c8ed997733a.yml"
            )
        )

        assert(pf), "Can't find downloaded manifest"

        self.ps.test_updates['passed'] = True

    # Case C8331 - 016 - Content Analyst | Download an ecosystem manifest
    @pytest.mark.skipif(str(8331) not in TESTS, reason='Excluded')
    def test_content_download_an_ecosystem_manifest_8331(self):
        """Download an ecosystem manifest.

        Steps:
        Open the drop down menu by clicking on the user menu link
            containing the user's name
        Click on the 'Customer Analyst' button
        Click the 'Ecosystems' button
        Click the 'Download Manifest' link for a book

        Expected Result:
        The ecosystem's manifest is downloaded.
        """
        self.ps.test_updates['name'] = 't1.58.016' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.58',
            't1.58.016',
            '8331'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (
                    By.XPATH, '%s%s' %
                    ('//li[contains(@class,"-hamburger-menu")]/',
                     'a[@type="button"]')
                )
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'Customer Analyst')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//h1[text()="Content Analyst Console"]')
            )
        )

        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Ecosystems')
            )
        ).click()

        assert('content_analyst/ecosystems' in self.admin.current_url()), \
            'Not in ecosystems'

        self.admin.find(By.LINK_TEXT, 'Download Manifest').click()
        self.admin.sleep(5)
        pf = os.path.isfile(
            os.path.expanduser(
                "~/Downloads/College_Physics_031da8d3-b525-429c-80cf-" +
                "6c8ed997733a.yml"
            )
        )

        assert(pf), "Can't find downloaded manifest"

        self.ps.test_updates['passed'] = True

    # Case C8332 - 017 - Admin | Delete an unused ecosystem
    @pytest.mark.skipif(str(8332) not in TESTS, reason='Excluded')
    def test_admin_delete_an_unused_ecosystem_8332(self):
        """Delete an unused ecosystem.

        Steps:
        Open the drop down menu by clicking on the user menu link
            containing the user's name
        Click on the 'Admin' button
        Open the drop down menu by clicking 'Content'
        Click the 'Ecosystems' button
        Click the 'Delete' button for a particular ecosystem
        Click 'OK' on the dialog box that appears

        Expected Result:
        Ecosystem is successfully deleted.
        """
        self.ps.test_updates['name'] = 't1.58.017' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.58',
            't1.58.017',
            '8332'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.admin.goto_admin_control()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Content')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Ecosystems')
            )
        ).click()

        assert('ecosystems' in self.admin.current_url()), \
            'Not in ecosystems'

        delete = ''
        lst = self.admin.driver.find_elements_by_link_text('Delete')
        for link in lst:
            if '334' in link.get_attribute("href"):
                # link.click()
                delete = link
        # self.admin.find(By.LINK_TEXT, 'Delete').click()

        delete.click()
        self.admin.sleep(3)
        self.admin.driver.switch_to.alert.accept()
        self.admin.sleep(60)
        '''
        How to verify?
        Didn't want to delete anything so did not test, should work
        '''

        self.ps.test_updates['passed'] = True

    # Case C8333 - 018 - Content Analyst | Delete an unused ecosystem
    @pytest.mark.skipif(str(8333) not in TESTS, reason='Excluded')
    def test_content_delete_an_unused_ecosystem_8333(self):
        """Delete an unused ecosystem.

        Steps:
        Open the drop down menu by clicking on the user menu link containing
            the user's name
        Click on the 'Customer Analyst' button
        Click the 'Ecosystems' button
        Click the 'Delete' button for a particular ecosystem
        Click 'OK' on the dialog box that appears

        Expected Result:
        Ecosystem is successfully deleted.
        """
        self.ps.test_updates['name'] = 't1.58.018' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.58',
            't1.58.018',
            '8333'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.admin.wait.until(
            expect.visibility_of_element_located(
                (
                    By.XPATH, '%s%s' %
                    ('//li[contains(@class,"-hamburger-menu")]/',
                     'a[@type="button"]')
                )
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'Customer Analyst')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//h1[text()="Content Analyst Console"]')
            )
        )

        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Ecosystems')
            )
        ).click()

        assert('content_analyst/ecosystems' in self.admin.current_url()), \
            'Not in ecosystems'

        self.admin.find(By.LINK_TEXT, 'Delete').click()
        self.admin.sleep(10)

        '''
        How to verfiy?
        Didn't want to delete so didn't test, should work
        '''

        self.ps.test_updates['passed'] = True

    # Case C8334 - 019 - Admin | Search for a tag
    @pytest.mark.skipif(str(8334) not in TESTS, reason='Excluded')
    def test_admin_search_for_a_tag_8334(self):
        """Search for a tag.

        Steps:
        Open the drop down menu by clicking on the user menu link containing
            the user's name
        Click on the 'Admin' button
        Open the drop down menu by clicking 'Content'
        Click the 'Tags' button
        Enter text into the text box with 'Search here'
        Click the 'Search' button

        Expected Result:
        Results of the search are returned.
        """
        self.ps.test_updates['name'] = 't1.58.019' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.58',
            't1.58.019',
            '8334'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.goto_admin_control()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Content')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Tags')
            )
        ).click()

        assert('tags' in self.admin.current_url()), \
            'Not in tags'

        self.admin.find(By.NAME, 'query').send_keys('bio')
        self.admin.find(By.NAME, 'query').send_keys(Keys.RETURN)

        assert('&query=bio&commit=Search' in self.admin.current_url()), \
            'Not viewing search results'

        self.ps.test_updates['passed'] = True

    # Case C8335 - 020 - Admin | Edit a tag
    @pytest.mark.skipif(str(8335) not in TESTS, reason='Excluded')
    def test_admin_edit_a_tag_8335(self):
        """Edit a tag.

        Steps:
        Open the drop down menu by clicking on the user menu link
            containing the user's name
        Click on the 'Admin' button
        Open the drop down menu by clicking 'Content'
        Click the 'Tags' button
        Enter text into the text box with 'Search here'
        Click the 'Search' button
        Click the 'Edit' button for one of the returned tags
        Edit the text box labeled 'Name'
        Edit the text box labeled 'Description'
        Click the 'Save' button

        Expected Result:
        The user is returned to the Tags page and the text
        'The tag has been updated.' is displayed.
        """
        self.ps.test_updates['name'] = 't1.58.020' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.58',
            't1.58.020',
            '8335'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        change = '%s' % randint(100, 999)
        self.admin.goto_admin_control()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Content')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Tags')
            )
        ).click()

        assert('tags' in self.admin.current_url()), \
            'Not in tags'

        self.admin.find(By.NAME, 'query').send_keys('bio')
        self.admin.find(By.NAME, 'query').send_keys(Keys.RETURN)

        assert('&query=bio&commit=Search' in self.admin.current_url()), \
            'Not viewing search results'

        self.admin.find(By.LINK_TEXT, 'Edit').click()

        assert('edit' in self.admin.current_url()), \
            'Not editing a tag'

        self.admin.find(By.ID, 'tag_name').clear()
        self.admin.find(By.ID, 'tag_description').clear()
        self.admin.find(By.ID, 'tag_name').send_keys('Automation' + change)
        self.admin.find(By.ID, 'tag_description').send_keys(
            'Automation' + change)
        self.admin.find(By.NAME, 'commit').click()

        assert('edit' not in self.admin.current_url()), \
            'Should not be editing a tag'

        assert('tags' in self.admin.current_url()), \
            'Not at the tags page'

        self.ps.test_updates['passed'] = True

    # Case C8336 - 021 - Admin | Search for a job by ID
    @pytest.mark.skipif(str(8336) not in TESTS, reason='Excluded')
    def test_admin_search_for_a_job_by_id_8336(self):
        """Search for a job by ID.

        Steps:
        Open the drop down menu by clicking on the user menu link
            containing the user's name
        Click on the 'Admin' button
        Click the 'Jobs' button
        Enter a job ID into the text box labeled
        'Search by ID, Status, or Progress'

        Expected Result:
        The results to the search are displayed.
        """
        self.ps.test_updates['name'] = 't1.58.021' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.58',
            't1.58.021',
            '8336'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.goto_admin_control()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Jobs')
            )
        ).click()

        assert('jobs' in self.admin.current_url()), \
            'Not at the jobs page'

        self.admin.find(By.ID, 'filter_id').send_keys('4d')
        page = self.admin.driver.page_source
        assert('004eefa9-6d0e-4d7d-b708-9e4106a6bd30' in page), \
            'Thing not in results'

        self.ps.test_updates['passed'] = True

    # Case C8337 - 022 - Admin | Search for a job by status
    @pytest.mark.skipif(str(8337) not in TESTS, reason='Excluded')
    def test_admin_search_for_a_job_by_status_8337(self):
        """Search for a job by status.

        Steps:
        Open the drop down menu by clicking on the user menu
            link containing the user's name
        Click on the 'Admin' button
        Click the 'Jobs' button
        Enter a job status into the text box labeled
        'Search by ID, Status, or Progress'

        Expected Result:
        The results of the search are displayed.
        """
        self.ps.test_updates['name'] = 't1.58.022' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.58',
            't1.58.022',
            '8337'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.goto_admin_control()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Jobs')
            )
        ).click()

        assert('jobs' in self.admin.current_url()), \
            'Not at the jobs page'

        self.admin.find(By.ID, 'filter_id').send_keys('succeeded')
        self.admin.sleep(5)
        self.admin.find(By.ID, 'filter_id').clear()
        self.admin.find(By.ID, 'filter_id').send_keys('failed')
        self.admin.sleep(5)
        self.admin.find(By.ID, 'filter_id').clear()
        self.admin.find(By.ID, 'filter_id').send_keys('queued')
        self.admin.sleep(5)
        self.admin.find(By.ID, 'filter_id').clear()
        self.admin.find(By.ID, 'filter_id').send_keys('started')

        self.ps.test_updates['passed'] = True

    # Case C8338 - 023 - Admin | Search for a job by progress percentage
    @pytest.mark.skipif(str(8338) not in TESTS, reason='Excluded')
    def test_admin_search_for_a_job_by_progress_percentage_8338(self):
        """Search for a job by progress percentage.

        Steps:
        Open the drop down menu by clicking on the user menu link
            containing the user's name
        Click on the 'Admin' button
        Click the 'Jobs' button
        Enter a job progress percentage into the text box labeled
        'Search by ID, Status, or Progress'

        Expected Result:
        The results of the search are displayed.
        """
        self.ps.test_updates['name'] = 't1.58.023' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.58',
            't1.58.023',
            '8338'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.goto_admin_control()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Jobs')
            )
        ).click()

        assert('jobs' in self.admin.current_url()), \
            'Not at the jobs page'

        self.admin.find(By.ID, 'filter_id').send_keys('100%')
        self.admin.sleep(5)
        page = self.admin.driver.page_source
        assert('0011b6e4-9c58-4e73-a6ce-e53d0814afdc' in page), \
            'Search results different from expected'

        self.admin.find(By.ID, 'filter_id').clear()
        self.admin.find(By.ID, 'filter_id').send_keys('20%')
        self.admin.sleep(5)
        self.admin.find(By.ID, 'filter_id').clear()
        self.admin.find(By.ID, 'filter_id').send_keys(' 0%')
        self.admin.sleep(5)

        page = self.admin.driver.page_source
        assert('008e4642-85a0-4fff-86ed-4f1e7be02233' in page), \
            'Search results different from expected'

        '''
        How to verify?
        '''

        self.ps.test_updates['passed'] = True

    # Case C8339 - 024 - Admin | Filter jobs by status
    @pytest.mark.skipif(str(8339) not in TESTS, reason='Excluded')
    def test_admin_filter_jobs_by_status_8339(self):
        """Filter jobs by status.

        Steps:
        Open the drop down menu by clicking on the user menu link
            containing the user's name
        Click on the 'Admin' button
        Click the 'Jobs' button
        Click one of the status tabs to filter jobs

        Expected Result:
        Jobs that fit the filter condition are displayed.
        """
        self.ps.test_updates['name'] = 't1.58.024' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.58',
            't1.58.024',
            '8339'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.goto_admin_control()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Jobs')
            )
        ).click()

        assert('jobs' in self.admin.current_url()), \
            'Not at the jobs page'

        self.admin.find(By.LINK_TEXT, 'all').click()
        assert('all' in self.admin.current_url()), \
            'Not viewing all jobs'
        self.admin.sleep(5)

        self.admin.find(By.LINK_TEXT, 'incomplete').click()
        assert('incomplete' in self.admin.current_url()), \
            'Not viewing incomplete jobs'
        self.admin.sleep(5)

        self.admin.find(By.LINK_TEXT, 'succeeded').click()
        assert('succeeded' in self.admin.current_url()), \
            'Not viewing succeeded jobs'
        self.admin.sleep(5)

        self.admin.find(By.LINK_TEXT, 'queued').click()
        assert('queued' in self.admin.current_url()), \
            'Not viewing queued jobs'
        self.admin.sleep(5)

        self.admin.find(By.LINK_TEXT, 'started').click()
        assert('started' in self.admin.current_url()), \
            'Not viewing started jobs'
        self.admin.sleep(5)

        self.admin.find(By.LINK_TEXT, 'failed').click()
        assert('failed' in self.admin.current_url()), \
            'Not viewing failed jobs'
        self.admin.sleep(5)

        self.admin.find(By.LINK_TEXT, 'killed').click()
        assert('killed' in self.admin.current_url()), \
            'Not viewing killed jobs'
        self.admin.sleep(5)

        self.admin.find(By.LINK_TEXT, 'unknown').click()
        assert('unknown' in self.admin.current_url()), \
            'Not viewing unknown jobs'

        self.ps.test_updates['passed'] = True

    # Case C8340 - 025 - Admin | View a job report
    @pytest.mark.skipif(str(8340) not in TESTS, reason='Excluded')
    def test_admin_view_a_job_report_8340(self):
        """View a job report.

        Steps:
        Open the drop down menu by clicking on the user menu link containing
            the user's name
        Click on the 'Admin' button
        Click the 'Jobs' button
        Click on a Job ID

        Expected Result:
        The report for the Job is displayed.
        """
        self.ps.test_updates['name'] = 't1.58.025' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.58',
            't1.58.025',
            '8340'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.admin.goto_admin_control()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Jobs')
            )
        ).click()

        assert('jobs' in self.admin.current_url()), \
            'Not at the jobs page'

        self.admin.find(By.ID, 'filter_id').send_keys(
            '008e4642-85a0-4fff-86ed-4f1e7be02233')
        self.admin.find(
            By.LINK_TEXT, '008e4642-85a0-4fff-86ed-4f1e7be02233').click()

        url = self.admin.current_url()
        assert('jobs/008e4642-85a0-4fff-86ed-4f1e7be02233' in url), \
            'Not at the jobs page'

        self.ps.test_updates['passed'] = True
