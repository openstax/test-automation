tutorCases = require './sections'

tutorCases.runCases 'CC1.04 - Exercise Editing and QA', JSON.parse(process.env.STAX_ATTACK_CASES)
