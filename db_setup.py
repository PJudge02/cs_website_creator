from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from hashing_examples import UpdatedHasher
import os, sys
from dataclasses import dataclass
from flask_login import UserMixin


def setup_web_builder_tables(
    app: Flask, db: SQLAlchemy, reinitialize=False, add_data=True
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
        imagePath = db.Column(db.Unicode, nullable=True)
        projects = db.relationship("Project", backref="user")
        experiences = db.relationship("Experience", backref="user")
        website = db.relationship("Website", backref="user")
        languages = db.relationship("Programming_Language", backref="user")

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
        imagePath = db.Column(db.Unicode, nullable=False)
        link = db.Column(db.Unicode, nullable=True)
        def __str__(self):
            return f"{self.userId=}\n{self.title=}\n{self.description=}"

        def __repr__(self) -> str:
            return str(self)

    class Experience(db.Model):
        __tablename__ = "Experiences"
        id = db.Column(db.Integer, primary_key=True)
        userId = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable=False)
        company = db.Column(db.Unicode, nullable=False)
        description = db.Column(db.Unicode, nullable=False)
        position = db.Column(db.Unicode, nullable=False)
        startYear = db.Column(db.Unicode, nullable=True)
        endYear = db.Column(db.Unicode, nullable=True)

        def __str__(self) -> str:
            return f"{self.userId=}\n{self.company=}\n{self.description=}\n{self.position=}"

        def __repr__(self) -> str:
            return str(self)

    class Website(db.Model):
        __tablename__ = "Websites"
        id = db.Column(db.Integer, primary_key=True)
        userId = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable=False)
        languageOrdering = db.Column(db.Unicode, nullable=True)
        workOrdering = db.Column(db.Unicode, nullable=True)

        def to_json(self):
            work_ordering = None
            lang_ordering = None

            if self.workOrdering:
                work_ordering = self.workOrdering.split(",")

            if self.languageOrdering:
                lang_ordering = self.languageOrdering.split(",")

            return {"work": work_ordering, "lang": lang_ordering}
        

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

            user: User = User(
                password="testingpassword",
                firstName="John",
                lastName="Doe",
                email="DoeJohn@gsail.com",
                phone="111-111-1111",
                major="Computer Science",
                college="Grove City",
                about="This is my cool about description",
                github = "https://github.com/",
                linkedIn="https://linkedin.com/",
            )  # type: ignore

            project: Project = Project(
                userId=1,
                title="My First Project",
                description="Little Project I made",
                imagePath="/static/images/pencil.png",
                link = "https://www.google.com/"
            )  # type: ignore

            work_experience1: Experience = Experience(
                userId=1,
                company="Grove City",
                description="Made my.gcc.edu worse",
                position="Software Developer",
                startYear= "2023",
                endYear="present"
            ) # type: ignore

            work_experience2: Experience = Experience(
                userId=1,
                company="NASA",
                description="Used imperial instead of metric",
                position="IT Intern",
                startYear= "2023",
                endYear= "2023",
            ) # type: ignore

            work_experience3: Experience = Experience(
                userId=1,
                company="Apple",
                description="Remade the same phone again",
                position="CEO",
                startYear= "2021",
                endYear= "2023",
            ) # type: ignore

            programming_language:Programming_Language = Programming_Language(
                userId=1,
                language = "Java",
                proficiency="Advanced",
            ) # type: ignore
            
            db.session.add_all((user, project, work_experience1, work_experience2, work_experience3, programming_language))
            db.session.commit()

        return (
            User,
            Project,
            Experience,
            Website,
            Programming_Language,
        )
