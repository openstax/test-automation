"""Product, Epic 34 - AccountManagement"""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
from random import randint  # NOQA
from selenium.webdriver.common.by import By  # NOQA
from selenium.webdriver.support import expected_conditions as expect  # NOQA
from staxing.assignment import Assignment  # NOQA

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Teacher  # NOQA

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': '50.0',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([8207, 8208, 8209, 8210, 8211,
         8212, 8213, 8214, 8215, 8216,
         8217, 8218, 8219, 8220, 8221,
         8222, 8223, 8224, 8225, 8226,
         8387, 8388])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestEpicName(unittest.TestCase):
    """Product.Epic - Epic Text."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.Teacher = Teacher(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        ###got to accounts-XXXX.openstax.org

    def tearDown(self):
        """Test destructor."""
        self.ps.update_job(job_id=str(self.teacher.driver.session_id),
                           **self.ps.test_updates)
        try:
            self.teacher.delete()
        except:
            pass

    # Case C8207 - 001 - User | Create a new Account with a username and password
    @pytest.mark.skipif(str(8207) not in TESTS, reason='Excluded')  # NOQA
    def test_user_create_a_new_account_with_a_username_and_password(self):
        """ Create a new Account with a username and password

        Steps:
        Click on the Sign up link
        Click on the Sign up with password button
        Enter first name into the 'First Name' text box
        Enter last name into the 'Last Name' text box
        Enter email into the 'Email Address' text box [in the form example@example.example]
        Enter username into the 'Username' text box
        Enter password into the 'Password' text box
        Renter password into the 'Confirm Password' text box
        Click the "Create Account Button"
        ########?????click the don't save passwords stuff, is this part of test case??????????????
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

        self.ps.test_updates['passed'] = True

    # Case C8208 - 002 - User | Create a new Account with Facebook
    @pytest.mark.skipif(str(8208) not in TESTS, reason='Excluded')  # NOQA
    def test_user_create_a_new_account_with_facebook(self):
        """ Create a new Account with Facebook

        Steps:
        Click on the Sign up link
        Click on the Sign up with Facebook button
        [redirects to facebbok.com]
        If you are not logged into Facebook:
        -enter email and password for facebook, then click the "Log In" button
        Click on the "okay" button

        [redirects back to accounts-qa.openstax.org]
        Click the checkbox to agree to the Terms of Use and Privacy Policy
        Click the "Create Account Button"
        
        Expected Result:
        User logged in and presented with their dashboard
        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

   # Case C8209 - 003 - User | Create a new Account with Google
    @pytest.mark.skipif(str(8209) not in TESTS, reason='Excluded')  # NOQA
    def test_user_create_a_new_account_with_google(self):
        """ Create a new Account with Google

        Steps:
        Click on the Sign up link
        Click on the Sign up with Google button
        [redirects to accounts.google.com]
        If you are not logged in:
        - Click the 'Add Account' button
        - Enter email into text box
        - Click on the 'Next' button
        - Enter password into text box 
        - Click on the 'Sign in' button
        Click on the "Allow" button
        [redirects back to accounts-qa.openstax.org]
        Click the checkbox to agree to the Terms of Use and Privacy Policy
        Click the "Create Account Button"

        
        Expected Result:
        User logged in and presented with their dashboard
        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # Case C8210 - 004 - User | Create a new Account with Twitter
    @pytest.mark.skipif(str(8210) not in TESTS, reason='Excluded')  # NOQA
    def test_user_create_a_new_account_with_twitter(self):
        """ Create a new Account with Twitter

        Steps:
        Click on the Sign up link
        Click on the Sign up with Twitter button
        ??????????????????????????????????????????????????
        
        Expected Result:
        User logged in and presented with their dashboard
        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # Case C8211 - 005 - User | Accept the terms of service
    @pytest.mark.skipif(str(8211) not in TESTS, reason='Excluded')  # NOQA
    def test_user_accept_the_terms_of_service(self):
        """ Accept the terms of service

        Steps:
        Click on the Sign up link
        Click on the Sign up with password button
        Enter first name into the 'First Name' text box
        Enter last name into the 'Last Name' text box
        Enter email into the 'Email Address' text box [in the form example@example.example]
        Enter username into the 'Username' text box
        Enter password into the 'Password' text box
        Renter password into the 'Confirm Password' text box
        Click the "Create Account Button"
        ########?????click the don't save passwords stuff, is this part of test case??????????????
        Click the checkbox, and click 'I Agree' for the Terms of Use
       
        Expected Result:
        Terms of use are accepted and user is presented witht the privacy policy
        """
        self.ps.test_updates['name'] = 't1.34.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.34', 't1.34.005', '8211']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8212 - 006 - User | Accept the privacy policy
    @pytest.mark.skipif(str(8212) not in TESTS, reason='Excluded')  # NOQA
    def test_user_accept_the_privacy_policy(self):
        """ Accept the privacy policy

        Steps:
        Click on the Sign up link
        Click on the Sign up with password button
        Enter first name into the 'First Name' text box
        Enter last name into the 'Last Name' text box
        Enter email into the 'Email Address' text box [in the form example@example.example]
        Enter username into the 'Username' text box
        Enter password into the 'Password' text box
        Renter password into the 'Confirm Password' text box
        Click the "Create Account Button"
        ########?????click the don't save passwords stuff, is this part of test case??????????????
        Click the checkbox, and click 'I Agree' for the Terms of Use
        Click the checkbox, and click 'I Agree' for the Privacy Policy
       
        Expected Result:
        User logged in and presented with their dashboard
        """
        self.ps.test_updates['name'] = 't1.34.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.34', 't1.34.006', '8212']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8213 - 007 - User | Log into Accounts
    @pytest.mark.skipif(str(8213) not in TESTS, reason='Excluded')  # NOQA
    def test_user_log_into_accounts(self):
        """ Log into Accounts

        Steps:
        Enter the teacher user account in the username and password text boxes
        Click on the Sign in button

        Expected Result:
        User logged in and presented with their dashboard
        """
        self.ps.test_updates['name'] = 't1.34.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.34', 't1.34.007', '8213']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8214 - 008 - User | Edit account name
    @pytest.mark.skipif(str(8214) not in TESTS, reason='Excluded')  # NOQA
    def test_user_edit_account_name(self):
        """ Edit account name

        Steps:
        Enter the teacher user account in the username and password text boxes
        Click on the Sign in button
        Click on the user's name
        Enter new information into Title, First name, Last Name, and Suffix text boxes
        Click on the checkmark button
        
        Expected Result:
        User's name has been updated
        """
        self.ps.test_updates['name'] = 't1.34.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.34', 't1.34.008', '8214']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8215 - 009 - User | Cancel editing the account name
    @pytest.mark.skipif(str(8215) not in TESTS, reason='Excluded')  # NOQA
    def test_user_canel_editing_the_account_name(self):
        """ Cancel editing the account name

        Steps:
        Enter the teacher user account in the username and password text boxes
        Click on the Sign in button
        Click on the user's name
        Enter new information into Title, First name, Last Name, and Suffix text boxes
        Click on the X button       

        Expected Result:
        User's name has not changed
        """
        self.ps.test_updates['name'] = 't1.34.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.34', 't1.34.009', '8215']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8216 - 010 - User | Edit the username
    @pytest.mark.skipif(str(8216) not in TESTS, reason='Excluded')  # NOQA
    def test_user_edit_the_username(self):
        """ Edit the username

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

        self.ps.test_updates['passed'] = True

    # Case C8217 - 011 - User | Cancel editing the username
    @pytest.mark.skipif(str(8217) not in TESTS, reason='Excluded')  # NOQA
    def test_user_canel_editing_the_username(self):
        """ Cancel editing the username

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

        self.ps.test_updates['passed'] = True

    # Case C8218 - 012 - User | Add an email address
    @pytest.mark.skipif(str(8218) not in TESTS, reason='Excluded')  # NOQA
    def test_user_add_an_email_address(self):
        """ Add an email address

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

        self.ps.test_updates['passed'] = True

    # Case C8218 - 012 - User | Add an email address
    @pytest.mark.skipif(str(8218) not in TESTS, reason='Excluded')  # NOQA
    def test_user_add_an_email_address(self):
        """ Add an email address

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

        self.ps.test_updates['passed'] = True

    # Case C8219 - 013 - User | Verify an email address
    @pytest.mark.skipif(str(8219) not in TESTS, reason='Excluded')  # NOQA
    def test_user_verify_an_email_address(self):
        """ Verify an email address

        Steps:
        Enter the teacher user account in the username and password text boxes
        Click on the Sign in button
        Click on Click to verify next to an email address
        #####then log into chosen emailadress and verify

        Expected Result:
        Confirmation message displayed saying an email has been sent.
        Email has been sent
        Email adress is verified
        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # Case C8220 - 014 - User | Make an email address serachable
    @pytest.mark.skipif(str(8220) not in TESTS, reason='Excluded')  # NOQA
    def test_user_make_an_email_adress_searchable(self):
        """ Make an email address searchable

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

        self.ps.test_updates['passed'] = True

    # Case C8221 - 015 - User | Delete an email address
    @pytest.mark.skipif(str(8221) not in TESTS, reason='Excluded')  # NOQA
    def test_user_delete_an_email_adress(self):
        """ Delete an email address

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

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # Case C8222 - 016 - User | Edit the account password
    @pytest.mark.skipif(str(8222) not in TESTS, reason='Excluded')  # NOQA
    def test_user_edit_the_account_password(self):
        """ Edit the account password

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

        self.ps.test_updates['passed'] = True

    # Case C8223 - 017 - User | Cancel editing the account password
    @pytest.mark.skipif(str(8223) not in TESTS, reason='Excluded')  # NOQA
    def test_user_cancel_editing_the_account_password(self):
        """ Cancel editing the account password

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

        self.ps.test_updates['passed'] = True

    # Case C8224 - 018 - User | Enable standard login with username and password
    @pytest.mark.skipif(str(8224) not in TESTS, reason='Excluded')  # NOQA
    def test_user_enable_standard_login_with_username_and_password(self):
        """ Enable standard login with username and password

        Steps:

        Expected Result:
        Confirmation message displayed. Password has been added to How you sign in list
        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # Case C8225 - 019 - User | Enable Facebook login 
    @pytest.mark.skipif(str(8225) not in TESTS, reason='Excluded')  # NOQA
    def test_user_enable_facebook_login(self):
        """ Enable Facebook login 

        Steps:

        Expected Result:
        Confirmation message displayed. Facebook has been added to How you sign in list
        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # Case C8226 - 020 - User | Enable Google login 
    @pytest.mark.skipif(str(8226) not in TESTS, reason='Excluded')  # NOQA
    def test_user_enable_google_login(self):
        """ Enable Google login 

        Steps:

        Expected Result:
        Confirmation message displayed. Google has been added to How you sign in list
        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # Case C8227 - 021 - User | Enable Twitter login 
    @pytest.mark.skipif(str(8227) not in TESTS, reason='Excluded')  # NOQA
    def test_user_enable_twitter_login(self):
        """ Enable Twitter login 

        Steps:

        Expected Result:
        Confirmation message displayed. Twitter has been added to How you sign in list
        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # Case C8387 - 022 - User | Delete login option 
    @pytest.mark.skipif(str(8227) not in TESTS, reason='Excluded')  # NOQA
    def test_user_delete_login_option(self):
        """ Delete login option 

        Steps:
        Enter the user account in the username and password text boxes
        Click on the Sign in button
        ######should the user have to login as someone with mutiple login options, or add a second option then delete it?

        Expected Result:
        Login option removed, and no longer visible under the list of How you sign in
        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # Case C8388 - 023 - User | Info Icon shows definiton for searchable option
    @pytest.mark.skipif(str(8388) not in TESTS, reason='Excluded')  # NOQA
    def test_user_info_icon_shows_definition_for_searchable_option(self):
        """ Info Icon shows definiton for searchable option

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

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True
