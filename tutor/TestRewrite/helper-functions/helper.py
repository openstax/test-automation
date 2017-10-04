from random import randint
import datetime
from time import strftime
from staxing.helper import Student, Teacher


def current_tutor_term(current_date):
    """
    Returns the current scholastic tutor term, which we can use in order to pick a
    course that's currently in session
    :param current_date:
    Today's date, in string format "mm/dd/year"
    :return:
        Current term:
        "Fall 2017" or "Summer 2018", for example
        Possible: Winter, Spring, Summer, Fall
    """
    month, day, year = [int(x) for x in current_date.split('/')]
    if month >= 1 and month <= 3:
        if month == 3 and day < 21 or month == 6 and day > 21:
            pass
        else:
            season = "Winter"

    if month >= 3 and month <= 6:
        if month == 3 and day < 21 or month == 6 and day > 21:
            pass
        else:
            season = "Spring"

    if month >= 6 and month <= 9:
        if month == 3 and day < 21 or month == 6 and day > 21:
            pass
        else:
            season = "Summer"

    if month >= 9 and month <= 12:
        if month == 9 and day < 21 or month == 12 and day > 21:
            pass
        else:
            season = "Fall"
    return season + ' ' + str(year)

### THIS IS A METHOD
def teacher_make_late_assignment(self, assignment_type, course_no, hw_name = None):
    """
    Uses: datetime, time.strftime

    Makes a late assignment --> usually due within a very short
    period of time from when it was made

    :param hw_name: (str) --> name that we're gonna give the assignment
    :param assignment_type: (str) --> type of assignment we want to make
        (options: homework, reading, external, event)
    :param course_no: (str) --> course number we want to make the assignment for
    :return:
    """
    self.teacher.login()
    today = datetime.date.today()
    begin = (today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
    end = (today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
    time_format = "%I %M %p"
    time_now = strftime(time_format)
    # of format "HH MM am/pm"

    if assignment_type.lower() == 'reading':
        heading = 'Read'

    if assignment_type.lower() == 'homework':
        heading = 'HW'

    if assignment_type.lower() == 'external':
        heading = 'Ext'

    if assignment_type.lower() == 'event':
        heading = 'Event'

    assignment_name = '{0} no.{1}: {2}'.format(heading,str(randint(0, 100)), str(today))

    ### WHAT NEEDS TO BE DONE:
    ### DECIDE HOW I'M GOGIN TO CHANGE THE ASSIGNMENT DUE DATE TO BE A MINUTE FROM NOW -->
        ### WILL I HAVE TO DO THIS DURING THE ASSINGMNET CREATION PROCESS?
        ### OR IWLL I HAVE TO DO THIS BY EDITING THE ASSIGNMNETM AFTER CREATING IT?
    ### IF I'M GONNA EDIT THE ASSIGNMENT, WRITE THE CODE TO DO THIS --> OR DOES SOMEONE ALREADY HAVE IT?
