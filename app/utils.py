from functools import wraps
from flask import g, request
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask_restful import Resource
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

from app import app
from config.config import config_settings
from models import User, BucketList, BucketListItem

auth = HTTPBasicAuth(scheme='Token')
token_auth = HTTPTokenAuth(scheme='Token')

def current_user_bucketlist(function):
    ''' This method check's whether a user is authorized to access and manipulate a bucketlist '''

    def auth_wrapper(*args, **kwargs):
        g.bucketlist = BucketList.query.filter_by(id=kwargs["id"]).first()
        try:
            if g.bucketlist:
                if g.bucketlist.created_by == g.user.id:
                    return function(*args, **kwargs)
                return 'You are not authorized'
            else:
                return 'The bucketlist does not exist', 404
        except:
            return 'Please check your token', 401

    return auth_wrapper

def current_user_blist_items(fuction):
    ''' This method checks whether a user is authorized to access and manipulate a bucketlist item '''

    def auth_wrapper(*args, **kwargs):
        bucketlist_item = BucketListItem.query.filter_by(id=kwargs["id"]).first()
        try:
            if bucketlist_item:
                if bucketlist_item.created_by == g.user.id:
                    return fuction(*args, **kwargs)
                return auth_error()
            else:
                return 'The bucketlist item does not exist', 404
        except:
            return 'Please check your token', 401

    return auth_wrapper

@app.before_request
def before_request():
    """
    This method validates a user's token and creates a global user object to be accessed by methods and requests
    """
    if request.endpoint not in ['home', 'register', 'login']:
        token = request.headers.get('Token')
        if token is not None:
            user = User.verify_token(token)
            if user:
                g.user = user
            else:
                message = {'message': 'The token entered is invalid!'}
                return message, 400
        else:
            message = {'message': 'Please provide a token'}
            return message, 401


class Home(Resource):
    """
    Returns welcome message to new user
    url: /api/v1/
    """

    def get(self):
        return {"message": "Welcome to live-it! To get started, register a new user or login"}
