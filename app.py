from flask import Flask, request, render_template, redirect, url_for, abort, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_required
from flask_login import login_user, logout_user, current_user
import os, sys

from hashing_examples import UpdatedHasher

script_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(script_dir)

scriptdir = os.path.abspath(os.path.dirname(__file__))
dbpath = os.path.join(scriptdir, 'WebsiteCreator.sqlite3')
pepfile = os.path.join(script_dir, "pepper.bin")

with open(pepfile, 'rb') as fin:
    pepper_key = fin.read()

pwd_hasher = UpdatedHasher(pepper_key)

# Configure the Flask App
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{dbpath}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'correcthorsebatterystaple'

db = SQLAlchemy(app)