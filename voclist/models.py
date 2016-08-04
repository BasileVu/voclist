from voclist import db

__author__ = "Basile Vu <basile.vu@gmail.com>"

entry_tag = db.Table("entry_tag",
                     db.Column("Entry_id", db.Integer, db.ForeignKey("entries.id")),
                     db.Column("Tag_id", db.Integer, db.ForeignKey("tags.id"))
                     )


class EntrySet(db.Model):
    __tablename__ = "entry_sets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    entries = db.relationship("Entry", backref="entry_sets", lazy="dynamic")

    def __repr__(self):
        return "<EntrySet(name='%s')>" % self.name


class Entry(db.Model):
    __tablename__ = "entries"

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String, nullable=False)
    translation = db.Column(db.String, nullable=False)

    entry_set_id = db.Column(db.Integer, db.ForeignKey("entry_sets.id"))
    tags = db.relationship("Tag", secondary=entry_tag, backref=db.backref("entries", lazy="dynamic"))

    def __repr__(self):
        return "<Entry(value='%s', translation='%s', entry_set_id='%s')>" % (self.value, self.translation, self.entry_set_id)


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String, nullable=False)

    def __repr__(self):
        return "<Tag(value='%s')>" % self.value
