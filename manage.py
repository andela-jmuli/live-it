from flask_restful import Api
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db
from app.bucketlists import AllBucketlists, BucketlistApi
from app.items import BucketlistItem
from app.users import RegisterUser, LoginUser
from app.utils import Home


manager = Manager(app)
api = Api(app)
migrate = Migrate(app, db)

api.add_resource(Home, "/api/v1/", endpoint="home")
api.add_resource(RegisterUser, "/api/v1/auth/register", "/api/v1/auth/register/", endpoint="register")
api.add_resource(LoginUser, "/api/v1/auth/login", "/api/v1/auth/login/", endpoint="login")
api.add_resource(AllBucketlists, "/api/v1/bucketlists", endpoint="bucketlists")
api.add_resource(BucketlistApi, "/api/v1/bucketlists/<id>", "/api/v1/bucketlists/<id>/" , endpoint="single_bucket_list")
api.add_resource(BucketlistItem, "/api/v1/bucketlists/<id>/items", "/api/v1/bucketlists/<id>/items/", endpoint="bucketlist_items")
api.add_resource(BucketlistItem, "/api/v1/bucketlists/<id>/items/<item_id>", endpoint="single_item")


manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
