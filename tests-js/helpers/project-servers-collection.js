var _ = require('lodash');
var SimpleCollection = require('./simple-collection');

function getProjectServersCollection(project){
  var projectServers = require('../' + project + '/servers.json');
  return new SimpleCollection(projectServers);
}

// only create a collection once per project.
module.exports = _.memoize(getProjectServersCollection);
