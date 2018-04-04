import unittest

from os import getenv
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import options
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from random import randint


class TestGive(unittest.TestCase):
    """04 - Give."""

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
        link = self.driver.find_element(
            By.CSS_SELECTOR, '[href="/give"][role="menuitem"]'
               )
        sleep(2)
        link.click()
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

    # Case C96851 - 001 - NonUser | Different donating options are visible
    """ Ensure users can view different options to donate

    Steps
    Go to oscms-qa.openstax.org
    Click on "Give" at the top of the page
    Scroll to the "Other ways to give" section

    Expected Result
    Once on the Give page user can view the different options on viewing the
    page
    """
    def test_different_donating_option_96851(self):
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//h2[contains(text(), "Other Ways")]')
            )
        )

    # Case 96853 - 001 - NonUser | Submit questions about donation
    def test_submit_questions_96853(self):
        """ Ensure users can ask questions about donation

        Steps
        From the give page 
        Scroll down to the bottom of the page and click the "contact us for help
        with your gift" link
        Redirected to the contact us form
        Fill out the form
        Click the " Send" button.

        Expected Result
        User will be taken to the confirmation page.
        """
        sleep(1)
        link = self.driver.find_element(
            By.XPATH, '//a[contains(text(), "GIFT")]'
               )
        self.driver.execute_script(
            'return arguments[0].scrollIntoView();',
            link
        )
        link.click()
        sleep(1)
        name = self.driver.find_element_by_name('name')
        name.send_keys("TestName")
        email = self.driver.find_element_by_name('email')
        email.send_keys("email@test.com")
        message = self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//textarea[@name="description"]')
            )
        )
        self.driver.execute_script(
            'return arguments[0].scrollIntoView();',
            message
        )
        message.send_keys("TestMsg")
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()
        assert('confirmation' in self.driver.current_url), \
            'redirected to wrong site'

    # Case 96854 - 001 - NonUser | Get back to the Home page from Give page
    def test_get_back_to_home_page_96854(self):
        """Ensure users can get back to the homepage from the give page

        Steps
        From the Give page click on the OpenStax Logo at the top left of the
        page

        Expected Result
        User will be redirected to the home page
        """
        self.driver.find_element(By.CSS_SELECTOR, '[href="/"]').click()
        assert(self.driver.current_url == "https://oscms-qa.openstax.org/"), \
            'redirected to wrong site'

    # Case C100143 - 001 - NonUser | Enter an alpha key to take to the first
    # state that starts with that character
    # def test_alpha_key_drop_down_100143(self):
        """ Enter an alpha key while in the drop down for states will take user
        to the first state starting with that character.

        Steps
        Click Give link/ Give banner
        Select a donation amount and click the donate button
        Type an alpha key when in the country or state drop down

        Expected Result
        User will be taken to the first state or country that starts with the
        letter they typed.
        """
    #     sleep(1)
    #     amount_buttons = self.driver.find_elements(By.CSS_SELECTOR, '.amount')
    #     button = amount_buttons[randint(0, len(amount_buttons) - 1)]
    #     button.click()
    #     self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()
    #     drop_down_menu = self.driver.find_element(
    #                         By.XPATH, '//label[contains(text(), "State")]/div'
    #                      )
    #     drop_down_menu.click()
    #     # this actually doesn't press the T key, find another way
    #     drop_down_menu.send_keys('t')
    #     selected = self.driver.find_element_by_class_name('option active')
    #     assert(selected.get_attribute('data-value' == 'TN')), \
    #         'wrong state selected'

    # Case 100146 - 001 - NonUser | Donation fields not required
    def test_donation_fields_not_required_100146(self):
        """
        Steps
        1. go to oscms-qa.openstax.org
        2. click on the give link
        3. select price you'd like to donate and click the donate button
        4. Fill out required fields (everything but "title" field)

        5. Use any one of the following cards if asked:
        Visa: 4222222222222 (4 followed by 12-2's)
        MC: 5454545454545454 (total of 16 digits)
        Discover: 60116666666666666 (total of 16 digits)
        AMEX: 343434343434343 (total of 15 digits)
        Security Code: 125
        Expiration Date: any date in the future

        Expected Result
        User should be able to submit the form by filling out the entire form
        minus title
        """
        donation_amounts = self.driver.find_element(
            By.XPATH, '//div[@class="box-row"]/div'
                          )
        sleep(1)
        amount_buttons = self.driver.find_elements(By.CSS_SELECTOR, '.amount')
        button = amount_buttons[randint(0, len(amount_buttons) - 1)]
        button.click()
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()
        input_box = self.driver.find_elements(
            By.CSS_SELECTOR, 'input[type="text"]'
                    )
        for element in input_box:
            if element.get_attribute("name") != "Title":
                element.send_keys("test")
                if element.get_attribute("name") == "Email":
                    element.send_keys("@test.com")
        state = self.driver.find_element(
                             By.XPATH, '//label[contains(text(), "State")]/div'
                          )
        state.selectByIndex(1)
        country = self.driver.find_element(
                             By.XPATH,
                             '//label[contains(text(), "Country")]/div'
                  )
        country.selectByIndex(0)
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()
        sleep(1)
        # finish by using required card infomration.
