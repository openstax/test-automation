Helpers = require 'openstax-tutor/test-integration/helpers'
{expect} = require 'chai'
USERS = require './users.json'

UserCollection = require '../helpers/users'

users = new UserCollection(USERS)

tutorTeacher = users.get('teacher', 'tutor')
coachTeacher = users.get('teacher', 'coach')

cases =

  'C7609':
    title: 'Teacher | View the Concept Coach dashboard'
    spec: ->
      @user = new Helpers.User(@)
      @courseSelect = new Helpers.CourseSelect(@)
      @conceptCoach = new Helpers.CCDashboard(@)

      @user.login(coachTeacher.username, coachTeacher.password)
      @courseSelect.waitUntilLoaded()

      @courseSelect.el.courseByAppearance(null, true).click()
      @conceptCoach.waitUntilLoaded()

  'C7610':
    title: 'Teacher | Able to switch between concurrently running courses'
    spec: ->
      @user = new Helpers.User(@)
      @courseSelect = new Helpers.CourseSelect(@)
      @calendar = new Helpers.Calendar(@)

      @user.login(tutorTeacher.username, tutorTeacher.password)
      @courseSelect.waitUntilLoaded()

      @courseSelect.el.courseByAppearance().forEach (courseSelector) =>
        courseSelector.click()
        @calendar.waitUntilLoaded()
        @user.el.homeLink().click()

  'C7611':
    title: 'Teacher | View links on dashboard to course materials'
    spec: ->
      @user = new Helpers.User(@)
      @courseSelect = new Helpers.CourseSelect(@)
      @calendar = new Helpers.Calendar(@)
      @referenceBook = new Helpers.ReferenceBook(@)

      @user.login(tutorTeacher.username, tutorTeacher.password)
      @courseSelect.waitUntilLoaded()

      @courseSelect.el.courseByAppearance(null, false, ignoreLengthChange: true).forEach (courseSelector) =>
        courseSelector.click()
        @calendar.waitUntilLoaded()
        @calendar.goToBook()
        @referenceBook.focus()
        @referenceBook.waitUntilLoaded()
        @referenceBook.close()
        @user.el.homeLink().click()

      # TODO check whether or not same tests need to be run for concept coach books

  'C7612':
    title: 'Teacher | Teacher | Able to copy a system-generated message with a student code, links, and other information'
    spec: ->
      @user = new Helpers.User(@)
      @courseSelect = new Helpers.CourseSelect(@)
      @ccRoster = new Helpers.CCRoster(@)
      @ccPeriodEditModal = new Helpers.CCRoster.PeriodEditModal(@)

      @user.login(coachTeacher.username, coachTeacher.password)

      @courseSelect.el.courseByAppearance(null, true).click()
      @user.goToRoster()

      @ccRoster.waitUntilLoaded()
      @ccRoster.el.getStudentEnrollmentCodeLink().waitClick()
      @ccPeriodEditModal.waitUntilLoaded()
      @ccPeriodEditModal.el.codeMessage().findElement().getText().then (text) ->
        console.info(text)




module.exports =
  cases: cases
