from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db
from app.bucketlists import AllBucketlists, BucketlistApi
from app.items import BucketlistItem
from app.users import RegisterUser, LoginUser
from flask_restful import Api

manager = Manager(app)
api = Api(app)
migrate = Migrate(app, db)

api.add_resource(RegisterUser, "/auth/register/", endpoint="register")
api.add_resource(LoginUser, "/auth/login/", endpoint="login")
api.add_resource(AllBucketlists, "/bucketlists/", endpoint="bucketlists")
api.add_resource(BucketlistApi, "/bucketlists/<id>", endpoint="single_bucket_list")
api.add_resource(BucketlistItem, "/bucketlists/<id>/items/", endpoint="bucketlist_items")
api.add_resource(BucketlistItem, "/bucketlists/<id>/items/<item_id>", endpoint="single_item")


manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
