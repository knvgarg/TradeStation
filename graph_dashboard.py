from connect import db
from models import Transactions, Users, stockDailyValue
from flask_login import current_user
from datetime import datetime
from sqlalchemy import func
import numpy as np
import plotly
import plotly.graph_objs as go
import pandas as pd
import json

today = datetime.today()

stocks = {
    "CIPLA": 0,
    "ASIANPAINT": 0,
    "HDFCBANK": 0,
    "HCLTECH": 0,
    "BRITANNIA": 0,
    "HEROMOTOCO": 0,
    "AXISBANK": 0,
    "BHARTIARTL": 0,
    "GAIL": 0,
    "BAJFINANCE": 0,
    "ICICIBANK": 0,
    "INDUSINDBK": 0,
    "INFY": 0,
    "MARUTI": 0,
    "SBIN": 0,
    "RELIANCE": 0,
    "TCS": 0,
    "TATASTEEL": 0,
    "TITAN": 0,
    "TATAMOTORS": 0,
}


def unique(list1):

    # insert the list to the set
    list_set = set(list1)
    # convert the set to the list
    unique_list = list(list_set)
    return unique_list


# equity
def main_graph1():

    mp = {}
    dstart = "2021-11-01"
    # print(type(dstart))
    mp[dstart] = 0
    rows = (
        Transactions.query.filter_by(userId=current_user.id)
        .order_by(Transactions.date)
        .all()
    )
    for r in rows:
        dt = (r.date).strftime("%Y-%m-%d")

        num = int(r.amount) / int(r.price)
        num = int(num)

        rval = stockDailyValue.query.filter_by(date=dt, sname=r.stock).first()

        if dt in mp.keys():
            if r.type == 0:
                mp[dt] = mp[dt] + int(r.amount)
            else:
                mp[dt] = mp[dt] - int(r.amount)
        else:
            if r.type == 0:
                mp[dt] = int(r.amount)
            else:
                mp[dt] = 0 - int(r.amount)

    x = list(mp.keys())
    y = list(mp.values())

    for idx in range(1, len(x)):
        y[idx] = y[idx - 1] + y[idx]

    return x, y


# invested
def main_graph2():
    mp = {}
    rows = (
        Transactions.query.filter_by(userId=current_user.id)
        .order_by(Transactions.date)
        .all()
    )
    dstart = "2021-11-01"
    # print(type(dstart))
    mp[dstart] = 0

    for r in rows:
        dt = (r.date).strftime("%Y-%m-%d")
        # print(type(dt))
        if dt in mp.keys():
            if r.type == 0:
                mp[dt] = mp[dt] + int(r.amount)
            else:
                mp[dt] = mp[dt] - int(r.amount)
        else:
            if r.type == 0:
                mp[dt] = int(r.amount)
            else:
                mp[dt] = 0 - int(r.amount)

        # v = mp[dt]

    # dend = str(today.year) + "-12-31"
    # if not dend in mp.keys():
    #     mp[dend] = v

    x = list(mp.keys())
    y = list(mp.values())

    for idx in range(1, len(x)):
        y[idx] = y[idx - 1] + y[idx]

    return x, y


def mainGraph1():

    x, y = main_graph1()
    df = pd.DataFrame({"x": x, "y": y})  # creating a sample dataframe

    data = [go.Scatter(x=df["x"], y=df["y"], mode="lines", name="Equity Holdings")]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


def mainGraph2():

    x, y = main_graph2()
    df = pd.DataFrame({"x": x, "y": y})  # creating a sample dataframe

    data = [
        go.Scatter(
            x=df["x"],
            y=df["y"],
            mode="lines",
            name="Invested",
        )
    ]
    # data.update_layout(
    #     xaxis_range=[datetime.datetime(2021, 1, 1), datetime.datetime(2021, 12, 31)]
    # )
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON
