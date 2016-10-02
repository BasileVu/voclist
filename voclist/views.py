"""Regroups all the views and their routes."""

from flask import abort, redirect, render_template, request, url_for, jsonify

from voclist import app, db
from voclist.models import Voclist, Entry, entry_tag, Tag
from voclist.utils.color_generator import ColorGenerator

__author__ = "Basile Vu <basile.vu@gmail.com>"


@app.route("/")
def render_index():
    """
    Renders the index page.

    :return: The index page.
    """
    return render_template("index.html", voclists=Voclist.query.all())


@app.route("/voclists/", methods=["POST"])
def create_voclist():
    """
    Creates a voclist and renders the page related to this voclist.

    In the json received, the left and right languages must exist with keys "language-left" and "language-right."

    :return: The page of the newly created voclist.
    """
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
    """
    Updates the name of the languages of a given voclist.

    In the json sent with the request, the left and right languages must exist with keys "language-left" and "language-right."

    :param voclist_id: The id of the voclist to update. Must be passed in the request url.
    """
    voclist = Voclist.query.get(voclist_id)
    voclist.language_left = request.get_json()["language-left"]
    voclist.language_right = request.get_json()["language-right"]

    db.session.commit()

    return ""


@app.route("/voclists/<int:voclist_id>", methods=["DELETE"])
def delete_voclist(voclist_id):
    """
    Deletes a given voclist and its entries.

    :param voclist_id: The id of the voclist to delete. Must be passed in the request url.
    """
    voclist = Voclist.query.get(voclist_id)
    for e in voclist.entries:
        e.remove_tags()

    db.session.delete(voclist)
    db.session.commit()

    return ""


@app.route("/voclist/<int:voclist_id>", methods=["GET"])
def render_voclist(voclist_id):
    """
    Prepares the page related to a given voclist and given entry filters and returns it.

    In the arguments of the request, some entry filters can be passed as arguments. These are the following:
     - word, showing entries whose "word" attribute contains the value,
     - tag, showing entries which have a tag having whose "value" attribute contains the value.

     For example:
      - /voclist/1?word=foo : shows all the entries whose word contains word "foo".
      - /voclist/1?tag=bar : shows all the entries whose tags contain "bar".
      - /voclist/1?word=foo&tag=bar : shows all the entries whose word contains word "foo" and tags contain "bar".

    :param voclist_id: The id of the voclist to render.
    :return: The page of the selected voclist.
    """
    voclist = Voclist.query.get(voclist_id)

    if voclist is None:
        abort(404)

    entries = voclist.entries

    word = request.args.get("word", "").strip()
    tag_value = request.args.get("tag", "").strip()

    if word != "":
        entries = entries.filter(Entry.word.contains(word))

    if tag_value != "":
        entries = entries.join(entry_tag).join(Tag).filter(Tag.value.contains(tag_value))

    return render_template(
        "voclist.html",
        voclist=voclist,
        entries=entries.order_by(Entry.word),
        search_word=word,
        search_tag=tag_value,
        color_generator=ColorGenerator(step=3, cp_max_value=9)
    )


@app.route("/voclist/<int:voclist_id>", methods=["POST"])
def create_entry(voclist_id):
    """
    Creates an entry with the given values in the given voclist.

    In the json sent with the request, the word, its translation and the optional tags for the entry must exist
    with keys "word", "translation" and "tags".
    The tags should be in a string of the form "t1, t2, ...".

    :param voclist_id: The voclist in which the entry will be added.
    """
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
    """
    Updates en entry with the given values.

    In the json sent with the request, the word, its translation and the optional tags for the entry must exist
    with keys "word", "translation" and "tags".
    The tags should be in a string of the form "t1, t2, ...".

    :param entry_id: The id of the entry to update.
    """
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
    """
    Deletes a given entry.

    :param entry_id: The id of the entry to delete.
    """
    entry = Entry.query.get(entry_id)
    entry.remove_tags()

    db.session.delete(entry)
    db.session.commit()

    return ""


@app.route("/voclist/<int:voclist_id>/tags", methods=["GET"])
def render_tags(voclist_id):
    """
    Renders the given voclist's page.

    :param voclist_id: The id of the voclist to render.
    :return: The voclist page.
    """
    voclist = Voclist.query.get(voclist_id)

    return render_template(
        "tags.html",
        voclist=voclist,
        tags=Tag.query.join(entry_tag).join(Entry).filter_by(voclist_id=voclist_id).order_by(Tag.value)
    )


@app.route("/tags/<string:old_value>", methods=["PUT"])
def update_tag(old_value):
    """
    Updates the value of a given tag.

    :param old_value: The old value of the tag.
    :return: A json containing the new value.
    """
    tag = Tag.get_from_val(old_value)
    value = request.get_json()["value"].strip()
    tag_existing = Tag.query.filter_by(value=value).first()

    if tag_existing is not None:
        for e in tag.entries:
            e.tags.append(tag_existing)
        db.session.delete(tag)
    else:
        tag.value = value

    db.session.commit()

    return jsonify(value=value)
