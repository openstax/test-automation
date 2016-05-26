Helpers = require 'openstax-tutor/test-integration/helpers'
{expect} = require 'chai'
USERS = require './users.json'

SimpleCollection = require '../helpers/simple-collection'

users = new SimpleCollection(USERS)

tutorTeacher = users.find('teacher', 'tutor')
contentAnalyst = users.find('content-analyst')
admin = users.find('admin')

cases =
  '7651':
    title: 'Content Analyst | See the full error list from a failed book import'
    spec: ->
      @user = new Helpers.User(@)
      @user.login(contentAnalyst.username, contentAnalyst.password)

      @user.toggleHamburgerMenu()
      @utils.wait.click(linkText: 'Content Analyst')

      @user.el.ecosystem().click()
      @user.waitUntilLoaded()

      # Cannot find "Failed Imports" tab
      # If looking for "Incomplete Imports", 
      @utils.wait.click(LinkText: 'Incomplete Imports')


  '7652':
    title: 'Admin | See the full error list from a failed book import'
    spec: ->
      @user = new Helpers.User(@)
      @user.login(admin.username, admin.password)

      @user.toggleHamburgerMenu()
      @utils.wait.click(linkText: 'admin')

      @utils.wait.click(linkText: 'Content')

      @user.el.ecosystem().click()
      @user.waitUntilLoaded()

      # Cannot find "Failed Imports" tab
      # If looking for "Incomplete Imports", 
      @utils.wait.click(LinkText: 'Incomplete Imports')

  '7653':
    title: '002a - Admin | Add the Content Analyst role to a user'
    spec: ->
      @user = new Helpers.User(@)
      @user.login(admin.username, admin.password)

      @user.toggleHamburgerMenu()
      @utils.wait.click(linkText: 'admin')
      @utils.wait.click(linkText: 'Users')

      # select the first user 
      @utils.wait.click(linkText: 'Edit')
      @user.driver.findElement(By.id("Content analyst")).click()
      @utils.wait.click(linkText: 'Save')

  '7654':
    title: 'Admin | Add the Exercise Editor role to a user'
    spec: ->
      @user = new Helpers.User(@)
      @user.login(admin.username, admin.password)

      @user.toggleHamburgerMenu()
      @utils.wait.click(linkText: 'admin')
      @utils.wait.click(linkText: 'Users')

      # select the first user 
      @utils.wait.click(linkText: 'Edit')
      @user.driver.findElement(By.id("Exercise editor")).click()
      @utils.wait.click(linkText: 'Save')

  '7655':
    title: 'Admin | Add the Exercise Author role to a user'
    spec: ->
      @user = new Helpers.User(@)
      @user.login(admin.username, admin.password)

      @user.toggleHamburgerMenu()
      @utils.wait.click(linkText: 'admin')
      @utils.wait.click(linkText: 'Users')

      # select the first user 
      @utils.wait.click(linkText: 'Edit')
      @user.driver.findElement(By.id("Exercise Author")).click()
      @utils.wait.click(linkText: 'Save')

  '7656':
    title: 'Content Analyst | Add an ecosystem comment'
    spec: ->
      @user = new Helpers.User(@)
      @user.login(contentAnalyst.username, contentAnalyst.password)
      
      @user.toggleHamburgerMenu()
      @utils.wait.click(linkText: 'Content Analyst')

      @user.el.ecosystem().click()
      @user.waitUntilLoaded()

      @user.driver.findElement(By.Xpath(//*[@id="ecosystem_comments"])).SendKeys("Test Comment")
      @user.driver.findElement(By.Xpath(//*[@id="edit_ecosystem"]/input[@class='btn btn-xs btn-primary'])).click()
      @user.waitUntilLoaded()


  '7657':
    title: 'Admin | Add an ecosystem comment'
    spec: ->
      @user = new Helpers.User(@)
      @user.login(admin.username, admin.password)

      @user.toggleHamburgerMenu()
      @utils.wait.click(linkText: 'admin')
      @utils.wait.click(linkText: 'Content')

      @user.el.ecosystem().click()
      @user.waitUntilLoaded()

      @user.driver.findElement(By.Xpath(//*[@id="ecosystem_comments"])).SendKeys("Test Comment")
      @user.driver.findElement(By.Xpath(//*[@id="edit_ecosystem"]/input[@class='btn btn-xs btn-primary'])).click()
      @user.waitUntilLoaded()

  '7658':
    title: 'Content Analyst | Delete an unused ecosystem'
    spec: ->
      @user = new Helpers.User(@)
      @user.login(contentAnalyst.username, contentAnalyst.password)
      
      @user.toggleHamburgerMenu()
      @utils.wait.click(linkText: 'Content Analyst')

      @user.el.ecosystem().click()
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Delete')
      @user.waitUntilLoaded()

  '7659':
    title: 'Admin | Delete an unused ecosystem'
    spec: ->
      @user = new Helpers.User(@)
      @user.login(admin.username, admin.password)

      @user.toggleHamburgerMenu()
      
      @utils.wait.click(linkText: 'admin')
      @user.waitUntilLoaded()
      
      @utils.wait.click(linkText: 'Content')
      @user.waitUntilLoaded()

      @user.el.ecosystem().click()
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Delete')
      @user.waitUntilLoaded()

  # '7660':
  #   title: '004c - Content Analyst | Unable to delete an assigned ecosystem'


  '7674':
    title: 'Content Analyst | Able to publish an exercise'

    before: ->
      @driver.get 'https://exercises-qa.openstax.org/'

    spec: ->
      @user = new Helpers.User(@)
      @user.login(OpenStax.username, OpenStax.password)

    before: ->
      @driver.get 'https://tutor-qa.openstax.org/'

    spec: ->
      @user = new Helpers.User(@)
      @user.login(contentAnalyst.username, contentAnalyst.password)

      @user.el.openHamburgerMenu().click()
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'QA Content')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'edit')
      @user.waitUntilLoaded()

      # Editting the exercise?

      @utils.wait.click(linkText: 'Save Draft')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Publish')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Publish')
      @user.waitUntilLoaded()
      
  '7675':
    title: '015b - Exercise Editor | Able to publish an exercise'

    before: ->
      @driver.get 'https://exercises-qa.openstax.org/'

    spec: ->
      @user = new Helpers.User(@)
      @user.login(OpenStax.username, OpenStax.password)

    before: ->
      @driver.get 'https://tutor-qa.openstax.org/'

    spec: ->
      @user = new Helpers.User(@)
      @user.login(ExerciseEditor.username, ExerciseEditor.password)

      @user.el.openHamburgerMenu().click()
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'QA Content')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'edit')
      @user.waitUntilLoaded()

      # Editting the exercise?

      @utils.wait.click(linkText: 'Save Draft')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Publish')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Publish')
      @user.waitUntilLoaded()

  '7676':
    title: '015b - Exercise Editor | Able to publish an exercise'

    before: ->
      @driver.get 'https://exercises-qa.openstax.org/'

    spec: ->
      @user = new Helpers.User(@)
      @user.login(OpenStax.username, OpenStax.password)

    before: ->
      @driver.get 'https://tutor-qa.openstax.org/'

    spec: ->
      @user = new Helpers.User(@)
      @user.login(ExerciseAuthor.username, ExerciseAuthor.password)

      @user.el.openHamburgerMenu().click()
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'QA Content')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'edit')
      @user.waitUntilLoaded()

      # Editting the exercise?

      @utils.wait.click(linkText: 'Save Draft')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Publish')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Publish')
      @user.waitUntilLoaded()

  '7677':
    title: '016a - Content Analyst | Able to save an exercise as a draft'

    before: ->
      @driver.get 'https://exercises-qa.openstax.org/'

    spec: ->
      @user = new Helpers.User(@)
      @user.login(OpenStax.username, OpenStax.password)

    before: ->
      @driver.get 'https://tutor-qa.openstax.org/'

    spec: ->
      @user = new Helpers.User(@)
      @user.login(contentAnalyst.username, contentAnalyst.password)

      @user.el.openHamburgerMenu().click()
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'QA Content')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'edit')
      @user.waitUntilLoaded()

      # Editting the exercise?

      @utils.wait.click(linkText: 'Save Draft')
      @user.waitUntilLoaded()

  '7678':
    title: '016b - Exercise Editor | Able to save an exercise as a draft'

    before: ->
      @driver.get 'https://exercises-qa.openstax.org/'

    spec: ->
      @user = new Helpers.User(@)
      @user.login(OpenStax.username, OpenStax.password)

    before: ->
      @driver.get 'https://tutor-qa.openstax.org/'

    spec: ->
      @user = new Helpers.User(@)
      @user.login(ExerciseEditor.username, ExerciseEditor.password)

      @user.el.openHamburgerMenu().click()
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'QA Content')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'edit')
      @user.waitUntilLoaded()

      # Editting the exercise?

      @utils.wait.click(linkText: 'Save Draft')
      @user.waitUntilLoaded()

  '7679':
    title: '016c - Exercise Author | Able to save an exercise as a draft'

    before: ->
      @driver.get 'https://exercises-qa.openstax.org/'

    spec: ->
      @user = new Helpers.User(@)
      @user.login(OpenStax.username, OpenStax.password)

    before: ->
      @driver.get 'https://tutor-qa.openstax.org/'

    spec: ->
      @user = new Helpers.User(@)
      @user.login(ExerciseAuthor.username, ExerciseAuthor.password)

      @user.el.openHamburgerMenu().click()
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'QA Content')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'edit')
      @user.waitUntilLoaded()

      # Editting the exercise?

      @utils.wait.click(linkText: 'Save Draft')
      @user.waitUntilLoaded()

  '7681':
    title: '018a - Student | Denied access to exercise solutions on Exercises'

    before: ->
      @driver.get 'https://exercises-qa.openstax.org/'

    spec: ->
      @user = new Helpers.User(@)
      @user.login(student.username, student.password)

      @driver.get("https://exercises-dev.openstax.org/api/exercises?q=<exercise ID>")
      # <exercise ID> is the ID of the exercise to search at

  '7682':
    title: '018b - Non-user | Denied access to exercise solutions on Exercises'

    spec: ->
      @driver.get("https://exercises-dev.openstax.org/api/exercises?q=<exercise ID>")
      # <exercise ID> is the ID of the exercise to search at

  '7683':
    title: '019 - Content Analyst | Able to repair content errata submitted by users'
    before: ->
      @driver.get 'http://openstaxcollege.org/'
    spec: ->
      @user = new Helpers.User(@)
      @user.login(staff.username, staff.password)

      @utils.wait.click(linkText: 'Staff')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Errata')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'all')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'New')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'numbers')
      @user.waitUntilLoaded()

      # Fix tickets with typos and minor issues

      @utils.wait.click(linkText: 'Published')
      @user.waitUntilLoaded()

  '7686':
    title: '020c - Content Analyst | Publish reviewed content from content creators'
    before: ->
      @driver.get 'http://openstaxcollege.org/'
    spec: ->
      @user = new Helpers.User(@)
      @user.login(staff.username, staff.password)

      @utils.wait.click(linkText: 'Staff')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Errata')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'all')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Approved for Publish')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Published')
      @user.waitUntilLoaded()

  '7687':
    title: '014d - Content Analyst | In the QA exercise view render the Markdown'
    spec: ->
      @user = new Herlpers.User(@)
      @user.login(contentAnalyst.username, contentAnalyst.password)

      @user.el.openHamburgerMenu().click()
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'QA Content')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Physics')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: '2.4 Velocity vs. Time Graphs')
      @user.waitUntilLoaded()

      





  ''
      




module.exports =
  cases: cases
