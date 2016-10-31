import os

from app import db
from flask.ext.sqlalchemy import SQLAlchemy


class User(db.Models):
    """ User Model """
    __tablename__ = "users"
    id = Column(db.Integer, primary_key=True)
    username = Column(db.String(50), index=True)
    password = Column(db.String(30), index=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password


class BucketList(db.Models):
    """ BucketList Model """
    __tablename__ = 'bucketlists'
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(50), unique=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp())
    created_by = Column(db.Integer, db.ForeignKey('user.id'))
    # user = db.relationship("User", backref='', lazy='')

    def __init__(self, name, created_by):
        self.name = name
        self.created_by = created_by


class BucketListItem(db.Models):
    """ Bucketlist Item model """
    __tablename__ = 'items'
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(50), unique=True)
    bucketlist_id = Column(db.Integer, db.ForeignKey('bucketlist.id'))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp())
    is_done = Column(db.Boolean, default=False)

    def __init__(self, name, bucketlist_id):
        self.name = name
        self.bucketlist_id = bucketlist_id
