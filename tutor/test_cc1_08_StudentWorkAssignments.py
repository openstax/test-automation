"""Concept Coach v1, Epic 08 - StudentsWorkAssignments."""

import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
from random import randint
from selenium.webdriver.common.by import By
from staxing.assignment import Assignment
from staxing.helper import Teacher, Student


BROWSERS = os.environ['BROWSERS']
TESTS = os.environ['CASELIST']


@PastaDecorator.on_platforms(BROWSERS)
class TestStudentsWorkAssignments(unittest.TestCase):
    """CC1.08 - Students Work Assignments."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        teacher = Teacher(username='Teacher100', password='password',
                          site='https://tutor-qa.openstax.org/')
        teacher.login()
        courses = teacher.find_all(By.CSS_CLASS,
                                   'tutor-booksplash-course-item')
        assert(courses), 'No courses found.'
        if not isinstance(courses, list):
            courses = [courses]
        course_id = randint(0, len(courses))
        self.course = courses[course_id].getattribute('data-title')
        teacher.select_course(title=self.course)
        teacher.goto_course_roster()
        section = '%s' % randint(100, 999)
        try:
            wait = teacher.wait_time
            teacher.change_wait_time(3)
            teacher.find(By.CSS_CLASS, '-no-periods-text')
            teacher.add_course_section(section)
        except:
            sections = teacher.find_all(
                By.XPATH,
                '//span[@class="tab-item-period-name"]'
            )
            section = sections[randint(0, len(sections))].text
        finally:
            teacher.change_wait_time(wait)
        self.code = teacher.get_enrollment_code(section)
        self.book_url = teacher.find(
            By.XPATH, '//a[span[text()="Online Book "]]'
        ).getattribute('href')
        self.student = Student()
        self.student.get(self.book_url)
        self.student.find(By.CSS_CLASS, 'nav next').click()
        self.student.page.wait_for_page_load()
        widget = self.student.find(By.CSS_CLASS, 'launcher-laptop')
        Assignment.scroll_to(self.student.driver, widget)

    # Case C7691 - 002 - Student | Selects an exercise answer
    @pytest.mark.skipif(str(7691) not in TESTS, reason='Excluded')
    def test_select_an_exercise_answer():
        """Select an exercise answer."""
        assert 1 != 4
