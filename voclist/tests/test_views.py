from flask_testing import TestCase

from voclist import *
from voclist.models import *
from voclist.tests.test_db import add_entry, add_tag, add_voclist

__author__ = "Basile Vu <basile.vu@gmail.com>"


class IndexViewTests(TestCase):
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


class VoclistViewTests(TestCase):
    def create_app(self):
        setup_app("config/test.cfg")
        db.create_all()
        return app

    def setUp(self):
        db.create_all()
        self.v = add_voclist("a", "b")
        self.v_uri = "/voclist/%d" % self.v.id

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @staticmethod
    def has_no_entries(response):
        return '<tbody></tbody>' in str(response.data).replace(" ", "").replace("\\n", "")

    def test_breadcrumbs(self):
        r = self.client.get(self.v_uri)
        self.assert200(r)
        data_str = str(r.data)

        assert '<ol class="breadcrumb">' in data_str
        assert '<li class="active">a - b</li>' in data_str

    def test_voclist_empty(self):
        r = self.client.get(self.v_uri)
        self.assert200(r)

        assert self.has_no_entries(r)

    def test_voclist_one_entry(self):
        t = add_tag("test")
        add_entry("c", "d", self.v, t)

        r = self.client.get(self.v_uri)
        self.assert200(r)

        stripped = str(r.data).replace(" ", "")

        assert '<td>c</td>' in stripped
        assert '<td>d</td>' in stripped
        assert 'test</span>' in stripped
        assert 'Edit</button>' in stripped
        assert 'Delete</button>' in stripped

    def test_voclist_word_filters(self):
        add_entry("c1", "d1", self.v)
        add_entry("c2", "d2", self.v)
        add_entry("c3", "d3", self.v)

        r = self.client.get(self.v_uri + "?word=d")
        self.assert200(r)
        assert self.has_no_entries(r)

        r = self.client.get(self.v_uri + "?word=c")
        self.assert200(r)
        data_str = str(r.data)

        assert "c1" in data_str
        assert "c2" in data_str
        assert "c3" in data_str

        r = self.client.get(self.v_uri + "?word=c1")
        self.assert200(r)
        data_str = str(r.data)

        assert "c1" in data_str
        assert "c2" not in data_str
        assert "c3" not in data_str

    def test_voclist_tag_filters(self):
        t1 = add_tag("test1")
        t2 = add_tag("test2")

        add_entry("c1", "d1", self.v, t1)
        add_entry("c2", "d2", self.v, t2)
        add_entry("c3", "d3", self.v, t2)

        r = self.client.get(self.v_uri + "?tag=d")
        self.assert200(r)
        assert self.has_no_entries(r)

        r = self.client.get(self.v_uri + "?tag=test")
        self.assert200(r)
        data_str = str(r.data)

        assert "c1" in data_str
        assert "c2" in data_str
        assert "c3" in data_str

        r = self.client.get(self.v_uri + "?tag=test2")
        self.assert200(r)
        data_str = str(r.data)

        assert "c1" not in data_str
        assert "c2" in data_str
        assert "c3" in data_str

    def test_filters_together(self):
        t1 = add_tag("test1")
        t2 = add_tag("test2")

        add_entry("c1", "d1", self.v, t1)
        add_entry("c2", "d2", self.v, t2)
        add_entry("c3", "d3", self.v, t2)

        r = self.client.get(self.v_uri + "?word=c&tag=test")
        self.assert200(r)
        data_str = str(r.data)

        assert "c1" in data_str
        assert "c2" in data_str
        assert "c3" in data_str

        r = self.client.get(self.v_uri + "?word=c2&tag=test2")
        self.assert200(r)
        data_str = str(r.data)

        assert "c1" not in data_str
        assert "c2" in data_str
        assert "c3" not in data_str


class TagViewTests(TestCase):
    def create_app(self):
        setup_app("config/test.cfg")
        db.create_all()
        return app

    def setUp(self):
        db.create_all()
        self.v = add_voclist("a", "b")
        self.voclist_uri = "/voclist/%d" % self.v.id
        self.tags_uri = self.voclist_uri + "/tags/"

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_breadcrumbs(self):
        r = self.client.get(self.tags_uri)
        self.assert200(r)
        data_str = str(r.data)

        assert '<ol class="breadcrumb">' in data_str
        assert '<li class="active">Tags</li>' in data_str

    def test_no_tag_existing(self):
        r = self.client.get(self.tags_uri)
        self.assert200(r)
        assert '<p>No tag found.</p>' in str(r.data)

    def test_tags_existing(self):
        t = add_tag("test1")
        add_entry("c", "d", self.v, t)

        r = self.client.get(self.tags_uri)
        self.assert200(r)

        assert '<a class="col-md-4" href="%s?tag=%s">%s</a>' % (self.voclist_uri, t.value, t.value) in str(r.data)
