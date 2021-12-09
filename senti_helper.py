import requests
import json
import pandas as pd
import re
import flair
from datetime import datetime, timedelta
import requests
import pandas as pd

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAHruTwEAAAAABJp%2BEy%2BaaemWdysJO8F%2BiWcxQzk%3DOACpILWJYuNjuaDpl9d7O50YvAvrMMnUs0cTsNWiGOWupsb2Bk"
dtformat = "%Y-%m-%dT%H:%M:%SZ"  # the date format string required by twitter


def get_data(tweet):
    data = {"id": tweet["id"], "created_at": tweet["created_at"], "text": tweet["text"]}
    return data


def clean_tweet(tweet, stk):
    whitespace = re.compile(r"\s+")
    web_address = re.compile(r"(?i)http(s):\/\/[a-z0-9.~_\-\/]+")
    # tesla = re.compile(r"(?i)@Nifty(?=\b)")
    user = re.compile(r"(?i)@[a-z0-9_]+")

    # we then use the sub method to replace anything matching
    tweet = whitespace.sub(" ", tweet)
    tweet = web_address.sub("", tweet)
    # tweet = tesla.sub(stk, tweet)
    tweet = user.sub("", tweet)

    return tweet


# we use this function to subtract 60 mins from our datetime string


def time_travel(now, mins):

    now = datetime.strptime(now, dtformat)
    back_in_time = now - timedelta(minutes=mins)
    return back_in_time.strftime(dtformat)


def predict_sentiment(params, stk):
    # setup the API request
    endpoint = "https://api.twitter.com/2/tweets/search/recent"
    headers = {"authorization": f"Bearer {BEARER_TOKEN}"}

    now = datetime.now() - timedelta(minutes=331)
    last_day = now - timedelta(days=1)
    now = now.strftime(dtformat)
    df = pd.DataFrame()

    while True:
        if datetime.strptime(now, dtformat) < last_day:
            break
        pre60 = time_travel(now, 60)  # get 60 minutes before 'now'
        params["start_time"] = pre60
        params["end_time"] = now

        response = requests.get(
            endpoint, params=params, headers={"authorization": "Bearer " + BEARER_TOKEN}
        )

        now = pre60  # move the window 60 minutes earlier

        if response.json()["meta"]["result_count"] > 0:
            for tweet in response.json()["data"]:
                row = get_data(tweet)
                df = df.append(row, ignore_index=True)

    sentiment_model = flair.models.TextClassifier.load("en-sentiment")
    probs = []
    sentiments = []

    tweets = []
    for tweet in df["text"]:
        tweets.append(clean_tweet(tweet, stk))

    df["text"] = tweets

    for tweet in df["text"].to_list():
        sentence = flair.data.Sentence(tweet)
        sentiment_model.predict(sentence)
        probs.append(sentence.labels[0].score)  # numerical score 0-1
        sentiments.append(sentence.labels[0].value)  # 'POSITIVE' or 'NEGATIVE'

    df["probability"] = probs
    df["sentiment"] = sentiments

    idx = pd.Index(df["sentiment"])
    le = len(df)

    return df, idx, le
