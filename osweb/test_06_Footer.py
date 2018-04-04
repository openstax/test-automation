import unittest

from os import getenv
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import options
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from time import sleep
from random import randint


class TestFooter(unittest.TestCase):
    """06 - Footer."""

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
        footer = self.wait.until(
            expect.visibility_of_element_located(
                (By.CLASS_NAME, 'page-footer')
            )
        )
        self.driver.execute_script(
            'return arguments[0].scrollIntoView();', footer)
        sleep(1)

    def tearDown(self):
        """Test destructor."""
        try:
            self.driver.quit()
        except:
            pass

    # Case C96703 - 001 - NonUser | Footer contain all neccessary elements
    def test_contain_all_elements_96703(self):
        """
        Make sure footer contains all the neccessary elements.

        Steps
        Navigate to oscms-qa.openstax.org

        Expected Result
        The footer must contain LICENSING, TERMS OF USE, ACCESSIBILITY
        STATEMENT, OPEN SOURCE CODE, CONTACT US, Press Kit, Newsletter, our
        sponsors, copyright notice, Advanced Placement trademark, social icons
        """
        self.wait.until(
            expect.presence_of_element_located(
                (By.CSS_SELECTOR, '[href ="/license"]')
            )
        )
        self.wait.until(
            expect.presence_of_element_located(
                (By.CSS_SELECTOR, '[href ="/tos"]')
            )
        )
        self.wait.until(
            expect.presence_of_element_located(
                (By.CSS_SELECTOR, '[href ="/privacy-policy"]')
            )
        )
        self.wait.until(
            expect.presence_of_element_located(
                (By.CSS_SELECTOR, '[href ="/accessibility-statement"]')
            )
        )
        self.wait.until(
            expect.presence_of_element_located(
                (By.CSS_SELECTOR, '[href ="https://github.com/openstax"]')
            )
        )
        self.wait.until(
            expect.presence_of_element_located(
                (By.CSS_SELECTOR, '[href ="/contact"]')
            )
        )
        self.wait.until(
            expect.presence_of_element_located(
                (By.XPATH, '//a[contains(text(), "Press Kit")]')
            )
        )
        self.wait.until(
            expect.presence_of_element_located(
                (By.XPATH, '//a[contains(text(), "Newsletter")]')
            )
        )
        # our sponsors???
        # how to test the copyright and trademarks???

        self.wait.until(
            expect.presence_of_element_located(
                (By.CSS_SELECTOR, '.social')
            )
        )

    # Case C187249 - 001 - NonUser | View OpenStax licensing
    def test_view_licensing_187249(self):
        """
        Test if users can view the OpenStax licensing at footer

        Steps
        Go to the OpenStax website
        Scroll to the bottom of the page
        Click "License" link

        Expected Result
        User will be taken to the License page
        """
        self.wait.until(
            expect.presence_of_element_located(
                (By.CSS_SELECTOR, '[href ="/license"]')
            )
        ).click()
        assert('license' in self.driver.current_url), "wrong link"

    # Case C187250 - 001 - NonUser | View OpenStax terms of use
    def test_view_tos_187250(self):
        """
        Test if users can view the OpenStax terms of use at footer

        Steps
        Go to the OpenStax website
        Scroll to the bottom of the page
        Click "Terms of Use" link

        Expected Result
        User will be taken to the tos page
        """
        self.wait.until(
            expect.presence_of_element_located(
                (By.CSS_SELECTOR, '[href ="/tos"]')
            )
        ).click()
        assert('tos' in self.driver.current_url), "wrong link"

    # Case C187251 - 001 - NonUser | View OpenStax accessibility statement
    def test_view_accessibility_statement_187251(self):
        """
        Test if users can view the OpenStax accessibility statement at footer

        Steps
        Go to the OpenStax website
        Scroll to the bottom of the page
        Click "Accessibility Statement" link

        Expected Result
        User will be taken to the accessibility statement page
        """
        self.wait.until(
            expect.presence_of_element_located(
                (By.CSS_SELECTOR, '[href ="/accessibility-statement"]')
            )
        ).click()
        assert('accessibility-statement' in self.driver.current_url), \
            "wrong link"

    # Case C187252 - 001 - NonUser | View OpenStax open source code
    def test_view_code_187252(self):
        """
        Test if users can view the OpenStax open source code at footer

        Steps
        Go to the OpenStax website
        Scroll to the bottom of the page
        Click "Open Source Code" link

        Expected Result
        User will be taken to the tos page
        """
        self.wait.until(
            expect.presence_of_element_located(
                (By.CSS_SELECTOR, '[href ="https://github.com/openstax"]')
            )
        ).click()
        self.driver.switch_to_window(self.driver.window_handles[-1])
        sleep(1)

        assert('github' in self.driver.current_url), "wrong link"

    # Case C187253 - 001 - NonUser | View OpenStax Press Kit
    def test_view_press_kit_187253(self):
        """
        Test if users can view the OpenStax press kit at footer

        Steps
        Go to the OpenStax website
        Scroll to the bottom of the page
        Click "Press Kit" link

        Expected Result
        Press Kit will be downloaded
        """
        self.wait.until(
            expect.presence_of_element_located(
                (By.XPATH, '//a[contains(text(), "Press Kit")]')
            )
        ).click()
        header = self.driver.find_element(
            By.XPATH, '//head/title'
        ).get_attribute('innerHTML')
        assert('bad request' not in header and 'error' not in header), \
            "broken link"

        # Case C187254 - 001 - NonUser | Sign up the for newsletters
    def test_newsletter_187254(self):
        """
        Test if users can sign up for the newsletter

        Steps
        Go to the OpenStax website
        Scroll to the bottom of the page
        Click on Newsletter

        Expected Result
        The newsletter signup form will open in a new tab.
        """
        self.wait.until(
            expect.presence_of_element_located(
                (By.XPATH, '//a[contains(text(), "Newsletter")]')
            )
        ).click()
        self.driver.switch_to_window(self.driver.window_handles[-1])
        sleep(1)

        self.wait.until(
            expect.presence_of_element_located(
                (By.CSS_SELECTOR, '.form')
            )
        )
