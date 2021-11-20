from typing import Protocol
from connect import app, db
from flask import Flask, render_template, session, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from forms import loginForm, registrationForm, profiles, WithdrawFunds, addFunds
from models import Users, Transactions
from werkzeug.security import generate_password_hash, check_password_hash
from flask_msearch import Search
from datetime import datetime
from graph_dashboard import mainGraph1, mainGraph2
import operator, pickle

today = datetime.today()
now = datetime.now()


@app.route("/", methods=["GET", "POST"])
def index():

    RegistrationForm = registrationForm()
    LoginForm = loginForm()

    if RegistrationForm.validate_on_submit():
        user = Users.query.filter_by(email=RegistrationForm.email2.data).first()

        if user is not None:
            flash("Email Id already registered!")

        else:

            passw = generate_password_hash(RegistrationForm.password2.data)

            user = Users(
                email=RegistrationForm.email2.data,
                name=RegistrationForm.username2.data,
                pasword_hash=passw,
            )

            db.session.add(user)
            db.session.commit()
            flash("Thanks for registeration! Login to continue")
            return redirect(url_for("index"))

    if LoginForm.validate_on_submit():
        user = Users.query.filter_by(email=LoginForm.email1.data).first()

        if user is not None and user.check_password(LoginForm.password1.data):

            login_user(user)
            # flash('Log in Success')

            next = request.args.get("next")

            if next == None or not next[0] == "/":
                next = url_for("dashboard")

            return redirect(next)

        elif user is None:
            flash("Email Id not registered!")

        else:
            flash("Wrong Password!")

    return render_template("index.html", logForm=LoginForm, signForm=RegistrationForm)


@app.route("/instructions")
def instructions():
    return render_template("instructions.html")


# @app.route("/test")
# def test():
#     bar = testchart()
#     return render_template("test.html", plot=bar)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    invested = 4000
    Holdings = 4500
    profit = ((Holdings - invested) / invested) * 100
    profit = round(profit, 2)
    Balance = current_user.funds
    AccValue = Holdings + Balance

    line1 = mainGraph1()
    line2 = mainGraph2()

    return render_template(
        "dashboard.html",
        invested=invested,
        AccValue=AccValue,
        Holdings=Holdings,
        profit=profit,
        Balance=Balance,
        line1=line1,
        line2=line2,
    )


@app.route("/portfolio", methods=["GET", "POST"])
@login_required
def portfolio():
    pickle_file = open("dictionary.pkl", "rb")
    objects = pickle.load(pickle_file)
    pickle_file.close()
    print(type(objects))
    sorted_d = dict(sorted(objects.items(), key=operator.itemgetter(1), reverse=True))

    for obj in sorted_d:
        sorted_d[obj] = round(sorted_d[obj], 2)

    return render_template("portfolio.html", recom=sorted_d)


@app.route("/orders", methods=["GET", "POST"])
@login_required
def orders():
    uid = current_user.id
    trans_data = Transactions.query.filter_by(userId=uid).order_by(
        Transactions.date.desc()
    )
    return render_template("orders.html", trans_data=trans_data)


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    pform = profiles()
    addform = addFunds()
    withform = WithdrawFunds()

    if addform.validate_on_submit() and addform.submit1.data:
        current_user.funds = current_user.funds + int(addform.amount.data)
        db.session.commit()
        flash("Funds added successfuly")
        return redirect(url_for("profile"))

    elif withform.validate_on_submit() and withform.submit2.data:
        funds = int(withform.amount.data)
        if funds <= current_user.funds:
            current_user.funds = current_user.funds - funds
            db.session.commit()
            flash("Funds withdrawn successfuly")
        return redirect(url_for("profile"))

    if pform.validate_on_submit():
        current_user.address = pform.address.data
        current_user.mode = pform.mode.data
        db.session.commit()
        flash("User Account Updated")
        return redirect(url_for("profile"))

    elif request.method == "GET":
        pform.name.data = current_user.name
        pform.email.data = current_user.email
        pform.funds.data = current_user.funds
        pform.address.data = current_user.address
        pform.mode.data = current_user.mode

    return render_template(
        "profile.html", proForm=pform, addform=addform, withform=withform
    )


if __name__ == "__main__":
    app.run(debug=True)
