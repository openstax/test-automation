"""
System: tutor
Title: working with scores
User(s): teacher
Testrail ID: C148069

Jacob Diaz
7/28/17

Corresponding Case(s):
            t1.23.03 --> 04
            t2.10 - 6,7
            T2.08 - 5--> 11, 14

Progress:
Not all written -->

Work to be done/Questions:
-FIND A WAY TO RESET THE POSITION OF THE WINDOW TO
THE TOPLEFT (BECAUSE YOU'RE GOING TO BE SCROLLING MULTIPLE TIMES --
once for each time you look for a different thing in scores)
-Write the remaining scripts:

-Run and see where it fails -- update and add code

 ### SUPPOSED TO CHECK FOR A PROGRESS BAR... IDK HOW TO DO THIS
        # I'm having trouble finding elements in the student scores table -->
        it would make it easier if each
        # column heading were the parent of the cells underneath it, but I
        don't believe it's so
        # there's no obvious relationship in the DOM between a header and its
        cells?
        # this makes things like seeing if the sort by progress or sort by
        score functions actually work on the
        # items of a column or row

Merge-able with any scripts? If so, which? :

"""
# import inspect
import json
import os
import pytest
import unittest

from pastasauce import PastaSauce, PastaDecorator
# from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as expect
# from selenium.webdriver.support import expected_conditions as expect
# from staxing.assignment import Assignment

# select user types: Admin, ContentQA, Teacher, and/or Student
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

    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestScoresReportingTeacher(unittest.TestCase):
    def setUp(self):
        """Pretest Settings"""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.teacher = Teacher(
            use_env_vars=True,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities
        )
        self.teacher.login()

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

    @pytest.mark.skipif(str(1) not in TESTS, reason='Excluded')
    def test_score_stuff(self):
        """
        Go to https://tutor-qa.openstax.org/
            Login with the account [ teacher01 | password]
            If the user has more than one course, select a Tutor course
            Click "Student Scores" from user menu
            ***The user is presented with the overall score column (t2.08.05)
            ***

            Click "number"
            ***Overall score percentage does not change format when selecting
            Number in the Percentage/Number toggle (t2.08.06)
            ***

            Scroll to a reading assignment
            ***The user is presented with progress icon but no score
            (t2.08.07)***


            Click on the info icon next to "Class Performance"
            ***The info icon displays a definition of how class and overall
            scores are calculated (t2.08.08)***

            Scroll until an assignment with an orange triangle is found
            Click on the orange triangle in the upper right corner of a
            progress cell
            Click "Accept late score" for a homework, OR Click "Accept late
            progress" for a reading
            ***The late score replaces the score at due date (t2.08.09)***
            ***The progress icon changes to reflect the last worked progress
            (t2.08.11)***

            Scroll until an assignment with a gray triangle is found
            Click on the gray triangle in the upper right corner of a progress
            cell
            Click "Use this score" for a homework OR "Use this Progress" for a
            reading
            ***The score is converted back to the score at due date
            (t2.08.10)***

            Click "Export"
            ***The teacher should be presented with their students' scores for
            each section taught (t1.13.03)***

            Click on the "Export" button
            ***Spreadsheet of scores is generating (t1.23.03)***
            ***External assignments are not included in the scores export
            t2.08.14***

            Select destination for saved spreadsheet in the pop up
            Click on the "Save" Button on the pop up
            ***Spreadsheet of scores is saved to chosen destination as an xlsx
            file
            (t1.23.4) ***

            Expected result:

            ***Corresponds to ***
            t1.23.03 --> 04
            t2.10 - 6,7
            T2.08 - 5--> 11, 14
            """
        # ARE WE JUST GONNA HARD CODE THE COURSE?
        # MAYBE THERE'S ANTOEHR WAY WE CAN ASSIGN IT?
        self.teacher.select_course(appearance='college_physics')

        assert('course' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.teacher.find(By.PARTIAL_LINK_TEXT, 'Student Scores').click()

        assert('scores' in self.teacher.current_url()), \
            'Not viewing Student Scores'

        # t2.08.05 --> The user is presented with the overall score column
        # (t2.08.05)

        self.teacher.wait.until(expect.presence_of_element_located(
            (By.XPATH, "//div[@class='overall-header-cell']")))

        # t2.08.06 --> Overall score percentage does not change format
        # when selecting Number in the Percentage/Number toggle

        overall_average1 = self.teacher.wait.until(
            expect.presence_of_element_located((
                By.XPATH,
                "//div[contains(@class,'overall-average')]//span"
            ))
        ).text

        self.teacher.find(
            By.XPATH,
            "//button[contains(@class,'btn btn-sm btn-default')" +
            "and contains(text(),'number')]"
        ).click()

        overall_average2 = self.teacher.wait.until(
            expect.presence_of_element_located((
                By.XPATH,
                "//div[contains(@class,'overall-average')]//span"
            ))
        ).text

        assert (overall_average1 == overall_average2), \
            'Overall average is not the same between percentage and number'

        # ADD A SCROLLING FEATURE HERE??

        # t2.08.07 -->  The user is presented with progress icon but no score

        # t2.08.08 --> The info icon displays a definition of how class and
        # overall scores are calculated

        self.teacher.find(
            By.XPATH,
            "//i[@class='tutor-icon fa fa-info-circle clickable']"
        ).click()
        self.teacher.sleep(2)
        self.teacher.find(By.XPATH, "//div[@class='popover-content']")

        # t2.08.09 --> The late score replaces the score at due date
        found = False

        scrollbar = self.teacher.find(
            By.XPATH,
            "//div[@class='ScrollbarLayout_main " +
            "ScrollbarLayout_mainHorizontal public_Scrollbar_main " +
            "public_Scrollbar_mainOpaque']")
        scrollbar.click()

        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(scrollbar)
        actions.click(scrollbar)
        actions.perform()

        newbar = self.teacher.find(
            By.XPATH,
            "//div[@class='ScrollbarLayout_main " +
            "ScrollbarLayout_mainHorizontal public_Scrollbar_main " +
            "public_Scrollbar_mainOpaque public_Scrollbar_mainActive']")

        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(newbar)
        actions.click(newbar)
        actions.perform()
        scrolls = 0
        # Four arrow rights bring a new assignment into view, try to bring
        # Bring three new assignments into view at a time
        p = False

        for num in range(100):
            for num1 in range(12):
                newbar.send_keys(Keys.ARROW_RIGHT)
            if len(self.teacher.driver.find_elements_by_xpath(
                    "//div[@class='late-caret']")) > 0:
                for num2 in range(5):
                    newbar.send_keys(Keys.ARROW_RIGHT)
                while not found:
                    try:
                        caret = self.teacher.find(
                            By.XPATH, "//div[@class='late-caret']")

                        try:
                            parent = caret.find_element_by_xpath(
                                "..").find_element_by_xpath("..")
                        except:
                            pass
                        try:
                            worked = parent.find_element_by_class_name(
                                "worked")
                        except:
                            pass
                        try:
                            not_started = worked.find_elements_by_class_name(
                                "not-started")
                        except:
                            pass

                        try:
                            if len(worked.find_elements_by_tag_name(
                                'path')
                            ) > 0:
                                p = True

                        except:
                            pass

                        caret1 = caret.find_element_by_xpath("..")

                        self.teacher.sleep(3)
                        caret.click()

                        self.teacher.find(
                            By.XPATH,
                            "//button[@class='late-button btn btn-default']"
                        ).click()
                        found = True
                        break

                    except:

                        if scrolls == 20:
                            break
                        try:
                            scrollbar = self.teacher.find(
                                By.XPATH,
                                "//div[@class='ScrollbarLayout_main " +
                                "ScrollbarLayout_mainVertical " +
                                "public_Scrollbar_main']")

                            scrollbar.click()

                        except:
                            pass

                        newbar = self.teacher.find(
                            By.XPATH,
                            "//div[@class='ScrollbarLayout_main " +
                            "ScrollbarLayout_mainVertical " +
                            "public_Scrollbar_main " +
                            "public_Scrollbar_mainActive']")

                        actions = ActionChains(self.teacher.driver)
                        actions.move_to_element(newbar)
                        actions.click(newbar)
                        actions.perform()
                        for i in range(3):
                            scrolls += 1
                            newbar.send_keys(Keys.ARROW_DOWN)
                break

        revert = False
        diff = False

        lates = self.teacher.driver.find_elements_by_xpath(
            "//div[@class='late-caret accepted']"
        )

        if len(not_started) > 0:
            slice_late = worked.find_elements_by_tag_name('circle')
            assert(slice_late[0].get_attribute('class') == 'slice late'), \
                'No change in the display of progress bar'
            diff = True

        # Case if assignment was partially complete before due date
        else:
            assert(p)
            assert(len(worked.find_elements_by_tag_name('path')) == 0), \
                'No change'

            diff = True

        if found:
            for item in lates:
                try:
                    item.click()
                    self.teacher.find(
                        By.XPATH,
                        "//button[@class='late-button btn btn-default']"
                    ).click()
                    revert = True
                    break

                except:
                    pass

        item = worked.find_element_by_xpath(
            "//div[@class='late-caret accepted']")

        item.click()
        self.teacher.find(
            By.XPATH,
            "//button[@class='late-button btn btn-default']"
        ).click()
        revert = True

        self.teacher.sleep(5)
        assert (found), \
            'Not found'

        assert (revert), \
            'Didnt revert'

        # t2.08.10 --> The score is converted back to the score at due date
        scrollbar.click()

        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(scrollbar)
        actions.click(scrollbar)
        actions.perform()

        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(newbar)
        actions.click(newbar)
        actions.perform()
        scrolls = 0

        # Four arrow rights bring a new assignment into view, try to bring
        # Bring three new assignments into view at a time

        for num in range(100):
            for num1 in range(12):
                newbar.send_keys(Keys.ARROW_RIGHT)
            if len(self.teacher.driver.find_elements_by_xpath(
                    "//div[@class='late-caret accepted']")) > 0:
                for num2 in range(3):
                    newbar.send_keys(Keys.ARROW_RIGHT)
                while not found:
                    try:

                        caret = self.teacher.find(
                            By.XPATH, "//div[@class='late-caret accepted']"
                        )
                        self.teacher.sleep(2)
                        caret.click()
                        self.teacher.sleep(5)

                        self.teacher.find(
                            By.XPATH,
                            "//button[@class='late-button btn btn-default']"
                        ).click()
                        self.teacher.sleep(5)

                        """
                        self.teacher.find_elements_by_xpath(
                            By.XPATH, "//div[@class='late-caret accepted']"
                        )[index].click()

                        self.teacher.find(
                            By.XPATH,
                            "//button[@class='late-button btn btn-default']"
                        ).click()
                        """
                        found = True
                        break

                    except:

                        if scrolls == 20:
                            break
                        try:
                            scrollbar = self.teacher.find(
                                By.XPATH,
                                "//div[@class='ScrollbarLayout_main " +
                                "ScrollbarLayout_mainVertical " +
                                "public_Scrollbar_main']")

                            scrollbar.click()

                        except:
                            pass

                        newbar = self.teacher.find(
                            By.XPATH,
                            "//div[@class='ScrollbarLayout_main " +
                            "ScrollbarLayout_mainVertical " +
                            "public_Scrollbar_main " +
                            "public_Scrollbar_mainActive']")

                        actions = ActionChains(self.teacher.driver)
                        actions.move_to_element(newbar)
                        actions.click(newbar)
                        actions.perform()
                        for i in range(1):
                            scrolls += 1
                            newbar.send_keys(Keys.ARROW_DOWN)

                break

        lates = self.teacher.driver.find_elements_by_xpath(
            "//div[@class='late-caret']"
        )

        revert = False
        if found:
            for item in lates:
                try:
                    item.click()
                    self.teacher.find(
                        By.XPATH,
                        "//button[@class='late-button btn btn-default']"
                    ).click()
                    revert = True
                    break

                except:
                    pass

        self.teacher.sleep(5)
        assert (found), \
            'Not found'

        assert (revert), \
            'Didnt revert'

        # t2.08.11  --> The progress icon changes to reflect the last worked
        # progress

        #  Setup scrollbar for scrolling
        scrollbar = self.teacher.find(
            By.XPATH,
            "//div[@class='ScrollbarLayout_main " +
            "ScrollbarLayout_mainHorizontal public_Scrollbar_main " +
            "public_Scrollbar_mainOpaque']")
        scrollbar.click()

        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(scrollbar)
        actions.click(scrollbar)
        actions.perform()

        newbar = self.teacher.find(
            By.XPATH,
            "//div[@class='ScrollbarLayout_main " +
            "ScrollbarLayout_mainHorizontal public_Scrollbar_main " +
            "public_Scrollbar_mainOpaque public_Scrollbar_mainActive']")
        actions = ActionChains(self.teacher.driver)
        actions.move_to_element(newbar)
        actions.click(newbar)
        actions.perform()
        scrolls = 0

        p = False
        for i in range(6):
            newbar.send_keys(Keys.PAGE_UP)
        self.teacher.sleep(3)
        # Four arrow rights bring a new assignment into view, try to bring
        # Bring three new assignments into view at a time
        for num in range(100):
            for num1 in range(12):
                newbar.send_keys(Keys.ARROW_RIGHT)
            if len(self.teacher.driver.find_elements_by_xpath(
                    "//div[@class='late-caret']")) > 0:
                for num2 in range(3):
                    newbar.send_keys(Keys.ARROW_RIGHT)

                while not found:
                    try:
                        caret = self.teacher.find(
                            By.XPATH, "//div[@class='late-caret']")

                        try:
                            parent = caret.find_element_by_xpath(
                                "..").find_element_by_xpath("..")
                        except:
                            pass
                        try:
                            worked = parent.find_element_by_class_name(
                                "worked")
                        except:
                            pass
                        try:
                            not_started = worked.find_elements_by_class_name(
                                "not-started")
                        except:
                            pass

                        try:
                            if len(worked.find_elements_by_tag_name(
                                    'path')) > 0:
                                p = True

                        except:
                            pass

                        caret1 = caret.find_element_by_xpath("..")

                        caret1.click()
                        self.teacher.find(
                            By.XPATH,
                            "//button[@class='late-button btn btn-default']"
                        ).click()
                        found = True
                        break

                    # Scroll down if the late assignment is not immediately
                    # visible, continue to scroll until found
                    except:

                        if scrolls == 20:
                            break
                        try:
                            scrollbar = self.teacher.find(
                                By.XPATH,
                                "//div[@class='ScrollbarLayout_main " +
                                "ScrollbarLayout_mainVertical " +
                                "public_Scrollbar_main']")

                            scrollbar.click()

                        except:
                            pass

                        newbar = self.teacher.find(
                            By.XPATH,
                            "//div[@class='ScrollbarLayout_main " +
                            "ScrollbarLayout_mainVertical " +
                            "public_Scrollbar_main " +
                            "public_Scrollbar_mainActive']")

                        actions = ActionChains(self.teacher.driver)
                        actions.move_to_element(newbar)
                        actions.click(newbar)
                        actions.perform()
                        for i in range(1):
                            scrolls += 1
                            newbar.send_keys(Keys.ARROW_DOWN)

                break

        revert = False
        diff = False

        # Case if assignment was not started at all before due date
        if len(not_started) > 0:
            slice_late = worked.find_elements_by_tag_name('circle')
            assert (slice_late[0].get_attribute('class') == 'slice late'), \
                'No change'

            diff = True

        # Case if assignment was partially complete before due date
        else:
            assert (p)
            assert (len(worked.find_elements_by_tag_name('path')) == 0), \
                'No change'

            diff = True

        assert (diff), \
            'No change'

        item = worked.find_element_by_xpath(
            "//div[@class='late-caret accepted']")

        item.click()
        self.teacher.find(
            By.XPATH,
            "//button[@class='late-button btn btn-default']"
        ).click()
        revert = True

        self.teacher.sleep(5)
        assert (found), \
            'Not found'

        assert (revert), \
            'Didnt revert'
    # t1.23.03 --> Spreadsheet of scores is generating
    # The teacher should be presented with their students' scores for each
    # section taught

    # t2.08.14 --> External assignments are not included in the scores export

    # Test steps and verification assertions
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[contains(@class,"export-button-buttons")]//button')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[@class="export-button"]//button[text()="Export"]')
            )
        )
        coursename = self.teacher.driver.find_element(
            By.XPATH, '//div[@class="course-name"]').text
        coursename = coursename.replace(' ', '_') + "_Scores"
        home = os.getenv("HOME")
        files = os.listdir(home + '/Downloads')
        for i in range(len(files)):
            if (coursename in files[i]) and (files[i][-5:] == '.xlsx'):
                break
            else:
                if i == len(files) - 1:
                    raise Exception

    # t1.23.04 --> Spreadsheet of scores is saved to chosen destination as an
    # xlsx file

        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[contains(@class,"export-button-buttons")]//button')
            )
        ).click()
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[@class="export-button"]//button[text()="Export"]')
            )
        )
        coursename = self.teacher.driver.find_element(
            By.XPATH, '//div[@class="course-name"]').text
        coursename = coursename.replace(' ', '_') + "_Scores"
        home = os.getenv("HOME")
        files = os.listdir(home + '/Downloads')
        for i in range(len(files)):
            if (coursename in files[i]) and (files[i][-5:] == '.xlsx'):
                break
            else:
                if i == len(files) - 1:
                    raise Exception
