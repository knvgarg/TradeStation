stocks = [
    "CIPLA",
    "ASIANPAINT",
    "HDFCBANK",
    "HCLTECH",
    "GAIL",
    "ICICIBANK",
    "INDUSINDBK",
    "MARUTI",
    "SBIN",
    "RELIANCE",
    "TCS",
    "TITAN",
]

from senti_helper import predict_sentiment
from collections import Counter
import pandas as pd
import pickle

parameters = [
    {
        "query": "(CIPLA) (lang:en)",
        "max_results": "100",
        "tweet.fields": "created_at,lang",
    },
    {
        "query": "(ASIANPAINT) (lang:en)",
        "max_results": "100",
        "tweet.fields": "created_at,lang",
    },
    {
        "query": "(HDFCBANK) (lang:en)",
        "max_results": "100",
        "tweet.fields": "created_at,lang",
    },
    {
        "query": "(HCLTECH) (lang:en)",
        "max_results": "100",
        "tweet.fields": "created_at,lang",
    },
    {
        "query": "(GAIL) (lang:en)",
        "max_results": "100",
        "tweet.fields": "created_at,lang",
    },
    {
        "query": "(ICICIBANK) (lang:en)",
        "max_results": "100",
        "tweet.fields": "created_at,lang",
    },
    {
        "query": "(INDUSINDBK OR INDUS INDIA BANK) (lang:en)",
        "max_results": "100",
        "tweet.fields": "created_at,lang",
    },
    {
        "query": "(MARUTI) (lang:en)",
        "max_results": "100",
        "tweet.fields": "created_at,lang",
    },
    {
        "query": "(SBIN OR STATE BANK OF INDIA) (lang:en)",
        "max_results": "100",
        "tweet.fields": "created_at,lang",
    },
    {
        "query": "(RELIANCE) (lang:en)",
        "max_results": "100",
        "tweet.fields": "created_at,lang",
    },
    {
        "query": "(TCS) (lang:en)",
        "max_results": "100",
        "tweet.fields": "created_at,lang",
    },
    {
        "query": "(TITAN) (lang:en)",
        "max_results": "100",
        "tweet.fields": "created_at,lang",
    },
]


def get_predictions():
    predictions = {}

    for i, stk in enumerate(stocks):
        # print(parameters[i])
        df = pd.DataFrame()
        df, idx, le = predict_sentiment(parameters[i], stk)
        pos = Counter(idx)["POSITIVE"]
        neg = Counter(idx)["NEGATIVE"]

        change = ((pos - neg) / (pos + neg)) * 100

        predictions[stk] = change * (le / 2400)

        print(stk, predictions[stk])
        # print(df)

    # open_file = open("dictionary.pkl", "wb")
    # pickle.dump(predictions, open_file)
    # open_file.close()

    return predictions
