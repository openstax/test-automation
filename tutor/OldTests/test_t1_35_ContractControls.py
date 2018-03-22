"""Tutor v1, Epic 35 - Contract Controls."""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
# from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

from staxing.helper import Admin

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': 'latest',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
LOCAL_RUN = os.getenv('LOCALRUN', 'false').lower() == 'true'
TESTS = os.getenv(
    'CASELIST',
    str([
        8228, 8230, 8231, 8232, 8233,
        8234, 8235, 8236, 8237
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestContractControls(unittest.TestCase):
    """T1.35 - Contract Controls."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        if not LOCAL_RUN:
            self.admin = Admin(
                use_env_vars=True,
                pasta_user=self.ps,
                capabilities=self.desired_capabilities
            )
        else:
            self.admin = Admin(
                use_env_vars=True,
            )
        self.admin.login()
        # make sure there are no new terms to accept
        try:
            self.admin.driver.find_element(
                By.ID, 'i_agree'
            ).click()
        except NoSuchElementException:
            pass
        try:
            self.admin.driver.find_element(
                By.ID, 'agreement_submit'
            ).click()
        except NoSuchElementException:
            pass
        # go to admin console
        self.wait = WebDriverWait(self.admin.driver, 15)
        self.admin.open_user_menu()
        self.admin.wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Admin')
            )
        ).click()
        self.admin.page.wait_for_page_load()
        self.admin.driver.find_element(
            By.XPATH, '//a[contains(text(),"Legal")]').click()

    def tearDown(self):
        """Test destructor."""
        if not LOCAL_RUN:
            self.ps.update_job(
                job_id=str(self.admin.driver.session_id),
                **self.ps.test_updates
            )
        try:
            self.admin.delete()
        except:
            pass

    # Case C8228 - 001 - Admin | Add a new contract
    @pytest.mark.skipif(str(8228) not in TESTS, reason='Excluded')
    def test_admin_add_a_new_contract_8228(self):
        """Add a new contract.

        Steps:
        Click on the 'Terms' option
        Click on the "New Contract" Link
        Enter information into the Name, Title, and Content text boxes
        Click on the 'Create contract' button

        Expected Result:
        Contract is created as a draft.
        User is shown the contract they just made,
        and has options on what to do with it next
        """
        self.ps.test_updates['name'] = 't1.35.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.35', 't1.35.001', '8228']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(text(),"Terms")]')
            )
        ).click()
        self.admin.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"links")]/a[text()="New Contract"]').click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//h1[text()="New Contract"]')
            )
        ).click()
        self.admin.driver.find_element(
            By.ID, 'contract_name').send_keys('test_contract_name_001')
        self.admin.driver.find_element(
            By.ID, 'contract_title').send_keys('test_contract_title_001')
        self.admin.driver.find_element(
            By.ID, 'contract_content').send_keys('test_contract_content_001')
        self.admin.driver.find_element(
            By.XPATH, '//input[@value="Create contract"]').click()
        self.admin.driver.find_element(
            By.XPATH, '//h1[contains(text(),"Details")]').click()

        self.ps.test_updates['passed'] = True

    '''
    # Case C8229 - 002 - Admin | Cancel adding a new contract
    @pytest.mark.skipif(str(8229) not in TESTS, reason='Excluded')
    def test_admin_cancel_adding_a_new_contract_8229(self):
        """Cancel adding a new contract.

        Steps:
        Click on the 'Terms' option
        Click on the "New Contract" Link
        Enter information into the Name, Title, and Content text boxes
        Click on the 'Create contract' button
        Click on the Delete link

        Expected Result:
        Contract is deleted. User is taken back to the Contracts page.
        """
        self.ps.test_updates['name'] = 't1.35.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.35', 't1.35.002', '8229']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(text(),"Terms")]')
            )
        ).click()
        self.admin.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"links")]/a[text()="New Contract"]').click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//h1[text()="New Contract"]')
            )
        ).click()
        self.admin.driver.find_element(
            By.ID, 'contract_name').send_keys('test_contract_name_002')
        self.admin.driver.find_element(
            By.ID, 'contract_title').send_keys('test_contract_title_002')
        self.admin.driver.find_element(
            By.ID, 'contract_content').send_keys('test_contract_content_002')
        self.admin.driver.find_element(
            By.XPATH, '//input[@value="Create contract"]').click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[text()="Delete"]')
            )
        ).click()
        self.admin.driver.find_element(
            By.XPATH, '//div[contains(@class,"alert-info")]')
        contracts = self.admin.driver.find_elements(
            By.XPATH, '//a[contains(text(),"test_contract_title_002")]')
        assert(len(contracts) == 0), 'contract not cancled'

        self.ps.test_updates['passed'] = True
    '''

    # Case C8230 - 003 - Admin | Publish a draft contract
    @pytest.mark.skipif(str(8230) not in TESTS, reason='Excluded')
    def test_admin_publish_a_draft_contract_8230(self):
        """Publish a draft contract.

        Steps:
        Click on the 'Terms' option
        Create a draft contract and return to contract list
        Click on the draft contract
        Click on the Publish link
        Click ok

        Expected Result:
        Draft contract is published
        """
        self.ps.test_updates['name'] = 't1.35.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.35', 't1.35.003', '8230']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(text(),"Terms")]')
            )
        ).click()
        self.admin.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"links")]/a[text()="New Contract"]').click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//h1[text()="New Contract"]')
            )
        ).click()
        self.admin.driver.find_element(
            By.ID, 'contract_name').send_keys('test_contract_name_003')
        self.admin.driver.find_element(
            By.ID, 'contract_title').send_keys('test_contract_title_003')
        self.admin.driver.find_element(
            By.ID, 'contract_content').send_keys('test_contract_content_003')
        self.admin.driver.find_element(
            By.XPATH, '//input[@value="Create contract"]').click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[text()="List"]')
            )
        ).click()
        self.admin.driver.find_element(
            By.XPATH,
            '//li//a[contains(text(),"test_contract_title_003")]').click()
        self.admin.driver.find_element(
            By.XPATH, '//a[contains(text(),"Publish")]').click()
        try:
            WebDriverWait(self.admin.driver, 3). \
                until(
                    expect.alert_is_present(),
                    'Timed out waiting for alert.'
                )
            alert = self.admin.driver.switch_to_alert()
            alert.accept()
            print('alert accepted')
        except TimeoutException:
            print('no alert')

        self.ps.test_updates['passed'] = True

    # Case C8231 - 004 - Admin | Delete a draft contract
    @pytest.mark.skipif(str(8231) not in TESTS, reason='Excluded')
    def test_admin_delete_a_draft_contract_8231(self):
        """Delete a draft contract.

        Steps:
        Click on the 'Terms' option
        Create a draft contract and return to the contract list
        Click on the draft contract
        Click on Delete next to chosen draft contract

        Expected Result:
        Draft contract is deleted
        """
        self.ps.test_updates['name'] = 't1.35.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.35', 't1.35.004', '8231']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(text(),"Terms")]')
            )
        ).click()
        contracts_original = self.admin.driver.find_elements(
            By.XPATH, '//a[contains(text(),"test_contract_title_004")]')

        self.admin.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"links")]/a[text()="New Contract"]').click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//h1[text()="New Contract"]')
            )
        ).click()
        self.admin.driver.find_element(
            By.ID, 'contract_name').send_keys('test_contract_name_004')
        self.admin.driver.find_element(
            By.ID, 'contract_title').send_keys('test_contract_title_004')
        self.admin.driver.find_element(
            By.ID, 'contract_content').send_keys('test_contract_content_004')
        self.admin.driver.find_element(
            By.XPATH, '//input[@value="Create contract"]').click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[text()="List"]')
            )
        ).click()
        self.admin.driver.find_element(
            By.XPATH,
            '//li//a[contains(text(),"test_contract_title_004")]').click()
        self.admin.page.wait_for_page_load()
        self.admin.sleep(2)
        self.admin.driver.find_element(
            By.XPATH, '//a[contains(text(),"Delete")]').click()
        self.admin.sleep(2)
        try:
            WebDriverWait(self.admin.driver, 3). \
                until(
                    expect.alert_is_present(),
                    'Timed out waiting for alert.'
                )
            alert = self.admin.driver.switch_to_alert()
            alert.accept()
            print('alert accepted')
        except TimeoutException:
            print('no alert')
        self.admin.page.wait_for_page_load()
        contracts = self.admin.driver.find_elements(
            By.XPATH, '//a[contains(text(),"test_contract_title_004")]')
        self.admin.page.wait_for_page_load()
        assert(len(contracts) == len(contracts_original)), \
            'contract not deleted'

        self.ps.test_updates['passed'] = True

    # Case C8232 - 005 - Admin | View a current contract
    @pytest.mark.skipif(str(8232) not in TESTS, reason='Excluded')
    def test_admin_view_a_current_contract_8232(self):
        """View a current contract.

        Steps:
        Click on the 'Terms' option
        Create a contract and then return to contract list
        Click on chosen contract

        Expected Result:
        Displays the information of chosen contract.
        """
        self.ps.test_updates['name'] = 't1.35.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.35', 't1.35.005', '8232']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(text(),"Terms")]')
            )
        ).click()
        self.admin.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"links")]/a[text()="New Contract"]').click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//h1[text()="New Contract"]')
            )
        ).click()
        self.admin.driver.find_element(
            By.ID, 'contract_name').send_keys('test_contract_name_005')
        self.admin.driver.find_element(
            By.ID, 'contract_title').send_keys('test_contract_title_005')
        self.admin.driver.find_element(
            By.ID, 'contract_content').send_keys('test_contract_content_005')
        self.admin.driver.find_element(
            By.XPATH, '//input[@value="Create contract"]').click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[text()="List"]')
            )
        ).click()
        self.admin.driver.find_element(
            By.XPATH,
            '//li//a[contains(text(),"test_contract_title_005")]').click()
        self.admin.driver.find_element(
            By.XPATH, '//h2[contains(text(),"test_contract_title_005")]')

        self.ps.test_updates['passed'] = True

    # Case C8233 - 006 - Admin | Add a new version of a current contract
    @pytest.mark.skipif(str(8233) not in TESTS, reason='Excluded')
    def test_admin_add_a_new_version_of_a_current_contract_8233(self):
        """Add a new version of a current contract.

        Steps:
        Click on the 'Terms' option
        Click on New version next to chosen contract
        Update information in the Name, Title, and Content text boxes.
        Click on the 'Create Contract' button

        Expected Result:
        New version of contract is saved as a draft.
        """
        self.ps.test_updates['name'] = 't1.35.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.35', 't1.35.006', '8233']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(text(),"Terms")]')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[text()="New Version"]')
            )
        ).click()
        self.admin.driver.find_element(
            By.ID, 'contract_name').send_keys('NEW_006')
        self.admin.driver.find_element(
            By.ID, 'contract_title').send_keys('NEW_006')
        self.admin.driver.find_element(
            By.ID, 'contract_content').send_keys('NEW_006')
        self.admin.driver.find_element(
            By.XPATH, '//input[@value="Create contract"]').click()
        self.admin.driver.find_element(
            By.XPATH, '//h2[contains(text(),"NEW_006")]')

        self.ps.test_updates['passed'] = True

    # Case C8234 - 007 - Admin | View a contract's signatories
    @pytest.mark.skipif(str(8234) not in TESTS, reason='Excluded')
    def test_admin_view_a_contracts_signatures_8234(self):
        """View a contract's signatories.

        Steps:
        Click on the 'Terms' option
        Click on Signatures next to chosen draft contract

        Expected Result:
        Displays list of signatures for the chosen contract.
        """
        self.ps.test_updates['name'] = 't1.35.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.35', 't1.35.007', '8234']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(text(),"Terms")]')
            )
        ).click()
        wait = WebDriverWait(self.admin.driver, 45)
        self.admin.driver.find_element(
            By.XPATH, '//a[text()="Signatures"]').click()
        wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//div[contains(@class,"signature_index")]')
            )
        )

        self.ps.test_updates['passed'] = True

    # Case C8235 - 008 - Admin | Terminate a signatory's contract
    @pytest.mark.skipif(str(8235) not in TESTS, reason='Excluded')
    def test_admin_terminate_a_signnatorys_contract_8235(self):
        """Terminate a signatory's contract.

        Steps:
        Click on the 'Terms' option
        Click on Signatures next to chosen draft contract
        Click on Terminate next to chosen user
        Click on the 'ok' button

        Expected Result:
        Selected user's signing of contract is terminated.
        """
        self.ps.test_updates['name'] = 't1.35.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.35', 't1.35.008', '8235']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(text(),"Terms")]')
            )
        ).click()
        self.admin.driver.find_element(
            By.XPATH, '//a[text()="Signatures"]').click()
        # is it okay to just terminate some random person's signature
        wait = WebDriverWait(self.admin.driver, 45)
        wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//td//a[contains(text(),"Terminate")]')
            )
        ).click()
        try:
            WebDriverWait(self.admin.driver, 3). \
                until(expect.alert_is_present(),
                      'Timed out waiting for PA creation ' +
                      'confirmation popup to appear.')
            alert = self.admin.driver.switch_to_alert()
            alert.accept()
            print('alert accepted')
        except TimeoutException:
            print('no alert')

        self.ps.test_updates['passed'] = True

    # Case C8236 - 009 - Admin | Add a targeted contract
    @pytest.mark.skipif(str(8236) not in TESTS, reason='Excluded')
    def test_admin_add_a_targeted_contract_8236(self):
        """Add a targeted contract.

        Steps:
        Click on the 'Targeted Contracts' option
        Click on the 'Add Target Contract' button
        Click the 'Submit' button

        Expected Result:
        User taken back to Targeted contracts page.
        New Targeted Contract is added
        """
        self.ps.test_updates['name'] = 't1.35.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.35', 't1.35.009', '8236']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(text(),"Targeted Contracts")]')
            )
        ).click()
        orig_contracts = self.admin.driver.find_elements(By.XPATH, '//tr')
        self.admin.driver.find_element(
            By.XPATH, '//a[text()="Add Targeted Contract"]').click()
        self.admin.driver.find_element(
            By.XPATH, '//input[@value="Submit"]').click()
        end_contracts = self.admin.driver.find_elements(By.XPATH, '//tr')
        assert(len(orig_contracts) == len(end_contracts)-1), \
            'targeted contract not added'

        self.ps.test_updates['passed'] = True

    # Case C8237 - 010 - Admin | Delete a targeted contract
    @pytest.mark.skipif(str(8237) not in TESTS, reason='Excluded')
    def test_admin_delete_a_targeted_contract_8237(self):
        """Delete a targeted contract.

        Steps:
        Click on the user's name in the top right corner to open drop down menu
        Click on the 'Admin' option of the drop down menu
        Click on 'Legal' on the bar across the top to open drop down menu
        Click on the 'Targeted Contracts' option
        Create a targeted contract and return to the list of targed contracts
        Click on delete next to chosen contract
        Click on the 'ok' button

        Expected Result:
        Targeted contract is deleted
        """
        self.ps.test_updates['name'] = 't1.35.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.35', 't1.35.010', '8237']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(text(),"Targeted Contracts")]')
            )
        ).click()
        orig_contracts = self.admin.driver.find_elements(By.XPATH, '//tr')
        # create contract
        self.admin.driver.find_element(
            By.XPATH, '//a[text()="Add Targeted Contract"]').click()
        self.admin.driver.find_element(
            By.XPATH, '//input[@value="Submit"]').click()
        # delete contract
        deletes = self.admin.driver.find_elements(
            By.XPATH, '//a[contains(text(),"delete")]')
        deletes[-1].click()
        try:
            WebDriverWait(self.admin.driver, 3).until(
                expect.alert_is_present(),
                'Timed out waiting for alert.'
            )
            alert = self.admin.driver.switch_to_alert()
            alert.accept()
            print('alert accepted')
        except TimeoutException:
            print('no alert')

        end_contracts = self.admin.driver.find_elements(By.XPATH, '//tr')
        assert(len(orig_contracts) == len(end_contracts)), \
            'targeted contract not added'

        self.ps.test_updates['passed'] = True

    '''
    # Case C8389 - 011 - Admin | Edit a draft contract
    @pytest.mark.skipif(str(8389) not in TESTS, reason='Excluded')
    def test_admin_edit_a_draft_contract_8389(self):
        """Edit a draft contract.

        Steps:
        Click on the 'Terms' option
        Create a new contract and return to list of contracts
        Click on Edit next to chosen draft contract
        Enter new information into the Name, Title, and Content text boxes
        Click on the 'Update Contract' button

        Expected Result:
        User is taken to Details page for selected contract.
        """
        self.ps.test_updates['name'] = 't1.35.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.35', 't1.35.011', '8389']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(text(),"Terms")]')
            )
        ).click()
        self.admin.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"links")]/a[text()="New Contract"]').click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//h1[text()="New Contract"]')
            )
        ).click()
        self.admin.driver.find_element(
            By.ID, 'contract_name').send_keys('test_contract_name_011')
        self.admin.driver.find_element(
            By.ID, 'contract_title').send_keys('test_contract_title_011')
        self.admin.driver.find_element(
            By.ID, 'contract_content').send_keys('test_contract_content_011')
        self.admin.driver.find_element(
            By.XPATH, '//input[@value="Create contract"]').click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[text()="List"]')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//li//a[contains(text(),"test_contract_title_011")]')
            )
        ).click()
        self.admin.sleep(1)
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//a[text()="Edit"]')
            )
        ).click()
        self.admin.sleep(1)
        self.admin.driver.find_element(
            By.ID, 'contract_name').send_keys('_New')
        self.admin.driver.find_element(
            By.ID, 'contract_title').send_keys('_New')
        self.admin.driver.find_element(
            By.ID, 'contract_content').send_keys('_New')
        self.admin.driver.find_element(
            By.XPATH, '//input[@value="Update contract"]').click()
        self.admin.sleep(1)
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//h2[contains(text(),"test_contract_title_011_New")]')
            )
        )
        self.ps.test_updates['passed'] = True
    '''
