from connect import db
from models import Transactions, Users
from flask_login import current_user
from datetime import datetime
from sqlalchemy import func
import numpy as np
import plotly
import plotly.graph_objs as go
import pandas as pd
import json

today = datetime.today()


def unique(list1):

    # insert the list to the set
    list_set = set(list1)
    # convert the set to the list
    unique_list = list(list_set)
    return unique_list


# account value1
def main_graph1():

    mp = {}
    dstart = "2021-10-01"
    # print(type(dstart))
    mp[dstart] = 0
    rows = (
        Transactions.query.filter_by(userId=current_user.id)
        .order_by(Transactions.date)
        .all()
    )
    for r in rows:
        dt = (r.date).strftime("%Y-%m-%d")

        if dt in mp.keys():
            if r.type == 0:
                mp[dt] = mp[dt] + int(r.amount) + 10
            else:
                mp[dt] = mp[dt] - int(r.amount)
        else:
            if r.type == 0:
                mp[dt] = int(r.amount) + 10
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
    dstart = "2021-10-01"
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
