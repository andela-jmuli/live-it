from flask import g, jsonify
from flask_restful import Resource, marshal
from flask_restful import reqparse

from app import db
from models import BucketList
from serializers import bucketlists_serializer


class AllBucketlists(Resource):
    """ Defines endpoints for method calls that affect all bucketlists
        methods: GET, POST
        url:
     """
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, help='A name is required')
        parser.add_argument('description', type=str, default='')
        args = parser.parse_args()
        name = args["name"]
        description = args["description"]
        b_list = BucketList(name=name, description=description)

        if not name:
            message = {'message': 'Please provide a name for the bucketlist'}
            return message, 400

        try:
            BucketList.query.filter_by(name=name).one()
            message = {'message': 'That name is already taken, try again'}
            return message, 400

        except:
            try:
                db.session.add(b_list)
                db.session.commit()
                message = {'message': 'Bucket List updated Successfully'}
                response = marshal(b_list, bucketlists_serializer)
                response.update(message)
                return response, 201
            except Exception as e:
                response = jsonify({'message': 'There was an error saving the bucketlist'})
                response.status_code = 400
                return e


    def get(self):
        pass


class BucketlistApi(Resource):
    """ Defines methods that affects a single bucketlist
        methods: GET, PUT, DELETE
        url:
    """

    def get(self):
        pass

    def put(self, id):
        bucketlist = BucketList.query.get(id)

        if bucketlist:
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, help='A name is required')
            parser.add_argument('description', type=str, default='')
            args = parser.parse_args()

            name = args["name"]
            description = args["description"]

            item_info = BucketList.query.filter_by(id=id).update(
                {'name': name, 'description': description})

            try:
                db.session.commit()
                message = {'message': 'Bucket List has been updated!'}
                return message, 201

            except Exception as e:
                message = {'message': 'There was an error updating the bucketlist'}
                return e
        else:
            message = {'message': 'The bucketlist does not exist'}
            return e, 404

    def delete(self):
        pass
