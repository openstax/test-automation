"""Exercises: Teacher"""

# import datetime
import inspect
import json
import os
import pytest
import random
import unittest

from pastasauce import PastaSauce, PastaDecorator
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.common.keys import Keys
from staxing.helper import Teacher

basic_test_env = json.dumps([
    {
        'platform': 'Windows 10',
        'browserName': 'chrome',
        'version': 'latest',
        'screenResolution': "1024x768",
    }
])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
LOCAL_RUN = os.getenv('LOCALRUN', 'false').lower() == 'true'
TESTS = os.getenv(
    'CASELIST',
    str([
        162257, 162258, 162259, 162260, 162261
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestExercisesTeacher(unittest.TestCase):
    """Tutor | Teacher"""

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
        # self.teacher.login(url='http://exercises-qa.openstax.org')

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

    @pytest.mark.skipif(str(162257) not in TESTS, reason='Excluded')
    def test_creating_true_and_false_question_162257(self):
        """
        Go to exercises qa
        Log in as a teacher
        Click "Write a new exercise"
        Click "True/False" button

        Expected result:

        ***User is presented with a page where a True/False question can be
        created***

        Corresponding test cases: T2.12 001, 002

        https://trello.com/c/w4T1eqT4/66-creating-vocabulary-question-and-true-false
        """

        self.ps.test_updates['name'] = \
            'exercises_new_exercise_teacher_162257' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = \
            ['exercises', 'new_exercise', 'teacher', '162257']
        self.ps.test_updates['passed'] = False

        # log into exercises
        self.teacher.login(
            url=os.getenv('EXERCISES_STAGING'),
            username=os.getenv('CONTENT_USER'),
            password=os.getenv('CONTENT_PASSWORD')
        )
        # Click "Write a new exercise"
        self.teacher.find(By.CSS_SELECTOR, "a[href*='new']").click()
        # Click true false button
        self.teacher.find(By.CSS_SELECTOR, "#input-true-false").click()
        # Verify that user is presented with a page where they can make a true
        # false q
        self.teacher.find(By.CSS_SELECTOR, "textarea")

        self.ps.test_updates['passed'] = True

    @pytest.mark.skipif(str(162258) not in TESTS, reason='Excluded')
    def test_question_library_functionality_162258(self):
        """
        Go to tutor qa
        Log in as a teacher
        Click on a course
        Upper right corner under user menu, click "Question Library"
        Select a section or chapter
        click "Show Questions"
        **User is presented with all the questions for the section or chapter**

        Scroll down to a question, click "Exclude Question"
        ***Observe that Question is excluded***

        Click on the "Reading" tab
        ***Exercises that are only for Reading appear***

        Click on the "Practice" tab @@@@@@@@@@@ Should this be Homework?
        ***Exercises that are only for Practice appear***

        Scroll down
        **Observe that tabs are pinned to the top of the screen when scrolled**

        Click on the section links at the top of the screen
        ***Observe that the screen scrolls to the selected screen***
        Hover over a question and click "Question details"
        Click "Report an error"

        Expected result:

        ***Observe that a new tab with the assessment errata form appears with
        the assessment ID already filled in***

        Corresponding test cases: T2.11 001-007

        https://trello.com/c/SchGDgfL/70-question-library-functionality
        """

        self.ps.test_updates['name'] = \
            'exercises_question_library_teacher_162258' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = \
            ['exercises', 'question_library', 'teacher', '162258']
        self.ps.test_updates['passed'] = False

        self.teacher.login()
        # select random tutor course
        self.teacher.random_course()
        # if Tutor feedback pops up
        try:
            self.teacher.find(
                By.XPATH,
                ".//*[contains(text(),'I won’t be using it')]"
            ).click()
        except:
            pass
        # go to question library
        self.teacher.open_user_menu()
        self.teacher.wait.until(
            expect.visibility_of_element_located((
                By.CSS_SELECTOR,
                "#menu-option-viewQuestionsLibrary"
            ))
        )
        self.teacher.find(
            By.CSS_SELECTOR,
            "#menu-option-viewQuestionsLibrary"
        ).click()
        # 50/50 coin toss. 0 = chapter, 1 = section(s)
        coin = randint(0, 1)
        # reveal sections
        chaptertitles = self.teacher.find_all(
            By.CSS_SELECTOR,
            ".chapter-heading.panel-title>a"
        )
        for num in range(1, len(chaptertitles) - 1):
            self.teacher.scroll_to(chaptertitles[num])
            self.teacher.sleep(.2)
            chaptertitles[num].click()
            self.teacher.sleep(.2)

        # choose a random chapter and all its sections
        if coin == 0:
            chapters = self.teacher.find_all(
                By.CSS_SELECTOR,
                ".chapter-checkbox"
            )
            chapternum = randint(0, len(chapters) - 1)
            self.teacher.scroll_to(chapters[chapternum])
            self.teacher.sleep(0.5)
            chapters[chapternum].click()
            self.teacher.sleep(0.5)

        # choose randomly 1-5 sections from anywhere in the book
        elif coin == 1:
            sections = self.teacher.find_all(
                By.CSS_SELECTOR,
                ".section-checkbox"
            )
            randomlist = random.sample(
                range(len(sections) - 1),
                k=randint(1, 5)
            )
            for num in randomlist:
                self.teacher.scroll_to(sections[num])
                self.teacher.sleep(.5)
                sections[num].click()

        # click show questions
        self.teacher.find(By.CSS_SELECTOR, ".btn.btn-primary").click()
        self.teacher.sleep(5)
        # verify questions show up
        readingq = self.teacher.find_all(By.CSS_SELECTOR, ".controls-overlay")
        excludebutton = self.teacher.find_all(
            By.CSS_SELECTOR,
            ".action.exclude"
        )[0]
        # exclude a random question
        self.teacher.scroll_to(excludebutton)
        self.teacher.sleep(1)
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(excludebutton)
        self.teacher.sleep(1)
        actions.perform()
        self.teacher.sleep(2)
        excludebutton.click()
        self.teacher.sleep(.5)
        self.teacher.find(By.CSS_SELECTOR, ".action.include").click()

        # click reading button
        self.teacher.find(By.CSS_SELECTOR, ".reading.btn.btn-default").click()
        self.teacher.page.wait_for_page_load()
        totalq = self.teacher.find_all(By.CSS_SELECTOR, ".controls-overlay")
        # click homework button
        self.teacher.find(By.CSS_SELECTOR, ".homework.btn.btn-default").click()
        homeworkq = self.teacher.find_all(
            By.CSS_SELECTOR,
            ".controls-overlay"
        )
        assert(len(totalq) > len(readingq))
        assert(len(totalq) > len(homeworkq))

        # Observe that tabs are pinned to the top of the screen when scrolled
        self.teacher.driver.execute_script("window.scrollTo(0, 0);")
        self.teacher.sleep(3)
        self.teacher.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        self.teacher.sleep(3)
        self.teacher.find(By.XPATH, "//div[@class='section active']")
        self.teacher.find(
            By.CSS_SELECTOR,
            ".homework.btn.btn-default"
        )
        self.teacher.find(
            By.CSS_SELECTOR,
            ".reading.btn.btn-default"
        )

        # jumps
        jumps = self.teacher.find_all(
            By.XPATH,
            "//div[@class='sectionizer']/div[@class='section']"
        )
        # Click the section links and verify the page is scrolled
        position = self.teacher.driver.execute_script("return window.scrollY;")
        for button in jumps:
            button.click()
            self.teacher.sleep(1)
            assert(position != self.teacher.driver.execute_script(
                "return window.scrollY;")), \
                'Section link did not jump to next section'
            position = \
                self.teacher.driver.execute_script("return window.scrollY;")
        # details will lead to Question details
        details = self.teacher.find_all(By.CSS_SELECTOR, ".action.details")[0]
        self.teacher.scroll_to(details)
        self.teacher.sleep(1)
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(details)
        self.teacher.sleep(1)
        actions.perform()
        self.teacher.sleep(2)
        details.click()
        self.teacher.find(By.CSS_SELECTOR, ".action.report-error").click()
        details_window = self.teacher.driver.window_handles[1]
        self.teacher.driver.switch_to_window(details_window)
        self.teacher.page.wait_for_page_load()
        self.teacher.sleep(2)
        self.teacher.find(By.CSS_SELECTOR, ".errata-page.page")

        self.ps.test_updates['passed'] = True

    @pytest.mark.skipif(str(162259) not in TESTS, reason='Excluded')
    def test_creating_multiple_choice_questions_162259(self):
        """
        Go to exercises qa
        Log in as a teacher
        Click "Write a new exercise"
        Enter the video embed link into the Question Stem text box
        ***The video should appear in the box to the right***

        Fill out the required fields
        Click on the box "Order Matters"
        ***User is able to preserve the order of choices***
        Click "Tags"
        Click "Question Type", "DOK", "Blooms", and/or "Time"
        ***The user is able to pull out the dropdown tags***

        Select a choice from the dropdown tags
        ***User is able to select a specific tag and the tag(s) appear in the
        box to the right***

        Check the box that says "Requires Context"
        ***The user is able to specify whether context is required for a
        question and the tag
        "requires-context:true" appears in the box to the right***

        Click "+" next to "CNX Module"
        Enter the CNX Module number
        Click "Save Draft"
        Click "Assets"
        Click "Add new image"
        Select an image
        ***The image and the options "Choose different image" and "Upload"
        should come up***

        Click "Upload"
        ***There shoould be a URL and a "Delete" button)***
        ***The user is presented with uploaded URL in the HTML snippet***
        Click "Delete"
        ***The image is deleted***

        Click "Save Draft", then click "Publish"
        ***Observe message: "Exercise [exercise ID] has published
        successfully")***

        Click "Search"
        Enter the desired exercise ID
        Scroll down to "Detailed Solutions"
        Edit text in the "Detailed Solutions" text box
        Click "Publish"

        Expected Result:

        ***The user is able to edit detailed solutions and the changes are in
        the box to the right***

        Corresponding test cases: T2.11 022-031

        https://trello.com/c/n5VmmdyB/83-creating-multiple-choice-questions
        """

        self.ps.test_updates['name'] = \
            'exercises_new_exercise_teacher_162259' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = \
            ['exercises', 'new_exercise', 'teacher', '162259']
        self.ps.test_updates['passed'] = False

        self.teacher.login(
            url=os.getenv('EXERCISES_QA'),
            username=os.getenv('CONTENT_USER'),
            password=os.getenv('CONTENT_PASSWORD')
        )
        # click create a new question
        self.teacher.find(By.CSS_SELECTOR, "a[href*='new']").click()
        textboxes = self.teacher.find_all(
            By.CSS_SELECTOR,
            ".question>div>textarea"
        )
        # put embed link into Question Stem text box
        embedlink = '<iframe width="560" height="315" ' + \
            'src="https://www.youtube.com/embed/'
        embedlink += 'QnQe0xW_JY4" frameborder="0" allowfullscreen></iframe>"'
        textboxes[0].send_keys(embedlink)
        # verify that the video appears in the box to the right
        self.teacher.find(By.CSS_SELECTOR, "iframe")
        # fill out the required fields
        answers = self.teacher.find_all(
            By.CSS_SELECTOR,
            ".correct-answer>textarea"
        )
        answers[0].send_keys('answer numero uno')
        answers[1].send_keys('answer numero dos')
        # textboxes[1].send_keys('answer numero tres')
        # click on Order Matters checkbox
        self.teacher.find(By.CSS_SELECTOR, "#input-om").click()

        # Click on Tabs tag
        self.teacher.find(By.CSS_SELECTOR, "#exercise-parts-tab-tags").click()
        # verify that all the dropdowns are clickable
        tagoptions = self.teacher.find_all(By.CSS_SELECTOR, ".form-control")
        for num in range(len(tagoptions)):
            expect.element_to_be_clickable(tagoptions[num])
        # choose an option from a dropdown
        tagoptions[1].click()
        self.teacher.find_all(By.CSS_SELECTOR, "option")[1].click()
        # verify that the tag appears in the box to the right
        self.teacher.find(
            By.XPATH,
            "//*[@class='exercise-tag' and contains(text(),'type')]"
        )
        self.teacher.find(By.CSS_SELECTOR, ".tag>input").click()
        self.teacher.find(
            By.XPATH,
            "//*[@class='exercise-tag' and contains(text(),'context:true')]"
        )
        # click "+" next to CNX Module
        self.teacher.find_all(By.CSS_SELECTOR, ".fa.fa-plus-circle")[2].click()
        # put in a CNX module
        self.teacher.find(
            By.XPATH,
            ".//*[@class='form-control' and @placeholder]"
            ).send_keys('12345678-1234-5788-9123-456798123456')

        # click save draft
        self.teacher.find(
            By.CSS_SELECTOR,
            ".async-button.draft.btn.btn-info"
        ).click()
        # click assets tab
        self.teacher.find(By.CSS_SELECTOR, "#exercise-parts-tab-assets") \
            .click()
        # Choose image. This is all local -- prob have to edit for diff
        # computer
        IMAGEPATH = "/Users/openstax10/desktop/bee_clip_art_18782.jpg"
        self.teacher.find(By.ID, "file").send_keys(IMAGEPATH)
        # check that Choose different image and Upload buttons are present
        self.teacher.find(
            By.XPATH,
            './/*[contains(text(),"Choose different image")]'
        )
        self.teacher.find(
            By.XPATH,
            './/*[contains(text(),"Upload")]'
        ).click()
        self.teacher.page.wait_for_page_load()
        # check if uploaded url is present
        self.teacher.find(By.CSS_SELECTOR, ".copypaste")
        # check that delete button is present and click it
        self.teacher.find(By.XPATH, './/*[contains(text(),"Delete")]').click()
        self.teacher.sleep(1)

        # click publish
        self.teacher.find(
            By.CSS_SELECTOR,
            '.async-button.publish.btn.btn-primary'
        ).click()
        self.teacher.sleep(1)
        # confirm that you want to publish
        self.teacher.find(
            By.XPATH,
            './/*[@class="btn btn-primary" and contains(text(),"Publish")]'
            ).click()
        self.teacher.sleep(1)
        # close popup window tellign you ID #
        self.teacher.find(
            By.XPATH,
            './/*[@class="btn btn-primary" and contains(text(),"Close")]'
            ).click()
        # get id
        ID = self.teacher.current_url().split('/')[-1]

        # click search button
        self.teacher.find(
            By.CSS_SELECTOR,
            '.btn.btn-danger.back.btn.btn-default'
        ).click()
        # enter ID into field
        self.teacher.find(By.CSS_SELECTOR, '.form-control').send_keys(ID)
        self.teacher.find(By.CSS_SELECTOR, '.btn.btn-default.load').click()
        # edit detailed solution
        self.teacher.find(By.XPATH, "//div[4]/textarea") \
            .send_keys('hello edited')
        detailedsol = self.teacher.find(
            By.CSS_SELECTOR,
            '.openstax-has-html.solution'
        ).get_attribute('innerHTML')
        # check that the text you inputted into detailed solution is in the
        # box to the right
        assert('hello edited' == detailedsol)

        self.ps.test_updates['passed'] = True

    @pytest.mark.skipif(str(162260) not in TESTS, reason='Excluded')
    def test_creating_vocabulary_questions_162260(self):
        """
        Go to exercises qa
        Log in with as a teacher
        Click "Write a new exercise"
        Click "New Vocabulary Term" from the header
        Fill out required fields
        Click "Save Draft"
        Click "Publish"
        ***The "Publish" button is whited out and the exercise ID appears in
        the box to the right***

        Click "Search"
        Enter the desired exercise ID
        ***The vocabulary question loads and user is able to review it***

        Enter next text into "Key Term", "Key Term Definition", and
        "Distractors"
        Click "Save Draft"
        Click "Publish"

        Expected result:

        ***The user is able to edit and save a vocabulary question***

        Corresponding test cases: T2.11 035-037

        https://trello.com/c/3j0K6fp0/89-creating-vocabulary-questions
        """

        self.ps.test_updates['name'] = \
            'exercises_new_exercise_teacher_162260' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = \
            ['exercises', 'new_exercise', 'teacher', '162260']
        self.ps.test_updates['passed'] = False

        # logging in with these credentials
        self.teacher.login(
            url=os.getenv('EXERCISES_QA'),
            username=os.getenv('CONTENT_USER'),
            password=os.getenv('CONTENT_PASSWORD')
        )
        # click create a new question
        self.teacher.find(By.CSS_SELECTOR, "a[href*='new']").click()
        # click New vocabulary question
        self.teacher.find(
            By.CSS_SELECTOR,
            ".btn.btn-success.vocabulary.blank"
        ).click()
        # enter testing as the key term
        self.teacher.find(By.CSS_SELECTOR, "#key-term").send_keys('testing')
        # enter 'ignore' as the definition
        self.teacher.find(By.CSS_SELECTOR, "#key-term-def").send_keys('ignore')
        # click save draft
        self.teacher.find(
            By.CSS_SELECTOR,
            ".async-button.draft.btn.btn-info"
        ).click()
        # click publish
        self.teacher.find(
            By.CSS_SELECTOR,
            ".async-button.publish.btn.btn-primary"
        ).click()
        self.teacher.sleep(1)
        # confirm publish
        self.teacher.find(
            By.XPATH,
            ".//*[@class='btn btn-primary' and contains(text(),'Publish')]"
        ).click()
        self.teacher.sleep(3)
        # get the exercise id
        exerciseid = self.teacher.find_all(
            By.CSS_SELECTOR,
            ".exercise-tag")[3].get_attribute('innerHTML')[4:]

        # go to search
        self.teacher.find(By.XPATH, ".//*[contains(text(),'Search')]").click()
        # search the exercise id
        self.teacher.find(By.CSS_SELECTOR, ".form-control") \
            .send_keys(exerciseid)
        # click search
        self.teacher.find(By.CSS_SELECTOR, ".btn.btn-default.load").click()
        # confirm key term value is what was inputted originally
        keyterm = self.teacher.find(By.CSS_SELECTOR, "#key-term") \
            .get_attribute('value')
        assert(keyterm == 'testing')
        # write something else for key term
        keyterm = self.teacher.find(By.CSS_SELECTOR, "#key-term")
        keyterm.send_keys(Keys.BACKSPACE * len('testing   '))
        self.teacher.sleep(0.2)
        keyterm.send_keys('test edit')
        # confirm key term def value is what was inputted oirignally
        keytermdef = self.teacher.find(By.CSS_SELECTOR, '#key-term-def') \
            .get_attribute('value')
        assert(keytermdef == 'ignore')
        # write something else for key term def
        keytermdef = self.teacher.find(By.CSS_SELECTOR, "#key-term-def")
        keytermdef.send_keys(Keys.BACKSPACE * len('ignore   '))
        self.teacher.sleep(0.2)
        keytermdef.send_keys('ignore edit')
        # fill in value for distractor
        self.teacher.find_all(
            By.CSS_SELECTOR,
            ".form-control")[2].send_keys('im a distractor')
        self.teacher.sleep(3)

        # save as draft
        self.teacher.find(
            By.CSS_SELECTOR,
            ".async-button.draft.btn.btn-info").click()
        self.teacher.sleep(1)
        # publish
        self.teacher.find(
            By.CSS_SELECTOR,
            ".async-button.publish.btn.btn-primary").click()
        # confirm publish
        self.teacher.find(
            By.XPATH,
            './/*[@class="btn btn-primary" and contains(text(),"Publish")]'
        ).click()
        self.teacher.sleep(2)
        # get new exercise id
        exerciseid = self.teacher.find_all(
            By.CSS_SELECTOR,
            ".exercise-tag")[3].get_attribute('innerHTML')[4:]
        # click search
        self.teacher.find(By.XPATH, ".//*[contains(text(),'Search')]").click()
        # search the exercise id
        self.teacher.find(By.CSS_SELECTOR, ".form-control") \
            .send_keys(exerciseid)
        self.teacher.find(By.CSS_SELECTOR, ".btn.btn-default.load").click()
        # verify that the value in key term is what was inputted previously
        keyterm = self.teacher.find(By.CSS_SELECTOR, "#key-term") \
            .get_attribute('value')
        assert(keyterm == 'test edit')

        self.ps.test_updates['passed'] = True

    @pytest.mark.skipif(str(162261) not in TESTS, reason='Excluded')
    def test_creating_multipart_question_162261(self):
        """
        Go to exercises qa
        Log in as a teacher
        Click "Write a new exercise"
        Check the box that says "Exercise contains multiple parts"
        Fill out the required fields
        Click "Publish"

        Expected result:

        ***The user gets a confirmation that says "Exercise [exercise ID] has
        published successfully"***

        Corresponding test case: T2.11 045

        https://trello.com/c/8LnE8Qml/162-creating-multi-part-question
        """
        self.ps.test_updates['name'] = \
            'exercises_new_exercise_teacher_162261' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = \
            ['exercises', 'new_exercise', 'teacher', '162261']
        self.ps.test_updates['passed'] = False

        # logging in with these credentials
        self.teacher.login(
            url=os.getenv('EXERCISES_QA'),
            username=os.getenv('CONTENT_USER'),
            password=os.getenv('CONTENT_PASSWORD')
        )
        # click create a new question
        self.teacher.find(By.CSS_SELECTOR, "a[href*='new']").click()
        # click "Exercise contains multiple parts"
        self.teacher.find(By.CSS_SELECTOR, '#mpq-toggle').click()
        # write in something for question stem
        self.teacher.find(By.CSS_SELECTOR, '.question>div>textarea') \
            .send_keys('test')
        # write in something for Distractor
        self.teacher.find(By.CSS_SELECTOR, '.correct-answer>textarea') \
            .send_keys('ignore')
        # click tab "question 2"
        self.teacher.find(By.CSS_SELECTOR, '#exercise-parts-tab-question-1') \
            .click()
        self.teacher.sleep(1)
        # write in something for question stem
        self.teacher.find_all(
            By.CSS_SELECTOR,
            '.question>div>textarea')[2].send_keys('test2')
        # write in something for Distractor
        self.teacher.find_all(
            By.CSS_SELECTOR,
            '.correct-answer>textarea')[2].send_keys('ignore2')
        # click save draft
        self.teacher.find(
            By.CSS_SELECTOR,
            '.async-button.draft.btn.btn-info'
        ).click()
        # click publish
        self.teacher.find(
            By.CSS_SELECTOR,
            '.async-button.publish.btn.btn-primary'
        ).click()
        self.teacher.sleep(1)
        # confirm publish
        self.teacher.find(
            By.XPATH,
            ".//*[@class='btn btn-primary' and contains(text(),'Publish')]"
        ).click()
        # confirm message appears
        self.teacher.find(By.CSS_SELECTOR, '.modal-body>b')

        self.ps.test_updates['passed'] = True
