from flask import Flask, request, render_template, redirect, url_for, abort, session, flash
from flask_sqlalchemy import SQLAlchemy
import os, sys

script_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(script_dir)

scriptdir = os.path.abspath(os.path.dirname(__file__))
dbpath = os.path.join(scriptdir, 'WebsiteCreator.sqlite3')

# Configure the Flask App
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{dbpath}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'correcthorsebatterystaple'

db = SQLAlchemy(app)