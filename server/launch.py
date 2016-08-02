"""Launches the app and setup folders / load db"""

import os

from server.models import DB_FOLDER
from server.models import EntrySet, Entry, Tag
from server.models import db

__author__ = "Basile Vu <basile.vu@gmail.com>"

if __name__ == "__main__":

    if not os.path.exists(DB_FOLDER):
        os.makedirs(DB_FOLDER)

    db.create_all()

    l1 = EntrySet(name="jp-en")
    e1 = Entry(value="test1", translation="t1", entry_set=l1)
    e2 = Entry(value="test2", translation="t2")
    tag1 = Tag(value="testing1")
    tag2 = Tag(value="testing2")
    e1.tags.append(tag1)
    e1.tags.append(tag2)
    e2.tags.append(tag1)

    print("related to 'testing1': ")

    for e in tag1.entries:
        print(e)
        print(" its tags are the following: ")
        for t in e.tags:
            print("  " + str(t))
