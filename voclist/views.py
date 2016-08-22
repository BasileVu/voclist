from flask import abort, redirect, render_template, request, url_for

from voclist import app, db
from voclist.models import Voclist, Entry, entry_tag, Tag
from voclist.utils.color_generator import ColorGenerator

__author__ = "Basile Vu <basile.vu@gmail.com>"


@app.route("/")
def render_index():
    return render_template("index.html", voclists=Voclist.query.all())


@app.route("/voclists/", methods=["POST"])
def create_voclist():
    language_left = request.get_json()["language-left"]
    language_right = request.get_json()["language-right"]

    if language_left == "" or language_right == "":
        abort(401)  # FIXME error code for invalid parameter or action

    voclist = Voclist(
        language_left=language_left,
        language_right=language_right
    )

    db.session.add(voclist)
    db.session.commit()

    return redirect(url_for("render_voclist", voclist_id=voclist.id))


@app.route("/voclists/<int:voclist_id>", methods=["PUT"])
def update_voclist(voclist_id):
    voclist = Voclist.query.get(voclist_id)
    voclist.language_left = request.get_json()["language-left"]
    voclist.language_right = request.get_json()["language-right"]

    db.session.commit()

    return ""


@app.route("/voclists/<int:voclist_id>", methods=["DELETE"])
def delete_voclist(voclist_id):
    voclist = Voclist.query.get(voclist_id)
    for e in voclist.entries:
        e.remove_tags()

    db.session.delete(voclist)
    db.session.commit()

    return ""


@app.route("/voclist/<int:voclist_id>", methods=["GET"])
def render_voclist(voclist_id):
    voclist = Voclist.query.get(voclist_id)

    if voclist is None:
        abort(404)

    entries = voclist.entries

    word = request.args.get("word", "").strip()
    tag = request.args.get("tag", "").strip()

    if word != "":
        if tag != "":
            entries = Tag.get_from_val(tag).entries
        entries = entries.filter(Entry.word.contains(word))
    elif tag != "":
        entries = Tag.get_from_val(tag).entries

    return render_template(
        "voclist.html",
        voclist=voclist,
        entries=entries.order_by(Entry.word),
        search_word=word,
        search_tag=tag,
        color_generator=ColorGenerator(step=3, cp_max_value=9)
    )


@app.route("/voclist/<int:voclist_id>", methods=["POST"])
def create_entry(voclist_id):
    word = request.get_json()["word"]
    translation = request.get_json()["translation"]
    tags = request.get_json()["tags"].split(",")

    if word == "" or translation == "":
        abort(401)  # FIXME error code for invalid parameter or action

    entry = Entry(
        word=word,
        translation=translation,
        voclist_id=voclist_id
    )

    entry.add_tags(tags)

    db.session.add(entry)
    db.session.commit()

    return ""


@app.route("/entry/<int:entry_id>", methods=["PUT"])
def update_entry(entry_id):
    json = request.get_json()
    entry = Entry.query.get(entry_id)
    tags = json.get("tags", "").split(",")

    entry.word = json["word"]
    entry.translation = json["translation"]

    entry.remove_tags()
    entry.add_tags(tags)

    db.session.commit()

    return ""


@app.route("/entry/<int:entry_id>", methods=["DELETE"])
def delete_entry(entry_id):
    entry = Entry.query.get(entry_id)
    entry.remove_tags()

    db.session.delete(entry)
    db.session.commit()

    return ""


@app.route("/voclist/<int:voclist_id>/tags", methods=["GET"])
def render_tags(voclist_id):
    voclist = Voclist.query.get(voclist_id)

    return render_template(
        "tags.html",
        voclist=voclist,
        tags=Tag.query.join(entry_tag).join(Entry).filter_by(voclist_id=voclist_id).order_by(Tag.value)
    )


@app.route("/tags/<string:old_value>", methods=["PUT"])
def update_tag(old_value):
    tag = Tag.get_from_val(old_value)
    tag.value = request.get_json()["value"].strip()
    db.session.commit()
    print(Tag.query.get(tag.id).value)
    return ""
