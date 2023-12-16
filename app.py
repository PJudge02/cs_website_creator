from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    abort,
    session,
    flash,
    jsonify,
)

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required
from flask_login import login_user, logout_user, current_user
import os, sys
from forms import PersonalInformation, LoginForm
from db_setup import setup_web_builder_tables
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
import json

ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg"])

script_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(script_dir)

dbpath = os.path.join(script_dir, "WebsiteCreator.sqlite3")
pepfile = os.path.join(script_dir, "pepper.bin")
UPLOAD_FOLDER = os.path.join(script_dir, "static\\upload_images")

app = Flask(__name__)
app.secret_key = "secret"
bootstrap = Bootstrap(app)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["SECRET_KEY"] = "correcthorsebatterystaple"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["UPLOAD_FOLDER_RELATIVE"] = "\\static\\upload_images"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{dbpath}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Creates db tables, set reinitialize to false if saving data, add data to false if dont need dummy data
# The returns are the classes/tables that can be used to query from or create rows
(
    User,
    Project,
    Experience,
    Website,
    Programming_Language,
) = setup_web_builder_tables(app, db, reinitialize=True, add_data=True)

# Prepare and connect the LoginManager to this app
login_manager = LoginManager()
login_manager.init_app(app)
# function name of the route that has the login form (so it can redirect users)
login_manager.login_view = "get_login"  # type: ignore


# function that takes a user id and
@login_manager.user_loader
def load_user(uid: int) -> User:
    return User.query.get(int(uid))  # type: ignore


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


##############################################################################################################
# Forms
##############################################################################################################
@app.route("/")
def index():
    if current_user.is_authenticated:  # type: ignore
        return redirect(url_for("userHome", userId=current_user.id))  # type: ignore
    return redirect(url_for("get_login"))


@app.get("/login/")
def get_login():
    form = LoginForm()
    return render_template("Login/login.html", form=form)


@app.post("/login/")
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
            next = request.args.get("next")
            if next is None or not next.startswith("/"):
                next = url_for("userHome", userId=user.id)
            return redirect(next)
        else:  # if the user does not exist or the password is incorrect
            # flash an error message and redirect to login form
            flash("Invalid email address or password")
            return redirect(url_for("userHome", userId=1))
    else:  # if the form was invalid
        # flash error messages and redirect to get login form again
        for field, error in form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for("get_login"))


@app.get("/logout/")
def get_logout():
    logout_user()
    return redirect(url_for("get_login"))


@app.get("/register/")
def get_register():
    form = PersonalInformation()
    return render_template("Login/register.html", form=form)


@app.post("/register/")
def post_register():
    form = PersonalInformation()
    if form.validate():
        # check if there is already a user with this email address
        user = User.query.filter_by(email=form.email.data).first()
        # if the email address is free, create a new user and send to login
        if user is None:
            user = User(
                email=form.email.data,
                password=form.password.data,
                firstName=form.firstName.data,
                lastName=form.lastName.data,
                phone=form.phoneNumber.data,
                about=form.about.data,
                college=form.college.data,
                major=form.major.data,
                github=form.github.data,
                linkedIn=form.linkedIn.data,
            )  # type:ignore
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("get_login", userId=1))
        else:  # if the user already exists
            # flash a warning message and redirect to get registration form
            flash("There is already an account with that email address")
            return redirect(url_for("get_register"))
    else:  # if the form was invalid
        # flash error messages and redirect to get registration form again
        for field, error in form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for("get_register"))


##############################################################################################################
# User Specific Pages Editor
##############################################################################################################


# User Home Page
@app.get("/user/<int:userId>/")
@login_required
def userHome(userId: int):
    user: User = User.query.filter_by(id=userId).first_or_404()
    if current_user.id == userId:  # type: ignore
        # render editor for page
        return render_template("UserPages/home.html", user=user)
    else:
        return redirect(url_for("view_home", userId=userId))


@app.get("/user/<int:userId>/projects/")
@login_required
def userProjects(userId: int):
    user: User = User.query.filter_by(id=userId).first_or_404()
    if current_user.id == userId:  # type: ignore
        # render editor for page
        return render_template("UserPages/projects.html", user=user)
    else:
        # redirect to view page
        return redirect(url_for("view_projects", userId=userId))


##############################################################################################################
# User Specific Website View
##############################################################################################################


@app.get("/view/<int:userId>/")
def view_home(userId: int):
    user: User = User.query.filter_by(id=userId).first_or_404()
    return render_template("WebsiteViews/home.html", user=user)


@app.get("/view/<int:userId>/projects/")
def view_projects(userId: int):
    user: User = User.query.filter_by(id=userId).first_or_404()
    return render_template("WebsiteViews/projects.html", user=user)


##############################################################################################################
# Creating/Editing Tables
##############################################################################################################


@app.put("/api/project/")
@app.put("/api/project/<int:projectId>/")
@login_required
def put_Project(projectId: int | None = None):
    info = request.form
    title = info["title"]
    description = info["description"]
    userId = info["userId"]

    image = request.files["image"]
    imagePath = ""

    User.query.get_or_404(userId)

    if int(userId) != current_user.id:  # type: ignore
        return "", 403

    if image and image.filename and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        directory = os.path.join(app.config["UPLOAD_FOLDER"], userId, "project")
        path = os.path.join(directory, filename)
        if not os.path.exists(directory):
            os.makedirs(directory)
        image.save(path)
        imagePath = os.path.join(
            app.config["UPLOAD_FOLDER_RELATIVE"], userId, "project", filename
        )
        db.session.commit()
    else:
        return "", 400

    if projectId:
        # update
        project = Project.query.get(projectId)

        if project:
            project.title = title
            project.description = description
            project.imagePath = imagePath
            db.session.commit()
            return "", 200
        else:
            return "", 404

    # create new
    project_new = Project(
        userId=userId, title=title, description=description, imagePath=imagePath
    )  # type: ignore

    db.session.add(project_new)
    db.session.commit()
    return "", 200


@app.put("/api/about/<int:userId>/")
def put_about(userId: int):
    info = request.get_json()
    description = info["description"]
    college = info["college"]
    major = info["major"]
    phone = info["phone"]

    if userId != current_user.id:  # type: ignore
        return "", 403

    user = User.query.get(userId)

    if not user:
        return "", 404

    user.about = description
    user.college = college
    user.major = major
    user.phone = phone

    db.session.commit()
    return "", 200


@app.put("/api/work/")
@app.put("/api/work/<int:Id>/")
def put_work(Id: int | None = None):
    info = request.get_json()
    userId = info["userId"]
    workplace = info["workplace"]
    description = info["description"]
    title = info["title"]
    startYear = info["startYear"]
    endYear = info["endYear"]

    User.query.get_or_404(userId)

    if userId != current_user.id:  # type: ignore
        return "", 403

    if Id:
        work = Experience.query.get(Id)
        if not work or not work.isWork:
            return "", 404

        work.userId = userId
        work.company = workplace
        work.description = description
        work.position = title
        work.startYear = startYear
        work.endYear = endYear

        db.session.commit()
        return "", 200

    # make new
    work_experience = Experience(
        userId=userId,
        company=workplace,
        description=description,
        position=title,
        startYear=startYear,
        endYear=endYear,
    )  # type: ignore

    db.session.add(work_experience)
    db.session.commit()

    return "", 200


@app.put("/api/language/")
@app.put("/api/language/<int:langId>/")
def put_Language(langId: int | None = None):
    info = request.get_json()
    name = info["name"]
    proficiency = info["proficiency"]
    userId = info["userId"]

    User.query.get_or_404(userId)

    if userId != current_user.id:  # type: ignore
        return "", 403

    if langId:
        # update
        language = Programming_Language.query.get(langId)

        if language:
            language.language = name
            language.proficiency = proficiency

            db.session.commit()
            return "", 200
        else:
            return "", 404

    # create new
    lang_new = Programming_Language(
        userId=userId,
        language=name,
        proficiency=proficiency,
    )  # type: ignore

    db.session.add(lang_new)
    db.session.commit()
    return "", 200


@app.put("/api/v1/language/ordering/")
def put_home_layout():
    info = request.get_json()
    userId = info["userId"]
    languageIds = info["languageIds"]
    languageOrdering = ",".join(languageIds)

    ordering = Website.query.filter_by(userId=userId).first()

    print(ordering)

    if not ordering:
        ordering = Website(userId=userId, languageOrdering=languageOrdering)  # type: ignore

        db.session.add(ordering)
    else:
        ordering.languageOrdering = languageOrdering

    db.session.commit()
    return "", 200


@app.put("/api/v1/work/ordering/")
def put_project_layout():
    info = request.get_json()
    userId = info["userId"]
    workIds = info["workIds"]
    workOrdering = ",".join(workIds)

    ordering = Website.query.filter_by(userId=userId).first()

    if not ordering:
        ordering = Website(userId=userId, workOrdering=workOrdering)  # type: ignore

        db.session.add(ordering)
    else:
        ordering.workOrdering = workOrdering

    db.session.commit()
    return "", 200


@app.put("/api/v1/image/profile/")
def put_image_upload():
    info = request.form
    userId = info["userId"]
    user = User.query.get_or_404(userId)
    image = request.files["image"]

    if image and image.filename and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        directory = os.path.join(app.config["UPLOAD_FOLDER"], userId)
        path = os.path.join(directory, filename)
        if not os.path.exists(directory):
            os.makedirs(directory)
        image.save(path)
        user.imagePath = os.path.join(
            app.config["UPLOAD_FOLDER_RELATIVE"], userId, filename
        )
        db.session.commit()
    else:
        return "", 400
    return "", 200


##############################################################################################################
# Getting data dynamically
##############################################################################################################


@app.get("/api/v1/ordering/<int:userId>/")
def get_work_ordering(userId: int):
    ordering: Website = Website.query.filter_by(userId=userId).first_or_404()

    work_ordering = None
    lang_ordering = None

    if ordering.workOrdering:
        work_ordering = ordering.workOrdering.split(",")

    if ordering.languageOrdering:
        lang_ordering = ordering.languageOrdering.split(",")

    return jsonify({"work": work_ordering, "lang": lang_ordering})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
