Helpers = require 'openstax-tutor/test-integration/helpers'
{expect} = require 'chai'
USERS = require './users.json'

UserCollection = require '../helpers/users'

users = new UserCollection(USERS)

tutorTeacher = users.get('teacher', 'tutor')
contentAnalyst = users.get('content-analyst')

cases =
  'C7651':
    title: 'Content Analyst | Add an ecosystem comment'
    spec: ->
      @user = new Helpers.User(@)
      @user.login(contentAnalyst.username, contentAnalyst.password)

      @user.toggleHamburgerMenu()
      @utils.wait.click(linkText: 'Content Analyst')

  'C7674':
    title: 'Content Analyst | Able to publish an exercise'
    spec: ->
      @user = new Helpers.User(@)
      @user.login(tutorTeacher.username, tutorTeacher.password)

      @calendar = new Helpers.Calendar(@)
      @calendarPopup = new Helpers.Calendar.Popup(@)
      @reading = new Helpers.ReadingBuilder(@)

      new Helpers.CourseSelect(@).goToByType('ANY')

module.exports =
  cases: cases
