from models import Transactions, Users, stockList, stockDailyValue
from connect import db
from flask_login import current_user

# -----------------------------------------------------
# all_data = Transactions.query.all()
# all_data1 = Users.query.filter_by(name="Pallavi").all()
# for row in all_data1:
# print(f"{row.id}, {row.name}, {row.funds}, {row.address}, {row.email}")
# -------------------------------------------------------

# ------------------------------------------------------
# data = stockList.query.all()
# keyword = "gail"
# data = Transactions.query.filter(Transactions.stock == "GAIL").all()
# for row in data:
#     print(f"{row.id}, {row.stockname}, {row.userId}, {row.invested}")
# ------------------------------------------------------


# ------------------------------------------------------
# data = stockDailyValue.query.all()
data = db.session.query(stockDailyValue.date).filter(stockDailyValue.date>"2021-11-23").distinct()
# .filter(stockDailyValue.date > "2021-11-24")
for row in data:
    print(f"{row.date}")
# --------------------------------------------------------


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
