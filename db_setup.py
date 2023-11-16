from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from hashing_examples import UpdatedHasher
import os, sys
from flask_login import UserMixin


def setup_web_builder_tables(
    app: Flask, db: SQLAlchemy, reinitialize=False, add_data=False
):
    class User(UserMixin, db.Model):
        __tablename__ = "Users"
        id = db.Column(db.Integer, primary_key=True)
        password_hash = db.Column(db.LargeBinary)
        firstName = db.Column(db.Unicode, nullable=False)
        lastName = db.Column(db.Unicode, nullable=False)
        email = db.Column(db.Unicode, nullable=False, unique=True)
        phone = db.Column(db.Unicode, nullable=False, unique=True)
        major = db.Column(db.Unicode, nullable=True)  # maybe enum?
        college = db.Column(db.Unicode, nullable=True)  # maybe enum?
        about = db.Column(db.Unicode, nullable=True)
        github = db.Column(db.Unicode, nullable=True)
        linkedIn = db.Column(db.Unicode, nullable=True)
        projects = db.relationship("Project", backref="user")
        clubs = db.relationship("Club", backref="user")
        experiences = db.relationship("Experience", backref="user")
        website = db.relationship("Website", backref="user")

        def __str__(self):
            return f"{self.firstName=} {self.lastName=}\n{self.email=} | {self.phone=}\n{self.major=}, {self.college=}\n{self.about=}\n{self.github=} {self.linkedIn=}"
        
        def __repr__(self):
            return str(self)

        @property
        def password(self):
            raise AttributeError("password is a write-only attribute")
        @password.setter
        def password(self, pwd: str) -> None:
            self.password_hash = pwd_hasher.hash(pwd)
    
        # add a verify_password convenience method
        def verify_password(self, pwd: str) -> bool:
            return pwd_hasher.check(pwd, self.password_hash)

    class Project(db.Model):
        __tablename__ = "Projects"
        id = db.Column(db.Integer, primary_key=True)
        userId = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable=False)
        title = db.Column(db.Unicode, nullable=False)
        description = db.Column(db.Unicode, nullable=False)
        repositoryLink = db.Column(db.Unicode, nullable=True)
        images = db.relationship("Project_Image", backref="project")

        def __str__(self):
            return f"{self.userId=}\n{self.title=}\n{self.description=}\n{self.repositoryLink=}"
        
        def __repr__(self) -> str:
            return str(self)

    class Project_Image(db.Model):
        __tablename__ = "Project_Images"
        id = db.Column(db.Integer, primary_key=True)
        projectId = db.Column(db.Integer, db.ForeignKey("Projects.id"), nullable=False)
        imageLink = db.Column(db.Unicode, nullable=False)

    class Club(db.Model):
        __tablename__ = "Clubs"
        id = db.Column(db.Integer, primary_key=True)
        userId = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable=False)
        title = db.Column(db.Unicode, nullable=False)
        description = db.Column(db.Unicode, nullable=False)
        position = db.Column(db.Unicode, nullable=True)

        def __str__(self) -> str:
            return f"{self.userId=}\n{self.title=}\n{self.description=}\n{self.position=}"
        
        def __repr__(self) -> str:
            return str(self)

    class Experience(db.Model):
        __tablename__ = "Experiences"
        id = db.Column(db.Integer, primary_key=True)
        userId = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable=False)
        company = db.Column(db.Unicode, nullable=False)
        description = db.Column(db.Unicode, nullable=False)
        position = db.Column(db.Unicode, nullable=False)
        isWork = db.Column(db.Boolean, nullable=False)

        def __str__(self) -> str:
            return f"{self.userId=}\n{self.company=}\n{self.description=}\n{self.position=}"
        
        def __repr__(self) -> str:
            return str(self)

    class Website(db.Model):
        __tablename__ = "Websites"
        id = db.Column(db.Integer, primary_key=True)
        userId = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable=False)
        websiteLink = db.Column(db.Unicode, unique=True)
        homePage = db.Column(db.Unicode, nullable=False)
        aboutPage = db.Column(db.Unicode, nullable=True)
        workPage = db.Column(db.Unicode, nullable=True)
        projectsPage = db.Column(db.Unicode, nullable=True)
        educationPage = db.Column(db.Unicode, nullable=True)

    class Programming_Language(db.Model):
        __tablename__ = "Programming_Language"
        id = db.Column(db.Integer, primary_key=True)
        userId = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable=False)
        language = db.Column(db.Unicode, nullable=False)
        proficiency = db.Column(db.Unicode, nullable=False)

        def __str__(self) -> str:
            return f"{self.userId=}\n{self.language=}\n{self.proficiency=}"
        
        def __repr__(self) -> str:
            return str(self)
    

    with app.app_context():
        if reinitialize:
            db.drop_all()
            db.create_all()

        if add_data:
            script_dir = os.path.abspath(os.path.dirname(__file__))
            pepfile = os.path.join(script_dir, "pepper.bin")
            with open(pepfile, "rb") as fin:
                pepper_key = fin.read()

            pwd_hasher = UpdatedHasher(pepper_key)

            user: User = User(password = "testingpassword",
                              firstName = "John",
                              lastName = "Doe",
                              email = "DoeJoh @gsail.com",
                              phone = "111-111-1111",
                              major = "Computer Science",
                              college = "Grove City",
                              about = "This is my cool about description") #type: ignore
            
            db.session.add(user)
            db.session.commit()

        return (User, Project, Project_Image, Club, Experience, Website)
