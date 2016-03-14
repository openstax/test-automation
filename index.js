var spawn = require('child_process').spawn;
var _ = require('lodash');
var yargs = require('yargs');
require('dotenv').config();

var ENV_PREFIX = 'STAX_ATTACK'

var argumentOptions = {
  n: {
    alias: 'name',
    describe: 'Name of the test run',
    demand: true,
    type: 'string'
  },
  t: {
    alias: 'title',
    describe: 'Description of the test run',
    demand: true,
    type: 'string'
  },
  r: {
    alias: 'remote',
    describe: 'Which remote service to use?  Set to false to run locally.',
    choices: ['sauce', 'browserstack', false]
  },
  p: {
    alias: 'project',
    describe: 'Which project are you testing?',
    default: 'tutor',
    choices: ['tutor']
  },
  c: {
    alias: 'cases',
    describe: 'Which case ids are you running?',
    type: 'array'
  },
  b: {
    alias: 'browsers',
    default: [
      'chrome:36:Windows',
      'firefox:36:Windows',
      // 'internet explorer:10:Windows 7'
    ],
    describe: 'What browsers should the tests run in?',
    type: 'array'
  },
  s: {
    alias: 'server',
    describe: 'What server should the tests run against?',
    default: 'https://tutor-qa.openstax.org'
  }
};

function hasSauceCredentials(){
  return _.isString(process.env.SAUCE_USERNAME) && _.isString(process.env.SAUCE_ACCESS_KEY);
}

function isSaucy(argv){
  return argv.r === 'sauce';
}

function isEnvOurs(envValue, envName){
  var envPrefixes = [ENV_PREFIX, 'SAUCE', 'BROWSERSTACK', 'SELENIUM', 'MOCHA'];

  return _.reduce(envPrefixes, function(result, prefix){
    return result || _.startsWith(envName, prefix);
  }, false);
}

function buildTestOptions(){
  var argv = yargs.usage('Usage: $0 ')
    .env(ENV_PREFIX)
    .config('settings')
    .options(argumentOptions)
    .example('c', '$0 -c C7651 C7674', 'Run tests for cases C7651 and C7674.')
    .help('h')
    .alias('h', 'help')
    .check(function(currentArgv, optionsArray){
      if(isSaucy(currentArgv) && !hasSauceCredentials()){
        throw "Credentials for Saucelabs need to be defined as environment variables in .env as SAUCE_USERNAME and SAUCE_ACCESS_KEY.";
      }
      return true;
    })
    .argv;

  var envs = _.pickBy(process.env, isEnvOurs);
  var systemEnvs = _.omitBy(process.env, isEnvOurs);

  var SELENIUM_CAPABILITIES = {name: argv.name};
  if(isSaucy(argv)){
    _.extend(SELENIUM_CAPABILITIES, {
      username: envs.SAUCE_USERNAME,
      accessKey: envs.SAUCE_ACCESS_KEY
    });
    envs.SELENIUM_REMOTE_URL = 'http://' + envs.SAUCE_USERNAME + ':' + envs.SAUCE_ACCESS_KEY + '@ondemand.saucelabs.com:80/wd/hub';
  }

  envs.SELENIUM_CAPABILITIES = JSON.stringify(SELENIUM_CAPABILITIES);
  envs.SERVER_URL = argv.server;

  var envsFromArgs = buildEnvFromArgs(_.pick(argv, ['cases', 'project', 'title']));

  _.defaults(envs, envsFromArgs);
  _.extend(envs, systemEnvs);

  var testEnvs = _.map(argv.browsers, function(browser){
    return buildBrowserEnv(envs, browser);
  });

  return {
    browsers: argv.browsers,
    envs: testEnvs,
    system: envs.SELENIUM_REMOTE_URL || 'local',
    cases: JSON.parse(envs.STAX_ATTACK_CASES),
    runName: argv.name
  };
}

function buildEnvFromArgs(args){
  var envs = {};
  _.each(args, function(arg, argName){
    var envArgName = _.chain(ENV_PREFIX + ' ' + argName).snakeCase().toUpper().value();
    if(!_.isString(arg)){
      arg = JSON.stringify(arg);
    }
    envs[envArgName] = arg;
  });

  return envs;
}

function buildBrowserEnv(baseEnv, browser){
  return _.extend({}, baseEnv, {SELENIUM_BROWSER: browser});
}

function buildReportInfo(testOptions){
  var browsers = testOptions.browsers.join(', ');
  var cases = testOptions.cases.join(', ');

  return 'Running ' + testOptions.runName + ' with cases ' + cases + ' on browsers ' + browsers + ' at ' + testOptions.system;
}

function runTests(){
  var testOptions = buildTestOptions();

  process.stdout.write(buildReportInfo(testOptions));

  var mochas = _.map(testOptions.envs, function(env){
    return spawn('mocha', ['-R', 'spec', 'tests/index.js'], {stdio: "inherit", env: env});
  });
}

runTests();
