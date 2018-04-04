"""OpenStax Web, Epic 02 - About Us"""

import unittest

from os import getenv
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import options
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep


class TestAboutUs(unittest.TestCase):
    """02 - About Us."""

    def setUp(self):
        """Pretest settings."""
        # Remove the info bars and password save alert from Chrome
        option_set = options.Options()
        option_set.add_argument("disable-infobars")
        option_set.add_experimental_option(
            'prefs', {
                'credentials_enable_service': False,
                'profile': {
                    'password_manager_enabled': False
                }
            }
        )
        self.driver = webdriver.Chrome(chrome_options=option_set)

        # Retrieve the defined server or default to the QA instance
        self.driver.get(getenv('OSWEBSITE', 'https://oscms-qa.openstax.org'))
        self.wait = WebDriverWait(self.driver, 15)
        self.wait.until(
            expect.presence_of_element_located(
                (By.CSS_SELECTOR, '.page-loaded')
            )
        )
        link = self.driver.find_element(By.CSS_SELECTOR, '[href="/about"]')
        sleep(2)
        link.click()

    def tearDown(self):
        """Test destructor."""
        try:
            self.driver.quit()
        except:
            pass

    # Case C96855 - 001 - Non-user | OpenStax and staff bios are available
    def test_openstax_and_staff_bios_are_available_96855(self):
        """OpenStax and staff bios are available.

        Steps:
        Verify bio is visible
        Scroll to a random staff portrait
        View the staff bio by clicking on the portrait

        Expected Result:
        OpenStax bio is visible
        Staff bio is displayed
        """
        # At About Us page
        self.wait.until(
            expect.presence_of_element_located(
                (By.CSS_SELECTOR, '.page-loaded')
            )
        )
        sleep(2)
        # OpenStax bio found; select a random, visible staff portrait
        portraits = self.driver.find_elements(
            By.CSS_SELECTOR,
            '.headshot'
        )
        assert(len(portraits) > 0), 'No headshots found'
        selected = portraits[randint(0, len(portraits) - 1)]
        self.driver.execute_script(
            'return arguments[0].scrollIntoView();',
            selected
        )
        sleep(0.5)
        headshot_id = selected.get_attribute('data-id')
        name = selected.find_element(By.CSS_SELECTOR, '.name') \
            .get_attribute('innerHTML')
        print('Using ID #%s - %s' % (headshot_id, name))

        # Open the staff bio pane
        selected.click()
        bio = selected.find_element(By.CSS_SELECTOR, '.description') \
            .get_attribute('innerHTML')
        print('Bio: %s' % bio)

        # Uncomment the next assertion to view the stdout print statements
        # assert(False), 'Output test data'

    # Check if the link for "Learn more about  how state policy leaders can
    # support initiatives like OpenStax" still exists
    def test_learn_more_state_policy(self):
        sleep(2)
        self.driver.find_element(
            By.XPATH, '//a[contains(text(), "leaders")]'
        ).click()
        header = self.driver.find_element(
            By.XPATH, '//head/title'
        ).get_attribute('innerHTML')
        # print(header)
        assert('bad request' not in header and 'error' not in header), \
            "broken link"

    # Check if the link to the support page still exists
    def test_support_page(self):
        sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, '[href="/support"]').click()
        assert('support' in self.driver.current_url), "wrong link"

    # Check if the link to the FAQ page still exists
    def test_faq_page(self):
        sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, '[href="/faq"]').click()
        assert('faq' in self.driver.current_url), "wrong link"
