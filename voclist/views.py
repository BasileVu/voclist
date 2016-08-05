from flask import render_template
from flask import request

from voclist import app, db
from voclist.models import EntrySet, Entry, Tag


@app.route("/")
def index():
    entry_set = EntrySet.query.filter_by(name="jp-en").first()  # FIXME
    print(entry_set)
    return render_template("entries.html", entry_set=entry_set)


@app.route("/entries/", methods=["POST"])
def create_entry():
    entry = Entry(
        value=request.form["value"],
        translation=request.form["translation"],
        entry_set_id=1  # FIXME
    )

    #entry.tags.append(Tag(value="tag"))  # FIXME

    print(entry)

    db.session.add(entry)
    db.session.commit()

    return "created"
