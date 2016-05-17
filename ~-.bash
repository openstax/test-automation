
rt SAUCE_USERNAME=''
export SAUCE_ACCESS_KEY=''

export SERVER_URL='tutor-qa.openstax.org'
export ADMIN_USER='admin'
export ADMIN_PASSWORD='password'
export TEACHER_USER='teacher01'
export TEACHER_PASSWORD='password'
export STUDENT_USER='student02'
export STUDENT_PASSWORD='password'
export TEST_EMAIL_USER='password_test'
export TEST_EMAIL_ACCOUNT='osttutor.test@gmail.com'
export TEST_EMAIL_PASSWORD='jL3eavehQ^9ZBq6A'

export GREP_OPTIONS='--color=auto'
export LESS='--ignore-case --raw-control-chars'
export PAGER='less'
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/projects
export VIRTUALENVWRAPPER_PYTHON='/usr/bin/python3'
export VIRTUALENVWRAPPER_VIRTUALENV_ARGS='--no-site-packages'
export VIRTUALENVWRAPPER_WORKON_CD='cdproject'
source /usr/local/bin/virtualenvwrapper.sh

close() { deactivate && cd; }

