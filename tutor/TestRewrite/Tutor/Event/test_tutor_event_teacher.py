"""Tutor Event Teacher"""

import datetime
import inspect
import json
import os
import pytest
# import random
import unittest

from pastasauce import PastaSauce, PastaDecorator
from random import randint
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
# from selenium.webdriver.support.ui import WebDriverWait
from staxing.assignment import Assignment
from time import sleep

# select user types: Teacher
from staxing.helper import Teacher


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
        162172, 162173, 162174, 162175, 162176,
        162177, 162178, 162179, 162180, 162181,
        162182, 162183, 162184, 162185, 162186,
        162187, 162188
        # 162188

    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestCreateAReading(unittest.TestCase):
    """T1.14 - Create a Reading."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        if not LOCAL_RUN:
            self.teacher = Teacher(
                use_env_vars=True,
                pasta_user=self.ps,
                capabilities=self.desired_capabilities
            )
        else:
            self.teacher = Teacher(
                use_env_vars=True
            )
        self.teacher.login()
        self.teacher.select_course(appearance='college_physics')

    def tearDown(self):
        """Test destructor."""
        if not LOCAL_RUN:
            self.ps.update_job(
                job_id=str(self.teacher.driver.session_id),
                **self.ps.test_updates
            )
        try:
            self.teacher.delete()
        except:
            pass

    # Case C162172 001 Teacher | Add a new open event for all periods
    @pytest.mark.skipif(str(162172) not in TESTS, reason="Excluded")
    def test_teacher_add_a_new_open_event_all_periods_162172(self):
        self.ps.test_updates['name'] = 'tutor_event_teacher' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = \
            ['tutor', 'event', 'teacher', '162172']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'event_001_%d' % (randint(100, 999))
        assignment = Assignment()

        # Open Add Reading page
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Event').click()
        assert ('event/new' in self.teacher.current_url()), \
            'not at add event screen'

        # Find and fill in title
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        ).send_keys(assignment_name)

        # Fill in description
        self.teacher.find(
            By.XPATH, '//textarea[contains(@class, "form-control")]'
        ).send_keys('description')

        # Set date
        today = datetime.date.today()
        end = randint(1, 5)
        opens_on = today.strftime(
            '%m/%d/%Y')  # make the start date today so it will be open
        closes_on = (today + datetime.timedelta(days=end)) \
            .strftime('%m/%d/%Y')
        assignment.assign_periods(
            self.teacher.driver, {'all': (opens_on, closes_on)})

        # publish
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"-publish")]')
            )
        ).click()
        try:
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(assignment_name)
            )
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH,
                '//a[contains(@class,"header-control next")]'
            ).click()
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(assignment_name)
            )

        self.ps.test_updates['passed'] = True

    # Case C162173 002 Teacher | Save a draft for individual periods
    @pytest.mark.skipif(str(162173) not in TESTS, reason="Excluded")
    def test_teacher_save_a_draft_event_for_individual_periods_162173(self):
        self.ps.test_updates['name'] = 'tutor_event_teacher' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['tutor', 'event', 'teacher',
                                        '162173']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'event_002_%d' % (randint(100, 999))
        assignment = Assignment()

        # Open Add Reading page
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Event').click()
        assert ('event/new' in self.teacher.current_url()), \
            'not at add readings screen'

        # Find and fill in title
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        ).send_keys(assignment_name)

        # Set date
        today = datetime.date.today()
        start = randint(0, 6)
        end = start + randint(1, 5)
        opens_on = (today + datetime.timedelta(days=start)) \
            .strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=end)) \
            .strftime('%m/%d/%Y')

        # Find all individual periods
        self.teacher.find(By.ID, 'show-periods-radio').click()
        period_boxes = self.teacher.driver.find_elements(
            By.XPATH, '//input[contains(@id, "period-toggle-period")]'
        )
        period_assignment = {}
        for period in period_boxes:
            period_assignment[
                self.teacher.driver.find_element(
                    By.XPATH,
                    '//label[contains(@for, "%s")]' % period.get_attribute(
                        'id')).text
            ] = (opens_on, closes_on)

        assignment.assign_periods(self.teacher.driver, period_assignment)

        # Save as draft
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'builder-draft-button')
            )
        ).click()

        # Check if the draft is on the dashboard
        try:
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(assignment_name)
            )
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH,
                '//a[contains(@class,"header-control next")]'
            ).click()
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(assignment_name)
            )

        self.ps.test_updates['passed'] = True

    # Case C162174 003 Teacher | Create and publish a new unopened assignment
    # from calendar
    @pytest.mark.skipif(str(162174) not in TESTS, reason="Excluded")
    def test_teacher_create_and_publish_new_unopen_event_from_cal_162174(self):
        self.ps.test_updates['name'] = 'tutor_event_teacher' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['tutor', 'event', 'teacher',
                                        '162174']
        self.ps.test_updates['passed'] = False
        # Test steps and verification assertions
        calendar_date = self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//div[contains(@class,"Day--upcoming")]')
            )
        )
        self.teacher.driver.execute_script(
            'return arguments[0].scrollIntoView();',
            calendar_date
        )
        self.teacher.sleep(1)
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(calendar_date)
        actions.move_by_offset(0, -35)
        actions.click()
        actions.move_by_offset(30, 105)
        actions.click()
        actions.perform()

        assert ('event/new' in self.teacher.current_url()), \
            'not at Add Event page'

        assignment_name = 'event_003_%d' % (randint(100, 999))
        assignment = Assignment()

        # Find and fill in title
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        ).send_keys(assignment_name)

        # Fill in description
        self.teacher.find(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]' +
            '//textarea[contains(@class,"form-control")]'
        ).send_keys('description')
        # or change it to span .assignment-description > .form-control

        # Set date
        today = datetime.date.today()
        start = randint(1, 5)
        end = start + randint(1, 5)

        # the open date should be in the future for the assignment to be
        # unopened
        opens_on = (today + datetime.timedelta(days=start)) \
            .strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=end)) \
            .strftime('%m/%d/%Y')
        assignment.assign_periods(
            self.teacher.driver, {'all': (opens_on, closes_on)})

        # Publish
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class, "-publish")]')
            )
        ).click()
        try:
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(assignment_name)
            )
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH,
                '//a[contains(@class,"header-control next")]'
            ).click()
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(assignment_name))

        self.ps.test_updates['passed'] = True

    # Case C162175 004 Teacher | Publish a draft event
    @pytest.mark.skipif(str(162175) not in TESTS, reason="Excluded")
    def test_teacher_publish_a_draft_event_162175(self):
        self.ps.test_updates['name'] = 'tutor_event_teacher' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['tutor', 'event', 'teacher',
                                        '162175']

        self.ps.test_updates['passed'] = False
        # Test steps and verification assertions
        assignment_name = 'event_004_%s' % randint(100, 999)
        today = datetime.date.today()
        start = randint(0, 6)
        finish = start + randint(1, 5)
        begin = (today + datetime.timedelta(days=start)) \
            .strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=finish)) \
            .strftime('%m/%d/%Y')
        self.teacher.add_assignment(
            assignment='event',
            args={
                'title': assignment_name,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'status': 'draft',
            }
        )

        # Find the draft event on the calendar
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'month-wrapper')
            )
        )
        self.teacher.find(
            By.XPATH, '//label[contains(text(),"{0}")]'.format(assignment_name)
        ).click()

        # Publish the draft assignment
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"-publish")]')
            )
        ).click()

        try:
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(assignment_name)
            )
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH,
                '//a[contains(@class,"header-control next")]'
            ).click()
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(assignment_name)
            )

        self.ps.test_updates['passed'] = True

    # Case C162176 005 Teacher | Cancel a new event before making changes
    @pytest.mark.skipif(str(162176) not in TESTS, reason="Excluded")
    def test_teacher_cancel_a_new_event_before_changes_162176(self):
        self.ps.test_updates['name'] = 'tutor_event_teacher' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['tutor', 'event', 'teacher',
                                        '162176']
        self.ps.test_updates['passed'] = False

        # Open "Add Event" page
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Event').click()
        assert ('event/new' in self.teacher.current_url()), \
            'not at add event screen'

        # Cancel a reading with "Cancel" button
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'builder-cancel-button')
            )
        ).click()
        assert ('month' in self.teacher.current_url()), \
            'not back at calendar after cancelling event'

        # Open "Add Event" page
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Event').click()
        assert ('event/new' in self.teacher.current_url()), \
            'not at add event screen'

        # Cancel an event with "X" button
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class,"openstax-close-x")]')
            )
        ).click()
        assert ('month' in self.teacher.current_url()), \
            'not back at calendar after cancelling event'

        self.ps.test_updates['passed'] = True

    # Case C162177 006 Teacher | Cancel a new event after making changes
    @pytest.mark.skipif(str(162177) not in TESTS, reason="Excluded")
    def test_teacher_cancel_a_new_event_after_changes_162177(self):
        self.ps.test_updates['name'] = 'tutor_event_teacher' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['tutor', 'event', 'teacher',
                                        '162177']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'event_006_%d' % (randint(100, 999))

        # Open "Add Event" page
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Event').click()
        assert ('event/new' in self.teacher.current_url()), \
            'not at add Event screen'

        # Add title
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        ).send_keys(assignment_name)
        sleep(1)

        # Cancel with "Cancel" button
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'builder-cancel-button')
            )
        ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class,"ok")]')
            )
        ).click()

        # Check if back at user dashboard
        assert ('month' in self.teacher.current_url()), \
            'not back at calendar after cancelling Event'

        # Open "Add Event" page
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Event').click()
        assert ('event/new' in self.teacher.current_url()), \
            'not at add Event screen'

        # Add title
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        ).send_keys(assignment_name)

        # Cancel with "X" button
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class,"openstax-close-x")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"ok")]')
            )
        ).click()
        assert ('month' in self.teacher.current_url()), \
            'not back at calendar after cancelling Event'

        self.ps.test_updates['passed'] = True

    # Case C162178 007 Teacher | Cancel a draft event before making changes
    @pytest.mark.skipif(str(162178) not in TESTS, reason="Excluded")
    def test_teacher_cancel_a_draft_event_before_changes_162178(self):
        self.ps.test_updates['name'] = 'tutor_event_teacher' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['tutor', 'event', 'teacher',
                                        '162178']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name_1 = 'event_007_%s' % randint(100, 500)
        assignment_name_2 = 'event_007_%s' % randint(500, 999)

        today = datetime.date.today()
        finish = randint(1, 5)
        begin = today.strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=finish)) \
            .strftime('%m/%d/%Y')

        # Create a draft assignment
        self.teacher.add_assignment(
            assignment='event',
            args={
                'title': assignment_name_1,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'status': 'draft',
            }
        )

        # Find the draft Event on the calendar
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'month-wrapper')
            )
        )
        self.teacher.find(
            By.XPATH,
            '//label[contains(text(),"{0}")]'.format(assignment_name_1)
        ).click()
        sleep(1)

        # Cancel with "Cancel" button
        cancel_button = self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'builder-cancel-button')
            )
        )
        self.teacher.scroll_to(cancel_button)
        cancel_button.click()

        # Check if teacher is taken to user dashboard
        self.teacher.page.wait_for_page_load()
        assert ('month' in self.teacher.current_url()), \
            'not back at calendar after cancelling Event'

        # Add a draft Event
        self.teacher.add_assignment(
            assignment='event',
            args={
                'title': assignment_name_2,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'status': 'draft',
            }
        )

        # Find the draft Event on the calendar
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'month-wrapper')
            )
        )
        self.teacher.find(
            By.XPATH,
            '//label[contains(text(),"{0}")]'.format(assignment_name_2)
        ).click()
        sleep(1)

        # Cancel with "X" button
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class,"openstax-close-x")]')
            )
        ).click()

        # Check if the teacher is back to user dashboard
        assert ('month' in self.teacher.current_url()), \
            'not back at calendar after cancelling Event'

        self.ps.test_updates['passed'] = True

    # Case C162179 008 Teacher | Cancel a draft event after making changes
    @pytest.mark.skipif(str(162179) not in TESTS, reason="Excluded")
    def test_teacher_cancel_a_draft_event_after_changes_162179(self):
        self.ps.test_updates['name'] = 'tutor_event_teacher' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['tutor', 'event', 'teacher',
                                        '162179']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name_1 = 'event_008_%s' % randint(100, 500)
        assignment_name_2 = 'event_008_%s' % randint(500, 999)

        today = datetime.date.today()
        finish = randint(1, 5)
        begin = today.strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=finish)) \
            .strftime('%m/%d/%Y')

        # Create a draft assignment
        self.teacher.add_assignment(
            assignment='event',
            args={
                'title': assignment_name_1,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'status': 'draft',
            }
        )

        # Find the draft Event on the calendar
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'month-wrapper')
            )
        )
        self.teacher.find(
            By.XPATH,
            '//label[contains(text(),"{0}")]'.format(assignment_name_1)
        ).click()
        sleep(1)

        # Edit the assignment
        self.teacher.find(
            By.ID, "reading-title"
        ).send_keys('changed')

        # Cancel with "Cancel" button
        cancel_button = self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'builder-cancel-button')
            )
        )
        self.teacher.scroll_to(cancel_button)
        cancel_button.click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class,"ok")]')
            )
        ).click()

        # Check if teacher is taken to user dashboard
        self.teacher.page.wait_for_page_load()
        assert ('month' in self.teacher.current_url()), \
            'not back at calendar after cancelling Event'

        # Create a draft assignment
        self.teacher.add_assignment(
            assignment='event',
            args={
                'title': assignment_name_2,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'status': 'draft',
            }
        )

        # Find the draft Event on the calendar
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'month-wrapper')
            )
        )
        self.teacher.find(
            By.XPATH,
            '//label[contains(text(),"{0}")]'.format(assignment_name_2)
        ).click()
        sleep(1)

        # Edit the assignment
        self.teacher.find(
            By.ID, "reading-title"
        ).send_keys('changed')

        # Cancel with "X" button
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class,"openstax-close-x")]')
            )
        ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class,"ok")]')
            )
        ).click()

        # Check if the teacher is back to user dashboard
        assert ('month' in self.teacher.current_url()), \
            'not back at calendar after cancelling Event'

        self.ps.test_updates['passed'] = True

    # Case C162180 009 Teacher | Attempt to save or publish an event with blank
    # required fields
    @pytest.mark.skipif(str(162180) not in TESTS, reason="Excluded")
    def test_teacher_attempt_to_save_pub_events_w_blank_req_field_162180(self):
        self.ps.test_updates['name'] = 'tutor_event_teacher' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['tutor', 'event', 'teacher',
                                        '162180']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Event').click()
        assert ('event/new' in self.teacher.current_url()), \
            'not at add Event screen'

        # Publish without filling in any fields
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class,"-publish")]')
            )
        ).click()

        # Required field reminder
        self.teacher.find(
            By.XPATH, '//div[contains(text(),"Required field")]')
        assert ('event' in self.teacher.current_url()), \
            'went back to calendar even though required fields were left blank'

        # Refresh the page
        self.teacher.driver.refresh()
        sleep(3)

        # Save without filling in any fields
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class, "save")]')
            )
        ).click()

        # Required field reminder
        self.teacher.find(
            By.XPATH, '//div[contains(text(),"Required field")]')
        assert ('event' in self.teacher.current_url()), \
            'went back to calendar even though required fields were left blank'

        self.ps.test_updates['passed'] = True

    # Case C162181 010 Teacher | Delete a draft event
    @pytest.mark.skipif(str(162181) not in TESTS, reason="Excluded")
    def test_teacher_delete_a_draft_event_162181(self):
        self.ps.test_updates['name'] = 'tutor_event_teacher' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['tutor', 'event', 'teacher',
                                        '162181']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'event_010_%s' % randint(100, 500)

        today = datetime.date.today()
        finish = randint(1, 5)
        begin = today.strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=finish)) \
            .strftime('%m/%d/%Y')

        # Create a draft assignment
        self.teacher.add_assignment(
            assignment='event',
            args={
                'title': assignment_name,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'status': 'draft',
            }
        )

        # Find the draft Event on the calendar
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'month-wrapper')
            )
        )
        self.teacher.find(
            By.XPATH,
            '//label[contains(text(),"{0}")]'.format(assignment_name)
        ).click()
        sleep(1)

        # Delete the draft assignment
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[contains(@class,"delete-link")]')
            )
        ).click()
        self.teacher.find(
            By.XPATH, '//button[contains(text(),"Yes")]'
        ).click()
        sleep(3)

        assert ('month' in self.teacher.current_url()), \
            'not returned to calendar after deleting an assignment'

        # have to refresh to remove the assignment tab from calendar
        self.teacher.driver.refresh()
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'month-wrapper')
            )
        )
        deleted_event = self.teacher.find_all(
            By.XPATH, '//label[@data-title="{0}"]'.format(assignment_name)
        )
        assert (len(deleted_event) == 0), 'Event not deleted'

        self.ps.test_updates['passed'] = True

    # Case C162182 011 Teacher | Delete an unopened event
    @pytest.mark.skipif(str(162182) not in TESTS, reason="Excluded")
    def test_teacher_delete_an_unopened_event_162182(self):
        self.ps.test_updates['name'] = 'tutor_event_teacher' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['tutor', 'event', 'teacher',
                                        '162182']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'event_011_%s' % randint(100, 500)

        today = datetime.date.today()
        start = randint(2, 3)
        finish = start + randint(1, 5)
        begin = (today + datetime.timedelta(days=start)) \
            .strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=finish)) \
            .strftime('%m/%d/%Y')

        # Create an unopened assignment
        self.teacher.add_assignment(
            assignment='event',
            args={
                'title': assignment_name,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'status': 'publish',
            }
        )

        # Find the unopened Event on the calendar
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'month-wrapper')
            )
        )
        self.teacher.find(
            By.XPATH,
            '//label[contains(text(),"{0}")]'.format(assignment_name)
        ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'edit-assignment-button')
            )
        ).click()

        # Delete the assignment
        delete_button = self.teacher.find(
            By.XPATH, '//button[contains(@class,"delete-link")]'
        )
        self.teacher.scroll_to(delete_button)
        delete_button.click()
        sleep(3)
        confirm_button = self.teacher.find(
            By.XPATH, '//button[contains(text(),"Yes")]'
        )
        self.teacher.scroll_to(confirm_button)
        confirm_button.click()
        sleep(3)

        assert ('month' in self.teacher.current_url()), \
            'not returned to calendar after deleting an assignment'

        # Have to refresh the browser to remove assignment tab from calendar
        self.teacher.driver.refresh()
        deleted_unopened = self.teacher.find_all(
            By.XPATH, '//label[@data-title="{0}"]'.format(assignment_name)
        )
        assert len(deleted_unopened) == 0, 'unopened reading not deleted'

        self.ps.test_updates['passed'] = True

    # Case C162183 012 Teacher | Delete an open event
    @pytest.mark.skipif(str(162183) not in TESTS, reason="Excluded")
    def test_teacher_delete_an_open_event_162183(self):
        self.ps.test_updates['name'] = 'tutor_event_teacher' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['tutor', 'event', 'teacher',
                                        '162183']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'event_012_%s' % randint(100, 500)

        today = datetime.date.today()
        finish = randint(1, 5)
        begin = today.strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=finish)) \
            .strftime('%m/%d/%Y')

        # Create an unopened assignment
        self.teacher.add_assignment(
            assignment='event',
            args={
                'title': assignment_name,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'status': 'publish',
            }
        )

        # Find the open Event on the calendar
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'month-wrapper')
            )
        )
        self.teacher.find(
            By.XPATH,
            '//label[contains(text(),"{0}")]'.format(assignment_name)
        ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'edit-assignment-button')
            )
        ).click()

        # Delete the assignment
        delete_button = self.teacher.find(
            By.XPATH, '//button[contains(@class,"delete-link")]'
        )
        self.teacher.scroll_to(delete_button)
        delete_button.click()
        sleep(3)
        confirm_button = self.teacher.find(
            By.XPATH, '//button[contains(text(),"Yes")]'
        )
        self.teacher.scroll_to(confirm_button)
        confirm_button.click()
        sleep(3)

        assert ('month' in self.teacher.current_url()), \
            'not returned to calendar after deleting an assignment'

        # Have to refresh the browser to remove assignment tab from calendar
        self.teacher.driver.refresh()
        deleted_unopened = self.teacher.find_all(
            By.XPATH, '//label[@data-title="{0}"]'.format(assignment_name)
        )
        assert len(
            deleted_unopened) == 0, 'open Event not deleted'

        self.ps.test_updates['passed'] = True

    # Case C162184 013 Teacher | Change a draft event
    @pytest.mark.skipif(str(162184) not in TESTS, reason="Excluded")
    def test_teacher_change_a_draft_event_162184(self):
        self.ps.test_updates['name'] = 'tutor_event_teacher' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['tutor', 'event', 'teacher',
                                        '162184']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'event_013_%s' % randint(100, 500)
        assignment = Assignment()
        today = datetime.date.today()
        finish = randint(1, 5)
        begin = today.strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=finish)) \
            .strftime('%m/%d/%Y')

        # Create a draft assignment
        self.teacher.add_assignment(
            assignment='event',
            args={
                'title': assignment_name,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'status': 'draft',
            }
        )

        # Find the draft Event on the calendar
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'month-wrapper')
            )
        )
        self.teacher.find(
            By.XPATH,
            '//label[contains(text(),"{0}")]'.format(assignment_name)
        ).click()
        sleep(1)

        # Change the title
        self.teacher.find(
            By.ID, "reading-title"
        ).send_keys("changed")

        # Change the description
        self.teacher.find(
            By.CSS_SELECTOR, ".assignment-description>.form-control"
        ).send_keys("changed")

        # Set new due dates
        today = datetime.date.today()
        start = randint(1, 6)
        end = start + randint(1, 5)
        opens_on = (today + datetime.timedelta(days=start)) \
            .strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=end)) \
            .strftime('%m/%d/%Y')
        assignment.assign_periods(
            self.teacher.driver,
            {'all': (opens_on, closes_on)}
        )

        # Save as draft
        self.teacher.find(
            By.XPATH, '//button[contains(@class,"-save")]'
        ).click()
        sleep(1)

        # Find the new title on the calendar
        try:
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(
                    assignment_name + 'changed')
            )
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH,
                '//a[contains(@class,"header-control next")]'
            ).click()
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(
                    assignment_name + 'changed')
            )

        self.ps.test_updates['passed'] = True

    # Case C162185 014 Teacher | Change an unopened event
    @pytest.mark.skipif(str(162185) not in TESTS, reason="Excluded")
    def test_teacher_change_an_unopened_event_162185(self):
        self.ps.test_updates['name'] = 'tutor_event_teacher' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['tutor', 'event', 'teacher',
                                        '162185']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'event_014_%s' % randint(100, 500)
        assignment = Assignment()

        today = datetime.date.today()
        start = randint(2, 3)
        finish = start + randint(1, 5)
        begin = (today + datetime.timedelta(days=start)) \
            .strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=finish)) \
            .strftime('%m/%d/%Y')

        # Create an unopened assignment
        self.teacher.add_assignment(
            assignment='event',
            args={
                'title': assignment_name,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'status': 'publish',
            }
        )

        # Find the unopened Event on the calendar
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'month-wrapper')
            )
        )
        self.teacher.find(
            By.XPATH,
            '//label[contains(text(),"{0}")]'.format(assignment_name)
        ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'edit-assignment-button')
            )
        ).click()

        # Change the title
        self.teacher.find(
            By.ID, "reading-title"
        ).send_keys("changed")

        # Change the description
        self.teacher.find(
            By.CSS_SELECTOR, ".assignment-description>.form-control"
        ).send_keys("changed")

        # Set new due dates
        today = datetime.date.today()
        start = randint(1, 6)
        end = start + randint(1, 5)
        opens_on = (today + datetime.timedelta(days=start)) \
            .strftime('%m/%d/%Y')
        closes_on = (today + datetime.timedelta(days=end)) \
            .strftime('%m/%d/%Y')
        assignment.assign_periods(
            self.teacher.driver,
            {'all': (opens_on, closes_on)}
        )

        # Publish
        self.teacher.find(
            By.XPATH, '//button[contains(@class,"-publish")]'
        ).click()
        sleep(1)

        # Find the new title on the calendar
        try:
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(
                    assignment_name + 'changed')
            )
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH,
                '//a[contains(@class,"header-control next")]'
            ).click()
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(
                    assignment_name + 'changed')
            )

        self.ps.test_updates['passed'] = True

    # Case C162186 015 Teacher | Change an open event
    @pytest.mark.skipif(str(162186) not in TESTS, reason="Excluded")
    def test_teacher_change_an_open_event_162186(self):
        self.ps.test_updates['name'] = 'tutor_event_teacher' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['tutor', 'event', 'teacher',
                                        '162186']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'event_015_%s' % randint(100, 500)
        assignment = Assignment()

        today = datetime.date.today()
        finish = randint(1, 5)
        begin = today.strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=finish)) \
            .strftime('%m/%d/%Y')

        # Create an open assignment
        self.teacher.add_assignment(
            assignment='event',
            args={
                'title': assignment_name,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'status': 'publish',
            }
        )

        # Find the open Event on the calendar
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'month-wrapper')
            )
        )
        self.teacher.find(
            By.XPATH,
            '//label[contains(text(),"{0}")]'.format(assignment_name)
        ).click()
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'edit-assignment-button')
            )
        ).click()

        # Change the title
        self.teacher.find(
            By.ID, "reading-title"
        ).send_keys("changed")

        # Change the description
        self.teacher.find(
            By.CSS_SELECTOR, ".assignment-description>.form-control"
        ).send_keys("changed")

        # Set new due dates
        end = randint(1, 5)
        closes_on = (today + datetime.timedelta(days=end)) \
            .strftime('%m/%d/%Y')
        assignment.assign_date(
            driver=self.teacher.driver, date=closes_on, is_all=True,
            target='due'
        )

        # Publish
        self.teacher.find(
            By.XPATH, '//button[contains(@class,"-publish")]'
        ).click()
        sleep(1)

        # Find the new title on the calendar
        try:
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(
                    assignment_name + 'changed')
            )
        except NoSuchElementException:
            self.teacher.find(
                By.XPATH,
                '//a[contains(@class,"header-control next")]'
            ).click()
            self.teacher.find(
                By.XPATH,
                '//label[contains(text(),"{0}")]'.format(
                    assignment_name + 'changed')
            )

        self.ps.test_updates['passed'] = True

    # Case C162187 016 Teacher | Add an event by dragging and dropping
    @pytest.mark.skipif(str(162187) not in TESTS, reason="Excluded")
    def test_teacher_add_an_event_by_drag_and_drop_162187(self):
        self.ps.test_updates['name'] = 'tutor_event_teacher' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['tutor', 'event', 'teacher',
                                        '162187']
        self.ps.test_updates['passed'] = False

        # Test verification
        self.teacher.assign.open_assignment_menu(self.teacher.driver)
        event_tab = self.teacher.find(
            By.LINK_TEXT, 'Add Event'
        )

        due_date = self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//div[contains(@class,"Day--upcoming")]')
            )
        )
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(event_tab)

        actions.drag_and_drop(event_tab, due_date).perform()
        sleep(3)

        assert ('event/new' in self.teacher.current_url()), \
            'not at Add Event page'

        self.ps.test_updates['passed'] = True

    # Case C162188 017 Teacher| Get assignment link test info icons
    @pytest.mark.skipif(str(162188) not in TESTS, reason="Excluded")
    def test_teacher_get_assignment_link_and_view_info_icons_162188(self):
        self.ps.test_updates['name'] = 'tutor_event_teacher' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['tutor', 'event', 'teacher',
                                        '162188']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        assignment_name = 'event_017_%d' % (randint(100, 999))
        assignment = Assignment()
        today = datetime.date.today()
        start = randint(2, 6)
        finish = start + randint(1, 5)
        begin_today = today.strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=finish)).strftime('%m/%d/%Y')

        # Open Add Event page
        assignment.open_assignment_menu(self.teacher.driver)
        self.teacher.find(By.LINK_TEXT, 'Add Event').click()
        assert ('event/new' in self.teacher.current_url()), \
            'not at add event screen'

        # Test info icon
        self.teacher.find(
            By.XPATH, '//button[contains(@class, "footer-instructions")]'
        ).click()
        self.teacher.find(By.ID, 'plan-footer-popover')

        self.ps.test_updates['passed'] = True

        # Back to dashboard
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'builder-cancel-button')
            )
        ).click()
        assert ('month' in self.teacher.current_url()), \
            'not back at calendar after cancelling event'

        self.teacher.add_assignment(
            assignment='event',
            args={
                'title': assignment_name,
                'description': 'description',
                'periods': {'all': (begin_today, end)},
                'url': 'www.openstax.org',
                'status': 'publish'
            }
        )

        # View assignment summary
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'month-wrapper')
            )
        )
        self.teacher.find(
            By.XPATH, '//label[contains(text(),"{0}")]'.format(assignment_name)
        ).click()

        # Get assignment link
        self.teacher.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'lms-info-link')
            )
        ).click()
        sleep(3)
        self.teacher.find(
            By.XPATH, '//div[contains(@id, "sharable-link-popover")]'
        )

        self.ps.test_updates['passed'] = True
