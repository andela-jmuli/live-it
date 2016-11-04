from flask import g, jsonify
from flask_restful import Resource, marshal
from flask_restful import reqparse

from app import db
from models import BucketList,BucketListItem
from serializers import items_serializer


class BucketlistItem(Resource):
    """ Defines endpoints for bucketlist items manipulation
        methods: GET, POST, PUT, DELETE
        url: /api/v1/bucketlists/<bucketlist_id>/items
     """
    def post(self, id):
        bucketlist = BucketList.query.get(id)
        if bucketlist:
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, help='A name is required')
            parser.add_argument('description', type=str, default='')
            args = parser.parse_args()

            name = args["name"]
            description = args["description"]

            item = BucketListItem(name=name, description=description, bucketlist_id=id, created_by=1)

            if not name:
                message = {'message': 'Please provide a name for the bucketlist'}
                return message, 400

            try:
                BucketListItem.query.filter_by(name=name).one()
                message = {'message': 'That name is already taken, try again'}
                return message, 400

            except:
                try:
                    db.session.add(item)
                    db.session.commit()
                    message = {'message': 'Bucket List item added Successfully!'}
                    response = marshal(item, items_serializer)
                    response.update(message)
                    return response, 201

                except Exception as e:
                    message = {'message': 'There was an error saving the item'}
                    return message, 400
        else:
            message = {'message': 'A bucketlist with the ID provided does not exist!'}
            return message, 404

    def put(self, id, item_id):
        bucketlist = BucketList.query.get(id)
        item = BucketListItem.query.filter_by(id=item_id).one()

        if bucketlist and item:
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, help='A name is required')
            parser.add_argument('description', type=str, default='')
            args = parser.parse_args()

            name = args["name"]
            description = args["description"]

            item_info = BucketListItem.query.filter_by(id=item_id).update(
                {'name': name, 'description': description})

            try:
                db.session.commit()
                message = {'message': 'Bucket List item updated'}
                return message, 201

            except Exception as e:
                message = {'message': 'There was an error updating the item'}
                return e
        else:
            message = {'message': 'The bucketlist or item does not exist'}
            return e, 404

    def get(self):
        item = BucketListItem.query.filter_by(id=id).first()
        if item:
            return marshal(bucketlist, bucketlists_serializer)
        else:
            message = {'message': 'the item does not exist'}
            return message, 404

    def delete(self, id, item_id):
        item = BucketListItem.query.get(item_id)

        if item:
            BucketListItem.query.filter_by(id=item_id).delete()
            db.session.commit()
            message = {'message': 'The item has been successfully deleted'}
            return message, 200
        else:
            message = {'message': 'The item does not exist'}
            return message, 400
