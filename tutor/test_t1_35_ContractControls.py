"""Tutor v1, Epic 35 - Add a new contract."""

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

# for template command line testing only
# - replace list_of_cases on line 31 with all test case IDs in this file
# - replace CaseID on line 52 with the actual cass ID
# - delete lines 17 - 22
list_of_cases = 0
CaseID = 0

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': '50.0',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([8228, 8229, 8230, 8231,
         8232, 8233, 8234, 8235,
         8236, 8237, 8389])  # NOQA
)


@PastaDecorator.on_platforms(BROWSERS)
class TestEpicName(unittest.TestCase):
    """T1.35 - Contract Controls."""

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

    # Case C8228 - 001 - Admin | Add a new contract
    @pytest.mark.skipif(str(8228) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Add a new contract.

        Steps:

        Click on the user's name in the top right corner to open drop down menu
        Click on the 'Admin' option of the drop down menu
        Click on 'Legal' on the bar across the top to open another drop down menu
        Click on the 'Terms' option
        Click on the "New Contract" Link
        Enter information into the Name, Title, and Content text boxes
        Click on the 'Create contract' button


        Expected Result:

        Contract is created as a draft. 
        User is shown the contract they just made, and has options on what to do with it next

        """
        self.ps.test_updates['name'] = 't1.35.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.35',
            't1.35.001',
            '8228'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8229 - 002 - Admin | Cancel adding a new contract
    @pytest.mark.skipif(str(8229) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Cancel adding a new contract.

        Steps:

        Click on the user's name in the top right corner to open drop down menu
        Click on the 'Admin' option of the drop down menu
        Click on 'Legal' on the bar across the top to open another drop down menu
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
        self.ps.test_updates['tags'] = [
            't1',
            't1.35',
            't1.35.002',
            '8229'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8230 - 003 - Admin | Publish a draft contract
    @pytest.mark.skipif(str(8230) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Publish a draft contract.

        Steps:

        Click on the user's name in the top right corner to open drop down menu
        Click on the 'Admin' option of the drop down menu
        Click on 'Legal' on the bar across the top to open another drop down menu
        Click on the 'Terms' option
        Click on Publish next to chosen draft contract
        Click on the 'ok' button


        Expected Result:

        Draft contract is published

        """
        self.ps.test_updates['name'] = 't1.35.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.35',
            't1.35.003',
            '8230'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8231 - 004 - Admin | Delete a draft contract
    @pytest.mark.skipif(str(8231) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Delete a draft contract.

        Steps:

        Click on the user's name in the top right corner to open drop down menu
        Click on the 'Admin' option of the drop down menu
        Click on 'Legal' on the bar across the top to open another drop down menu
        Click on the 'Terms' option
        Click on Delete next to chosen draft contract
        Click on the 'ok' button


        Expected Result:

        Draft contract is deleted

        """
        self.ps.test_updates['name'] = 't1.35.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.35',
            't1.35.004',
            '8231'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8232 - 005 - Admin | View a current contract
    @pytest.mark.skipif(str(8232) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """View a current contract.

        Steps:

        Click on the user's name in the top right corner to open drop down menu
        Click on the 'Admin' option of the drop down menu
        Click on 'Legal' on the bar across the top to open another drop down menu
        Click on the 'Terms' option
        Click on chosen contract


        Expected Result:

        Displays the information of chosen contract.

        """
        self.ps.test_updates['name'] = 't1.35.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.35',
            't1.35.005',
            '8232'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8233 - 006 - Admin | Add a new version of a current contract
    @pytest.mark.skipif(str(8233) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Add a new version of a current contract.

        Steps:

        Click on the user's name in the top right corner to open drop down menu
        Click on the 'Admin' option of the drop down menu
        Click on 'Legal' on the bar across the top to open another drop down menu
        Click on the 'Terms' option
        Click on New version next to chosen contract
        Update information in the Name, Title, and Content text boxes.
        Click on the 'Create Contract' button


        Expected Result:

        New version of contract is saved as a draft.

        """
        self.ps.test_updates['name'] = 't1.35.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.35',
            't1.35.006',
            '8233'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8234 - 007 - Admin | View a contract's signatories
    @pytest.mark.skipif(str(8234) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """View a contract's signatories.

        Steps:

        Click on the user's name in the top right corner to open drop down menu
        Click on the 'Admin' option of the drop down menu
        Click on 'Legal' on the bar across the top to open another drop down menu
        Click on the 'Terms' option
        Click on Signatures next to chosen draft contract


        Expected Result:

        Displays list of signatures for the chosen contract.

        """
        self.ps.test_updates['name'] = 't1.35.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.35',
            't1.35.007',
            '8234'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8235 - 008 - Admin | Terminate a signatory's contract
    @pytest.mark.skipif(str(8235) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Terminate a signatory's contract.

        Steps:

        Click on the user's name in the top right corner to open drop down menu
        Click on the 'Admin' option of the drop down menu
        Click on 'Legal' on the bar across the top to open another drop down menu
        Click on the 'Terms' option
        Click on Signatures next to chosen draft contract
        Click on Terminate next to chosen user
        Click on the 'ok' button


        Expected Result:

        Selected user's signing of contract is terminated.

        """
        self.ps.test_updates['name'] = 't1.35.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.35',
            't1.35.008',
            '8235'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8236 - 009 - Admin | Add a targeted contract
    @pytest.mark.skipif(str(8236) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Add a targeted contract.

        Steps:

        Click on the user's name in the top right corner to open drop down menu
        Click on the 'Admin' option of the drop down menu
        Click on 'Legal' on the bar across the top to open another drop down menu
        Click on the 'Targeted Contracts' option
        Click on the 'Add Target Contract' button
        [optional] Select a contract name from the Contract name drop down menu
        [optional] Select a target from the target drop down menu
        [optional] Select a masked contract(s) from the Masked Contracts list
        [optional] click on the 'Is Proxy Signed?' or 'Can Shown Contents' check boxes
        Click the 'Submit' button

        Expected Result:

        User taken back to Targeted contracts page. 
        New Targeted Contract is added

        """
        self.ps.test_updates['name'] = 't1.35.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.35',
            't1.35.009',
            '8236'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8237 - 010 - Admin | Delete a targeted contract
    @pytest.mark.skipif(str(8237) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Delete a targetd contract.

        Steps:

        Click on the user's name in the top right corner to open drop down menu
        Click on the 'Admin' option of the drop down menu
        Click on 'Legal' on the bar across the top to open another drop down menu
        Click on the 'Targeted Contracts' option
        Click on delete next to chosen contract
        Click on the 'ok' button

        Expected Result:

        Targeted contract is deleted

        """
        self.ps.test_updates['name'] = 't1.35.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.35',
            't1.35.010',
            '8237'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C8389 - 011 - Admin | Edit a draft contract
    @pytest.mark.skipif(str(8389) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Edit a draft contract.

        Steps:

        Click on the user's name in the top right corner to open drop down menu
        Click on the 'Admin' option of the drop down menu
        Click on 'Legal' on the bar across the top to open another drop down menu
        Click on the 'Terms' option
        Click on Edit next to chosen draft contract
        Enter new information into the Name, Title, and Content text boxes
        Click on the 'Update Contract' button


        Expected Result:

        User is taken to Details page for selected contract.

        """
        self.ps.test_updates['name'] = 't1.35.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't1',
            't1.35',
            't1.35.011',
            '8389'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True
