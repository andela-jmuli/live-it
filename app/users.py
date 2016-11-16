from flask import jsonify
from flask_restful import marshal, \
    reqparse, Resource

from app import db
from models import User
from serializers import users_serializer


class RegisterUser(Resource):
    """ Defines endpoint for User registration
        method: POST
        url: /api/v1/auth/register
     """

    def post(self):
        """
        request that handles User registration
        """
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True,
                            type=str, help='Username is required')
        parser.add_argument('password', required=True, default='')
        args = parser.parse_args()
        username = args['username']
        password = args['password']
        user = User(username=username)
        user.set_password(password)
        try:
            User.query.filter_by(username=username).one()
            response = jsonify(
                {'message': 'the username is already registered'})
            response.status_code = 400
            return response
        except:
            try:
                db.session.add(user)
                db.session.commit()
                response = jsonify(
                    {'message': 'new user successfully registered!'})
                response.status_code = 201
                return response
            except Exception:
                response = jsonify(
                    {'message': 'there was a problem while saving the data'})
                response.status_code = 500
                return response


class LoginUser(Resource):
    """ Defines endpoint for User login
        method: POST
        url: /api/v1/auth/login
     """

    def post(self):
        '''
        request that handles login
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True,
                            type=str, help='Username is required')
        parser.add_argument('password', required=True)
        args = parser.parse_args()
        username = args['username']
        password = args['password']
        if username and password:
            user = User.query.filter_by(username=username).first()
            if user and user.verify_password(password):
                user_token = user.generate_auth_token()
                return {'token': user_token}, 200
            else:
                message = {'message': 'Invalid password'}
                return message
        else:
            message = {'message': 'one or more fields is not complete'}
            return message, 400
