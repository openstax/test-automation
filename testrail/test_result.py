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

DEBUG = os.getenv('DEBUG', False)


class Result(object):
    """Test Result Control."""

    NEW_LINE = ''.join([chr(10), chr(13)])

    def __init__(self, url, path='./', data='result.xml', debug=False):
        """Result class constructor."""
        self.debugging = debug
        self.file = ''.join([path, '/', data])
        if self.debugging:
            print('File', self.file)
        self.run_id = os.getenv('RUNID')
        if self.debugging:
            print('RunID', self.run_id)
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

    @classmethod
    def print_xml_tree(cls, root):
        """Print all tags and attributes."""
        print(root.tag, root.attrib)
        for node in root.iter():
            print(node.tag, node.attrib)

    def retrieve_test_results(self):
        """Split the tree."""
        for child in self.root:
            child.attrib['case'] = child.attrib['name'].split('_')[-1]
            child.attrib['test'] = self.find_test_id(child.attrib['case'],
                                                     self.test_set)
            sub = list(child.iter())
            if len(sub) >= 2:
                child.attrib['status'] = sub[1].tag
                if DEBUG:
                    print(child.attrib)
                message = sub[1].attrib['message'] if 'message' in \
                    sub[1].attrib else ''
                parts = message.split(
                    '_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ ' +
                    '_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _'
                )
                if self.debugging:
                    for i, x in enumerate(parts):
                        print(Result.NEW_LINE + '====================', i, x,
                              Result.NEW_LINE + '====================')
                reorder = 'Break Point:' + Result.NEW_LINE + \
                          parts[0] + Result.NEW_LINE
                if len(parts) > 1:
                    final = str(parts[len(parts) - 1])
                    reorder = reorder + Result.NEW_LINE + \
                        'Reason:' + Result.NEW_LINE
                    reorder = reorder + \
                        final[:-operator.floordiv(len(final), 4)]
                    reorder = reorder + Result.NEW_LINE
                child.attrib['message'] = reorder
                if self.debugging:
                    print(reorder)
                child.attrib['text'] = sub[1].text
            else:
                child.attrib['status'] = 'passed'
                child.attrib['message'] = ''
                child.attrib['text'] = ''


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
            if DEBUG:
                print('Path:', path)
                print('File:', file_name)
        elif option in ('-u', '--url'):
            server = argument
            if DEBUG:
                print('URL: ', server)
    # Break up the XML file
    runner = Result(path=path, data=file_name, url=server)
    # Process the tests
    runner.retrieve_test_results()
    # Build the data results for load
    results = []
    for child in runner.root:
        if DEBUG:
            print(Result.NEW_LINE)
            for key in child.attrib:
                print(key, ':', child.attrib[key])
        if 'status' not in child.attrib:
            child.attrib['status'] = 'skipped'
        if child.attrib['status'] != 'skipped':
            if 'test_id' in child.attrib and child.attrib['test_id'] != -1:
                results.append({
                    'test_id': child.attrib['test'],
                    'status_id': runner.get_status(child.attrib['status']),
                    'comment': child.attrib['message'],
                    'version': '',
                    'elapsed': runner.get_time_string(child.attrib['time']),
                    'defects': '',
                    'assignedto_id': '',
                })
    if DEBUG:
        print(' ')
        print('Run:', int(runner.run_id))
        print('Results:')
    if len(results) < 2:
        results = [results]
    if DEBUG:
        for result in results:
            print('\t', result)
    package = runner.test_rail.add_results(run_id=int(runner.run_id),
                                           data={'results': results})
    if DEBUG:
        print(package)


if __name__ == '__main__':
    # execute when run as a script
    main(sys.argv[1:])
