from flask_testing import TestCase

from voclist import *
from voclist.models import *
from voclist.tests.test_db import add_entry, add_tag, add_voclist

__author__ = "Basile Vu <basile.vu@gmail.com>"


class IndexViewTest(TestCase):

    def create_app(self):
        setup_app("config/test.cfg")
        db.create_all()
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_breadcrumbs(self):
        r = self.client.get("/")
        self.assert200(r)
        assert '<ol class="breadcrumb">' in str(r.data)
        assert '<li class="active">Voclists</li>' in str(r.data)

    def test_no_voclist(self):
        r = self.client.get("/")
        self.assert200(r)
        assert '<p>No voclist found yet. Please create one.</p>' in str(r.data)

    def test_existing_voclist(self):
        db.session.add(Voclist(language_left="a", language_right="b"))
        db.session.commit()

        r = self.client.get("/")
        self.assert200(r)
        assert '<option voclist-id="1">a - b</option>' in str(r.data)


class VoclistViewTest(TestCase):

    def create_app(self):
        setup_app("config/test.cfg")
        db.create_all()
        return app

    def setUp(self):
        db.create_all()
        self.v = add_voclist("a", "b")

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_voclist_empty(self):
        r = self.client.get("/voclist/1")
        self.assert200(r)

        assert '<tbody></tbody>' in str(r.data).replace(" ", "").replace("\\n", "")

    def test_voclist_one_entry(self):
        t = add_tag("test")
        add_entry("c", "d", self.v, t)

        r = self.client.get("/voclist/1")
        self.assert200(r)

        stripped = str(r.data).replace(" ", "")

        assert '<td>c</td>' in stripped
        assert '<td>d</td>' in stripped
        assert 'test</span>' in stripped
        assert 'Edit</button>' in stripped
        assert 'Delete</button>' in stripped

    def test_voclist_tag_filter(self):
        t1 = add_tag("test1")
        t2 = add_tag("test2")

        e1 = add_entry("c1", "d1", self.v, t1)
        e2 = add_entry("c2", "d2", self.v, t2)
        e3 = add_entry("c3", "d3", self.v, t2)

