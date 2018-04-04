import unittest

from os import getenv
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import options
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep


class TestSubjects(unittest.TestCase):
    """07 - Subjects."""

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
        sleep(1)

    def tearDown(self):
        """Test destructor."""
        try:
            self.driver.quit()
        except:
            pass

    # Case C187255 - 001 - NonUser | Navigate to All Subjects from homepage
    def test_all_subjects_banner_187255(self):
        """
        Test if user can navigate to All Subjects page from homepage banner

        Steps
        Go to the OpenStax website
        Click on Explore All Subjects on the homepage banner

        Expected Result
        You should be re-directed to the All subjects page
        """
        self.wait.until(
            expect.element_to_be_clickable(
                (
                    By.XPATH,
                    '//a[contains(text(), "All Subjects")][@tabindex=0]'
                )
            )
        ).click()
        assert('subjects' in self.driver.current_url), "wrong link"

    # Case C187256 - 001 - NonUser | Navigate to All Subjects from header
    def test_all_subjects_header_187256(self):
        """
        Test if usr can navigate to All Subjects page from homepage header

        Steps
        Go to the OpenStax website
        Click on Subjects -> All

        Expected Result
        You should be re-directed to the All subjects page
        """
        self.wait.until(
            expect.presence_of_element_located(
                (By.CSS_SELECTOR, '[href ="/subjects"]')
            )
        ).click()
        self.wait.until(
            expect.element_to_be_clickable(
                (
                    By.XPATH,
                    '//a[contains(text(), "All")]'
                )
            )
        ).click()
        assert('subjects' in self.driver.current_url), "wrong link"

    # Case C187257 - 001 - NonUser | Navigate to Math from header
    def test_math_187257(self):
        """
        Test if usr can navigate to Math page from homepage header

        Steps
        Go to the OpenStax website
        Click on Subjects -> Math

        Expected Result
        You should be re-directed to the Mathpage
        """
        self.wait.until(
            expect.presence_of_element_located(
                (By.CSS_SELECTOR, '[href ="/subjects"]')
            )
        ).click()
        self.wait.until(
            expect.element_to_be_clickable(
                (
                    By.XPATH,
                    '//a[contains(text(), "Math")]'
                )
            )
        ).click()
        assert('math' in self.driver.current_url), "wrong link"

    # Case C187258 - 001 - NonUser | Navigate to Science from header
    def test_science_187258(self):
        """
        Test if usr can navigate to Science page from homepage header

        Steps
        Go to the OpenStax website
        Click on Subjects -> Science

        Expected Result
        You should be re-directed to the Science page
        """
        self.wait.until(
            expect.presence_of_element_located(
                (By.CSS_SELECTOR, '[href ="/subjects"]')
            )
        ).click()
        self.wait.until(
            expect.presence_of_element_located(
                (By.CSS_SELECTOR, '[href ="/subjects/science"]')
            )
        ).click()
        assert('science' in self.driver.current_url), "wrong link"

    # Case C187259 - 001 - NonUser | Navigate to Social Sciences from header
    def test_social_sciences_187259(self):
        """
        Test if usr can navigate to Social Sciences page from homepage header

        Steps
        Go to the OpenStax website
        Click on Subjects -> Social Sciences

        Expected Result
        You should be re-directed to the Social Sciences page
        """
        self.wait.until(
            expect.presence_of_element_located(
                (By.CSS_SELECTOR, '[href ="/subjects"]')
            )
        ).click()
        self.wait.until(
            expect.presence_of_element_located(
                (By.CSS_SELECTOR, '[href ="/subjects/social-sciences"]')
            )
        ).click()
        assert('social-sciences' in self.driver.current_url), "wrong link"

    # Case C187260 - 001 - NonUser | Navigate to Humanities from header
    def test_humanities_187260(self):
        """
        Test if usr can navigate to Social Sciences page from homepage header

        Steps
        Go to the OpenStax website
        Click on Subjects -> Humanities

        Expected Result
        You should be re-directed to the Humanities page
        """
        self.wait.until(
            expect.presence_of_element_located(
                (By.CSS_SELECTOR, '[href ="/subjects"]')
            )
        ).click()
        self.wait.until(
            expect.presence_of_element_located(
                (By.CSS_SELECTOR, '[href ="/subjects/humanities"]')
            )
        ).click()
        assert('humanities' in self.driver.current_url), "wrong link"

    # Case C187261 - 001 - NonUser | Navigate to AP from header
    def test_AP_187261(self):
        """
        Test if usr can navigate to Social Sciences page from homepage header

        Steps
        Go to the OpenStax website
        Click on Subjects -> AP

        Expected Result
        You should be re-directed to the AP page
        """
        self.wait.until(
            expect.presence_of_element_located(
                (By.CSS_SELECTOR, '[href ="/subjects"]')
            )
        ).click()
        self.wait.until(
            expect.presence_of_element_located(
                (By.CSS_SELECTOR, '[href ="/subjects/AP"]')
            )
        ).click()
        assert('AP' in self.driver.current_url), "wrong link"
 