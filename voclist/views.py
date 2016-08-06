from flask import abort,    redirect, render_template, request, url_for

from voclist import app, db
from voclist.models import Voclist, Entry, Tag


@app.route("/")
def index():
    return render_template("index.html", voclists=Voclist.query.all())


@app.route("/voclists/", methods=["POST"])
def create_voclist():
    language_left = request.form["language-left"]
    language_right = request.form["language-right"]

    if language_left == "" or language_right == "":
        abort(401) # FIXME error code for invalid parameter or action

    voclist = Voclist(
        language_left=language_left ,
        language_right=language_right
    )

    db.session.add(voclist)
    db.session.commit()

    return redirect("/entries/%d/" % voclist.id)  # FIXME url_for


@app.route("/entries/<int:voclist_id>/", methods=["GET"])
def entries(voclist_id):
    voclist = Voclist.query.get(voclist_id)

    if voclist is None:
        abort(404)

    return render_template("entries.html", voclist=voclist)


@app.route("/entries/", methods=["POST"])
def create_entry():

    word = request.form["word"]
    translation = request.form["translation"]
    voclist_id = 1  # FIXME

    if word == "" or translation == "":
        abort(401) # FIXME error code for invalid parameter or action

    entry = Entry(
        word=word,
        translation=translation,
        voclist_id=voclist_id
    )

    db.session.add(entry)
    db.session.commit()

    return redirect("/entries/%d/" % voclist_id)  # FIXME url_for
