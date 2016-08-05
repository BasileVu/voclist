from voclist import db

__author__ = "Basile Vu <basile.vu@gmail.com>"

entry_tag = db.Table("entry_tag",
                     db.Column("Entry_id", db.Integer, db.ForeignKey("entries.id")),
                     db.Column("Tag_id", db.Integer, db.ForeignKey("tags.id"))
                     )


class Voclist(db.Model):
    __tablename__ = "voclists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    entries = db.relationship("Entry", backref="voclists", lazy="dynamic")

    def __repr__(self):
        return "<EntrySet(name='%s')>" % self.name


class Entry(db.Model):
    __tablename__ = "entries"

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String, nullable=False)
    translation = db.Column(db.String, nullable=False)

    voclist_id = db.Column(db.Integer, db.ForeignKey("voclists.id"))
    tags = db.relationship("Tag", secondary=entry_tag, backref=db.backref("entries", lazy="dynamic"))

    def __repr__(self):
        return "<Entry(word='%s', translation='%s', voclist_id='%s')>" % (self.word, self.translation, self.voclist_id)


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String, nullable=False)

    def __repr__(self):
        return "<Tag(value='%s')>" % self.value
