import json

from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from rest_framework.views import status

from api.models import User, Location

client = APIClient()


class LocationApiTest(APITestCase):
    def setUp(self):
        self.url = reverse("location-list")
        self.admin_user = User.objects.create_superuser(
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
        self.new_location = Location.objects.create(
            country="kenya",
            country_code="KNY",
            city="Nairobi",
            latitude=0.000044,
            longitude=0.000125,
        )
        self.location_count_before = Location.objects.count()

    def test_admin_can_create_a_location_object(self):
        new_location = {
            "country": "Nigeria",
            "country_code": "NGA",
            "city": "Lagos",
            "latitude": 0.000011,
            "longitude": 0.000013,
        }
        response = client.post(
            self.url,
            data=json.dumps(new_location),
            HTTP_AUTHORIZATION="Token {}".format(self.token),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), self.location_count_before + 1)
        self.assertIn("country", response.data)
        self.assertIn("country_code", response.data)

    def test_admin_can_get_all_location_objects(self):
        response = client.get(
            self.url, HTTP_AUTHORIZATION="Token {}".format(self.token)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Location.objects.count(), self.location_count_before)

    def test_admin_can_get_a_location_object(self):
        url = reverse("location-detail", args=(self.new_location.id,))
        response = client.get(url, HTTP_AUTHORIZATION="Token {}".format(self.token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("country"), self.new_location.country)

    def test_admin_can_delete_a_location_object(self):
        url = reverse("location-detail", args=(self.new_location.id,))
        response = client.delete(url, HTTP_AUTHORIZATION="Token {}".format(self.token))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_admin_can_update_a_location_object(self):
        url = reverse("location-detail", args=(self.new_location.id,))
        new_city = {"city": "Mombasa"}
        response = client.patch(
            url,
            data=json.dumps(new_city),
            HTTP_AUTHORIZATION="Token {}".format(self.token),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("city"), new_city.get("city"))
