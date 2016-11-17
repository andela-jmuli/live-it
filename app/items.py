from flask import g, jsonify
from flask_restful import Resource, marshal
from flask_restful import abort, reqparse

from app import db
from models import BucketList, BucketListItem
from serializers import items_serializer
from utils import multiauth


class BucketlistItem(Resource):
    """ Defines endpoints for bucketlist items manipulation
        methods: GET, POST, PUT, DELETE
        url: /api/v1/bucketlists/<bucketlist_id>/items/
     """
    @multiauth.login_required
    def post(self, id, item_id=None):
        """
        request that handles bucketlist item creation
        """
        if item_id:
            response = jsonify({'message': 'Method not allowed(POST)'})
            response.status_code = 400
            return response

        bucketlist = BucketList.query.get(id)
        if bucketlist:
            if bucketlist.created_by != g.user.id:
                response = jsonify(
                    {'message': 'You are not authorized to use the bucketlist'})
                response.status_code = 401
                return response
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, help='A name is required')
            parser.add_argument('description', type=str, default='')
            parser.add_argument('is_done', type=bool, default=False)
            args = parser.parse_args()

            name = args["name"]
            description = args["description"]

            if not name:
                response = jsonify(
                    {'message': 'Please provide a name for the bucketlist item'})
                response.status_code = 400
                return response
            is_done = args["is_done"]
            if not is_done or type(is_done) != bool:
                is_done == False

            item = BucketListItem(
                name=name, description=description,
                bucketlist_id=id, is_done=is_done, created_by=g.user.id)

            if not name:
                response = jsonify(
                    {'message': 'Please provide a name for the item'})
                response.status_code = 400
                return response

            try:
                BucketListItem.query.filter_by(name=name).one()
                response = jsonify(
                    {'message': 'That name is already taken, try again'})
                response.status_code = 400
                return response

            except:
                try:
                    db.session.add(item)
                    db.session.commit()
                    message = {
                        'message': 'Bucket List item added Successfully!'}
                    response = marshal(item, items_serializer)
                    response.update(message)
                    return response, 201

                except:
                    response = jsonify(
                        {'message': 'There was an error saving the item'})
                    response.status_code = 400
                    return response
        else:
            response = jsonify(
                {'message': 'A bucketlist with the ID provided does not exist!'})
            response.status_code = 204
            return response

    @multiauth.login_required
    def put(self, id, item_id=None):
        """
        request that updates an item
        """
        if item_id == None:
            response = jsonify({'message': 'Method not allowed, check url'})
            response.status_code = 400
            return response
        try:
            bucketlist = BucketList.query.get(id)
            item = BucketListItem.query.filter_by(id=item_id).one()
        except:
            response = jsonify(
                {'message': 'The bucketlist or item does not exist'})
            response.status_code = 204
            return response

        if item.created_by == g.user.id:
            if bucketlist and item:
                parser = reqparse.RequestParser()
                parser.add_argument(
                    'name', type=str, help='A name is required')
                parser.add_argument('description', type=str, default='')
                parser.add_argument('is_done', type=bool, default=False)
                args = parser.parse_args()

                name = args["name"]
                description = args["description"]

                is_done = args["is_done"]

                data = {'name': name, 'description': description, 'is_done':is_done}
                if not name or name == None:
                    data = {'description': description, 'is_done': is_done}

                item_info = BucketListItem.query.filter_by(id=item_id).update(data)

                try:
                    db.session.commit()
                    response = jsonify({'message': 'Bucket List item updated'})
                    response.status_code = 200
                    return response

                except Exception:
                    response = jsonify(
                        {'message': 'There was an error updating the item'})
                    response.status_code = 500
                    return response
            else:
                response = jsonify(
                    {'message': 'The bucketlist or item does not exist'})
                response.status_code = 204
                return response
        else:
            response = jsonify(
                {'message': 'You are not authorized to edit this'})
            response.status_code = 401
            return response

    @multiauth.login_required
    def get(self, id, item_id=None):
        """
        request that lists a single item
        """
        if item_id == None:
            response = jsonify({'message': 'Method not allowed, check url'})
            response.status_code = 400
            return response
        bucketlist = BucketList.query.filter_by(id=id).first()
        item = BucketListItem.query.filter_by(
            id=item_id, bucketlist_id=id).first()
        if bucketlist:
            if item:
                if item.created_by == g.user.id:
                    return marshal(item, items_serializer)
                else:
                    response = jsonify(
                        {'message': 'You are not authorized to view this'})
                    response.status_code = 401
                    return response
            else:
                response = jsonify({'message': 'The item does not exist'})
                response.status_code = 204
                return response
        else:
            response = jsonify({'message': 'the bucketlist does not exist'})
            response.status_code = 204
            return response

    @multiauth.login_required
    def delete(self, id, item_id=None):
        """
        request that deletes an item
        """
        if item_id == None:
            response = jsonify({'message': 'Method not allowed (DELETE)'})
            response.status_code = 400
            return response

        item = BucketListItem.query.get(item_id)

        if item:
            if item.created_by == g.user.id:
                BucketListItem.query.filter_by(id=item_id).delete()
                db.session.commit()
                response = jsonify(
                    {'message': 'The item has been successfully deleted'})
                response.status_code = 200
                return response
            else:
                response = jsonify(
                    {'message': 'You are not authorized to del this'})
                response.status_code = 401
                return response
        else:
            response = jsonify({'message': 'The item does not exist'})
            response.status_code = 204
            return response
