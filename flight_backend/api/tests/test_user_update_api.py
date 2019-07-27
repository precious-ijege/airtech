import json

from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from rest_framework.views import status

from api.models import User

client = APIClient()


class UserUpdateProfileTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name="Ghost",
            last_name="Ghost",
            email="ghost@gmail.com",
            password="password1*",
        )
        self.login_details = {"email": "ghost@gmail.com", "password": "password1*"}
        self.response = client.post(
            reverse("log-in"),
            data=json.dumps(self.login_details),
            content_type="application/json",
        )
        self.token = self.response.data["token"]

    def test_authenticated_user_can_update_profile(self):
        url = reverse("update-profile", args=(self.response.data["id"],))
        new_details = {"first_name": "Spirit"}
        response = client.put(
            url,
            data=json.dumps(new_details),
            HTTP_AUTHORIZATION="Token {}".format(self.token),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"],
            "{} has been updated successfully".format(new_details.get("first_name")),
        )

    def test_authenticated_user_cannot_update_another_profile(self):
        new_user = User.objects.create_user(
            first_name="kris",
            last_name="kris",
            email="kris@gmail.com",
            password="password1*",
        )
        url = reverse("update-profile", args=(new_user.id,))
        new_details = {"first_name": "Emi"}
        response = client.put(
            url,
            data=json.dumps(new_details),
            HTTP_AUTHORIZATION="Token {}".format(self.token),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )
