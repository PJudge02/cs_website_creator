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
#ethan made a comment here
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
    LoginForm
)
from db_setup import setup_web_builder_tables
from hashing_examples import UpdatedHasher
from flask_bootstrap import Bootstrap

script_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(script_dir)

dbpath = os.path.join(script_dir, "WebsiteCreator.sqlite3")
pepfile = os.path.join(script_dir, "pepper.bin")

# with open(pepfile, "rb") as fin:
#     pepper_key = fin.read()

# pwd_hasher = UpdatedHasher(pepper_key)

app = Flask(__name__)
app.secret_key = 'secret'
bootstrap = Bootstrap(app)
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
@app.route('/')
def index():
    return redirect(url_for('step', step=1))


@app.route('/step/<int:step>/', methods=['GET', 'POST'])
def step(step):
    forms = {
        1: PersonalInformation(),
        2: MajorRelated(),
        3: Projcts(),
        4: WorkExperience(),
        5: VolunteerWork(),
        6: Extracurricular()
    }

    form = forms.get(step, 1)

    if request.method == 'POST':
        if form.validate_on_submit():
            # Save form data to session
            session['step{}'.format(step)] = form.data
            if step < len(forms):
                # Redirect to next step
                return redirect(url_for('step', step=step+1))
            else:
                # Redirect to finish
                return redirect(url_for('finish'))

    # If form data for this step is already in the session, populate the form with it
    if 'step{}'.format(step) in session:
        form.process(data=session['step{}'.format(step)])

    content = {
        'progress': int(step / len(forms) * 100),
        'step': step, 
        'form': form,
    }
    return render_template('step.html', **content)


@app.route('/finish/')
def finish():
    data = {}
    for key in session.keys():
        if key.startswith('step'):
            data.update(session[key])
    session.clear()
    return render_template('finish.html', data=data)

@app.get('/login/')
def get_login():
    form = LoginForm()
    return render_template('login.html', form=form)

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
    if current_user.id == userId: # type: ignore
        # render editor for page
        return render_template("UserPages/home.html", user=user)
    else:
        return redirect(url_for("view_home", userId=userId))

@app.get("/user/<int:userId>/about/")
@login_required
def userAbout(userId: int):
    user: User = User.query.filter_by(id=userId).first_or_404()
    if current_user.id == userId: # type: ignore
        # render editor for page
        return render_template("UserPages/about.html", user=user)
    else:
        return redirect(url_for("view_about", userId=userId))

@app.get("/user/<int:userId>/education/")
@login_required
def userEducation(userId: int):
    user: User = User.query.filter_by(id=userId).first_or_404()
    if current_user.id == userId: # type: ignore
        # render editor for page
        return render_template("UserPages/education.html", user=user)
    else:
        #redirect to view page
        return redirect(url_for("view_education", userId=userId))

@app.get("/user/<int:userId>/projects/")
@login_required
def userProjects(userId: int):
    user: User = User.query.filter_by(id=userId).first_or_404()
    if current_user.id == userId: # type: ignore
        # render editor for page
        return render_template("UserPages/projects.html", user=user)
    else:
        #redirect to view page
        return redirect(url_for("view_projects", userId=userId))

@app.get("/user/<int:userId>/work/")
@login_required
def userWork(userId: int):
    user: User = User.query.filter_by(id=userId).first_or_404()
    if current_user.id == userId: # type: ignore
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

