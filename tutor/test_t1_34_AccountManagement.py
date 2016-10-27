"""Product, Epic 34 - AccountManagement"""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Student

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
        8207, 8208, 8209, 8210, 8211,
        8212, 8213, 8214, 8215, 8216,
        8217, 8218, 8219, 8220, 8221,
        8222, 8223, 8224, 8225, 8226,
        8227, 8387, 8388
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestAccountManagement(unittest.TestCase):
    """T1.34 - Account mangement."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.student = Student(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        self.google_account = os.getenv('GOOGLE_USER')
        self.google_password = os.getenv('GOOGLE_PASSWORD')
        self.facebook_account = os.getenv('FACEBOOK_USER')
        self.facebook_password = os.getenv('FACEBOOK_PASSWORD')
        self.twitter_account = os.getenv('TWITTER_USER')
        self.twitter_password = os.getenv('TWITTER_PASSWORD')
        self.student.get("http://accounts-qa.openstax.org")

    def tearDown(self):
        """Test destructor."""
        self.ps.update_job(
            job_id=str(self.student.driver.session_id),
            **self.ps.test_updates
        )
        try:
            self.student.delete()
        except:
            pass

    # Case C8207 - 001 - User | Create a new Account with username and password
    @pytest.mark.skipif(str(8207) not in TESTS, reason='Excluded')
    def test_user_create_a_new_account_with_a_username_and_password_8207(self):
        """Create a new Account with a username and password.

        Steps:
        Click on the Sign up link
        Click on the Sign up with password button
        Enter first name into the 'First Name' text box
        Enter last name into the 'Last Name' text box
        Enter email into the 'Email Address' text box
        Enter username into the 'Username' text box
        Enter password into the 'Password' text box
        Renter password into the 'Confirm Password' text box
        Click the "Create Account Button"
        Click the checkbox, and click 'I Agree' for the Terms of Use
        Click the checkbox, and click 'I Agree' for the Privacy Policy

        Expected Result:
        User logged in and presented with their dashboard
        """
        self.ps.test_updates['name'] = 't1.34.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.34', 't1.34.001', '8207']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        num = str(randint(0, 999))
        self.student.find(By.LINK_TEXT, 'Sign up').click()
        self.student.find(
            By.ID, 'identity-login-button').click()
        self.student.find(
            By.ID, 'signup_first_name').send_keys('first_name_001')
        self.student.find(
            By.ID, 'signup_last_name').send_keys('last_name_001')
        self.student.find(
            By.ID, 'signup_email_address').send_keys('email_001@test.com')
        self.student.find(
            By.ID, 'signup_username').send_keys('automated_34_'+num)
        self.student.find(
            By.ID, 'signup_password').send_keys(self.student.password)
        self.student.find(
            By.ID, 'signup_password_confirmation'
        ).send_keys(self.student.password)
        self.student.find(By.ID, 'signup_i_agree').click()
        self.student.find(
            By.ID, 'create_account_submit').click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[@id="session-info"]//a[text()="automated_34_'+num+'"]')
            )
        )

        self.ps.test_updates['passed'] = True

    # Case C8208 - 002 - User | Create a new Account with Facebook
    @pytest.mark.skipif(str(8208) not in TESTS, reason='Excluded')
    def test_user_create_a_new_account_with_facebook_8208(self):
        """Create a new Account with Facebook.

        Steps:
        Click on the Sign up link
        Click on the Sign up with Facebook button
        [redirects to facebbok.com]
        If you are not logged into Facebook:
        * enter email and password for facebook, then click the "Log In" button
        Click on the "okay" button
        [redirects back to Accounts]
        Click the checkbox to agree to the Terms of Use and Privacy Policy
        Click the "Create Account Button"

        Expected Result:
        User logged in and presented with their dashboard
        """
        self.ps.test_updates['name'] = 't1.34.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.34', 't1.34.002', '8208']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.find(By.LINK_TEXT, 'Sign up').click()
        self.student.find(
            By.ID, 'facebook-login-button').click()
        self.student.page.wait_for_page_load()
        self.student.find(
            By.ID, 'email').send_keys(self.facebook_account)
        self.student.find(
            By.ID, 'pass').send_keys(self.facebook_password+Keys.RETURN)
        self.student.page.wait_for_page_load()
        username = self.student.find(
            By.ID, 'signup_username').get_attribute('value')
        self.student.find(By.ID, 'signup_i_agree').click()
        self.student.find(
            By.ID, 'create_account_submit').click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[@id="session-info"]//a[text()="'+username+'"]')
            )
        )
        # add password sign in, (and delete facebook so account can be reused)
        self.student.find(
            By.ID, 'enable-other-sign-in').click()
        self.student.sleep(2)
        self.student.find(
            By.XPATH, '//div[@data-provider="identity"]//' +
            'span[contains(@class,"add mod")]').click()
        self.student.sleep(1)
        self.student.find(
            By.XPATH, '//input[@name="password"]'
        ).send_keys(self.student.password)
        self.student.find(
            By.XPATH, '//input[@name="password_confirmation"]'
        ).send_keys(self.student.password)
        self.student.find(
            By.XPATH, '//button[@type="submit"]//i[contains(@class,"ok")]'
        ).click()
        self.student.sleep(1)
        # delete login option
        self.student.find(
            By.XPATH,
            '//div[contains(@class,"enabled-providers")]' +
            '//div[@data-provider="facebook"]//span[contains(@class,"trash")]'
        ).click()
        self.student.find(
            By.XPATH, '//div[@class="popover-content"]//button[text()="OK"]'
        ).click()

        self.ps.test_updates['passed'] = True

    # Case C8209 - 003 - User | Create a new Account with Google
    @pytest.mark.skipif(str(8209) not in TESTS, reason='Excluded')
    def test_user_create_a_new_account_with_google_8209(self):
        """Create a new Account with Google.

        Steps:
        Click on the Sign up link
        Click on the Sign up with Google button
        [redirects to accounts.google.com]
        If you are not logged in:
        * Click the 'Add Account' button
        * Enter email into text box
        * Click on the 'Next' button
        * Enter password into text box
        * Click on the 'Sign in' button
        Click on the "Allow" button
        [redirects back to Accounts]
        Click the checkbox to agree to the Terms of Use and Privacy Policy
        Click the "Create Account Button"

        Expected Result:
        User logged in and presented with their dashboard
        """
        self.ps.test_updates['name'] = 't1.34.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.34', 't1.34.003', '8208']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.find(By.LINK_TEXT, 'Sign up').click()
        self.student.find(By.ID, 'google-login-button').click()
        self.student.page.wait_for_page_load()
        self.student.find(
            By.ID, 'Email').send_keys(self.google_account)
        self.student.find(By.ID, 'next').click()
        self.student.find(
            By.ID, 'Passwd').send_keys(self.google_password)
        self.student.find(By.ID, 'signIn').click()
        self.student.page.wait_for_page_load()
        username = self.student.find(
            By.ID, 'signup_username').get_attribute('value')
        self.student.find(By.ID, 'signup_i_agree').click()
        self.student.find(
            By.ID, 'create_account_submit').click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[@id="session-info"]//a[text()="'+username+'"]')
            )
        )
        # add password sign in, (and delete google so account can be reused)
        self.student.find(
            By.ID, 'enable-other-sign-in').click()
        self.student.sleep(2)
        self.student.find(
            By.XPATH, '//div[@data-provider="identity"]//' +
            'span[contains(@class,"add mod")]').click()
        self.student.sleep(1)
        self.student.find(
            By.XPATH, '//input[@name="password"]'
        ).send_keys(self.student.password)
        self.student.find(
            By.XPATH, '//input[@name="password_confirmation"]'
        ).send_keys(self.student.password)
        self.student.find(
            By.XPATH, '//button[@type="submit"]//i[contains(@class,"ok")]'
        ).click()
        self.student.sleep(1)
        # delete login option
        self.student.find(
            By.XPATH,
            '//div[contains(@class,"enabled-providers")]' +
            '//div[@data-provider="google_oauth2"]//' +
            'span[contains(@class,"trash")]'
        ).click()
        self.student.find(
            By.XPATH, '//div[@class="popover-content"]//button[text()="OK"]'
        ).click()

        self.ps.test_updates['passed'] = True

    # Case C8210 - 004 - User | Create a new Account with Twitter
    @pytest.mark.skipif(str(8210) not in TESTS, reason='Excluded')
    def test_user_create_a_new_account_with_twitter_8210(self):
        """Create a new Account with Twitter.

        Steps:
        Click on the Sign up link
        Click on the Sign up with Twitter button
        Enter email and password on twitter
        Click login
        Enter email and last name on signup page on openstax
        Accept terms
        Click button to create account

        Expected Result:
        User logged in and presented with their dashboard
        """
        self.ps.test_updates['name'] = 't1.34.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.34', 't1.34.003', '8208']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.find(By.LINK_TEXT, 'Sign up').click()
        self.student.find(By.ID, 'twitter-login-button').click()
        self.student.page.wait_for_page_load()
        self.student.find(
            By.ID, 'username_or_email').send_keys(self.twitter_account)
        self.student.find(
            By.ID, 'password').send_keys(self.twitter_password)
        self.student.find(By.ID, 'allow').click()
        self.student.page.wait_for_page_load()
        self.student.find(
            By.ID, 'signup_last_name').send_keys('last_name_004')
        self.student.find(
            By.ID, 'signup_email_address').send_keys('email_004@test.com')
        username = self.student.find(
            By.ID, 'signup_username').get_attribute('value')
        self.student.find(By.ID, 'signup_i_agree').click()
        self.student.find(
            By.ID, 'create_account_submit').click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[@id="session-info"]//a[text()="'+username+'"]')
            )
        )
        # add password sign in, (and delete twitter so account can be reused)
        self.student.find(
            By.ID, 'enable-other-sign-in').click()
        self.student.sleep(2)
        self.student.find(
            By.XPATH, '//div[@data-provider="identity"]//' +
            'span[contains(@class,"add mod")]').click()
        self.student.sleep(1)
        self.student.find(
            By.XPATH, '//input[@name="password"]'
        ).send_keys(self.student.password)
        self.student.find(
            By.XPATH, '//input[@name="password_confirmation"]'
        ).send_keys(self.student.password)
        self.student.find(
            By.XPATH, '//button[@type="submit"]//i[contains(@class,"ok")]'
        ).click()
        self.student.sleep(1)
        # delete login option
        self.student.find(
            By.XPATH,
            '//div[contains(@class,"enabled-providers")]' +
            '//div[@data-provider="twitter"]//span[contains(@class,"trash")]'
        ).click()
        self.student.find(
            By.XPATH, '//div[@class="popover-content"]//button[text()="OK"]'
        ).click()

        self.ps.test_updates['passed'] = True

    # Case C8211 - 005 - User | Accept the terms of service
    @pytest.mark.skipif(str(8211) not in TESTS, reason='Excluded')
    def test_user_accept_the_terms_of_service_8211(self):
        """Accept the terms of service.

        Steps:
        Sign up with password

        Expected Result:
        Terms of use are accepted
        User is presented with the privacy policy
        """
        self.ps.test_updates['name'] = 't1.34.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.34', 't1.34.005', '8211']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        num = str(randint(1000, 1999))
        self.student.find(By.LINK_TEXT, 'Sign up').click()
        self.student.find(
            By.ID, 'identity-login-button').click()
        self.student.find(
            By.ID, 'signup_first_name').send_keys('first_name_005')
        self.student.find(
            By.ID, 'signup_last_name').send_keys('last_name_005')
        self.student.find(
            By.ID, 'signup_email_address').send_keys('email_005@test.com')
        self.student.find(
            By.ID, 'signup_username').send_keys('automated_34_'+num)
        self.student.find(
            By.ID, 'signup_password').send_keys(self.student.password)
        self.student.find(
            By.ID, 'signup_password_confirmation'
        ).send_keys(self.student.password)
        self.student.find(By.ID, 'signup_i_agree').click()
        self.student.find(
            By.ID, 'create_account_submit').click()

        self.ps.test_updates['passed'] = True

    # Case C8212 - 006 - User | Accept the privacy policy
    @pytest.mark.skipif(str(8212) not in TESTS, reason='Excluded')
    def test_user_accept_the_privacy_policy_8212(self):
        """Accept the privacy policy.

        Steps:
        Sign up with password

        Expected Result:
        User logged in and presented with their dashboard
        """
        self.ps.test_updates['name'] = 't1.34.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.34', 't1.34.006', '8212']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        num = str(randint(2000, 2999))
        self.student.find(By.LINK_TEXT, 'Sign up').click()
        self.student.find(
            By.ID, 'identity-login-button').click()
        self.student.find(
            By.ID, 'signup_first_name').send_keys('first_name_006')
        self.student.find(
            By.ID, 'signup_last_name').send_keys('last_name_006')
        self.student.find(
            By.ID, 'signup_email_address').send_keys('email_006@test.com')
        self.student.find(
            By.ID, 'signup_username').send_keys('automated_34_'+num)
        self.student.find(
            By.ID, 'signup_password').send_keys(self.student.password)
        self.student.find(
            By.ID, 'signup_password_confirmation'
        ).send_keys(self.student.password)
        self.student.find(By.ID, 'signup_i_agree').click()
        self.student.find(
            By.ID, 'create_account_submit').click()

        self.ps.test_updates['passed'] = True

    # Case C8213 - 007 - User | Log into Accounts
    @pytest.mark.skipif(str(8213) not in TESTS, reason='Excluded')
    def test_user_log_into_accounts_8213(self):
        """Log into Accounts.

        Steps:
        Enter the  user account in the username and password text boxes
        Click on the Sign in button

        Expected Result:
        User logged in and presented with their dashboard
        """
        self.ps.test_updates['name'] = 't1.34.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.34', 't1.34.007', '8213']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.find(
            By.ID, 'auth_key').send_keys(self.student.username)
        self.student.find(
            By.ID, 'password').send_keys(self.student.password)
        # click on the sign in button
        self.student.find(
            By.XPATH, '//button[text()="Sign in"]'
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[@id="session-info"]//a[text()="' +
                 self.student.username + '"]')
            )
        )

        self.ps.test_updates['passed'] = True

    # Case C8214 - 008 - User | Edit account name
    @pytest.mark.skipif(str(8214) not in TESTS, reason='Excluded')
    def test_user_edit_account_name_8214(self):
        """Edit account name.

        Steps:
        Enter the teacher user account in the username and password text boxes
        Click on the Sign in button
        Click on the user's name
        Enter new information into Title, First name, Last Name, and
        Suffix text boxes
        Click on the checkmark button

        Expected Result:
        User's name has been updated
        """
        self.ps.test_updates['name'] = 't1.34.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.34', 't1.34.008', '8214']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.login(url='http://accounts-qa.openstax.org')
        name_original = self.student.wait.until(
            expect.visibility_of_element_located((By.ID, 'name'))
        )
        first = name_original.text.split(' ')[0]
        last = name_original.text.split(' ')[1]
        name_original.click()
        self.student.find(
            By.XPATH, '//input[@name="first_name"]').send_keys('_NEW')
        self.student.find(
            By.XPATH, '//input[@name="last_name"]').send_keys('_NEW')
        self.student.find(
            By.XPATH, '//button[@type="submit"]//i[contains(@class,"ok")]'
        ).click()
        name = self.student.wait.until(
            expect.visibility_of_element_located((By.ID, 'name'))
        )
        assert(name.text.split(' ')[0] == first + ('_NEW')), \
            'first name not changed'
        assert(name.text.split(' ')[1] == last + ('_NEW')), \
            'last name not changed'
        # change back
        name.click()
        for _ in range(len('_NEW')):
            self.student.find(
                By.XPATH, '//input[@name="first_name"]'
            ).send_keys(Keys.BACKSPACE)
            self.student.find(
                By.XPATH, '//input[@name="last_name"]'
            ).send_keys(Keys.BACKSPACE)
        self.student.find(
            By.XPATH, '//button[@type="submit"]//i[contains(@class,"ok")]'
        ).click()

        self.ps.test_updates['passed'] = True

    # Case C8215 - 009 - User | Cancel editing the account name
    @pytest.mark.skipif(str(8215) not in TESTS, reason='Excluded')
    def test_user_canel_editing_the_account_name_8215(self):
        """Cancel editing the account name.

        Steps:
        Enter the teacher user account in the username and password text boxes
        Click on the Sign in button
        Click on the user's name
        Enter new information into Title, First name, Last Name, and
        Suffix text boxes
        Click on the X button

        Expected Result:
        User's name has not changed
        """
        self.ps.test_updates['name'] = 't1.34.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.34', 't1.34.009', '8215']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.login(url='http://accounts-qa.openstax.org')
        name_original = self.student.wait.until(
            expect.visibility_of_element_located((By.ID, 'name'))
        )
        first = name_original.text.split(' ')[0]
        last = name_original.text.split(' ')[1]
        name_original.click()
        self.student.find(
            By.XPATH, '//input[@name="first_name"]').send_keys('_NEW')
        self.student.find(
            By.XPATH, '//input[@name="last_name"]').send_keys('_NEW')
        self.student.find(
            By.XPATH,
            '//button[@type="button"]//i[contains(@class,"remove")]'
        ).click()
        name = self.student.wait.until(
            expect.visibility_of_element_located((By.ID, 'name'))
        )
        assert(name.text.split(' ')[0] == first), 'first changed'
        assert(name.text.split(' ')[1] == last), 'last changed'

        self.ps.test_updates['passed'] = True

    # Case C8216 - 010 - User | Edit the username
    @pytest.mark.skipif(str(8216) not in TESTS, reason='Excluded')
    def test_user_edit_the_username_8216(self):
        """Edit the username.

        Steps:
        Enter the teacher user account in the username and password text boxes
        Click on the Sign in button
        Click on the username
        Enter a new username into the username text box
        Click on the checkmark button

        Expected Result:
        Username has been updated
        """
        self.ps.test_updates['name'] = 't1.34.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.34', 't1.34.010', '8216']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.login(url='http://accounts-qa.openstax.org')
        original = self.student.wait.until(
            expect.visibility_of_element_located((By.ID, 'username'))
        )
        username_original = original.text
        original.click()
        self.student.find(
            By.XPATH, '//input[@type="text"]').send_keys('_NEW')
        self.student.find(
            By.XPATH,
            '//button[@type="submit"]//i[contains(@class,"ok")]'
        ).click()
        username_edit = self.student.wait.until(
            expect.visibility_of_element_located((By.ID, 'username'))
        )
        assert(username_edit.text == username_original+('_NEW')), \
            'username not changed'
        # change back
        username_edit.click()
        for _ in range(len('_NEW')):
            self.student.find(
                By.XPATH, '//input[@type="text"]').send_keys(Keys.BACKSPACE)
        self.student.find(
            By.XPATH,
            '//button[@type="submit"]//i[contains(@class,"ok")]'
        ).click()

        self.ps.test_updates['passed'] = True

    # Case C8217 - 011 - User | Cancel editing the username
    @pytest.mark.skipif(str(8217) not in TESTS, reason='Excluded')
    def test_user_canel_editing_the_username_8217(self):
        """Cancel editing the username.

        Steps:
        Enter the teacher user account in the username and password text boxes
        Click on the Sign in button
        Click on the user's name
        Enter a new username into the username text box
        Click on the X button

        Expected Result:
        Username has not changed
        """
        self.ps.test_updates['name'] = 't1.34.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.34', 't1.34.011', '8217']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.login(url='http://accounts-qa.openstax.org')
        original = self.student.wait.until(
            expect.visibility_of_element_located((By.ID, 'username'))
        )
        username_original = original.text
        original.click()
        self.student.find(
            By.XPATH, '//input[@type="text"]').send_keys('_NEW')
        self.student.find(
            By.XPATH,
            '//button[@type="button"]//i[contains(@class,"remove")]'
        ).click()
        username_edit = self.student.wait.until(
            expect.visibility_of_element_located((By.ID, 'username'))
        )
        assert(username_edit.text == username_original), 'username not changed'

        self.ps.test_updates['passed'] = True

    # Case C8218 - 012 - User | Add an email address
    @pytest.mark.skipif(str(8218) not in TESTS, reason='Excluded')
    def test_user_add_an_email_address_8218(self):
        """Add an email address.

        Steps:
        Enter the teacher user account in the username and password text boxes
        Click on the Sign in button
        Click Add an email
        Enter email adress into the textbox
        Click on the checkmark button

        Expected Result:
        Email adress has been added to the end of the list of email adresses
        """
        self.ps.test_updates['name'] = 't1.34.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.34', 't1.34.012', '8218']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.login(url='http://accounts-qa.openstax.org')
        self.student.wait.until(
            expect.visibility_of_element_located((By.ID, 'add-an-email'))
        ).click()
        self.student.find(
            By.XPATH, '//input[@type="text"]').send_keys('email_2@test.com')
        self.student.find(
            By.XPATH, '//button[@type="submit"]//i[contains(@class,"ok")]'
        ).click()
        email = self.student.find(
            By.XPATH, '//span[contains(text(),"email_2@test.com")]')
        # delete the new email
        email.click()
        self.student.find(
            By.XPATH, '//div[@class="email-entry"]' +
            '//span[contains(@class,"trash")]').click()
        self.student.find(
            By.XPATH, '//div[@class="popover-content"]' +
            '//button[contains(text(),"OK")]').click()

        self.ps.test_updates['passed'] = True

    # Case C8219 - 013 - User | Verify an email address
    @pytest.mark.skipif(str(8219) not in TESTS, reason='Excluded')
    def test_user_verify_an_email_address_8219(self):
        """Verify an email address.

        Steps:
        Enter the teacher user account in the username and password text boxes
        Click on the Sign in button
        Click on Click to verify next to an email address
        Log into chosen email address and verify

        Expected Result:
        Confirmation message displayed saying an email has been sent.
        Email has been sent
        Email adress is verified
        """
        self.ps.test_updates['name'] = 't1.34.013' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.34', 't1.34.013', '8219']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.login(url='http://accounts-qa.openstax.org')
        self.student.wait.until(
            expect.visibility_of_element_located((By.ID, 'add-an-email'))
        ).click()
        self.student.find(
            By.XPATH, '//input[@type="text"]').send_keys(self.google_account)
        self.student.find(
            By.XPATH, '//button[@type="submit"]//i[contains(@class,"ok")]'
        ).click()
        verify = self.student.find(
            By.XPATH,
            '//div[not(@id="email-template")]' +
            '//input[@value="Click to verify"]'
        )
        actions = ActionChains(self.student.driver)
        actions.move_to_element(verify).click().perform()
        self.student.get('https://www.google.com/gmail/')
        self.student.find(
            By.ID, 'Email').send_keys(self.google_account)
        self.student.find(By.ID, 'next').click()
        self.student.find(
            By.ID, 'Passwd').send_keys(self.google_password)
        self.student.find(By.ID, 'signIn').click()
        self.student.page.wait_for_page_load()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//b[text()="[OpenStax] Verify your email address"]')
            )
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//a[contains(@href,' +
                 '"https://accounts-qa.openstax.org/confirm?code=")]')
            )
        ).click()
        verification_window = self.student.driver.window_handles[1]
        self.student.driver.switch_to_window(verification_window)
        self.student.find(
            By.XPATH,
            "//div[contains(text()," +
            "'Thank you for verifying your email address')]"
        )
        self.student.get('http://accounts-qa.openstax.org')
        self.student.find(
            By.XPATH, '//span[contains(text(),"' + self.google_account + '")]'
        ).click()
        self.student.find(
            By.XPATH, '//div[@class="email-entry"]' +
            '//span[contains(@class,"trash")]').click()
        self.student.find(
            By.XPATH, '//div[@class="popover-content"]' +
            '//button[contains(text(),"OK")]').click()

        self.ps.test_updates['passed'] = True

    # Case C8220 - 014 - User | Make an email address serachable
    @pytest.mark.skipif(str(8220) not in TESTS, reason='Excluded')
    def test_user_make_an_email_adress_searchable_8220(self):
        """Make an email address searchable.

        Steps:
        Enter the teacher user account in the username and password text boxes
        Click on the Sign in button
        Click on an email adress
        Check the Searchable checkbox next to the email adress

        Expected Result:
        Email adress is searchable, checkbox remains checked
        """
        self.ps.test_updates['name'] = 't1.34.014' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.34', 't1.34.014', '8220']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.login(url='http://accounts-qa.openstax.org')
        self.student.wait.until(
            expect.visibility_of_element_located((By.ID, 'add-an-email'))
        ).click()
        self.student.find(
            By.XPATH, '//input[@type="text"]').send_keys('email_2@test.com')
        self.student.find(
            By.XPATH, '//button[@type="submit"]//i[contains(@class,"ok")]'
        ).click()
        self.student.find(
            By.XPATH, '//span[contains(text(),"email_2@test.com")]').click()
        self.student.sleep(1)
        boxes = self.student.find_all(
            By.XPATH, '//input[@type="checkbox" and @class="searchable"]'
        )
        boxes[-1].click()
        # delete the new email
        self.student.sleep(1)
        self.student.find(
            By.XPATH, '//div[@class="email-entry"]' +
            '//span[contains(@class,"trash")]').click()
        self.student.find(
            By.XPATH, '//div[@class="popover-content"]' +
            '//button[contains(text(),"OK")]').click()

        self.ps.test_updates['passed'] = True

    # Case C8221 - 015 - User | Delete an email address
    @pytest.mark.skipif(str(8221) not in TESTS, reason='Excluded')
    def test_user_delete_an_email_adress_8221(self):
        """Delete an email address.

        Steps:
        Enter the teacher user account in the username and password text boxes
        Click on the Sign in button
        Click on an email adress
        Check on the trachcan icon next to seleceted email adress
        Click on the OK button

        Expected Result:
        Email adress is no longer in the list of email adresses
        """
        self.ps.test_updates['name'] = 't1.34.015' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.34', 't1.34.015', '8221']
        self.ps.test_updates['passed'] = False

        # create an email
        self.student.login(url='http://accounts-qa.openstax.org')
        self.student.wait.until(
            expect.visibility_of_element_located((By.ID, 'add-an-email'))
        ).click()
        self.student.find(
            By.XPATH, '//input[@type="text"]').send_keys('email_2@test.com')
        self.student.find(
            By.XPATH, '//button[@type="submit"]//i[contains(@class,"ok")]'
        ).click()
        email = self.student.find(
            By.XPATH, '//span[contains(text(),"email_2@test.com")]')
        # delete the new email
        email.click()
        self.student.find(
            By.XPATH,
            '//div[@class="email-entry"]//span[contains(@class,"trash")]'
        ).click()
        self.student.find(
            By.XPATH,
            '//div[@class="popover-content"]//button[contains(text(),"OK")]'
        ).click()

        self.ps.test_updates['passed'] = True

    # Case C8222 - 016 - User | Edit the account password
    @pytest.mark.skipif(str(8222) not in TESTS, reason='Excluded')
    def test_user_edit_the_account_password_8222(self):
        """Edit the account password.

        Steps:
        Enter the teacher user account in the username and password text boxes
        Click on the Sign in button
        Check on the pencil icon next to password
        Enter new password into each of the textboxes
        Click on the checkmark button

        Expected Result:
        Confirmation message appears saying password has been changed
        """
        self.ps.test_updates['name'] = 't1.34.016' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.34', 't1.34.016', '8222']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.login(url='http://accounts-qa.openstax.org')
        self.student.find(
            By.XPATH,
            '//div[@data-provider="identity"]//span[contains(@class,"pencil")]'
        ).click()
        self.student.find(
            By.XPATH, '//input[@name="password"]'
        ).send_keys(self.student.password)
        self.student.find(
            By.XPATH, '//input[@name="password_confirmation"]'
        ).send_keys(self.student.password)
        self.student.find(
            By.XPATH, '//button[@type="submit"]//i[contains(@class,"ok")]'
        ).click()
        self.student.find(
            By.XPATH, '//span[contains(text(),"Password changed")]')

        self.ps.test_updates['passed'] = True

    # Case C8223 - 017 - User | Cancel editing the account password
    @pytest.mark.skipif(str(8223) not in TESTS, reason='Excluded')
    def test_user_cancel_editing_the_account_password_8223(self):
        """Cancel editing the account password.

        Steps:
        Enter the teacher user account in the username and password text boxes
        Click on the Sign in button
        Check on the pencil icon next to password
        Enter new password into each of the textboxes
        Click on the X button

        Expected Result:
        No changes have been made to user account
        """
        self.ps.test_updates['name'] = 't1.34.017' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.34', 't1.34.017', '8223']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.login(url='http://accounts-qa.openstax.org')
        self.student.find(
            By.XPATH,
            '//div[@data-provider="identity"]//span[contains(@class,"pencil")]'
        ).click()
        self.student.find(
            By.XPATH, '//input[@name="password"]'
        ).send_keys(self.student.password)
        self.student.find(
            By.XPATH,
            '//input[@name="password_confirmation"]'
        ).send_keys(self.student.password)
        self.student.find(
            By.XPATH,
            '//button[@type="button"]//i[contains(@class,"remove")]'
        ).click()

        self.ps.test_updates['passed'] = True

    # Case C8224 - 018 - User | Enable login with username and password
    @pytest.mark.skipif(str(8224) not in TESTS, reason='Excluded')
    def test_user_enable_standard_login_with_username_and_password_8224(self):
        """Enable standard login with username and password.

        Steps:
        Login with something other than password
        Click enable other login options
        Click the plus sign next to password
        Enter password into input, and enter agian to confirm
        Click check mark

        Expected Result:
        Confirmation message displayed.
        Password has been added to How you sign in list
        """
        self.ps.test_updates['name'] = 't1.34.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.34', 't1.34.003', '8208']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        # create a social login account
        self.student.find(By.LINK_TEXT, 'Sign up').click()
        self.student.find(By.ID, 'google-login-button').click()
        self.student.page.wait_for_page_load()
        self.student.find(
            By.ID, 'Email').send_keys(self.google_account)
        self.student.find(By.ID, 'next').click()
        self.student.find(
            By.ID, 'Passwd').send_keys(self.google_password)
        self.student.find(By.ID, 'signIn').click()
        self.student.page.wait_for_page_load()
        username = self.student.find(
            By.ID, 'signup_username').get_attribute('value')
        self.student.find(By.ID, 'signup_i_agree').click()
        self.student.find(
            By.ID, 'create_account_submit').click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[@id="session-info"]//a[text()="'+username+'"]')
            )
        )
        # add password sign in
        self.student.find(
            By.ID, 'enable-other-sign-in').click()
        self.student.sleep(2)
        self.student.find(
            By.XPATH, '//div[@data-provider="identity"]//' +
            'span[contains(@class,"add mod")]').click()
        self.student.sleep(1)
        self.student.find(
            By.XPATH, '//input[@name="password"]'
        ).send_keys(self.student.password)
        self.student.find(
            By.XPATH,
            '//input[@name="password_confirmation"]'
        ).send_keys(self.student.password)
        self.student.find(
            By.XPATH,
            '//button[@type="submit"]//i[contains(@class,"ok")]'
        ).click()
        self.student.sleep(1)
        # delete social login option so it can be reused
        self.student.find(
            By.XPATH,
            '//div[contains(@class,"enabled-providers")]' +
            '//div[@data-provider="google_oauth2"]' +
            '//span[contains(@class,"trash")]'
        ).click()
        self.student.find(
            By.XPATH, '//div[@class="popover-content"]//button[text()="OK"]'
        ).click()

        self.ps.test_updates['passed'] = True

    # Case C8225 - 019 - User | Enable Facebook login
    @pytest.mark.skipif(str(8225) not in TESTS, reason='Excluded')
    def test_user_enable_facebook_login_8225(self):
        """Enable Facebook login.

        Steps:
        Sign in with password
        Click on Enable other sign in options
        Click on the plus sign next to facebook
        Enter email and passwork on facebook
        Click login OR click return

        Expected Result:
        Confirmation message displayed.
        Facebook has been added to How you sign in list
        """
        self.ps.test_updates['name'] = 't1.34.019' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.34', 't1.34.019', '8225']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.login(url='http://accounts-qa.openstax.org')
        self.student.find(
            By.ID, 'enable-other-sign-in').click()
        self.student.sleep(2)
        self.student.find(
            By.XPATH,
            '//div[@data-provider="facebook"]//' +
            'span[contains(@class,"add mod")]'
        ).click()
        self.student.page.wait_for_page_load()
        self.student.find(
            By.ID, 'email').send_keys(self.facebook_account)
        self.student.find(
            By.ID, 'pass').send_keys(self.facebook_password+Keys.RETURN)
        # self.student.find(
        #    By.XPATH, '//button[@name="login"]').click()
        self.student.page.wait_for_page_load()
        # check that it was added
        self.student.find(
            By.XPATH,
            '//div[contains(@class,"enabled-providers")]' +
            '//div[@class="authentication" and @data-provider="facebook"]')
        # delete login option
        self.student.find(
            By.XPATH,
            '//div[contains(@class,"enabled-providers")]' +
            '//div[@data-provider="facebook"]//span[contains(@class,"trash")]'
        ).click()
        self.student.find(
            By.XPATH, '//div[@class="popover-content"]//button[text()="OK"]'
        ).click()

        self.ps.test_updates['passed'] = True

    # Case C8226 - 020 - User | Enable Google login
    @pytest.mark.skipif(str(8226) not in TESTS, reason='Excluded')
    def test_user_enable_google_login_8226(self):
        """Enable Google login.

        Steps:
        Login with  password
        Click enable other login options
        Click the plus sign next to google
        Enter email into input and then click next
        Enter password and then click sign in

        Expected Result:
        Confirmation message displayed.
        Google has been added to How you sign in list
        """
        self.ps.test_updates['name'] = 't1.34.020' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.34', 't1.34.020', '8226']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.login(url='http://accounts-qa.openstax.org')
        self.student.find(
            By.ID, 'enable-other-sign-in').click()
        self.student.sleep(2)
        self.student.find(
            By.XPATH, '//div[@data-provider="google_oauth2"]//' +
            'span[contains(@class,"add mod")]').click()
        self.student.page.wait_for_page_load()
        self.student.find(
            By.ID, 'Email').send_keys(self.google_account)
        self.student.find(By.ID, 'next').click()
        self.student.find(
            By.ID, 'Passwd').send_keys(self.google_password)
        self.student.find(By.ID, 'signIn').click()
        self.student.page.wait_for_page_load()
        # check that it was added
        self.student.find(
            By.XPATH,
            '//div[contains(@class,"enabled-providers")]' +
            '//div[@class="authentication" and ' +
            '@data-provider="google_oauth2"]')
        # delete login option
        self.student.find(
            By.XPATH,
            '//div[contains(@class,"enabled-providers")]' +
            '//div[@data-provider="google_oauth2"]' +
            '//span[contains(@class,"trash")]'
        ).click()
        self.student.find(
            By.XPATH, '//div[@class="popover-content"]//button[text()="OK"]'
        ).click()

        self.ps.test_updates['passed'] = True

    # Case C8227 - 021 - User | Enable Twitter login
    @pytest.mark.skipif(str(8227) not in TESTS, reason='Excluded')
    def test_user_enable_twitter_login_8227(self):
        """Enable Twitter login.

        Steps:
        Login with  password
        Click enable other login options
        Click the plus sign next to twitter
        Enter email and password into input boxes
        Click login

        Expected Result:
        Confirmation message displayed.
        Twitter has been added to How you sign in list
        """
        self.ps.test_updates['name'] = 't1.34.021' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.34', 't1.34.021', '8227']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.login(url='http://accounts-qa.openstax.org')
        self.student.find(
            By.ID, 'enable-other-sign-in').click()
        self.student.sleep(2)
        self.student.find(
            By.XPATH, '//div[@data-provider="twitter"]//' +
            'span[contains(@class,"add mod")]').click()
        self.student.page.wait_for_page_load()
        self.student.find(
            By.ID, 'username_or_email').send_keys(self.twitter_account)
        self.student.find(
            By.ID, 'password').send_keys(self.twitter_password)
        self.student.find(By.ID, 'allow').click()
        self.student.page.wait_for_page_load()
        # check that it was added
        self.student.find(
            By.XPATH, '//div[contains(@class,"enabled-providers")]' +
            '//div[@class="authentication" and @data-provider="twitter"]')
        # delete login option
        self.student.find(
            By.XPATH,
            '//div[contains(@class,"enabled-providers")]' +
            '//div[@data-provider="twitter"]//span[contains(@class,"trash")]'
        ).click()
        self.student.find(
            By.XPATH, '//div[@class="popover-content"]//button[text()="OK"]'
        ).click()

        self.ps.test_updates['passed'] = True

    # Case C8387 - 022 - User | Delete login option
    @pytest.mark.skipif(str(8387) not in TESTS, reason='Excluded')
    def test_user_delete_login_option_8387(self):
        """Delete login option.

        Steps:
        Click on the trashcan icon next to login in option to be removed
        Click on the 'ok' button

        Expected Result:
        Login option removed,
        and no longer visible under the list of How you sign in
        """
        self.ps.test_updates['name'] = 't1.34.022' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.34', 't1.34.022', '8287']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.login(url='http://accounts-qa.openstax.org')
        self.student.find(
            By.ID, 'enable-other-sign-in').click()
        self.student.sleep(2)
        self.student.find(
            By.XPATH, '//div[@data-provider="twitter"]//' +
            'span[contains(@class,"add mod")]').click()
        self.student.page.wait_for_page_load()
        self.student.find(
            By.ID, 'username_or_email').send_keys(self.twitter_account)
        self.student.find(
            By.ID, 'password').send_keys(self.twitter_password)
        self.student.find(By.ID, 'allow').click()
        self.student.page.wait_for_page_load()
        # check that it was added
        self.student.find(
            By.XPATH,
            '//div[contains(@class,"enabled-providers")]' +
            '//div[@class="authentication" and @data-provider="twitter"]')
        # delete login option
        self.student.find(
            By.XPATH,
            '//div[contains(@class,"enabled-providers")]' +
            '//div[@data-provider="twitter"]//span[contains(@class,"trash")]'
        ).click()
        self.student.find(
            By.XPATH, '//div[@class="popover-content"]//button[text()="OK"]'
        ).click()

        self.ps.test_updates['passed'] = True

    # Case C8388 - 023 - User | Info Icon shows definiton for searchable option
    @pytest.mark.skipif(str(8388) not in TESTS, reason='Excluded')
    def test_user_info_icon_shows_definition_for_searchable_option_8388(self):
        """Info Icon shows definiton for searchable option.

        Steps:
        Enter the teacher user account in the username and password text boxes
        Click on the Sign in button
        Click on an email address
        Click on the info icon next to the searchable check box

        Expected Result:
        Info icon shows definition for searchable option
        """
        self.ps.test_updates['name'] = 't1.34.023' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.34', 't1.34.023', '8388']
        self.ps.test_updates['passed'] = False

        # create an email
        self.student.login(url='http://accounts-qa.openstax.org')
        self.student.wait.until(
            expect.visibility_of_element_located((By.ID, 'add-an-email'))
        ).click()
        self.student.find(
            By.XPATH, '//input[@type="text"]').send_keys('email_2@test.com')
        self.student.find(
            By.XPATH, '//button[@type="submit"]//i[contains(@class,"ok")]'
        ).click()
        self.student.sleep(1)
        # check info icon (must reload page to work)
        self.student.get('https://accounts-qa.openstax.org/profile')
        self.student.page.wait_for_page_load()
        email = self.student.find(
            By.XPATH, '//span[contains(text(),"email_2@test.com")]')
        email.click()
        info_icon = self.student.find(
            By.XPATH, '//input[@type="checkbox" and @class="searchable"]')
        actions = ActionChains(self.student.driver)
        actions.move_to_element(info_icon).perform()
        self.student.sleep(1)
        self.student.find(
            By.XPATH, '//i[@data-toggle="tooltip"]')
        # delete the new email
        self.student.sleep(1)
        self.student.find(
            By.XPATH, '//div[@class="email-entry"]' +
            '//span[contains(@class,"trash")]').click()
        self.student.find(
            By.XPATH, '//div[@class="popover-content"]' +
            '//button[contains(text(),"OK")]').click()

        self.ps.test_updates['passed'] = True
