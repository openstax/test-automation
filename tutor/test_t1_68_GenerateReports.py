"""Tutor v1, Epic 68 - Generate Reports."""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
# from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect

from staxing.helper import Admin

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': '50.0',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([8361])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestGenerateReports(unittest.TestCase):
    """T1.68 - Generate Reports."""

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
        self.ps.update_job(job_id=str(self.admin.driver.session_id),
                           **self.ps.test_updates)
        try:
            self.admin.delete()
        except:
            pass

    # Case C8361 - 001 - Admin | Export research data to OwnCloud Research
    @pytest.mark.skipif(str(8361) not in TESTS, reason='Excluded')
    def test_admin_export_research_data_to_own_cloud_research_8361(self):
        """Export research data to OwnCloud Research.

        Steps:
        Open the user menu by clicking on the user's name
        Click on the 'Admin' button
        Click the 'Research Data' button
        Click on the 'Export Data' button

        Expected Result:
        The page is reloaded and a confirmation message is displayed.
        """
        self.ps.test_updates['name'] = 't1.68.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.68', 't1.68.001', '8361']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.open_user_menu()
        self.admin.wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Admin')
            )
        ).click()
        self.admin.page.wait_for_page_load()
        self.admin.driver.find_element(
            By.XPATH, '//a[contains(text(),"Research Data")]').click()
        self.admin.driver.find_element(
            By.XPATH, '//input[@value="Export Data"]').click()
        self.admin.driver.find_element(
            By.XPATH, '//div[contains(@class,"alert-info")]')

        self.ps.test_updates['passed'] = True
