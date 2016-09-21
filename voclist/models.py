"""
Contains the models used in the DB.
"""

from voclist import db

__author__ = "Basile Vu <basile.vu@gmail.com>"

entry_tag = db.Table(
    "entry_tag",
    db.Column("Entry_id", db.Integer, db.ForeignKey("entries.id"), primary_key=True),
    db.Column("Tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True)
)


class Voclist(db.Model):
    """Represents a vocbulary list containing entries."""

    __tablename__ = "voclists"

    id = db.Column(db.Integer, primary_key=True)
    language_left = db.Column(db.String, nullable=False)
    language_right = db.Column(db.String, nullable=False)

    entries = db.relationship("Entry", backref="voclists", lazy="dynamic", cascade="delete")

    def __repr__(self):
        return "<EntrySet(language_left='%s', language_right='%s')>" % (self.language_left, self.language_right)

    def __str__(self):
        return "%s - %s" % (self.language_left, self.language_right)


class Entry(db.Model):
    """Represents an entry of a voclist."""

    __tablename__ = "entries"

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String, nullable=False)
    translation = db.Column(db.String, nullable=False)

    voclist_id = db.Column(db.Integer, db.ForeignKey("voclists.id"))
    tags = db.relationship("Tag", secondary=entry_tag, backref=db.backref("entries", lazy="dynamic"))

    def __repr__(self):
        return "<Entry(word='%s', translation='%s', voclist_id='%s')>" % (self.word, self.translation, self.voclist_id)

    def remove_tags(self):
        """Removes the tags related to this entry if they aren't being referred by another entry."""

        for tag in self.tags:
            if tag.entries.count() <= 1:
                db.session.delete(tag)
                db.session.commit()

        self.tags.clear()

    def add_tags(self, tags):
        """
        Adds tags to this entry, creating them if they don't exist.

        :param tags: the tags to add. A list of strings.
        """

        for tag_str in tags:
            tag_str = tag_str.strip()
            if tag_str != "":
                tag = Tag.query.filter_by(value=tag_str).first()
                if tag is None:
                    tag = Tag(value=tag_str)
                    db.session.add(tag)
                    db.session.commit()
                if tag not in self.tags:
                    self.tags.append(tag)


class Tag(db.Model):
    """Represents a tag linked to some entries."""
    
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return "<Tag(value='%s')>" % self.value

    @staticmethod
    def get_from_val(value):
        return Tag.query.filter_by(value=value).first()
