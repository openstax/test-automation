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
export TEACHER_PASSWORD=''
export STUDENT_USER=''
export STUDENT_USER_MULTI=''
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

Either activate the changes to your profile in your current terminal session by:

```source <profile-path>/<profile-filename>```

or close the terminal and start a new one.

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
