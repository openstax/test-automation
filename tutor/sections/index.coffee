Helpers = require 'openstax-tutor/test-integration/helpers'
{describe} = Helpers
_ = require 'lodash'
fs = require 'fs'

requireDirectory = require 'require-directory'

sections = requireDirectory(module)

sectionsCases = _(sections)
  .mapValues((sectionCases) ->
    _.keys(sectionCases.cases)
  )
  .value()

cases = _(sections)
  .map _.property('cases')
  .reduce((allCases, currentCases) ->
    _.extend(allCases, currentCases)
  , {})

runCase = (caseNumber) ->
  {spec, title} = cases[caseNumber]

  @it(title, spec)

runSuite = (suiteDescription, caseNumbers) ->

  availableCases = _.filter caseNumbers, (caseNumber) ->
    cases[caseNumber]

  describe suiteDescription, ->
    _.each availableCases, _.bind(runCase, @)

runSection = (suiteDescription, sectionName) ->
  caseNumbers = sectionsCases[sectionName]
  return if _.isEmpty(caseNumbers)

  runSuite(suiteDescription, caseNumbers)

module.exports =
  runSuite: runSuite
  runSection: runSection
