from tests import SuperTestCase
from flask import jsonify
from manage import app
import json

class TestEndPoints(SuperTestCase):
    """ Endpoints being tested:
        /api/v1/bucketlists/
        /api/v1/bucketlists/<bucket_list_id>
        /api/v1/bucketlists/<bucketlist_id>/items/
        /api/v1/bucketlists/<bucketlist_id>/items/<item ID>

        Methods: GET, PUT, POST, DELETE
      """

    def test_creation_of_a_bucketlist(self):
        """ Test for creation of a bucketlist """
        self.buck = {"name":"tomorrowland", "description":"dance time"}
        response = self.client.get("/api/v1/bucketlists/", headers=self.make_token(), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_editing_a_bucketlist(self):
        """ Test for editing an existent bucketlist """
        self.bucketlist = {"name":"tomorrowland", "description":"party time"}
        response = self.app.put("/api/v1/bucketlists/2",data=self.bucketlist, headers=self.make_token())
        self.assertEqual(response.status_code, 201)

    def test_deletion_of_a_bucketlist(self):
        """ Test deletion of a bucketlist """
        response = self.app.delete("/api/v1/bucketlists/1", headers=self.make_token(), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_bucketlists(self):
        """ Test listing all bucketlists via a get request """
        response = self.app.get("/api/v1/bucketlists/", headers=self.make_token(), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_single_bucketlist(self):
        """ Test listing a single bucketlist item """
        response = self.app.get("/api/v1/bucketlists/1", headers=self.make_token())
        self.assertEqual(response.status_code, 200)

    def test_get_none_existent_bucketlist(self):
        """ Test get request on a none existent bucketlist """
        response = self.app.get("/api/v1/bucketlists/350", headers=self.make_token())
        self.assertEqual(response.status_code, 404)

    def test_item_creation(self):
        """ Test for response on new item creation """
        item_data = {"name":"invite guyz", "description":"call up the hommies"}
        response = self.app.post("/api/v1/bucketlists/2/items/", data=item_data, headers=self.make_token())
        self.assertEqual(response.status_code, 201)

    def test_editing_an_item(self):
        """ Test for editing an item """
        self.item = {"name":"learn the guitar", "description":"take guitar classes"}
        response = self.app.put("/api/v1/bucketlists/1/items/1", headers=self.make_token())
        self.assertEqual(response.status_code, 201)

    def test_deletion_of_an_item(self):
        """ Test for deletion of an item  """
        response = self.app.delete("/api/v1/bucketlists/2/items/1", headers=self.make_token(), content_type='application/json')
        self.assertEqual(response.status_code, 200)
