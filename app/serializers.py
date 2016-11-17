from flask_restful import fields


users_serializer = {
    "id": fields.Integer,
    "username": fields.String
}

items_serializer = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "bucketlist_id": fields.Integer,
    "date_created": fields.DateTime,
    "date_modified": fields.DateTime,
    "is_done": fields.Boolean
}


bucketlists_serializer = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "date_created": fields.DateTime,
    "date_modified": fields.DateTime,
    "created_by": fields.Integer,
    "items": fields.List(fields.Nested(items_serializer))
}
