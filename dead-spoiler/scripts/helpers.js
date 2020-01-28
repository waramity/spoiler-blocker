var addClass, hasClass, loadUserPreferences;

loadUserPreferences = (function(_this) {
  return function(callback) {
    return chrome.storage.sync.get(DATA_KEY, function(result) {
      var userPreferencesJSONString;
      userPreferencesJSONString = result[DATA_KEY];
      if (!userPreferencesJSONString) {
        _this.userPreferences = {
          blockingEnabled: true,
          destroySpoilers: false,

          facebookEnabled: true,
          twitterEnabled: true,
          googleNewsEnabled: true,

        };
      } else {
        _this.userPreferences = JSON.parse(userPreferencesJSONString);
        if (!_this.userPreferences.hasOwnProperty('blockingEnabled')) {
          _this.userPreferences.blockingEnabled = true;
        }

        if (!_this.userPreferences.hasOwnProperty('destroySpoilers')) {
          _this.userPreferences.destroySpoilers = false;
        }

        if (!_this.userPreferences.hasOwnProperty('facebookEnabled')) {
          _this.userPreferences.facebookEnabled = true;
        }
        if (!_this.userPreferences.hasOwnProperty('twitterEnabled')) {
          _this.userPreferences.twitterEnabled = true;
        }
        if (!_this.userPreferences.hasOwnProperty('googleNewsEnabled')) {
          _this.userPreferences.googleNewsEnabled = true;
        }
      }
      if (callback) {
        return callback();
      }
    });
  };
})(this);
