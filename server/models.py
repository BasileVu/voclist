from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

__author__ = "Basile Vu <basile.vu@gmail.com>"

Base = declarative_base()


class Language(Base):
    __tablename__ = "languages"
    id = Column(Integer, primary_key=True)
    value = Column(String)


class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True)
    value = Column(String)


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    value = Column(String)
