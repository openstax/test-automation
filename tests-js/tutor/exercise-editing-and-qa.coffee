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
      @utils.wait.click(linkText: 'Content')

      @user.el.ecosystem().click()
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Delete')
      @user.waitUntilLoaded()

  '7660':
    title: '004c - Content Analyst | Unable to delete an assigned ecosystem'


  '7674':
    title: 'Content Analyst | Able to publish an exercise'
    spec: ->
      @user = new Helpers.User(@)
      @user.login(contentAnalyst.username, contentAnalyst.password)

      @calendar = new Helpers.Calendar(@)
      @calendarPopup = new Helpers.Calendar.Popup(@)
      @reading = new Helpers.ReadingBuilder(@)

      @user = new Helpers.User(@)
      @user.login()
      @user.el.ecosystem().click()
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Delete')
      @user.waitUntilLoaded()

      

  ''


module.exports =
  cases: cases
