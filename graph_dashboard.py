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

# account value1
def main_graph1():

    month = today.month

    x = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
    y = [0] * 12
    y[2] = 1.5
    y[3] = 2
    y[4] = 4
    y[5] = 4
    y[6] = 4.5
    y[7] = 4
    y[8] = 4
    y[9] = 5
    y[10] = 4.8
    y[11] = 4.7
    # for idx, xi in enumerate(x):
    #     y[idx] = current_user.budget - expenditure(idx + 1)

    return x, y


# invested
def main_graph2():

    month = today.month

    x = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
    y = [0] * 12
    y[2] = 1.5
    y[3] = 1.5
    y[4] = 3
    y[5] = 3
    y[6] = 3
    y[7] = 3
    y[8] = 3
    y[9] = 3.5
    y[10] = 3.5
    y[11] = 3.5

    # for idx, xi in enumerate(x):
    #     y[idx] = current_user.budget - expenditure(idx + 1)

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

    data = [go.Scatter(x=df["x"], y=df["y"], mode="lines", name="Invested")]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON
