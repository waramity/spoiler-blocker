var $document, exileTraitorousSpoiler, first_feed_elem_text, incrementBadgeNumber, initialize, initiateSpoilerBlocking, num_feed_elems, searchForAndBlockSpoilers, settings;

first_feed_elem_text = null;

num_feed_elems = null;

settings = {
  show_specific_words: true,
  execute_trailors: false,
  facebook_blocked: true,
  twitter_blocked: true,
  google_news_blocked: true
};

$document = $(document);

$document.ready(function() {
  return chrome.runtime.sendMessage({
    userPreferencesRequested: true
  }, (function(_this) {
    return function(response) {

      settings.execute_trailors = response.destroySpoilers;

      settings.facebook_blocked = response.facebookEnabled ;
      settings.twitter_blocked = response.twitterEnabled ;
      settings.google_news_blocked = response.googleNewsEnabled ;

      if (response.blockingEnabled) {
        return initialize();
      }
    };
  })(this));
});
  //============================================
initiateSpoilerBlocking = function(selector_string, remove_parent) { //selector_string and start search tag elements
  searchForAndBlockSpoilers(selector_string, true, remove_parent);
  return $document.mousemove(function() {
      return searchForAndBlockSpoilers(selector_string, false, remove_parent);
  });
};
//============================================
character_names = ''

searchForAndBlockSpoilers = (function(_this) {
  return function(feed_elements_selector, force_update, remove_parent) {
    var $new_feed_elems, last_feed_elem_text, new_last_text, new_length;
    $new_feed_elems = $(feed_elements_selector);
    if (remove_parent) {
      $new_feed_elems = $new_feed_elems.parent();
    }
    if ($new_feed_elems.length === 0) {
      return;
    }
    new_length = $new_feed_elems.length;
    new_last_text = $new_feed_elems.last()[0].textContent


    if (force_update || (new_length !== num_feed_elems) || (new_last_text !== last_feed_elem_text)) {
      last_feed_elem_text = new_last_text;
      num_feed_elems = new_length;

      return $new_feed_elems.each(function() {
        var matchedSpoiler;
        if (this.className.search(/glamoured/) > -1) {
          return;
        }
        //=========================================
        if(character_names == ''){
          theUrl = 'http://127.0.0.1:5000/get-character-names'
          xmlHttp = new XMLHttpRequest();
          xmlHttp.open( "GET", theUrl, false );
          xmlHttp.send( null );
          character_names = xmlHttp.responseText
        }
        //=========================================
        extra_character = []
        extra_words_to_block = character_names.split('|')

        for(var i = 0; i < extra_words_to_block.length; i ++) {
          character_list = extra_words_to_block[i].split(',')
          extra_character.push(character_list)
        }

        function getUnique(arr){
          const final = [ ];
          arr.map((e,i)=> !final.includes(e) && final.push(e) )
          return final
        }
        clean_character_name = []


        // """ clean text """
        extra_character_to_block = [[]]

        for(var i = 0; i < extra_character.length; i++) {
          for(var j = 0; j < extra_character[i].length; j++) {
            if(extra_character[i][j].replace(/[^a-zA-Z ]/g, "") != '' && extra_character[i][j].replace(/[^a-zA-Z ]/g, "") != ' ') {
              clean_character_name.push(extra_character[i][j].replace(/[^a-zA-Z ]/g, ""))

            }
        }
          extra_character_to_block.push(clean_character_name)
          clean_character_name = []

        }

        extra_character_to_block = getUnique(extra_character_to_block)
        matchedSpoiler = null
        movie_id = -1

        for(var i = 0; i < extra_character_to_block.length; i++) {

          matchedSpoiler = this.textContent.match(new RegExp(SPOILER_WORDS_LIST.concat(extra_character_to_block[i]).join('|'), 'i'));

          if(matchedSpoiler != null) {
            movie_id = i
            break;
          }
        }

        var removed_bleu_score =  '';
        var marked
        //============= Check
        if(matchedSpoiler !== null) {
          var bleu_score_regex = /\(Bleu\sscore:\s[\d.a-z-]+\)/g;
          marked = matchedSpoiler.input.match(bleu_score_regex)
        }
        //============= Check

        // var marked = matchedSpoiler.input.match(bleu_score_regex)
        if (!POST_ARR.includes(matchedSpoiler) &&  marked == null) {
          POST_ARR.push(matchedSpoiler)



          var xhr = new XMLHttpRequest();
          xhr.open("POST", 'http://127.0.0.1:5000/get-spoil-and-send-score', true);
          //Send the proper header information along with the request
          xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
          var spoiler_suspect = $(this);


          xhr.onreadystatechange = function() { // Call a function when the state changes.
              if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
                  // Request finished.
                  decimal_score = parseInt(this.response * 10)
                  console.log("score:" + decimal_score)
                  bleu_score = parseFloat(this.response)
                  if(decimal_score === 0) {
                    // console.log("red: ", score)
                    return exileTraitorousSpoiler(spoiler_suspect, 'white', bleu_score); // red
                  }
                  else if(decimal_score >= 1 && decimal_score <= 3) {
                    // console.log("orange: ", score)
                    return exileTraitorousSpoiler(spoiler_suspect, 'green', bleu_score); //orange
                  }
                  else if(decimal_score >= 4 && decimal_score <= 6) {
                    // console.log("yellow: ", score)
                    return exileTraitorousSpoiler(spoiler_suspect, 'orange', bleu_score); //yellow
                  }
                  else if(decimal_score >= 7 && decimal_score <= 10) {
                    // console.log("green: ", score)
                    return exileTraitorousSpoiler(spoiler_suspect, 'red', bleu_score); // dark green
                  }
                  // else if(decimal_score === 4) {
                  //   // console.log("blue: ", score)
                  //   return exileTraitorousSpoiler(spoiler_suspect, 'blue', bleu_score); //light green
                  // }
              }
          }
          xhr.send("spoil_suspect=" + $(this).context.innerText + "&movie_id=" + movie_id);
        }
      });
    }
  };
})(this);

exileTraitorousSpoiler = function($traitor, score_color, bleu_score) {
  var $glamour, glamour_string, specific_words;

  if (settings.execute_trailors) {
    if(bleu_score * 10 > 0)
      $traitor.empty();
    return;
  }

  bleu_string = "\(Bleu score: " +  bleu_score  + "\)"
  // glamour_string = "<div style='background-color: " + score_color + ";' class='spoiler-glamour'> <h4 class='spoiler-glamour'>" + bleu_string + "</h4></div>";

  glamour_string = "<div style='background-color: " + score_color + ";' class='spoiler-glamour'> <h4 class='spoiler-glamour'>" + bleu_string + "</h4></div>";

  $(glamour_string).appendTo($traitor);
  $glamour = $traitor.find('.spoiler-glamour');
};

initialize = (function(_this) {
  return function() {
    var url;
    url = window.location.href.toLowerCase();
    if (url.indexOf('facebook') > -1 && settings.facebook_blocked) {
      return initiateSpoilerBlocking(FACEBOOK_FEED_ELEMENTS_SELECTOR);
    } else if (url.indexOf('twitter') > -1 && settings.twitter_blocked) {
      return initiateSpoilerBlocking(TWITTER_FEED_ELEMENTS_SELECTOR);
    } else if (url.indexOf('news.google') > -1 && settings.google_news_blocked) {
      return initiateSpoilerBlocking(GOOGLE_NEWS_FEED_ELEMENTS_SELECTOR, true);
    }
  };
})(this);
