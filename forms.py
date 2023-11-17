from flask_wtf import FlaskForm
from wtforms.fields import (
    SubmitField,
    StringField,
    EmailField,
    PasswordField,
)
from wtforms.validators import InputRequired, Length, EqualTo, Email


class PersonalInformation(FlaskForm):
    title = "Register"
    email = EmailField("Email: ", validators=[InputRequired(), Email()])
    password = PasswordField(
        "Password: ", validators=[InputRequired(), Length(min=8, max=256)]
    )
    confirm_password = PasswordField(
        "Confirm Password: ", validators=[EqualTo("password")]
    )
    firstName = StringField("First Name:", validators=[InputRequired()])
    lastName = StringField("Last Name:", validators=[InputRequired()])
    phoneNumber = StringField("Phone:")
    about = StringField("Personal Description:", validators=[InputRequired()])
    college = StringField("College/University:")
    major = StringField("Major:")
    github = StringField("Github url:")
    linkedIn = StringField("LinkedIn url:")
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    title = "Login"
    email = StringField("Username", validators=[InputRequired()])
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=8, max=255)]
    )
    submit = SubmitField("Login")
