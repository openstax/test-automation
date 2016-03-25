CaseCollections = require './case-collections'

runTests = (project, title, cases) ->
  projectCaseRunner = new CaseCollections(project)
  projectCaseRunner.runCases title, cases

module.exports = runTests
