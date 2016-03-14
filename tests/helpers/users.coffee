_ = require 'lodash'

matchTags = (tagsToFind, tags) ->
  _.isEmpty _.difference(tagsToFind, tags)


class UserCollection
  constructor: (users) ->
    @users = users
  get: (tags...) ->
    _.find @users, (user) ->
      matchTags(tags, user.tags)

  getAll: (tags...) ->
    _.filter @users, (user) ->
      matchTags(tags, user.tags)


module.exports = UserCollection
