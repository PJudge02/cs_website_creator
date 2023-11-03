from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    abort,
    session,
    flash,
)
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_required
from flask_login import login_user, logout_user, current_user
import os, sys
from forms import (
    PersonalInformation,
    MajorRelated,
    Projcts,
    WorkExperience,
    VolunteerWork,
    Extracurricular,
)
from db_setup import setup_web_builder_tables
from hashing_examples import UpdatedHasher

script_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(script_dir)

dbpath = os.path.join(script_dir, "WebsiteCreator.sqlite3")
pepfile = os.path.join(script_dir, "pepper.bin")

with open(pepfile, "rb") as fin:
    pepper_key = fin.read()

pwd_hasher = UpdatedHasher(pepper_key)

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["SECRET_KEY"] = "correcthorsebatterystaple"

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{dbpath}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Creates db tables, set reinitialize to false if saving data, add data to false if dont need dummy data
User, Project, Project_Image, Club, Experience, Website = setup_web_builder_tables(
    app, db, reinitialize=True, add_data=True
)


@app.get("/")
def getLandingPage():
    return render_template("landingPage.html")


@app.get("/personal-information-form/")
def getPersonal():
    form = PersonalInformation()
    return render_template("personalInformationForm.html", form=form)


@app.post("/personal-information-form/")
def postPersonal():
    form = PersonalInformation()
    if form.validate():
        return redirect(url_for("getMajor"))
    for field, msg in form.errors.items():
        flash(f"{field}: {msg}")
    return redirect(url_for("getPersonal"))


@app.get("/major-form/")
def getMajor():
    form = MajorRelated()
    return render_template("majorForm.html", form=form)


@app.post("/major-form/")
def postMajor():
    form = MajorRelated()
    if form.validate():
        return redirect(url_for("getProject"))
    for field, msg in form.errors.items():
        flash(f"{field}: {msg}")
    return redirect(url_for("getMajor"))


@app.get("/project-form/")
def getProject():
    form = Projcts()
    return render_template("projectForm.html", form=form)


@app.post("/project-form/")
def postProject():
    form = Projcts()
    if form.validate():
        return redirect(url_for("getWorkExperience"))
    for field, msg in form.errors.items():
        flash(f"{field}: {msg}")
    return redirect(url_for("getProject"))


@app.get("/work-experience-form/")
def getWorkExperience():
    form = WorkExperience()
    return render_template("workExperienceForm.html", form=form)


@app.post("/work-experience-form/")
def postWorkExperience():
    form = Projcts()
    if form.validate():
        return redirect(url_for("getVolunteerWork"))
    for field, msg in form.errors.items():
        flash(f"{field}: {msg}")
    return redirect(url_for("getWorkExperience"))


@app.get("/volunteer-work-form/")
def getVolunteerWork():
    form = VolunteerWork()
    return render_template("volunteerWorkForm.html", form=form)


@app.post("/volunteer-work-form/")
def postVolunteerWork():
    form = Projcts()
    if form.validate():
        return redirect(url_for("getExtracurricular"))
    for field, msg in form.errors.items():
        flash(f"{field}: {msg}")
    return redirect(url_for("getVolunteerWork"))


@app.get("/extracurricular-form/")
def getExtracurricular():
    form = Extracurricular()
    return render_template("volunteerWorkForm.html", form=form)


@app.post("/extracurricular-form/")
def postExtracurricular():
    form = Projcts()
    if form.validate():
        return redirect(url_for("getExtracurricular"))
    for field, msg in form.errors.items():
        flash(f"{field}: {msg}")
    return redirect(url_for("getExtracurricular"))


@app.get("/actual-website/")
def actualWebsite():
    return render_template("actualWebsite.html")
