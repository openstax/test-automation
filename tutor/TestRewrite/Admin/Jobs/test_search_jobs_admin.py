"""
Title: test search job
User(s): admin
Testrail ID: C148086


Jacob Diaz
7/26/17


Corresponding Case(s):
t1.58 21 --> 25


Progress:
None

Work to be done/Questions:
Copy code over from t1.58
Add setup and teardown and imports

Merge-able with any scripts? If so, which? :
Other admin courses, maybe bring them all to the control console in setup
"""


def test_search_job_admin():
        """
        Go to https://tutor-qa.openstax.org/
        Login to admin account

        Open the drop down menu by clicking on the user menu link containing
        the user's name
        Click on the 'Admin' button
        Click the 'Jobs' button
        Enter a job ID into the text box labeled 'Search by ID, Status, or
        Progress'
        ***The results to the search are displayed. (t1.58.21)***


        Click the 'Jobs' button
        Enter a job status into the text box labeled 'Search by ID, Status, or
        Progress'
        ***The results to the search are displayed. (t1.58.22)***

        Click the 'Jobs' button
        Enter a job progress percentage into the text box labeled 'Search by
        ID, Status, or Progress'
        ***The results to the search are displayed. (t1.58.23)***


        Click the 'Jobs' button
        Click one of the status tabs to filter jobs
        ***Jobs that fit the filter condition are displayed. (t1.58.24)***

        Click the 'Jobs' button
        Click on a Job ID
        ***The report for the job is displayed (t1.58.25)***


        Corresponds to...
        t1.58 21 --> 25
        :return:
        """
        # (t1.58.21) --> The results to the search are displayed.
        # (t1.58.22) --> The results to the search are displayed.
        # (t1.58.23)--> The results to the search are displayed.
        # (t1.58.24)--> Jobs that fit the filter condition are displayed.
        # (t1.58.25) --> The report for the job is displayed
