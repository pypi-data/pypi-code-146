"""
Twitter Threader is a library to manage threads on Twitter. You can GET and POST threads on Twitter
"""
__version__ = "1.5.1"
__author__ = "Iyanuoluwa Ajao"
__license__ = "MIT"

import textwrap
import tweepy


def connect_api(consumer_key, consumer_secret, access_token_key, access_token_secret):
    """
    Twitter Authentication Keys
    @param consumer_key:
    @param consumer_secret:
    @param access_token_key:
    @param access_token_secret:
    @return:
    """
    auth = tweepy.OAuth1UserHandler(consumer_key=consumer_key, consumer_secret=consumer_secret,
                                    access_token=access_token_key, access_token_secret=access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api


class Thread:
    """
    Thread Class
    """

    def __init__(self, api):
        self.api = api

    def get_thread(self, status_id, thread=None):
        """
        GET a Thread from a Tweet status ID.
        @param status_id: The ID of a Tweet
        @param thread: A list of tweets
        @return: A list of tweets
        """
        status = (
            self.api.get_status(status_id, tweet_mode="extended")
            if status_id is None
            else self.api.get_status(status_id, tweet_mode="extended")
        )
        thread = [] if thread is None else thread
        status_id = status.in_reply_to_status_id
        tweet = str(status.full_text)
        thread.append(tweet)
        if status_id is None:
            return thread
        return self.get_thread(status_id, thread)

    def convert_to_post(self, status_id):
        """
        Convert a thread(list of tweets) to a string of words
        @param status_id: The ID of a Tweet.
        @return: A string of words.
        """
        thread = self.get_thread(status_id)
        thread = reversed(thread)
        post = " ".join(thread)
        return post

    def _check_username(self, user):
        user = self.api.get_user(screen_name=user)
        screen_name = user.screen_name
        return screen_name

    def _convert_username(self, username):
        mention = f"@{self._check_username(username)} "
        return mention

    def post_thread(self, sentences, username, in_reply_to_status_id=None, thread=None):
        """
        POST a thread from a string of words.
        @param sentences: A string a words.
        @param username: The username of a Twitter account
        @param in_reply_to_status_id:
        @param thread: A list of tweets
        @return:
        """
        mention = self._convert_username(username)
        mention_length = len(mention)
        left = 280 - mention_length

        thread = [] if thread is None else thread
        tweets = textwrap.wrap(sentences, width=left)
        for tweet in tweets:
            sentences = sentences[len(tweet):]
            tweet = self.api.update_status(status=mention + f"{tweet}", in_reply_to_status_id=in_reply_to_status_id)
            thread.append(tweet.id)
            if sentences is None:
                return thread
            in_reply_to_status_id = int(tweet.id)
            return self.post_thread(sentences, mention, in_reply_to_status_id, thread)
