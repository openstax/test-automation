"""Convert test_result.py into jenkins_junit_results."""

import os

if os.path.isfile('test_result.py'):
    with open('test_result.py', 'r') as file_in:
        with open('jenkins_junit_results', 'w') as file_out:
            file = file_in.read()
            file = str.replace(file, ' \\', ' \\\\')
            file = str.replace(file, '    ', '\\t')
            file = str.replace(file, '\n', '\\n')
            file_out.write(file)
