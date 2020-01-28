var DATA_KEY, FACEBOOK_FEED_ELEMENTS_SELECTOR, GOOGLE_NEWS_FEED_ELEMENTS_SELECTOR, SPOILER_WORDS_LIST, SPOILER_WORDS_REGEX, TWITTER_FEED_ELEMENTS_SELECTOR, POST_ARR;

DATA_KEY = 'smart-spoiler-blocker';

// FACEBOOK_FEED_ELEMENTS_SELECTOR = 'div[data-testid="fbfeed_story"], div[role="article"], #pagelet_trending_tags_and_topics ul > li';
FACEBOOK_FEED_ELEMENTS_SELECTOR = 'div[data-testid="fbfeed_story"], div[role="article"], #pagelet_trending_tags_and_topics ul > li';

GOOGLE_NEWS_FEED_ELEMENTS_SELECTOR = 'a[target="_blank"]';

TWITTER_FEED_ELEMENTS_SELECTOR = "[data-testid='tweet']";

// TWITTER_FEED_ELEMENTS_SELECTOR = "[data-testid='tweet']";
// TWITTER_FEED_ELEMENTS_SELECTOR = "[data-item-type='tweet'], .trend-item";


SPOILER_WORDS_LIST = ['Tony Stark','Iron Man','Steve Rogers','Captain America','Bruce Banner','Hulk','Thor','Natasha Romanoff','Black Widow','Clint Barton','Hawkeye','James Rhodes','War Machine','Scott Lang','Ant Man','Stephen Strange','Doctor Strange','TChalla','Black Phanther','Carol Danvers','Captain Marvel','Peter Parker','Spider Man','Nebula','Gamora','Hope Van Dyne','The Wasp','Valkyrie','Frigga','Wanda Maximoff','Scarlet Witch','Sam Wilson','Falcon','Bucky Barnes','Winter Soldier','Loki','Okoye','Wong','Mantis','Drax','Shuri','Howard Stark','The Ancient One','Happy Hogan','Peggy Carter','Jane Foster','Aunt May','Korg','Ramonda','Hank Pym','Janet Van Dyne','Maria Hill','MBaku','Laura Barton','Agent Sitwell','Brock Rumlow','Akihiko','Ebony Maw','Javis','Groot','Rocket','Pepper Potts','Alexander Pierce','Thanos','Peter Quill','Star Lord','Nick Fury','Morgan Stark','Red Skull','Cassie Langl','Friday','Cooper Barton','Lila Barton','Nathaniel Barton'];

SPOILER_WORDS_REGEX = new RegExp(SPOILER_WORDS_LIST.join('|'), 'i');

POST_ARR = new Array()
