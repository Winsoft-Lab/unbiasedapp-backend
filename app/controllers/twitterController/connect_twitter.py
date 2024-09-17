import tweepy as tw
from config import Config


def connect_api():
    """A function that connects the Twitter API with KEYS and SECRET"""

    auth = tw.OAuthHandler(Config.TWITTER_KEY, Config.TWITTER_SECRET)

    twitter_api = tw.API(auth, wait_on_rate_limit=True)

    return twitter_api
