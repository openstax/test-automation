## Test Rail Automation ##

### Execution Path 1 - Test Full Suite ###

`/suites/view/<suite_id>` => 'Start Automated Tests'
1. Creates a new test run for `<suite_id>`
2. Forwards the test information to the intermediary system
3. Intermediary sends the task information to the Jenkins system
4. Jenkins activates the test
5. Jenkins returns the task result
6. Intermediary sends the result to Test Rail

### Execution Path 2 - Automate Test Run ###

`/runs/view/<run_id>` => 'Start Automated Tests'
1. Forwards the test information to the intermediary system
2. Intermediary sends the task information to the Jenkins system
3. Jenkins activates the test
4. Jenkins returns the task result
5. Intermediary sends the result to Test Rail
