from flask_testing import TestCase

import os

from app.models import User, BucketList, BucketListItem
from config.config import config_settings
from manage import app, db
import json

basedir = os.path.abspath(os.path.dirname(__file__))


class SuperTestCase(TestCase):

    def create_app(self):
        app.config.from_object(config_settings['testing'])
        return app

    def setUp(self):
        self.app = self.create_app().test_client()
        self.database = db
        db.create_all()

        # Add dummy data for test purposes
        user = User(username="testuser")
        user.set_password('master12')

        user2 = User(username="testuser2")
        user2.set_password('password')

        b_list1 = BucketList(
            name="btest1", description="test one", created_by=1)
        b_list2 = BucketList(
            name="btest2", description="test two", created_by=1)

        b_item1 = BucketListItem(
            name="itest1", description="part of test", created_by=1, bucketlist_id=1)
        b_item2 = BucketListItem(
            name="itest2", description="part of 2nd test", created_by=1, bucketlist_id=2)

        db.session.add(user)
        db.session.add(user2)
        db.session.add(b_list1)
        db.session.add(b_list2)
        db.session.add(b_item1)
        db.session.add(b_item2)
        db.session.commit()

    def make_token(self):
        self.user_data = {'username': 'testuser', 'password': 'master12'}
        response = self.app.post("api/v1/auth/login", data=self.user_data)
        output = json.loads(response.data)
        token = output.get("token").encode("ascii")
        self.authorization = {'Authorization': 'Token %s' % token}
        return self.authorization

    def make_second_user_token(self):
        self.user_data = {'username': 'testuser2', 'password': 'password'}
        response = self.app.post("api/v1/auth/login", data=self.user_data)
        output = json.loads(response.data)
        token = output.get("token").encode("ascii")
        self.authorization = {'Authorization': 'Token %s' % token}
        return self.authorization

    def tearDown(self):
        db.session.remove()
        db.drop_all()
