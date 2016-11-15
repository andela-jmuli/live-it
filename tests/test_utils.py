from tests import SuperTestCase



class TestUtilityMethods(SuperTestCase):

    def test_home_endpoint(self):
        response = self.app.get("/api/v1/")
        self.assertEqual(response.status_code, 200)
#
