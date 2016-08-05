from flask import render_template
from flask import request

from voclist import app, db
from voclist.models import Voclist, Entry, Tag


@app.route("/")
def index():
    voclist = Voclist.query.filter_by(name="jp-en").first()  # FIXME
    print(voclist)
    return render_template("entries.html", voclist=voclist)


@app.route("/entries/", methods=["POST"])
def create_entry():
    entry = Entry(
        word=request.form["word"],
        translation=request.form["translation"],
        voclist_id=1  # FIXME
    )

    #entry.tags.append(Tag(value="tag"))  # FIXME

    print(entry)

    db.session.add(entry)
    db.session.commit()

    return "created"
