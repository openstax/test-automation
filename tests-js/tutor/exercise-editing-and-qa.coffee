Helpers = require 'openstax-tutor/test-integration/helpers'
{expect} = require 'chai'
USERS = require './users.json'

SimpleCollection = require '../helpers/simple-collection'

users = new SimpleCollection(USERS)

tutorTeacher = users.find('teacher', 'tutor')
contentAnalyst = users.find('content-analyst')

cases =
  '7651':
    title: 'Content Analyst | Add an ecosystem comment'
    spec: ->
      @user = new Helpers.User(@)
      @user.login(contentAnalyst.username, contentAnalyst.password)

      @user.toggleHamburgerMenu()
      @utils.wait.click(linkText: 'Content Analyst')

  '7674':
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
