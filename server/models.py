from sqlalchemy import ForeignKey, Column, Table
from sqlalchemy import Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

__author__ = "Basile Vu <basile.vu@gmail.com>"

Base = declarative_base()

entry_tag = Table("entry_tag", Base.metadata,
                  Column("Entry_id", Integer, ForeignKey("entries.id")),
                  Column("Tag_id", Integer, ForeignKey("tags.id"))
                 )

class Language(Base):
    __tablename__ = "languages"
    id = Column(Integer, primary_key=True)
    value = Column(String, nullable=False)


class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True)
    value = Column(String, nullable=False)
    translation = Column(String, nullable=False)

    language_id = Column(Integer, ForeignKey('languages.id'))
    tags = relationship("Tag", secondary=entry_tag, backref="entries")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    value = Column(String, nullable=False)
