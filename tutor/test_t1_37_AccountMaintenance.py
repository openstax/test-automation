"""Tutor v1, Epic 37 - Account Maintenance."""

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
from staxing.helper import Admin  # NOQA

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': '50.0',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([8247, 8248, 8249, 8250,
         8251, 8252, 8253])  # NOQA
)


@PastaDecorator.on_platforms(BROWSERS)
class TestEpicName(unittest.TestCase):
    """T1.37 - Account Maintenance."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.Teacher = Teacher(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )

    def tearDown(self):
        """Test destructor."""
        self.ps.update_job(job_id=str(self.teacher.driver.session_id),
                           **self.ps.test_updates)
        try:
            self.teacher.delete()
        except:
            pass

    # Case C8247 - 001 - Admin | Search for a username 
    @pytest.mark.skipif(str(8247) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Search for a username.

        Steps:

        Click on the user's name in the top right corner to open drop down menu
        Click on the 'Admin' option of the drop down menu
        Click on 'Users' on the bar across the top
        Enter a username into the search here text box
        Click on the 'Search' button


        Expected Result:

        A list of users with the search term in their name, or username is displayed.

        """
        self.ps.test_updates['name'] = 't1.37.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.37',
            't1.37.001',
            '8247'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8248 - 002 - Admin | Search for a user's name
    @pytest.mark.skipif(str(8248) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Search for a user's name.

        Steps:

        Click on the user's name in the top right corner to open drop down menu
        Click on the 'Admin' option of the drop down menu
        Click on 'Users' on the bar across the top
        Enter a user's name into the search here text box
        Click on the 'Search' button


        Expected Result:

        A list of users with the search term in their name, or username is displayed.

        """
        self.ps.test_updates['name'] = 't1.37.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.37',
            't1.37.002',
            '8248'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8249 - 003 - Admin | Create a new user
    @pytest.mark.skipif(str(8249) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Create a new user. 

        Steps:

        Click on the user's name in the top right corner to open drop down menu
        Click on the 'Admin' option of the drop down menu
        Click on 'Users' on the bar across the top
        Scroll to the bottom of the page
        Click on the 'Create user' button
        Enter desired account information into the Username, Password, First name, and Last name text boxes
        [optional] Enter additional information into the Full name override, Title, and Email text boxes
        [optional] Check one of more of the following checkboxes: administrator, Customer Service, Content Analysis
        Click on the 'Save' button


        Expected Result:

        Takes User back to the Users screen. New user is added.

        """
        self.ps.test_updates['name'] = 't1.37.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.37',
            't1.37.003',
            '8249'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8250 - 004 - Admin | Edit a user
    @pytest.mark.skipif(str(8250) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Edit a user. 

        Steps:

        Click on the user's name in the top right corner to open drop down menu
        Click on the 'Admin' option of the drop down menu
        Click on 'Users' on the bar across the top
        [optional] Enter a user's name into the search here text box, then Click on the 'Search' button
        Click on the 'Edit' button next to desired user
        Enter new account information into any of the following: Username, Password, First name, and Last name, Full name override, Title, and Email text boxes.
        Click on the 'Save' button


        Expected Result:

        User is taken back to the User screen. The chosen account's information is updated

        """
        self.ps.test_updates['name'] = 't1.37.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.37',
            't1.37.004',
            '8250'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8251 - 005 - Admin | Assign elevated permissions
    @pytest.mark.skipif(str(8251) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Assign elevated permissions. 

        Steps:

        Click on the user's name in the top right corner to open drop down menu
        Click on the 'Admin' option of the drop down menu
        Click on 'Users' on the bar across the top
        [optional] Enter a user's name into the search here text box, then Click on the 'Search' button
        Click on the 'Edit' button next to desired user
        [optional] Enter new account information into any of the following: Username, Password, First name, and Last name, Full name override, Title, and Email text boxes.
        If check box for chosen permission is not checked, click on check box.
        Click on the 'Save' button


        Expected Result:

        User is taken back to the User screen. The chosen account's permissions are modified.

        """
        self.ps.test_updates['name'] = 't1.37.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.37',
            't1.37.005',
            '8251'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8252 - 006 - Admin | Remove elevated permissions
    @pytest.mark.skipif(str(8252) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Remove elevated permissions. 

        Steps:

        Click on the user's name in the top right corner to open drop down menu
        Click on the 'Admin' option of the drop down menu
        Click on 'Users' on the bar across the top
        [optional] Enter a user's name into the search here text box, then Click on the 'Search' button
        Click on the 'Edit' button next to desired user
        [optional] Enter new account information into any of the following: Username, Password, First name, and Last name, Full name override, Title, and Email text boxes.
        If check box for chosen permission is checked, click on check box to uncheck it.
        Click on the 'Save' button


        Expected Result:

        User is taken back to the User screen. The chosen account's permissions are modified.

        """
        self.ps.test_updates['name'] = 't1.37.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.37',
            't1.37.006',
            '8252'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8253 - 007 - Admin | Impersonate a user
    @pytest.mark.skipif(str(8253) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Impersonate a user. 

        Steps:

        Click on the user's name in the top right corner to open drop down menu
        Click on the 'Admin' option of the drop down menu
        Click on 'Users' on the bar across the top
        [optional] Enter a user's name into the search here text box, then Click on the 'Search' button
        Click on the 'Sign in as' button next to chosen user


        Expected Result:

        Signs in as chosen chosen user. Goes to chosen users initial screen after login (different depending on the user)

        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

