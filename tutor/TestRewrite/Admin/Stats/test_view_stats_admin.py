
"""
Title: test_view_stats
User(s): admin
Testrail ID: C148075

Jacob Diaz
7/26/17


Corresponding Case(s):
t2.07.01

Progress:
Some

Work to be done/Questions:
Test, make sure it works

Merge-able with any scripts? If so, which?:
Other admin scripts?

"""

# import inspect
import json
import os
# import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
# from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
# from staxing.assignment import Assignment

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Admin, Teacher

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
        14651, 14657, 14850, 14660, 116648
        # not implemented
        # 14658, 14661
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestImproveCourseManagement(unittest.TestCase):
    """T2.07 - Improve Course Management."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.teacher = Teacher(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        self.admin = Admin(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities,
            existing_driver=self.teacher.driver
        )

    def tearDown(self):
        """Test destructor."""
        if not LOCAL_RUN:
            self.ps.update_job(
                job_id=str(self.teacher.driver.session_id),
                **self.ps.test_updates
            )
        self.admin = None
        try:
            self.teacher.delete()
        except:
            pass

    def test_view_stats_admin(self):
        """
        Log in as Admin
        Click on User Menu for drop-down
        Click on 'Admin' on user menu
        Click "Stats"
        Click "Concept Coach"
        ***The user is presented with Concept Coach Statistics (t2.07.01)***

        Corresponds to...
        t2.07.01
        :return:
        """
        # t2.07.01 --> The user is presented with Concept Coach Statistics
        self.admin.login()
        self.admin.goto_admin_control()
        self.admin.sleep(5)
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Stats')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Concept Coach')
            )
        ).click()

        assert ('/stats/concept_coach' in self.admin.current_url()), \
            'Not viewing Concept Coach stats'
