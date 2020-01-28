var loadUserPreferencesAndUpdate, sessionSpoilersBlocked, storeUserPreferences, updateSessionSpoilersBlocked;

sessionSpoilersBlocked = 0;

document.addEventListener('DOMContentLoaded', (function(_this) {
  return function() {

        theUrl = 'http://127.0.0.1:5000/get-movie-names'
        xmlHttp = new XMLHttpRequest();
        xmlHttp.open( "GET", theUrl, false );
        xmlHttp.send( null );
        movie_names = xmlHttp.responseText

        //=======================================

        movieLength = 0
        let movieList = document.getElementById('movie-list');
        movie_names = movie_names.split(", ")

        var para = document.createElement("p");
        movie_names.forEach(addMovieItems);

        function addMovieItems(item, index) {
          if(index != 0)
            document.getElementById("movie-list").innerHTML += "<li id='movies' value='" + item + "' index='" + index + "'>" + index + ":" + item +"</li><br>";

            // document.getElementById("movie-list").innerHTML += "<input type='checkbox' checked='checked' id='movies' value='" + item + "' index='" + index + "' />" + index + ":" + item +"<br>";
          movieLength += 1
        }

        //==========================================


    _this.blockingEnabledToggle = document.getElementById('blocking-enabled-toggle');
    _this.destroySpoilersToggle = document.getElementById('destroy-spoilers-toggle');

    _this.facebookToggle = document.getElementById('facebook-toggle');
    _this.twitterToggle = document.getElementById('twitter-toggle');
    _this.googleNewsToggle = document.getElementById('google-news-toggle');

    //==========================================


    _this.blockingEnabledToggle.addEventListener('change', storeUserPreferences);
    _this.destroySpoilersToggle.addEventListener('change', storeUserPreferences);

    _this.facebookToggle.addEventListener('change', storeUserPreferences);
    _this.twitterToggle.addEventListener('change', storeUserPreferences);
    _this.googleNewsToggle.addEventListener('change', storeUserPreferences);

    //==========================================

    loadUserPreferencesAndUpdate();
    //==========================================

    return setTimeout((function() {
      return chrome.runtime.sendMessage({
        fetchPopupTotal: true
      }, function(response) {
        if (response.newTotal) {
          sessionSpoilersBlocked = response.newTotal;
        }
      });
    }), 1);
  };
})(this));

loadUserPreferencesAndUpdate = (function(_this) {
  return function() {
    return loadUserPreferences(function() {
      _this.blockingEnabledToggle.checked = _this.userPreferences.blockingEnabled;
      _this.destroySpoilersToggle.checked = _this.userPreferences.destroySpoilers;

      _this.facebookToggle.checked = _this.userPreferences.facebookEnabled;
      _this.twitterToggle.checked = _this.userPreferences.twitterEnabled;
      _this.googleNewsToggle.checked = _this.userPreferences.googleNewsEnabled;

    });
  };
})(this);

storeUserPreferences = (function(_this) {
  return function() {
    var data;
    data = {};


    dataJSON = {
      blockingEnabled: _this.blockingEnabledToggle.checked,
      destroySpoilers: _this.destroySpoilersToggle.checked,

      facebookEnabled: _this.facebookToggle.checked,
      twitterEnabled: _this.twitterToggle.checked,
      googleNewsEnabled: _this.googleNewsToggle.checked,
    }


    data[DATA_KEY] = JSON.stringify(dataJSON);

    return chrome.storage.sync.set(data, function(response) {
      return chrome.runtime.sendMessage({
        userPreferencesUpdated: true
      }, (function() {}));
    });
  };
})(this);
