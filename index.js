var spawn = require('child_process').spawn;
var _ = require('lodash');

require('dotenv-safe').load();

var browsers = ['chrome:36:Windows', 'firefox:36:Windows', 'internet explorer:10:Windows 7'];

var mochas = _.map(browsers, function(browser){
  var browserOptions = _.extend({}, process.env, {SELENIUM_BROWSER: browser});
  return spawn('mocha', ['-R', 'spec', 'tutor/index.js'], {stdio: "inherit", env: browserOptions});
});
