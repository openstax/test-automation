Tutor Automation Installation/Configuration
===========================================

Install X-Code
--------------
Open a terminal

```
xcode-select --install
```

Click Install
Click Agree for the license

Install Homebrew
----------------
```
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Follow the on-terminal prompts

Then continue

```
brew doctor
brew update
brew upgrade
echo 'export PATH="/usr/local/bin:/usr/local/sbin:$PATH"' >> ~/.bash_profile
```

Install Git
-----------

```
brew install git
```

Optional: Install GitHub for Mac
--------------------------------
Go to: https://mac.github.com/ and either Sign Up or Sign In

Install Python 3
----------------

```
brew install python3
```

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

Initialize the Wrapper
----------------------

Activate the changes to your profile

```source <profile-path>/<profile-filename>```

Repository
----------

```
mkproject automation
```

Switch into the automation project folder if it isn't already

```
git clone https://github.com/openstax/test-automation
cd test-automation
pip3 install -r tutor/requirements.txt
```

-----------------------------------------------------

Browser Drivers
===============

Chrome
------
Open a Chrome window and type `chrome://help/` in the address bar. Allow Chrome to auto-install any updates and then Relaunch the browser.

Now download, at minimum, the ChromeDriver: https://sites.google.com/a/chromium.org/chromedriver/downloads and extract it from the ZIP file; copy or move the driver to a publicly available location like `/Applications`.

_The current version is 2.28 and works with Chrome v55 and v56; it will also support Chrome v57 when it is released._

Open a new Terminal window, run the driver (`/Applications/chromedriver` if moved to the app directory) and verify that it shows "Only local connections are allowed."

Safari
------
The Safari driver should be installed under `/usr/bin/safaridriver`. Run `/usr/bin/safaridriver -p 0` to verify the installation.

Internet Explorer
-----------------
Don't use it.

Edge
----
Follow instructions at https://docs.microsoft.com/en-us/microsoft-edge/dev-guide/tools/webdriver

Firefox
-------
Installing Firefox should be sufficient to use it for Selenium. If not, make sure the app is in the system path. Selenium expects the executable to be in `/Applications/Firefox.app/Contents/MacOS/firefox-bin`. If it still complains, install the Firefox IDE and let it record and play back.

Opera
-----
The Opera driver is based on the ChromeDriver. Download the [current binary for your system](https://github.com/operasoftware/operachromiumdriver/releases) and follow the Chrome steps mentioned above.

Additional steps are required to work with Opera in-code: https://github.com/operasoftware/operachromiumdriver/blob/master/docs/desktop.md

Mobile
------
Follow instructions at https://github.com/appium/appium for iOS, Android and Windows Phone. Appium instructions are available at https://github.com/appium/appium/blob/master/docs/en/appium-setup/running-on-osx.md

Use the [iPhone simulator SDK](https://developer.apple.com/library/prerelease/content/documentation/IDEs/Conceptual/iOS_Simulator_Guide/Introduction/Introduction.html) for iDevice emulation and the [Android SDK](https://developer.android.com/studio/index.html) for Android emulation.

_Note that you may also use devices attached to your test host computer but setup and driver control can be problematic._

-----------------------------------------------------

Tutor Automation Project
========================

Status
------

|Finished?|Verified?|Epic|Epic Name|Started|Total Cases|Notes|
|:-------:|:-------:|----|---------|------:|----------:|-----|
|&#x2611;| |CC1.01|Recruiting Teachers|9|9| |
|&#x2611;| |CC1.03|Content Preparation and Import|10|10| |
| | |CC1.04|Exercise Editing and QA|23|27| |
|&#x2611;| |CC1.05|CNX Navigation|4|4| |
|&#x2611;| |CC1.06|Concept Coach Widget Mechanics and Infrastructure|3|3| |
| | |CC1.07|Student Registration, Enrollment, Login and Authentication|14|17| |
| | |CC1.08|Students Work Assignments|6|14| |
|&#x2611;| |CC1.09|Student Progress Views|4|4| |
| | |CC1.10|Admin and Teacher Course Setup|14|16| |
|&#x2611;| |CC1.11|Teacher Login and Authentication|2|2| |
|&#x2611;| |CC1.12|Delivering Assignments|3|3| |
|&#x2611;| |CC1.13|Teacher Views|0|15| |
| | |CC1.14|Training and Supporting Teachers and Students|8|9| |
|&#x2611;| |CC1.15|OpenStax Metrics|1|1| |
|&#x2611;| |CC2.08|Improves Scores Reporting|11|11| |
| | |CC2.09|Improve Login, Registration, Enrollment|5|6| |
| | |CC2.11|Improve Question Management|5|7| |
| | |CC2.18|Guide, Monitor, Support &amp; Train Users|17|19| |
|&#x2611;| |T1.13|View the calendar dashboard|13|13| |
|&#x2611;| |T1.14|Create a reading|37|37| |
|&#x2611;| |T1.16|Create a homework|57|57| |
|&#x2611;| |T1.18|Create an external assignment|33|33| |
|&#x2611;| |T1.21|Create an event|31|31| |
|&#x2611;| |T1.22|View class performance|8|8| |
| | |T1.23|View class scores|25|26| |
| | |T1.27|Tutor works with CNX|0|2| |
| | |T1.28|Work a reading|15|20| |
| | |T1.34|Account management|21|22| |
|&#x2611;| |T1.35|Contract controls|9|9| |
| | |T1.36|User login|13|17| |
|&#x2611;| |T1.37|Account maintenance|7|7| |
|&#x2611;| |T1.38|Choose course|3|3| |
|&#x2611;| |T1.42|Edit course settings and roster|9|9| |
|&#x2611;| |T1.45|View the list dashboard|13|13| |
|&#x2611;| |T1.48|Work an external assignment|6|6| |
|&#x2611;| |T1.50|View student performance|10|10| |
|&#x2611;| |T1.55|Practice|14|14| |
| | |T1.57|Course maintenance|7|10| |
| | |T1.58|Manage ecosystems|31|32| |
|&#x2611;| |T1.59|Manage districts, schools, and courses|26|26| |
|&#x2611;| |T1.68|Generate reports|1|1| |
| | |T1.71|Work a homework|22|25| |
|&#x2611;| |T2.05|Analyze College Workflow|3|3| |
| | |T2.07|Improve Course Management|5|7| |
| | |T2.08|Improve Scores Reporting|5|11| |
| | |T2.09|Improve Login, Registration, Enrollment|14|18| |
| | |T2.10|Improve Assignment Management|8|16| |
| | |T2.11|Question Work: Faculty Reviews, Excludes, Edits, Creates Assignments|44|47| |
| | |T2.12|Create New Question &amp; Assignment Types|4|5| |
| | |T2.13|Simplify &amp; Improve Readings|2|6| |
| | |T2.14|Improve Practice and Forecast|0|1| |
| | |T2.18|Guide, Monitor, Support &amp; Train Users|12|16| |
| | |T3.09|Course Adoption &amp; Readoption|0|23| |
| | |T3.16|Accounts Enhancements|0|37| |
| | | |**Total Cases:**|**647**|**914**|*70.78% Done*|

Templater
---------
Build the structure for a new test epic

```
python3 build_template.py <arguments>
```

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
