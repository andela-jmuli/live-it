import os

from app import db
from flask_sqlalchemy import SQLAlchemy


class User(db.Model):
    """ User Model """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True)
    password = db.Column(db.String(30), index=True)


class BucketList(db.Model):
    """ BucketList Model """
    __tablename__ = 'bucketlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship("User", backref=db.backref("users", lazy="dynamic"))

    items = db.relationship("BucketListItem", backref=db.backref("bucketlist"))


class BucketListItem(db.Model):
    """ Bucketlist Item model """
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.Text)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp())
    is_done = db.Column(db.Boolean, default=False)

    user = db.relationship("User", backref=db.backref("items", lazy="dynamic"))

