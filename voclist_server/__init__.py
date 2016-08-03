import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

__author__ = "Basile Vu <basile.vu@gmail.com>"

DB_FOLDER = "db"
DB_NAME = "db.db"

if not os.path.exists(DB_FOLDER):
    os.makedirs(DB_FOLDER)

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s/%s" % (DB_FOLDER, DB_NAME)

db = SQLAlchemy(app)
db.create_all()

from . import views
