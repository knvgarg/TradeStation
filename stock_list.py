from datetime import date, datetime
from models import stockList, stockDailyValue
from connect import db
from flask_login import current_user

stocks = [
    "CIPLA",
    "ASIANPAINT",
    "HDFCBANK",
    "HCLTECH",
    "BRITANNIA",
    "HEROMOTOCO",
    "AXISBANK",
    "BHARTIARTL",
    "GAIL",
    "BAJFINANCE",
    "ICICIBANK",
    "INDUSINDBK",
    "INFY",
    "MARUTI",
    "SBIN",
    "RELIANCE",
    "TCS",
    "TATASTEEL",
    "TITAN",
    "TATAMOTORS",
]


def function(idd):
    user = stockList.query.filter_by(userId=idd).first()
    if user is not None:
        return

    for stock in stocks:
        stk = stockList(stockname=stock, curr_value=100, userId=idd)
        db.session.add(stk)
        db.session.commit()
        print("stock added")


def changePrice():
    now = "2021-11-24"
    for stock in stocks:
        stk = stockDailyValue(sname=stock, value=102, date=now)
        db.session.add(stk)
        db.session.commit()
        print("stock added")


# changePrice()
