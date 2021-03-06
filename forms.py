from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    BooleanField,
    DateTimeField,
    RadioField,
    SelectField,
    PasswordField,
    TextField,
    TextAreaField,
    SubmitField,
    IntegerField,
    FileField,
    ValidationError,
    DateField,
    DecimalField,
)
from wtforms.validators import DataRequired, Email, EqualTo, Required
from flask_wtf.file import FileField, FileAllowed
from models import Users


class addFunds(FlaskForm):
    amount = IntegerField("amount", validators=[DataRequired()])
    submit1 = SubmitField("Add Funds")


class WithdrawFunds(FlaskForm):
    amount = IntegerField("amount", validators=[DataRequired()])
    submit2 = SubmitField("Withdraw")


class profiles(FlaskForm):
    name = StringField("Name")
    email = StringField("Email")
    funds = IntegerField("Funds")
    address = StringField("Address")
    # mode = BooleanField('Mode')
    mode = RadioField(
        "Mode", choices=[(0, "Manual"), (1, "Automatic")], default=0, coerce=int
    )
    submit = SubmitField("Update")


class loginForm(FlaskForm):
    email1 = StringField(
        "Email",
        validators=[DataRequired(), Email(message=("Not a valid email address!"))],
    )
    password1 = PasswordField("Password", validators=[DataRequired()])
    submit1 = SubmitField("Log In")


class registrationForm(FlaskForm):
    username2 = StringField("UserName", validators=[DataRequired()])
    email2 = StringField(
        "Email",
        validators=[DataRequired(), Email(message=("Not a valid email address!"))],
    )
    password2 = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("pass_confirm", message="Passwords must match"),
        ],
    )
    pass_confirm = PasswordField("Confirm Password", validators=[DataRequired()])
    submit2 = SubmitField("Register")

    def check_email(self, field):
        if Users.query.filter_by(email=field.data).first():
            raise ValidationError("Your email has been registered already!")
