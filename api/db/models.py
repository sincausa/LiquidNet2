"""
Repository models
"""
import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, event

db = SQLAlchemy()


# I used string representation of uuid as PK to save time


class Request(db.Model):
    """Data model for requests."""
    id = db.Column(
        db.String(36),
        primary_key=True)
    user_id = db.Column(
        db.String(36),
        ForeignKey("users.id"),
        index=True,
        unique=False,
        nullable=False)
    title_id = db.Column(
        db.String,
        ForeignKey("titles.id"),
        index=False,
        unique=False,
        nullable=True)
    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        index=False,
        unique=False,
        nullable=False)


class User(db.Model):
    """Data model for users."""
    __tablename__ = 'users'
    id = db.Column(db.String(36),
                   primary_key=True)
    email = db.Column(db.String(80),
                      index=True,
                      unique=True,
                      nullable=False)
    created = db.Column(db.DateTime,
                        index=False,
                        unique=False,
                        nullable=False)


class Title(db.Model):
    """Data model for titles."""
    __tablename__ = 'titles'
    id = db.Column(db.String(36),
                   primary_key=True)
    title = db.Column(db.String(80),
                      index=True,
                      unique=True,
                      nullable=False)


# pylint: disable=unused-argument
def insert_initial_values(*args, **kwargs):
    """
    Titles table initialization
    :param args:
    :param kwargs:
    :return:
    """
    db.session.add(Title(id=str(uuid.uuid4()), title='title1'))
    db.session.add(Title(id=str(uuid.uuid4()), title='title2'))
    db.session.add(Title(id=str(uuid.uuid4()), title='title3'))
    db.session.commit()


event.listen(Title.__table__, 'after_create', insert_initial_values)
