Helpers = require 'openstax-tutor/test-integration/helpers'
{expect} = require 'chai'
USERS = require './users.json'

SimpleCollection = require '../helpers/simple-collection'

users = new SimpleCollection(USERS)

tutorTeacher = users.find('teacher', 'tutor')
coachTeacher = users.find('teacher', 'coach')

cases =

  '7609':
    title: 'Teacher | View the Concept Coach dashboard'
    spec: ->
      @user = new Helpers.User(@)
      @courseSelect = new Helpers.CourseSelect(@)
      @conceptCoach = new Helpers.CCDashboard(@)

      @user.login(coachTeacher.username, coachTeacher.password)
      @courseSelect.waitUntilLoaded()

      @courseSelect.el.courseByAppearance(null, true).click()
      @conceptCoach.waitUntilLoaded()

  '7610':
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

  '7611':
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
      
  '7612':
    title: 'Teacher | Able to copy a system-generated message with a student code, links, and other information'
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
        expect(text).to.include('1. Paste this link in your web browser to visit the class textbook:')
        expect(text).to.include('two-word enrollment code')

      @ccPeriodEditModal.close()

  '7613':
    title: 'Teacher | Periods are relabeled as sections for college courses'
    spec: ->
      @user = new Helpers.User(@)
      @courseSelect = new Helpers.CourseSelect(@)
      @ccRoster = new Helpers.ccRoster(@)

      @user.login(coachTeacher.username, coachTeacher.password)

      @courseSelect.el.courseByAppearance(null, true).click()
      @user.goToRoster() 

      @ccRoster.waitUntilLoaded()

      # check if a high school course uses "period"

      # log into a college course to check if "section"
      # Two options here: 
      # 1. same user but have both high school courses and college courses
      # 2. different user that has high school courses

  '7614':
    title: 'Teacher | View a score report'
    spec: ->
      @user = new Helpers.User(@)
      @courseSelect = new Helpers.CourseSelect(@)
      @conceptCoach = new Helpers.CCDashboard(@)
      @scores = new Helpers.Scores(@)

      @user.login(tutorTeacher.username, tutorTeacher.password)
      @courseSelect.waitUntilLoaded()

      @courseSelect.el.courseByAppearance(null, true).click()
      @conceptCoach.waitUntilLoaded()

      @conceptCoach.goToScores()
      @scores.waitUntilLoaded()

  '7615':
    title: "Teacher | View a report showing an individual student's work pages"
    spec: ->
      @user = new Helpers.User(@)
      @courseSelect = new Helpers.CourseSelect(@)
      @conceptCoach = new Helpers.CCDashboard(@)
      @scores = new Helpers.Scores(@)
      
      @user.login(tutorTeacher.username, tutorTeacher.password)
      @courseSelect.waitUntilLoaded()

      @courseSelect.el.courseByAppearance(null, true).click()
      @conceptCoach.waitUntilLoaded()

      @conceptCoach.goToScores()
      @scores.waitUntilLoaded()

      @scores.el.scoreCell().click()
      @scores.waitUntilLoaded()

  '7616':
    title: "Teacher | View a summary report showing a class's work pages"
    spec: ->
      # Note that the course can not be a college course since this feature is not 
      # available for college courses.
      @user = new Helpers.User(@)
      @courseSelect = new Helpers.CourseSelect(@)
      @calendar = new Helpers.Calendar(@)
      @scores = new Helpers.Scores(@)

      @user.login(tutorTeacher.username, tutorTeacher.password)
      @courseSelect.waitUntilLoaded()

      @courseSelect.el.courseByAppearance(null, true).click()
      @calendar.waitUntilLoaded()

      @calendar.goToScores()
      @scores.waitUntilLoaded()

      @scores.el.hsReviewLink().click()
      @scores.waitUntilLoaded()

  '7617':
    title: "Teacher | View the aggregate student scores"
    spec: ->
      @user = new Helpers.User(@)
      @courseSelect = new Helpers.CourseSelect(@)
      @conceptCoach = new Helpers.CCDashboard(@)
      @scores = new Helpers.Scores(@)

      @user.login(tutorTeacher.username, tutorTeacher.password)
      @courseSelect.waitUntilLoaded()

      @courseSelect.el.courseByAppearance(null, true).click()
      @conceptCoach.waitUntilLoaded()

      @conceptCoach.goToScores()
      @scores.waitUntilLoaded()

      @scores.el.displayAsNumber().click()
      @scores.waitUntilLoaded()

  '7618':
     # title: "Teacher | View scores for an individual student's scores"
     # skipped this one because it is not an available feature for concept coach

  '7619':
    title: "Teacher | View an individual student's question set for an assignment"
    spec: ->
      @user = new Helpers.User(@)
      @courseSelect = new Helpers.CourseSelect(@)
      @conceptCoach = new Helpers.CCDashboard(@)
      @scores = new Helpers.Scores(@)
      
      @user.login(tutorTeacher.username, tutorTeacher.password)
      @courseSelect.waitUntilLoaded()

      @courseSelect.el.courseByAppearance(null, true).click()
      @conceptCoach.waitUntilLoaded()

      @conceptCoach.goToScores()
      @scores.waitUntilLoaded()

      @scores.el.scoreCell().click()
      @scores.waitUntilLoaded()

  '7620':
    title: "Teacher | View an assignment summary"
    # Note that the assignment summary currently would be simply the dashboard of the course
    spec: ->
      @user = new Helpers.User(@)
      @courseSelect = new Helpers.CourseSelect(@)
      @conceptCoach = new Helpers.CCDashboard(@)

      @user.login(coachTeacher.username, coachTeacher.password)
      @courseSelect.waitUntilLoaded()

      @courseSelect.el.courseByAppearance(null, true).click()
      @conceptCoach.waitUntilLoaded()

  '7621':
    title: "Teacher | View analytics by module"
    # Note that currently the dashboard is displaying analytics by module
    spec: ->
      @user = new Helpers.User(@)
      @courseSelect = new Helpers.CourseSelect(@)
      @conceptCoach = new Helpers.CCDashboard(@)

      @user.login(coachTeacher.username, coachTeacher.password)
      @courseSelect.waitUntilLoaded()

      @courseSelect.el.courseByAppearance(null, true).click()
      @conceptCoach.waitUntilLoaded()

  '7622':
    title: "Teacher | Download student scores"
    spec: ->
      @user = new Helpers.User(@)
      @courseSelect = new Helpers.CourseSelect(@)
      @conceptCoach = new Helpers.CCDashboard(@)
      @scores = new Helpers.Scores(@)

      @user.login(tutorTeacher.username, tutorTeacher.password)
      @courseSelect.waitUntilLoaded()

      @courseSelect.el.courseByAppearance(null, true).click()
      @conceptCoach.waitUntilLoaded()

      @conceptCoach.goToScores()
      @scores.waitUntilLoaded()

      @scores.el.generateExport().click()
      @scores.waitUntilLoaded()

      @scores.downloadExport()
      @scores.waitUntilLoaded()






module.exports =
  cases: cases
