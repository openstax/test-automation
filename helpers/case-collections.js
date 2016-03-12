var describe = require('openstax-tutor/test-integration/helpers').describe;
var _ = require('lodash');

var requireDirectory = require('require-directory');

// Utils
function loadSections(sectionModule){
  return requireDirectory(sectionModule);
}

function getCasesBySections(sections){
  return _(sections)
    .mapValues(function(sectionCases){
      return _.keys(sectionCases.cases);
    })
    .value();
}

function getCasesFromSections(sections){
  return _(sections)
    .map(_.property('cases'))
    .reduce(function(allCases, currentCases){
      return _.extend(allCases, currentCases);
    }, {});
}

function getCaseById(cases, caseId){
  return cases[caseId];
}

function getCaseIdsBySectionName(sectionCases, sectionName){
  return sectionCases[sectionName];
}



// CaseCollections class

function CaseCollections(sectionModule){
  this.loadSections(sectionModule);
  this.setCasesBySections();
  this.setCases();
}

CaseCollections.prototype.loadSections = function(sectionModule){
  this.sections = loadSections(sectionModule);
  return this;
}

CaseCollections.prototype.setCasesBySections = function(){
  this.sectionCases = getCasesBySections(this.sections);
  return this;
}

CaseCollections.prototype.setCases = function(){
  this.cases = getCasesFromSections(this.sections);
  return this;
}

CaseCollections.prototype.runCaseById = function(caseId, context){
  var caseToRun = getCaseById(this.cases, caseId);
  context.it(caseToRun.title, caseToRun.spec);

  return this;
}

CaseCollections.prototype.runCases = function(suiteDescription, caseIds){
  var collectionContext = this;
  var availableCases = _.filter(caseIds, _.partial(getCaseById, this.cases));

  describe(suiteDescription, function(){
    var testContext = this;
    _.each(availableCases, _.bind(collectionContext.runCaseById, collectionContext, _, testContext));
  });

  return this;
}

CaseCollections.prototype.runSection = function(suiteDescription, sectionName){
  var caseIds = getCaseIdsBySectionName(this.sectionCases, sectionName)
  if(_.isEmpty(caseIds)){
    // TODO throw a message
    return this;
  }

  this.runCases(suiteDescription, caseIds);

  return this;
}

module.exports = CaseCollections;
