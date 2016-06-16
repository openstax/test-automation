"""Concept Coach v1, Epic 3 - Content Preparation and Import."""

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
from staxing.helper import Admin, ContentQA  # NOQA

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': '50.0',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([7603, 7604, 7962, 7963, 7964,
         7965, 7966, 7967, 7968, 7969])  # NOQA
)


@PastaDecorator.on_platforms(BROWSERS)
class TestEpicName(unittest.TestCase):
    """CC1.03 - Content Preparation and Import."""

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

    # Case C7603 - 001 - Content Analyst | Import content into Tutor
    @pytest.mark.skipif(str(7603) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Import content into Tutor.

        Steps: 

        Go to tutor-staging
        login as content
        Select Customer Analyst from the dropdown menu on the name
        Click on Ecosystems in the header
        Click "Download Manifest" for the desired course
        Scroll down and click Import a new Ecosystem button. 
        Click "Choose File" 
        Select the desired file
        In comment section add today's date and your name. Eg: 2016-03-03 Kajal
        Click on the button Import
        Now wait for at most 5 mins.

        Expected Result:

        The message "Ecosystem import job queued" appears at the top

        """
        self.ps.test_updates['name'] = 'cc1.03.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.03',
            'cc1.03.001',
            '7603'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C7604 - 002 - Admin | Import content into Tutor
    @pytest.mark.skipif(str(7604) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Import content into Tutor.

        Steps: 

        Select Customer Analyst from the dropdown menu on the name
        Click on Ecosystems in the header
        Click "Download Manifest" for the desired course
        Scroll down and click Import a new Ecosystem button. 
        Click "Choose File" 
        Select the desired file
        In comment section add today's date and your name. Eg: 2016-03-03 Kajal
        Click on the button Import
        Now wait for at most 5 mins.

        Expected Result:

        The message "Ecosystem import job queued" appears at the top

        """
        self.ps.test_updates['name'] = 'cc1.03.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.03',
            'cc1.03.002',
            '7604'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C7962 - 003 - Content Analyst| Verify question availability for CC-Derived Biology
    @pytest.mark.skipif(str(7962) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Verify question availability for CC-Derived Biology.

        Steps: 

        Click QA content 
        Click Available Books 
        Select CC-Derived Biology
        Click on a section in the table of contents

        Expected Result:

        Questions are available

        """
        self.ps.test_updates['name'] = 'cc1.03.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.03',
            'cc1.03.003',
            '7962'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C7963 - 004 - Content Analyst| Verify question availability for CC-Derived College Physics
    @pytest.mark.skipif(str(7963) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Verify question availability for CC-Derived College Physics.

        Steps: 
        
        Click QA content 
        Click Available Books 
        Select CC-Derived College Physics
        Click on a section in the table of contents


        Expected Result:

        Questions are available

        """
        self.ps.test_updates['name'] = 'cc1.03.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.03',
            'cc1.03.004',
            '7963'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C7964 - 005 - Content Analyst| Verify question availability for CC-Derived Concepts of Biology
    @pytest.mark.skipif(str(7964) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Verify question availability for CC-Derived Concepts of Biology.

        Steps: 
        
        Click QA content 
        Click Available Books 
        Select CC-Derived Concepts of Biology
        Click on a section in the table of contents


        Expected Result:

        Questions are available

        """
        self.ps.test_updates['name'] = 'cc1.03.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.03',
            'cc1.03.005',
            '7964'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C7965 - 006 - Content Analyst| Verify question availability for CC-Derived Anatomy & Physiology
    @pytest.mark.skipif(str(7965) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Verify question availability for CC-Derived Anatomy & Physiology.

        Steps: 
        
        Click QA content 
        Click Available Books 
        Select CC-Derived Anatomy and Physiology
        Click on a section in the table of contents


        Expected Result:

        Questions are available

        """
        self.ps.test_updates['name'] = 'cc1.03.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.03',
            'cc1.03.006',
            '7965'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C7966 - 007 - Content Analyst| Verify question availability for CC-Derived Macroeconomics
    @pytest.mark.skipif(str(7966) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Verify question availability for CC-Derived Macroeconomics.

        Steps: 
        
        Click QA content 
        Click Available Books 
        Select CC-Derived Macroeconomics
        Click on a section in the table of contents


        Expected Result:

        Questions are available

        """
        self.ps.test_updates['name'] = 'cc1.03.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.03',
            'cc1.03.007',
            '7966'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C7967 - 008 - Content Analyst| Verify question availability for CC-Derived Microeconomics
    @pytest.mark.skipif(str(7967) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Verify question availability for CC-Derived Microeconomics.

        Steps: 
        
        Click QA content 
        Click Available Books 
        Select CC-Derived Microeconomics
        Click on a section in the table of contents


        Expected Result:

        Questions are available

        """
        self.ps.test_updates['name'] = 'cc1.03.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.03',
            'cc1.03.008',
            '7967'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C7968 - 009 - Content Analyst| Verify question availability for CC-Derived Principles of Economics
    @pytest.mark.skipif(str(7968) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Verify question availability for CC-Derived Principles of Economics.

        Steps: 
        
        Click QA content 
        Click Available Books 
        Select CC-Derived Principles of Economics
        Click on a section in the table of contents


        Expected Result:

        Questions are available

        """
        self.ps.test_updates['name'] = 'cc1.03.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.03',
            'cc1.03.009',
            '7968'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True


    # Case C7969 - 010 - Content Analyst| Verify question availability for CC-Derived Introduction to Sociology
    @pytest.mark.skipif(str(7969) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        """Verify question availability for CC-Derived Introduction to Sociology.

        Steps: 
        
        Click QA content 
        Click Available Books 
        Select CC-Derived Introcution to Sociology
        Click on a section in the table of contents


        Expected Result:

        Questions are available

        """
        self.ps.test_updates['name'] = 'cc1.03.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.03',
            'cc1.03.010',
            '7969'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True
        

