import json

from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from rest_framework.views import status

from api.models import User

client = APIClient()


class UserSignUpTest(APITestCase):
    def setUp(self):
        self.users_count_before = User.objects.count()
        self.url = reverse("sign-up")
        self.valid_user = {
            "first_name": "eyo",
            "last_name": "eyo",
            "email": "eyo.eyo@gmail.com",
            "password": "password1*",
        }

        self.wrong_password_user = {
            "first_name": "zhao",
            "last_name": "zhao",
            "email": "Zhao@gmail.com",
            "password": "wrong",
        }

        self.wrong_email_user = {
            "first_name": "zhao",
            "last_name": "zhao",
            "email": "Zhao@gmail",
            "password": "wrong",
        }

        self.invalid_user = {
            "first_name": "",
            "last_name": "",
            "email": "mira.mira@gmail.com",
            "password": "password1*",
        }

    def test_user_signup_with_valid_input(self):
        response = client.post(
            self.url, data=json.dumps(self.valid_user), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), self.users_count_before + 1)
        self.assertEqual(User.objects.get().email, "eyo.eyo@gmail.com")

    def test_user_signup_with_invalid_password(self):
        response = client.post(
            self.url,
            data=json.dumps(self.wrong_password_user),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), self.users_count_before)
        self.assertEqual(
            response.data[0],
            "Password must be at least 8 characters long,it must contain a letter, number and special character",
        )

    def test_user_signup_with_invalid_email(self):
        response = client.post(
            self.url,
            data=json.dumps(self.wrong_email_user),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), self.users_count_before)
        self.assertEqual(response.data[0], "Please enter a valid email address")

    def test_user_signup_with_invalid_user(self):
        response = client.post(
            self.url,
            data=json.dumps(self.invalid_user),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), self.users_count_before)
        self.assertEqual(
            response.data["message"],
            "email, password, firstname and lastname are required",
        )
