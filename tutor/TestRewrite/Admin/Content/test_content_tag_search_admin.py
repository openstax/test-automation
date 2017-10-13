"""
System: ??
Subsystem: Content Tag Search
User: Admin
Testrail ID: C148100

Jacob Diaz
7/26/17


Corresponding Case(s):
t1.58.19 --> 20

Progress:
Still in revision. element selections needs to be added
and script tested for completion

Work to be done/Questions:
element selections needs to be added
and script tested for completion

Merge-able with any scripts? If so, which? :


"""

# import inspect
import json
import os
# import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
# from random import randint
from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as expect
from staxing.assignment import Assignment
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Admin
from staxing.helper import ContentQA

# for template command line testing only
# - replace list_of_cases on line 31 with all test case IDs in this file
# - replace CaseID on line 52 with the actual cass ID
# - delete lines 17 - 22
list_of_cases = None
CaseID = 'skip'

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

    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestManageEcosystems(unittest.TestCase):

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
            self.content = ContentQA(
                existing_driver=self.admin.driver,
                use_env_vars=True,
                pasta_user=self.ps,
                capabilities=self.desired_capabilities
            )
        else:
            self.admin = Admin(
                use_env_vars=True
            )
            self.content = ContentQA(
                use_env_vars=True,
                existing_driver=self.admin.driver
            )
        self.wait = WebDriverWait(self.admin.driver, Assignment.WAIT_TIME)
        self.admin.login()
        self.wait.sleep(2)
        self.admin.goto_admin_control()

    def tearDown(self):
        """Test destructor."""
        if not LOCAL_RUN:
            self.ps.update_job(
                job_id=str(self.admin.driver.session_id),
                **self.ps.test_updates
            )
        try:
            self.admin.delete()
            # self.content.delete()
        except:
            pass

    def test_content_tag_search_admin(self):
        """
        Go to https://tutor-qa.openstax.org/
        Login to admin account
        Open the drop down menu by clicking on the user menu link containing
        the user's name
        Click on the 'Admin' button
        Open the drop down menu by clicking 'Content'
        Click the 'Tags' button
        Enter text into the text box with 'Search here'
        Click the 'Search' button
        ***Results of the search are returned.(t1.58.19)***

        Click the 'Edit' button for one of the returned tags
        Edit the text box labeled 'Name'
        Edit the text box labeled 'Description'
        Click the 'Save' button
        ***The user is returned to the Tags page and the text 'The tag has been
        updated.' is displayed. (t1.58.20)***
        :return:

        CORRESPONDS TO:
        t1.58.19,20
        """
        # t1.58.19 --> Results of the search are returned.
        content_dropdown = "//a[contains(@class,'dropdown-toggle') and " + \
                           "contains(text(),'Content')]"
        content_ecosystems = "//a[contains(text(),'Tags')]"

        search_term = "bio"
        search_btn = "//input[contains(@value,'Search')]"

        # (t1.58.20) --> The user is returned to the Tags page and the text
        # 'The tag has been updated.' is displayed.

        edit = "//a[contains(@edit,'Edit')]"

        # NEED CODE FOR ACTUALLY FILLING IN TEXTBOXES
        print(content_dropdown, content_ecosystems, search_term, search_btn)
        print(edit)

        self.admin.find(
            By.XPATH,
            "//div[contains(@class,'alert-info')]"
        )

        self.admin.find(
            By.XPATH,
            "//div[contains(@class,'alert-info')]" +
            "//*[contains(text(),'The tag has been updated')]"
        )
