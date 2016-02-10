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
            print(response.status_code, response.text)
        except requests.exceptions.RequestException as e:
            response = e.read()
            error = e
        return (response, error)

    def request(self, method=GET, uri='', data=None):
        """Combined HTTP requester."""
        response, error = self._request_call(method, uri, data)
        if response.status_code == '429':
            # too many requests sent; wait required sec then resend request
            snooze = response.json()['Retry-After']
            sleep(int(snooze) + 1)
            response, error = self._request_call(method, uri, data)
        result = json.loads(response.text) if response else {}
        if error is not None:
            message = '' if 'error' not in result else result['error']
            raise TestRailAPIError('Error return: %s (%s)' %
                                   (error.code, message))
        return response

    # Reference Users #
    def get_user_by_id(self, _id):
        """Return user information for a specific user ID."""
        return self.request(self.GET, 'get_user/%s' % _id)

    def get_user_by_email(self, email):
        """Return user information for a specific user email."""
        return self.request(self.GET, 'get_user_by_email&email=%s' % email)

    def get_users(self):
        """Return the list of users."""
        return self.request(self.GET, 'get_users')


class TestRailAPIError(Exception):
    """Inline error class for TestRailAPI."""

    pass


if __name__ == "__main__":
    # execute only if run as a script
    rail = TestRailAPI('https://%s.testrail.net/' %
                       os.environ['TESTRAIL_GROUP'])
    print(rail)
    user_one = rail.get_user_by_id(1)
    print(user_one)
    user_list = rail.get_users()
    for user in user_list:
        print(json.dumps(user))
