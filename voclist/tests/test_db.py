from flask_testing import TestCase

from voclist import *
from voclist.views import *
from voclist.models import *

__author__ = "Basile Vu <basile.vu@gmail.com>"


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
        v = Voclist(language_left="a", language_right="b")
        db.session.add(v)
        db.session.commit()

        self.assertEqual(Voclist.query.count(), 1)

        v_get = Voclist.query.get(1)
        self.assertEqual(v_get, v)
        self.assertEqual(v_get.language_left, "a")
        self.assertEqual(v_get.language_right, "b")

    def test_tag_creation(self):
        t = Tag(value="test")
        db.session.add(t)
        db.session.commit()

        self.assertEqual(Tag.query.count(), 1)

        t_get = Tag.query.get(1)
        self.assertEqual(t_get, t)
        self.assertEqual(Tag.query.get(1).value, "test")

    def test_entry_creation(self):
        v = Voclist(language_left="a", language_right="b")
        db.session.add(v)
        db.session.commit()

        e = Entry(word="word", translation="translation", voclist_id=Voclist.query.get(1).id)
        db.session.add(e)
        db.session.commit()

        self.assertEqual(Entry.query.count(), 1)

        e_get = Entry.query.get(1)
        self.assertEqual(e_get, e)

        self.assertEqual(e_get.word, "word")
        self.assertEqual(e_get.translation, "translation")
        self.assertEqual(e_get.voclist_id, v.id)
