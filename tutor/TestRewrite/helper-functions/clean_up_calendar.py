import json
import os

# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
# from selenium.webdriver.support.ui import WebDriverWait
# from staxing.assignment import Assignment
from time import sleep

from staxing.helper import Teacher

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': 'latest',
    'screenResolution': "1024x768",
}])

BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
COURSE = "college_physics"

# Log in to tutor
teacher = Teacher(use_env_vars=True)
teacher.login()
teacher.select_course(appearance=COURSE)


def delete_assignment(target_element, is_published):
    """
    target_element: the web element of assignment to be deleted
    """
    target_element.click()
    sleep(1)
    if is_published:
        teacher.find(
            By.ID, "edit-assignment-button"
        ).click()
        sleep(1)
    delete_button = teacher.wait.until(
        expect.element_to_be_clickable(
            (By.XPATH, '//button[contains(@class,"delete-link")]')
        )
    )
    teacher.scroll_to(delete_button)
    sleep(1)
    delete_button.click()
    teacher.find(
        By.XPATH, '//button[contains(text(), "Yes")]'
    ).click()
    sleep(1)


def find_published(assignment_type, is_all):
    """
    assignment_type: can be "reading", "homework", "external" or "event"
    is_all: boolean value
            True when you want to find all assignment of assignment_type
    """
    if is_all:
        published = teacher.find_all(
            By.XPATH,
            '//div[@data-assignment-type="' + assignment_type + '"'
            ' and contains(@class, "is-published") and not(@draggable="true")]'
        )
    else:
        published = teacher.find(
            By.XPATH,
            '//div[@data-assignment-type="' + assignment_type + '"'
            ' and contains(@class, "is-published") and not(@draggable="true")]'
        )
    return published


def find_draft(assignment_type, is_all):
    """
    assignment_type: can be "reading", "homework", "external" or "event"
    is_all: boolean value
            True when you want to find all assignment of assignment_type
    """
    if is_all:
        draft = teacher.find_all(
            By.XPATH,
            '//div[@data-assignment-type="' + assignment_type + '"'
            ' and not(contains(@class, "is-published")) and ' +
            'not(@draggable="true")]'
        )
    else:
        draft = teacher.find(
            By.XPATH,
            '//div[@data-assignment-type="' + assignment_type + '"'
            ' and not(contains(@class, "is-published")) and ' +
            'not(@draggable="true")]'
        )
    return draft


def clean_up_assignment(assignment_type, is_published):
    """
    assignment_type: string of "reading", "homework", "external" or "event"
    is_published: boolean value
                  True when you want to delete published assignment
    """
    if is_published:  # clean up published
        all_assignment = find_published(assignment_type, True)
    else:  # if we want to clean up drafts
        all_assignment = find_draft(assignment_type, True)

    num = len(all_assignment)
    while num > 0:
        if is_published:
            target = find_published(assignment_type, False)
            delete_assignment(target, True)
            teacher.driver.refresh()
            num -= 1
        else:
            target = find_draft(assignment_type, False)
            delete_assignment(target, False)
            teacher.driver.refresh()
            num -= 1

clean_up_assignment("event", False)
