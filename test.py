from models import Transactions, Users, stockList, stockDailyValue
from connect import db
from flask_login import current_user
from datetime import datetime

today = (datetime.today()).strftime("%Y-%m-%d")


# -----------------------------------------------------
# all_data = Transactions.query.all()
# all_data1 = Users.query.all()
# for row in all_data:
# row.date = row.date[:10]
# db.session.commit()
# print(f"{row.id}, {row.name}, {row.funds}, {row.address}, {row.email}")
# -------------------------------------------------------

# ------------------------------------------------------
# stocks = [
#     "AXISBANK",
#     "HDFCBANK",
#     "HEROMOTOCO",
#     "INFY",
#     "BRITANNIA",
#     "BHARTIARTL",
#     "TATASTEEL",
#     "TATAMOTORS",
# ]
# for stock in stocks:
# stockDailyValue.query.filter_by(date="2021-11-28").delete()
# db.session.commit()

# keyword = "gail"
# data = Transactions.query.filter(Transactions.stock == "GAIL").all()
# for row in data:
# print(f"{row.stockname}, {row.curr_value}, {row.invested}")
# ------------------------------------------------------


# ------------------------------------------------------
# data = stockDailyValue.query.filter_by(date=today).all()
# data = db.session.query(stockDailyValue.date).filter(stockDailyValue.date>="2021-11-21").distinct().order_by(stockDailyValue.date).all()
# for row in data:
#     print(f"{row.date},{row.sname},{row.value}")
# --------------------------------------------------------


# data = Transactions.query.all()
Transactions.query.filter_by(
    userId=1, date="2021-12-05", stock="HDFCBANK", type=0
).delete()
db.session.commit()
# for row in data:
# print(f"{row.id}, {row.stock}, {row.userId}, {row.date}")
# -------------------------------------------------------
# users = stockDailyValue.query.all()
# db.session.query(stockDailyValue).delete()
# db.session.commit()
# ----------------------------------------------------


# -----------------------------------------------------
# from datetime import date, datetime

# now = date.today()
# dd/mm/YY H:M:S
# print("now =", now)

# dt_string = now.strftime("%Y-%m-%d")
# print("date and time =", dt_string)
# --------------------------------------------------------
