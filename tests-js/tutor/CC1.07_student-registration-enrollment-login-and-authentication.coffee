Helpers = require 'openstax-tutor/test-integration/helpers'
{expect} = require 'chai'
USERS = require './users.json'
selenium = require 'selenium-webdriver'

SimpleCollection = require '../helpers/simple-collection'

users = new SimpleCollection(USERS)

tutorTeacher = users.find('teacher', 'tutor')
student = users.find('student')
contentAnalyst = users.find('content-analyst')
admin = users.find('admin')
driver = new selenium.Builder()
  .withCapabilities(selenium.Capabilities.chrome())
  .build()

cases =
  '7631':
  	title: 'Student | Register for a class using a provided registration code - non-social login'
  	before: ->
  	  @driver.get 'https://demo.cnx.org/contents/lHoUF1_V@2.2:7J0h_NWu@2/Preface'
  	spec: ->
      @user = new Helpers.User(@)

  	  @utils.wait.click(linkText: 'Next')
  	  @user.waitUntilLoaded()

  	  @utils.wait.click(linkText: 'Next')
  	  @user.waitUntilLoaded()

  	  @utils.wait.click(linkText: 'Launch Concept Coach')
  	  @user.waitUntilLoaded()

  	  @user.driver.findElement(By.Xpath(//*[@id="coach-wrapper"])).SendKeys("careful must")
  	  @utils.wait.click(linkText: 'Enroll')
  	  @user.waitUntilLoaded()

  	  @utils.wait.click(linkText: 'click to begin login.')
  	  @user.waitUntilLoaded()

  	  @utils.wait.click(linkText: 'Sign up')
  	  @user.waitUntilLoaded()

  	  @user.driver.findElement(By.Xpath(//*[@id="identity-login-button"])).click()
  	  @user.waitUntilLoaded()

  	  @user.driver.findElement(By.Xpath(//*[@id="signup_first_name"])).SendKeys("test1")
  	  @user.driver.findElement(By.Xpath(//*[@id="signup_last_name"])).SendKeys("test2")
  	  @user.driver.findElement(By.Xpath(//*[@id="signup_email_address"])).SendKeys("test3")
  	  @user.driver.findElement(By.Xpath(//*[@id="signup_username"])).SendKeys("test4")
  	  @user.driver.findElement(By.Xpath(//*[@id="signup_password"])).SendKeys("testtest")
	    @user.driver.findElement(By.Xpath(//*[@id="signup_password_confirmation"])).SendKeys("testtest")

	    @utils.wait.click(linkText: 'Create Account')
      @user.waitUntilLoaded()

  '7632':
    title: '002 - Student | Register for a class using a provided registration code - Facebook login'
    before: ->
      @driver.get 'https://demo.cnx.org/contents/lHoUF1_V@2.2:7J0h_NWu@2/Preface'
    spec: ->
      @user = new Helpers.User(@)

      @utils.wait.click(linkText: 'Next')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Next')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Launch Concept Coach')
      @user.waitUntilLoaded()

      @user.driver.findElement(By.Xpath(//*[@id="coach-wrapper"])).SendKeys("careful must")
      @utils.wait.click(linkText: 'Enroll')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'click to begin login.')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Sign up')
      @user.waitUntilLoaded()

      @user.driver.findElement(By.Xpath(//*[@id="facebook-login-button"])).click()
      @user.waitUntilLoaded()

      # The next few steps require that facebook is already logged in #

      @user.driver.findElement(By.Xpath(//*[@id="i_agree"])).click()
      @utils.wait.click(linkText: 'I Agree')
      @user.waitUntilLoaded()

      @user.driver.findElement(By.Xpath(//*[@id="i_agree"])).click()
      @utils.wait.click(linkText: 'I Agree')
      @user.waitUntilLoaded()

  '7633':
    title: '003 - Student | Register for a class using a provided registration code - Twitter login'
    before: ->
      @driver.get 'https://demo.cnx.org/contents/lHoUF1_V@2.2:7J0h_NWu@2/Preface'
    spec: ->
      @user = new Helpers.User(@)

      @utils.wait.click(linkText: 'Next')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Next')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Launch Concept Coach')
      @user.waitUntilLoaded()

      @user.driver.findElement(By.Xpath(//*[@id="coach-wrapper"])).SendKeys("careful must")
      @utils.wait.click(linkText: 'Enroll')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'click to begin login.')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Sign up')
      @user.waitUntilLoaded()

      @user.driver.findElement(By.Xpath(//*[@id="twitter-login-button"])).click()
      @user.waitUntilLoaded()

      # The next few steps require that twitter is already logged in #

      @user.driver.findElement(By.Xpath(//*[@id="i_agree"])).click()
      @utils.wait.click(linkText: 'I Agree')
      @user.waitUntilLoaded()

      @user.driver.findElement(By.Xpath(//*[@id="i_agree"])).click()
      @utils.wait.click(linkText: 'I Agree')
      @user.waitUntilLoaded()

  '7634':
    title: '003 - Student | Register for a class using a provided registration code - Google login'
    before: ->
      @driver.get 'https://demo.cnx.org/contents/lHoUF1_V@2.2:7J0h_NWu@2/Preface'
    spec: ->
      @user = new Helpers.User(@)

      @utils.wait.click(linkText: 'Next')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Next')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Launch Concept Coach')
      @user.waitUntilLoaded()

      @user.driver.findElement(By.Xpath(//*[@id="coach-wrapper"])).SendKeys("careful must")
      @utils.wait.click(linkText: 'Enroll')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'click to begin login.')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Sign up')
      @user.waitUntilLoaded()

      @user.driver.findElement(By.Xpath(//*[@id="google-login-button"])).click()
      @user.waitUntilLoaded()

      # The next few steps require that Google is already logged in #

      @user.driver.findElement(By.Xpath(//*[@id="i_agree"])).click()
      @utils.wait.click(linkText: 'I Agree')
      @user.waitUntilLoaded()

      @user.driver.findElement(By.Xpath(//*[@id="i_agree"])).click()
      @utils.wait.click(linkText: 'I Agree')
      @user.waitUntilLoaded()

  '7635':
    title: '005 - Student | After registering the user is shown a confirmation message'
    before: ->
      @driver.get 'https://demo.cnx.org/contents/lHoUF1_V@2.2:7J0h_NWu@2/Preface'
    spec: ->
      @user = new Helpers.User(@)

      @utils.wait.click(linkText: 'Next')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Next')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Launch Concept Coach')
      @user.waitUntilLoaded()

      @user.driver.findElement(By.Xpath(//*[@id="coach-wrapper"])).SendKeys("careful must")
      @utils.wait.click(linkText: 'Enroll')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'click to begin login.')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Sign up')
      @user.waitUntilLoaded()

      @user.driver.findElement(By.Xpath(//*[@id="identity-login-button"])).click()
      @user.waitUntilLoaded()

      @user.driver.findElement(By.Xpath(//*[@id="signup_first_name"])).SendKeys("test1")
      @user.driver.findElement(By.Xpath(//*[@id="signup_last_name"])).SendKeys("test2")
      @user.driver.findElement(By.Xpath(//*[@id="signup_email_address"])).SendKeys("test3")
      @user.driver.findElement(By.Xpath(//*[@id="signup_username"])).SendKeys("test4")
      @user.driver.findElement(By.Xpath(//*[@id="signup_password"])).SendKeys("testtest")
      @user.driver.findElement(By.Xpath(//*[@id="signup_password_confirmation"])).SendKeys("testtest")

      @utils.wait.click(linkText: 'Create Account')
      @user.waitUntilLoaded()

  '7636':
    title: '006 - Student | After a failed registration the user is shown an error message'
    before: ->
      @driver.get 'https://demo.cnx.org/contents/lHoUF1_V@2.2:7J0h_NWu@2/Preface'
    spec: ->
      @user = new Helpers.User(@)

      @utils.wait.click(linkText: 'Next')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Next')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Launch Concept Coach')
      @user.waitUntilLoaded()

      @user.driver.findElement(By.Xpath(//*[@id="coach-wrapper"])).SendKeys("careful must")
      @utils.wait.click(linkText: 'Enroll')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'click to begin login.')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Sign up')
      @user.waitUntilLoaded()

      @user.driver.findElement(By.Xpath(//*[@id="identity-login-button"])).click()
      @user.waitUntilLoaded()

      @user.driver.findElement(By.Xpath(//*[@id="signup_first_name"])).SendKeys("test1")
      @user.driver.findElement(By.Xpath(//*[@id="signup_last_name"])).SendKeys("test2")
      @user.driver.findElement(By.Xpath(//*[@id="signup_email_address"])).SendKeys("test3")
      @user.driver.findElement(By.Xpath(//*[@id="signup_username"])).SendKeys("test4")
      @user.driver.findElement(By.Xpath(//*[@id="signup_password"])).SendKeys("testtest")
      @user.driver.findElement(By.Xpath(//*[@id="signup_password_confirmation"])).SendKeys("testtesttest")
      # This is a failed registration in the sense that the re-entering password is different.
      # Thus, a failed message should be displayed

      @utils.wait.click(linkText: 'Create Account')
      @user.waitUntilLoaded()

  '7637':
    title: '007 - Student | Able to change to another course'
    before: ->
      @driver.get 'https://tutor-staging.openstax.org/'
    spec: ->
      @user = new Helpers.User(@)
      @courseSelect = new Helpers.CourseSelect(@)

      @utils.wait.click(linkText: 'Login')
      @user.waitUntilLoaded()

      #login as a student
      @user.driver.findElement(By.Xpath(//*[@id="auth_key"])).SendKeys("student01")
      @user.driver.findElement(By.Xpath(//*[@id="password"])).SendKeys("password")
      @utils.wait.click(linkText: 'Sign in')
      @user.waitUntilLoaded()

      @courseSelect.el.courseByAppearance(null, true).click()

      @utils.wait.click(linkText: 'Next')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Next')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Launch Concept Coach')
      @user.waitUntilLoaded()

      # open the user menu
      @user.el.userMenu().click()
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Change Course')
      @user.waitUntilLoaded()

      @user.driver.findElement(By.Xpath(//*[@id="coach-wrapper"]/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div/input)).SendKeys("careful must")
      @utils.wait.click(linkText: 'Enroll')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Confirm')
      @user.waitUntilLoaded()

  '7638':
    title: '008 - Student | Able to change period in the same course'
    before: ->
      @driver.get 'https://tutor-staging.openstax.org/'
    spec: ->
      @user = new Helpers.User(@)
      @courseSelect = new Helpers.CourseSelect(@)

      @utils.wait.click(linkText: 'Login')
      @user.waitUntilLoaded()

      #login as a student
      @user.driver.findElement(By.Xpath(//*[@id="auth_key"])).SendKeys("student01")
      @user.driver.findElement(By.Xpath(//*[@id="password"])).SendKeys("password")
      @utils.wait.click(linkText: 'Sign in')
      @user.waitUntilLoaded()

      @courseSelect.el.courseByAppearance(null, true).click()

      @utils.wait.click(linkText: 'Next')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Next')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Launch Concept Coach')
      @user.waitUntilLoaded()

      # open the user menu
      @user.el.userMenu().click()
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Change Course')
      @user.waitUntilLoaded()

      @user.driver.findElement(By.Xpath(//*[@id="coach-wrapper"]/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div/input)).SendKeys("mild tray")
      @utils.wait.click(linkText: 'Enroll')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Confirm')
      @user.waitUntilLoaded()

  '7639':
    title: '009 - Student | Able to enroll in more than one Concept Coach course'
    before: ->
      @driver.get 'https://tutor-staging.openstax.org/'
    spec: ->
      @user = new Helpers.User(@)
      @courseSelect = new Helpers.CourseSelect(@)

      @utils.wait.click(linkText: 'Login')
      @user.waitUntilLoaded()

      #login as a student
      @user.driver.findElement(By.Xpath(//*[@id="auth_key"])).SendKeys("student01")
      @user.driver.findElement(By.Xpath(//*[@id="password"])).SendKeys("password")
      @utils.wait.click(linkText: 'Sign in')
      @user.waitUntilLoaded()

      @courseSelect.el.courseByAppearance(null, true).click()

      @utils.wait.click(linkText: 'Next')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Next')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Launch Concept Coach')
      @user.waitUntilLoaded()

      @user.driver.findElement(By.Xpath(//*[@id="coach-wrapper"]/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div/input)).SendKeys("careful must")
      @utils.wait.click(linkText: 'Enroll')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Confirm')
      @user.waitUntilLoaded()

  '7640':
    title: '010 - Student | If not logged in, the sign up and sign in widget options are displayed'
    before: ->
      @driver.get 'http://demo.cnx.org/contents/v5a_xecj@2.2:Pj8cW7X1@4/Introduction'
    spec: ->  
      @utils.wait.click(linkText: 'Next')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Next')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Launch Concept Coach')
      @user.waitUntilLoaded()

  '7641':
    title: '011 - Student | Able to view their name in the header sections'
    before: ->
      @driver.get 'https://tutor-staging.openstax.org'
    spec: ->
      @utils.wait.click(linkText: 'Login')
      @user.waitUntilLoaded()

      #login as a student
      @user.driver.findElement(By.Xpath(//*[@id="auth_key"])).SendKeys("student01")
      @user.driver.findElement(By.Xpath(//*[@id="password"])).SendKeys("password")
      @utils.wait.click(linkText: 'Sign in')
      @user.waitUntilLoaded()

      @courseSelect.el.courseByAppearance(null, true).click()

      @utils.wait.click(linkText: 'Next')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Next')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Launch Concept Coach')
      @user.waitUntilLoaded()

  '7642':
    title: '012 - Student | Presented the current privacy policy when registering for an account'
    before: ->
      @driver.get 'https://accounts-qa.openstax.org/signin'
    spec: ->
      @utils.wait.click(linkText: 'Sign up')
      @user.waitUntilLoaded()

      @user.driver.findElement(By.Xpath(//*[@id="identity-login-button"])).click()
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Privacy Policy')
      @user.waitUntilLoaded()

  '7643':
    title: '013 - Student | Presented the current terms of service when registering for an account'
    before: ->
      @driver.get 'https://accounts-qa.openstax.org/signin'
    spec: ->
      @utils.wait.click(linkText: 'Sign up')
      @user.waitUntilLoaded()

      @user.driver.findElement(By.Xpath(//*[@id="identity-login-button"])).click()
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Terms of Use')
      @user.waitUntilLoaded()

  '7644':
    title: '014 - Student | Presented the new privacy policy when the privacy policy is changed'
    before: ->
      @driver.get 'https://tutor-staging.openstax.org'
    spec: ->
      @utils.wait.click(linkText: 'Login')
      @user.waitUntilLoaded()

      #login as a student
      @user.driver.findElement(By.Xpath(//*[@id="auth_key"])).SendKeys("student01")
      @user.driver.findElement(By.Xpath(//*[@id="password"])).SendKeys("password")
      @utils.wait.click(linkText: 'Sign in')
      @user.waitUntilLoaded()

      # The user is presented with the new privacy policy when the privacy policy is changed

  '7645':
    title: '015 - Student | Presented the new terms of service when the terms of service is changed'
    before: ->
      @driver.get 'https://tutor-staging.openstax.org'
    spec: ->
      @utils.wait.click(linkText: 'Login')
      @user.waitUntilLoaded()

      #login as a student
      @user.driver.findElement(By.Xpath(//*[@id="auth_key"])).SendKeys("student01")
      @user.driver.findElement(By.Xpath(//*[@id="password"])).SendKeys("password")
      @utils.wait.click(linkText: 'Sign in')
      @user.waitUntilLoaded()

      # The user is presented with the new terms of service when the terms of service is changed

  '7646':
    title: '016 - Student | Re-presented the current privacy policy if not accepted previously'
    before: ->
      @driver.get 'https://tutor-staging.openstax.org'
    spec: ->
      @utils.wait.click(linkText: 'Login')
      @user.waitUntilLoaded()

      @user.driver.findElement(By.Xpath(//*[@id="auth_key"])).SendKeys("student01")
      @user.driver.findElement(By.Xpath(//*[@id="password"])).SendKeys("password")
      @utils.wait.click(linkText: 'Sign in')
      @user.waitUntilLoaded()

      #The user is re-presented with the current privacy policy

  '7647':
    title: '017 - Student | Re-presented the current terms of server if not accepted previously'
    before: ->
      @driver.get 'https://tutor-staging.openstax.org'
    spec: ->
      @utils.wait.click(linkText: 'Login')
      @user.waitUntilLoaded()

      @user.driver.findElement(By.Xpath(//*[@id="auth_key"])).SendKeys("student01")
      @user.driver.findElement(By.Xpath(//*[@id="password"])).SendKeys("password")
      @utils.wait.click(linkText: 'Sign in')
      @user.waitUntilLoaded()

      # The user is re-presented with the current terms of server

  '7648':
    title: '018 - Student | Able to edit their OpenStax Accounts profile'
    before: ->
      @driver.get 'https://tutor-staging.openstax.org'
    spec: ->
      @utils.wait.click(linkText: 'Login')
      @user.waitUntilLoaded()

      @user.driver.findElement(By.Xpath(//*[@id="auth_key"])).SendKeys("student01")
      @user.driver.findElement(By.Xpath(//*[@id="password"])).SendKeys("password")
      @utils.wait.click(linkText: 'Sign in')
      @user.waitUntilLoaded()

      @user.el.openHamburgerMenu().click()
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'My Account')
      @user.waitUntilLoaded()

      # The user is presented with "Your Account" page that allows them to edit their OpenStax Accounts profile

  '7650':
    title: '019 - Student | Registration and login are assistive technology-friendly'
    before: ->
      @driver.get 'https://tutor-staging.openstax.org'
    spec_signing_in: ->
      @utils.wait.click(linkText: 'Login')
      @user.waitUntilLoaded()

      @user.driver.findElement(By.id("Enter_ID")).SendKeys("\t")
      @user.driver.findElement(By.id("Enter_ID")).SendKeys("\t")
      @user.driver.findElement(By.id("Enter_ID")).SendKeys("\t")
      @user.driver.findElement(By.id("Enter_ID")).SendKeys("\t")
      @user.driver.findElement(By.id("Enter_ID")).SendKeys("\t")
      @user.findElement().SendKeys("student01")

      @user.driver.findElement(By.id("Enter_ID")).SendKeys("\t")
      @user.findElement().SendKeys("password")

      @user.driver.findElement(By.id("Value")).SendKeys(Keys.RETURN)

      #The user is successfully logged in 

    spec_registering: ->
      @utils.wait.click(linkText: 'Login')
      @user.waitUntilLoaded()

      @utils.wait.click(linkText: 'Sign up')
      @user.waitUntilLoaded()

      @user.driver.findElement(By.Xpath(//*[@id="identity-login-button"])).click()
      @user.waitUntilLoaded()

      @user.driver.findElement(By.id("Enter_ID")).SendKeys("\t")
      @user.driver.findElement(By.id("Enter_ID")).SendKeys("\t")
      @user.driver.findElement().SendKeys("test")
      @user.driver.findElement(By.id("Enter_ID")).SendKeys("\t")
      @user.driver.findElement().SendKeys("test")   
      @user.driver.findElement(By.id("Enter_ID")).SendKeys("\t")
      @user.driver.findElement(By.id("Enter_ID")).SendKeys("\t")
      @user.driver.findElement().SendKeys("test@test.com")
      @user.driver.findElement(By.id("Enter_ID")).SendKeys("\t")
      @user.driver.findElement().SendKeys("testbot")
      @user.driver.findElement(By.id("Enter_ID")).SendKeys("\t")
      @user.driver.findElement().SendKeys("testtest")
      @user.driver.findElement(By.id("Enter_ID")).SendKeys("\t")
      @user.driver.findElement().SendKeys("testtest")

      @user.driver.findElement(By.id("Value")).SendKeys(Keys.RETURN)


      #The user is successfully registered.




















module.exports =
  cases: cases



