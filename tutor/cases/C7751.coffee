Helpers = require 'openstax-tutor/test-integration/helpers'
{expect} = require 'chai'

DESCRIPTION = 'Admin | Recruitment and promo website is available'

RECRUITMENT_SITE = 'http://cc.openstax.org'

TEST = ->
  @driver.get(RECRUITMENT_SITE)
  @utils.wait.for(css: 'a[href*="sign-up"]')

module.exports =
  spec: TEST
  description: DESCRIPTION
