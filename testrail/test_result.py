"""Breakup result.xml to send to TestRail."""


from defusedxml import ElementTree
import os
from testrail import TestRailAPI


def find_test_id(case_id, tests):
    """Find the case number and return the test ID."""
    try:
        case = case_id if type(case_id) is int else int(case_id)
    except ValueError:
        print('Case "%s" is not a valid case ID.' % case_id)
        return -1
    for test in tests:
        if case == test['case_id']:
            return test['id']
    return -1


def get_status(string):
    """Replace status tag with TestRail's status code."""
    if string == 'passed':
        return TestRailAPI.PASSED
    elif string == 'failure':
        return TestRailAPI.FAILED
    return TestRailAPI.UNTESTED


def get_time_string(time):
    """Return a TestRail test time string from the full time in seconds."""
    to_string = ''
    new_time = int(float(time))
    if new_time <= 0:
        return '1s'
    hours = int(new_time / 3600)
    new_time = new_time - (hours * 3600)
    minutes = int(new_time / 60)
    new_time = new_time - (minutes * 60)
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


path = '/Users/fitch/projects/automation/test-automation/tmp/xml/'
file = path + 'result.xml'
run_file = path + 'version.txt'
run = ''
if not os.path.exists(file):
    raise FileNotFoundError('Results file not found.')  # NOQA
with open(run_file, 'r') as f:
    run = f.readline()
tree = ElementTree.parse(file)
root = tree.getroot()
# print(tree)
# print(root.tag, root.attrib)
tr = TestRailAPI(url='https://openstax.testrail.net/')
test_set = tr.get_tests(run_id=int(run))
# print(test_set)
# url, user, key, headers, json:
line = '\n'
for child in root:
    child.attrib['case'] = child.attrib['name'].split('_')[-1]
    child.attrib['test'] = find_test_id(child.attrib['case'], test_set)
    sub = list(child.iter())
    if len(sub) >= 2:
        # print(str(sub))
        child.attrib['status'] = sub[1].tag
        child.attrib['message'] = sub[1].attrib['message']
        child.attrib['text'] = sub[1].text
    else:
        child.attrib['status'] = 'passed'
        child.attrib['message'] = ''
        child.attrib['text'] = ''
    line += '%s :\n' % child.tag
    for key in child.attrib:
        line += '    %s : %s\n' % (key, child.attrib[key])
    # print(child.tag, child.attrib)
# print(line)

results = []
for child in root:
    if child.attrib['status'] != 'skipped':
        results.append({
            'test_id': child.attrib['test'],
            'status_id': get_status(child.attrib['status']),
            'comment': '{0}{1}'.format(child.attrib['message'],
                                       child.attrib['text']),
            'version': '',
            'elapsed': get_time_string(child.attrib['time']),
            'defects': '',
            'assignedto_id': '',
        })
print(len(results), results)

package = tr.add_results(run_id=int(run), data={'results': results})
