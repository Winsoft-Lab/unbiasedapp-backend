import re
import pandas as pd
import numpy as np
from textblob import TextBlob


def process_tweets(tweets):

    """A function that processess the tweets"""

    # twitterApi = connect_api()

    tweets_array = []

    for tweet in tweets:

        tweets_array.append(tweet)

    # ----------------CONVERTING TO DATA FRAME-----------------------
    tweets_df = pd.DataFrame()
    # populate the dataframe
    for tweet in tweets_array:
        hashtags = []
        for hashtag in tweet.entities["hashtags"]:
            hashtags.append(hashtag["text"])

        # text = twitterApi.get_status(id=tweet.id, tweet_mode='extended').full_text

        tweets_df = tweets_df.append(
            pd.DataFrame(
                {
                    "user_name": tweet.user.name,
                    "user_location": tweet.user.location,
                    "user_description": tweet.user.description,
                    "user_verified": tweet.user.verified,
                    "date": tweet.created_at,
                    "text": tweet.text,
                    "hashtags": [hashtags if hashtags else None],
                    "source": tweet.source,
                }
            )
        )

    tweets_df = tweets_df.reset_index(drop=True)

    df_tweets = tweets_df[["date", "user_location", "text"]]

    # -------------CONVERTING TO JSON-------------------------------------
    df_tweets["date"] = df_tweets["date"].astype("string")
    df_tweets[["date", "Date"]] = df_tweets["date"].str.split(" ", expand=True)

    df_val = df_tweets.drop(["Date"], axis=1)

    main_value = df_val.to_dict(orient="index")

    # --------------PORCESSESS TO ANALIZE TWEETS---------------------#

    list_dictionary = []

    for items in main_value.values():

        list_dictionary.append(items)

    new_main_value = pd.DataFrame(
        list_dictionary, columns=["date", "text", "user_location"]
    )

    # main_value = pd.DataFrame(main_value)#Convert list dictionary to dataframe.

    new_main_value["date"] = pd.to_datetime(new_main_value["date"])
    new_main_value["text"] = new_main_value["text"].astype("string")
    new_main_value["user_location"] = new_main_value["user_location"].astype("category")

    df_value = new_main_value
    a = np.array(df_value["text"])
    array_text = []
    for n in a:
        k = " ".join(
            re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|RT", " ", n).split()
        )
        array_text.append(k)

    data = pd.DataFrame(array_text, columns=["new_text"])

    df_data = pd.concat([df_value, data], axis=1)
    df_data = df_data.drop("text", axis=1)

    pol_val = []
    sent = np.array(df_data["new_text"])
    for i in sent:
        analysis = TextBlob(i)
        sent_polarity = round(analysis.sentiment.polarity, 4)
        pol_val.append(sent_polarity)
    sent_df = pd.DataFrame(pol_val, columns=["sentiment_polarity"])

    df_sentiment = pd.concat([df_data, sent_df], axis=1)

    def_sentiment = df_sentiment.to_dict()

    return def_sentiment
