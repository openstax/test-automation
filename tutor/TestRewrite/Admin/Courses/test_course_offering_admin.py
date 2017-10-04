"""
System: ??
Title: Test Course Offering
User(s): Admin
Testrail ID: C148085


Jacob Diaz
7/26/17


Corresponding Case(s):
t1.58 01 --> 06


Progress:
None

Work to be done/Questions:
Test code from corresponding cases copied over  from t1.58 and reworked
together

Merge-able with any scripts? If so, which? :
Other admin control console scripts?

"""


def test_course_offering_admin(self):
        """
        Go to https://tutor-qa.openstax.org/
        Click on the 'Login' button
        Enter the admin user account [ admin | password ] in the username and
        password text boxes
        Click on the 'Sign in' button
        Open the drop down menu by clicking on the user menu link containing
        the user's name

        Click on the 'Admin' button
        Open the drop down menu by clicking 'Course Organization'
        Click the 'Catalog Offerings' button
        Click the 'Add offering' button
        Enter text into the 'Salesforce book name' text box
        Enter text into the 'Appearance code' text box
        Enter text into the 'Description' text box
        Choose an option in the 'Ecosystem' drop down menu
        Check either the 'Works for full Tutor?' or the 'Works for Concept
        Coach?' button
        Enter text into the 'Pdf url" text box
        Enter text into the 'Webview url' text box
        Enter text into the 'Default course name' text box
        Click the 'Save' button
        ***The user is returned to the Catalog Offerings page and the text
        'The offering has been created.' is displayed.(t1.58.01)***

        Click the 'Edit' link for the desired course
        Edit the text in the 'Salesforce book name' text box
        Click the 'Save' button
        ***The Catalog Offerings page is reloaded with the changes visible and
        the text 'The offering has been updated.' is visible. (t1.58.02)***

        Click the 'Edit' link for the desired course
        Select a different option in the 'Ecosystem' drop down menu
        Click the 'Save' button
        ***The Catalog Offerings page is reloaded with the changes visible and
        the text 'The offering has been updated.' is visible. (t1.58.03)***

        Click the 'Edit' link for the desired course
        Edit the checkboxes for 'Works for full Tutor?' and 'Works for Concept
        Coach?'
        Click the 'Save' button
        ***The user is returned to the Catalog Offerings page with the changes
        visible. The text 'The offering has been updated.' is visible.
        (t1.58.04)***

        Click the 'Edit' link for the desired course
        Edit the text in the 'Pdf url' text box
        Edit the text in the 'Webview url' text box
        Click the 'Save' button
        ***The user is returned to the Catalog Offerings page with the changes
        visible. The text 'The offering has been updated.' is visible.
        (t1.58.05)***

        Click the 'Edit' link for the desired course
        Edit the text in the 'Default course name' text box
        Click the 'Save' button
        ***The user is returned to the Catalog Offerings page with the changes
        visible. The text 'The offering has been updated.' is visible.
        (t1.58.06)***


        Corresponds to...
        t1.58 01 --> 06
        :return:
        """
