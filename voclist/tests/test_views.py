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

    def test_empty_voclist(self):
        r = self.client.get("/")
        self.assert200(r)
        assert "<p>No voclist found yet. Please create one.</p>" in str(r.data)
