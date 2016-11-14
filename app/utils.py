from functools import wraps
from flask import g, jsonify, request
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask_restful import Resource
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

from app import app
from config.config import config_settings
from models import User, BucketList, BucketListItem

auth = HTTPBasicAuth(scheme='Token')
token_auth = HTTPTokenAuth(scheme='Token')


@auth.verify_password
def authenticate_token(token):
    user = User.verify_token(token)
    if user:
        g.user = user
        return user
    return False


@auth.error_handler
def unauthorized(message=None):
    return make_response(jsonify(
        {'Error': 'Invalid token given, '
         'Login again to gain access'}), 403)


def current_user_bucketlist(function):
    ''' This method check's whether a user is authorized
        to access and manipulate a bucketlist
    '''

    def auth_wrapper(*args, **kwargs):
        g.bucketlist = BucketList.query.filter_by(id=kwargs["id"]).first()
        try:
            if g.bucketlist.created_by == g.user.id:
                return function(*args, **kwargs)

            return 'You are not authorized', 401
        except:
            return 'The bucketlist does not exist', 404
    return auth_wrapper


def current_user_blist_items(fuction):
    ''' This method checks whether a user is authorized
        to access and manipulate a bucketlist item
    '''

    def auth_wrapper(*args, **kwargs):
        g.bucketlist_item = BucketListItem.query.filter_by(
            id=kwargs["id"]).first()
        try:
            if g.bucketlist_item.created_by == g.user.id:
                return fuction(*args, **kwargs)
            response = jsonify({'message': 'You are not authorized'})
            response.status_code = 401
            return response
        except:
            response = jsonify(
                {'message': 'The item requested does not exist'})
            response.status_code = 404
            return response
    return auth_wrapper


@app.before_request
def before_request():
    """
    This method validates a user's token and creates a global user
    object to be accessed by methods and requests
    The method runs before all requests, exceptional requests
    are 'home', 'register' and 'login'
    """
    if request.endpoint not in ['home', 'register', 'login']:
        token = request.headers.get('token')
        if token is not None:
            user = authenticate_token(token)
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
    method: GET
    headers: None
    """

    def get(self):
        response = jsonify(
            {"message": "Welcome to live-it! To get started, \
             register a new user or login"})
        return response
