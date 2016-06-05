"""Breakup result.xml to send to TestRail."""

from defusedxml import ElementTree
import operator
from functools import reduce
import os
try:
    from staxrail.testrail import TestRailAPI
except ImportError:
    from testrail import TestRailAPI


def prod(vals):
    """Non operator multiplier."""
    return reduce(operator.mul, vals, 1)


def find_test_id(case_id, tests):
    """Return a test ID."""
    try:
        case = int(case_id)
    except ValueError:
        print('Case "%s" is not a valid case ID.' % case_id)
        return -1
    for test in tests:
        if case == test['case_id']:
            return test['id']
    return -1


def get_status(string):
    """Return test status."""
    if string == 'passed':
        return TestRailAPI.PASSED
    elif string == 'failure':
        return TestRailAPI.FAILED
    return TestRailAPI.UNTESTED


def get_time_string(time):
    """Return the time string."""
    to_string = ''
    new_time = int(float(time))
    if new_time <= 0:
        return '1s'
    hours = int(new_time / 3600)
    new_time = new_time - prod([hours, 3600])
    minutes = int(new_time / 60)
    new_time = new_time - prod([minutes, 60])
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

path = './'
file = path + 'result.xml'
run = os.getenv('RUNID', 150)
tree = ElementTree.parse(file)
root = tree.getroot()
tr = TestRailAPI(url='https://openstax.testrail.net/')
test_set = tr.get_tests(run_id=int(run))
for child in root:
    child.attrib['case'] = child.attrib['name'].split('_')[-1]
    child.attrib['test'] = find_test_id(child.attrib['case'], test_set)
    sub = list(child.iter())
    if len(sub) >= 2:
        child.attrib['status'] = sub[1].tag
        child.attrib['message'] = sub[1].attrib['message']
        child.attrib['text'] = sub[1].text
    else:
        child.attrib['status'] = 'passed'
        child.attrib['message'] = ''
        child.attrib['text'] = ''

results = []
for child in root:
    if child.attrib['status'] != 'skipped':
        results.append({
            'test_id': child.attrib['test'],
            'status_id': get_status(child.attrib['status']),
            'comment': '{0}{1}'.format(
                child.attrib['message'],
                child.attrib['text']
            ),
            'version': '',
            'elapsed': get_time_string(child.attrib['time']),
            'defects': '',
            'assignedto_id': '',
        })
print(chr(10), 'Results:', chr(10), results, chr(10))
package = tr.add_results(run_id=int(run), data={'results': results})
