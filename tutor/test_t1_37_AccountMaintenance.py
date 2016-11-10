"""Tutor v1, Epic 37 - Account Maintenance."""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.ui import WebDriverWait

from staxing.helper import Admin

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': 'latest',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([
        8247, 8248, 8249, 8250, 8251,
        8252, 8253
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestAccountMaintenance(unittest.TestCase):
    """T1.37 - Account Maintenance."""

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
        self.admin.wait = WebDriverWait(self.admin.driver, 15)
        self.admin.open_user_menu()
        self.admin.wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Admin')
            )
        ).click()
        self.admin.page.wait_for_page_load()
        self.admin.driver.find_element(
            By.XPATH,
            '//a[contains(text(),"Users")]'
        ).click()

    def tearDown(self):
        """Test destructor."""
        self.ps.update_job(
            job_id=str(self.admin.driver.session_id),
            **self.ps.test_updates
        )
        try:
            self.admin.delete()
        except:
            pass

    # Case C8247 - 001 - Admin | Search for a username
    @pytest.mark.skipif(str(8247) not in TESTS, reason='Excluded')
    def test_admin_search_for_a_username_8247(self):
        """Search for a username.

        Steps:
        Enter a username into the search here text box
        Click on the 'Search' button

        Expected Result:
        A list of users with the search term in their name,
        or username is displayed.
        """
        self.ps.test_updates['name'] = 't1.37.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.37', 't1.37.001', '8247']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.driver.find_element(
            By.ID, 'query').send_keys('Atticus')
        self.admin.driver.find_element(
            By.XPATH, '//input[@value="Search"]').click()
        self.admin.driver.find_element(
            By.XPATH, '//td[contains(text(),"Atticus")]')

        self.ps.test_updates['passed'] = True

    # Case C8248 - 002 - Admin | Search for a user's name
    @pytest.mark.skipif(str(8248) not in TESTS, reason='Excluded')
    def test_admin_search_for_a_users_name_8248(self):
        """Search for a user's name.

        Steps:
        Click on the user's name in the top right corner to open drop down menu
        Click on the 'Admin' option of the drop down menu
        Click on 'Users' on the bar across the top
        Enter a user's name into the search here text box
        Click on the 'Search' button

        Expected Result:
        A list of users with the search term in their name,
        or username is displayed.
        """
        self.ps.test_updates['name'] = 't1.37.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.37', 't1.37.002', '8248']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.driver.find_element(
            By.ID, 'query').send_keys('student01')
        self.admin.driver.find_element(
            By.XPATH, '//input[@value="Search"]').click()
        self.admin.driver.find_element(
            By.XPATH, '//td[text()="student01"]')

        self.ps.test_updates['passed'] = True

    # Case C8249 - 003 - Admin | Create a new user
    @pytest.mark.skipif(str(8249) not in TESTS, reason='Excluded')
    def test_admin_create_a_user_8249(self):
        """Create a new user.

        Steps:
        Scroll to the bottom of the page
        Click on the 'Create user' button
        Enter account information into:
        -Username, Password, First name, and Last name text boxes
        Click on the 'Save' button

        Expected Result:
        Takes User back to the Users screen. New user is added.
        """
        self.ps.test_updates['name'] = 't1.37.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.37', 't1.37.003', '8249']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        num = str(randint(0, 999))
        self.admin.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        self.admin.driver.find_element(
            By.XPATH, '//a[contains(text(),"Create user")]').click()
        self.admin.wait.until(
            expect.element_to_be_clickable((By.ID, 'user_username'))
        ).click()
        self.admin.driver.find_element(
            By.ID, 'user_username').send_keys('automated_test_user_'+num)
        self.admin.driver.find_element(
            By.ID, 'user_password').send_keys('password')
        self.admin.driver.find_element(
            By.ID, 'user_first_name').send_keys('first_name_'+num)
        self.admin.driver.find_element(
            By.ID, 'user_last_name').send_keys('last_name_'+num)
        self.admin.driver.find_element(
            By.XPATH, '//input[@value="Save"]').click()
        # look up account to check that the account was made
        self.admin.wait.until(
            expect.element_to_be_clickable((By.ID, 'query'))
        ).send_keys('automated_test_user_'+num)
        self.admin.driver.find_element(
            By.XPATH, '//input[@value="Search"]').click()
        self.admin.driver.find_element(
            By.XPATH, '//td[text()="automated_test_user_'+num+'"]')

        self.ps.test_updates['passed'] = True

    # Case C8250 - 004 - Admin | Edit a user
    @pytest.mark.skipif(str(8250) not in TESTS, reason='Excluded')
    def test_admin_edit_a_user_8250(self):
        """Edit a user.

        Steps:
        Create a user to edit
        Enter the user's name into the search here text box
        Click on the 'Search' button
        Click on the 'Edit' button next to the user
        Enter new account information into the First name text box
        Click on the 'Save' button

        Expected Result:
        User is taken back to the User screen.
        The chosen account's information is updated
        """
        self.ps.test_updates['name'] = 't1.37.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.37', 't1.37.004', '8250']
        self.ps.test_updates['passed'] = False

        # create a user
        num = str(randint(1000, 1999))
        self.admin.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        self.admin.driver.find_element(
            By.XPATH, '//a[contains(text(),"Create user")]').click()
        self.admin.wait.until(
            expect.element_to_be_clickable((By.ID, 'user_username'))
        ).click()
        self.admin.driver.find_element(
            By.ID, 'user_username').send_keys('automated_test_user_'+num)
        self.admin.driver.find_element(
            By.ID, 'user_password').send_keys('password')
        self.admin.driver.find_element(
            By.ID, 'user_first_name').send_keys('first_name_'+num)
        self.admin.driver.find_element(
            By.ID, 'user_last_name').send_keys('last_name_'+num)
        self.admin.driver.find_element(
            By.XPATH, '//input[@value="Save"]').click()
        # search for that user
        self.admin.wait.until(
            expect.element_to_be_clickable((By.ID, 'query'))
        ).send_keys('automated_test_user_'+num)
        self.admin.driver.find_element(
            By.XPATH, '//input[@value="Search"]').click()
        # edit user
        self.admin.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(text(),"Edit")]')
            )
        ).click()
        self.admin.driver.find_element(
            By.ID, 'user_first_name').send_keys('_EDITED')
        self.admin.driver.find_element(
            By.XPATH, '//input[@value="Save"]').click()
        # search for user to make sure they were updated
        self.admin.wait.until(
            expect.element_to_be_clickable((By.ID, 'query'))
        ).send_keys('automated_test_user_'+num)
        self.admin.driver.find_element(
            By.XPATH, '//input[@value="Search"]').click()
        self.admin.driver.find_element(
            By.XPATH, '//td[contains(text(),"first_name_' + num + '_EDITED")]')

        self.ps.test_updates['passed'] = True

    # Case C8251 - 005 - Admin | Assign elevated permissions
    @pytest.mark.skipif(str(8251) not in TESTS, reason='Excluded')
    def test_admin_assign_elevated_permissions_8251(self):
        """Assign elevated permissions.

        Steps:
        Create a user to edit
        Enter the user's username into the search here text box
        Click on the 'Search' button
        Click on the 'Edit' button next to the user
        If check box for chosen permission is not checked, click on check box.
        Click on the 'Save' button

        Expected Result:
        User is taken back to the User screen.
        The chosen account's permissions are modified.
        """
        self.ps.test_updates['name'] = 't1.37.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.37', 't1.37.005', '8251']
        self.ps.test_updates['passed'] = False

        # create a user
        num = str(randint(2000, 2999))
        self.admin.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        self.admin.driver.find_element(
            By.XPATH, '//a[contains(text(),"Create user")]').click()
        self.admin.wait.until(
            expect.element_to_be_clickable((By.ID, 'user_username'))
        ).click()
        self.admin.driver.find_element(
            By.ID, 'user_username').send_keys('automated_test_user_'+num)
        self.admin.driver.find_element(
            By.ID, 'user_password').send_keys('password')
        self.admin.driver.find_element(
            By.ID, 'user_first_name').send_keys('first_name_'+num)
        self.admin.driver.find_element(
            By.ID, 'user_last_name').send_keys('last_name_'+num)
        self.admin.driver.find_element(
            By.XPATH, '//input[@value="Save"]').click()
        # search for that user
        self.admin.wait.until(
            expect.element_to_be_clickable((By.ID, 'query'))
        ).send_keys('automated_test_user_'+num)
        self.admin.driver.find_element(
            By.XPATH, '//input[@value="Search"]').click()
        # edit user
        self.admin.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(text(),"Edit")]')
            )
        ).click()
        self.admin.driver.find_element(
            By.ID, 'user_content_analyst').click()
        self.admin.driver.find_element(
            By.XPATH, '//input[@value="Save"]').click()
        # search for user to make sure they were updated
        self.admin.wait.until(
            expect.element_to_be_clickable((By.ID, 'query'))
        ).send_keys('automated_test_user_'+num)
        self.admin.driver.find_element(
            By.XPATH, '//input[@value="Search"]').click()
        element = self.admin.driver.find_element(By.XPATH, '//tr/td[5]')
        assert(element.get_attribute('innerHTML') == 'Yes'), \
            'permission not elevated ' + element.get_attribute('innerHTML')

        self.ps.test_updates['passed'] = True

    # Case C8252 - 006 - Admin | Remove elevated permissions
    @pytest.mark.skipif(str(8252) not in TESTS, reason='Excluded')
    def test_admin_remove_elevated_permissions_8252(self):
        """Remove elevated permissions.

        Steps:
        Create a user to edit
        Enter the user's name into the search here text box
        Click on the 'Search' button
        Click on the 'Edit' button next to the user
        If check box for chosen permission is checked, click to uncheck it.
        Click on the 'Save' button

        Expected Result:
        User is taken back to the User screen.
        The chosen account's permissions are modified.
        """
        self.ps.test_updates['name'] = 't1.37.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.37', 't1.37.006', '8252']
        self.ps.test_updates['passed'] = False

        # create a user
        num = str(randint(3000, 3999))
        self.admin.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        self.admin.driver.find_element(
            By.XPATH, '//a[contains(text(),"Create user")]').click()
        self.admin.wait.until(
            expect.element_to_be_clickable((By.ID, 'user_username'))
        ).click()
        self.admin.driver.find_element(
            By.ID, 'user_username').send_keys('automated_test_user_'+num)
        self.admin.driver.find_element(
            By.ID, 'user_password').send_keys('password')
        self.admin.driver.find_element(
            By.ID, 'user_first_name').send_keys('first_name_'+num)
        self.admin.driver.find_element(
            By.ID, 'user_last_name').send_keys('last_name_'+num)
        self.admin.driver.find_element(
            By.ID, 'user_content_analyst').click()
        self.admin.driver.find_element(
            By.XPATH, '//input[@value="Save"]').click()
        # search for that user
        self.admin.wait.until(
            expect.element_to_be_clickable((By.ID, 'query'))
        ).send_keys('automated_test_user_'+num)
        self.admin.driver.find_element(
            By.XPATH, '//input[@value="Search"]').click()
        element = self.admin.driver.find_element(By.XPATH, '//tr/td[5]')
        assert(element.get_attribute('innerHTML') == 'Yes'), \
            'permission not elevated ' + element.get_attribute('innerHTML')
        # edit user
        self.admin.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(text(),"Edit")]')
            )
        ).click()
        self.admin.driver.find_element(
            By.ID, 'user_content_analyst').click()
        self.admin.driver.find_element(
            By.XPATH, '//input[@value="Save"]').click()
        # search for user to make sure they were updated
        self.admin.wait.until(
            expect.element_to_be_clickable((By.ID, 'query'))
        ).send_keys('automated_test_user_'+num)
        self.admin.driver.find_element(
            By.XPATH, '//input[@value="Search"]').click()
        element = self.admin.driver.find_element(By.XPATH, '//tr/td[5]')
        assert(element.get_attribute('innerHTML') == 'No'), \
            'permission not elevated ' + element.get_attribute('innerHTML')

        self.ps.test_updates['passed'] = True

    # Case C8253 - 007 - Admin | Impersonate a user
    @pytest.mark.skipif(str(8253) not in TESTS, reason='Excluded')
    def test_admin_impersonate_a_user_8253(self):
        """Impersonate a user.

        Steps:
        Click on the 'Sign in as' button next to a user

        Expected Result:
        Signs in as chosen chosen user.
        Goes to chosen users initial screen after login
        (different depending on the user)
        """
        self.ps.test_updates['name'] = 't1.37.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.37', 't1.37.007', '8253']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.driver.find_element(By.ID, 'query').send_keys('student01')
        self.admin.driver.find_element(
            By.XPATH, '//input[@value="Search"]').click()
        self.admin.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(text(),"Sign in as")]')
            )
        ).click()
        self.admin.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//span[contains(text(),"Atticus Finch")]')
            )
        )

        self.ps.test_updates['passed'] = True
