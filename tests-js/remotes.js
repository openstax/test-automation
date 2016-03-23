var _ = require('lodash');

var remotes = {
  sauce: {
    check: function(){
      return _.isString(process.env.SAUCE_USERNAME) && _.isString(process.env.SAUCE_KEY);
    },
    error: 'Credentials for Saucelabs need to be defined as environment variables SAUCE_USERNAME and SAUCE_KEY.',
    buildEnvs: function(envs){
      var remoteEnvs = {
        SELENIUM_CAPABILITIES: {
          username: envs.SAUCE_USERNAME,
          accessKey: envs.SAUCE_KEY
        },
        SELENIUM_REMOTE_URL: 'http://' + envs.SAUCE_USERNAME + ':' + envs.SAUCE_KEY + '@ondemand.saucelabs.com:80/wd/hub'
      };
      return remoteEnvs;
    },
    cleanEnvs: function(envs){
      delete envs.BROWSERSTACK_USERNAME;
      delete envs.BROWSERSTACK_KEY;
    }
  },
  browserstack: {
    check: function(){
      return _.isString(process.env.BROWSERSTACK_USERNAME) && _.isString(process.env.BROWSERSTACK_KEY);
    },
    error: 'Credentials for Browserstack need to be defined as environment variables BROWSERSTACK_USERNAME and BROWSERSTACK_KEY.',
    buildEnvs: function(envs){
      var remoteEnvs = {
        SELENIUM_CAPABILITIES: {
          'browserstack.user': envs.BROWSERSTACK_USERNAME,
          'browserstack.key': envs.BROWSERSTACK_KEY
        },
        SELENIUM_REMOTE_URL: 'http://hub.browserstack.com/wd/hub'
      };
      return remoteEnvs;
    },
    cleanEnvs: function(envs){
      delete envs.SAUCE_USERNAME;
      delete envs.SAUCE_KEY;
    }
  }
};

module.exports = remotes;
