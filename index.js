var spawn = require('child_process').spawn;
var _ = require('lodash');

require('dotenv-safe').load();

var browsers = ['chrome:36:Windows', 'firefox:36:Windows', 'internet explorer:10:Windows 7'];
var SELENIUM_REMOTE_URL = 'http://' + process.env.SAUCE_USERNAME + ':' + process.env.SAUCE_ACCESS_KEY + '@ondemand.saucelabs.com:80/wd/hub';

var mochas = _.map(browsers, function(browser){
  var browserOptions = _.extend({}, process.env, {
    SELENIUM_BROWSER: browser,
    SELENIUM_REMOTE_URL: SELENIUM_REMOTE_URL
  });
  return spawn('mocha', ['-R', 'spec', 'tutor/index.js'], {stdio: "inherit", env: browserOptions});
});
