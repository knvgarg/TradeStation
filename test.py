from models import Transactions, Users, stockList
from connect import db
from flask_login import current_user

# all_data = Transactions.query.all()
# all_data1 = Users.query.filter_by(name="Pallavi").all()
# for row in all_data1:
# print(f"{row.id}, {row.name}, {row.funds}, {row.address}, {row.email}")

# data = stockList.query.all()
# keyword = "gail"
# data = Transactions.query.filter(Transactions.stock == "GAIL").all()

# for row in data:
#     print("k")
#     print((row.stock))
#     print(f"{row.id}, {row.stockname}, {row.userId}, {row.invested}")

# user = Users.query.get(5)
# db.session.delete(user)
# db.session.commit()

# # for row in all_data1:
#     # print(f"{row.profile_image}")


# from datetime import datetime
# uid = current_user.id
# print(uid)
# print(type(uid))

# today = datetime.today()
# datem = datetime(today.year, today.month, 1)
# # print(today)
# # print(datem)

# # monthlyTransactions = Transactions.query.filter_by(date < str(datem)).all()
# # print(monthlyTransactions)
# # print(monthlyTransactions.cat)

# from datetime import datetime

# datetime object containing current date and time
# now = datetime.today()

# print("now =", now)

# dd/mm/YY H:M:S
# dt_string = now.strftime("%Y-%m-%d")
# print("date and time =", dt_string)
print(type(1))
