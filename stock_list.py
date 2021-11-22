from models import stockList
from connect import db
from flask_login import current_user


def function(idd):
    user = stockList.query.filter_by(userId=idd).first()
    if user is not None:
        return

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
    for stock in stocks:
        stk = stockList(stockname=stock, curr_value=100, userId=idd)
        db.session.add(stk)
        db.session.commit()
        print("stock added")