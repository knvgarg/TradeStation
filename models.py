from connect import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from connect import login_manager


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


class Users(db.Model, UserMixin):

    __tablename__ = "users"
    name = db.Column(db.String(64))
    pasword_hash = db.Column(db.String(128))
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(128))
    funds = db.Column(db.Integer, default=0)
    email = db.Column(db.String(64), unique=True, index=True)
    mode = db.Column(db.Integer, default=0)  # 0 is manual, 1 is automatic

    def check_password(self, password):
        return check_password_hash(self.pasword_hash, password)

    def _repr_(self):
        return f"Username {self.username}"


class Transactions(db.Model):

    __searchable__ = ["stock", "type"]
    users = db.relationship(Users)
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    type = db.Column(db.Integer)  # 0buy #1sell
    stock = db.Column(db.String(64))
    date = db.Column(db.DateTime)
    userId = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def _repr_(self):
        return f"amount : {self.amount}\
             ,cash : {self.type},\
                       stock : {self.stock},\
                            date : {self.date} "


class stockList(db.Model):
    # __searchable__ = ["stockname"]

    users = db.relationship(Users)
    id = db.Column(db.Integer, primary_key=True)
    stockname = db.Column(db.String(64))
    curr_value = db.Column(db.Integer)  # everyday changes
    no_of_stocks = db.Column(db.Integer, default=0)
    invested = db.Column(
        db.Integer, default=0
    )  # (value at time of buying)*(num of stocks)
    userId = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def _repr_(self):
        return f"stockname: {self.stockname} , curr_value: {self.curr_value}"


class stockDailyValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sname = db.Column(db.String(64))
    date = db.Column(db.String(64))
    value = db.Column(db.Integer)

    def _repr_(self):
        return f"stockname: {self.sname}, date:{self.date}, value: {self.value}"
