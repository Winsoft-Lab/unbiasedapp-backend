from .connect_twitter import connect_api
import tweepy as tw


def search_tweets(search_query, item_count):

    twitterApi = connect_api()

    from_date = "2020-09-16"

    tweets = tw.Cursor(
        twitterApi.search_tweets, q=search_query, lang="en", since=from_date
    ).items(item_count)

    return tweets


def tweet_texts(q, count):
    tweets = search_tweets(q, count)
    pass
