"""
TestRail Python functionality.

Pull the API commands into a class as opposed to just sending URI command
strings.

http://docs.gurock.com/testrail-api2/start
http://docs.gurock.com/testrail-api2/accessing
"""

import json
import os
import requests

# from http import HTTPStatus as http
from time import sleep

__version__ = '0.0.1'


class TestRailAPI(object):
    """TestRail API interface."""

    GET = 'get'
    PUT = 'put'
    DELETE = 'delete'
    HEAD = 'head'
    OPTIONS = 'options'
    _actions = {
        GET: lambda url, user, key, headers:
            requests.get(url, auth=(user, key), headers=headers),
        PUT: lambda url, user, key, headers, json:
            requests.put(url, json=json, auth=(user, key), headers=headers),
        DELETE: lambda url, user, key, headers:
            requests.delete(url, auth=(user, key), headers=headers),
        HEAD: lambda url, user, key, headers:
            requests.head(url, auth=(user, key), headers=headers),
        OPTIONS: lambda url, user, key, headers:
            requests.options(url, auth=(user, key), headers=headers),
    }
    PASSED = 1
    BLOCKED = 2
    UNTESTED = 3
    RETEST = 4
    FAILED = 5
    SHOW_ALL_RESULTS = False

    def __init__(self, url, api=None, key=None):
        """Initializer using API key/values."""
        api_uri = 'index.php?/api/v2/'
        self.url = '%s%s' % (url, api_uri)
        self.headers = {'Content-Type': 'application/json'}
        if api is None:
            print('Username not set, using environment value')
            try:
                self.user = os.environ['TESTRAIL_USER']
            except KeyError as e:
                print('KeyError: %s' % e.read())
                raise ValueError('"TESTRAIL_USER" environment variable not' +
                                 ' set')
        else:
            print('Using username')
            self.user = api
        if key is None:
            print('Password/API key value not set, using environment value')
            try:
                self.key = os.environ['TESTRAIL_VALUE']
            except KeyError as e:
                print('KeyError: %s' % e.read())
                raise ValueError('"TESTRAIL_VALUE" environment variable not' +
                                 'set')
        else:
            print('Using Password/API key value')
            self.key = key

    def __str__(self):
        """Return the public variables for a TestRailAPI object."""
        return '%s: URL(%s) - User(%s)' % (self.__class__.__name__,
                                           self.url, self.user)

    def _request_call(self, method, uri, data):
        """Class function request short-hand helper."""
        response = None
        error = None
        try:
            if method == self.PUT:
                response = self._actions[self.PUT](self.url + uri,
                                                   self.user,
                                                   self.key,
                                                   data,
                                                   self.headers)
            else:
                response = self._actions[method](self.url + uri,
                                                 self.user,
                                                 self.key,
                                                 self.headers)
            if response.status_code != 200 or self.SHOW_ALL_RESULTS:
                print(response.status_code, self.url + uri)
                print(
                    json.dumps(
                        json.loads(response.text),
                        sort_keys=True,
                        indent=2,
                        separators=(',', ': ')
                    )
                )
        except requests.exceptions.RequestException as e:
            response = e.read()
            error = e
        return (response, error)

    def request(self, method=GET, uri='', data=None):
        """Combined HTTP requester."""
        response, error = self._request_call(method, uri, data)
        if response.status_code == '429':
            # too many requests sent; wait required sec then resend request
            snooze = int(response.json()['Retry-After']) + 1
            print('429 received; sleeping for %s before retrying' %
                  (snooze, ))
            sleep(snooze)
            response, error = self._request_call(method, uri, data)
        result = json.loads(response.text) if response else {}
        if error is not None:
            message = '' if 'error' not in result else result['error']
            raise TestRailAPIError('Error return: %s (%s)' %
                                   (error.code, message))
        return result

    @classmethod
    def uri_field_appends(cls, data={}):
        """Return a string of URI key/value pairs for the URL address.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        data (dict) - String key/value pairs for in-address URL
                      i.e. '&key1=value1&key2=value2'
                      Not to be used for the data/json request field
        """
        if data == {}:
            return ''
        if type(data) is not dict:
            raise TypeError('Parameter must be %s; received %s.' %
                            (dict, type(data)))
        fields = ''
        for key, value in data.items():
            fields += '&%s=%s' % (key, value)
        return fields

    # Users #
    def get_user_by_id(self, user_id):
        """Return user information for a specific user ID.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        user_id (int) - The ID of the user (required)
        """
        return self.request(self.GET, 'get_user/%s' % user_id)

    def get_user_by_email(self, email):
        """Return user information for a specific user email.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        email (string) - The email address for a current user (required)
        """
        return self.request(self.GET, 'get_user_by_email&email=%s' % email)

    def get_users(self):
        """Return the list of users."""
        return self.request(self.GET, 'get_users')

    # Projects #
    def get_project(self, project_id):
        """Return an existing project.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        project_id (int) - The ID of the project (required)
        """
        return self.request(self.GET, 'get_project/%s' % project_id)

    def get_projects(self, data={}):
        """Return a list of available projects.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        is_completed (bool) - True to return completed projects only.
                              False to return active projects only. (default)
        """
        return self.request(
            self.GET,
            'get_projects%s' % TestRailAPI.uri_field_appends(data)
        )

    def add_project(self, name, data={}):
        """Create a new project.

        Requires administrative access.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        name (string) - The name of the project (required)
        -------------------------------------------
        announcement (string) - The description of the project
        show_announcement (bool) - True if the announcement should be
                                   displayed on the project's overview page
                                   and False otherwise
        suite_mode (integer) - The suite mode of the project (1 for single
                               suite mode, 2 for single suite + baselines, 3
                               for multiple suites) (added with TestRail 4.0)
        """
        payload = data
        payload['name'] = name
        return self.request(self.POST, 'add_project', json=payload)

    def update_project(self, project_id, name, data={}):
        """Update an existing project.

        Requires administrative access.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        project_id (int) - The ID of the project (required)
        name (string) - The name of the project (required)
        -------------------------------------------
        announcement (string) - The description of the project
        show_announcement (bool) - True if the announcement should be
                                   displayed on the project's overview page
                                   and false otherwise
        suite_mode (integer) - The suite mode of the project (1 for single
                               suite mode, 2 for single suite + baselines, 3
                               for multiple suites) (added with TestRail 4.0)
        is_completed (bool) - Specifies whether a project is considered
                              completed or not
        """
        payload = data
        payload['name'] = name
        return self.request(self.POST,
                            'update_project/%s' % project_id,
                            json=payload)

    def delete_project(self, project_id):
        """Delete an existing project.

        Requires administrative access.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        project_id (int) - The ID of the project (required)
        """
        return self.request(self.POST, 'delete_project/%s' % project_id)

    def get_configs(self, project_id):
        """Return a list of available configurations group by config groups.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        project_id (int) - The ID of the project (required)
        """
        return self.request(self.GET, 'get_configs/%s' % project_id)

    # Milestones #
    def get_milestone(self, milestone_id):
        """Return detailed information on a specific milestone.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        milestone_id (int) - The ID of the milestone (required)
        """
        return self.request(self.GET, 'get_milestone/%s' % milestone_id)

    def get_milestones(self, project_id, data={}):
        """Return a list of milestones for a specific project (by ID).

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        project_id (int) - The ID of the project (required)
        -------------------------------------------
        is_completed (bool) - True to return completed milestones only.
                              False to return active milestones only.
        """
        return self.request(
            self.GET,
            'get_milestones/%s%s' % (
                project_id,
                TestRailAPI.uri_field_appends(data)
            )
        )

    def add_milestone(self, project_id, name, data={}):
        """Create a new milestone under a project.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        project_id (int) - The ID of the project (required)
        name (string) - The name of the milestone (required)
        -------------------------------------------
        description (string) - The description of the milestone
        due_on (timestamp) - The due date of the milestone (as UNIX timestamp)
        """
        payload = data
        payload['name'] = name
        return self.request(self.POST, 'add_milestone/%s' % project_id,
                            json=payload)

    def update_milestone(self, milestone_id, name, data={}):
        """Update an existing milestone.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        milestone_id (int) - The ID of the milestone (required)
        name (string) - The name of the milestone (required)
        -------------------------------------------
        description (string) - The description of the milestone
        due_on (timestamp) - The due date of the milestone (as UNIX timestamp)
        is_completed (bool) - Specifies whether a milestone is considered
                              completed or not
        """
        payload = data
        payload['name'] = name
        return self.request(self.POST, 'update_milestone/%s' % milestone_id,
                            json=payload)

    def delete_milestone(self, milestone_id):
        """Delete an existing milestone.

        Deletions are permanent and cannot be undone.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        milestone_id (int) - The ID of the milestone (required)
        """
        return self.request(self.POST, 'delete_milestone/%s' % milestone_id)

    # Plan Management #
    def get_plan(self, plan_id):
        """Return an existing test plan (by ID).

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        plan_id (int) - The ID of the test plan (required)
        """
        return self.request(self.GET, 'get_plan/%s' % plan_id)

    def get_plans(self, project_id, data={}):
        """Return a list of test plans for a specific project (by ID).

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        project_id (int) - The ID of the project (required)
        -------------------------------------------
        created_after (timestamp) - Only return test plans created after this
                                    date (as UNIX timestamp).
        created_before (timestamp) - Only return test plans created before
                                     this date (as UNIX timestamp).
        created_by (list) - A comma-separated list of creators (user IDs) to
                            filter by.
        is_completed (bool) - True to return completed test plans only.
                              False to return active test plans only.
        limit (int) - Limit the result to a specific number of test plans.
        offset (int) - Skip records.
        milestone_id (list) - A comma-separated list of milestone IDs to
                              filter by.
        """
        return self.request(
            self.GET,
            'get_plans/%s%s' % (
                project_id,
                TestRailAPI.uri_field_appends(data)
            )
        )

    def add_plan(self, project_id, name, data={}):
        """Add a new test plan under a specific project (by ID).

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        project_id (int) - The ID of the project (required)
        name (string) - The name of the test plan (required)
        -------------------------------------------
        description (string) - The description of the test plan
        milestone_id (int) - The ID of the milestone to link to the test plan
        entries (array) - An array of objects describing the test runs of the
                          plan, see the example below and add_plan_entry

        Entry Fields (dictionaries): [Name (Type) - Description]
        --------------------------------------------------------
        suite_id (int) - The ID of the test suite for the test run(s)
                         (required)
        name (string) - The name of the test run(s)
        description (string) - The description of the test run(s) (requires
                               TestRail 5.2 or later)
        assignedto_id (int) - The ID of the user the test run(s) should be
                              assigned to
        include_all (bool) - True for including all test cases of the test
                             suite and false for a custom case selection
                             (default: true)
        case_ids (array) - An array of case IDs for the custom case selection
        config_ids (array) - An array of configuration IDs used for the test
                             runs of the test plan entry (requires TestRail
                             3.1 or later)
        runs (array) - An array of test runs with configurations, please see
                       the example below for details (requires TestRail 3.1 or
                       later)
        """
        payload = data
        payload['name'] = name
        return self.request(self.POST, 'add_plan/%s' % project_id,
                            json=payload)

    def add_plan_entry(self, plan_id, suite_id, data={}):
        """Add one or more new test runs to a test plan.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        plan_id (int) - The ID of the plan the test runs should be added to
                        (required)
        suite_id (int) - The ID of the test suite for the test run(s)
                         (required)
        -------------------------------------------
        name (string) - The name of the test plan
        description (string) - The description of the test run(s) (requires
                               TestRail 5.2 or later)
        assignedto_id (int) - The ID of the user the test run(s) should be
                              assigned to
        include_all (bool) - True for including all test cases of the test
                             suite and False for a custom case selection
                             (default: True)
        case_ids (array) - An array of case IDs for the custom case selection
        config_ids (array) - An array of configuration IDs used for the test
                             runs of the test plan entry (requires TestRail
                             3.1 or later)
        runs (array) - An array of test runs with configurations, please see
                       the example below for details (requires TestRail 3.1 or
                       later)
        """
        payload = data
        payload['suite_id'] = suite_id
        return self.request(self.POST, 'add_plan_entry/%s' % plan_id,
                            json=payload)

    def update_plan(self, plan_id, name, data={}):
        """Update an existing test plan.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        plan_id (int) - The ID of the test plan (required)
        name (string) - The name of the test plan (required)
        -------------------------------------------
        description (string) - The description of the test plan
        milestone_id (int) - The ID of the milestone to link to the test plan
        entries (array) - An array of objects describing the test runs of the
                          plan, see the example below and add_plan_entry

        Entry Fields (dictionaries): [Name (Type) - Description]
        --------------------------------------------------------
        suite_id (int) - The ID of the test suite for the test run(s)
                         (required)
        name (string) - The name of the test run(s)
        description (string) - The description of the test run(s) (requires
                               TestRail 5.2 or later)
        assignedto_id (int) - The ID of the user the test run(s) should be
                              assigned to
        include_all (bool) - True for including all test cases of the test
                             suite and false for a custom case selection
                             (default: true)
        case_ids (array) - An array of case IDs for the custom case selection
        config_ids (array) - An array of configuration IDs used for the test
                             runs of the test plan entry (requires TestRail
                             3.1 or later)
        runs (array) - An array of test runs with configurations, please see
                       the example below for details (requires TestRail 3.1 or
                       later)
        """
        payload = data
        payload['name'] = name
        return self.request(self.POST, 'update_plan/%s' % plan_id,
                            json=payload)

    def update_plan_entry(self, plan_id, entry_id, data={}):
        """Update one or more existing test runs in a plan.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        plan_id (int) - The ID of the test plan (required)
        entry_id (int) -  The ID of the test plan entry (required)
        -------------------------------------------
        name (string) - The name of the test run(s)
        description (string) - The description of the test run(s) (requires
                               TestRail 5.2 or later)
        assignedto_id (int) - The ID of the user the test run(s) should be
                              assigned to
        include_all (bool) - True for including all test cases of the test
                             suite and false for a custom case selection
                             (default: True)
        case_ids (array) - An array of case IDs for the custom case selection
        """
        payload = data
        return self.request(
            self.POST,
            'update_plan_entry/%s/%s' % (plan_id, entry_id),
            json=payload
        )

    def close_plan(self, plan_id):
        """Close and existing test plan and archive the run and results.

        Archival is permanent and cannot be undone.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        plan_id (int) - The ID of the test plan (required)
        """
        return self.request(self.POST, 'close_plan/%s' % plan_id)

    def delete_plan(self, plan_id):
        """Delete an existing test plan.

        Deletion is permanent and cannot be undone.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        plan_id (int) - The ID of the test plan (required)
        """
        return self.request(self.POST, 'delete_plan/%s' % plan_id)

    def delete_plan_entry(self, plan_id, entry_id):
        """Delete one or more existing test runs from a plan.

        Deletion is permanent and cannot be undone.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        plan_id (int) - The ID of the test plan (required)
        entry_id (int) - The ID of the test plan entry (required)
        """
        return self.request(
            self.POST,
            'delete_plan_entry/%s/%s' % (plan_id, entry_id)
        )

    # Test Suite Management #
    def get_suite(self, suite_id):
        """Return an existing test suite.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        suite_id (int) - The ID of the test suite (required)
        """
        return self.request(self.GET, 'get_suite/%s' % suite_id)

    def get_suites(self, project_id):
        """Return a list of test suites for a project.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        project_id (int) - The ID of the project (required)
        """
        return self.request(self.GET, 'get_suites/%s' % project_id)

    def add_suite(self, project_id, name, data={}):
        """Create a new test suite.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        project_id (int) - The ID of the project (required)
        name (string) - The name of the test suite (required)
        -------------------------------------------
        description (string) - The description of the test suite
        """
        payload = data
        payload['name'] = name
        return self.request(
            self.POST,
            'add_suite/%s' % project_id,
            json=payload
        )

    def update_suite(self, suite_id, data={}):
        """Update an existing test suite.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        suite_id (int) - The ID of the suite (required)
        -------------------------------------------
        name (string) - The name of the test suite
        description (string) - The description of the test suite
        """
        return self.request(
            self.POST,
            'update_suite/%s' % suite_id,
            json=data
        )

    def delete_suite(self, suite_id):
        """Delete an existing test suite.

        Deletions are permanent and cannot be undone.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        suite_id (int) - The ID of the suite (required)
        """
        return self.request(self.POST, 'delete_suite/%s' % suite_id)

    # Case Management #
    def get_case(self, case_id):
        """Return the detailed information for a specific test case (by ID).

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        case_id (int) - The ID of the test case (required)
        """
        return self.request(self.GET, 'get_case/%s' % case_id)

    def get_cases(self, project_id, data={}):
        """Return a list of test cases for a project (by project ID).

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        project_id (int) - The ID of the project (required)
        -------------------------------------------
        suite_id (int) - Restrict the list to a specific test suite
        section_id (int) - Restrict the list to a specific section
        created_after (timestamp) - Only return test cases created after this
                                    date (as UNIX timestamp).
        created_before (timestamp) - Only return test cases created before
                                     this date (as UNIX timestamp).
        created_by (list) - A comma-separated list of creators (user IDs) to
                            filter by.
        milestone_id (list) - A comma-separated list of milestone IDs to
                              filter by (not available if the milestone field
                              is disabled for the project).
        priority_id (list) - A comma-separated list of priority IDs to filter
                             by.
        template_id (list) - A comma-separated list of template IDs to filter
                             by (requires TestRail 5.2 or later)
        type_id (list) - A comma-separated list of case type IDs to filter by.
        updated_after (timestamp) - Only return test cases updated after this
                                    date (as UNIX timestamp).
        updated_before (timestamp) - Only return test cases updated before
                                     this date (as UNIX timestamp).
        updated_by (list) - A comma-separated list of users who updated test
                            cases to filter by.
        """
        return self.request(
            self.GET,
            'get_cases/%s%s' % (
                project_id,
                TestRailAPI.uri_field_appends(data)
            )
        )

    def get_case_fields(self):
        """Return a list of available test case custom fields."""
        return self.request(self.GET, 'get_case_fields')

    def get_case_types(self):
        """Return a list of available case types."""
        return self.request(self.GET, 'get_case_types')

    def get_priorities(self):
        """Return a list of available priority levels."""
        return self.request(self.GET, 'get_priorities')

    def get_templates(self, project_id):
        """Return a list of available templates.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        project_id (int) - The ID of the project (required)
        """
        return self.request(self.GET, 'get_templates/%s' % project_id)

    def add_case(self, section_id, title, data={}):
        """Create a new test case to a section.

        Custom Fields must be submitted with their system name prefixed by
        'custom_'.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        section_id (int) - The ID of the section the test case should be added
                           to (required)
        title (string) - The title of the test case (required)
        -------------------------------------------
        template_id (int) - The ID of the template (field layout)
                             (requires TestRail 5.2 or later)
        type_id (int) - The ID of the case type
        priority_id (int) - The ID of the case priority
        estimate (timespan) - The estimate, e.g. "30s" or "1m 45s"
        milestone_id (int) - The ID of the milestone to link to the test case
        refs (string) - A comma-separated list of references/requirements

        Custom Field Types: [Name (Type) - Description]
        -----------------------------------------------
        Checkbox (bool) - True for checked and false otherwise
        Date (string) - A date in the same format as configured for TestRail
                        and API user (e.g. "07/08/2013")
        Dropdown (int) - The ID of a dropdown value as configured in the field
                         configuration
        Integer (int) - A valid integer
        Milestone (int) - The ID of a milestone for the custom field
        Multi-select (array) - An array of IDs as configured in the field
                               configuration
        Steps (array) - An array of objects specifying the steps. Also see the
                        example below.
        String (string) - A valid string with a maximum length of 250
                          characters
        Text (string) - A string without a maximum length
        URL (string) - A string with matches the syntax of a URL
        User (int) - The ID of a user for the custom field
        """
        payload = data
        payload['title'] = title
        return self.request(
            self.POST,
            'add_case/%s' % section_id,
            json=payload
        )

    def update_case(self, case_id, data={}):
        """Update fields in an existing test case.

        'section_id' cannot be changed. Custom Fields must be submitted with
        their system name prefixed by 'custom_'.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        case_id (int) - The ID of the test case (required)
        -------------------------------------------
        title (string) - The title of the test case
        template_id (int) - The ID of the template (field layout)
                            (requires TestRail 5.2 or later)
        type_id (int) - The ID of the case type
        priority_id (int) - The ID of the case priority
        estimate (timespan) - The estimate, e.g. "30s" or "1m 45s"
        milestone_id (int) - The ID of the milestone to link to the test case
        refs (string) - A comma-separated list of references/requirements

        Custom Field Types: [Name (Type) - Description]
        -----------------------------------------------
        Checkbox (bool) - True for checked and false otherwise
        Date (string) - A date in the same format as configured for TestRail
                        and API user (e.g. "07/08/2013")
        Dropdown (int) - The ID of a dropdown value as configured in the field
                         configuration
        Integer (int) - A valid integer
        Milestone (int) - The ID of a milestone for the custom field
        Multi-select (array) - An array of IDs as configured in the field
                               configuration
        Steps (array) - An array of objects specifying the steps. Also see the
                        example below.
        String (string) - A valid string with a maximum length of 250
                          characters
        Text (string) - A string without a maximum length
        URL (string) - A string with matches the syntax of a URL
        User (int) - The ID of a user for the custom field
        """
        return self.request(self.POST, 'update_case/%s' % case_id, json=data)

    def delete_case(self, case_id):
        """Delete an existing test case.

        Deletions are permanent and cannot be undone.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        case_id (int) - The ID of the test case (required)
        """
        return self.request(self.POST, 'delete_case/%s' % case_id)

    # Result Management #
    def get_result_fields(self):
        """Return a list of available test result custom fields."""
        return self.request(self.GET, 'get_result_fields')

    def get_results(self, test_id, data={}):
        """Return a list of test results for a particular test case.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        test_id (int) - The ID of the test (required)
        -------------------------------------------
        limit (int) - Limit the result to a specific number of test results.
        offset (int) - Skip records.
        status_id (list) - A comma-separated list of status IDs to filter by.
        """
        return self.request(
            self.GET,
            'get_results/%s%s' % (test_id, self.uri_field_appends(data))
        )

    def get_results_for_case(self, run_id, case_id, data={}):
        """Return a list of test results for a test case in a test run.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        run_id (int) - The ID of the test run (required)
        case_id (int) - The ID of the test case (required)
        -------------------------------------------
        limit (int) - Limit the result to a specific number of test results.
        offset (int) - Skip records.
        status_id (list) - A comma-separated list of status IDs to filter by.
        """
        return self.request(
            self.GET,
            'get_results_for_case/%s/%s%s' % (
                run_id,
                case_id,
                TestRailAPI.uri_field_appends(data)
            )
        )

    def get_results_for_run(self, run_id, data={}):
        """Return a list of test results for a test case in a test run.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        run_id (int) - The ID of the test run (required)
        -------------------------------------------
        created_after (timestamp) - Only return test results created after
                                    this date (as UNIX timestamp).
        created_before (timestamp) - Only return test results created before
                                     this date (as UNIX timestamp).
        created_by (list) - A comma-separated list of creators (user IDs) to
                            filter by.
        limit (int) - Limit the result to a specific number of test results.
        offset (int) - Skip records.
        status_id (list) - A comma-separated list of status IDs to filter by.
        """
        return self.request(
            self.GET,
            'get_results_for_run/%s%s' % (
                run_id,
                TestRailAPI.uri_field_appends(data)
            )
        )

    def add_result(self, test_id, data={}):
        """Add a new test result, comment, or assign a test.

        Use add_results instead if you plan to add results for multiple tests.

        Custom fields are supported as well and must be submitted with their
        system name, prefixed with 'custom_'.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        test_id (int) - The ID of the test the result should be applied to
                        (required)
        -------------------------------------------
        status_id (int) - The ID of the test status. The built-in system
                          statuses have the following IDs:
                          PASSED   (=1)
                          BLOCKED  (=2)
                          RETEST   (=4)
                          FAILED   (=5)
                          You can get a full list of system and custom
                          statuses via get_statuses.
        comment (string) - The comment / description for the test result
        version (string) - The version or build you tested against
        elapsed (timespan) - The time it took to execute the test, e.g. "30s"
                             or "1m 45s"
        defects (string) - A comma-separated list of defects to link to the
                           test result
        assignedto_id (int) - The ID of a user the test should be assigned to

        Custom Field Types: [Name (Type) - Description]
        -----------------------------------------------
        Checkbox (bool) - True for checked and False otherwise
        Date (string) - A date in the same format as configured for TestRail
                        and API user (e.g. "07/08/2013")
        Dropdown (int) - The ID of a dropdown value as configured in the field
                         configuration
        Integer (int) - A valid integer
        Milestone (int) - The ID of a milestone for the custom field
        Multi-select (array) - An array of IDs as configured in the field
                               configuration
        Step Results (array) - An array of objects specifying the step
                               results. Also see the example below.
        String (string) - A valid string with a maximum length of 250
                          characters
        Text (string) - A string without a maximum length
        URL (string) - A string with matches the syntax of a URL
        User (int) - The ID of a user for the custom field
        """
        return self.request(
            self.POST,
            'add_result/%s' % test_id,
            json=data
        )

    def add_result_for_case(self, run_id, case_id, data={}):
        """Add a new test result, comment, or assigns a test.

        Use add_results_for_cases instead if you plan to add results for
        multiple tests.

        Custom fields are supported as well and must be submitted with their
        system name, prefixed with 'custom_'.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        run_id (int) - The ID of the test run (required)
        case_id (int) - The ID of the test case (required)
        -------------------------------------------
        status_id (int) - The ID of the test status. The built-in system
                          statuses have the following IDs:
                          PASSED   (=1)
                          BLOCKED  (=2)
                          RETEST   (=4)
                          FAILED   (=5)
                          You can get a full list of system and custom
                          statuses via get_statuses.
        comment (string) - The comment / description for the test result
        version (string) - The version or build you tested against
        elapsed (timespan) - The time it took to execute the test, e.g. "30s"
                             or "1m 45s"
        defects (string) - A comma-separated list of defects to link to the
                           test result
        assignedto_id (int) - The ID of a user the test should be assigned to

        Custom Field Types: [Name (Type) - Description]
        -----------------------------------------------
        Checkbox (bool) - True for checked and False otherwise
        Date (string) - A date in the same format as configured for TestRail
                        and API user (e.g. "07/08/2013")
        Dropdown (int) - The ID of a dropdown value as configured in the field
                         configuration
        Integer (int) - A valid integer
        Milestone (int) - The ID of a milestone for the custom field
        Multi-select (array) - An array of IDs as configured in the field
                               configuration
        Step Results (array) - An array of objects specifying the step
                               results. Also see the example below.
        String (string) - A valid string with a maximum length of 250
                          characters
        Text (string) - A string without a maximum length
        URL (string) - A string with matches the syntax of a URL
        User (int) - The ID of a user for the custom field
        """
        return self.request(
            self.POST,
            'add_result_for_case/%s/%s%s' % (
                run_id,
                case_id,
                TestRailAPI.uri_field_appends(data)
            )
        )

    def add_results(self, run_id, data={}):
        """Add a new test result, comment, or assign a test.

        This method expects an array of test results via the 'results' field.
        Each test result must specify the test ID.

        Custom fields are supported as well and must be submitted with their
        system name, prefixed with 'custom_'.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        run_id (int) - The ID of the test run the result should be applied to
                       (required)
        -------------------------------------------
        results (list) - The test results
            test_id (int) - The ID of the test (required)
            status_id (int) - The ID of the test status. The built-in system
                              statuses have the following IDs:
                              PASSED   (=1)
                              BLOCKED  (=2)
                              RETEST   (=4)
                              FAILED   (=5)
                              You can get a full list of system and custom
                              statuses via get_statuses.
            comment (string) - The comment / description for the test result
            version (string) - The version or build you tested against
            elapsed (timespan) - The time it took to execute the test, e.g.
                                 "30s" or "1m 45s"
            defects (string) - A comma-separated list of defects to link to the
                               test result
            assignedto_id (int) - The ID of a user the test should be assigned
                                  to

        Custom Field Types: [Name (Type) - Description]
        -----------------------------------------------
        Checkbox (bool) - True for checked and False otherwise
        Date (string) - A date in the same format as configured for TestRail
                        and API user (e.g. "07/08/2013")
        Dropdown (int) - The ID of a dropdown value as configured in the field
                         configuration
        Integer (int) - A valid integer
        Milestone (int) - The ID of a milestone for the custom field
        Multi-select (array) - An array of IDs as configured in the field
                               configuration
        Step Results (array) - An array of objects specifying the step
                               results. Also see the example below.
        String (string) - A valid string with a maximum length of 250
                          characters
        Text (string) - A string without a maximum length
        URL (string) - A string with matches the syntax of a URL
        User (int) - The ID of a user for the custom field
        """
        return self.request(
            self.POST,
            'add_results/%s' % run_id,
            json=data
        )

    def add_results_for_cases(self, run_id, data={}):
        """Add one or more new test results, comments, or assign tests.

        This method expects an array of test results via the 'results' field.
        Each test result must specify the test case ID.

        Custom fields are supported as well and must be submitted with their
        system name, prefixed with 'custom_'.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        run_id (int) - The ID of the test run (required)
        -------------------------------------------
        results (list) -
            case_id (int) - The ID of the test case (required)
            status_id (int) - The ID of the test status. The built-in system
                              statuses have the following IDs:
                              PASSED   (=1)
                              BLOCKED  (=2)
                              RETEST   (=4)
                              FAILED   (=5)
                              You can get a full list of system and custom
                              statuses via get_statuses.
            comment (string) - The comment / description for the test result
            version (string) - The version or build you tested against
            elapsed (timespan) - The time it took to execute the test, e.g.
                                 "30s" or "1m 45s"
            defects (string) - A comma-separated list of defects to link to the
                               test result
            assignedto_id (int) - The ID of a user the test should be assigned
                                  to

        Custom Field Types: [Name (Type) - Description]
        -----------------------------------------------
        Checkbox (bool) - True for checked and False otherwise
        Date (string) - A date in the same format as configured for TestRail
                        and API user (e.g. "07/08/2013")
        Dropdown (int) - The ID of a dropdown value as configured in the field
                         configuration
        Integer (int) - A valid integer
        Milestone (int) - The ID of a milestone for the custom field
        Multi-select (array) - An array of IDs as configured in the field
                               configuration
        Step Results (array) - An array of objects specifying the step
                               results. Also see the example below.
        String (string) - A valid string with a maximum length of 250
                          characters
        Text (string) - A string without a maximum length
        URL (string) - A string with matches the syntax of a URL
        User (int) - The ID of a user for the custom field
        """
        return self.request(
            self.POST,
            'add_results_for_cases/%s' % run_id,
            json=data
        )

    # Test Runs #
    def get_run(self, run_id):
        """Return an existing test run.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        run_id (int) - The ID of the test run (required)
        """
        return self.request(self.GET, 'get_run/%s' % run_id)

    def get_runs(self, project_id, data={}):
        """Return a list of test runs for a project not part of a test plan.

        Custom fields are supported as well and must be submitted with their
        system name, prefixed with 'custom_'.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        project_id (int) - The ID of the project (required)

        Custom Field Types: [Name (Type) - Description]
        -----------------------------------------------
        created_after (timestamp) - Only return test runs created after this
                                    date (as UNIX timestamp).
        created_before (timestamp) - Only return test runs created before this
                                     date (as UNIX timestamp).
        created_by (list) - A comma-separated list of creators (user IDs) to
                            filter by.
        is_completed (bool) - True to return completed test runs only.
                              False to return active test runs only.
        limit (int) - Limit the result to specific number of test runs.
        offset  (int) - Skip records.
        milestone_id (list) - A comma-separated list of milestone IDs to
                              filter by.
        suite_id (list) - A comma-separated list of test suite IDs to filter
                          by.
        """
        return self.request(
            self.GET,
            'get_runs/%s%s' % (
                project_id,
                TestRailAPI.uri_field_appends(data)
            )
        )

    def get_statuses(self):
        """Return a list of available test statuses."""
        return self.request(self.GET, 'get_statuses')

    def add_run(self, project_id, data={}):
        """Create a new test run.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        project_id (int) - The ID of the project (required)
        -------------------------------------------
        suite_id (int) - The ID of the test suite for the test run (optional
                         if the project is operating in single suite mode,
                         required otherwise)
        name (string) - The name of the test run
        description (string) - The description of the test run
        milestone_id (int) - The ID of the milestone to link to the test run
        assignedto_id (int) - The ID of the user the test run should be
                              assigned to
        include_all (bool) - True for including all test cases of the test
                             suite and False for a custom case selection
                             (default: True)
        case_ids (list) - An array of case IDs for the custom case selection
        """
        return self.request(
            self.POST,
            'add_run/%s' % project_id,
            json=data
        )

    def update_run(self, run_id, data={}):
        """Update an existing test run.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        run_id (int) - The ID of the test run (required)
        -------------------------------------------
        name (string) - The name of the test run
        description (string) - The description of the test run
        milestone_id (int) - The ID of the milestone to link to the test run
        include_all (bool) - True for including all test cases of the test
                             suite and False for a custom case selection
                             (default: True)
        case_ids (array) - An array of case IDs for the custom case selection
        """
        return self.request(
            self.POST,
            'update_run/%s' % run_id,
            json=data
        )

    def close_run(self, run_id):
        """Close an existing test run and archive its tests and results.

        Closing is permanent and cannot be undone.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        run_id (int) - The ID of the test run (required)
        """
        return self.request(self.POST, 'close_run/%s' % run_id)

    def delete_run(self, run_id):
        """Delete an existing test run.

        Deletion is permanent and cannot be undone.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        run_id (int) - The ID of the test run (required)
        """
        return self.request(self.POST, 'delete_run/%s' % run_id)

    def get_test(self, test_id):
        """Return an existing test.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        test_id (int) - The ID of the test (required)
        """
        return self.request(self.GET, 'get_test/%s' % test_id)

    def get_tests(self, run_id, data={}):
        """Return an existing test.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        run_id (int) - The ID of the test run (required)
        -------------------------------------------
        status_id (list) - A comma-separated list of status IDs to filter by
        """
        return self.request(
            self.GET,
            'get_tests/%s%s' % (
                run_id,
                TestRailAPI.uri_field_appends(data)
            )
        )

    # Section Management #
    def get_section(self, section_id):
        """Return an existing section.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        section_id (int) - The ID of the section (required)
        """
        return self.request(self.GET, 'get_section/%s' % section_id)

    def get_sections(self, project_id, data={}):
        """Return a list of sections for a project and test suite.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        project_id (int) - The ID of the project (required)
        -------------------------------------------
        suite_id (int) - The ID of the test suite (optional if the project is
                         operating in single suite mode)
        """
        return self.request(
            self.GET,
            'get_sections/%s%s' % (
                project_id,
                TestRailAPI.uri_field_appends(data)
            )
        )

    def add_section(self, project_id, name, data={}):
        """Create a new section under a project.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        project_id (int) - The ID of the project (required)
        name (string) - The name of the section (required)
        -------------------------------------------
        description (string) - The description of the section (added with
                               TestRail 4.0)
        suite_id (int) - The ID of the test suite (ignored if the project is
                         operating in single suite mode, required otherwise)
        parent_id (int) - The ID of the parent section (to build section
                          hierarchies)
        """
        return self.request(
            self.POST,
            'add_section/%s' % project_id,
            json=data
        )

    def update_section(self, section_id, data={}):
        """Update an existing section.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        section_id (int) - The ID of the section (required)
        -------------------------------------------
        description (string) - The description of the section (added with
                               TestRail 4.0)
        name (string) - The name of the section
        """
        return self.request(
            self.POST,
            'update_section/%s' % section_id,
            json=data
        )

    def delete_section(self, section_id):
        """Delete an existing section.

        Deletion is permanent and cannot be undone.

        Request Fields: [Name (Type) - Description]
        -------------------------------------------
        section_id (int) - The ID of the section (required)
        """
        return self.request(self.POST, 'delete_section/%s' % section_id)


class TestRailAPIError(Exception):
    """Inline error class for TestRailAPI."""

    pass


if __name__ == "__main__":
    # execute only if run as a script
    rail = TestRailAPI('https://%s.testrail.net/' %
                       os.environ['TESTRAIL_GROUP'])
    TestRailAPI.SHOW_ALL_RESULTS = True
    user_one = rail.get_user_by_id(1)
    email = user_one['email']
    email_user = rail.get_user_by_email(email)
    user_list = rail.get_users()
    projects = rail.get_projects()
    project = rail.get_project(1)
    milestones = rail.get_milestones(1)
    plan = rail.get_plan(90)
    plans = rail.get_plans(1)
    suite = rail.get_suite(1)
    suites = rail.get_suites(1)
    case = rail.get_case(1)
    cases = rail.get_cases(1, {'suite_id': 1, })
    fields = rail.get_case_fields()
    types = rail.get_case_types()
    priorities = rail.get_priorities()
    templates = rail.get_templates(1)
    result_fields = rail.get_result_fields()
    results = rail.get_results(6865)
    case_results = rail.get_results_for_case(65, 2)
    run_results = rail.get_results_for_run(65)
    test_run = rail.get_run(65)
    test_runs = rail.get_runs(1)
    statuses = rail.get_statuses()
    test = rail.get_test(6865)
    tests = rail.get_tests(65)
    section = rail.get_section(1)
    sections = rail.get_sections(1, {'suite_id': 1, })
