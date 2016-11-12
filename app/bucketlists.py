from flask import g, jsonify, request
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask_restful import Resource, marshal
from flask_restful import reqparse

from app import db
from models import BucketList
from serializers import bucketlists_serializer
from utils import current_user_bucketlist, token_auth

auth = HTTPTokenAuth(scheme='Token')


class AllBucketlists(Resource):
    """ Defines endpoints for method calls that affect all bucketlists
        methods: GET, POST
        url: api/v1/bucketlists/
     """

    def post(self):
        """ Method to create new bucketlists """
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, help='A name is required')
        parser.add_argument('description', type=str, default='')
        args = parser.parse_args()
        name = args["name"]
        description = args["description"]

        b_list = BucketList(name=name, description=description, created_by=g.user.id)

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
        """ Method that gets all bucketlists """
        args = request.args.to_dict()
        page = int(args.get('page', 1)) # query start as an integer
        limit = int(args.get('limit', 20)) # 100 items == 20 per page for 5 pages
        q = args.get('q')

        if q:
            b_lists = BucketList.query.filter(BucketList.name.contains(q)).filter_by(
            created_by=g.user.id).paginate(page, limit, False)
            if len(b_lists) < 0:
                message = {'message':'No bucketlists with that query...'}
                return message, 404
        else:
            # query a paginate object
            b_lists = BucketList.query.filter_by(created_by=g.user.id).paginate(
            page,limit, False)

            all_pages = b_lists.pages # get total page count
            next_pg = b_lists.has_next # check for next page
            previous_pg = b_lists.has_prev # check for previous page

            # if the query allows a max over the limit, generate a url for the next page
            if next_pg:
                next_page = str(request.url_root) + 'api/v1/bucketlists?' + \
                'limit=' + str(limit) + '&page=' + str(page + 1)
            else:
                next_page = 'None'

            # set a url for the previous page
            if previous_pg:
                previous_page = str(request.url_root) + 'api/v1/bucketlists?' + \
                'limit=' + str(limit) + '&page=' + str(page - 1)
            else:
                previous_page = 'None'

            b_lists = b_lists.items

            data = {'bucketlists': marshal(b_lists, bucketlists_serializer),
                    'total pages': all_pages,
                    'next page': next_page,
                    'previous page': previous_page }
            # if bucketlists are note None, return data as output
            if b_lists:
                return data
            else:
                message = {'message': 'There are no bucketlists available'}
                return message, 404


class BucketlistApi(Resource):
    """ Defines methods that affects a single bucketlist
        methods: GET, PUT, DELETE
        url: url: api/v1/bucketlists/<bucketlist_id>
    """

    @current_user_bucketlist
    def get(self, id):
        """
        Method that gets a single bucketlist
        """
        bucketlist = BucketList.query.filter_by(id=id).first()
        if bucketlist:
            response = marshal(bucketlist, bucketlists_serializer)
            return response
        else:
            response = {'message': 'the bucketlist does not exist'}
            return response, 404

    @current_user_bucketlist
    def put(self, id):
        """
        Method that edits an existing bucketlist
        """
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
            return message, 404

    @current_user_bucketlist
    def delete(self, id):
        """
        Method that deletes an existing bucketlist
        """
        bucketlist = BucketList.query.get(id)

        if bucketlist:
            BucketList.query.filter_by(id=id).delete()
            db.session.commit()
            message = {'message': 'The bucketlist has been successfully deleted'}
            return message, 200
        else:
            message = {'message': 'The buckelist does not exist'}
            return message, 400
