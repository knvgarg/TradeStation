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
    funds = db.Column(db.Integer, default = 0)
    email = db.Column(db.String(64), unique=True, index=True)
    mode = db.Column(db.Boolean, default=0) #0 is manual, 1 is automatic

    def check_password(self, password):
        return check_password_hash(self.pasword_hash, password)

    def _repr_(self):
        return f"Username {self.username}"

