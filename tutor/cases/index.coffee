Helpers = require 'openstax-tutor/test-integration/helpers'
{describe} = Helpers
_ = require 'lodash'
fs = require 'fs'

cases = {}

loadCase = (caseNumber) ->
  return if cases[caseNumber]?
  testCase = if fs.existsSync("#{__dirname}/#{caseNumber}.coffee") then require("./#{caseNumber}") else null
  cases[caseNumber] = testCase

runCase = (caseNumber) ->
  loadCase(caseNumber) unless cases?[caseNumber]

  {spec, description} = cases[caseNumber]

  @it(description, spec)

runSuite = (suiteDescription, caseNumbers) ->

  _.each caseNumbers, loadCase

  cases = _.filter caseNumbers, (caseNumber) ->
    cases[caseNumber]

  describe suiteDescription, ->
    _.each cases, _.bind(runCase, @)


module.exports =
  runSuite: runSuite
