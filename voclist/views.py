from flask import render_template
from flask import request

from voclist import app, db
from voclist.models import Voclist, Entry, Tag


@app.route("/")
def index():
    return render_template("index.html", voclists=Voclist.query.all())


@app.route("/voclists/", methods=["POST"])
def create_voclist():
    voclist = Voclist(
        name="%s-%s" % (request.form["lang-left"], request.form["lang-right"])
    )

    print(voclist)

    db.session.add(voclist)
    db.session.commit()

    return "created" + voclist.name


@app.route("/entries/", methods=["GET"])
def entries():
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
