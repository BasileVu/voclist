import sqlalchemy.exc

from flask_testing import TestCase

from voclist import *
from voclist.models import *

__author__ = "Basile Vu <basile.vu@gmail.com>"


def add_voclist(language_left, language_right):
    v = Voclist(language_left=language_left, language_right=language_right)
    db.session.add(v)
    db.session.commit()
    return v


def add_tag(value):
    t = Tag(value=value)
    db.session.add(t)
    db.session.commit()
    return t


def add_entry(word, translation, _voclist, tag=None):
    e = Entry(word=word, translation=translation, voclist_id=_voclist.id)
    if tag is not None:
        e.tags.append(tag)
    db.session.add(e)
    db.session.commit()
    return e


class DBTest(TestCase):

    def create_app(self):
        setup_app("config/test.cfg")
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_voclist_creation(self):
        v = add_voclist("a", "b")

        self.assertEqual(Voclist.query.count(), 1)

        v_get = Voclist.query.get(1)
        self.assertEqual(v_get, v)
        self.assertEqual(v_get.language_left, "a")
        self.assertEqual(v_get.language_right, "b")

    def test_tag_creation(self):
        t = add_tag("test")

        self.assertEqual(Tag.query.count(), 1)

        t_get = Tag.query.get(1)
        self.assertEqual(t_get, t)
        self.assertEqual(Tag.query.get(1).value, "test")

    def test_tag_value_uniqueness(self):
        add_tag("t")
        self.assertRaises(sqlalchemy.exc.IntegrityError, add_tag, "t")
        db.session.rollback()

        t2 = add_tag("t2")
        t2.value = "t"
        self.assertRaises(sqlalchemy.exc.IntegrityError, db.session.commit)

    def test_entry_creation(self):
        v = add_voclist("a", "b")
        e = add_entry("w", "t", v)

        self.assertEqual(Entry.query.count(), 1)

        e_get = Entry.query.get(1)
        self.assertEqual(e_get, e)

        self.assertEqual(e_get.word, "w")
        self.assertEqual(e_get.translation, "t")
        self.assertEqual(e_get.voclist_id, v.id)

    def test_entry_with_tags_creation(self):
        t = add_tag("t")
        v = add_voclist("a", "b")
        e = add_entry("w", "t", v, t)

        self.assertEqual(Entry.query.count(), 1)

        e_get = Entry.query.get(1)
        self.assertEqual(e_get, e)

        self.assertEqual(e_get.word, "w")
        self.assertEqual(e_get.translation, "t")
        self.assertEqual(len(e_get.tags), 1)
        self.assertEqual(e_get.tags[0], t)
        self.assertEqual(e_get.voclist_id, v.id)

    def test_tag_deletion(self):
        t = add_tag("t")
        v = add_voclist("a", "b")
        e = add_entry("w", "t", v, t)

        db.session.delete(t)
        db.session.commit()

        self.assertEqual(len(e.tags), 0)

    def test_entry_deletion(self):
        t = add_tag("t")
        v = add_voclist("a", "b")
        e = add_entry("w", "t", v, t)
        e2 = add_entry("w2", "t2", v, t)

        e.remove_tags()
        db.session.delete(e)
        db.session.commit()
        self.assertEqual(Tag.query.count(), 1)

        e2.remove_tags()
        db.session.delete(e2)
        db.session.commit()

        self.assertEqual(Tag.query.count(), 0)

        db.session.commit()

    def test_voclist_deletion(self):
        t = add_tag("t")
        v = add_voclist("a", "b")
        add_entry("w", "t", v, t)
        add_entry("w2", "t2", v, t)

        for entry in v.entries:
            entry.remove_tags()

        db.session.delete(v)
        db.session.commit()

        self.assertEqual(Entry.query.count(), 0)
        self.assertEqual(Tag.query.count(), 0)
