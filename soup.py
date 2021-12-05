import requests
from bs4 import BeautifulSoup as BS
from models import stockDailyValue, stockList
from datetime import datetime
from connect import db
from flask_login import current_user


stocks = [
    "CIPLA",
    "ASIANPAINT",
    "HCLTECH",
    "HDFCBANK",
    "GAIL",
    "ICICIBANK",
    "INDUSINDBK",
    "MARUTI",
    "SBIN",
    "RELIANCE",
    "TCS",
    "TITAN",
]

today = (datetime.today()).strftime("%Y-%m-%d")


def refresh_prices():
    table = stockDailyValue.query.filter_by(date=today).all()

    if len(table) != 0:
        # print("hekko")
        for stock in stocks:
            baseurl = "http://google.com/finance/quote/"
            url = baseurl + stock + ":NSE?hl=en&gl=in"
            r = requests.get(url)

            soup = BS(r.text, features="html.parser")
            price = soup.find(class_="YMlKec fxKbKc").text[1:]

            price = float(price.replace(",", ""))
            data = stockDailyValue.query.filter_by(date=today, sname=stock).first()
            data.value = price
            db.session.commit()

            stockdata = stockList.query.filter_by(
                userId=current_user.id, stockname=stock
            ).first()
            # print(len(stockdata))
            stockdata.curr_value = price
            db.session.commit()

    else:
        for stock in stocks:
            baseurl = "http://google.com/finance/quote/"
            url = baseurl + stock + ":NSE?hl=en&gl=in"
            r = requests.get(url)

            soup = BS(r.text, features="html.parser")
            price = soup.find(class_="YMlKec fxKbKc").text[1:]

            price = float(price.replace(",", ""))

            data = stockDailyValue(sname=stock, date=today, value=price)
            db.session.add(data)
            db.session.commit()

    return


# refresh_prices()
