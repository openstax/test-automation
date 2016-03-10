var spawn = require('child_process').spawn;

require('dotenv-safe').load();
spawn('mocha', ['-R', 'spec', 'tutor/index.js'], {stdio: "inherit"});
