from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def setup_web_builder_tables(
    app: Flask, db: SQLAlchemy, reinitialize=False, add_data=False
):
    class User(db.Model):
        __tablename__ = "Users"
        id = db.Column(db.Integer, primary_key=True)
        firstName = db.Column(db.Unicode, nullable=False)
        lastName = db.Column(db.Unicode, nullable=False)
        email = db.Column(db.Unicode, nullable=False, unique=True)
        phone = db.Column(db.Unicode, nullable=False, unique=True)
        major = db.Column(db.Unicode, nullable=True)  # maybe enum?
        college = db.Column(db.Unicode, nullable=True)  # maybe enum?
        about = db.Column(db.Unicode, nullable=True)
        github = db.Column(db.Unicode, nullable=True)
        projects = db.relationship("Project", backref='user')
        clubs = db.relationship("Club", backref='user')
        experiences = db.relationship("Experience", backref="user")
        website = db.relationship("Website", backref='user')

    class Project(db.Model):
        __tablename__ = "Projects"
        id = db.Column(db.Integer, primary_key=True)
        userId = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
        title = db.Column(db.Unicode, nullable=False)
        description = db.Column(db.Unicode, nullable=False)
        repositoryLink = db.Column(db.Unicode, nullable=True)
        images = db.relationship('Poject_Image', backref='project')

    class Project_Image(db.Model):
        __tablename__ = "Project_Images"
        id = db.Column(db.Integer, primary_key=True)
        projectId = db.Column(db.Integer, db.ForeignKey('Projects.id'), nullable=False)
        imageLink = db.Column(db.Unicode, nullable=False)

    class Club(db.Model):
        __tablename__ = "Clubs"
        id = db.Column(db.Integer, primary_key=True)
        userId = db.Column(db.Integer, db.ForeginKey('Users.id'), nullable=False)
        title = db.Column(db.Unicode, nullable=False)
        description = db.Column(db.Unicode, nullable=False)
        position = db.Column(db.Unicode, nullable=True)

    class Experience(db.Model):
        __tablename__ = "Experiences"
        id = db.Column(db.Integer, primary_key=True)
        userId = db.Column(db.Integer, db.ForeginKey('Users.id'), nullable=False)
        company = db.Column(db.Unicode, nullable=False)
        description = db.Column(db.Unicode, nullable=False)
        position = db.Column(db.Unicode, nullable=False)
        isWork = db.Column(db.Boolean, nullable=False)

    class Website(db.Model):
        __tablename__ = "Websites"
        id = db.Column(db.Integer, primary_key=True)
        userId = db.Column(db.Integer, db.ForeginKey('Users.id'), nullable=False)
        websiteLink = db.Column(db.Unicode, unique=True)
        homePage = db.Column(db.Unicode, nullable=False)
        aboutPage = db.Column(db.Unicode, nullable=True)
        workPage = db.Column(db.Unicode, nullable=True)
        projectsPage = db.Column(db.Unicode, nullable=True)
        educationPage = db.Column(db.Unicode, nullable=True)

    with app.app_context():
        if reinitialize:
            db.drop_all()
            db.create_all()

        if add_data:
            # TODO : dummy data
            pass

        return (User, Project, Project_Image, Club, Experience, Website)
