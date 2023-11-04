from flask_wtf import FlaskForm
from wtforms.fields import (
    SubmitField,
    StringField,
    IntegerField,
    SelectField,
    EmailField,
    PasswordField,
)
from wtforms.validators import InputRequired, Length, Email, EqualTo


class PersonalInformation(FlaskForm):
    firstName = StringField("First name?", validators=[InputRequired()])
    lastName = StringField("Last name?", validators=[InputRequired()])
    phoneNumber = StringField("First name?")
    email = EmailField("Email")
    homeAdress = StringField("Home Address")
    about = StringField("About you", validators=[InputRequired()])
    submit = SubmitField("Submit")


class MajorRelated(FlaskForm):
    college = StringField("College/University?", validators=[InputRequired()])
    major = StringField("Major?", validators=[InputRequired()])
    concentration = StringField("Major Concentration?", validators=[InputRequired()])
    minors = StringField("Minors?", validators=[InputRequired()])
    classes = StringField("Important Classes?", validators=[InputRequired()])
    tools = StringField("Tools/Platforms?", validators=[InputRequired()])
    languages = StringField("Laungages?", validators=[InputRequired()])
    submit = SubmitField("Submit")


class Projcts(FlaskForm):
    github = StringField("Github URL?", validators=[InputRequired()])
    project1Title = StringField("Project Title #1?", validators=[InputRequired()])
    project1GitRepo = StringField(
        "Project #1 Github Repo?", validators=[InputRequired()]
    )
    project1Discription = StringField("Discription:", validators=[InputRequired()])
    submit = SubmitField("Submit")


class WorkExperience(FlaskForm):
    company1 = StringField("Company?", validators=[InputRequired()])
    position1 = StringField("Position?", validators=[InputRequired()])
    typeOfWork1 = StringField("Type of Work?", validators=[InputRequired()])
    work1Discription = StringField("Discription:", validators=[InputRequired()])
    submit = SubmitField("Submit")


class VolunteerWork(FlaskForm):
    organization1 = StringField("Organization?", validators=[InputRequired()])
    position1 = StringField("Position?", validators=[InputRequired()])
    typeOfWork1 = StringField("Type of Work?", validators=[InputRequired()])
    discription1 = StringField("Discription:", validators=[InputRequired()])
    submit = SubmitField("Submit")


class Extracurricular(FlaskForm):
    activity1 = StringField("Activity/Club?", validators=[InputRequired()])
    leadership1 = StringField("Leadership Position:", validators=[InputRequired()])
    submit = SubmitField("Submit")

class RegisterForm(FlaskForm):
    email = EmailField("Email: ", validators=[InputRequired(), Email()])
    password = PasswordField("Password: ", 
        validators=[InputRequired(), Length(min=8, max=256)])
    confirm_password = PasswordField("Confirm Password: ", 
        validators=[EqualTo('password')])
    submit = SubmitField("Register")

# define our own FlaskForm subclass for our form
class LoginForm(FlaskForm):
    email = EmailField("Email: ", validators=[InputRequired(), Email()])
    password = PasswordField("Password: ", 
        validators=[InputRequired(), Length(min=8, max=256)])
    submit = SubmitField("Login")