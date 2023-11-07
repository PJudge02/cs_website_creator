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
    RegisterForm,
    LoginForm
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

# Prepare and connect the LoginManager to this app
login_manager = LoginManager()
login_manager.init_app(app)
# function name of the route that has the login form (so it can redirect users)
login_manager.login_view = 'get_login' # type: ignore
# function that takes a user id and 
@login_manager.user_loader
def load_user(uid: int) -> User:
    return User.query.get(int(uid)) # type: ignore

##############################################################################################################
# Forms
##############################################################################################################

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

##############################################################################################################
# Site-Wide Pages
##############################################################################################################


@app.get("/")
def index():
    return render_template("landingPage.html")

@app.get('/register/')
def get_register():
    form = RegisterForm()
    return render_template('Login/register.html', form=form)

@app.post('/register/')
def post_register():
    form = RegisterForm()
    if form.validate():
        # check if there is already a user with this email address
        user = User.query.filter_by(email=form.email.data).first()
        # if the email address is free, create a new user and send to login
        if user is None:
            user = User(email=form.email.data, password=form.password.data) # type:ignore
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('getPersonal'))
        else: # if the user already exists
            # flash a warning message and redirect to get registration form
            flash('There is already an account with that email address')
            return redirect(url_for('get_register'))
    else: # if the form was invalid
        # flash error messages and redirect to get registration form again
        for field, error in form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('get_register'))

@app.get('/login/')
def get_login():
    form = LoginForm()
    return render_template("Login/login.html", form=form)

@app.post('/login/')
def post_login():
    form = LoginForm()
    if form.validate():
        # try to get the user associated with this email address
        user = User.query.filter_by(email=form.email.data).first()
        # if this user exists and the password matches
        if user is not None and user.verify_password(form.password.data):
            # log this user in through the login_manager
            login_user(user)
            # redirect the user to the page they wanted or the home page
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('index')
            return redirect(next)
        else: # if the user does not exist or the password is incorrect
            # flash an error message and redirect to login form
            flash('Invalid email address or password')
            return redirect(url_for('get_login'))
    else: # if the form was invalid
        # flash error messages and redirect to get login form again
        for field, error in form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('get_login'))


##############################################################################################################
# User Specific Pages Editor
##############################################################################################################

#User Home Page
@app.get("/user/<int:userId>/")
@login_required
def userHome(userId: int):
    user: User = User.query.filter_by(id=userId).first_or_404()
    if current_user.id == userId:
        # render editor for page
        return render_template("UserPages/home.html", user=user)
    else:
        return redirect(url_for("view_home", userId=userId))

@app.get("/user/<int:userId>/about/")
@login_required
def userAbout(userId: int):
    user: User = User.query.filter_by(id=userId).first_or_404()
    if current_user.id == userId:
        # render editor for page
        return render_template("UserPages/about.html", user=user)
    else:
        return redirect(url_for("view_about", userId=userId))

@app.get("/user/<int:userId>/education/")
@login_required
def userEducation(userId: int):
    user: User = User.query.filter_by(id=userId).first_or_404()
    if current_user.id == userId:
        # render editor for page
        return render_template("UserPages/education.html", user=user)
    else:
        #redirect to view page
        return redirect(url_for("view_education", userId=userId))

@app.get("/user/<int:userId>/projects/")
@login_required
def userProjects(userId: int):
    user: User = User.query.filter_by(id=userId).first_or_404()
    if current_user.id == userId:
        # render editor for page
        return render_template("UserPages/projects.html", user=user)
    else:
        #redirect to view page
        return redirect(url_for("view_projects", userId=userId))

@app.get("/user/<int:userId>/work/")
@login_required
def userWork(userId: int):
    user: User = User.query.filter_by(id=userId).first_or_404()
    if current_user.id == userId:
        # render editor for page
        return render_template("UserPages/work.html", user=user)
    else:
        #redirect to view page
        return redirect(url_for("view_work", userId=userId))


##############################################################################################################
# User Specific Website View
##############################################################################################################

@app.get("/view/<int:userId>/")
def view_home(userId:int):
    user: User = User.query.filter_by(id=userId).first_or_404()
    return render_template("WebsiteViews/home.html", user=user)

@app.get("/view/<int:userId>/about/")
def view_about(userId:int):
    user: User = User.query.filter_by(id=userId).first_or_404()
    return render_template("WebsiteViews/about.html", user=user)

@app.get("/view/<int:userId>/education/")
def view_education(userId:int):
    user: User = User.query.filter_by(id=userId).first_or_404()
    return render_template("WebsiteViews/education.html", user=user)

@app.get("/view/<int:userId>/projects/")
def view_projects(userId:int):
    user: User = User.query.filter_by(id=userId).first_or_404()
    return render_template("WebsiteViews/projects.html", user=user)

@app.get("/view/<int:userId>/work/")
def view_work(userId:int):
    user: User = User.query.filter_by(id=userId).first_or_404()
    return render_template("WebsiteViews/work.html", user=user)