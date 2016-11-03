from tests import SuperTestCase


class TestItems(SuperTestCase):
    """ Endpoints being tested:
        /api/v1/bucketlists/<bucketlist_id>/items/
        /api/v1/bucketlists/<bucketlist_id>/items/<item ID>
        Methods: GET, PUT, POST, DELETE
    """

    def test_item_creation(self):
        """ Test for response on new item creation """
        self.item = {"name":"invite guyz", "description":"call up the hommies"}
        response = self.app.post("/api/v1/bucketlists/2/items/", content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_duplicate_item(self):
        pass

    def test_get_bucketlist_item(self):
        """ Test response for an item's get request """
        response = self.app.get("/api/v1/bucketlists/1/items/1")
        self.assertEqual(response.status_code, 200)

    def test_editing_an_item(self):
        """ Test for editing an item """
        self.item = {"name":"learn the guitar", "description":"take guitar classes"}
        response = self.app.put("/api/v1/bucketlists/1/items/1", content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_deletion_of_an_item(self):
        """ Test for deletion of an item  """
        response = self.app.delete("/api/v1/bucketlists/2/items/1")
        self.assertEqual(response.status_code, 200)

    def test_get_none_existent_item(self):
        """ Test for a none existent bucketlist item """
        response = self.app.get("/api/v1/bucketlists/1/items/990")
        self.assertEqual(response.status_code, 204)
