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
    language_left = request.form["language-left"]
    language_right = request.form["language-right"]

    if language_left == "" or language_right == "":
        abort(401)  # FIXME error code for invalid parameter or action

    voclist = Voclist(
        language_left=language_left,
        language_right=language_right
    )

    db.session.add(voclist)
    db.session.commit()

    return redirect(url_for("render_voclist", voclist_id=voclist.id))


@app.route("/voclists/<int:voclist_id>", methods=["UPDATE"])
def update_voclist(voclist_id):
    voclist = Voclist.query.get(voclist_id)
    voclist.language_left = request.get_json()["language-left"]
    voclist.language_right = request.get_json()["language-right"]

    db.session.commit()

    return ""


@app.route("/voclists/<int:voclist_id>", methods=["DELETE"])
def delete_voclist(voclist_id):
    # FIXME on delete cascade
    voclist = Voclist.query.get(voclist_id)
    for e in voclist.entries:
        delete_entry(e.id)

    db.session.delete(voclist)
    db.session.commit()

    return ""


def filter_entries_by_tag(entries, tag_value):
    return entries.join(entry_tag).join(Tag).filter(Tag.value == tag_value)


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
            entries = filter_entries_by_tag(entries, tag).filter(Entry.word.contains(word))
        else:
            entries = voclist.entries.filter(Entry.word.contains(word))
    elif tag != "":
        entries = filter_entries_by_tag(entries, tag)

    return render_template(
        "voclist.html",
        voclist=voclist,
        entries=entries,
        search_word=word,
        search_tag=tag,
        color_generator=ColorGenerator(step=3, cp_max_value=9)
    )


def add_tags(entry, tags):
    """
    Adds tags to an entry, creating them if they don't exist.

    :param entry: the entry to which the tags will be added.
    :param tags: the tags to add. A list of strings.
    """

    for tag_str in tags:
        tag_str = tag_str.strip()
        if tag_str != "":
            tag = Tag.query.filter_by(value=tag_str).first()
            if tag is None:
                tag = Tag(value=tag_str)
                db.session.add(tag)
                db.session.commit()
            if tag not in entry.tags:
                entry.tags.append(tag)


def remove_tags(entry):
    tags = entry.tags

    for tag in tags:
        if filter_entries_by_tag(Entry.query, tag.value).count() <= 1:
            db.session.delete(tag)
            db.session.commit()

    entry.tags.clear()


@app.route("/voclist/<int:voclist_id>", methods=["POST"])
def create_entry(voclist_id):
    word = request.form["word"]
    translation = request.form["translation"]
    tags = request.form["tags"].split(",")

    if word == "" or translation == "":
        abort(401)  # FIXME error code for invalid parameter or action

    entry = Entry(
        word=word,
        translation=translation,
        voclist_id=voclist_id
    )

    add_tags(entry, tags)

    db.session.add(entry)
    db.session.commit()

    return redirect(url_for("render_voclist", voclist_id=voclist_id))


@app.route("/entry/<int:entry_id>", methods=["UPDATE"])
def update_entry(entry_id):
    json = request.get_json()
    entry = Entry.query.get(entry_id)
    tags = json.get("tags", "").split(",")

    entry.word = json["word"]
    entry.translation = json["translation"]

    remove_tags(entry)
    add_tags(entry, tags)

    db.session.commit()

    return ""


@app.route("/entry/<int:entry_id>", methods=["DELETE"])
def delete_entry(entry_id):
    entry = Entry.query.get(entry_id)
    remove_tags(entry)

    db.session.delete(entry)
    db.session.commit()

    # FIXME check if on non-referenced delete exits

    return ""
