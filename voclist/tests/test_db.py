from flask_testing import TestCase

from voclist import *
from voclist.views import *
from voclist.models import *

__author__ = "Basile Vu <basile.vu@gmail.com>"


def add_voclist():
    v = Voclist(language_left="a", language_right="b")
    db.session.add(v)
    db.session.commit()
    return v


def add_tag():
    t = Tag(value="test")
    db.session.add(t)
    db.session.commit()
    return t


def add_entry(voclist, tag=None):
    e = Entry(word="word", translation="translation", voclist_id=voclist.id)
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
        v = add_voclist()

        self.assertEqual(Voclist.query.count(), 1)

        v_get = Voclist.query.get(1)
        self.assertEqual(v_get, v)
        self.assertEqual(v_get.language_left, "a")
        self.assertEqual(v_get.language_right, "b")

    def test_tag_creation(self):
        t = add_tag()

        self.assertEqual(Tag.query.count(), 1)

        t_get = Tag.query.get(1)
        self.assertEqual(t_get, t)
        self.assertEqual(Tag.query.get(1).value, "test")

    def test_entry_creation(self):
        v = add_voclist()
        e = add_entry(v)

        self.assertEqual(Entry.query.count(), 1)

        e_get = Entry.query.get(1)
        self.assertEqual(e_get, e)

        self.assertEqual(e_get.word, "word")
        self.assertEqual(e_get.translation, "translation")
        self.assertEqual(e_get.voclist_id, v.id)

    def test_entry_with_tags_creation(self):
        t = add_tag()
        v = add_voclist()
        e = add_entry(v, t)

        self.assertEqual(Entry.query.count(), 1)

        e_get = Entry.query.get(1)
        self.assertEqual(e_get, e)

        self.assertEqual(e_get.word, "word")
        self.assertEqual(e_get.translation, "translation")
        self.assertEqual(len(e_get.tags), 1)
        self.assertEqual(e_get.tags[0], t)
        self.assertEqual(e_get.voclist_id, v.id)

    def test_tag_deletion(self):
        t = add_tag()
        v = add_voclist()
        e = add_entry(v, t)

        db.session.delete(t)
        db.session.commit()

        self.assertEqual(len(e.tags), 0)

    def test_entry_deletion(self):
        t = add_tag()
        v = add_voclist()
        e = add_entry(v, t)
        e2 = add_entry(v, t)

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
        t = add_tag()
        v = add_voclist()
        add_entry(v, t)
        add_entry(v, t)

        for entry in v.entries:
            entry.remove_tags()

        db.session.delete(v)
        db.session.commit()

        self.assertEqual(Entry.query.count(), 0)
        self.assertEqual(Tag.query.count(), 0)
