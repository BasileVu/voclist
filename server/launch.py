"""Launches the app and setup folders / load db"""

import os

from server.models import *
from server.session import DB_FOLDER, engine, Session

__author__ = "Basile Vu <basile.vu@gmail.com>"

if __name__ == "__main__":

    if not os.path.exists(DB_FOLDER):
        os.makedirs(DB_FOLDER)

    Base.metadata.create_all(engine, checkfirst=True)

    session = Session()
    e1 = Entry(value="test1", translation="t1")
    e2 = Entry(value="test2", translation="t2")
    tag1 = Tag(value="testing1")
    tag2 = Tag(value="testing2")
    e1.tags.append(tag1)
    e1.tags.append(tag2)
    e2.tags.append(tag1)

    print("related to 'testing1': ")

    for e in tag1.entries:
        print(e.value)
        print(" its tags are the following: ")
        for t in e.tags:
            print("  " + t.value)
