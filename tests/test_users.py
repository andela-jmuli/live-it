from tests import SuperTestCase


class TestUsers(SuperTestCase):


    def test_successful_registration(self):
        self.user_data = {"username":"kimani", "password":"passsword"}
        response = self.app.post("/api/v1/auth/register", data=self.user_data)
        self.assertEqual(response.status_code, 201)

    def test_succesful_login(self):
        self.user_data = {'username':'kimani', 'password':'passsword'}
        response = self.app.post("api/v1/auth/login", data=self.user_data)
        self.assertEqual(response.status_code, 200)
