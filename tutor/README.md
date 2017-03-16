Tutor Automation Installation/Configuration
===========================================

Install X-Code
--------------
Open a terminal
```xcode-select --install```
Click Install
Click Agree for the license

Install Homebrew
----------------
```ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"```
Follow the on-terminal prompts
```
brew doctor
brew update
brew upgrade
echo 'export PATH="/usr/local/bin:/usr/local/sbin:$PATH"' >> ~/.bash_profile
```

Install Git
-----------
```brew install git```

Optional: Install GitHub for Mac
--------------------------------
Go to: https://mac.github.com/
Either Sign Up or Sign In

Install Python 3
----------------
```brew install python3```

Environment Setup
-----------------
```
pip3 install virtualenvwrapper
cd
mkdir projects
mkdir .virtualenvs
```

Open your profile in a text editor (options may be)
1) ~/.profile
2) ~/.bashrc
3) ~/.bash_profile

Add the following to the profile:
```
export SAUCE_USERNAME=''
export SAUCE_ACCESS_KEY=''
export SERVER_URL=''
export ADMIN_USER=''
export ADMIN_PASSWORD=''
export TEACHER_USER=''
export TEACHER_USER_MULTI=''
export TEACHER_USER_CC=''
export TEACHER_PASSWORD=''
export STUDENT_USER=''
export STUDENT_USER_MULTI=''
export STUDENT_USER_CC=''
export STUDENT_PASSWORD=''
export TEST_EMAIL_USER=''
export TEST_EMAIL_ACCOUNT=''
export TEST_EMAIL_PASSWORD=''
export CONTENT_USER=''
export CONTENT_PASSWORD=''
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/projects
export VIRTUALENVWRAPPER_PYTHON='/usr/local/bin/python3.6'
export VIRTUALENVWRAPPER_VIRTUALENV_ARGS='--no-site-packages'
export VIRTUALENVWRAPPER_WORKON_CD='cdproject'
source /usr/local/bin/virtualenvwrapper.sh
close() { deactivate && cd; }
```

Repository
----------
```mkproject automation```

Switch into the automation project folder if it isn't already
```
git clone https://github.com/openstax/test-automation
cd test-automation
pip3 install -r tutor/requirements.txt
```

Tutor Automation Project
========================
Status:
-------

|Finished?|Verified?|Epic|Epic Name|Started|Total Cases|Notes|
|:-------:|:-------:|----|---------|------:|----------:|-----|
| | |CC1.01|Recruiting Teachers|0|21| |
|&#x2611;|&#x2611;|CC1.02|Wise Wire and OpenStax Content Generation|0|0|No user cases|
| | |CC1.03|Content Preparation and Import|0|10| |
| | |CC1.04|Exercise Editing and QA|0|30| |
| | |CC1.05|CNX Navigation|0|6| |
| | |CC1.06|Concept Coach Widget Mechanics and Infrastructure|0|3| |
| | |CC1.07|Student Registration, Enrollment, Login and Authentication|0|19| |
| | |CC1.08|Students Work Assignments|0|13| |
| | |CC1.09|Student Progress Views|0|5| |
| | |CC1.10|Admin and Teacher Course Setup|0|17| |
| | |CC1.11|Teacher Login and Authentication|0|3| |
| | |CC1.12|Delivering Assignments|0|6| |
| | |CC1.13|Teacher Views|0|14| |
| | |CC1.14|Training and Supporting Teachers and Students|0|11| |
| | |CC1.15|OpenStax Metrics|0|1| |
|&#x2611;|&#x2611;|CC1.16|Concept Coach Pilots|0|0|No user cases|
|&#x2611;|&#x2611;|CC1.17|Hot Fixes|0|0|No user cases|
|&#x2611;|&#x2611;|CC2.03|Gain Accessibility Compliance|0|0|No user cases|
| | |CC2.08|Improves Scores Reporting|0|13| |
| | |CC2.09|Improve Login, Registration, Enrollment|0|7| |
| | |CC2.11|Improve Question Management|0|6| |
| | |CC2.18|Guide, Monitor, Support &amp; Train Users|0|3| |
| | |T1.13|View the calendar dashboard|10|14|In progress|
| | |T1.14|Create a reading|0|36| |
|&#x2611;| |T1.16|Create a homework|57|57| |
| | |T1.18|Create an external assignment|31|32|In progress|
| | |T1.21|Create an event|16|21|In progress|
|&#x2611;| |T1.22|View class performance|8|8| |
| | |T1.23|View class scores|22|23|In progress|
| | |T1.27|Tutor works with CNX|0|2| |
| | |T1.28|Work a reading|12|21|In progress|
| | |T1.34|Account management|0|23| |
|&#x2611;| |T1.35|Contract controls|11|11| |
|&#x2611;|&#x2611;|T1.36|User login|11|11| |
|&#x2611;| |T1.37|Account maintenance|7|7| |
|&#x2611;| |T1.38|Choose course|4|4| |
|&#x2611;| |T1.42|Edit course settings and roster|10|10| |
|&#x2611;| |T1.45|View the list dashboard|13|13| |
|&#x2611;| |T1.48|Work an external assignment|6|6| |
|&#x2611;| |T1.50|View student performance|10|10| |
|&#x2611;| |T1.55|Practice|14|14| |
| | |T1.57|Course maintenance|2|5|In progress|
| | |T1.58|Manage ecosystems|21|25|In progress|
| | |T1.59|Manage districts, schools, and courses|19|20|In progress|
|&#x2611;| |T1.68|Generate reports|1|1| |
| | |T1.71|Work a homework|21|24|In progress|
|&#x2611;|&#x2611;|T2.01|Generate &amp; Import Content for College Physics, Bio, Sociology|0|0|No user cases|
|&#x2611;|&#x2611;|T2.02|Research: Analyzing Data, Emerging Insights|0|0|No user cases|
|&#x2611;|&#x2611;|T2.03|Research: Electronic Consent|0|0|No user cases|
|&#x2611;|&#x2611;|T2.04|Gain Accessibility Compliance|0|0|No user cases|
| | |T2.05|Analyze College Workflow|0|4| |
| | |T2.07|Improve Course Management|0|9| |
| | |T2.08|Improve Scores Reporting|0|12| |
| | |T2.09|Improve Login, Registration, Enrollment|0|29| |
| | |T2.10|Improve Assignment Management|0|19| |
| | |T2.11|Question Work: Faculty Reviews, Excludes, Edits, Creates Assignments|0|46| |
| | |T2.12|Create New Question &amp; Assignment Types|0|5| |
| | |T2.13|Simplify &amp; Improve Readings|0|2| |
| | |T2.14|Improve Practice and Forecast|0|3| |
|&#x2611;|&#x2611;|T2.15|Faculty Recruitment|0|0|No user cases|
|&#x2611;|&#x2611;|T2.16|Conduct Spring 2016 College Research Pilots|0|0|No user cases|
|&#x2611;|&#x2611;|T2.17|Involve Users in Building Tutor|0|0|No user cases|
| | |T2.18|Guide, Monitor, Support &amp; Train Users|0|5| |
|&#x2611;|&#x2611;|T2.19|Create Tutor Business Model|0|0|No user cases|
| | | |**Total Cases:**|**306**|**640**|*47.81% Done*|

Templater:
----------
Build the structure for a new test epic

    python3 build_template.py <arguments>

|Available options:| |
|:--------|---------|
|`-h` / `--help` | Display help text|
|`-o` / `--ofile` | Output file name if different from camel-case "epic-name"|
| | `-o test_t2_25_EpicName.py`|
|`-p` / `--product` | Product type (t1, t2, cc1, cc2, ...)|
| | `-p t2`|
|`-e` / `--epic` | Epic number|
| | `-e 25`|
|`-n` / `--epic-name` | Full epic text in quotes|
| | `-n "Epic name"` |
|`-c` / `--case_list` | A comma-separated list of TestRail case IDs|
| | `-c 1,2,3,4,5`|
|`-v` | verbose / debugging output|
