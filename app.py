from connect import app, db
from flask import Flask, render_template, session, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from forms import loginForm, registrationForm, profiles
from models import Users
from werkzeug.security import generate_password_hash, check_password_hash
from flask_msearch import Search
from datetime import datetime

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

    return render_template("dashboard.html")


@app.route("/passbook", methods=["GET", "POST"])
@login_required
def passbook():
    # uid = current_user.id
    # trans_data = Transactions.query.filter_by(userId=uid).order_by(
    #     Transactions.date.desc()
    # )
    return render_template("passbook.html")


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    form = profiles()

    if form.validate_on_submit():
        current_user.funds = form.funds.data
        current_user.address = form.address.data
        current_user.mode = form.mode.data
        db.session.commit()
        flash("User Account Updated")
        return redirect(url_for("profile"))

    elif request.method == "GET":
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.funds.data = current_user.funds
        form.address.data = current_user.address
        form.mode.data = current_user.mode

    return render_template("profile.html", proForm=form)


if __name__ == "__main__":
    app.run(debug=True)
