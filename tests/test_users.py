import json

from tests import SuperTestCase


class TestUsers(SuperTestCase):

    def test_successful_registration(self):
        self.user_data = {"username": "kimani",
                          "password": "passsword"}
        response = self.app.post("/api/v1/auth/register", data=self.user_data)
        msg = json.loads(response.data)
        self.assertIn(msg['message'], 'new user successfully registered!')
        self.assertEqual(response.status_code, 201)

    def test_registration_with_existing_credentials(self):
        self.user_data = {"username": "testuser",
                          "password": "passsword"}
        response = self.app.post("/api/v1/auth/register", data=self.user_data)
        msg = json.loads(response.data)
        self.assertEqual(str(msg['message']),
                         'the username is already registered')
        self.assertEqual(response.status_code, 400)

    def test_succesful_login(self):
        self.user_data = {'username': 'kimani', 'password': 'passsword'}
        response = self.app.post("api/v1/auth/login", data=self.user_data)
        self.assertEqual(response.status_code, 200)

    def test_login_without_credentials(self):
        self.user_data = {'username': '', 'password': ''}
        response = self.app.post("api/v1/auth/login", data=self.user_data)
        msg = json.loads(response.data)
        self.assertIn(msg['message'], 'one or more fields is not complete')
        self.assertEqual(response.status_code, 400)
