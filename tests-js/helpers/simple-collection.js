var _ = require('lodash');

function matchTags(tagsToFind, tags){
  // does the array of tags have all the tags in tagsToFind?
  return _.isEmpty(_.difference(tagsToFind, tags));
}

function SimpleCollection(data){
  this.data = data;

  return this;
}

SimpleCollection.prototype.find = function(){
  var tags = _.toArray(arguments);
  var firstMatchingData = _.find(this.data, function(dataObject){
    return matchTags(tags, dataObject.tags);
  });

  return firstMatchingData;
}

SimpleCollection.prototype.findAll = function(){
  var tags = _.toArray(arguments);
  var allMatchingData = _.filter(this.data, function(dataObject){
    return matchTags(tags, dataObject.tags);
  });

  return allMatchingData;
}

SimpleCollection.prototype.get = function(){
  return _.cloneDeep(this.data);
}

SimpleCollection.prototype.getDefault = function(){
  // assumes that first is default
  return _.first(this.data);
}

SimpleCollection.prototype.getAllTags = function(){
  var allTags = _(this.data)
    .map(_.property('tags'))
    .flatten();

  return allTags;
}

module.exports = SimpleCollection
