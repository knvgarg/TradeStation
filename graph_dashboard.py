from connect import db
from models import Transactions, Users, stockDailyValue
from flask_login import current_user
from datetime import datetime, date
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


def numOfDays(date1, date2):
    return (date2 - date1).days


# equity
def main_graph1():
    #x,y
    #x - date
    #y - equity holding
    #EH - no. of stocks at that date * price of stock at that date(from StockDailyValue)
    #no. of stock at that date =
    mp = {}
    rows = (Transactions.query.filter_by(userId=current_user.id).order_by(
        Transactions.date).all())
    stocksUtil = {
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
    prev_day = "hello"
    for i, row in enumerate(rows):
        no_of_stocks = int(row.amount) // int(row.price)
        # print(no_of_stocks)
        cur_day = (row.date).strftime("%Y-%m-%d")
        if cur_day == prev_day:
            pass
        else:
            for stock in stocksUtil.keys():
                cur_price_row = stockDailyValue.query.filter_by(
                    sname=stock, date=prev_day).first()
                if cur_price_row:
                    cur_price = int(cur_price_row.value)
                    if prev_day not in mp.keys():
                        mp[prev_day] = cur_price * stocksUtil[stock]
                    else:
                        mp[prev_day] += cur_price * stocksUtil[stock]

            prev_day = cur_day

        if int(row.type) == 0:
            stocksUtil[row.stock] += no_of_stocks
            print(f"{row.stock}: {stocksUtil[row.stock]}")
        else:
            stocksUtil[row.stock] -= no_of_stocks
            print(f"{row.stock}: {stocksUtil[row.stock]}")

        if i == len(rows) - 1:
            for stock in stocksUtil.keys():
                cur_price_row = stockDailyValue.query.filter_by(
                    sname=stock, date=cur_day).first()
                if cur_price_row:
                    cur_price = int(cur_price_row.value)
                    if cur_day not in mp.keys():
                        mp[cur_day] = cur_price * stocksUtil[stock]
                    else:
                        mp[cur_day] += cur_price * stocksUtil[stock]

    x = list(mp.keys())
    y = list(mp.values())
    return x, y


# invested
def main_graph2():
    mp = {}
    rows = (Transactions.query.filter_by(userId=current_user.id).order_by(
        Transactions.date).all())

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

    data = [
        go.Scatter(x=df["x"], y=df["y"], mode="lines", name="Equity Holdings")
    ]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


def mainGraph2():

    x, y = main_graph2()
    df = pd.DataFrame({"x": x, "y": y})  # creating a sample dataframe

    data = [go.Scatter(
        x=df["x"],
        y=df["y"],
        mode="lines",
        name="Invested",
    )]
    # data.update_layout(
    #     xaxis_range=[datetime.datetime(2021, 1, 1), datetime.datetime(2021, 12, 31)]
    # )
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON
