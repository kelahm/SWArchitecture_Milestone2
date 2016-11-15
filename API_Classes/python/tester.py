import twitter

twitter = twitter.Twitter()

tweet_list = twitter.search("$TWTR")

for tweet in tweet_list:
    print('@%s on %s tweeted: %s' % (tweet['user']['screen_name'], tweet['created_at'], tweet['text']))
