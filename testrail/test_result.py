"""Breakup result.xml to send to TestRail."""

import getopt
import operator
import os
import sys

from defusedxml import ElementTree
from functools import reduce
try:
    from staxrail.testrail import TestRailAPI
except ImportError:
    from testrail import TestRailAPI


class Result(object):
    """Test Result Control."""

    NEW_LINE = ''.join([chr(10), chr(13)])

    def __init__(self, url, path='./', data='result.xml', debug=False):
        """Result class constructor."""
        self.debugging = debug
        self.file = ''.join([path, '/', data])
        self.run_id = os.getenv('RUNID')
        self.tree, self.root = self.get_tree()
        self.test_rail = TestRailAPI(url=url)
        self.test_set = self.test_rail.get_tests(run_id=int(self.run_id))

    @classmethod
    def prod(cls, vals):
        """Non operator multiplier."""
        return reduce(operator.mul, vals, 1)

    def get_tree(self):
        """Return the tree and the tree root."""
        tree = ElementTree.parse(self.file)
        return tree, tree.getroot()

    def find_test_id(self, case_id, tests):
        """Return a test ID."""
        try:
            case = int(case_id)
        except ValueError:
            list_tests = []
            for val in tests:
                list_tests.append(val['case_id'])
            print(
                'Case "%s" is not a valid case ID in %s.' %
                (case_id, list_tests.sort())
            )
            return -1
        for test in tests:
            if case == test['case_id']:
                return test['id']
        return -1

    def get_status(self, string):
        """Return test status."""
        if string == 'passed':
            return TestRailAPI.PASSED
        elif string == 'failure':
            return TestRailAPI.FAILED
        return TestRailAPI.UNTESTED

    def get_time_string(self, time):
        """Return the time string."""
        to_string = ''
        new_time = int(float(time))
        if new_time <= 0:
            return '1s'
        hours = int(new_time / 3600)
        new_time = new_time - Result.prod([hours, 3600])
        minutes = int(new_time / 60)
        new_time = new_time - Result.prod([minutes, 60])
        seconds = int(new_time)
        if hours > 0:
            to_string += '%sh ' % hours
            if minutes == 0 and seconds == 0:
                return to_string[:-1]
        if minutes > 0:
            to_string += '%sm ' % minutes
            if seconds == 0:
                return to_string[:-1]
        return to_string + '%ss' % seconds

    def retrieve_test_results(self):
        """Split the tree."""
        for child in self.root:
            child.set(
                'case',
                child.get('name').split('_')[-1]
            )
            child.set(
                'test',
                self.find_test_id(child.get('case'), self.test_set)
            )
            sub = list(child.iter())
            if len(sub) >= 2:
                child.set('status', sub[1].tag)
                message = sub[1].get('message') if 'message' in \
                    sub[1].attrib else ''
                parts = message.split(
                    '_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ ' +
                    '_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _'
                )
                reorder = 'Break Point:' + Result.NEW_LINE + \
                          parts[0] + Result.NEW_LINE
                if len(parts) > 1:
                    final = str(parts[len(parts) - 1])
                    reorder = reorder + Result.NEW_LINE + \
                        'Reason:' + Result.NEW_LINE
                    reorder = reorder + \
                        final[:-operator.floordiv(len(final), 4)]
                    reorder = reorder + Result.NEW_LINE
                child.set('message', reorder)
                child.set('text', sub[1].text)
            else:
                child.set('status', 'passed')
                child.set('message', '')
                child.set('text', '')


def main(argv):
    """Script runner."""
    path = './'
    file_name = 'result.xml'
    server = ''
    # Process arguments
    try:
        options, arguments = getopt.getopt(
            argv,
            'hi:u:',
            ['help', 'input=', 'url=']
        )
    except getopt.GetoptError:
        print('test_result.py -i <input file> -u <url>')
        sys.exit(2)
    for option, argument in options:
        if option in ('-h', '--help'):
            print('test_result.py -i <input file> -u <url>')
            sys.exit()
        elif option in ('-i', '--input'):
            path, file_name = os.path.split(argument)
        elif option in ('-u', '--url'):
            server = argument
    # Break up the XML file
    runner = Result(path=path, data=file_name, url=server)
    # Process the tests
    runner.retrieve_test_results()
    # Build the data results for load
    results = []
    for child in runner.root:
        if 'status' not in child.attrib:
            child.set('status', 'skipped')
        if child.get('status') != 'skipped':
            if 'test' in child.attrib and child.get('test') != -1:
                results.append({
                    'test_id': child.get('test'),
                    'status_id': runner.get_status(child.get('status')),
                    'comment': child.get('message'),
                    'version': '',
                    'elapsed': runner.get_time_string(child.get('time')),
                    'defects': '',
                    'assignedto_id': '',
                })
    if len(results) < 2:
        results = [results]
    package = runner.test_rail.add_results(
        run_id=int(runner.run_id),
        data={'results': results}
    )
    print(package)


if __name__ == '__main__':
    # execute when run as a script
    main(sys.argv[1:])
