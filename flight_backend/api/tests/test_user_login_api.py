import json

from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from rest_framework.views import status

from api.models import User

client = APIClient()


class UserLogInTest(APITestCase):
    def setUp(self):
        self.url = reverse("log-in")
        self.normal_user = User.objects.create_user(
            first_name="Ghost",
            last_name="Ghost",
            email="ghost@gmail.com",
            password="password1*",
        )
        self.login_details = {"email": "ghost@gmail.com", "password": "password1*"}

    def test_successful_login(self):
        response = client.post(
            self.url,
            data=json.dumps(self.login_details),
            content_type="application/json",
        )
        self.assertIn("token", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "ghost@gmail.com")

    def test_login_with_wrong_details(self):
        login_details = {"email": "test@gmail.com", "password": "password"}
        response = client.post(
            self.url, data=json.dumps(login_details), content_type="application/json"
        )
        self.assertEqual(
            response.data["message"], "Login not successful, check email and password."
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_login_with_invalid_details(self):
        login_details = {"email": "", "password": "password"}
        response = client.post(
            self.url, data=json.dumps(login_details), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data[0], "You must enter an email and a password to login"
        )
