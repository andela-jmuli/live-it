from functools import wraps
from flask import g, jsonify, request, make_response
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from flask_restful import Resource
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from werkzeug.security import generate_password_hash, check_password_hash

from app import app
from config.config import config_settings
from models import User, BucketList, BucketListItem, s

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth('Token')
multiauth = MultiAuth(basic_auth, token_auth)

@basic_auth.verify_password
def verify_password(username, password):
    user_det = User.query.filter_by(username=username).first()
    if user_det and check_password_hash(user_det.password, password):
        return True
    return False

@token_auth.verify_token
def verify_token(token):
    try:
        data = s.loads(token)
    except SignatureExpired:
        return 'Expired!'
    except BadSignature:
        return 'Bad signature'
    user = User.query.get(data['id'])
    if user:
        g.user = user
        return True
    return False

@app.errorhandler(403)
def unauthorized(message=None):
    return make_response(jsonify(
        {'Error': 'Invalid token given, '
         'Login again to gain access'}), 403)

@app.errorhandler(404)
def unauthorized(message=None):
     return make_response(jsonify(
         {'Error': 'The requested url was not found'}), 404)

@app.errorhandler(400)
def unauthorized(message=None):
     return make_response(jsonify(
         {'Error': 'Bad request'}), 400)
def search_bucketlists(q):
    bucketlists = BucketList.query.filter(BucketList.name.contains(q)).all()
    return bucketlists


class Home(Resource):
    """
    Returns welcome message to new user
    url: /api/v1/
    method: GET
    headers: None
    """

    def get(self):
        response = jsonify(
            {"message": "Welcome to live-it! To get started, register a new user or login"})
        return response
