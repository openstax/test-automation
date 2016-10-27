"""Tutor v1, Epic 13 - ViewTheCalendarDashboard."""

import inspect
import json
import os
import pytest
import unittest
import datetime

from pastasauce import PastaSauce, PastaDecorator
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from staxing.assignment import Assignment
from staxing.helper import Teacher
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


basic_test_env = json.dumps([
    {
        'platform': 'Windows 10',
        'browserName': 'chrome',
        'version': '50.0',
        'screenResolution': "1024x768",
    },
    # {
    #     'platform': 'Windows 7',
    #     'browserName': 'firefox',
    #     'version': 'latest',
    #     'screenResolution': '1024x768',
    # },
])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
TESTS = os.getenv(
    'CASELIST',
    # str([
    #     7978, 7979, 7980, 7981, 7982,
    #     7983, 7984, 7985, 7986, 7987,
    #     7988, 7989, 7990, 7991
    # ])
    str([7984])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestViewTheCalendarDashboard(unittest.TestCase):
    """T1.13 - View the calendar."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.teacher = Teacher(
            use_env_vars=True,
            # pasta_user=self.ps,
            # capabilities=self.desired_capabilities
        )
        self.teacher.login()

    def tearDown(self):
        """Test destructor."""
        self.ps.update_job(
            job_id=str(self.teacher.driver.session_id),
            **self.ps.test_updates
        )
        try:
            self.teacher.delete()
        except:
            pass

    # Case C7978 - 001 - Teacher | View the calendar dashboard
    @pytest.mark.skipif(str(7978) not in TESTS, reason='Excluded')
    def test_teacher_view_the_calendar_dashboard_7978(self):
        """View the calendar dashboard.

        Steps:
        If the user has more than one course, click on a Tutor course name

        Expected Result:
        The teacher is presented their calendar dashboard.
        """
        self.ps.test_updates['name'] = 't1.13.001' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.001', '7978']
        self.ps.test_updates['passed'] = False

        # self.teacher.select_course(title='HS Physics')
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.ps.test_updates['passed'] = True

    # Case C7979 - 002 - Teacher | View student scores using dashboard button
    @pytest.mark.skipif(str(7979) not in TESTS, reason='Excluded')
    def test_teacher_view_student_scores_using_the_dashboard_button_7979(self):
        """View student scores using the dashboard button.

        Steps:
        If the user has more than one course, click on a Tutor course name
        Click on the 'Student Scores' button

        Expected Result:
        The teacher is presented with the student scores
        """
        self.ps.test_updates['name'] = 't1.13.002' + \
            inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.002', '7979']
        self.ps.test_updates['passed'] = False

        # self.teacher.select_course(title='HS Physics')
        self.teacher.find(By.LINK_TEXT, 'Student Scores').click()
        assert('scores' in self.teacher.current_url()), \
            'Not viewing student scores'

        self.ps.test_updates['passed'] = True

    # Case C7980 - 003 - Teacher | View student scores using the user menu link
    @pytest.mark.skipif(str(7980) not in TESTS, reason='Excluded')
    def test_teacher_view_student_scores_using_the_user_menu_link_7980(self):
        """View student scores using the user menu link.

        Steps:
        If the user has more than one course, click on a Tutor course name
        Click on the user menu
        Click on the 'Student Scores' link

        Expected Result:
        The teacher is presented with the student scores
        """
        self.ps.test_updates['name'] = 't1.13.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.003', '7980']
        self.ps.test_updates['passed'] = False

        # self.teacher.select_course(title='HS Physics')
        self.teacher.open_user_menu()
        self.teacher.find(By.CLASS_NAME, 'viewScores'). \
            find_element_by_tag_name('a'). \
            click()
        assert('scores' in self.teacher.current_url()), \
            'Not viewing the student scores'

        self.ps.test_updates['passed'] = True

    # Case C7981 - 004 - Teacher | View performance forecast using the
    # dashboard button
    @pytest.mark.skipif(str(7981) not in TESTS, reason='Excluded')
    def test_teacher_view_performance_forecast_using_dash_button_7981(self):
        """View performance forecast using the dashboard button.

        Steps:
        If the user has more than one course, click on a Tutor course name
        Click on the 'Performance Forecast' button on the dashboard

        Expected Result:
        The teacher is presented with the performance forecast
        """
        self.ps.test_updates['name'] = 't1.13.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.004', '7981']
        self.ps.test_updates['passed'] = False

        self.teacher.find(By.LINK_TEXT, 'Performance Forecast').click()
        self.teacher.page.wait_for_page_load()
        assert('guide' in self.teacher.current_url()), \
            'Not viewing the performance forecast'

        self.ps.test_updates['passed'] = True

    # Case C7982 - 005 - Teacher | View performace forecast using
    # the user menu link
    @pytest.mark.skipif(str(7982) not in TESTS, reason='Excluded')
    def test_teacher_view_performance_forecast_using_user_menu_link_7982(self):
        """View performance forecast using the user menu link.

        Steps:
        If the user has more than one course, click on a Tutor course name
        Click on the user menu
        Click on the 'Performance Forecast' link

        Expected Result:
        The teacher is presented with the performance forecast
        """
        self.ps.test_updates['name'] = 't1.13.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.005', '7982']
        self.ps.test_updates['passed'] = False

        # self.teacher.select_course(title='HS Physics')
        self.teacher.open_user_menu()
        self.teacher.find(By.CLASS_NAME, 'viewTeacherPerformanceForecast'). \
            find_element_by_tag_name('a'). \
            click()
        self.teacher.page.wait_for_page_load()
        assert('guide' in self.teacher.current_url()), \
            'Not viewing the performance forecast'

        self.ps.test_updates['passed'] = True

    # Case C7983 - 006 - Teacher | View a reading assignment summary
    @pytest.mark.skipif(str(7983) not in TESTS, reason='Excluded')
    def test_teacher_view_a_reading_assignment_summary_7983(self):
        """View a reading assignment summary.

        Steps:
        If the user has more than one course, click on a Tutor course name
        Create a reading assignment
        Click on the reading assignment on the calendar

        Expected Result:
        The teacher is presented with the reading assignment summary
        """
        self.ps.test_updates['name'] = 't1.13.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.006', '7983']
        self.ps.test_updates['passed'] = False

        # self.teacher.select_course(appearance='physics')
        # create an assignemnt
        assignment_name = 'reading-%s' % randint(100, 999)
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(
            assignment='reading',
            args={
                'title': assignment_name,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'reading_list': ['1.1'],
                'status': 'publish',
            }
        )
        # click on assignemnt
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.XPATH, '//label[contains(text(), "%s")]' % assignment_name)
            )
        ).click()
        # check that it opened
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.XPATH, '//h2[contains(text(), "%s")]' % assignment_name)
            )
        )

        self.ps.test_updates['passed'] = True





    def find_all_questions(self, driver, problems):
        """Final all available questions."""

        assignment = Assignment()

        questions = {}
        section = ''
        wait = WebDriverWait(driver, 5)
        try:
            loading = wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//span[text()="Loading..."]')
                )
            )
            wait.until(expect.staleness_of(loading))
        except:
            pass
        rows = driver.find_elements(
            By.XPATH,
            '//div[contains(@class,"exercise-sections")]' +
            '//div[@class="exercises"]')                 # #######CHANGE (and below)
        print("rows: " + str(rows))
        for row in rows:
            children = row.find_elements(By.XPATH, './/span[contains(text(),"ID:")]')
            print("children: " + str(children))
            if len(children) == 0:
                # print('FAQ - No children tags')
                questions[section] = []
                continue
            # elif len(children) == 1:
            #     try:
            #         section = children[0].find_element(
            #             By.XPATH,
            #             './/span[@class="chapter-section"]').text
            #         questions[section] = []
            #     except:
            #         question = children[0].find_element(
            #             By.XPATH,
            #             './/span[contains(text(),"@")]').text
            #         question = question.split(' ')[1]
            #         questions[section].append(question)
            else:
                for q in children:
                    question = q.text.split(' ')[1]
                    questions[section].append(question)
                # question = children[0].find_element(
                #     By.XPATH,
                #     './/span[contains(text(),"@")]').text
                # question = question.split(' ')[1]
                # questions[section].append(question)
                # try:
                #     question = children[1].find_element(
                #         By.XPATH,
                #         './/span[contains(text(),"@")]').text
                #     question = question.split(' ')[1]
                #     questions[section].append(question)
                # except:
                #     pass
        return questions

    def add_homework_problems(self, driver, problems):
        """Add assessments to a homework."""
        assignment = Assignment()  # #######

        wait = WebDriverWait(driver, Assignment.WAIT_TIME)
        driver.find_element(By.ID, 'problems-select').click()
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[text()="Add Questions"]')    # CHANGE!!
            )
        )
        assignment.select_sections(driver, list(problems.keys()))
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        driver.find_element(
            By.XPATH, '//button[contains(@class,"-show-problems")]'
        ).click()
        all_available = self.find_all_questions(driver, problems)
        using = []
        # print('AHP - Selection list: %s' % selections)
        print(all_available)
        print(problems)
        for section in problems:
            print("section: " + str(section))
            if problems is None or str(problems).lower() == 'none':
                print('%s: No exercises (%s)' % (section, problems[section]))
                continue
            # Set maximum Tutor-selected problems
            if section == 'tutor':
                print('Using %s Tutor selections' % problems[section])
                assignment.set_tutor_selections(driver, problems)
            # Select all exercises in the section
            elif problems[section] == 'all':
                print('Selecting all from %s' % section)
                available = assignment.get_chapter_list(all_available, section) if \
                    'ch' in section else all_available[section]
                for ex in available:
                    using.append(ex)
            # Select between X and Y exercises, inclusive, from the section
            elif type(problems[section]) == tuple:
                low, high = problems[section]
                total = randint(int(low), int(high))         # removed rsndom
                print('Selecting %s random from %s (%s to %s)' %
                      (total, section, low, high))
                available = assignment.get_chapter_list(all_available, section) if \
                    'ch' in section else all_available[section]
                for i in range(total):
                    ex = randint(0, len(available) - 1)      # removed random
                    using.append(available[ex])
                    available.remove(available[ex])
            # Select the first X exercises from the section
            elif type(problems[section]) == int:
                print('Selecting first %s from %s' %
                      (problems[section], section))
                available = assignment.get_chapter_list(all_available, section) if \
                    'ch' in section else all_available[section]
                for position in range(problems[section]):
                    using.append(available[position])
            elif problems[section] is list:
                print('Adding %s custom if available' % len(problems[section]))
                for ex in problems[section]:
                    for section in all_available:
                        if ex in all_available[section]:
                            using.append(ex)
        for exercise in set(using):
            ac = ActionChains(driver)
            time.sleep(0.5)
            ac.move_to_element(
                driver.find_element(
                    By.XPATH,
                    '//span[contains(@data-reactid,"%s")]' % exercise
                )
            )
            ac.move_by_offset(0, -80)
            ac.click()
            ac.perform()
        ActionChains(driver). \
            move_to_element(
                driver.find_element(
                    By.XPATH, '//span[text()="Tutor Selections"]'
                )). \
            move_by_offset(0, -80). \
            perform()
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//*[text()="Next"]')
            )
        ).click()


    # Case C7984 - 007 - Teacher | View a homework assignment summary
    @pytest.mark.skipif(str(7984) not in TESTS, reason='Excluded')
    def test_teacher_view_a_homework_assignment_summary_7984(self):
        """View a homework assignment summary.

        Steps:
        create a homework assignment
        If the user has more than one course, click on a Tutor course name
        Click on a homework assignment on the calendar

        Expected Result:
        The teacher is presented with the homework assignment summary
        """
        self.ps.test_updates['name'] = 't1.13.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.007', '7984']
        self.ps.test_updates['passed'] = False

        # self.teacher.select_course(appearance='physics')
        # create an assignment
        self.teacher.select_course(appearance='physics')  # ############


        assignment_name = "homework-%s" % randint(100, 999)
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=2)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=4)).strftime('%m/%d/%Y')
        # self.teacher.add_assignment(
        #     assignment='homework',
        #     args={
        #         'title': assignment_name,
        #         'description': 'description',
        #         'periods': {'all': (begin, end)},
        #         'problems': {'1.1': (4, 8), },
        #         'status': 'publish',
        #         'feedback': 'immediate'
        #     }
        # )


        break_point = None
        assignment = Assignment()
        driver = self.teacher.driver
        description = "description"
        title = "title"
        periods = {'all': (begin, end)}
        status = 'publish'
        feedback = 'immediate'
        problems = {'1.1': (2, 4), }

        print('Creating a new Homework')
        assignment.open_assignment_menu(driver)
        driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        wait = WebDriverWait(driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"homework-plan")]')
            )
        )
        if break_point == Assignment.BEFORE_TITLE:
            return
        driver.find_element(By.ID, 'reading-title').send_keys(title)
        if break_point == Assignment.BEFORE_DESCRIPTION:
            return
        driver.find_element(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]' +
            '//textarea[contains(@class,"form-control")]'). \
            send_keys(description)
        if break_point == Assignment.BEFORE_PERIOD:
            return
        assignment.assign_periods(driver, periods)
        if break_point == Assignment.BEFORE_EXERCISE_SELECT:
            return
        self.add_homework_problems(driver, problems)  #############

        driver.find_element(By.ID, 'feedback-select').click()
        if feedback == 'immediate':
            driver.find_element(
                By.XPATH,
                '//option[@value="immediate"]'
            ).click()
        else:
            driver.find_element(By.XPATH, '//option[@value="due_at"]').click()
        if break_point == Assignment.BEFORE_STATUS_SELECT:
            return
        assignment.select_status(driver, status)










        # click on assignemnt
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.XPATH, '//label[contains(text(), "%s")]' % assignment_name)
            )
        ).click()
        # check that it opened
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.XPATH, '//h2[contains(text(), "%s")]' % assignment_name)
            )
        )
        self.ps.test_updates['passed'] = True

    # NOT DONE
    # Case C7985 - 008 - Teacher | View an external assignment summary
    @pytest.mark.skipif(str(7985) not in TESTS, reason='Excluded')
    def test_teacher_view_an_external_assignment_summary_7985(self):
        """View an external assignment summary.

        Steps:
        If the user has more than one course, click on a Tutor course name
        Click on an external assignment on the calendar

        Expected Result:
        The teacher is presented with the external assignment summary
        """
        self.ps.test_updates['name'] = 't1.13.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.008', '7985']
        self.ps.test_updates['passed'] = False

        self.teacher.select_course(appearance='physics')
        # create an assignemnt
        assignment_name = 'external-%s' % randint(100, 999)
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(
            assignment='external',
            args={
                'title': assignment_name,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'url': 'google.com',
                'status': 'publish'
            }
        )
        # click on assignemnt
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.XPATH, '//label[contains(text(), "%s")]' % assignment_name)
            )
        ).click()
        # check that it opened
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.XPATH, '//h2[contains(text(), "%s")]' % assignment_name)
            )
        )

        self.ps.test_updates['passed'] = True

    # Case C7986 - 009 - Teacher | View an event summary
    @pytest.mark.skipif(str(7986) not in TESTS, reason='Excluded')
    def test_teacher_view_an_event_summary_7986(self):
        """View an event summary.

        Steps:
        If the user has more than one course, click on a Tutor course name
        Click on an event on the calendar

        Expected Result:
        The teacher is presented with the event summary
        """
        self.ps.test_updates['name'] = 't1.13.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.009', '7986']
        self.ps.test_updates['passed'] = False

        # self.teacher.select_course(appearance='physics')
        # create an assignment
        assignment_name = "homework-%s" % randint(100, 999)
        today = datetime.date.today()
        begin = (today + datetime.timedelta(days=2)).strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=4)).strftime('%m/%d/%Y')
        self.teacher.add_assignment(
            assignment='event',
            args={
                'title': assignment_name,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'status': 'publish'
            }
        )
        # click on assignemnt
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.XPATH, '//label[contains(text(), "%s")]' % assignment_name)
            )
        ).click()
        # check that it opened
        self.teacher.wait.until(
            expect.presence_of_element_located(
                (By.XPATH, '//h2[contains(text(), "%s")]' % assignment_name)
            )
        )
        self.ps.test_updates['passed'] = True

    # Case C7987 - 010 - Teacher | Open the refrenece book using the dashboard
    # button
    @pytest.mark.skipif(str(7987) not in TESTS, reason='Excluded')
    def test_teacher_open_the_reference_book_using_dashboard_button_7987(self):
        """Open the refrenece book using the dashboard button.

        Steps:
        If the user has more than one course, click on a Tutor course name
        Click on the 'Browse The Book'button

        Expected Result:
        The teacher is preseneted with the book in a new tab
        """
        self.ps.test_updates['name'] = 't1.13.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.010', '7987']
        self.ps.test_updates['passed'] = False

        # self.teacher.select_course(title='HS Physics')
        self.teacher.driver.find_element(
            By.LINK_TEXT,
            'Browse The Book'
        ).click()
        window_with_book = self.teacher.driver.window_handles[1]
        self.teacher.driver.switch_to_window(window_with_book)
        assert('book' in self.teacher.current_url()), \
            'Not viewing the textbook PDF'

        self.ps.test_updates['passed'] = True

    # Case C7988 - 011 - Teacher | Open the refrenece book using user menu link
    @pytest.mark.skipif(str(7988) not in TESTS, reason='Excluded')
    def test_teacher_open_the_reference_book_using_user_menu_link_7988(self):
        """Open the refrenece book using the user menu link.

        Steps:
        If the user has more than one course, click on a Tutor course name
        Click on the user menu
        Click on the 'Browse the Book' link

        Expected Result:
        The teacher is presented with the book in a new tab
        """
        self.ps.test_updates['name'] = 't1.13.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.011', '7988']
        self.ps.test_updates['passed'] = False

        # self.teacher.select_course(title='HS Physics')
        self.teacher.open_user_menu()
        self.teacher.driver.find_element(
            By.CLASS_NAME,
            'view-reference-guide'
        ).click()
        window_with_book = self.teacher.driver.window_handles[1]
        self.teacher.driver.switch_to_window(window_with_book)
        assert('book' in self.teacher.current_url()), \
            'Not viewing the textbook PDF'

        self.ps.test_updates['passed'] = True

    # Case C7989 - 012 - Teacher | Click on the course name to return to
    # the dashboard
    @pytest.mark.skipif(str(7989) not in TESTS, reason='Excluded')
    def test_teacher_click_course_name_to_return_to_the_dashboard_7989(self):
        """Click on the course name to return to the dashboard.

        Steps:
        If the user has more than one course, click on a Tutor course name
        Click on the 'Performance Forecast' button
        Click on the course name in the header

        Expected Result:
        The teacher is presented with their calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.13.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.012', '7989']
        self.ps.test_updates['passed'] = False

        self.teacher.open_user_menu()
        self.teacher.driver.find_element(
            By.CLASS_NAME,
            'viewTeacherPerformanceForecast'
        ).click()
        self.teacher.driver.find_element(
            By.CLASS_NAME,
            'course-name'
        ).click()
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.ps.test_updates['passed'] = True

    # Case C7990 - 013 - Teacher | Cick on the OpenStax logo to return to
    # the course picker
    @pytest.mark.skipif(str(7990) not in TESTS, reason='Excluded')
    def test_teacher_click_openstax_logo_to_return_to_course_picker_7990(self):
        """Cick on the OpenStax logo to return to the course picker.

        Steps:
        If the user has more than one course, click on a Tutor course name
        Click in the OpenStax logo in the header

        Expected Result:
        The teacher is presented with the course picker
        """
        self.ps.test_updates['name'] = 't1.13.013' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.013', '7990']
        self.ps.test_updates['passed'] = False

        # self.teacher.select_course(appearance='physics')
        self.teacher.driver.find_element(
            By.CLASS_NAME,
            'ui-brand-logo'
        ).click()
        assert('dashboard' in self.teacher.current_url()), \
            'Not viewing the course picker'

        self.ps.test_updates['passed'] = True

    # Case C7991 - 014 - Teacher | CLick in the OpenStax logo to return to the
    # dashboard
    @pytest.mark.skipif(str(7991) not in TESTS, reason='Excluded')
    def test_teacher_clicks_openstax_logo_to_return_to_dashboard_7991(self):
        """CLick in the OpenStax logo to return to the dashboard.

        Steps:
        Click on the 'Performance Forecast' button
        Click on the OpenStax logo in the header

        Expected Result:
        The teacher is presented with their calendar dashboard
        """
        self.ps.test_updates['name'] = 't1.13.014' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t1', 't1.13', 't1.13.014', '7991']
        self.ps.test_updates['passed'] = False

        self.teacher.logout()
        teacher2 = Teacher(
            username=os.getenv('TEACHER_USER_ONE_COURSE'),
            password=os.getenv('TEACHER_PASSWORD'),
            site='https://tutor-qa.openstax.org',
            existing_driver=self.teacher.driver,
            pasta_user=self.ps,
            capabilities=self.desired_capabilities,
        )
        print(teacher2.username)
        print(teacher2.password)
        teacher2.login()
        self.teacher.open_user_menu()
        self.teacher.driver.find_element(
            By.CLASS_NAME,
            'viewTeacherPerformanceForecast'
        ).click()
        self.teacher.driver.find_element(
            By.CLASS_NAME,
            'ui-brand-logo'
        ).click()
        assert('calendar' in self.teacher.current_url()), \
            'Not viewing the calendar dashboard'

        self.ps.test_updates['passed'] = True
