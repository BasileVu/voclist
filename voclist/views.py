from flask import abort,    redirect, render_template, request, url_for

from voclist import app, db
from voclist.models import Voclist, Entry, Tag


@app.route("/")
def render_index():
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

    return redirect("/voclist/%d/" % voclist.id)  # FIXME url_for


@app.route("/voclist/<int:voclist_id>/", methods=["GET"])
def render_voclist(voclist_id):
    voclist = Voclist.query.get(voclist_id)

    if voclist is None:
        abort(404)

    return render_template("voclist.html", voclist=voclist)


@app.route("/voclist/", methods=["POST"])
def create_entry():
    word = request.form["word"]
    translation = request.form["translation"]
    voclist_id = request.form["voclist-id"]

    if word == "" or translation == "":
        abort(401) # FIXME error code for invalid parameter or action

    entry = Entry(
        word=word,
        translation=translation,
        voclist_id=voclist_id
    )

    db.session.add(entry)
    db.session.commit()

    return redirect("/voclist/%s/" % voclist_id)  # FIXME url_for
