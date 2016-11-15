from tests import SuperTestCase
from flask import jsonify
from manage import app
import json
from werkzeug.exceptions import HTTPException

class TestEndPoints(SuperTestCase):
    """ Endpoints being tested:
        /api/v1/bucketlists/
        /api/v1/bucketlists/<bucket_list_id>
        /api/v1/bucketlists/<bucketlist_id>/items/
        /api/v1/bucketlists/<bucketlist_id>/items/<item ID>

        Methods: GET, PUT, POST, DELETE
      """

    def test_invalid_url_on_creation_of_a_bucketlist(self):
        self.buck = {"name": "tomorrowland", "description": "dance time"}
        response = self.client.get(
            "/api/v1/bucketlists//", data=self.buck, headers=self.make_token(),
            content_type='application/json')
        print(response.data)
        msg = str(response.json['Error'])
        self.assertEqual(msg, 'The requested url was not found')
        self.assertEqual(response.status_code, 404)

    def test_requesting_a_bucketlist_without_auth(self):
        response = self.client.get("/api/v1/bucketlists/", content_type='application/json')
        self.assertEqual(response.data, 'Unauthorized Access')
        self.assertEqual(response.status_code, 401)

    def test_requesting_other_users_bucketlists(self):
        response = self.client.get(
            "/api/v1/bucketlists/1", headers=self.make_second_user_token(),
            content_type='application/json')
        msg = str(response.json['message'])
        self.assertEqual(msg, 'You are not authorized to view this')
        self.assertEqual(response.status_code, 401)

    def test_requesting_bucketlists(self):
        response = self.client.get(
            "/api/v1/bucketlists/", headers=self.make_second_user_token(),
            content_type='application/json')
        msg = str(response.json['message'])
        self.assertEqual(msg, 'There are no bucketlists available')
        self.assertEqual(response.status_code, 404)

    def test_editing_a_bucketlist_without_auth(self):
        self.buck = {"name": "tomorrowland", "description": "dance time"}
        response = self.client.put(
            "/api/v1/bucketlists/1", data=self.buck, headers=self.make_second_user_token(),
            content_type='application/json')
        msg = str(response.json['message'])
        self.assertEqual(msg, 'You are not authorized to edit this')
        self.assertEqual(response.status_code, 401)

    def test_creation_of_a_bucketlist(self):
        """ Test for creation of a bucketlist """
        self.buck = {"name": "tomorrowland", "description": "dance time"}
        response = self.client.post(
            "/api/v1/bucketlists/", data=self.buck, headers=self.make_token())
        msg = str(response.json['message'])
        self.assertEqual(msg, 'Bucket List updated Successfully')
        self.assertEqual(response.status_code, 200)

    def test_creation_of_a_bucketlist_without_name(self):
        """ Test for creation of a bucketlist """
        self.buck = {"description": "dance time"}
        response = self.client.post(
            "/api/v1/bucketlists/", data=self.buck, headers=self.make_token())
        msg = str(response.json['message'])
        self.assertEqual(msg, 'Please provide a name for the bucketlist')
        self.assertEqual(response.status_code, 400)

    def test_creation_of_a_bucketlist_with_existing_name(self):
        """ Test for creation of a bucketlist """
        self.buck = {"name": "btest1", "description": "dance time"}
        response = self.client.post(
            "/api/v1/bucketlists/", data=self.buck, headers=self.make_token())
        msg = str(response.json['message'])
        self.assertEqual(msg, 'That name is already taken, try again')
        self.assertEqual(response.status_code, 400)

    def test_deletion_of_a_bucketlist(self):
        """ Test deletion of a bucketlist """
        response = self.app.delete(
            "/api/v1/bucketlists/1", headers=self.make_token(),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_deletion_of_other_user_bucketlists(self):
        """ Test deletion of a bucketlist """
        response = self.app.delete(
            "/api/v1/bucketlists/1", headers=self.make_second_user_token(),
            content_type='application/json')
        msg = str(response.json['message'])
        self.assertEqual(msg, 'You are not authorized to delete this')
        self.assertEqual(response.status_code, 401)

    def test_deletion_of_a_none_existent_bucketlist(self):
        """ Test deletion of a bucketlist """
        response = self.app.delete(
            "/api/v1/bucketlists/1200", headers=self.make_token(),
            content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_get_bucketlists(self):
        """ Test listing all bucketlists via a get request """
        response = self.app.get(
            "/api/v1/bucketlists/", headers=self.make_token(),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_editing_a_bucketlist_that_doesnt_exist(self):
        """ Test editing a bucketlists that doesn't exist """
        self.bucketlist = {"name": "tomorrowland", "description": "party time"}
        response = self.app.put(
            "/api/v1/bucketlists/2000", data=self.bucketlist,
            headers=self.make_token(), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_editing_a_bucketlist_without_auth(self):
        self.buck = {"name": "tomorrowland", "description": "dance time"}
        response = self.client.put(
            "/api/v1/bucketlists/1", data=self.buck, headers=self.make_second_user_token(),
            content_type='application/json')
        msg = str(response.json['message'])
        self.assertEqual(msg, 'You are not authorized to edit this')
        self.assertEqual(response.status_code, 401)

    def test_editing_other_users_bucketlists(self):
        self.bucketlist = {"name": "tomorrowland", "description": "party time"}
        response = self.client.put(
            "/api/v1/bucketlists/1", headers=self.make_second_user_token(),
            content_type='application/json')
        msg = str(response.json['message'])
        self.assertEqual(msg, 'You are not authorized to edit this')
        self.assertEqual(response.status_code, 401)

    def test_editing_a_bucketlist(self):
        self.buck = {"name": "tomorrowland", "description": "dance time"}
        response = self.client.put(
            "/api/v1/bucketlists/1", data=self.buck, headers=self.make_token())
        self.assertEqual(response.status_code, 201)

    def test_get_single_bucketlist(self):
        """ Test listing a single bucketlist item """
        response = self.app.get("/api/v1/bucketlists/1",
                                headers=self.make_token())
        self.assertEqual(response.status_code, 200)

    def test_get_none_existent_bucketlist(self):
        """ Test get request on a none existent bucketlist """
        response = self.app.get("/api/v1/bucketlists/350",
                                headers=self.make_token())
        self.assertEqual(response.status_code, 404)

    def test_input_on_get_bucketlists_request(self):
        response = self.app.get("/api/v1/bucketlists?limit=abc",
                                headers=self.make_token())
        msg = str(response.json['message'])
        self.assertEqual(msg, ' provide an integer')
        self.assertEqual(response.status_code, 400)

    def test_item_creation(self):
        """ Test for response on new item creation """
        item_data = {"name": "invite guyz",
                     "description": "call up the hommies"}
        response = self.app.post(
            "/api/v1/bucketlists/2/items/", data=item_data,
            headers=self.make_token())
        self.assertEqual(response.status_code, 201)

    def test_item_creation_with_invalid_url(self):
        item_data = {"name": "invite guyz",
                     "description": "call up the hommies"}
        response = self.app.post(
            "/api/v1/bucketlists/2/items/1", data=item_data,
            headers=self.make_token())
        msg = str(response.json['message'])
        self.assertEqual(msg, 'Method not allowed(POST)')
        self.assertEqual(response.status_code, 400)

    def test_item_creation_with_invalid_credentials(self):
        item_data = {"namee": "invite guyz",
                     "description": "call up the hommies"}
        response = self.app.post(
            "/api/v1/bucketlists/2/items/", data=item_data,
            headers=self.make_token())
        msg = str(response.json['message'])
        self.assertEqual(msg, 'Please provide a name for the item')
        self.assertEqual(response.status_code, 400)

    def test_creation_of_item_with_existing_item_name(self):
        item_data = {"name": "itest1",
                     "description": "call up the hommies"}
        response = self.app.post(
            "/api/v1/bucketlists/2/items/", data=item_data,
            headers=self.make_token())
        msg = str(response.json['message'])
        self.assertEqual(msg, 'That name is already taken, try again')
        self.assertEqual(response.status_code, 400)

    def test_creation_of_item_in_none_existent_bucketlist(self):
        item_data = {"name": "itest8",
                     "description": "call up the hommies"}
        response = self.app.post(
            "/api/v1/bucketlists/200/items/", data=item_data,
            headers=self.make_token())
        msg = str(response.json['message'])
        self.assertEqual(msg, 'A bucketlist with the ID provided does not exist!')
        self.assertEqual(response.status_code, 404)

    def test_creation_of_item_in_other_users_bucketlist(self):
        item_data = {"name": "itest8","description": "call up the hommies"}
        response = self.app.post(
            "/api/v1/bucketlists/1/items/", data=item_data,
            headers=self.make_second_user_token())
        msg = str(response.json['message'])
        self.assertEqual(msg, 'You are not authorized to use the bucketlist')
        self.assertEqual(response.status_code, 401)

    def test_editing_an_item(self):
        """ Test for editing an item """
        self.item = {"name": "learn the guitar",
                     "description": "take guitar classes"}
        response = self.app.put(
            "/api/v1/bucketlists/1/items/1", headers=self.make_token())
        msg = str(response.json['message'])
        self.assertEqual(msg, 'Bucket List item updated')
        self.assertEqual(response.status_code, 200)

    def test_editing_other_users_item(self):
        """ Test for editing an item """
        self.item = {"name": "learn the guitar",
                     "description": "take guitar classes"}
        response = self.app.put(
            "/api/v1/bucketlists/1/items/1", headers=self.make_second_user_token())
        msg = str(response.json['message'])
        self.assertEqual(msg, 'You are not authorized to edit this')
        self.assertEqual(response.status_code, 401)

    def test_editing_item_with_invalid_url(self):
        self.item = {"name": "learn the guitar",
                     "description": "take guitar classes"}
        response = self.app.put(
            "/api/v1/bucketlists/1/items/", headers=self.make_token())
        msg = str(response.json['message'])
        self.assertEqual(msg, 'Method not allowed, check url')
        self.assertEqual(response.status_code, 400)

    def test_editing_none_existent_bucketlist_and_item(self):
        self.item = {"name": "learn the guitar",
                     "description": "take guitar classes"}
        response = self.app.put(
            "/api/v1/bucketlists/100/items/100", headers=self.make_token())
        msg = str(response.json['message'])
        self.assertEqual(msg, 'The bucketlist or item does not exist')
        self.assertEqual(response.status_code, 404)

    def test_invalid_url_on_item_request(self):
        response = self.app.get("/api/v1/bucketlists/1/items/",
                                headers=self.make_token())
        msg = str(response.json['message'])
        self.assertEqual(msg, 'Method not allowed, check url')
        self.assertEqual(response.status_code, 400)

    def test_item_request_on_none_existent_bucketlist(self):
        response = self.app.get("/api/v1/bucketlists/4/items/1",
                                headers=self.make_token())
        msg = str(response.json['message'])
        self.assertEqual(msg, 'the bucketlist does not exist')
        self.assertEqual(response.status_code, 404)

    def test_invalid_credentials_on_item_request(self):
        response = self.app.get("/api/v1/bucketlists/1/items/1",
                                headers=self.make_second_user_token())
        msg = str(response.json['message'])
        self.assertEqual(msg, 'You are not authorized to view this')
        self.assertEqual(response.status_code, 401)

    def test_requesting_a_none_existent_item(self):

        response = self.app.get("/api/v1/bucketlists/1/items/20",
                                headers=self.make_token())
        msg = str(response.json['message'])
        self.assertEqual(msg, 'The item does not exist')
        self.assertEqual(response.status_code, 404)

    def test_deletion_of_an_item(self):
        """ Test for deletion of an item  """
        response = self.app.delete("/api/v1/bucketlists/2/items/1",
                                   headers=self.make_token(),
                                   content_type='application/json')
        msg = str(response.json['message'])
        self.assertEqual(msg, 'The item has been successfully deleted')
        self.assertEqual(response.status_code, 200)

    def test_deletion_of_item_in_other_user_bucketlists(self):
        """ Test for deletion of an item  """
        response = self.app.delete("/api/v1/bucketlists/1/items/1",
                                   headers=self.make_second_user_token(),
                                   content_type='application/json')
        msg = str(response.json['message'])
        self.assertEqual(msg, 'You are not authorized to del this')
        self.assertEqual(response.status_code, 401)

    def test_deletion_of_a_none_existent_item(self):
        response = self.app.delete("/api/v1/bucketlists/2/items/300",
                                   headers=self.make_token(),
                                   content_type='application/json')
        msg = str(response.json['message'])
        self.assertEqual(msg, 'The item does not exist')
        self.assertEqual(response.status_code, 404)

    def test_deleting_an_item_with_invalid_url(self):
        response = self.app.delete("/api/v1/bucketlists/2/items/",headers=self.make_token(),content_type='application/json')
        msg = str(response.json['message'])
        self.assertEqual(msg, 'Method not allowed (DELETE)')
        self.assertEqual(response.status_code, 400)
