module.exports = {
  // This is just shorthand to reference the installed dependencies you have.
  // Zapier will need to know these before we can upload.
  version: require('./package.json').version,
  platformVersion: require('zapier-platform-core').version,

  // If you want your trigger to show up, you better include it here!
  triggers: {},

  // If you want your searches to show up, you better include it here!
  searches: {},

  // If you want your creates to show up, you better include it here!
  creates: {},

  resources: {},
};
const dan_event = require('./triggers/dan_event');
const send_prompt = require('./creates/send_prompt');

module.exports = {
  version: require('./package.json').version,
  platformVersion: require('zapier-platform-core').version,

  triggers: {
    [dan_event.key]: dan_event,
  },

  creates: {
    [send_prompt.key]: send_prompt,
  },

  searches: {},
  resources: {},
};
