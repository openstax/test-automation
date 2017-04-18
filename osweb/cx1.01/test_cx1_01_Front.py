"""CNX v1, Epic 01 - Front Page."""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
from selenium.webdriver.common.by import By
from staxing.helper import User


basic_test_env = json.dumps([
    {
        'platform': 'Windows 10',
        'browserName': 'chrome',
        'version': 'latest',
        'screenResolution': '1280x960',
    },
    {
        'platform': 'Windows 7',
        'browserName': 'firefox',
        'version': 'latest',
        'screenResolution': '1280x960',
    },
    {
        'platform': 'OS X 10.11',
        'browserName': 'safari',
        'version': 'latest',
        'screenResolution': '1280x960',
    },
])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([
        96869, 96870, 96871,  # 96872, 96873,
        # 96874, 96875, 96876, 96877, 96878,
        # 96879, 96880
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestFrontPage(unittest.TestCase):
    """CX1.01 - Front Page."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.user = User(
            username='',
            password='',
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        self.user.get('https://qa.cnx.org/')

    def tearDown(self):
        """Test destructor."""
        self.ps.update_job(
            job_id=str(self.user.driver.session_id),
            **self.ps.test_updates
        )
        try:
            self.user.delete()
        except:
            pass

    # Case C96869 - 001 - User | Support link visible
    @pytest.mark.skipif(str(96869) not in TESTS, reason='Excluded')
    def test_user_support_link_visible_96869(self):
        """See the support link.

        Steps:

        Expected Result:
        The user sees the support link.
        """
        self.ps.test_updates['name'] = 'cx1.01.001' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cx1', 'cx1.01', 'cx1.01.001', '96869']
        self.ps.test_updates['passed'] = False

        support = self.user.find(By.LINK_TEXT, 'Support')
        assert('openstax.force.com' in support.get_attribute('href')), \
            'Support link not seen'

        self.ps.test_updates['passed'] = True

    # Case C96870 - 002 - User | Salesforce support is available
    @pytest.mark.skipif(str(96870) not in TESTS, reason='Excluded')
    def test_user_salesforce_support_available_96870(self):
        """Open Salesforce support.

        Steps:
        Click on Support

        Expected Result:
        The user sees the support page.
        """
        self.ps.test_updates['name'] = 'cx1.01.002' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cx1', 'cx1.01', 'cx1.01.002', '96870']
        self.ps.test_updates['passed'] = False

        # primary_window = self.user.driver.window_handles[0]
        self.user.find(By.LINK_TEXT, 'Support').click()
        secondary_window = self.user.driver.window_handles[1]
        self.user.driver.switch_to_window(secondary_window)
        assert('CNX Help Center' in self.user.find(
                By.CSS_SELECTOR, 'center.landingHeader').text), \
            'Salesforce CNX support page not open'

        self.ps.test_updates['passed'] = True

    # Case C96871 - 003 - User | Heading links are visible
    @pytest.mark.skipif(str(96871) not in TESTS, reason='Excluded')
    def test_user_header_links_seen_96871(self):
        """See the support link.

        Steps:

        Expected Result:
        Header links are available (CNX, Search, About Us, Give, RICE)
        """
        self.ps.test_updates['name'] = 'cx1.01.003' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cx1', 'cx1.01', 'cx1.01.003', '96871']
        self.ps.test_updates['passed'] = False

        expected_links = ['Search', 'About Us', 'Give']

        nav_bar_brand = self.user.find(By.CSS_SELECTOR, 'a.navbar-brand')
        assert('OpenStax CNX' in nav_bar_brand.text), 'Brand image not seen'

        found_links = []
        nav_bar = self.user.find_all(By.CSS_SELECTOR, 'div#page-nav ul li a')
        for link in nav_bar[:-1]:
            found_links.append(link.text)
            assert(link.text in expected_links), \
                '"' + link.text + '" not expected'
        for link_name in expected_links:
            assert(link_name in found_links), '"' + link_name + '" not found'

        nav_bar_rice = nav_bar[-1].find_element(
            By.XPATH, './img[@class="rice"]')
        assert('Rice University' in nav_bar_rice.get_attribute('alt')), \
            'Rice brand not found'

        self.ps.test_updates['passed'] = True

    # Case C96872 - 004 - User | Legacy CNX link is visible
    @pytest.mark.skipif(str(96872) not in TESTS, reason='Excluded')
    def test_user_legacy_cnx_visible_96872(self):
        """See the support link.

        Steps:

        Expected Result:

        """
        self.ps.test_updates['name'] = 'cx1.01.001' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cx1', 'cx1.01', 'cx1.01.001', '96872']
        self.ps.test_updates['passed'] = False

        # Test steps

        self.ps.test_updates['passed'] = True

    # Case C96873 - 005 - User | Legacy CNX available
    @pytest.mark.skipif(str(96873) not in TESTS, reason='Excluded')
    def test_user_legacy_cnx_available_96873(self):
        """See the support link.

        Steps:

        Expected Result:

        """
        self.ps.test_updates['name'] = 'cx1.01.005' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cx1', 'cx1.01', 'cx1.01.005', '96873']
        self.ps.test_updates['passed'] = False

        # Test steps

        self.ps.test_updates['passed'] = True

    # Case C96874 - 006 - User | All OS books are shown in the College section
    @pytest.mark.skipif(str(96874) not in TESTS, reason='Excluded')
    def test_user_all_os_books_in_college_section_96874(self):
        """See the support link.

        Steps:

        Expected Result:

        """
        self.ps.test_updates['name'] = 'cx1.01.006' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cx1', 'cx1.01', 'cx1.01.006', '96874']
        self.ps.test_updates['passed'] = False

        # Test steps

        self.ps.test_updates['passed'] = True

    # Case C96875 - 007 - User | Non-active books are shown in the CNX section
    @pytest.mark.skipif(str(96875) not in TESTS, reason='Excluded')
    def test_user_non_os_books_in_cnx_section_96875(self):
        """See the support link.

        Steps:

        Expected Result:

        """
        self.ps.test_updates['name'] = 'cx1.01.007' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cx1', 'cx1.01', 'cx1.01.007', '96875']
        self.ps.test_updates['passed'] = False

        # Test steps

        self.ps.test_updates['passed'] = True

    # Case C96876 - 008 - User | Books show part of the introduction
    @pytest.mark.skipif(str(96876) not in TESTS, reason='Excluded')
    def test_user_books_show_part_of_intro_96876(self):
        """See the support link.

        Steps:

        Expected Result:

        """
        self.ps.test_updates['name'] = 'cx1.01.008' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cx1', 'cx1.01', 'cx1.01.008', '96876']
        self.ps.test_updates['passed'] = False

        # Test steps

        self.ps.test_updates['passed'] = True

    # Case C96877 - 009 - User | Read More links to the book's Webview
    @pytest.mark.skipif(str(96877) not in TESTS, reason='Excluded')
    def test_user_read_more_links_to_books_webview_96877(self):
        """See the support link.

        Steps:

        Expected Result:

        """
        self.ps.test_updates['name'] = 'cx1.01.009' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cx1', 'cx1.01', 'cx1.01.009', '96877']
        self.ps.test_updates['passed'] = False

        # Test steps

        self.ps.test_updates['passed'] = True

    # Case C96878 - 010 - User | Book cover links to the book's Webview
    @pytest.mark.skipif(str(96878) not in TESTS, reason='Excluded')
    def test_user_book_cover_links_to_books_webview_96878(self):
        """See the support link.

        Steps:

        Expected Result:

        """
        self.ps.test_updates['name'] = 'cx1.01.010' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cx1', 'cx1.01', 'cx1.01.010', '96878']
        self.ps.test_updates['passed'] = False

        # Test steps

        self.ps.test_updates['passed'] = True

    # Case C96879 - 011 - User | Book title links to the book's Webview
    @pytest.mark.skipif(str(96879) not in TESTS, reason='Excluded')
    def test_user_book_title_links_to_books_webview_96879(self):
        """See the support link.

        Steps:

        Expected Result:

        """
        self.ps.test_updates['name'] = 'cx1.01.011' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cx1', 'cx1.01', 'cx1.01.011', '96879']
        self.ps.test_updates['passed'] = False

        # Test steps

        self.ps.test_updates['passed'] = True

    # Case C96880 - 012 - User | OpenStax CNX logo redirects to the front page
    @pytest.mark.skipif(str(96880) not in TESTS, reason='Excluded')
    def test_user_oscnx_logo_redirects_to_front_page_96880(self):
        """See the support link.

        Steps:

        Expected Result:

        """
        self.ps.test_updates['name'] = 'cx1.01.012' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['cx1', 'cx1.01', 'cx1.01.012', '96880']
        self.ps.test_updates['passed'] = False

        # Test steps

        self.ps.test_updates['passed'] = True
