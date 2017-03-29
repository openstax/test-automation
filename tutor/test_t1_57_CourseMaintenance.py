"""Tutor v1, Epic 57 - CourseMaintenance."""

import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
# from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
# from staxing.assignment import Assignment

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Admin, Student, Teacher


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
        8311, 8312, 8313, 8314, 8315,
        112519, 112520, 112521, 112522,
        112523
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestCourseMaintenance(unittest.TestCase):
    """T1.57 - Course Maintenance."""

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
        self.admin.goto_admin_control()
        self.admin.sleep(5)

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

    # Case C8311 - 001 - Admin | Import courses from Salesforece
    @pytest.mark.skipif(str(8311) not in TESTS, reason='Excluded')
    def test_admin_import_courses_from_salesforce_8311(self):
        """Import courses from Salesforce.

        Steps:
        Click on the user menu
        Click on the Admin option
        Click on Salesforce on the header
        Click on the Import Courses button

        Expected Result:

        """
        self.ps.test_updates['name'] = 't1.57.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.57', 't1.57.001', '8311']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C8312 - 002 - Admin | Update Salesforce Staistics
    @pytest.mark.skipif(str(8312) not in TESTS, reason='Excluded')
    def test_admin_update_salesforce_statistice_8312(self):
        """Update Salesforce statistics.

        Steps:
        Click on the user menu
        Click on the Admin option
        Click on Salesforce on the header
        Click on Update Salesforce

        Expected Result:

        """
        self.ps.test_updates['name'] = 't1.57.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.57', 't1.57.002', '8312']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C8313 - 003 - Admin | Exclude assesments from all courses
    @pytest.mark.skipif(str(8313) not in TESTS, reason='Excluded')
    def test_admin_exclude_assesments_from_all_courses_8313(self):
        """Exclude assesments from all courses.

        Steps:

        Expected Result:
        """
        self.ps.test_updates['name'] = 't1.57.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.57', 't1.57.003', '8313']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C8314 - 004 - Admin | Add a system notification
    @pytest.mark.skipif(str(8314) not in TESTS, reason='Excluded')
    def test_admin_add_a_system_notification_8314(self):
        """Add a system notification.

        Steps:
        Click on the user menu
        Click on the Admin option
        Click on System Setting on the header
        Click on the Notifications option
        Enter a notification into the New Notification text box
        Click on the Add button

        Expected Result:
        A system notification is added
        """
        self.ps.test_updates['name'] = 't1.57.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.57', 't1.57.004', '8314']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'System Setting')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Notifications')
            )
        ).click()
        self.admin.sleep(5)

        self.admin.find(By.XPATH, "//input[@id='new_message']").send_keys(
            'automated test')

        self.admin.find(By.XPATH, "//input[@class='btn btn-default']").click()

        self.admin.sleep(5)

        notif = self.admin.driver.find_elements_by_xpath(
            "//div[@class='col-xs-12']")

        for index, n in enumerate(notif):
            if n.text.find('automated test') >= 0:
                self.admin.driver.find_elements_by_xpath(
                    "//a[@class='btn btn-warning']")[index].click()
                self.admin.driver.switch_to_alert().accept()
                self.ps.test_updates['passed'] = True
                break

    # Case C8315 - 005 - Admin | Delete a system notification
    @pytest.mark.skipif(str(8315) not in TESTS, reason='Excluded')
    def test_admin_delete_a_system_notification_8315(self):
        """Delete a system notification.

        Steps:
        Click on the user menu
        Click on the Admin option
        Click on System Setting on the header
        Click on the Notifications option
        Click on the Remove button next to a notification
        Click OK on the dialouge box

        Expected Result:
        A system notification is deleted
        """
        self.ps.test_updates['name'] = 't1.57.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.57', 't1.57.005', '8315']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'System Setting')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Notifications')
            )
        ).click()
        self.admin.sleep(5)

        self.admin.find(By.XPATH, "//input[@id='new_message']").send_keys(
            'automated test')

        self.admin.find(By.XPATH, "//input[@class='btn btn-default']").click()

        self.admin.sleep(5)

        notif = self.admin.driver.find_elements_by_xpath(
            "//div[@class='col-xs-12']")

        for index, n in enumerate(notif):
            if n.text.find('automated test') >= 0:
                self.admin.driver.find_elements_by_xpath(
                    "//a[@class='btn btn-warning']")[index].click()
                self.admin.driver.switch_to_alert().accept()
                break

        deleted = True

        notif = self.admin.driver.find_elements_by_xpath(
            "//div[@class='col-xs-12']")

        for n in notif:
            if n.text.find('automated test') >= 0:
                deleted = False
                break

        if deleted:
            self.ps.test_updates['passed'] = True

    # Case C112519 - 006 - Admin | Add an instructor-only system notification
    @pytest.mark.skipif(str(112519) not in TESTS, reason='Excluded')
    def test_admin_add_instructor_notification_112519(self):
        """Add an instructor-only system notification.

        Steps:

        Expected Result:

        """
        self.ps.test_updates['name'] = 't1.57.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.57', 't1.57.006', '112519']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'System Setting')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Notifications')
            )
        ).click()
        self.admin.sleep(5)

        self.admin.find(By.XPATH, "//div[3]//input[@id='message']").send_keys(
            'automated test')

        self.admin.driver.find_elements_by_xpath(
            "//input[@class='btn btn-default']")[1].click()

        self.admin.sleep(5)

        notif = self.admin.driver.find_elements_by_xpath(
            "//div[@class='col-xs-12']")

        for index, n in enumerate(notif):
            if n.text.find('automated test') >= 0:
                self.admin.driver.find_elements_by_xpath(
                    "//a[@class='btn btn-warning']")[index].click()
                self.admin.driver.switch_to_alert().accept()
                self.ps.test_updates['passed'] = True
                break

        self.admin.sleep(5)

        self.ps.test_updates['passed'] = True

    # Case C112520 - 007 - Admin | Delete a instructor-only system notification
    @pytest.mark.skipif(str(112520) not in TESTS, reason='Excluded')
    def test_admin_delete_instructor_notification_112520(self):
        """Delete an instructor-only system notification.

        Steps:

        Expected Result:

        """
        self.ps.test_updates['name'] = 't1.57.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.57', 't1.57.007', '112520']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'System Setting')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Notifications')
            )
        ).click()
        self.admin.sleep(5)

        self.admin.find(By.XPATH, "//div[3]//input[@id='message']").send_keys(
            'automated test')

        self.admin.driver.find_elements_by_xpath(
            "//input[@class='btn btn-default']")[1].click()

        self.admin.sleep(5)

        notif = self.admin.driver.find_elements_by_xpath(
            "//div[@class='col-xs-12']")

        for index, n in enumerate(notif):
            if n.text.find('automated test') >= 0:
                self.admin.driver.find_elements_by_xpath(
                    "//a[@class='btn btn-warning']")[index].click()
                self.admin.driver.switch_to_alert().accept()
                self.ps.test_updates['passed'] = True
                break

        self.admin.sleep(5)

        deleted = True

        notif = self.admin.driver.find_elements_by_xpath(
            "//div[@class='col-xs-12']")

        for n in notif:
            if n.text.find('automated test') >= 0:
                deleted = False
                break

        assert(deleted), 'notification not deleted'

        self.ps.test_updates['passed'] = True

    # Case C112521 - 008 - Student | View an active system notification
    @pytest.mark.skipif(str(112521) not in TESTS, reason='Excluded')
    def test_student_view_active_notification_112521(self):
        """View an active system notification.

        Steps:

        Expected Result: //div[@class='notification system']/span

        """
        self.ps.test_updates['name'] = 't1.57.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.57', 't1.57.008', '112521']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        # Create notification
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'System Setting')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Notifications')
            )
        ).click()
        self.admin.sleep(5)

        self.admin.find(By.XPATH, "//input[@id='message']").send_keys(
            'automated test')

        self.admin.driver.find_elements_by_xpath(
            "//input[@class='btn btn-default']")[0].click()

        self.admin.sleep(5)

        # View notification as student
        student = Student(use_env_vars=True)
        student.login()
        student.select_course(appearance='physics')
        student.sleep(10)
        notifs = student.driver.find_elements_by_xpath(
            "//div[@class='notification system']/span")

        found = False

        for notif in notifs:
            if notif.text.find("automated test") >= 0:
                found = True

        student.delete()

        # Delete notification
        notif = self.admin.driver.find_elements_by_xpath(
            "//div[@class='col-xs-12']")

        for index, n in enumerate(notif):
            if n.text.find('automated test') >= 0:
                self.admin.driver.find_elements_by_xpath(
                    "//a[@class='btn btn-warning']")[index].click()
                self.admin.driver.switch_to_alert().accept()
                self.ps.test_updates['passed'] = True
                break

        self.admin.sleep(5)

        notif = self.admin.driver.find_elements_by_xpath(
            "//div[@class='col-xs-12']")

        assert(found), 'notification not seen'

        self.ps.test_updates['passed'] = True

    # Case C112522 - 009 - Teacher | View an active system notification
    @pytest.mark.skipif(str(112522) not in TESTS, reason='Excluded')
    def test_teacher_view_active_notification_112522(self):
        """View an active system notification.

        Steps:

        Expected Result:

        """
        self.ps.test_updates['name'] = 't1.57.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.57', 't1.57.009', '112522']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'System Setting')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Notifications')
            )
        ).click()
        self.admin.sleep(5)

        self.admin.find(By.XPATH, "//input[@id='message']").send_keys(
            'automated test')

        self.admin.driver.find_elements_by_xpath(
            "//input[@class='btn btn-default']")[0].click()

        self.admin.sleep(5)

        # View notification as student
        teacher = Teacher(use_env_vars=True)
        teacher.login()
        teacher.select_course(appearance='physics')
        teacher.sleep(10)
        notifs = teacher.driver.find_elements_by_xpath(
            "//div[@class='notification system']/span")

        found = False

        for notif in notifs:
            if notif.text.find("automated test") >= 0:
                found = True

        teacher.delete()

        # Delete notification
        notif = self.admin.driver.find_elements_by_xpath(
            "//div[@class='col-xs-12']")

        for index, n in enumerate(notif):
            if n.text.find('automated test') >= 0:
                self.admin.driver.find_elements_by_xpath(
                    "//a[@class='btn btn-warning']")[index].click()
                self.admin.driver.switch_to_alert().accept()
                self.ps.test_updates['passed'] = True
                break

        self.admin.sleep(5)

        notif = self.admin.driver.find_elements_by_xpath(
            "//div[@class='col-xs-12']")

        assert(found), 'notification not seen'

        self.ps.test_updates['passed'] = True

    # Case C112523 - 010 - Teacher | View an active instructor-only
    # system notification
    @pytest.mark.skipif(str(112523) not in TESTS, reason='Excluded')
    def test_teacher_view_instructor_notification_112523(self):
        """View an active instructor-only system notification.

        Steps:

        Expected Result:

        """
        self.ps.test_updates['name'] = 't1.57.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.57', 't1.57.010', '112523']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'System Setting')
            )
        ).click()
        self.admin.wait.until(
            expect.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Notifications')
            )
        ).click()
        self.admin.sleep(5)

        self.admin.find(By.XPATH, "//div[3]//input[@id='message']").send_keys(
            'automated test')

        self.admin.driver.find_elements_by_xpath(
            "//input[@class='btn btn-default']")[1].click()

        self.admin.sleep(5)

        # View notification as student
        teacher = Teacher(use_env_vars=True)
        teacher.login()
        teacher.select_course(appearance='physics')
        teacher.sleep(10)
        notifs = teacher.driver.find_elements_by_xpath(
            "//div[@class='notification system']/span")

        found = False

        for notif in notifs:
            if notif.text.find("automated test") >= 0:
                found = True

        teacher.delete()

        # Delete notification
        notif = self.admin.driver.find_elements_by_xpath(
            "//div[@class='col-xs-12']")

        for index, n in enumerate(notif):
            if n.text.find('automated test') >= 0:
                self.admin.driver.find_elements_by_xpath(
                    "//a[@class='btn btn-warning']")[index].click()
                self.admin.driver.switch_to_alert().accept()
                self.ps.test_updates['passed'] = True
                break

        self.admin.sleep(5)

        notif = self.admin.driver.find_elements_by_xpath(
            "//div[@class='col-xs-12']")

        assert(found), 'notification not seen'

        self.ps.test_updates['passed'] = True
