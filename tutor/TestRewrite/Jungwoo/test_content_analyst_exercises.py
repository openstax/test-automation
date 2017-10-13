"""Exercises: Content Analyst"""

import datetime
import inspect
import json
import os
import pytest
import random
import unittest

from pastasauce import PastaSauce, PastaDecorator
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
        162262, 162263, 162264
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
            self.content = ContentQA(
                use_env_vars=True,
                pasta_user=self.ps,
                capabilities=self.desired_capabilities
            )
        else:
            self.content = ContentQA(
                use_env_vars=True
            )

    def tearDown(self):
        """Test destructor."""
        if not LOCAL_RUN:
            self.ps.update_job(
                job_id=str(self.teacher.driver.session_id),
                **self.ps.test_updates
            )
        try:
            self.content.delete()
        except:
            pass

   @pytest.mark.skipif(str(162262) not in TESTS, reason='Excluded')
    def test_creating_multiple_choice_questions_162262(self):
        """
        Go to exercises qa
        Log in as a content analyst
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
        ***User is able to select a specific tag and the tag(s) appear in the box to the right***

        Check the box that says "Requires Context"
        ***The user is able to specify whether context is required for a question and the tag 
        "requires-context:true" appears in the box to the right***

        Click "+" next to "CNX Module"
        Enter the CNX Module number
        Click "Save Draft"
        Click "Assets"
        Click "Add new image"
        Select an image
        ***The image and the options "Choose different image" and "Upload" should come up***

        Click "Upload"
        ***There shoould be a URL and a "Delete" button)***
        ***The user is presented with uploaded URL in the HTML snippet***
        Click "Delete"
        ***The image is deleted***

        Click "Save Draft", then click "Publish"
        ***Observe message: "Exercise [exercise ID] has published successfully")***

        Click "Search"
        Enter the desired exercise ID
        Scroll down to "Detailed Solutions"
        Edit text in the "Detailed Solutions" text box
        Click "Publish"

        Expected Result:

        ***The user is able to edit detailed solutions and the changes are in the box to the right***

        Corresponding test cases: T2.11 010-021

        https://trello.com/c/6XGtFvPm/88-creating-multiple-choice-questions
        """

        self.ps.test_updates['name'] = 'exercises_new_exercise_content_analyst_162262' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['exercises', 'new_exercise', 'content_analyst', '162262']
        self.ps.test_updates['passed'] = False

        self.teacher.login(url=os.getenv('EXERCISES_QA'),
            username=os.getenv('CONTENT_USER'),
            password=os.getenv('CONTENT_PASSWORD')
        )
        #click create a new question
        self.teacher.find(By.CSS_SELECTOR, "a[href*='new']").click()
        textboxes = self.teacher.find_all(By.CSS_SELECTOR,".question>div>textarea")
        #put embed link into Question Stem text box
        embedlink='<iframe width="560" height="315" src="https://www.youtube.com/embed/'
        embedlink+='QnQe0xW_JY4" frameborder="0" allowfullscreen></iframe>"'
        textboxes[0].send_keys(embedlink)
        #verify that the video appears in the box to the right
        self.teacher.find(By.CSS_SELECTOR, "iframe")
        #fill out the required fields
        answers = self.teacher.find_all(By.CSS_SELECTOR,".correct-answer>textarea")
        answers[0].send_keys('answer numero uno')
        answers[1].send_keys('answer numero dos')
        #textboxes[1].send_keys('answer numero tres')
        #click on Order Matters checkbox
        self.teacher.find(By.CSS_SELECTOR,"#input-om").click()

        #Click on Tabs tag
        self.teacher.find(By.CSS_SELECTOR,"#exercise-parts-tab-tags").click()
        #verify that all the dropdowns are clickable
        tagoptions = self.teacher.find_all(By.CSS_SELECTOR, ".form-control")
        for num in range(len(tagoptions)):
            expect.element_to_be_clickable(tagoptions[num])
        #choose an option from a dropdown
        tagoptions[1].click()
        self.teacher.find_all(By.CSS_SELECTOR,"option")[1].click()
        #verify that the tag appears in the box to the right
        self.teacher.find(
            By.XPATH, 
            "//*[@class='exercise-tag' and contains(text(),'type')]"
        )
        self.teacher.find(By.CSS_SELECTOR,".tag>input").click()
        self.teacher.find(
            By.XPATH,
            "//*[@class='exercise-tag' and contains(text(),'context:true')]"
        )
        #click "+" next to CNX Module
        self.teacher.find_all(By.CSS_SELECTOR,".fa.fa-plus-circle")[2].click()
        #put in a CNX module
        self.teacher.find(
            By.XPATH, 
            ".//*[@class='form-control' and @placeholder]"
            ).send_keys('12345678-1234-5788-9123-456798123456')

        #click save draft
        self.teacher.find(By.CSS_SELECTOR,".async-button.draft.btn.btn-info").click()
        #click assets tab
        self.teacher.find(By.CSS_SELECTOR,"#exercise-parts-tab-assets").click()
        # Choose image. This is all local -- prob have to edit for diff computer
        IMAGEPATH = "/Users/openstax10/desktop/bee_clip_art_18782.jpg"
        self.teacher.find(By.ID,"file").send_keys(IMAGEPATH)
        # check that Choose different image and Upload buttons are present
        self.teacher.find(By.XPATH,'.//*[contains(text(),"Choose different image")]')
        self.teacher.find(By.XPATH,'.//*[contains(text(),"Upload")]').click()
        self.teacher.page.wait_for_page_load()
        # check if uploaded url is present
        self.teacher.find(By.CSS_SELECTOR,".copypaste")
        # check that delete button is present and click it
        self.teacher.find(By.XPATH,'.//*[contains(text(),"Delete")]').click()
        self.teacher.sleep(1)

        # click publish
        self.teacher.find(By.CSS_SELECTOR,'.async-button.publish.btn.btn-primary').click()
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
        self.teacher.find(By.CSS_SELECTOR,'.btn.btn-danger.back.btn.btn-default').click()
        # enter ID into field
        self.teacher.find(By.CSS_SELECTOR,'.form-control').send_keys(ID)
        self.teacher.find(By.CSS_SELECTOR,'.btn.btn-default.load').click()
        # edit detailed solution
        self.teacher.find(By.XPATH, "//div[4]/textarea").send_keys('hello edited')
        detailedsol = self.teacher.find(By.CSS_SELECTOR,
            '.openstax-has-html.solution'
            ).get_attribute('innerHTML')
        # check that the text you inputted into detailed solution is in the 
        # box to the right
        assert('hello edited' == detailedsol)
        
        self.ps.test_updates['passed'] = True

    @pytest.mark.skipif(str(162263) not in TESTS, reason='Excluded')
    def test_creating_vocabulary_questions_162263(self):
        """
        Go to exercises qa
        Log in as a content analyst
        Click "Write a new exercise"
        Click "New Vocabulary Term" from the header
        Fill out required fields
        Click "Save Draft"
        Click "Publish"
        ***The "Publish" button is whited out and the exercise ID appears in the box to the right***

        Click "Search"
        Enter the desired exercise ID
        ***The vocabulary question loads and user is able to review it***

        Enter next text into "Key Term", "Key Term Definition", and "Distractors"
        Click "Save Draft"
        Click "Publish"

        Expected result:

        ***The user is able to edit and save a vocabulary question***

        Corresponding test cases: T2.11 032-034

        https://trello.com/c/BAcghIsM/92-creating-vocabulary-questions
        """

        self.ps.test_updates['name'] = 'exercises_new_exercise_content_analyst_162263' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['exercises', 'new_exercise', 'content_analyst', '162263']
        self.ps.test_updates['passed'] = False

        # logging in with these credentials 
        self.teacher.login(url=os.getenv('EXERCISES_QA'),
            username=os.getenv('CONTENT_USER'),
            password=os.getenv('CONTENT_PASSWORD')
        )
        # click create a new question
        self.teacher.find(By.CSS_SELECTOR, "a[href*='new']").click()
        # click New vocabulary question
        self.teacher.find(By.CSS_SELECTOR,".btn.btn-success.vocabulary.blank").click()
        # enter testing as the key term
        self.teacher.find(By.CSS_SELECTOR,"#key-term").send_keys('testing')
        # enter 'ignore' as the definition
        self.teacher.find(By.CSS_SELECTOR,"#key-term-def").send_keys('ignore')
        # click save draft
        self.teacher.find(By.CSS_SELECTOR,".async-button.draft.btn.btn-info").click()
        # click publish
        self.teacher.find(By.CSS_SELECTOR,".async-button.publish.btn.btn-primary").click()
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
        self.teacher.find(By.CSS_SELECTOR,".form-control").send_keys(exerciseid)
        # click search
        self.teacher.find(By.CSS_SELECTOR,".btn.btn-default.load").click()
        # confirm key term value is what was inputted originally
        keyterm = self.teacher.find(By.CSS_SELECTOR,"#key-term").get_attribute('value')
        assert(keyterm == 'testing')
        # write something else for key term
        keyterm = self.teacher.find(By.CSS_SELECTOR,"#key-term")
        keyterm.send_keys(Keys.BACKSPACE*len('testing   '))
        self.teacher.sleep(.2)
        keyterm.send_keys('test edit')
        # confirm key term def value is what was inputted oirignally
        keytermdef = self.teacher.find(By.CSS_SELECTOR,'#key-term-def').get_attribute('value')
        assert(keytermdef == 'ignore')
        # write something else for key term def
        keytermdef = self.teacher.find(By.CSS_SELECTOR,"#key-term-def")
        keytermdef.send_keys(Keys.BACKSPACE*len('ignore   '))
        self.teacher.sleep(.2)
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
            './/*[@class="btn btn-primary" and contains(text(),"Publish")]').click()
        self.teacher.sleep(2)
        # get new exercise id 
        exerciseid = self.teacher.find_all(
            By.CSS_SELECTOR,
            ".exercise-tag")[3].get_attribute('innerHTML')[4:]
        # click search
        self.teacher.find(By.XPATH, ".//*[contains(text(),'Search')]").click()
        # search the exercise id
        self.teacher.find(By.CSS_SELECTOR,".form-control").send_keys(exerciseid)
        self.teacher.find(By.CSS_SELECTOR,".btn.btn-default.load").click()
        # verify that the value in key term is what was inputted previously
        keyterm = self.teacher.find(By.CSS_SELECTOR,"#key-term").get_attribute('value')
        assert(keyterm == 'test edit')

        self.ps.test_updates['passed'] = True

    @pytest.mark.skipif(str(162264) not in TESTS, reason='Excluded')
    def test_creating_multipart_question_162264(self):
        """
        Go to exercises qa
        Log in as a content analyst
        Click "Write a new exercise"
        Check the box that says "Exercise contains multiple parts" 
        Fill out the required fields
        Click "Publish"

        Expected result:

        ***The user gets a confirmation that says "Exercise [exercise ID] has published successfully"***

        Corresponding test case: T2.11 044, 046

        https://trello.com/c/L1RjXiSx/160-creating-multi-part-questions-without-detailed-solutions
        """
        self.ps.test_updates['name'] = 'exercises_new_exercise_content_analyst_162264' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['exercises', 'new_exercise', 'content_analyst', '162264']
        self.ps.test_updates['passed'] = False

        # logging in with these credentials 
        self.teacher.login(url=os.getenv('EXERCISES_QA'),
            username=os.getenv('CONTENT_USER'),
            password=os.getenv('CONTENT_PASSWORD')
        )
        # click create a new question
        self.teacher.find(By.CSS_SELECTOR, "a[href*='new']").click()
        # click "Exercise contains multiple parts"
        self.teacher.find(By.CSS_SELECTOR,'#mpq-toggle').click()
        # write in something for question stem
        self.teacher.find(By.CSS_SELECTOR,'.question>div>textarea').send_keys('test')
        # write in something for Distractor
        self.teacher.find(By.CSS_SELECTOR,'.correct-answer>textarea').send_keys('ignore')
        # click tab "question 2"
        self.teacher.find(By.CSS_SELECTOR,'#exercise-parts-tab-question-1').click()
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
        self.teacher.find(By.CSS_SELECTOR,'.async-button.draft.btn.btn-info').click()
        # click publish
        self.teacher.find(
            By.CSS_SELECTOR,
            '.async-button.publish.btn.btn-primary').click()
        self.teacher.sleep(1)
        # confirm publish
        self.teacher.find(
            By.XPATH,
            ".//*[@class='btn btn-primary' and contains(text(),'Publish')]"
        ).click()
        # confirm message appears
        self.teacher.find(By.CSS_SELECTOR,'.modal-body>b')

        self.ps.test_updates['passed'] = True


