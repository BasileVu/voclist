from flask_testing import TestCase

from voclist import *
from voclist.models import *

__author__ = "Basile Vu <basile.vu@gmail.com>"


class ViewsTest(TestCase):

    def create_app(self):
        setup_app("config/test.cfg")
        db.create_all()
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_root_breadcrumbs(self):
        r = self.client.get("/")
        self.assert200(r)
        assert '<ol class="breadcrumb">' in str(r.data)
        assert '<li class="active">Voclists</li>' in str(r.data)

    def test_empty_voclist(self):
        r = self.client.get("/")
        self.assert200(r)
        assert '<p>No voclist found yet. Please create one.</p>' in str(r.data)

    def test_existing_voclist(self):
        db.session.add(Voclist(language_left="a", language_right="b"))
        db.session.commit()

        r = self.client.get("/")
        self.assert200(r)
        print(r.data)
        assert '<option voclist-id="1">a - b</option>' in str(r.data)
