from tests import SuperTestCase

import json

class TestEndPoints(SuperTestCase):
    """ Endpoints being tested:
        /api/v1/bucketlists/
        /api/v1/bucketlists/<bucket_list_id>
        Methods: GET, PUT, POST, DELETE
      """

    def test_creation_of_a_bucketlist(self):
        """ Test for creation of a bucketlist """
        self.bucketlist = {"name":"tomorrowland", "description":"dance time"}
        response = self.app.post("/api/v1/bucketlists/",data=self.bucketlist)
        self.assertEqual(response.status_code, 201 )

    def test_creation_of_a_duplicate_bucketlist(self):
        pass

    def test_editing_a_bucketlist(self):
        """ Test for editing an existent bucketlist """
        self.bucketlist = {"name":"tomorrowland", "description":"party time"}
        response = self.app.put("/api/v1/bucketlists/1",data=self.bucketlist)
        self.assertEqual(response.status_code, 200)

    def test_deletion_of_a_bucketlist(self):
        """ Test deletion of a bucketlist """
        response = self.app.delete("/api/v1/bucketlists/1")
        self.assertEqual(response.status_code, 200)

    def test_get_bucketlists(self):
        """ Test listing all bucketlists via a get request """
        response = self.app.get("/api/v1/bucketlists/")
        self.assertEqual(response.status_code, 200)

    def test_get_single_bucketlist(self):
        """ Test listing a single bucketlist item """
        response = self.app.get("/api/v1/bucketlists/1")
        self.assertEqual(response.status_code, 200)

    def test_get_none_existent_bucketlist(self):
        """ Test get request on a none existent bucketlist """
        response = self.app.get("/api/v1/bucketlists/350")
        self.assertEqual(response.status_code, 204)
