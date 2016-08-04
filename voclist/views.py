from flask import render_template

from voclist import app
from voclist.models import EntrySet, Entry, Tag


@app.route("/")
def hello():

    l1 = EntrySet(name="jp-en")
    e1 = Entry(value="test1", translation="t1", entry_set=l1)
    e2 = Entry(value="test2", translation="t2")
    tag1 = Tag(value="testing1")
    tag2 = Tag(value="testing2")
    e1.tags.append(tag1)
    e1.tags.append(tag2)
    e2.tags.append(tag1)

    entries = [e1, e2]

    return render_template("index.html", entryset=l1, entries=entries)
