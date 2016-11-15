from app import db
from config.config import config_settings
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import (TimedJSONWebSignatureSerializer as
                          Serializer, BadSignature, SignatureExpired)
from werkzeug.security import generate_password_hash, check_password_hash

s = Serializer(config_settings['SECRET_KEY'], expires_in=10000)

class User(db.Model):
    """ User Model """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=10000):
        return s.dumps({'id': self.id}).decode('utf-8')


class BucketList(db.Model):
    """ BucketList Model """
    __tablename__ = 'bucketlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False)
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
    name = db.Column(db.String(50), unique=False)
    description = db.Column(db.Text)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp())
    is_done = db.Column(db.Boolean, default=False)

    user = db.relationship("User", backref=db.backref("items", lazy="dynamic"))
