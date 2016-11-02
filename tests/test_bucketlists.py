from tests import SuperTestCase

import json

class TestEndPoints(SuperTestCase):


    def test_creation_of_a_bucketlist(self):
        self.bucketlist = {"name":"tomorrowland", "description":"dance time"}
        response = self.app.post("/api/v1/bucketlists/",data=self.bucketlist)
        self.assertEqual(response.status_code, 201)

    def test_creation_of_a_duplicate_bucketlist(self):
        pass

    def test_editing_a_bucketlist(self):
        pass

    def test_deletion_of_a_bucketlist(self):
        pass

    def test_get_bucketlists(self):
        pass

    def test_get_single_bucketlist(self):
        pass
