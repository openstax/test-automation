var fs = require('fs');
var path = require('path');

var _ = require('lodash');
var validator = require('validator');

var remotes = require('../../remotes');
var getProjectServersCollection = require('../project-servers-collection');

var VALID_PROJECTS = getValidProjects();

// Exposed functions and properties

function checkArgs(currentArgv, optionsArray){
  var checksToRun = [checkIsProjectValid, checkForValidRemotes, checkForValidUrl];

  setServerUrlFallback(currentArgv);

  var isAllChecksPassing = _.reduce(checksToRun, function(previousResults, checkToRun){
    return previousResults && checkToRun(currentArgv, optionsArray);
  }, true);

  return isAllChecksPassing;
}

function isRemote(argv){
  return _.isString(argv.r) && _.includes(_.keys(remotes), argv.r);
}

function isEnvOurs(ourPrefix, envValue, envName){
  var envPrefixes = [ourPrefix, 'SAUCE', 'BROWSERSTACK', 'SELENIUM', 'MOCHA', 'SERVER_URL'];

  return _.reduce(envPrefixes, function(result, prefix){
    return result || _.startsWith(envName, prefix);
  }, false);
}

function getServerUrlFromArgs(currentArgv){
  var isUrl = _.partial(validator.isURL, _, {require_protocol: true});

  var isURLSet = _.isString(currentArgv.server)? isUrl(currentArgv.server) : false;
  var serverUrl= isURLSet? currentArgv.server : getServerUrlByProject(currentArgv.project, currentArgv.server);

  if(isUrl(serverUrl)){
    return serverUrl;
  }

  return false;
}


module.exports = {
  checkArgs: checkArgs,
  getValidProjects: _.constant(VALID_PROJECTS),
  isRemote: isRemote,
  isEnvOurs: isEnvOurs,
  getServerUrlFromArgs: getServerUrlFromArgs
};



// Private functions
function getValidProjects() {
  var srcpath = path.resolve(__dirname + '../../../');
  return _.filter(fs.readdirSync(srcpath), function(file) {
    // ignore helpers and only get return directories
    return file !== 'helpers' && fs.statSync(path.join(srcpath, file)).isDirectory();
  });
}

function setServerUrlFallback(currentArgv){
  if (!currentArgv.server){
    if (process.env.SERVER_URL){
      // pulls in SERVER_URL from env if defined
      currentArgv.server = process.env.SERVER_URL;
    } else {
      // as last resort, fallback to project default
      currentArgv.server = 'default';
    }

    currentArgv.s = currentArgv.server;
  }
}

function checkIsProjectValid(currentArgv){
  var isProjectValid = _.includes(VALID_PROJECTS, currentArgv.project);
  var error;

  if(!isProjectValid){
    error = '\n\nInvalid --project option of "' + currentArgv.project + '" given.  ';
    error += '\nPlease give one of the following for option --project instead: \n\n';
    error += VALID_PROJECTS.join(', ');
    error += '\n\n';
    throw error;
  }

  return true;
}

function checkForValidRemotes(currentArgv, optionsArray){
  var remoteName = currentArgv.r;
  if(isRemote(currentArgv)){
    if(!remotes[remoteName].check()){
      throw remotes[remoteName].error;
    }
  }

  return true;
}

function checkForValidUrl(currentArgv, optionsArray){
  var serverCollection = getProjectServersCollection(currentArgv.project);
  var serverUrl = getServerUrlFromArgs(currentArgv);
  var serverAliases;
  var error;

  if(!serverUrl){
    error = '\n\nInvalid --server option of "' + currentArgv.server + '" given.  ';
    error += '\nPlease give one of the following for option --server instead: \n\n';
    error += 'A valid server URL with protocol (i.e. https://) \n\n'
    error += 'or one of the server aliases for ' + currentArgv.project + ': \n\n';
    serverAliases = serverCollection.getAllTags();
    error += serverAliases.join(', ') + '\n\n';
    throw error;
  }

  return true;
}

function getServerUrlByProject(project, serverAlias){
  var serverCollection = getProjectServersCollection(project);
  var server = serverAlias? serverCollection.find(serverAlias) : false;
  var serverUrl = '';

  if(_.isObject(server)){
    serverUrl = server.url;
  }

  return serverUrl;
}
