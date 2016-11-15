from TwitterSearch import *


class Twitter:
    def __init__(self):
        # Twitter API Keys
        self._consumer_key = 'ysTOqH80Wkf2RTm4ZdPzCam2E'
        self._consumer_secret = 'uHYz1s8I87VQmkKD00hyr1OOje7enGxQgmoSDOWTtwI3sYvRQP'
        self._access_token = '794268625096085504-Ft5NgnNZmkHi8bDIzqYUSTW0TzIx9Dh'
        self._access_token_secret = 'GRCErJ9qtVbL9mjo5mLhCAO22dSvOAgu9ajtxvXnNqL1O'

        # Setting up the Twitter Search Order object
        self._tso = TwitterSearchOrder()  # create a TwitterSearchOrder object
        self._tso.set_language('en')  # English tweets only
        self._tso.set_include_entities(False)  # Don't include all entities info
        self._tso.set_count(2)  # Limit number of tweets
        self._tso.set_result_type('popular')  # Most popular tweets are shown

    def search(self, term):
        try:
            self._tso.set_keywords([term])  # What is being searched for

            # Add keys to Twitter Search object
            ts = TwitterSearch(
                consumer_key=self._consumer_key,
                consumer_secret=self._consumer_secret,
                access_token=self._access_token,
                access_token_secret=self._access_token_secret
            )

            # Adding tweets to a list
            tweet_list = []
            for tweet in ts.search_tweets_iterable(self._tso):
                tweet_list.append(tweet)

            return tweet_list

        except TwitterSearchException as e:  # error handling
            print(e)
