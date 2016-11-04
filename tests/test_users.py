# from tests import SuperTestCase


# class TestUsers(SuperTestCase):


#     def test_successful_registration(self):
#         self.user_data = {"username":"tester", "password":"master12"}
#         response = self.app.post("/api/v1/auth/register", data=self.user_data, content_type="application/json")
#         self.assertEqual(response.status_code, 200)

#     def test_user_login(self):
#         self.login_info = {"username":"testuser", "password":"master21"}
#         response = self.app.post("/api/v1/auth/login", data=self.login_info, content_type="application/json")
#         self.assertEqual(response.status_code, 200)

#     def test_login_with_invalid_info(self):
#         pass
