"""
Tutor v2, Epic 11.

Question Work: Faculty Reviews, Excludes, Edits, Creates Assignments
"""

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
from staxing.helper import Teacher, Admin, Content Analyst  # NOQA

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': '50.0',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    str([14695, 14696, 14691, 14692, 14693, 14694, 14699, 14700, 14701, 14702,
         14718, 14715, 14717, 14710, 14711, 14712, 14723, 14722, 14705, 14704,
         14704, 15903, 14719, 14714, 14716, 14709, 14713, 14721, 14720, 14707,
         14706, 15902, 14724, 14725, 14735, 14799, 14727, 14734, 14728, 14729,
         147998, 14730, 14731, 14732, 14736, 14737, 14738])  # NOQA
)


@PastaDecorator.on_platforms(BROWSERS)
class TestQuestionWork(unittest.TestCase):
    """
    T2.11.

    Question Work: Faculty Reviews, Excludes, Edits, Creates Assignments.
    """

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

    # 14695 - 001 - Teacher | Review all questions
    @pytest.mark.skipif(str(14695) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_review_all_questions_14695(self):
        """Review all questions.

        Steps:

        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a Tutor course name

        Click "Question Library" from the user menu
        Select a section or chapter
        Click "Show Questions"


        Expected Result:

        The user is presented with all the questions for the section or chapter


        """
        self.ps.test_updates['name'] = 't2.11.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.001',
            '14695'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14696 - 002 - Teacher | Exclude certain questions
    @pytest.mark.skipif(str(14696) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_exclude_certain_questions_14696(self):
        """Exclude certain questions.

        Steps:

        If the user has more than one course, click on a Tutor course name

        Click "Question Library" from the user menu
        Select a section or chapter
        Click "Show Questions"
        Hover over the desired question and click "Exclude question"


        Expected Result:

        Question is excluded

        """
        self.ps.test_updates['name'] = 't2.11.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.002',
            '14696'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14691 - 003 - Teacher | Tabs filter exercises into 'Reading'
    @pytest.mark.skipif(str(14691) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_tabs_filter_exercises_into_reading_14691(self):
        """Tab filters exercises into 'Reading'.

        Steps:

        If the user has more than one course, click on a Tutor course name

        Click "Question Library" from the user menu
        Select a section or chapter
        Click "Show Questions"
        Click on the "Reading" tab


        Expected Result:

        Exercises that are only for Reading appear

        """
        self.ps.test_updates['name'] = 't2.11.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.003',
            '14691'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14692 - 004 - Teacher | Tabs filter exercises into 'Practice'
    @pytest.mark.skipif(str(14692) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_tabs_filter_exercises_into_practice_14692(self):
        """Tab filters exercises into 'Practice'.

        Steps:

        If the user has more than one course, click on a Tutor course name

        Click "Question Library" from the user menu
        Select a section or chapter
        Click "Show Questions"
        Click on the "Practice" tab


        Expected Result:

        Exercises that are only for practice appear

        """
        self.ps.test_updates['name'] = 't2.11.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.004',
            '14692'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14693 - 005 - Teacher | Pin tabs to top of screen when scrolled
    @pytest.mark.skipif(str(14693) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_pin_tabs_to_top_of_screen_when_scrolled_14693(self):
        """Pin tabs to top of screen when scrolled.

        Steps:

        If the user has more than one course, click on a Tutor course name

        Click "Question Library" from the user menu
        Select a section or chapter
        Click "Show Questions"
        Scroll down


        Expected Result:

        Tabs are pinned to the top of the screen when scrolled

        """
        self.ps.test_updates['name'] = 't2.11.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.005',
            '14693'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14694 - 006 - Teacher | Make section links jumpable
    @pytest.mark.skipif(str(14694) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_make_section_links_jumpable_14694(self):
        """Make section links jumpable.

        Steps:

        If the user has more than one course, click on a Tutor course name

        Click "Question Library" from the user menu
        Select a section or chapter
        Click "Show Questions"
        Click on the section links at the top of the screen


        Expected Result:

        The screen scrolls to the selected screen

        """
        self.ps.test_updates['name'] = 't2.11.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.006',
            '14694'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14699 - 007 - Teacher | Report errata about assessments in Tutor
    @pytest.mark.skipif(str(14699) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_report_errata_about_assessments_in_tutor_14699(self):
        """Report errata about assessments in Tutor.

        Steps:

        If the user has more than one course, click on a Tutor course name

        Click "Question Library" from the user menu
        Select a section or chapter
        Click "Show Questions"
        Hover over the desired question and click "Question details"
        Click "Report an error"


        Expected Result:

        A new tab with the assessment errata form appears, with the assessment
        ID already filled in

        """
        self.ps.test_updates['name'] = 't2.11.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.007',
            '14699'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14700 - 008 - Student | Report errata about assessments in Tutor
    @pytest.mark.skipif(str(14700) not in TESTS, reason='Excluded')  # NOQA
    def test_student_report_errata_about_assessments_in_tutor_14700(self):
        """Report errata about assessments in Tutor.

        Steps:

        If the user has more than one course, click on a Tutor course name

        Click on an assignment
        On an assessment card, click on the "Report an error" link in the
        bottom right corner


        Expected Result:

        A new tab with the assessment errata form appears, with the assessment
        ID already filled in

        """
        self.ps.test_updates['name'] = 't2.11.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.008',
            '14700'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14701 - 009 - Admin | Exclude questions from all courses
    @pytest.mark.skipif(str(14701) not in TESTS, reason='Excluded')  # NOQA
    def test_admin_exclude_questions_from_all_courses_14701(self):
        """Exclude questions from all courses.

        Steps:



        Expected Result:


        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # 14702 - 010 - Teacher | Exclude a question from already worked
    # assignments
    @pytest.mark.skipif(str(14702) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_exclude_a_question_from_already_worked_assign_14702(self):
        """Exclude a question from already worked assignments.

        Steps:

        If the user has more than one course, click on a Tutor course name

        Go to an open assignment that has already been worked
        Click the X on the upper right corner of an assessment card
        Click "Remove"


        Expected Result:

        A question is excluded from already worked assignments

        """
        self.ps.test_updates['name'] = 't2.11.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.009',
            '14702'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14718 - 011 - Content Analyst | Create a brand new multiple choice
    # question
    @pytest.mark.skipif(str(14702) not in TESTS, reason='Excluded')  # NOQA
    def test_content_analyst_create_a_brand_new_multiple_choice_qu_14718(self):
        """Create a brand new multiple choice question.

        Steps:

        Go to https://exercises-qa.openstax.org/
        Click on the 'Login' button
        Enter the content analyst account
        Click on the 'Sign in' button

        Click "Write a new exercise"
        Click on the "Multiple Choice" radio button if it is not already
        selected
        Fill out the required fields
        Click "Publish"


        Expected Result:

        The user gets a confirmation that says "Exercise [exercise ID] has
        published successfully"

        """
        self.ps.test_updates['name'] = 't2.11.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.011',
            '14718'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14715 - 012 - Content Analyst | Preserve the order of choices for
    # questions where the choice order matters
    @pytest.mark.skipif(str(14715) not in TESTS, reason='Excluded')  # NOQA
    def test_content_analyst_preserve_the_order_of_choices_for_que_14715(self):
        """Preserve order of choices for questions where choice order matters.

        Steps:

        Click "Write a new exercise"
        Click on the box "Order Matters"


        Expected Result:

        The user is able to preserve the order of choices

        """
        self.ps.test_updates['name'] = 't2.11.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.012',
            '14715'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14717 - 013 - Content Analyst | Edit detailed solutions
    @pytest.mark.skipif(str(14717) not in TESTS, reason='Excluded')  # NOQA
    def test_content_analyst_edit_detailed_solutions_14717(self):
        """Edit detailed solutions.

        Steps:

        Click "Search"
        Enter the desired exercise ID
        Scroll down to "Detailed Solutions"
        Edit text in the "Detailed Solutions" text box
        Click "Publish"


        Expected Result:

        The user is able to edit detailed solutions and the changes are
        reflected in the box to the right

        """
        self.ps.test_updates['name'] = 't2.11.013' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.013',
            '14717'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14710 - 014 - Content Analyst | Reference an embedded video
    @pytest.mark.skipif(str(14710) not in TESTS, reason='Excluded')  # NOQA
    def test_content_analyst_reference_an_embedded_video_14710(self):
        """Reference an embedded video.

        Steps:

        Click "Write a new exercise"
        Enter the video embed link into the Question Stem text box


        Expected Result:

        The video should appear in the box to the right

        """
        self.ps.test_updates['name'] = 't2.11.014' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.014',
            '14710'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14711 - 015 - Content Analyst | Pull out the dropdown tags
    @pytest.mark.skipif(str(14711) not in TESTS, reason='Excluded')  # NOQA
    def test_content_analyst_pull_out_the_dropdown_tags_14711(self):
        """Pull out the dropdown tags.

        Steps:

        Click "Write a new exercise"
        Click "Tags"
        Click "Question Type," "DOK," "Blooms," and/or "Time"


        Expected Result:

        The user is able to pull out the dropdown tags

        """
        self.ps.test_updates['name'] = 't2.11.015' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.015',
            '14711'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14712 - 016 - Content Analyst | Use drop down choices from tagging legend
    @pytest.mark.skipif(str(14712) not in TESTS, reason='Excluded')  # NOQA
    def test_content_analyst_use_dropdown_choices_from_tagging_leg_14712(self):
        """Use drop down choices from tagging legend.

        Steps:

        Click "Write a new exercise"
        Click "Tags"
        Click "Question Type," "DOK," "Blooms," and/or "Time"
        Select a choice from the dropdown tags

        Expected Result:

        The user is able to select a specific tag from the dropdown choices and
        the tag(s) appear in the box to the right

        """
        self.ps.test_updates['name'] = 't2.11.016' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.016',
            '14712'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14723 - 017 - Content Analyst | Specify whether context is required for a
    # question
    @pytest.mark.skipif(str(14723) not in TESTS, reason='Excluded')  # NOQA
    def test_content_analyst_specify_whether_context_is_required_14723(self):
        """Specify whether context is required for a question.

        Steps:

        Click "Write a new exercise"
        Click "Tags"
        Check the box that says "Requires Context"

        Expected Result:

        The tag "requires-contact:true" appears in the box to the right

        """
        self.ps.test_updates['name'] = 't2.11.017' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.017',
            '14723'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14722 - 018 - Content Analyst | Add context to a question
    @pytest.mark.skipif(str(14722) not in TESTS, reason='Excluded')  # NOQA
    def test_content_analyst_add_context_to_a_question_14722(self):
        """Add context to a question.

        Steps:

        Click "Write a new exercise"
        Click "Tags"
        Check the box that says "Requires Context"
        Click "+" next to "CNX Module"
        Enter the CNX Module number

        Expected Result:

        The user is able to add context to a question

        """
        self.ps.test_updates['name'] = 't2.11.018' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.018',
            '14722'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14705 - 019 - Content Analyst | Add the image
    @pytest.mark.skipif(str(14705) not in TESTS, reason='Excluded')  # NOQA
    def test_content_analyst_add_the_image_14705(self):
        """Add the image.

        Steps:

        Click "Write a new exercise"
        Enter text into Question Stem, Distractor, and Detailed Solution
        Click "Save Draft"
        Click "Assets"
        Click "Add new image"
        Select an image

        Expected Result:

        The image and the options "Choose different image" and "Upload" should
        come up

        """
        self.ps.test_updates['name'] = 't2.11.019' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.019',
            '14705'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14704 - 020 - Content Analyst | Upload an image
    @pytest.mark.skipif(str(14705) not in TESTS, reason='Excluded')  # NOQA
    def test_content_analyst_add_the_image_14705(self):
        """Add the image.

        Steps:

        Click "Write a new exercise"
        Enter text into Question Stem, Distractor, and Detailed Solution
        Click "Save Draft"
        Click "Assets"
        Click "Add new image"
        Select an image
        Click "Upload"


        Expected Result:

        There should be a URL and a "Delete" button

        """
        self.ps.test_updates['name'] = 't2.11.020' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.020',
            '14704'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14703 - 021 - Content Analyst | Show uploaded URL in the HTML snippet
    @pytest.mark.skipif(str(14703) not in TESTS, reason='Excluded')  # NOQA
    def test_content_analyst_show_uploaded_url_in_the_html_snippet_14703(self):
        """Show uploaded URL in the HTML snippet.

        Steps:

        Click "Write a new exercise"
        Enter text into Question Stem, Distractor, and Detailed Solution
        Click "Save Draft"
        Click "Assets"
        Click "Add new image"
        Select an image
        Click "Upload"


        Expected Result:

        The user is presented with uploaded URL in the HTML snippet

        """
        self.ps.test_updates['name'] = 't2.11.021' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.021',
            '14703'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 15903 - 022 - Content Analyst | Delete an image
    @pytest.mark.skipif(str(15903) not in TESTS, reason='Excluded')  # NOQA
    def test_content_analyst_delete_an_image_15903(self):
        """Delete an image.

        Steps:

        Click "Write a new exercise"
        Enter text into Question Stem, Distractor, and Detailed Solution
        Click "Save Draft"
        Click "Assets"
        Click "Add new image"
        Select an image
        Click "Upload"
        Click "Delete"


        Expected Result:

        The image is deleted

        """
        self.ps.test_updates['name'] = 't2.11.022' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.022',
            '15903'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14719 - 023 - Teacher | Create a brand new multiple choice question
    @pytest.mark.skipif(str(14719) not in TESTS, reason='Excluded')  # NOQA
    def test_content_analyst_delete_an_image_14719(self):
        """Create a brand new multiple choice question.

        Steps:

        Go to https://exercises-qa.openstax.org/
        Click on the 'Login' button
        Enter the teacher account in the username and password text boxes
        Click on the 'Sign in' button

        Click "Write a new exercise"
        Click on the "Multiple Choice" radio button if it is not already
        selected
        Fill out the required fields
        Click "Publish"


        Expected Result:

        The user gets a confirmation that says "Exercise [exercise ID] has
        published successfully"

        """
        self.ps.test_updates['name'] = 't2.11.023' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.023',
            '14719'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14714 - 024 - Teacher | Preserve the order of choices for questions where
    # the choice order matters
    @pytest.mark.skipif(str(14714) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_preserve_the_order_of_choices_for_questions_14714(self):
        """Preserve order of choices for questions where choice order matters.

        Steps:

        Click "Write a new exercise"
        Click on the box "Order Matters"



        Expected Result:

        The user is able to preserve the order of choices

        """
        self.ps.test_updates['name'] = 't2.11.024' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.024',
            '14714'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14716 - 025 - Teacher | Edit detailed solutions
    @pytest.mark.skipif(str(14716) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_edit_detailed_solutions_14716(self):
        """Edit detailed solutions.

        Steps:

        Click "Search"
        Enter the desired exercise ID
        Scroll down to "Detailed Solutions"
        Edit text in the "Detailed Solutions" text box
        Click "Publish"


        Expected Result:

        The user is able to edit detailed solutions and the change is reflected
        in the box to the right

        """
        self.ps.test_updates['name'] = 't2.11.025' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.025',
            '14716'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14709 - 026 - Teacher | Reference an embedded video
    @pytest.mark.skipif(str(14709) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_reference_an_embedded_video_14709(self):
        """Reference an embedded video.

        Steps:

        Click "Search"
        Enter the desired exercise ID
        Scroll down to "Detailed Solutions"
        Edit text in the "Detailed Solutions" text box
        Click "Publish"


        Expected Result:

        The user is able to edit detailed solutions and the change is reflected
        in the box to the right

        """
        self.ps.test_updates['name'] = 't2.11.026' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.026',
            '14709'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14713 - 027 - Teacher | Use drop down choices from tagging legend
    @pytest.mark.skipif(str(14713) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_use_dropdown_choices_from_tagging_legend_14713(self):
        """Use drop down choices from tagging legend.

        Steps:

        Click "Write a new exercise"
        Click "Tags"
        Click "Question Type," "DOK," "Blooms," and/or "Time"
        Select a choice from the dropdown tags



        Expected Result:

        The user is able to select a specific tag from the dropdown choices and
        the tags appear on the box to the right

        """
        self.ps.test_updates['name'] = 't2.11.027' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.027',
            '14713'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14721 - 028 - Teacher | Specify whether context is required for question
    @pytest.mark.skipif(str(14721) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_specify_whether_context_is_required_for_quest_14721(self):
        """Specify whether context is required for a question.

        Steps:

        Click "Write a new exercise"
        Click "Tags"
        Check the box that says "Requires Context"


        Expected Result:

        The user is able to specify whether context is required for a question
        and the tag "requires-context:true" appears in the box to the right

        """
        self.ps.test_updates['name'] = 't2.11.028' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.028',
            '14721'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14720 - 029 - Teacher | Add context to a question
    @pytest.mark.skipif(str(14720) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_add_context_to_a_question_14720(self):
        """Add context to a question.

        Steps:

        Click "Write a new exercise"
        Click "Tags"
        Check the box that says "Requires Context"
        Click "+" next to "CNX Module"
        Enter the CNX Module number


        Expected Result:

        The user is able to add context to a question

        """
        self.ps.test_updates['name'] = 't2.11.029' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.029',
            '14720'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14707 - 030 - Teacher | Add an image
    @pytest.mark.skipif(str(14707) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_add_an_image_14707(self):
        """Add an image.

        Steps:

        Click "Write a new exercise"
        Enter text into Question Stem, Distractor, and Detailed Solution
        Click "Save Draft"
        Click "Assets"
        Click "Add new image"
        Select an image


        Expected Result:

        The image and the options "Choose different image" and "Upload" should
        come up

        """
        self.ps.test_updates['name'] = 't2.11.030' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.030',
            '14707'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14706 - 031 - Teacher | Upload an image
    @pytest.mark.skipif(str(14706) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_upload_an_image_14706(self):
        """Upload an image.

        Steps:

        Click "Write a new exercise"
        Enter text into Question Stem, Distractor, and Detailed Solution
        Click "Save Draft"
        Click "Assets"
        Click "Add new image"
        Select an image
        Click "Upload"


        Expected Result:

        There should be a URL and a "Delete" button

        """
        self.ps.test_updates['name'] = 't2.11.031' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.031',
            '14706'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 15902 - 032 - Teacher | Delete an image
    @pytest.mark.skipif(str(15902) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_delete_an_image_15902(self):
        """Delete an image.

        Steps:

        Click "Write a new exercise"
        Enter text into Question Stem, Distractor, and Detailed Solution
        Click "Save Draft"
        Click "Assets"
        Click "Add new image"
        Select an image
        Click "Upload"
        Click "Delete"


        Expected Result:

        The image is deleted

        """
        self.ps.test_updates['name'] = 't2.11.032' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.032',
            '15902'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14724 - 033 - Content Analyst | Add a vocabulary question
    @pytest.mark.skipif(str(14724) not in TESTS, reason='Excluded')  # NOQA
    def test_content_analyst_add_a_vocabulary_question_14724(self):
        """Add a vocabulary question.

        Steps:

        Click "Write a new exercise"
        Click "New Vocabulary Term" from the header
        Fill out the required fields
        Click "Save Draft"
        Click "Publish"


        Expected Result:

        The "Publish" button is whited out and the exercise ID appears in the
        box to the right

        """
        self.ps.test_updates['name'] = 't2.11.033' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.033',
            '14724'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14725 - 034 - Content Analyst | Edit a vocabulary question
    @pytest.mark.skipif(str(14725) not in TESTS, reason='Excluded')  # NOQA
    def test_content_analyst_edit_a_vocabulary_question_14725(self):
        """Edit a vocabulary question.

        Steps:

        Click "Write a new exercise"
        Click "New Vocabulary Term" from the header
        Enter text into "Key Term," "Key Term Definition," and "Distractors"
        Click "Save Draft"
        Click "Publish"
        Copy the exercise ID
        Click "Back"
        Paste the exercise ID
        Enter new text into the aforementioned text boxes and the rest of the
        fields if desired
        Click "Save Draft"
        Click "Publish"



        Expected Result:

        The user is able to edit and save a vocabulary question

        """
        self.ps.test_updates['name'] = 't2.11.034' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.034',
            '14725'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14735 - 035 - Content Analyst | Review a vocabulary question
    @pytest.mark.skipif(str(14735) not in TESTS, reason='Excluded')  # NOQA
    def test_content_analyst_review_a_vocabulary_question_14735(self):
        """Review a vocabulary question.

        Steps:

        Click "Search"
        Enter the desired exercise ID


        Expected Result:

        The vocabulary question loads and user is able to review it

        """
        self.ps.test_updates['name'] = 't2.11.035' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.035',
            '14735'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14799 - 036 - Teacher | Add vocabulary question
    @pytest.mark.skipif(str(14799) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_add_a_vocabulary_question_14799(self):
        """Add vocabulary question.

        Steps:

        Go to https://exercises-qa.openstax.org/
        Click on the 'Login' button
        Enter the teacher account in the username and password text boxes
        Click on the 'Sign in' button

        Click "Write a new exercise"
        Click "New Vocabulary Term" from the header
        Fill in the required fields
        Click "Save Draft"
        Click "Publish"

        Expected Result:

        The "Publish" button is whited out and the exercise ID appears in the
        box to the right

        """
        self.ps.test_updates['name'] = 't2.11.036' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.036',
            '14799'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14727 - 037 - Teacher | Edit vocabulary questions
    @pytest.mark.skipif(str(14727) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_edit_vocabulary_questions_14727(self):
        """Edit vocabulary questions.

        Steps:

        Click "Write a new exercise"
        Click "New Vocabulary Term" from the header
        Enter text into "Key Term," "Key Term Definition," and "Distractors"
        Click "Save Draft"
        Click "Publish"
        Copy the exercise ID
        Click "Back"
        Paste the exercise ID
        Enter new text into the aforementioned text boxes and the rest of the
        fields if desired
        Click "Save Draft"
        Click "Publish"


        Expected Result:

        The user is able to edit and save a vocabulary question

        """
        self.ps.test_updates['name'] = 't2.11.037' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.037',
            '14727'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14734 - 038 - Teacher | Review vocabulary questions
    @pytest.mark.skipif(str(14734) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_review_vocabulary_questions_14734(self):
        """Review vocabulary questions.

        Steps:

        Click "Search"
        Enter the desired exercise ID


        Expected Result:

        The vocabulary question loads and user is able to review it

        """
        self.ps.test_updates['name'] = 't2.11.038' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.038',
            '14734'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14728 - 039 - Content Analyst | "Show 2-Step Preview" checkbox and free-
    # response or multiple-choice are displaye
    @pytest.mark.skipif(str(14728) not in TESTS, reason='Excluded')  # NOQA
    def test_content_analyst_show_2_step_preview_checkbox_and_free_14728(self):
        """Review vocabulary questions.

        Steps:

        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the content analyst user account in the username and password
        text boxes
        Click on the 'Sign in' button

        Click "QA Content" from the user menu
        Click on a non-introductory section
        Check the box that says "Show 2-Step Preview"


        Expected Result:

        The user is presented with a free response text box and multiple choice
        question

        """
        self.ps.test_updates['name'] = 't2.11.039' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.039',
            '14728'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14729 - 040 - Content Analyst | Multiple choice and True/False do not
    # have a free response
    @pytest.mark.skipif(str(14729) not in TESTS, reason='Excluded')  # NOQA
    def test_content_analyst_multiple_choice_and_true_false_do_not_14729(self):
        """Review vocabulary questions.

        Steps:

        Click "QA Content" from the user menu
        Click on a non-introductory section
        Check the box that says "Show 2-Step Preview"
        Scroll to a multiple choice only question or true/false question


        Expected Result:

        If the question is only multiple choice or true/false, it does not have
        a free response box

        """
        self.ps.test_updates['name'] = 't2.11.040' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.040',
            '14729'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14798 - 041 - Content Analyst | Filter assessments by type
    @pytest.mark.skipif(str(14798) not in TESTS, reason='Excluded')  # NOQA
    def test_content_analyst_filter_assessments_by_type_14798(self):
        """Filter assessments by type.

        Steps:

        Click "QA Content" from the user menu
        Click on a non-introductory section
        Click "Exercise Types"
        Select the options that you do not want


        Expected Result:

        The user is able to filter assessments by type

        """
        self.ps.test_updates['name'] = 't2.11.041' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.041',
            '14798'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14730 - 042 - Content Analyst | View human-created question IDs
    @pytest.mark.skipif(str(14730) not in TESTS, reason='Excluded')  # NOQA
    def test_content_analyst_view_human_created_question_ids_14730(self):
        """View human-created question IDs.

        Steps:


        Expected Result:


        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    # 14731 - 043 - Content Analyst | Hide the non-visible tags for faculty and
    # students
    @pytest.mark.skipif(str(14731) not in TESTS, reason='Excluded')  # NOQA
    def test_content_analyst_hide_the_nonvisible_tags_for_faculty_14731(self):
        """Hide the non-visible tags for faculty and students.

        Steps:

        Click "QA Content" from the user menu
        Click on a non-introductory section

        Open an incognito window
        Sign in as teacher01
        Click on the same course that you are viewing in QA Content as content
        analyst
        Go to Question Library
        Click on the same section that you are viewing in QA Content as content
        analyst
        Pick an assessment


        Expected Result:

        The assessment in the teacher view should not have the tags that the
        assessment has in QA Content view

        """
        self.ps.test_updates['name'] = 't2.11.043' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.043',
            '14731'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14732 - 044 - Content Analyst | View all tags in the Assesment QA View
    @pytest.mark.skipif(str(14732) not in TESTS, reason='Excluded')  # NOQA
    def test_content_analyst_view_all_tags_in_assessment_qa_view_14732(self):
        """View all tags in the Assesment QA View.

        Steps:

        Click "QA Content" from the user menu
        Click on a non-introductory section
        Scroll/look to the bottom of an assessment card


        Expected Result:

        The user is presented with all the tags for an assessment

        """
        self.ps.test_updates['name'] = 't2.11.044' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.044',
            '14732'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14736 - 045 - Content Analyst | Create a new multi-part question
    @pytest.mark.skipif(str(14736) not in TESTS, reason='Excluded')  # NOQA
    def test_content_analyst_create_a_new_multipart_question_14736(self):
        """Create a new multi-part question.

        Steps:

        Click "Write a new exercise"
        Check the box that says "Exercise contains multiple parts"
        Fill out the required fields
        Click "Save Draft"
        Click "Publish"


        Expected Result:

        The user gets a confirmation that says "Exercise [exercise ID] has
        published successfully"

        """
        self.ps.test_updates['name'] = 't2.11.045' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.045',
            '14736'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14737 - 046 - Teacher | Create a new multi-part question
    @pytest.mark.skipif(str(14737) not in TESTS, reason='Excluded')  # NOQA
    def test_teacher_create_a_new_multipart_question_14737(self):
        """Create a new multi-part question.

        Steps:

        Go to https://exercises-qa.openstax.org/
        Click on the 'Login' button
        Enter the teacher account in the username and password text boxes
        Click on the 'Sign in' button

        Click "Write a new exercise"
        Check the box that says "Exercise contains multiple parts"
        Fill out the required fields
        Click "Publish"


        Expected Result:

        The user gets a confirmation that says "Exercise [exercise ID] has
        published successfully"

        """
        self.ps.test_updates['name'] = 't2.11.046' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            't2',
            't2.11',
            't2.11.046',
            '14737'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True

    # 14738 - 047 - Editor | View a list of all the exercises and vocabulary
    # I have access to
    @pytest.mark.skipif(str(14738) not in TESTS, reason='Excluded')  # NOQA
    def test_editor_view_a_list_of_all_the_exercises_and_vocab_14738(self):
        """View a list of all the exercises and vocabulary I have access to.

        Steps:

        Go to https://exercises-qa.openstax.org/
        Click on the 'Login' button
        Enter the content analyst account in username and password textboxes
        Click on the 'Sign in' button

        Click "Exercise List"


        Expected Result:

        The user is presented with a list of all the exercises and vocabulary


        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)
