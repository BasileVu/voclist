from flask import redirect, render_template, request, url_for

from voclist import app, db
from voclist.models import Voclist, Entry, Tag


@app.route("/")
def index():
    return render_template("index.html", voclists=Voclist.query.all())


@app.route("/voclists/", methods=["POST"])
def create_voclist():
    voclist = Voclist(
        language_left = request.form["language-left"],
        language_right = request.form["language-right"]
    )

    print(voclist)

    db.session.add(voclist)
    db.session.commit()

    return redirect("/entries/%s/" % str(voclist.id))  # FIXME url_for


@app.route("/entries/<int:voclist_id>/", methods=["GET"])
def entries(voclist_id):
    voclist = Voclist.query.get(voclist_id)
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

    return redirect("/entries/1")  # FIXME url_for + id
