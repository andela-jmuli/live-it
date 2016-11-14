from flask import g, jsonify, request
from flask_httpauth import HTTPTokenAuth
from flask_jwt import jwt_required
from flask_restful import marshal, reqparse, Resource

from app import db
from models import BucketList
from serializers import bucketlists_serializer
from utils import multiauth


class AllBucketlists(Resource):
    """ Defines endpoints for method calls that affect all bucketlists
        methods: GET, POST
        url: api/v1/bucketlists/
     """
    
    @multiauth.login_required
    def post(self):
        """ Method to create new bucketlists """
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, help='A name is required')
        parser.add_argument('description', type=str, default='')
        args = parser.parse_args()
        name = args["name"]
        description = args["description"]
        # set parsed items to an object of model class
        b_list = BucketList(name=name, description=description, created_by=g.user.id)

        if not name:
            response = jsonify({'message': 'Please provide a name for the bucketlist'})
            response.status_code = 400
            return response
        try:
            BucketList.query.filter_by(name=name).one()
            response = jsonify({'message': 'That name is already taken, try again'})
            response.status_code = 400
            return response

        except:
            try:
                db.session.add(b_list)
                db.session.commit()
                message = {'message': 'Bucket List updated Successfully'}
                response = marshal(b_list, bucketlists_serializer)
                response.update(message)
                response.status_code = 201
                return response

            except Exception:
                response = jsonify({'message': 'There was an error saving the bucketlist'})
                response.status_code = 400
                return response

    @multiauth.login_required
    def get(self):
        """ Method that gets all bucketlists """
        print("it work")
        args = request.args.to_dict()
        page = int(args.get('page', 1)) # query start as an integer
        limit = int(args.get('limit', 20)) # 100 items == 20 per page for 5 pages
        q = args.get('q')

        if q:
            b_lists = BucketList.query.filter(BucketList.name.contains(q)).filter_by(
            created_by=g.user.id).paginate(page, limit, False)
            if len(b_lists) <= 0:
                response = jsonify({'message': 'No bucketlists with that query...'})
                response.status_code = 404
                return response
        else:
            # query a paginate object
            b_lists = BucketList.query.filter_by(created_by=g.user.id).paginate(
            page, limit, False)

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
            # if bucketlists are not None, return data as output
            if b_lists:
                return data
            else:
                response = jsonify({'message': 'There are no bucketlists available'})
                response.status_code = 404
                return response


class BucketlistApi(Resource):
    """ Defines methods that affects a single bucketlist
        methods: GET, PUT, DELETE
        url: url: api/v1/bucketlists/<bucketlist_id>
    """

    @multiauth.login_required
    def get(self, id):
        """
        Method that gets a single bucketlist
        """
        # gets all bucketlists belonging to the user
        bucketlist = BucketList.query.filter_by(id=id).first()
        if bucketlist:
            response = marshal(bucketlist, bucketlists_serializer)
            return response
        else:
            response = jsonify({'message': 'the bucketlist does not exist'})
            response.status_code = 404
            return response

    @multiauth.login_required
    def put(self, id):
        """
        Method that edits an existing bucketlist
        """
        bucketlist = BucketList.query.get(id)
        # if the bucketlist exists get new changes
        if bucketlist:
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, help='A name is required')
            parser.add_argument('description', type=str, default='')
            args = parser.parse_args()

            name = args["name"]
            description = args["description"]
            # update changes and commit to db
            item_info = BucketList.query.filter_by(id=id).update(
                {'name': name, 'description': description})

            try:
                db.session.commit()
                response = jsonify({'message': 'Bucket List has been updated!'})
                response.status_code = 201
                return response

            except Exception:
                response = jsonify({'message': 'There was an error updating the bucketlist'})
                response.status_code = 500
                return response
        else:
            response = jsonify({'message': 'The bucketlist does not exist'})
            response.status_code = 404
            return response

    @multiauth.login_required
    def delete(self, id):
        """
        Method that deletes an existing bucketlist
        """
        # query whether the bucketlist exists
        bucketlist = BucketList.query.get(id)

        # if it exists delete and commit changes to db
        if bucketlist:
            BucketList.query.filter_by(id=id).delete()
            db.session.commit()
            response = jsonify({'message': 'The bucketlist has been successfully deleted'})
            response.status_code = 200
            return response
        else: # else return a 404 response
            response = jsonify({'message': 'The buckelist does not exist'})
            response.status_code = 404
            return response
