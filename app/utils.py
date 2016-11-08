from functools import wraps
from flask import g, request
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask_restful import Resource
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

from app import app
from config.config import config_settings
from models import User

auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(scheme='Token')

@auth.error_handler
def auth_error(message=None):
    ''' This method returns an error message in cases of authentication errors '''
    if not message:
        message = {'message': 'you are not allowed to make this request'}
        return message

@token_auth.verify_token
def verify_token(token):
    ''' This method verifies the token provided in a request header '''
    s = Serializer(config_settings['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        message = {'message': 'The token has expired'}
        return message
    except BadSignature:
        message = {'message': 'Bad or invalid token!'}
        return None
    user = User.query.get(data['id'])
    return user

def current_user_bucketlist(fuction):
    ''' This method check's whether a user is authorized to access and manipulate a bucketlist '''
    pass

def current_user_blist_items(fuction):
    ''' This method checks whether a user is authorized to access and manipulate a bucketlist item '''
    pass


class Home(Resource):
    """
    Returns welcome message to new user
    url: /api/v1/
    """
    def get(self):
        return {"message": "Welcome to live-it! To get started, register a new user or login"}
