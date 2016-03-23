runTests = require './helpers/test-runner'
{STAX_ATTACK_PROJECT, STAX_ATTACK_TITLE, STAX_ATTACK_CASES} = process.env

project = STAX_ATTACK_PROJECT
title = STAX_ATTACK_TITLE
cases = JSON.parse(STAX_ATTACK_CASES)

runTests(project, title, cases)
