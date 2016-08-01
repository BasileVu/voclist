"""Launches the app and setup folders / load db"""

import os

from server.models import Base, Word
from server.session import DB_FOLDER, engine, Session

__author__ = "Basile Vu <basile.vu@gmail.com>"

if __name__ == "__main__":

    if not os.path.exists(DB_FOLDER):
        os.makedirs(DB_FOLDER)

    Base.metadata.create_all(engine, checkfirst=True)

    session = Session()
    w = Word(value="test")
    session.add(w)
    session.commit()

