Helpers = require 'openstax-tutor/test-integration/helpers'
{expect} = require 'chai'

cases =
  'C7651':
    title: 'Content Analyst | Add an ecosystem comment'
    spec: ->
      @user = new Helpers.User(@)
      @user.login('content')
      @user.toggleHamburgerMenu()
      @utils.wait.click(linkText: 'Content Analyst')

  'C7674':
    title: 'Content Analyst | Able to publish an exercise'
    spec: ->
      @user = new Helpers.User(@)
      @user.login('openstax')

      @calendar = new Helpers.Calendar(@)
      @calendarPopup = new Helpers.Calendar.Popup(@)
      @reading = new Helpers.ReadingBuilder(@)

      # new Helpers.CourseSelect(@).goToByType('ANY')
      @calendar.el.unopenPlan().waitClick()


module.exports =
  cases: cases
  beforeEach: beforeEach
