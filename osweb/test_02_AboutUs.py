"""OpenStax Web, Epic 01 - About Us"""

import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.ui import WebDriverWait


class TestAboutUs(unittest.TestCase):
    """01 - About Us."""

    def setUp(self):
        """Pretest settings."""

    def tearDown(self):
        """Test destructor."""

    # Case C96855 - 001 - Non-user | OpenStax bio is visible
    def test__96855(self):
        """OpenStax bio is visible.

        Steps:

        Expected Result:

        """

        assert(False), 'Test not written'


"""
    Test C96855: Click on "About us" at the top of the page.
    The user will be presented with a description on OpenStax
    as well as a brief bio on each staff member and Strategic
    advisor.
"""
url = 'https://oscms-qa.openstax.org/'

driver = webdriver.Chrome()
driver.maximize_window()  # required to display the header links
driver.execute_script('window.focus()')
driver.get(url)

wait = WebDriverWait(driver, 10)

# look for the link
xpath_about = '//a[@href="/about"]'

link = wait.until(
    expect.element_to_be_clickable(
        (By.XPATH, xpath_about)
    )
)

# simulate a click to get around the overlay issue hiding
# the click in the header
link.send_keys('\n')

# check if page content loads
try:
    wait.until(
        expect.presence_of_element_located(
            (By.CSS_SELexpectTOR, '.about-page')
        )
    )
    print('PASS: About page content loaded')
except:
    print('FAIL: page content not loaded')
finally:
    driver.quit()
