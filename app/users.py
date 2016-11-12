from flask_restful import marshal, reqparse, Resource
from serializers import users_serializer

from app import db
from models import User


class RegisterUser(Resource):
    """ Defines endpoint for User registration
        method: POST
        url: /api/v1/auth/register
     """

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, type=str, help='Username is required')
        parser.add_argument('password', required=True, default='')
        args = parser.parse_args()
        username = args['username']
        password = args['password']
        user = User(username=username)
        user.set_password(password)
        try:
            User.query.filter_by(username=username).one()
            message = {'message': 'the username is already registered'}
            return message, 400
        except:
            try:
                db.session.add(user)
                db.session.commit()
                message = {'message': 'new user successfully registered!'}
                return message, 201
            except Exception as e:
                return e

class LoginUser(Resource):
    """ Defines endpoint for User login
        method: POST
        url: /api/v1/auth/login
     """

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, type=str, help='Username is required')
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

