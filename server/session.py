from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

__author__ = "Basile Vu <basile.vu@gmail.com>"

DB_FOLDER = "db"
DB_NAME = "database.db"

engine = create_engine("sqlite:///" + DB_FOLDER + "/" + DB_NAME)

Session = sessionmaker(bind=engine)
