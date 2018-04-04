import unittest

from os import getenv
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import options
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep


class TestHomePage(unittest.TestCase):
    """01 - Home Page."""

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

    def tearDown(self):
        """Test destructor."""
        try:
            self.driver.quit()
        except:
            pass

    # Case C96693 - 001 - NonUser | Banners are visible and switching
    def test_banner_visible_switch_96693(self):
        """Ensure that banners are visible.

        Steps:
        Navigate to oscms-qa.openstax.org

        Expected Result
        Banners should be visible and should switch every few seconds
        """
        banners = self.driver.find_elements(
            By.XPATH, '//div[@role="banner"]/div'
        )
        # print(len(banners))
        assert(len(banners) > 0), "no banner found"
        current_banner = self.driver.find_elements(
            By.XPATH, '//div[contains(@class, "fadein")]'
        )
        sleep(17)
        next_banner = self.driver.find_elements(
            By.XPATH, '//div[contains(@class, "fadein")]'
        )
        assert(current_banner != next_banner), "banners don't switch"

    # Case C96694 - 001 - NonUser | The Give Now sticky is visible
    # def test_give_now_visibility_96694(self):
    #     """Ensure the Give Now sticky is visible the first 5 times the site
    #     is visited.

    #     Steps
    #     Navigate to oscms-qa.openstax.org

    #     Expected Result
    #     The orange Give Now sticky is visible the first 5 times the site
    #     is visited
    #     """
    #     sleep(1)
    #     times = 4
    #     while times > 0:
    #         try:
    #             self.wait.until(
    #                 expect.visibility_of_element_located(
    #                     (By.LINK_TEXT, "GIVE OTHER AMOUNT")
    #                 )
    #             )
    #         except:
    #             self.wait.until(
    #                 expect.visibility_of_element_located(
    #                     (By.LINK_TEXT, "GIVE NOW")
    #                 )
    #             )
    #         self.driver.refresh()
    #         times -= 1

    # Case C96695 - 001 - NonUser | The Give Now sitcky is not visible for
    # frequent visitors
    # def test_give_now_disappear_96695(self):
        """Ensure the Give Now sticky is not visible for frequent visitors.

        Steps
        Navigate to oscms-qa.openstax.org

        Expected Result
        The orange Give Now sticky is not visible after visiting the site
        5 times or visiting the Give page at least once
        """

    # Case C96699 - 001 - NonUser | Quote by professor is visble
    def test_quote_by_professor_96699(self):
        """Ensure quotes by a professor shown on homepage.

        Steps
        Navigate to oscms-qa.openstax.org

        Expected Result
        Homepage displays a quote from one of our textbook heroes
        """
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//blockquote//p[starts-with(.,"\"")]')
            )
        )

    # Case C96700 - 001 - NonUser | Renewal form is visible
    def test_renewal_form_96700(self):
        """Ensure the renewal form shown on homepage.

        Steps
        Navigate to oscms-qa.openstax.org

        Expected Result
        Faculty should be able to access the renewal form from the homepage.
        Clicking on Let Us Know takes them to the renewal form
        """
        sleep(1)
        self.driver.find_element(By.LINK_TEXT, "LET US KNOW").click()
        assert(
            "adoption" in self.driver.current_url
        ), "link doesn't take to renewal form"
        header = self.driver.find_element(
            By.XPATH, '//head/title'
        ).get_attribute('innerHTML')
        assert('bad request' not in header and 'error' not in header), \
            "broken link"

    # Case C96702 - 001 - NonUser | In reduced screen size, hamburger menu
    # appears
    def test_hamburger_menu_96702(self):
        """Ensure in reduced size, hamburger menu appears

        Steps
        Navigate to oscms-qa.openstax.org
        Reduce size of window

        Expected Result
        The header should collapse into a hamburger menu
        """
        self.driver.set_window_size(480, 320)
        self.wait.until(
            expect.visibility_of_element_located(
                (By.CLASS_NAME, "expand")
            )
        )

    # The subscribe button is visible
    def test_subscribe_button(self):
        sleep(1)
        self.driver.find_element(By.LINK_TEXT, "SUBSCRIBE").click()
        header = self.driver.find_element(
            By.XPATH, '//head/title'
        ).get_attribute('innerHTML')
        assert('bad request' not in header and 'error' not in header), \
            "broken link"

    # The see our impact button is visible
    def test_see_our_impact_button(self):
        sleep(1)
        self.driver.find_element(By.LINK_TEXT, "SEE OUR IMPACT").click()
        assert(
            "impact" in self.driver.current_url
        ), "link doesn't take to impact page"
        header = self.driver.find_element(
            By.XPATH, '//head/title'
        ).get_attribute('innerHTML')
        assert('bad request' not in header and 'error' not in header), \
            "broken link"

    # The view partners button is visible
    def test_subscribe_button(self):
        sleep(1)
        self.driver.find_element(By.LINK_TEXT, "VIEW PARTNERS").click()
        assert(
            "partners" in self.driver.current_url
        ), "link doesn't take to partners page"
        header = self.driver.find_element(
            By.XPATH, '//head/title'
        ).get_attribute('innerHTML')
        assert('bad request' not in header and 'error' not in header), \
            "broken link"
