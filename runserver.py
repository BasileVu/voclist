from voclist import app, db
from voclist.models import EntrySet, Entry, Tag

__author__ = "Basile Vu <basile.vu@gmail.com>"

if __name__ == "__main__":

    db.create_all()

    # TODO remove when entry set creation ok
    es = EntrySet(name="jp-en")
    tag1 = Tag(value="testing1")
    tag2 = Tag(value="testing2")

    db.session.add(es)
    db.session.add(tag1)
    db.session.add(tag2)
    db.session.commit()

    """
    e1 = Entry(value="test1", translation="t1", entry_set_id=es.id)
    e2 = Entry(value="test2", translation="t2", entry_set_id=es.id)

    db.session.add(e1)
    db.session.add(e2)
    db.session.commit()

    l = EntrySet.query.first()

    tmp = EntrySet.query.filter_by(name="jp-en").first()

    print(tmp)

    print("entries in '%s': " % l.name)
    for e in l.entries:
        print(e)
    """
    app.run()
