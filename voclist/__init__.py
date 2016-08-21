from flask import Flask
from flask_sqlalchemy import SQLAlchemy

__author__ = "Basile Vu <basile.vu@gmail.com>"

app = Flask(__name__)
db = SQLAlchemy()


def setup_app(config_file):
    app.config.from_pyfile(config_file)
    db.init_app(app)
    app.app_context().push()

import voclist.views
